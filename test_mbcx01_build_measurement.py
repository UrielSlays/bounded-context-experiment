"""BUILD B red witnesses — production Windows Job/ETW measurement authority.

Every witness here is written BEFORE the authority path exists and must fail on
the current skeletons for its intended reason:

- `mbcx01_build_windows_producer.produce_signed_measurement_receipt_v2` raises
  `NotImplementedError("BUILD_B_PRODUCER_NOT_IMPLEMENTED")`, so every witness
  that needs a simulated production grid ERRORs;
- `mbcx01_build_measurement_authority.evaluate_production_measurement` returns
  `["PHYSICAL_HARNESS_UNAVAILABLE"]` for every input, so every witness that
  demands a named rejection or an admitted grid FAILS;
- `mbcx01_build_measurement_authority.validate_production_trust_root_manifest`
  and `mbcx01_build_exactness_authority.verify_production_carrier_exactness`
  always raise, so their positive witnesses ERROR and their adversarial
  witnesses FAIL on the error name.

Witness map to the r13.2 handoff "Windows/measurement authority" list:
bw04 ABI · bw05 job accounting · bw06 membership/PID reuse · bw07 breakaway,
network, broker, preexisting helper, external worker · bw08 final-query
ordering and active-process race · bw09 completion-message loss stays
diagnostic · bw10 raw/scalar mismatch · bw11 ETW · bw12 replay · bw13
self-authored root, fixture relabel and frozen-evaluator compatibility ·
bw01/bw02/bw03 trust root, validity/revocation and custody separation · bw14
malformed evidence returns a closed error list · bw15 QPC/elapsed cross-check
(V2-only tightening) · bw16 production carrier-exactness authority · bw17-bw21
the BUILD acceptance r1 fix class AUTHENTICATED_PRODUCTION_TRUST_BOOTSTRAP
(self-authored universe, anchored ceremony path, fail-closed anchor, strict
signature carrier, exactness door) · bw22/bw24-bw27 the BUILD acceptance r2 fix
class FIXTURE_ISOLATION / INSTANCE_SCOPED_VERIFIER_CONTEXT (committed fixture
anchor refused at every production door, verifier-controlled clock, binding-only
exactness labelling, strict anchor document parse, and the immutable
instance-scoped context itself). bw23, the wiring-FREEZE witness, was DELETED on
2026-08-14 with the machinery it tested — see the note where it stood.

No test in this file runs the experiment, makes a provider call, executes a
Windows Job, opens an ETW session or runs the 100-cell grid: every collection
is simulated in memory and every key is a committed test key.
"""

from __future__ import annotations

import base64
import copy
import ctypes
import dataclasses
import datetime
import glob
import inspect
import json
import os
import re
import shutil
import struct
import sys
import tempfile
import threading
import unittest

import mbcx01_build_ceremony_fixture as ceremony
import mbcx01_build_exactness_authority as exactness
import mbcx01_build_measurement_authority as authority
import mbcx01_build_trust_anchor as trust_anchor
import mbcx01_build_win32 as win32
import mbcx01_build_windows_producer as producer
import mbcx01_r13_measurement as measurement
from test_mbcx01_r13_measurement import sign_no_paid_test_envelopes

RUN_ID = "RUN.BUILD.B.SIMULATED.TEST"
R13_RUN_ID = "RUN.R13.NO-PAID.TEST"
CANDIDATE_ID = "CANDIDATE.BUILD.B.SIMULATED"
GENERATOR_DIGEST = measurement.sha384("MBCX01.BUILD.B.SIMULATED.GENERATOR")

SIMULATED_KEY_ID = "MBCX01.BUILD.FIXTURE.ED25519.TEST.1"
SIMULATED_EDITOR_KEY_ID = "MBCX01.BUILD.FIXTURE.TRUST-ROOT-EDITOR.ED25519.TEST.1"
SIGNER_ROLE = "MEASUREMENT_KEY_CUSTODIAN"
EDITOR_ROLE = "TRUST_ROOT_APPROVAL_AUTHORITY"
FIXTURE_MANIFEST_PATH = "MBCX-01-BUILD-MEASUREMENT-TRUST-ROOTS-V3.fixture.json"
FIXTURE_SCHEMA_PATH = "MBCX-01-BUILD-MEASUREMENT-TRUST-ROOTS-V3.schema.json"

# The COMMITTED test Ed25519 key pair. It is committed on purpose: its public half is
# the only root in the committed fixture manifest, which is `production_ready:false`,
# and it signs the FIXTURE lane. It is NOT the production lane's key any more — a
# council seat made exactly this pair the PRODUCTION measurement signing root and
# cleared admission, so committed key material is now refused by name at every
# production door (`test_bw57`), and this pair stays here as that witness's material.
COMMITTED_TEST_SIGNING_PRIVATE_KEY_PEM = """-----BEGIN PRIVATE KEY-----
MC4CAQAwBQYDK2VwBCIEILRRWTLhkdS7vEp7U2Bq6T/QV7MFJqaWVVzADPvjfIEf
-----END PRIVATE KEY-----
"""
COMMITTED_TEST_SIGNING_PUBLIC_KEY_PEM = (
    "-----BEGIN PUBLIC KEY-----\n"
    "MCowBQYDK2VwAyEA80rr2l2aDSC4TaeI0a5Yj9LhncDLIA+mUlXcqt2mK+Q=\n"
    "-----END PUBLIC KEY-----\n")

# The PRODUCTION-lane signing pair, generated IN MEMORY at first use and never written
# to this repository — the same move the r2 fold made for the owner ANCHOR, for the
# same reason: after the signing-key fold a committed key cannot be a production root,
# so the POSITIVE lane needs material that is in no committed document. Its public half
# changes every run, which is itself a guarantee that no witness quietly depends on
# committed signing material.
SIMULATED_PRIVATE_KEY_PEM, SIMULATED_PUBLIC_KEY_PEM = (
    ceremony.test_production_signing_keypair("MBCX01.BUILD.MEASUREMENT.SIGNER"))

# A FRESH attacker Ed25519 key pair, generated for the r1 trust-bootstrap witnesses
# (bw17-bw19). It is in no manifest this repository ships and in no ceremony: the
# witnesses use it to author an ENTIRE trust universe — manifest, custody documents,
# activation statement and 100 signed envelopes — the way the r1 council's SEAT2 and
# SEAT3 attacks did. The `.TEST.` marker is required only by `FixtureSigner`'s test-key
# guard and is read by no admission check.
ATTACKER_KEY_ID = "ATTACKER.SELF.AUTHORED.MEASUREMENT.TEST.1"
ATTACKER_EDITOR_KEY_ID = "ATTACKER.SELF.AUTHORED.EDITOR.TEST.1"
ATTACKER_PRIVATE_KEY_PEM = (
    "-----BEGIN PRIVATE KEY-----\n"
    "MC4CAQAwBQYDK2VwBCIEIEQ88tt0UVLFKV++UEwMgBsw0p8vw/zkqIBKAcuh3HRq\n"
    "-----END PRIVATE KEY-----\n")
ATTACKER_PUBLIC_KEY_PEM = (
    "-----BEGIN PUBLIC KEY-----\n"
    "MCowBQYDK2VwAyEAvQ1p7m2R4nT8y5vRCV9PtvoLcrx1koVrfTxqpOpoKNQ=\n"
    "-----END PUBLIC KEY-----\n")


def setUpModule():  # noqa: N802 - unittest name
    """OPERATOR WIRING for the suite: install the TEST PRODUCTION verifier context.

    This is the seam the r1 fix class turns on and the r2 FIXTURE-ISOLATION fold
    tightens: the verifier context is constructed at process construction, structurally
    apart from every per-request call. No witness below may pass an anchor or a context
    to `evaluate_production_measurement` — there is no parameter for either.

    The anchor is NOT the committed fixture anchor any more, and that is the point of
    the r2 fold: a `fixture_only` anchor can no longer grant production authority
    (codex r2 F1), so the positive lane needs a production-SHAPED anchor. It is
    generated in memory at run time by `mbcx01_build_ceremony_fixture` and never
    written to this repository — the committed anchor document stays fixture-only and
    key-free. `test_bw22` is the witness that the committed fixture anchor is refused.
    """
    ceremony.configure_test_production_anchor()


def tearDownModule():  # noqa: N802 - unittest name
    trust_anchor.clear_owner_trust_anchor()

# Realistic QPC facts for the V2 elapsed cross-check: 10 MHz performance
# counter, 20,000 ticks of member lifetime, 2,000,000 ns elapsed.
QPC_FREQUENCY_HZ = 10_000_000
PROCESS_STARTED_QPC = 1_000_000
PROCESS_ENDED_QPC = 1_020_000
THREAD_STARTED_QPC = 1_000_010
THREAD_ENDED_QPC = 1_019_990
CSWITCH_QPC = (1_005_000, 1_015_000)
ELAPSED_QPC_TICKS = PROCESS_ENDED_QPC - PROCESS_STARTED_QPC
ELAPSED_MONOTONIC_NS = ELAPSED_QPC_TICKS * 1_000_000_000 // QPC_FREQUENCY_HZ

HARNESS_IDENTITY = {
    "harness_artifact_digest": measurement.sha384("MBCX01.BUILD.B.HARNESS.ARTIFACT"),
    "harness_build_digest": measurement.sha384("MBCX01.BUILD.FIXTURE.HARNESS.BUILD"),
    "host_environment_digest": measurement.sha384("MBCX01.BUILD.B.HOST.ENVIRONMENT"),
    "harness_configuration_digest": measurement.sha384(
        "MBCX01.BUILD.B.HARNESS.CONFIGURATION"),
}

# The four external custody documents a production ceremony must produce. The
# in-memory simulated manifest binds their SHA-384 digests; a manifest whose
# digests do not recompute from these exact documents is refused.
CUSTODY_DOCUMENTS = {
    "SEPARATE_KEY_CUSTODY_ATTESTATION": {
        "schema_id": "KeyCustodyAttestationV1",
        "custodian_role": SIGNER_ROLE,
        "key_id": SIMULATED_KEY_ID,
        "private_key_never_leaves_custody": True,
        "attested_by": "SIMULATED.CUSTODY.OFFICER.TEST"},
    "SEPARATE_TRUST_ROOT_EDITOR_APPROVAL": {
        "schema_id": "TrustRootEditorApprovalV1",
        "editor_role": EDITOR_ROLE,
        "approver_key_id": SIMULATED_EDITOR_KEY_ID,
        "approved_manifest_id": "MBCX01.BUILD.MEASUREMENT.TRUST.ROOTS.V3.SIMULATED",
        "signer_key_ids_excluded": [SIMULATED_KEY_ID]},
    "HARNESS_BUILD_PROVENANCE": {
        "schema_id": "HarnessBuildProvenanceV1",
        "harness_build_digest": HARNESS_IDENTITY["harness_build_digest"],
        "build_reviewed": True,
        "builder_role": "HARNESS_BUILD_AUTHORITY"},
    "PRODUCTION_SIGNING_CEREMONY_RECEIPT": {
        "schema_id": "SigningCeremonyReceiptV1",
        "ceremony_id": "CEREMONY.BUILD.B.SIMULATED.TEST",
        "signer_key_id": SIMULATED_KEY_ID,
        "witness_roles": [EDITOR_ROLE, "HARNESS_BUILD_AUTHORITY"],
        "candidate_and_evaluator_received_private_key": False},
}


def _pem_body(public_key_pem: str) -> str:
    """The base64 body of a PEM public key, read from the TEXT and nothing else.

    Deliberately independent of `mbcx01_build_trust_anchor.public_key_identity`: the
    key-identity witnesses build their variants from the DECODED bytes, and a variant
    built from the normalizer under test can only ever confirm that normalizer's own
    fixed points (the recorded defect in bw28's original re-wrap sub-case).
    """
    return "".join(public_key_pem.split("-----")[2].split())


def _spki_der(public_key_pem: str) -> bytes:
    """The SubjectPublicKeyInfo DER a PEM public key carries."""
    return base64.b64decode(_pem_body(public_key_pem).encode("ascii"), validate=True)


def _pem_from_der_body(body: str) -> str:
    return ("-----BEGIN PUBLIC KEY-----\n" + body + "\n-----END PUBLIC KEY-----\n")


def _pem_from_der(der: bytes) -> str:
    return _pem_from_der_body(base64.b64encode(der).decode("ascii"))


def _non_canonical_base64_body(der: bytes) -> str:
    """A DIFFERENT base64 string for the SAME bytes (RFC 4648 §3.5 trailing bits).

    The final base64 character of a 2-byte final group carries 4 significant bits and 2
    that are not; where they are not required to be zero, several strings decode to one
    byte sequence. This searches the alphabet for such a string and asserts nothing —
    the witness asserts the decode equality itself.
    """
    body = base64.b64encode(der).decode("ascii")
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    for char in alphabet:
        candidate = body[:-2] + char + body[-1]
        if candidate != body and base64.b64decode(
                candidate.encode("ascii"), validate=True) == der:
            return candidate
    raise AssertionError("no non-canonical base64 carrier exists for these bytes")


def _long_form_bit_string_spki(der: bytes) -> bytes:
    """The SAME Ed25519 key rebuilt from its DECODED 32-byte point, with the inner BIT
    STRING length in DER long form.

    Built out of the key bytes and the RFC 8410 §4 grammar — never out of any identity
    the module under test computes — so it can reach an encoding the normalizer has to
    NORMALIZE rather than one it happens to fix already.
    """
    point = der[-32:]
    bit_string = bytes((0x03, 0x81, 0x21, 0x00)) + point
    algorithm = bytes.fromhex("300506032b6570")
    return bytes((0x30, len(algorithm) + len(bit_string))) + algorithm + bit_string


def _long_form_spki(der: bytes) -> bytes:
    """The SAME SPKI value with the outer SEQUENCE length in DER long form.

    X.690 §8.1.3.3 permits the long form; §10.1 requires the short form for DER, so this
    is a non-canonical encoding of an identical key — the next variant in the key-identity
    class once the base64 text axis is closed. The 32-byte Ed25519 public point is
    untouched.
    """
    return der[:1] + bytes([0x81, der[1]]) + der[2:]


def committed_fixture_manifest() -> dict:
    """The committed, production_ready:false V3 manifest instance."""
    with open(FIXTURE_MANIFEST_PATH, encoding="utf-8") as stream:
        return json.load(stream)


def simulated_production_manifest(*, policy_overrides=None, root_overrides=None,
                                  manifest_overrides=None) -> dict:
    """TEST-ONLY in-memory `MeasurementTrustRootManifestV3`.

    Built in memory and never written to disk. Its roots are the committed test
    key, so nothing it authorizes is physical evidence; it exists only so the
    production admission path has a positive witness to be red against.
    """
    policy = {
        "schema_id": "ProductionMeasurementTrustPolicyV2",
        "status": "ACTIVATED",
        "fail_loud_sentinel": "PHYSICAL_HARNESS_UNAVAILABLE",
        "signer_custodian_role": SIGNER_ROLE,
        "trust_root_editor_role": EDITOR_ROLE,
        "roles_must_be_distinct": True,
        "manifest_edit_cannot_activate_production": True,
        "required_external_evidence": list(authority.REQUIRED_CUSTODY_EVIDENCE),
        "key_custodian_attestation_digest": measurement.sha384(
            CUSTODY_DOCUMENTS["SEPARATE_KEY_CUSTODY_ATTESTATION"]),
        "trust_root_editor_approval_digest": measurement.sha384(
            CUSTODY_DOCUMENTS["SEPARATE_TRUST_ROOT_EDITOR_APPROVAL"]),
        "harness_build_provenance_digest": measurement.sha384(
            CUSTODY_DOCUMENTS["HARNESS_BUILD_PROVENANCE"]),
        "signing_ceremony_receipt_digest": measurement.sha384(
            CUSTODY_DOCUMENTS["PRODUCTION_SIGNING_CEREMONY_RECEIPT"]),
        "editor_approval_key_ids": [SIMULATED_EDITOR_KEY_ID],
    }
    policy.update(policy_overrides or {})
    root = {
        "key_id": SIMULATED_KEY_ID,
        "algorithm": "ED25519",
        "fixture_only": False,
        "authorized_producer_role": producer.PRODUCTION_PRODUCER_ROLE,
        "authorized_fixture_kind": producer.PRODUCTION_FIXTURE_KIND,
        "signer_custodian_role": SIGNER_ROLE,
        "authorized_harness_build_digest": HARNESS_IDENTITY["harness_build_digest"],
        "trust_policy_digest": measurement.sha384(policy),
        "public_key_pem": SIMULATED_PUBLIC_KEY_PEM,
        "validity": {"not_before": "2026-08-14T00:00:00Z",
                     "not_after": "2027-08-14T00:00:00Z"},
        "revocation_state": "ACTIVE",
    }
    root.update(root_overrides or {})
    revoked: list[str] = []
    document = {
        "schema_id": "MeasurementTrustRootManifestV3",
        "manifest_id": "MBCX01.BUILD.MEASUREMENT.TRUST.ROOTS.V3.SIMULATED",
        "production_ready": True,
        "activation_authority": "SIMULATED_TEST_INJECTION_ONLY",
        "trust_policy": policy,
        "validity": {"not_before": "2026-08-14T00:00:00Z",
                     "not_after": "2027-08-14T00:00:00Z"},
        "revocation": {
            "schema_id": "MeasurementTrustRootRevocationListV1",
            "revocation_list_id": "MBCX01.BUILD.MEASUREMENT.REVOCATION.V3.SIMULATED",
            "published_at": "2026-08-14T00:00:00Z",
            "revoked_key_ids": revoked,
            "revocation_list_digest": measurement.sha384(revoked)},
        "roots": [root],
    }
    document.update(manifest_overrides or {})
    return document


def simulated_custody_evidence(manifest=None, *, activation_overrides=None,
                               private_key_pem=None, anchor_id=None) -> dict:
    """The four external custody documents PLUS the owner-signed activation statement.

    The four documents are unchanged. The fifth item is the r1 fix class: an
    `OwnerCeremonyActivationV1` statement signed by the operator-wired TEST PRODUCTION
    owner anchor over the EXACT manifest it is presented with, so a witness that forges a manifest
    gets an activation for THAT manifest and still has to survive every other check —
    the anchor witnesses (bw17-bw19) are the ones that attack the activation itself.
    """
    documents = copy.deepcopy(CUSTODY_DOCUMENTS)
    manifest = manifest if manifest is not None else simulated_production_manifest()
    try:
        roots = authority.validate_production_trust_root_manifest(manifest)
        binding = authority.production_activation_binding(manifest, roots, documents)
    except authority.MeasurementAuthorityError:
        binding = None
    documents[authority.OWNER_ACTIVATION_EVIDENCE] = None if binding is None else (
        ceremony.activation_statement(
            manifest=manifest, overrides=activation_overrides,
            private_key_pem=private_key_pem, anchor_id=anchor_id, **binding))
    return documents


def simulated_signer() -> producer.FixtureSigner:
    return producer.FixtureSigner(SIMULATED_KEY_ID, SIMULATED_PRIVATE_KEY_PEM)


def simulated_identity(*, run_id: str = RUN_ID, **overrides) -> producer.ProductionRunIdentity:
    manifest = simulated_production_manifest()
    fields = {
        "run_id": run_id,
        "candidate_id": CANDIDATE_ID,
        "candidate_artifact_digest": measurement.sha384(
            "MBCX01.BUILD.B.CARRIER.ARTIFACT"),
        "generator_digest": GENERATOR_DIGEST,
        "harness_identity": copy.deepcopy(HARNESS_IDENTITY),
        "signing_key_id": SIMULATED_KEY_ID,
        "trust_policy_digest": manifest["roots"][0]["trust_policy_digest"],
    }
    fields.update(overrides)
    return producer.ProductionRunIdentity(**fields)


def _query_metadata(row: dict) -> dict:
    return {key: value for key, value in row.items()
            if key not in ("raw_bytes_b64", "raw_bytes_sha384")}


def simulated_collections() -> list[producer.SimulatedCollection]:
    """One simulated Windows collection per registered cell (100 cells).

    The raw 96/144-byte buffers come from the frozen ABI packer
    `mbcx01_r13_measurement._query_evidence`, which is the authoritative
    reference for the exact 64-bit layout. QPC lifetimes are rewritten to
    self-consistent 10 MHz values so the V2 elapsed cross-check has a true
    positive to verify.
    """
    rows = measurement.baseline_receipt_rows(
        candidate_id=CANDIDATE_ID, generator_digest=GENERATOR_DIGEST, run_id=RUN_ID)
    collections = []
    for ordinal, envelope in enumerate(rows):
        receipt = envelope["receipt"]
        job = receipt["job_receipt"]
        job["elapsed_monotonic_ns"] = ELAPSED_MONOTONIC_NS
        evidence = job["evidence"]
        membership = evidence["process_membership"]
        trace = evidence["trace"]
        queries = measurement._query_evidence(job)
        processes = copy.deepcopy(membership["processes"])
        for process in processes:
            process["started_qpc"] = PROCESS_STARTED_QPC
            process["ended_qpc"] = PROCESS_ENDED_QPC
        threads = copy.deepcopy(trace["thread_lifetimes"])
        for thread in threads:
            thread["started_qpc"] = THREAD_STARTED_QPC
            thread["ended_qpc"] = THREAD_ENDED_QPC
        observations = copy.deepcopy(trace["cswitch_observations"])
        for index, observation in enumerate(observations):
            observation["qpc"] = CSWITCH_QPC[index]
        collections.append(producer.SimulatedCollection(
            H=receipt["H"], D=receipt["D"], F=receipt["F"],
            job_object_id=job["job_object_id"],
            root_process_id=job["root_process_id"],
            root_process_start_key=membership["root_process_start_key"],
            created_suspended=True,
            completion_port_associated_before_resume=True,
            assigned_before_resume=True,
            breakaway_enabled=False,
            silent_breakaway_enabled=False,
            basic_and_io_raw_bytes=base64.b64decode(
                queries["basic_and_io"]["raw_bytes_b64"]),
            basic_and_io_query=_query_metadata(queries["basic_and_io"]),
            extended_limit_raw_bytes=base64.b64decode(
                queries["extended_limit"]["raw_bytes_b64"]),
            extended_limit_query=_query_metadata(queries["extended_limit"]),
            process_lifetimes=tuple(processes),
            thread_lifetimes=tuple(threads),
            cswitch_observations=tuple(observations),
            cswitch_first_member_baselines=tuple(
                copy.deepcopy(trace["cswitch_first_member_baselines"])),
            trace_capability_query=copy.deepcopy(trace["capability_query"]),
            trace_event_attachment=copy.deepcopy(trace["event_attachment"]),
            trace_facts={
                "instruction_backend": job["instruction_backend"],
                "instruction_profile_source": job["instruction_profile_source"],
                "instruction_event_list": job["instruction_event_list"],
                "instruction_attribution": job["instruction_attribution"],
                "etw_capability_query_succeeded": job["etw_capability_query_succeeded"],
                "etw_pmc_source_available": job["etw_pmc_source_available"],
                "etw_max_pmc_counters": job["etw_max_pmc_counters"],
                "etw_counter_owner_conflict_count":
                    job["etw_counter_owner_conflict_count"],
                "etw_pmc_strict_mode": job["etw_pmc_strict_mode"],
                "etw_pmc_multiplexing_detected": job["etw_pmc_multiplexing_detected"],
                "etw_events_lost": job["etw_events_lost"],
                "etw_log_buffers_lost": job["etw_log_buffers_lost"],
                "etw_realtime_buffers_lost": job["etw_realtime_buffers_lost"],
                "etw_attribution_complete": job["etw_attribution_complete"]},
            scalars={
                "user_time_ns": job["user_time_ns"],
                "kernel_time_ns": job["kernel_time_ns"],
                "total_page_faults": job["total_page_faults"],
                "total_processes": job["total_processes"],
                "active_processes_at_final_query":
                    job["active_processes_at_final_query"],
                "total_terminated_processes": job["total_terminated_processes"],
                "read_operations": job["read_operations"],
                "write_operations": job["write_operations"],
                "other_operations": job["other_operations"],
                "read_transfer_bytes": job["read_transfer_bytes"],
                "write_transfer_bytes": job["write_transfer_bytes"],
                "other_transfer_bytes": job["other_transfer_bytes"],
                "peak_committed_bytes": job["peak_committed_bytes"],
                "retired_instructions": job["retired_instructions"]},
            qpc_frequency_hz=QPC_FREQUENCY_HZ,
            elapsed_qpc_ticks=ELAPSED_QPC_TICKS,
            elapsed_monotonic_ns=ELAPSED_MONOTONIC_NS,
            environment=copy.deepcopy(evidence["environment"]),
            external_enforcement=copy.deepcopy(evidence["external_enforcement"]),
            completion=copy.deepcopy(evidence["completion"]),
            nonce=f"NONCE.BUILD.B.SIMULATED.{ordinal:03d}"))
    return collections


def simulated_production_grid(collections=None, *, signer=None,
                              identity=None) -> list[dict]:
    """Produce the 100-cell simulated production grid through the BUILD producer."""
    signer = signer or simulated_signer()
    identity = identity or simulated_identity()
    rows = collections if collections is not None else simulated_collections()
    return [producer.produce_signed_measurement_receipt_v2(
        collection, signer=signer, identity=identity) for collection in rows]


def admit(envelopes, *, manifest=None, custody=None, run_id: str = RUN_ID) -> list[str]:
    manifest = manifest if manifest is not None else simulated_production_manifest()
    return authority.evaluate_production_measurement(
        envelopes,
        trust_root_manifest=manifest,
        custody_evidence=custody if custody is not None
        else simulated_custody_evidence(manifest),
        expected_run_id=run_id)


def perturbed(collections, index, **changes):
    """Return the grid collections with one cell's collection replaced."""
    rows = list(collections)
    rows[index] = dataclasses.replace(rows[index], **changes)
    return rows


class BuildTrustRootAuthorityTests(unittest.TestCase):
    """bw01-bw03: V3 trust root, validity/revocation and custody separation."""

    def test_bw01_positive_committed_fixture_manifest_is_a_closed_fixture_only_v3(self):
        """The committed V3 instance validates as a closed document and stays fixture-only."""
        document = committed_fixture_manifest()
        self.assertEqual(document["schema_id"], "MeasurementTrustRootManifestV3")
        self.assertIs(document["production_ready"], False)
        self.assertIs(document["roots"][0]["fixture_only"], True)
        self.assertEqual(document["roots"][0]["authorized_producer_role"],
                         producer.PRODUCTION_PRODUCER_ROLE)
        self.assertEqual(document["roots"][0]["trust_policy_digest"],
                         measurement.sha384(document["trust_policy"]))
        self.assertNotIn("PRIVATE", document["roots"][0]["public_key_pem"])
        roots = authority.validate_production_trust_root_manifest(document)
        self.assertEqual(set(roots), {SIMULATED_KEY_ID})

    def test_bw01_adversarial_committed_manifest_flipped_to_production_is_refused(self):
        """Flipping production_ready in the committed file cannot mint authority."""
        forged = committed_fixture_manifest()
        forged["production_ready"] = True
        forged["roots"][0]["fixture_only"] = False
        errors = admit([], manifest=forged)
        self.assertIn("MEASUREMENT_CUSTODY_EVIDENCE_INVALID", errors)

    def test_bw02_positive_simulated_manifest_authorizes_one_producer_root(self):
        """An injected V3 manifest authorizes exactly the reviewed producer role/key."""
        roots = authority.validate_production_trust_root_manifest(
            simulated_production_manifest())
        self.assertEqual(set(roots), {SIMULATED_KEY_ID})
        self.assertEqual(roots[SIMULATED_KEY_ID]["authorized_fixture_kind"],
                         producer.PRODUCTION_FIXTURE_KIND)

    def test_bw02_adversarial_expired_validity_window_is_refused(self):
        """A root outside its signed validity window has no authority."""
        forged = simulated_production_manifest(root_overrides={
            "validity": {"not_before": "2020-01-01T00:00:00Z",
                         "not_after": "2020-12-31T00:00:00Z"}})
        with self.assertRaisesRegex(authority.MeasurementAuthorityError,
                                    "TRUST_ROOT_VALIDITY_EXPIRED"):
            authority.validate_production_trust_root_manifest(forged)

    def test_bw02_adversarial_revoked_root_is_refused(self):
        """A revoked key id has no authority even while the manifest still lists it."""
        forged = simulated_production_manifest(root_overrides={
            "revocation_state": "REVOKED"})
        with self.assertRaisesRegex(authority.MeasurementAuthorityError,
                                    "TRUST_ROOT_REVOKED"):
            authority.validate_production_trust_root_manifest(forged)

    def test_bw03_positive_custody_digests_recompute_from_injected_documents(self):
        """The four external custody digests are recomputed, never trusted as labels."""
        manifest = simulated_production_manifest()
        policy = manifest["trust_policy"]
        evidence = simulated_custody_evidence()
        self.assertEqual(policy["key_custodian_attestation_digest"],
                         measurement.sha384(evidence["SEPARATE_KEY_CUSTODY_ATTESTATION"]))
        self.assertEqual(policy["signing_ceremony_receipt_digest"],
                         measurement.sha384(
                             evidence["PRODUCTION_SIGNING_CEREMONY_RECEIPT"]))
        roots = authority.validate_production_trust_root_manifest(manifest)
        self.assertEqual(roots[SIMULATED_KEY_ID]["revocation_state"], "ACTIVE")

    def test_bw03_adversarial_signer_and_editor_role_collision_is_refused(self):
        """Signer custodian and trust-root editor may never be the same role."""
        forged = simulated_production_manifest(
            policy_overrides={"trust_root_editor_role": SIGNER_ROLE})
        with self.assertRaisesRegex(authority.MeasurementAuthorityError,
                                    "CUSTODY_SEPARATION_INVALID"):
            authority.validate_production_trust_root_manifest(forged)

    def test_bw03_adversarial_signer_key_in_editor_approval_chain_is_refused(self):
        """The signing key may never appear in the trust-root editor approval chain."""
        forged = simulated_production_manifest(
            policy_overrides={"editor_approval_key_ids": [SIMULATED_KEY_ID]})
        with self.assertRaisesRegex(authority.MeasurementAuthorityError,
                                    "CUSTODY_SEPARATION_INVALID"):
            authority.validate_production_trust_root_manifest(forged)


class BuildCalendarValidityTests(unittest.TestCase):
    """bw64: a validity ENDPOINT is a CALENDAR INSTANT, and windows order as instants.

    NUMBER ALLOCATION, stated because the field is a hard ceiling: `bw64` is a
    MODULE-QUALIFIED REUSE — it is a GAP in this module and is carried by
    `test_mbcx01_build_cohort.py`, which is the mechanism `verify-build-bundle.py`
    already sanctions for `bw70-bw84` (`WITNESS_ID` is `<module>.<class>.<method>`,
    :275-290). The two-digit `bw` field has no free number left in ANY module; that is
    a namespace fact for the driver, not a licence to renumber an existing witness.
    """

    maxDiff = None

    def setUp(self):
        ceremony.configure_test_production_anchor()
        self.addCleanup(ceremony.configure_test_production_anchor)

    def fixed_clock(self, instant="2026-08-16T00:00:00Z"):
        trust_anchor.configure_owner_trust_anchor(
            ceremony.test_production_anchor_document(), current_time=instant)
        return instant

    def test_bw64_adversarial_a_non_calendar_validity_window_cannot_extend_production_trust(self):
        """Invariant (codex r5 P1): trust-root validity is an interval between two
        CALENDAR instants, and every comparison happens on the parsed instants.

        RED against the pre-fix bytes: `TIMESTAMP_RE` proved digit PLACEMENT only, and
        the comparisons were STRING comparisons, so the window
        `2020-00-00T00:00:00Z .. 2030-99-99T99:99:99Z` — a month `00`, a day `00`, an
        hour/minute/second `99` — validated and `evaluate_production_measurement`
        returned `[]` at a 2026 verifier instant. A malformed date EXTENDED production
        trust; that is a WRONG ADMISSION, and the widest possible one, because no
        calendar bound can close a window that is not on the calendar.

        RED against the PRE-FIX bytes (`git show HEAD:mbcx01_build_measurement_authority.py`,
        sha256 6eeda49e85154d02f8aa168a656ea58f31349e2dfda8f87be99f83577b5c99eb, loaded
        under the real module name and hash-asserted before the run):

            FAIL: AssertionError: 'MEASUREMENT_TRUST_ROOT_INVALID' not found in []
        """
        window = {"not_before": "2020-00-00T00:00:00Z",
                  "not_after": "2030-99-99T99:99:99Z"}
        instant = self.fixed_clock()
        # The premise, at the byte: the OLD gate accepts both endpoints, and the OLD
        # (string) ordering places the verifier's instant inside them.
        for value in window.values():
            self.assertIsNotNone(authority.TIMESTAMP_RE.fullmatch(value))
        self.assertTrue(window["not_before"] < instant < window["not_after"])

        manifest = simulated_production_manifest(
            manifest_overrides={"validity": dict(window)})
        custody = simulated_custody_evidence(manifest)
        grid = simulated_production_grid()
        errors = admit(grid, manifest=manifest, custody=custody)
        self.assertIn("MEASUREMENT_TRUST_ROOT_INVALID", errors)
        self.assertIn(authority.FAIL_LOUD_SENTINEL, errors)
        self.assertNotEqual(errors, [])
        with self.assertRaisesRegex(authority.MeasurementAuthorityError,
                                    "MEASUREMENT_TRUST_ROOT_INVALID"):
            authority.validate_production_trust_root_manifest(
                manifest, evaluation_instant=instant)

        # CONTROL — the SAME grid, the SAME custody ceremony and the SAME verifier
        # instant, under a window whose endpoints ARE calendar instants: admitted. The
        # refusal above is the calendar, not the width of the window.
        calendar = simulated_production_manifest(
            manifest_overrides={"validity": {"not_before": "2020-01-01T00:00:00Z",
                                             "not_after": "2030-01-01T00:00:00Z"}})
        self.assertEqual(admit(grid, manifest=calendar,
                               custody=simulated_custody_evidence(calendar)), [])

    def test_bw64_adversarial_every_non_calendar_endpoint_shape_is_refused(self):
        """Invariant: the refusal is the CALENDAR, not one hand-picked string. Each
        endpoint below satisfies `TIMESTAMP_RE` and denotes no instant — a zero month,
        a 32nd day, a 30th of February, an hour 24 and a leap day of a non-leap year —
        and each is refused wherever a validity endpoint is read (manifest window, root
        window) and wherever an instant is read (the revocation list's `published_at`,
        which is the STRUCTURAL default evaluation instant)."""
        instant = self.fixed_clock()
        for value in ("2026-00-14T00:00:00Z", "2026-08-32T00:00:00Z",
                      "2026-02-30T00:00:00Z", "2026-08-14T24:00:00Z",
                      "2025-02-29T00:00:00Z"):
            with self.subTest(value=value):
                self.assertIsNotNone(authority.TIMESTAMP_RE.fullmatch(value))
                self.assertIsNone(authority.parse_instant(value))
                template = simulated_production_manifest()
                for overrides in (
                        {"validity": {"not_before": value,
                                      "not_after": "2027-08-14T00:00:00Z"}},
                        {"revocation": dict(template["revocation"], published_at=value)}):
                    forged = simulated_production_manifest(manifest_overrides=overrides)
                    with self.assertRaisesRegex(authority.MeasurementAuthorityError,
                                                "MEASUREMENT_TRUST_ROOT_INVALID"):
                        authority.validate_production_trust_root_manifest(
                            forged, evaluation_instant=instant)
                root_forged = simulated_production_manifest(
                    root_overrides={"validity": {"not_before": value,
                                                 "not_after": "2027-08-14T00:00:00Z"}})
                with self.assertRaisesRegex(authority.MeasurementAuthorityError,
                                            "MEASUREMENT_TRUST_ROOT_INVALID"):
                    authority.validate_production_trust_root_manifest(
                        root_forged, evaluation_instant=instant)

    def test_bw64_positive_parsed_instants_order_by_time_not_by_text(self):
        """Invariant: `parse_instant` returns the UTC instant a spelling denotes, and
        only the one accepted spelling parses — an offset form, a space separator, a
        fractional-second form and a lower-case `z` all denote nothing HERE, because
        this plane has exactly one document spelling (`TIMESTAMP_RE`)."""
        parsed = authority.parse_instant("2026-08-16T00:00:00Z")
        self.assertEqual(parsed.year, 2026)
        self.assertEqual(parsed.tzinfo, datetime.timezone.utc)
        self.assertLess(authority.parse_instant("2026-08-16T00:00:00Z"),
                        authority.parse_instant("2026-08-16T00:00:01Z"))
        for value in ("2026-08-16T00:00:00+00:00", "2026-08-16 00:00:00Z",
                      "2026-08-16T00:00:00.000000Z", "2026-08-16t00:00:00z",
                      "2026-8-16T00:00:00Z", None, 20260816, {}):
            with self.subTest(value=value):
                self.assertIsNone(authority.parse_instant(value))


class BuildProducerAbiTests(unittest.TestCase):
    """bw04: exact 96/144-byte Job query ABI, referenced to the frozen packer."""

    def setUp(self):
        self.collections = simulated_collections()

    def test_bw04_positive_collection_round_trips_the_exact_96_and_144_byte_layout(self):
        """The produced envelope carries the collector's raw bytes unaltered."""
        collection = self.collections[0]
        self.assertEqual(len(collection.basic_and_io_raw_bytes),
                         producer.BASIC_AND_IO_SIZE_BYTES)
        self.assertEqual(len(collection.extended_limit_raw_bytes),
                         producer.EXTENDED_LIMIT_SIZE_BYTES)
        values = struct.unpack("<qqqqIIIIQQQQQQ", collection.basic_and_io_raw_bytes)
        self.assertEqual(values[4:8], (0, 1, 0, 0))
        self.assertEqual(
            struct.unpack_from("<Q", collection.extended_limit_raw_bytes,
                               producer.PEAK_COMMITTED_OFFSET)[0],
            collection.scalars["peak_committed_bytes"])
        envelope = producer.produce_signed_measurement_receipt_v2(
            collection, signer=simulated_signer(), identity=simulated_identity())
        queries = envelope["receipt"]["job_receipt"]["evidence"]["job_queries"]
        self.assertEqual(base64.b64decode(queries["basic_and_io"]["raw_bytes_b64"]),
                         collection.basic_and_io_raw_bytes)
        self.assertEqual(base64.b64decode(queries["extended_limit"]["raw_bytes_b64"]),
                         collection.extended_limit_raw_bytes)

    def test_bw04_adversarial_short_basic_and_io_buffer_is_refused(self):
        """A 92-byte Basic+IO buffer (fourth DWORD dropped) is not admissible."""
        truncated = self.collections[0].basic_and_io_raw_bytes[:92]
        grid = simulated_production_grid(
            perturbed(self.collections, 0, basic_and_io_raw_bytes=truncated))
        self.assertIn("JOB_QUERY_EVIDENCE_INVALID", admit(grid))

    def test_bw04_adversarial_peak_memory_read_at_the_wrong_offset_is_refused(self):
        """Peak committed bytes moved off offset 136 is a rejected perturbation."""
        raw = bytearray(self.collections[0].extended_limit_raw_bytes)
        struct.pack_into("<Q", raw, producer.PEAK_COMMITTED_OFFSET, 0)
        struct.pack_into("<Q", raw, producer.PEAK_COMMITTED_OFFSET - 8,
                         self.collections[0].scalars["peak_committed_bytes"])
        grid = simulated_production_grid(
            perturbed(self.collections, 0, extended_limit_raw_bytes=bytes(raw)))
        self.assertIn("JOB_QUERY_EVIDENCE_INVALID", admit(grid))


