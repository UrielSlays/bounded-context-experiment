"""r13 cohort provenance, signed physical-receipt admission, and call ledger.

The deterministic Ed25519 fixture key is test-only. Its signatures exercise the
trust boundary but cannot establish that the unbuilt physical harness ran.
"""

from __future__ import annotations

import base64
import copy
import hashlib
import json
import re
import struct
import subprocess
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any

MOTIFS = ("CORRECTION_RESTORATION", "OBLIGATION_LIFECYCLE", "DEPENDENCY_REVERSAL",
          "CROSS_SCOPE_COLLISION", "DELEGATION_IDEMPOTENT_HANDOFF", "MIXED_DELAYED_CONTINUITY")
H_VALUES = (128, 1024, 10000, 100000)
D_VALUES = (1, 4, 16, 64, 256)
F_VALUES = (1, 4, 16, 64, 256)
SHA256_RE = re.compile(r"^[0-9A-F]{64}$")
SHA384_RE = re.compile(r"^[0-9A-F]{96}$")
SEMANTIC_RE = re.compile(r"^[A-Z0-9][A-Z0-9:._/-]{0,127}$")
ROOT = Path(__file__).resolve().parent

ENVELOPE_DOMAIN = "MBCX01.SIGNED-MEASUREMENT-RECEIPT.V1"
SIGNATURE_ALGORITHM = "ED25519"
TEST_KEY_ID = "MBCX01.R13.NO-PAID.ED25519.TEST.1"
VERIFIER = ROOT / "verify-r13-receipt-signature.mjs"
EXACTNESS_SUITE = ROOT / "MBCX-01-R13-CARRIER-EXACTNESS-SUITE.json"

INSTRUCTION_MODE = "ETW_PMC_EVENT_ATTACHED_V1"
INSTRUCTION_SOURCE = "INSTRUCTIONRETIRED"
INSTRUCTION_EVENT_LIST = "CSWITCH"
INSTRUCTION_ATTRIBUTION = "SUM_INSTRUCTIONRETIRED_CSWITCH_DELTAS_BY_OLD_THREAD_JOINED_TO_SIGNED_JOB_PID_TID_LIFETIMES_INCLUDING_TERMINATED"
CALL_IDENTITY_FIELDS = ("handoff_id", "scenario_id", "condition", "node", "task_packet_hash",
                        "served_request_hash", "request_parameters_hash", "idempotency_token",
                        "route_contract_hash")
ENGINEERING_METRICS = ("retired_instructions", "aggregate_cpu_time_ns",
                       "elapsed_monotonic_ns", "peak_committed_bytes",
                       "total_io_transfer_bytes", "total_io_operations")
EPISODE_POSITIONS = ("BC.A0", "BC.B", "BC.A1", "OM.A0", "OM.B", "OM.A1")
_RETAINED_SOURCE_CACHE: tuple[list[dict[str, Any]], dict[str, Any]] | None = None
_RETAINED_INDEX_CACHE: dict[str, tuple[int, dict[str, Any], str]] | None = None
_RETAINED_AUTHORITY_CACHE: dict[str, Any] | None = None


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def sha256(value: Any) -> str:
    data = value if isinstance(value, bytes) else canonical_json(value)
    return hashlib.sha256(data).hexdigest().upper()


def sha384(value: Any) -> str:
    data = value if isinstance(value, bytes) else canonical_json(value)
    return hashlib.sha384(data).hexdigest().upper()


def _call_identity_hash(record: dict[str, Any]) -> str:
    return sha384({key: record[key] for key in CALL_IDENTITY_FIELDS})


def make_durability_receipt(record: dict[str, Any], transaction_id: str) -> dict[str, Any]:
    receipt = {"schema_id": "DurabilityReceiptV1",
               "ledger_identity_hash": _call_identity_hash(record),
               "raw_response_hash": record["raw_response_hash"],
               "response_ref": record["response_ref"],
               "provider_request_id": record["provider_request_id"],
               "transaction_id": transaction_id,
               "fsync_completed": True, "commit_completed": True}
    receipt["receipt_hash"] = sha384(receipt)
    return receipt


def valid_durability_receipt(receipt: Any, record: dict[str, Any]) -> bool:
    required = {"schema_id", "ledger_identity_hash", "raw_response_hash", "response_ref",
                "provider_request_id", "transaction_id", "fsync_completed",
                "commit_completed", "receipt_hash"}
    return (isinstance(receipt, dict) and set(receipt) == required
            and receipt["schema_id"] == "DurabilityReceiptV1"
            and receipt["ledger_identity_hash"] == _call_identity_hash(record)
            and receipt["raw_response_hash"] == record["raw_response_hash"]
            and receipt["response_ref"] == record["response_ref"]
            and receipt["provider_request_id"] == record["provider_request_id"]
            and SEMANTIC_RE.fullmatch(str(receipt["transaction_id"])) is not None
            and receipt["fsync_completed"] is True and receipt["commit_completed"] is True
            and receipt["receipt_hash"] == sha384(
                {key: value for key, value in receipt.items() if key != "receipt_hash"}))


def _load_json(name: str) -> dict[str, Any]:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def _validate_trust_root_document(document: Any) -> dict[str, dict[str, Any]]:
    manifest_keys = {"schema_id", "production_ready", "retirement_policy", "roots"}
    policy_keys = {"schema_id", "status", "fail_loud_sentinel", "signer_custodian_role",
                   "trust_root_editor_role", "roles_must_be_distinct",
                   "manifest_edit_cannot_activate_production", "activation_authority",
                   "required_external_evidence"}
    if isinstance(document, dict) and document.get("production_ready") is True:
        # R13 deliberately has no code path by which editing this document can mint
        # production authority. Retirement requires a future reviewed implementation.
        raise ValueError("production authority unavailable: PHYSICAL_HARNESS_UNAVAILABLE")
    if (not isinstance(document, dict)
            or set(document) != manifest_keys
            or document.get("schema_id") != "MeasurementTrustRootManifestV2"
            or document.get("production_ready") is not False
            or not isinstance(document.get("roots"), list) or not document["roots"]):
        raise ValueError("measurement trust-root document invalid")
    policy = document.get("retirement_policy")
    required_external = ["SEPARATE_KEY_CUSTODY_ATTESTATION",
                         "SEPARATE_TRUST_ROOT_EDITOR_APPROVAL",
                         "HARNESS_BUILD_PROVENANCE",
                         "PRODUCTION_SIGNING_CEREMONY_RECEIPT"]
    if (not isinstance(policy, dict) or set(policy) != policy_keys
            or policy.get("schema_id") != "ProductionMeasurementTrustRetirementPolicyV1"
            or policy.get("status") != "NOT_RETIRED"
            or policy.get("fail_loud_sentinel") != "PHYSICAL_HARNESS_UNAVAILABLE"
            or policy.get("roles_must_be_distinct") is not True
            or policy.get("manifest_edit_cannot_activate_production") is not True
            or policy.get("activation_authority") != "NONE_IN_R13"
            or policy.get("signer_custodian_role") == policy.get("trust_root_editor_role")
            or policy.get("required_external_evidence") != required_external):
        raise ValueError("measurement trust-root retirement policy invalid")
    policy_digest = sha384(policy)
    roots: dict[str, dict[str, Any]] = {}
    for row in document["roots"]:
        if (not isinstance(row, dict)
                or set(row) != {"key_id", "algorithm", "fixture_only",
                                "authorized_fixture_kind", "authorized_producer_role",
                                "trust_policy_digest", "public_key_pem"}
                or SEMANTIC_RE.fullmatch(str(row.get("key_id", ""))) is None
                or row.get("algorithm") != SIGNATURE_ALGORITHM
                or row.get("fixture_only") is not True
                or row.get("authorized_fixture_kind") != "NO_PAID_TEST_FIXTURE"
                or row.get("authorized_producer_role") != "NO_PAID_TEST_HARNESS"
                or row.get("trust_policy_digest") != policy_digest
                or not isinstance(row.get("public_key_pem"), str)
                or not row["public_key_pem"].startswith("-----BEGIN PUBLIC KEY-----\n")
                or not row["public_key_pem"].endswith("-----END PUBLIC KEY-----\n")
                or row["key_id"] in roots):
            raise ValueError("measurement trust-root row invalid")
        roots[row["key_id"]] = copy.deepcopy(row)
    if TEST_KEY_ID not in roots:
        raise ValueError("no-paid fixture trust root missing")
    return roots


def _load_trust_roots() -> dict[str, dict[str, Any]]:
    return _validate_trust_root_document(
        _load_json("MBCX-01-R13-MEASUREMENT-TRUST-ROOTS.json"))


def _selection_domains() -> tuple[str, str]:
    cohort = _load_json("MBCX-01-MEASUREMENT-CONTRACT-v7.json")["cohort"]
    return cohort["one_cut_hash_domain"], cohort["retention_hash_domain"]


def _generator_spec() -> tuple[dict[str, Any], str]:
    spec = _load_json("MBCX-01-R13-SYNTHETIC-COHORT-GENERATOR.json")
    if (spec.get("schema_id") != "SyntheticCohortGeneratorSpecV1"
            or spec.get("generator_id") != "GENERATOR.R13.SYNTHETIC"):
        raise ValueError("synthetic generator artifact invalid")
    return spec, sha384(spec)


def framed_hash(parts: list[str]) -> bytes:
    payload = bytearray()
    for part in parts:
        encoded = part.encode("utf-8")
        payload.extend(len(encoded).to_bytes(8, "big")); payload.extend(encoded)
    return hashlib.sha256(bytes(payload)).digest()


def choose_one_cut(scenario_id: str, cut_ids: list[str], domain: str) -> str:
    if not cut_ids or len(cut_ids) != len(set(cut_ids)) or not domain:
        raise ValueError("cut authority must be nonempty and unique")
    return min(cut_ids, key=lambda cut: (framed_hash([domain, scenario_id, cut]),
                                         cut.encode("utf-8")))


def _source_authority(row: dict[str, Any]) -> dict[str, Any]:
    return {"scenario_id": row["scenario_id"], "motif": row["motif"],
            "cut_ids": copy.deepcopy(row["cut_ids"]),
            "cut_set_hash": sha384(row["cut_ids"]),
            "action_universe_hash": sha384(row["action_ids_by_cut"]),
            "gold_authority_hash": sha384(row["gold_action_id_by_cut"]),
            "canonical_state_hash": sha384(row["canonical_state_by_cut"]),
            "canonical_world_hash": sha384(row["canonical_world_by_cut"]),
            "observation_hash": sha384(row["observation_by_cut"]),
            "cut_authority_hash": sha384(row["cut_by_id"])}


def _candidate_world(spec: dict[str, Any], target_action: str) -> list[dict[str, Any]]:
    scope = spec["scope_id"]
    target = spec["target_obligation_id"]
    prerequisite = spec["prerequisite_obligation_id"]
    decoy = "OBL.DECOY"
    world = [
        {"object_id": f"DEP.{target.split('.', 1)[-1]}.PREREQ",
         "object_kind": "DEPENDENCY",
         "fields": {"obligation_id": target,
                    "prerequisite_obligation_id": prerequisite},
         "source_event_ids": ["SOURCE.DEP"]},
        {"object_id": decoy, "object_kind": "OBLIGATION",
         "fields": {"subject_id": "SUB.SHARED", "owner_role": "WORKER",
                    "lifecycle": "OPEN", "critical": False,
                    "due_at": spec["cut"]["valid_time"],
                    "completion_action_id": "ACT." + sha256([scope, decoy]),
                    "prerequisite_obligation_ids": []},
         "source_event_ids": ["SOURCE.DECOY"]},
        {"object_id": prerequisite, "object_kind": "OBLIGATION",
         "fields": {"subject_id": "SUB.SHARED", "owner_role": "WORKER",
                    "lifecycle": spec["prerequisite_lifecycle"], "critical": True,
                    "due_at": spec["cut"]["valid_time"],
                    "completion_action_id": "ACT." + sha256([scope, prerequisite]),
                    "prerequisite_obligation_ids": []},
         "source_event_ids": ["SOURCE.PREREQ"]},
        {"object_id": target, "object_kind": "OBLIGATION",
         "fields": {"subject_id": "SUB.SHARED", "owner_role": "WORKER",
                    "lifecycle": spec["target_lifecycle"], "critical": True,
                    "due_at": spec["cut"]["valid_time"],
                    "completion_action_id": target_action,
                    "prerequisite_obligation_ids": [prerequisite]},
         "source_event_ids": ["SOURCE.TARGET"]},
        {"object_id": "OBS.SHARED", "object_kind": "OBSERVATION",
         "fields": {"code": "TARGET_VISIBLE",
                    "observed_at": spec["cut"]["knowledge_time"]},
         "source_event_ids": ["SOURCE.OBS"]},
    ]
    return sorted(world, key=lambda row: row["object_id"].encode("utf-8"))


