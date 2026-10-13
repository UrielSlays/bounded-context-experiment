"""BUILD — the operator-preconfigured owner trust anchor (production bootstrap).

Why this module exists
----------------------
BUILD acceptance council r1 closed NO-GO: production admission on both authority
planes could be bootstrapped entirely by its claimant. `evaluate_production_measurement`
and `verify_state_authority_receipt_v2` took the trust-root manifest AND its custody
evidence as per-request parameters, and the only checks over them were internal
consistency of the graph the caller supplied (hash-match of caller documents against
caller digests, distinct role STRINGS, disjoint key-ID lists). Nothing anchored that
graph to anything the api-caller could not author, so a fresh attacker Ed25519 key plus
an invented manifest and invented custody documents cleared production admission
(`MBCX-01-BUILD-ACCEPTANCE-ROUND-r1-SYNTHESIS.md`; SEAT2 and SEAT3 both EXECUTED it).

The model this adopts is the established one, not a new invention: SLSA v1.2 "Verifying
artifacts" step 1 and TUF §§2.1/5.3 both begin verification from a VERIFIER-CONTROLLED,
PRECONFIGURED root of trust and never accept the claimant's own root as bootstrap.

The one invariant this module exists to enforce
-----------------------------------------------
    NO UNAUTHENTICATED TRUST GRAPH REACHES PRODUCTION ADMISSION: production activation
    of either authority requires an owner-signed activation statement, verified against
    an anchor the VERIFIER loads from operator-injected configuration, that binds the
    EXACT canonical digest of the manifest under evaluation together with its validity
    window, the authorized signing-key identity, the trust-root editor key set, the
    build provenance digest, the four custody-evidence digests, and the activation
    generation.

Everything else (hash-match of custody documents, role distinctness, key-set
disjointness, validity/revocation) is retained UNCHANGED as additional structural
checks. They were never wrong; they were simply not authentication.

How the anchor gets here (it is NOT a request parameter — that is the whole point)
---------------------------------------------------------------------------------
  * `configure_owner_trust_anchor(anchor, current_time=None)` — operator/process wiring,
    called once at process or verifier construction time (the same seam the signer
    already uses: an injected interface,
    `mbcx01_build_state_adapter.produce_state_authority_receipt_v2` docstring, "the
    private key never lives here ... `signer` is an injected object");
  * `configure_production_verifier_context(context)` / `installed_production_verifier(...)`
    — the same seam with the context constructed explicitly, and (for the context
    manager) restored on exit, so a fixture ASSEMBLER can wire what it needs without
    leaving it behind for the next caller in the process;
  * `MBCX01_BUILD_OWNER_TRUST_ANCHOR` — an OS-controlled configuration path the verifier
    LOADS. A fresh verifying process (`test_ba28`-style cold verification) needs no
    in-process wiring, only the operator's environment.

A per-request evaluation call can supply none of them: `evaluate_production_measurement`,
`verify_state_authority_receipt_v2` and `verify_production_scorer_input` keep their
signatures, and none of them accepts an anchor or a context. T2 is unchanged: this
separates the bounded api-caller from the OPERATOR, not the operator from the box owner.

r2 FIX CLASS — FIXTURE_ISOLATION / INSTANCE-SCOPED VERIFIER CONTEXT
-------------------------------------------------------------------
BUILD acceptance council r2 closed GO-WITH-FIXES on three executed defects of the shape
above (`MBCX-01-BUILD-SEAT3-CODEX-VERDICT-r2.md` F1/F2/F3): the `fixture_only` flag was
PARSED and never consulted, so the committed fixture anchor — whose private half is
committed, and therefore public — authorized production admission at all three doors;
the anchor was a mutable process global re-read DURING an evaluation, so a caller
mapping object whose `.get`/`__getitem__` reconfigured it substituted the root of trust
mid-verification; and the integration fixture installed the fixture anchor process-wide
and never restored it.

The one invariant that collapses all three, adopted from Go `crypto/x509`'s
`VerifyOptions` (roots AND `CurrentTime` are fields of a per-verification value the
VERIFIER constructs) and TUF's out-of-band trusted root
(`MBCX-01-BUILD-R2-TRUSTCONTEXT-SWEEP-LOG.md`), stated as a COMPLEMENT:

    PRODUCTION VERIFICATION ACCEPTS EXACTLY ONE THING — an immutable, INSTANCE-SCOPED
    `ProductionVerifierContext` whose anchor is operator-supplied and NOT fixture-marked,
    carrying its own current time — AND REFUSES EVERYTHING ELSE.

Mechanically: a `fixture_only` anchor cannot be built into a context through any public
constructor or wiring call (F1); every production door resolves its context ONCE, before
any caller-supplied object is read, and carries that immutable value through the whole
evaluation, so re-wiring the process during a verification cannot change the decision in
flight (F2); and an assembler wires its context inside `installed_production_verifier(...)`,
which restores the operator's own wiring on exit (F3). The clock is the verifier's: when
the operator injects no instant the fallback is the REAL clock, never a value read out of
the artifact under verification (F4). The anchor DOCUMENT is parsed strictly, so a
duplicate member is a named refusal rather than a silent last-member-wins resolution (F6).

THE KEY, NOT THE LABEL (2026-08-14 fold — committed fixture KEY MATERIAL)
-------------------------------------------------------------------------
The r2 fold above recognises non-production trust material by a FLAG IN A DOCUMENT. The
BUILD acceptance r3 council seat pointed out what that leaves open, and it was
reproduced at the byte: take the committed `MBCX-01-BUILD-OWNER-TRUST-ANCHOR.fixture.json`,
flip `fixture_only` to false, give it a new `anchor_id`, and
`new_production_verifier_context()` built a PRODUCTION context around a public key whose
private half is committed at `mbcx01_build_ceremony_fixture.py:39`.

This is an OPERATOR FOOTGUN, not an attack path — the ceremony (§3 step 0) is exactly
when a human hand-writes that document, and copying the committed example is the obvious
way to write one. The prior art is MITRE CWE-1291 ("Public Key Re-Use for Signing both
Debug and Production Code", PeerOf CWE-321), whose mitigation phase is IMPLEMENTATION
("use different keys for Production and Debug"). We satisfy it at CONTEXT CONSTRUCTION,
which is our choice of site and not something MITRE prescribes. A context refuses any anchor whose
public key is committed to this repository, by name
(`PRODUCTION_VERIFIER_CONTEXT_FIXTURE_KEY_MATERIAL`), regardless of the flag. The set of
such keys is DERIVED from the committed documents themselves
(`committed_fixture_key_material`), so it cannot drift from the repository's bytes.

THE KEY, NOT THE TEXT — AND NOT ONLY THE ANCHOR (2026-08-15 fold)
------------------------------------------------------------------
The r3 fold above recognises committed key material by comparing the PEM's base64 BODY.
The BUILD acceptance r4 council seats found both halves of what that leaves open, and
both were reproduced at the byte:

  * IDENTITY WAS AN ENCODING, NOT A KEY. RFC 4648 §3.5 is explicit that where the
    non-significant trailing bits of the final base64 character are not required to be
    zero there is no canonical representation. The committed anchor body ending
    `...DvZ8zY=` and the body ending `...DvZ8zZ=` decode to the SAME 44 octets, but only
    the first was in the derived set — so through the documented
    `MBCX01_BUILD_OWNER_TRUST_ANCHOR` door the verbatim committed key was REFUSED while
    the same key re-encoded by hand was ADMITTED as a production root. `public_key_identity`
    now decodes first and identifies an Ed25519 key by its 32-byte PUBLIC POINT, read
    structurally out of the SubjectPublicKeyInfo (`ed25519_public_key_bytes`), so a
    re-encoded carrier AND a re-wrapped DER envelope are the same key. The shelf pattern
    is the mcp-bridge CRL path, which loads the key from the RAW SPKI octets and parses
    the structure rather than the text (`src/crl/crl-authenticate.ts`, `src/crl/der-reader.ts`).
    `strict_public_key_carrier_ok` then refuses any non-canonical carrier outright —
    `strict_signature_carrier_ok`'s property, one field away, on the field that names the
    root of trust.
  * THE REFUSAL COVERED THE ANCHOR CLASS ONLY. A seat made the committed Ed25519 test
    SIGNING pair the production measurement signing root under an INDEPENDENTLY generated
    owner anchor and cleared admission with `production_admission_errors = []`. The
    committed-key set is now harvested from EVERY `public_key_pem` in every committed
    `*.fixture.json` document, and the two authorities consult it for their production
    ROOTS as well: `PRODUCTION_SIGNING_KEY_FIXTURE_MATERIAL` and
    `STATE_AUTHORITY_V2_SIGNING_KEY_FIXTURE_MATERIAL`. The ceremony always said this
    (`MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md` §3 steps 0 and 3); prose is not a control.

SCOPE, STATED PLAINLY (2026-08-14 premise correction)
------------------------------------------------------
These are SCIENTIFIC-VALIDITY invariants — they stop the experiment fooling ITSELF (a
fixture root silently counting as real, a stale root silently counting as fresh, a
binding-only result reading as a suite PASS). They are NOT an access-control boundary.
MBCX-01 has no API, no production runtime and no external submitter; every caller of
these authorities is the harness and its own tests. An actor able to execute arbitrary
Python in this interpreter can therefore reach past every guard here
(`object.__setattr__` on a live context, `object.__new__` around a fixture anchor,
re-wiring the process between calls) — and that actor IS the box owner. Under the
permanent T2 ceiling (`DESIGN-SHELF-MAP.md` §1) on-box walls against the box owner are
theatre, so that whole family is a NAMED, ACCEPTED residual with zero grind:
tamper-EVIDENT, not tamper-proof. The r2 rider that froze this wiring seam for the
length of a verification was REVERTED on 2026-08-14 for exactly that reason
(`MBCX-01-BUILD-ADVERSARY-PREMISE-CORRECTION-2026-08-14.md`); it also carried a real
reliability cost, since its depth counter was a plain module int that could only ever
false-fire, never true-fire.

Ceremony mapping (`MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md`)
---------------------------------------------------------
§3 step 5: "OWNER reviews all three, runs the BUILD verifier against the manifest +
evidence, and signs evidence document 4." The owner's signature is what this module
authenticates. The owner root signs ONE statement; that statement names the identities
and digests of the other three documents plus the ceremony receipt, so the whole custody
set is authenticated by one anchored signature (per the round's TAR-PIT ruling: one
invariant closes the class; do not grind fake-role permutations).

ADJUDICATED DEVIATION (byte reason, recorded rather than papered over): the owner
signature is carried in a DETACHED activation statement rather than inside
`PRODUCTION_SIGNING_CEREMONY_RECEIPT` itself. A ceremony receipt that contained the
manifest digest could not also be hash-bound INTO that manifest by
`trust_policy.signing_ceremony_receipt_digest` — SHA-384 over each other is a preimage
cycle with no solution. The detached statement binds both directions from outside:
`manifest_digest` covers the entire manifest (including the four custody digest fields),
and `custody_evidence_digests` covers the four documents.

No key material, no ceremony and no activation lives in this module or in this
repository: the committed anchor instance is FIXTURE-ONLY and carries a public key.
"""

