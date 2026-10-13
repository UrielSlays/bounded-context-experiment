"""BUILD A — single-writer durable state store (GREEN STAGE, sqlite3 stdlib).

This module is an additive BUILD-lane sibling of the frozen r13.2 subjects. It never
edits, wraps, or weakens them: the frozen reducers (`mbcx01_r13_state_reference`,
`mbcx01_r13_state_oracle`) and the frozen canonical primitives in `mbcx01_r13_common`
remain the only authority for state semantics, canonical bytes, hashes, and cuts.

CRASH-WINDOW LAW (handoff r13.2 BUILD A requirement 8, net-new — unmodeled in frozen code)
------------------------------------------------------------------------------------------
A transition is `COMMITTED` or it yields NO receipt. There is no partial receipt and no
"probably committed" receipt. The journal carries distinguished terminals, mirroring the
in-repo `CallLedger` `ACCEPTANCE_AMBIGUOUS` precedent:

  COMMITTED  the single write transaction that persists (proposal row, applied-child row,
             poststate snapshot, journal terminal) succeeded and was durably flushed.
             This is the ONLY terminal from which `mbcx01_build_state_adapter` may mint a
             `StateAuthorityReceiptV2`.
  PENDING    the writer recorded intent before the effect (record-before-effect) and the
             process died before the commit fsync returned. Distinguished terminal:
             the transition MAY or MAY NOT have landed; the store refuses to answer and
             refuses to mint. Recovery is an operator action, never an automatic promotion.
  BROKEN     the journal rows for the transaction are internally inconsistent (for example
             a proposal row with no applied-child row, or a poststate snapshot whose hash
             does not equal the recomputed canonical bytes). Never mintable; never silently
             repaired. Reopening a BROKEN transaction id is refused.

Additional laws this module enforces (each has a named witness):

  * one-door verified open: `journal_mode=WAL`, `synchronous=FULL`, schema-version check,
    and store identity (`store_id`, `namespace`, `namespace_version`) verified against the
    persisted `meta` header (plus `application_id` / `user_version`) at open time — not
    asserted by the caller afterwards. Both the foreign-database and the wrong-store
    comparisons happen through the NON-WRITING connection BEFORE the writable one exists,
    so a mistyped path is refused with the file it named byte-identical;
  * writer door, stated for exactly what it is (r3 fold): `_OPEN_WRITERS` refuses a
    second live writer for the same durable target IN THIS PROCESS. It is a registry of
    live objects, not an interprocess lock, and it is not claimed as one — nothing here
    validates a token, and a dictionary entry is not mutual exclusion. Across processes
    the serializer is SQLITE ITSELF: a database file admits one write transaction at a
    time, so the store allocates the journal sequence INSIDE the `BEGIN IMMEDIATE`
    transaction that writes the row (never from a read that precedes it) and `journal.seq`
    carries a UNIQUE index. Two producer processes therefore cannot mint the same journal
    sequence number: the second either serializes behind the first and reads a MAX that
    already includes it, or loses the row to the unique index and is refused by name
    (`STATE_STORE_JOURNAL_SEQ_CONFLICT`);
  * record-before-effect: the intent row (`PENDING`) is durably committed before any
    effect row is written; the effect (proposal row + applied-child row + poststate
    snapshot + `COMMITTED` terminal) then lands in ONE write transaction;
  * durable anti-replay anchors: the five-value anchor set (`ANTI_REPLAY_KEYS`) a
    transition is committed under is written into the journal intent row BEFORE any
    effect row exists, is covered by the terminal classification (anchors that do not
    recompute make the transaction BROKEN, never COMMITTED), and is the only source an
    adapter may mint receipt anchors from or a verifier may check them against;
  * postcommit authority comes from a durable readback through an INDEPENDENTLY IDENTIFIED
    reader connection (a separate `sqlite3.Connection`, opened read-only), never from the
    writer's in-memory object. `reader_identity` must be a distinct, role-bound identity
    from the writer `producer_id`; that comparison is enforced by the adapter/verifier,
    which are the components holding the injected identity configuration.

Durability note (byte-honest): `journal_mode=WAL` is only obtainable for a file-backed
database. An in-memory database answers `PRAGMA journal_mode` with `memory`; the store
records the effective mode and refuses any other value, so a file-backed store that fails
to reach WAL is refused loudly instead of silently downgrading.

In-memory targets (`":memory:"`) are given a private shared-cache URI so that a SEPARATE
reader connection — the independent readback and operator B — can open the same durable
bytes. Every `open_verified(":memory:")` mints a fresh database; nothing is inherited.
Each such store also gets its OWN routing key (`":memory:#<n>"`, `store.path`), because
one shared `":memory:"` entry made the newest in-memory store answer for every older one:
a reader asking for store A's bytes got store B's rows, or was told A's own transaction
was missing. Readers address an in-memory store by that key and by nothing else; the bare
`":memory:"` is not a durable identity and is refused rather than guessed.
"""

from __future__ import annotations

import copy
import itertools
import json
import os
import sqlite3
from typing import Any

import mbcx01_r13_common as common
import mbcx01_r13_state_oracle as oracle
import mbcx01_r13_state_reference as reference


STORE_SCHEMA_VERSION = 2
STORE_JOURNAL_MODE = "WAL"
STORE_SYNCHRONOUS = "FULL"
STORE_APPLICATION_ID = 0x4D42_4341 & 0x7FFFFFFF  # "MBCA" truncated to a positive int32

#: Distinguished journal terminals. Only COMMITTED can mint a production receipt.
TRANSACTION_COMMITTED = "COMMITTED"
TRANSACTION_PENDING = "PENDING"
TRANSACTION_BROKEN = "BROKEN"
TRANSACTION_TERMINALS = (TRANSACTION_COMMITTED, TRANSACTION_PENDING, TRANSACTION_BROKEN)

#: Test-only fault-injection points for the crash-window witnesses. These only ever ABORT
#: a transition (they can never complete one), so they cannot become an activation path.
CRASH_BEFORE_COMMIT = "BEFORE_COMMIT"
CRASH_AFTER_PROPOSAL_ROW = "AFTER_PROPOSAL_ROW"
CRASH_BEFORE_READBACK = "BEFORE_READBACK"
CRASH_POINTS = (CRASH_BEFORE_COMMIT, CRASH_AFTER_PROPOSAL_ROW, CRASH_BEFORE_READBACK)

#: Readback phases. Both are durable reads through the independent reader connection.
PHASE_PRESTATE = "PRESTATE"
PHASE_POSTCOMMIT = "POSTCOMMIT"
PHASES = (PHASE_PRESTATE, PHASE_POSTCOMMIT)

MEMORY_PATH = ":memory:"

#: The private routing key ONE in-memory store is known by (`store.path`). `MEMORY_PATH`
#: itself is never a routing key: a single `":memory:"` entry is a singleton that the next
#: `open_verified(":memory:")` overwrites, which routed an independent reader for one live
#: store at another live store's bytes.
MEMORY_ROUTE_KEY_FORMAT = MEMORY_PATH + "#%d"

#: The name ONE in-memory database is addressed by inside its shared-cache URI. Minted by
#: this module from a counter, so it can never carry a caller's characters.
MEMORY_DATABASE_NAME_FORMAT = "mbcx01-build-state-%d"