class BuildJobAccountingTests(unittest.TestCase):
    """bw05-bw10: Job accounting, membership, enforcement, ordering, raw/scalar."""

    def setUp(self):
        self.collections = simulated_collections()

    def _scalars(self, index=0, **changes):
        scalars = dict(self.collections[index].scalars)
        scalars.update(changes)
        return scalars

    def test_bw05_positive_ordinary_child_exit_with_zero_terminations_is_admitted(self):
        """A clean cell exits normally: TotalTerminatedProcesses == 0 is accepted."""
        collection = self.collections[0]
        self.assertEqual(collection.scalars["total_terminated_processes"], 0)
        self.assertEqual(collection.scalars["active_processes_at_final_query"], 0)
        self.assertEqual(collection.process_lifetimes[0]["terminal_status"], "EXITED")
        self.assertEqual(admit(simulated_production_grid(self.collections)), [])

    def test_bw05_adversarial_nonzero_limit_violation_termination_is_refused(self):
        """A Job-limit-violation termination disqualifies the cell."""
        scalars = self._scalars(total_terminated_processes=1)
        job = dict(scalars, elapsed_monotonic_ns=ELAPSED_MONOTONIC_NS)
        raw = base64.b64decode(
            measurement._query_evidence(job)["basic_and_io"]["raw_bytes_b64"])
        grid = simulated_production_grid(perturbed(
            self.collections, 0, scalars=scalars, basic_and_io_raw_bytes=raw))
        self.assertIn("JOB_LIMIT_VIOLATION_TERMINATION", admit(grid))

    def test_bw06_adversarial_missing_descendant_is_refused(self):
        """TotalProcesses may never exceed the signed membership roster."""
        scalars = self._scalars(total_processes=2)
        job = dict(scalars, elapsed_monotonic_ns=ELAPSED_MONOTONIC_NS)
        raw = base64.b64decode(
            measurement._query_evidence(job)["basic_and_io"]["raw_bytes_b64"])
        grid = simulated_production_grid(perturbed(
            self.collections, 0, scalars=scalars, basic_and_io_raw_bytes=raw))
        self.assertIn("PROCESS_MEMBERSHIP_INVALID", admit(grid))

    def test_bw06_adversarial_pid_reuse_with_a_different_start_key_is_refused(self):
        """Same PID with a different 64-bit start key is a substituted member."""
        processes = copy.deepcopy(list(self.collections[0].process_lifetimes))
        processes[0]["process_start_key"] = "FFFFFFFFFFFFFFFF"
        grid = simulated_production_grid(perturbed(
            self.collections, 0, process_lifetimes=tuple(processes)))
        self.assertIn("PROCESS_MEMBERSHIP_INVALID", admit(grid))

    def test_bw07_adversarial_breakaway_evidence_is_refused(self):
        """Either breakaway mode enabled breaks descendant accounting."""
        for field_name in ("breakaway_enabled", "silent_breakaway_enabled"):
            with self.subTest(field=field_name):
                grid = simulated_production_grid(
                    perturbed(self.collections, 0, **{field_name: True}))
                self.assertIn("DESCENDANT_ACCOUNTING_MISSING", admit(grid))

    def test_bw07_adversarial_network_broker_and_helper_flags_are_refused(self):
        """Supervisor-owned enforcement must deny network, brokers and helpers."""
        cases = (("deny_outbound_network", False),
                 ("deny_external_compute_brokers", False),
                 ("deny_preexisting_helper_delegation", False),
                 ("external_compute_endpoint_count", 1),
                 ("applied_before_resume", False))
        for name, value in cases:
            with self.subTest(flag=name):
                enforcement = copy.deepcopy(
                    self.collections[0].external_enforcement)
                enforcement[name] = value
                grid = simulated_production_grid(perturbed(
                    self.collections, 0, external_enforcement=enforcement))
                self.assertIn("EXTERNAL_WORK_UNMEASURED", admit(grid))

    def test_bw07_adversarial_candidate_owned_enforcement_is_not_evidence(self):
        """An external worker allowed by candidate-owned policy is not enforcement."""
        enforcement = copy.deepcopy(self.collections[0].external_enforcement)
        enforcement["enforcement_owner_role"] = "CANDIDATE"
        grid = simulated_production_grid(
            perturbed(self.collections, 0, external_enforcement=enforcement))
        self.assertIn("EXTERNAL_WORK_UNMEASURED", admit(grid))

    def test_bw08_adversarial_final_query_before_the_terminal_barrier_is_refused(self):
        """Final queries collected before the terminal barrier are out of order."""
        metadata = dict(self.collections[0].basic_and_io_query)
        metadata["collected_after_terminal_barrier"] = False
        grid = simulated_production_grid(
            perturbed(self.collections, 0, basic_and_io_query=metadata))
        self.assertIn("FINAL_QUERY_ORDERING_INVALID", admit(grid))

    def test_bw08_adversarial_active_process_race_is_refused(self):
        """A nonzero final active-process count means the run was still alive."""
        completion = copy.deepcopy(self.collections[0].completion)
        completion["final_active_processes"] = 1
        grid = simulated_production_grid(
            perturbed(self.collections, 0, completion=completion))
        self.assertIn("ACTIVE_PROCESS_RACE", admit(grid))

    def test_bw09_positive_completion_message_loss_stays_diagnostic(self):
        """Lost completion messages do not fail a cell whose load-bearing evidence holds."""
        completion = copy.deepcopy(self.collections[0].completion)
        completion["completion_port_drained"] = False
        completion["active_zero_message_seen"] = False
        completion["new_process_messages"] = 0
        completion["exit_process_messages"] = 0
        completion["diagnostic_messages_complete"] = False
        grid = simulated_production_grid(
            perturbed(self.collections, 0, completion=completion))
        self.assertEqual(admit(grid), [])

    def test_bw10_adversarial_raw_bytes_and_scalar_disagreement_is_refused(self):
        """A scalar that disagrees with the raw returned buffer is fatal."""
        scalars = self._scalars(read_transfer_bytes=999_999)
        grid = simulated_production_grid(
            perturbed(self.collections, 0, scalars=scalars))
        self.assertIn("JOB_QUERY_EVIDENCE_INVALID", admit(grid))


class BuildInstructionAccountingTests(unittest.TestCase):
    """bw11: strict ETW PMC capability, attachment, loss and attribution."""

    def setUp(self):
        self.collections = simulated_collections()

    def _facts(self, **changes):
        facts = dict(self.collections[0].trace_facts)
        facts.update(changes)
        return facts

    def test_bw11_adversarial_unavailable_pmc_source_is_refused(self):
        """An unavailable PMC source is unavailable, never a guessed metric."""
        for name, value in (("etw_pmc_source_available", False),
                            ("etw_capability_query_succeeded", False)):
            with self.subTest(fact=name):
                grid = simulated_production_grid(perturbed(
                    self.collections, 0, trace_facts=self._facts(**{name: value})))
                self.assertIn("INSTRUCTION_ACCOUNTING_INCOMPLETE", admit(grid))

    def test_bw11_adversarial_sampled_backend_is_unsupported(self):
        """Only strict ETW_PMC_EVENT_ATTACHED_V1 counts as retired-instruction evidence."""
        grid = simulated_production_grid(perturbed(
            self.collections, 0,
            trace_facts=self._facts(
                instruction_backend="ETW_PMC_SAMPLED_PROFILE_V1")))
        self.assertIn("INSTRUCTION_ACCOUNTING_UNSUPPORTED", admit(grid))

    def test_bw11_adversarial_wrong_event_attachment_is_refused(self):
        """InstructionRetired must be attached to CSwitch through the documented classes."""
        attachment = dict(self.collections[0].trace_event_attachment)
        attachment["event_list"] = "PROFILE"
        grid = simulated_production_grid(
            perturbed(self.collections, 0, trace_event_attachment=attachment))
        self.assertIn("INSTRUCTION_ACCOUNTING_INCOMPLETE", admit(grid))

    def test_bw11_adversarial_multiplexing_conflict_and_loss_are_refused(self):
        """Multiplexing, counter-owner conflict and any loss counter are fatal."""
        for name, value in (("etw_pmc_multiplexing_detected", True),
                            ("etw_counter_owner_conflict_count", 1),
                            ("etw_events_lost", 1),
                            ("etw_log_buffers_lost", 1),
                            ("etw_realtime_buffers_lost", 1),
                            ("etw_pmc_strict_mode", False)):
            with self.subTest(fact=name):
                grid = simulated_production_grid(perturbed(
                    self.collections, 0, trace_facts=self._facts(**{name: value})))
                self.assertIn("INSTRUCTION_ACCOUNTING_INCOMPLETE", admit(grid))

    def test_bw11_adversarial_incomplete_thread_attribution_is_refused(self):
        """Every counter delta must join a signed PID/start-key/TID lifetime."""
        observations = copy.deepcopy(list(self.collections[0].cswitch_observations))
        observations[1]["old_thread_id"] += 1
        grid = simulated_production_grid(perturbed(
            self.collections, 0, cswitch_observations=tuple(observations),
            trace_facts=self._facts(etw_attribution_complete=False)))
        self.assertIn("INSTRUCTION_ACCOUNTING_INCOMPLETE", admit(grid))


class BuildReplayAndRelabelTests(unittest.TestCase):
    """bw12-bw13: replay with repaired hashes, self-authored root, fixture relabel."""

    def setUp(self):
        self.collections = simulated_collections()

    def _resigned(self, grid):
        signer = simulated_signer()
        signatures = signer.sign_preimages(
            [envelope["receipt_preimage_b64"] for envelope in grid])
        for envelope, signature in zip(grid, signatures):
            envelope["signature_b64"] = signature
        return grid

    def test_bw12_adversarial_replay_across_run_and_cell_is_refused(self):
        """A grid replayed under another run id fails even fully re-signed."""
        grid = simulated_production_grid(self.collections)
        for envelope in grid:
            envelope["run_id"] = "RUN.BUILD.B.OTHER.TEST"
        self._resigned(grid)
        self.assertIn("MEASUREMENT_REPLAY_IDENTITY_MISMATCH", admit(grid))

    def test_bw12_adversarial_carrier_artifact_substitution_is_refused(self):
        """A substituted candidate/carrier artifact digest breaks grid identity."""
        grid = simulated_production_grid(self.collections)
        grid[0]["receipt"]["candidate_artifact_digest"] = measurement.sha384("OTHER")
        self._resigned(grid)
        self.assertIn("GRID_IDENTITY_MISMATCH", admit(grid))

    def test_bw12_adversarial_harness_build_and_host_substitution_is_refused(self):
        """Harness build and host/environment are part of the one exact grid identity."""
        for field_name in ("harness_build_digest", "host_environment_digest"):
            with self.subTest(field=field_name):
                grid = simulated_production_grid(self.collections)
                grid[0]["receipt"]["job_receipt"]["evidence"][
                    "harness_identity"][field_name] = measurement.sha384("OTHER")
                self._resigned(grid)
                self.assertIn("GRID_IDENTITY_MISMATCH", admit(grid))

    def test_bw12_adversarial_unauthorized_key_or_role_is_refused(self):
        """A key or producer role outside the injected manifest has no authority."""
        grid = simulated_production_grid(self.collections)
        for envelope in grid:
            envelope["producer_role"] = "SELF_DECLARED_PRODUCER"
        self._resigned(grid)
        self.assertIn("PRODUCER_ROLE_UNAUTHORIZED", admit(grid))

    def test_bw13_adversarial_self_authored_root_is_refused(self):
        """A manifest whose only root is a key the signer minted for itself is refused."""
        forged = simulated_production_manifest(
            policy_overrides={"editor_approval_key_ids": [SIMULATED_KEY_ID],
                              "trust_root_editor_role": SIGNER_ROLE})
        grid = simulated_production_grid(self.collections)
        self.assertIn("CUSTODY_SEPARATION_INVALID", admit(grid, manifest=forged))

    def test_bw13_adversarial_key_absent_from_the_manifest_is_refused(self):
        """A signing key not present in the injected manifest cannot admit anything."""
        forged = simulated_production_manifest(
            root_overrides={"key_id": "MBCX01.BUILD.OTHER.ED25519.TEST.1"})
        grid = simulated_production_grid(self.collections)
        self.assertIn("MEASUREMENT_SIGNATURE_INVALID", admit(grid, manifest=forged))

    def test_bw13_adversarial_r13_fixture_relabeled_as_physical_is_refused(self):
        """An r13 fixture envelope relabeled PHYSICAL_HARNESS_RECEIPT stays fixture."""
        rows = sign_no_paid_test_envelopes(
            measurement.baseline_receipt_rows(run_id=R13_RUN_ID))
        for envelope in rows:
            envelope["fixture_kind"] = producer.PRODUCTION_FIXTURE_KIND
            envelope["producer_role"] = producer.PRODUCTION_PRODUCER_ROLE
            measurement.refresh_receipt_hash(envelope)
        self.assertIn("FIXTURE_EVIDENCE_RELABELED", admit(rows, run_id=R13_RUN_ID))

    def test_bw13_positive_frozen_r13_evaluator_stays_unavailable_for_everything(self):
        """Compatibility: the frozen evaluator admits nothing, before and after BUILD B."""
        rows = sign_no_paid_test_envelopes(
            measurement.baseline_receipt_rows(run_id=R13_RUN_ID))
        self.assertEqual(measurement.evaluate_measurement_receipts(
            rows, expected_run_id=R13_RUN_ID), ["PHYSICAL_HARNESS_UNAVAILABLE"])
        grid = simulated_production_grid(self.collections)
        self.assertIn("PHYSICAL_HARNESS_UNAVAILABLE",
                      measurement.evaluate_measurement_receipts(
                          grid, expected_run_id=RUN_ID))
        self.assertEqual(admit(grid), [])


class BuildMalformedEvidenceTests(unittest.TestCase):
    """bw14: malformed input returns a closed error list, never a traceback."""

    def test_bw14_adversarial_wrong_types_return_a_closed_error_list(self):
        """Non-list, non-dict and None inputs return closed errors."""
        for payload in (None, "envelopes", 17, {}, [None], [{"schema_id": 1}]):
            with self.subTest(payload=repr(payload)[:32]):
                errors = admit(payload)
                self.assertTrue(set(errors) <= authority.PRODUCTION_ERROR_CODES, errors)
                self.assertIn("MEASUREMENT_ENVELOPE_INVALID", errors)

    def test_bw14_adversarial_missing_and_extra_envelope_keys_are_refused(self):
        """The V2 envelope key set is closed in both directions."""
        template = {key: "" for key in producer.PRODUCTION_ENVELOPE_KEYS}
        missing = {key: value for key, value in template.items() if key != "nonce"}
        extra = dict(template, unexpected_field="X")
        for payload in (missing, extra):
            with self.subTest(keys=len(payload)):
                errors = admit([payload])
                self.assertTrue(set(errors) <= authority.PRODUCTION_ERROR_CODES, errors)
                self.assertIn("MEASUREMENT_ENVELOPE_INVALID", errors)

    def test_bw14_adversarial_malformed_manifest_raises_a_typed_error(self):
        """A malformed manifest raises MeasurementAuthorityError; a valid one does not."""
        for document in (None, [], {"schema_id": "MeasurementTrustRootManifestV2"}):
            with self.subTest(document=repr(document)[:32]):
                with self.assertRaises(authority.MeasurementAuthorityError):
                    authority.validate_production_trust_root_manifest(document)
        # The typed error must be selective: a well-formed injected manifest
        # validates, otherwise the assertions above prove nothing.
        roots = authority.validate_production_trust_root_manifest(
            simulated_production_manifest())
        self.assertIsInstance(roots, dict)

    def test_bw14_adversarial_malformed_custody_evidence_is_named_not_thrown(self):
        """Missing custody documents produce a named closed error."""
        errors = admit([], custody={})
        self.assertTrue(set(errors) <= authority.PRODUCTION_ERROR_CODES, errors)
        self.assertIn("MEASUREMENT_CUSTODY_EVIDENCE_INVALID", errors)