def synthetic_candidates_r13() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    spec, generator_digest = _generator_spec()
    rows = []
    target_action = "ACT." + sha256([spec["scope_id"], spec["target_obligation_id"]])
    for motif_index, motif in enumerate(MOTIFS):
        for index in range(spec["candidate_count_per_motif"]):
            sid = spec["scenario_id_template"].format(motif_index=motif_index, index=index)
            cuts = [spec["cut_id_template"].format(index=index, label=label)
                    for label in spec["cut_labels"]]
            actions = {cut: [target_action] for cut in cuts}
            state = {"eligible": True, "scope_id": spec["scope_id"],
                     "target_obligation_id": spec["target_obligation_id"],
                     "target_lifecycle": spec["target_lifecycle"],
                     "prerequisite_obligation_id": spec["prerequisite_obligation_id"],
                     "prerequisite_lifecycle": spec["prerequisite_lifecycle"]}
            world = _candidate_world(spec, target_action)
            observation = {"scope_id": spec["scope_id"],
                           "observed_at": spec["cut"]["knowledge_time"],
                           "code": "TARGET_VISIBLE"}
            rows.append({"scenario_id": sid, "motif": motif, "cut_ids": cuts,
                         "action_ids_by_cut": actions,
                         "gold_action_id_by_cut": {cut: actions[cut][0] for cut in cuts},
                         "canonical_state_by_cut": {cut: copy.deepcopy(state) for cut in cuts},
                         "canonical_world_by_cut": {cut: copy.deepcopy(world) for cut in cuts},
                         "observation_by_cut": {cut: copy.deepcopy(observation) for cut in cuts},
                         "cut_by_id": {cut: {"cut_id": cut, **copy.deepcopy(spec["cut"])}
                                       for cut in cuts}})
    provenance = {"schema_id": "SourceProvenanceManifestV1",
                  "generator_id": spec["generator_id"], "generator_digest": generator_digest,
                  "scenario_authority": [_source_authority(row) for row in rows]}
    provenance["provenance_hash"] = sha384(provenance)
    return rows, provenance


def validate_source_provenance(candidates: list[dict[str, Any]],
                               provenance: dict[str, Any]) -> list[str]:
    try:
        spec, digest = _generator_spec()
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return ["SOURCE_GENERATOR_INVALID"]
    if (not isinstance(provenance, dict)
            or provenance.get("schema_id") != "SourceProvenanceManifestV1"
            or provenance.get("generator_id") != spec["generator_id"]
            or provenance.get("generator_digest") != digest
            or provenance.get("provenance_hash") != sha384(
                {key: value for key, value in provenance.items()
                 if key != "provenance_hash"})):
        return ["SOURCE_PROVENANCE_INVALID"]
    errors = set()
    if [_source_authority(row) for row in candidates] != provenance.get("scenario_authority", []):
        errors.add("SOURCE_PROVENANCE_MISMATCH")
    ids = [row.get("scenario_id") for row in candidates]
    if len(ids) != len(set(ids)):
        errors.add("DUPLICATE_SCENARIO_ID")
    if any(row.get("motif") not in MOTIFS for row in candidates):
        errors.add("UNKNOWN_MOTIF")
    if any(sum(row.get("motif") == motif for row in candidates) != 160 for motif in MOTIFS):
        errors.add("WRONG_MOTIF_TOTAL")
    return sorted(errors)


def select_cohort(candidates: list[dict[str, Any]],
                  provenance: dict[str, Any]) -> list[dict[str, Any]]:
    cut_domain, retain_domain = _selection_domains()
    errors = validate_source_provenance(candidates, provenance)
    if errors:
        raise ValueError(",".join(errors))
    selected = []
    for motif in MOTIFS:
        eligible = []
        for source in (row for row in candidates if row["motif"] == motif):
            row = copy.deepcopy(source)
            chosen = choose_one_cut(row["scenario_id"], row["cut_ids"], cut_domain)
            row["chosen_cut_id"] = chosen
            row["eligibility_source"] = "RECOMPUTED"
            state = row["canonical_state_by_cut"][chosen]
            actions = row["action_ids_by_cut"][chosen]
            gold = row["gold_action_id_by_cut"][chosen]
            row["eligible"] = state.get("eligible") is True and actions.count(gold) == 1
            row["retention_hash"] = framed_hash(
                [retain_domain, motif, row["scenario_id"], chosen]).hex().upper()
            if row["eligible"]:
                eligible.append(row)
        eligible.sort(key=lambda row: (bytes.fromhex(row["retention_hash"]),
                                        row["scenario_id"].encode("utf-8")))
        if len(eligible) < 128:
            raise ValueError("eligible motif shortfall")
        selected.extend(eligible[:128])
    if len(selected) != 768:
        raise ValueError("selected-total invariant failed")
    return sorted(selected,
                  key=lambda row: hashlib.sha256(row["scenario_id"].encode("utf-8")).digest())


def _pinned_retained_source() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    global _RETAINED_SOURCE_CACHE, _RETAINED_INDEX_CACHE
    if _RETAINED_SOURCE_CACHE is None:
        candidates, provenance = synthetic_candidates_r13()
        _RETAINED_SOURCE_CACHE = (select_cohort(candidates, provenance), provenance)
        _RETAINED_INDEX_CACHE = {
            row["scenario_id"]: (index, row, sha384(row))
            for index, row in enumerate(_RETAINED_SOURCE_CACHE[0])}
    return _RETAINED_SOURCE_CACHE


def retained_cohort_authority_r13() -> dict[str, Any]:
    """Recompute the pinned source and exact retained population from first principles."""
    global _RETAINED_AUTHORITY_CACHE
    if _RETAINED_AUTHORITY_CACHE is not None:
        return copy.deepcopy(_RETAINED_AUTHORITY_CACHE)
    retained, provenance = _pinned_retained_source()
    candidate_hashes = [sha384(row) for row in retained]
    authority = {
        "schema_id": "RetainedCohortAuthorityV2",
        "generator_id": provenance["generator_id"],
        "generator_digest": provenance["generator_digest"],
        "source_provenance_hash": provenance["provenance_hash"],
        "retained_total": len(retained),
        "retained_scenario_ids": [row["scenario_id"] for row in retained],
        "retained_candidate_hashes": candidate_hashes,
        "retained_set_root": sha384(candidate_hashes),
    }
    authority["authority_hash"] = sha384(authority)
    _RETAINED_AUTHORITY_CACHE = copy.deepcopy(authority)
    return authority


def retained_scenario_authority(candidate: dict[str, Any]) -> dict[str, Any]:
    """Issue authority only for one byte-exact member of the pinned retained set."""
    retained, provenance = _pinned_retained_source()
    retained_cohort_authority_r13()
    cohort = _RETAINED_AUTHORITY_CACHE
    if cohort is None:
        raise ValueError("RETAINED_SCENARIO_AUTHORITY_INVALID")
    candidate_hash = sha384(candidate)
    indexed = (_RETAINED_INDEX_CACHE or {}).get(candidate.get("scenario_id"))
    if (indexed is None or indexed[1] != candidate or indexed[2] != candidate_hash
            or cohort["retained_candidate_hashes"][indexed[0]] != candidate_hash):
        raise ValueError("RETAINED_SCENARIO_AUTHORITY_INVALID")
    position = indexed[0]
    authority = {
        "schema_id": "RetainedScenarioAuthorityV2",
        "generator_id": provenance["generator_id"],
        "generator_digest": provenance["generator_digest"],
        "source_provenance_hash": provenance["provenance_hash"],
        "retained_set_root": cohort["retained_set_root"],
        "retained_total": 768,
        "retained_position": position,
        "candidate_record": copy.deepcopy(candidate),
        "candidate_hash": candidate_hash,
    }
    authority["authority_hash"] = sha384(authority)
    return authority


def validate_retained_scenario_authority(authority: Any) -> list[str]:
    keys = {"schema_id", "generator_id", "generator_digest", "source_provenance_hash",
            "retained_set_root", "retained_total", "retained_position",
            "candidate_record", "candidate_hash", "authority_hash"}
    try:
        if (not isinstance(authority, dict) or set(authority) != keys
                or authority.get("schema_id") != "RetainedScenarioAuthorityV2"
                or authority.get("candidate_hash") != sha384(authority["candidate_record"])
                or authority.get("authority_hash") != sha384(
                    {key: value for key, value in authority.items() if key != "authority_hash"})
                or retained_scenario_authority(authority["candidate_record"]) != authority):
            raise ValueError
        return []
    except (KeyError, TypeError, ValueError, AttributeError):
        return ["RETAINED_SCENARIO_AUTHORITY_INVALID"]


JOB_KEYS = {
    "receipt_source", "job_object_id", "root_process_id", "created_suspended",
    "completion_port_associated_before_resume", "assigned_before_resume", "breakaway_enabled",
    "silent_breakaway_enabled", "active_processes_at_final_query", "completion_port_drained",
    "total_page_faults", "total_processes", "total_terminated_processes",
    "user_time_ns", "kernel_time_ns", "read_operations", "write_operations", "other_operations",
    "read_transfer_bytes", "write_transfer_bytes", "other_transfer_bytes", "peak_committed_bytes",
    "elapsed_monotonic_ns", "retired_instructions", "instruction_backend",
    "instruction_profile_source", "instruction_event_list", "instruction_attribution",
    "etw_capability_query_succeeded", "etw_pmc_source_available",
    "etw_max_pmc_counters", "etw_counter_owner_conflict_count", "etw_pmc_strict_mode",
    "etw_pmc_multiplexing_detected", "etw_events_lost",
    "etw_log_buffers_lost", "etw_realtime_buffers_lost", "etw_attribution_complete",
    "evidence",
}
RECEIPT_KEYS = {"schema_id", "candidate_id", "candidate_artifact_digest",
                "generator_digest", "H", "D", "F",
                "external_work_policy", "job_receipt"}
ENVELOPE_KEYS = {"schema_id", "domain", "version", "algorithm", "signing_key_id",
                 "run_id", "cell_id", "receipt", "receipt_preimage_b64", "receipt_digest",
                 "signature_b64", "fixture_kind", "producer_role", "trust_policy_digest",
                 "subject_digest", "environment_digest"}
HARNESS_IDENTITY_KEYS = {"harness_artifact_digest", "harness_build_digest",
                         "host_environment_digest", "harness_configuration_digest"}
ENVIRONMENT_KEYS = {"execution_environment", "host_architecture", "nested_virtualization",
                    "guest_pmu_exposure", "guest_pmu_capability_receipt_digest"}
PROCESS_KEYS = {"process_id", "process_start_key", "parent_process_id",
                "parent_process_start_key", "job_object_id", "assigned_before_resume",
                "membership_source", "started_qpc", "ended_qpc", "terminal_status"}
MEMBERSHIP_KEYS = {"root_process_id", "root_process_start_key", "membership_complete",
                   "membership_snapshot_digest", "processes"}
QUERY_KEYS = {"query_status_code", "information_class", "structure_version", "abi",
              "structure_size_bytes", "returned_size_bytes", "collected_after_terminal_barrier",
              "raw_bytes_b64", "raw_bytes_sha384"}
QUERY_BUNDLE_KEYS = {"basic_and_io", "extended_limit"}
COMPLETION_KEYS = {"completion_port_drained", "active_zero_message_seen",
                   "new_process_messages", "exit_process_messages",
                   "diagnostic_messages_complete", "diagnostics_query_succeeded",
                   "final_active_processes", "all_members_terminal"}