_MEMORY_SEQUENCE = itertools.count(1)
#: in-memory routing key -> live shared-cache URI (the durable target an independent reader
#: opens). One entry per LIVE in-memory store, published only after that store opens clean
#: and removed when it closes.
_MEMORY_TARGETS: dict[str, str] = {}
#: durable target -> live writer store (the single-writer gate).
_OPEN_WRITERS: dict[str, "SingleWriterStateStore"] = {}
#: (store_id, namespace, namespace_version) -> live store (verifier resolution).
#: SINGLE OCCUPANCY (r4 fold): a receipt names a store by identity and never by path, so
#: this slot must resolve to one store. A second store claiming a live identity is refused
#: by name rather than quietly replacing the entry; the slot frees when that store closes.
_STORES_BY_IDENTITY: dict[tuple[str, str, int], "SingleWriterStateStore"] = {}

_SCHEMA = (
    "CREATE TABLE IF NOT EXISTS meta ("
    " key TEXT PRIMARY KEY, value TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS journal ("
    " transaction_commit_id TEXT PRIMARY KEY,"
    " seq INTEGER NOT NULL,"
    " status TEXT NOT NULL,"
    " prestate_utf8 TEXT NOT NULL,"
    " prestate_hash TEXT NOT NULL,"
    " anti_replay_utf8 TEXT NOT NULL,"
    " anti_replay_hash TEXT NOT NULL)",
    # r3 fold: the DATABASE owns the uniqueness of its own ordering fact. A unique index
    # (rather than a column constraint) is used deliberately: it also applies to a store
    # file an earlier build created, and it converts any residual duplicate-sequence race
    # into a named refusal instead of a silent second row wearing a taken number.
    "CREATE UNIQUE INDEX IF NOT EXISTS journal_seq_unique ON journal (seq)",
    "CREATE TABLE IF NOT EXISTS proposals ("
    " transaction_commit_id TEXT PRIMARY KEY,"
    " persistence_identity TEXT NOT NULL,"
    " event_id TEXT NOT NULL,"
    " event_utf8 TEXT NOT NULL,"
    " event_hash TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS children ("
    " transaction_commit_id TEXT PRIMARY KEY,"
    " event_id TEXT NOT NULL,"
    " event_utf8 TEXT NOT NULL,"
    " event_hash TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS snapshots ("
    " transaction_commit_id TEXT PRIMARY KEY,"
    " state_utf8 TEXT NOT NULL,"
    " state_hash TEXT NOT NULL,"
    " next_sequence INTEGER NOT NULL)",
)

#: The tables a store the verifier is allowed to ANSWER FROM must actually have.
#: Read at the read-only door (`ReadOnlyStateStoreView.open_verified_readonly`) because a
#: file can carry every IDENTITY signal — `meta` rows, `application_id`, `user_version` —
#: and still not carry the rows a question is asked of (codex-CLI r9 F2: a truncated store
#: made `SELECT * FROM journal` raise a raw `sqlite3.OperationalError` out of the public
#: verifier). Order is the order a reader meets them.
STORE_REQUIRED_TABLES = ("meta", "journal", "proposals", "children", "snapshots")

_REQUEST_KEYS = {"transaction_commit_id", "prestate", "proposal_event", "applied_child_event"}

#: FOLD 1 — the DURABLE anti-replay anchor set. These five values are written into
#: the journal intent row at commit time (record-before-effect), covered by the
#: terminal classification, and are the ONLY source an adapter may mint them from or
#: a verifier may check a receipt against. They are opaque semantic identifiers: the
#: store deliberately does NOT require `SCOPE.x -> SCENARIO.x`, `SUBJECT.x -> RUN.x`
#: or `TXN.x -> NONCE.x` label transforms, because a real production run names its
#: scenario, run and nonce independently — and because a value anybody can derive
#: from a label is not evidence of anything.
ANTI_REPLAY_KEYS = {"receipt_nonce", "scope_id", "scenario_id", "run_id",
                    "subject_identity"}


class StateStoreError(ValueError):
    """Closed, fail-loud store error. Never raised to signal a successful commit."""


def read_id(transaction_commit_id: str, phase: str) -> str:
    """Deterministic durable read identity (same construction as the frozen fixture path)."""
    return "READ." + common.sha256([transaction_commit_id, phase])


def persistence_row_identity(transaction_commit_id: str, event_id: str) -> str:
    """Journal row identity for a persisted proposal event."""
    return "ROW." + common.sha256([transaction_commit_id, event_id])


def anti_replay_shape_errors(anti_replay: Any) -> list[str]:
    """Closed-shape check for a durable anti-replay anchor set (no label transforms)."""
    if not isinstance(anti_replay, dict) or set(anti_replay) != ANTI_REPLAY_KEYS:
        return ["STATE_STORE_ANTI_REPLAY_SHAPE_INVALID"]
    if any(common.SEMANTIC_ID.fullmatch(anti_replay[key] or "") is None
           if isinstance(anti_replay[key], str) else True
           for key in sorted(ANTI_REPLAY_KEYS)):
        return ["STATE_STORE_ANTI_REPLAY_SHAPE_INVALID"]
    return []


def decoded_anti_replay(anti_replay_utf8: Any, anti_replay_hash: Any,
                        transaction_commit_id: str) -> dict[str, Any]:
    """Decode + re-verify the durable anchor bytes of one journal row, or refuse."""
    try:
        anchors = json.loads(anti_replay_utf8)
    except (TypeError, ValueError) as exc:
        raise StateStoreError(
            "STATE_STORE_ANTI_REPLAY_CORRUPT:%s" % transaction_commit_id) from exc
    if (anti_replay_shape_errors(anchors)
            or common.canonical_json(anchors).decode("utf-8") != anti_replay_utf8
            or anti_replay_hash != common.sha384(anti_replay_utf8.encode("utf-8"))):
        raise StateStoreError(
            "STATE_STORE_ANTI_REPLAY_CORRUPT:%s" % transaction_commit_id)
    return anchors


#: THE URI PATH ESCAPES, and the ORDER IS PART OF THE RULE (codex-CLI r8 P1).
#: sqlite.org/uri.html §3.1 "The URI Path" gives the conversion from an ordinary
#: filename to a URI verbatim:
#:
#:   "1. Convert all "?" characters into "%3f".
#:    2. Convert all "#" characters into "%23".
#:    3. On windows only, convert all "\" characters into "/".
#:    4. Convert all sequences of two or more "/" characters into a single "/" character.
#:    5. On windows only, if the filename begins with a drive letter, prepend a single "/"
#:       character.
#:    6. Prepend the "file:" scheme."
#:
#: `%` IS THE THIRD MEMBER OF THE SET AND THE DOC DOES NOT LIST IT, because §3
#: "URI Format" makes it structural rather than optional: "Zero or more escape
#: sequences of the form "%HH" (where H represents any hexadecimal digit) can
#: occur in the path, query string, or fragment." A filename that literally
#: contains `%23` is therefore READ AS `#` unless the `%` is itself escaped, and
#: `%23` is a perfectly legal Windows filename. So `%` -> `%25` runs FIRST; doing
#: it after `#` -> `%23` would re-escape the escapes this function just wrote.
_URI_PATH_ESCAPES = (("%", "%25"), ("#", "%23"), ("?", "%3f"))