class BuildTimingCrossCheckTests(unittest.TestCase):
    """bw15: V2-only QPC/elapsed cross-check (tightens r13's `> 0` check)."""

    def setUp(self):
        self.collections = simulated_collections()

    def test_bw15_positive_elapsed_matches_the_signed_qpc_lifetimes_span(self):
        """Elapsed monotonic ns is reproducible from the signed QPC span and frequency."""
        collection = self.collections[0]
        span = (collection.process_lifetimes[0]["ended_qpc"]
                - collection.process_lifetimes[0]["started_qpc"])
        self.assertEqual(span, collection.elapsed_qpc_ticks)
        self.assertEqual(collection.elapsed_monotonic_ns,
                         span * 1_000_000_000 // collection.qpc_frequency_hz)
        grid = simulated_production_grid(self.collections)
        block = grid[0]["timing_cross_check"]
        self.assertEqual(set(block), set(producer.TIMING_CROSS_CHECK_KEYS))
        self.assertEqual(admit(grid), [])

    def test_bw15_adversarial_elapsed_inconsistent_with_lifetimes_is_refused(self):
        """An elapsed value the QPC lifetimes cannot produce is fatal, not merely > 0."""
        grid = simulated_production_grid(perturbed(
            self.collections, 0, elapsed_monotonic_ns=ELAPSED_MONOTONIC_NS * 7))
        self.assertIn("MONOTONIC_TIME_CROSS_CHECK_FAILED", admit(grid))

    def test_bw15_adversarial_forged_qpc_frequency_is_refused(self):
        """A frequency chosen to make a wrong elapsed value fit is still rejected."""
        grid = simulated_production_grid(perturbed(
            self.collections, 0, qpc_frequency_hz=QPC_FREQUENCY_HZ * 7))
        self.assertIn("MONOTONIC_TIME_CROSS_CHECK_FAILED", admit(grid))


class BuildExactnessAuthorityTests(unittest.TestCase):
    """bw16/bw63: production carrier-exactness authority stays separate from fixture
    mode, and binds only evidence its signature actually covers."""

    def setUp(self):
        self.collections = simulated_collections()
        with open(measurement.EXACTNESS_SUITE, encoding="utf-8") as stream:
            self.suite = json.load(stream)

    def test_bw16_positive_production_exactness_binds_suite_carrier_build_and_grid(self):
        """A production exactness receipt verifies only against recomputed bindings."""
        grid = simulated_production_grid(self.collections)
        manifest = simulated_production_manifest()
        receipt = exactness.verify_production_carrier_exactness(
            {"schema_id": exactness.EXACTNESS_RECEIPT_SCHEMA_ID},
            envelopes=grid, suite_document=self.suite,
            trust_root_manifest=manifest,
            custody_evidence=simulated_custody_evidence(manifest))
        self.assertEqual(set(receipt), set(exactness.EXACTNESS_RECEIPT_V3_KEYS))
        self.assertEqual(receipt["authority_mode"], exactness.PRODUCTION_AUTHORITY_MODE)

    def test_bw16_adversarial_fixture_receipt_relabeled_production_is_refused(self):
        """A CarrierExactnessReceiptV2 fixture receipt cannot become production authority."""
        rows = sign_no_paid_test_envelopes(
            measurement.baseline_receipt_rows(run_id=R13_RUN_ID))
        fixture_receipt = measurement.fixture_carrier_exactness_receipt(
            "CANDIDATE.BASELINE", rows)
        fixture_receipt["authority_mode"] = exactness.PRODUCTION_AUTHORITY_MODE
        fixture_receipt["receipt_hash"] = measurement.sha384(
            {key: value for key, value in fixture_receipt.items()
             if key != "receipt_hash"})
        with self.assertRaisesRegex(authority.MeasurementAuthorityError,
                                    "FIXTURE_EVIDENCE_RELABELED"):
            exactness.verify_production_carrier_exactness(
                fixture_receipt, envelopes=rows, suite_document=self.suite,
                trust_root_manifest=simulated_production_manifest(),
                custody_evidence=simulated_custody_evidence())

    def test_bw63_adversarial_receipt_edited_after_signing_cannot_rebind_the_carrier(self):
        """Invariant I16 (codex r1 P1): the receipt this door BINDS must be the receipt
        the signature COVERS. The door verified `receipt_preimage_b64` but read every
        binding out of `envelope["receipt"]` — two different objects — so editing the
        receipt after signing left the signature valid over the ORIGINAL bytes while the
        carrier artifact digest and grid identity were recomputed from the EDITED one.
        A stale signed payload could therefore authorize an arbitrary CURRENT
        carrier/grid binding, which is exactly the exactness claim I16 says is pinned
        (`MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md` row I16). The mismatch is refused
        by name before any binding is derived, never silently rebound."""
        manifest = simulated_production_manifest()
        custody = simulated_custody_evidence(manifest)
        grid = simulated_production_grid(self.collections)
        honest = exactness.verify_production_carrier_exactness(
            {"schema_id": exactness.EXACTNESS_RECEIPT_SCHEMA_ID}, envelopes=grid,
            suite_document=self.suite, trust_root_manifest=manifest,
            custody_evidence=custody)
        substituted = measurement.sha384("MBCX01.BUILD.B.SUBSTITUTED.CARRIER.ARTIFACT")
        self.assertNotEqual(honest["carrier_artifact_digest"], substituted)
        edited = copy.deepcopy(grid)
        for envelope in edited:
            envelope["receipt"]["candidate_artifact_digest"] = substituted
        # The SIGNED members are untouched, which is what made the stale payload usable:
        # the signature still verifies over the original preimage bytes.
        for row, signed in zip(edited, grid):
            self.assertEqual(row["receipt_preimage_b64"], signed["receipt_preimage_b64"])
            self.assertEqual(row["signature_b64"], signed["signature_b64"])
            self.assertEqual(row["receipt_digest"], signed["receipt_digest"])
        with self.assertRaisesRegex(authority.MeasurementAuthorityError,
                                    "MEASUREMENT_SIGNATURE_INVALID"):
            exactness.verify_production_carrier_exactness(
                {"schema_id": exactness.EXACTNESS_RECEIPT_SCHEMA_ID}, envelopes=edited,
                suite_document=self.suite, trust_root_manifest=manifest,
                custody_evidence=custody)
        # The refusal stays inside the closed production vocabulary, and the untouched
        # grid still carries its own signed carrier: strictness, not breakage.
        self.assertIn("MEASUREMENT_SIGNATURE_INVALID", authority.PRODUCTION_ERROR_CODES)
        self.assertEqual(grid[0]["receipt"]["candidate_artifact_digest"],
                         honest["carrier_artifact_digest"])


def attacker_custody_documents() -> dict:
    """Four custody documents the attacker writes for itself (SEAT2/SEAT3 shape)."""
    return {
        "SEPARATE_KEY_CUSTODY_ATTESTATION": {
            "schema_id": "KeyCustodyAttestationV1",
            "custodian_role": "ATTACKER_NAMED_CUSTODIAN_ROLE",
            "key_id": ATTACKER_KEY_ID,
            "private_key_never_leaves_custody": True,
            "attested_by": "ATTACKER.SELF.AUTHORED.OFFICER"},
        "SEPARATE_TRUST_ROOT_EDITOR_APPROVAL": {
            "schema_id": "TrustRootEditorApprovalV1",
            "editor_role": "ATTACKER_NAMED_EDITOR_ROLE",
            "approver_key_id": ATTACKER_EDITOR_KEY_ID,
            "approved_manifest_id": "ATTACKER.SELF.AUTHORED.MEASUREMENT.MANIFEST",
            "signer_key_ids_excluded": [ATTACKER_KEY_ID]},
        "HARNESS_BUILD_PROVENANCE": {
            "schema_id": "HarnessBuildProvenanceV1",
            "harness_build_digest": HARNESS_IDENTITY["harness_build_digest"],
            "build_reviewed": True,
            "builder_role": "ATTACKER_NAMED_BUILDER_ROLE"},
        "PRODUCTION_SIGNING_CEREMONY_RECEIPT": {
            "schema_id": "SigningCeremonyReceiptV1",
            "ceremony_id": "ATTACKER.SELF.AUTHORED.CEREMONY",
            "signer_key_id": ATTACKER_KEY_ID,
            "witness_roles": ["ATTACKER_NAMED_EDITOR_ROLE"],
            "candidate_and_evaluator_received_private_key": False},
    }


def attacker_manifest(documents: dict) -> dict:
    """An entirely attacker-authored `MeasurementTrustRootManifestV3`.

    Every field of it — activation authority, roles, editor key ids, custody digests,
    the root public key — is chosen by the attacker, and it is internally consistent:
    exactly the universe SEAT2 and SEAT3 built, which cleared production admission
    before the r1 fold.
    """
    policy = {
        "schema_id": "ProductionMeasurementTrustPolicyV2",
        "status": "ACTIVATED",
        "fail_loud_sentinel": "PHYSICAL_HARNESS_UNAVAILABLE",
        "signer_custodian_role": "ATTACKER_NAMED_CUSTODIAN_ROLE",
        "trust_root_editor_role": "ATTACKER_NAMED_EDITOR_ROLE",
        "roles_must_be_distinct": True,
        "manifest_edit_cannot_activate_production": True,
        "required_external_evidence": list(authority.REQUIRED_CUSTODY_EVIDENCE),
        "key_custodian_attestation_digest": measurement.sha384(
            documents["SEPARATE_KEY_CUSTODY_ATTESTATION"]),
        "trust_root_editor_approval_digest": measurement.sha384(
            documents["SEPARATE_TRUST_ROOT_EDITOR_APPROVAL"]),
        "harness_build_provenance_digest": measurement.sha384(
            documents["HARNESS_BUILD_PROVENANCE"]),
        "signing_ceremony_receipt_digest": measurement.sha384(
            documents["PRODUCTION_SIGNING_CEREMONY_RECEIPT"]),
        "editor_approval_key_ids": [ATTACKER_EDITOR_KEY_ID],
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
        "roots": [{
            "key_id": ATTACKER_KEY_ID,
            "algorithm": "ED25519",
            "fixture_only": False,
            "authorized_producer_role": producer.PRODUCTION_PRODUCER_ROLE,
            "authorized_fixture_kind": producer.PRODUCTION_FIXTURE_KIND,
            "signer_custodian_role": "ATTACKER_NAMED_CUSTODIAN_ROLE",
            "authorized_harness_build_digest":
                HARNESS_IDENTITY["harness_build_digest"],
            "trust_policy_digest": measurement.sha384(policy),
            "public_key_pem": ATTACKER_PUBLIC_KEY_PEM,
            "validity": {"not_before": "2026-08-14T00:00:00Z",
                         "not_after": "2027-08-14T00:00:00Z"},
            "revocation_state": "ACTIVE",
        }],
    }


def attacker_universe() -> tuple[dict, dict, list[dict]]:
    """(manifest, custody_evidence, 100 signed envelopes), all attacker-authored."""
    documents = attacker_custody_documents()
    manifest = attacker_manifest(documents)
    roots = authority.validate_production_trust_root_manifest(manifest)
    binding = authority.production_activation_binding(manifest, roots, documents)
    # The attacker also writes an activation statement — and signs it with the only key
    # it has. It names the anchor id it read out of the repository, so this is the
    # strongest form of the attack: everything the verifier compares is present and
    # coherent, and the ONE thing the attacker cannot produce is the owner signature.
    documents[authority.OWNER_ACTIVATION_EVIDENCE] = ceremony.activation_statement(
        manifest=manifest, private_key_pem=ATTACKER_PRIVATE_KEY_PEM, **binding)
    grid = simulated_production_grid(
        signer=producer.FixtureSigner(ATTACKER_KEY_ID, ATTACKER_PRIVATE_KEY_PEM),
        identity=simulated_identity(
            signing_key_id=ATTACKER_KEY_ID,
            trust_policy_digest=manifest["roots"][0]["trust_policy_digest"]))
    return manifest, documents, grid


class BuildAuthenticatedTrustBootstrapTests(unittest.TestCase):
    """bw17-bw21: the r1 fix class AUTHENTICATED_PRODUCTION_TRUST_BOOTSTRAP.

    ONE invariant is under test in all five: no unauthenticated trust graph reaches
    production admission. The anchor is operator-preconfigured and unreachable from any
    request; every self-authored universe fails BEFORE any grid or scientific analysis.
    """

    maxDiff = None

    def setUp(self):
        ceremony.configure_test_production_anchor()
        self.addCleanup(ceremony.configure_test_production_anchor)

    def test_bw17_adversarial_fully_self_authored_universe_fails_before_grid_analysis(self):
        """Invariant: a fresh attacker key + attacker manifest + attacker custody
        documents + attacker activation + 100 attacker-signed envelopes is refused by
        NAME, and refused before any grid, evidence-tree or scientific analysis runs.

        This is the r1 deciding attack (SEAT2 and SEAT3, both EXECUTED). Before the
        fold `evaluate_production_measurement` returned `[]` for exactly this input."""
        manifest, custody, grid = attacker_universe()
        self.assertEqual(len(grid), 100)
        errors = authority.evaluate_production_measurement(
            grid, trust_root_manifest=manifest, custody_evidence=custody,
            expected_run_id=RUN_ID)
        self.assertIn("PRODUCTION_ACTIVATION_UNAUTHENTICATED", errors)
        self.assertIn(authority.FAIL_LOUD_SENTINEL, errors)
        # Nothing downstream of the trust bootstrap was consulted: the verdict is the
        # authentication failure and the sentinel, and nothing else.
        self.assertEqual(set(errors), {"PRODUCTION_ACTIVATION_UNAUTHENTICATED",
                                       authority.FAIL_LOUD_SENTINEL})
        # ... and the same verdict with NO grid at all, which proves the grid was never
        # what carried the decision.
        self.assertEqual(
            set(authority.evaluate_production_measurement(
                [], trust_root_manifest=manifest, custody_evidence=custody,
                expected_run_id=RUN_ID)),
            {"PRODUCTION_ACTIVATION_UNAUTHENTICATED", authority.FAIL_LOUD_SENTINEL})

    def test_bw18_positive_operator_anchored_ceremony_activation_admits_the_grid(self):
        """Invariant: the LEGITIMATE authenticated ceremony path is green — a manifest
        the operator-preconfigured owner anchor actually signed admits the simulated
        production grid — and the anchor is not, and cannot be, a request parameter."""
        parameters = set(inspect.signature(
            authority.evaluate_production_measurement).parameters)
        self.assertEqual(parameters, {"envelopes", "trust_root_manifest",
                                      "custody_evidence", "expected_run_id"})
        self.assertNotIn("anchor", " ".join(parameters))
        manifest = simulated_production_manifest()
        custody = simulated_custody_evidence(manifest)
        self.assertEqual(custody[authority.OWNER_ACTIVATION_EVIDENCE]["anchor_id"],
                         ceremony.test_production_anchor_document()["anchor_id"])
        grid = simulated_production_grid()
        self.assertEqual(authority.evaluate_production_measurement(
            grid, trust_root_manifest=manifest, custody_evidence=custody,
            expected_run_id=RUN_ID), [])

    def test_bw19_adversarial_anchor_absent_wrong_signer_wrong_binding_or_rolled_back(self):
        """Invariant: every way of reaching admission without THIS owner anchor having
        signed THIS manifest fails closed with a named refusal — an unconfigured anchor
        most of all, because "nobody configured a root of trust" must never read as
        "no root of trust was required"."""
        manifest = simulated_production_manifest()
        grid = simulated_production_grid()

        # (a) no anchor configured at all -> REFUSAL, never a bypass.
        trust_anchor.clear_owner_trust_anchor()
        errors = admit(grid, manifest=manifest,
                       custody=simulated_custody_evidence(manifest))
        ceremony.configure_test_production_anchor()
        self.assertIn("PRODUCTION_TRUST_ANCHOR_UNAVAILABLE", errors)
        self.assertIn(authority.FAIL_LOUD_SENTINEL, errors)

        # (b) a genuinely signed statement — signed by a key that is not the anchor.
        self.assertIn("PRODUCTION_ACTIVATION_UNAUTHENTICATED", admit(
            grid, manifest=manifest,
            custody=simulated_custody_evidence(
                manifest,
                private_key_pem=ceremony.FIXTURE_NON_ANCHOR_PRIVATE_KEY_PEM)))

        # (c) an owner-signed statement that binds a DIFFERENT manifest digest: the
        #     signature is real, the authorization is for something else.
        self.assertIn("PRODUCTION_ACTIVATION_UNAUTHENTICATED", admit(
            grid, manifest=manifest,
            custody=simulated_custody_evidence(
                manifest,
                activation_overrides={"manifest_digest": measurement.sha384(
                    "MBCX01.SOME.OTHER.MANIFEST")})))

        # (d) an owner-signed activation from BEFORE the operator's current generation.
        self.assertIn("PRODUCTION_ACTIVATION_UNAUTHENTICATED", admit(
            grid, manifest=manifest,
            custody=simulated_custody_evidence(
                manifest, activation_overrides={"activation_generation": 0})))

        # (e) the activation simply absent from the custody set.
        custody = simulated_custody_evidence(manifest)
        del custody[authority.OWNER_ACTIVATION_EVIDENCE]
        self.assertIn("MEASUREMENT_CUSTODY_EVIDENCE_INVALID",
                      admit(grid, manifest=manifest, custody=custody))

    def test_bw20_adversarial_whitespace_injected_signature_carrier_is_refused(self):
        """Invariant (MBCX01-BUILD-R1-SIGNATURE-CARRIER / codex F6): one signature has
        exactly ONE accepted carrier. A whitespace-injected but otherwise valid
        Ed25519 carrier is a named refusal, not a silent acceptance."""
        grid = simulated_production_grid()
        self.assertEqual(admit(grid), [])
        carrier = grid[7]["signature_b64"]
        for mutation in (carrier[:8] + "\n" + carrier[8:],
                         carrier[:8] + " " + carrier[8:],
                         carrier.replace("+", "-").replace("/", "_")):
            with self.subTest(carrier=mutation[:16]):
                if mutation == carrier:
                    continue
                forged = copy.deepcopy(grid)
                forged[7]["signature_b64"] = mutation
                self.assertIn("MEASUREMENT_SIGNATURE_CARRIER_INVALID", admit(forged))
        self.assertTrue(trust_anchor.strict_signature_carrier_ok(carrier))

    def test_bw21_adversarial_exactness_authority_requires_the_anchored_activation(self):
        """Invariant: the exactness authority is the THIRD production door and takes the
        same bootstrap. A self-authored trust universe cannot buy an exactness AUTHORITY
        BINDING either, and neither can a missing activation."""
        with open(measurement.EXACTNESS_SUITE, encoding="utf-8") as stream:
            suite = json.load(stream)
        manifest, custody, grid = attacker_universe()
        with self.assertRaisesRegex(authority.MeasurementAuthorityError,
                                    "PRODUCTION_ACTIVATION_UNAUTHENTICATED"):
            exactness.verify_production_carrier_exactness(
                {"schema_id": exactness.EXACTNESS_RECEIPT_SCHEMA_ID},
                envelopes=grid, suite_document=suite,
                trust_root_manifest=manifest, custody_evidence=custody)
        with self.assertRaisesRegex(authority.MeasurementAuthorityError,
                                    "PRODUCTION_ACTIVATION_UNAUTHENTICATED"):
            exactness.verify_production_carrier_exactness(
                {"schema_id": exactness.EXACTNESS_RECEIPT_SCHEMA_ID},
                envelopes=simulated_production_grid(), suite_document=suite,
                trust_root_manifest=simulated_production_manifest(),
                custody_evidence=None)


class BuildFixtureIsolationTests(unittest.TestCase):
    """bw22/bw24-bw27: the r2 fix class FIXTURE_ISOLATION / INSTANCE_SCOPED_VERIFIER_CONTEXT.

    ONE invariant is under test in all five: production verification accepts exactly one
    thing — an immutable, INSTANCE-SCOPED verifier context whose anchor is
    operator-supplied and NOT fixture-marked, carrying its own current time — and
    refuses everything else. Adopted, not invented: Go `crypto/x509` `VerifyOptions`
    (roots AND `CurrentTime` are per-verification fields the verifier constructs; the
    no-time fallback is the real clock, never a value read out of the artifact) and the
    TUF out-of-band trusted root (`MBCX-01-BUILD-R2-TRUSTCONTEXT-SWEEP-LOG.md`).
    """

    maxDiff = None

    def setUp(self):
        ceremony.configure_test_production_anchor()
        self.addCleanup(ceremony.configure_test_production_anchor)
        with open(measurement.EXACTNESS_SUITE, encoding="utf-8") as stream:
            self.suite = json.load(stream)

    def fixture_anchored_universe(self):
        """A universe whose owner activation is signed by the COMMITTED fixture key."""
        document = ceremony.fixture_owner_anchor_document()
        manifest = simulated_production_manifest()
        custody = simulated_custody_evidence(
            manifest, anchor_id=document["anchor_id"],
            private_key_pem=ceremony.FIXTURE_OWNER_PRIVATE_KEY_PEM)
        return manifest, custody, simulated_production_grid()

    def test_bw22_adversarial_committed_fixture_anchor_cannot_grant_production(self):
        """Invariant (codex r2 F1, the deciding one): the COMMITTED fixture owner anchor
        — whose private half is committed at `mbcx01_build_ceremony_fixture.py`, and is
        therefore public to anyone holding this repository — cannot authorize a
        production admission at ANY door, even when it correctly signs an activation
        that binds the exact manifest and custody set. The fixture LANE (structural
        parsing, which activates nothing) stays green, which is what makes this a
        refusal of fixture AUTHORITY rather than a refusal of fixture DOCUMENTS."""
        ceremony.configure_fixture_owner_anchor()
        manifest, custody, grid = self.fixture_anchored_universe()
        self.assertEqual(custody[authority.OWNER_ACTIVATION_EVIDENCE]["anchor_id"],
                         ceremony.fixture_owner_anchor_document()["anchor_id"])
        errors = admit(grid, manifest=manifest, custody=custody)
        self.assertIn(authority.PRODUCTION_TRUST_ANCHOR_FIXTURE_ONLY, errors)
        self.assertIn(authority.FAIL_LOUD_SENTINEL, errors)
        with self.assertRaisesRegex(authority.MeasurementAuthorityError,
                                    authority.PRODUCTION_TRUST_ANCHOR_FIXTURE_ONLY):
            exactness.verify_production_carrier_exactness(
                {"schema_id": exactness.EXACTNESS_RECEIPT_SCHEMA_ID}, envelopes=grid,
                suite_document=self.suite, trust_root_manifest=manifest,
                custody_evidence=custody)
        # The fixture LANE is untouched: the committed fixture manifest still parses,
        # and the committed anchor document is still fixture-only and key-free.
        roots = authority.validate_production_trust_root_manifest(
            committed_fixture_manifest())
        self.assertEqual({row["fixture_only"] for row in roots.values()}, {True})
        document = ceremony.fixture_owner_anchor_document()
        self.assertIs(document["fixture_only"], True)
        self.assertNotIn("PRIVATE", json.dumps(document))
        # A fixture anchor is not even representable as a production context.
        with self.assertRaisesRegex(trust_anchor.TrustAnchorError, "FIXTURE_ANCHOR"):
            trust_anchor.ProductionVerifierContext(
                anchor=trust_anchor.anchor_from_document(document, source="TEST"))

    # bw23 (the wiring-FREEZE witness) was DELETED on 2026-08-14 together with the
    # machinery it tested. It asserted that a caller-supplied mapping whose
    # `.get`/`__getitem__` re-wire the process anchor is refused
    # `*_REWIRED_DURING_VERIFICATION` and cannot leave the process re-wired. That
    # defence was built against an adversary the design of record does not have:
    # MBCX-01 has no API, no production runtime and no external submitter, so an actor
    # able to run code in this interpreter IS the box owner, and on-box walls against
    # the box owner are theatre under the permanent T2 ceiling (`DESIGN-SHELF-MAP.md`
    # §1). See `MBCX-01-BUILD-ADVERSARY-PREMISE-CORRECTION-2026-08-14.md`. The
    # ACCEPTED RESIDUAL, named rather than defended: such a gadget now succeeds in
    # re-wiring the process for subsequent calls. What survives and is still witnessed
    # is the part that serves scientific validity — each door snapshots its verifier
    # context ONCE at entry (bw27), and a fixture ASSEMBLER restores the operator's
    # wiring on scope exit (bi05).

    def test_bw24_adversarial_expired_manifest_is_refused_at_the_verifier_clock(self):
        """Invariant (codex r2 F4): the evaluation instant belongs to the VERIFIER, not
        to the artifact under verification. A manifest whose validity window closed in
        2001 — carrying a 2000 revocation `published_at` of its own choosing, and
        correctly activated by the operator's anchor — is refused, and the fallback when
        the operator injects no instant is the REAL clock (Go `VerifyOptions.CurrentTime`
        falls back to `time.Now()`). A test may inject a fixed instant, which is how this
        suite stays deterministic."""
        window = {"not_before": "2000-01-01T00:00:00Z",
                  "not_after": "2001-01-01T00:00:00Z"}
        template = simulated_production_manifest()
        manifest = simulated_production_manifest(
            root_overrides={"validity": dict(window)},
            manifest_overrides={
                "validity": dict(window),
                "revocation": dict(template["revocation"],
                                   published_at="2000-06-01T00:00:00Z")})
        custody = simulated_custody_evidence(manifest)
        grid = simulated_production_grid()
        # (a) the operator wired NO instant: the fallback is the real clock.
        trust_anchor.configure_owner_trust_anchor(
            ceremony.test_production_anchor_document())
        errors = admit(grid, manifest=manifest, custody=custody)
        self.assertIn("TRUST_ROOT_VALIDITY_EXPIRED", errors)
        self.assertIn(authority.FAIL_LOUD_SENTINEL, errors)
        # (b) an INJECTED instant inside the window admits — the clock is the
        #     verifier's, and it is injectable, so the suite is deterministic.
        trust_anchor.configure_owner_trust_anchor(
            ceremony.test_production_anchor_document(),
            current_time="2000-06-01T00:00:00Z")
        self.assertEqual(admit(grid, manifest=manifest, custody=custody), [])
        # (c) the manifest's own `published_at` is NEVER the fallback: restore the
        #     operator's real-clock context and the same manifest is refused again.
        trust_anchor.configure_owner_trust_anchor(
            ceremony.test_production_anchor_document())
        self.assertIn("TRUST_ROOT_VALIDITY_EXPIRED",
                      admit(grid, manifest=manifest, custody=custody))

    def test_bw25_adversarial_binding_only_exactness_is_not_labelled_suite_executed(self):
        """Invariant (codex r2 F7): this authority BINDS an exactness claim; it does not
        execute the carrier suite (`MBCX-01-BUILD-EXACTNESS-PRODUCTION-VERIFIER-SPEC.md`
        section 3 defers the runner). A binding-only result must therefore not emit a
        value that reads as "the suite ran", and a receipt CLAIMING `PASS` is a named
        refusal rather than a blessing."""
        manifest = simulated_production_manifest()
        custody = simulated_custody_evidence(manifest)
        grid = simulated_production_grid()
        receipt = exactness.verify_production_carrier_exactness(
            {"schema_id": exactness.EXACTNESS_RECEIPT_SCHEMA_ID}, envelopes=grid,
            suite_document=self.suite, trust_root_manifest=manifest,
            custody_evidence=custody)
        self.assertEqual(receipt["result"], exactness.BINDING_ONLY_RESULT)
        self.assertNotEqual(receipt["result"], "PASS")
        self.assertNotIn("PASS", receipt["result"])
        self.assertIn("SUITE_NOT_EXECUTED", receipt["result"])
        with self.assertRaisesRegex(authority.MeasurementAuthorityError,
                                    "CARRIER_EXACTNESS_SUITE_NOT_EXECUTED"):
            exactness.verify_production_carrier_exactness(
                {"schema_id": exactness.EXACTNESS_RECEIPT_SCHEMA_ID, "result": "PASS"},
                envelopes=grid, suite_document=self.suite,
                trust_root_manifest=manifest, custody_evidence=custody)

    def test_bw26_adversarial_ambiguous_anchor_document_is_refused_at_the_loader(self):
        """Invariant (codex r2 F6): the operator configuration boundary parses strictly.
        A duplicate member is an AMBIGUOUS document — `json.load` silently takes the
        last one, which for `fixture_only` flips the document's meaning — so it is
        refused by name instead of resolved by accident."""
        document = ceremony.fixture_owner_anchor_document()
        serialized = json.dumps(document)
        directory = tempfile.mkdtemp(prefix="mbcx01-build-anchor-")
        self.addCleanup(shutil.rmtree, directory, True)
        ambiguous = os.path.join(directory, "ambiguous.json")
        with open(ambiguous, "w", encoding="utf-8") as stream:
            stream.write(serialized[:-1] + ', "fixture_only": false}')
        with self.assertRaisesRegex(trust_anchor.TrustAnchorError,
                                    "OWNER_TRUST_ANCHOR_AMBIGUOUS"):
            trust_anchor.load_owner_trust_anchor(ambiguous)
        # The unambiguous document still loads, so this is strictness, not breakage.
        honest = os.path.join(directory, "honest.json")
        with open(honest, "w", encoding="utf-8") as stream:
            stream.write(serialized)
        self.assertIs(trust_anchor.load_owner_trust_anchor(honest).fixture_only, True)

    def test_bw27_positive_verifier_context_is_immutable_instance_scoped_and_clocked(self):
        """Invariant (the r2 COMPLEMENT): production verification accepts EXACTLY one
        thing. The context refuses ordinary attribute assignment, carries its own current
        time, is constructed by the OPERATOR, and is not reachable from any admission
        parameter — while the legitimate operator-anchored path stays green through it.
        The guards emulate immutability against ordinary use only: `object.__setattr__`
        still edits a live context, and that bypass needs an in-process actor who is the
        box owner, so it is an accepted residual, not a defended boundary (T2 ceiling,
        `DESIGN-SHELF-MAP.md` §1)."""
        context = trust_anchor.ProductionVerifierContext(
            anchor=trust_anchor.anchor_from_document(
                ceremony.test_production_anchor_document(), source="TEST"),
            current_time=ceremony.TEST_VERIFIER_INSTANT)
        self.assertIs(context.anchor.fixture_only, False)
        self.assertEqual(context.current_instant(), ceremony.TEST_VERIFIER_INSTANT)
        for attribute in ("anchor", "current_time", "source"):
            with self.subTest(attribute=attribute):
                with self.assertRaises(trust_anchor.TrustAnchorError):
                    setattr(context, attribute, "MUTATED")
        # No admission entry point takes an anchor or a context: the api-caller cannot
        # supply one, which is what "operator-supplied" means mechanically.
        for function in (authority.evaluate_production_measurement,
                         exactness.verify_production_carrier_exactness):
            parameters = " ".join(inspect.signature(function).parameters)
            with self.subTest(function=function.__name__):
                self.assertNotIn("anchor", parameters)
                self.assertNotIn("context", parameters)
        # With no wiring at all, the context resolves to a REFUSAL, never to a bypass.
        trust_anchor.clear_owner_trust_anchor()
        resolved, refusal = trust_anchor.resolve_production_verifier_context(
            trust_anchor.AUTHORITY_MEASUREMENT)
        self.assertIsNone(resolved)
        self.assertEqual(refusal, trust_anchor.ANCHOR_UNAVAILABLE)
        # ... and the operator's own context admits the legitimate grid.
        trust_anchor.configure_production_verifier_context(context)
        resolved, refusal = trust_anchor.resolve_production_verifier_context(
            trust_anchor.AUTHORITY_MEASUREMENT)
        self.assertIs(resolved, context)
        self.assertIsNone(refusal)
        self.assertEqual(admit(simulated_production_grid()), [])

    def test_bw28_adversarial_relabelled_committed_fixture_key_is_not_a_production_root(self):
        """Invariant (BUILD acceptance r3 seat finding, reproduced at the byte): a
        production root of trust is recognised by its KEY, not by a flag in a document.

        The committed anchor document is the example an operator copies: the custody
        ceremony (`MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md` §3 step 0) is a human
        hand-writing an `OwnerTrustAnchorV1`, and editing the two fields that look like
        labels — `fixture_only` to `false`, a new `anchor_id` — used to produce a
        PRODUCTION context around a public key whose private half is committed at
        `mbcx01_build_ceremony_fixture.py` and is therefore held by everyone holding this
        repository. That is MITRE CWE-1291 (public key re-used for debug and production
        signing, PeerOf CWE-321), whose mitigation phase is Implementation — and we
        satisfy it with a refusal at CONTEXT CONSTRUCTION, by name, and the known-key set is DERIVED
        from the committed documents rather than pasted in.

        This is an OPERATOR FOOTGUN guard, not an access-control boundary: MBCX-01 has no
        threat model and no untrusted caller (`MBCX-01-BUILD-ADVERSARY-PREMISE-
        CORRECTION-2026-08-14.md`). It stops the experiment fooling ITSELF."""
        document = ceremony.fixture_owner_anchor_document()
        # (a) the set is DERIVED from the repository's own committed documents.
        material = trust_anchor.committed_fixture_key_material()
        identity = trust_anchor.public_key_identity(document["public_key_pem"])
        self.assertEqual(material.get(identity),
                         os.path.basename(ceremony.FIXTURE_ANCHOR_PATH))
        with open(trust_anchor.__file__, encoding="utf-8") as stream:
            module_source = stream.read()
        self.assertNotIn(identity, module_source)
        # (b) the relabelled copy: the LABELS say production, the KEY says otherwise.
        relabelled = dict(document, fixture_only=False,
                          anchor_id="MBCX01.RELABELLED.ANCHOR.1")
        self.assertEqual(relabelled["public_key_pem"], document["public_key_pem"])
        for label, candidate in (
                ("document", relabelled),
                ("anchor object", trust_anchor.OwnerTrustAnchor(
                    anchor_id="MBCX01.RELABELLED.ANCHOR.2", algorithm="ED25519",
                    public_key_pem=document["public_key_pem"],
                    authorities=list(trust_anchor.AUTHORITIES),
                    minimum_activation_generation=1, fixture_only=False)),
                # The same key, RE-ENCODED by a hand edit, is the same key. The variant is
                # built from the DECODED key bytes (`_long_form_bit_string_spki`), never
                # from `public_key_identity`: the original sub-case here wrapped the
                # output of that very normalizer, so it could only ever confirm the
                # normalizer's own fixed points and could never reach a re-encoding
                # (recorded as MBCX01-R4-BW28-WITNESS-CANNOT-DISCRIMINATE-ITS-CLASS).
                ("re-encoded key", dict(
                    relabelled,
                    public_key_pem=_pem_from_der(_long_form_bit_string_spki(
                        _spki_der(document["public_key_pem"])))))):
            with self.subTest(candidate=label):
                with self.assertRaisesRegex(
                        trust_anchor.TrustAnchorError,
                        trust_anchor.PRODUCTION_VERIFIER_CONTEXT_FIXTURE_KEY_MATERIAL):
                    trust_anchor.new_production_verifier_context(candidate)
        # (c) the same document delivered the way an operator delivers a real one — an OS
        #     configuration path — is refused at the same seam, not resolved to a root.
        directory = tempfile.mkdtemp(prefix="mbcx01-build-fixturekey-")
        self.addCleanup(shutil.rmtree, directory, True)
        path = os.path.join(directory, "owner-trust-anchor.json")
        with open(path, "w", encoding="utf-8") as stream:
            json.dump(relabelled, stream)
        trust_anchor.clear_owner_trust_anchor()
        saved = os.environ.get(trust_anchor.ANCHOR_PATH_ENV)
        os.environ[trust_anchor.ANCHOR_PATH_ENV] = path
        try:
            with self.assertRaisesRegex(
                    trust_anchor.TrustAnchorError,
                    trust_anchor.PRODUCTION_VERIFIER_CONTEXT_FIXTURE_KEY_MATERIAL):
                trust_anchor.resolve_production_verifier_context(
                    trust_anchor.AUTHORITY_MEASUREMENT)
        finally:
            if saved is None:
                os.environ.pop(trust_anchor.ANCHOR_PATH_ENV, None)
            else:
                os.environ[trust_anchor.ANCHOR_PATH_ENV] = saved
        # (d) CONTROL — the legitimate path is untouched. The production-shaped TEST
        #     anchor's pair is generated IN MEMORY per run, is not committed material,
        #     builds a context and admits the grid.
        production = ceremony.test_production_anchor_document()
        self.assertNotIn(trust_anchor.public_key_identity(production["public_key_pem"]),
                         material)
        ceremony.configure_test_production_anchor()
        self.assertEqual(admit(simulated_production_grid()), [])
        # (e) CONTROL — the fixture LANE is untouched: refusing fixture KEY MATERIAL at
        #     the production root is not refusing fixture DOCUMENTS.
        roots = authority.validate_production_trust_root_manifest(
            committed_fixture_manifest())
        self.assertEqual({row["fixture_only"] for row in roots.values()}, {True})
        self.assertIs(trust_anchor.load_owner_trust_anchor(
            ceremony.FIXTURE_ANCHOR_PATH).fixture_only, True)

    def test_bw55_adversarial_re_encoded_committed_fixture_key_is_not_a_production_root(self):
        """Invariant (BUILD acceptance r4 seat finding, reproduced at the byte): key
        identity is a fact about the KEY BYTES, never about the text that carries them.

        RFC 4648 §3.5: where the non-significant trailing bits of the final base64
        character are not zeroed there is NO canonical representation, so several
        distinct strings decode to identical bytes. The committed anchor body ending
        `...DvZ8zY=` and the body ending `...DvZ8zZ=` decode to the SAME 44-byte SPKI —
        and while identity was the base64 TEXT, only the first was in the derived set,
        so the SAME committed key re-encoded by hand was ADMITTED as a production root
        through the documented `MBCX01_BUILD_OWNER_TRUST_ANCHOR` configuration door.
        That is the CWE-1291 seam the fixture-key fold exists to close, still open one
        text transformation away.

        The variants here are built from the DECODED key bytes, never from
        `public_key_identity`: a witness constructed out of the normalizer under test
        can only ever confirm that normalizer's own fixed points (the defect recorded
        against bw28's re-wrap sub-case). Two independent axes are covered — the base64
        TEXT (same DER, different string) and the DER ENVELOPE (same 32-byte Ed25519
        point, different SubjectPublicKeyInfo encoding)."""
        document = ceremony.fixture_owner_anchor_document()
        committed_der = _spki_der(document["public_key_pem"])
        material = trust_anchor.committed_fixture_key_material()
        committed_identity = trust_anchor.public_key_identity(document["public_key_pem"])
        self.assertEqual(material.get(committed_identity),
                         os.path.basename(ceremony.FIXTURE_ANCHOR_PATH))
        variants = {
            # (a) the base64 TEXT axis: one changed character, identical decoded bytes.
            "re-encoded base64 body": _pem_from_der_body(
                _non_canonical_base64_body(committed_der)),
            # (b) the DER ENVELOPE axis: the same Ed25519 public point wrapped in a
            #     long-form length. `openssl`/`node` never emit it; a hand edit can.
            "re-encoded SPKI envelope": _pem_from_der(
                _long_form_spki(committed_der)),
        }
        for label, variant_pem in variants.items():
            with self.subTest(variant=label):
                # THE DISCRIMINATOR, computed here from the bytes: a different carrier
                # string, carrying the same 32-byte public point as the committed key.
                self.assertNotEqual(variant_pem, document["public_key_pem"])
                self.assertEqual(_spki_der(variant_pem)[-32:], committed_der[-32:])
                # Identity is over the KEY, so every carrier of that key has ONE identity.
                self.assertEqual(trust_anchor.public_key_identity(variant_pem),
                                 committed_identity)
                relabelled = dict(document, fixture_only=False,
                                  anchor_id="MBCX01.RE.ENCODED.ANCHOR.1",
                                  public_key_pem=variant_pem)
                with self.assertRaisesRegex(
                        trust_anchor.TrustAnchorError,
                        trust_anchor.PRODUCTION_VERIFIER_CONTEXT_FIXTURE_KEY_MATERIAL):
                    trust_anchor.new_production_verifier_context(relabelled)
                # ... and through the OS configuration door an operator actually uses.
                directory = tempfile.mkdtemp(prefix="mbcx01-build-keyidentity-")
                self.addCleanup(shutil.rmtree, directory, True)
                path = os.path.join(directory, "owner-trust-anchor.json")
                with open(path, "w", encoding="utf-8") as stream:
                    json.dump(relabelled, stream)
                trust_anchor.clear_owner_trust_anchor()
                saved = os.environ.get(trust_anchor.ANCHOR_PATH_ENV)
                os.environ[trust_anchor.ANCHOR_PATH_ENV] = path
                try:
                    with self.assertRaisesRegex(
                            trust_anchor.TrustAnchorError,
                            trust_anchor.PRODUCTION_VERIFIER_CONTEXT_FIXTURE_KEY_MATERIAL):
                        trust_anchor.resolve_production_verifier_context(
                            trust_anchor.AUTHORITY_MEASUREMENT)
                finally:
                    if saved is None:
                        os.environ.pop(trust_anchor.ANCHOR_PATH_ENV, None)
                    else:
                        os.environ[trust_anchor.ANCHOR_PATH_ENV] = saved
        # (c) the ALPHABET axis (RFC 4648 §5), which needs a key whose canonical body
        #     actually contains `+` or `/` — for the committed ANCHOR key it does not, so
        #     base64url is the same string and would witness nothing. The committed
        #     measurement SIGNING key is such a key, and pasting it into an anchor
        #     document is the same operator hand edit: it is committed material whatever
        #     alphabet carries it, and the refusal names the document it is published in.
        signing_pem = committed_fixture_manifest()["roots"][0]["public_key_pem"]
        signing_der = _spki_der(signing_pem)
        url_body = base64.urlsafe_b64encode(signing_der).decode("ascii")
        self.assertNotEqual(url_body, base64.b64encode(signing_der).decode("ascii"))
        url_pem = _pem_from_der_body(url_body)
        self.assertEqual(trust_anchor.public_key_identity(url_pem),
                         trust_anchor.public_key_identity(signing_pem))
        with self.assertRaisesRegex(
                trust_anchor.TrustAnchorError,
                trust_anchor.PRODUCTION_VERIFIER_CONTEXT_FIXTURE_KEY_MATERIAL):
            trust_anchor.new_production_verifier_context(
                dict(document, fixture_only=False,
                     anchor_id="MBCX01.RE.ENCODED.ANCHOR.2", public_key_pem=url_pem))
        # CONTROL — a key that is in no committed document keeps ONE identity across the
        # same two transformations, and still builds a production context.
        production = ceremony.test_production_anchor_document()
        production_der = _spki_der(production["public_key_pem"])
        production_identity = trust_anchor.public_key_identity(
            production["public_key_pem"])
        self.assertNotIn(production_identity, material)
        self.assertEqual(
            trust_anchor.public_key_identity(_pem_from_der(production_der)),
            production_identity)
        ceremony.configure_test_production_anchor()
        self.assertEqual(admit(simulated_production_grid()), [])

    def test_bw56_adversarial_non_canonical_public_key_carrier_is_refused_at_the_context(self):
        """Invariant: one production root key has exactly ONE accepted carrier.

        This is `strict_signature_carrier_ok` (`mbcx01_build_trust_anchor.py`) applied one
        field away, to the anchor's `public_key_pem`: grammar, padding, length, and a
        decode/re-encode equality check, plus the canonical RFC 8410 §4 Ed25519
        SubjectPublicKeyInfo encoding. Without it the operator configuration boundary
        accepts many strings for one key, so a document's key has no single identity for
        review, diff or audit — the same defect class the signature carrier closed, on the
        field that names the root of trust itself."""
        _private, public_pem = ceremony._generate_ed25519_keypair()
        der = _spki_der(public_pem)
        self.assertTrue(trust_anchor.strict_public_key_carrier_ok(_pem_from_der(der)))
        for label, carrier in (
                ("non-canonical base64 tail",
                 _pem_from_der_body(_non_canonical_base64_body(der))),
                ("long-form SPKI length", _pem_from_der(_long_form_spki(der))),
                ("line-wrapped body", "-----BEGIN PUBLIC KEY-----\n"
                 + "\n".join(base64.b64encode(der).decode("ascii")[i:i + 32]
                             for i in range(0, 60, 32))
                 + "\n-----END PUBLIC KEY-----\n")):
            with self.subTest(carrier=label):
                self.assertFalse(trust_anchor.strict_public_key_carrier_ok(carrier))
                anchor = ceremony.owner_anchor_document(
                    anchor_id="MBCX01.CARRIER.ANCHOR.1", public_key_pem=carrier,
                    fixture_only=False)
                with self.assertRaisesRegex(
                        trust_anchor.TrustAnchorError,
                        trust_anchor.PRODUCTION_VERIFIER_CONTEXT_KEY_CARRIER_INVALID):
                    trust_anchor.new_production_verifier_context(anchor)
        # CONTROL — the canonical carrier the ceremony actually produces still wires.
        trust_anchor.new_production_verifier_context(ceremony.owner_anchor_document(
            anchor_id="MBCX01.CARRIER.ANCHOR.2", public_key_pem=public_pem,
            fixture_only=False))
        ceremony.configure_test_production_anchor()

    def test_bw57_adversarial_committed_test_signing_key_is_not_production_signing_material(self):
        """Invariant (BUILD acceptance r4 seat finding, EXECUTED): the committed-key
        refusal covers the SIGNING key class, not only the anchor class.

        A council seat took the Ed25519 test signing pair committed in this file, made it
        the PRODUCTION measurement signing root under an independently generated owner
        anchor — so this is not the anchor class already closed — and cleared production
        admission: `production_admission_errors = []`, `root_fixture_only = False`,
        `production_ready = True`, `root_is_committed_test_public = True`, with custody
        documents asserting the private key never left custody. The ceremony forbids
        exactly this (`MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md` §3 step 0 and step 3: every
        key in the manifest must be generated in the ceremony, never copied out of a
        committed fixture document) — but prose is not a control.

        The refusal is at every production door, by name, over the set DERIVED from the
        committed documents; the FIXTURE lane is untouched, because refusing fixture KEY
        MATERIAL at a production root is not refusing fixture DOCUMENTS."""
        ceremony.configure_test_production_anchor()
        # The committed test signing key: its private half is in this file and its public
        # half is published in the committed fixture manifest.
        self.assertEqual(
            trust_anchor.public_key_identity(
                committed_fixture_manifest()["roots"][0]["public_key_pem"]),
            trust_anchor.public_key_identity(COMMITTED_TEST_SIGNING_PUBLIC_KEY_PEM))
        manifest = simulated_production_manifest(
            root_overrides={"public_key_pem": COMMITTED_TEST_SIGNING_PUBLIC_KEY_PEM})
        self.assertIs(manifest["production_ready"], True)
        self.assertIs(manifest["roots"][0]["fixture_only"], False)
        custody = simulated_custody_evidence(manifest)
        grid = simulated_production_grid(
            signer=producer.FixtureSigner(SIMULATED_KEY_ID,
                                          COMMITTED_TEST_SIGNING_PRIVATE_KEY_PEM))
        errors = admit(grid, manifest=manifest, custody=custody)
        self.assertIn(authority.PRODUCTION_SIGNING_KEY_FIXTURE_MATERIAL, errors)
        self.assertIn("PHYSICAL_HARNESS_UNAVAILABLE", errors)
        self.assertTrue(set(errors) <= authority.PRODUCTION_ERROR_CODES, errors)
        # The exactness door is the third door and takes the same refusal.
        with self.assertRaisesRegex(authority.MeasurementAuthorityError,
                                    authority.PRODUCTION_SIGNING_KEY_FIXTURE_MATERIAL):
            exactness.verify_production_carrier_exactness(
                {"schema_id": exactness.EXACTNESS_RECEIPT_SCHEMA_ID}, envelopes=grid,
                suite_document=exactness._pinned_suite()[0],
                trust_root_manifest=manifest, custody_evidence=custody)
        # CONTROL — the same admission over a signing key generated IN MEMORY for this
        # run, which is in no committed document, is green.
        self.assertEqual(admit(simulated_production_grid()), [])
        # CONTROL — the fixture LANE is untouched: the committed manifest still parses
        # and still resolves its fixture-only root.
        roots = authority.validate_production_trust_root_manifest(
            committed_fixture_manifest())
        self.assertEqual({row["fixture_only"] for row in roots.values()}, {True})

    # --- AMENDMENT-2: the carrier is the KEY, not the operator's line endings -

    def test_bw61_positive_rfc7468_eol_conventions_are_one_carrier(self):
        """A real operator export must not be refused for spelling its newlines.

        RFC 7468 §2 tells parsers to handle the differing newline conventions
        (CRLF, CR, LF) and the §3 ABNF makes the EOL after the final
        `-----END PUBLIC KEY-----` OPTIONAL. CRLF is the NATIVE Windows line
        ending, so the ceremony's own `openssl`/`node` export on the operator's
        box is a CRLF document — and the anchor door required literal LF plus a
        final EOL, which refuses RIGHT evidence and blocks the ceremony with a
        message about a malformed key that is not malformed at all.

        The key is generated FRESH here (it is in no committed document), so
        the committed-material refusal is not what is being measured.
        """
        _private, public_pem = ceremony._generate_ed25519_keypair()
        self.assertTrue(public_pem.endswith("-----END PUBLIC KEY-----\n"))
        identity = trust_anchor.public_key_identity(public_pem)
        spellings = (
            ("LF, final EOL present", public_pem),
            ("CRLF, final EOL present", public_pem.replace("\n", "\r\n")),
            ("CR, final EOL present", public_pem.replace("\n", "\r")),
            ("LF, final EOL absent", public_pem.rstrip("\n")),
            ("CRLF, final EOL absent",
             public_pem.replace("\n", "\r\n").rstrip("\r\n")),
        )
        for label, carrier in spellings:
            with self.subTest(carrier=label):
                # one key: the transport spelling never changes the identity
                self.assertEqual(trust_anchor.public_key_identity(carrier), identity)
                self.assertTrue(trust_anchor.strict_public_key_carrier_ok(carrier))
                anchor = trust_anchor.OwnerTrustAnchor(
                    anchor_id="MBCX01.EOL.ANCHOR.1", algorithm="ED25519",
                    public_key_pem=carrier,
                    authorities=[trust_anchor.AUTHORITY_MEASUREMENT],
                    minimum_activation_generation=1, fixture_only=False)
                # the anchor holds the NORMALISED carrier, so every downstream
                # comparison sees one text for one key
                self.assertEqual(anchor.public_key_pem, public_pem)
                trust_anchor.new_production_verifier_context(
                    ceremony.owner_anchor_document(
                        anchor_id="MBCX01.EOL.ANCHOR.2", public_key_pem=carrier,
                        fixture_only=False))
        ceremony.configure_test_production_anchor()

    def test_bw62_adversarial_eol_normalisation_weakens_no_other_carrier_check(self):
        """Normalising the TRANSPORT spelling must change nothing else.

        The outer text convention is the only thing RFC 7468 makes optional. A
        re-spelling must not launder COMMITTED key material into an unknown key
        (AB-09's invariant), and it must not smuggle a non-canonical body or a
        non-canonical SPKI past the carrier check — so every refusal bw55/bw56
        establish is re-run here through CRLF and through a missing final EOL.
        """
        committed_pem = committed_fixture_manifest()["roots"][0]["public_key_pem"]
        document = ceremony.fixture_owner_anchor_document()
        for label, carrier in (
                ("CRLF", committed_pem.replace("\n", "\r\n")),
                ("no final EOL", committed_pem.rstrip("\n"))):
            with self.subTest(committed=label):
                self.assertEqual(trust_anchor.committed_fixture_key_document(carrier),
                                 FIXTURE_MANIFEST_PATH)
                with self.assertRaisesRegex(
                        trust_anchor.TrustAnchorError,
                        trust_anchor.PRODUCTION_VERIFIER_CONTEXT_FIXTURE_KEY_MATERIAL):
                    trust_anchor.new_production_verifier_context(
                        dict(document, fixture_only=False,
                             anchor_id="MBCX01.EOL.COMMITTED.1",
                             public_key_pem=carrier))
        # The ALPHABET axis needs a key whose canonical body actually contains
        # `+` or `/` — bw55 makes the same point: for a body without them,
        # base64url is the SAME string and would witness nothing.
        while True:
            _private, public_pem = ceremony._generate_ed25519_keypair()
            der = _spki_der(public_pem)
            body = base64.b64encode(der).decode("ascii")
            if base64.urlsafe_b64encode(der).decode("ascii") != body:
                break
        mutants = (
            ("non-canonical base64 tail",
             _pem_from_der_body(_non_canonical_base64_body(der))),
            ("long-form SPKI length", _pem_from_der(_long_form_spki(der))),
            ("line-wrapped body", _pem_from_der_body(
                "\n".join(body[i:i + 32] for i in range(0, len(body), 32)))),
            ("whitespace inside the body",
             _pem_from_der_body(body[:8] + " " + body[8:])),
            ("base64url alphabet", _pem_from_der_body(
                base64.urlsafe_b64encode(der).decode("ascii"))),
        )
        for label, mutant in mutants:
            for spelling, carrier in (("CRLF", mutant.replace("\n", "\r\n")),
                                      ("no final EOL", mutant.rstrip("\n")),
                                      ("LF", mutant)):
                with self.subTest(mutant=label, spelling=spelling):
                    self.assertFalse(
                        trust_anchor.strict_public_key_carrier_ok(carrier))
                    with self.assertRaisesRegex(
                            trust_anchor.TrustAnchorError,
                            trust_anchor.PRODUCTION_VERIFIER_CONTEXT_KEY_CARRIER_INVALID):
                        trust_anchor.new_production_verifier_context(
                            ceremony.owner_anchor_document(
                                anchor_id="MBCX01.EOL.CARRIER.1",
                                public_key_pem=carrier, fixture_only=False))
        # A carrier whose framing is broken is still not a carrier at all.
        for broken in ("-----BEGIN PUBLIC KEY-----\n" + body,
                       body + "\n-----END PUBLIC KEY-----\n",
                       "-----BEGIN PUBLIC KEY-----\r" + body
                       + "\r-----END PUBLIC KEY-----extra"):
            self.assertFalse(trust_anchor.strict_public_key_carrier_ok(broken))
        ceremony.configure_test_production_anchor()


def _etw():
    """Import the ETW consumer lazily.

    Lazy so that a MISSING consumer reds exactly the ETW witnesses and leaves
    the other 55 BUILD B witnesses passing — a discriminating red, not a
    collection-time blast radius.
    """
    import mbcx01_build_etw_consumer as module
    return module


#: The ONLY primary source on this machine for the ETW ordinals Learn names but
#: never numbers. Read at witness time so a pin can never drift away from the
#: header the operator's smoke run will actually be compiled against.
SDK_EVNTCONS_HEADERS = (
    r"C:\Program Files (x86)\Windows Kits\10\Include\*\um\evntcons.h")


class _FakeTraceApi:
    """A stand-in for the advapi32 trace entry points. Touches NO ETW state.

    `EtwPmcConsumer.stop()`/`capture()` are teardown LOGIC — what is checked,
    in what order, and which counters are carried — and that logic is exactly
    what a live-only method hides. Every call is RECORDED, so "the loss
    counters were queried a second time after the session was stopped" is an
    observed call rather than an inference, and the queried values are
    scripted per call so a second query cannot return the first one's numbers
    by accident.

    ⛔ Nothing here starts, opens, controls or closes a real trace session.
    """

    def __init__(self, *, close_trace_status=0, query_events_lost=(0,)):
        self.calls: list[tuple] = []
        self.close_trace_status = int(close_trace_status)
        self._query_events_lost = list(query_events_lost)

    @property
    def query_count(self) -> int:
        return sum(1 for call in self.calls
                   if call[0] == "ControlTraceW" and call[2] == 0)

    def CloseTrace(self, handle):  # noqa: N802 - the Win32 spelling
        self.calls.append(("CloseTrace", int(handle.value)))
        return self.close_trace_status

    def ControlTraceW(self, handle, name, block, code):  # noqa: N802
        self.calls.append(("ControlTraceW", int(handle.value), int(code)))
        if int(code) == 0:  # EVENT_TRACE_CONTROL_QUERY
            index = min(self.query_count - 1, len(self._query_events_lost) - 1)
            block._obj.Props.EventsLost = self._query_events_lost[index]
        return 0


#: The event VERSION each synthetic record claims when the caller does not say.
#: These are the versions whose templates `KERNEL_PROCESS_PAYLOAD_LAYOUTS`
#: pins as carrying `ProcessSequenceNumber`; the thread events are
#: version-independent for the two fields the decoder reads.
_DEFAULT_KERNEL_PROCESS_VERSIONS = {1: 4, 2: 2, 3: 1, 4: 1}


def _wide(text):
    return text.encode("utf-16-le") + b"\x00\x00"


def _process_start_payload(process_id, start_key, *, parent_process_id=0,
                           parent_start_key=0):
    """A ProcessStart payload with the manifest's VERSION 4 field order.

    From this box's own Microsoft-Windows-Kernel-Process manifest, read back
    through TDH and pinned in `KERNEL_PROCESS_PAYLOAD_LAYOUTS`: ProcessID u32,
    ProcessSequenceNumber u64, CreateTime FILETIME, ParentProcessID u32,
    ParentProcessSequenceNumber u64, SessionID u32, Flags u32,
    ProcessTokenElevationType u32, ProcessTokenIsElevated u32, MandatoryLabel
    SID, ImageName, ImageChecksum u32, TimeDateStamp u32, PackageFullName,
    PackageRelativeAppId, SecurityMitigations u32. The tail is built out too,
    not just the prefix the decoder reads, so a witness cannot pass because the
    payload happened to end where the decoder stopped looking.
    """
    return (struct.pack("<IQQIQIIII", int(process_id), int(start_key),
                        133_000_000_000_000_000, int(parent_process_id),
                        int(parent_start_key), 1, 0, 1, 0)
            + struct.pack("<BB6sI", 1, 1, b"\x00\x00\x00\x00\x00\x10", 8192)
            + _wide("candidate.exe")
            + struct.pack("<II", 0xABCD1234, 0x66000000)
            + _wide("") + _wide("")
            + struct.pack("<I", 0))


def _process_stop_payload(process_id, start_key):
    """A ProcessStop payload with the manifest's VERSION 2 field order.

    ProcessID u32, ProcessSequenceNumber u64, CreateTime, ExitTime, ExitCode
    u32, TokenElevationType u32, HandleCount u32, CommitCharge u64, CommitPeak
    u64, CPUCycleCount u64, ReadOperationCount u32, WriteOperationCount u32,
    ReadTransferKiloBytes u32, WriteTransferKiloBytes u32, HardFaultCount u32,
    ImageName ansi.
    """
    return (struct.pack("<IQQQIIIQQQIIIII", int(process_id), int(start_key),
                        133_000_000_000_000_000, 133_000_000_000_100_000,
                        0, 1, 12, 4096, 8192, 1_000_000, 1, 2, 3, 4, 5)
            + b"candidate.exe\x00")


def _kernel_process_record(etw, *, event_id, payload, logging_process_id=0,
                           timestamp=0, version=None):
    """One synthetic Microsoft-Windows-Kernel-Process EVENT_RECORD.

    Built out of the module's OWN ctypes structures and handed to the REAL
    `_on_event_record` callback, so the decode path under test is the physical
    one — only the record's origin is synthetic. The payload buffer is returned
    with the record because `UserData` is a raw pointer into it.

    `version` fills `EventHeader.EventDescriptor.Version`, which the decoder
    reads to choose the payload template; it defaults to the version whose
    template matches the payload builders above.
    """
    record = etw.EVENT_RECORD()
    record.EventHeader.ProviderId = etw.GUID.from_le_bytes(
        etw.KERNEL_PROCESS_PROVIDER_GUID_BYTES)
    record.EventHeader.EventDescriptor.Id = int(event_id)
    record.EventHeader.EventDescriptor.Version = int(
        _DEFAULT_KERNEL_PROCESS_VERSIONS.get(int(event_id), 0)
        if version is None else version)
    record.EventHeader.ProcessId = int(logging_process_id)
    record.EventHeader.TimeStamp = int(timestamp)
    buffer = ctypes.create_string_buffer(payload, len(payload))
    record.UserData = ctypes.cast(buffer, ctypes.c_void_p)
    record.UserDataLength = len(payload)
    return record, buffer


def _classic_cswitch_record(etw, *, flags, processor, qpc, new_thread_id,
                            old_thread_id, counters):
    """One synthetic classic (MOF) CSwitch EVENT_RECORD carrying PMC counters.

    The MOF published on the CSwitch page puts NewThreadId at payload offset 0
    and OldThreadId at offset 4, which is what `_cswitch_old_thread_id()` reads.
    `flags` is the caller's business: this is the witness that shows what the
    EVENT_HEADER.Flags gate DECIDES. The payload and counter buffers are
    returned because the record holds raw pointers into them.
    """
    record = etw.EVENT_RECORD()
    record.EventHeader.ProviderId = etw.GUID.from_le_bytes(etw.THREAD_GUID_BYTES)
    record.EventHeader.Flags = int(flags)
    record.EventHeader.EventDescriptor.Opcode = etw.CSWITCH_EVENT_TYPE
    record.EventHeader.TimeStamp = int(qpc)
    record.BufferContext.ProcessorIndex = int(processor)
    payload = struct.pack("<II", int(new_thread_id), int(old_thread_id))
    payload_buffer = ctypes.create_string_buffer(payload, len(payload))
    record.UserData = ctypes.cast(payload_buffer, ctypes.c_void_p)
    record.UserDataLength = len(payload)
    blob = struct.pack("<%dQ" % len(counters), *counters)
    counter_buffer = ctypes.create_string_buffer(blob, len(blob))
    items = (etw.EVENT_HEADER_EXTENDED_DATA_ITEM * 1)()
    items[0].ExtType = etw.EVENT_HEADER_EXT_TYPE_PMC_COUNTERS
    items[0].DataSize = len(blob)
    items[0].DataPtr = ctypes.cast(counter_buffer, ctypes.c_void_p).value
    record.ExtendedDataCount = 1
    record.ExtendedData = ctypes.cast(
        items, ctypes.POINTER(etw.EVENT_HEADER_EXTENDED_DATA_ITEM))
    return record, (payload_buffer, counter_buffer, items)


class BuildEtwConsumerTests(unittest.TestCase):
    """bw29-bw53: the real ETW PMC consumer — the seam `collect()` requires.

    `mbcx01_build_win32.collect()` takes `etw_session_factory: Callable[[],
    EtwPmcSession]` and NOTHING in the lane supplied one, so the reviewed
    collector was unrunnable (MBCX-01-OPEN-ISSUES.json
    MBCX01-BUILD-B-ETW-CONSUMER-UNBUILT). These witnesses exercise the parts of
    the consumer that can be exercised WITHOUT an ETW session: the pinned Win32
    ABI, the pure ordering/join/lifetime logic against synthetic records, and
    the UNAVAILABLE-not-a-number posture. NOTHING here starts a trace session,
    opens a PMU, sets MBCX01_BUILD_ALLOW_PHYSICAL or calls `collect()`.
    """

    # --- static ABI ---------------------------------------------------------

    def test_bw29_positive_etw_struct_layout_matches_the_pinned_win32_abi(self):
        """Every ETW structure size/offset is re-derived from ctypes and pinned.

        A wrong offset must fail at verify time, not at 3am on the operator's
        box, so the check runs the same way `verify_struct_layout()` does for
        the Job ABI.
        """
        etw = _etw()
        derived = etw.verify_etw_struct_layout()
        self.assertEqual(derived["event_trace_properties_size"], 120)
        self.assertEqual(derived["wnode_header_size"], 48)
        self.assertEqual(derived["event_record_size"], 112)
        self.assertEqual(derived["event_header_size"], 80)
        self.assertEqual(derived["etw_buffer_context_size"], 4)
        self.assertEqual(derived["extended_data_item_size"], 16)
        self.assertEqual(derived["event_trace_logfile_size"], 448)
        self.assertEqual(derived["classic_event_id_size"], 24)
        self.assertEqual(derived["logger_name_offset_field"], 116)
        self.assertEqual(derived["log_file_name_offset_field"], 112)
        self.assertEqual(derived["wnode_flags_offset"], 44)
        self.assertEqual(derived["events_lost_offset"], 88)
        self.assertEqual(derived["log_buffers_lost_offset"], 96)
        self.assertEqual(derived["realtime_buffers_lost_offset"], 100)
        self.assertEqual(etw.WNODE_FLAG_TRACED_GUID, 0x00020000)
        # The two PMC classes the collector already names, re-derived here from
        # the SAME primary source (TRACE_QUERY_INFO_CLASS) so a drift between
        # the two modules is a hard failure.
        self.assertEqual(etw.TracePmcEventListInfo, 8)
        self.assertEqual(etw.TracePmcCounterListInfo, 9)
        self.assertEqual(etw.TracePmcEventListInfo, win32.TracePmcEventListInfo)
        self.assertEqual(etw.TracePmcCounterListInfo, win32.TracePmcCounterListInfo)

    def test_bw30_adversarial_etw_abi_drift_is_a_fault_at_verify_time(self):
        """A pinned size that no longer matches the structure fails loudly."""
        etw = _etw()
        saved = etw.EVENT_TRACE_PROPERTIES_SIZE
        try:
            etw.EVENT_TRACE_PROPERTIES_SIZE = saved + 8
            with self.assertRaises(etw.EtwConsumerFault) as caught:
                etw.verify_etw_struct_layout()
            self.assertIn("ETW_ABI_DRIFT", str(caught.exception))
        finally:
            etw.EVENT_TRACE_PROPERTIES_SIZE = saved
        self.assertEqual(etw.verify_etw_struct_layout()["event_trace_properties_size"], saved)

    # --- ordering -----------------------------------------------------------

    def test_bw31_positive_records_are_emitted_in_per_processor_timestamp_order(self):
        """Real-time buffers interleave across processors; the emitted stream does not.

        The collector recomputes each delta from consecutive values on the SAME
        processor, so the consumer owes it a per-processor timestamp order and
        must SAY how much reordering the raw capture needed.
        """
        etw = _etw()
        captured = [
            {"processor": 1, "qpc": 50, "old_thread_id": 7, "instruction_retired": 500},
            {"processor": 0, "qpc": 10, "old_thread_id": 5, "instruction_retired": 100},
            {"processor": 1, "qpc": 40, "old_thread_id": 7, "instruction_retired": 400},
            {"processor": 0, "qpc": 20, "old_thread_id": 5, "instruction_retired": 180},
        ]
        ordered, reordered = etw.order_records_per_processor(captured)
        self.assertEqual([(row["processor"], row["qpc"]) for row in ordered],
                         [(0, 10), (0, 20), (1, 40), (1, 50)])
        self.assertGreater(reordered, 0)
        # Already-ordered input is reported as needing NO reordering.
        again, zero = etw.order_records_per_processor(ordered)
        self.assertEqual([(r["processor"], r["qpc"]) for r in again],
                         [(0, 10), (0, 20), (1, 40), (1, 50)])
        self.assertEqual(zero, 0)

    def test_bw32_adversarial_a_record_missing_a_join_field_is_refused(self):
        """A record the consumer cannot order or attribute is a fault, not a skip."""
        etw = _etw()
        for missing in ("processor", "qpc", "old_thread_id", "instruction_retired"):
            record = {"processor": 0, "qpc": 1, "old_thread_id": 3,
                      "instruction_retired": 9}
            record.pop(missing)
            with self.assertRaises(etw.EtwConsumerFault) as caught:
                etw.order_records_per_processor([record])
            self.assertIn("ETW_CSWITCH_RECORD_INCOMPLETE", str(caught.exception))

    # --- the PMC join -------------------------------------------------------

    def test_bw33_positive_pmc_counters_are_read_from_the_pinned_extended_item(self):
        """InstructionRetired comes from EVENT_HEADER_EXT_TYPE_PMC_COUNTERS.

        The payload is an array of ULONG64 in the order of the counter list the
        session pinned, so the pinned index selects InstructionRetired.
        """
        etw = _etw()
        payload = struct.pack("<QQ", 111, 222)
        items = [(etw.EVENT_HEADER_EXT_TYPE_STACK_TRACE64, b"\x00" * 8),
                 (etw.EVENT_HEADER_EXT_TYPE_PMC_COUNTERS, payload)]
        counters = etw.pmc_counters_from_extended_data(items)
        self.assertEqual(counters, (111, 222))
        self.assertEqual(etw.select_pinned_counter(counters, 0), 111)
        self.assertEqual(etw.select_pinned_counter(counters, 1), 222)

    def test_bw34_adversarial_absent_or_short_pmc_data_is_unavailable_not_zero(self):
        """No counter is never counter==0: an absent PMC item is a fault."""
        etw = _etw()
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            etw.pmc_counters_from_extended_data(
                [(etw.EVENT_HEADER_EXT_TYPE_SID, b"\x01" * 12)])
        self.assertIn("ETW_PMC_EXTENDED_DATA_ABSENT", str(caught.exception))
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            etw.pmc_counters_from_extended_data(
                [(etw.EVENT_HEADER_EXT_TYPE_PMC_COUNTERS, b"\x01\x02\x03")])
        self.assertIn("ETW_PMC_EXTENDED_DATA_MALFORMED", str(caught.exception))
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            etw.select_pinned_counter((111,), 1)
        self.assertIn("ETW_PMC_COUNTER_INDEX_UNAVAILABLE", str(caught.exception))

    # --- member lifetimes ---------------------------------------------------

    def test_bw35_positive_member_lifetimes_cover_every_member_including_terminated(self):
        """ProcessStart/ProcessStop is the only source that sees an unopened descendant.

        The assembled rows are the frozen `PROCESS_KEYS` shape, carry PID plus
        the 64-bit start key, and include a descendant the collector never held
        a handle to.
        """
        etw = _etw()
        events = [
            {"kind": "START", "process_id": 4100, "process_start_key": 0x11,
             "parent_process_id": None, "parent_process_start_key": None, "qpc": 10},
            {"kind": "START", "process_id": 4200, "process_start_key": 0x22,
             "parent_process_id": 4100, "parent_process_start_key": 0x11, "qpc": 12},
            {"kind": "STOP", "process_id": 4200, "process_start_key": 0x22, "qpc": 28},
            {"kind": "STOP", "process_id": 4100, "process_start_key": 0x11, "qpc": 30},
        ]
        rows = etw.assemble_member_lifetimes(
            events, job_object_id="JOB.0.0.0", root_process_id=4100,
            root_process_start_key="0000000000000011")
        self.assertEqual(len(rows), 2)
        for row in rows:
            self.assertEqual(set(row), measurement.PROCESS_KEYS)
            self.assertRegex(row["process_start_key"], r"^[0-9A-F]{16}$")
            self.assertLess(row["started_qpc"], row["ended_qpc"])
            self.assertEqual(row["job_object_id"], "JOB.0.0.0")
            self.assertIs(row["assigned_before_resume"], True)
            self.assertEqual(row["terminal_status"], "EXITED")
        descendant = [row for row in rows if row["process_id"] == 4200][0]
        self.assertEqual(descendant["parent_process_id"], 4100)
        self.assertEqual(descendant["parent_process_start_key"], "0000000000000011")

    def test_bw36_adversarial_an_unterminated_or_keyless_member_is_refused(self):
        """A member without a terminal, or without a start key, cannot be signed."""
        etw = _etw()
        base = [{"kind": "START", "process_id": 4100, "process_start_key": 0x11,
                 "parent_process_id": None, "parent_process_start_key": None, "qpc": 10},
                {"kind": "STOP", "process_id": 4100, "process_start_key": 0x11, "qpc": 30}]

        def assemble(events):
            return etw.assemble_member_lifetimes(
                events, job_object_id="JOB.0.0.0", root_process_id=4100,
                root_process_start_key="0000000000000011")

        self.assertEqual(len(assemble(list(base))), 1)
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            assemble([base[0]])
        self.assertIn("ETW_PROCESS_LIFETIME_INCOMPLETE", str(caught.exception))
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            assemble([base[1]])
        self.assertIn("ETW_PROCESS_LIFETIME_UNMATCHED_STOP", str(caught.exception))
        keyless = copy.deepcopy(base)
        keyless[0]["process_start_key"] = 0
        keyless[1]["process_start_key"] = 0
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            assemble(keyless)
        self.assertIn("ETW_PROCESS_START_KEY_UNAVAILABLE", str(caught.exception))
        rootless = copy.deepcopy(base)
        for row in rootless:
            row["process_id"] = 9999
            row["process_start_key"] = 0x99
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            assemble(rootless)
        self.assertIn("ETW_PROCESS_LIFETIME_ROOT_ABSENT", str(caught.exception))

    # --- availability posture ----------------------------------------------

    def test_bw37_adversarial_any_nonzero_loss_counter_makes_evidence_unavailable(self):
        """EventsLost / LogBuffersLost / RealTimeBuffersLost are each fatal alone."""
        etw = _etw()
        facts = etw.granted_capability_facts_for_test()
        available, reasons = etw.evaluate_evidence_availability(
            capability_facts=facts, loss=etw.LossCounters(0, 0, 0))
        self.assertTrue(available)
        self.assertEqual(reasons, ())
        for field, reason in (("events_lost", "ETW_EVENTS_LOST"),
                              ("log_buffers_lost", "ETW_LOG_BUFFERS_LOST"),
                              ("realtime_buffers_lost", "ETW_REALTIME_BUFFERS_LOST")):
            loss = etw.LossCounters(**{field: 1})
            available, reasons = etw.evaluate_evidence_availability(
                capability_facts=facts, loss=loss)
            self.assertFalse(available)
            self.assertIn(reason, reasons)
            with self.assertRaises(etw.EtwConsumerFault) as caught:
                etw.require_available_evidence(capability_facts=facts, loss=loss)
            self.assertIn("ETW_EVIDENCE_UNAVAILABLE", str(caught.exception))
            self.assertIn(reason, str(caught.exception))

    def test_bw38_adversarial_ungranted_capability_is_unavailable_never_estimated(self):
        """An unavailable source, an owner conflict or no counters is UNAVAILABLE.

        Never a diagnostic success and never an estimated instruction count —
        the posture the `EtwPmcSession` docstring states.
        """
        etw = _etw()
        for change, reason in (
                ({"pmc_source_available": False}, "ETW_PMC_SOURCE_UNAVAILABLE"),
                ({"counter_owner_conflict_count": 1}, "ETW_PMC_COUNTER_OWNER_CONFLICT"),
                ({"max_pmc_counters": 0}, "ETW_PMC_NO_COUNTERS_GRANTED"),
                ({"attribution_complete": False}, "ETW_ATTRIBUTION_INCOMPLETE")):
            facts = etw.granted_capability_facts_for_test(**change)
            available, reasons = etw.evaluate_evidence_availability(
                capability_facts=facts, loss=etw.LossCounters(0, 0, 0))
            self.assertFalse(available)
            self.assertIn(reason, reasons)

    def test_bw39_adversarial_multiplexed_counters_are_unavailable(self):
        """Multiplexing means the counter did not run for the whole interval."""
        etw = _etw()
        facts = etw.granted_capability_facts_for_test(multiplexing_detected=True)
        available, reasons = etw.evaluate_evidence_availability(
            capability_facts=facts, loss=etw.LossCounters(0, 0, 0))
        self.assertFalse(available)
        self.assertIn("ETW_PMC_MULTIPLEXING_DETECTED", reasons)

    # --- environment gate ---------------------------------------------------

    def test_bw40_adversarial_a_virtualization_guest_or_nested_host_aborts(self):
        """Root partition or bare metal only; a guest needs a signed PMU receipt."""
        etw = _etw()
        native = etw.classify_execution_environment(
            hypervisor_present=True, is_root_partition=True,
            nested_virtualization=False, host_architecture="WINDOWS_64BIT")
        self.assertEqual(set(native), measurement.ENVIRONMENT_KEYS)
        self.assertEqual(native["execution_environment"], "HYPER_V_ROOT_PARTITION")
        self.assertEqual(native["guest_pmu_exposure"], "NOT_APPLICABLE")
        self.assertIsNone(native["guest_pmu_capability_receipt_digest"])
        bare = etw.classify_execution_environment(
            hypervisor_present=False, is_root_partition=False,
            nested_virtualization=False, host_architecture="WINDOWS_64BIT")
        self.assertEqual(bare["execution_environment"], "BARE_METAL_WINDOWS")
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            etw.classify_execution_environment(
                hypervisor_present=True, is_root_partition=False,
                nested_virtualization=False, host_architecture="WINDOWS_64BIT")
        self.assertIn("SMOKE_ENVIRONMENT_IS_A_VIRTUALIZATION_GUEST", str(caught.exception))
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            etw.classify_execution_environment(
                hypervisor_present=True, is_root_partition=True,
                nested_virtualization=True, host_architecture="WINDOWS_64BIT")
        self.assertIn("SMOKE_ENVIRONMENT_IS_NESTED", str(caught.exception))
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            etw.classify_execution_environment(
                hypervisor_present=False, is_root_partition=False,
                nested_virtualization=False, host_architecture="WINDOWS_32BIT")
        self.assertIn("SMOKE_ENVIRONMENT_ARCHITECTURE_UNSUPPORTED", str(caught.exception))

    # --- the seam collect() consumes ---------------------------------------

    def test_bw41_positive_the_factory_yields_a_contract_shaped_etwpmcsession(self):
        """`etw_session_factory()` must return exactly what `collect()` consumes.

        Built from captured records only — no session is opened here. The
        capability/attachment records are the frozen evidence shapes, and the
        joined observations pass the frozen validator's own delta rule.
        """
        etw = _etw()
        capture = etw.CapturedTrace(
            cswitch_records=[
                {"processor": 0, "qpc": 12, "old_thread_id": 900,
                 "instruction_retired": 1_000},
                {"processor": 0, "qpc": 20, "old_thread_id": 900,
                 "instruction_retired": 1_700}],
            process_events=[
                {"kind": "START", "process_id": 4100, "process_start_key": 0x11,
                 "parent_process_id": None, "parent_process_start_key": None, "qpc": 10},
                {"kind": "STOP", "process_id": 4100, "process_start_key": 0x11, "qpc": 30}],
            thread_events=[
                {"kind": "START", "thread_id": 900, "process_id": 4100,
                 "process_start_key": 0x11, "qpc": 11},
                {"kind": "STOP", "thread_id": 900, "process_id": 4100,
                 "process_start_key": 0x11, "qpc": 29}],
            capability_facts=etw.granted_capability_facts_for_test(),
            loss=etw.LossCounters(0, 0, 0),
            session_handle=0x1234, source_id=3, counter_index=0)
        factory = etw.make_etw_session_factory(
            capture, job_object_id="JOB.0.0.0", root_process_id=4100,
            root_process_start_key="0000000000000011")
        session = factory()
        self.assertIsInstance(session, win32.EtwPmcSession)
        self.assertEqual(set(session.capability), measurement.CAPABILITY_QUERY_KEYS)
        self.assertEqual(session.capability["counter_information_class"],
                         "TracePmcCounterListInfo")
        self.assertEqual(session.capability["event_information_class"],
                         "TracePmcEventListInfo")
        self.assertEqual(session.capability["counter_width_bits"], 64)
        self.assertEqual(session.capability["source_id"], 3)
        self.assertEqual(session.attachment, {
            "counter_query_class": "TracePmcCounterListInfo",
            "event_query_class": "TracePmcEventListInfo",
            "profile_source": measurement.INSTRUCTION_SOURCE,
            "event_list": measurement.INSTRUCTION_EVENT_LIST,
            "attached": True})
        # The CSwitch attachment blob is the documented CLASSIC_EVENT_ID pair
        # (Thread class GUID + type 36), never a zero-filled placeholder.
        self.assertEqual(len(session.event_id_blob), 24)
        self.assertNotEqual(session.event_id_blob, b"\x00" * 24)
        self.assertEqual(session.event_id_blob[16], 36)
        # The lifetimes and the ordered observations satisfy the frozen rules.
        self.assertEqual(len(session.members()), 1)
        for row in session.thread_lifetimes:
            self.assertEqual(set(row), measurement.THREAD_LIFETIME_KEYS)
        observations = session.consume_cswitch()
        self.assertEqual(len(observations), 2)
        self.assertEqual([row["delta_from_previous"] for row in observations], [0, 700])
        for row in observations:
            self.assertEqual(set(row), measurement.CSWITCH_OBSERVATION_KEYS)
        self.assertEqual(sum(row["delta_from_previous"] for row in observations), 700)

    def test_bw42_adversarial_unattached_consumer_seams_stay_faults(self):
        """An unattached seam is a FAULT, never an empty result — unchanged."""
        etw = _etw()
        session = win32.EtwPmcSession(
            session_handle=0, capability={}, attachment={},
            observations=[], thread_lifetimes=[])
        with self.assertRaises(win32.CollectorFault) as caught:
            session.records()
        self.assertIn("ETW_CONSUMER_NOT_ATTACHED", str(caught.exception))
        with self.assertRaises(win32.CollectorFault) as caught:
            session.members()
        self.assertIn("ETW_PROCESS_LIFETIME_STREAM_NOT_ATTACHED", str(caught.exception))
        # And the two seams the consumer build ADDS fault the same way rather
        # than configuring the session with a zero-filled placeholder blob.
        with self.assertRaises(win32.CollectorFault) as caught:
            session.classic_event_id_blob()
        self.assertIn("ETW_EVENT_ATTACHMENT_BLOB_NOT_ATTACHED", str(caught.exception))
        with self.assertRaises(win32.CollectorFault) as caught:
            win32._trace_facts(session)
        self.assertIn("ETW_CAPABILITY_FACTS_NOT_ATTACHED", str(caught.exception))
        self.assertTrue(issubclass(etw.EtwConsumerFault, RuntimeError))

    # --- the two riders this build had to correct ---------------------------

    def test_bw43_positive_capability_evidence_and_capability_facts_are_separate(self):
        """RIDER RED: `_trace_facts` cannot read facts out of the evidence record.

        `collect()` copies `dict(session.capability)` straight into
        `trace_capability_query`, which the frozen validator requires to equal
        EXACTLY `CAPABILITY_QUERY_KEYS` (five keys). `_trace_facts` used to
        `.get()` `pmc_source_available`/`max_pmc_counters`/
        `counter_owner_conflict_count`/`multiplexing_detected`/
        `attribution_complete` out of that SAME dict, so a real run could only
        produce a self-contradicting receipt: summed PMC deltas alongside
        `etw_pmc_source_available: False`. The granted facts live in their own
        attached record.
        """
        etw = _etw()
        capability = {"query_status_code": 0,
                      "counter_information_class": "TracePmcCounterListInfo",
                      "event_information_class": "TracePmcEventListInfo",
                      "source_id": 3, "counter_width_bits": 64}
        session = win32.EtwPmcSession(
            session_handle=1, capability=capability, attachment={},
            observations=[], thread_lifetimes=[],
            capability_facts=etw.granted_capability_facts_for_test(max_pmc_counters=4))
        facts = win32._trace_facts(session)
        self.assertEqual(set(session.capability), measurement.CAPABILITY_QUERY_KEYS)
        self.assertIs(facts["etw_pmc_source_available"], True)
        self.assertEqual(facts["etw_max_pmc_counters"], 4)
        self.assertEqual(facts["etw_counter_owner_conflict_count"], 0)
        self.assertIs(facts["etw_pmc_multiplexing_detected"], False)
        self.assertIs(facts["etw_attribution_complete"], True)
        self.assertIs(facts["etw_capability_query_succeeded"], True)
        self.assertEqual(set(facts), producer.TRACE_FACT_FIELDS)

    def test_bw44_adversarial_ungranted_facts_travel_into_the_receipt_unchanged(self):
        """An ungranted capability is RECORDED as ungranted, never repaired.

        The producer is a faithful recorder and the adapter is the judge, so an
        unavailable PMU must reach admission as a refusal, not be softened here.
        """
        etw = _etw()
        capability = {"query_status_code": 0,
                      "counter_information_class": "TracePmcCounterListInfo",
                      "event_information_class": "TracePmcEventListInfo",
                      "source_id": 3, "counter_width_bits": 64}
        session = win32.EtwPmcSession(
            session_handle=1, capability=capability, attachment={},
            observations=[], thread_lifetimes=[], events_lost=2,
            capability_facts=etw.granted_capability_facts_for_test(
                pmc_source_available=False, multiplexing_detected=True,
                counter_owner_conflict_count=3, attribution_complete=False))
        facts = win32._trace_facts(session)
        self.assertIs(facts["etw_pmc_source_available"], False)
        self.assertIs(facts["etw_pmc_multiplexing_detected"], True)
        self.assertEqual(facts["etw_counter_owner_conflict_count"], 3)
        self.assertIs(facts["etw_attribution_complete"], False)
        self.assertEqual(facts["etw_events_lost"], 2)
        # And a session carrying loss refuses to produce observations at all.
        session.record_stream = lambda: []
        with self.assertRaises(win32.CollectorFault) as caught:
            session.consume_cswitch()
        self.assertIn("ETW_EVENT_LOSS_DETECTED", str(caught.exception))
    # --- the terminal-barrier hook a LIVE session cannot exist without -------

    def test_bw45_positive_the_trace_window_closes_at_the_terminal_barrier(self):
        """`collect()` must close the trace window BEFORE it reads any delta.

        A LIVE `etw_session_factory()` is called before `ResumeThread`, so at
        that instant the candidate has not run and the signed roster it must
        carry does not exist yet. `consume_cswitch()` reads
        `self.thread_lifetimes` on its FIRST line, before it ever calls
        `records()`, so the roster has to be complete by then — and `collect()`
        offered no call site between the terminal barrier and consumption where
        a consumer could complete it. `close_trace_window()` is that call site.
        """
        etw = _etw()
        order = []
        # Records stream in from the consumer thread WHILE the candidate runs;
        # the signed roster only completes at ProcessStop, i.e. at the barrier.
        records = [{"processor": 0, "qpc": 12, "old_thread_id": 900,
                    "instruction_retired": 1_000},
                   {"processor": 0, "qpc": 20, "old_thread_id": 900,
                    "instruction_retired": 1_700}]
        session = win32.EtwPmcSession(
            session_handle=1, capability=etw.capability_evidence_record(source_id=0),
            attachment=etw.event_attachment_record(), observations=[],
            thread_lifetimes=[], record_stream=lambda: list(records),
            member_lifetimes=[], event_id_blob=etw.classic_event_id_blob(),
            capability_facts=etw.granted_capability_facts_for_test())

        def finalize(target):
            order.append("close_trace_window")
            target.thread_lifetimes.append(
                {"process_id": 4100, "process_start_key": "0000000000000011",
                 "thread_id": 900, "started_qpc": 11, "ended_qpc": 29})
            target.member_lifetimes.append(
                {"process_id": 4100, "process_start_key": "0000000000000011"})

        session.trace_finalizer = finalize
        # Before the barrier the roster is EMPTY, so consumption cannot
        # attribute a single delta — which is why the hook has to exist.
        self.assertEqual(session.thread_lifetimes, [])
        with self.assertRaises(win32.CollectorFault) as caught:
            session.consume_cswitch()
        self.assertIn("ETW_CSWITCH_UNATTRIBUTED_THREAD", str(caught.exception))
        session.close_trace_window()
        order.append("consume_cswitch")
        observations = session.consume_cswitch()
        self.assertEqual(order, ["close_trace_window", "consume_cswitch"])
        self.assertEqual([row["delta_from_previous"] for row in observations], [0, 700])
        self.assertEqual(len(session.members()), 1)
        # And the collector itself calls it, in that position.
        source = inspect.getsource(win32.collect)
        self.assertIn("session.close_trace_window()", source)
        self.assertLess(source.index("session.close_trace_window()"),
                        source.index("session.consume_cswitch()"))
        self.assertLess(source.index("WaitForSingleObject"),
                        source.index("session.close_trace_window()"))

    def test_bw46_adversarial_an_unattached_trace_finalizer_is_a_fault(self):
        """No finalizer means the trace window was never closed — never a no-op."""
        etw = _etw()
        session = win32.EtwPmcSession(
            session_handle=1, capability=etw.capability_evidence_record(source_id=0),
            attachment=etw.event_attachment_record(), observations=[],
            thread_lifetimes=[])
        with self.assertRaises(win32.CollectorFault) as caught:
            session.close_trace_window()
        self.assertIn("ETW_TRACE_FINALIZER_NOT_ATTACHED", str(caught.exception))
        # A pre-captured (replay/witness) session attaches a finalizer that
        # VERIFIES the capture is already complete rather than doing nothing.
        capture = etw.CapturedTrace(
            cswitch_records=[{"processor": 0, "qpc": 12, "old_thread_id": 900,
                              "instruction_retired": 1_000},
                             {"processor": 0, "qpc": 20, "old_thread_id": 900,
                              "instruction_retired": 1_700}],
            process_events=[
                {"kind": "START", "process_id": 4100, "process_start_key": 0x11,
                 "parent_process_id": None, "parent_process_start_key": None,
                 "qpc": 10},
                {"kind": "STOP", "process_id": 4100, "process_start_key": 0x11,
                 "qpc": 30}],
            thread_events=[
                {"kind": "START", "thread_id": 900, "process_id": 4100,
                 "process_start_key": 0x11, "qpc": 11},
                {"kind": "STOP", "thread_id": 900, "process_id": 4100,
                 "process_start_key": 0x11, "qpc": 29}],
            capability_facts=etw.granted_capability_facts_for_test(),
            loss=etw.LossCounters(0, 0, 0), session_handle=7, source_id=0)
        replayed = etw.make_etw_session_factory(
            capture, job_object_id="JOB.0.0.0", root_process_id=4100,
            root_process_start_key="0000000000000011")()
        replayed.close_trace_window()
        self.assertEqual(len(replayed.consume_cswitch()), 2)

    def test_bw47_positive_collect_tells_the_session_which_root_it_is_measuring(self):
        """The root PID/start key reach the session as VALUES, not by patching.

        The trace-window finalizer has to bind the observed roster to the root
        `collect()` actually created, and `collect()` already knows both values
        one line before it calls the factory (`root_start_key` and
        `process_information.dwProcessId`). Handing them to the session there
        is the difference between a typed seam and a smoke driver that
        monkey-patches `query_process_start_key` to eavesdrop on them.
        """
        etw = _etw()
        session = win32.EtwPmcSession(
            session_handle=1, capability=etw.capability_evidence_record(source_id=0),
            attachment=etw.event_attachment_record(), observations=[],
            thread_lifetimes=[])
        with self.assertRaises(win32.CollectorFault) as caught:
            session.root_identity()
        self.assertIn("ETW_ROOT_IDENTITY_NOT_ATTACHED", str(caught.exception))
        session.root_process_id = 4100
        session.root_process_start_key = "0000000000000011"
        self.assertEqual(session.root_identity(), (4100, "0000000000000011"))
        # `collect()` sets both, after it has queried the start key and BEFORE
        # it configures the session or resumes the candidate.
        source = inspect.getsource(win32.collect)
        self.assertIn("session.root_process_id", source)
        self.assertIn("session.root_process_start_key", source)
        self.assertLess(source.index("root_start_key = query_process_start_key"),
                        source.index("session.root_process_id"))
        self.assertLess(source.index("session.root_process_start_key"),
                        source.index("session.configure("))
        self.assertLess(source.index("session.root_process_start_key"),
                        source.index("ResumeThread"))
        # A malformed key is refused at the seam, not carried into a roster.
        session.root_process_start_key = "nope"
        with self.assertRaises(win32.CollectorFault) as caught:
            session.root_identity()
        self.assertIn("ETW_ROOT_IDENTITY_INVALID", str(caught.exception))

    # --- the three live-path defects the pure suite could not see ------------

    def test_bw48_positive_flagged_etw_ordinals_match_the_installed_sdk_header(self):
        """Every `VALUE NOT PUBLISHED` ExtType/Flags pin equals the SDK's value.

        These constants are the ones Learn NAMES and never NUMBERS, so the pins
        were carried on the module's own authority and nothing re-derived them.
        Three were wrong, and one of the three sat on a LIVE decode path:
        `EVENT_HEADER_FLAG_CLASSIC_HEADER` was 0x0040, which is
        `EVENT_HEADER_FLAG_64_BIT_HEADER`, so `_on_event_record` took its bare
        `return` on every CSwitch on a 64-bit host — a SILENT RECORD DROP, the
        one failure mode this module says it does not have.

        The witness therefore does both halves: it pins the values, and it
        re-derives them from the installed header when the SDK is present, so
        the pin cannot drift from the header the smoke run compiles against.
        """
        etw = _etw()
        # Wrong, and LIVE: 0x0040 is EVENT_HEADER_FLAG_64_BIT_HEADER.
        self.assertEqual(etw.EVENT_HEADER_FLAG_CLASSIC_HEADER, 0x0100)
        self.assertNotEqual(etw.EVENT_HEADER_FLAG_CLASSIC_HEADER, 0x0040)
        # Wrong, and DEAD: defined and never read. Corrected anyway, because a
        # future reader binding an ExtType from this table would inherit the
        # error at the point where it becomes live.
        self.assertEqual(etw.EVENT_HEADER_EXT_TYPE_EVENT_KEY, 0x000A)
        self.assertEqual(etw.EVENT_HEADER_EXT_TYPE_PROCESS_START_KEY, 0x000D)
        # Right, and load-bearing: the PMC join reads this one every record.
        self.assertEqual(etw.EVENT_HEADER_EXT_TYPE_PMC_COUNTERS, 0x0008)
        self.assertEqual(etw.EVENT_HEADER_FLAG_EXTENDED_INFO, 0x0001)
        # ⛔ NO SILENT CAP. The literal pins above are asserted unconditionally, but the
        # re-derivation below can only run where an SDK is installed. A green on a host
        # without one means LESS than a green on a host with one, so it SAYS so rather
        # than passing quietly (ANTI-DRIFT §4: print what the green means).
        sdk_headers = sorted(glob.glob(SDK_EVNTCONS_HEADERS))
        if not sdk_headers:
            sys.stderr.write(
                "\n[bw48] NOTE: no Windows SDK evntcons.h found on this host — the pins above\n"
                "       were checked, but NOT re-derived from a header. This green does not\n"
                "       cover ABI drift; the smoke-run host must re-run this witness.\n")
        for path in sdk_headers:
            with open(path, "r", encoding="utf-8", errors="ignore") as handle:
                text = handle.read()
            defined = dict(re.findall(
                r"#define\s+(EVENT_HEADER_(?:EXT_TYPE|FLAG)_[A-Z0-9_]+)\s+"
                r"(0x[0-9A-Fa-f]+)", text))
            self.assertIn("EVENT_HEADER_FLAG_CLASSIC_HEADER", defined)
            checked = 0
            for name, value in sorted(defined.items()):
                pinned = getattr(etw, name, None)
                if pinned is None:
                    continue
                self.assertEqual(pinned, int(value, 16),
                                 "%s disagrees with %s" % (name, path))
                checked += 1
            self.assertGreaterEqual(checked, 12)

    def test_bw49_positive_decoded_thread_events_join_the_signed_member_roster(self):
        """The REAL decoder emits thread events a member roster can join.

        `_decode_kernel_process_event` hard-coded `"process_start_key": None`
        for every thread event while `assemble_thread_lifetimes()` requires a
        real key, so the LIVE thread path could never join: every physical run
        would have died at `ETW_PROCESS_START_KEY_INVALID:None` — after the
        candidate had already run. The key is not invented and no new capture
        path is opened for it: it is BOUND from the ProcessStart events this
        same consumer already decoded, by PID and by QPC interval, so the
        thread roster and the member roster carry the SAME key by construction.

        Records are fed to the real `_on_event_record` in an arrival order that
        does NOT match QPC order (thread 950 arrives before its own process's
        ProcessStart), because a real-time session delivers per-processor
        buffers as they flush.
        """
        etw = _etw()
        consumer = etw.EtwPmcConsumer(session_name="MBCX01-BUILD-B-PMC-WITNESS")
        api = _FakeTraceApi()
        consumer._win32 = etw._EtwWin32(advapi32=api, kernel32=None)
        consumer._capability_facts = etw.granted_capability_facts_for_test()
        feed = [
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START,
             _process_start_payload(4100, 0x11, parent_process_id=4000,
                                    parent_start_key=0x07), 4000, 10),
            (etw.KERNEL_PROCESS_EVENT_ID_THREAD_START,
             struct.pack("<II", 4100, 900), 4100, 11),
            # Arrives BEFORE its process's ProcessStart, at a LATER qpc.
            (etw.KERNEL_PROCESS_EVENT_ID_THREAD_START,
             struct.pack("<II", 4200, 950), 4200, 13),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START,
             _process_start_payload(4200, 0x22, parent_process_id=4100,
                                    parent_start_key=0x11), 4100, 12),
            (etw.KERNEL_PROCESS_EVENT_ID_THREAD_STOP,
             struct.pack("<II", 4200, 950), 4200, 27),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_STOP,
             _process_stop_payload(4200, 0x22), 4200, 28),
            (etw.KERNEL_PROCESS_EVENT_ID_THREAD_STOP,
             struct.pack("<II", 4100, 900), 4100, 29),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_STOP,
             _process_stop_payload(4100, 0x11), 4100, 30),
        ]
        alive = []
        for event_id, payload, logging_process_id, timestamp in feed:
            record, buffer = _kernel_process_record(
                etw, event_id=event_id, payload=payload,
                logging_process_id=logging_process_id, timestamp=timestamp)
            alive.append((record, buffer))
            consumer._on_event_record(ctypes.pointer(record))
        self.assertEqual(consumer.stop(), etw.LossCounters(0, 0, 0))
        capture = consumer.capture()
        self.assertEqual(len(capture.process_events), 4)
        self.assertEqual(len(capture.thread_events), 4)
        # No thread event leaves the consumer without a real key.
        self.assertNotIn(None, [row["process_start_key"]
                                for row in capture.thread_events])
        members = etw.assemble_member_lifetimes(
            capture.process_events, job_object_id="JOB.0.0.0",
            root_process_id=4100, root_process_start_key="0000000000000011")
        threads = etw.assemble_thread_lifetimes(capture.thread_events, members)
        self.assertEqual(
            [(row["thread_id"], row["process_id"], row["process_start_key"])
             for row in threads],
            [(900, 4100, "0000000000000011"), (950, 4200, "0000000000000022")])
        self.assertEqual([row["started_qpc"] for row in threads], [11, 13])
        self.assertEqual([row["ended_qpc"] for row in threads], [29, 27])

    def test_bw50_adversarial_an_unbindable_thread_event_is_refused_by_name(self):
        """A thread the ProcessStart stream never explained is a NAMED fault.

        Two ways a key cannot be bound, and neither may be guessed or dropped:
        a thread of a process with no decoded ProcessStart at all, and a thread
        whose own QPC PRECEDES every ProcessStart for that PID — which is what
        PID reuse looks like from inside the stream. Binding it to the later
        incarnation would attribute a dead process's threads to a live member.
        """
        etw = _etw()
        for name, feed in (
                ("no ProcessStart at all",
                 [(etw.KERNEL_PROCESS_EVENT_ID_THREAD_START,
                   struct.pack("<II", 5000, 700), 5000, 11)]),
                ("thread predates every ProcessStart for its PID",
                 [(etw.KERNEL_PROCESS_EVENT_ID_THREAD_START,
                   struct.pack("<II", 5000, 700), 5000, 50),
                  (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START,
                   _process_start_payload(5000, 0x33), 4100, 100)])):
            with self.subTest(case=name):
                consumer = etw.EtwPmcConsumer(
                    session_name="MBCX01-BUILD-B-PMC-WITNESS")
                consumer._win32 = etw._EtwWin32(advapi32=_FakeTraceApi(),
                                                kernel32=None)
                consumer._capability_facts = etw.granted_capability_facts_for_test()
                alive = []
                for event_id, payload, logging_process_id, timestamp in feed:
                    record, buffer = _kernel_process_record(
                        etw, event_id=event_id, payload=payload,
                        logging_process_id=logging_process_id,
                        timestamp=timestamp)
                    alive.append((record, buffer))
                    consumer._on_event_record(ctypes.pointer(record))
                consumer.stop()
                with self.assertRaises(etw.EtwConsumerFault) as caught:
                    consumer.capture()
                self.assertIn("ETW_THREAD_START_KEY_UNBINDABLE",
                              str(caught.exception))
                self.assertIn("5000", str(caught.exception))

    def test_bw51_adversarial_a_failed_closetrace_is_an_incomplete_drain(self):
        """`CloseTrace`'s return was DISCARDED, so a failed close read as a drain.

        `stop()` called `CloseTrace` and threw the status away, then queried the
        loss counters and reported them as evidence. A `CloseTrace` that did not
        succeed means the consumer never proved the pump stopped, so the
        counters describe a stream that may still be moving: that is UNAVAILABLE
        evidence, never a count. The session is still STOPPED first — a drain
        fault must not leave a system logger running.
        """
        etw = _etw()
        consumer = etw.EtwPmcConsumer(session_name="MBCX01-BUILD-B-PMC-WITNESS")
        api = _FakeTraceApi(close_trace_status=6)  # ERROR_INVALID_HANDLE
        consumer._win32 = etw._EtwWin32(advapi32=api, kernel32=None)
        consumer._capability_facts = etw.granted_capability_facts_for_test()
        consumer._session_handle = ctypes.c_ulonglong(0x1234)
        consumer._trace_handle = ctypes.c_ulonglong(0x99)
        consumer._started = True
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            consumer.stop()
        self.assertIn("ETW_TRACE_DRAIN_INCOMPLETE", str(caught.exception))
        self.assertIn("CloseTrace", str(caught.exception))
        # Teardown still happened: the session was stopped despite the fault.
        self.assertIn(("ControlTraceW", 0x1234, etw.EVENT_TRACE_CONTROL_STOP),
                      api.calls)
        # And the capture is unavailable, not a count.
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            consumer.capture()
        self.assertIn("ETW_TRACE_DRAIN_INCOMPLETE", str(caught.exception))

    def test_bw52_adversarial_a_pump_that_outlives_the_join_is_an_incomplete_drain(self):
        """`join(timeout=30)`'s result was DISCARDED, so a timeout read as a drain.

        A `ProcessTrace` pump that is still alive after the join is still
        appending records, so the capture is a snapshot of a moving stream and
        the loss counters do not describe it. `stop()` must say so by name
        rather than return counters that look complete.
        """
        etw = _etw()
        saved = etw.CONSUMER_JOIN_TIMEOUT_SECONDS
        release = threading.Event()
        pump = threading.Thread(target=release.wait, name="mbcx01-witness-pump",
                                daemon=True)
        pump.start()
        try:
            etw.CONSUMER_JOIN_TIMEOUT_SECONDS = 0.05
            consumer = etw.EtwPmcConsumer(session_name="MBCX01-BUILD-B-PMC-WITNESS")
            api = _FakeTraceApi()
            consumer._win32 = etw._EtwWin32(advapi32=api, kernel32=None)
            consumer._capability_facts = etw.granted_capability_facts_for_test()
            consumer._thread = pump
            with self.assertRaises(etw.EtwConsumerFault) as caught:
                consumer.stop()
            self.assertIn("ETW_TRACE_DRAIN_INCOMPLETE", str(caught.exception))
            self.assertIn("ProcessTrace", str(caught.exception))
            with self.assertRaises(etw.EtwConsumerFault) as caught:
                consumer.capture()
            self.assertIn("ETW_TRACE_DRAIN_INCOMPLETE", str(caught.exception))
        finally:
            etw.CONSUMER_JOIN_TIMEOUT_SECONDS = saved
            release.set()
            pump.join(timeout=5)
        self.assertFalse(pump.is_alive())

    def test_bw53_adversarial_loss_is_never_re_queried_after_the_session_stops(self):
        """`capture()` queried the loss counters a SECOND time, after the STOP.

        `stop()` read the counters while the session was alive and then stopped
        it; `capture()` then called `_query_loss()` again on a handle nobody had
        invalidated. Whatever that second query returns, it is not evidence
        about the trace that ran — so the counters `stop()` read are the only
        ones a capture may carry, and a post-stop query is refused by name.

        The fake scripts a DIFFERENT `EventsLost` for a second query, so a
        carried counter and a re-queried one cannot be confused.
        """
        etw = _etw()
        consumer = etw.EtwPmcConsumer(session_name="MBCX01-BUILD-B-PMC-WITNESS")
        api = _FakeTraceApi(query_events_lost=(0, 7))
        consumer._win32 = etw._EtwWin32(advapi32=api, kernel32=None)
        consumer._capability_facts = etw.granted_capability_facts_for_test()
        consumer._session_handle = ctypes.c_ulonglong(0x1234)
        consumer._started = True
        # A capture taken BEFORE the drain has no loss evidence at all.
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            consumer.capture()
        self.assertIn("ETW_TRACE_NOT_STOPPED", str(caught.exception))
        self.assertEqual(api.query_count, 0)
        loss = consumer.stop()
        self.assertEqual(loss, etw.LossCounters(0, 0, 0))
        self.assertEqual(api.query_count, 1)
        # Two captures, still ONE query: the counters are carried, not re-read.
        self.assertEqual(consumer.capture().loss, etw.LossCounters(0, 0, 0))
        self.assertEqual(consumer.capture().loss, etw.LossCounters(0, 0, 0))
        self.assertEqual(api.query_count, 1)
        self.assertEqual(consumer.capture().session_handle, 0x1234)
        # A repeat stop() is idempotent and does not re-run the teardown.
        self.assertEqual(consumer.stop(), etw.LossCounters(0, 0, 0))
        self.assertEqual(api.query_count, 1)
        self.assertEqual(sum(1 for call in api.calls
                             if call[0] == "ControlTraceW"
                             and call[2] == etw.EVENT_TRACE_CONTROL_STOP), 1)
        # And the query itself is refused after the session is gone.
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            consumer._query_loss()
        self.assertIn("ETW_LOSS_QUERY_AFTER_SESSION_STOP", str(caught.exception))

    def test_bw54_adversarial_a_classic_cswitch_survives_the_header_flag_gate(self):
        """The wrong CLASSIC_HEADER pin DROPPED records. Show the drop, not the number.

        bw48 pins the constant; this witness shows what the constant decides. A
        classic (MOF) CSwitch whose header is not a 64-bit header carries
        EVENT_HEADER_FLAG_CLASSIC_HEADER (0x0100) and not 0x0040, so the old pin
        made `_on_event_record()` take its bare `return`: no record, no fault,
        no count — a delta simply gone from a retired-instruction total. It must
        decode. And the gate must still GATE: a record without the classic flag
        is ignored, and neither case may leave a callback fault behind.

        The record's Flags are written as the SDK's LITERALS
        (evntcons.h:156 CLASSIC_HEADER 0x0100, :148 EXTENDED_INFO 0x0001) and
        NOT as `etw.EVENT_HEADER_FLAG_*`: a witness that builds its input out of
        the constant it is testing agrees with any value that constant has, and
        would have passed on the wrong pin.
        """
        etw = _etw()
        consumer = etw.EtwPmcConsumer(session_name="MBCX01-BUILD-B-PMC-WITNESS")
        counters = [0] * len(etw.PINNED_COUNTER_NAMES)
        counters[etw.PINNED_INSTRUCTION_RETIRED_INDEX] = 4_242_424_242
        classic, alive = _classic_cswitch_record(
            etw, flags=0x0100 | 0x0001,
            processor=3, qpc=907, new_thread_id=901, old_thread_id=900,
            counters=counters)
        consumer._on_event_record(ctypes.pointer(classic))
        self.assertEqual(consumer._callback_faults, [])
        self.assertEqual(consumer._cswitch_records,
                         [{"processor": 3, "qpc": 907, "old_thread_id": 900,
                           "instruction_retired": 4_242_424_242}])
        # The gate still gates: no classic header, no classic decode.
        modern, alive_modern = _classic_cswitch_record(
            etw, flags=0x0001,
            processor=3, qpc=908, new_thread_id=902, old_thread_id=900,
            counters=counters)
        consumer._on_event_record(ctypes.pointer(modern))
        self.assertEqual(len(consumer._cswitch_records), 1)
        self.assertEqual(consumer._callback_faults, [])

    # --- AMENDMENT-2: thread identity in TIME, not by TID or PID alone -------

    def test_bw58_positive_a_reused_tid_gets_one_lifetime_per_incarnation(self):
        """Windows REUSES thread ids, and the consumer must read that correctly.

        "The operating system may reuse a thread ID after the thread has
        terminated" (Learn, *PsGetThreadId* Remarks; *Thread Handles and
        Identifiers*). Two DISJOINT lifetimes for TID 77 inside one live process
        are an ordinary observation of a long capture, and refusing them refuses
        RIGHT evidence: the whole capture faults and every delta in it is lost.

        Both lifetimes must survive assembly AND each CSwitch observation must
        be attributed to the lifetime whose interval CONTAINS its QPC — the
        containment is what makes the join unambiguous once a TID is no longer
        a key.
        """
        etw = _etw()
        members = etw.assemble_member_lifetimes(
            [{"kind": "START", "process_id": 4100, "process_start_key": 0x11,
              "parent_process_id": None, "parent_process_start_key": None,
              "qpc": 10},
             {"kind": "STOP", "process_id": 4100, "process_start_key": 0x11,
              "qpc": 100}],
            job_object_id="JOB.0.0.0", root_process_id=4100,
            root_process_start_key="0000000000000011")
        events = []
        for started, ended in ((20, 30), (60, 70)):
            events.append({"kind": "START", "thread_id": 77, "process_id": 4100,
                           "process_start_key": 0x11, "qpc": started})
            events.append({"kind": "STOP", "thread_id": 77, "process_id": 4100,
                           "process_start_key": 0x11, "qpc": ended})
        threads = etw.assemble_thread_lifetimes(events, members)
        self.assertEqual([(row["thread_id"], row["started_qpc"], row["ended_qpc"])
                          for row in threads], [(77, 20, 30), (77, 60, 70)])
        for row in threads:
            self.assertEqual(set(row), measurement.THREAD_LIFETIME_KEYS)
        # The join is by TID *and* QPC: each observation lands in its own
        # incarnation, and a QPC inside NEITHER lifetime is unattributed.
        records = [{"processor": 0, "qpc": 25, "old_thread_id": 77,
                    "instruction_retired": 1_000},
                   {"processor": 0, "qpc": 65, "old_thread_id": 77,
                    "instruction_retired": 1_700}]
        session = win32.EtwPmcSession(
            session_handle=0, capability={}, attachment={}, observations=[],
            thread_lifetimes=threads, record_stream=lambda: records)
        observations = session.consume_cswitch()
        self.assertEqual([row["delta_from_previous"] for row in observations],
                         [0, 700])
        self.assertEqual(
            [win32.resolve_thread_lifetime(threads, row["old_thread_id"],
                                           row["qpc"])["started_qpc"]
             for row in observations], [20, 60])
        gap = win32.EtwPmcSession(
            session_handle=0, capability={}, attachment={}, observations=[],
            thread_lifetimes=threads,
            record_stream=lambda: [{"processor": 0, "qpc": 45,
                                    "old_thread_id": 77,
                                    "instruction_retired": 1_000}])
        with self.assertRaises(win32.CollectorFault) as caught:
            gap.consume_cswitch()
        self.assertIn("ETW_CSWITCH_UNATTRIBUTED_THREAD", str(caught.exception))

    def test_bw59_adversarial_overlapping_lifetimes_for_one_tid_still_fault(self):
        """Reuse is SEQUENTIAL. Two lifetimes alive at once are impossible.

        Permitting reuse must not permit the world where one TID is running
        twice: that would make the CSwitch join ambiguous and let a delta be
        attributed to either of two rows. Both spellings of the impossible world
        fault BY NAME — two starts before any stop, and two intervals that
        overlap — and a duplicate START at the very same QPC keeps its own name
        rather than being re-labelled.
        """
        etw = _etw()
        members = etw.assemble_member_lifetimes(
            [{"kind": "START", "process_id": 4100, "process_start_key": 0x11,
              "parent_process_id": None, "parent_process_start_key": None,
              "qpc": 10},
             {"kind": "STOP", "process_id": 4100, "process_start_key": 0x11,
              "qpc": 100}],
            job_object_id="JOB.0.0.0", root_process_id=4100,
            root_process_start_key="0000000000000011")

        def event(kind, qpc):
            return {"kind": kind, "thread_id": 77, "process_id": 4100,
                    "process_start_key": 0x11, "qpc": qpc}

        cases = (
            ("overlapping intervals",
             [event("START", 20), event("START", 25), event("STOP", 30),
              event("STOP", 35)],
             "ETW_THREAD_LIFETIME_OVERLAPPING_REUSE:77"),
            ("second start at the same qpc",
             [event("START", 20), event("START", 20), event("STOP", 30),
              event("STOP", 35)],
             "ETW_THREAD_LIFETIME_DUPLICATE_START:77"),
            ("touching intervals share an instant",
             [event("START", 20), event("STOP", 30), event("START", 30),
              event("STOP", 40)],
             "ETW_THREAD_LIFETIME_OVERLAPPING_REUSE:77"),
        )
        for name, events, expected in cases:
            with self.subTest(case=name):
                with self.assertRaises(etw.EtwConsumerFault) as caught:
                    etw.assemble_thread_lifetimes(events, members)
                self.assertIn(expected, str(caught.exception))
        # An unbalanced roster keeps its own two names, not the reuse one.
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            etw.assemble_thread_lifetimes(
                [event("START", 20), event("STOP", 30), event("START", 60)],
                members)
        self.assertIn("ETW_THREAD_LIFETIME_INCOMPLETE", str(caught.exception))
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            etw.assemble_thread_lifetimes(
                [event("START", 20), event("STOP", 30), event("STOP", 70)],
                members)
        self.assertIn("ETW_THREAD_LIFETIME_UNMATCHED_STOP", str(caught.exception))

    def test_bw60_adversarial_a_thread_outside_every_live_incarnation_is_refused(self):
        """A thread must live INSIDE one process incarnation, never beside it.

        `bind_thread_start_keys` documented a bind by "PID *and* QPC interval"
        but only ever read `kind == "START"` events, so ProcessStop was never
        consulted and the rule degraded to "the last start not in the future".
        A thread observed while NO incarnation of that PID is alive was bound to
        the DEAD one, and nothing downstream re-checked it: the assembler joined
        on the (PID, start key) PAIR and the frozen validator checked pair
        membership and thread monotonicity, never nesting.

        That admits WRONG evidence — a foreign thread's retired instructions
        summed into a member's total under a start key that had already exited.
        """
        etw = _etw()
        process_events = [
            {"kind": "START", "process_id": 5000,
             "process_start_key": "00000000000000AA", "parent_process_id": None,
             "parent_process_start_key": None, "qpc": 10},
            {"kind": "STOP", "process_id": 5000,
             "process_start_key": "00000000000000AA", "qpc": 40},
            {"kind": "START", "process_id": 5000,
             "process_start_key": "00000000000000BB", "parent_process_id": 5000,
             "parent_process_start_key": "00000000000000AA", "qpc": 60},
            {"kind": "STOP", "process_id": 5000,
             "process_start_key": "00000000000000BB", "qpc": 90},
        ]
        dead_gap = [{"kind": "START", "thread_id": 303, "process_id": 5000,
                     "process_start_key": None, "qpc": 50},
                    {"kind": "STOP", "thread_id": 303, "process_id": 5000,
                     "process_start_key": None, "qpc": 55}]
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            etw.bind_thread_start_keys(dead_gap, process_events)
        self.assertIn("ETW_THREAD_START_KEY_UNBINDABLE:5000@50",
                      str(caught.exception))
        # Each incarnation still binds its OWN threads, by containment.
        bound = etw.bind_thread_start_keys(
            [{"kind": "START", "thread_id": 303, "process_id": 5000,
              "process_start_key": None, "qpc": 20},
             {"kind": "STOP", "thread_id": 303, "process_id": 5000,
              "process_start_key": None, "qpc": 30},
             {"kind": "START", "thread_id": 404, "process_id": 5000,
              "process_start_key": None, "qpc": 70},
             {"kind": "STOP", "thread_id": 404, "process_id": 5000,
              "process_start_key": None, "qpc": 80}],
            process_events)
        self.assertEqual([row["process_start_key"] for row in bound],
                         ["00000000000000AA"] * 2 + ["00000000000000BB"] * 2)
        # And a thread arriving with a key ALREADY set — the path the binder
        # passes straight through — is caught by the assembler instead.
        members = etw.assemble_member_lifetimes(
            process_events, job_object_id="JOB.0.0.0", root_process_id=5000,
            root_process_start_key="00000000000000AA")
        for started, ended in ((5, 30), (20, 45)):
            with self.subTest(interval=(started, ended)):
                with self.assertRaises(etw.EtwConsumerFault) as caught:
                    etw.assemble_thread_lifetimes(
                        [{"kind": "START", "thread_id": 303, "process_id": 5000,
                          "process_start_key": "00000000000000AA",
                          "qpc": started},
                         {"kind": "STOP", "thread_id": 303, "process_id": 5000,
                          "process_start_key": "00000000000000AA",
                          "qpc": ended}],
                        members)
                self.assertIn("ETW_THREAD_LIFETIME_OUTSIDE_PROCESS:303",
                              str(caught.exception))

    def test_bw95_adversarial_a_stop_from_another_member_cannot_close_a_lifetime(self):
        """A STOP is an event OF A PROCESS, and the pairing must read that.

        codex-CLI r6 SEAT1 F2 (`mbcx01_build_etw_consumer.py:1528`). The pairing
        VALIDATED the STOP's `(pid, start key)` against the member roster and then
        threw it away, keeping only the QPC: `stops.setdefault(thread_id,
        []).append(int(qpc))`. Both halves of a lifetime were therefore free to
        come from DIFFERENT member processes, because a TID is unique to neither.
        The row that came out named process A and carried process B's end instant,
        which is misattributed lifetime evidence under a signed identity: every
        CSwitch delta whose QPC falls in the borrowed tail is attributed to A's
        thread by `resolve_thread_lifetime`, and the roster is signed as A's.

        Same family as the AMENDMENT-2 folds above (bw58-bw60): identity is a TID
        *and* an interval *and* the process the interval belongs to. Windows
        reuses a thread id "after the thread has terminated" (Learn, PsGetThreadId
        Remarks), which is exactly the world where two members can carry the same
        TID in one capture.
        """
        etw = _etw()
        members = etw.assemble_member_lifetimes(
            [{"kind": "START", "process_id": 4100, "process_start_key": 0x11,
              "parent_process_id": None, "parent_process_start_key": None,
              "qpc": 10},
             {"kind": "START", "process_id": 4200, "process_start_key": 0x22,
              "parent_process_id": 4100, "parent_process_start_key": 0x11,
              "qpc": 15},
             {"kind": "STOP", "process_id": 4200, "process_start_key": 0x22,
              "qpc": 95},
             {"kind": "STOP", "process_id": 4100, "process_start_key": 0x11,
              "qpc": 100}],
            job_object_id="JOB.0.0.0", root_process_id=4100,
            root_process_start_key="0000000000000011")

        def thread_event(kind, qpc, process_id, start_key):
            return {"kind": kind, "thread_id": 77, "process_id": process_id,
                    "process_start_key": start_key, "qpc": qpc}

        # THE RED: A-START (4100) closed by a B-STOP (4200) for the same TID.
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            etw.assemble_thread_lifetimes(
                [thread_event("START", 20, 4100, 0x11),
                 thread_event("STOP", 90, 4200, 0x22)], members)
        self.assertIn("ETW_THREAD_LIFETIME_PROCESS_MISMATCH:77",
                      str(caught.exception))
        # Both identity halves are named, so the operator can read WHICH pair
        # disagreed rather than being told only that something did.
        self.assertIn("0000000000000011", str(caught.exception))
        self.assertIn("0000000000000022", str(caught.exception))

        # DISCRIMINATING (a): the same TID living in BOTH members, each with its
        # OWN matched stop, is an ordinary capture and must still assemble. A
        # refusal here would be right evidence refused — the failure mode the
        # whole AMENDMENT-2 fold set exists to prevent.
        honest = etw.assemble_thread_lifetimes(
            [thread_event("START", 20, 4100, 0x11),
             thread_event("STOP", 30, 4100, 0x11),
             thread_event("START", 40, 4200, 0x22),
             thread_event("STOP", 50, 4200, 0x22)], members)
        self.assertEqual(
            [(row["process_id"], row["process_start_key"], row["started_qpc"],
              row["ended_qpc"]) for row in honest],
            [(4100, "0000000000000011", 20, 30),
             (4200, "0000000000000022", 40, 50)])

        # DISCRIMINATING (b): the mismatch is decided on the PAIR, not on the PID
        # alone — one PID's two incarnations are two processes, and a STOP from
        # the second cannot close a lifetime opened in the first.
        reused = etw.assemble_member_lifetimes(
            [{"kind": "START", "process_id": 4100, "process_start_key": 0x11,
              "parent_process_id": None, "parent_process_start_key": None,
              "qpc": 10},
             {"kind": "STOP", "process_id": 4100, "process_start_key": 0x11,
              "qpc": 40},
             {"kind": "START", "process_id": 4100, "process_start_key": 0x33,
              "parent_process_id": 4100, "parent_process_start_key": 0x11,
              "qpc": 60},
             {"kind": "STOP", "process_id": 4100, "process_start_key": 0x33,
              "qpc": 100}],
            job_object_id="JOB.0.0.0", root_process_id=4100,
            root_process_start_key="0000000000000011")
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            etw.assemble_thread_lifetimes(
                [thread_event("START", 20, 4100, 0x11),
                 thread_event("STOP", 70, 4100, 0x33)], reused)
        self.assertIn("ETW_THREAD_LIFETIME_PROCESS_MISMATCH:77",
                      str(caught.exception))

        # DISCRIMINATING (c): the existing vocabulary is not re-labelled. An
        # unmatched stop and an incomplete start keep their own names.
        for events, expected in (
                ([thread_event("START", 20, 4100, 0x11),
                  thread_event("STOP", 30, 4100, 0x11),
                  thread_event("STOP", 60, 4200, 0x22)],
                 "ETW_THREAD_LIFETIME_UNMATCHED_STOP"),
                ([thread_event("START", 20, 4100, 0x11)],
                 "ETW_THREAD_LIFETIME_INCOMPLETE")):
            with self.subTest(expected=expected):
                with self.assertRaises(etw.EtwConsumerFault) as caught:
                    etw.assemble_thread_lifetimes(events, members)
                self.assertIn(expected, str(caught.exception))

    # --- the measured Job is a TREE, and the root has no parent inside it ----

    def _live_process_feed(self, etw, *, root_pid, root_key, child_pid, child_key,
                           collector_pid=4000):
        """The four ProcessStart/ProcessStop records a one-descendant cell emits.

        Shaped the way a LIVE session delivers them: each start names its
        creator in the PAYLOAD (`ParentProcessID` / `ParentProcessSequenceNumber`,
        which is what the decoder reads after codex-CLI r7 P2) and is logged in
        that same creator's context, which is the ORDINARY direct-creation case
        where the two agree. The case where they DIFFER is bw97's.
        """
        return [
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START,
             _process_start_payload(root_pid, root_key,
                                    parent_process_id=collector_pid,
                                    parent_start_key=0x07), collector_pid, 1),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START,
             _process_start_payload(child_pid, child_key,
                                    parent_process_id=root_pid,
                                    parent_start_key=root_key), root_pid, 3),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_STOP,
             _process_stop_payload(child_pid, child_key), child_pid, 25),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_STOP,
             _process_stop_payload(root_pid, root_key), root_pid, 30),
        ]

    def _decode(self, etw, feed):
        """Drive the REAL callback with synthetic records and return the consumer."""
        consumer = etw.EtwPmcConsumer(session_name="MBCX01-BUILD-B-PMC-WITNESS")
        consumer._win32 = etw._EtwWin32(advapi32=_FakeTraceApi(), kernel32=None)
        consumer._capability_facts = etw.granted_capability_facts_for_test()
        alive = []
        for event_id, payload, logging_process_id, timestamp in feed:
            record, buffer = _kernel_process_record(
                etw, event_id=event_id, payload=payload,
                logging_process_id=logging_process_id, timestamp=timestamp)
            alive.append((record, buffer))
            consumer._on_event_record(ctypes.pointer(record))
        consumer.stop()
        self._alive = alive
        return consumer

    def test_bw65_positive_a_live_capture_carries_the_frozen_parent_tuple(self):
        """The decoded stream must produce the parent fields the validator reads.

        `_decode_kernel_process_event` records `EventHeader.ProcessId` — the
        CREATOR — for every ProcessStart, and no parent start key at all,
        because the payload carries none. The frozen validator
        (`mbcx01_r13_measurement._validate_physical_evidence`, :889-899) reads
        both fields as evidence: the ROOT must carry (None, None), because the
        process that created it is the collector and the collector is not a Job
        member, and every descendant must carry a 16-hex parent key whose pair
        is itself a roster member.

        So every LIVE capture produced `PROCESS_MEMBERSHIP_INVALID` — right
        evidence, refused, after the candidate had already run. The root is now
        special-cased and a descendant's key is RESOLVED from the
        process-incarnation stream by containment; the resolution is never a
        guess, and its three impossible worlds each fault by name.
        """
        etw = _etw()
        fixture = measurement.baseline_receipt_rows(run_id="RUN.BW63")
        job = copy.deepcopy(fixture[0]["receipt"]["job_receipt"])
        evidence = job["evidence"]
        # The harness itself is proven first: the untouched fixture validates
        # clean, so a later non-empty error set is the ROSTER's doing.
        self.assertEqual(measurement._validate_physical_evidence(job, evidence), set())
        root_pid = job["root_process_id"]
        root_key = evidence["process_membership"]["root_process_start_key"]
        consumer = self._decode(etw, self._live_process_feed(
            etw, root_pid=root_pid, root_key=int(root_key, 16),
            child_pid=root_pid + 100, child_key=0xC2))
        capture = consumer.capture()
        self.assertEqual(len(capture.process_events), 4)
        # What the DECODER wrote: the PAYLOAD's parent tuple on both starts
        # (codex-CLI r7 P2), with the emitting context kept beside it.
        starts = [row for row in capture.process_events if row["kind"] == "START"]
        self.assertEqual([row["parent_process_id"] for row in starts], [4000, root_pid])
        self.assertEqual([row["parent_process_start_key"] for row in starts],
                         [0x07, int(root_key, 16)])
        self.assertEqual([row["event_header_process_id"] for row in starts],
                         [4000, root_pid])
        rows = etw.assemble_member_lifetimes(
            capture.process_events, job_object_id=job["job_object_id"],
            root_process_id=root_pid, root_process_start_key=root_key)
        root_row = [row for row in rows if row["process_id"] == root_pid][0]
        child_row = [row for row in rows if row["process_id"] == root_pid + 100][0]
        self.assertIsNone(root_row["parent_process_id"])
        self.assertIsNone(root_row["parent_process_start_key"])
        self.assertEqual(child_row["parent_process_id"], root_pid)
        self.assertEqual(child_row["parent_process_start_key"], root_key)
        # And the frozen validator accepts that roster, which is the whole point.
        evidence["process_membership"]["processes"] = rows
        evidence["process_membership"]["membership_snapshot_digest"] = \
            measurement.sha384(rows)
        job["total_processes"] = len(rows)
        evidence["job_queries"] = measurement._query_evidence(job)
        self.assertEqual(measurement._validate_physical_evidence(job, evidence), set())

        # The three worlds the resolution refuses instead of guessing.
        def assemble(events, root=4100, key="0000000000000011"):
            return etw.assemble_member_lifetimes(
                events, job_object_id="JOB.0.0.0", root_process_id=root,
                root_process_start_key=key)

        root_pair = [
            {"kind": "START", "process_id": 4100, "process_start_key": 0x11,
             "parent_process_id": 4000, "parent_process_start_key": None, "qpc": 10},
            {"kind": "STOP", "process_id": 4100, "process_start_key": 0x11, "qpc": 30}]
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            assemble(root_pair + [
                {"kind": "START", "process_id": 4200, "process_start_key": 0x22,
                 "parent_process_id": 4100, "parent_process_start_key": None, "qpc": 5},
                {"kind": "STOP", "process_id": 4200, "process_start_key": 0x22,
                 "qpc": 8}])
        self.assertIn("ETW_PROCESS_PARENT_START_KEY_UNBINDABLE:4100@5",
                      str(caught.exception))
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            assemble(root_pair + [
                {"kind": "START", "process_id": 4200, "process_start_key": 0x22,
                 "parent_process_id": None, "parent_process_start_key": None,
                 "qpc": 12},
                {"kind": "STOP", "process_id": 4200, "process_start_key": 0x22,
                 "qpc": 20}])
        self.assertIn("ETW_PROCESS_LIFETIME_PARENT_UNKNOWN", str(caught.exception))
        # One PID alive TWICE at the instant its child started: the parent
        # incarnation cannot be chosen, and choosing either would attribute the
        # child to a life that may not have created it.
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            assemble([
                {"kind": "START", "process_id": 4100, "process_start_key": 0x11,
                 "parent_process_id": 4000, "parent_process_start_key": None,
                 "qpc": 10},
                {"kind": "START", "process_id": 4200, "process_start_key": 0x21,
                 "parent_process_id": 4100, "parent_process_start_key": 0x11,
                 "qpc": 15},
                {"kind": "START", "process_id": 4200, "process_start_key": 0x22,
                 "parent_process_id": 4100, "parent_process_start_key": 0x11,
                 "qpc": 20},
                {"kind": "START", "process_id": 4300, "process_start_key": 0x33,
                 "parent_process_id": 4200, "parent_process_start_key": None,
                 "qpc": 25},
                {"kind": "STOP", "process_id": 4300, "process_start_key": 0x33,
                 "qpc": 30},
                {"kind": "STOP", "process_id": 4200, "process_start_key": 0x21,
                 "qpc": 40},
                {"kind": "STOP", "process_id": 4200, "process_start_key": 0x22,
                 "qpc": 50},
                {"kind": "STOP", "process_id": 4100, "process_start_key": 0x11,
                 "qpc": 60}])
        self.assertIn("ETW_PROCESS_INCARNATION_AMBIGUOUS:4200@25", str(caught.exception))

    def test_bw66_adversarial_foreign_host_events_are_out_of_population(self):
        """A busy host must not be able to abort or corrupt a measurement.

        `_enable_process_provider` enables Microsoft-Windows-Kernel-Process
        MACHINE-WIDE — it must, because at enable time the Job holds only the
        suspended root and no filter could name descendants that do not exist
        yet — and the callback forwarded every decoded event into assembly. So
        ordinary host activity decided the outcome: a stranger's ProcessStop was
        `ETW_PROCESS_LIFETIME_UNMATCHED_STOP`, a stranger's thread was
        `ETW_THREAD_START_KEY_UNBINDABLE`, and a stranger that STARTED inside
        the window was assembled into the signed roster, where the Job's own
        `TotalProcesses` contradicts it.

        Scoping is not silencing: a foreign event is OUT OF POPULATION and
        counted in the capture's provenance, while every fault about MEMBER
        evidence still fires by name.
        """
        etw = _etw()
        member = [
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START,
             _process_start_payload(4100, 0x11, parent_process_id=4000,
                                    parent_start_key=0x07), 4000, 10),
            (etw.KERNEL_PROCESS_EVENT_ID_THREAD_START,
             struct.pack("<II", 4100, 900), 4100, 11),
            (etw.KERNEL_PROCESS_EVENT_ID_THREAD_STOP,
             struct.pack("<II", 4100, 900), 4100, 99),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_STOP,
             _process_stop_payload(4100, 0x11), 4100, 100)]
        foreign = [
            # a host process that STARTS inside the window, with a thread
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START,
             _process_start_payload(7777, 0x77, parent_process_id=6666,
                                    parent_start_key=0x66), 6666, 20),
            (etw.KERNEL_PROCESS_EVENT_ID_THREAD_START,
             struct.pack("<II", 7777, 7100), 7777, 22),
            (etw.KERNEL_PROCESS_EVENT_ID_THREAD_STOP,
             struct.pack("<II", 7777, 7100), 7777, 25),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_STOP,
             _process_stop_payload(7777, 0x77), 7777, 30),
            # a host process that was already running when the session opened
            (etw.KERNEL_PROCESS_EVENT_ID_THREAD_START,
             struct.pack("<II", 9999, 7000), 9999, 21),
            (etw.KERNEL_PROCESS_EVENT_ID_THREAD_STOP,
             struct.pack("<II", 9999, 7000), 9999, 26),
            # a host process that EXITS inside the window
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_STOP,
             _process_stop_payload(8888, 0x88), 8888, 40)]
        consumer = self._decode(etw, member + foreign)
        self.assertEqual(len(consumer._process_events), 5)
        self.assertEqual(len(consumer._thread_events), 6)
        capture = consumer.capture(root_process_id=4100,
                                   root_process_start_key="0000000000000011")
        self.assertEqual(capture.provenance["member_scope"], "JOB_MEMBER_TREE")
        self.assertEqual(capture.provenance["excluded_foreign_process_events"], 3)
        self.assertEqual(capture.provenance["excluded_foreign_thread_events"], 4)
        members = etw.assemble_member_lifetimes(
            capture.process_events, job_object_id="JOB.0.0.0",
            root_process_id=4100, root_process_start_key="0000000000000011")
        threads = etw.assemble_thread_lifetimes(capture.thread_events, members)
        self.assertEqual([row["process_id"] for row in members], [4100])
        self.assertEqual([(row["thread_id"], row["process_id"]) for row in threads],
                         [(900, 4100)])
        # The excluded events are RETAINED as the other half of the partition,
        # so "the host was busy" is a counted observation, not an invisible drop.
        partition = etw.partition_job_member_events(
            consumer._process_events, consumer._thread_events,
            root_process_id=4100, root_process_start_key="0000000000000011")
        self.assertEqual(sorted({row["process_id"]
                                 for row in partition.excluded_process_events}),
                         [7777, 8888])
        self.assertEqual(sorted({row["process_id"]
                                 for row in partition.excluded_thread_events}),
                         [7777, 9999])

        # A DESCENDANT of the root is in the population, foreign siblings are not.
        with_child = self._decode(etw, member[:1] + [
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START,
             _process_start_payload(4200, 0x22, parent_process_id=4100,
                                    parent_start_key=0x11), 4100, 12),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_STOP,
             _process_stop_payload(4200, 0x22), 4200, 28)] + member[1:] + foreign)
        scoped = with_child.capture(root_process_id=4100,
                                    root_process_start_key="0000000000000011")
        self.assertEqual(
            sorted({row["process_id"] for row in scoped.process_events}),
            [4100, 4200])

        # Nothing about MEMBER evidence is weakened. Unscoped, the same stream
        # still refuses; a member PID observed when no incarnation of it was
        # alive still refuses even WITH the scope; and a half-given root
        # identity is a fault rather than a partial population.
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            consumer.capture()
        self.assertIn("ETW_THREAD_START_KEY_UNBINDABLE:9999@21", str(caught.exception))
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            consumer.capture(root_process_id=4100)
        self.assertIn("ETW_MEMBER_SCOPE_IDENTITY_INCOMPLETE", str(caught.exception))
        early = self._decode(etw, [
            (etw.KERNEL_PROCESS_EVENT_ID_THREAD_START,
             struct.pack("<II", 4100, 901), 4100, 5)] + member)
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            early.capture(root_process_id=4100,
                          root_process_start_key="0000000000000011")
        self.assertIn("ETW_THREAD_START_KEY_UNBINDABLE:4100@5", str(caught.exception))

        # The replay/witness path is scoped by the SAME function, in the same
        # position, so a synthetic capture and a physical one are one code path.
        capture = etw.CapturedTrace(
            cswitch_records=[{"processor": 0, "qpc": 12, "old_thread_id": 900,
                              "instruction_retired": 1_000},
                             {"processor": 0, "qpc": 20, "old_thread_id": 900,
                              "instruction_retired": 1_700}],
            process_events=[
                {"kind": "START", "process_id": 4100, "process_start_key": 0x11,
                 "parent_process_id": None, "parent_process_start_key": None,
                 "qpc": 10},
                {"kind": "STOP", "process_id": 4100, "process_start_key": 0x11,
                 "qpc": 30},
                {"kind": "START", "process_id": 7777, "process_start_key": 0x77,
                 "parent_process_id": 6666, "parent_process_start_key": None,
                 "qpc": 12},
                {"kind": "STOP", "process_id": 7777, "process_start_key": 0x77,
                 "qpc": 18}],
            thread_events=[
                {"kind": "START", "thread_id": 900, "process_id": 4100,
                 "process_start_key": 0x11, "qpc": 11},
                {"kind": "STOP", "thread_id": 900, "process_id": 4100,
                 "process_start_key": 0x11, "qpc": 29},
                {"kind": "START", "thread_id": 7100, "process_id": 7777,
                 "process_start_key": 0x77, "qpc": 13},
                {"kind": "STOP", "thread_id": 7100, "process_id": 7777,
                 "process_start_key": 0x77, "qpc": 17}],
            capability_facts=etw.granted_capability_facts_for_test(),
            loss=etw.LossCounters(0, 0, 0), session_handle=0x1234, source_id=3,
            counter_index=0)
        session = etw.make_etw_session_factory(
            capture, job_object_id="JOB.0.0.0", root_process_id=4100,
            root_process_start_key="0000000000000011")()
        self.assertEqual([row["process_id"] for row in session.members()], [4100])
        self.assertEqual([row["thread_id"] for row in session.thread_lifetimes], [900])

    # --- codex-CLI r2: the three round-2 P1 findings ------------------------
    #
    # bw80-bw84 are THIS fold's witnesses. bw67-bw69 and bw75-bw79 are left
    # free deliberately: bw70-bw74 were taken by a fold landing in parallel in
    # this same worktree while these were being written, so this block starts
    # clear of the neighbouring ranges rather than renumbering anybody.

    def _source_list_blob(self, etw, entries):
        """The exact `TraceProfileSourceListInfo` answer: PROFILE_SOURCE_INFO chain.

        Each entry is the fixed prefix (evntrace.h: NextEntryOffset, Source,
        MinInterval, MaxInterval, Reserved) followed by the WCHAR Description
        with its NUL terminator, padded so the next entry starts 8-byte
        aligned. The LAST entry carries `NextEntryOffset = 0`, which is what
        ends the list.
        """
        prefix_size = ctypes.sizeof(etw.PROFILE_SOURCE_INFO)
        blob = b""
        for index, (source, description) in enumerate(entries):
            text = description.encode("utf-16-le") + b"\x00\x00"
            size = prefix_size + len(text)
            size += -size % 8
            last = index == len(entries) - 1
            body = struct.pack("<IIIIQ", 0 if last else size, source,
                               1_000, 1_000_000, 0) + text
            blob += body + b"\x00" * (size - len(body))
        return blob

    def _source_consumer(self, etw, blob):
        consumer = etw.EtwPmcConsumer(session_name="MBCX01-BUILD-B-PMC-WITNESS")
        consumer._win32 = etw._EtwWin32(
            advapi32=_FakeQueryApi({etw.TraceProfileSourceListInfo: blob}),
            kernel32=None)
        return consumer

    def test_bw80_positive_the_pinned_profile_source_is_found_by_its_whole_name(self):
        """A present source must resolve, wherever it sits in the chain.

        `Description` is a WCHAR array (evntrace.h line 1413), so the name ends
        at the first NUL CODE UNIT — a two-byte NUL on a two-byte boundary.
        Splitting the raw bytes on `b"\\x00\\x00"` matched the UNALIGNED pair
        made of the last character's high byte and the terminator's low byte,
        so `InstructionRetired` parsed as `InstructionRetire`; and
        `offset + next or len(raw)` evaluated to `offset` for a final entry at
        a nonzero offset, i.e. an EMPTY name. Either way the preflight reported
        `ETW_PMC_SOURCE_UNAVAILABLE` for a source the platform HAS, which
        refuses a healthy run before it starts.
        """
        etw = _etw()
        middle = self._source_list_blob(
            etw, [(1, "TotalCycles"), (2, win32.PMC_SOURCE_NAME),
                  (3, "BranchInstructions")])
        final = self._source_list_blob(
            etw, [(1, "TotalCycles"), (2, win32.PMC_SOURCE_NAME)])
        for name, blob in (("a middle chained entry", middle),
                           ("the final entry (NextEntryOffset == 0)", final)):
            with self.subTest(position=name):
                consumer = self._source_consumer(etw, blob)
                self.assertEqual(
                    consumer._resolve_profile_source_id(win32.PMC_SOURCE_NAME), 2)
        # The decoder itself: a code-unit terminator ends the name, a name with
        # no terminator at all is still read whole, and a trailing odd byte is
        # not a code unit.
        self.assertEqual(
            etw._profile_source_description(b"A\x00B\x00\x00\x00C\x00"), "AB")
        self.assertEqual(etw._profile_source_description(b"A\x00B\x00"), "AB")
        self.assertEqual(etw._profile_source_description(b"A\x00B\x00\x7f"), "AB")
        self.assertEqual(etw._profile_source_description(b""), "")
        # A name that merely CONTAINS the pinned one is not the pinned one.
        near = self._source_list_blob(etw, [(9, "InstructionRetiredFixed")])
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            self._source_consumer(etw, near)._resolve_profile_source_id(
                win32.PMC_SOURCE_NAME)
        self.assertIn("ETW_PMC_SOURCE_UNAVAILABLE", str(caught.exception))

    def test_bw81_adversarial_a_malformed_source_list_is_named_not_looped(self):
        """A chain this build cannot walk is a fault, never a silent absence.

        A `NextEntryOffset` that does not advance past the fixed prefix would
        re-read the same bytes forever, and a buffer that ends mid-prefix would
        raise a raw `ValueError` out of `from_buffer_copy`. Both are refused by
        name, and an EMPTY list stays the fault it already was.
        """
        etw = _etw()
        prefix_size = ctypes.sizeof(etw.PROFILE_SOURCE_INFO)
        short_next = struct.pack("<IIIIQ", 4, 1, 0, 0, 0) + b"\x00" * 8
        # A chain whose SECOND entry is cut off before its fixed prefix ends.
        two = self._source_list_blob(etw, [(1, "TotalCycles"), (2, "Other")])
        second_at = struct.unpack_from("<I", two, 0)[0]
        truncated = two[:second_at + prefix_size - 4]
        for name, blob, expected in (
                ("NextEntryOffset smaller than the prefix", short_next,
                 "ETW_PMC_SOURCE_LIST_MALFORMED:NextEntryOffset=4"),
                ("a buffer that ends mid-prefix", truncated,
                 "ETW_PMC_SOURCE_LIST_MALFORMED:truncated_entry")):
            with self.subTest(case=name):
                with self.assertRaises(etw.EtwConsumerFault) as caught:
                    self._source_consumer(etw, blob)._resolve_profile_source_id(
                        win32.PMC_SOURCE_NAME)
                self.assertIn(expected, str(caught.exception))
        consumer = etw.EtwPmcConsumer(session_name="MBCX01-BUILD-B-PMC-WITNESS")
        consumer._win32 = etw._EtwWin32(
            advapi32=_FakeQueryApi({etw.TraceProfileSourceListInfo: b""}),
            kernel32=None)
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            consumer._resolve_profile_source_id(win32.PMC_SOURCE_NAME)
        self.assertIn("TraceProfileSourceListInfo:EMPTY_SOURCE_LIST",
                      str(caught.exception))

    def test_bw82_positive_free_pmc_counters_are_not_an_ownership_conflict(self):
        """`NumberOfCounters` is metadata; only an owner row is an owner.

        evntrace.h lines 2345-2361 define TracePmcCounterOwners as a
        PER-PROCESSOR query whose input buffer is sized from
        TraceMaxPmcCounterQuery, answering with
        `ETW_PMC_COUNTER_OWNERSHIP_STATUS` — ProcessorNumber, NumberOfCounters,
        then that many `ETW_PMC_COUNTER_OWNER` rows. A healthy host with four
        unused counters therefore answers `NumberOfCounters = 4` beside four
        `EtwPmcOwnerFree` rows. Reading the buffer as opaque and calling any
        nonzero byte an owner reported that host as
        `ETW_PMC_COUNTER_OWNER_CONFLICT` and refused its evidence.
        """
        etw = _etw()
        free = [(etw.EtwPmcOwnerFree, 0, 0)] * 4
        owned = [(etw.EtwPmcOwnerFree, 0, 0), (etw.EtwPmcOwnerTagged, 2, 0x99),
                 (etw.EtwPmcOwnerFree, 0, 0), (etw.EtwPmcOwnerUntagged, 3, 0)]
        for name, rows, processors, expected in (
                ("every counter free, two processors", free, 2, 0),
                ("two owners per processor, two processors", owned, 2, 4),
                ("two owners on the only processor", owned, 1, 2)):
            with self.subTest(case=name):
                consumer = _ownership_consumer(etw, rows, processors=processors)
                self.assertEqual(consumer._count_counter_owners(4), expected)
        # End to end: the healthy host's facts are AVAILABLE evidence.
        consumer = _ownership_consumer(etw, free, processors=2)
        facts = consumer._query_capability_facts(2)
        self.assertEqual(facts["counter_owner_conflict_count"], 0)
        self.assertEqual(facts["max_pmc_counters"], 4)
        self.assertEqual(
            etw.evaluate_evidence_availability(
                capability_facts=facts, loss=etw.LossCounters(0, 0, 0)),
            (True, ()))
        # The rows themselves decode by the header layout, per processor.
        blob = _ownership_blob(3, owned)
        self.assertEqual(
            etw.pmc_counter_owner_rows(blob, max_counters=4),
            [{"processor_number": 3, "counter_index": 0, "owner_type": 0,
              "profile_source": 0, "owner_tag": 0},
             {"processor_number": 3, "counter_index": 1, "owner_type": 2,
              "profile_source": 2, "owner_tag": 0x99},
             {"processor_number": 3, "counter_index": 2, "owner_type": 0,
              "profile_source": 0, "owner_tag": 0},
             {"processor_number": 3, "counter_index": 3, "owner_type": 1,
              "profile_source": 3, "owner_tag": 0}])
        # A platform that grants no counters has no owner rows to ask about,
        # and the GRANT is what the availability rule names.
        consumer = _ownership_consumer(etw, [], processors=2)
        self.assertEqual(consumer._count_counter_owners(0), 0)
        self.assertIn("ETW_PMC_NO_COUNTERS_GRANTED",
                      etw.evaluate_evidence_availability(
                          capability_facts=etw.granted_capability_facts_for_test(
                              max_pmc_counters=0),
                          loss=etw.LossCounters(0, 0, 0))[1])

    def test_bw82_adversarial_an_unreadable_ownership_answer_is_refused(self):
        """A mis-sized or unknown ownership answer never becomes "nobody owns"."""
        etw = _etw()
        header = struct.pack("<II", 0, 4)
        for name, blob, max_counters, expected in (
                ("buffer shorter than the prefix", b"\x00\x00", 4,
                 "ETW_PMC_COUNTER_OWNERS_MALFORMED:short_buffer"),
                ("more rows than the platform's maximum",
                 _ownership_blob(0, [(0, 0, 0)] * 4), 2,
                 "ETW_PMC_COUNTER_OWNERS_MALFORMED:NumberOfCounters=4"),
                ("more rows than the buffer holds", header + b"\x00" * 12, 4,
                 "ETW_PMC_COUNTER_OWNERS_MALFORMED:NumberOfCounters=4")):
            with self.subTest(case=name):
                with self.assertRaises(etw.EtwConsumerFault) as caught:
                    etw.pmc_counter_owner_rows(blob, max_counters=max_counters)
                self.assertIn(expected, str(caught.exception))
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            etw.count_owned_pmc_counters([{"owner_type": 77}])
        self.assertIn("ETW_PMC_COUNTER_OWNER_TYPE_UNKNOWN:77", str(caught.exception))
        # A failed query is a fault, not a zero.
        consumer = etw.EtwPmcConsumer(session_name="MBCX01-BUILD-B-PMC-WITNESS")
        api = _FakeQueryApi({etw.TracePmcCounterOwners: b""}, status=5)
        api.processors = 1
        consumer._win32 = etw._EtwWin32(advapi32=api, kernel32=api)
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            consumer._count_counter_owners(4)
        self.assertIn("TraceQueryInformation(PmcCounterOwners,cpu=0):WIN32_ERROR=5",
                      str(caught.exception))

    def _busy_host_capture(self, etw, cswitch_records):
        """A one-member capture plus whatever CSwitch stream the case needs."""
        return etw.CapturedTrace(
            cswitch_records=list(cswitch_records),
            process_events=[
                {"kind": "START", "process_id": 4100, "process_start_key": 0x11,
                 "parent_process_id": None, "parent_process_start_key": None,
                 "qpc": 10},
                {"kind": "STOP", "process_id": 4100, "process_start_key": 0x11,
                 "qpc": 100}],
            thread_events=[
                {"kind": "START", "thread_id": 900, "process_id": 4100,
                 "process_start_key": 0x11, "qpc": 11},
                {"kind": "STOP", "thread_id": 900, "process_id": 4100,
                 "process_start_key": 0x11, "qpc": 99}],
            capability_facts=etw.granted_capability_facts_for_test(),
            loss=etw.LossCounters(0, 0, 0), session_handle=0x1234, source_id=2)

    def test_bw83_positive_foreign_switches_are_baselines_never_member_deltas(self):
        """A busy host must not abort, and must not be counted either.

        Every context switch on the box arrives on this session, so on a normal
        host most switches belong to threads the Job never held. Handing them to
        `consume_cswitch()` aborts the collection as
        `ETW_CSWITCH_UNATTRIBUTED_THREAD` after the candidate has run — a wrong
        diagnosis of right evidence.

        Dropping them would be just as wrong in the other direction: both
        `consume_cswitch()` and the frozen validator recompute each delta from
        the previous counter value on the same processor IN THE EMITTED STREAM,
        so raw counters minus the foreign rows would telescope the whole
        machine's work into the member's total. The foreign records are
        therefore used for exactly the arithmetic they are evidence for: a kept
        record's emitted counter is its raw counter minus the foreign work
        already accumulated on that processor, so each member delta is exactly
        the interval that member thread ran.
        """
        etw = _etw()
        # processor 0: foreign, member, foreign, member; processor 1: member only.
        records = [{"processor": 0, "qpc": 12, "old_thread_id": 7100,
                    "instruction_retired": 1_000},
                   {"processor": 0, "qpc": 14, "old_thread_id": 900,
                    "instruction_retired": 1_500},
                   {"processor": 0, "qpc": 16, "old_thread_id": 7200,
                    "instruction_retired": 2_500},
                   {"processor": 0, "qpc": 18, "old_thread_id": 900,
                    "instruction_retired": 2_700},
                   {"processor": 1, "qpc": 20, "old_thread_id": 900,
                    "instruction_retired": 5_000},
                   {"processor": 1, "qpc": 22, "old_thread_id": 900,
                    "instruction_retired": 5_050}]
        capture = self._busy_host_capture(etw, records)
        session = etw.make_etw_session_factory(
            capture, job_object_id="JOB.0.0.0", root_process_id=4100,
            root_process_start_key="0000000000000011")()
        self.assertEqual([(row["processor"], row["qpc"], row["old_thread_id"],
                           row["instruction_retired"]) for row in session.records()],
                         [(0, 14, 900, 1_500), (0, 18, 900, 1_700),
                          (1, 20, 900, 5_000), (1, 22, 900, 5_050)])
        observations = session.consume_cswitch()
        self.assertEqual([row["delta_from_previous"] for row in observations],
                         [500, 200, 0, 50])
        # AMENDMENT-3 (2026-08-16): 500 is exactly 1500-1000 — the interval
        # thread 900 ran on processor 0 BEFORE its first switch-out, counted
        # from the foreign predecessor's baseline. This assertion previously
        # expected 0 here: the banked expectation encoded the undercount the
        # amendment closes (the r6 NO-GO). 200 is exactly 2700-2500 and 50 is
        # exactly 5050-5000. Processor 1 begins AT the member switch-out — no
        # predecessor, no baseline, so its first delta stays the declared
        # capture-start zero. The 1000 instructions retired between qpc 14 and
        # qpc 16 belong to a foreign thread and are counted nowhere.
        self.assertEqual(sum(row["delta_from_previous"] for row in observations), 750)
        self.assertEqual({row["process_id"] for row in observations}, {4100})
        # Exclusion is scoping, never silencing: every number is on the capture.
        self.assertEqual(capture.provenance["cswitch_scope"],
                         "JOB_MEMBER_THREAD_ROSTER")
        self.assertEqual(capture.provenance["member_attributed_cswitch_records"], 4)
        self.assertEqual(capture.provenance["excluded_foreign_cswitch_records"], 2)
        self.assertEqual(
            capture.provenance["foreign_instructions_excluded_after_first_member"],
            1_000)
        self.assertEqual(capture.provenance["per_processor_baseline_records"], 2)
        scope = etw.scope_cswitch_records_to_members(
            records, [{"thread_id": 900, "process_id": 4100,
                       "process_start_key": "0000000000000011",
                       "started_qpc": 11, "ended_qpc": 99}])
        self.assertEqual([row["old_thread_id"] for row in scope.excluded],
                         [7100, 7200])
        self.assertEqual([row["instruction_retired"] for row in scope.excluded],
                         [1_000, 2_500])
        # With NO foreign switch the subtraction is zero and the emitted
        # counters are the RAW ones, byte for byte.
        quiet = [{"processor": 0, "qpc": 14, "old_thread_id": 900,
                  "instruction_retired": 1_000},
                 {"processor": 0, "qpc": 18, "old_thread_id": 900,
                  "instruction_retired": 1_700}]
        quiet_capture = self._busy_host_capture(etw, quiet)
        quiet_session = etw.make_etw_session_factory(
            quiet_capture, job_object_id="JOB.0.0.0", root_process_id=4100,
            root_process_start_key="0000000000000011")()
        self.assertEqual([row["instruction_retired"]
                          for row in quiet_session.records()], [1_000, 1_700])
        self.assertEqual([row["delta_from_previous"]
                          for row in quiet_session.consume_cswitch()], [0, 700])
        self.assertEqual(
            quiet_capture.provenance["excluded_foreign_cswitch_records"], 0)

    def test_bw84_adversarial_member_cswitch_inconsistencies_keep_their_faults(self):
        """Scoping must not silence a statement about MEMBER evidence.

        A switch whose outgoing TID is in the signed roster is KEPT even when
        its QPC falls inside none of that TID's lifetimes — the stream
        disagreeing with itself about a member — and `consume_cswitch()` still
        refuses it by name. A counter that goes BACKWARDS across a foreign
        interval is refused here, because after exclusion nothing downstream
        would ever see that step. And a stream that is not in per-processor
        order is refused rather than rebased against the wrong predecessor.
        """
        etw = _etw()
        roster = [{"thread_id": 900, "process_id": 4100,
                   "process_start_key": "0000000000000011",
                   "started_qpc": 11, "ended_qpc": 99}]
        outside = [{"processor": 0, "qpc": 12, "old_thread_id": 7100,
                    "instruction_retired": 1_000},
                   {"processor": 0, "qpc": 500, "old_thread_id": 900,
                    "instruction_retired": 1_500}]
        scope = etw.scope_cswitch_records_to_members(outside, roster)
        self.assertEqual([row["qpc"] for row in scope.records], [500])
        capture = self._busy_host_capture(etw, outside)
        session = etw.make_etw_session_factory(
            capture, job_object_id="JOB.0.0.0", root_process_id=4100,
            root_process_start_key="0000000000000011")()
        with self.assertRaises(win32.CollectorFault) as caught:
            session.consume_cswitch()
        self.assertIn("ETW_CSWITCH_UNATTRIBUTED_THREAD", str(caught.exception))
        for name, records, expected in (
                ("a foreign interval whose counter went backwards",
                 [{"processor": 0, "qpc": 12, "old_thread_id": 900,
                   "instruction_retired": 1_000},
                  {"processor": 0, "qpc": 14, "old_thread_id": 7100,
                   "instruction_retired": 900}],
                 "ETW_PMC_COUNTER_WENT_BACKWARDS:0@14"),
                ("a stream that is not in per-processor order",
                 [{"processor": 0, "qpc": 20, "old_thread_id": 900,
                   "instruction_retired": 1_000},
                  {"processor": 0, "qpc": 14, "old_thread_id": 900,
                   "instruction_retired": 1_100}],
                 "ETW_CSWITCH_RECORDS_UNORDERED:0@14"),
                ("a record that is not a record", [42],
                 "ETW_CSWITCH_RECORD_INCOMPLETE:not_a_record"),
                ("a record missing its counter",
                 [{"processor": 0, "qpc": 14, "old_thread_id": 900}],
                 "ETW_CSWITCH_RECORD_INCOMPLETE:instruction_retired")):
            with self.subTest(case=name):
                with self.assertRaises(etw.EtwConsumerFault) as caught:
                    etw.scope_cswitch_records_to_members(records, roster)
                self.assertIn(expected, str(caught.exception))
        # A backwards step ending at a MEMBER record is still the downstream
        # refusal it has always been, unchanged by the scope.
        backwards = self._busy_host_capture(
            etw, [{"processor": 0, "qpc": 12, "old_thread_id": 900,
                   "instruction_retired": 1_000},
                  {"processor": 0, "qpc": 14, "old_thread_id": 900,
                   "instruction_retired": 900}])
        session = etw.make_etw_session_factory(
            backwards, job_object_id="JOB.0.0.0", root_process_id=4100,
            root_process_start_key="0000000000000011")()
        with self.assertRaises(win32.CollectorFault) as caught:
            session.consume_cswitch()
        self.assertIn("ETW_PMC_COUNTER_WENT_BACKWARDS", str(caught.exception))
        # A thread roster row without a thread id cannot decide membership.
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            etw.scope_cswitch_records_to_members([], [{"process_id": 4100}])
        self.assertIn("ETW_THREAD_LIFETIME_ROW_INVALID", str(caught.exception))

    # --- council r6 FOLD-A: lifetime-aware scope, version gate, denominator ---
    #
    # bw75-bw79 are THIS fold's witnesses. bw70-bw74 were ALREADY TAKEN by the
    # live-cell fold below (`BuildCollectorLivePathTests`), so this block uses
    # the free tail of the range rather than renumbering anybody.

    def _tid_reuse_capture(self, etw, cswitch_records):
        """A capture in which the HOST reuses the member's TID after it dies.

        Member process 4100 [10,100] holds thread 900 [11,40] and thread 901
        [11,99]. Host process 7777 [46,90] then gets TID 900 back at qpc 50 —
        an ordinary Windows TID reuse ("The operating system may reuse a thread
        ID after the thread has terminated", *PsGetThreadId* Remarks), and the
        exact stream all three r6 seats constructed independently.
        """
        return etw.CapturedTrace(
            cswitch_records=list(cswitch_records),
            process_events=[
                {"kind": "START", "process_id": 4100, "process_start_key": 0x11,
                 "parent_process_id": None, "parent_process_start_key": None,
                 "qpc": 10},
                {"kind": "STOP", "process_id": 4100, "process_start_key": 0x11,
                 "qpc": 100},
                {"kind": "START", "process_id": 7777, "process_start_key": 0x77,
                 "parent_process_id": 6666, "parent_process_start_key": None,
                 "qpc": 46},
                {"kind": "STOP", "process_id": 7777, "process_start_key": 0x77,
                 "qpc": 90}],
            thread_events=[
                {"kind": "START", "thread_id": 900, "process_id": 4100,
                 "process_start_key": 0x11, "qpc": 11},
                {"kind": "STOP", "thread_id": 900, "process_id": 4100,
                 "process_start_key": 0x11, "qpc": 40},
                {"kind": "START", "thread_id": 901, "process_id": 4100,
                 "process_start_key": 0x11, "qpc": 11},
                {"kind": "STOP", "thread_id": 901, "process_id": 4100,
                 "process_start_key": 0x11, "qpc": 99},
                # The host's incarnation of the SAME TID, already separated by
                # `partition_job_member_events()`.
                {"kind": "START", "thread_id": 900, "process_id": 7777,
                 "process_start_key": 0x77, "qpc": 50},
                {"kind": "STOP", "thread_id": 900, "process_id": 7777,
                 "process_start_key": 0x77, "qpc": 80}],
            capability_facts=etw.granted_capability_facts_for_test(),
            loss=etw.LossCounters(0, 0, 0), session_handle=0x1234, source_id=2)

    def test_bw75_positive_a_reused_tid_inside_a_known_foreign_life_is_excluded(self):
        """An ordinary TID reuse must not destroy a valid capture.

        The scope used to keep any record whose `old_thread_id` appears
        ANYWHERE in the member roster, whatever its QPC. A dead member TID that
        the host recycles mid-capture therefore reached `consume_cswitch()`,
        which refused it as `ETW_CSWITCH_UNATTRIBUTED_THREAD` — the whole
        collection aborted, after the candidate had run, on a documented
        Windows behaviour. That is right evidence refused.

        The evidence that tells the two incarnations apart is ALREADY DERIVED:
        `partition_job_member_events()` separates the foreign thread events, and
        `capture()` now carries that half forward. A record whose QPC lands
        inside a KNOWN FOREIGN lifetime of that TID is therefore classified
        exactly like any other foreign record — baseline/offset arithmetic, not
        kept — and the capture survives.

        ⚠ CLASSIFICATION ONLY. The kept record's emitted counter is still its
        raw counter minus the foreign work accumulated on that processor, so
        the delta downstream recomputes is still exactly
        `raw(this) - raw(previous)`: 400 = 3400 - 3000, the interval thread 901
        actually ran, with the recycled TID's 2000 instructions subtracted.
        """
        etw = _etw()
        records = [{"processor": 0, "qpc": 20, "old_thread_id": 900,
                    "instruction_retired": 1_000},
                   # TID 900 again — but this is the HOST's thread 900.
                   {"processor": 0, "qpc": 60, "old_thread_id": 900,
                    "instruction_retired": 3_000},
                   {"processor": 0, "qpc": 70, "old_thread_id": 901,
                    "instruction_retired": 3_400}]
        capture = self._tid_reuse_capture(etw, records)
        session = etw.make_etw_session_factory(
            capture, job_object_id="JOB.0.0.0", root_process_id=4100,
            root_process_start_key="0000000000000011")()
        self.assertEqual([(row["qpc"], row["old_thread_id"],
                           row["instruction_retired"])
                          for row in session.records()],
                         [(20, 900, 1_000), (70, 901, 1_400)])
        observations = session.consume_cswitch()
        self.assertEqual([row["delta_from_previous"] for row in observations],
                         [0, 400])
        self.assertEqual(capture.provenance["excluded_foreign_cswitch_records"], 1)
        self.assertEqual(
            capture.provenance["foreign_instructions_excluded_after_first_member"],
            2_000)
        self.assertEqual(
            capture.provenance["kept_roster_tid_outside_any_lifetime"], 0)
        # The scope itself, called directly with the partition's own evidence.
        roster = [{"thread_id": 900, "process_id": 4100,
                   "process_start_key": "0000000000000011",
                   "started_qpc": 11, "ended_qpc": 40},
                  {"thread_id": 901, "process_id": 4100,
                   "process_start_key": "0000000000000011",
                   "started_qpc": 11, "ended_qpc": 99}]
        foreign_events = [{"kind": "START", "thread_id": 900,
                           "process_id": 7777, "qpc": 50},
                          {"kind": "STOP", "thread_id": 900,
                           "process_id": 7777, "qpc": 80}]
        scope = etw.scope_cswitch_records_to_members(
            records, roster, foreign_thread_events=foreign_events)
        self.assertEqual([row["qpc"] for row in scope.excluded], [60])
        self.assertEqual(scope.foreign_instructions, 2_000)
        self.assertEqual(scope.roster_tid_outside_any_lifetime, 0)
        # With NO foreign-lifetime evidence in hand the old fail-loud posture is
        # exactly what is left: the record is kept and counted as unplaceable.
        blind = etw.scope_cswitch_records_to_members(records, roster)
        self.assertEqual([row["qpc"] for row in blind.records], [20, 60, 70])
        self.assertEqual(blind.roster_tid_outside_any_lifetime, 1)
        # The LIVE path gets the same evidence: `capture()` partitions, and the
        # foreign half now travels on the capture instead of being dropped.
        consumer = self._decode(etw, [
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START,
             _process_start_payload(4100, 0x11), 4000, 10),
            (etw.KERNEL_PROCESS_EVENT_ID_THREAD_START,
             struct.pack("<II", 4100, 900), 4100, 11),
            (etw.KERNEL_PROCESS_EVENT_ID_THREAD_STOP,
             struct.pack("<II", 4100, 900), 4100, 40),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START,
             _process_start_payload(7777, 0x77), 6666, 46),
            (etw.KERNEL_PROCESS_EVENT_ID_THREAD_START,
             struct.pack("<II", 7777, 900), 7777, 50),
            (etw.KERNEL_PROCESS_EVENT_ID_THREAD_STOP,
             struct.pack("<II", 7777, 900), 7777, 80),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_STOP,
             _process_stop_payload(7777, 0x77), 7777, 90),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_STOP,
             _process_stop_payload(4100, 0x11), 4100, 100)])
        live = consumer.capture(root_process_id=4100,
                                root_process_start_key="0000000000000011")
        self.assertEqual([(row["kind"], row["thread_id"], row["process_id"])
                          for row in live.foreign_thread_events],
                         [("START", 900, 7777), ("STOP", 900, 7777)])
        live.cswitch_records = [{"processor": 0, "qpc": 20,
                                 "old_thread_id": 900,
                                 "instruction_retired": 1_000},
                                {"processor": 0, "qpc": 60,
                                 "old_thread_id": 900,
                                 "instruction_retired": 3_000}]
        live_session = etw.make_etw_session_factory(
            live, job_object_id="JOB.0.0.0", root_process_id=4100,
            root_process_start_key="0000000000000011")()
        self.assertEqual([row["qpc"] for row in live_session.records()], [20])
        self.assertEqual([row["delta_from_previous"]
                          for row in live_session.consume_cswitch()], [0])

    def test_bw76_adversarial_a_tid_in_no_known_life_still_faults_and_is_counted(self):
        """The genuinely ambiguous case keeps its fault AND becomes a number.

        A roster TID observed when neither the member lifetime nor any KNOWN
        foreign lifetime contains its QPC is the case that cannot be resolved
        from inside the stream. The posture there is unchanged — the record is
        kept, `consume_cswitch()` refuses it by name, no receipt is signed — but
        the operator of the aborted capture can now tell "the host recycled a
        TID we cannot place" from "the roster is incomplete", because the count
        is on the capture's provenance BEFORE the refusal.
        """
        etw = _etw()
        records = [{"processor": 0, "qpc": 20, "old_thread_id": 900,
                    "instruction_retired": 1_000},
                   # After the member thread AND the host's incarnation of 900
                   # are both gone: inside no lifetime this capture knows.
                   {"processor": 0, "qpc": 95, "old_thread_id": 900,
                    "instruction_retired": 4_000}]
        capture = self._tid_reuse_capture(etw, records)
        session = etw.make_etw_session_factory(
            capture, job_object_id="JOB.0.0.0", root_process_id=4100,
            root_process_start_key="0000000000000011")()
        self.assertEqual([row["qpc"] for row in session.records()], [20, 95])
        self.assertEqual(
            capture.provenance["kept_roster_tid_outside_any_lifetime"], 1)
        self.assertEqual(capture.provenance["member_attributed_cswitch_records"], 2)
        with self.assertRaises(win32.CollectorFault) as caught:
            session.consume_cswitch()
        self.assertIn("ETW_CSWITCH_UNATTRIBUTED_THREAD", str(caught.exception))
        # A TID that is in NO roster at all is foreign as it always was, and is
        # never counted as an unplaceable roster TID.
        stranger = etw.scope_cswitch_records_to_members(
            [{"processor": 0, "qpc": 20, "old_thread_id": 900,
              "instruction_retired": 1_000},
             {"processor": 0, "qpc": 30, "old_thread_id": 7100,
              "instruction_retired": 1_500}],
            [{"thread_id": 900, "process_id": 4100,
              "process_start_key": "0000000000000011",
              "started_qpc": 11, "ended_qpc": 40}])
        self.assertEqual([row["qpc"] for row in stranger.excluded], [30])
        self.assertEqual(stranger.roster_tid_outside_any_lifetime, 0)

    def test_bw77_adversarial_an_unverified_thread_event_version_is_refused(self):
        """A thread payload template this build never read is never decoded.

        `KERNEL_THREAD_PAYLOAD_VERSIONS_VERIFIED` pinned the two published
        versions and was then consumed NOWHERE: the ThreadStart/ThreadStop
        branch decoded ANY version with eight payload bytes, so a future
        version whose first eight bytes are not `ProcessID, ThreadID` would be
        read at guessed offsets and could feed a fabricated TID into the signed
        roster. The process branch has always version-gated; this is the same
        mechanism on the thread branch.
        """
        etw = _etw()
        consumer = etw.EtwPmcConsumer(session_name="MBCX01-BUILD-B-PMC-WITNESS")
        consumer._win32 = etw._EtwWin32(advapi32=_FakeTraceApi(), kernel32=None)
        consumer._capability_facts = etw.granted_capability_facts_for_test()
        for event_id in (etw.KERNEL_PROCESS_EVENT_ID_THREAD_START,
                         etw.KERNEL_PROCESS_EVENT_ID_THREAD_STOP):
            with self.subTest(event_id=event_id):
                record, _buffer = _kernel_process_record(
                    etw, event_id=event_id,
                    payload=struct.pack("<II", 4100, 900),
                    logging_process_id=4100, timestamp=11, version=9)
                with self.assertRaises(etw.EtwConsumerFault) as caught:
                    consumer._decode_kernel_process_event(record, 11)
                self.assertIn("ETW_KERNEL_THREAD_VERSION_UNVERIFIED",
                              str(caught.exception))
                self.assertIn("version=9", str(caught.exception))
        self.assertEqual(consumer._thread_events, [])
        # The pinned frozenset is now READ, not merely declared.
        self.assertIn("KERNEL_THREAD_PAYLOAD_VERSIONS_VERIFIED",
                      inspect.getsource(
                          etw.EtwPmcConsumer._decode_kernel_process_event))
        # And through the REAL callback the fault is carried to `capture()`
        # rather than swallowed, exactly like every other decode fault.
        live = etw.EtwPmcConsumer(session_name="MBCX01-BUILD-B-PMC-WITNESS")
        live._win32 = etw._EtwWin32(advapi32=_FakeTraceApi(), kernel32=None)
        live._capability_facts = etw.granted_capability_facts_for_test()
        alive = []
        for event_id, payload, logging_pid, timestamp, version in (
                (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START,
                 _process_start_payload(4100, 0x11), 4000, 10, None),
                (etw.KERNEL_PROCESS_EVENT_ID_THREAD_START,
                 struct.pack("<II", 4100, 900), 4100, 11, 9),
                (etw.KERNEL_PROCESS_EVENT_ID_THREAD_STOP,
                 struct.pack("<II", 4100, 900), 4100, 29, None),
                (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_STOP,
                 _process_stop_payload(4100, 0x11), 4100, 30, None)):
            record, buffer = _kernel_process_record(
                etw, event_id=event_id, payload=payload,
                logging_process_id=logging_pid, timestamp=timestamp,
                version=version)
            alive.append((record, buffer))
            live._on_event_record(ctypes.pointer(record))
        live.stop()
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            live.capture(root_process_id=4100,
                         root_process_start_key="0000000000000011")
        self.assertIn("ETW_CONSUMER_CALLBACK_FAULT", str(caught.exception))
        self.assertIn("ETW_KERNEL_THREAD_VERSION_UNVERIFIED", str(caught.exception))

    def test_bw78_positive_guard_both_verified_thread_versions_still_decode(self):
        """GUARD: the version gate must refuse nothing that was verified.

        Versions 0 and 1 are the two published templates
        (`KERNEL_THREAD_PAYLOAD_VERSIONS_VERIFIED`), and both begin
        `ProcessID u32 @0, ThreadID u32 @4`. Both must still decode to the same
        event they decoded to before the gate existed — a gate that refuses
        right evidence is the failure this build class exists to prevent.
        """
        etw = _etw()
        consumer = etw.EtwPmcConsumer(session_name="MBCX01-BUILD-B-PMC-WITNESS")
        consumer._win32 = etw._EtwWin32(advapi32=_FakeTraceApi(), kernel32=None)
        consumer._capability_facts = etw.granted_capability_facts_for_test()
        self.assertEqual(etw.KERNEL_THREAD_PAYLOAD_VERSIONS_VERIFIED,
                         frozenset({0, 1}))
        for version in sorted(etw.KERNEL_THREAD_PAYLOAD_VERSIONS_VERIFIED):
            for event_id, kind in (
                    (etw.KERNEL_PROCESS_EVENT_ID_THREAD_START, "START"),
                    (etw.KERNEL_PROCESS_EVENT_ID_THREAD_STOP, "STOP")):
                with self.subTest(version=version, kind=kind):
                    record, _buffer = _kernel_process_record(
                        etw, event_id=event_id,
                        payload=struct.pack("<II", 4100, 900),
                        logging_process_id=4100, timestamp=11 + version,
                        version=version)
                    consumer._decode_kernel_process_event(record, 11 + version)
        self.assertEqual([(row["kind"], row["thread_id"], row["process_id"],
                           row["qpc"]) for row in consumer._thread_events],
                         [("START", 900, 4100, 11), ("STOP", 900, 4100, 11),
                          ("START", 900, 4100, 12), ("STOP", 900, 4100, 12)])

    def test_bw79_positive_the_foreign_instruction_field_names_its_denominator(self):
        """Two provenance numbers, two different denominators — said out loud.

        `excluded_foreign_cswitch_records` counts EVERY excluded record.
        The instruction total accumulates only the steps taken AFTER that
        processor's first member record, because foreign work before it is
        outside the emitted chain and is deliberately not subtracted. An
        auditor dividing one by the other got a number that means nothing, and
        the dict said so nowhere. The field now carries its own denominator in
        its name, and the docstring states it.
        """
        etw = _etw()
        roster = [{"thread_id": 900, "process_id": 4100,
                   "process_start_key": "0000000000000011",
                   "started_qpc": 11, "ended_qpc": 99}]
        records = [{"processor": 0, "qpc": 12, "old_thread_id": 7100,
                    "instruction_retired": 1_000},
                   {"processor": 0, "qpc": 14, "old_thread_id": 7100,
                    "instruction_retired": 1_100},
                   {"processor": 0, "qpc": 16, "old_thread_id": 900,
                    "instruction_retired": 1_200},
                   {"processor": 0, "qpc": 18, "old_thread_id": 7200,
                    "instruction_retired": 1_330},
                   {"processor": 0, "qpc": 20, "old_thread_id": 900,
                    "instruction_retired": 1_400}]
        scope = etw.scope_cswitch_records_to_members(records, roster)
        provenance = etw.record_cswitch_scope_provenance(scope)
        # Three records excluded; only the 130 after the first member record
        # was subtracted from anything. 3 and 130 have no common denominator.
        self.assertEqual(provenance["excluded_foreign_cswitch_records"], 3)
        self.assertEqual(
            provenance["foreign_instructions_excluded_after_first_member"], 130)
        self.assertNotIn("foreign_instructions_excluded", provenance)
        self.assertEqual(set(provenance),
                         {"cswitch_scope", "member_attributed_cswitch_records",
                          "excluded_foreign_cswitch_records",
                          "foreign_instructions_excluded_after_first_member",
                          "per_processor_baseline_records",
                          "kept_roster_tid_outside_any_lifetime"})
        self.assertIn("after that processor's first member record",
                      etw.record_cswitch_scope_provenance.__doc__)
        # The arithmetic is UNCHANGED by the rename: the emitted counters are
        # still raw minus the foreign work accumulated after the baseline.
        self.assertEqual([row["instruction_retired"] for row in scope.records],
                         [1_200, 1_270])

    # ------------------------------------------------------------------
    # AMENDMENT-3 (2026-08-16): the first member interval per processor is
    # counted from the predecessor baseline. Pre-amendment RED, driver-banked
    # on the pre-A3 worktree bytes (consumer blob 3f218eb3…, win32 blob
    # 66e55b2a…): the stream below produced deltas [0, 100], aggregate 100,
    # where the stream proves 1,000,100 — twice the 500,000 boundedness
    # threshold, invisible to provenance.
    # ------------------------------------------------------------------

    @staticmethod
    def _seat3_records():
        def rec(qpc, tid, counter):
            return {"qpc": qpc, "old_thread_id": tid, "processor": 0,
                    "instruction_retired": counter}
        return [rec(10, 999, 100), rec(20, 700, 1_000_100),
                rec(30, 700, 1_000_200)]

    @staticmethod
    def _scope(records, roster):
        return _etw().scope_cswitch_records_to_members(records, roster)

    @staticmethod
    def _member_roster():
        return [{"thread_id": 700, "process_id": 4100,
                 "process_start_key": "0000000000000001",
                 "started_qpc": 5, "ended_qpc": 500}]

    def _session_for(self, scope, roster):
        return win32.EtwPmcSession(
            session_handle=1, capability={}, attachment={}, observations=[],
            thread_lifetimes=roster, record_stream=lambda: list(scope.records),
            member_lifetimes=[], event_id_blob=b"", capability_facts={},
            first_member_baselines=scope.first_member_baselines,
            trace_finalizer=lambda session: None)

    def test_bw87_positive_the_first_member_interval_is_counted(self):
        """RED pre-A3: deltas [0, 100], aggregate 100 — the wrong number.

        The scope now records the foreign predecessor's raw counter as the
        processor's baseline, and consume_cswitch seeds its delta rule from
        it: the first member delta is the member's actual first interval.
        """
        roster = self._member_roster()
        scope = self._scope(self._seat3_records(), roster)
        self.assertEqual(scope.first_member_baselines,
                         ({"processor": 0, "counter_value": 100},))
        observations = self._session_for(scope, roster).consume_cswitch()
        self.assertEqual(
            [row["delta_from_previous"] for row in observations],
            [1_000_000, 100])
        self.assertEqual(
            sum(row["delta_from_previous"] for row in observations), 1_000_100)

    def test_bw88_positive_capture_start_emits_its_own_counter_as_baseline(self):
        """A stream that BEGINS at the member switch-out has no predecessor:
        the r7 totality rule emits a row anyway, carrying the first record's
        OWN counter, so the first delta stays the declared zero-truncation
        while an absent row stops being expressible for an observed processor
        (the forgotten-field shape three seats executed at r7)."""
        roster = self._member_roster()
        scope = self._scope(self._seat3_records()[1:], roster)
        self.assertEqual(scope.first_member_baselines,
                         ({"processor": 0, "counter_value": 1_000_100},))
        observations = self._session_for(scope, roster).consume_cswitch()
        self.assertEqual(
            [row["delta_from_previous"] for row in observations], [0, 100])

    def test_bw90_adversarial_an_omitting_producer_caller_faults_before_signing(self):
        """The pre-AMENDMENT-3 caller shape is unconstructible: omitting the
        baseline observation faults at SimulatedCollection construction —
        before anything is signed (r7, SEAT2's end-to-end executed wrong-by-
        1,000,000; the field deliberately has NO default)."""
        import dataclasses as _dc
        field_names = {f.name for f in _dc.fields(producer.SimulatedCollection)}
        self.assertIn("cswitch_first_member_baselines", field_names)
        required = {f.name for f in _dc.fields(producer.SimulatedCollection)
                    if f.default is _dc.MISSING
                    and f.default_factory is _dc.MISSING}
        self.assertIn("cswitch_first_member_baselines", required)

    def test_bw91_positive_a_leading_foreign_stop_is_a_prefix_interval(self):
        """SEAT2's executed r7 shape: a host thread that predates the trace
        stops at QPC 50; the member later receives the recycled TID. The
        pre-existing thread's switch at QPC 40 is now classified foreign via
        the capture-prefix interval instead of aborting the capture. RED
        pre-r7-fold: kept both records, ambiguous 1, consume faulted
        ETW_CSWITCH_UNATTRIBUTED_THREAD."""
        etw = _etw()
        roster = [{"thread_id": 900, "process_id": 4100,
                   "process_start_key": "0000000000000001",
                   "started_qpc": 60, "ended_qpc": 90}]
        foreign_events = [{"kind": "STOP", "thread_id": 900,
                           "process_id": 5000, "qpc": 50}]
        records = [
            {"qpc": 40, "old_thread_id": 900, "processor": 0,
             "instruction_retired": 1_000},
            {"qpc": 70, "old_thread_id": 900, "processor": 0,
             "instruction_retired": 1_400}]
        scope = etw.scope_cswitch_records_to_members(
            records, roster, foreign_events)
        self.assertEqual([row["qpc"] for row in scope.records], [70])
        self.assertEqual(len(scope.excluded), 1)
        self.assertEqual(scope.roster_tid_outside_any_lifetime, 0)
        self.assertEqual(scope.first_member_baselines,
                         ({"processor": 0, "counter_value": 1_000},))
        observations = self._session_for(scope, roster).consume_cswitch()
        self.assertEqual(
            [row["delta_from_previous"] for row in observations], [400])

    def test_bw92_adversarial_member_and_foreign_intervals_cannot_overlap(self):
        """SEAT2's r8 shape: one TID claimed alive as BOTH a member and a
        foreign thread at the same instant is an internally contradictory
        trace, not an ambiguity — the member-first rule would silently pick a
        side and attribute a delta under ownership the stream contradicts.

        RED pre-r8-fold: the overlap was admitted, deltas [0, 300] signed.
        A TID is unique system-wide while its thread lives (PsGetThreadId), so
        this input is platform-impossible; the check is a consistency gate
        between two of our OWN derived structures, at correctness volume."""
        etw = _etw()
        roster = [{"thread_id": 900, "process_id": 4100,
                   "process_start_key": "0000000000000001",
                   "started_qpc": 40, "ended_qpc": 80}]
        foreign_events = [{"kind": "STOP", "thread_id": 900,
                           "process_id": 5000, "qpc": 50}]
        records = [{"qpc": 45, "old_thread_id": 900, "processor": 0,
                    "instruction_retired": 1_000},
                   {"qpc": 70, "old_thread_id": 900, "processor": 0,
                    "instruction_retired": 1_300}]
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            etw.scope_cswitch_records_to_members(records, roster, foreign_events)
        self.assertIn("ETW_THREAD_MEMBER_FOREIGN_INTERVAL_OVERLAP",
                      str(caught.exception))
        # The DISJOINT arrangement bw91 relies on is untouched: the foreign
        # prefix ends before the member's life begins.
        disjoint = [dict(roster[0], started_qpc=60, ended_qpc=90)]
        scope = etw.scope_cswitch_records_to_members(
            records, disjoint, foreign_events)
        self.assertEqual([row["qpc"] for row in scope.records], [70])

    def test_bw93_pin_a_malformed_roster_row_faults_by_name(self):
        """PIN, NOT A RED — labelled as such (driver-verified: this passes on
        the pre-r8 bytes too, because the r7 fold already emitted the name).

        The r7 fold created ETW_THREAD_ROSTER_ROW_INVALID and nothing pinned
        it (SEAT1 r8 F6 — its own r7 finding's name, unwitnessed). Unpinned
        vocabulary is a name a refactor can drop with every suite still green,
        which is the rule this lane already ruled at r6 4(3). Its job begins
        now: it discriminates against a future silent rename or a reversion to
        a raw KeyError, not against the r7 bytes."""
        for row in ({"thread_id": 900}, None,
                    {"thread_id": 900, "process_id": 1,
                     "process_start_key": "x", "started_qpc": 10}):
            with self.subTest(row=row):
                with self.assertRaises(win32.CollectorFault) as caught:
                    win32.resolve_thread_lifetime([row], 900, 50)
                self.assertIn("ETW_THREAD_ROSTER_ROW_INVALID",
                              str(caught.exception))

    def test_bw89_adversarial_a_malformed_baseline_faults_by_name(self):
        """A baseline the session cannot trust is a fault, never a silent
        zero — wrong shape, negative value, or duplicate processor."""
        roster = self._member_roster()
        scope = self._scope(self._seat3_records(), roster)
        for rows in (({"processor": 0},),
                     ({"processor": 0, "counter_value": -1},),
                     ({"processor": 0, "counter_value": 1},
                      {"processor": 0, "counter_value": 2})):
            with self.subTest(rows=rows):
                session = win32.EtwPmcSession(
                    session_handle=1, capability={}, attachment={},
                    observations=[], thread_lifetimes=roster,
                    record_stream=lambda: list(scope.records),
                    member_lifetimes=[], event_id_blob=b"",
                    capability_facts={}, first_member_baselines=rows,
                    trace_finalizer=lambda session: None)
                with self.assertRaises(win32.CollectorFault) as caught:
                    session.consume_cswitch()
                self.assertIn("ETW_CSWITCH_BASELINE_INVALID",
                              str(caught.exception))


