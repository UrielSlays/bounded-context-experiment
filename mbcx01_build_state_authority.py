"""BUILD A — `StateAuthorityReceiptV2` verifier + production admission (GREEN STAGE).

This is the ONLY new entry point into scientific admission. It never edits, patches, or
monkeypatches the frozen r13.2 path: `mbcx01_r13_packets.validate_scorer_input` runs in
full, with production semantics, on every call.

The non-weakening admission shape (BUILD design notes §2):

  1. run the FROZEN `validate_scorer_input(..., require_production_authority=True)` and
     collect its error set E_prod — nothing is bypassed;
  2. verify the `StateAuthorityReceiptV2` fully (closed schema, store identity from the
     INJECTED manifest, Ed25519 signature against the INJECTED trust-root manifest, custody
     disjointness, validity/revocation, anti-replay identity, reader != writer identity,
     durable terminal, dual-reducer replay of ITS bytes through frozen `reference_apply` /
     `oracle_apply`);
  3. BYTE-BIND the V2 evidence to the graph the frozen path validated (prestate /
     proposal / child / readback `state_utf8` / `event_utf8` bytes, hashes and cuts must
     equal the scorer input's `transition_authority` and its embedded fixture receipt
     exactly);
  4. discharge is subtractive and exact: the named sentinel `STATE_AUTHORITY_UNAVAILABLE`
     is removed ONLY when steps 2 AND 3 are fully clean, and any V2 defect keeps the
     sentinel AND adds the named V2 error.

r1 FIX CLASS — AUTHENTICATED_PRODUCTION_TRUST_BOOTSTRAP
-------------------------------------------------------
Step 2 above says "the INJECTED trust-root manifest". BUILD acceptance council r1 found
that "injected" was doing work it could not do: the manifest and the custody evidence
arrive as per-request PARAMETERS, and before this fold nothing tied either of them to
anything the api-caller could not author. A fresh attacker key plus an invented manifest
and invented custody digests verified clean (SEAT3 F1, EXECUTED). Verification now
begins from a VERIFIER-CONTROLLED root of trust, per SLSA v1.2 "Verifying artifacts"
step 1 and TUF §§2.1/5.3: the owner anchor that `mbcx01_build_trust_anchor` loads from
OPERATOR wiring or OS configuration — never from the request — must have SIGNED an
activation statement binding the exact canonical digest of this manifest and the whole
custody set (`_activation_errors`). Both defects r1 named are closed by that one
invariant: the fixture-shaped self-authored root is no longer ACCEPTED, and the ceremony
spec's own production-shaped manifest is no longer REFUSED (`manifest_shape`).

Discharge formula (driver-adjudicated, byte-reproduced on this tree)
--------------------------------------------------------------------
`E_prod = validate_scorer_input(..., require_production_authority=True)` and
`E_fix  = validate_scorer_input(..., require_production_authority=False)` are BOTH run —
the frozen validator, unmodified, twice. Nothing is ever removed from `E_fix`.

  * If `V2_errors` is empty AND byte binding is clean AND
    `set(E_prod) - set(E_fix) ⊆ SENTINEL_CASCADE_CLOSURE`, the answer is
    `sorted(set(E_fix))` — i.e. exactly the frozen verdict with the sentinel and its
    mechanical cascade discharged, and every other frozen error preserved.
  * Otherwise the answer is `sorted(set(E_prod) | set(V2_errors))` — the frozen production
    verdict (sentinel intact) plus the named V2 rejection.

`SENTINEL_CASCADE_CLOSURE` is the byte-reproduced closure of the sentinel inside the
frozen validator, not a guess:
  * `mbcx01_r13_packets.py:544` — `validate_manifest_cut_state_receipt` adds
    `STATE_AUTHORITY_UNAVAILABLE` unconditionally when `require_production=True`;
  * `mbcx01_r13_packets.py:1043` — that non-empty error set forces `expected_a0 = None`,
    so `a0_packet != expected_a0` adds `A0_PACKET_INVALID` at `:1044-1045`;
  * `mbcx01_r13_packets.py:917-918` — invariant `I02` conjoins `not manifest_cut_errors`
    and both frozen state-authority verdicts, so it flips false and yields
    `I02_INVARIANT_INVALID`.
On this tree the measured difference is exactly
`{'A0_PACKET_INVALID', 'I02_INVARIANT_INVALID', 'STATE_AUTHORITY_UNAVAILABLE'}` with
`E_fix == []`. The guard is a SUBSET test: if the frozen path ever grows a
production-only error outside that closure, the formula refuses to discharge and returns
the production verdict instead of silently absorbing the new error.

Anchors used by `verify_state_authority_receipt_v2` (it receives NO identity config)
------------------------------------------------------------------------------------
Nothing in the anti-replay / identity block is free-floating; every axis is a function of
an independently anchored value, so a re-signed receipt with one axis changed is a named
replay rejection rather than a new authority:

  * `transaction_commit_id`  -> the DURABLE store named by the receipt's store identity
    (`mbcx01_build_state_store.transaction_terminal`): unknown transaction is a transaction
    IDENTITY failure, a known-but-not-`COMMITTED` transaction is a commit failure;
  * `store_identity`         -> the INJECTED manifest's `store_binding`;
  * `producer_id` / `producer_role` / `subject_identity` / key validity / revocation
                             -> the INJECTED manifest's root row for `signer_key_id`;
  * `scope_id`               -> the scopes actually carried by the receipt's own state
    bytes (a receipt cannot claim a scope its bytes do not contain);
  * `scope_id` / `scenario_id` / `run_id` / `receipt_nonce` / `subject_identity`
                             -> BYTE-EQUAL to the anti-replay anchor set persisted in
    the DURABLE journal row at commit time (`mbcx01_build_state_store.ANTI_REPLAY_KEYS`,
    FOLD 1). They are not re-derived from the receipt's own labels: a value the holder
    of the receipt can recompute from a label it already controls is not an anchor, and
    label transforms cannot express a production run whose scenario, run and nonce are
    independent identifiers.

The validity window is evaluated at the AUTHORITY INSTANT the receipt itself attests (the
readback cut's `knowledge_time`), not at wall-clock time: a deterministic verifier must not
change its verdict because a year passed.

Nothing here can be reached by a fixture receipt: `StateAuthorityReceiptV1` cannot express
production at all (`mbcx01_r13_common.py:303-305`, `:366-370`), and the frozen verifiers
append the sentinel unconditionally (`mbcx01_r13_state_reference.py:487`,
`mbcx01_r13_state_oracle.py:725`, `mbcx01_r13_packets.py:544`).
"""

from __future__ import annotations

import base64
import copy
import datetime
import json
import os
import subprocess
from typing import Any

import mbcx01_r13_common as common
import mbcx01_r13_packets as packets
import mbcx01_r13_state_oracle as oracle
import mbcx01_r13_state_reference as reference

import mbcx01_build_state_store as store_mod
import mbcx01_build_trust_anchor as trust_anchor


#: The one frozen sentinel this module may ever discharge, and only with strictly
#: stronger evidence bound to the same bytes.
STATE_AUTHORITY_SENTINEL = "STATE_AUTHORITY_UNAVAILABLE"

#: Byte-reproduced closure of the sentinel inside the frozen validator (see module docstring).
SENTINEL_CASCADE_CLOSURE = frozenset({
    STATE_AUTHORITY_SENTINEL, "A0_PACKET_INVALID", "I02_INVARIANT_INVALID",
})

STATE_AUTHORITY_V2_SCHEMA_ID = "StateAuthorityReceiptV2"
STATE_AUTHORITY_V2_DOMAIN = "MBCX01.STATE.AUTHORITY"
STATE_AUTHORITY_V2_VERSION = 2
AUTHORITY_MODE_PRODUCTION = "PRODUCTION"
AUTHORITY_MODE_FIXTURE = "FIXTURE_CONFORMANCE"
SIGNATURE_ALGORITHM = "ED25519"

#: Closed key sets for the V2 receipt (BUILD design notes §2 field plan; handoff r13.2
#: lines 151-172). Any addition is a re-version, never an edit.
V2_TOP_KEYS = {
    "schema_id", "authority_mode", "domain", "version", "store_identity",
    "transaction_commit_id", "prestate_read", "proposal_persistence", "applied_child",
    "postcommit_readback", "signer_identity", "anti_replay",
    "receipt_preimage_b64", "signature_b64", "receipt_digest",
}
V2_STORE_KEYS = {"store_id", "namespace", "namespace_version"}
V2_PRESTATE_KEYS = {"read_id", "state_utf8", "state_hash", "cut"}
V2_PROPOSAL_KEYS = {"event_id", "event_utf8", "event_hash", "persistence_identity"}
V2_CHILD_KEYS = {"event_id", "event_utf8", "event_hash", "next_sequence"}
V2_READBACK_KEYS = {"read_id", "state_utf8", "state_hash", "cut", "reader_identity"}
V2_SIGNER_KEYS = {
    "producer_id", "producer_role", "signer_key_id", "signature_algorithm",
    "trust_root_id", "trust_policy_digest", "validity_not_before", "validity_not_after",
    "revocation_state", "subject_identity",
}
V2_ANTI_REPLAY_KEYS = {
    "receipt_nonce", "scope_id", "scenario_id", "run_id", "transaction_commit_id",
}
#: The signed region: everything except the signature carrier fields.
V2_UNSIGNED_KEYS = {"receipt_preimage_b64", "signature_b64", "receipt_digest"}
V2_CUT_KEYS = {"journal_seq", "knowledge_time", "valid_time"}

