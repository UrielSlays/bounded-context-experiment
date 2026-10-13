"""BUILD B production carrier-exactness authority.

Role: the frozen r13 verifier `mbcx01_r13_measurement._valid_exactness_receipt`
returns `False` for every input whenever production authority is required
(`mbcx01_r13_measurement.py:1602-1605`), so `CarrierExactnessReceiptV2`
fixture receipts stay conformance-only forever. This versioned sibling is the
only place a `CarrierExactnessReceiptV3` may be verified: bound to the pinned
suite/witness set, the exact carrier artifact digest, the exact harness build,
the exact measurement grid identity and a production trust root.

What this module DOES bind (each recomputed, never read as a label):

- the pinned suite artifact and witness set, taken from the committed suite
  file through the frozen `_exactness_suite_authority` (:1546-1566); the
  injected `suite_document` must be byte-identical in canonical form;
- the carrier artifact digest, harness build digest and measurement grid
  identity hash, recomputed from the supplied production envelope set;
- the production trust root: manifest structure, activation AUTHENTICATED
  against the operator-preconfigured owner anchor (r1 fix class; the injected
  `custody_evidence` must carry the owner-signed activation for exactly this
  manifest), the root that signed every envelope, and its authorized harness
  build.

What it does NOT do, stated plainly so no reviewer over-reads the receipt: it
does not execute the carrier exactness suite. The per-witness comparison is the
pinned suite runner's job (not built in this task), so the ONLY `result` this
authority emits or accepts is `AUTHORITY_BINDING_ONLY_SUITE_NOT_EXECUTED`, and
a receipt claiming `PASS` is refused `CARRIER_EXACTNESS_SUITE_NOT_EXECUTED`
rather than blessed. This receipt is an AUTHORITY BINDING over an exactness
claim — it is only meaningful alongside a clean
`mbcx01_build_measurement_authority.evaluate_production_measurement` result for
the same envelope set, which is where custody evidence is judged.

r2 FIX CLASS (codex F7, and the fixture-isolation invariant): the emitted label
used to be `PASS`, which reads as "the carrier suite executed" to anyone who has
not opened this docstring — an advertised contract must be the enforced artifact,
so the label now says what actually happened. The trust context this door
verifies against is resolved ONCE at entry, exactly like the other two doors.
"""

from __future__ import annotations

import base64
import hashlib
from typing import Any

import mbcx01_build_trust_anchor as trust_anchor
import mbcx01_build_windows_producer as producer
import mbcx01_r13_measurement as measurement
from mbcx01_build_measurement_authority import (
    MeasurementAuthorityError, PRODUCTION_FIXTURE_KIND, PRODUCTION_PRODUCER_ROLE,
    PRODUCTION_SIGNING_KEY_FIXTURE_MATERIAL,
    authenticated_activation_errors, production_activation_errors,
    resolve_verifier_context, validate_production_trust_root_manifest)

EXACTNESS_RECEIPT_SCHEMA_ID = "CarrierExactnessReceiptV3"
PRODUCTION_AUTHORITY_MODE = "PRODUCTION_MEASUREMENT_AUTHORITY"
FIXTURE_AUTHORITY_MODE = "FIXTURE_CONFORMANCE"
EXACTNESS_UNAVAILABLE = "CARRIER_EXACTNESS_AUTHORITY_UNAVAILABLE"

#: The ONLY `result` a receipt from this authority may carry, and the named refusal for
#: a receipt that claims otherwise (codex r2 F7). This module BINDS an exactness claim to
#: a pinned suite, an exact carrier artifact, an exact harness build, an exact grid
#: identity and an authenticated production root — it does NOT execute the carrier
#: exactness suite (`MBCX-01-BUILD-EXACTNESS-PRODUCTION-VERIFIER-SPEC.md` section 3
#: defers the per-witness runner). Emitting `PASS` invited a downstream reader to take
#: the receipt as proof that the suite ran, so the emitted value now says what actually
#: happened, and a caller CLAIMING `PASS` is refused rather than blessed.
BINDING_ONLY_RESULT = "AUTHORITY_BINDING_ONLY_SUITE_NOT_EXECUTED"
SUITE_NOT_EXECUTED = "CARRIER_EXACTNESS_SUITE_NOT_EXECUTED"