from __future__ import annotations

import base64
import contextlib
import datetime
import hashlib
import json
import os
import re
import subprocess
from typing import Any

import mbcx01_r13_common as common

#: Schema ids of the two documents this module reads.
ANCHOR_SCHEMA_ID = "OwnerTrustAnchorV1"
ACTIVATION_SCHEMA_ID = "OwnerCeremonyActivationV1"

#: The two production authorities an anchor may be scoped to.
AUTHORITY_MEASUREMENT = "MBCX01_BUILD_MEASUREMENT_AUTHORITY"
AUTHORITY_STATE = "MBCX01_BUILD_STATE_AUTHORITY"
AUTHORITIES = (AUTHORITY_MEASUREMENT, AUTHORITY_STATE)

#: OS-controlled configuration: the path the verifier LOADS its anchor from.
ANCHOR_PATH_ENV = "MBCX01_BUILD_OWNER_TRUST_ANCHOR"

SIGNATURE_ALGORITHM = "ED25519"
SIGNATURE_BYTES = 64

#: The BUILD-side Ed25519 verifier. It is a strict-carrier sibling of the FROZEN
#: `verify-r13-receipt-signature.mjs` (which stays untouched and keeps serving the
#: frozen r13.2 suites): identical closed request/response contract, plus the canonical
#: base64 grammar/padding/length + decode/re-encode equality check that closes
#: MBCX01-BUILD-R1-SIGNATURE-CARRIER (codex F6).
SIGNATURE_VERIFIER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "verify-build-receipt-signature.mjs")

ANCHOR_KEYS = {"schema_id", "anchor_id", "fixture_only", "algorithm", "public_key_pem",
               "authorities", "minimum_activation_generation", "custody_note"}

ACTIVATION_KEYS = {"schema_id", "anchor_id", "authority", "activation_generation",
                   "manifest_digest", "manifest_validity", "authorized_signing_key_id",
                   "authorized_editor_key_ids", "custody_evidence_digests",
                   "provenance_digest", "signature_b64"}

#: Carrier fields are never part of the signed region (mirrors
#: `mbcx01_build_state_authority.V2_UNSIGNED_KEYS`).
ACTIVATION_UNSIGNED_KEYS = {"signature_b64"}

#: Canonical base64: the standard alphabet, correct padding, length a multiple of 4.
#: Whitespace, base64url characters and non-canonical padding are all refused BEFORE
#: any cryptographic verification, and the decoded bytes must re-encode to the exact
#: same string, so one signature has exactly one accepted carrier.
STRICT_BASE64_RE = re.compile(r"^[A-Za-z0-9+/]+={0,2}$")