def _ownership_blob(processor, owners):
    """One processor's `ETW_PMC_COUNTER_OWNERSHIP_STATUS` answer, as bytes.

    ProcessorNumber, NumberOfCounters, then one 12-byte
    `ETW_PMC_COUNTER_OWNER` (OwnerType, ProfileSource, OwnerTag) per row —
    the layout read verbatim out of the installed SDK header, evntrace.h
    lines 1423-1433.
    """
    blob = struct.pack("<II", int(processor), len(owners))
    for owner_type, profile_source, owner_tag in owners:
        blob += struct.pack("<III", int(owner_type), int(profile_source),
                            int(owner_tag))
    return blob


def _ownership_consumer(etw, owners, *, processors):
    """A consumer whose fake platform answers the PER-PROCESSOR ownership query."""
    def per_processor(input_bytes):
        processor = (struct.unpack_from("<I", input_bytes, 0)[0]
                     if len(input_bytes) >= 4 else 0)
        return _ownership_blob(processor, owners)

    api = _FakeQueryApi({etw.TracePmcCounterOwners: per_processor,
                         etw.TraceMaxPmcCounterQuery: struct.pack("<I", 4)})
    api.processors = int(processors)
    consumer = etw.EtwPmcConsumer(session_name="MBCX01-BUILD-B-PMC-WITNESS")
    consumer._win32 = etw._EtwWin32(advapi32=api, kernel32=api)
    return consumer


