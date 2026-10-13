"""BUILD B production measurement admission adapter.

Role: this module is the only path by which a *production* signed measurement
envelope set (`fixture_kind = PHYSICAL_HARNESS_RECEIPT`, `producer_role =
PHYSICAL_MEASUREMENT_PRODUCER`) may clear `PHYSICAL_HARNESS_UNAVAILABLE`. The
frozen r13 evaluator `mbcx01_r13_measurement.evaluate_measurement_receipts`
adds that sentinel unconditionally (`mbcx01_r13_measurement.py:1140`) and is
never edited; this versioned sibling adapter re-validates the full evidence
tree with the frozen pure helpers and then applies the V3 trust-root logic
(signature, role authorization, custody disjointness, validity/revocation,
ceremony receipts, grid identity, exactness authority).

Validation order (authority precedes analysis, mirroring frozen :996-1000):

1. trust-root manifest structure + custody separation + validity/revocation;
2. production activation and the four external custody-evidence documents,
   recomputed by digest, AND the owner-signed activation statement verified
   against the OPERATOR-preconfigured trust anchor (`mbcx01_build_trust_anchor`)
   — a custody or authentication failure is returned BEFORE any grid analysis,
   so an empty or forged grid can never look like a custody pass;
3. per-envelope closed key set, schema/domain/version, role authorization,
   anti-replay identity, digests and Ed25519 signature;
4. grid identity, coverage and nonce uniqueness;
5. the full `MeasurementReceiptV3` evidence tree — the frozen pure validators
   `mbcx01_r13_measurement._validate_physical_evidence` (:807-989) and, through
   it, `_validate_query_evidence` (:752-804) are CALLED, not re-implemented, so
   every shared field is judged by the frozen bytes;
6. the frozen job-level checks (mirrored from :1071-1103, cited inline because
   they live inside the frozen evaluator body and cannot be called without the
   unconditional sentinel), plus the V2-only tightenings;
7. the affordability and H-shape gates (mirrored from :1108-1137).

The adapter is at least as strict as the frozen evaluator on every shared
field, with exactly one adjudicated divergence, documented at
`_descendant_accounting_errors`: the job-level `completion_port_drained` flag
is diagnostic rather than fatal when the load-bearing terminal barrier is
independently proven (MBCX-01-R13-PHYSICAL-HARNESS-REQUIREMENTS.md §3: "Ordinary
completion messages, including active-zero, remain diagnostic because delivery
is not guaranteed"; witness bw09).

Absence, ambiguity, unsupported hardware, incomplete evidence, signature or
root failure, custody-policy failure and join mismatch all stay red; fixture
evidence never crosses into production admission.

r1 FIX CLASS — AUTHENTICATED_PRODUCTION_TRUST_BOOTSTRAP
-------------------------------------------------------
`trust_root_manifest` and `custody_evidence` remain per-request PARAMETERS, because
the manifest of record is delivered by operator configuration OUTSIDE this repository
(`MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md` §3.6) — but they are no longer TRUSTED
because they arrived. Production admission now begins from a verifier-controlled root
the request cannot supply or substitute: the owner trust anchor loaded from operator
wiring / OS configuration by `mbcx01_build_trust_anchor`. The caller-supplied graph is
admissible only when the anchor has SIGNED an activation binding the exact canonical
manifest digest and the four recomputed custody-document digests. The pre-existing
hash-match and role-separation checks are all retained, unweakened, as structural
checks on top of that authentication.

r2 FIX CLASS — FIXTURE_ISOLATION / INSTANCE-SCOPED VERIFIER CONTEXT
-------------------------------------------------------------------
r1 was right about WHERE authority comes from and wrong about WHAT HOLDS IT. This module
now resolves an immutable `ProductionVerifierContext` ONCE, at the top of `_evaluate`,
BEFORE it reads any caller-supplied object, and carries it through the whole evaluation
(`mbcx01_build_trust_anchor`). Three consequences, each with a witness:

  * a `fixture_only` anchor is refused `PRODUCTION_TRUST_ANCHOR_FIXTURE_ONLY` — the
    committed fixture anchor's private half is committed, so it is public (bw22);
  * an object graph that re-wires process authority while this evaluation is reading it
    changes nothing IN FLIGHT: the decision is made against the context snapshotted at
    entry. It is not otherwise refused — an in-process actor that re-wires the process
    is the BOX OWNER, and defending against it is theatre under the permanent T2 ceiling
    (`DESIGN-SHELF-MAP.md` §1). The r2 rider that raised
    `PRODUCTION_TRUST_ANCHOR_REWIRED_DURING_VERIFICATION` was reverted on 2026-08-14
    (`MBCX-01-BUILD-ADVERSARY-PREMISE-CORRECTION-2026-08-14.md`);
  * validity and revocation are judged at `context.current_instant()` — the operator's
    instant or the REAL clock — instead of defaulting to the `revocation.published_at`
    the manifest under evaluation chose for itself (bw24).
"""

from __future__ import annotations

import base64
import copy
import datetime
import hashlib
import re
from typing import Any

import mbcx01_build_trust_anchor as trust_anchor
import mbcx01_build_windows_producer as producer
import mbcx01_r13_measurement as measurement

PRODUCTION_ENVELOPE_DOMAIN = "MBCX01.SIGNED-MEASUREMENT-RECEIPT.V2"
PRODUCTION_ENVELOPE_VERSION = 2
PRODUCTION_ENVELOPE_SCHEMA_ID = "SignedMeasurementReceiptV2"
PRODUCTION_FIXTURE_KIND = "PHYSICAL_HARNESS_RECEIPT"
PRODUCTION_PRODUCER_ROLE = "PHYSICAL_MEASUREMENT_PRODUCER"
TRUST_ROOT_MANIFEST_SCHEMA_ID = "MeasurementTrustRootManifestV3"
TRUST_ROOT_POLICY_SCHEMA_ID = "ProductionMeasurementTrustPolicyV2"
REVOCATION_LIST_SCHEMA_ID = "MeasurementTrustRootRevocationListV1"
FAIL_LOUD_SENTINEL = "PHYSICAL_HARNESS_UNAVAILABLE"

