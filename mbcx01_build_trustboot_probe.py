"""RED-WITNESS PROBE — reproduces the r1 NO-GO attacks on the CURRENT bytes.

This script is evidence, not an authority: it constructs the two EXECUTED attack
shapes banked by SEAT2 (ChatGPT Sol) and SEAT3 (codex-exec) in the BUILD
acceptance r1 round, plus ChatGPT's false-REJECT corollary and codex F6's
signature-carrier malleability, and prints what the reviewed BUILD verifiers
answer.

Attack shapes (all reachable by the packet's declared `api-caller` adversary,
which reaches the authority only through DATA it supplies):

  A  BUILD B — fully self-authored measurement universe: a FRESH attacker
     Ed25519 key, an attacker-authored `MeasurementTrustRootManifestV3`,
     attacker-authored custody documents, and 100 attacker-signed envelopes.
     Expected AFTER the fix: a named refusal BEFORE any grid analysis.
  B  BUILD A — fully self-authored state universe: a FRESH attacker Ed25519
     key, an attacker-authored `StateTrustRootManifestV1`, arbitrary custody
     digests (codex F1 used "A"*96), an attacker-signed `StateAuthorityReceiptV2`.
     Expected AFTER the fix: a named refusal before scientific admission.
  C  BUILD A false-REJECT — the ceremony spec's own production-shaped manifest
     (`production_ready:true`, `ACTIVATED`, roots not `fixture_only`) is refused
     `STATE_AUTHORITY_V2_ROOT_NOT_TRUSTED`. Expected AFTER the fix: admitted
     when, and only when, the operator-anchored activation authenticates it.
  D  codex F6 — a whitespace-injected but otherwise valid Ed25519 signature
     carrier is accepted. Expected AFTER the fix: a named carrier refusal.

NO experiment, provider call, network call, physical collection or signing
ceremony happens here. Every key is a labelled FIXTURE/attacker test key.
"""

from __future__ import annotations

import base64
import copy
import json

import mbcx01_r13_common as common
import mbcx01_r13_measurement as measurement
import mbcx01_r13_packets as packets

import mbcx01_build_measurement_authority as measurement_authority
import mbcx01_build_state_authority as state_authority
import mbcx01_build_state_store as store_mod
import mbcx01_build_windows_producer as producer

import test_mbcx01_build_measurement as bw
import test_mbcx01_build_state as ba

# FIXTURE-ONLY attacker keys, generated for this probe. The `.TEST.` marker in
# the key ids is required only by `FixtureSigner`'s test-key guard; it is not
# read by any admission check, so it does not weaken the attack.
ATTACKER_MEASUREMENT_KEY_ID = "ATTACKER.SELF.AUTHORED.MEASUREMENT.TEST.1"
ATTACKER_MEASUREMENT_PRIVATE_PEM = (
    "-----BEGIN PRIVATE KEY-----\n"
    "MC4CAQAwBQYDK2VwBCIEIEQ88tt0UVLFKV++UEwMgBsw0p8vw/zkqIBKAcuh3HRq\n"
    "-----END PRIVATE KEY-----\n")
ATTACKER_MEASUREMENT_PUBLIC_PEM = (
    "-----BEGIN PUBLIC KEY-----\n"
    "MCowBQYDK2VwAyEAvQ1p7m2R4nT8y5vRCV9PtvoLcrx1koVrfTxqpOpoKNQ=\n"
    "-----END PUBLIC KEY-----\n")

ATTACKER_STATE_KEY_ID = "ATTACKER.SELF.AUTHORED.STATE.TEST.1"
ATTACKER_STATE_PRIVATE_PEM = (
    "-----BEGIN PRIVATE KEY-----\n"
    "MC4CAQAwBQYDK2VwBCIEIDQz+qAQTbN/9tw5KAPKhmqByyJXcsIjovqLX+7d/1Zo\n"
    "-----END PRIVATE KEY-----\n")
ATTACKER_STATE_PUBLIC_PEM = (
    "-----BEGIN PUBLIC KEY-----\n"
    "MCowBQYDK2VwAyEAvu/Y1LEMLW3gt9rXWr0WKe3JilD+nAeecpgLWD/3C0I=\n"
    "-----END PUBLIC KEY-----\n")


# ---- A: self-authored measurement universe ---------------------------------------