class _FakeQueryApi:
    """A `TraceQueryInformation` stand-in that hands back scripted buffers.

    ⛔ Touches NO ETW state: it opens no session, queries no PMU and reads no
    processor. It answers the two shapes the real API has — a size probe with
    a NULL buffer, and a call with a caller-supplied buffer — so the consumer's
    OWN parsing and sizing logic is what the witness exercises. A scripted
    payload may be a callable, which receives the caller's INPUT buffer bytes;
    that is how the per-processor ownership query is answered per processor.
    """

    def __init__(self, blobs, *, status=0):
        self.blobs = dict(blobs)
        self.status = int(status)
        self.processors = 1
        self.calls = []

    def GetActiveProcessorCount(self, group):  # noqa: N802 - the Win32 spelling
        self.calls.append(("GetActiveProcessorCount", int(group)))
        return int(self.processors)

    def TraceQueryInformation(self, handle, info_class, buffer, length,  # noqa: N802
                              returned):
        payload = self.blobs[int(info_class)]
        destination = None if buffer is None else getattr(buffer, "_obj", buffer)
        if callable(payload):
            payload = payload(b"" if destination is None
                              else bytes(bytearray(destination)))
        self.calls.append((int(info_class), buffer is None, len(payload)))
        if self.status:
            return self.status
        target = getattr(returned, "_obj", returned)
        if destination is None:
            target.value = len(payload)
            return 0
        ctypes.memmove(ctypes.addressof(destination), payload,
                       min(len(payload), ctypes.sizeof(destination)))
        target.value = len(payload)
        return 0