#: The keys the FROZEN layer DEREFERENCES on a state object, and therefore the shape a
#: receipt's `state_utf8` bytes must carry before any later check touches them:
#: `mbcx01_r13_common.current_cut` (:109-112) reads `next_seq` and `last_observed_at`,
#: both frozen reducers read `events` / `idempotency` / `scopes` / `responses`
#: (`mbcx01_r13_state_reference.py:33-37,95`, `mbcx01_r13_state_oracle.py:49-52,156,537`),
#: and `_anti_replay_errors` / `_semantic_errors` below read the same set.
#: A SUBSET test, deliberately: a state carrying MORE than this is still a state.
V2_STATE_REQUIRED_KEYS = ("events", "idempotency", "last_observed_at", "next_seq",
                          "responses", "scopes")

#: The two RFC-3339 UTC spellings this module has to ORDER AGAINST EACH OTHER: the
#: state layer's six-fractional-digit instant (`mbcx01_r13_common.UTC`, :71 — the
#: spelling every manifest validity value and every cut `knowledge_time` carries) and
#: the WHOLE-SECOND instant a verifier context emits
#: (`mbcx01_build_trust_anchor.INSTANT_RE` :231, `ProductionVerifierContext.current_instant`
#: :445-450). Lexically `'Z'` (0x5A) sorts AFTER `'.'` (0x2E), so `...00.500000Z` read
#: EXPIRED at `...00Z` and a legal window refused right evidence up to a second early
#: (codex r5 P2). Both spellings are parsed to instants before any comparison.
STATE_INSTANT_FORMS = ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ")

ROLE_STATE_OWNER_WRITER = "STATE_OWNER_WRITER"
ROLE_STATE_READBACK_READER = "STATE_READBACK_READER"

TRUST_ROOT_MANIFEST_SCHEMA_ID = "StateTrustRootManifestV1"
TRUST_POLICY_SCHEMA_ID = "ProductionStateTrustPolicyV1"
TRUST_POLICY_STATUS_NOT_ACTIVATED = "NOT_ACTIVATED"
TRUST_POLICY_STATUS_ACTIVATED = "ACTIVATED"
REVOCATION_NOT_REVOKED = "NOT_REVOKED"
REQUIRED_EXTERNAL_EVIDENCE = (
    "SEPARATE_STATE_KEY_CUSTODY_ATTESTATION", "SEPARATE_TRUST_ROOT_EDITOR_APPROVAL",
    "STATE_STORE_BUILD_PROVENANCE", "PRODUCTION_SIGNING_CEREMONY_RECEIPT",
)
#: The four custody digest fields, in the order of `REQUIRED_EXTERNAL_EVIDENCE`.
CUSTODY_DIGEST_FIELDS = (
    ("SEPARATE_STATE_KEY_CUSTODY_ATTESTATION", "key_custody_attestation_digest"),
    ("SEPARATE_TRUST_ROOT_EDITOR_APPROVAL", "root_editor_approval_digest"),
    ("STATE_STORE_BUILD_PROVENANCE", "store_build_provenance_digest"),
    ("PRODUCTION_SIGNING_CEREMONY_RECEIPT", "signing_ceremony_receipt_digest"),
)
#: The owner-signed activation statement (r1 fix class). Presented by the caller like
#: everything else in the custody set — and authenticated against an anchor the caller
#: cannot supply (`mbcx01_build_trust_anchor`).
OWNER_ACTIVATION_EVIDENCE = "owner_ceremony_activation"
CUSTODY_EVIDENCE_KEYS = {
    "signer_custodian_role", "trust_root_editor_role", "signer_key_ids",
    "root_editor_key_ids", "key_custody_attestation_digest",
    "root_editor_approval_digest", "store_build_provenance_digest",
    "signing_ceremony_receipt_digest", OWNER_ACTIVATION_EVIDENCE,
}

#: Ed25519 verifier contract: {"items":[{payload_b64, public_key_pem, signature_b64}]}
#: -> {"ok": true, "valid": [bool]}. Never edited; only invoked. This is the BUILD-side
#: STRICT-carrier sibling of the frozen `verify-r13-receipt-signature.mjs` (which is
#: untouched and still serves the frozen r13.2 suites): same contract, plus canonical
#: base64 grammar/padding/length + decode/re-encode equality before verification
#: (MBCX01-BUILD-R1-SIGNATURE-CARRIER / codex F6).
SIGNATURE_VERIFIER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "verify-build-receipt-signature.mjs")

#: Named rejection codes. Each is the deliverable of one adversarial witness.
STATE_AUTHORITY_V2_SCHEMA_INVALID = "STATE_AUTHORITY_V2_SCHEMA_INVALID"
STATE_AUTHORITY_V2_CANONICAL_BYTES_INVALID = "STATE_AUTHORITY_V2_CANONICAL_BYTES_INVALID"
STATE_AUTHORITY_V2_HASH_INVALID = "STATE_AUTHORITY_V2_HASH_INVALID"
STATE_AUTHORITY_V2_ROOT_NOT_TRUSTED = "STATE_AUTHORITY_V2_ROOT_NOT_TRUSTED"
STATE_AUTHORITY_V2_SIGNATURE_INVALID = "STATE_AUTHORITY_V2_SIGNATURE_INVALID"
STATE_AUTHORITY_V2_ROOT_SELF_AUTHORED = "STATE_AUTHORITY_V2_ROOT_SELF_AUTHORED"
STATE_AUTHORITY_V2_CUSTODY_SEPARATION_INVALID = "STATE_AUTHORITY_V2_CUSTODY_SEPARATION_INVALID"
STATE_AUTHORITY_V2_ROLE_NOT_AUTHORIZED = "STATE_AUTHORITY_V2_ROLE_NOT_AUTHORIZED"
STATE_AUTHORITY_V2_KEY_REVOKED_OR_EXPIRED = "STATE_AUTHORITY_V2_KEY_REVOKED_OR_EXPIRED"
STATE_AUTHORITY_V2_READER_NOT_INDEPENDENT = "STATE_AUTHORITY_V2_READER_NOT_INDEPENDENT"
STATE_AUTHORITY_V2_STORE_IDENTITY_MISMATCH = "STATE_AUTHORITY_V2_STORE_IDENTITY_MISMATCH"
STATE_AUTHORITY_V2_TRANSACTION_IDENTITY_MISMATCH = "STATE_AUTHORITY_V2_TRANSACTION_IDENTITY_MISMATCH"
STATE_AUTHORITY_V2_CUT_INVALID = "STATE_AUTHORITY_V2_CUT_INVALID"
STATE_AUTHORITY_V2_EVENT_SUBSTITUTION = "STATE_AUTHORITY_V2_EVENT_SUBSTITUTION"
STATE_AUTHORITY_V2_SEQUENCE_INVALID = "STATE_AUTHORITY_V2_SEQUENCE_INVALID"
STATE_AUTHORITY_V2_STATE_SUBSTITUTION = "STATE_AUTHORITY_V2_STATE_SUBSTITUTION"
STATE_AUTHORITY_V2_REPLAY_IDENTITY_INVALID = "STATE_AUTHORITY_V2_REPLAY_IDENTITY_INVALID"
STATE_AUTHORITY_V2_TRANSACTION_NOT_COMMITTED = "STATE_AUTHORITY_V2_TRANSACTION_NOT_COMMITTED"
STATE_AUTHORITY_V2_REDUCER_DISAGREEMENT = "STATE_AUTHORITY_V2_REDUCER_DISAGREEMENT"
STATE_AUTHORITY_V2_OPERATOR_DISAGREEMENT = "STATE_AUTHORITY_V2_OPERATOR_DISAGREEMENT"
STATE_AUTHORITY_V2_BYTE_BINDING_MISMATCH = "STATE_AUTHORITY_V2_BYTE_BINDING_MISMATCH"
#: r1 fix class AUTHENTICATED_PRODUCTION_TRUST_BOOTSTRAP.
STATE_AUTHORITY_V2_TRUST_ANCHOR_UNAVAILABLE = "STATE_AUTHORITY_V2_TRUST_ANCHOR_UNAVAILABLE"
STATE_AUTHORITY_V2_ACTIVATION_UNAUTHENTICATED = "STATE_AUTHORITY_V2_ACTIVATION_UNAUTHENTICATED"
STATE_AUTHORITY_V2_SIGNATURE_CARRIER_INVALID = "STATE_AUTHORITY_V2_SIGNATURE_CARRIER_INVALID"
#: r2 fix class FIXTURE_ISOLATION: the operator wired a FIXTURE anchor. Anchor-class,
#: like `..._TRUST_ANCHOR_UNAVAILABLE`, and deliberately not folded into the single
#: authentication code.
STATE_AUTHORITY_V2_TRUST_ANCHOR_FIXTURE_ONLY = "STATE_AUTHORITY_V2_TRUST_ANCHOR_FIXTURE_ONLY"
#: 2026-08-15 fold: a production-shaped manifest whose SIGNING roots are key material
#: COMMITTED to this repository. The anchor class of this refusal is the line above; this
#: is the signing class, which a council seat executed on the measurement plane and which
#: has the identical shape here. Its own code, because "your test key is not a production
#: key" is a different fact from "this manifest is not a trusted root".
STATE_AUTHORITY_V2_SIGNING_KEY_FIXTURE_MATERIAL = (
    "STATE_AUTHORITY_V2_SIGNING_KEY_FIXTURE_MATERIAL")