def attacker_measurement_custody_documents() -> dict:
    """Four custody documents the attacker writes for itself."""
    return {
        "SEPARATE_KEY_CUSTODY_ATTESTATION": {
            "schema_id": "KeyCustodyAttestationV1",
            "custodian_role": "ATTACKER_NAMED_CUSTODIAN_ROLE",
            "key_id": ATTACKER_MEASUREMENT_KEY_ID,
            "private_key_never_leaves_custody": True,
            "attested_by": "ATTACKER.SELF.AUTHORED.OFFICER"},
        "SEPARATE_TRUST_ROOT_EDITOR_APPROVAL": {
            "schema_id": "TrustRootEditorApprovalV1",
            "editor_role": "ATTACKER_NAMED_EDITOR_ROLE",
            "approver_key_id": "ATTACKER.SELF.AUTHORED.EDITOR.TEST.1",
            "approved_manifest_id": "ATTACKER.SELF.AUTHORED.MEASUREMENT.MANIFEST",
            "signer_key_ids_excluded": [ATTACKER_MEASUREMENT_KEY_ID]},
        "HARNESS_BUILD_PROVENANCE": {
            "schema_id": "HarnessBuildProvenanceV1",
            "harness_build_digest": bw.HARNESS_IDENTITY["harness_build_digest"],
            "build_reviewed": True,
            "builder_role": "ATTACKER_NAMED_BUILDER_ROLE"},
        "PRODUCTION_SIGNING_CEREMONY_RECEIPT": {
            "schema_id": "SigningCeremonyReceiptV1",
            "ceremony_id": "ATTACKER.SELF.AUTHORED.CEREMONY",
            "signer_key_id": ATTACKER_MEASUREMENT_KEY_ID,
            "witness_roles": ["ATTACKER_NAMED_EDITOR_ROLE"],
            "candidate_and_evaluator_received_private_key": False},
    }


def attacker_measurement_manifest(documents: dict) -> dict:
    policy = {
        "schema_id": "ProductionMeasurementTrustPolicyV2",
        "status": "ACTIVATED",
        "fail_loud_sentinel": "PHYSICAL_HARNESS_UNAVAILABLE",
        "signer_custodian_role": "ATTACKER_NAMED_CUSTODIAN_ROLE",
        "trust_root_editor_role": "ATTACKER_NAMED_EDITOR_ROLE",
        "roles_must_be_distinct": True,
        "manifest_edit_cannot_activate_production": True,
        "required_external_evidence": list(
            measurement_authority.REQUIRED_CUSTODY_EVIDENCE),
        "key_custodian_attestation_digest": measurement.sha384(
            documents["SEPARATE_KEY_CUSTODY_ATTESTATION"]),
        "trust_root_editor_approval_digest": measurement.sha384(
            documents["SEPARATE_TRUST_ROOT_EDITOR_APPROVAL"]),
        "harness_build_provenance_digest": measurement.sha384(
            documents["HARNESS_BUILD_PROVENANCE"]),
        "signing_ceremony_receipt_digest": measurement.sha384(
            documents["PRODUCTION_SIGNING_CEREMONY_RECEIPT"]),
        "editor_approval_key_ids": ["ATTACKER.SELF.AUTHORED.EDITOR.TEST.1"],
    }
    root = {
        "key_id": ATTACKER_MEASUREMENT_KEY_ID,
        "algorithm": "ED25519",
        "fixture_only": False,
        "authorized_producer_role": producer.PRODUCTION_PRODUCER_ROLE,
        "authorized_fixture_kind": producer.PRODUCTION_FIXTURE_KIND,
        "signer_custodian_role": "ATTACKER_NAMED_CUSTODIAN_ROLE",
        "authorized_harness_build_digest": bw.HARNESS_IDENTITY["harness_build_digest"],
        "trust_policy_digest": measurement.sha384(policy),
        "public_key_pem": ATTACKER_MEASUREMENT_PUBLIC_PEM,
        "validity": {"not_before": "2026-08-14T00:00:00Z",
                     "not_after": "2027-08-14T00:00:00Z"},
        "revocation_state": "ACTIVE",
    }
    revoked: list[str] = []
    return {
        "schema_id": "MeasurementTrustRootManifestV3",
        "manifest_id": "ATTACKER.SELF.AUTHORED.MEASUREMENT.MANIFEST",
        "production_ready": True,
        "activation_authority": "ATTACKER_DECLARED_ACTIVATION_AUTHORITY",
        "trust_policy": policy,
        "validity": {"not_before": "2026-08-14T00:00:00Z",
                     "not_after": "2027-08-14T00:00:00Z"},
        "revocation": {
            "schema_id": "MeasurementTrustRootRevocationListV1",
            "revocation_list_id": "ATTACKER.SELF.AUTHORED.REVOCATION.LIST",
            "published_at": "2026-08-14T00:00:00Z",
            "revoked_key_ids": revoked,
            "revocation_list_digest": measurement.sha384(revoked)},
        "roots": [root],
    }