class _FakeKernel32:
    """Only the four entry points the collector's barrier helpers call.

    No real completion port, Job Object or process exists anywhere in this
    class: `GetQueuedCompletionStatus` replays a scripted message list and
    `QueryInformationJobObject` fills the pinned 96-byte accounting buffer from
    a scripted active-process sequence. A wait this fake is asked to perform is
    RECORDED rather than performed, so a blocking call is observable in finite
    time instead of hanging the suite.
    """

    def __init__(self, messages=(), active_counts=(0,)):
        self.messages = list(messages)
        self.active_counts = list(active_counts)
        self.completion_waits_requested = []
        self.job_queries = 0

    def GetQueuedCompletionStatus(self, port, code_ref, key_ref, ov_ref, timeout):
        self.completion_waits_requested.append(int(timeout) & 0xFFFFFFFF)
        if self.messages:
            ctypes.cast(code_ref,
                        ctypes.POINTER(win32.wintypes.DWORD))[0] = self.messages.pop(0)
            return 1
        ctypes.set_last_error(win32.WAIT_TIMEOUT)
        return 0

    def QueryInformationJobObject(self, job, information_class, buffer_ref, size,
                                  returned_ref):
        self.job_queries += 1
        active = (self.active_counts.pop(0) if len(self.active_counts) > 1
                  else self.active_counts[0])
        accounting = win32.JOBOBJECT_BASIC_AND_IO_ACCOUNTING_INFORMATION()
        accounting.BasicInfo.ActiveProcesses = active
        raw = ctypes.string_at(ctypes.byref(accounting), ctypes.sizeof(accounting))
        ctypes.memmove(buffer_ref, raw, min(len(raw), size))
        ctypes.cast(returned_ref, ctypes.POINTER(win32.wintypes.DWORD))[0] = size
        return 1