#: r3 fold: the signature could not be CHECKED — malformed root key material in the
#: injected manifest, no Node runtime, a verifier timeout, or a reply that is not the
#: closed verifier contract. Deliberately NOT `..._SIGNATURE_INVALID`: "this signature
#: was not verified" is a different fact from "this signature is wrong", and an
#: instrument that reports the second when it means the first is reporting a wrong
#: number. Both refuse, and both keep `STATE_AUTHORITY_UNAVAILABLE`.
STATE_AUTHORITY_V2_SIGNATURE_VERIFIER_UNAVAILABLE = (
    "STATE_AUTHORITY_V2_SIGNATURE_VERIFIER_UNAVAILABLE")


class StateAuthorityError(ValueError):
    """Closed, fail-loud production state-authority error."""


#: The exception classes a MALFORMED CALLER INPUT produces when it reaches code that
#: expected a well-formed one: an absent key, an index off the end, an attribute a
#: scalar does not have, an unhashable or wrongly-typed value, an exhausted iterator,
#: a text value that will not decode. This is the same enumeration the lane's shelf
#: pattern uses (`mbcx01_build_cohort_packet.verify_build_scorer_input`'s
#: `frozen_verdict`, :1010-1025 — "a gate that crashes is not a gate").
#:
#: ⚠ IT IS DELIBERATELY NOT `Exception`. An `AssertionError`, a `MemoryError`, a
#: `RecursionError` or any other class outside this tuple is THIS MODULE'S OWN
#: DEFECT, and a verifier that converted its own bugs into a caller-shaped refusal
#: would be reporting a wrong number about itself. Those still fault loud.
MALFORMED_CALLER_INPUT_EXCEPTIONS = (AttributeError, IndexError, KeyError,
                                     StopIteration, TypeError, UnicodeError,
                                     ValueError)


# ---- small helpers ---------------------------------------------------------------


def parse_instant(value: Any) -> datetime.datetime | None:
    """The UTC CALENDAR instant `value` denotes, or `None` when it denotes none.

    Accepts either spelling in `STATE_INSTANT_FORMS` and requires the parse to
    ROUND-TRIP to the original text, so `2026-02-30T00:00:00.000000Z` and a
    three-fractional-digit spelling are both refusals rather than values that get
    ordered anyway. Mechanism adopted from the frozen `mbcx01_r13_common._valid_utc`
    (:119-126); `mbcx01_build_measurement_authority.parse_instant` is the
    measurement-plane sibling (whole seconds only, that plane's one document spelling).
    The helper is duplicated rather than shared because the two planes accept
    DIFFERENT spellings, and widening either grammar to reach one helper would weaken
    a document format; the two are kept in step by this cross-reference.
    """
    if not isinstance(value, str):
        return None
    for form in STATE_INSTANT_FORMS:
        try:
            parsed = datetime.datetime.strptime(value, form)
        except ValueError:
            continue
        if parsed.strftime(form) == value:
            return parsed.replace(tzinfo=datetime.timezone.utc)
    return None


def _is_state_shaped(value: Any) -> bool:
    """Is this parsed object a STATE, and not merely a dict?

    Canonical `{}` is a dict, and before this guard it rode through `_structural_errors`
    as NON-fatal and then raised `KeyError('next_seq')` out of `common.current_cut`
    inside `_semantic_errors` — a raw traceback out of a public verifier that advertises
    a CLOSED ERROR LIST for every input (codex r5 P2). The posture is unchanged: such a
    receipt never verified; the refusal is now named.

    A SCOPE MAP WHOSE VALUES ARE NOT SCOPES IS NOT A STATE EITHER (codex-CLI r6 SEAT1
    F3). The r5 guard tested `scopes` ONE level deep, so `{"SCOPE.SHARED": null}` was
    "a dict" and rode through to the frozen reducers, where `scope["obligations"]`
    raised `TypeError: 'NoneType' object is not subscriptable`
    (`mbcx01_r13_state_reference.py:129`). Both frozen reducers index every scope, so a
    non-dict scope value can never be a state this verifier could judge. This is the
    SPECIFIC refusal for that shape; the CLASS is closed at the public boundary
    (`verify_state_authority_receipt_v2`), which is what makes the next unanticipated
    shape a named refusal too rather than the next round's finding.
    """
    if not isinstance(value, dict):
        return False
    if any(key not in value for key in V2_STATE_REQUIRED_KEYS):
        return False
    return (isinstance(value["next_seq"], int) and not isinstance(value["next_seq"], bool)
            and isinstance(value["last_observed_at"], str)
            and isinstance(value["scopes"], dict)
            and all(isinstance(scope, dict) for scope in value["scopes"].values())
            and isinstance(value["events"], dict)
            and isinstance(value["idempotency"], dict)
            and isinstance(value["responses"], list))


def _canonical_content(receipt: dict[str, Any]) -> dict[str, Any]:
    """The signed region of a receipt: everything except the signature carrier fields."""
    return {key: value for key, value in receipt.items() if key not in V2_UNSIGNED_KEYS}


def _invoke_signature_verifier(items: list[dict[str, str]]) -> list[bool]:
    """Shell out to the frozen Ed25519 verifier (`verify-r13-receipt-signature.mjs`)."""
    request = {"items": items}
    try:
        process = subprocess.run(
            ["node", SIGNATURE_VERIFIER], input=json.dumps(request), text=True,
            capture_output=True, timeout=20, check=False)
        reply = json.loads(process.stdout)
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        raise StateAuthorityError("receipt signature verifier unavailable") from exc
    if process.returncode != 0 or not isinstance(reply, dict) or reply.get("ok") is not True:
        raise StateAuthorityError("receipt signature operation failed")
    valid = reply.get("valid")
    if not isinstance(valid, list) or len(valid) != len(items):
        raise StateAuthorityError("receipt signature verifier response invalid")
    return [value is True for value in valid]