ANCHOR_ID_RE = re.compile(r"^[A-Z][A-Z0-9.\-]{0,95}$")

#: RFC-3339 UTC seconds, the one instant grammar this lane uses.
INSTANT_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")

#: Generic outcome codes. Each authority maps them into its own closed vocabulary.
ANCHOR_UNAVAILABLE = "ANCHOR_UNAVAILABLE"
ACTIVATION_UNAUTHENTICATED = "ACTIVATION_UNAUTHENTICATED"
SIGNATURE_CARRIER_INVALID = "SIGNATURE_CARRIER_INVALID"
#: r2 fix class: the operator wired an anchor, but it is FIXTURE material. This is an
#: ANCHOR-class outcome (like `ANCHOR_UNAVAILABLE`), deliberately NOT folded into the
#: single authentication code: "your test root is not a production root" and "this did
#: not authenticate" are different facts for the operator reading the log.
ANCHOR_FIXTURE_ONLY = "ANCHOR_FIXTURE_ONLY"

#: The refusal raised when an anchor carries KEY MATERIAL that is committed to this
#: repository, whatever its `fixture_only` flag says. See
#: `committed_fixture_key_material()` for how that set is derived and why the flag alone
#: was never enough.
PRODUCTION_VERIFIER_CONTEXT_FIXTURE_KEY_MATERIAL = (
    "PRODUCTION_VERIFIER_CONTEXT_FIXTURE_KEY_MATERIAL")

#: The refusal raised when an anchor's `public_key_pem` is not the ONE canonical carrier
#: of the key it carries (`strict_public_key_carrier_ok`). Same shape, same reason, one
#: field away from `strict_signature_carrier_ok`.
PRODUCTION_VERIFIER_CONTEXT_KEY_CARRIER_INVALID = (
    "PRODUCTION_VERIFIER_CONTEXT_KEY_CARRIER_INVALID")

#: RFC 8410 §4: an Ed25519 SubjectPublicKeyInfo is a SEQUENCE of an AlgorithmIdentifier
#: carrying OID 1.3.101.112 with ABSENT parameters, and a BIT STRING with no unused bits
#: holding the 32-byte public point — 44 DER octets whose first 12 are fixed.
ED25519_OID_DER = bytes((0x2b, 0x65, 0x70))
ED25519_PUBLIC_KEY_BYTES = 32
ED25519_SPKI_PREFIX = bytes.fromhex("302a300506032b6570032100")
ED25519_SPKI_BYTES = len(ED25519_SPKI_PREFIX) + ED25519_PUBLIC_KEY_BYTES

#: Committed example anchor documents live beside this module under this suffix. The
#: NAME is the ground truth here, not the flag inside the file: the whole point of this
#: refusal is that the flag can be edited, and an operator editing the committed example
#: in place would take the last committed copy of that key out of the derived set if the
#: derivation trusted the flag.
FIXTURE_DOCUMENT_SUFFIX = ".fixture.json"


def normalize_pem_eol(value: Any) -> Any:
    """RFC 7468 transport normalisation: CRLF/CR -> LF, and the final EOL supplied.

    AMENDMENT-2 (2026-08-15). RFC 7468 §2 says generators MUST wrap lines and
    that parsers are to handle the differing newline conventions in use (CRLF,
    CR and LF), and the §3 ABNF spells the EOL after the final
    `-----END PUBLIC KEY-----` boundary as OPTIONAL. This door required literal
    LF *and* a final EOL, so on Windows — where CRLF is the NATIVE line ending
    and the ceremony's own `openssl`/`node` export produces it — a real
    operator key was refused as malformed. That is REFUSING RIGHT EVIDENCE: the
    key is the same key, and the ceremony stops.

    Only the outer TEXT TRANSPORT is normalised, and it is normalised BEFORE any
    other check rather than instead of one. Everything that decides whether one
    key has one carrier is untouched and still runs on the normalised text:
    canonical base64 (standard alphabet, correct padding, no whitespace inside
    the body, decode/re-encode equality), the canonical RFC 8410 §4 SPKI
    encoding, the decoded-key identity, and the committed-key refusal. A
    non-string is returned unchanged so the caller's own type check still fires.

    Deliberately BROADER than `openssl pkey -pubin`, which rejects a bare-CR
    document: this follows RFC 7468's parser guidance rather than one parser's
    behaviour. The latitude is over line endings only and cannot change which
    key a document carries.
    """
    if not isinstance(value, str):
        return value
    text = value.replace("\r\n", "\n").replace("\r", "\n")
    if text.endswith("-----") and not text.endswith("\n"):
        text += "\n"
    return text


class TrustAnchorError(ValueError):
    """A malformed anchor document, or an unusable anchor configuration."""


class OwnerTrustAnchor:
    """An immutable, operator-preconfigured owner root of trust (public key only)."""

    __slots__ = ("anchor_id", "algorithm", "public_key_pem", "authorities",
                 "minimum_activation_generation", "fixture_only", "source")

    def __init__(self, *, anchor_id: str, algorithm: str, public_key_pem: str,
                 authorities: Any, minimum_activation_generation: int,
                 fixture_only: bool, source: str = "INJECTED_OBJECT") -> None:
        # AMENDMENT-2: the operator's line endings are TRANSPORT, not identity.
        # Normalised here, before the framing check, so the anchor holds ONE
        # text for one key and every downstream comparison keeps seeing the
        # canonical LF spelling it always saw. Nothing else is relaxed.
        public_key_pem = normalize_pem_eol(public_key_pem)
        if (not isinstance(anchor_id, str) or ANCHOR_ID_RE.fullmatch(anchor_id) is None
                or algorithm != SIGNATURE_ALGORITHM
                or not isinstance(public_key_pem, str)
                or not public_key_pem.startswith("-----BEGIN PUBLIC KEY-----\n")
                or not public_key_pem.endswith("-----END PUBLIC KEY-----\n")
                or not isinstance(authorities, (list, tuple)) or not authorities
                or any(value not in AUTHORITIES for value in authorities)
                or len(set(authorities)) != len(list(authorities))
                or not isinstance(minimum_activation_generation, int)
                or isinstance(minimum_activation_generation, bool)
                or minimum_activation_generation < 1
                or not isinstance(fixture_only, bool)):
            raise TrustAnchorError("OWNER_TRUST_ANCHOR_INVALID")
        object.__setattr__(self, "anchor_id", anchor_id)
        object.__setattr__(self, "algorithm", algorithm)
        object.__setattr__(self, "public_key_pem", public_key_pem)
        object.__setattr__(self, "authorities", tuple(authorities))
        object.__setattr__(self, "minimum_activation_generation",
                           minimum_activation_generation)
        object.__setattr__(self, "fixture_only", fixture_only)
        object.__setattr__(self, "source", str(source))

    def __setattr__(self, name: str, value: Any) -> None:  # pragma: no cover - guard
        raise TrustAnchorError("OWNER_TRUST_ANCHOR_IMMUTABLE")

    def __repr__(self) -> str:  # pragma: no cover - diagnostics only
        return ("OwnerTrustAnchor(anchor_id=%r, authorities=%r, fixture_only=%r, "
                "source=%r)" % (self.anchor_id, self.authorities, self.fixture_only,
                                self.source))