# Closed error vocabulary for production admission. `evaluate_production_measurement`
# may only ever return a sorted subset of this set: an unlisted string, an
# unexpected traceback or a caller Boolean are all defects.
PRODUCTION_ERROR_CODES = frozenset({
    "ACTIVE_PROCESS_RACE",
    "AFFORDABILITY_LIMIT",
    "CANDIDATE_ID_MISMATCH",
    "CARRIER_EXACTNESS_AUTHORITY_UNAVAILABLE",
    "CARRIER_EXACTNESS_SUITE_NOT_EXECUTED",
    "COMPLETION_EVIDENCE_INCOMPLETE",
    "CUSTODY_SEPARATION_INVALID",
    "DESCENDANT_ACCOUNTING_MISSING",
    "EXTERNAL_WORK_UNMEASURED",
    "FINAL_QUERY_ORDERING_INVALID",
    "FIXTURE_EVIDENCE_RELABELED",
    "GENERATOR_ID_MISMATCH",
    "GRID_COVERAGE_INVALID",
    "GRID_IDENTITY_MISMATCH",
    "H_SHAPE_LIMIT",
    "INSTRUCTION_ACCOUNTING_INCOMPLETE",
    "INSTRUCTION_ACCOUNTING_MISSING",
    "INSTRUCTION_ACCOUNTING_UNSUPPORTED",
    "JOB_LIMIT_VIOLATION_TERMINATION",
    "JOB_QUERY_EVIDENCE_INVALID",
    "MEASUREMENT_CUSTODY_EVIDENCE_INVALID",
    "MEASUREMENT_ENVELOPE_INVALID",
    "MEASUREMENT_REPLAY_IDENTITY_MISMATCH",
    "MEASUREMENT_SCHEMA_INVALID",
    "MEASUREMENT_SIGNATURE_CARRIER_INVALID",
    "MEASUREMENT_SIGNATURE_INVALID",
    "MEASUREMENT_TRUST_ROOT_INVALID",
    "MONOTONIC_TIME_CROSS_CHECK_FAILED",
    "PHYSICAL_EVIDENCE_INCOMPLETE",
    "PHYSICAL_HARNESS_UNAVAILABLE",
    "PROCESS_MEMBERSHIP_INVALID",
    "PRODUCER_ROLE_UNAUTHORIZED",
    "PRODUCTION_ACTIVATION_UNAUTHENTICATED",
    "PRODUCTION_SIGNING_KEY_FIXTURE_MATERIAL",
    "PRODUCTION_TRUST_ANCHOR_FIXTURE_ONLY",
    "PRODUCTION_TRUST_ANCHOR_UNAVAILABLE",
    "TRUST_ROOT_REVOKED",
    "TRUST_ROOT_VALIDITY_EXPIRED",
    "UNSUPPORTED_MEASUREMENT_ENVIRONMENT",
})

REQUIRED_CUSTODY_EVIDENCE = (
    "SEPARATE_KEY_CUSTODY_ATTESTATION",
    "SEPARATE_TRUST_ROOT_EDITOR_APPROVAL",
    "HARNESS_BUILD_PROVENANCE",
    "PRODUCTION_SIGNING_CEREMONY_RECEIPT",
)

#: The fifth injected item: the OWNER-SIGNED activation statement (r1 fix class
#: AUTHENTICATED_PRODUCTION_TRUST_BOOTSTRAP). It is presented by the caller like the
#: four documents — and, exactly like them, it is worthless unless it verifies against
#: the anchor the OPERATOR preconfigured, which the caller cannot supply or substitute
#: (`mbcx01_build_trust_anchor`). It is required only for production ADMISSION;
#: `validate_production_trust_root_manifest` stays structural and needs none of it.
OWNER_ACTIVATION_EVIDENCE = "OWNER_CEREMONY_ACTIVATION"

#: r2 fix class named refusals, as module constants so a witness cannot mistype one.
PRODUCTION_TRUST_ANCHOR_FIXTURE_ONLY = "PRODUCTION_TRUST_ANCHOR_FIXTURE_ONLY"
PRODUCTION_TRUST_ANCHOR_UNAVAILABLE = "PRODUCTION_TRUST_ANCHOR_UNAVAILABLE"

#: 2026-08-15 fold: a production trust root whose public key is COMMITTED to this
#: repository. The anchor class of this refusal lives in `mbcx01_build_trust_anchor`
#: (`PRODUCTION_VERIFIER_CONTEXT_FIXTURE_KEY_MATERIAL`); this is the SIGNING class, which
#: a council seat executed — the committed test signing pair cleared production admission
#: under an independently generated owner anchor. It is a separate code from
#: `MEASUREMENT_TRUST_ROOT_INVALID` for the reason the anchor class is a separate code:
#: "your test key is not a production key" and "this manifest is malformed" are different
#: facts for the operator reading the log.
PRODUCTION_SIGNING_KEY_FIXTURE_MATERIAL = "PRODUCTION_SIGNING_KEY_FIXTURE_MATERIAL"
PRODUCTION_CUSTODY_EVIDENCE_KEYS = frozenset(
    set(REQUIRED_CUSTODY_EVIDENCE) | {OWNER_ACTIVATION_EVIDENCE})

# Each external custody document is bound to the policy by SHA-384 over its
# canonical bytes — the digest is recomputed, never read as a label.
CUSTODY_DIGEST_FIELDS = (
    ("SEPARATE_KEY_CUSTODY_ATTESTATION", "key_custodian_attestation_digest"),
    ("SEPARATE_TRUST_ROOT_EDITOR_APPROVAL", "trust_root_editor_approval_digest"),
    ("HARNESS_BUILD_PROVENANCE", "harness_build_provenance_digest"),
    ("PRODUCTION_SIGNING_CEREMONY_RECEIPT", "signing_ceremony_receipt_digest"),
)

MANIFEST_KEYS = {"schema_id", "manifest_id", "production_ready",
                 "activation_authority", "trust_policy", "validity",
                 "revocation", "roots"}
POLICY_KEYS = {"schema_id", "status", "fail_loud_sentinel",
               "signer_custodian_role", "trust_root_editor_role",
               "roles_must_be_distinct",
               "manifest_edit_cannot_activate_production",
               "required_external_evidence", "key_custodian_attestation_digest",
               "trust_root_editor_approval_digest",
               "harness_build_provenance_digest",
               "signing_ceremony_receipt_digest", "editor_approval_key_ids"}
REVOCATION_KEYS = {"schema_id", "revocation_list_id", "published_at",
                   "revoked_key_ids", "revocation_list_digest"}
ROOT_KEYS = {"key_id", "algorithm", "fixture_only", "authorized_producer_role",
             "authorized_fixture_kind", "signer_custodian_role",
             "authorized_harness_build_digest", "trust_policy_digest",
             "public_key_pem", "validity", "revocation_state"}
VALIDITY_KEYS = {"not_before", "not_after"}

# Roles and activation authorities are UPPER_SNAKE identifiers; the frozen
# `SEMANTIC_RE` forbids underscores, so it governs key/manifest/list ids only.
ROLE_RE = re.compile(r"^[A-Z][A-Z0-9_]{0,63}$")
TIMESTAMP_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")
#: The ONE accepted RFC-3339 UTC spelling on this plane: whole seconds, `Z`.
TIMESTAMP_FORM = "%Y-%m-%dT%H:%M:%SZ"


class MeasurementAuthorityError(ValueError):
    """Typed, closed failure of the production measurement authority."""


def _refuse(code: str) -> None:
    raise MeasurementAuthorityError(code)


def _closed(errors: set[str]) -> list[str]:
    """Return the sorted closed error list; an unlisted code is itself a defect."""
    known = {code for code in errors if code in PRODUCTION_ERROR_CODES}
    if known != set(errors):
        known.add("MEASUREMENT_SCHEMA_INVALID")
    return sorted(known)


def _authority_code(exc: MeasurementAuthorityError) -> str:
    code = str(exc)
    return code if code in PRODUCTION_ERROR_CODES else "MEASUREMENT_TRUST_ROOT_INVALID"