def _structural_errors(receipt: Any) -> tuple[list[str], bool]:
    """Closed key sets + canonical bytes + hashes.

    Returns `(errors, fatal)`. `fatal` marks a receipt whose SHAPE cannot carry the later
    checks (unusable key sets, unparseable canonical bytes, unusable cuts) — only those
    short-circuit. A merely WRONG value (a repaired hash, a stale preimage, a mutated
    field) is never fatal: the signature check must still run and still name itself.
    """
    if not isinstance(receipt, dict) or set(receipt) != V2_TOP_KEYS:
        return [STATE_AUTHORITY_V2_SCHEMA_INVALID], True
    errors: list[str] = []
    blocks = (("store_identity", V2_STORE_KEYS), ("prestate_read", V2_PRESTATE_KEYS),
              ("proposal_persistence", V2_PROPOSAL_KEYS), ("applied_child", V2_CHILD_KEYS),
              ("postcommit_readback", V2_READBACK_KEYS), ("signer_identity", V2_SIGNER_KEYS),
              ("anti_replay", V2_ANTI_REPLAY_KEYS))
    for name, keys in blocks:
        block = receipt.get(name)
        if not isinstance(block, dict) or set(block) != keys:
            errors.append(STATE_AUTHORITY_V2_SCHEMA_INVALID)
    if errors:
        return errors, True
    # Bytes/cuts the later checks dereference: unusable shapes are FATAL and stop here.
    fatal: list[str] = []
    for name in ("prestate_read", "postcommit_readback"):
        row, cut = receipt[name], receipt[name].get("cut")
        if (not isinstance(cut, dict) or set(cut) != V2_CUT_KEYS
                or not isinstance(cut.get("journal_seq"), int)
                or isinstance(cut.get("journal_seq"), bool)):
            fatal.append(STATE_AUTHORITY_V2_SCHEMA_INVALID)
        try:
            parsed_state = json.loads(row["state_utf8"])
            if not isinstance(parsed_state, dict):
                raise ValueError
        except (TypeError, ValueError):
            fatal.append(STATE_AUTHORITY_V2_CANONICAL_BYTES_INVALID)
        else:
            # A dict is not yet a STATE. Everything downstream — the cuts, the
            # anti-replay scope test and both frozen reducers — dereferences the state
            # shape, so a state-shaped-but-not-a-state object belongs with the other
            # unusable shapes: FATAL and named, never a traceback (codex r5 P2).
            if not _is_state_shaped(parsed_state):
                fatal.append(STATE_AUTHORITY_V2_SCHEMA_INVALID)
    for name in ("proposal_persistence", "applied_child"):
        try:
            if not isinstance(json.loads(receipt[name]["event_utf8"]), dict):
                raise ValueError
        except (TypeError, ValueError):
            fatal.append(STATE_AUTHORITY_V2_CANONICAL_BYTES_INVALID)
    if fatal:
        return sorted(set(fatal)), True
    if (receipt["schema_id"] != STATE_AUTHORITY_V2_SCHEMA_ID
            or receipt["domain"] != STATE_AUTHORITY_V2_DOMAIN
            or receipt["version"] != STATE_AUTHORITY_V2_VERSION
            or receipt["authority_mode"] not in {AUTHORITY_MODE_PRODUCTION,
                                                 AUTHORITY_MODE_FIXTURE}
            or common.SEMANTIC_ID.fullmatch(receipt.get("transaction_commit_id") or "") is None
            or common.SEMANTIC_ID.fullmatch(
                receipt["store_identity"].get("store_id") or "") is None
            or common.SEMANTIC_ID.fullmatch(
                receipt["store_identity"].get("namespace") or "") is None
            or not isinstance(receipt["store_identity"].get("namespace_version"), int)
            or isinstance(receipt["store_identity"].get("namespace_version"), bool)
            or receipt["store_identity"]["namespace_version"] < 1
            or not isinstance(receipt["applied_child"].get("next_sequence"), int)
            or isinstance(receipt["applied_child"].get("next_sequence"), bool)):
        errors.append(STATE_AUTHORITY_V2_SCHEMA_INVALID)
    for name in ("prestate_read", "postcommit_readback"):
        row = receipt[name]
        value = json.loads(row["state_utf8"])
        if (common.SEMANTIC_ID.fullmatch(row.get("read_id") or "") is None
                or common.SHA384.fullmatch(row.get("state_hash") or "") is None):
            errors.append(STATE_AUTHORITY_V2_SCHEMA_INVALID)
        if common.canonical_json(value).decode("utf-8") != row["state_utf8"]:
            errors.append(STATE_AUTHORITY_V2_CANONICAL_BYTES_INVALID)
        if row["state_hash"] != common.sha384(row["state_utf8"].encode("utf-8")):
            errors.append(STATE_AUTHORITY_V2_HASH_INVALID)
    for name in ("proposal_persistence", "applied_child"):
        row = receipt[name]
        value = json.loads(row["event_utf8"])
        if (common.canonical_json(value).decode("utf-8") != row["event_utf8"]
                or value.get("event_id") != row.get("event_id")
                or common.canonical_event_id(value) != row.get("event_id")):
            errors.append(STATE_AUTHORITY_V2_CANONICAL_BYTES_INVALID)
        if (common.SHA384.fullmatch(row.get("event_hash") or "") is None
                or row["event_hash"] != common.sha384(row["event_utf8"].encode("utf-8"))):
            errors.append(STATE_AUTHORITY_V2_HASH_INVALID)
    preimage = common.canonical_json(_canonical_content(receipt))
    if receipt.get("receipt_preimage_b64") != base64.b64encode(preimage).decode("ascii"):
        errors.append(STATE_AUTHORITY_V2_CANONICAL_BYTES_INVALID)
    if (common.SHA384.fullmatch(receipt.get("receipt_digest") or "") is None
            or receipt["receipt_digest"] != common.sha384(preimage)):
        errors.append(STATE_AUTHORITY_V2_HASH_INVALID)
    return errors, False


def manifest_shape(manifest: Any) -> str | None:
    """`FIXTURE`, `PRODUCTION`, or None for an incoherent mixture (BUILD A split).

    Before the r1 fold this module recognised ONE shape — `production_ready:false`,
    `NOT_ACTIVATED`, every root `fixture_only:true` — and required it for PRODUCTION
    admission. That was wrong in both directions at once: it ACCEPTED an attacker's
    fixture-shaped self-authored root, and it REFUSED the ceremony spec's own published
    production manifest (`STATE_AUTHORITY_V2_ROOT_NOT_TRUSTED`), which
    `MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md` §3.3 defines as `production_ready:true`
    over non-fixture roots. Structural PARSING now accepts both coherent shapes so the
    committed fixture stays readable/testable and the ceremony manifest is expressible;
    production ACTIVATION is a separate, AUTHENTICATED step (`_activation_errors`).
    A mixed manifest — a fixture relabelled `production_ready:true`, or an activated
    policy over `fixture_only` roots — is neither shape and is refused.
    """
    if not isinstance(manifest, dict):
        return None
    policy = manifest.get("trust_policy")
    roots = manifest.get("roots")
    if not isinstance(policy, dict) or not isinstance(roots, list) or not roots:
        return None
    fixture_flags = {root.get("fixture_only") for root in roots
                     if isinstance(root, dict)}
    if (manifest.get("production_ready") is False
            and policy.get("status") == TRUST_POLICY_STATUS_NOT_ACTIVATED
            and fixture_flags == {True}):
        return "FIXTURE"
    if (manifest.get("production_ready") is True
            and policy.get("status") == TRUST_POLICY_STATUS_ACTIVATED
            and fixture_flags == {False}):
        return "PRODUCTION"
    return None


def _manifest_structural_errors(manifest: Any) -> list[str]:
    """Shape-agnostic structure of a `StateTrustRootManifestV1`.

    Structural admissibility only: it accepts the committed FIXTURE instance and an
    injected PRODUCTION instance alike, exactly as
    `mbcx01_build_measurement_authority.validate_production_trust_root_manifest` does
    on the BUILD B side. A manifest is admissible INPUT; relabelling it is never a
    ceremony, and no shape of it activates anything on its own.
    """
    if not isinstance(manifest, dict):
        return [STATE_AUTHORITY_V2_ROOT_NOT_TRUSTED]
    policy = manifest.get("trust_policy")
    roles = manifest.get("custody_roles")
    errors: list[str] = []
    if (manifest.get("schema_id") != TRUST_ROOT_MANIFEST_SCHEMA_ID
            or manifest_shape(manifest) is None
            or not isinstance(policy, dict)
            or policy.get("schema_id") != TRUST_POLICY_SCHEMA_ID
            or policy.get("fail_loud_sentinel") != STATE_AUTHORITY_SENTINEL
            or policy.get("roles_must_be_distinct") is not True
            or policy.get("signer_cannot_edit_root") is not True
            or policy.get("manifest_edit_cannot_activate_production") is not True
            or sorted(policy.get("required_external_evidence") or [])
            != sorted(REQUIRED_EXTERNAL_EVIDENCE)
            or manifest.get("trust_policy_digest") != common.sha384(policy)
            or not isinstance(manifest.get("roots"), list) or not manifest["roots"]
            or not isinstance(roles, dict)
            or len({roles.get("signer_custodian_role"), roles.get("trust_root_editor_role"),
                    roles.get("readback_reader_role"), roles.get("writer_producer_role")}) != 4):
        errors.append(STATE_AUTHORITY_V2_ROOT_NOT_TRUSTED)
    return errors


def production_activation_binding(manifest: Any,
                                  custody_evidence: Any) -> dict[str, Any] | None:
    """The exact facts an owner activation must bind for THIS manifest and custody set.

    One definition, used by the verifier and by the fixture ceremony helper, so the
    signed statement and the checked statement can never drift apart.

    BUILD A DIFFERENCE FROM BUILD B, stated rather than glossed: the state interface
    receives custody DIGESTS, not custody documents (the four documents are never
    injected here), so the owner statement authenticates those four digest VALUES plus
    the key sets and the exact manifest. BUILD B additionally recomputes each digest
    from the injected document. Making BUILD A carry the documents too would be a
    stronger fold and is recorded as a residual, not claimed here.

    r4 fold (FOLD-2C, second site). The binding below is handed to the SHARED trust
    anchor, which compares the editor key set by sorting it
    (`mbcx01_build_trust_anchor.py:1058`). A key list whose elements are not all strings
    makes that comparison raise a raw `TypeError` from inside the anchor — outside this
    module's closed error list, which is the contract
    `verify_state_authority_receipt_v2` advertises. So the elements are checked HERE, and
    a malformed key list yields no binding at all: `ACTIVATION_UNAUTHENTICATED`, named,
    alongside the custody refusal `_custody_errors` returns for the same input.
    """
    if not isinstance(custody_evidence, dict) or not isinstance(manifest, dict):
        return None
    signer_keys = custody_evidence.get("signer_key_ids")
    editor_keys = custody_evidence.get("root_editor_key_ids")
    if (not isinstance(signer_keys, list) or not isinstance(editor_keys, list)
            or any(not isinstance(key, str) for key in signer_keys + editor_keys)):
        return None
    try:
        return {
            "authority": trust_anchor.AUTHORITY_STATE,
            "manifest_validity": manifest["validity"],
            # BUILD A's custody evidence declares a SET of authorized writer keys.
            "signing_key_id": sorted(custody_evidence["signer_key_ids"]),
            "editor_key_ids": list(custody_evidence["root_editor_key_ids"]),
            "custody_evidence_digests": {
                name: custody_evidence[field] for name, field in CUSTODY_DIGEST_FIELDS},
            "provenance_digest": custody_evidence["store_build_provenance_digest"],
        }
    except (KeyError, TypeError):
        return None