# Every field a production exactness receipt must bind. A receipt that omits or
# adds a field is invalid; no subset may be waived by a caller flag.
EXACTNESS_RECEIPT_V3_KEYS = frozenset({
    "schema_id", "candidate_id", "carrier_artifact_digest",
    "harness_build_digest", "measurement_grid_identity_hash",
    "suite_id", "suite_artifact_hash", "witness_set_hash", "result",
    "authority_mode", "producer_id", "trust_root_id", "trust_policy_digest",
    "receipt_hash",
})


def _refuse(code: str) -> None:
    raise MeasurementAuthorityError(code)


def _single(values: set[Any], code: str) -> Any:
    if len(values) != 1:
        _refuse(code)
    return next(iter(values))


def _signed_preimage_covers_receipt(envelope: Any) -> bool:
    """Does the SIGNED preimage still cover the `receipt` this envelope carries?

    2026-08-15 fold (codex r1 P1, invariant I16): the signature check below verifies
    `receipt_preimage_b64`, but every binding this module returns is read out of
    `envelope["receipt"]`. Those are two different objects, and nothing tied them
    together, so a receipt edited AFTER signing left the signature valid over the
    ORIGINAL bytes while the carrier artifact digest, harness build digest and
    grid identity were recomputed from the EDITED one — a stale signed payload
    authorising an arbitrary current carrier/grid binding (I16:
    `MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md`). Recomputing the preimage from
    the CURRENT receipt and comparing it — and `receipt_digest` — to what the
    envelope supplies closes the gap, exactly as the sibling measurement door
    does (`mbcx01_build_measurement_authority.py:622-632`).
    """
    try:
        preimage = producer.production_receipt_preimage(envelope)
        supplied = base64.b64decode(envelope.get("receipt_preimage_b64", ""),
                                    validate=True)
    except (ValueError, TypeError, KeyError, AttributeError):
        return False
    return (supplied == preimage
            and envelope.get("receipt_digest")
            == hashlib.sha384(preimage).hexdigest().upper())