def parse_instant(value: Any) -> datetime.datetime | None:
    """The UTC CALENDAR instant `value` denotes, or `None` when it denotes none.

    `TIMESTAMP_RE` proves digit PLACEMENT and nothing else, so `2030-99-99T99:99:99Z`
    matched it — and because every validity comparison in this module was a STRING
    comparison, a window whose endpoints are not calendar instants still ORDERED as
    though it were a real interval. `2020-00-00T00:00:00Z .. 2030-99-99T99:99:99Z`
    therefore validated and ADMITTED a grid at a 2026 verifier instant: a malformed
    date EXTENDED production trust (codex r5 P1). A date nobody can place on a
    calendar is not a date, and refusing it stops a WRONG ADMISSION.

    Mechanism ADOPTED from the frozen layer rather than invented: the frozen
    `mbcx01_r13_common._valid_utc` (:119-126) parses with an explicit `strptime` form
    and requires the parse to ROUND-TRIP to the original spelling, which is what makes
    `2026-02-30` and `2026-2-3` both refusals. The frozen helper is not CALLED here
    because it fixes the STATE plane's six-fractional-digit spelling; this plane's
    spelling is whole seconds (`TIMESTAMP_RE`), and widening either grammar to reach
    one helper would weaken a document format. `mbcx01_build_state_authority.parse_instant`
    is the state-plane sibling, with the same round-trip mechanism.
    """
    if not isinstance(value, str) or TIMESTAMP_RE.fullmatch(value) is None:
        return None
    try:
        parsed = datetime.datetime.strptime(value, TIMESTAMP_FORM)
    except ValueError:
        return None
    if parsed.strftime(TIMESTAMP_FORM) != value:
        return None
    return parsed.replace(tzinfo=datetime.timezone.utc)


def _window_instants(window: Any) -> tuple[datetime.datetime, datetime.datetime] | None:
    """The two PARSED endpoints of a validity window, or `None` if it is not one.

    Every ordering below happens on these values, never on the strings: a comparison
    is only meaningful once both sides are known to be instants.
    """
    if not isinstance(window, dict) or set(window) != VALIDITY_KEYS:
        return None
    not_before = parse_instant(window.get("not_before"))
    not_after = parse_instant(window.get("not_after"))
    if not_before is None or not_after is None or not not_before < not_after:
        return None
    return not_before, not_after


def _valid_window(window: Any) -> bool:
    return _window_instants(window) is not None


def validate_production_trust_root_manifest(
        document: Any, *, evaluation_instant: str | None = None) -> dict[str, dict[str, Any]]:
    """Validate a `MeasurementTrustRootManifestV3` and return its roots by key id.

    Structural authority only: it accepts both the committed fixture instance
    (`production_ready:false`, `fixture_only:true` roots) and an injected
    production instance, because the fixture instance must remain a readable,
    verifiable document. Production ADMISSION additionally requires activation
    and custody evidence and lives in `evaluate_production_measurement`.

    `evaluation_instant` is the RFC-3339 instant the validity/revocation state
    is judged at. PRODUCTION ADMISSION ALWAYS SUPPLIES IT, from the verifier's
    own context (r2 fix class / codex F4): the caller's manifest does not get to
    choose the moment it is judged at. The remaining default — the revocation
    list's `published_at` — belongs to STRUCTURAL reads of a document (a fixture
    instance, a reviewer inspecting a historical manifest), where a deterministic
    instant taken from the document is a feature and no authority is granted.
    """
    if not isinstance(document, dict) or set(document) != MANIFEST_KEYS:
        _refuse("MEASUREMENT_TRUST_ROOT_INVALID")
    policy = document.get("trust_policy")
    revocation = document.get("revocation")
    roots_rows = document.get("roots")
    if (document.get("schema_id") != TRUST_ROOT_MANIFEST_SCHEMA_ID
            or measurement.SEMANTIC_RE.fullmatch(str(document.get("manifest_id"))) is None
            or not isinstance(document.get("production_ready"), bool)
            or ROLE_RE.fullmatch(str(document.get("activation_authority"))) is None
            or not isinstance(policy, dict) or set(policy) != POLICY_KEYS
            or not isinstance(revocation, dict) or set(revocation) != REVOCATION_KEYS
            or not isinstance(roots_rows, list) or not roots_rows
            or not _valid_window(document.get("validity"))):
        _refuse("MEASUREMENT_TRUST_ROOT_INVALID")
    if (policy.get("schema_id") != TRUST_ROOT_POLICY_SCHEMA_ID
            or policy.get("status") not in {"NOT_ACTIVATED", "ACTIVATED"}
            or policy.get("fail_loud_sentinel") != FAIL_LOUD_SENTINEL
            or policy.get("roles_must_be_distinct") is not True
            or policy.get("manifest_edit_cannot_activate_production") is not True
            or list(policy.get("required_external_evidence") or []) != list(REQUIRED_CUSTODY_EVIDENCE)
            or ROLE_RE.fullmatch(str(policy.get("signer_custodian_role"))) is None
            or ROLE_RE.fullmatch(str(policy.get("trust_root_editor_role"))) is None
            or any(measurement.SHA384_RE.fullmatch(str(policy.get(field))) is None
                   for _, field in CUSTODY_DIGEST_FIELDS)
            or not isinstance(policy.get("editor_approval_key_ids"), list)
            or not policy["editor_approval_key_ids"]
            or any(measurement.SEMANTIC_RE.fullmatch(str(value)) is None
                   for value in policy["editor_approval_key_ids"])
            or len(set(policy["editor_approval_key_ids"]))
            != len(policy["editor_approval_key_ids"])):
        _refuse("MEASUREMENT_TRUST_ROOT_INVALID")
    # I13 custody separation, checked mechanically and not merely declared:
    # the signing custodian role and the trust-root editor role are disjoint.
    if policy["signer_custodian_role"] == policy["trust_root_editor_role"]:
        _refuse("CUSTODY_SEPARATION_INVALID")
    if (revocation.get("schema_id") != REVOCATION_LIST_SCHEMA_ID
            or measurement.SEMANTIC_RE.fullmatch(
                str(revocation.get("revocation_list_id"))) is None
            or parse_instant(revocation.get("published_at")) is None
            or not isinstance(revocation.get("revoked_key_ids"), list)
            or any(measurement.SEMANTIC_RE.fullmatch(str(value)) is None
                   for value in revocation["revoked_key_ids"])
            or len(set(revocation["revoked_key_ids"])) != len(revocation["revoked_key_ids"])
            or revocation.get("revocation_list_digest")
            != measurement.sha384(revocation["revoked_key_ids"])):
        _refuse("MEASUREMENT_TRUST_ROOT_INVALID")
    # The instant and both window endpoints are PARSED before anything is ordered: a
    # value that is not a calendar instant is refused here, never compared (codex r5 P1).
    instant = parse_instant(
        evaluation_instant if evaluation_instant is not None else revocation["published_at"])
    if instant is None:
        _refuse("MEASUREMENT_TRUST_ROOT_INVALID")
    window = _window_instants(document["validity"])
    if not window[0] <= instant <= window[1]:
        _refuse("TRUST_ROOT_VALIDITY_EXPIRED")
    policy_digest = measurement.sha384(policy)
    revoked = set(revocation["revoked_key_ids"])
    roots: dict[str, dict[str, Any]] = {}
    for row in roots_rows:
        if (not isinstance(row, dict) or set(row) != ROOT_KEYS
                or measurement.SEMANTIC_RE.fullmatch(str(row.get("key_id"))) is None
                or row.get("algorithm") != measurement.SIGNATURE_ALGORITHM
                or not isinstance(row.get("fixture_only"), bool)
                or row.get("authorized_producer_role") != PRODUCTION_PRODUCER_ROLE
                or row.get("authorized_fixture_kind") != PRODUCTION_FIXTURE_KIND
                or row.get("signer_custodian_role") != policy["signer_custodian_role"]
                or measurement.SHA384_RE.fullmatch(
                    str(row.get("authorized_harness_build_digest"))) is None
                or row.get("trust_policy_digest") != policy_digest
                or not isinstance(row.get("public_key_pem"), str)
                or not row["public_key_pem"].startswith("-----BEGIN PUBLIC KEY-----\n")
                or not row["public_key_pem"].endswith("-----END PUBLIC KEY-----\n")
                or row.get("revocation_state") not in {"ACTIVE", "SUSPENDED", "REVOKED"}
                or not _valid_window(row.get("validity"))
                or row["key_id"] in roots):
            _refuse("MEASUREMENT_TRUST_ROOT_INVALID")
        # Signer-cannot-edit-root: a key that appears in the editor approval
        # chain has approved (or could approve) the document that authorises
        # it, which is exactly the self-authored-root attack.
        if row["key_id"] in set(policy["editor_approval_key_ids"]):
            _refuse("CUSTODY_SEPARATION_INVALID")
        if row["revocation_state"] != "ACTIVE" or row["key_id"] in revoked:
            _refuse("TRUST_ROOT_REVOKED")
        root_window = _window_instants(row["validity"])
        if (not root_window[0] <= instant <= root_window[1]
                or root_window[0] < window[0] or root_window[1] > window[1]):
            _refuse("TRUST_ROOT_VALIDITY_EXPIRED")
        roots[row["key_id"]] = copy.deepcopy(row)
    return roots