class ProductionVerifierContext:
    """An immutable, INSTANCE-SCOPED verifier context (the r2 fix class).

    The shape is Go's `crypto/x509.VerifyOptions`, which is the reference implementation
    of exactly this problem: the ROOTS and the CURRENT TIME are fields of a value the
    VERIFIER constructs and passes into each verification, never a process-global the
    artifact under verification can reach, and never a value read out of that artifact.

    Two properties hold against ORDINARY USE — construction and attribute assignment
    through the public API — and the claim is deliberately no stronger than that:

      * a `fixture_only` anchor cannot be built into a production context through
        `ProductionVerifierContext(...)`, `new_production_verifier_context(...)` or
        `configure_owner_trust_anchor(...)`: test material whose private half is
        committed does not become a production root of trust by relabelling (codex
        r2 F1). It is NOT unrepresentable in the absolute sense: `object.__new__` plus
        `object.__setattr__` builds such a context, and `configure_production_verifier_context`
        accepts it, because that entry point is an `isinstance` check;
      * an anchor carrying KEY MATERIAL committed to this repository cannot be built
        into a production context either, WHATEVER its `fixture_only` flag says. That
        flag is a claim the document makes about itself, and the ceremony's own
        procedure (`MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md` section 3 step 0) has a human
        hand-writing the document — copying the committed example and editing the labels
        is the obvious way to do it. The refusal is
        `PRODUCTION_VERIFIER_CONTEXT_FIXTURE_KEY_MATERIAL` and it names the committed
        document the key came from; the set is DERIVED from the repository's own bytes
        (`committed_fixture_key_material`), never hand-listed. Prior art: MITRE CWE-1291,
        whose mitigation phase is Implementation;
      * `__setattr__`/`__delattr__` raise, so a reference handed to a verification
        cannot be edited through ordinary attribute assignment. `object.__setattr__`
        still edits a live context.

    Both bypasses need an in-process actor executing arbitrary Python inside this
    interpreter. That actor IS the box owner: this harness has no untrusted caller —
    no API, no production runtime, no external submitter — and every caller of these
    authorities is the harness and its own tests. Under the permanent T2 ceiling
    (`DESIGN-SHELF-MAP.md` section 1) defending the box owner from itself is
    theatre, so the bypass is a NAMED, ACCEPTED residual and no code chases it. The
    invariants here are a SCIENTIFIC-VALIDITY device against the experiment fooling
    itself, not an access-control boundary against an adversary.

    `current_time` is the operator's fixed instant when it supplies one — which is what
    lets a deterministic suite pin its own clock — and `None` otherwise, in which case
    `current_instant()` reads the REAL clock at the moment of use, exactly as
    `VerifyOptions.CurrentTime` falls back to `time.Now()`.
    """

    __slots__ = ("anchor", "current_time", "source")

    def __init__(self, *, anchor: Any, current_time: Any = None,
                 source: str = "OPERATOR_WIRING") -> None:
        if not isinstance(anchor, OwnerTrustAnchor):
            raise TrustAnchorError("PRODUCTION_VERIFIER_CONTEXT_INVALID")
        if anchor.fixture_only is not False:
            raise TrustAnchorError(
                "PRODUCTION_VERIFIER_CONTEXT_FIXTURE_ANCHOR_REFUSED:%s"
                % (anchor.anchor_id,))
        # The KEY, not the label, and not the TEXT the key arrived in. `fixture_only`
        # above is a claim the anchor document makes about itself; this is a fact about
        # the key material it carries, established from the DECODED key bytes so that
        # re-encoding the carrier or re-wrapping the DER envelope cannot launder it.
        committed = committed_fixture_key_document(anchor.public_key_pem)
        if committed is not None:
            raise TrustAnchorError(
                "%s:%s:%s" % (PRODUCTION_VERIFIER_CONTEXT_FIXTURE_KEY_MATERIAL,
                              anchor.anchor_id, committed))
        # One key, one accepted carrier — the `strict_signature_carrier_ok` property on
        # the field that names the root of trust. Checked AFTER the committed-material
        # refusal on purpose: a re-encoded committed key must be told what it really is,
        # not merely that its carrier is malformed.
        if not strict_public_key_carrier_ok(anchor.public_key_pem):
            raise TrustAnchorError(
                "%s:%s" % (PRODUCTION_VERIFIER_CONTEXT_KEY_CARRIER_INVALID,
                           anchor.anchor_id))
        if current_time is not None and (
                not isinstance(current_time, str)
                or INSTANT_RE.fullmatch(current_time) is None):
            raise TrustAnchorError("PRODUCTION_VERIFIER_CONTEXT_INVALID")
        object.__setattr__(self, "anchor", anchor)
        object.__setattr__(self, "current_time", current_time)
        object.__setattr__(self, "source", str(source))

    def __setattr__(self, name: str, value: Any) -> None:
        raise TrustAnchorError("PRODUCTION_VERIFIER_CONTEXT_IMMUTABLE")

    def __delattr__(self, name: str) -> None:
        raise TrustAnchorError("PRODUCTION_VERIFIER_CONTEXT_IMMUTABLE")

    def authorizes(self, authority: str) -> bool:
        return authority in self.anchor.authorities

    def current_instant(self) -> str:
        """The instant this verification judges validity at (RFC-3339 UTC seconds)."""
        if self.current_time is not None:
            return self.current_time
        return datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ")

    def __repr__(self) -> str:  # pragma: no cover - diagnostics only
        return ("ProductionVerifierContext(anchor_id=%r, current_time=%r, source=%r)"
                % (self.anchor.anchor_id, self.current_time, self.source))


class _OperatorWiring:
    """What the OPERATOR installed: the anchor, and the context it does (or does not) make."""

    __slots__ = ("anchor", "context")

    def __init__(self, anchor: OwnerTrustAnchor,
                 context: ProductionVerifierContext | None) -> None:
        object.__setattr__(self, "anchor", anchor)
        object.__setattr__(self, "context", context)

    def __setattr__(self, name: str, value: Any) -> None:  # pragma: no cover - guard
        raise TrustAnchorError("OWNER_TRUST_ANCHOR_IMMUTABLE")


#: Process-level operator wiring. It is deliberately NOT reachable from any
#: per-request argument: an api-caller can reach the authorities only through the
#: data it passes to them. Every production door SNAPSHOTS the context out of this
#: once, at entry, so re-wiring the process during a verification cannot change that
#: verification's decision (codex r2 F2).
_INSTALLED_WIRING: _OperatorWiring | None = None


class _AmbiguousDocument(ValueError):
    """A configuration document with more than one meaning (duplicate member)."""


def _strict_object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    names = [name for name, _value in pairs]
    if len(set(names)) != len(names):
        raise _AmbiguousDocument("duplicate member")
    return dict(pairs)