def probe_a() -> list[str]:
    documents = attacker_measurement_custody_documents()
    manifest = attacker_measurement_manifest(documents)
    signer = producer.FixtureSigner(ATTACKER_MEASUREMENT_KEY_ID,
                                    ATTACKER_MEASUREMENT_PRIVATE_PEM)
    identity = bw.simulated_identity(
        signing_key_id=ATTACKER_MEASUREMENT_KEY_ID,
        trust_policy_digest=manifest["roots"][0]["trust_policy_digest"])
    grid = bw.simulated_production_grid(signer=signer, identity=identity)
    assert len(grid) == 100
    return measurement_authority.evaluate_production_measurement(
        grid, trust_root_manifest=manifest, custody_evidence=documents,
        expected_run_id=bw.RUN_ID)


# ---- B/C: self-authored state universe, and the ceremony-shaped false reject ------


def attacker_state_manifest() -> dict:
    """An attacker-authored `StateTrustRootManifestV1` in the shape the verifier wants."""
    manifest = copy.deepcopy(ba._load_trust_root_manifest())
    manifest["manifest_id"] = "ATTACKER.SELF.AUTHORED.STATE.MANIFEST"
    policy = manifest["trust_policy"]
    policy["signer_custodian_role"] = "ATTACKER_NAMED_STATE_CUSTODIAN"
    policy["trust_root_editor_role"] = "ATTACKER_NAMED_STATE_EDITOR"
    manifest["trust_policy_digest"] = common.sha384(policy)
    manifest["custody_roles"]["signer_custodian_role"] = "ATTACKER_NAMED_STATE_CUSTODIAN"
    manifest["custody_roles"]["trust_root_editor_role"] = "ATTACKER_NAMED_STATE_EDITOR"
    for root in manifest["roots"]:
        root["trust_policy_digest"] = manifest["trust_policy_digest"]
    writer = manifest["roots"][0]
    writer["key_id"] = ATTACKER_STATE_KEY_ID
    writer["public_key_pem"] = ATTACKER_STATE_PUBLIC_PEM
    return manifest


def attacker_state_custody() -> dict:
    """codex F1: four alleged custody digests, all the same arbitrary "A"*96."""
    return {
        "signer_custodian_role": "ATTACKER_NAMED_STATE_CUSTODIAN",
        "trust_root_editor_role": "ATTACKER_NAMED_STATE_EDITOR",
        "signer_key_ids": [ATTACKER_STATE_KEY_ID],
        "root_editor_key_ids": ["ATTACKER.SELF.AUTHORED.STATE.EDITOR.TEST.1"],
        "key_custody_attestation_digest": "A" * 96,
        "root_editor_approval_digest": "A" * 96,
        "store_build_provenance_digest": "A" * 96,
        "signing_ceremony_receipt_digest": "A" * 96,
    }


def _packet_graph():
    expected_manifest = packets.packet_fixture_manifest()
    scorer_input = packets.build_scoring_fixture(expected_manifest, "OM")
    transition = scorer_input["transition_authority"]
    return expected_manifest, scorer_input, (
        copy.deepcopy(transition["precommit_state"]),
        copy.deepcopy(transition["proposal_event"]),
        copy.deepcopy(transition["applied_child_event"]),
        copy.deepcopy(transition["postcommit_state"]))


def probe_b() -> tuple[list[str], list[str]]:
    expected_manifest, scorer_input, graph = _packet_graph()
    precommit, proposal, child, postcommit = graph
    store = store_mod.SingleWriterStateStore.open_verified(
        store_mod.MEMORY_PATH, store_id=ba.IDENTITY_CONFIG["store_id"],
        namespace=ba.IDENTITY_CONFIG["namespace"],
        namespace_version=ba.IDENTITY_CONFIG["namespace_version"])
    request = {"transaction_commit_id": ba.TRANSACTION_ID, "prestate": precommit,
               "proposal_event": proposal, "applied_child_event": child}
    store.commit_transition(request, anti_replay=ba.ANTI_REPLAY_ANCHORS)
    manifest = attacker_state_manifest()
    receipt = ba._v2_receipt(
        precommit, proposal, child, postcommit,
        identity={"signer_key_id": ATTACKER_STATE_KEY_ID,
                  "trust_root_id": manifest["manifest_id"],
                  "trust_policy_digest": manifest["trust_policy_digest"]},
        private_key_pem=ATTACKER_STATE_PRIVATE_PEM)
    custody = attacker_state_custody()
    verify_errors = state_authority.verify_state_authority_receipt_v2(
        receipt, trust_root_manifest=manifest, custody_evidence=custody,
        require_production=True)
    admit_errors = state_authority.verify_production_scorer_input(
        scorer_input, receipt, expected_manifest=expected_manifest,
        trust_root_manifest=manifest, custody_evidence=custody)
    store.close()
    return verify_errors, admit_errors