def production_activation_errors(document: dict[str, Any],
                       roots: dict[str, dict[str, Any]]) -> set[str]:
    """Production admission requires an ACTIVATED, non-fixture manifest whose roots are
    not COMMITTED key material.

    A committed instance is always `production_ready:false` with `fixture_only`
    roots, so editing this repository can never mint authority: the custody
    documents below have to recompute as well, and they exist only outside it.

    THE KEY, NOT THE LABEL — SIGNING CLASS (2026-08-15 fold). Everything above is a label
    the caller's manifest asserts about itself. A council seat took the Ed25519 test
    signing pair committed at `test_mbcx01_build_measurement.py`, made it the PRODUCTION
    signing root under an INDEPENDENTLY generated owner anchor (so not the anchor class
    the r3 fold closed), and cleared admission: `production_admission_errors = []`,
    `root_fixture_only = False`, `production_ready = True`,
    `root_is_committed_test_public = True`, custody documents asserting the private key
    never left custody. `MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md` §3 step 0 and §3 step 3
    forbid exactly that — every key in a production manifest is generated in the ceremony,
    never copied out of a committed fixture document — and prose is not a control. The
    refusal names the committed document the key is published in, and the set is DERIVED
    from the repository's own bytes (`trust_anchor.committed_fixture_key_material`).
    """
    errors: set[str] = set()
    if (document.get("production_ready") is not True
            or document.get("trust_policy", {}).get("status") != "ACTIVATED"
            or any(row.get("fixture_only") is not False for row in roots.values())):
        errors.add("MEASUREMENT_TRUST_ROOT_INVALID")
    if any(trust_anchor.committed_fixture_key_document(row.get("public_key_pem"))
           is not None for row in roots.values()):
        errors.add(PRODUCTION_SIGNING_KEY_FIXTURE_MATERIAL)
    return errors


def _custody_errors(document: dict[str, Any], roots: dict[str, dict[str, Any]],
                    custody_evidence: Any) -> tuple[set[str], str | None]:
    """Recompute the four external custody documents and their bindings.

    Returns the error set and the attested signing key id (the key the custody
    ceremony covers), which every envelope must then match.
    """
    policy = document["trust_policy"]
    if (not isinstance(custody_evidence, dict)
            or set(custody_evidence) != set(PRODUCTION_CUSTODY_EVIDENCE_KEYS)):
        return {"MEASUREMENT_CUSTODY_EVIDENCE_INVALID"}, None
    for name, field in CUSTODY_DIGEST_FIELDS:
        document_bytes = custody_evidence.get(name)
        if (not isinstance(document_bytes, dict)
                or measurement.sha384(document_bytes) != policy.get(field)):
            return {"MEASUREMENT_CUSTODY_EVIDENCE_INVALID"}, None
    attestation = custody_evidence["SEPARATE_KEY_CUSTODY_ATTESTATION"]
    approval = custody_evidence["SEPARATE_TRUST_ROOT_EDITOR_APPROVAL"]
    provenance = custody_evidence["HARNESS_BUILD_PROVENANCE"]
    ceremony = custody_evidence["PRODUCTION_SIGNING_CEREMONY_RECEIPT"]
    editors = set(policy["editor_approval_key_ids"])
    harness_digests = {row["authorized_harness_build_digest"] for row in roots.values()}
    if (attestation.get("schema_id") != "KeyCustodyAttestationV1"
            or attestation.get("custodian_role") != policy["signer_custodian_role"]
            or attestation.get("private_key_never_leaves_custody") is not True
            or measurement.SEMANTIC_RE.fullmatch(str(attestation.get("key_id"))) is None
            or approval.get("schema_id") != "TrustRootEditorApprovalV1"
            or approval.get("editor_role") != policy["trust_root_editor_role"]
            or approval.get("approver_key_id") not in editors
            or approval.get("approved_manifest_id") != document["manifest_id"]
            or not isinstance(approval.get("signer_key_ids_excluded"), list)
            or provenance.get("schema_id") != "HarnessBuildProvenanceV1"
            or provenance.get("build_reviewed") is not True
            or ROLE_RE.fullmatch(str(provenance.get("builder_role"))) is None
            or provenance.get("harness_build_digest") not in harness_digests
            or ceremony.get("schema_id") != "SigningCeremonyReceiptV1"
            or measurement.SEMANTIC_RE.fullmatch(str(ceremony.get("ceremony_id"))) is None
            or ceremony.get("candidate_and_evaluator_received_private_key") is not False
            or policy["trust_root_editor_role"] not in (ceremony.get("witness_roles") or [])
            or ceremony.get("signer_key_id") != attestation.get("key_id")):
        return {"MEASUREMENT_CUSTODY_EVIDENCE_INVALID"}, None
    # The attested signing key must be excluded from the editor approval chain
    # by the approval document itself AND absent from it in fact.
    if (attestation["key_id"] not in set(approval["signer_key_ids_excluded"])
            or attestation["key_id"] in editors):
        return {"CUSTODY_SEPARATION_INVALID"}, None
    return set(), attestation["key_id"]