def _refuse_json_constant(name: str) -> Any:
    raise _AmbiguousDocument("non-JSON constant: %s" % name)


def strict_json_document(text: str) -> Any:
    """Parse a configuration document with exactly one meaning, or refuse.

    `json.load` resolves a duplicate member by last-member-wins, so a document carrying
    `fixture_only` twice has two readings and the parser silently picks one (codex r2
    F6). NaN/Infinity are refused for the same reason: they are not JSON, and a
    configuration boundary is the wrong place to be generous.
    """
    return json.loads(text, object_pairs_hook=_strict_object_pairs,
                      parse_constant=_refuse_json_constant)


#: Cache for `committed_fixture_key_material()`. The committed documents do not change
#: while a verifier runs, and this sits on the production context-construction path.
_FIXTURE_KEY_MATERIAL: dict[str, str] | None = None


def _pem_base64_body(public_key_pem: Any) -> str | None:
    """The base64 body between the PEM framing lines, whitespace removed, or None."""
    if not isinstance(public_key_pem, str):
        return None
    begin = "-----BEGIN PUBLIC KEY-----"
    end = "-----END PUBLIC KEY-----"
    start = public_key_pem.find(begin)
    stop = public_key_pem.find(end)
    if start < 0 or stop < start:
        return None
    return "".join(public_key_pem[start + len(begin):stop].split())


def _read_der_tlv(data: bytes, offset: int) -> tuple[int, int, int, int] | None:
    """One BER/DER TLV at `offset` as `(tag, content_start, content_end, next)`, or None.

    Deliberately tolerant of the LONG FORM length (X.690 §8.1.3.5) even though DER
    requires the short form where it fits (§10.1): the point of this reader is that a
    NON-canonical encoding of a key must still resolve to the SAME key identity, so that
    re-wrapping the envelope is not a way to launder committed key material. Canonicality
    is judged separately and loudly by `strict_public_key_carrier_ok`.
    """
    if offset < 0 or offset >= len(data):
        return None
    tag = data[offset]
    if tag & 0x1F == 0x1F:  # multi-octet tag number: no SPKI field uses one
        return None
    index = offset + 1
    if index >= len(data):
        return None
    first = data[index]
    index += 1
    if first < 0x80:
        length = first
    else:
        count = first & 0x7F
        if count == 0 or count > 4 or index + count > len(data):
            return None
        length = int.from_bytes(data[index:index + count], "big")
        index += count
    end = index + length
    if end > len(data):
        return None
    return tag, index, end, end


def ed25519_public_key_bytes(der: bytes) -> bytes | None:
    """The 32-byte Ed25519 public point inside a SubjectPublicKeyInfo, or None.

    Structural, not pattern-matched: the SEQUENCE, the AlgorithmIdentifier, the
    1.3.101.112 OID with ABSENT parameters (RFC 8410 §3) and the BIT STRING with zero
    unused bits are each READ. The shelf pattern is
    `src/crl/crl-authenticate.ts:109-120` in the mcp-bridge repository (SPKI parsed
    structurally through `src/crl/der-reader.ts`, the key loaded from the RAW octets
    rather than from a text envelope); this is that pattern at Ed25519 scale.
    """
    sequence = _read_der_tlv(der, 0)
    if sequence is None or sequence[0] != 0x30 or sequence[3] != len(der):
        return None
    algorithm = _read_der_tlv(der, sequence[1])
    if algorithm is None or algorithm[0] != 0x30 or algorithm[2] > sequence[2]:
        return None
    oid = _read_der_tlv(der, algorithm[1])
    if (oid is None or oid[0] != 0x06 or oid[3] != algorithm[2]
            or der[oid[1]:oid[2]] != ED25519_OID_DER):
        return None
    bits = _read_der_tlv(der, algorithm[3])
    if bits is None or bits[0] != 0x03 or bits[3] != sequence[2]:
        return None
    if bits[2] - bits[1] != ED25519_PUBLIC_KEY_BYTES + 1 or der[bits[1]] != 0:
        return None
    return der[bits[1] + 1:bits[2]]


def public_key_identity(public_key_pem: Any) -> str | None:
    """The identity of a public key for comparison: the KEY, never the text carrying it.

    Ed25519 keys are identified by their 32-byte PUBLIC POINT, read structurally out of
    the decoded SubjectPublicKeyInfo; anything else that decodes is identified by a
    SHA-384 over its decoded DER. Returns `None` when the value is not a PEM public key
    at all, or when its body is not decodable base64.

    WHY THE TEXT WAS NEVER AN IDENTITY (BUILD acceptance r4, reproduced at the byte):
    this function used to return the base64 BODY with whitespace removed, which made two
    encodings of one key two different keys. RFC 4648 §3.5 is explicit that where the
    non-significant trailing bits of the final character are not required to be zero
    there is NO canonical representation, so the committed anchor body ending `...DvZ8zY=`
    and the body ending `...DvZ8zZ=` decode to the SAME 44 octets — and only the first was
    in `committed_fixture_key_material()`. The consequence was executed through the
    documented `MBCX01_BUILD_OWNER_TRUST_ANCHOR` door: the verbatim committed fixture key
    was refused `PRODUCTION_VERIFIER_CONTEXT_FIXTURE_KEY_MATERIAL` while the SAME key
    re-encoded by hand was ADMITTED as a production root. The DER ENVELOPE is the same
    class one layer down (a long-form length carries an identical point), which is why the
    identity is the POINT and not the envelope.
    """
    body = _pem_base64_body(public_key_pem)
    if body is None:
        return None
    try:
        der = base64.b64decode(body.encode("ascii"), validate=True)
    except (ValueError, TypeError, UnicodeEncodeError):
        try:
            # The base64url alphabet (RFC 4648 §5) is the other way one key becomes two
            # strings — the same permissiveness `strict_signature_carrier_ok` exists to
            # deny in a CARRIER. Here it must be RECOGNISED, not denied: an identity that
            # refuses to read a carrier hands that carrier a way to be an unknown key.
            der = base64.urlsafe_b64decode(body.encode("ascii"))
        except (ValueError, TypeError, UnicodeEncodeError):
            return None
    if not der:
        return None
    point = ed25519_public_key_bytes(der)
    if point is not None:
        return "ED25519:" + point.hex().upper()
    # Not an Ed25519 SPKI: still identified by BYTES, never by the text. `SIGNATURE_ALGORITHM`
    # means no other key type reaches an anchor today; this keeps the property if one ever does.
    return "SPKI-SHA384:" + hashlib.sha384(der).hexdigest().upper()