#: Steps 4 and 5 are DELIBERATELY NOT APPLIED, each for a stated reason:
#:   * step 4 (collapse runs of "/") is a no-op on any path `os.path.abspath`
#:     returns EXCEPT a UNC path, where `//server/share/...` would collapse to
#:     `/server/share/...` and silently name a different thing. A UNC path is
#:     refused loudly by sqlite itself ("invalid uri authority: <server>",
#:     measured on sqlite 3.45.1) both before and after this fold, so nothing
#:     here turns a loud refusal into a wrong file;
#:   * step 5 (prepend "/" before a drive letter) makes no difference to
#:     sqlite's own parser: `file:C:/dir/db` and `file:/C:/dir/db` were measured
#:     to open the SAME file, in both the writable and the `?mode=ro` form. It is
#:     not applied so that the URI a store reports is the one it has always
#:     reported, and no wrong number is available either way.


def _percent_encode_uri_path(text: str) -> str:
    """Escape the three characters sqlite's URI parser reads as SYNTAX."""
    for character, escape in _URI_PATH_ESCAPES:
        text = text.replace(character, escape)
    return text


def sqlite_file_uri(path: str) -> str:
    """The `file:` URI that addresses EXACTLY the filesystem path it was handed.

    THE ONE ENCODING SITE (codex-CLI r8 P1). Before this fold three URIs were
    built by string concatenation, and sqlite parsed the caller's own filename as
    URI syntax: a store requested at `<dir>\\a#b.sqlite` OPENED `<dir>\\a`, so
    `refuse_foreign_database()` inspected the REQUESTED path while the connection
    addressed a DIFFERENT file — a foreign database admitted behind a green
    identity check, and (because the `?mode=ro` fell inside the discarded
    fragment) admitted through a connection that was not read-only either. All of
    it measured, not inferred; `#` and `%` are both legal Windows filename
    characters, `?` is not (it is escaped anyway, because this module is portable
    Python and a POSIX host allows it).
    """
    return "file:" + _percent_encode_uri_path(
        os.path.abspath(path).replace("\\", "/"))


def sqlite_memory_uri(sequence: int) -> str:
    """The shared-cache URI for ONE freshly minted private in-memory database.

    Routed through the SAME escape as the file URIs even though the name is a
    module-owned literal (`MEMORY_DATABASE_NAME_FORMAT` and an integer, which
    cannot contain `%`, `#` or `?`): one encoder, no second place for the rule to
    drift to. `mode=memory&cache=shared` is the query, not the name.
    """
    return ("file:" + _percent_encode_uri_path(MEMORY_DATABASE_NAME_FORMAT % sequence)
            + "?mode=memory&cache=shared")


def readonly_connection_uri(path: Any) -> str:
    """Return the URI an INDEPENDENT reader uses to open `path`'s durable bytes read-only.

    File targets get `mode=ro`. In-memory targets must keep `mode=memory&cache=shared`
    (sqlite has no `mode=ro` for a shared-cache memory database), so the caller additionally
    sets `PRAGMA query_only=ON`; `_open_readonly` does both.

    An in-memory store is addressed by its OWN routing key (`store.path`,
    `MEMORY_ROUTE_KEY_FORMAT`). The bare `":memory:"` names no store, and a routing key
    whose store has closed names no store any more: both are refused loudly, because
    answering them with whichever in-memory database happens to be live is a cross-store
    read wearing the caller's own question.
    """
    if isinstance(path, str) and path in _MEMORY_TARGETS:
        return _MEMORY_TARGETS[path]
    if not isinstance(path, str) or path.startswith(MEMORY_PATH):
        raise StateStoreError("STATE_STORE_TARGET_UNRESOLVED")
    return sqlite_file_uri(path) + "?mode=ro"


def open_readonly_connection(path: Any) -> sqlite3.Connection:
    """Open a SEPARATE read-only connection object on `path` (never the writer's object)."""
    uri = readonly_connection_uri(path)
    connection = sqlite3.connect(uri, uri=True, isolation_level=None)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only=ON")
    return connection


def pre_existing_identity_signals(path: str) -> tuple[list[str], int, int]:
    """Read a pre-existing file's sqlite identity signals WITHOUT writing to it.

    The connection is `mode=ro` plus `PRAGMA query_only=ON` — the same non-writing door
    `ReadOnlyStateStoreView` uses — so asking "whose database is this?" cannot itself
    modify the answer. A file that is not a database at all raises `sqlite3.DatabaseError`
    here exactly as it did before this fold: an unreadable file is neither refused as
    foreign (nothing was read) nor adopted as fresh, and its bytes are left alone.
    """
    connection = sqlite3.connect(readonly_connection_uri(path), uri=True,
                                 isolation_level=None)
    try:
        connection.execute("PRAGMA query_only=ON")
        objects = [row[0] for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type IN ('table', 'view')"
            " AND name NOT LIKE 'sqlite_%' ORDER BY name")]
        application_id = int(connection.execute("PRAGMA application_id").fetchone()[0])
        user_version = int(connection.execute("PRAGMA user_version").fetchone()[0])
    finally:
        connection.close()
    return objects, application_id, user_version


def refuse_foreign_database(path: Any) -> None:
    """Refuse a path that already holds somebody else's database, WITHOUT touching it.

    r4 fold (FOLD-2A). Two defects this closes, both of them honest-mistake defects rather
    than anything adversarial — a mistyped or stale path in an operator's configuration:

      * the r3 fold read the identity signals before the store DDL, but AFTER
        `PRAGMA journal_mode=WAL`. WAL is a PERSISTENT database property written into the
        header, so `STATE_STORE_FOREIGN_DATABASE` was raised only once this store had
        already rewritten another application's file. Every signal is now read before the
        writer connection exists at all;
      * `user_version` was not a signal. A tableless database whose only mark was a
        nonzero `user_version` therefore passed the check, was initialized, and was
        ADOPTED — and the tell was destroyed by the adoption itself, because schema
        initialization overwrites `user_version`. It is a signal now.

    A path with no file, a zero-length file, and an unmarked empty database are all a
    FRESH store and are accepted: refusing right paths is not a repair.
    """
    if not isinstance(path, str) or not os.path.isfile(path):
        return
    objects, application_id, user_version = pre_existing_identity_signals(path)
    if ((objects or application_id or user_version)
            and application_id != STORE_APPLICATION_ID):
        raise StateStoreError("STATE_STORE_FOREIGN_DATABASE")


def pre_existing_store_header(path: str) -> dict[str, str] | None:
    """Read a pre-existing file's PERSISTED STORE HEADER without writing to it.

    The BA-19 non-writing door (`mode=ro` + `PRAGMA query_only=ON`), extended from the
    sqlite-level identity signals to the store's OWN identity rows. `None` means the file
    carries no `meta` table at all, which is a different fact from "the header disagrees"
    and is reported as one; an empty dict means the table exists and is empty.
    """
    connection = sqlite3.connect(readonly_connection_uri(path), uri=True,
                                 isolation_level=None)
    try:
        connection.execute("PRAGMA query_only=ON")
        if connection.execute(
                "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'meta'"
        ).fetchone() is None:
            return None
        return {row[0]: row[1] for row in connection.execute("SELECT key, value FROM meta")}
    finally:
        connection.close()