def production_activation_binding(document: dict[str, Any],
                                  roots: dict[str, dict[str, Any]],
                                  custody_evidence: dict[str, Any]) -> dict[str, Any] | None:
    """The exact facts an owner activation must bind for THIS manifest and custody set.

    One definition, used by the verifier and by the fixture ceremony helper, so the
    signed statement and the checked statement can never drift apart. Every custody
    digest here is RECOMPUTED from the injected document, never read from the manifest:
    the owner signature therefore authenticates the documents themselves, not the
    caller's claims about them.
    """
    policy = document["trust_policy"]
    harness_digests = {row["authorized_harness_build_digest"] for row in roots.values()}
    if len(harness_digests) != 1:
        return None
    try:
        return {
            "authority": trust_anchor.AUTHORITY_MEASUREMENT,
            "manifest_validity": document["validity"],
            "signing_key_id": custody_evidence[
                "SEPARATE_KEY_CUSTODY_ATTESTATION"]["key_id"],
            "editor_key_ids": list(policy["editor_approval_key_ids"]),
            "custody_evidence_digests": {
                name: measurement.sha384(custody_evidence[name])
                for name in REQUIRED_CUSTODY_EVIDENCE},
            "provenance_digest": next(iter(harness_digests)),
        }
    except (KeyError, TypeError):
        return None


#: Generic trust-anchor outcomes -> this authority's closed vocabulary.
_ACTIVATION_CODES = {
    trust_anchor.ANCHOR_UNAVAILABLE: PRODUCTION_TRUST_ANCHOR_UNAVAILABLE,
    trust_anchor.ANCHOR_FIXTURE_ONLY: PRODUCTION_TRUST_ANCHOR_FIXTURE_ONLY,
    trust_anchor.ACTIVATION_UNAUTHENTICATED: "PRODUCTION_ACTIVATION_UNAUTHENTICATED",
    trust_anchor.SIGNATURE_CARRIER_INVALID: "MEASUREMENT_SIGNATURE_CARRIER_INVALID",
}


def resolve_verifier_context() -> tuple[Any, str | None]:
    """Snapshot the verifier context for ONE evaluation (r2 fix class).

    Called ONCE, at the top of each production door, BEFORE any caller-supplied object
    is read. The returned value is immutable and is threaded through the rest of the
    evaluation, so an object graph that reconfigures process authority while the
    verifier is reading it cannot change this evaluation's root of trust — and a
    `fixture_only` anchor is refused here rather than silently accepted (codex r2
    F1/F2/F3).
    """
    return trust_anchor.resolve_production_verifier_context(
        trust_anchor.AUTHORITY_MEASUREMENT)


def authenticated_activation_errors(document: dict[str, Any],
                                    roots: dict[str, dict[str, Any]],
                                    custody_evidence: Any, *,
                                    context: Any,
                                    anchor_refusal: str | None = None) -> set[str]:
    """THE production bootstrap invariant, in one place.

    No trust graph reaches production admission unless the anchor of the verifier's OWN
    context — operator-supplied and not fixture-marked — has signed a statement binding
    the exact canonical digest of THIS manifest, its validity window, the attested
    signing-key identity, the trust-root editor key set, the build provenance digest and
    the four recomputed custody-document digests. An anchor that was never configured,
    and an anchor that is fixture material, are both REFUSALS, never a bypass.
    """
    if anchor_refusal is not None:
        return {_ACTIVATION_CODES[anchor_refusal]}
    if not isinstance(custody_evidence, dict):
        return {"PRODUCTION_ACTIVATION_UNAUTHENTICATED"}
    binding = production_activation_binding(document, roots, custody_evidence)
    if binding is None:
        return {"PRODUCTION_ACTIVATION_UNAUTHENTICATED"}
    outcome = trust_anchor.authenticate_production_activation(
        custody_evidence.get(OWNER_ACTIVATION_EVIDENCE), context=context,
        manifest=document, **binding)
    if outcome is None:
        return set()
    return {_ACTIVATION_CODES[outcome]}


def _is_frozen_v1_envelope(envelope: dict[str, Any]) -> bool:
    return (envelope.get("schema_id") == "SignedMeasurementReceiptV1"
            or envelope.get("domain") == measurement.ENVELOPE_DOMAIN
            or envelope.get("version") == 1)


def _claims_production(envelope: dict[str, Any]) -> bool:
    return (envelope.get("fixture_kind") == PRODUCTION_FIXTURE_KIND
            or envelope.get("producer_role") == PRODUCTION_PRODUCER_ROLE)


def _timing_errors(envelope: dict[str, Any], receipt: Any) -> set[str]:
    """V2-only exact elapsed/QPC cross-check (tightens frozen :1099 `> 0`).

    WHICH INTERVAL (codex r2 P1). Every value compared here describes ONE
    interval: the signed member-lifetime interval, from the earliest
    `started_qpc` to the latest `ended_qpc` of the signed
    `process_membership.processes` rows — that is, from the first member's ETW
    ProcessStart to the last member's ProcessStop, in ticks of the signed QPC
    frequency. `elapsed_qpc_ticks`, `lifetimes_span_qpc` and the job's
    `elapsed_monotonic_ns` are three views of THAT interval and nothing else, so
    exact equality is the right relation and a mismatch is a real disagreement
    inside one signed preimage rather than two clocks being compared.

    The collector's own observation interval is a DIFFERENT interval — it opens
    before `CreateProcessW` and closes after the terminal barrier, so it
    contains this one — and it is deliberately absent from the signed block.
    `mbcx01_build_win32.collect()` derives both signed elapsed values from the
    two endpoints above (`_member_lifetime_endpoints`) and uses its own window
    only as a containment fence (`_check_span_within_observation_window`), which
    is what makes the equality below satisfiable on a physical run instead of
    failing every live envelope.
    """
    block = envelope.get("timing_cross_check")
    if (not isinstance(block, dict)
            or set(block) != set(producer.TIMING_CROSS_CHECK_KEYS)
            or any(not isinstance(block.get(name), int) or isinstance(block.get(name), bool)
                   or block[name] < 0 for name in sorted(producer.TIMING_CROSS_CHECK_KEYS))
            or block["qpc_frequency_hz"] <= 0
            or block["tolerance_ns"] != producer.TIMING_TOLERANCE_NS):
        return {"MONOTONIC_TIME_CROSS_CHECK_FAILED"}
    try:
        job = receipt["job_receipt"]
        lifetimes = job["evidence"]["process_membership"]["processes"]
        span = (max(int(row["ended_qpc"]) for row in lifetimes)
                - min(int(row["started_qpc"]) for row in lifetimes))
        elapsed = int(job["elapsed_monotonic_ns"])
    except (KeyError, TypeError, ValueError, AttributeError):
        return {"MONOTONIC_TIME_CROSS_CHECK_FAILED"}
    recomputed = span * 1_000_000_000 // block["qpc_frequency_hz"]
    if (block["lifetimes_span_qpc"] != span
            or block["elapsed_qpc_ticks"] != span
            or block["elapsed_monotonic_ns"] != elapsed
            or recomputed != elapsed or elapsed <= 0):
        return {"MONOTONIC_TIME_CROSS_CHECK_FAILED"}
    return set()


