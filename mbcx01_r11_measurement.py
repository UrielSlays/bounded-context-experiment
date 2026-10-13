"""r11 cohort provenance, physical-receipt evaluation and durable call ledger."""

from __future__ import annotations

import base64
import copy
import hashlib
import json
import re
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any

from mbcx01_r11_common import (canonical_json, make_durability_receipt, sha256, sha384,
                               valid_durability_receipt)


MOTIFS = ("CORRECTION_RESTORATION", "OBLIGATION_LIFECYCLE", "DEPENDENCY_REVERSAL",
          "CROSS_SCOPE_COLLISION", "DELEGATION_IDEMPOTENT_HANDOFF", "MIXED_DELAYED_CONTINUITY")
H_VALUES = (128, 1024, 10000, 100000)
D_VALUES = (1, 4, 16, 64, 256)
F_VALUES = (1, 4, 16, 64, 256)
SHA256_RE = re.compile(r"^[0-9A-F]{64}$")
SHA384_RE = re.compile(r"^[0-9A-F]{96}$")
SEMANTIC_RE = re.compile(r"^[A-Z0-9][A-Z0-9:._/-]{0,127}$")
ROOT = Path(__file__).resolve().parent


def _load_json(name: str) -> dict[str, Any]:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def _selection_domains() -> tuple[str, str]:
    cohort = _load_json("MBCX-01-MEASUREMENT-CONTRACT-v5.json")["cohort"]
    return cohort["one_cut_hash_domain"], cohort["retention_hash_domain"]


def _generator_spec() -> tuple[dict[str, Any], str]:
    spec = _load_json("MBCX-01-R11-SYNTHETIC-COHORT-GENERATOR.json")
    if (spec.get("schema_id") != "SyntheticCohortGeneratorSpecV1"
            or spec.get("generator_id") != "GENERATOR.R11.SYNTHETIC"):
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
    return min(cut_ids, key=lambda cut: (framed_hash([domain, scenario_id, cut]), cut.encode("utf-8")))


def _source_authority(row: dict[str, Any]) -> dict[str, Any]:
    return {"scenario_id": row["scenario_id"], "motif": row["motif"],
            "cut_ids": copy.deepcopy(row["cut_ids"]),
            "cut_set_hash": sha384(row["cut_ids"]),
            "action_universe_hash": sha384(row["action_ids_by_cut"]),
            "gold_authority_hash": sha384(row["gold_action_id_by_cut"]),
            "canonical_state_hash": sha384(row["canonical_state_by_cut"]),
            "cut_authority_hash": sha384(row["cut_by_id"])}


def synthetic_candidates_r11() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    spec, generator_digest = _generator_spec()
    rows = []
    target_action = "ACT." + sha256([spec["scope_id"], spec["target_obligation_id"]])
    for motif_index, motif in enumerate(MOTIFS):
        for index in range(spec["candidate_count_per_motif"]):
            sid = spec["scenario_id_template"].format(motif_index=motif_index, index=index)
            cut_ids = [spec["cut_id_template"].format(index=index, label=label)
                       for label in spec["cut_labels"]]
            action_ids = {cut: [target_action] for cut in cut_ids}
            gold = {cut: action_ids[cut][0] for cut in cut_ids}
            authority_state = {"eligible": True, "scope_id": spec["scope_id"],
                               "target_obligation_id": spec["target_obligation_id"],
                               "target_lifecycle": spec["target_lifecycle"],
                               "prerequisite_obligation_id": spec["prerequisite_obligation_id"],
                               "prerequisite_lifecycle": spec["prerequisite_lifecycle"]}
            rows.append({"scenario_id": sid, "motif": motif, "cut_ids": cut_ids,
                         "action_ids_by_cut": action_ids, "gold_action_id_by_cut": gold,
                         "canonical_state_by_cut": {cut: copy.deepcopy(authority_state)
                                                    for cut in cut_ids},
                         "cut_by_id": {cut: {"cut_id": cut, **copy.deepcopy(spec["cut"])}
                                       for cut in cut_ids}})
    provenance = {"schema_id": "SourceProvenanceManifestV1", "generator_id": "GENERATOR.R11.SYNTHETIC",
                  "generator_digest": generator_digest,
                  "scenario_authority": [_source_authority(row) for row in rows]}
    provenance["provenance_hash"] = sha384(provenance)
    return rows, provenance