EXTERNAL_KEYS = {"policy_id", "policy_artifact_digest", "applied_before_resume",
                 "enforcement_owner_role", "deny_outbound_network",
                 "deny_external_compute_brokers", "deny_preexisting_helper_delegation",
                 "external_compute_endpoint_count", "validation_receipt_digest"}
# AMENDMENT-3 (2026-08-16): "cswitch_first_member_baselines" is deliberately
# part of the exact TRACE_KEYS set — the per-processor predecessor baseline is
# the evidence the FIRST member interval is measured against; a trace without
# the field is refused rather than silently undercounted (the r6 NO-GO:
# aggregate 100 validated where the stream proved 1,000,100).
TRACE_KEYS = {"cswitch_first_member_baselines",
              "mode", "profile_source", "event_list", "attribution",
              "capability_query_succeeded", "pmc_source_available", "max_pmc_counters",
              "counter_owner_conflict_count", "strict_mode", "multiplexing_detected",
              "events_lost", "log_buffers_lost", "realtime_buffers_lost",
              "attribution_complete", "capability_query", "event_attachment",
              "thread_lifetimes", "cswitch_observations", "aggregate_retired_instructions"}
CAPABILITY_QUERY_KEYS = {"query_status_code", "counter_information_class",
                         "event_information_class", "source_id", "counter_width_bits"}
EVENT_ATTACHMENT_KEYS = {"counter_query_class", "event_query_class", "profile_source",
                         "event_list", "attached"}
THREAD_LIFETIME_KEYS = {"process_id", "process_start_key", "thread_id",
                        "started_qpc", "ended_qpc"}
CSWITCH_OBSERVATION_KEYS = {"sequence", "processor", "qpc", "old_thread_id",
                            "counter_value", "delta_from_previous", "process_id",
                            "process_start_key"}
EVIDENCE_KEYS = {"harness_identity", "environment", "process_membership", "job_queries",
                 "completion", "external_enforcement", "trace"}


def _cell_id(receipt: dict[str, Any]) -> str:
    return f"CELL.H{receipt['H']}.D{receipt['D']}.F{receipt['F']}"


def _grid_identity_preimage(envelope: dict[str, Any]) -> dict[str, Any]:
    receipt = envelope["receipt"]
    evidence = receipt["job_receipt"]["evidence"]
    return {
        "run_id": envelope["run_id"],
        "candidate_id": receipt["candidate_id"],
        "candidate_artifact_digest": receipt["candidate_artifact_digest"],
        "generator_digest": receipt["generator_digest"],
        "harness_identity": evidence["harness_identity"],
        "environment": evidence["environment"],
        "signing_key_id": envelope["signing_key_id"],
        "fixture_kind": envelope["fixture_kind"],
        "producer_role": envelope["producer_role"],
        "trust_policy_digest": envelope["trust_policy_digest"],
    }


def measurement_grid_identity_hash(envelopes: list[dict[str, Any]]) -> str:
    try:
        hashes = {sha384(_grid_identity_preimage(row)) for row in envelopes}
        if len(envelopes) != 100 or len(hashes) != 1:
            raise ValueError
        return next(iter(hashes))
    except (KeyError, TypeError, ValueError, AttributeError) as exc:
        raise ValueError("GRID_IDENTITY_MISMATCH") from exc


def _receipt_preimage(envelope: dict[str, Any]) -> bytes:
    return canonical_json({
        "domain": envelope["domain"], "version": envelope["version"],
        "algorithm": envelope["algorithm"], "signing_key_id": envelope["signing_key_id"],
        "run_id": envelope["run_id"], "cell_id": envelope["cell_id"],
        "fixture_kind": envelope["fixture_kind"], "producer_role": envelope["producer_role"],
        "trust_policy_digest": envelope["trust_policy_digest"],
        "subject_digest": envelope["subject_digest"],
        "environment_digest": envelope["environment_digest"], "receipt": envelope["receipt"],
    })


def _invoke_signature_verifier(items: list[dict[str, str]]) -> list[bool]:
    request = {"items": items}
    try:
        process = subprocess.run(
            ["node", str(VERIFIER)], input=json.dumps(request), text=True,
            capture_output=True, timeout=15, check=False)
        reply = json.loads(process.stdout)
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        raise ValueError("receipt signature verifier unavailable") from exc
    if process.returncode != 0 or not isinstance(reply, dict) or reply.get("ok") is not True:
        raise ValueError("receipt signature operation failed")
    valid = reply.get("valid")
    if not isinstance(valid, list) or len(valid) != len(items):
        raise ValueError("receipt signature verifier response invalid")
    return [value is True for value in valid]


def refresh_receipt_hash(envelope: dict[str, Any]) -> None:
    """Refresh only unsigned preimage/digest fields; never confers signature authority."""
    if not isinstance(envelope, dict) or "receipt" not in envelope:
        raise ValueError("signed measurement envelope required")
    envelope["subject_digest"] = sha384(envelope["receipt"])
    try:
        envelope["environment_digest"] = envelope["receipt"]["job_receipt"]["evidence"][
            "harness_identity"]["host_environment_digest"]
    except (KeyError, TypeError):
        # Preserve an already supplied signed value so malformed-evidence witnesses
        # reach the closed evaluator instead of being silently repaired.
        envelope.setdefault("environment_digest", "0" * 96)
    preimage = _receipt_preimage(envelope)
    envelope["receipt_preimage_b64"] = base64.b64encode(preimage).decode("ascii")
    envelope["receipt_digest"] = hashlib.sha384(preimage).hexdigest().upper()


def _query_evidence(job: dict[str, Any]) -> dict[str, Any]:
    basic_raw = struct.pack(
        "<qqqqIIIIQQQQQQ", job["user_time_ns"] // 100,
        job["kernel_time_ns"] // 100, 0, 0, job["total_page_faults"],
        job["total_processes"], job["active_processes_at_final_query"],
        job["total_terminated_processes"],
        job["read_operations"], job["write_operations"], job["other_operations"],
        job["read_transfer_bytes"], job["write_transfer_bytes"],
        job["other_transfer_bytes"])
    extended_raw = bytearray(144)
    struct.pack_into("<Q", extended_raw, 136, job["peak_committed_bytes"])
    def row(name: str, size: int, raw: bytes) -> dict[str, Any]:
        return {"query_status_code": 0, "information_class": name,
                "structure_version": 1, "abi": "WINDOWS_64BIT",
                "structure_size_bytes": size, "returned_size_bytes": len(raw),
                "collected_after_terminal_barrier": True,
                "raw_bytes_b64": base64.b64encode(raw).decode("ascii"),
                "raw_bytes_sha384": sha384(raw)}
    return {"basic_and_io": row("JobObjectBasicAndIoAccountingInformation", 96, basic_raw),
            "extended_limit": row("JobObjectExtendedLimitInformation", 144,
                                  bytes(extended_raw))}


def _physical_evidence(job: dict[str, Any], ordinal: int) -> dict[str, Any]:
    pid = job["root_process_id"]
    start_key = f"{ordinal + 1:016X}"
    processes = [{"process_id": pid, "process_start_key": start_key,
                  "parent_process_id": None, "parent_process_start_key": None,
                  "job_object_id": job["job_object_id"], "assigned_before_resume": True,
                  "membership_source": "JOB_ASSIGNMENT_PROCESS_ETW_AND_FINAL_QUERY",
                  "started_qpc": 1, "ended_qpc": 30, "terminal_status": "EXITED"}]
    membership_digest = sha384(processes)
    return {
        "harness_identity": {
            "harness_artifact_digest": sha384("MBCX01.R13.HARNESS.ARTIFACT"),
            "harness_build_digest": sha384("MBCX01.R13.HARNESS.BUILD"),
            "host_environment_digest": sha384("MBCX01.R13.HOST.ENVIRONMENT"),
            "harness_configuration_digest": sha384("MBCX01.R13.HARNESS.CONFIGURATION")},
        "environment": {"execution_environment": "BARE_METAL_WINDOWS",
                        "host_architecture": "WINDOWS_64BIT",
                        "nested_virtualization": False,
                        "guest_pmu_exposure": "NOT_APPLICABLE",
                        "guest_pmu_capability_receipt_digest": None},
        "process_membership": {"root_process_id": pid,
                               "root_process_start_key": start_key,
                               "membership_complete": True,
                               "membership_snapshot_digest": membership_digest,
                               "processes": processes},
        "job_queries": _query_evidence(job),
        "completion": {"completion_port_drained": True, "active_zero_message_seen": True,
                       "new_process_messages": 1, "exit_process_messages": 1,
                       "diagnostic_messages_complete": True,
                       "diagnostics_query_succeeded": True,
                       "final_active_processes": 0, "all_members_terminal": True},
        "external_enforcement": {
            "policy_id": "POLICY.R13.NO.EXTERNAL.COMPUTE",
            "policy_artifact_digest": sha384("MBCX01.R13.EXTERNAL.POLICY"),
            "applied_before_resume": True, "enforcement_owner_role": "SUPERVISOR",
            "deny_outbound_network": True, "deny_external_compute_brokers": True,
            "deny_preexisting_helper_delegation": True,
            "external_compute_endpoint_count": 0,
            "validation_receipt_digest": sha384("MBCX01.R13.EXTERNAL.VALIDATION")},
        "trace": {"mode": job["instruction_backend"],
                  "profile_source": job["instruction_profile_source"],
                  "event_list": job["instruction_event_list"],
                  "attribution": job["instruction_attribution"],
                  "capability_query_succeeded": job["etw_capability_query_succeeded"],
                  "pmc_source_available": job["etw_pmc_source_available"],
                  "max_pmc_counters": job["etw_max_pmc_counters"],
                  "counter_owner_conflict_count": job["etw_counter_owner_conflict_count"],
                  "strict_mode": job["etw_pmc_strict_mode"],
                  "multiplexing_detected": job["etw_pmc_multiplexing_detected"],
                  "events_lost": job["etw_events_lost"],
                  "log_buffers_lost": job["etw_log_buffers_lost"],
                  "realtime_buffers_lost": job["etw_realtime_buffers_lost"],
                  "attribution_complete": job["etw_attribution_complete"],
                  "capability_query": {
                      "query_status_code": 0,
                      "counter_information_class": "TracePmcCounterListInfo",
                      "event_information_class": "TracePmcEventListInfo",
                      "source_id": 0, "counter_width_bits": 64},
                  "event_attachment": {
                      "counter_query_class": "TracePmcCounterListInfo",
                      "event_query_class": "TracePmcEventListInfo",
                      "profile_source": INSTRUCTION_SOURCE,
                      "event_list": INSTRUCTION_EVENT_LIST, "attached": True},
                  "thread_lifetimes": [{"process_id": pid,
                                        "process_start_key": start_key,
                                        "thread_id": pid * 10,
                                        "started_qpc": 2, "ended_qpc": 29}],
                  # AMENDMENT-3 (r7 totality): the fixture stream begins at
                  # the member's first switch-out with no predecessor —
                  # capture-start, so the row carries that first record's OWN
                  # counter and the first delta stays a declared zero. Every
                  # observed processor carries exactly one row; an empty list
                  # beside observations is the forgotten-field shape and is
                  # refused.
                  "cswitch_first_member_baselines": [
                      {"processor": 0, "counter_value": 100}],
                  "cswitch_observations": [
                      {"sequence": 0, "processor": 0, "qpc": 10,
                       "old_thread_id": pid * 10, "counter_value": 100,
                       "delta_from_previous": 0, "process_id": pid,
                       "process_start_key": start_key},
                      {"sequence": 1, "processor": 0, "qpc": 20,
                       "old_thread_id": pid * 10,
                       "counter_value": 100 + job["retired_instructions"],
                       "delta_from_previous": job["retired_instructions"],
                       "process_id": pid, "process_start_key": start_key}],
                  "aggregate_retired_instructions": job["retired_instructions"]}}