def _envelope_errors(envelope: Any, expected_run_id: str,
                     roots: dict[str, dict[str, Any]],
                     attested_key_id: str | None) -> tuple[set[str], dict[str, Any] | None, bool]:
    """Closed-key-set, identity, role, digest and signature checks for one envelope.

    Mirrors frozen `_verify_envelope_structure` (:707-749) field for field, with
    the V2 key set, the V2 domain/version, the V2 preimage, and three additions:
    a named `PRODUCER_ROLE_UNAUTHORIZED`, the anti-replay nonce shape and the
    binding of the signing key to the custody attestation.
    """
    errors: set[str] = set()
    if isinstance(envelope, dict) and _is_frozen_v1_envelope(envelope) and _claims_production(envelope):
        # An r13 fixture envelope relabeled with production role/kind stays
        # fixture evidence: the V1 envelope cannot carry the V2 evidence a
        # production claim requires, and relabeling is not producing.
        errors.add("FIXTURE_EVIDENCE_RELABELED")
    if not isinstance(envelope, dict) or set(envelope) != set(producer.PRODUCTION_ENVELOPE_KEYS):
        errors.add("MEASUREMENT_ENVELOPE_INVALID")
        return errors, None, False
    receipt = envelope.get("receipt")
    root = roots.get(envelope.get("signing_key_id"))
    if (envelope.get("schema_id") != PRODUCTION_ENVELOPE_SCHEMA_ID
            or envelope.get("domain") != PRODUCTION_ENVELOPE_DOMAIN
            or envelope.get("version") != PRODUCTION_ENVELOPE_VERSION
            or envelope.get("algorithm") != measurement.SIGNATURE_ALGORITHM
            or measurement.SEMANTIC_RE.fullmatch(str(envelope.get("run_id", ""))) is None
            or envelope.get("run_id") != expected_run_id
            or root is None
            or envelope.get("fixture_kind") != root.get("authorized_fixture_kind")
            or envelope.get("producer_role") != root.get("authorized_producer_role")
            or envelope.get("trust_policy_digest") != root.get("trust_policy_digest")
            or not isinstance(receipt, dict)):
        errors.add("MEASUREMENT_ENVELOPE_INVALID")
    if root is not None and envelope.get("producer_role") != root.get("authorized_producer_role"):
        errors.add("PRODUCER_ROLE_UNAUTHORIZED")
    if root is not None and envelope.get("fixture_kind") != root.get("authorized_fixture_kind"):
        errors.add("FIXTURE_EVIDENCE_RELABELED")
    if attested_key_id is not None and envelope.get("signing_key_id") != attested_key_id:
        errors.add("MEASUREMENT_CUSTODY_EVIDENCE_INVALID")
    if measurement.SEMANTIC_RE.fullmatch(str(envelope.get("nonce", ""))) is None:
        errors.add("MEASUREMENT_REPLAY_IDENTITY_MISMATCH")
    if isinstance(receipt, dict):
        try:
            expected_cell = measurement._cell_id(receipt)
        except (KeyError, TypeError):
            expected_cell = None
        if envelope.get("cell_id") != expected_cell or envelope.get("run_id") != expected_run_id:
            errors.add("MEASUREMENT_REPLAY_IDENTITY_MISMATCH")
        if (envelope.get("subject_digest") != measurement.sha384(receipt)
                or envelope.get("environment_digest") != receipt.get("job_receipt", {}).get(
                    "evidence", {}).get("harness_identity", {}).get("host_environment_digest")):
            errors.add("MEASUREMENT_ENVELOPE_INVALID")
    errors |= _timing_errors(envelope, receipt)
    if root is None:
        errors.add("MEASUREMENT_SIGNATURE_INVALID")
        return errors, receipt if isinstance(receipt, dict) else None, False
    signature_candidate = True
    # The signature CARRIER is judged before any cryptography. `b64decode(validate=True)`
    # already refused the alphabet, but not a non-canonical encoding of the same 64
    # bytes, so one signature could still have more than one accepted carrier string
    # (MBCX01-BUILD-R1-SIGNATURE-CARRIER / codex F6). Grammar + padding + length +
    # decode/re-encode equality makes the mapping one-to-one, and the refusal is NAMED
    # rather than folded into the generic signature failure. This subsumes the previous
    # `len(signature) != 64` check.
    if not trust_anchor.strict_signature_carrier_ok(envelope.get("signature_b64")):
        errors.add("MEASUREMENT_SIGNATURE_CARRIER_INVALID")
        signature_candidate = False
    try:
        preimage = producer.production_receipt_preimage(envelope)
        supplied = base64.b64decode(envelope.get("receipt_preimage_b64", ""), validate=True)
        if (supplied != preimage
                or envelope.get("receipt_digest")
                != hashlib.sha384(preimage).hexdigest().upper()):
            errors.add("MEASUREMENT_SIGNATURE_INVALID")
            signature_candidate = False
    except (ValueError, TypeError, KeyError):
        errors.add("MEASUREMENT_SIGNATURE_INVALID")
        signature_candidate = False
    return errors, receipt if isinstance(receipt, dict) else None, signature_candidate


def _descendant_accounting_errors(job: dict[str, Any],
                                  evidence: Any) -> set[str]:
    """Frozen :1071-1080 descendant-accounting checks, plus the barrier rule.

    ADJUDICATED DIVERGENCE (the only one): frozen :1079 requires
    `completion_port_drained is True`. MBCX-01-R13-PHYSICAL-HARNESS-REQUIREMENTS.md
    §3 states that ordinary completion messages, including active-zero, remain
    diagnostic because delivery is not guaranteed, and witness bw09 pins that a
    cell whose load-bearing evidence holds is not failed by lost messages.
    So a non-drained port is tolerated ONLY when the stronger terminal barrier
    is independently proven: every signed member terminal, final active
    processes zero in both the completion record and the final query, and both
    final queries collected after that barrier. Everything else in the frozen
    check is applied unchanged.
    """
    errors: set[str] = set()
    if (job["receipt_source"] != producer.PRODUCTION_RECEIPT_SOURCE
            or measurement.SEMANTIC_RE.fullmatch(str(job["job_object_id"])) is None
            or job["root_process_id"] <= 0 or job["created_suspended"] is not True
            or job["completion_port_associated_before_resume"] is not True
            or job["assigned_before_resume"] is not True
            or job["breakaway_enabled"] is not False
            or job["silent_breakaway_enabled"] is not False
            or job["active_processes_at_final_query"] != 0):
        errors.add("DESCENDANT_ACCOUNTING_MISSING")
    if job["completion_port_drained"] is not True and not _terminal_barrier_proven(evidence):
        errors.add("DESCENDANT_ACCOUNTING_MISSING")
    return errors


def _terminal_barrier_proven(evidence: Any) -> bool:
    if not isinstance(evidence, dict):
        return False
    completion = evidence.get("completion")
    membership = evidence.get("process_membership")
    queries = evidence.get("job_queries")
    if not isinstance(completion, dict) or not isinstance(membership, dict):
        return False
    processes = membership.get("processes")
    if not isinstance(processes, list) or not processes:
        return False
    if any(not isinstance(row, dict) or row.get("terminal_status") != "EXITED"
           for row in processes):
        return False
    if (completion.get("all_members_terminal") is not True
            or completion.get("final_active_processes") != 0):
        return False
    if not isinstance(queries, dict) or set(queries) != measurement.QUERY_BUNDLE_KEYS:
        return False
    return all(isinstance(row, dict)
               and row.get("collected_after_terminal_barrier") is True
               for row in queries.values())