def expected_store_header(store_id: str, namespace: str,
                          namespace_version: int) -> dict[str, str]:
    """The persisted header ONE store identity must carry. One spelling, one place."""
    return {
        "store_id": store_id,
        "namespace": namespace,
        "namespace_version": str(namespace_version),
        "schema_version": str(STORE_SCHEMA_VERSION),
    }


def refuse_mismatched_pre_existing_store(path: Any, *, store_id: str, namespace: str,
                                         namespace_version: int) -> None:
    """Refuse a path holding ANOTHER MBCX store, WITHOUT touching it (codex-CLI r9 F1).

    `refuse_foreign_database` closes the case where the file belongs to somebody else
    (`application_id != STORE_APPLICATION_ID`). It cannot see the case that actually
    happens to an operator with two stores: a mistyped or stale path that names ANOTHER
    STORE OF THIS APPLICATION — same `application_id`, different `store_id` / `namespace`
    / `namespace_version`, or an older `schema_version`. `open_verified` DID refuse that
    (`STATE_STORE_IDENTITY_MISMATCH`), but only after `PRAGMA journal_mode=WAL` had
    rewritten the header of the other store's file and after `_SCHEMA` had executed over
    it — a store mutated by the very open that then rejected it. It also adopted a
    HEADERLESS database of this application (rows present, `meta` empty or absent) by
    stamping this caller's identity into it, which is the same defect `refuse_foreign_
    database` closed one application over: the tell is destroyed by the adoption.

    So the persisted identity is compared through the NON-WRITING connection BEFORE any
    writable open. Only a path that is absent, empty, or ALREADY THIS EXACT IDENTITY goes
    on to the writable DDL. The post-DDL header and version checks in `open_verified`
    stay exactly as they were: they are what the in-memory arm (nothing pre-existing to
    inspect) and a freshly stamped file are checked by, and a check that moved would be a
    check that could drift.

    A file that is not a database at all raises `sqlite3.DatabaseError` here, unchanged
    and uncaught, exactly as `pre_existing_identity_signals` already did: an unreadable
    file is neither refused as a mismatch (nothing was read) nor adopted as fresh.
    """
    if not isinstance(path, str) or not os.path.isfile(path):
        return
    objects, application_id, user_version = pre_existing_identity_signals(path)
    if not objects and not application_id and not user_version:
        return  # an unmarked, empty database: a FRESH store, accepted as before.
    if application_id != STORE_APPLICATION_ID:
        return  # somebody else's database: `refuse_foreign_database` owns that answer.
    if user_version != STORE_SCHEMA_VERSION:
        raise StateStoreError("STATE_STORE_SCHEMA_VERSION_MISMATCH")
    header = pre_existing_store_header(path)
    if header != expected_store_header(store_id, namespace, namespace_version):
        # Includes the headerless shape (`None` / `{}` beside existing rows): a store
        # whose durable identity is absent is not this store, and is never adopted.
        raise StateStoreError("STATE_STORE_IDENTITY_MISMATCH")


def registered_store(store_id: str, namespace: str,
                     namespace_version: int) -> "SingleWriterStateStore | None":
    """Resolve the live durable store bound to one store identity, or `None`."""
    return _STORES_BY_IDENTITY.get((store_id, namespace, namespace_version))


def transaction_terminal(store_id: str, namespace: str, namespace_version: int,
                         transaction_commit_id: str) -> str | None:
    """Return the durable terminal for one transaction, or `None` when unknown.

    `None` means "this durable store has never heard of that transaction id" — which is a
    transaction IDENTITY failure, not a commit failure. An unresolvable store is also
    `None`: absence of durable evidence is never an argument for admission.
    """
    store = registered_store(store_id, namespace, namespace_version)
    if store is None:
        return None
    rows = store.journal_rows(transaction_commit_id)
    if not rows:
        return None
    return rows[0]["status"]