#: Generic trust-anchor outcomes -> this authority's named rejections.
_ACTIVATION_CODES = {
    trust_anchor.ANCHOR_UNAVAILABLE: STATE_AUTHORITY_V2_TRUST_ANCHOR_UNAVAILABLE,
    trust_anchor.ANCHOR_FIXTURE_ONLY: STATE_AUTHORITY_V2_TRUST_ANCHOR_FIXTURE_ONLY,
    trust_anchor.ACTIVATION_UNAUTHENTICATED: STATE_AUTHORITY_V2_ACTIVATION_UNAUTHENTICATED,
    trust_anchor.SIGNATURE_CARRIER_INVALID: STATE_AUTHORITY_V2_SIGNATURE_CARRIER_INVALID,
}


def resolve_verifier_context() -> tuple[Any, str | None]:
    """Snapshot the verifier context for ONE verification (r2 fix class).

    Called ONCE, at the top of the production path, BEFORE any caller-supplied object is
    read, so an object graph that reconfigures process authority while the verifier is
    walking the request cannot substitute this verification's root of trust — and a
    `fixture_only` anchor is refused here by name (codex r2 F1/F2/F3).
    """
    return trust_anchor.resolve_production_verifier_context(
        trust_anchor.AUTHORITY_STATE)


def _activation_errors(manifest: Any, custody_evidence: Any, *, context: Any,
                       anchor_refusal: str | None) -> list[str]:
    """THE production bootstrap invariant for BUILD A (see `mbcx01_build_trust_anchor`).

    Production admission requires a PRODUCTION-shaped manifest, valid AT THE VERIFIER'S
    OWN INSTANT, whose exact canonical digest — together with its validity window, the
    authorized writer key set, the trust-root editor key set, the store-build provenance
    digest and the four custody digests — has been SIGNED by the anchor of the verifier's
    own context. A manifest that merely arrived in the request, in any shape, is not
    authority. An anchor that was never configured, and an anchor that is FIXTURE
    material, are both REFUSALS, never a bypass.

    On the clock (codex r2 F4): every other instant in this module is the AUTHORITY
    INSTANT the receipt attests, which is deliberate — a deterministic replay of a
    receipt must not change its verdict because a year passed. Trust-root FRESHNESS is a
    different question with a different answer: a verifier must not accept a root
    because the artifact under verification says the root was fresh when the artifact
    was made, so the manifest's own validity window is judged at the verifier's instant.
    """
    if manifest_shape(manifest) != "PRODUCTION":
        return [STATE_AUTHORITY_V2_ROOT_NOT_TRUSTED]
    if anchor_refusal is not None:
        return [_ACTIVATION_CODES[anchor_refusal]]
    # THE KEY, NOT THE LABEL — SIGNING CLASS (2026-08-15 fold). `PRODUCTION` above is a
    # shape the caller's manifest asserts about itself. A key that is PUBLISHED in a
    # committed `*.fixture.json` document of this repository is test material whatever
    # the manifest says, and the ceremony requires every key in a production manifest to
    # be generated in the ceremony rather than copied out of a committed fixture document
    # (`MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md` §3 steps 0 and 3). A council seat executed
    # this class on the measurement plane; the state plane had the identical shape.
    if any(trust_anchor.committed_fixture_key_document(root.get("public_key_pem"))
           is not None for root in manifest["roots"] if isinstance(root, dict)):
        return [STATE_AUTHORITY_V2_SIGNING_KEY_FIXTURE_MATERIAL]
    # The manifest's window is written in the state layer's six-fractional-digit
    # spelling; the context's instant is whole seconds. Comparing the two as STRINGS
    # misorders them across the two forms, so both are parsed to instants first and a
    # window that is not a calendar interval is a MALFORMED MANIFEST — not an expiry
    # (codex r5 P2, and the measurement plane's `parse_instant` for the same reason).
    instant = parse_instant(context.current_instant())
    window = manifest.get("validity") if isinstance(manifest.get("validity"), dict) else {}
    not_before = parse_instant(window.get("not_before"))
    not_after = parse_instant(window.get("not_after"))
    if instant is None or not_before is None or not_after is None:
        return [STATE_AUTHORITY_V2_ROOT_NOT_TRUSTED]
    if not not_before <= instant < not_after:
        return [STATE_AUTHORITY_V2_KEY_REVOKED_OR_EXPIRED]
    binding = production_activation_binding(manifest, custody_evidence)
    if binding is None:
        return [STATE_AUTHORITY_V2_ACTIVATION_UNAUTHENTICATED]
    outcome = trust_anchor.authenticate_production_activation(
        custody_evidence.get(OWNER_ACTIVATION_EVIDENCE), context=context,
        manifest=manifest, **binding)
    if outcome is None:
        return []
    return [_ACTIVATION_CODES[outcome]]


def _custody_errors(manifest: Any, custody_evidence: Any, signer_key_id: Any) -> list[str]:
    """I13 mechanically: the signing custodian can neither edit nor approve the root.

    r4 fold (FOLD-2C). The two key lists are CALLER-SUPPLIED material, and the separation
    test below compares them as SETS. Their elements were never checked, so a custody
    object that was otherwise exact but carried a dict inside `signer_key_ids` raised a
    raw `TypeError: unhashable type: 'dict'` out of the public verifier — which promises a
    CLOSED ERROR LIST for every input. An element that is hashable but is not a key id
    (an integer, say) had the quieter failure: no exception, and no refusal either, so
    junk rode along beside the real key and the separation test passed over it. A key id
    is a string; every element is checked before any set is built, and anything else is
    the named custody refusal. Same family as the ETW thread-roster row fold: the posture
    is unchanged, the refusal is named.
    """
    roles = manifest.get("custody_roles") if isinstance(manifest, dict) else None
    if not isinstance(custody_evidence, dict) or set(custody_evidence) != CUSTODY_EVIDENCE_KEYS:
        return [STATE_AUTHORITY_V2_CUSTODY_SEPARATION_INVALID]
    signer_keys = custody_evidence.get("signer_key_ids")
    editor_keys = custody_evidence.get("root_editor_key_ids")
    if (not isinstance(signer_keys, list) or not isinstance(editor_keys, list)
            or any(not isinstance(key, str) for key in signer_keys)
            or any(not isinstance(key, str) for key in editor_keys)
            or not isinstance(roles, dict)
            or custody_evidence.get("signer_custodian_role")
            != roles.get("signer_custodian_role")
            or custody_evidence.get("trust_root_editor_role")
            != roles.get("trust_root_editor_role")
            or custody_evidence["signer_custodian_role"]
            == custody_evidence["trust_root_editor_role"]
            or signer_key_id not in signer_keys
            or set(signer_keys) & set(editor_keys)
            or any(common.SHA384.fullmatch(custody_evidence.get(name) or "") is None
                   for name in ("key_custody_attestation_digest",
                                "root_editor_approval_digest",
                                "store_build_provenance_digest",
                                "signing_ceremony_receipt_digest"))):
        return [STATE_AUTHORITY_V2_CUSTODY_SEPARATION_INVALID]
    return []