def _final_query_ordering_errors(evidence: Any) -> set[str]:
    """V2-only named ordering failure (frozen folds it into JOB_QUERY_EVIDENCE_INVALID)."""
    queries = evidence.get("job_queries") if isinstance(evidence, dict) else None
    if not isinstance(queries, dict) or set(queries) != measurement.QUERY_BUNDLE_KEYS:
        return {"FINAL_QUERY_ORDERING_INVALID"}
    if any(not isinstance(row, dict)
           or row.get("collected_after_terminal_barrier") is not True
           for row in queries.values()):
        return {"FINAL_QUERY_ORDERING_INVALID"}
    return set()


def _instruction_accounting_errors(job: dict[str, Any]) -> set[str]:
    """Frozen :1081-1098 instruction/ETW checks, mirrored verbatim."""
    errors: set[str] = set()
    if (job["instruction_backend"] not in {measurement.INSTRUCTION_MODE,
                                           "ETW_PMC_SAMPLED_PROFILE_V1"}
            or job["instruction_profile_source"] != measurement.INSTRUCTION_SOURCE
            or job["instruction_event_list"] != measurement.INSTRUCTION_EVENT_LIST
            or job["instruction_attribution"] != measurement.INSTRUCTION_ATTRIBUTION
            or job["retired_instructions"] <= 0):
        errors.add("INSTRUCTION_ACCOUNTING_MISSING")
    if job["instruction_backend"] != measurement.INSTRUCTION_MODE:
        errors.add("INSTRUCTION_ACCOUNTING_UNSUPPORTED")
    if (job["etw_capability_query_succeeded"] is not True
            or job["etw_pmc_source_available"] is not True
            or job["etw_max_pmc_counters"] < 1
            or job["etw_counter_owner_conflict_count"] != 0
            or job["etw_pmc_strict_mode"] is not True
            or job["etw_pmc_multiplexing_detected"] is not False
            or job["etw_events_lost"] != 0 or job["etw_log_buffers_lost"] != 0
            or job["etw_realtime_buffers_lost"] != 0
            or job["etw_attribution_complete"] is not True):
        errors.add("INSTRUCTION_ACCOUNTING_INCOMPLETE")
    return errors


def _receipt_errors(receipt: dict[str, Any]) -> tuple[set[str], tuple[int, int, int] | None,
                                                      dict[str, Any] | None]:
    """Full evidence-tree admission for one receipt.

    Frozen schema/job checks (:1046-1103) are mirrored here because they live
    inside the frozen evaluator body; the evidence tree itself is judged by the
    frozen pure validators, which are CALLED, not copied.
    """
    errors: set[str] = set()
    job = receipt.get("job_receipt")
    if (set(receipt) != measurement.RECEIPT_KEYS
            or receipt.get("schema_id") != "MeasurementReceiptV3"
            or measurement.SEMANTIC_RE.fullmatch(str(receipt.get("candidate_id", ""))) is None
            or measurement.SHA384_RE.fullmatch(
                str(receipt.get("candidate_artifact_digest", ""))) is None
            or measurement.SHA384_RE.fullmatch(str(receipt.get("generator_digest", ""))) is None
            or any(not isinstance(receipt.get(axis), int) or isinstance(receipt.get(axis), bool)
                   for axis in ("H", "D", "F"))
            or receipt.get("H") not in measurement.H_VALUES
            or receipt.get("D") not in measurement.D_VALUES
            or receipt.get("F") not in measurement.F_VALUES
            or not isinstance(job, dict) or set(job or {}) != measurement.JOB_KEYS):
        return {"MEASUREMENT_SCHEMA_INVALID"}, None, None
    integer_fields = (
        "root_process_id", "active_processes_at_final_query", "user_time_ns",
        "total_page_faults", "total_processes", "total_terminated_processes",
        "kernel_time_ns", "read_operations", "write_operations", "other_operations",
        "read_transfer_bytes", "write_transfer_bytes", "other_transfer_bytes",
        "peak_committed_bytes", "elapsed_monotonic_ns", "retired_instructions",
        "etw_max_pmc_counters", "etw_counter_owner_conflict_count", "etw_events_lost",
        "etw_log_buffers_lost", "etw_realtime_buffers_lost")
    if any(not isinstance(job[name], int) or isinstance(job[name], bool) or job[name] < 0
           for name in integer_fields):
        return {"MEASUREMENT_SCHEMA_INVALID"}, None, None
    coordinate = (receipt["H"], receipt["D"], receipt["F"])
    evidence = job.get("evidence")
    errors |= _descendant_accounting_errors(job, evidence)
    errors |= _instruction_accounting_errors(job)
    if job["elapsed_monotonic_ns"] <= 0:
        errors.add("MEASUREMENT_SCHEMA_INVALID")
    if receipt["external_work_policy"] != "NETWORK_EGRESS_DENIED_NO_EXTERNAL_COMPUTE":
        errors.add("EXTERNAL_WORK_UNMEASURED")
    # The frozen evidence-tree validators, called on the identical evidence
    # shape: membership, raw 96/144-byte query ABI, completion, external
    # enforcement, environment and the full ETW attribution join.
    errors |= measurement._validate_physical_evidence(job, evidence)
    errors |= _final_query_ordering_errors(evidence)
    # V2-only named refusals. The frozen evaluator folds each of these into a
    # broader code; production admission names the mechanism that failed.
    if job["total_terminated_processes"] != 0:
        # Harness requirements §3: TotalTerminatedProcesses counts Job-limit
        # violation kills, never ordinary exits; a clean cell requires zero.
        errors.add("JOB_LIMIT_VIOLATION_TERMINATION")
    membership = evidence.get("process_membership") if isinstance(evidence, dict) else None
    roster = membership.get("processes") if isinstance(membership, dict) else None
    if not isinstance(roster, list) or job["total_processes"] != len(roster):
        errors.add("PROCESS_MEMBERSHIP_INVALID")
    completion = evidence.get("completion") if isinstance(evidence, dict) else None
    if (not isinstance(completion, dict)
            or completion.get("final_active_processes") != 0
            or completion.get("all_members_terminal") is not True
            or job["active_processes_at_final_query"] != 0):
        errors.add("ACTIVE_PROCESS_RACE")
    return errors, coordinate, job