class SingleWriterStateStore:
    """Durable single-writer state store behind the production state-owner adapter."""

    def __init__(self, connection: sqlite3.Connection, *, target: str, path: str,
                 store_id: str, namespace: str, namespace_version: int,
                 journal_mode: str) -> None:
        self._connection = connection
        self._target = target
        self.path = path
        self.store_id = store_id
        self.namespace = namespace
        self.namespace_version = namespace_version
        self.journal_mode = journal_mode
        self.closed = False

    # ---- one door ---------------------------------------------------------------

    @classmethod
    def open_verified(cls, path: Any, *, store_id: str, namespace: str,
                      namespace_version: int) -> "SingleWriterStateStore":
        """Open the one door: WAL + synchronous=FULL + schema version + store identity.

        The identity is VERIFIED against the persisted store header; a caller-supplied
        label can never define the store identity that a receipt binds. Any mismatch is a
        loud `StateStoreError`, never a silent re-label.

        Three things this door does NOT do, said plainly because the code does not do them:

          * it does not create or migrate a store on top of a database that is already
            somebody else's. Pre-existing user objects, a foreign `application_id` and a
            foreign `user_version` are inspected through a NON-WRITING connection BEFORE
            this store's first PRAGMA and refused (`STATE_STORE_FOREIGN_DATABASE`), so a
            mistaken path is refused with the other database untouched. The same door
            settles the case one application over (codex-CLI r9 F1): a path holding
            ANOTHER MBCX STORE — same `application_id`, different persisted identity or
            schema version, or no header at all — is refused
            (`STATE_STORE_IDENTITY_MISMATCH` / `STATE_STORE_SCHEMA_VERSION_MISMATCH`)
            with that store's bytes byte-identical, instead of after `journal_mode=WAL`
            and `_SCHEMA` had already rewritten it;
          * it does not let a second store take a LIVE store identity. The identity is
            how a receipt reaches durable evidence, so it resolves to one store or the
            open is refused (`STATE_STORE_IDENTITY_ALREADY_OPEN`). A CLOSED identity is
            free again; this is not a permanent claim on a name;
          * it does not take an interprocess lock. `STATE_STORE_WRITER_ALREADY_OPEN`
            refuses a second live writer OBJECT in THIS process and says nothing about
            any other process. What keeps two producer processes from minting the same
            journal sequence number is not this door: it is sqlite's own one-writer-at-a-
            time write transaction, inside which `commit_transition` allocates the
            sequence, plus the `journal_seq_unique` index behind it.
        """
        if (common.SEMANTIC_ID.fullmatch(store_id or "") is None
                or common.SEMANTIC_ID.fullmatch(namespace or "") is None
                or not isinstance(namespace_version, int)
                or isinstance(namespace_version, bool) or namespace_version < 1):
            raise StateStoreError("STATE_STORE_IDENTITY_INVALID")
        if path == MEMORY_PATH:
            # One routing key per in-memory store, minted here and published below only
            # if this open succeeds. Two live in-memory stores never share an entry.
            sequence = next(_MEMORY_SEQUENCE)
            logical_path = MEMORY_ROUTE_KEY_FORMAT % sequence
            target = sqlite_memory_uri(sequence)
        elif isinstance(path, str) and path and not path.startswith(MEMORY_PATH):
            logical_path = path
            target = sqlite_file_uri(path)
        else:
            raise StateStoreError("STATE_STORE_PATH_INVALID")

        live = _OPEN_WRITERS.get(target)
        if live is not None and not live.closed:
            raise StateStoreError("STATE_STORE_WRITER_ALREADY_OPEN")

        # ONE LIVE STORE PER STORE IDENTITY (r4 fold, FOLD-2B). `_STORES_BY_IDENTITY` is
        # how a receipt reaches durable evidence: it carries store IDENTITY and never a
        # path, deliberately, so that a receipt cannot point a verifier at a store its own
        # holder chose. That makes the identity a single-occupancy slot. Assigning it
        # unconditionally meant a second store opened on a DIFFERENT path silently
        # displaced a live one, and from that moment a true receipt of the first store's
        # COMMITTED transaction resolved against the second store — where the transaction
        # does not exist — and was refused; closing the second store then removed
        # resolution altogether, because `close()` only deletes the entry it still owns.
        # The refusal is checked BEFORE the connection is opened, so a refused open also
        # leaves no half-made database file behind.
        bound = _STORES_BY_IDENTITY.get((store_id, namespace, namespace_version))
        if bound is not None and not bound.closed:
            raise StateStoreError("STATE_STORE_IDENTITY_ALREADY_OPEN")

        # IDENTITY BEFORE ANY BYTE IS WRITTEN (r4 fold, FOLD-2A). See
        # `refuse_foreign_database`: every identity signal is read through a NON-WRITING
        # connection before this store's first PRAGMA, so a mistaken path that names an
        # unrelated database is refused with that database untouched. In-memory targets
        # are freshly minted private databases (`MEMORY_ROUTE_KEY_FORMAT`), so there is
        # nothing pre-existing to inspect.
        if path != MEMORY_PATH:
            refuse_foreign_database(path)
            # ...and the same door now also answers "is this ANOTHER STORE OF MINE?"
            # (codex-CLI r9 F1). Identity is a store-level fact, not only an
            # application-level one, and it has to be settled before the first PRAGMA.
            refuse_mismatched_pre_existing_store(
                path, store_id=store_id, namespace=namespace,
                namespace_version=namespace_version)

        connection = sqlite3.connect(target, uri=True, isolation_level=None)
        connection.row_factory = sqlite3.Row
        journal_mode = str(connection.execute(
            "PRAGMA journal_mode=%s" % STORE_JOURNAL_MODE).fetchone()[0]).upper()
        expected_modes = {STORE_JOURNAL_MODE} if path != MEMORY_PATH else {"MEMORY"}
        if journal_mode not in expected_modes:
            connection.close()
            raise StateStoreError("STATE_STORE_JOURNAL_MODE_REFUSED:" + journal_mode)
        connection.execute("PRAGMA synchronous=%s" % STORE_SYNCHRONOUS)
        synchronous = int(connection.execute("PRAGMA synchronous").fetchone()[0])
        if synchronous != 2:  # 2 == FULL
            connection.close()
            raise StateStoreError("STATE_STORE_SYNCHRONOUS_REFUSED:%d" % synchronous)
        connection.execute("PRAGMA foreign_keys=ON")

        # IDENTITY BEFORE DDL (r3 fold) now happens BEFORE THIS CONNECTION EXISTS (r4
        # fold): the r3 check lived here, after `PRAGMA journal_mode=WAL` had already
        # rewritten the header of whatever database the path named. It is one check in
        # one place — `refuse_foreign_database`, called above — rather than two that can
        # drift apart. A genuinely empty file initializes and gets stamped, exactly as
        # before.
        try:
            for statement in _SCHEMA:
                connection.execute(statement)
        except sqlite3.DatabaseError as exc:
            # Durable rows that cannot carry the store's own invariants — for example a
            # store file holding duplicate journal sequence numbers, which the unique
            # index refuses to build over — are a loud refusal, never a store that is
            # opened anyway and answered from.
            connection.close()
            raise StateStoreError(
                "STATE_STORE_SCHEMA_REFUSED:%s" % type(exc).__name__) from exc

        header = {row["key"]: row["value"]
                  for row in connection.execute("SELECT key, value FROM meta")}
        expected = expected_store_header(store_id, namespace, namespace_version)
        if not header:
            connection.execute("BEGIN IMMEDIATE")
            connection.executemany("INSERT INTO meta (key, value) VALUES (?, ?)",
                                   sorted(expected.items()))
            connection.execute("PRAGMA application_id=%d" % STORE_APPLICATION_ID)
            connection.execute("PRAGMA user_version=%d" % STORE_SCHEMA_VERSION)
            connection.execute("COMMIT")
            header = dict(expected)
        if header != expected:
            connection.close()
            raise StateStoreError("STATE_STORE_IDENTITY_MISMATCH")
        application_id = int(connection.execute("PRAGMA application_id").fetchone()[0])
        user_version = int(connection.execute("PRAGMA user_version").fetchone()[0])
        if application_id != STORE_APPLICATION_ID or user_version != STORE_SCHEMA_VERSION:
            connection.close()
            raise StateStoreError("STATE_STORE_SCHEMA_VERSION_MISMATCH")

        store = cls(connection, target=target, path=logical_path,
                    store_id=store_id, namespace=namespace,
                    namespace_version=namespace_version, journal_mode=journal_mode)
        _OPEN_WRITERS[target] = store
        _STORES_BY_IDENTITY[(store_id, namespace, namespace_version)] = store
        if path == MEMORY_PATH:
            # Published only now, so a REFUSED open leaves no routable in-memory key.
            _MEMORY_TARGETS[logical_path] = target
        return store

    def close(self) -> None:
        """Release the write door. A closed store answers nothing and mints nothing."""
        if self.closed:
            return
        self.closed = True
        self._connection.close()
        if _OPEN_WRITERS.get(self._target) is self:
            del _OPEN_WRITERS[self._target]
        key = (self.store_id, self.namespace, self.namespace_version)
        if _STORES_BY_IDENTITY.get(key) is self:
            del _STORES_BY_IDENTITY[key]
        if _MEMORY_TARGETS.get(self.path) == self._target:
            del _MEMORY_TARGETS[self.path]

    @property
    def store_identity(self) -> dict[str, Any]:
        return {"store_id": self.store_id, "namespace": self.namespace,
                "namespace_version": self.namespace_version}

    # ---- durable write path ------------------------------------------------------

    def commit_transition(self, transition_request: Any, *, anti_replay: Any,
                          crash_point: str | None = None) -> dict[str, Any]:
        """Persist proposal + applied child + poststate in ONE write transaction.

        Returns the COMMITTED journal terminal record, or raises `StateStoreError` with a
        distinguished terminal (`PENDING` / `BROKEN`) that cannot mint a receipt.
        `crash_point` is test-only fault injection (see `CRASH_POINTS`); it can only abort.

        `anti_replay` (REQUIRED, `ANTI_REPLAY_KEYS`) is the anchor set this transition is
        committed under. It is durable BEFORE any effect row exists, so an adapter mints
        the receipt's anchors from a fact the writer had to commit to, and a verifier can
        refuse anchors that merely agree with the receipt's own labels. There is no
        default: a transition with no durable anchor set cannot be committed at all.
        """
        self._require_open()
        if crash_point is not None and crash_point not in CRASH_POINTS:
            raise StateStoreError("STATE_STORE_CRASH_POINT_INVALID")
        transaction_commit_id, prestate, proposal, child = self._validated_request(
            transition_request)
        anti_replay_utf8 = self._validated_anti_replay(anti_replay)

        if self.journal_rows(transaction_commit_id):
            raise StateStoreError("STATE_STORE_TRANSACTION_ALREADY_RECORDED")

        prestate_utf8 = common.canonical_json(prestate).decode("utf-8")
        proposal_utf8 = common.canonical_json(proposal).decode("utf-8")
        child_utf8 = common.canonical_json(child).decode("utf-8")

        # Record-before-effect: the intent row is durable before any effect row exists.
        #
        # r3 fold — SEQUENCE ALLOCATION IS PART OF THE WRITE. `MAX(seq) + 1` used to be
        # read before the transaction opened, so two producers (in this process or in two
        # processes, which `_OPEN_WRITERS` cannot see) could both read the same MAX and
        # both write it. `BEGIN IMMEDIATE` takes sqlite's write lock for this database
        # FIRST, and sqlite admits one write transaction at a time, so the MAX read below
        # already includes any row a writer that went before us committed.
        self._connection.execute("BEGIN IMMEDIATE")
        try:
            seq = int(self._connection.execute(
                "SELECT COALESCE(MAX(seq), 0) + 1 FROM journal").fetchone()[0])
            self._connection.execute(
                "INSERT INTO journal (transaction_commit_id, seq, status, prestate_utf8,"
                " prestate_hash, anti_replay_utf8, anti_replay_hash)"
                " VALUES (?, ?, ?, ?, ?, ?, ?)",
                (transaction_commit_id, seq, TRANSACTION_PENDING, prestate_utf8,
                 common.sha384(prestate_utf8.encode("utf-8")), anti_replay_utf8,
                 common.sha384(anti_replay_utf8.encode("utf-8"))))
            self._connection.execute("COMMIT")
        except sqlite3.IntegrityError as exc:
            # The durable constraints are the last word, and they are read back from the
            # database rather than guessed from the driver's message: a transaction id
            # another writer already recorded, or a sequence number already taken, loses
            # its row and is told so by name.
            self._connection.execute("ROLLBACK")
            if self._connection.execute(
                    "SELECT 1 FROM journal WHERE transaction_commit_id = ?",
                    (transaction_commit_id,)).fetchone() is not None:
                raise StateStoreError(
                    "STATE_STORE_TRANSACTION_ALREADY_RECORDED") from exc
            raise StateStoreError(
                "STATE_STORE_JOURNAL_SEQ_CONFLICT:%s" % transaction_commit_id) from exc

        if crash_point == CRASH_BEFORE_COMMIT:
            # The commit fsync never returned: the transition MAY or MAY NOT have landed.
            raise StateStoreError(
                "STATE_STORE_TRANSACTION_%s:%s" % (TRANSACTION_PENDING, transaction_commit_id))

        # Both FROZEN reducers must agree that this exact child applies to this exact
        # prestate before any effect row is written. The store never picks a winner.
        poststate = self._replayed_poststate(prestate, proposal, child)

        poststate_utf8 = common.canonical_json(poststate).decode("utf-8")
        self._connection.execute("BEGIN IMMEDIATE")
        self._connection.execute(
            "INSERT INTO proposals (transaction_commit_id, persistence_identity, event_id,"
            " event_utf8, event_hash) VALUES (?, ?, ?, ?, ?)",
            (transaction_commit_id,
             persistence_row_identity(transaction_commit_id, proposal["event_id"]),
             proposal["event_id"], proposal_utf8,
             common.sha384(proposal_utf8.encode("utf-8"))))
        if crash_point == CRASH_AFTER_PROPOSAL_ROW:
            # Durable partial effect: a proposal row with no applied-child row and no
            # poststate snapshot. The consistency classifier (the same one recovery runs)
            # records the BROKEN terminal; it is never silently repaired or promoted.
            self._connection.execute("COMMIT")
            self._record_terminal(transaction_commit_id, self._classify(transaction_commit_id))
            raise StateStoreError(
                "STATE_STORE_TRANSACTION_%s:%s" % (TRANSACTION_BROKEN, transaction_commit_id))
        self._connection.execute(
            "INSERT INTO children (transaction_commit_id, event_id, event_utf8, event_hash)"
            " VALUES (?, ?, ?, ?)",
            (transaction_commit_id, child["event_id"], child_utf8,
             common.sha384(child_utf8.encode("utf-8"))))
        self._connection.execute(
            "INSERT INTO snapshots (transaction_commit_id, state_utf8, state_hash,"
            " next_sequence) VALUES (?, ?, ?, ?)",
            (transaction_commit_id, poststate_utf8,
             common.sha384(poststate_utf8.encode("utf-8")), int(poststate["next_seq"])))
        self._connection.execute(
            "UPDATE journal SET status = ? WHERE transaction_commit_id = ?",
            (TRANSACTION_COMMITTED, transaction_commit_id))
        self._connection.execute("COMMIT")

        terminal = self._classify(transaction_commit_id)
        if terminal != TRANSACTION_COMMITTED:
            self._record_terminal(transaction_commit_id, terminal)
            raise StateStoreError(
                "STATE_STORE_TRANSACTION_%s:%s" % (terminal, transaction_commit_id))
        if crash_point == CRASH_BEFORE_READBACK:
            # The terminal is durable, but this writer died before the durable readback:
            # no receipt may be minted from this CALL; the terminal itself stays honest.
            raise StateStoreError(
                "STATE_STORE_READBACK_MISSING:%s" % transaction_commit_id)
        return self.journal_rows(transaction_commit_id)[0]

    # ---- durable read path -------------------------------------------------------

    def independent_readback(self, transaction_commit_id: str, *, reader_identity: str,
                             phase: str = PHASE_POSTCOMMIT) -> dict[str, Any]:
        """Read state back through an independently identified reader CONNECTION.

        The reader is a separate `sqlite3.Connection` object opened read-only on the same
        durable target — never the writer's connection object and never the writer's
        in-memory poststate. `reader_identity` is carried into the evidence so the receipt
        verifier can refuse a writer-owned readback (`reader_identity == producer_id`),
        which is a masquerade this store cannot detect on its own (it holds no producer
        identity by construction: `open_verified` takes store identity only).
        """
        self._require_open()
        if common.SEMANTIC_ID.fullmatch(reader_identity or "") is None:
            raise StateStoreError("STATE_STORE_READER_IDENTITY_INVALID")
        if phase not in PHASES:
            raise StateStoreError("STATE_STORE_PHASE_INVALID")
        rows = self.journal_rows(transaction_commit_id)
        if not rows:
            raise StateStoreError(
                "STATE_STORE_TRANSACTION_UNKNOWN:%s" % transaction_commit_id)
        if rows[0]["status"] != TRANSACTION_COMMITTED:
            raise StateStoreError("STATE_STORE_TRANSACTION_%s:%s"
                                  % (rows[0]["status"], transaction_commit_id))
        connection = open_readonly_connection(self.path or self._target)
        try:
            if phase == PHASE_PRESTATE:
                row = connection.execute(
                    "SELECT prestate_utf8 AS state_utf8, prestate_hash AS state_hash"
                    " FROM journal WHERE transaction_commit_id = ?",
                    (transaction_commit_id,)).fetchone()
            else:
                row = connection.execute(
                    "SELECT state_utf8, state_hash FROM snapshots"
                    " WHERE transaction_commit_id = ?",
                    (transaction_commit_id,)).fetchone()
        finally:
            connection.close()
        if row is None:
            raise StateStoreError("STATE_STORE_READBACK_MISSING:%s" % transaction_commit_id)
        state_utf8 = row["state_utf8"]
        state = json.loads(state_utf8)
        if (common.canonical_json(state).decode("utf-8") != state_utf8
                or row["state_hash"] != common.sha384(state_utf8.encode("utf-8"))):
            raise StateStoreError("STATE_STORE_SNAPSHOT_CORRUPT:%s" % transaction_commit_id)
        return {
            "read_id": read_id(transaction_commit_id, phase),
            "state_utf8": state_utf8,
            "state_hash": row["state_hash"],
            "cut": common.current_cut(state),
            "reader_identity": reader_identity,
        }

    def transaction_rows(self, transaction_commit_id: str) -> dict[str, Any]:
        """Return the durable proposal / child / snapshot rows for one COMMITTED terminal."""
        self._require_open()
        rows = self.journal_rows(transaction_commit_id)
        if not rows:
            raise StateStoreError(
                "STATE_STORE_TRANSACTION_UNKNOWN:%s" % transaction_commit_id)
        if rows[0]["status"] != TRANSACTION_COMMITTED:
            raise StateStoreError("STATE_STORE_TRANSACTION_%s:%s"
                                  % (rows[0]["status"], transaction_commit_id))
        record: dict[str, Any] = {"journal": rows[0]}
        for table in ("proposals", "children", "snapshots"):
            row = self._connection.execute(
                "SELECT * FROM %s WHERE transaction_commit_id = ?" % table,
                (transaction_commit_id,)).fetchone()
            if row is None:
                raise StateStoreError("STATE_STORE_ROW_MISSING:%s" % table)
            record[table] = dict(row)
        return record

    def anti_replay_anchors(self, transaction_commit_id: str) -> dict[str, Any]:
        """Return the DURABLE anti-replay anchor set for one transaction.

        Read from the journal row and re-verified against its own digest and key set:
        a row whose anchors do not recompute is a corrupt durable fact, refused loudly
        rather than returned. This is the ONLY anchor source for minting or verifying.
        """
        self._require_open()
        row = self._connection.execute(
            "SELECT anti_replay_utf8, anti_replay_hash FROM journal"
            " WHERE transaction_commit_id = ?", (transaction_commit_id,)).fetchone()
        if row is None:
            raise StateStoreError(
                "STATE_STORE_TRANSACTION_UNKNOWN:%s" % transaction_commit_id)
        return decoded_anti_replay(row["anti_replay_utf8"], row["anti_replay_hash"],
                                   transaction_commit_id)

    def journal_rows(self, transaction_commit_id: str | None = None) -> list[dict[str, Any]]:
        """Return the durable journal rows (status in `TRANSACTION_TERMINALS`)."""
        self._require_open()
        if transaction_commit_id is None:
            cursor = self._connection.execute(
                "SELECT * FROM journal ORDER BY seq")
        else:
            cursor = self._connection.execute(
                "SELECT * FROM journal WHERE transaction_commit_id = ? ORDER BY seq",
                (transaction_commit_id,))
        return [dict(row) for row in cursor.fetchall()]

    # ---- internals ---------------------------------------------------------------

    def _require_open(self) -> None:
        if self.closed:
            raise StateStoreError("STATE_STORE_CLOSED")

    def _validated_request(self, transition_request: Any):
        if not isinstance(transition_request, dict) or set(transition_request) != _REQUEST_KEYS:
            raise StateStoreError("STATE_STORE_REQUEST_INVALID")
        transaction_commit_id = transition_request["transaction_commit_id"]
        prestate = transition_request["prestate"]
        proposal = transition_request["proposal_event"]
        child = transition_request["applied_child_event"]
        if (common.SEMANTIC_ID.fullmatch(transaction_commit_id or "") is None
                or not isinstance(prestate, dict) or not isinstance(proposal, dict)
                or not isinstance(child, dict)):
            raise StateStoreError("STATE_STORE_REQUEST_INVALID")
        if (common.canonical_event_id(proposal) != proposal.get("event_id")
                or common.canonical_event_id(child) != child.get("event_id")):
            raise StateStoreError("STATE_STORE_EVENT_IDENTITY_INVALID")
        if (proposal.get("event_type") != "propose_handoff_result"
                or prestate.get("events", {}).get(proposal["event_id"])
                != common.sha384(proposal)):
            raise StateStoreError("STATE_STORE_PROPOSAL_NOT_PERSISTED")
        return transaction_commit_id, prestate, proposal, child

    @staticmethod
    def _validated_anti_replay(anti_replay: Any) -> str:
        """Return the canonical durable bytes of the anchor set, or refuse the commit."""
        if anti_replay_shape_errors(anti_replay):
            raise StateStoreError("STATE_STORE_ANTI_REPLAY_INVALID")
        return common.canonical_json(anti_replay).decode("utf-8")

    @staticmethod
    def _replayed_poststate(prestate: dict[str, Any], proposal: dict[str, Any],
                            child: dict[str, Any]) -> dict[str, Any]:
        reference_state, reference_result = reference.reference_apply(
            copy.deepcopy(prestate), copy.deepcopy(child))
        oracle_state, oracle_result = oracle.oracle_apply(
            copy.deepcopy(prestate), copy.deepcopy(child))
        if reference_result != "APPLIED" or oracle_result != "APPLIED":
            raise StateStoreError("STATE_STORE_TRANSITION_REFUSED:%s|%s"
                                  % (reference_result, oracle_result))
        if reference_state != oracle_state:
            raise StateStoreError("STATE_STORE_REDUCER_DISAGREEMENT")
        return reference_state

    def _classify(self, transaction_commit_id: str) -> str:
        """Classify one transaction's durable rows into a distinguished terminal."""
        journal = self._connection.execute(
            "SELECT * FROM journal WHERE transaction_commit_id = ?",
            (transaction_commit_id,)).fetchone()
        if journal is None:
            return TRANSACTION_BROKEN
        # The durable anchor set is part of the transaction's consistency, not an
        # annotation on it: anchors that do not recompute are a BROKEN terminal, so a
        # tampered anchor row can never be read back as if it were committed evidence.
        try:
            decoded_anti_replay(journal["anti_replay_utf8"], journal["anti_replay_hash"],
                                transaction_commit_id)
        except StateStoreError:
            return TRANSACTION_BROKEN
        present = []
        for table in ("proposals", "children", "snapshots"):
            present.append(self._connection.execute(
                "SELECT 1 FROM %s WHERE transaction_commit_id = ?" % table,
                (transaction_commit_id,)).fetchone() is not None)
        if not any(present):
            return TRANSACTION_PENDING
        if not all(present):
            return TRANSACTION_BROKEN
        snapshot = self._connection.execute(
            "SELECT state_utf8, state_hash FROM snapshots WHERE transaction_commit_id = ?",
            (transaction_commit_id,)).fetchone()
        if snapshot["state_hash"] != common.sha384(snapshot["state_utf8"].encode("utf-8")):
            return TRANSACTION_BROKEN
        return TRANSACTION_COMMITTED

    def _record_terminal(self, transaction_commit_id: str, terminal: str) -> None:
        if terminal not in TRANSACTION_TERMINALS:
            raise StateStoreError("STATE_STORE_TERMINAL_INVALID:%s" % terminal)
        self._connection.execute("BEGIN IMMEDIATE")
        self._connection.execute(
            "UPDATE journal SET status = ? WHERE transaction_commit_id = ?",
            (terminal, transaction_commit_id))
        self._connection.execute("COMMIT")