def _root_errors(manifest: dict[str, Any], receipt: dict[str, Any],
                 authority_instant: str) -> tuple[list[str], dict[str, Any] | None]:
    """Resolve the signer root from the INJECTED manifest only; never from the envelope."""
    errors: list[str] = []
    signer = receipt["signer_identity"]
    if signer.get("trust_root_id") != manifest.get("manifest_id"):
        errors.append(STATE_AUTHORITY_V2_ROOT_SELF_AUTHORED)
    if signer.get("trust_policy_digest") != manifest.get("trust_policy_digest"):
        errors.append(STATE_AUTHORITY_V2_ROOT_NOT_TRUSTED)
    roots = manifest.get("roots") if isinstance(manifest.get("roots"), list) else []
    root = next((entry for entry in roots
                 if isinstance(entry, dict)
                 and entry.get("key_id") == signer.get("signer_key_id")), None)
    if root is None:
        errors.append(STATE_AUTHORITY_V2_ROOT_NOT_TRUSTED)
        return errors, None
    revoked_ids = {row.get("key_id") for row in manifest.get("revocation_list") or []
                   if isinstance(row, dict)}
    validity = root.get("validity") or {}
    manifest_validity = manifest.get("validity") or {}
    # The window comparisons are between CALENDAR INSTANTS, never strings (codex r5 P2
    # class; this is the ENUMERATED remaining member of the same site set — the
    # `:527-530`-class sibling was folded first, and `:863` is homogeneous by
    # construction). The signer↔root equality checks above stay STRING equality on
    # purpose: they are identity-of-declaration, not ordering. An endpoint or attested
    # instant that does not parse lands in the same refusal disjunction — `or`
    # short-circuits before any None comparison can raise.
    instant = parse_instant(authority_instant)
    windows = (parse_instant(validity.get("not_before")),
               parse_instant(validity.get("not_after")),
               parse_instant(manifest_validity.get("not_before")),
               parse_instant(manifest_validity.get("not_after")))
    if (root.get("revocation_state") != REVOCATION_NOT_REVOKED
            or signer.get("revocation_state") != REVOCATION_NOT_REVOKED
            or root.get("key_id") in revoked_ids
            or signer.get("validity_not_before") != validity.get("not_before")
            or signer.get("validity_not_after") != validity.get("not_after")
            or instant is None or None in windows
            or not (windows[0] <= instant < windows[1])
            or not (windows[2] <= instant < windows[3])):
        errors.append(STATE_AUTHORITY_V2_KEY_REVOKED_OR_EXPIRED)
    if (root.get("algorithm") != SIGNATURE_ALGORITHM
            or signer.get("signature_algorithm") != SIGNATURE_ALGORITHM
            or root.get("authorized_role") != ROLE_STATE_OWNER_WRITER
            or signer.get("producer_role") != ROLE_STATE_OWNER_WRITER
            or signer.get("producer_id") != root.get("authorized_producer_id")):
        errors.append(STATE_AUTHORITY_V2_ROLE_NOT_AUTHORIZED)
    return errors, root


def _reader_errors(manifest: dict[str, Any], receipt: dict[str, Any]) -> list[str]:
    """A writer-owned readback is a self-attestation wearing a readback label."""
    reader = receipt["postcommit_readback"].get("reader_identity")
    producer = receipt["signer_identity"].get("producer_id")
    roots = manifest.get("roots") if isinstance(manifest.get("roots"), list) else []
    reader_root = next((entry for entry in roots
                        if isinstance(entry, dict)
                        and entry.get("authorized_role") == ROLE_STATE_READBACK_READER
                        and entry.get("authorized_producer_id") == reader), None)
    if reader == producer or reader_root is None:
        return [STATE_AUTHORITY_V2_READER_NOT_INDEPENDENT]
    return []


def _anti_replay_errors(receipt: dict[str, Any], root: dict[str, Any] | None,
                        prestate: dict[str, Any], poststate: dict[str, Any],
                        durable_anchors: dict[str, Any] | None) -> list[str]:
    """The anti-replay block must BYTE-EQUAL the anchors of the durable journal row.

    FOLD 1. Before this fold the verifier re-derived `receipt_nonce`, `scenario_id` and
    `run_id` from the receipt's own labels (`TXN.x -> NONCE.x`, `SCOPE.x -> SCENARIO.x`,
    `SUBJECT.x -> RUN.x`). That was a self-check, not an anchor: it accepted any anchor
    set an attacker could compute from labels the attacker already controls, and it
    could not express a production run whose scenario/run/nonce are independent
    identifiers. The anchors are now a durable fact committed by the writer before any
    effect row exists, and the receipt's five-value anchor set (the four `anti_replay`
    axes plus the attested `subject_identity`) is compared to it as canonical BYTES.

    Retained, unweakened, on top of the byte comparison:
      * `anti_replay.transaction_commit_id` equals the receipt's transaction identity;
      * the claimed scope is actually carried by BOTH of the receipt's own state bytes;
      * the attested subject is the subject the injected manifest root authorizes.
    Absent durable anchors (unresolvable store, unknown or non-COMMITTED transaction)
    is a rejection: absence of durable evidence is never an argument for admission.
    """
    anti_replay = receipt["anti_replay"]
    transaction_commit_id = receipt["transaction_commit_id"]
    scope_id = anti_replay.get("scope_id")
    subject = receipt["signer_identity"].get("subject_identity")
    scopes = set(prestate.get("scopes") or {}) & set(poststate.get("scopes") or {})
    claimed = {"receipt_nonce": anti_replay.get("receipt_nonce"),
               "scope_id": scope_id,
               "scenario_id": anti_replay.get("scenario_id"),
               "run_id": anti_replay.get("run_id"),
               "subject_identity": subject}
    failures = [
        anti_replay.get("transaction_commit_id") != transaction_commit_id,
        scope_id not in scopes,
        durable_anchors is None,
        durable_anchors is not None
        and common.canonical_json(claimed) != common.canonical_json(durable_anchors),
        root is not None and subject != root.get("authorized_subject_identity"),
    ]
    return [STATE_AUTHORITY_V2_REPLAY_IDENTITY_INVALID] if any(failures) else []


def _resolve_store(receipt: dict[str, Any], store_path: Any) -> tuple[Any, Any]:
    """Resolve the DURABLE store the receipt names (FOLD 2).

    Two resolution arms, in order, and the receipt never chooses either one:

      1. the live in-process registry (`mbcx01_build_state_store.registered_store`) —
         the `:memory:` and same-process arm, unchanged;
      2. an INJECTED durable path (`store_path`), opened read-only in this process with
         its persisted store header verified against the receipt's `store_identity`.
         This is what makes verification possible in a FRESH process that has opened
         nothing: durable evidence must be checkable from the durable bytes, not from
         the privilege of having been the writer.

    `store_path` comes from the verifying operator's configuration, exactly like the
    trust-root manifest and custody evidence. It is never read out of the receipt — a
    receipt that could name its own store would be resolving itself.

    Returns `(store, opened)`; `opened` is the read-only view this call is responsible
    for closing, or `None` when the live registry answered.
    """
    identity = receipt["store_identity"]
    store = store_mod.registered_store(identity.get("store_id"), identity.get("namespace"),
                                       identity.get("namespace_version"))
    if store is not None:
        return store, None
    if not store_path:
        return None, None
    try:
        view = store_mod.ReadOnlyStateStoreView.open_verified_readonly(
            store_path, store_id=identity.get("store_id"),
            namespace=identity.get("namespace"),
            namespace_version=identity.get("namespace_version"))
    except store_mod.StateStoreError:
        # An unreadable path, a store whose persisted identity is not the identity the
        # receipt claims, a schema-version mismatch, or a file that carries the identity
        # signals but not the tables a reader would be answered from
        # (`STATE_STORE_SCHEMA_INCOMPLETE`, codex-CLI r9 F2 — the read-only door refuses
        # it BY NAME rather than letting `SELECT * FROM journal` raise a raw
        # `sqlite3.OperationalError` through this function and out of the public
        # verifier): in every one of those cases no durable store was resolved, and an
        # unresolved store is `STATE_AUTHORITY_V2_TRANSACTION_IDENTITY_MISMATCH` plus the
        # sentinel. Absence of durable evidence is never an argument for admission, and
        # it is never an exception either — this verifier ANSWERS.
        return None, None
    return view, view


def _durable_terminal_errors(store: Any, receipt: dict[str, Any]) -> tuple[list[str], bool]:
    """Read the distinguished terminal of the receipt's transaction from the store."""
    if store is None:
        return [STATE_AUTHORITY_V2_TRANSACTION_IDENTITY_MISMATCH], False
    rows = store.journal_rows(receipt["transaction_commit_id"])
    if not rows:
        return [STATE_AUTHORITY_V2_TRANSACTION_IDENTITY_MISMATCH], False
    if rows[0]["status"] != store_mod.TRANSACTION_COMMITTED:
        return [STATE_AUTHORITY_V2_TRANSACTION_NOT_COMMITTED], False
    return [], True


def _durable_anchors(store: Any, receipt: dict[str, Any]) -> dict[str, Any] | None:
    """The durable anchor set of the receipt's transaction, or `None` when unavailable.

    `None` covers every "there is no durable fact to compare against" case — no
    resolvable store, unknown transaction, corrupt anchor row — and each of those is a
    replay rejection in `_anti_replay_errors`, never a pass.
    """
    if store is None:
        return None
    try:
        return store.anti_replay_anchors(receipt["transaction_commit_id"])
    except store_mod.StateStoreError:
        return None


def _durable_evidence_errors(store: Any, receipt: dict[str, Any]) -> list[str]:
    """The attested bytes must be the bytes the durable store actually holds."""
    try:
        durable = store.transaction_rows(receipt["transaction_commit_id"])
    except store_mod.StateStoreError:
        return [STATE_AUTHORITY_V2_TRANSACTION_NOT_COMMITTED]
    errors: list[str] = []
    if (receipt["prestate_read"]["state_utf8"] != durable["journal"]["prestate_utf8"]
            or receipt["postcommit_readback"]["state_utf8"]
            != durable["snapshots"]["state_utf8"]):
        errors.append(STATE_AUTHORITY_V2_STATE_SUBSTITUTION)
    if (receipt["proposal_persistence"]["event_utf8"] != durable["proposals"]["event_utf8"]
            or receipt["proposal_persistence"]["persistence_identity"]
            != durable["proposals"]["persistence_identity"]
            or receipt["applied_child"]["event_utf8"] != durable["children"]["event_utf8"]):
        errors.append(STATE_AUTHORITY_V2_EVENT_SUBSTITUTION)
    return errors