def baseline_receipt_rows(candidate_id: str = "CANDIDATE.BASELINE",
                          generator_digest: str = "A" * 96, *,
                          run_id: str = "RUN.R13.NO-PAID.TEST") -> list[dict[str, Any]]:
    envelopes = []
    for h in H_VALUES:
        for d in D_VALUES:
            for f in F_VALUES:
                job = {
                    "receipt_source": "WINDOWS_JOB_OBJECT_HARNESS_V2",
                    "job_object_id": f"JOB.{h}.{d}.{f}", "root_process_id": 1000 + len(envelopes),
                    "created_suspended": True, "completion_port_associated_before_resume": True,
                    "assigned_before_resume": True, "breakaway_enabled": False,
                    "silent_breakaway_enabled": False, "active_processes_at_final_query": 0,
                    "total_page_faults": 0, "total_processes": 1,
                    "total_terminated_processes": 0,
                    "completion_port_drained": True, "user_time_ns": 600000,
                    "kernel_time_ns": 400000, "read_operations": 2, "write_operations": 1,
                    "other_operations": 0, "read_transfer_bytes": 4096,
                    "write_transfer_bytes": 1024, "other_transfer_bytes": 0,
                    "peak_committed_bytes": 16777216, "elapsed_monotonic_ns": 2000000,
                    "retired_instructions": 100000, "instruction_backend": INSTRUCTION_MODE,
                    "instruction_profile_source": INSTRUCTION_SOURCE,
                    "instruction_event_list": INSTRUCTION_EVENT_LIST,
                    "instruction_attribution": INSTRUCTION_ATTRIBUTION,
                    "etw_capability_query_succeeded": True,
                    "etw_pmc_source_available": True, "etw_max_pmc_counters": 4,
                    "etw_counter_owner_conflict_count": 0, "etw_pmc_strict_mode": True,
                    "etw_pmc_multiplexing_detected": False, "etw_events_lost": 0,
                    "etw_log_buffers_lost": 0, "etw_realtime_buffers_lost": 0,
                    "etw_attribution_complete": True,
                }
                job["evidence"] = _physical_evidence(job, len(envelopes))
                receipt = {"schema_id": "MeasurementReceiptV3", "candidate_id": candidate_id,
                           "candidate_artifact_digest": sha384(
                               f"MBCX01.R13.CARRIER.ARTIFACT.{candidate_id}"),
                           "generator_digest": generator_digest, "H": h, "D": d, "F": f,
                           "external_work_policy": "NETWORK_EGRESS_DENIED_NO_EXTERNAL_COMPUTE",
                           "job_receipt": job}
                envelope = {"schema_id": "SignedMeasurementReceiptV1",
                            "domain": ENVELOPE_DOMAIN, "version": 1,
                            "algorithm": SIGNATURE_ALGORITHM, "signing_key_id": TEST_KEY_ID,
                            "run_id": run_id, "cell_id": _cell_id(receipt), "receipt": receipt,
                            "receipt_preimage_b64": "", "receipt_digest": "",
                            "signature_b64": "", "fixture_kind": "NO_PAID_TEST_FIXTURE",
                            "producer_role": "NO_PAID_TEST_HARNESS",
                            "trust_policy_digest":
                                "90D0104E044F68A4BD1DE6653B89EE36C7F99FD87D1F96AAA4FB7619834762A5038F2C214654903207135F6BB8861C49",
                            "subject_digest": "", "environment_digest": ""}
                refresh_receipt_hash(envelope)
                envelopes.append(envelope)
    return envelopes


def _verify_envelope_structure(envelope: Any, expected_run_id: str,
                               trust_roots: dict[str, dict[str, Any]]) -> tuple[dict[str, Any] | None,
                                                                                 set[str]]:
    errors: set[str] = set()
    if not isinstance(envelope, dict) or set(envelope) != ENVELOPE_KEYS:
        return None, {"MEASUREMENT_ENVELOPE_INVALID"}
    receipt = envelope.get("receipt")
    root = trust_roots.get(envelope.get("signing_key_id"))
    if (envelope.get("schema_id") != "SignedMeasurementReceiptV1"
            or envelope.get("domain") != ENVELOPE_DOMAIN or envelope.get("version") != 1
            or envelope.get("algorithm") != SIGNATURE_ALGORITHM
            or SEMANTIC_RE.fullmatch(str(envelope.get("run_id", ""))) is None
            or envelope.get("run_id") != expected_run_id
            or root is None
            or envelope.get("fixture_kind") != root.get("authorized_fixture_kind")
            or envelope.get("producer_role") != root.get("authorized_producer_role")
            or envelope.get("trust_policy_digest") != root.get("trust_policy_digest")
            or not isinstance(receipt, dict)):
        errors.add("MEASUREMENT_ENVELOPE_INVALID")
    if isinstance(receipt, dict):
        try:
            expected_cell = _cell_id(receipt)
        except (KeyError, TypeError):
            expected_cell = None
        if envelope.get("cell_id") != expected_cell or envelope.get("run_id") != expected_run_id:
            errors.add("MEASUREMENT_REPLAY_IDENTITY_MISMATCH")
        if (envelope.get("subject_digest") != sha384(receipt)
                or envelope.get("environment_digest") != receipt.get("job_receipt", {}).get(
                    "evidence", {}).get("harness_identity", {}).get("host_environment_digest")):
            errors.add("MEASUREMENT_ENVELOPE_INVALID")
    if envelope.get("signing_key_id") not in trust_roots:
        errors.add("MEASUREMENT_SIGNATURE_INVALID")
        return receipt if isinstance(receipt, dict) else None, errors
    try:
        preimage = _receipt_preimage(envelope)
        supplied = base64.b64decode(envelope.get("receipt_preimage_b64", ""), validate=True)
        signature = base64.b64decode(envelope.get("signature_b64", ""), validate=True)
        if (supplied != preimage or len(signature) != 64
                or envelope.get("receipt_digest") != hashlib.sha384(preimage).hexdigest().upper()):
            errors.add("MEASUREMENT_SIGNATURE_INVALID")
    except (ValueError, TypeError, KeyError):
        errors.add("MEASUREMENT_SIGNATURE_INVALID")
    return receipt if isinstance(receipt, dict) else None, errors


