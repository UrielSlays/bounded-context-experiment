"""r12 cohort provenance, signed physical-receipt admission, and call ledger.

The deterministic Ed25519 fixture key is test-only. Its signatures exercise the
trust boundary but cannot establish that the unbuilt physical harness ran.
"""

from __future__ import annotations

import base64
import copy
import hashlib
import json
import re
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
TEST_KEY_ID = "MBCX01.R12.NO-PAID.ED25519.TEST.1"
VERIFIER = ROOT / "verify-r12-receipt-signature.mjs"

INSTRUCTION_MODE = "ETW_PMC_EVENT_ATTACHED_V1"
INSTRUCTION_SOURCE = "INSTRUCTIONRETIRED"
INSTRUCTION_EVENT_LIST = "CSWITCH"
INSTRUCTION_ATTRIBUTION = "SUM_INSTRUCTIONRETIRED_CSWITCH_DELTAS_BY_OLD_THREAD_JOINED_TO_SIGNED_JOB_PID_TID_LIFETIMES_INCLUDING_TERMINATED"
CALL_IDENTITY_FIELDS = ("scenario_id", "condition", "node", "task_packet_hash",
                        "served_request_hash", "request_parameters_hash", "idempotency_token",
                        "route_contract_hash")


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


def _load_trust_roots() -> dict[str, dict[str, Any]]:
    document = _load_json("MBCX-01-R12-MEASUREMENT-TRUST-ROOTS.json")
    if (not isinstance(document, dict)
            or set(document) != {"schema_id", "production_ready", "roots"}
            or document.get("schema_id") != "MeasurementTrustRootManifestV1"
            or document.get("production_ready") is not False
            or not isinstance(document.get("roots"), list) or not document["roots"]):
        raise ValueError("measurement trust-root document invalid")
    roots: dict[str, dict[str, Any]] = {}
    for row in document["roots"]:
        if (not isinstance(row, dict)
                or set(row) != {"key_id", "algorithm", "fixture_only", "public_key_pem"}
                or SEMANTIC_RE.fullmatch(str(row.get("key_id", ""))) is None
                or row.get("algorithm") != SIGNATURE_ALGORITHM
                or row.get("fixture_only") is not True
                or not isinstance(row.get("public_key_pem"), str)
                or not row["public_key_pem"].startswith("-----BEGIN PUBLIC KEY-----\n")
                or not row["public_key_pem"].endswith("-----END PUBLIC KEY-----\n")
                or row["key_id"] in roots):
            raise ValueError("measurement trust-root row invalid")
        roots[row["key_id"]] = copy.deepcopy(row)
    if TEST_KEY_ID not in roots:
        raise ValueError("no-paid fixture trust root missing")
    return roots


def _selection_domains() -> tuple[str, str]:
    cohort = _load_json("MBCX-01-MEASUREMENT-CONTRACT-v6.json")["cohort"]
    return cohort["one_cut_hash_domain"], cohort["retention_hash_domain"]


def _generator_spec() -> tuple[dict[str, Any], str]:
    spec = _load_json("MBCX-01-R12-SYNTHETIC-COHORT-GENERATOR.json")
    if (spec.get("schema_id") != "SyntheticCohortGeneratorSpecV1"
            or spec.get("generator_id") != "GENERATOR.R12.SYNTHETIC"):
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
            "cut_authority_hash": sha384(row["cut_by_id"])}