class _FakeWin32:
    def __init__(self, **kwargs):
        self.kernel32 = _FakeKernel32(**kwargs)


class BuildCollectorLivePathTests(unittest.TestCase):
    """bw70-bw74: the three codex r2 defects that only a LIVE cell could hit.

    Each of the three made every physical collection fail or hang while the
    whole simulated suite stayed green, because nothing exercised the collector's
    own scalar assembly, its terminal barrier or the interval its signed elapsed
    values describe:

    - bw70: `retired_instructions` was the literal `0` for every physical
      collection, so admission refused every real envelope twice over
      (`INSTRUCTION_ACCOUNTING_MISSING`, and the frozen equality with the summed
      CSwitch deltas at `mbcx01_r13_measurement.py:1040-1042`);
    - bw71/bw72: the DIAGNOSTIC completion drain ran before the load-bearing
      barrier and waited for `JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO`, a message §3
      permits to be undelivered — forever at the default `INFINITE`, 60 s on the
      smoke path — and then reported two barrier facts it had never observed;
    - bw73/bw74: the signed `elapsed_qpc_ticks` was the collector's OWN QPC
      window while the cross-check compares it to the signed member-lifetime
      span, so every live envelope failed `MONOTONIC_TIME_CROSS_CHECK_FAILED`.

    Nothing here starts a process, a Job, a completion port or an ETW session.
    """

    def setUp(self):
        self.collections = simulated_collections()
        self.observations = [
            {"sequence": 0, "processor": 0, "qpc": 1_005_000, "old_thread_id": 900,
             "counter_value": 1_000, "delta_from_previous": 0,
             "process_id": 4100, "process_start_key": "0000000000000011"},
            {"sequence": 1, "processor": 0, "qpc": 1_015_000, "old_thread_id": 900,
             "counter_value": 3_000, "delta_from_previous": 2_000,
             "process_id": 4100, "process_start_key": "0000000000000011"}]

    def _raw_buffers(self):
        accounting = win32.JOBOBJECT_BASIC_AND_IO_ACCOUNTING_INFORMATION()
        accounting.BasicInfo.TotalUserTime = 120_000
        accounting.BasicInfo.TotalProcesses = 1
        extended = win32.JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        extended.PeakJobMemoryUsed = 4_194_304
        return (ctypes.string_at(ctypes.byref(accounting), ctypes.sizeof(accounting)),
                ctypes.string_at(ctypes.byref(extended), ctypes.sizeof(extended)))

    # --- bw70: the instruction total the Job cannot supply --------------------

    def test_bw70_positive_retired_instructions_are_the_summed_attributed_deltas(self):
        """The scalar equals the sum the evidence tree carries, by construction.

        The Job has no instruction counter, so `retired_instructions` can only
        come from the attributed PMC deltas `consume_cswitch()` recomputed. The
        producer sums the SAME deltas into `aggregate_retired_instructions` and
        the frozen validator requires the two to be equal, so the collector must
        pass the total in rather than leave a placeholder in a signed receipt.
        """
        basic_raw, extended_raw = self._raw_buffers()
        total = win32._sum_attributed_retired_instructions(self.observations)
        self.assertEqual(total, 2_000)
        scalars = win32._decode_scalars(basic_raw, extended_raw,
                                        retired_instructions=total)
        self.assertEqual(scalars["retired_instructions"], total)
        self.assertEqual(scalars["user_time_ns"], 12_000_000)
        # The total is a REQUIRED keyword: a caller that forgets it cannot get a
        # silent zero into a signed receipt.
        with self.assertRaises(TypeError):
            win32._decode_scalars(basic_raw, extended_raw)
        # And `collect()` is that caller, in that position.
        source = inspect.getsource(win32.collect)
        self.assertIn("retired_instructions=retired_instructions", source)
        self.assertLess(source.index("session.consume_cswitch()"),
                        source.index("_sum_attributed_retired_instructions("))
        self.assertLess(source.index("_sum_attributed_retired_instructions("),
                        source.index("_decode_scalars("))

    def test_bw70_adversarial_a_zero_or_unreadable_instruction_total_is_named(self):
        """Zero is refused at admission by name; an unreadable delta is a fault."""
        job = {"instruction_backend": measurement.INSTRUCTION_MODE,
               "instruction_profile_source": measurement.INSTRUCTION_SOURCE,
               "instruction_event_list": measurement.INSTRUCTION_EVENT_LIST,
               "instruction_attribution": measurement.INSTRUCTION_ATTRIBUTION,
               "retired_instructions": 0,
               "etw_capability_query_succeeded": True,
               "etw_pmc_source_available": True, "etw_max_pmc_counters": 4,
               "etw_counter_owner_conflict_count": 0, "etw_pmc_strict_mode": True,
               "etw_pmc_multiplexing_detected": False, "etw_events_lost": 0,
               "etw_log_buffers_lost": 0, "etw_realtime_buffers_lost": 0,
               "etw_attribution_complete": True}
        self.assertIn("INSTRUCTION_ACCOUNTING_MISSING",
                      authority._instruction_accounting_errors(dict(job)))
        self.assertEqual(
            authority._instruction_accounting_errors(
                dict(job, retired_instructions=2_000)), set())
        for delta in (None, "2000", 2.0, True, -1):
            with self.subTest(delta=repr(delta)):
                with self.assertRaises(win32.CollectorFault) as caught:
                    win32._sum_attributed_retired_instructions(
                        [{"delta_from_previous": delta}])
                self.assertIn("ETW_PMC_DELTA_UNREADABLE", str(caught.exception))
        basic_raw, extended_raw = self._raw_buffers()
        with self.assertRaises(win32.CollectorFault) as caught:
            win32._decode_scalars(basic_raw, extended_raw, retired_instructions=-1)
        self.assertIn("RETIRED_INSTRUCTIONS_UNREADABLE", str(caught.exception))

    # --- bw71: the diagnostic drain leaves the critical path ------------------

    def test_bw71_positive_the_completion_drain_never_waits_for_a_message(self):
        """Every completion poll asks for 0 ms, so an absent message costs nothing.

        `JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO` may never be delivered (harness
        requirements §3). The drain therefore takes what is queued and returns:
        the messages below arrive WITHOUT an active-zero, and the drain still
        returns instead of waiting out the caller's timeout.
        """
        fake = _FakeWin32(messages=[win32.JOB_OBJECT_MSG_NEW_PROCESS,
                                    win32.JOB_OBJECT_MSG_EXIT_PROCESS])
        diagnostics = win32._drain_completion_port(fake, "PORT")
        self.assertEqual(win32.COMPLETION_DRAIN_POLL_MS, 0)
        self.assertEqual(set(fake.kernel32.completion_waits_requested), {0})
        self.assertEqual(diagnostics["new_process_messages"], 1)
        self.assertEqual(diagnostics["exit_process_messages"], 1)
        self.assertIs(diagnostics["active_zero_message_seen"], False)
        # Counters accumulate across polls; the second poll adds the message the
        # first one had not been delivered yet.
        fake.kernel32.messages.append(win32.JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO)
        win32._drain_completion_port(fake, "PORT", diagnostics)
        self.assertIs(diagnostics["active_zero_message_seen"], True)
        self.assertEqual(diagnostics["new_process_messages"], 1)
        # The load-bearing barrier runs FIRST in `collect()`; the drain follows.
        source = inspect.getsource(win32.collect)
        self.assertLess(source.index("WaitForSingleObject"),
                        source.index("_await_active_process_zero("))
        self.assertLess(source.index("WaitForSingleObject"),
                        source.index("_drain_completion_port("))

    def test_bw71_adversarial_the_drain_states_no_barrier_fact_it_cannot_see(self):
        """A message drain may not report the Job's state; only a query can.

        `final_active_processes` and `all_members_terminal` are load-bearing at
        admission (`_terminal_barrier_proven`, `ACTIVE_PROCESS_RACE`). They used
        to be hard-coded `0`/`True` inside the drain, which asserted the exact
        barrier the drain had not observed — and did so BEFORE the barrier ran.
        """
        fake = _FakeWin32()
        diagnostics = win32._drain_completion_port(fake, "PORT")
        self.assertNotIn("final_active_processes", diagnostics)
        self.assertNotIn("all_members_terminal", diagnostics)
        self.assertEqual(fake.kernel32.job_queries, 0)
        record = win32._completion_record(diagnostics, final_active_processes=0,
                                          all_members_terminal=True)
        self.assertEqual(set(record), measurement.COMPLETION_KEYS)
        self.assertEqual(record["final_active_processes"], 0)
        self.assertIs(record["all_members_terminal"], True)
        # The observed values are carried, not overwritten with optimism.
        observed = win32._completion_record(diagnostics, final_active_processes=3,
                                            all_members_terminal=False)
        self.assertEqual(observed["final_active_processes"], 3)
        self.assertIs(observed["all_members_terminal"], False)
        # A port that never delivered the end-of-job message does not claim to
        # have been drained through it.
        self.assertIs(record["completion_port_drained"], False)
        self.assertIs(record["diagnostic_messages_complete"], False)
        drained = win32._completion_record(
            dict(diagnostics, active_zero_message_seen=True),
            final_active_processes=0, all_members_terminal=True)
        self.assertIs(drained["completion_port_drained"], True)

    # --- bw72: the Job query IS the barrier -----------------------------------

    def test_bw72_positive_the_barrier_is_the_job_query_under_one_deadline(self):
        """Active-process zero is waited on by QUERYING the Job, not by a message."""
        fake = _FakeWin32(messages=[win32.JOB_OBJECT_MSG_NEW_PROCESS],
                          active_counts=[2, 1, 0])
        diagnostics = win32._new_completion_diagnostics()
        active = win32._await_active_process_zero(
            fake, "JOB", "PORT", diagnostics, win32._barrier_deadline(win32.INFINITE))
        self.assertEqual(active, 0)
        self.assertEqual(fake.kernel32.job_queries, 3)
        self.assertEqual(diagnostics["new_process_messages"], 1)
        self.assertEqual(set(fake.kernel32.completion_waits_requested), {0})
        self.assertEqual(win32._remaining_ms(None), win32.INFINITE)
        self.assertLessEqual(win32._remaining_ms(win32._barrier_deadline(50)), 50)

    def test_bw72_adversarial_an_open_barrier_expires_by_name_not_forever(self):
        """A Job that never empties exhausts the ONE deadline and is named.

        The old code could not reach this state at all: it waited for a
        completion message first, so a caller's `timeout_ms` was spent before
        the barrier was ever queried.
        """
        fake = _FakeWin32(active_counts=[1])
        with self.assertRaises(win32.CollectorFault) as caught:
            win32._await_active_process_zero(
                fake, "JOB", "PORT", win32._new_completion_diagnostics(),
                deadline=0.0)
        self.assertIn("ACTIVE_PROCESS_ZERO_DEADLINE_EXCEEDED", str(caught.exception))
        self.assertGreaterEqual(fake.kernel32.job_queries, 1)
        self.assertEqual(win32._remaining_ms(0.0), 0)

    # --- bw73/bw74: which interval the signed elapsed values describe ---------

    def test_bw73_positive_elapsed_derives_from_the_signed_lifetime_endpoints(self):
        """The collector and the authority use the SAME two endpoints.

        `_member_lifetime_endpoints()` returns the earliest member ProcessStart
        and the latest member ProcessStop of the signed roster, which is exactly
        the pair `_timing_errors()` recomputes from the receipt, so the exact
        equality it requires is satisfiable on a physical run.
        """
        collection = self.collections[0]
        started, ended = win32._member_lifetime_endpoints(collection.process_lifetimes)
        self.assertEqual((started, ended), (PROCESS_STARTED_QPC, PROCESS_ENDED_QPC))
        self.assertEqual(ended - started, collection.elapsed_qpc_ticks)
        self.assertEqual(collection.elapsed_monotonic_ns,
                         (ended - started) * 1_000_000_000 // collection.qpc_frequency_hz)
        grid = simulated_production_grid(self.collections)
        block = grid[0]["timing_cross_check"]
        self.assertEqual(block["elapsed_qpc_ticks"], block["lifetimes_span_qpc"])
        self.assertEqual(admit(grid), [])
        for members in ([], [{"process_id": 1}],
                        [{"started_qpc": 5, "ended_qpc": 5}]):
            with self.subTest(members=repr(members)):
                with self.assertRaises(win32.CollectorFault):
                    win32._member_lifetime_endpoints(members)

    def test_bw73_adversarial_the_collectors_own_window_is_not_the_signed_span(self):
        """Signing the observation interval instead of the lifetime span is refused.

        This is the live failure in its permanent form: a collector that signs
        its own QPC pair — read after `CreateProcessW` and job/session setup,
        and again before the final queries — hands the authority two different
        intervals, and the cross-check says so by name rather than accepting a
        number it cannot reproduce.
        """
        window_ticks = ELAPSED_QPC_TICKS + 7_000
        grid = simulated_production_grid(perturbed(
            self.collections, 0, elapsed_qpc_ticks=window_ticks,
            elapsed_monotonic_ns=window_ticks * 1_000_000_000 // QPC_FREQUENCY_HZ))
        errors = admit(grid)
        self.assertIn("MONOTONIC_TIME_CROSS_CHECK_FAILED", errors)
        self.assertTrue(set(errors) <= authority.PRODUCTION_ERROR_CODES, errors)
        # The docstring of the check names the interval it compares, because a
        # cross-check whose two values are different intervals is not a check.
        self.assertIn("signed member-lifetime interval",
                      inspect.getdoc(authority._timing_errors))

    def test_bw74_positive_the_observation_window_fences_the_signed_span(self):
        """The collector's own QPC pair stays load-bearing as a containment fence.

        The window opens BEFORE `CreateProcessW`, so the root's ETW ProcessStart
        cannot precede it, and closes AFTER the barrier, so no member ProcessStop
        can follow it. A roster that does not nest inside it is a roster from
        some other window and is a fault, never a signed number.
        """
        win32._check_span_within_observation_window(500, 1_500, 400, 1_600)
        win32._check_span_within_observation_window(400, 1_600, 400, 1_600)
        for span_started, span_ended in ((399, 1_500), (500, 1_601)):
            with self.subTest(span=(span_started, span_ended)):
                with self.assertRaises(win32.CollectorFault) as caught:
                    win32._check_span_within_observation_window(
                        span_started, span_ended, 400, 1_600)
                self.assertIn("ETW_LIFETIME_SPAN_OUTSIDE_OBSERVATION_WINDOW",
                              str(caught.exception))
        source = inspect.getsource(win32.collect)
        self.assertLess(source.index("QueryPerformanceCounter(observation_start)"),
                        source.index("kernel32.CreateProcessW("))
        self.assertLess(source.index("_await_active_process_zero("),
                        source.index("QueryPerformanceCounter(observation_end)"))
        self.assertLess(source.index("QueryPerformanceCounter(observation_end)"),
                        source.index("_check_span_within_observation_window("))


class _FakeTelemetryNtdll:
    """`NtQueryInformationProcess(ProcessTelemetryIdInformation)`, faked.

    Honours the real call protocol measured on this box: the record is
    variable-length, a buffer shorter than it is refused with
    STATUS_INFO_LENGTH_MISMATCH and fills NOTHING, and `ReturnLength` reports
    the requirement on both the failing and the succeeding call.
    """

    STATUS_INFO_LENGTH_MISMATCH = -1073741820  # 0xC0000004 as a signed long

    def __init__(self, *, process_id=8548, start_key=0x0048000000000096,
                 sequence_number=0x0000000000000096, record_bytes=454):
        record = (struct.pack("<IIQQQQQ", 96, process_id, start_key,
                              0x01DD2D37D0704D0D, 0, 0, sequence_number)
                  + b"\x00" * max(0, record_bytes - 48))
        self.blob = record[:record_bytes]
        self.lengths = []

    def NtQueryInformationProcess(self, handle, information_class, buffer_ref,  # noqa: N802
                                  size, returned_ref):
        assert int(information_class) == win32.ProcessTelemetryIdInformation
        self.lengths.append(int(size))
        ctypes.cast(returned_ref,
                    ctypes.POINTER(win32.wintypes.ULONG))[0] = len(self.blob)
        if int(size) < len(self.blob):
            return self.STATUS_INFO_LENGTH_MISMATCH
        ctypes.memmove(buffer_ref, self.blob, len(self.blob))
        return 0


class _FakeCollectKernel32:
    """The kernel32 entry points `collect()` reaches before the ETW session.

    Nothing here is real: no process is created, no Job Object exists, no handle
    addresses anything. Every call is RECORDED by name so the order of the
    cleanup is observable.
    """

    PROCESS_HANDLE = 0x1000
    THREAD_HANDLE = 0x1001
    JOB_HANDLE = 0x2000
    PORT_HANDLE = 0x3000
    PROCESS_ID = 4100

    def __init__(self, *, assign_ok=False, terminate_ok=True):
        self.calls = []
        self.assign_ok = assign_ok
        self.terminate_ok = terminate_ok

    def QueryPerformanceFrequency(self, ref):  # noqa: N802
        ctypes.cast(ref, ctypes.POINTER(ctypes.c_longlong))[0] = 10_000_000
        return 1

    def QueryPerformanceCounter(self, ref):  # noqa: N802
        ctypes.cast(ref, ctypes.POINTER(ctypes.c_longlong))[0] = 1_000_000
        return 1

    def CreateProcessW(self, app, cmd, pa, ta, inherit, flags, env, cwd,  # noqa: N802
                       startup_ref, information_ref):
        assert int(flags) & win32.CREATE_SUSPENDED, "the child must be suspended"
        self.calls.append("CreateProcessW")
        information = ctypes.cast(
            information_ref, ctypes.POINTER(win32.PROCESS_INFORMATION)).contents
        information.hProcess = self.PROCESS_HANDLE
        information.hThread = self.THREAD_HANDLE
        information.dwProcessId = self.PROCESS_ID
        information.dwThreadId = 900
        return 1

    def CreateJobObjectW(self, attributes, name):  # noqa: N802
        self.calls.append("CreateJobObjectW")
        return self.JOB_HANDLE

    def SetInformationJobObject(self, job, information_class, buffer_ref, size):  # noqa: N802
        self.calls.append("SetInformationJobObject(%d)" % int(information_class))
        return 1

    def CreateIoCompletionPort(self, handle, port, key, threads):  # noqa: N802
        self.calls.append("CreateIoCompletionPort")
        return self.PORT_HANDLE

    def AssignProcessToJobObject(self, job, process):  # noqa: N802
        self.calls.append("AssignProcessToJobObject")
        if self.assign_ok:
            return 1
        ctypes.set_last_error(5)
        return 0

    def TerminateProcess(self, handle, exit_code):  # noqa: N802
        self.calls.append("TerminateProcess(0x%X,0x%X)"
                          % (int(handle), int(exit_code)))
        if self.terminate_ok:
            return 1
        ctypes.set_last_error(87)
        return 0

    def CloseHandle(self, handle):  # noqa: N802
        self.calls.append("CloseHandle(0x%X)" % int(handle))
        return 1


class _FakeCollectWin32:
    def __init__(self, **kwargs):
        self.kernel32 = _FakeCollectKernel32(**kwargs)
        self.ntdll = _FakeTelemetryNtdll()
        self.advapi32 = None


class BuildCodexRound3Tests(unittest.TestCase):
    """bw67-bw69: the three codex round-3 findings.

    bw67-bw69 were left free by the fold that took bw80-bw84; bw70-bw74 and
    bw75-bw79 are somebody else's, so nothing here renumbers a neighbour.

    - bw67: the ProcessStart/ProcessStop decoder read `<QI` — a 64-bit start key
      followed by a 32-bit pid — at payload offset 0. Every version of both
      events actually begins with a UINT32 `ProcessID`, and the 64-bit identity
      is `ProcessSequenceNumber`, present only in the later versions. Both
      identities were therefore derived from unrelated bytes and the captured
      root could never match the known one. The same witness covers the OTHER
      half of that mismatch: `query_process_start_key()` read the boot-tagged
      `ProcessStartKey` — a value no ProcessStart payload carries — out of a
      48-byte buffer this information class refuses outright.
    - bw68: `_query_loss()` raised out of `stop()` BEFORE the STOP control call,
      so an unreadable loss counter left the system logger running and the box
      one slot short for the next run.
    - bw69: a failure between `CreateProcessW` and `AssignProcessToJobObject`
      closed the suspended child's handles without terminating it. Closing a
      handle does not end a process and KILL_ON_JOB_CLOSE cannot reach one no
      Job holds, so the child stayed suspended indefinitely.

    Nothing here starts an ETW session, creates a process or needs elevation.
    """

    # --- bw67: the payload the provider actually emits ------------------------

    def _feed(self, etw, consumer, feed):
        alive = []
        for event_id, payload, logging_process_id, timestamp in feed:
            record, buffer = _kernel_process_record(
                etw, event_id=event_id, payload=payload,
                logging_process_id=logging_process_id, timestamp=timestamp)
            alive.append((record, buffer))
            consumer._on_event_record(ctypes.pointer(record))
        return alive

    def test_bw67_positive_the_decoder_reads_the_manifest_field_order(self):
        """ProcessID is a UINT32 at offset 0; the key is the sequence number at 4.

        The payloads are built by `_process_start_payload` /
        `_process_stop_payload`, whose field order is this box's own
        Microsoft-Windows-Kernel-Process manifest read back through TDH. A
        decoder that unpacks `<QI` at offset 0 gets neither field: it reads the
        pid and the low half of the sequence number as one 64-bit "key" and the
        high half of the sequence number as the "pid".
        """
        etw = _etw()
        consumer = etw.EtwPmcConsumer(session_name="MBCX01-BUILD-B-PMC-WITNESS")
        consumer._win32 = etw._EtwWin32(advapi32=_FakeTraceApi(), kernel32=None)
        consumer._capability_facts = etw.granted_capability_facts_for_test()
        payload = _process_start_payload(4100, 0x11, parent_process_id=4000,
                                         parent_start_key=0x07)
        self.assertEqual(struct.unpack_from("<I", payload, 0)[0], 4100)
        self.assertEqual(struct.unpack_from("<Q", payload, 4)[0], 0x11)
        alive = self._feed(etw, consumer, [
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START, payload, 4000, 10),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_STOP,
             _process_stop_payload(4100, 0x11), 4100, 30)])
        self.assertEqual(len(alive), 2)
        self.assertEqual(consumer._callback_faults, [])
        self.assertEqual(
            [(row["kind"], row["process_id"], row["process_start_key"])
             for row in consumer._process_events],
            [("START", 4100, 0x11), ("STOP", 4100, 0x11)])
        # The identity the collector holds for the root is now the SAME
        # quantity, so the scoped capture finds it instead of aborting.
        consumer.stop()
        capture = consumer.capture(root_process_id=4100,
                                   root_process_start_key="0000000000000011")
        self.assertEqual(len(capture.process_events), 2)
        # What the pre-fix `<QI` decode would have produced from these bytes.
        wrong_key, wrong_pid = struct.unpack_from("<QI", payload, 0)
        self.assertNotEqual(wrong_pid, 4100)
        self.assertNotEqual(wrong_key, 0x11)

    def test_bw67_adversarial_an_unverified_event_version_is_named_not_guessed(self):
        """A template this build did not read is a fault, never an offset guess.

        Three cases, and none of them may decode: the ProcessStart versions
        whose manifest template carries NO sequence number (v0, v1, v2), the
        ProcessStop versions likewise (v0, v1), and any version this build never
        saw at all. A payload too short for the template it claims is refused
        the same way.
        """
        etw = _etw()
        cases = [
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START, 0,
             "ETW_KERNEL_PROCESS_EVENT_VERSION_WITHOUT_START_KEY:id=1,version=0"),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START, 2,
             "ETW_KERNEL_PROCESS_EVENT_VERSION_WITHOUT_START_KEY:id=1,version=2"),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_STOP, 1,
             "ETW_KERNEL_PROCESS_EVENT_VERSION_WITHOUT_START_KEY:id=2,version=1"),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START, 9,
             "ETW_KERNEL_PROCESS_EVENT_VERSION_UNSUPPORTED:id=1,version=9"),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_STOP, 7,
             "ETW_KERNEL_PROCESS_EVENT_VERSION_UNSUPPORTED:id=2,version=7"),
        ]
        for event_id, version, expected in cases:
            with self.subTest(event_id=event_id, version=version):
                consumer = etw.EtwPmcConsumer(
                    session_name="MBCX01-BUILD-B-PMC-WITNESS")
                record, buffer = _kernel_process_record(
                    etw, event_id=event_id,
                    payload=_process_start_payload(4100, 0x11),
                    logging_process_id=4000, timestamp=10, version=version)
                self.assertEqual(len(buffer.raw) > 0, True)
                consumer._on_event_record(ctypes.pointer(record))
                self.assertEqual(consumer._callback_faults, [expected])
                self.assertEqual(consumer._process_events, [])
        # A payload that cannot hold the template's identity fields.
        consumer = etw.EtwPmcConsumer(session_name="MBCX01-BUILD-B-PMC-WITNESS")
        record, buffer = _kernel_process_record(
            etw, event_id=etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START,
            payload=b"\x04\x10\x00\x00\x11\x00", logging_process_id=4000,
            timestamp=10)
        consumer._on_event_record(ctypes.pointer(record))
        self.assertEqual(
            consumer._callback_faults,
            ["ETW_KERNEL_PROCESS_PAYLOAD_SHORT:6<32:id=1,version=4"])

    def test_bw67_positive_the_root_identity_is_the_quantity_etw_publishes(self):
        """`query_process_start_key()` returns ProcessSequenceNumber.

        `PROCESS_TELEMETRY_ID_INFORMATION` carries BOTH `ProcessStartKey` and
        `ProcessSequenceNumber`, and they are not the same number: measured on
        this box, the start key is the sequence number with a boot session id in
        its high 16 bits. Only the sequence number appears in a ProcessStart
        payload, so only the sequence number can be matched against the captured
        root. The buffer is also sized by the OS rather than by the struct
        prefix, because this information class refuses a short buffer outright
        and fills nothing.
        """
        ntdll = _FakeTelemetryNtdll()
        fake = _FakeCollectWin32()
        fake.ntdll = ntdll
        value = win32.query_process_start_key(fake, ctypes.c_void_p(0x1000))
        self.assertEqual(value, 0x0000000000000096)
        self.assertNotEqual(value, 0x0048000000000096)
        self.assertEqual("%016X" % value, "0000000000000096")
        # Sizing call first (zero length), then the full record.
        self.assertEqual(ntdll.lengths, [0, 454])
        self.assertGreater(ctypes.sizeof(win32.PROCESS_TELEMETRY_ID_INFORMATION), 0)
        self.assertLess(ctypes.sizeof(win32.PROCESS_TELEMETRY_ID_INFORMATION), 454)

    def test_bw67_adversarial_an_unusable_telemetry_record_is_refused(self):
        """A length that cannot hold the prefix, an absurd one, or a zero key."""
        cases = [
            (dict(record_bytes=16), "PROCESS_TELEMETRY_ID_LENGTH_IMPLAUSIBLE:16"),
            (dict(record_bytes=win32.PROCESS_TELEMETRY_ID_MAX_BYTES + 1),
             "PROCESS_TELEMETRY_ID_LENGTH_IMPLAUSIBLE:%d"
             % (win32.PROCESS_TELEMETRY_ID_MAX_BYTES + 1)),
            (dict(sequence_number=0), "PROCESS_START_KEY_UNAVAILABLE"),
        ]
        for kwargs, expected in cases:
            with self.subTest(case=expected):
                fake = _FakeCollectWin32()
                fake.ntdll = _FakeTelemetryNtdll(**kwargs)
                with self.assertRaises(win32.CollectorFault) as caught:
                    win32.query_process_start_key(fake, ctypes.c_void_p(0x1000))
                self.assertIn(expected, str(caught.exception))

    # --- bw68: the teardown no fault may skip ---------------------------------

    def _started_consumer(self, etw, api):
        consumer = etw.EtwPmcConsumer(session_name="MBCX01-BUILD-B-PMC-WITNESS")
        consumer._win32 = etw._EtwWin32(advapi32=api, kernel32=None)
        consumer._started = True
        consumer._session_handle = ctypes.c_ulonglong(0xABCD)
        consumer._recorded_session_handle = 0xABCD
        return consumer

    def test_bw68_positive_an_unreadable_loss_counter_still_stops_the_logger(self):
        """The unknown-loss fault is preserved AND the session is torn down.

        Before this, `_query_loss()` raised before the STOP block ran, so a
        failed QUERY left one of the box's eight system logger slots occupied by
        a session nobody would stop — and `_stop_orphan_session()` only cleans
        that up on the NEXT run.
        """
        etw = _etw()

        class QueryFailsApi:
            def __init__(self):
                self.calls = []

            def ControlTraceW(self, handle, name, block, code):  # noqa: N802
                self.calls.append(int(code))
                return 1168 if int(code) == etw.EVENT_TRACE_CONTROL_QUERY else 0

        api = QueryFailsApi()
        consumer = self._started_consumer(etw, api)
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            consumer.stop()
        self.assertIn("ControlTraceW(QUERY):WIN32_ERROR=1168", str(caught.exception))
        self.assertIn("loss is UNKNOWN", str(caught.exception))
        self.assertEqual(api.calls, [etw.EVENT_TRACE_CONTROL_QUERY,
                                     etw.EVENT_TRACE_CONTROL_STOP])
        self.assertTrue(consumer._session_stopped)
        self.assertFalse(consumer._started)
        # The loss stays UNKNOWN, so a capture is still refused.
        consumer._capability_facts = etw.granted_capability_facts_for_test()
        with self.assertRaises(etw.EtwConsumerFault) as refused:
            consumer.capture()
        self.assertIn("ETW_TRACE_NOT_STOPPED", str(refused.exception))

    def test_bw68_adversarial_a_failed_teardown_is_secondary_never_a_mask(self):
        """A STOP that also fails is NAMED, and never replaces the primary.

        Two orderings: a teardown failure while the loss query already failed
        (the loss fault stays primary, the teardown is appended after
        SECONDARY), and a teardown failure on its own (it IS the fault).
        """
        etw = _etw()

        class Api:
            def __init__(self, query_status, stop_status):
                self.calls = []
                self.query_status = query_status
                self.stop_status = stop_status

            def ControlTraceW(self, handle, name, block, code):  # noqa: N802
                self.calls.append(int(code))
                if int(code) == etw.EVENT_TRACE_CONTROL_QUERY:
                    return self.query_status
                return self.stop_status

        api = Api(query_status=1168, stop_status=5)
        consumer = self._started_consumer(etw, api)
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            consumer.stop()
        message = str(caught.exception)
        self.assertTrue(message.startswith("ControlTraceW(QUERY):WIN32_ERROR=1168"),
                        message)
        self.assertIn("SECONDARY ETW_SESSION_TEARDOWN_FAULT:ControlTraceW(STOP):"
                      "WIN32_ERROR=5", message)
        self.assertEqual(api.calls, [etw.EVENT_TRACE_CONTROL_QUERY,
                                     etw.EVENT_TRACE_CONTROL_STOP])

        api = Api(query_status=0, stop_status=5)
        consumer = self._started_consumer(etw, api)
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            consumer.stop()
        self.assertEqual(
            str(caught.exception),
            "ETW_SESSION_TEARDOWN_FAULT:ControlTraceW(STOP):WIN32_ERROR=5")
        # The counters the QUERY did read are still carried.
        self.assertEqual(consumer._loss, etw.LossCounters(0, 0, 0))

    # --- bw69: the child no Job owns ------------------------------------------

    def _authorized(self):
        # The document names the run these witnesses actually make:
        # `cmd.exe /c exit 0` at cell (0, 0, 0). It used to carry the marker and
        # nothing else, which the gate accepted — that bare-marker shape is now
        # refused and is pinned as such by
        # `BuildAuthorizationScopeBindingTests.test_bw94_red_a_bare_marker_document_authorizes_nothing`.
        directory = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, directory, True)
        path = os.path.join(directory, "authorization.txt")
        with open(path, "w", encoding="utf-8") as stream:
            stream.write(win32.AUTHORIZATION_MARKER + "\n"
                         "Candidate binary: `cmd.exe /c exit 0`\n"
                         "Cell: `(H, D, F) = (0, 0, 0)`\n")
        previous = os.environ.get(win32.ALLOW_PHYSICAL_ENV)
        os.environ[win32.ALLOW_PHYSICAL_ENV] = "1"

        def restore():
            if previous is None:
                os.environ.pop(win32.ALLOW_PHYSICAL_ENV, None)
            else:
                os.environ[win32.ALLOW_PHYSICAL_ENV] = previous

        self.addCleanup(restore)
        return path

    def _collect(self, fake, authorization_path, session_factory=None):
        previous = win32._win32
        win32._win32 = lambda: fake
        self.addCleanup(lambda: setattr(win32, "_win32", previous))

        def refuse_a_session():
            raise win32.CollectorFault("ETW_SESSION_UNAVAILABLE_IN_WITNESS")

        with self.assertRaises(win32.CollectorFault) as caught:
            win32.collect("cmd.exe /c exit 0", cell=(0, 0, 0), nonce="0" * 32,
                          external_enforcement={}, environment_record={},
                          pmc_source_id=1,
                          etw_session_factory=session_factory or refuse_a_session,
                          authorization_path=authorization_path, timeout_ms=1000)
        return caught.exception

    def test_bw69_positive_an_unassigned_suspended_child_is_terminated(self):
        """The child dies BEFORE its handle is closed, and only if unassigned.

        `CreateProcessW` returns a suspended child that belongs to no Job until
        `AssignProcessToJobObject` succeeds. In that window `CloseHandle` does
        not end it and `KILL_ON_JOB_CLOSE` cannot reach it, so a setup failure
        left it suspended for the life of the box.
        """
        authorization_path = self._authorized()
        fake = _FakeCollectWin32(assign_ok=False)
        fault = self._collect(fake, authorization_path)
        self.assertEqual(str(fault), "AssignProcessToJobObject:WIN32_ERROR=5")
        calls = fake.kernel32.calls
        terminate = "TerminateProcess(0x%X,0x%X)" % (
            _FakeCollectKernel32.PROCESS_HANDLE,
            win32.SUSPENDED_CHILD_TERMINATION_EXIT_CODE)
        self.assertIn(terminate, calls)
        self.assertLess(calls.index(terminate),
                        calls.index("CloseHandle(0x%X)"
                                    % _FakeCollectKernel32.PROCESS_HANDLE))
        self.assertEqual(getattr(fault, "__notes__", []), [])

    def test_bw69_adversarial_an_assigned_child_is_left_to_the_job(self):
        """Once the Job owns the child, nothing here terminates it.

        The failure below happens AFTER the assignment succeeded — the session
        factory refuses, which is the next step — and the cleanup must not touch
        the child: ending a Job-owned process behind the Job's back is not this
        function's business, and KILL_ON_JOB_CLOSE already bounds it.
        """
        authorization_path = self._authorized()
        fake = _FakeCollectWin32(assign_ok=True)
        fault = self._collect(fake, authorization_path)
        self.assertEqual(str(fault), "ETW_SESSION_UNAVAILABLE_IN_WITNESS")
        self.assertIn("AssignProcessToJobObject", fake.kernel32.calls)
        self.assertEqual([call for call in fake.kernel32.calls
                          if call.startswith("TerminateProcess")], [])
        self.assertIn("CloseHandle(0x%X)" % _FakeCollectKernel32.PROCESS_HANDLE,
                      fake.kernel32.calls)

    def test_bw69_adversarial_a_failed_termination_is_noted_never_silent(self):
        """A TerminateProcess that fails does not mask the setup fault.

        The setup failure stays the PRIMARY error — it is why the collection
        stopped — and the leaked child is attached to it as a note, so a run
        that left a suspended process behind can never look like a clean
        failure.
        """
        authorization_path = self._authorized()
        fake = _FakeCollectWin32(assign_ok=False, terminate_ok=False)
        fault = self._collect(fake, authorization_path)
        self.assertEqual(str(fault), "AssignProcessToJobObject:WIN32_ERROR=5")
        self.assertEqual(
            getattr(fault, "__notes__", []),
            ["SUSPENDED_CHILD_NOT_TERMINATED:TerminateProcess:WIN32_ERROR=87"])