def _validate_query_evidence(job: dict[str, Any], queries: Any,
                             membership_count: int | None = None) -> set[str]:
    errors: set[str] = set()
    if not isinstance(queries, dict) or set(queries) != QUERY_BUNDLE_KEYS:
        return {"PHYSICAL_EVIDENCE_INCOMPLETE"}
    specs = (("basic_and_io", "JobObjectBasicAndIoAccountingInformation", 96),
             ("extended_limit", "JobObjectExtendedLimitInformation", 144))
    raw: dict[str, bytes] = {}
    for key, class_name, size in specs:
        row = queries.get(key)
        if (not isinstance(row, dict) or set(row) != QUERY_KEYS
                or row.get("query_status_code") != 0
                or row.get("information_class") != class_name
                or row.get("structure_version") != 1 or row.get("abi") != "WINDOWS_64BIT"
                or row.get("structure_size_bytes") != size
                or row.get("returned_size_bytes") != size
                or row.get("collected_after_terminal_barrier") is not True):
            errors.add("JOB_QUERY_EVIDENCE_INVALID"); continue
        try:
            decoded = base64.b64decode(row.get("raw_bytes_b64", ""), validate=True)
        except (ValueError, TypeError):
            decoded = b""
        if len(decoded) != size or row.get("raw_bytes_sha384") != sha384(decoded):
            errors.add("JOB_QUERY_EVIDENCE_INVALID"); continue
        raw[key] = decoded
    if "basic_and_io" in raw:
        try:
            values = struct.unpack("<qqqqIIIIQQQQQQ", raw["basic_and_io"])
            expected_tail = (job["read_operations"], job["write_operations"],
                             job["other_operations"], job["read_transfer_bytes"],
                             job["write_transfer_bytes"], job["other_transfer_bytes"])
            if (values[:4] != (job["user_time_ns"] // 100,
                               job["kernel_time_ns"] // 100, 0, 0)
                    or values[4] != job["total_page_faults"]
                    or membership_count is None
                    or values[5] != job["total_processes"]
                    or values[5] != membership_count
                    or values[6] != job["active_processes_at_final_query"]
                    or values[7] != job["total_terminated_processes"]
                    or job["total_terminated_processes"] != 0
                    or values[8:] != expected_tail
                    or job["user_time_ns"] % 100 or job["kernel_time_ns"] % 100):
                errors.add("JOB_QUERY_EVIDENCE_INVALID")
        except (KeyError, struct.error, TypeError):
            errors.add("JOB_QUERY_EVIDENCE_INVALID")
    if "extended_limit" in raw:
        try:
            if struct.unpack_from("<Q", raw["extended_limit"], 136)[0] != job[
                    "peak_committed_bytes"]:
                errors.add("JOB_QUERY_EVIDENCE_INVALID")
        except (KeyError, struct.error, TypeError):
            errors.add("JOB_QUERY_EVIDENCE_INVALID")
    return errors


def _process_intervals(processes: Any) -> dict[tuple[Any, Any], tuple[int, int]]:
    """`(process_id, process_start_key) -> (started_qpc, ended_qpc)` (AMENDMENT-2).

    The membership roster already has to carry both ends of every incarnation's
    life; nothing read them. They are what makes a (PID, start key) pair a fact
    about a WINDOW OF TIME rather than a label, which is what a thread lifetime
    has to be nested inside for its retired instructions to be that member's.
    """
    intervals: dict[tuple[Any, Any], tuple[int, int]] = {}
    if not isinstance(processes, list):
        return intervals
    for process in processes:
        if not isinstance(process, dict):
            continue
        started = process.get("started_qpc")
        ended = process.get("ended_qpc")
        if (isinstance(started, int) and not isinstance(started, bool)
                and isinstance(ended, int) and not isinstance(ended, bool)):
            intervals[(process.get("process_id"),
                       process.get("process_start_key"))] = (started, ended)
    return intervals


def _validate_physical_evidence(job: dict[str, Any], evidence: Any) -> set[str]:
    errors: set[str] = set()
    if not isinstance(evidence, dict) or set(evidence) != EVIDENCE_KEYS:
        return {"PHYSICAL_EVIDENCE_INCOMPLETE"}
    harness = evidence.get("harness_identity")
    if (not isinstance(harness, dict) or set(harness) != HARNESS_IDENTITY_KEYS
            or any(SHA384_RE.fullmatch(str(value)) is None for value in harness.values())):
        errors.add("PHYSICAL_EVIDENCE_INCOMPLETE")
    environment = evidence.get("environment")
    if not isinstance(environment, dict) or set(environment) != ENVIRONMENT_KEYS:
        errors.add("PHYSICAL_EVIDENCE_INCOMPLETE")
    else:
        kind = environment.get("execution_environment")
        guest_ok = (kind == "HYPER_V_GUEST"
                    and environment.get("guest_pmu_exposure") == "EXPLICITLY_ENABLED"
                    and SHA384_RE.fullmatch(str(
                        environment.get("guest_pmu_capability_receipt_digest"))) is not None)
        native_ok = (kind in {"BARE_METAL_WINDOWS", "HYPER_V_ROOT_PARTITION"}
                     and environment.get("guest_pmu_exposure") == "NOT_APPLICABLE"
                     and environment.get("guest_pmu_capability_receipt_digest") is None)
        if (environment.get("host_architecture") != "WINDOWS_64BIT"
                or environment.get("nested_virtualization") is not False
                or not (native_ok or guest_ok)):
            errors.add("UNSUPPORTED_MEASUREMENT_ENVIRONMENT")
    membership = evidence.get("process_membership")
    pairs: set[tuple[int, str]] = set()
    #: AMENDMENT-2: the same rows, read as WINDOWS OF TIME. Empty unless the
    #: membership roster itself validated, so a thread can never nest inside an
    #: incarnation this function has not already accepted.
    process_intervals: dict[tuple[Any, Any], tuple[int, int]] = {}
    if not isinstance(membership, dict) or set(membership) != MEMBERSHIP_KEYS:
        errors.add("PHYSICAL_EVIDENCE_INCOMPLETE")
    else:
        processes = membership.get("processes")
        valid_processes = isinstance(processes, list) and bool(processes)
        if valid_processes:
            for process in processes:
                if (not isinstance(process, dict) or set(process) != PROCESS_KEYS
                        or not isinstance(process.get("process_id"), int)
                        or isinstance(process.get("process_id"), bool) or process["process_id"] <= 0
                        or re.fullmatch(r"[0-9A-F]{16}", str(process.get("process_start_key"))) is None
                        or process.get("job_object_id") != job.get("job_object_id")
                        or process.get("assigned_before_resume") is not True
                        or process.get("membership_source") !=
                        "JOB_ASSIGNMENT_PROCESS_ETW_AND_FINAL_QUERY"
                        or not isinstance(process.get("started_qpc"), int)
                        or isinstance(process.get("started_qpc"), bool)
                        or not isinstance(process.get("ended_qpc"), int)
                        or isinstance(process.get("ended_qpc"), bool)
                        or process["started_qpc"] >= process["ended_qpc"]
                        or process.get("terminal_status") != "EXITED"):
                    valid_processes = False; break
                pairs.add((process["process_id"], process["process_start_key"]))
            valid_processes = valid_processes and len(pairs) == len(processes)
            if valid_processes:
                process_intervals = _process_intervals(processes)
        root_pair = (membership.get("root_process_id"), membership.get("root_process_start_key"))
        if valid_processes:
            for process in processes:
                pair = (process["process_id"], process["process_start_key"])
                parent_id = process["parent_process_id"]
                parent_key = process["parent_process_start_key"]
                if pair == root_pair:
                    if parent_id is not None or parent_key is not None:
                        valid_processes = False
                elif (not isinstance(parent_id, int) or isinstance(parent_id, bool)
                      or parent_id <= 0
                      or re.fullmatch(r"[0-9A-F]{16}", str(parent_key)) is None
                      or (parent_id, parent_key) not in pairs):
                    valid_processes = False
        if (not valid_processes or root_pair not in pairs
                or membership.get("root_process_id") != job.get("root_process_id")
                or membership.get("membership_complete") is not True
                or membership.get("membership_snapshot_digest") != sha384(processes)):
            errors.add("PROCESS_MEMBERSHIP_INVALID")
    membership_count = (len(membership.get("processes", []))
                        if isinstance(membership, dict)
                        and isinstance(membership.get("processes"), list) else None)
    errors.update(_validate_query_evidence(job, evidence.get("job_queries"), membership_count))
    completion = evidence.get("completion")
    if (not isinstance(completion, dict) or set(completion) != COMPLETION_KEYS):
        errors.add("PHYSICAL_EVIDENCE_INCOMPLETE")
    elif (not isinstance(completion.get("completion_port_drained"), bool)
          or not isinstance(completion.get("active_zero_message_seen"), bool)
          or not isinstance(completion.get("diagnostic_messages_complete"), bool)
          or completion.get("diagnostics_query_succeeded") is not True
          or completion.get("final_active_processes") != 0
          or completion.get("all_members_terminal") is not True
          or membership_count is None
          or any(not isinstance(completion.get(name), int)
                 or isinstance(completion.get(name), bool) or completion[name] < 0
                 for name in ("new_process_messages", "exit_process_messages"))):
        errors.add("COMPLETION_EVIDENCE_INCOMPLETE")
    external = evidence.get("external_enforcement")
    if (not isinstance(external, dict) or set(external) != EXTERNAL_KEYS):
        errors.add("PHYSICAL_EVIDENCE_INCOMPLETE")
    elif (SEMANTIC_RE.fullmatch(str(external.get("policy_id", ""))) is None
          or SHA384_RE.fullmatch(str(external.get("policy_artifact_digest", ""))) is None
          or external.get("applied_before_resume") is not True
          or external.get("enforcement_owner_role") != "SUPERVISOR"
          or external.get("deny_outbound_network") is not True
          or external.get("deny_external_compute_brokers") is not True
          or external.get("deny_preexisting_helper_delegation") is not True
          or external.get("external_compute_endpoint_count") != 0
          or SHA384_RE.fullmatch(str(external.get("validation_receipt_digest", ""))) is None):
        errors.add("EXTERNAL_WORK_UNMEASURED")
    trace = evidence.get("trace")
    trace_map = {"mode": "instruction_backend", "profile_source": "instruction_profile_source",
                 "event_list": "instruction_event_list", "attribution": "instruction_attribution",
                 "capability_query_succeeded": "etw_capability_query_succeeded",
                 "pmc_source_available": "etw_pmc_source_available",
                 "max_pmc_counters": "etw_max_pmc_counters",
                 "counter_owner_conflict_count": "etw_counter_owner_conflict_count",
                 "strict_mode": "etw_pmc_strict_mode",
                 "multiplexing_detected": "etw_pmc_multiplexing_detected",
                 "events_lost": "etw_events_lost", "log_buffers_lost": "etw_log_buffers_lost",
                 "realtime_buffers_lost": "etw_realtime_buffers_lost",
                 "attribution_complete": "etw_attribution_complete"}
    if (not isinstance(trace, dict) or set(trace) != TRACE_KEYS
            or any(trace.get(left) != job.get(right) for left, right in trace_map.items())):
        errors.add("INSTRUCTION_ACCOUNTING_INCOMPLETE")
    else:
        capability = trace["capability_query"]
        attachment = trace["event_attachment"]
        threads = trace["thread_lifetimes"]
        observations = trace["cswitch_observations"]
        baselines = trace["cswitch_first_member_baselines"]
        trace_ok = (
            isinstance(capability, dict) and set(capability) == CAPABILITY_QUERY_KEYS
            and capability.get("query_status_code") == 0
            and capability.get("counter_information_class") == "TracePmcCounterListInfo"
            and capability.get("event_information_class") == "TracePmcEventListInfo"
            and isinstance(capability.get("source_id"), int)
            and not isinstance(capability.get("source_id"), bool)
            and capability.get("counter_width_bits") == 64
            and isinstance(attachment, dict) and set(attachment) == EVENT_ATTACHMENT_KEYS
            and attachment == {"counter_query_class": "TracePmcCounterListInfo",
                               "event_query_class": "TracePmcEventListInfo",
                               "profile_source": INSTRUCTION_SOURCE,
                               "event_list": INSTRUCTION_EVENT_LIST,
                               "attached": True}
            and isinstance(threads, list) and bool(threads)
            and isinstance(observations, list) and len(observations) >= 2
            and isinstance(baselines, list))
        thread_map: dict[int, list[dict[str, Any]]] = {}
        intervals = process_intervals
        if trace_ok:
            for thread in threads:
                pair = (thread.get("process_id"), thread.get("process_start_key")) \
                    if isinstance(thread, dict) else None
                if (not isinstance(thread, dict) or set(thread) != THREAD_LIFETIME_KEYS
                        or pair not in pairs
                        or not isinstance(thread.get("thread_id"), int)
                        or isinstance(thread.get("thread_id"), bool) or thread["thread_id"] <= 0
                        or not isinstance(thread.get("started_qpc"), int)
                        or isinstance(thread.get("started_qpc"), bool)
                        or not isinstance(thread.get("ended_qpc"), int)
                        or isinstance(thread.get("ended_qpc"), bool)
                        or thread["started_qpc"] >= thread["ended_qpc"]
                        # AMENDMENT-2: the thread must NEST inside the process
                        # incarnation whose start key it carries. A PID is
                        # reused, so the pair alone says nothing about WHEN.
                        or pair not in intervals
                        or not (intervals[pair][0] <= thread["started_qpc"]
                                and thread["ended_qpc"] <= intervals[pair][1])
                        # AMENDMENT-2: a TID may carry SEVERAL lifetimes, but
                        # only DISJOINT ones — overlapping (or merely touching)
                        # lives would make the observation join ambiguous.
                        or any(thread["started_qpc"] <= row["ended_qpc"]
                               and row["started_qpc"] <= thread["ended_qpc"]
                               for row in thread_map.get(thread["thread_id"], ()))):
                    trace_ok = False; break
                thread_map.setdefault(thread["thread_id"], []).append(thread)
        previous_by_processor: dict[int, int] = {}
        # AMENDMENT-3: seed each baselined processor with its predecessor's
        # counter, so the first member interval is COUNTED — the first
        # observation's delta must equal counter_value - baseline. A processor
        # with no baseline row keeps the declared capture-start zero. Rows are
        # exact-shape, non-negative, unique per processor, and every baselined
        # processor must actually carry observations; anything else refuses.
        observed_processors: set[int] = set()
        if trace_ok:
            for row in baselines:
                if (not isinstance(row, dict)
                        or set(row) != {"processor", "counter_value"}
                        or not all(isinstance(row.get(name), int)
                                   and not isinstance(row.get(name), bool)
                                   and row[name] >= 0
                                   for name in ("processor", "counter_value"))
                        or row["processor"] in previous_by_processor):
                    trace_ok = False; break
                previous_by_processor[row["processor"]] = row["counter_value"]
        baselined_processors = set(previous_by_processor)
        delta_total = 0
        if trace_ok:
            for sequence, observation in enumerate(observations):
                if (not isinstance(observation, dict)
                        or set(observation) != CSWITCH_OBSERVATION_KEYS
                        or observation.get("sequence") != sequence
                        or not all(isinstance(observation.get(name), int)
                                   and not isinstance(observation.get(name), bool)
                                   and observation[name] >= 0
                                   for name in ("processor", "qpc", "old_thread_id",
                                                "counter_value", "delta_from_previous",
                                                "process_id"))
                        or (observation["process_id"],
                            observation.get("process_start_key")) not in pairs
                        or observation["old_thread_id"] not in thread_map):
                    trace_ok = False; break
                # AMENDMENT-2: resolve by TID *and* QPC. The lifetimes of one
                # TID are disjoint by the rule above, so at most one contains
                # this observation; none means the delta is unattributable and
                # is never summed into a member's retired-instruction total.
                containing = [row for row in thread_map[observation["old_thread_id"]]
                              if row["started_qpc"] <= observation["qpc"]
                              <= row["ended_qpc"]]
                if len(containing) != 1:
                    trace_ok = False; break
                thread = containing[0]
                prior = previous_by_processor.get(observation["processor"])
                expected_delta = 0 if prior is None else observation["counter_value"] - prior
                if (observation["process_id"] != thread["process_id"]
                        or observation["process_start_key"] != thread["process_start_key"]
                        or expected_delta < 0
                        or observation["delta_from_previous"] != expected_delta):
                    trace_ok = False; break
                previous_by_processor[observation["processor"]] = observation["counter_value"]
                observed_processors.add(observation["processor"])
                delta_total += expected_delta
        # AMENDMENT-3, r7 totality rule: the baselined set must EQUAL the
        # observed set. A baseline for an unobserved processor is evidence
        # about nothing; an OBSERVED processor with no baseline row is the
        # empty-but-forgotten shape that silently reproduced the pre-amendment
        # undercount (r7, three seats convergent — SEAT2 pushed it through
        # full production admission wrong by 1,000,000). The scope emits a row
        # for every observed processor (capture-start rows carry the first
        # record's own counter, so their delta stays the declared zero), so
        # equality cannot refuse a truthful capture.
        if trace_ok and baselined_processors != observed_processors:
            trace_ok = False
        if (not trace_ok or trace.get("aggregate_retired_instructions") != delta_total
                or delta_total != job.get("retired_instructions")):
            errors.add("INSTRUCTION_ACCOUNTING_INCOMPLETE")
    return errors


def evaluate_measurement_receipts(envelopes: list[dict[str, Any]], *,
                                  expected_run_id: str) -> list[str]:
    errors: set[str] = set()
    try:
        trust_roots = _load_trust_roots()
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return ["MEASUREMENT_TRUST_ROOT_INVALID", "PHYSICAL_HARNESS_UNAVAILABLE"]
    if not isinstance(envelopes, list):
        return ["MEASUREMENT_ENVELOPE_INVALID", "PHYSICAL_HARNESS_UNAVAILABLE"]
    receipts = []
    signature_candidates = []
    for envelope in envelopes:
        receipt, envelope_errors = _verify_envelope_structure(
            envelope, expected_run_id, trust_roots)
        errors.update(envelope_errors)
        if receipt is not None:
            receipts.append(receipt)
        if (isinstance(envelope, dict) and set(envelope) == ENVELOPE_KEYS
                and envelope.get("signing_key_id") in trust_roots
                and "MEASUREMENT_SIGNATURE_INVALID" not in envelope_errors):
            signature_candidates.append(envelope)
    if signature_candidates:
        items = [{"payload_b64": envelope["receipt_preimage_b64"],
                  "public_key_pem": trust_roots[envelope["signing_key_id"]]["public_key_pem"],
                  "signature_b64": envelope["signature_b64"]}
                 for envelope in signature_candidates]
        try:
            if not all(_invoke_signature_verifier(items)):
                errors.add("MEASUREMENT_SIGNATURE_INVALID")
        except ValueError:
            errors.add("MEASUREMENT_SIGNATURE_INVALID")
    if len(envelopes) != 100 or len(receipts) != 100:
        errors.add("GRID_COVERAGE_INVALID")
    candidate_ids = {row.get("candidate_id") for row in receipts}
    candidate_artifacts = {row.get("candidate_artifact_digest") for row in receipts}
    generator_ids = {row.get("generator_digest") for row in receipts}
    if len(candidate_ids) != 1:
        errors.add("CANDIDATE_ID_MISMATCH")
    if len(candidate_artifacts) != 1:
        errors.add("GRID_IDENTITY_MISMATCH")
    if len(generator_ids) != 1:
        errors.add("GENERATOR_ID_MISMATCH")
    grid_identity_hashes = set()
    for envelope in envelopes:
        try:
            grid_identity_hashes.add(sha384(_grid_identity_preimage(envelope)))
        except (KeyError, TypeError):
            errors.add("GRID_IDENTITY_MISMATCH")
    if len(grid_identity_hashes) != 1:
        errors.add("GRID_IDENTITY_MISMATCH")
    valid_rows = []
    coordinates = []
    for row in receipts:
        job = row.get("job_receipt")
        if (set(row) != RECEIPT_KEYS or row.get("schema_id") != "MeasurementReceiptV3"
                or SEMANTIC_RE.fullmatch(str(row.get("candidate_id", ""))) is None
                or SHA384_RE.fullmatch(
                    str(row.get("candidate_artifact_digest", ""))) is None
                or SHA384_RE.fullmatch(str(row.get("generator_digest", ""))) is None
                or any(not isinstance(row.get(axis), int) or isinstance(row.get(axis), bool)
                       for axis in ("H", "D", "F"))
                or row.get("H") not in H_VALUES or row.get("D") not in D_VALUES
                or row.get("F") not in F_VALUES or not isinstance(job, dict)
                or set(job or {}) != JOB_KEYS):
            errors.add("MEASUREMENT_SCHEMA_INVALID")
            continue
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
            errors.add("MEASUREMENT_SCHEMA_INVALID")
            continue
        coordinates.append((row["H"], row["D"], row["F"]))
        if (job["receipt_source"] != "WINDOWS_JOB_OBJECT_HARNESS_V2"
                or SEMANTIC_RE.fullmatch(str(job["job_object_id"])) is None
                or job["root_process_id"] <= 0 or job["created_suspended"] is not True
                or job["completion_port_associated_before_resume"] is not True
                or job["assigned_before_resume"] is not True
                or job["breakaway_enabled"] is not False
                or job["silent_breakaway_enabled"] is not False
                or job["active_processes_at_final_query"] != 0
                or job["completion_port_drained"] is not True):
            errors.add("DESCENDANT_ACCOUNTING_MISSING")
        if (job["instruction_backend"] not in {INSTRUCTION_MODE, "ETW_PMC_SAMPLED_PROFILE_V1"}
                or job["instruction_profile_source"] != INSTRUCTION_SOURCE
                or job["instruction_event_list"] != INSTRUCTION_EVENT_LIST
                or job["instruction_attribution"] != INSTRUCTION_ATTRIBUTION
                or job["retired_instructions"] <= 0):
            errors.add("INSTRUCTION_ACCOUNTING_MISSING")
        if job["instruction_backend"] != INSTRUCTION_MODE:
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
        if job["elapsed_monotonic_ns"] <= 0:
            errors.add("MEASUREMENT_SCHEMA_INVALID")
        if row["external_work_policy"] != "NETWORK_EGRESS_DENIED_NO_EXTERNAL_COMPUTE":
            errors.add("EXTERNAL_WORK_UNMEASURED")
        errors.update(_validate_physical_evidence(job, job.get("evidence")))
        valid_rows.append(row)
    expected = {(h, d, f) for h in H_VALUES for d in D_VALUES for f in F_VALUES}
    if set(coordinates) != expected or len(coordinates) != len(set(coordinates)):
        errors.add("GRID_COVERAGE_INVALID")
    for row in valid_rows:
        job = row["job_receipt"]
        if (job["retired_instructions"] > 3_000_000
                or job["user_time_ns"] + job["kernel_time_ns"] > 150_000_000
                or job["peak_committed_bytes"] > 201_326_592
                or job["elapsed_monotonic_ns"] > 300_000_000
                or sum(job[name] for name in ("read_transfer_bytes", "write_transfer_bytes",
                                               "other_transfer_bytes")) > 67_108_864):
            errors.add("AFFORDABILITY_LIMIT")
    for d in D_VALUES:
        for f in F_VALUES:
            group = [row["job_receipt"] for row in valid_rows
                     if row["D"] == d and row["F"] == f]
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
    # The deterministic signer proves the verifier path only. The physical harness
    # remains unbuilt, so no local fixture can create a green physical claim.
    errors.add("PHYSICAL_HARNESS_UNAVAILABLE")
    return sorted(errors)


@dataclass(frozen=True)
class CallLedger:
    schema_id: str
    scenario_id: str
    condition: str
    node: str
    handoff_id: str
    task_packet_hash: str
    served_request_hash: str
    request_parameters_hash: str
    idempotency_token: str
    route_contract_hash: str
    state: str
    raw_response_b64: str | None = None
    raw_response_hash: str | None = None
    response_ref: str | None = None
    provider_request_id: str | None = None
    durability_receipt: dict[str, Any] | None = None
    preaccept_failure_receipt: dict[str, Any] | None = None
    ledger_hash: str = ""

    @classmethod
    def prepare(cls, scenario_id: str, condition: str, node: str, task_packet_hash: str,
                served_request_hash: str, request_parameters_hash: str,
                idempotency_token: str, route_contract_hash: str, *,
                handoff_id: str | None = None) -> "CallLedger":
        exact_handoff = handoff_id or f"HANDOFF.{condition}"
        if (SEMANTIC_RE.fullmatch(scenario_id or "") is None or condition not in {"BC", "OM"}
                or node not in {"A0", "B", "A1"}
                or SEMANTIC_RE.fullmatch(exact_handoff) is None
                or SHA384_RE.fullmatch(task_packet_hash or "") is None
                or SHA256_RE.fullmatch(served_request_hash or "") is None
                or SHA384_RE.fullmatch(request_parameters_hash or "") is None
                or SEMANTIC_RE.fullmatch(idempotency_token or "") is None
                or SHA384_RE.fullmatch(route_contract_hash or "") is None):
            raise ValueError("invalid nonempty call identity")
        return cls("CallLedgerV3", scenario_id, condition, node, exact_handoff, task_packet_hash,
                   served_request_hash, request_parameters_hash, idempotency_token,
                   route_contract_hash, "PREPARED")._rehash()

    def _payload(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if key != "ledger_hash"}

    def _rehash(self) -> "CallLedger":
        return replace(self, ledger_hash=sha384(self._payload()))

    def terminal_missing_reason(self) -> str | None:
        if self.state == "ACCEPTANCE_AMBIGUOUS":
            return "ACCEPTANCE_AMBIGUOUS"
        if self.state == "PROVEN_PRE_ACCEPT_FAILURE":
            return "PROVEN_PRE_ACCEPT_FAILURE"
        return None

    def transition(self, event: str, *, response_bytes: bytes | None = None,
                   response_ref: str | None = None, provider_request_id: str | None = None,
                   durability_receipt: dict[str, Any] | None = None,
                   route_attestation: Any = None,
                   preaccept_failure_receipt: dict[str, Any] | None = None) -> "CallLedger":
        del route_attestation  # Runtime assertions have no authority in r13.
        if self.ledger_hash != sha384(self._payload()):
            raise ValueError("ledger digest mismatch")
        matrix = {
            "PREPARED": {"DISPATCH_CONFIRMED": "DISPATCHED",
                         "PROVEN_NOT_ACCEPTED": "PROVEN_PRE_ACCEPT_FAILURE"},
            "DISPATCHED": {"PROVEN_NOT_ACCEPTED": "PROVEN_PRE_ACCEPT_FAILURE",
                           "CONNECTION_LOST_AFTER_DISPATCH": "ACCEPTANCE_AMBIGUOUS",
                           "RESPONSE_BYTES_FSYNCED": "RESPONSE_DURABLY_RECORDED"},
            "RESPONSE_DURABLY_RECORDED": {}, "PROVEN_PRE_ACCEPT_FAILURE": {},
            "ACCEPTANCE_AMBIGUOUS": {},
        }
        target = matrix.get(self.state, {}).get(event)
        if target is None:
            raise ValueError("illegal ledger transition")
        value = self
        if event == "RESPONSE_BYTES_FSYNCED":
            if (not isinstance(response_bytes, bytes) or not response_bytes
                    or SEMANTIC_RE.fullmatch(response_ref or "") is None
                    or SEMANTIC_RE.fullmatch(provider_request_id or "") is None
                    or not _valid_durability_receipt(self, response_bytes, response_ref,
                                                     provider_request_id, durability_receipt)):
                raise ValueError("durable response evidence required")
            value = replace(value, raw_response_b64=base64.b64encode(response_bytes).decode("ascii"),
                            raw_response_hash=sha384(response_bytes), response_ref=response_ref,
                            provider_request_id=provider_request_id,
                            durability_receipt=copy.deepcopy(durability_receipt))
        if event == "PROVEN_NOT_ACCEPTED":
            if not _valid_preaccept_failure_receipt(self, preaccept_failure_receipt):
                raise ValueError("preaccept failure evidence required")
            value = replace(value, preaccept_failure_receipt=copy.deepcopy(preaccept_failure_receipt))
        return replace(value, state=target)._rehash()

    def serialize(self) -> str:
        return canonical_json(asdict(self)).decode("utf-8")

    @classmethod
    def recover(cls, serialized: str) -> "CallLedger":
        raw = json.loads(serialized)
        if not isinstance(raw, dict) or set(raw) != set(cls.__dataclass_fields__):
            raise ValueError("invalid serialized ledger")
        value = cls(**raw)
        if value.ledger_hash != sha384(value._payload()):
            raise ValueError("ledger digest mismatch")
        if (value.schema_id != "CallLedgerV3"
                or SEMANTIC_RE.fullmatch(value.scenario_id or "") is None
                or value.condition not in {"BC", "OM"} or value.node not in {"A0", "B", "A1"}
                or SEMANTIC_RE.fullmatch(value.handoff_id or "") is None
                or SHA384_RE.fullmatch(value.task_packet_hash or "") is None
                or SHA256_RE.fullmatch(value.served_request_hash or "") is None
                or SHA384_RE.fullmatch(value.request_parameters_hash or "") is None
                or SEMANTIC_RE.fullmatch(value.idempotency_token or "") is None
                or SHA384_RE.fullmatch(value.route_contract_hash or "") is None
                or value.state not in {"PREPARED", "DISPATCHED", "RESPONSE_DURABLY_RECORDED",
                                       "PROVEN_PRE_ACCEPT_FAILURE", "ACCEPTANCE_AMBIGUOUS"}):
            raise ValueError("recovered ledger schema invalid")
        if value.state == "RESPONSE_DURABLY_RECORDED":
            try:
                response_bytes = base64.b64decode(value.raw_response_b64 or "", validate=True)
            except Exception as exc:
                raise ValueError("response bytes invalid") from exc
            if (not response_bytes or value.raw_response_hash != sha384(response_bytes)
                    or not _valid_durability_receipt(value, response_bytes, value.response_ref,
                                                     value.provider_request_id,
                                                     value.durability_receipt)):
                raise ValueError("durable response evidence invalid")
        elif any(item is not None for item in (value.raw_response_b64, value.raw_response_hash,
                                               value.response_ref, value.provider_request_id,
                                               value.durability_receipt)):
            raise ValueError("response evidence present outside durable state")
        if value.state == "PROVEN_PRE_ACCEPT_FAILURE":
            if not _valid_preaccept_failure_receipt(value, value.preaccept_failure_receipt):
                raise ValueError("preaccept failure evidence invalid")
        elif value.preaccept_failure_receipt is not None:
            raise ValueError("preaccept evidence present outside proven failure state")
        return value


def _ledger_identity(ledger: CallLedger) -> dict[str, Any]:
    return {key: getattr(ledger, key) for key in (
        "scenario_id", "condition", "node", "handoff_id", "task_packet_hash", "served_request_hash",
        "request_parameters_hash", "idempotency_token", "route_contract_hash")}


def durability_receipt_fixture(ledger: CallLedger, response_bytes: bytes,
                               response_ref: str = "RESPONSE.SHARED",
                               provider_request_id: str = "PROVIDER.SHARED") -> dict[str, Any]:
    record = {**_ledger_identity(ledger), "raw_response_hash": sha384(response_bytes),
              "response_ref": response_ref, "provider_request_id": provider_request_id}
    return make_durability_receipt(record, "TXN.SHARED")


def _valid_durability_receipt(ledger: CallLedger, response_bytes: bytes,
                              response_ref: str | None, provider_request_id: str | None,
                              receipt: Any) -> bool:
    record = {**_ledger_identity(ledger), "raw_response_hash": sha384(response_bytes),
              "response_ref": response_ref, "provider_request_id": provider_request_id}
    return valid_durability_receipt(receipt, record)


def preaccept_failure_fixture(ledger: CallLedger) -> dict[str, Any]:
    row = {"schema_id": "PreacceptFailureReceiptV1",
           "ledger_identity_hash": sha384(_ledger_identity(ledger)),
           "failure_code": "TRANSPORT_PROVED_NOT_ACCEPTED",
           "dispatch_probe_ref": "PROBE.SHARED"}
    row["receipt_hash"] = sha384(row)
    return row


def _valid_preaccept_failure_receipt(ledger: CallLedger, row: Any) -> bool:
    required = {"schema_id", "ledger_identity_hash", "failure_code",
                "dispatch_probe_ref", "receipt_hash"}
    return (isinstance(row, dict) and set(row) == required
            and row["schema_id"] == "PreacceptFailureReceiptV1"
            and row["ledger_identity_hash"] == sha384(_ledger_identity(ledger))
            and row["failure_code"] == "TRANSPORT_PROVED_NOT_ACCEPTED"
            and SEMANTIC_RE.fullmatch(row["dispatch_probe_ref"]) is not None
            and row["receipt_hash"] == sha384(
                {key: value for key, value in row.items() if key != "receipt_hash"}))


B_RESPONSE_JOIN_FIELDS = (*CALL_IDENTITY_FIELDS, "raw_response_hash", "response_ref",
                          "provider_request_id", "durability_receipt")
B_BINDING_KEYS = {"schema_id", "ledger_snapshot", "b_response_snapshot", "transaction_id",
                  "durability_receipt_hash", "binding_hash"}


def _binding_without_hash(binding: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in binding.items() if key != "binding_hash"}


def bind_durable_b_response(ledger: CallLedger,
                            b_response: dict[str, Any]) -> dict[str, Any]:
    """Bind one full packet B-call record to the exact full durable ledger snapshot."""
    if not isinstance(b_response, dict):
        raise ValueError("B_LEDGER_MISMATCH")
    try:
        recovered = CallLedger.recover(ledger.serialize())
        if recovered.state != "RESPONSE_DURABLY_RECORDED" or recovered.node != "B":
            raise ValueError
        if any(b_response.get(field) != getattr(recovered, field)
               for field in B_RESPONSE_JOIN_FIELDS if field != "durability_receipt"):
            raise ValueError
        if b_response.get("durability_receipt") != recovered.durability_receipt:
            raise ValueError
        raw_utf8 = b_response.get("raw_response_utf8")
        if not isinstance(raw_utf8, str) or sha384(raw_utf8.encode("utf-8")) != recovered.raw_response_hash:
            raise ValueError
        receipt = recovered.durability_receipt or {}
        binding = {"schema_id": "DurableBResponseBindingV1",
                   "ledger_snapshot": asdict(recovered),
                   "b_response_snapshot": copy.deepcopy(b_response),
                   "transaction_id": receipt["transaction_id"],
                   "durability_receipt_hash": receipt["receipt_hash"],
                   "binding_hash": ""}
        binding["binding_hash"] = sha384(_binding_without_hash(binding))
        return binding
    except (KeyError, TypeError, ValueError, AttributeError) as exc:
        raise ValueError("B_LEDGER_MISMATCH") from exc


def validate_b_response_ledger_binding(binding: Any,
                                       b_response: dict[str, Any]) -> list[str]:
    try:
        if (not isinstance(binding, dict) or set(binding) != B_BINDING_KEYS
                or binding.get("schema_id") != "DurableBResponseBindingV1"
                or binding.get("binding_hash") != sha384(_binding_without_hash(binding))
                or binding.get("b_response_snapshot") != b_response):
            raise ValueError
        ledger = CallLedger.recover(canonical_json(binding["ledger_snapshot"]).decode("utf-8"))
        expected = bind_durable_b_response(ledger, b_response)
        if expected != binding:
            raise ValueError
        receipt = ledger.durability_receipt or {}
        if (binding["transaction_id"] != receipt.get("transaction_id")
                or binding["durability_receipt_hash"] != receipt.get("receipt_hash")):
            raise ValueError
        return []
    except (KeyError, TypeError, ValueError, AttributeError, json.JSONDecodeError):
        return ["B_LEDGER_MISMATCH"]


EPISODE_KEYS = {"schema_id", "episode_id", "scenario_id", "manifest_position", "calls",
                "terminal_class", "missing_positions", "episode_hash"}
EPISODE_LAUNCHED_CALL_KEYS = {"position", "condition", "node", "launch_status",
                              "ledger_snapshot", "ledger_hash"}
EPISODE_SKIPPED_CALL_KEYS = {"position", "condition", "node", "launch_status",
                             "upstream_terminal_position", "upstream_terminal_ledger_hash",
                             "reason", "skip_hash"}
TERMINAL_LEDGER_STATES = {"RESPONSE_DURABLY_RECORDED", "PROVEN_PRE_ACCEPT_FAILURE",
                          "ACCEPTANCE_AMBIGUOUS"}


def build_episode_receipt(scenario_id: str, manifest_position: int,
                          calls: list[Any]) -> dict[str, Any]:
    if (SEMANTIC_RE.fullmatch(scenario_id or "") is None
            or not isinstance(manifest_position, int) or isinstance(manifest_position, bool)
            or manifest_position < 0 or manifest_position >= 768
            or not isinstance(calls, list) or len(calls) != 6):
        raise ValueError("EPISODE_PARTITION_MISMATCH")
    rows = []
    upstream_terminal: dict[str, tuple[str, str]] = {}
    for expected_position, item in zip(EPISODE_POSITIONS, calls):
        condition, node = expected_position.split(".")
        if isinstance(item, CallLedger):
            if condition in upstream_terminal:
                raise ValueError("EPISODE_PARTITION_MISMATCH")
            try:
                recovered = CallLedger.recover(item.serialize())
            except (AttributeError, ValueError, TypeError, json.JSONDecodeError) as exc:
                raise ValueError("EPISODE_PARTITION_MISMATCH") from exc
            if (recovered.scenario_id != scenario_id
                    or f"{recovered.condition}.{recovered.node}" != expected_position
                    or recovered.state not in TERMINAL_LEDGER_STATES):
                raise ValueError("EPISODE_PARTITION_MISMATCH")
            row = {"position": expected_position, "condition": condition, "node": node,
                   "launch_status": "LAUNCHED",
                   "ledger_snapshot": asdict(recovered), "ledger_hash": recovered.ledger_hash}
            rows.append(row)
            if recovered.state != "RESPONSE_DURABLY_RECORDED":
                upstream_terminal[condition] = (expected_position, recovered.ledger_hash)
        else:
            terminal = upstream_terminal.get(condition)
            row = copy.deepcopy(item)
            if (terminal is None or not isinstance(row, dict)
                    or set(row) != EPISODE_SKIPPED_CALL_KEYS
                    or row.get("position") != expected_position
                    or row.get("condition") != condition or row.get("node") != node
                    or row.get("launch_status") != "NOT_LAUNCHED_UPSTREAM_TERMINAL"
                    or row.get("upstream_terminal_position") != terminal[0]
                    or row.get("upstream_terminal_ledger_hash") != terminal[1]
                    or row.get("reason") != "UPSTREAM_TERMINAL"
                    or row.get("skip_hash") != sha384(
                        {key: value for key, value in row.items() if key != "skip_hash"})):
                raise ValueError("EPISODE_PARTITION_MISMATCH")
            rows.append(row)
    missing = [row["position"] for row in rows if row["launch_status"] != "LAUNCHED"
               or row["ledger_snapshot"]["state"] != "RESPONSE_DURABLY_RECORDED"]
    receipt = {"schema_id": "EpisodeReceiptV1",
               "episode_id": "EPISODE." + sha256([scenario_id, manifest_position]),
               "scenario_id": scenario_id, "manifest_position": manifest_position,
               "calls": rows,
               "terminal_class": "WHOLE_PAIR_MISSING" if missing else "COMPLETE_PAIR",
               "missing_positions": missing, "episode_hash": ""}
    receipt["episode_hash"] = sha384({key: value for key, value in receipt.items()
                                      if key != "episode_hash"})
    return receipt


def validate_episode_receipt(receipt: Any, expected_scenario_id: str,
                             expected_manifest_position: int) -> list[str]:
    try:
        if (not isinstance(receipt, dict) or set(receipt) != EPISODE_KEYS
                or receipt.get("schema_id") != "EpisodeReceiptV1"
                or receipt.get("scenario_id") != expected_scenario_id
                or receipt.get("manifest_position") != expected_manifest_position
                or receipt.get("episode_id") != "EPISODE." + sha256(
                    [expected_scenario_id, expected_manifest_position])
                or receipt.get("episode_hash") != sha384(
                    {key: value for key, value in receipt.items() if key != "episode_hash"})
                or not isinstance(receipt.get("calls"), list)
                or len(receipt["calls"]) != 6):
            raise ValueError
        calls = []
        for index, row in enumerate(receipt["calls"]):
            if (not isinstance(row, dict) or row.get("position") != EPISODE_POSITIONS[index]):
                raise ValueError
            if row.get("launch_status") == "LAUNCHED":
                if set(row) != EPISODE_LAUNCHED_CALL_KEYS:
                    raise ValueError
                ledger = CallLedger.recover(
                    canonical_json(row["ledger_snapshot"]).decode("utf-8"))
                if (row["condition"] != ledger.condition or row["node"] != ledger.node
                        or row["position"] != f"{ledger.condition}.{ledger.node}"
                        or row["ledger_hash"] != ledger.ledger_hash):
                    raise ValueError
                calls.append(ledger)
            elif row.get("launch_status") == "NOT_LAUNCHED_UPSTREAM_TERMINAL":
                if set(row) != EPISODE_SKIPPED_CALL_KEYS:
                    raise ValueError
                calls.append(copy.deepcopy(row))
            else:
                raise ValueError
        rebuilt = build_episode_receipt(expected_scenario_id, expected_manifest_position, calls)
        if rebuilt != receipt:
            raise ValueError
        return []
    except (KeyError, TypeError, ValueError, AttributeError, json.JSONDecodeError):
        return ["EPISODE_PARTITION_MISMATCH"]


def episode_receipt_fixture(scenario_id: str, manifest_position: int, *,
                            missing_position: str | None = None) -> dict[str, Any]:
    if missing_position is not None and missing_position not in EPISODE_POSITIONS:
        raise ValueError("unknown missing position")
    calls = []
    upstream_terminal: dict[str, tuple[str, str]] = {}
    for position in EPISODE_POSITIONS:
        condition, node = position.split(".")
        if condition in upstream_terminal:
            upstream_position, upstream_hash = upstream_terminal[condition]
            skipped = {"position": position, "condition": condition, "node": node,
                       "launch_status": "NOT_LAUNCHED_UPSTREAM_TERMINAL",
                       "upstream_terminal_position": upstream_position,
                       "upstream_terminal_ledger_hash": upstream_hash,
                       "reason": "UPSTREAM_TERMINAL"}
            skipped["skip_hash"] = sha384(skipped)
            calls.append(skipped)
            continue
        ledger = CallLedger.prepare(
            scenario_id, condition, node, "A" * 96, "B" * 64, "C" * 96,
            f"IDEM.{manifest_position}.{condition}.{node}", "D" * 96,
            handoff_id=f"HANDOFF.{manifest_position}.{condition}").transition(
                "DISPATCH_CONFIRMED")
        if position == missing_position:
            ledger = ledger.transition("CONNECTION_LOST_AFTER_DISPATCH")
            upstream_terminal[condition] = (position, ledger.ledger_hash)
        else:
            response = canonical_json({"position": position, "scenario_id": scenario_id})
            reference = f"RESPONSE.{manifest_position}.{condition}.{node}"
            provider = f"PROVIDER.{manifest_position}.{condition}.{node}"
            ledger = ledger.transition(
                "RESPONSE_BYTES_FSYNCED", response_bytes=response, response_ref=reference,
                provider_request_id=provider,
                durability_receipt=durability_receipt_fixture(
                    ledger, response, reference, provider))
        calls.append(ledger)
    return build_episode_receipt(scenario_id, manifest_position, calls)


EXACTNESS_RECEIPT_KEYS = {
    "schema_id", "candidate_id", "carrier_artifact_digest",
    "measurement_grid_identity_hash", "suite_id", "suite_artifact_hash",
    "witness_set_hash", "result", "authority_mode", "producer_id",
    "trust_root_id", "receipt_hash",
}
ENGINEERING_EVIDENCE_KEYS = {
    "schema_id", "candidate_id", "run_id", "exactness_receipt",
    "measurement_envelopes", "measurement_evidence_set_hash", "grid_identity_hash",
    "exactness_pass", "accounting_complete", "boundedness_pass",
    "affordability_pass", "worst_cell_metrics", "authority_mode", "evidence_hash",
}


def _exactness_suite_authority() -> tuple[dict[str, Any], str, str]:
    try:
        raw = EXACTNESS_SUITE.read_bytes()
        document = json.loads(raw.decode("utf-8"))
        keys = {"schema_id", "suite_id", "production_ready", "activation_authority",
                "fixture_producer_id", "witness_ids"}
        if (not isinstance(document, dict) or set(document) != keys
                or document.get("schema_id") != "CarrierExactnessSuiteV1"
                or document.get("suite_id") != "MBCX01.R13.CARRIER.EXACTNESS.SUITE"
                or document.get("production_ready") is not False
                or document.get("activation_authority") != "NONE_IN_R13_2"
                or document.get("fixture_producer_id")
                != "FIXTURE.MBCX01.CARRIER.EXACTNESS"
                or not isinstance(document.get("witness_ids"), list)
                or len(document["witness_ids"]) != len(set(document["witness_ids"]))
                or any(SEMANTIC_RE.fullmatch(str(value)) is None
                       for value in document["witness_ids"])):
            raise ValueError
        return document, sha384(raw), sha384(document["witness_ids"])
    except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
        raise ValueError("CARRIER_EXACTNESS_AUTHORITY_INVALID") from exc


def fixture_carrier_exactness_receipt(
        candidate_id: str, envelopes: list[dict[str, Any]]) -> dict[str, Any]:
    if SEMANTIC_RE.fullmatch(candidate_id or "") is None:
        raise ValueError("ENGINEERING_SELECTION_INVALID")
    suite, suite_hash, witness_hash = _exactness_suite_authority()
    try:
        candidate_artifacts = {row["receipt"]["candidate_artifact_digest"]
                               for row in envelopes
                               if row["receipt"]["candidate_id"] == candidate_id}
        if len(envelopes) != 100 or len(candidate_artifacts) != 1:
            raise ValueError
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("ENGINEERING_SELECTION_INVALID") from exc
    receipt = {
        "schema_id": "CarrierExactnessReceiptV2", "candidate_id": candidate_id,
        "carrier_artifact_digest": next(iter(candidate_artifacts)),
        "measurement_grid_identity_hash": measurement_grid_identity_hash(envelopes),
        "suite_id": suite["suite_id"], "suite_artifact_hash": suite_hash,
        "witness_set_hash": witness_hash, "result": "PASS",
        "authority_mode": "FIXTURE_CONFORMANCE",
        "producer_id": suite["fixture_producer_id"], "trust_root_id": None,
    }
    receipt["receipt_hash"] = sha384(receipt)
    return receipt


def _valid_exactness_receipt(receipt: Any, candidate_id: str,
                             envelopes: list[dict[str, Any]], *,
                             require_production_authority: bool) -> bool:
    try:
        suite, suite_hash, witness_hash = _exactness_suite_authority()
        candidate_artifacts = {row["receipt"]["candidate_artifact_digest"]
                               for row in envelopes}
        if require_production_authority:
            # The reviewed physical BUILD must add the production exactness
            # verifier. A mode-label or self-authored hash edit has no authority.
            return False
        return (isinstance(receipt, dict) and set(receipt) == EXACTNESS_RECEIPT_KEYS
                and receipt.get("schema_id") == "CarrierExactnessReceiptV2"
                and receipt.get("candidate_id") == candidate_id
                and len(candidate_artifacts) == 1
                and receipt.get("carrier_artifact_digest") == next(iter(candidate_artifacts))
                and receipt.get("measurement_grid_identity_hash")
                == measurement_grid_identity_hash(envelopes)
                and receipt.get("suite_id") == suite["suite_id"]
                and receipt.get("suite_artifact_hash") == suite_hash
                and receipt.get("witness_set_hash") == witness_hash
                and receipt.get("result") == "PASS"
                and receipt.get("authority_mode") == "FIXTURE_CONFORMANCE"
                and receipt.get("producer_id") == suite["fixture_producer_id"]
                and receipt.get("trust_root_id") is None
                and receipt.get("receipt_hash") == sha384(
                    {key: value for key, value in receipt.items()
                     if key != "receipt_hash"}))
    except (KeyError, TypeError, ValueError, AttributeError):
        return False


def derive_engineering_candidate_evidence(
        exactness_receipt: dict[str, Any], envelopes: list[dict[str, Any]], *,
        expected_run_id: str, require_production_authority: bool = True) -> dict[str, Any]:
    try:
        candidate_ids = {row["receipt"]["candidate_id"] for row in envelopes}
        if len(candidate_ids) != 1:
            raise ValueError
        candidate_id = next(iter(candidate_ids))
        if not _valid_exactness_receipt(
                exactness_receipt, candidate_id, envelopes,
                require_production_authority=require_production_authority):
            raise ValueError("CARRIER_EXACTNESS_AUTHORITY_UNAVAILABLE"
                             if require_production_authority
                             else "ENGINEERING_SELECTION_INVALID")
        evaluation_errors = set(evaluate_measurement_receipts(
            envelopes, expected_run_id=expected_run_id))
        if require_production_authority and "PHYSICAL_HARNESS_UNAVAILABLE" in evaluation_errors:
            raise ValueError("ENGINEERING_AUTHORITY_UNAVAILABLE")
        admitted_errors = evaluation_errors - ({"PHYSICAL_HARNESS_UNAVAILABLE"}
                                               if not require_production_authority else set())
        jobs = [row["receipt"]["job_receipt"] for row in envelopes]
        worst = {
            "retired_instructions": max(job["retired_instructions"] for job in jobs),
            "aggregate_cpu_time_ns": max(job["user_time_ns"] + job["kernel_time_ns"]
                                         for job in jobs),
            "elapsed_monotonic_ns": max(job["elapsed_monotonic_ns"] for job in jobs),
            "peak_committed_bytes": max(job["peak_committed_bytes"] for job in jobs),
            "total_io_transfer_bytes": max(sum(job[name] for name in
                                                ("read_transfer_bytes",
                                                 "write_transfer_bytes",
                                                 "other_transfer_bytes")) for job in jobs),
            "total_io_operations": max(sum(job[name] for name in
                                           ("read_operations", "write_operations",
                                            "other_operations")) for job in jobs),
        }
        identity_hashes = {sha384(_grid_identity_preimage(row)) for row in envelopes}
        if len(identity_hashes) != 1:
            raise ValueError
        evidence = {
            "schema_id": "EngineeringCandidateEvidenceV1", "candidate_id": candidate_id,
            "run_id": expected_run_id, "exactness_receipt": copy.deepcopy(exactness_receipt),
            "measurement_envelopes": copy.deepcopy(envelopes),
            "measurement_evidence_set_hash": sha384(
                [row["receipt_digest"] for row in envelopes]),
            "grid_identity_hash": next(iter(identity_hashes)),
            "exactness_pass": True,
            "accounting_complete": not bool(admitted_errors & {
                "DESCENDANT_ACCOUNTING_MISSING", "INSTRUCTION_ACCOUNTING_MISSING",
                "INSTRUCTION_ACCOUNTING_INCOMPLETE", "INSTRUCTION_ACCOUNTING_UNSUPPORTED",
                "PHYSICAL_EVIDENCE_INCOMPLETE", "PROCESS_MEMBERSHIP_INVALID",
                "JOB_QUERY_EVIDENCE_INVALID", "COMPLETION_EVIDENCE_INCOMPLETE",
                "EXTERNAL_WORK_UNMEASURED", "GRID_IDENTITY_MISMATCH"}),
            "boundedness_pass": "H_SHAPE_LIMIT" not in admitted_errors,
            "affordability_pass": "AFFORDABILITY_LIMIT" not in admitted_errors,
            "worst_cell_metrics": worst,
            "authority_mode": ("PRODUCTION" if require_production_authority
                               else "FIXTURE_CONFORMANCE"),
        }
        if admitted_errors:
            evidence["accounting_complete"] = False
        evidence["evidence_hash"] = sha384(evidence)
        return evidence
    except ValueError:
        raise
    except (KeyError, TypeError, AttributeError) as exc:
        raise ValueError("ENGINEERING_SELECTION_INVALID") from exc


def engineering_selection(evidence_rows: list[dict[str, Any]], *,
                          require_production_authority: bool = True) -> dict[str, Any]:
    if not isinstance(evidence_rows, list) or not evidence_rows:
        raise ValueError("ENGINEERING_SELECTION_INVALID")
    survivors = []
    rejected = []
    for report in evidence_rows:
        if not isinstance(report, dict) or set(report) != ENGINEERING_EVIDENCE_KEYS:
            raise ValueError("ENGINEERING_SELECTION_INVALID")
        rebuilt = derive_engineering_candidate_evidence(
            report["exactness_receipt"], report["measurement_envelopes"],
            expected_run_id=report["run_id"],
            require_production_authority=require_production_authority)
        if rebuilt != report:
            raise ValueError("ENGINEERING_SELECTION_INVALID")
        if all(report[gate] for gate in ("exactness_pass", "accounting_complete",
                                         "boundedness_pass", "affordability_pass")):
            survivors.append(report)
        else:
            rejected.append(report["candidate_id"])
    nondominated = []
    for candidate in survivors:
        vector = candidate["worst_cell_metrics"]
        dominated = any(
            all(other["worst_cell_metrics"][metric] <= vector[metric]
                for metric in ENGINEERING_METRICS)
            and any(other["worst_cell_metrics"][metric] < vector[metric]
                    for metric in ENGINEERING_METRICS)
            for other in survivors if other is not candidate)
        if not dominated:
            nondominated.append(candidate["candidate_id"])
    nondominated.sort(key=lambda value: value.encode("utf-8"))
    return {"schema_id": "EngineeringSelectionV1",
            "hard_gate_survivor_ids": sorted(
                [row["candidate_id"] for row in survivors], key=lambda value: value.encode("utf-8")),
            "hard_gate_rejected_ids": sorted(rejected, key=lambda value: value.encode("utf-8")),
            "objective_order": list(ENGINEERING_METRICS),
            "nondominated_candidate_ids": nondominated,
            "status": ("NO_ADMISSIBLE_CANDIDATE" if not nondominated else
                       "EVIDENCE_UNIQUE" if len(nondominated) == 1 else
                       "OWNER_SELECTION_REQUIRED"),
            "evidence_claim": "NO_OWNER_PREFERENCE_IN_EVIDENCE"}