def _semantic_errors(receipt: dict[str, Any], prestate: dict[str, Any],
                     poststate: dict[str, Any], proposal: dict[str, Any],
                     child: dict[str, Any]) -> list[str]:
    """Cuts, persistence, dual-reducer replay, and sequence — all from the frozen seams."""
    errors: list[str] = []
    transaction_commit_id = receipt["transaction_commit_id"]
    if (receipt["prestate_read"]["read_id"]
            != store_mod.read_id(transaction_commit_id, store_mod.PHASE_PRESTATE)
            or receipt["postcommit_readback"]["read_id"]
            != store_mod.read_id(transaction_commit_id, store_mod.PHASE_POSTCOMMIT)):
        errors.append(STATE_AUTHORITY_V2_TRANSACTION_IDENTITY_MISMATCH)

    pre_cut = receipt["prestate_read"]["cut"]
    post_cut = receipt["postcommit_readback"]["cut"]
    if (pre_cut != common.current_cut(prestate) or post_cut != common.current_cut(poststate)
            or post_cut["journal_seq"] <= pre_cut["journal_seq"]
            or post_cut["knowledge_time"] < pre_cut["knowledge_time"]):
        errors.append(STATE_AUTHORITY_V2_CUT_INVALID)

    if (receipt["proposal_persistence"]["persistence_identity"]
            != store_mod.persistence_row_identity(transaction_commit_id,
                                                  proposal.get("event_id", ""))
            or proposal.get("event_type") != "propose_handoff_result"
            or prestate.get("events", {}).get(proposal.get("event_id"))
            != common.sha384(proposal)):
        errors.append(STATE_AUTHORITY_V2_EVENT_SUBSTITUTION)
    if (child.get("event_type") not in {"commit_handoff_result", "reject_handoff_result"}
            or poststate.get("events", {}).get(child.get("event_id"))
            != common.sha384(child)):
        errors.append(STATE_AUTHORITY_V2_EVENT_SUBSTITUTION)

    # Both FROZEN reducers replay the exact persisted child from the exact read prestate.
    # Attribute lookup at call time: an independently patched reducer must be SEEN.
    reference_state, reference_result = reference.reference_apply(
        copy.deepcopy(prestate), copy.deepcopy(child))
    oracle_state, oracle_result = oracle.oracle_apply(
        copy.deepcopy(prestate), copy.deepcopy(child))
    if reference_state != oracle_state or reference_result != oracle_result:
        # The verifier never picks a winner and never discharges on a split decision.
        errors.append(STATE_AUTHORITY_V2_REDUCER_DISAGREEMENT)
    elif reference_result != "APPLIED" or reference_state != poststate:
        errors.append(STATE_AUTHORITY_V2_STATE_SUBSTITUTION)

    if receipt["applied_child"]["next_sequence"] != poststate.get("next_seq"):
        errors.append(STATE_AUTHORITY_V2_SEQUENCE_INVALID)
    return errors


# ---- public API -------------------------------------------------------------------


def verify_state_authority_receipt_v2(receipt: Any, *, trust_root_manifest: Any,
                                      custody_evidence: Any,
                                      require_production: bool = True,
                                      store_path: Any = None) -> list[str]:
    """Verify a `StateAuthorityReceiptV2` against an injected trust root and custody set.

    Returns `[]` only for a receipt that is structurally closed, canonically exact,
    signed by a manifest-resolved root under separated custody, bound to a COMMITTED
    durable terminal in the store it names, carrying the durable anti-replay anchors of
    that transaction, read back by an independent reader, and reproduced identically by
    BOTH frozen reducers. Any defect yields the named rejection AND keeps
    `STATE_AUTHORITY_UNAVAILABLE`: a defect never buys a discharge.

    The answer is a CLOSED LIST for every input, including inputs whose own material is
    broken: a malformed root PEM, an absent Node runtime, a verifier timeout or an
    off-contract verifier reply are named
    (`STATE_AUTHORITY_V2_SIGNATURE_VERIFIER_UNAVAILABLE`), not raised. Caller-supplied
    authority material can refuse a receipt; it cannot crash the verification.

    `store_path` (FOLD 2, optional) is the INJECTED durable filesystem path of the
    FILE-backed store the receipt names. With it, a FRESH process that has opened
    nothing can resolve the store read-only and verify from the durable bytes alone
    (`_resolve_store`). Without it, resolution is the live in-process registry only,
    which is what `:memory:` stores and same-process callers keep using. An
    unresolvable store is never an admission: it is
    `STATE_AUTHORITY_V2_TRANSACTION_IDENTITY_MISMATCH`.

    THE CLOSED LIST IS TOTAL AT THIS BOUNDARY, NOT MERELY AT THE SHAPES SOMEONE
    ENUMERATED (codex-CLI r6 SEAT1 F3 — the THIRD round in which a malformed caller
    JSON escaped the documented closed list as a raw traceback: ba43's custody key
    list, ba45's state-shaped non-state, and now a scope map whose values are not
    scopes). Each of those was closed AT ITS SITE, and each time the next
    unanticipated shape found the next site. So the class is closed as a COMPLEMENT
    HERE: every `MALFORMED_CALLER_INPUT_EXCEPTIONS` member raised anywhere under this
    call becomes `STATE_AUTHORITY_V2_SCHEMA_INVALID` plus the sentinel, which is
    exactly the verdict a receipt whose shape cannot carry the checks already gets
    from `_structural_errors`. The per-site guards STAY — they say WHICH shape was
    wrong, and this says only that one was.

    ⚠ THE HONESTY CONSTRAINT, STATED AT THE BOUNDARY IT BINDS. This catches that
    enumerated tuple and NOTHING ELSE — never bare `Exception`. An `AssertionError`,
    a `MemoryError`, or any other class is a defect of THIS module rather than a
    statement about the caller's input, and it still faults loud and unconverted:
    an instrument that answered "your receipt is malformed" when it means "I am
    broken" would be reporting a wrong number about itself. The module's own named
    errors (`StateAuthorityError`, `store_mod.StateStoreError`) are `ValueError`
    subclasses and are RE-RAISED for the same reason — when this module speaks, the
    caller hears it, not a schema code.
    """
    try:
        return _verify_state_authority_receipt_v2(
            receipt, trust_root_manifest=trust_root_manifest,
            custody_evidence=custody_evidence,
            require_production=require_production, store_path=store_path)
    except (StateAuthorityError, store_mod.StateStoreError):
        raise
    except MALFORMED_CALLER_INPUT_EXCEPTIONS:
        return sorted({STATE_AUTHORITY_V2_SCHEMA_INVALID}
                      | ({STATE_AUTHORITY_SENTINEL} if require_production else set()))