# ==========================================================================
# codex-CLI r7 (2026-08-16) — the PHYSICAL collection path
# ==========================================================================


class BuildEtwPhysicalPathTests(unittest.TestCase):
    """bw96-bw98: the two codex-CLI r7 defects that only the ELEVATED run reaches.

    Measured RED against the PRE-FIX bytes of `mbcx01_build_etw_consumer.py`
    (worktree checkout sha256
    ccc46d55cd0d6db330dee55ce59250f993764c5faad12acdd37c1d2c3bb28764; the same
    bytes as `git show HEAD:mbcx01_build_etw_consumer.py`, whose LF blob hashes
    d926c762373e395379a6f0eeec96eed87b8c6a9d263214bbeffc670bd3e90699 — the two
    differ only in line endings), loaded from a scratch directory placed at
    `sys.path[0]`. The runner PRINTS the bound module's `__file__` and its
    sha256 and ASSERTS the intended copy won, because a red harness that
    silently binds the worktree copy reports PASS and FAIL exactly like a real
    one.

    bw96 (P1 — REFUSES A RIGHT CAPTURE). `start()` enabled the provider and
    opened the `ProcessTrace` pump; `mbcx01_smoke_cell.execute()` called
    `configure_pmc()` only after `start()` had RETURNED. Every context switch
    delivered in that window carries no PMC extended-data item, so
    `_on_event_record` records `ETW_PMC_EXTENDED_DATA_ABSENT` and `capture()`
    then refuses the WHOLE one-shot run — a right capture thrown away on the one
    elevated session the owner gets. Pre-fix measurement: the recorded startup
    order puts `OPEN_AND_CONSUME` before either `TraceSetInformation` call
    because `start()` issues neither.

    bw97 (P2 — WRONG MEMBERSHIP, EITHER SIGN). ProcessStart recorded
    `EventHeader.ProcessId` (the context the start was LOGGED in) as the parent
    and discarded the payload's authoritative `ParentProcessID` /
    `ParentProcessSequenceNumber`, which this module's own TDH-verified layout
    table puts at offsets 20 and 24 of the v3/v4 template. `member_tree_
    incarnations()` builds Job membership from that field, so a brokered or
    explicit-parent creation is OMITTED (a legitimate descendant vanishes from
    the roster) and a foreign process whose start happens to be logged in a
    member's context is ADMITTED. Either way the grid is invalid.

    bw98 is the GUARD in the other direction — a fix that refused right evidence
    would be the same defect wearing the other sign. ⚠ Reported honestly: its
    parts (a) and (c) exercise behaviour the PRE-FIX bytes did not have at all
    (idempotence; the payload-short length that covers the parent tuple), so
    they are red pre-fix as NEW CAPABILITY, not as a fold red. Part (b) — a
    parent that started before the trace window still resolving by incarnation
    containment — is the guard proper and is green on both sides.

    ⛔ Nothing here starts an ETW session, attaches a PMU counter, opens a trace
    or creates a process: every OS entry point is a recording stand-in, the
    records are synthetic and built from the module's own ctypes structures, and
    `MBCX01_BUILD_ALLOW_PHYSICAL` is never set.
    """

    maxDiff = None

    def _swap(self, target, name, value):
        """Replace one attribute for the duration of the test, then restore it."""
        previous = getattr(target, name)
        setattr(target, name, value)
        self.addCleanup(lambda: setattr(target, name, previous))

    # ---- bw96 ---------------------------------------------------------------

    def _startup_order(self, etw):
        """Drive the REAL `start()` with every OS call replaced by a recorder.

        The seam IS the record: `configure_pmc()` is not stubbed, so its two
        `TraceSetInformation` calls land in the same list as the pump, and "the
        counter was attached before the pump opened" is an OBSERVED call order
        rather than an inference from the source.

        THE RECORDER NOW READS `EnableFlags` OFF THE PROPERTIES BLOCK (codex-CLI
        r8 P1). The r7 reading of this seam could not see the defect it was
        written for, because it recorded only the NAME of each call: the CSwitch
        system provider is turned on by a FIELD of the block `StartTraceW` is
        handed, so "the session was already producing switches" was invisible in
        a list of names. `self.enable_flags` is a parallel list of
        `(index, call, EnableFlags)` for every call that carries a block, and the
        `order` strings are unchanged so the older assertions still read.
        """
        order = []
        enable_flags = []

        class RecordingApi:
            @staticmethod
            def _record_flags(call, block):
                enable_flags.append((len(order) - 1, call,
                                     int(block._obj.Props.EnableFlags)))

            def ControlTraceW(self, handle, name, block, code):  # noqa: N802
                order.append("ControlTraceW(%d)" % int(code))
                self._record_flags(order[-1], block)
                return 0

            def StartTraceW(self, handle, name, block):  # noqa: N802
                order.append("StartTraceW")
                self._record_flags(order[-1], block)
                handle._obj.value = 0xABCD
                return 0

            def TraceSetInformation(self, handle, info, buffer, size):  # noqa: N802
                order.append("TraceSetInformation(%d)" % int(info))
                return 0

        self.enable_flags = enable_flags
        api = RecordingApi()
        self._swap(etw, "verify_etw_struct_layout",
                   lambda: order.append("verify_layout"))
        self._swap(etw, "_etw_win32",
                   lambda: etw._EtwWin32(advapi32=api, kernel32=None))
        self._swap(etw.EtwPmcConsumer, "_resolve_profile_source_id",
                   lambda self, name: (order.append("resolve_source"), 7)[1])
        self._swap(etw.EtwPmcConsumer, "_query_capability_facts",
                   lambda self, source_id: (
                       order.append("query_capability"),
                       etw.granted_capability_facts_for_test())[1])
        self._swap(etw.EtwPmcConsumer, "_enable_process_provider",
                   lambda self: order.append("EnableTraceEx2"))
        self._swap(etw.EtwPmcConsumer, "_open_and_consume",
                   lambda self: order.append("OPEN_AND_CONSUME"))
        consumer = etw.EtwPmcConsumer(session_name="MBCX01-BUILD-B-PMC-WITNESS")
        consumer.start()
        return consumer, order

    def test_bw96_red_the_pmc_counter_is_attached_before_the_pump_opens(self):
        """codex-CLI r7 P1: a CSwitch delivered before PMC attachment kills the run.

        The two `TraceSetInformation` classes ARE the counter attachment
        (`TracePmcCounterListInfo` pins the source list, `TracePmcEventListInfo`
        names the event that samples it). `OpenTraceW`/`ProcessTrace` is the
        moment records start arriving. Between them there must be no window.
        """
        etw = _etw()
        consumer, order = self._startup_order(etw)
        counter_list = "TraceSetInformation(%d)" % etw.TracePmcCounterListInfo
        event_list = "TraceSetInformation(%d)" % etw.TracePmcEventListInfo
        # THE RED: pre-fix `start()` issues neither call, so both are absent.
        self.assertIn(counter_list, order)
        self.assertIn(event_list, order)
        self.assertIn("OPEN_AND_CONSUME", order)
        self.assertLess(order.index(counter_list), order.index(event_list), order)
        self.assertLess(order.index(event_list), order.index("OPEN_AND_CONSUME"),
                        order)
        # And the whole documented lifetime is still in its documented order.
        #
        # ⚠ RIDER, FLAGGED (codex-CLI r8 P1). This list encoded the r7 sequence,
        # which was INCOMPLETE: it had no step between the counter attach and
        # `EnableTraceEx2`, because r7 believed the pump was the earliest point
        # at which a CSwitch could exist. It is not — the CSwitch flag rides
        # `StartTraceW` — so the r8 fold adds
        # `ControlTraceW(EVENT_TRACE_CONTROL_UPDATE)` there and this assertion
        # has to name it. The edit changes what the assertion ACCEPTS, so it is
        # called out rather than folded in silently; its own red is
        # `test_bw96_red_the_cswitch_flag_is_not_enabled_until_the_counter_is_attached`
        # below.
        self.assertEqual(
            ["verify_layout", "ControlTraceW(%d)" % etw.EVENT_TRACE_CONTROL_STOP,
             "StartTraceW", "resolve_source", "query_capability",
             counter_list, event_list,
             "ControlTraceW(%d)" % etw.EVENT_TRACE_CONTROL_UPDATE,
             "EnableTraceEx2", "OPEN_AND_CONSUME"],
            order)
        self.assertTrue(consumer._pmc_configured)

    def test_bw96_red_the_cswitch_flag_is_not_enabled_until_the_counter_is_attached(self):
        """codex-CLI r8 P1: the r7 fold's own NEIGHBOUR — StartTraceW is EARLIER.

        `EVENT_TRACE_FLAG_CSWITCH` is a FIELD of the `EVENT_TRACE_PROPERTIES`
        block handed to `StartTraceW`, so a session started with it is producing
        context switches from the moment that call returns. Attaching the counter
        after it — which is what r7 achieved — still leaves every switch buffered
        in between without a PMC extended-data item, and ONE of those refuses the
        whole one-shot elevated run (`ETW_PMC_EXTENDED_DATA_ABSENT`, the
        consequence witness below).

        Pre-fix measurement: `StartTraceW` carries `0x10000013`
        (NO_SYSCONFIG|CSWITCH|THREAD|PROCESS) at index 2, and the PMC attach does
        not happen until index 6.
        """
        etw = _etw()
        consumer, order = self._startup_order(etw)
        recorded = dict((call, flags) for _, call, flags in self.enable_flags)
        # THE RED: pre-fix this bit is SET on the start call.
        self.assertEqual(0, recorded["StartTraceW"] & etw.EVENT_TRACE_FLAG_CSWITCH,
                         self.enable_flags)
        # The session still collects switches — the flag moved, it was not dropped.
        update = "ControlTraceW(%d)" % etw.EVENT_TRACE_CONTROL_UPDATE
        self.assertIn(update, recorded)
        self.assertTrue(recorded[update] & etw.EVENT_TRACE_FLAG_CSWITCH,
                        self.enable_flags)
        # ControlTraceW's own page: a non-zero EnableFlags names the providers to
        # "enable or keep enabled", so the UPDATE carries the WHOLE set. Passing
        # CSWITCH alone would DISABLE the process/thread flags the start turned on.
        self.assertEqual(etw.SESSION_ENABLE_FLAGS_AFTER_PMC, recorded[update])
        self.assertEqual(etw.SESSION_ENABLE_FLAGS_AT_START, recorded["StartTraceW"])
        self.assertEqual(
            etw.SESSION_ENABLE_FLAGS_AT_START | etw.EVENT_TRACE_FLAG_CSWITCH,
            etw.SESSION_ENABLE_FLAGS_AFTER_PMC)

    def test_bw96_red_the_attach_precedes_every_cswitch_generating_enable(self):
        """THE SET, walked instead of the one instance codex reported.

        Every point at which this module can make the session GENERATE events is
        enumerated from the recorded call stream, and the PMC attach must precede
        the first of them that can produce a record requiring a counter:

          1. `StartTraceW` EnableFlags        — system providers, live at return
          2. `ControlTraceW(UPDATE)` EnableFlags — the same providers, later
          3. `EnableTraceEx2(Kernel-Process)` — the manifest provider
          4. `OpenTraceW`/`ProcessTrace`      — DELIVERY, not generation

        and there is no fifth: `start()` is the module's only `StartTraceW`
        caller, `_enable_process_provider()` its only `EnableTraceEx2` caller, and
        every other `ControlTraceW` is STOP or QUERY. Asserted here from the
        module SOURCE, not from memory of it.
        """
        etw = _etw()
        consumer, order = self._startup_order(etw)
        counter_list = "TraceSetInformation(%d)" % etw.TracePmcCounterListInfo
        event_list = "TraceSetInformation(%d)" % etw.TracePmcEventListInfo
        generating = [index for index, call, flags in self.enable_flags
                      if flags & etw.EVENT_TRACE_FLAG_CSWITCH]
        generating.append(order.index("EnableTraceEx2"))
        # THE RED: pre-fix the earliest CSwitch-generating call is StartTraceW at
        # index 2 and the attach is at index 6.
        self.assertTrue(generating)
        self.assertLess(order.index(counter_list), min(generating), order)
        self.assertLess(order.index(event_list), min(generating), order)
        # Delivery is still last, and the attach still precedes it (the r7 half).
        self.assertLess(order.index(event_list), order.index("OPEN_AND_CONSUME"))
        # THE SET IS CLOSED at the source: one StartTraceW, one EnableTraceEx2,
        # and every other ControlTraceW is STOP or QUERY.
        with open(etw.__file__, encoding="utf-8") as stream:
            source = stream.read()
        self.assertEqual(1, source.count("advapi32.StartTraceW("))
        self.assertEqual(1, source.count("advapi32.EnableTraceEx2("))
        self.assertEqual(
            sorted(["EVENT_TRACE_CONTROL_STOP)", "EVENT_TRACE_CONTROL_STOP)",
                    "EVENT_TRACE_CONTROL_QUERY)", "EVENT_TRACE_CONTROL_UPDATE)"]),
            sorted([line.strip() for line in source.splitlines()
                    if line.strip().startswith("EVENT_TRACE_CONTROL_")
                    and line.strip().endswith(")")]))

    def test_bw96_guard_the_update_call_carries_what_controltracew_documents(self):
        """GUARD — an UPDATE built like a STOP would FAIL, and a failed update is
        a session that collects no context switches at all.

        ⚠ Reported honestly: this exercises a function the PRE-FIX bytes do not
        have, so it is red pre-fix as NEW CAPABILITY, not as a fold red — the
        same label bw98 parts (a) and (c) carry.

        ControlTraceW, *Properties*, on EVENT_TRACE_CONTROL_UPDATE:
          * "LogFileNameOffset: ... If the offset is not zero and you do not
            change the log file name, the function returns an error."
          * "LogFileMode: Set this member if you want to turn
            EVENT_TRACE_REAL_TIME_MODE on and off. To turn real time consuming
            off, set this member to 0."
        """
        etw = _etw()
        block = etw._enable_flags_update_properties(etw.SESSION_ENABLE_FLAGS_AFTER_PMC)
        self.assertEqual(0, block.Props.LogFileNameOffset)
        self.assertEqual(etw.EVENT_TRACE_REAL_TIME_MODE, block.Props.LogFileMode)
        self.assertEqual(etw.SESSION_ENABLE_FLAGS_AFTER_PMC, block.Props.EnableFlags)
        self.assertEqual(etw.WNODE_FLAG_TRACED_GUID, block.Props.Wnode.Flags)
        self.assertEqual(ctypes.sizeof(etw.EVENT_TRACE_PROPERTIES_BUFFER),
                         block.Props.Wnode.BufferSize)
        self.assertEqual(etw.EVENT_TRACE_PROPERTIES_BUFFER.LoggerName.offset,
                         block.Props.LoggerNameOffset)
        # The STOP/QUERY blocks are UNCHANGED: only the update builder differs.
        stop = etw._new_properties(log_file_mode=0, enable_flags=0)
        self.assertEqual(etw.EVENT_TRACE_PROPERTIES_BUFFER.LogFileName.offset,
                         stop.Props.LogFileNameOffset)
        self.assertEqual(0, stop.Props.EnableFlags)

    def test_bw96_red_an_early_cswitch_without_pmc_rejects_the_whole_run(self):
        """What the pre-fix window COSTS, demonstrated on pure functions.

        This is the consequence half of bw96 and it is unchanged by the fix: a
        CSwitch that carries no PMC item is a FAULT, never a counter of zero, and
        one such record refuses the ENTIRE capture. That is right — an
        unattributable context switch is not evidence — which is exactly why the
        attachment may not lag the pump.
        """
        etw = _etw()
        consumer = etw.EtwPmcConsumer(session_name="MBCX01-BUILD-B-PMC-WITNESS")
        consumer._win32 = etw._EtwWin32(advapi32=_FakeTraceApi(), kernel32=None)
        consumer._capability_facts = etw.granted_capability_facts_for_test()
        # The record's Flags carry CLASSIC_HEADER but NOT EXTENDED_INFO, which
        # is exactly the shape a CSwitch has while the counter is unattached:
        # `_extended_data_items()` returns nothing and the PMC item is ABSENT.
        record, alive = _classic_cswitch_record(
            etw, flags=etw.EVENT_HEADER_FLAG_CLASSIC_HEADER, processor=0, qpc=10,
            new_thread_id=900, old_thread_id=901, counters=(1234,))
        self.assertIsNotNone(alive)
        consumer._on_event_record(ctypes.pointer(record))
        self.assertEqual(["ETW_PMC_EXTENDED_DATA_ABSENT"], consumer._callback_faults)
        consumer.stop()
        with self.assertRaises(etw.EtwConsumerFault) as caught:
            consumer.capture()
        self.assertIn("ETW_CONSUMER_CALLBACK_FAULT", str(caught.exception))
        self.assertIn("ETW_PMC_EXTENDED_DATA_ABSENT", str(caught.exception))

    # ---- bw97 ---------------------------------------------------------------

    def _decode_starts(self, etw, feed):
        """Decode a synthetic ProcessStart/Stop feed through the REAL callback."""
        consumer = etw.EtwPmcConsumer(session_name="MBCX01-BUILD-B-PMC-WITNESS")
        consumer._win32 = etw._EtwWin32(advapi32=_FakeTraceApi(), kernel32=None)
        consumer._capability_facts = etw.granted_capability_facts_for_test()
        alive = []
        for event_id, payload, logging_process_id, timestamp in feed:
            record, buffer = _kernel_process_record(
                etw, event_id=event_id, payload=payload,
                logging_process_id=logging_process_id, timestamp=timestamp)
            alive.append((record, buffer))
            consumer._on_event_record(ctypes.pointer(record))
        self._alive = alive
        self.assertEqual([], consumer._callback_faults)
        return consumer

    def test_bw97_red_the_parent_identity_comes_from_the_payload_not_the_header(self):
        """codex-CLI r7 P2: the authoritative parent tuple is at payload 20/24.

        Two shapes, one defect, opposite signs. A BROKERED creation logs the
        start in the broker's context while naming the real parent in the
        payload: reading the header omits a legitimate descendant. A FOREIGN
        process whose start is logged in a member's context names an unrelated
        parent in the payload: reading the header admits it into the Job.
        """
        etw = _etw()
        root_pid, root_key = 4100, 0x11
        child_pid, child_key = 4200, 0x22
        broker_pid, foreign_pid, foreign_key = 6000, 7000, 0x77
        consumer = self._decode_starts(etw, [
            # The root, created by the collector.
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START,
             _process_start_payload(root_pid, root_key,
                                    parent_process_id=4000, parent_start_key=0x07),
             4000, 1),
            # A BROKERED descendant: logged in the broker's context, parented to
            # the root by the payload.
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START,
             _process_start_payload(child_pid, child_key,
                                    parent_process_id=root_pid,
                                    parent_start_key=root_key),
             broker_pid, 3),
            # A FOREIGN process, logged in the ROOT's context, parented
            # elsewhere by the payload.
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START,
             _process_start_payload(foreign_pid, foreign_key,
                                    parent_process_id=9000,
                                    parent_start_key=0x99),
             root_pid, 4),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_STOP,
             _process_stop_payload(child_pid, child_key), child_pid, 25),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_STOP,
             _process_stop_payload(foreign_pid, foreign_key), foreign_pid, 26),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_STOP,
             _process_stop_payload(root_pid, root_key), root_pid, 30),
        ])
        starts = [row for row in consumer._process_events if row["kind"] == "START"]
        self.assertEqual(3, len(starts))
        # THE RED (decode): pre-fix these are [4000, 6000, 4100] and [None]*3.
        self.assertEqual([4000, root_pid, 9000],
                         [row["parent_process_id"] for row in starts])
        self.assertEqual([0x07, root_key, 0x99],
                         [row["parent_process_start_key"] for row in starts])
        # The header pid is KEPT — as diagnostic evidence, never as identity.
        self.assertEqual([4000, broker_pid, root_pid],
                         [row["event_header_process_id"] for row in starts])

        # THE RED (membership): pre-fix the tree omits the brokered child and
        # admits the foreign process.
        tree = etw.member_tree_incarnations(
            consumer._process_events, root_process_id=root_pid,
            root_process_start_key="%016X" % root_key)
        self.assertIn((child_pid, "%016X" % child_key), tree)
        self.assertNotIn((foreign_pid, "%016X" % foreign_key), tree)
        self.assertEqual(2, len(tree))

    def test_bw97_red_the_scoped_roster_follows_the_payload_parent(self):
        """The same defect where it lands: the SIGNED membership roster."""
        etw = _etw()
        root_pid, root_key = 4100, 0x11
        child_pid, child_key = 4200, 0x22
        consumer = self._decode_starts(etw, [
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START,
             _process_start_payload(root_pid, root_key,
                                    parent_process_id=4000, parent_start_key=0x07),
             4000, 1),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START,
             _process_start_payload(child_pid, child_key,
                                    parent_process_id=root_pid,
                                    parent_start_key=root_key),
             6000, 3),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_STOP,
             _process_stop_payload(child_pid, child_key), child_pid, 25),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_STOP,
             _process_stop_payload(root_pid, root_key), root_pid, 30),
        ])
        consumer.stop()
        capture = consumer.capture(root_process_id=root_pid,
                                   root_process_start_key="%016X" % root_key)
        # THE RED: pre-fix the brokered descendant is scoped OUT, so the roster
        # is the root alone and the Job's own TotalProcesses disagrees with it.
        self.assertEqual(4, len(capture.process_events))
        rows = etw.assemble_member_lifetimes(
            capture.process_events, job_object_id="JOB.0.0.0",
            root_process_id=root_pid, root_process_start_key="%016X" % root_key)
        self.assertEqual([root_pid, child_pid], [row["process_id"] for row in rows])
        child_row = [row for row in rows if row["process_id"] == child_pid][0]
        self.assertEqual(root_pid, child_row["parent_process_id"])
        self.assertEqual("%016X" % root_key, child_row["parent_process_start_key"])
        # The ROOT still carries two Nones: its creator is the collector, which
        # is not a Job member, and the payload's parent tuple never overrides it.
        root_row = [row for row in rows if row["process_id"] == root_pid][0]
        self.assertIsNone(root_row["parent_process_id"])
        self.assertIsNone(root_row["parent_process_start_key"])

    # ---- bw98 ---------------------------------------------------------------

    def test_bw98_guard_the_fixes_refuse_nothing_that_was_right_before(self):
        """GUARD (green both sides where the pre-fix bytes had the behaviour).

        (a) `configure_pmc()` stays PUBLIC and becomes IDEMPOTENT, so the
            runbook's old `start(); configure_pmc()` sequence still works and
            cannot re-issue the two calls against a live pump.
        (b) a ProcessStart whose payload parent sequence number is 0 — a parent
            that started before the trace window — still RESOLVES by incarnation
            containment, exactly as it did when the decoder supplied no key.
        (c) a payload too short for the parent tuple is a NAMED refusal at the
            new length, never a decode at a guessed offset.
        """
        etw = _etw()
        # (a)
        consumer, order = self._startup_order(etw)
        before = list(order)
        consumer.configure_pmc()
        self.assertEqual(before, order)
        # (b)
        root_pid, root_key, child_pid, child_key = 4100, 0x11, 4200, 0x22
        consumer = self._decode_starts(etw, [
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START,
             _process_start_payload(root_pid, root_key,
                                    parent_process_id=4000, parent_start_key=0x07),
             4000, 1),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START,
             _process_start_payload(child_pid, child_key,
                                    parent_process_id=root_pid,
                                    parent_start_key=0),
             root_pid, 3),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_STOP,
             _process_stop_payload(child_pid, child_key), child_pid, 25),
            (etw.KERNEL_PROCESS_EVENT_ID_PROCESS_STOP,
             _process_stop_payload(root_pid, root_key), root_pid, 30),
        ])
        starts = [row for row in consumer._process_events if row["kind"] == "START"]
        self.assertEqual([0x07, 0], [row["parent_process_start_key"] for row in starts])
        rows = etw.assemble_member_lifetimes(
            consumer._process_events, job_object_id="JOB.0.0.0",
            root_process_id=root_pid, root_process_start_key="%016X" % root_key)
        child_row = [row for row in rows if row["process_id"] == child_pid][0]
        self.assertEqual("%016X" % root_key, child_row["parent_process_start_key"])
        # (c)
        consumer = etw.EtwPmcConsumer(session_name="MBCX01-BUILD-B-PMC-WITNESS")
        short = _process_start_payload(root_pid, root_key,
                                       parent_process_id=root_pid,
                                       parent_start_key=root_key)[:28]
        record, buffer = _kernel_process_record(
            etw, event_id=etw.KERNEL_PROCESS_EVENT_ID_PROCESS_START,
            payload=short, logging_process_id=4000, timestamp=10)
        self.assertEqual(28, len(buffer.raw))
        consumer._on_event_record(ctypes.pointer(record))
        self.assertEqual(["ETW_KERNEL_PROCESS_PAYLOAD_SHORT:28<32:id=1,version=4"],
                         consumer._callback_faults)