class ReadOnlyStateStoreView:
    """FOLD 2 — a registry-free, READ-ONLY view of a FILE-backed durable store.

    Why this exists: before FOLD 2 the only way a verifier could reach durable evidence
    was `registered_store`, the in-process registry of live writer objects. That made
    verification a privilege of the process that happened to have opened the store — an
    independent auditor, a fresh CI process, or a later re-verification of an archived
    store could not check anything, and "no store in my registry" looked exactly like
    "this transaction never happened". A durable receipt has to be checkable from the
    durable bytes alone.

    What it is NOT: it never takes the write door, never appears in `_OPEN_WRITERS` or
    `_STORES_BY_IDENTITY`, never creates or migrates schema, and never repairs anything.
    It opens the file with `mode=ro` plus `PRAGMA query_only=ON`, verifies that the tables
    a reader will be answered from are actually there (`STORE_REQUIRED_TABLES`;
    `STATE_STORE_SCHEMA_INCOMPLETE`), verifies the persisted store header (`store_id` /
    `namespace` / `namespace_version` / `schema_version`) and `application_id` /
    `user_version` against the identity the CALLER asked for, and refuses loudly on any
    mismatch. The path is supplied by the verifying operator's own
    configuration — never by the receipt, which must not be able to point a verifier at
    a store the receipt's own holder fabricated.

    Byte-honest limits: a WAL store that was not closed cleanly may need recovery, which
    a read-only connection cannot perform; that surfaces as a loud `StateStoreError`
    rather than a partial answer. In-memory targets are out of scope by construction —
    they have no durable path, so `:memory:` stores keep the live-registry path.
    """

    def __init__(self, connection: sqlite3.Connection, *, path: str, store_id: str,
                 namespace: str, namespace_version: int) -> None:
        self._connection = connection
        self.path = path
        self.store_id = store_id
        self.namespace = namespace
        self.namespace_version = namespace_version
        self.closed = False

    @classmethod
    def open_verified_readonly(cls, path: Any, *, store_id: str, namespace: str,
                               namespace_version: int) -> "ReadOnlyStateStoreView":
        """Open one durable FILE store read-only and VERIFY its persisted identity."""
        if not isinstance(path, str) or not path or path.startswith(MEMORY_PATH):
            raise StateStoreError("STATE_STORE_PATH_INVALID")
        if not os.path.isfile(path):
            raise StateStoreError("STATE_STORE_TARGET_UNRESOLVED")
        connection = open_readonly_connection(path)
        try:
            # THE SCHEMA IS PART OF THE DOOR, NOT OF THE ANSWER (codex-CLI r9 F2). The
            # identity signals below say WHOSE store this is; they say nothing about
            # whether it can be asked anything. A truncated file carrying `meta`, the
            # application id and the user version but no `journal` table passed every
            # one of them and then raised a raw `sqlite3.OperationalError` out of the
            # PUBLIC verifier — outside the r6 wholesale boundary's malformed-caller-
            # input tuple, because a driver-level sqlite fault is not a `ValueError`
            # and must never be converted into one there (that boundary's own honesty
            # constraint: an instrument may not answer "your receipt is malformed"
            # when it means "I could not read my own store"). The refusal therefore
            # lives HERE, at the door, in the shape this module already refuses in:
            # named, loud, and before anything is answered from. `_resolve_store` then
            # reads it as "no durable store resolved", which is the documented
            # transaction-identity refusal plus the sentinel — a verdict, not a raise.
            present = {row[0] for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'")}
            missing = [table for table in STORE_REQUIRED_TABLES if table not in present]
            if missing:
                raise StateStoreError("STATE_STORE_SCHEMA_INCOMPLETE:" + ",".join(missing))
            header = {row["key"]: row["value"]
                      for row in connection.execute("SELECT key, value FROM meta")}
            expected = expected_store_header(store_id, namespace, namespace_version)
            if header != expected:
                raise StateStoreError("STATE_STORE_IDENTITY_MISMATCH")
            application_id = int(connection.execute(
                "PRAGMA application_id").fetchone()[0])
            user_version = int(connection.execute("PRAGMA user_version").fetchone()[0])
            if (application_id != STORE_APPLICATION_ID
                    or user_version != STORE_SCHEMA_VERSION):
                raise StateStoreError("STATE_STORE_SCHEMA_VERSION_MISMATCH")
        except sqlite3.Error as exc:
            connection.close()
            raise StateStoreError("STATE_STORE_UNREADABLE:%s" % type(exc).__name__) from exc
        except StateStoreError:
            connection.close()
            raise
        return cls(connection, path=path, store_id=store_id, namespace=namespace,
                   namespace_version=namespace_version)

    def close(self) -> None:
        if self.closed:
            return
        self.closed = True
        self._connection.close()

    @property
    def store_identity(self) -> dict[str, Any]:
        return {"store_id": self.store_id, "namespace": self.namespace,
                "namespace_version": self.namespace_version}

    def _require_open(self) -> None:
        if self.closed:
            raise StateStoreError("STATE_STORE_CLOSED")

    def journal_rows(self, transaction_commit_id: str | None = None) -> list[dict[str, Any]]:
        """Durable journal rows, read through the read-only connection."""
        self._require_open()
        if transaction_commit_id is None:
            cursor = self._connection.execute("SELECT * FROM journal ORDER BY seq")
        else:
            cursor = self._connection.execute(
                "SELECT * FROM journal WHERE transaction_commit_id = ? ORDER BY seq",
                (transaction_commit_id,))
        return [dict(row) for row in cursor.fetchall()]

    def transaction_rows(self, transaction_commit_id: str) -> dict[str, Any]:
        """Durable proposal / child / snapshot rows for one COMMITTED terminal."""
        self._require_open()
        rows = self.journal_rows(transaction_commit_id)
        if not rows:
            raise StateStoreError(
                "STATE_STORE_TRANSACTION_UNKNOWN:%s" % transaction_commit_id)
        if rows[0]["status"] != TRANSACTION_COMMITTED:
            raise StateStoreError("STATE_STORE_TRANSACTION_%s:%s"
                                  % (rows[0]["status"], transaction_commit_id))
        record: dict[str, Any] = {"journal": rows[0]}
        for table in ("proposals", "children", "snapshots"):
            row = self._connection.execute(
                "SELECT * FROM %s WHERE transaction_commit_id = ?" % table,
                (transaction_commit_id,)).fetchone()
            if row is None:
                raise StateStoreError("STATE_STORE_ROW_MISSING:%s" % table)
            record[table] = dict(row)
        return record

    def anti_replay_anchors(self, transaction_commit_id: str) -> dict[str, Any]:
        """The DURABLE anchor set, re-decoded and re-digested from the durable bytes."""
        self._require_open()
        row = self._connection.execute(
            "SELECT anti_replay_utf8, anti_replay_hash FROM journal"
            " WHERE transaction_commit_id = ?", (transaction_commit_id,)).fetchone()
        if row is None:
            raise StateStoreError(
                "STATE_STORE_TRANSACTION_UNKNOWN:%s" % transaction_commit_id)
        return decoded_anti_replay(row["anti_replay_utf8"], row["anti_replay_hash"],
                                   transaction_commit_id)