def _verify_state_authority_receipt_v2(receipt: Any, *, trust_root_manifest: Any,
                                       custody_evidence: Any,
                                       require_production: bool = True,
                                       store_path: Any = None) -> list[str]:
    # (0) r2 fix class: the verifier context is snapshotted BEFORE any caller-supplied
    # object is read, and carried through the whole verification.
    context, anchor_refusal = resolve_verifier_context() if require_production else (None, None)
    structural, fatal = _structural_errors(receipt)
    errors = list(structural)
    if fatal:
        return sorted(set(errors) | ({STATE_AUTHORITY_SENTINEL} if require_production else set()))
    if require_production and receipt["authority_mode"] != AUTHORITY_MODE_PRODUCTION:
        errors.append(STATE_AUTHORITY_V2_SCHEMA_INVALID)

    prestate = json.loads(receipt["prestate_read"]["state_utf8"])
    poststate = json.loads(receipt["postcommit_readback"]["state_utf8"])
    proposal = json.loads(receipt["proposal_persistence"]["event_utf8"])
    child = json.loads(receipt["applied_child"]["event_utf8"])
    authority_instant = receipt["postcommit_readback"]["cut"].get("knowledge_time")

    errors.extend(_manifest_structural_errors(trust_root_manifest))
    manifest = trust_root_manifest if isinstance(trust_root_manifest, dict) else {}
    root_errors, root = _root_errors(manifest, receipt, authority_instant)
    errors.extend(root_errors)
    errors.extend(_custody_errors(manifest, custody_evidence,
                                  receipt["signer_identity"].get("signer_key_id")))
    if require_production:
        # AUTHENTICATION, not merely internal consistency: everything above is a graph
        # the CALLER supplied, so production admission begins from the anchor of the
        # verifier's OWN context (r1 fix class AUTHENTICATED_PRODUCTION_TRUST_BOOTSTRAP,
        # r2 fix class FIXTURE_ISOLATION).
        errors.extend(_activation_errors(trust_root_manifest, custody_evidence,
                                         context=context,
                                         anchor_refusal=anchor_refusal))
    if receipt["store_identity"] != manifest.get("store_binding"):
        errors.append(STATE_AUTHORITY_V2_STORE_IDENTITY_MISMATCH)
    errors.extend(_reader_errors(manifest, receipt))

    # The durable store is resolved BEFORE the anti-replay check, because the anchors
    # the receipt must match are a durable fact of the journal row (FOLD 1). The
    # resolution itself is registry-or-injected-path (FOLD 2).
    store, opened = _resolve_store(receipt, store_path)
    try:
        terminal_errors, committed = _durable_terminal_errors(store, receipt)
        errors.extend(_anti_replay_errors(receipt, root, prestate, poststate,
                                          _durable_anchors(store, receipt)))

        if root is not None:
            # The CARRIER is judged before the cryptography: a whitespace- or
            # base64url-bearing carrier decodes to a valid 64-byte signature under a
            # permissive decoder, giving one receipt many accepted byte strings and no
            # single identity for dedup or audit (MBCX01-BUILD-R1-SIGNATURE-CARRIER).
            if not trust_anchor.strict_signature_carrier_ok(receipt.get("signature_b64")):
                errors.append(STATE_AUTHORITY_V2_SIGNATURE_CARRIER_INVALID)
            else:
                preimage = common.canonical_json(_canonical_content(receipt))
                try:
                    valid = _invoke_signature_verifier([{
                        "payload_b64": base64.b64encode(preimage).decode("ascii"),
                        "public_key_pem": root.get("public_key_pem", ""),
                        "signature_b64": receipt.get("signature_b64", ""),
                    }])
                except StateAuthorityError:
                    # r3 fold: this verifier answers with a CLOSED LIST, always. The
                    # root key material comes out of a caller-supplied manifest, so a
                    # malformed PEM (and equally a missing Node runtime, a timeout, or a
                    # reply outside the closed verifier contract) must not escape as a
                    # raw exception — that would let caller-supplied authority material
                    # crash verification instead of being refused by it. Same discipline
                    # `mbcx01_build_trust_anchor.authenticate_production_activation`
                    # already applies to the activation verifier: a verifier that cannot
                    # run is never an admission.
                    errors.append(STATE_AUTHORITY_V2_SIGNATURE_VERIFIER_UNAVAILABLE)
                else:
                    if not valid[0]:
                        errors.append(STATE_AUTHORITY_V2_SIGNATURE_INVALID)

        errors.extend(terminal_errors)
        if committed:
            errors.extend(_durable_evidence_errors(store, receipt))
    finally:
        if opened is not None:
            opened.close()
    errors.extend(_semantic_errors(receipt, prestate, poststate, proposal, child))

    if errors and require_production:
        errors.append(STATE_AUTHORITY_SENTINEL)
    return sorted(set(errors))


def compare_operator_receipt_content(receipt: Any,
                                     operator_b_content: Any) -> list[str]:
    """Gate operator-1 vs operator-B receipt content on byte-identical canonical bytes.

    The gate never averages, prefers, or silently drops one operator: any difference in the
    signed preimage region is a DETECTED disagreement that keeps the sentinel.
    """
    errors: list[str] = []
    if not isinstance(receipt, dict) or not isinstance(operator_b_content, dict):
        errors.append(STATE_AUTHORITY_V2_SCHEMA_INVALID)
    else:
        operator_one = _canonical_content(receipt)
        operator_two = _canonical_content(operator_b_content)
        if set(operator_b_content) & V2_UNSIGNED_KEYS:
            # Operator B never signs; carrying a signature field is a schema breach.
            errors.append(STATE_AUTHORITY_V2_SCHEMA_INVALID)
        if common.canonical_json(operator_one) != common.canonical_json(operator_two):
            errors.append(STATE_AUTHORITY_V2_OPERATOR_DISAGREEMENT)
    if errors:
        errors.append(STATE_AUTHORITY_SENTINEL)
    return sorted(set(errors))


def _byte_binding_errors(scorer_input: Any, receipt: dict[str, Any]) -> list[str]:
    """BYTE-BIND the V2 evidence to the exact graph the frozen path validated."""
    try:
        transition = scorer_input["transition_authority"]
        fixture_receipt = scorer_input["state_authority_receipt"]
        pairs = (
            (receipt["prestate_read"]["state_utf8"],
             common.canonical_json(transition["precommit_state"]).decode("utf-8")),
            (receipt["prestate_read"]["state_hash"], transition["precommit_state_hash"]),
            (receipt["postcommit_readback"]["state_utf8"],
             common.canonical_json(transition["postcommit_state"]).decode("utf-8")),
            (receipt["postcommit_readback"]["state_hash"], transition["postcommit_state_hash"]),
            (receipt["proposal_persistence"]["event_utf8"], transition["proposal_event_utf8"]),
            (receipt["proposal_persistence"]["event_hash"], transition["proposal_event_hash"]),
            (receipt["applied_child"]["event_utf8"],
             common.canonical_json(transition["applied_child_event"]).decode("utf-8")),
            (receipt["applied_child"]["event_hash"], transition["applied_child_event_hash"]),
            (receipt["prestate_read"]["cut"], transition["precommit_cut"]),
            (receipt["postcommit_readback"]["cut"], transition["postcommit_cut"]),
            (receipt["applied_child"]["next_sequence"], transition["postcommit_state"]["next_seq"]),
            # ... and to the embedded fixture-projection receipt the frozen path verified.
            (receipt["prestate_read"]["state_utf8"],
             fixture_receipt["prestate_read"]["state_utf8"]),
            (receipt["prestate_read"]["state_hash"],
             fixture_receipt["prestate_read"]["state_hash"]),
            (receipt["prestate_read"]["cut"], fixture_receipt["prestate_read"]["cut"]),
            (receipt["postcommit_readback"]["state_utf8"],
             fixture_receipt["postcommit_readback"]["state_utf8"]),
            (receipt["postcommit_readback"]["state_hash"],
             fixture_receipt["postcommit_readback"]["state_hash"]),
            (receipt["postcommit_readback"]["cut"],
             fixture_receipt["postcommit_readback"]["cut"]),
            (receipt["proposal_persistence"]["event_utf8"],
             fixture_receipt["proposal_persistence"]["event_utf8"]),
            (receipt["proposal_persistence"]["event_id"],
             fixture_receipt["proposal_persistence"]["event_id"]),
            (receipt["applied_child"]["event_utf8"],
             fixture_receipt["applied_child"]["event_utf8"]),
            (receipt["applied_child"]["event_id"],
             fixture_receipt["applied_child"]["event_id"]),
        )
    except (KeyError, TypeError, ValueError):
        return [STATE_AUTHORITY_V2_BYTE_BINDING_MISMATCH]
    if any(left != right for left, right in pairs):
        return [STATE_AUTHORITY_V2_BYTE_BINDING_MISMATCH]
    return []


def verify_production_scorer_input(scorer_input: Any, production_receipt: Any, *,
                                   expected_manifest: dict[str, Any],
                                   trust_root_manifest: Any = None,
                                   custody_evidence: Any = None,
                                   store_path: Any = None) -> list[str]:
    """Production scientific admission for one scorer input (see the module docstring).

    The FROZEN `mbcx01_r13_packets.validate_scorer_input` runs twice, unmodified, and its
    fixture-mode verdict is never edited: the only thing this function may do is decline to
    re-add the sentinel and its byte-reproduced cascade
    (`SENTINEL_CASCADE_CLOSURE`; `mbcx01_r13_packets.py:544`, `:917-918`, `:1043`) when a
    fully clean, byte-bound `StateAuthorityReceiptV2` supplies the stronger evidence.

    NOTE (deviation from the design-notes signature, byte reason): the frozen validator is
    `validate_scorer_input(expected_manifest, value, *, require_production_authority)`
    (`mbcx01_r13_packets.py:1013`) — the expected manifest is a REQUIRED separate input and
    must not be read out of the scorer input under test (`:1020` compares them and raises
    `EXPECTED_MANIFEST_MISMATCH`). It is passed here as a required keyword-only argument.
    """
    production_errors = list(packets.validate_scorer_input(
        expected_manifest, scorer_input, require_production_authority=True))
    if production_receipt is None:
        # No V2 alongside: production admission is byte-for-byte the frozen behaviour.
        return sorted(set(production_errors))

    fixture_errors = list(packets.validate_scorer_input(
        expected_manifest, scorer_input, require_production_authority=False))
    v2_errors = verify_state_authority_receipt_v2(
        production_receipt, trust_root_manifest=trust_root_manifest,
        custody_evidence=custody_evidence, require_production=True,
        store_path=store_path)
    binding_errors = _byte_binding_errors(scorer_input, production_receipt)
    cascade = set(production_errors) - set(fixture_errors)
    if not v2_errors and not binding_errors and cascade <= SENTINEL_CASCADE_CLOSURE:
        return sorted(set(fixture_errors))
    return sorted(set(production_errors) | set(v2_errors) | set(binding_errors))