def validate_source_provenance(candidates: list[dict[str, Any]], provenance: dict[str, Any]) -> list[str]:
    errors: set[str] = set()
    try:
        generator_spec, generator_digest = _generator_spec()
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return ["SOURCE_GENERATOR_INVALID"]
    if (not isinstance(provenance, dict) or provenance.get("schema_id") != "SourceProvenanceManifestV1"
            or provenance.get("generator_id") != generator_spec["generator_id"]
            or provenance.get("generator_digest") != generator_digest
            or SEMANTIC_RE.fullmatch(str(provenance.get("generator_id", ""))) is None
            or provenance.get("provenance_hash") != sha384({k: v for k, v in provenance.items()
                                                            if k != "provenance_hash"})):
        errors.add("SOURCE_PROVENANCE_INVALID")
        return sorted(errors)
    expected = provenance.get("scenario_authority", [])
    actual = [_source_authority(row) for row in candidates]
    if actual != expected:
        errors.add("SOURCE_PROVENANCE_MISMATCH")
    ids = [row.get("scenario_id") for row in candidates]
    if len(ids) != len(set(ids)):
        errors.add("DUPLICATE_SCENARIO_ID")
    if any(row.get("motif") not in MOTIFS for row in candidates):
        errors.add("UNKNOWN_MOTIF")
    if any(sum(row.get("motif") == motif for row in candidates) != 160 for motif in MOTIFS):
        errors.add("WRONG_MOTIF_TOTAL")
    return sorted(errors)


def _eligible(row: dict[str, Any], chosen: str) -> bool:
    state = row["canonical_state_by_cut"][chosen]
    actions = row["action_ids_by_cut"][chosen]
    gold = row["gold_action_id_by_cut"][chosen]
    return state.get("eligible") is True and actions.count(gold) == 1


def select_cohort(candidates: list[dict[str, Any]], provenance: dict[str, Any]) -> list[dict[str, Any]]:
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
            row["eligible"] = _eligible(row, chosen)
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
    selected.sort(key=lambda row: hashlib.sha256(row["scenario_id"].encode("utf-8")).digest())
    return selected


JOB_KEYS = {"receipt_source", "job_object_id", "root_process_id", "created_suspended",
            "completion_port_associated_before_resume", "assigned_before_resume", "breakaway_enabled",
            "silent_breakaway_enabled", "active_processes_at_final_query", "completion_port_drained",
            "user_time_ns", "kernel_time_ns", "read_operations", "write_operations", "other_operations",
            "read_transfer_bytes", "write_transfer_bytes", "other_transfer_bytes",
            "peak_committed_bytes", "elapsed_monotonic_ns", "retired_instructions",
            "instruction_backend", "instruction_attribution"}
ROW_KEYS = {"schema_id", "candidate_id", "generator_digest", "H", "D", "F",
            "external_work_policy", "job_receipt", "measurement_receipt_hash"}


def _row_hash(row: dict[str, Any]) -> str:
    return sha384({key: value for key, value in row.items() if key != "measurement_receipt_hash"})


def refresh_receipt_hash(row: dict[str, Any]) -> None:
    row["measurement_receipt_hash"] = _row_hash(row)


def baseline_receipt_rows(candidate_id: str = "CANDIDATE.BASELINE",
                          generator_digest: str = "A" * 96) -> list[dict[str, Any]]:
    rows = []
    for h in H_VALUES:
        for d in D_VALUES:
            for f in F_VALUES:
                job = {"receipt_source": "WINDOWS_JOB_OBJECT_HARNESS_V1",
                       "job_object_id": f"JOB.{h}.{d}.{f}", "root_process_id": 1000 + len(rows),
                       "created_suspended": True, "completion_port_associated_before_resume": True,
                       "assigned_before_resume": True, "breakaway_enabled": False,
                       "silent_breakaway_enabled": False, "active_processes_at_final_query": 0,
                       "completion_port_drained": True, "user_time_ns": 600000,
                       "kernel_time_ns": 400000, "read_operations": 2, "write_operations": 1,
                       "other_operations": 0, "read_transfer_bytes": 4096,
                       "write_transfer_bytes": 1024, "other_transfer_bytes": 0,
                       "peak_committed_bytes": 16777216, "elapsed_monotonic_ns": 2000000,
                       "retired_instructions": 100000, "instruction_backend": "ETW_PMC_RETIRED_INSTRUCTIONS_V1",
                       "instruction_attribution": "JOB_MEMBER_PROCESS_SUM_INCLUDING_TERMINATED"}
                row = {"schema_id": "MeasurementReceiptV1", "candidate_id": candidate_id,
                       "generator_digest": generator_digest, "H": h, "D": d, "F": f,
                       "external_work_policy": "NETWORK_EGRESS_DENIED_NO_EXTERNAL_COMPUTE",
                       "job_receipt": job}
                refresh_receipt_hash(row); rows.append(row)
    return rows