def strict_public_key_carrier_ok(value: Any) -> bool:
    """Canonical carrier check for a PEM public key — the sibling of
    `strict_signature_carrier_ok`, one field away.

    One key, exactly one accepted carrier: RFC 7468 §13 framing with a single body line,
    canonical base64 (standard alphabet, correct padding, length a multiple of four, and
    decode/re-encode equality — the RFC 4648 §3.5 trailing-bit malleability), and the
    canonical RFC 8410 §4 Ed25519 SubjectPublicKeyInfo encoding of the decoded point.
    An Ed25519 SPKI is 44 octets, so its base64 body is 60 characters and RFC 7468's
    64-character line limit never wraps it: a wrapped body is a hand edit, not an emitter.

    This is a CARRIER check, not an identity check. `public_key_identity` deliberately
    still recognises the key inside a non-canonical carrier — otherwise re-encoding would
    launder committed key material into an unknown key, which is the defect this pair of
    functions closes from both ends.

    AMENDMENT-2 (2026-08-15): the RFC-permitted EOL conventions and the optional final
    EOL are NORMALISED first (`normalize_pem_eol`), because RFC 7468 §§2-3 makes them
    spellings of the same document and Windows writes CRLF natively. Everything below is
    unchanged and now runs on the normalised text: a body wrapped over lines, carrying
    whitespace, using the base64url alphabet, encoding non-canonical trailing bits, or
    wrapping a long-form DER length is refused exactly as before.
    """
    value = normalize_pem_eol(value)
    if not isinstance(value, str):
        return False
    begin = "-----BEGIN PUBLIC KEY-----\n"
    end = "\n-----END PUBLIC KEY-----\n"
    if not value.startswith(begin) or not value.endswith(end):
        return False
    body = value[len(begin):len(value) - len(end)]
    if STRICT_BASE64_RE.fullmatch(body) is None or len(body) % 4 != 0:
        return False
    try:
        der = base64.b64decode(body.encode("ascii"), validate=True)
    except (ValueError, TypeError):
        return False
    if base64.b64encode(der).decode("ascii") != body:
        return False
    point = ed25519_public_key_bytes(der)
    if point is None:
        return False
    return der == ED25519_SPKI_PREFIX + point


def _public_keys_in(document: Any) -> list[Any]:
    """Every `public_key_pem` member anywhere in a parsed document, in document order."""
    found: list[Any] = []
    stack: list[Any] = [document]
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            for name, value in node.items():
                if name == "public_key_pem":
                    found.append(value)
                elif isinstance(value, (dict, list)):
                    stack.append(value)
        elif isinstance(node, list):
            stack.extend(item for item in node if isinstance(item, (dict, list)))
    return found


def committed_fixture_key_material() -> dict[str, str]:
    """Public keys that are COMMITTED TO THIS REPOSITORY, derived, never hand-listed.

    Mapping: key identity (`public_key_identity`) -> the committed document it came from.

    HOW IT IS DERIVED: every `*.fixture.json` document sitting beside this module is
    parsed, and EVERY `public_key_pem` member anywhere inside it contributes its key —
    anchor documents, trust-root manifests, and any committed fixture document that lands
    later. Nothing is pasted in as a literal, so the set cannot drift away from the
    repository's own bytes. The `fixture_only` flag inside those documents is deliberately
    NOT consulted — it is the very field this refusal exists to stop trusting.

    THE SIGNING KEY CLASS (2026-08-15 fold): the harvest used to stop at
    `OwnerTrustAnchorV1` documents, which covered the ANCHOR class and left the SIGNING
    class open. A council seat took the committed Ed25519 test signing pair, made it the
    PRODUCTION measurement signing root under an INDEPENDENTLY generated owner anchor,
    and cleared production admission (`production_admission_errors = []`,
    `root_fixture_only = False`, `production_ready = True`,
    `root_is_committed_test_public = True`). The ceremony forbids exactly that
    (`MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md` §3 step 0 and §3 step 3: every key in a
    production manifest is generated in the ceremony, never copied out of a committed
    fixture document) — and prose is not a control, so the two authorities now consult
    this set for their production ROOTS as well as for the anchor.

    WHY: `MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md` section 3 step 0 is a human hand-writing
    an anchor document, and the obvious way to write one is to copy the committed
    example. Before this fold, editing two LABELS in that copy (`fixture_only` to false,
    a new `anchor_id`) produced a PRODUCTION root of trust whose private half is
    committed at `mbcx01_build_ceremony_fixture.py` and is therefore held by everyone
    holding this repository. That is MITRE CWE-1291 (public key re-used for signing debug
    and production material, PeerOf CWE-321), whose mitigation phase is Implementation
    — satisfied here, at context construction.

    This is an OPERATOR FOOTGUN guard, not an access-control boundary: MBCX-01 has no
    threat model, no API and no untrusted caller (`MBCX-01-BUILD-ADVERSARY-PREMISE-
    CORRECTION-2026-08-14.md`). It stops the experiment fooling ITSELF — an operator
    believing they hold the only copy of the root key when they hold a public one — and
    it says so in a named refusal instead of in a comment.

    SCOPE, stated rather than implied: it covers key material carried by committed
    `*.fixture.json` DOCUMENTS. A committed test PRIVATE key whose public half appears in
    no committed document (`mbcx01_build_ceremony_fixture.FIXTURE_NON_ANCHOR_PRIVATE_KEY_PEM`)
    is not in this set, because deriving a public key from a private one needs an Ed25519
    implementation this module does not have and will not grow for it. Nor are private
    keys pasted into TEST modules, unless their public half is published in a committed
    fixture document — which is how the committed measurement and state signing keys are
    in fact covered. Nobody reaches those keys by copying a file; the remainder is a
    NAMED, ACCEPTED gap rather than a silent one.
    """
    global _FIXTURE_KEY_MATERIAL
    if _FIXTURE_KEY_MATERIAL is not None:
        return dict(_FIXTURE_KEY_MATERIAL)
    directory = os.path.dirname(os.path.abspath(__file__))
    material: dict[str, str] = {}
    try:
        names = sorted(os.listdir(directory))
    except OSError:  # pragma: no cover - the module itself was loaded from here
        names = []
    for name in names:
        # r5 council, seat 1, EXECUTED: this used to read
        # `if not name.endswith(FIXTURE_DOCUMENT_SUFFIX): continue`, and that suffix was
        # the defect. `MBCX-01-R13-MEASUREMENT-TRUST-ROOTS.json` is committed, publishes a
        # `public_key_pem`, and has its PRIVATE half committed in the r12/r13 test modules
        # — yet it is not a `*.fixture.json`, so it was not refused and could sign
        # production measurement evidence. Third appearance of one class (committed anchor
        # key, committed test signing key, now this), so the close is a SUBTRACTION rather
        # than a longer list of filenames: every committed JSON document beside this module
        # publishes into the refused set. ⛔ Deliberately NOT a repository-wide key census —
        # this artifact has no adversary, only an operator who may copy a committed template
        # during the ceremony, and a scanner would be machinery for a phantom (owner ruling
        # 2026-08-15). RESIDUAL, named not chased: a key published only in prose (`.md`,
        # `.txt`) or in a witness-run bank is NOT in this set; the ceremony's own
        # generate-in-custody step is that case's control.
        if not name.endswith(".json"):
            continue
        try:
            with open(os.path.join(directory, name), encoding="utf-8") as stream:
                document = strict_json_document(stream.read())
        except (OSError, ValueError):
            continue
        if not isinstance(document, (dict, list)):
            continue
        for public_key_pem in _public_keys_in(document):
            identity = public_key_identity(public_key_pem)
            if identity:
                material.setdefault(identity, name)
    _FIXTURE_KEY_MATERIAL = material
    return dict(material)