def probe_c() -> list[str]:
    """The ceremony spec's own production-shaped manifest, honestly presented."""
    expected_manifest, scorer_input, graph = _packet_graph()
    precommit, proposal, child, postcommit = graph
    store = store_mod.SingleWriterStateStore.open_verified(
        store_mod.MEMORY_PATH, store_id=ba.IDENTITY_CONFIG["store_id"],
        namespace=ba.IDENTITY_CONFIG["namespace"],
        namespace_version=ba.IDENTITY_CONFIG["namespace_version"])
    request = {"transaction_commit_id": ba.TRANSACTION_ID, "prestate": precommit,
               "proposal_event": proposal, "applied_child_event": child}
    store.commit_transition(request, anti_replay=ba.ANTI_REPLAY_ANCHORS)
    manifest = copy.deepcopy(ba._load_trust_root_manifest())
    manifest["production_ready"] = True
    manifest["trust_policy"]["status"] = "ACTIVATED"
    manifest["trust_policy_digest"] = common.sha384(manifest["trust_policy"])
    for root in manifest["roots"]:
        root["fixture_only"] = False
        root["trust_policy_digest"] = manifest["trust_policy_digest"]
    receipt = ba._v2_receipt(
        precommit, proposal, child, postcommit,
        identity={"trust_policy_digest": manifest["trust_policy_digest"]})
    errors = state_authority.verify_state_authority_receipt_v2(
        receipt, trust_root_manifest=manifest, custody_evidence=ba.CUSTODY_EVIDENCE,
        require_production=True)
    store.close()
    return errors


# ---- D: signature carrier malleability (codex F6) ---------------------------------


def probe_d() -> tuple[list[str], list[str]]:
    expected_manifest, scorer_input, graph = _packet_graph()
    precommit, proposal, child, postcommit = graph
    store = store_mod.SingleWriterStateStore.open_verified(
        store_mod.MEMORY_PATH, store_id=ba.IDENTITY_CONFIG["store_id"],
        namespace=ba.IDENTITY_CONFIG["namespace"],
        namespace_version=ba.IDENTITY_CONFIG["namespace_version"])
    request = {"transaction_commit_id": ba.TRANSACTION_ID, "prestate": precommit,
               "proposal_event": proposal, "applied_child_event": child}
    store.commit_transition(request, anti_replay=ba.ANTI_REPLAY_ANCHORS)
    manifest = ba._load_trust_root_manifest()
    receipt = ba._v2_receipt(precommit, proposal, child, postcommit)
    baseline = state_authority.verify_state_authority_receipt_v2(
        receipt, trust_root_manifest=manifest, custody_evidence=ba.CUSTODY_EVIDENCE,
        require_production=True)
    injected = copy.deepcopy(receipt)
    carrier = injected["signature_b64"]
    injected["signature_b64"] = carrier[:8] + "\n" + carrier[8:]
    whitespace = state_authority.verify_state_authority_receipt_v2(
        injected, trust_root_manifest=manifest, custody_evidence=ba.CUSTODY_EVIDENCE,
        require_production=True)
    store.close()
    return baseline, whitespace


def main() -> int:
    print("== PROBE A: BUILD B, fully self-authored measurement universe "
          "(SEAT2 + SEAT3 F2) ==")
    print("evaluate_production_measurement -> %r" % (probe_a(),))
    print()
    print("== PROBE B: BUILD A, fully self-authored state universe (SEAT3 F1) ==")
    verify_errors, admit_errors = probe_b()
    print("verify_state_authority_receipt_v2 -> %r" % (verify_errors,))
    print("verify_production_scorer_input    -> %r" % (admit_errors,))
    print()
    print("== PROBE C: BUILD A, the ceremony spec's own production-shaped manifest "
          "(ChatGPT corollary) ==")
    print("verify_state_authority_receipt_v2 -> %r" % (probe_c(),))
    print()
    print("== PROBE D: signature carrier malleability (SEAT3 F6) ==")
    baseline, whitespace = probe_d()
    print("canonical carrier                 -> %r" % (baseline,))
    print("whitespace-injected carrier       -> %r" % (whitespace,))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