def synthetic_candidates_r12() -> tuple[list[dict[str, Any]], dict[str, Any]]:
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
            rows.append({"scenario_id": sid, "motif": motif, "cut_ids": cuts,
                         "action_ids_by_cut": actions,
                         "gold_action_id_by_cut": {cut: actions[cut][0] for cut in cuts},
                         "canonical_state_by_cut": {cut: copy.deepcopy(state) for cut in cuts},
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


JOB_KEYS = {
    "receipt_source", "job_object_id", "root_process_id", "created_suspended",
    "completion_port_associated_before_resume", "assigned_before_resume", "breakaway_enabled",
    "silent_breakaway_enabled", "active_processes_at_final_query", "completion_port_drained",
    "user_time_ns", "kernel_time_ns", "read_operations", "write_operations", "other_operations",
    "read_transfer_bytes", "write_transfer_bytes", "other_transfer_bytes", "peak_committed_bytes",
    "elapsed_monotonic_ns", "retired_instructions", "instruction_backend",
    "instruction_profile_source", "instruction_event_list", "instruction_attribution",
    "etw_capability_query_succeeded", "etw_pmc_source_available",
    "etw_max_pmc_counters", "etw_counter_owner_conflict_count", "etw_pmc_strict_mode",
    "etw_pmc_multiplexing_detected", "etw_events_lost",
    "etw_log_buffers_lost", "etw_realtime_buffers_lost", "etw_attribution_complete",
}
RECEIPT_KEYS = {"schema_id", "candidate_id", "generator_digest", "H", "D", "F",
                "external_work_policy", "job_receipt"}
ENVELOPE_KEYS = {"schema_id", "domain", "version", "algorithm", "signing_key_id",
                 "run_id", "cell_id", "receipt", "receipt_preimage_b64", "receipt_digest",
                 "signature_b64", "fixture_kind"}


def _cell_id(receipt: dict[str, Any]) -> str:
    return f"CELL.H{receipt['H']}.D{receipt['D']}.F{receipt['F']}"


def _receipt_preimage(envelope: dict[str, Any]) -> bytes:
    return canonical_json({
        "domain": envelope["domain"], "version": envelope["version"],
        "algorithm": envelope["algorithm"], "signing_key_id": envelope["signing_key_id"],
        "run_id": envelope["run_id"], "cell_id": envelope["cell_id"],
        "fixture_kind": envelope["fixture_kind"], "receipt": envelope["receipt"],
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
    preimage = _receipt_preimage(envelope)
    envelope["receipt_preimage_b64"] = base64.b64encode(preimage).decode("ascii")
    envelope["receipt_digest"] = hashlib.sha384(preimage).hexdigest().upper()


def baseline_receipt_rows(candidate_id: str = "CANDIDATE.BASELINE",
                          generator_digest: str = "A" * 96, *,
                          run_id: str = "RUN.R12.NO-PAID.TEST") -> list[dict[str, Any]]:
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
                receipt = {"schema_id": "MeasurementReceiptV2", "candidate_id": candidate_id,
                           "generator_digest": generator_digest, "H": h, "D": d, "F": f,
                           "external_work_policy": "NETWORK_EGRESS_DENIED_NO_EXTERNAL_COMPUTE",
                           "job_receipt": job}
                envelope = {"schema_id": "SignedMeasurementReceiptV1",
                            "domain": ENVELOPE_DOMAIN, "version": 1,
                            "algorithm": SIGNATURE_ALGORITHM, "signing_key_id": TEST_KEY_ID,
                            "run_id": run_id, "cell_id": _cell_id(receipt), "receipt": receipt,
                            "receipt_preimage_b64": "", "receipt_digest": "",
                            "signature_b64": "", "fixture_kind": "NO_PAID_TEST_FIXTURE"}
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
    if (envelope.get("schema_id") != "SignedMeasurementReceiptV1"
            or envelope.get("domain") != ENVELOPE_DOMAIN or envelope.get("version") != 1
            or envelope.get("algorithm") != SIGNATURE_ALGORITHM
            or SEMANTIC_RE.fullmatch(str(envelope.get("run_id", ""))) is None
            or envelope.get("run_id") != expected_run_id
            or (envelope.get("signing_key_id") == TEST_KEY_ID
                and envelope.get("fixture_kind") != "NO_PAID_TEST_FIXTURE")
            or (envelope.get("fixture_kind") == "PHYSICAL_HARNESS_RECEIPT"
                and envelope.get("signing_key_id") == TEST_KEY_ID)
            or not isinstance(receipt, dict)):
        errors.add("MEASUREMENT_ENVELOPE_INVALID")
    if isinstance(receipt, dict):
        try:
            expected_cell = _cell_id(receipt)
        except (KeyError, TypeError):
            expected_cell = None
        if envelope.get("cell_id") != expected_cell or envelope.get("run_id") != expected_run_id:
            errors.add("MEASUREMENT_REPLAY_IDENTITY_MISMATCH")
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
    generator_ids = {row.get("generator_digest") for row in receipts}
    if len(candidate_ids) != 1:
        errors.add("CANDIDATE_ID_MISMATCH")
    if len(generator_ids) != 1:
        errors.add("GENERATOR_ID_MISMATCH")
    valid_rows = []
    coordinates = []
    for row in receipts:
        job = row.get("job_receipt")
        if (set(row) != RECEIPT_KEYS or row.get("schema_id") != "MeasurementReceiptV2"
                or SEMANTIC_RE.fullmatch(str(row.get("candidate_id", ""))) is None
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
                idempotency_token: str, route_contract_hash: str) -> "CallLedger":
        if (SEMANTIC_RE.fullmatch(scenario_id or "") is None or condition not in {"BC", "OM"}
                or node not in {"A0", "B", "A1"}
                or SHA384_RE.fullmatch(task_packet_hash or "") is None
                or SHA256_RE.fullmatch(served_request_hash or "") is None
                or SHA384_RE.fullmatch(request_parameters_hash or "") is None
                or SEMANTIC_RE.fullmatch(idempotency_token or "") is None
                or SHA384_RE.fullmatch(route_contract_hash or "") is None):
            raise ValueError("invalid nonempty call identity")
        return cls("CallLedgerV2", scenario_id, condition, node, task_packet_hash,
                   served_request_hash, request_parameters_hash, idempotency_token,
                   route_contract_hash, "PREPARED")._rehash()

    def _payload(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if key != "ledger_hash"}

    def _rehash(self) -> "CallLedger":
        return replace(self, ledger_hash=sha384(self._payload()))

    def terminal_missing_reason(self) -> str | None:
        return "ACCEPTANCE_AMBIGUOUS" if self.state == "ACCEPTANCE_AMBIGUOUS" else None

    def transition(self, event: str, *, response_bytes: bytes | None = None,
                   response_ref: str | None = None, provider_request_id: str | None = None,
                   durability_receipt: dict[str, Any] | None = None,
                   route_attestation: Any = None,
                   preaccept_failure_receipt: dict[str, Any] | None = None) -> "CallLedger":
        del route_attestation  # Runtime assertions have no authority in r12.
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
        if (value.schema_id != "CallLedgerV2"
                or SEMANTIC_RE.fullmatch(value.scenario_id or "") is None
                or value.condition not in {"BC", "OM"} or value.node not in {"A0", "B", "A1"}
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
        "scenario_id", "condition", "node", "task_packet_hash", "served_request_hash",
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