def committed_fixture_key_document(public_key_pem: Any) -> str | None:
    """The committed fixture document a public key is published in, or None.

    The one question every production door asks about a key it is about to trust. It is
    a fact about the KEY (`public_key_identity`), so a re-encoded carrier or a re-wrapped
    DER envelope answers the same way as the verbatim committed bytes.
    """
    identity = public_key_identity(public_key_pem)
    if identity is None:
        return None
    return committed_fixture_key_material().get(identity)


def anchor_from_document(document: Any, *, source: str) -> OwnerTrustAnchor:
    """Build an anchor from an `OwnerTrustAnchorV1` document (closed key set)."""
    if not isinstance(document, dict) or set(document) != ANCHOR_KEYS:
        raise TrustAnchorError("OWNER_TRUST_ANCHOR_INVALID")
    if document.get("schema_id") != ANCHOR_SCHEMA_ID:
        raise TrustAnchorError("OWNER_TRUST_ANCHOR_INVALID")
    return OwnerTrustAnchor(
        anchor_id=document.get("anchor_id"),
        algorithm=document.get("algorithm"),
        public_key_pem=document.get("public_key_pem"),
        authorities=document.get("authorities"),
        minimum_activation_generation=document.get("minimum_activation_generation"),
        fixture_only=document.get("fixture_only"),
        source=source)


def load_owner_trust_anchor(path: str) -> OwnerTrustAnchor:
    """Load the anchor document the OPERATOR placed at `path` (strict parse)."""
    try:
        with open(path, encoding="utf-8") as stream:
            text = stream.read()
    except OSError as exc:
        raise TrustAnchorError("OWNER_TRUST_ANCHOR_UNREADABLE:%s" % path) from exc
    try:
        document = strict_json_document(text)
    except _AmbiguousDocument as exc:
        raise TrustAnchorError("OWNER_TRUST_ANCHOR_AMBIGUOUS:%s" % path) from exc
    except ValueError as exc:
        raise TrustAnchorError("OWNER_TRUST_ANCHOR_UNREADABLE:%s" % path) from exc
    return anchor_from_document(document, source=str(path))


def _coerce_anchor(anchor: Any) -> OwnerTrustAnchor:
    if isinstance(anchor, str):
        anchor = load_owner_trust_anchor(anchor)
    elif isinstance(anchor, dict):
        anchor = anchor_from_document(anchor, source="INJECTED_DOCUMENT")
    if not isinstance(anchor, OwnerTrustAnchor):
        raise TrustAnchorError("OWNER_TRUST_ANCHOR_INVALID")
    return anchor


def new_production_verifier_context(anchor: Any, *, current_time: Any = None,
                                    source: str = "OPERATOR_WIRING"
                                    ) -> ProductionVerifierContext:
    """OPERATOR side: build the immutable context from an anchor, path or document."""
    return ProductionVerifierContext(anchor=_coerce_anchor(anchor),
                                     current_time=current_time, source=source)


def configure_owner_trust_anchor(anchor: Any, *,
                                 current_time: Any = None) -> OwnerTrustAnchor:
    """Operator wiring: install the process anchor (an object, document or config path).

    Retained as the thin backward-compatible entry point. Installing a `fixture_only`
    anchor is ALLOWED — a fixture lane must be able to say what root it is reading — but
    it installs NO production context, so every production door refuses it by name
    (`ANCHOR_FIXTURE_ONLY`). That is the r2 fix class in one line: labelling test
    material as the root of trust is not an error, GRANTING production authority to it
    is, and the refusal is at the authority, not at the label.
    """
    global _INSTALLED_WIRING
    anchor = _coerce_anchor(anchor)
    context = None if anchor.fixture_only else ProductionVerifierContext(
        anchor=anchor, current_time=current_time, source=anchor.source)
    _INSTALLED_WIRING = _OperatorWiring(anchor, context)
    return anchor


def configure_production_verifier_context(
        context: Any) -> ProductionVerifierContext:
    """Operator wiring, context-first: install an already-constructed context."""
    global _INSTALLED_WIRING
    if not isinstance(context, ProductionVerifierContext):
        raise TrustAnchorError("PRODUCTION_VERIFIER_CONTEXT_INVALID")
    _INSTALLED_WIRING = _OperatorWiring(context.anchor, context)
    return context


@contextlib.contextmanager
def installed_production_verifier(anchor_or_context: Any, *, current_time: Any = None):
    """Operator wiring for the LENGTH OF A SCOPE, restored on exit.

    This is what a fixture ASSEMBLER uses. Codex r2 F3 is exactly the absence of it:
    `mbcx01_build_integration` installed the fixture anchor process-wide and never put
    back what the operator had, so every later verification in that process ran under a
    root the operator never chose.
    """
    global _INSTALLED_WIRING
    saved = _INSTALLED_WIRING
    try:
        if isinstance(anchor_or_context, ProductionVerifierContext):
            yield configure_production_verifier_context(anchor_or_context)
        else:
            configure_owner_trust_anchor(anchor_or_context, current_time=current_time)
            yield None if _INSTALLED_WIRING is None else _INSTALLED_WIRING.context
    finally:
        _INSTALLED_WIRING = saved


def clear_owner_trust_anchor() -> None:
    """Remove the process wiring. Verification then FAILS CLOSED, never open."""
    global _INSTALLED_WIRING
    _INSTALLED_WIRING = None


def resolve_owner_trust_anchor(authority: str) -> OwnerTrustAnchor | None:
    """The ANCHOR for `authority`, from operator wiring or OS configuration, or None.

    Inspection and diagnostics only: it answers "what root did the operator install",
    including a fixture one. Production admission does NOT go through here — it goes
    through `resolve_production_verifier_context`, which is where fixture material is
    refused. Resolution order is fixed: explicit process wiring first, then the
    `MBCX01_BUILD_OWNER_TRUST_ANCHOR` path. A malformed or unreadable anchor is NOT
    silently downgraded to "no anchor" — it raises, because an operator who configured
    an anchor and got a typo must not be told "unanchored" in a log line.
    """
    wiring = _INSTALLED_WIRING
    anchor = wiring.anchor if wiring is not None else None
    if anchor is None:
        path = os.environ.get(ANCHOR_PATH_ENV)
        if path:
            anchor = load_owner_trust_anchor(path)
    if anchor is None or authority not in anchor.authorities:
        return None
    return anchor