def _production_envelope_bindings(envelopes: Any,
                                  roots: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Recompute the carrier/harness/grid bindings from the envelope set itself."""
    if not isinstance(envelopes, list) or len(envelopes) != 100:
        _refuse("GRID_COVERAGE_INVALID")
    try:
        for envelope in envelopes:
            if (not isinstance(envelope, dict)
                    or set(envelope) != set(producer.PRODUCTION_ENVELOPE_KEYS)
                    or envelope.get("schema_id") != producer.PRODUCTION_ENVELOPE_SCHEMA_ID
                    or envelope.get("domain") != producer.PRODUCTION_ENVELOPE_DOMAIN
                    or envelope.get("version") != producer.PRODUCTION_ENVELOPE_VERSION):
                _refuse("MEASUREMENT_ENVELOPE_INVALID")
            if (envelope.get("fixture_kind") != PRODUCTION_FIXTURE_KIND
                    or envelope.get("producer_role") != PRODUCTION_PRODUCER_ROLE):
                _refuse("FIXTURE_EVIDENCE_RELABELED")
            if not _signed_preimage_covers_receipt(envelope):
                # The signature is about to be checked against `receipt_preimage_b64`,
                # but every binding below is read out of `envelope["receipt"]`. Refuse
                # BEFORE deriving any of them: an envelope whose signed bytes do not
                # cover the receipt it presents carries no valid signature over the
                # evidence actually being bound. Named with the sibling door's code for
                # this exact class (`mbcx01_build_measurement_authority.py:628`) so the
                # closed production vocabulary stays closed and one class keeps one name.
                _refuse("MEASUREMENT_SIGNATURE_INVALID")
        key_id = _single({envelope["signing_key_id"] for envelope in envelopes},
                         "MEASUREMENT_SIGNATURE_INVALID")
        root = roots.get(key_id)
        if root is None:
            _refuse("MEASUREMENT_SIGNATURE_INVALID")
        candidate_id = _single({envelope["receipt"]["candidate_id"]
                                for envelope in envelopes}, "CANDIDATE_ID_MISMATCH")
        carrier = _single({envelope["receipt"]["candidate_artifact_digest"]
                           for envelope in envelopes}, "GRID_IDENTITY_MISMATCH")
        harness_build = _single(
            {envelope["receipt"]["job_receipt"]["evidence"]["harness_identity"][
                "harness_build_digest"] for envelope in envelopes},
            "GRID_IDENTITY_MISMATCH")
        policy_digest = _single({envelope["trust_policy_digest"] for envelope in envelopes},
                                "MEASUREMENT_TRUST_ROOT_INVALID")
    except (KeyError, TypeError, AttributeError) as exc:
        raise MeasurementAuthorityError("MEASUREMENT_ENVELOPE_INVALID") from exc
    if policy_digest != root["trust_policy_digest"]:
        _refuse("MEASUREMENT_TRUST_ROOT_INVALID")
    if harness_build != root["authorized_harness_build_digest"]:
        _refuse("MEASUREMENT_TRUST_ROOT_INVALID")
    try:
        grid_identity = measurement.measurement_grid_identity_hash(envelopes)
    except ValueError as exc:
        raise MeasurementAuthorityError("GRID_IDENTITY_MISMATCH") from exc
    if any(not trust_anchor.strict_signature_carrier_ok(envelope.get("signature_b64"))
           for envelope in envelopes):
        _refuse("MEASUREMENT_SIGNATURE_CARRIER_INVALID")
    items = [{"payload_b64": envelope["receipt_preimage_b64"],
              "public_key_pem": root["public_key_pem"],
              "signature_b64": envelope["signature_b64"]} for envelope in envelopes]
    try:
        signatures_valid = all(measurement._invoke_signature_verifier(items))
    except ValueError as exc:
        raise MeasurementAuthorityError("MEASUREMENT_SIGNATURE_INVALID") from exc
    if not signatures_valid:
        _refuse("MEASUREMENT_SIGNATURE_INVALID")
    return {"candidate_id": candidate_id, "carrier_artifact_digest": carrier,
            "harness_build_digest": harness_build,
            "measurement_grid_identity_hash": grid_identity,
            "producer_id": key_id, "trust_policy_digest": policy_digest}


def verify_production_carrier_exactness(receipt: Any, *, envelopes: Any,
                                        suite_document: Any,
                                        trust_root_manifest: Any,
                                        custody_evidence: Any = None) -> dict[str, Any]:
    """Verify a production `CarrierExactnessReceiptV3`, or raise.

    The supplied `receipt` is a CLAIM: every field it carries must equal the
    value recomputed here from the pinned suite, the production envelope set
    and the injected V3 manifest, and the returned receipt is the recomputed
    one with its own `receipt_hash`. A fixture-mode receipt, a relabeled
    authority mode or a repaired `receipt_hash` can never satisfy it.
    """
    return _verify_production_carrier_exactness(
        receipt, envelopes=envelopes, suite_document=suite_document,
        trust_root_manifest=trust_root_manifest,
        custody_evidence=custody_evidence)


def _verify_production_carrier_exactness(receipt: Any, *, envelopes: Any,
                                         suite_document: Any,
                                         trust_root_manifest: Any,
                                         custody_evidence: Any) -> dict[str, Any]:
    if not isinstance(receipt, dict):
        _refuse("MEASUREMENT_SCHEMA_INVALID")
    if receipt.get("schema_id") != EXACTNESS_RECEIPT_SCHEMA_ID:
        # A receipt minted under any other schema — notably the frozen
        # `CarrierExactnessReceiptV2` fixture receipt — cannot become
        # production authority by relabeling `authority_mode` and repairing
        # `receipt_hash`: fixture conformance is not a production ceremony.
        _refuse("FIXTURE_EVIDENCE_RELABELED")
    if not set(receipt) <= set(EXACTNESS_RECEIPT_V3_KEYS):
        _refuse("MEASUREMENT_SCHEMA_INVALID")
    if receipt.get("authority_mode", PRODUCTION_AUTHORITY_MODE) != PRODUCTION_AUTHORITY_MODE:
        _refuse("FIXTURE_EVIDENCE_RELABELED")
    claimed_result = receipt.get("result", BINDING_ONLY_RESULT)
    if claimed_result == "PASS":
        # r2 F7: `PASS` is the vocabulary of a suite RUN. This authority did not run it,
        # so a receipt claiming it is asserting something nobody here verified.
        _refuse(SUITE_NOT_EXECUTED)
    if claimed_result != BINDING_ONLY_RESULT:
        # Any other exactness claim carries no authority to grant.
        _refuse(EXACTNESS_UNAVAILABLE)
    # r2 fix class: the verifier context is snapshotted at entry, before any
    # caller-supplied object is read, and its clock judges trust-root validity.
    context, anchor_refusal = resolve_verifier_context()
    roots = validate_production_trust_root_manifest(
        trust_root_manifest,
        evaluation_instant=None if context is None else context.current_instant())
    manifest_errors = production_activation_errors(trust_root_manifest, roots)
    if PRODUCTION_SIGNING_KEY_FIXTURE_MATERIAL in manifest_errors:
        # The SIGNING-key class keeps its own name at this door too (2026-08-15 fold):
        # folding it into MEASUREMENT_TRUST_ROOT_INVALID would tell an operator their
        # manifest is malformed when in fact their production key is a committed test key.
        _refuse(PRODUCTION_SIGNING_KEY_FIXTURE_MATERIAL)
    if manifest_errors:
        _refuse("MEASUREMENT_TRUST_ROOT_INVALID")
    # r1 fix class: this is the THIRD production door, so it takes the same
    # verifier-controlled bootstrap as the other two. Without an owner-anchored
    # activation over exactly this manifest and custody set, a self-authored trust
    # root could still buy an exactness AUTHORITY BINDING.
    activation_errors = authenticated_activation_errors(
        trust_root_manifest, roots, custody_evidence, context=context,
        anchor_refusal=anchor_refusal)
    if activation_errors:
        _refuse(sorted(activation_errors)[0])
    suite, suite_hash, witness_hash = _pinned_suite()
    if measurement.canonical_json(suite_document) != measurement.canonical_json(suite):
        _refuse(EXACTNESS_UNAVAILABLE)
    bindings = _production_envelope_bindings(envelopes, roots)
    verified = {
        "schema_id": EXACTNESS_RECEIPT_SCHEMA_ID,
        "candidate_id": bindings["candidate_id"],
        "carrier_artifact_digest": bindings["carrier_artifact_digest"],
        "harness_build_digest": bindings["harness_build_digest"],
        "measurement_grid_identity_hash": bindings["measurement_grid_identity_hash"],
        "suite_id": suite["suite_id"],
        "suite_artifact_hash": suite_hash,
        "witness_set_hash": witness_hash,
        "result": BINDING_ONLY_RESULT,
        "authority_mode": PRODUCTION_AUTHORITY_MODE,
        "producer_id": bindings["producer_id"],
        "trust_root_id": trust_root_manifest["manifest_id"],
        "trust_policy_digest": bindings["trust_policy_digest"],
    }
    verified["receipt_hash"] = measurement.sha384(verified)
    if set(verified) != set(EXACTNESS_RECEIPT_V3_KEYS):
        _refuse("MEASUREMENT_SCHEMA_INVALID")
    for name, value in receipt.items():
        # Any field the claim carried must match the recomputed value exactly.
        if verified[name] != value:
            _refuse(EXACTNESS_UNAVAILABLE)
    return verified


def _pinned_suite() -> tuple[dict[str, Any], str, str]:
    """The committed carrier-exactness suite, via the frozen pure authority."""
    try:
        return measurement._exactness_suite_authority()
    except ValueError as exc:
        raise MeasurementAuthorityError(EXACTNESS_UNAVAILABLE) from exc