def evaluate_measurement_receipts(rows: list[dict[str, Any]]) -> list[str]:
    errors: set[str] = set()
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        return ["MEASUREMENT_SCHEMA_INVALID", "PHYSICAL_HARNESS_UNAVAILABLE"]
    if len(rows) != 100:
        errors.add("GRID_COVERAGE_INVALID")
    candidate_ids = {row.get("candidate_id") for row in rows}
    generator_ids = {row.get("generator_digest") for row in rows}
    if len(candidate_ids) != 1:
        errors.add("CANDIDATE_ID_MISMATCH")
    if len(generator_ids) != 1:
        errors.add("GENERATOR_ID_MISMATCH")
    coordinates = []
    valid_rows = []
    for row in rows:
        if (not isinstance(row, dict) or set(row) != ROW_KEYS
                or row.get("schema_id") != "MeasurementReceiptV1"
                or row.get("measurement_receipt_hash") != _row_hash(row)
                or SEMANTIC_RE.fullmatch(str(row.get("candidate_id", ""))) is None
                or not isinstance(row.get("H"), int) or isinstance(row.get("H"), bool)
                or not isinstance(row.get("D"), int) or isinstance(row.get("D"), bool)
                or not isinstance(row.get("F"), int) or isinstance(row.get("F"), bool)
                or row.get("H") not in H_VALUES or row.get("D") not in D_VALUES or row.get("F") not in F_VALUES
                or not isinstance(row.get("job_receipt"), dict) or set(row["job_receipt"]) != JOB_KEYS
                or SHA384_RE.fullmatch(str(row.get("generator_digest", ""))) is None):
            errors.add("MEASUREMENT_SCHEMA_INVALID")
            continue
        job = row["job_receipt"]
        integer_fields = ("root_process_id", "active_processes_at_final_query", "user_time_ns", "kernel_time_ns",
                          "read_operations", "write_operations", "other_operations", "read_transfer_bytes",
                          "write_transfer_bytes", "other_transfer_bytes", "peak_committed_bytes",
                          "elapsed_monotonic_ns", "retired_instructions")
        if any(not isinstance(job[name], int) or isinstance(job[name], bool) or job[name] < 0
               for name in integer_fields):
            errors.add("MEASUREMENT_SCHEMA_INVALID"); continue
        coordinates.append((row["H"], row["D"], row["F"]))
        if (job["receipt_source"] != "WINDOWS_JOB_OBJECT_HARNESS_V1"
                or SEMANTIC_RE.fullmatch(str(job["job_object_id"])) is None
                or job["root_process_id"] <= 0
                or job["created_suspended"] is not True
                or job["completion_port_associated_before_resume"] is not True
                or job["assigned_before_resume"] is not True or job["breakaway_enabled"] is not False
                or job["silent_breakaway_enabled"] is not False
                or job["active_processes_at_final_query"] != 0 or job["completion_port_drained"] is not True):
            errors.add("DESCENDANT_ACCOUNTING_MISSING")
        if (job["instruction_backend"] != "ETW_PMC_RETIRED_INSTRUCTIONS_V1"
                or job["instruction_attribution"] != "JOB_MEMBER_PROCESS_SUM_INCLUDING_TERMINATED"
                or job["retired_instructions"] <= 0):
            errors.add("INSTRUCTION_ACCOUNTING_MISSING")
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
                or job["read_transfer_bytes"] + job["write_transfer_bytes"] + job["other_transfer_bytes"] > 67_108_864):
            errors.add("AFFORDABILITY_LIMIT")
    for d in D_VALUES:
        for f in F_VALUES:
            group = [row["job_receipt"] for row in valid_rows if row["D"] == d and row["F"] == f]
            if len(group) != 4:
                continue
            ranges = (("retired_instructions", 500_000), ("elapsed_monotonic_ns", 75_000_000),
                      ("peak_committed_bytes", 67_108_864), ("read_transfer_bytes", 67_108_864))
            if any(max(row[name] for row in group) - min(row[name] for row in group) > limit
                   for name, limit in ranges):
                errors.add("H_SHAPE_LIMIT")
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
                or node not in {"A0", "B", "A1"} or SHA384_RE.fullmatch(task_packet_hash or "") is None
                or SHA256_RE.fullmatch(served_request_hash or "") is None
                or SHA384_RE.fullmatch(request_parameters_hash or "") is None
                or SEMANTIC_RE.fullmatch(idempotency_token or "") is None
                or SHA384_RE.fullmatch(route_contract_hash or "") is None):
            raise ValueError("invalid nonempty call identity")
        value = cls("CallLedgerV1", scenario_id, condition, node, task_packet_hash, served_request_hash,
                    request_parameters_hash, idempotency_token, route_contract_hash, "PREPARED")
        return value._rehash()

    def _payload(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if key != "ledger_hash"}

    def _rehash(self) -> "CallLedger":
        return replace(self, ledger_hash=sha384(self._payload()))

    def transition(self, event: str, *, response_bytes: bytes | None = None,
                   response_ref: str | None = None, provider_request_id: str | None = None,
                   durability_receipt: dict[str, Any] | None = None,
                   route_attestation: dict[str, Any] | Any = None,
                   preaccept_failure_receipt: dict[str, Any] | None = None) -> "CallLedger":
        if self.ledger_hash != sha384(self._payload()):
            raise ValueError("ledger digest mismatch")
        matrix = {
            "PREPARED": {"DISPATCH_CONFIRMED": "DISPATCHED", "PROVEN_NOT_ACCEPTED": "PROVEN_PRE_ACCEPT_FAILURE"},
            "DISPATCHED": {"PROVEN_NOT_ACCEPTED": "PROVEN_PRE_ACCEPT_FAILURE",
                           "CONNECTION_LOST_AFTER_DISPATCH": "ACCEPTANCE_AMBIGUOUS",
                           "RESPONSE_BYTES_FSYNCED": "RESPONSE_DURABLY_RECORDED"},
            "RESPONSE_DURABLY_RECORDED": {},
            "PROVEN_PRE_ACCEPT_FAILURE": {},
            "ACCEPTANCE_AMBIGUOUS": {"CONNECTION_LOST_AFTER_DISPATCH": "ACCEPTANCE_AMBIGUOUS",
                                     "RESPONSE_BYTES_FSYNCED": "RESPONSE_DURABLY_RECORDED",
                                     "RETRY_REQUESTED": "PREPARED"},
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
        if event == "RETRY_REQUESTED" and self.state == "ACCEPTANCE_AMBIGUOUS":
            if not _valid_route_attestation(self, route_attestation):
                raise ValueError("structured exact route attestation required")
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
        if (value.schema_id != "CallLedgerV1"
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
    return {key: getattr(ledger, key) for key in ("scenario_id", "condition", "node", "task_packet_hash",
                                                   "served_request_hash", "request_parameters_hash",
                                                   "idempotency_token", "route_contract_hash")}


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
            and row["receipt_hash"] == sha384({k: v for k, v in row.items()
                                               if k != "receipt_hash"}))


def route_attestation_fixture(ledger: CallLedger) -> dict[str, Any]:
    row = {"schema_id": "RouteAttestationV1", "route_contract_hash": ledger.route_contract_hash,
           "request_parameters_hash": ledger.request_parameters_hash,
           "idempotency_token": ledger.idempotency_token,
           "semantic_guarantee": "SAME_TOKEN_SAME_PARAMETERS_RETURNS_FIRST_RESULT"}
    row["attestation_hash"] = sha384(row)
    return row


def _valid_route_attestation(ledger: CallLedger, row: Any) -> bool:
    required = {"schema_id", "route_contract_hash", "request_parameters_hash", "idempotency_token",
                "semantic_guarantee", "attestation_hash"}
    return (isinstance(row, dict) and set(row) == required and row["schema_id"] == "RouteAttestationV1"
            and row["route_contract_hash"] == ledger.route_contract_hash
            and row["request_parameters_hash"] == ledger.request_parameters_hash
            and row["idempotency_token"] == ledger.idempotency_token
            and row["semantic_guarantee"] == "SAME_TOKEN_SAME_PARAMETERS_RETURNS_FIRST_RESULT"
            and row["attestation_hash"] == sha384({k: v for k, v in row.items() if k != "attestation_hash"}))