def _gate_errors(jobs_by_coordinate: dict[tuple[int, int, int], dict[str, Any]]) -> set[str]:
    """Affordability and H-shape gates, mirrored from frozen :1108-1137."""
    errors: set[str] = set()
    jobs = list(jobs_by_coordinate.values())
    for job in jobs:
        if (job["retired_instructions"] > 3_000_000
                or job["user_time_ns"] + job["kernel_time_ns"] > 150_000_000
                or job["peak_committed_bytes"] > 201_326_592
                or job["elapsed_monotonic_ns"] > 300_000_000
                or sum(job[name] for name in ("read_transfer_bytes", "write_transfer_bytes",
                                              "other_transfer_bytes")) > 67_108_864):
            errors.add("AFFORDABILITY_LIMIT")
    for d in measurement.D_VALUES:
        for f in measurement.F_VALUES:
            group = [job for (_, group_d, group_f), job in jobs_by_coordinate.items()
                     if group_d == d and group_f == f]
            if len(group) != 4:
                continue
            metrics = (
                (lambda job: job["retired_instructions"], 500_000),
                (lambda job: job["user_time_ns"] + job["kernel_time_ns"], 75_000_000),
                (lambda job: job["elapsed_monotonic_ns"], 75_000_000),
                (lambda job: job["peak_committed_bytes"], 67_108_864),
                (lambda job: sum(job[name] for name in
                                 ("read_transfer_bytes", "write_transfer_bytes",
                                  "other_transfer_bytes")), 16_777_216),
                (lambda job: sum(job[name] for name in
                                 ("read_operations", "write_operations", "other_operations")),
                 4_096),
            )
            if any(max(project(row) for row in group) - min(project(row) for row in group) > limit
                   for project, limit in metrics):
                errors.add("H_SHAPE_LIMIT")
    return errors


def evaluate_production_measurement(envelopes: Any, *, trust_root_manifest: Any,
                                    custody_evidence: Any,
                                    expected_run_id: str) -> list[str]:
    """Admit a production measurement grid, or return a closed sorted error list.

    An empty list means the grid is admitted and `PHYSICAL_HARNESS_UNAVAILABLE`
    is discharged for this envelope set only. Any defect returns that sentinel
    alongside the named cause: admission is never satisfied by a caller
    Boolean, a label, a self-hash or an outer receipt repair.
    """
    try:
        return _evaluate(envelopes, trust_root_manifest, custody_evidence,
                         expected_run_id)
    except (KeyError, TypeError, ValueError, AttributeError, IndexError, OverflowError):
        # A closed list, never a traceback: malformed input is a named verdict.
        return _closed({"MEASUREMENT_ENVELOPE_INVALID", FAIL_LOUD_SENTINEL})


def _evaluate(envelopes: Any, trust_root_manifest: Any, custody_evidence: Any,
              expected_run_id: str) -> list[str]:
    errors: set[str] = set()
    # (0) The verifier context is snapshotted BEFORE any caller object is read (r2 fix
    # class): its anchor and its clock decide this evaluation, whatever happens to
    # process state while the caller's data is being walked.
    context, anchor_refusal = resolve_verifier_context()
    # (1) Authority precedes grid analysis, mirroring frozen :996-1000. Validity and
    # revocation are judged at the VERIFIER's instant, never at an instant the manifest
    # under evaluation chose for itself (codex r2 F4; Go's `VerifyOptions.CurrentTime`).
    try:
        roots = validate_production_trust_root_manifest(
            trust_root_manifest,
            evaluation_instant=None if context is None else context.current_instant())
    except MeasurementAuthorityError as exc:
        return _closed({_authority_code(exc), FAIL_LOUD_SENTINEL})
    errors |= production_activation_errors(trust_root_manifest, roots)
    custody_errors, attested_key_id = _custody_errors(trust_root_manifest, roots, custody_evidence)
    errors |= custody_errors
    if not custody_errors:
        # (1b) AUTHENTICATION, not merely internal consistency: the custody set above
        # is a graph the CALLER supplied, so it is admissible only once the anchor of
        # the verifier's own context has signed exactly this manifest and exactly these
        # documents (r1 fix class, r2 fixture isolation).
        errors |= authenticated_activation_errors(
            trust_root_manifest, roots, custody_evidence, context=context,
            anchor_refusal=anchor_refusal)
    if errors:
        # (2) Custody failure is terminal: no grid may be analysed under an
        # unproven root, so a forged or empty grid cannot mask it.
        return _closed(errors | {FAIL_LOUD_SENTINEL})
    if not isinstance(envelopes, list):
        return _closed({"MEASUREMENT_ENVELOPE_INVALID", "GRID_COVERAGE_INVALID",
                        FAIL_LOUD_SENTINEL})
    # (3) Per-envelope structure, identity, role and signature.
    receipts: list[dict[str, Any]] = []
    signature_candidates: list[dict[str, Any]] = []
    nonces: list[str] = []
    for envelope in envelopes:
        row_errors, receipt, is_candidate = _envelope_errors(
            envelope, expected_run_id, roots, attested_key_id)
        errors |= row_errors
        if receipt is not None:
            receipts.append(receipt)
        if is_candidate:
            signature_candidates.append(envelope)
        if isinstance(envelope, dict) and isinstance(envelope.get("nonce"), str):
            nonces.append(envelope["nonce"])
    if signature_candidates:
        items = [{"payload_b64": envelope["receipt_preimage_b64"],
                  "public_key_pem": roots[envelope["signing_key_id"]]["public_key_pem"],
                  "signature_b64": envelope["signature_b64"]}
                 for envelope in signature_candidates]
        try:
            if not all(measurement._invoke_signature_verifier(items)):
                errors.add("MEASUREMENT_SIGNATURE_INVALID")
        except ValueError:
            errors.add("MEASUREMENT_SIGNATURE_INVALID")
    # (4) Grid identity, coverage and anti-replay uniqueness.
    if len(envelopes) != 100 or len(receipts) != 100:
        errors.add("GRID_COVERAGE_INVALID")
    if len(set(nonces)) != len(envelopes) or len(nonces) != len(envelopes):
        errors.add("MEASUREMENT_REPLAY_IDENTITY_MISMATCH")
    if len({row.get("candidate_id") for row in receipts}) != 1:
        errors.add("CANDIDATE_ID_MISMATCH")
    if len({row.get("candidate_artifact_digest") for row in receipts}) != 1:
        errors.add("GRID_IDENTITY_MISMATCH")
    if len({row.get("generator_digest") for row in receipts}) != 1:
        errors.add("GENERATOR_ID_MISMATCH")
    identity_hashes = set()
    for envelope in envelopes:
        try:
            identity_hashes.add(measurement.sha384(
                measurement._grid_identity_preimage(envelope)))
        except (KeyError, TypeError, AttributeError):
            errors.add("GRID_IDENTITY_MISMATCH")
    if len(identity_hashes) != 1:
        errors.add("GRID_IDENTITY_MISMATCH")
    # (5) The evidence tree, cell by cell.
    jobs_by_coordinate: dict[tuple[int, int, int], dict[str, Any]] = {}
    coordinates: list[tuple[int, int, int]] = []
    for receipt in receipts:
        receipt_errors, coordinate, job = _receipt_errors(receipt)
        errors |= receipt_errors
        if coordinate is not None and job is not None:
            coordinates.append(coordinate)
            jobs_by_coordinate[coordinate] = job
    expected = {(h, d, f) for h in measurement.H_VALUES for d in measurement.D_VALUES
                for f in measurement.F_VALUES}
    if set(coordinates) != expected or len(coordinates) != len(set(coordinates)):
        errors.add("GRID_COVERAGE_INVALID")
    # (6) Gates.
    errors |= _gate_errors(jobs_by_coordinate)
    if errors:
        errors.add(FAIL_LOUD_SENTINEL)
    return _closed(errors)