def resolve_production_verifier_context(
        authority: str) -> tuple[ProductionVerifierContext | None, str | None]:
    """THE single resolution point for production verification.

    Returns `(context, None)` for the one thing production verification accepts, or
    `(None, code)` — `ANCHOR_UNAVAILABLE` or `ANCHOR_FIXTURE_ONLY` — for everything
    else. Each production door calls this ONCE, at entry, BEFORE it reads any
    caller-supplied object, and threads the returned immutable value through the whole
    evaluation. Nothing that runs later in that evaluation can change the answer.
    """
    wiring = _INSTALLED_WIRING
    if wiring is None:
        path = os.environ.get(ANCHOR_PATH_ENV)
        if not path:
            return None, ANCHOR_UNAVAILABLE
        anchor = load_owner_trust_anchor(path)
        if anchor.fixture_only:
            return None, ANCHOR_FIXTURE_ONLY
        context = ProductionVerifierContext(anchor=anchor, source=str(path))
    elif wiring.context is None:
        return None, ANCHOR_FIXTURE_ONLY
    else:
        context = wiring.context
    if not context.authorizes(authority):
        return None, ANCHOR_UNAVAILABLE
    return context, None


def strict_signature_carrier_ok(value: Any, *, expected_bytes: int = SIGNATURE_BYTES) -> bool:
    """Canonical base64 carrier check (MBCX01-BUILD-R1-SIGNATURE-CARRIER / codex F6).

    Node's `Buffer.from(value, "base64")` ignores whitespace and also accepts the
    base64url alphabet, so many carrier strings decode to one signature and a receipt
    has no single identity for dedup or audit. Grammar + padding + length + a
    decode/re-encode equality check make the mapping one-to-one, and it runs BEFORE any
    cryptographic verification.
    """
    if not isinstance(value, str) or STRICT_BASE64_RE.fullmatch(value) is None:
        return False
    if len(value) % 4 != 0:
        return False
    try:
        raw = base64.b64decode(value.encode("ascii"), validate=True)
    except (ValueError, TypeError):
        return False
    if expected_bytes is not None and len(raw) != expected_bytes:
        return False
    return base64.b64encode(raw).decode("ascii") == value


def invoke_signature_verifier(items: list[dict[str, str]]) -> list[bool]:
    """Shell out to the BUILD-side strict Ed25519 verifier (never edited, only invoked)."""
    try:
        process = subprocess.run(
            ["node", SIGNATURE_VERIFIER], input=json.dumps({"items": items}), text=True,
            capture_output=True, timeout=20, check=False)
        reply = json.loads(process.stdout)
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        raise TrustAnchorError("OWNER_ACTIVATION_VERIFIER_UNAVAILABLE") from exc
    if process.returncode != 0 or not isinstance(reply, dict) or reply.get("ok") is not True:
        raise TrustAnchorError("OWNER_ACTIVATION_VERIFIER_FAILED")
    valid = reply.get("valid")
    if not isinstance(valid, list) or len(valid) != len(items):
        raise TrustAnchorError("OWNER_ACTIVATION_VERIFIER_RESPONSE_INVALID")
    return [value is True for value in valid]


def activation_signed_region(statement: dict[str, Any]) -> dict[str, Any]:
    """The signed region of an activation statement: everything except the carrier."""
    return {key: value for key, value in statement.items()
            if key not in ACTIVATION_UNSIGNED_KEYS}


def activation_preimage_b64(statement: dict[str, Any]) -> str:
    return base64.b64encode(
        common.canonical_json(activation_signed_region(statement))).decode("ascii")


def manifest_activation_digest(manifest: Any) -> str:
    """SHA-384 over the canonical bytes of the ENTIRE manifest document."""
    return common.sha384(manifest)


def authenticate_production_activation(statement: Any, *,
                                       context: Any,
                                       authority: str,
                                       manifest: Any,
                                       manifest_validity: Any,
                                       signing_key_id: Any,
                                       editor_key_ids: Any,
                                       custody_evidence_digests: Any,
                                       provenance_digest: Any) -> str | None:
    """Authenticate one production activation against the verifier's OWN context.

    `context` is the immutable `ProductionVerifierContext` the calling authority
    resolved ONCE at entry (r2 fix class). It is a REQUIRED keyword: there is no path
    through this function that reads process state, so nothing that runs during an
    evaluation can substitute the root of trust, and no caller can reach an
    authentication that begins from an anchor the operator did not install.

    Returns `None` when the activation is authentic and binds EXACTLY this manifest and
    this custody set, or one of `ANCHOR_UNAVAILABLE` / `ANCHOR_FIXTURE_ONLY` /
    `SIGNATURE_CARRIER_INVALID` / `ACTIVATION_UNAUTHENTICATED`. There is deliberately ONE
    failure code for the whole authentication class: an attacker learns "this did not
    authenticate", not which of fourteen bindings to grind next, and the reviewer has one
    invariant to check.
    """
    if authority not in AUTHORITIES:
        raise TrustAnchorError("OWNER_ACTIVATION_AUTHORITY_UNKNOWN:%s" % (authority,))
    if context is None:
        return ANCHOR_UNAVAILABLE
    if not isinstance(context, ProductionVerifierContext):
        raise TrustAnchorError("PRODUCTION_VERIFIER_CONTEXT_INVALID")
    anchor = context.anchor
    # Defence in depth: a context cannot be built around a fixture anchor, so this
    # cannot fire — and it is checked anyway, because the whole finding was a flag that
    # was parsed and never consulted.
    if anchor.fixture_only is not False:
        return ANCHOR_FIXTURE_ONLY
    if not context.authorizes(authority):
        return ANCHOR_UNAVAILABLE
    if not isinstance(statement, dict) or set(statement) != ACTIVATION_KEYS:
        return ACTIVATION_UNAUTHENTICATED
    if not strict_signature_carrier_ok(statement.get("signature_b64")):
        return SIGNATURE_CARRIER_INVALID
    generation = statement.get("activation_generation")
    if (statement.get("schema_id") != ACTIVATION_SCHEMA_ID
            or statement.get("anchor_id") != anchor.anchor_id
            or statement.get("authority") != authority
            or not isinstance(generation, int) or isinstance(generation, bool)
            or generation < anchor.minimum_activation_generation
            or statement.get("manifest_digest") != manifest_activation_digest(manifest)
            or statement.get("manifest_validity") != manifest_validity
            or statement.get("authorized_signing_key_id") != signing_key_id
            or not isinstance(statement.get("authorized_editor_key_ids"), list)
            or sorted(statement["authorized_editor_key_ids"]) != sorted(editor_key_ids)
            or statement.get("custody_evidence_digests") != custody_evidence_digests
            or statement.get("provenance_digest") != provenance_digest):
        return ACTIVATION_UNAUTHENTICATED
    try:
        valid = invoke_signature_verifier([{
            "payload_b64": activation_preimage_b64(statement),
            "public_key_pem": anchor.public_key_pem,
            "signature_b64": statement["signature_b64"],
        }])
    except TrustAnchorError:
        # A verifier that cannot run is never an admission.
        return ACTIVATION_UNAUTHENTICATED
    return None if valid[0] else ACTIVATION_UNAUTHENTICATED
