"""Executable r10 reference functions. No provider/model calls occur here."""

from __future__ import annotations

import copy
import hashlib
import itertools
import json
import math
import re
from dataclasses import dataclass, replace
from datetime import datetime
from pathlib import Path
from typing import Any

import mbcx01_r9_reference as r9


ROOT = Path(__file__).resolve().parent
T0 = r9.T0
T1 = r9.T1
EVENT_TYPES = tuple(json.loads((ROOT / "MBCX-01-STATE-ACTION-CONTRACT-v5.json").read_text(
    encoding="utf-8"))["event_types"])

canonical_json = r9.canonical_json
action_id = r9.action_id
cut_hash = r9.cut_hash
initial_state = r9.initial_state
current_cut = r9.current_cut
paired_intervals = r9.paired_intervals
scientific_decision = r9.scientific_decision


def load_contract(name: str) -> dict[str, Any]:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def sha384(value: Any) -> str:
    return hashlib.sha384(canonical_json(value)).hexdigest().upper()


def fact_key(subject_id: str, predicate_id: str) -> str:
    return hashlib.sha256(canonical_json([subject_id, predicate_id])).hexdigest().upper()


def _real_utc(value: Any) -> bool:
    if not isinstance(value, str) or not re.fullmatch(
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}Z", value):
        return False
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        return False
    return parsed.strftime("%Y-%m-%dT%H:%M:%S.%fZ") == value


def _resolve_ref(root: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValueError("only local refs are allowed")
    node: Any = root
    for part in ref[2:].split("/"):
        node = node[part.replace("~1", "/").replace("~0", "~")]
    return node


def _schema_errors(instance: Any, schema: dict[str, Any], root: dict[str, Any],
                   path: str = "$") -> list[str]:
    if "$ref" in schema:
        return _schema_errors(instance, _resolve_ref(root, schema["$ref"]), root, path)
    errors: list[str] = []
    if "allOf" in schema:
        for part in schema["allOf"]:
            errors.extend(_schema_errors(instance, part, root, path))
    if "oneOf" in schema:
        successes = sum(not _schema_errors(instance, part, root, path) for part in schema["oneOf"])
        if successes != 1:
            errors.append(f"{path}:oneOf")
        return errors
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}:const")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}:enum")
    kind = schema.get("type")
    type_ok = {
        "object": isinstance(instance, dict),
        "array": isinstance(instance, list),
        "string": isinstance(instance, str),
        "integer": isinstance(instance, int) and not isinstance(instance, bool),
        "number": isinstance(instance, (int, float)) and not isinstance(instance, bool),
        "boolean": isinstance(instance, bool),
        "null": instance is None,
    }.get(kind, True)
    if kind is not None and not type_ok:
        return errors + [f"{path}:type:{kind}"]
    if isinstance(instance, dict):
        required = schema.get("required", [])
        errors.extend(f"{path}:required:{name}" for name in required if name not in instance)
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            errors.extend(f"{path}:additional:{name}" for name in instance if name not in properties)
        for name, subschema in properties.items():
            if name in instance:
                errors.extend(_schema_errors(instance[name], subschema, root, f"{path}.{name}"))
    elif isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            errors.append(f"{path}:minItems")
        if len(instance) > schema.get("maxItems", math.inf):
            errors.append(f"{path}:maxItems")
        if schema.get("uniqueItems") and len({canonical_json(item) for item in instance}) != len(instance):
            errors.append(f"{path}:uniqueItems")
        if "items" in schema:
            for index, item in enumerate(instance):
                errors.extend(_schema_errors(item, schema["items"], root, f"{path}[{index}]"))
    elif isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0) or len(instance) > schema.get("maxLength", math.inf):
            errors.append(f"{path}:length")
        if "pattern" in schema and re.fullmatch(schema["pattern"], instance) is None:
            errors.append(f"{path}:pattern")
        if schema.get("format") == "microsecond-utc" and not _real_utc(instance):
            errors.append(f"{path}:format")
    elif isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if instance < schema.get("minimum", -math.inf) or instance > schema.get("maximum", math.inf):
            errors.append(f"{path}:range")
    return errors


def validate_event_schema(event: Any) -> list[str]:
    contract = load_contract("MBCX-01-STATE-ACTION-CONTRACT-v5.json")
    errors = _schema_errors(event, contract["event_envelope"], contract)
    if not isinstance(event, dict):
        return errors or ["$:type:object"]
    rule = contract["event_types"].get(event.get("event_type"))
    if rule is None:
        return errors + ["$.event_type:unknown"]
    if event.get("semantic_operation") != rule["semantic_operation"]:
        errors.append("$.semantic_operation:const")
    errors.extend(_schema_errors(event.get("payload"), rule["payload_schema"], contract, "$.payload"))
    return sorted(set(errors))


def make_event(event_type: str, payload: dict[str, Any], **kwargs) -> dict[str, Any]:
    event = r9.make_event(event_type, payload, **kwargs)
    return event


def _visible_effective(version: dict[str, Any], cut: dict[str, Any]) -> bool:
    return (not version["retracted"]
            and version["journal_seq"] <= cut["journal_seq"]
            and version["observed_at"] <= cut["knowledge_time"]
            and version["valid_from"] <= cut["valid_time"]
            and (version["valid_to"] is None or cut["valid_time"] < version["valid_to"]))


def _reference_semantic_guard(state: dict[str, Any], event: dict[str, Any]) -> str | None:
    payload = event["payload"]
    scope = state["scopes"].get(event["scope_id"], {"facts": {}, "obligations": {}})
    if event["event_type"] == "open_obligation":
        if payload["completion_action_id"] != action_id(event["scope_id"], payload["obligation_id"]):
            return "ACTION_ID_HASH_GUARD"
    if event["event_type"] in {"correct_fact", "retract_fact"}:
        versions = scope.get("facts", {}).get(fact_key(payload["subject_id"], payload["predicate_id"]), [])
        target_field = "parent_event_id" if event["event_type"] == "correct_fact" else "target_event_id"
        target = next((row for row in versions if row["event_id"] == payload[target_field]), None)
        if target is None or not _visible_effective(target, event["originating_cut"]):
            return "FACT_PARENT_NOT_HEAD" if event["event_type"] == "correct_fact" else "FACT_TARGET_UNAVAILABLE"
    if event["event_type"] == "open_handoff":
        obligations = scope.get("obligations", {})
        if payload["originating_cut_hash"] != cut_hash(event["originating_cut"]):
            return "HANDOFF_OR_TARGET_ILLEGAL"
        if payload["action_catalog_hash"] != sha384(payload["action_catalog"]):
            return "HANDOFF_OR_TARGET_ILLEGAL"
        if payload["canonical_snapshot_hash"] != sha384(obligations):
            return "HANDOFF_OR_TARGET_ILLEGAL"
        if any(row["action_id"] != action_id(event["scope_id"], row["obligation_id"])
               for row in payload["action_catalog"]):
            return "ACTION_ID_HASH_GUARD"
    if event["event_type"] == "propose_handoff_result":
        handoff = scope.get("handoffs", {}).get(payload["handoff_id"])
        durable_hashes = {row["response_hash"] for row in state.get("responses", {}).values()}
        if handoff and durable_hashes and payload["worker_handoff_hash"] not in durable_hashes:
            return "PROPOSAL_INVALID"
    return None


def _legacy_event(event: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(event)
    if value["event_type"] == "open_handoff":
        for key in ("action_catalog_hash", "canonical_snapshot_hash"):
            value["payload"].pop(key)
    return value


def reference_apply(state: dict[str, Any], event: dict[str, Any],
                    mutant: str | None = None) -> tuple[dict[str, Any], str]:
    if validate_event_schema(event):
        return copy.deepcopy(state), "SCHEMA_INVALID"
    guard = _reference_semantic_guard(state, event)
    if guard:
        return copy.deepcopy(state), guard
    result_state, result = r9.reference_apply(copy.deepcopy(state), _legacy_event(event), mutant=mutant)
    if result == "APPLIED" and event["event_type"] == "open_handoff":
        handoff = result_state["scopes"][event["scope_id"]]["handoffs"][event["payload"]["handoff_id"]]
        handoff["action_catalog_hash"] = event["payload"]["action_catalog_hash"]
        handoff["canonical_snapshot_hash"] = event["payload"]["canonical_snapshot_hash"]
    return result_state, result


def fixture_payload(event_type: str, state: dict[str, Any]) -> dict[str, Any]:
    payload = r9.fixture_payload(event_type, state)
    if event_type == "open_handoff":
        payload["action_catalog_hash"] = sha384(payload["action_catalog"])
        payload["canonical_snapshot_hash"] = sha384(state["scopes"]["SCOPE.SHARED"]["obligations"])
    return payload


def legal_fixture(event_type: str) -> tuple[dict[str, Any], dict[str, Any]]:
    state, payload = r9.legal_fixture(event_type)
    if event_type == "open_handoff":
        payload["action_catalog_hash"] = sha384(payload["action_catalog"])
        payload["canonical_snapshot_hash"] = sha384(state["scopes"]["SCOPE.SHARED"]["obligations"])
    event = make_event(event_type, payload, state=state)
    return state, event


def run_r10_mutation_suite() -> dict[str, bool]:
    results = dict(r9.run_mutation_suite())
    state = initial_state()
    bad = make_event("open_obligation", {
        "obligation_id": "OBL.BAD", "subject_id": "SUB.BAD", "owner_role": "WORKER",
        "due_at": T1, "critical": True,
        "completion_action_id": action_id("SCOPE.SHARED", "OBL.NOT.BAD"),
        "prerequisite_obligation_ids": []}, state=state)
    results["ACTION_ID_HASH_GUARD"] = reference_apply(state, bad)[1] == "ACTION_ID_HASH_GUARD"
    for name, valid_from, valid_to, observed_at in (
        ("EXPIRED_FACT_VISIBLE", T0, "2026-08-12T12:00:00.000000Z", T0),
        ("FUTURE_EFFECTIVE_VISIBLE", "2026-08-14T00:00:00.000000Z", None, T0),
        ("FUTURE_KNOWLEDGE_VISIBLE", T0, None, "2026-08-14T00:00:00.000000Z"),
    ):
        s = initial_state()
        s["scopes"]["SCOPE.SHARED"]["facts"][fact_key("SUB.X", "PRED.X")] = [{
            "event_id": "EV.FACT.X", "parent_event_id": None, "value_code": "VALUE.X",
            "observed_at": observed_at, "valid_from": valid_from, "valid_to": valid_to,
            "journal_seq": 1, "retracted": False}]
        s["next_seq"] = 2
        cut = {"journal_seq": 1, "knowledge_time": T1, "valid_time": T1}
        event = make_event("retract_fact", {"subject_id": "SUB.X", "predicate_id": "PRED.X",
            "target_event_id": "EV.FACT.X"}, state=s, originating_cut=cut)
        results[name] = reference_apply(s, event)[1] == "FACT_TARGET_UNAVAILABLE"
    s = initial_state()
    payload = fixture_payload("open_handoff", s)
    payload["action_catalog_hash"] = "0" * 96
    event = make_event("open_handoff", payload, state=s)
    results["FORGED_HANDOFF_HASH"] = reference_apply(s, event)[1] == "HANDOFF_OR_TARGET_ILLEGAL"
    return results


# ---- Packet construction and exact scoring ---------------------------------

def _hash_without(record: dict[str, Any], field: str) -> str:
    return sha384({key: value for key, value in record.items() if key != field})


def packet_hash(packet: dict[str, Any]) -> str:
    return _hash_without(packet, "packet_hash")


def packet_fixture_manifest() -> tuple[dict[str, Any], dict[str, dict[str, Any]], list[str]]:
    world, cut, actions, gold_read_set = r9.packet_fixture_world()
    world_rows = [copy.deepcopy(world[key]) for key in sorted(world, key=lambda x: x.encode("utf-8"))]
    manifest: dict[str, Any] = {
        "schema_id": "ExperimentPacketManifestV1",
        "scenario_id": "SCENARIO.SHARED",
        "scope_id": "SCOPE.SHARED",
        "cut": cut,
        "observation": {"scope_id": "SCOPE.SHARED", "observed_at": T1, "code": "TARGET_VISIBLE"},
        "canonical_world": world_rows,
        "canonical_world_hash": sha384(world_rows),
        "action_catalog": copy.deepcopy(actions),
        "action_catalog_hash": sha384(actions),
        "gold_read_set": copy.deepcopy(gold_read_set),
        "gold_action_id": action_id("SCOPE.SHARED", "OBL.SHARED"),
        "expected_a1_action_ids": [],
    }
    manifest["manifest_hash"] = _hash_without(manifest, "manifest_hash")
    return manifest, world, ["OBL.SHARED", "OBS.SHARED"]


def _manifest_world(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["object_id"]: row for row in manifest["canonical_world"]}


def _object_closure(manifest: dict[str, Any], selected: list[str]) -> list[str]:
    world = _manifest_world(manifest)
    result = set(selected)
    result.update(row["obligation_id"] for row in manifest["action_catalog"]
                  if row["action_kind"] == "ACT_ON_OBLIGATION")
    changed = True
    while changed:
        changed = False
        for object_id in list(result):
            row = world.get(object_id)
            if row and row["object_kind"] == "OBLIGATION":
                for prereq in row["fields"].get("prerequisite_obligation_ids", []):
                    if prereq not in result:
                        result.add(prereq)
                        changed = True
    if any(name not in world for name in result):
        raise ValueError("selected object absent from canonical manifest")
    return sorted(result, key=lambda value: value.encode("utf-8"))


def _build_packet(manifest: dict[str, Any], selected: list[str]) -> dict[str, Any]:
    world = _manifest_world(manifest)
    packet: dict[str, Any] = {
        "schema_id": "DecisionPacketV4",
        "scenario_id": manifest["scenario_id"],
        "scope_id": manifest["scope_id"],
        "cut": copy.deepcopy(manifest["cut"]),
        "objects": [copy.deepcopy(world[name]) for name in _object_closure(manifest, selected)],
        "action_catalog": copy.deepcopy(manifest["action_catalog"]),
        "observation": copy.deepcopy(manifest["observation"]),
        "manifest_hash": manifest["manifest_hash"],
    }
    packet["packet_hash"] = packet_hash(packet)
    return packet


def build_bc_packet(manifest: dict[str, Any], candidate_selected_object_ids: list[str]) -> dict[str, Any]:
    return _build_packet(manifest, candidate_selected_object_ids)


def build_om_packet(manifest: dict[str, Any], gold_read_set: list[str]) -> dict[str, Any]:
    if gold_read_set != manifest["gold_read_set"]:
        raise ValueError("gold read-set is not the expected manifest value")
    return _build_packet(manifest, gold_read_set)


def validate_packet_semantics(packet: dict[str, Any], manifest: dict[str, Any]) -> list[str]:
    errors: set[str] = set()
    if packet.get("scenario_id") != manifest.get("scenario_id"):
        errors.add("MANIFEST_SCENARIO_MISMATCH")
    for field, code in (("scope_id", "MANIFEST_SCOPE_MISMATCH"), ("cut", "MANIFEST_CUT_MISMATCH"),
                        ("observation", "MANIFEST_OBSERVATION_MISMATCH"),
                        ("action_catalog", "MANIFEST_ACTION_CATALOG_MISMATCH"),
                        ("manifest_hash", "MANIFEST_HASH_MISMATCH")):
        if packet.get(field) != manifest.get(field):
            errors.add(code)
    canonical = _manifest_world(manifest)
    ids: list[Any] = []
    for row in packet.get("objects", []):
        ids.append(row.get("object_id") if isinstance(row, dict) else None)
        if not isinstance(row, dict) or canonical.get(row.get("object_id")) != row:
            errors.add("CANONICAL_OBJECT_MISMATCH")
    if len(ids) != len(set(ids)):
        errors.add("DUPLICATE_OBJECT_ID")
    if manifest.get("canonical_world_hash") != sha384(manifest.get("canonical_world")):
        errors.add("CANONICAL_WORLD_HASH_MISMATCH")
    if manifest.get("action_catalog_hash") != sha384(manifest.get("action_catalog")):
        errors.add("ACTION_CATALOG_HASH_MISMATCH")
    if manifest.get("manifest_hash") != _hash_without(manifest, "manifest_hash"):
        errors.add("MANIFEST_HASH_MISMATCH")
    if packet.get("packet_hash") != packet_hash(packet):
        errors.add("PACKET_HASH_MISMATCH")
    try:
        if len(canonical_json(packet)) > 65536:
            errors.add("PACKET_ENVELOPE_EXCEEDED")
    except Exception:
        errors.add("SCHEMA_INVALID")
    return sorted(errors)


def render_served_input(packet: dict[str, Any]) -> bytes:
    encoded = canonical_json(packet)
    if len(encoded) > 65536:
        raise ValueError("PACKET_ENVELOPE_EXCEEDED")
    return encoded + b" " * (65536 - len(encoded))


def served_input_hash(served: bytes) -> str:
    if len(served) != 65536:
        raise ValueError("served input must be exactly 65536 bytes")
    return hashlib.sha256(served).hexdigest().upper()


def scoring_fixture(manifest: dict[str, Any]):
    packet = build_om_packet(manifest, manifest["gold_read_set"])
    a0 = {"schema_id": "A0ResultV2", "input_packet_hash": packet["packet_hash"],
          "manifest_hash": manifest["manifest_hash"],
          "selected_action_ids": [manifest["gold_action_id"]]}
    worker = {"schema_id": "WorkerHandoffV4", "scenario_id": manifest["scenario_id"],
              "scope_id": manifest["scope_id"], "input_packet_hash": packet["packet_hash"],
              "manifest_hash": manifest["manifest_hash"], "request_hash": "A" * 96,
              "status_code": "PROPOSE", "proposed_action_ids": [manifest["gold_action_id"]],
              "produced_at": T1}
    worker["response_hash"] = _hash_without(worker, "response_hash")
    receipt = {"schema_id": "WriterReceiptV1", "manifest_hash": manifest["manifest_hash"],
               "worker_response_hash": worker["response_hash"], "status_code": "COMMITTED",
               "committed_action_ids": [manifest["gold_action_id"]],
               "child_event_ids": ["EV.CHILD.COMMIT"]}
    receipt["receipt_hash"] = _hash_without(receipt, "receipt_hash")
    a1 = {"schema_id": "A1ResultV2", "input_packet_hash": packet["packet_hash"],
          "manifest_hash": manifest["manifest_hash"], "writer_receipt_hash": receipt["receipt_hash"],
          "selected_action_ids": copy.deepcopy(manifest["expected_a1_action_ids"])}
    return a0, worker, receipt, a1


def score_exact(manifest: dict[str, Any], a0: dict[str, Any], worker: dict[str, Any],
                receipt: dict[str, Any], a1: dict[str, Any]) -> int:
    manifest_hash = manifest.get("manifest_hash")
    if manifest_hash != _hash_without(manifest, "manifest_hash"):
        return 0
    if any(row.get("manifest_hash") != manifest_hash for row in (a0, worker, receipt, a1)):
        return 0
    if worker.get("scenario_id") != manifest.get("scenario_id") or worker.get("scope_id") != manifest.get("scope_id"):
        return 0
    if worker.get("response_hash") != _hash_without(worker, "response_hash"):
        return 0
    if receipt.get("worker_response_hash") != worker.get("response_hash"):
        return 0
    if receipt.get("receipt_hash") != _hash_without(receipt, "receipt_hash"):
        return 0
    if a1.get("writer_receipt_hash") != receipt.get("receipt_hash"):
        return 0
    packet_hashes = {a0.get("input_packet_hash"), worker.get("input_packet_hash"), a1.get("input_packet_hash")}
    if len(packet_hashes) != 1:
        return 0
    gold = [manifest["gold_action_id"]]
    a0_ok = a0.get("selected_action_ids") == gold
    b_ok = (worker.get("status_code") == "PROPOSE"
            and worker.get("proposed_action_ids") == gold
            and receipt.get("status_code") == "COMMITTED"
            and receipt.get("committed_action_ids") == gold
            and len(receipt.get("child_event_ids", [])) == 1)
    a1_ok = a1.get("selected_action_ids") == manifest.get("expected_a1_action_ids")
    return int(a0_ok and b_ok and a1_ok)


# ---- Cohort ---------------------------------------------------------------

def synthetic_candidates_r10() -> list[dict[str, Any]]:
    return r9.synthetic_candidates()


def select_cohort_r10(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    freeze = load_contract("MBCX-01-MEASUREMENT-CONTRACT-v4.json")["source_and_cohort_freeze"]
    motifs = freeze["motifs"]
    ids = [row.get("scenario_id") for row in candidates]
    if len(ids) != len(set(ids)):
        raise ValueError("scenario IDs must be globally unique before selection")
    if any(row.get("motif") not in motifs for row in candidates):
        raise ValueError("unknown motif")
    generated = freeze["generated_unique_scenarios_per_motif"]
    if any(sum(row["motif"] == motif for row in candidates) != generated for motif in motifs):
        raise ValueError("wrong motif total")
    selected: list[dict[str, Any]] = []
    for motif in motifs:
        eligible: list[dict[str, Any]] = []
        for source in (row for row in candidates if row["motif"] == motif):
            row = copy.deepcopy(source)
            chosen = r9.choose_one_cut(row["scenario_id"], row["cut_ids"])
            okay, reason = r9.evaluate_eligibility(row["canonical_state_by_cut"][chosen],
                row["cut_by_id"][chosen], row["action_ids_by_cut"][chosen],
                row["gold_action_id_by_cut"][chosen])
            row.pop("eligible", None)
            row.pop("supplied_eligible", None)
            row.update({"chosen_cut_id": chosen, "eligible": okay,
                        "eligibility_reason": reason, "eligibility_source": "RECOMPUTED"})
            row["retention_hash"] = r9.framed_hash(
                [motif, row["scenario_id"], chosen, "stage2-retain-r10"]).hex().upper()
            if okay:
                eligible.append(row)
        eligible.sort(key=lambda row: (bytes.fromhex(row["retention_hash"]),
                                        row["scenario_id"].encode("utf-8")))
        retained = freeze["retained_unique_scenarios_per_motif"]
        if len(eligible) < retained:
            raise ValueError("eligible motif shortfall")
        selected.extend(eligible[:retained])
    if len(selected) != freeze["selected_total"]:
        raise ValueError("selected-total invariant failed")
    return selected


# ---- Measurement and provider call ledger --------------------------------

def measurement_grid_r10() -> set[tuple[int, int, int]]:
    axes = load_contract("MBCX-01-MEASUREMENT-CONTRACT-v4.json")["axis_values"]
    return {(h, d, f) for h in axes["H"] for d in axes["D"] for f in axes["F"]}


def baseline_counter_rows_r10(candidate_id: str = "BASELINE") -> list[dict[str, Any]]:
    return [{"candidate_id": candidate_id, "H": h, "D": d, "F": f,
             "descendant_accounted": True, "child_escape": False,
             "counters": {"root_instructions": 100000, "child_instructions": 0,
                          "root_cpu_time_ns": 1000000, "child_cpu_time_ns": 0,
                          "peak_committed_bytes": 16777216}}
            for h, d, f in sorted(measurement_grid_r10())]


def evaluate_counter_grid_r10(rows: list[dict[str, Any]]) -> list[str]:
    contract = load_contract("MBCX-01-MEASUREMENT-CONTRACT-v4.json")
    errors: set[str] = set()
    required_keys = {"candidate_id", "H", "D", "F", "descendant_accounted", "child_escape", "counters"}
    expected = measurement_grid_r10()
    coordinates = [(row.get("H"), row.get("D"), row.get("F")) for row in rows]
    if len(rows) != 100 or set(coordinates) != expected or len(coordinates) != len(set(coordinates)):
        errors.add("GRID_COVERAGE_INVALID")
        return sorted(errors)
    counter_keys = set(contract["process_tree_accounting"]["required_counters"])
    for row in rows:
        if set(row) != required_keys or set(row.get("counters", {})) != counter_keys:
            errors.add("COUNTER_SCHEMA_INVALID")
            continue
        if row["descendant_accounted"] is not True or row["child_escape"] is not False:
            errors.add("DESCENDANT_ACCOUNTING_MISSING")
        if any(not isinstance(value, int) or isinstance(value, bool) or value < 0
               for value in row["counters"].values()):
            errors.add("COUNTER_SCHEMA_INVALID")
            continue
        total_i = row["counters"]["root_instructions"] + row["counters"]["child_instructions"]
        total_cpu = row["counters"]["root_cpu_time_ns"] + row["counters"]["child_cpu_time_ns"]
        budget = contract["affordability_gates"]
        if (total_i > budget["aggregate_instructions_absolute_max"]
                or total_cpu > budget["aggregate_cpu_time_absolute_max_ns"]
                or row["counters"]["peak_committed_bytes"] > budget["peak_committed_absolute_max_bytes"]):
            errors.add("AFFORDABILITY_LIMIT")
    shape = contract["boundedness_gates"]
    for d in contract["axis_values"]["D"]:
        for f in contract["axis_values"]["F"]:
            group = [row for row in rows if row["D"] == d and row["F"] == f]
            aggregates = [row["counters"]["root_instructions"] + row["counters"]["child_instructions"]
                          for row in group]
            cpu = [row["counters"]["root_cpu_time_ns"] + row["counters"]["child_cpu_time_ns"]
                   for row in group]
            memory = [row["counters"]["peak_committed_bytes"] for row in group]
            if (max(aggregates) - min(aggregates) > shape["aggregate_instruction_H_range_max"]
                    or max(cpu) - min(cpu) > shape["aggregate_cpu_time_H_range_max_ns"]
                    or max(memory) - min(memory) > shape["peak_committed_H_range_max_bytes"]):
                errors.add("H_SHAPE_LIMIT")
    return sorted(errors)


def execute_red_candidate_r10(name: str) -> list[dict[str, Any]]:
    if name not in load_contract("MBCX-01-MEASUREMENT-CONTRACT-v4.json")["red_candidates"]:
        raise ValueError("unknown red candidate")
    rows = baseline_counter_rows_r10(name)
    if name == "ROOT_LINEAR_10H":
        for row in rows:
            row["counters"]["root_instructions"] = 10 * row["H"]
    elif name == "HIDDEN_CHILD_LINEAR_10H":
        for row in rows:
            row["counters"]["child_instructions"] = 10 * row["H"]
    elif name == "ROOT_LINEAR_5H":
        for row in rows:
            row["counters"]["root_instructions"] = 5 * row["H"]
    elif name == "CHILD_ESCAPE":
        rows[0]["child_escape"] = True
    elif name == "CONSTANT_OVER_BUDGET":
        for row in rows:
            row["counters"]["root_instructions"] = 4000000
    return rows


@dataclass(frozen=True)
class CallLedger:
    state: str
    request_hash: str
    idempotency_token: str

    @classmethod
    def prepare(cls, request_hash: str, idempotency_token: str) -> "CallLedger":
        return cls("PREPARED", request_hash, idempotency_token)

    def transition(self, event: str, request_hash: str | None = None,
                   idempotency_token: str | None = None, route_attested: bool = False) -> "CallLedger":
        contract = load_contract("MBCX-01-MEASUREMENT-CONTRACT-v4.json")["call_ledger"]
        if event not in contract["events"]:
            raise ValueError("unknown ledger event")
        target = contract["transition_matrix"][self.state][event]
        if target == "ILLEGAL":
            raise ValueError("illegal ledger transition")
        if target == "PREPARED_IF_ROUTE_ATTESTS_EXACT_IDEMPOTENCY":
            if not route_attested:
                raise ValueError("ambiguous acceptance is terminal without attested idempotency")
            target = "PREPARED"
        if event == "RETRY_REQUESTED":
            if request_hash not in (None, self.request_hash) or idempotency_token not in (None, self.idempotency_token):
                raise ValueError("retry identity mismatch")
        return replace(self, state=target)

    def can_retry(self, route_attested: bool) -> bool:
        return self.state == "PROVEN_PRE_ACCEPT_FAILURE" or (
            self.state == "ACCEPTANCE_AMBIGUOUS" and route_attested)


# ---- Missingness and reliability ------------------------------------------

def _stream_hull(values: list[float | None], choices: tuple[float, ...]) -> tuple[float, float]:
    kappa = 0.25
    states: dict[int, float] = {0: 1.0 / (2.0 * kappa * kappa)}
    scale = 2
    for index, observed in enumerate(values, start=1):
        next_states: dict[int, float] = {}
        possible = choices if observed is None else (observed,)
        for scaled_sum, variance in states.items():
            prefix = scaled_sum / scale
            estimate = (0.5 + prefix) / index
            for value in possible:
                new_sum = scaled_sum + int(round(scale * value))
                new_variance = variance + r9.psi_e(abs(value - estimate))
                next_states[new_sum] = max(next_states.get(new_sum, -math.inf), new_variance)
        states = next_states
    n = len(values)
    lowers, uppers = [], []
    for scaled_sum, variance in states.items():
        mean = (scaled_sum / scale) / n
        half = r9.mixture_boundary(variance, alpha=0.025, kappa=kappa) / n
        lowers.append(max(0.0, mean - half))
        uppers.append(min(1.0, mean + half))
    return min(lowers), max(uppers)


def _streams_from_observed(observed_pairs: list[tuple[int, int]], missing_positions: list[int]):
    n = len(observed_pairs) + len(missing_positions)
    if n != 768 or len(missing_positions) != len(set(missing_positions)) or any(
            not 0 <= pos < n for pos in missing_positions):
        raise ValueError("observed plus missing positions must partition 768")
    missing = set(missing_positions)
    iterator = iter(observed_pairs)
    delta: list[float | None] = []
    om: list[float | None] = []
    for position in range(n):
        if position in missing:
            delta.append(None); om.append(None)
        else:
            bc, oracle = next(iterator)
            delta.append((bc - oracle + 1.0) / 2.0)
            om.append(float(oracle))
    return delta, om


def missing_completion_bounds(observed_pairs: list[tuple[int, int]],
                              missing_positions: list[int]) -> tuple[float, float, float, float]:
    delta, om = _streams_from_observed(observed_pairs, missing_positions)
    delta_unit = _stream_hull(delta, (0.0, 0.5, 1.0))
    om_hull = _stream_hull(om, (0.0, 1.0))
    return 2 * delta_unit[0] - 1, 2 * delta_unit[1] - 1, om_hull[0], om_hull[1]


def exhaustive_missing_completion_bounds(observed_pairs: list[tuple[int, int]],
                                         missing_positions: list[int]) -> tuple[float, float, float, float]:
    if len(missing_positions) > 7:
        raise ValueError("exhaustive verifier is restricted to small witnesses")
    n = len(observed_pairs) + len(missing_positions)
    missing = set(missing_positions)
    results = []
    for completion in itertools.product(((0, 0), (0, 1), (1, 0), (1, 1)), repeat=len(missing_positions)):
        observed_it = iter(observed_pairs)
        completion_it = iter(completion)
        pairs = [next(completion_it) if i in missing else next(observed_it) for i in range(n)]
        delta, om = paired_intervals(pairs)
        results.append((delta[0], delta[1], om[0], om[1]))
    return (min(row[0] for row in results), max(row[1] for row in results),
            min(row[2] for row in results), max(row[3] for row in results))


def decision_with_missingness(observed_pairs: list[tuple[int, int]], missing_positions: list[int]) -> str:
    if not missing_positions:
        return scientific_decision(*paired_intervals(observed_pairs))
    delta_lower, delta_upper, om_lower, om_upper = missing_completion_bounds(
        observed_pairs, missing_positions)
    if om_upper < 0.80:
        return "MODEL_OR_INTERFACE_CEILING"
    if delta_upper < -0.10 and om_lower >= 0.80:
        return "MODEL_INTERFACE_FAIL"
    if delta_lower > -0.10 and om_lower >= 0.80:
        return "PROMOTE_TO_COORDINATION_STAGE"
    return "TRANSPORT_INCONCLUSIVE"


def binomial_cdf(allowed_failures: int, trials: int, probability: float) -> float:
    if not 0 <= allowed_failures <= trials or not 0 <= probability <= 1:
        raise ValueError("invalid binomial arguments")
    if probability == 0:
        return 1.0
    if probability == 1:
        return 1.0 if allowed_failures == trials else 0.0
    term = (1.0 - probability) ** trials
    total = term
    odds = probability / (1.0 - probability)
    for k in range(1, allowed_failures + 1):
        term *= (trials - k + 1) / k * odds
        total += term
    return total


def smallest_reliability_plan(p_bad: float, p_good: float, consumer_risk: float,
                              producer_risk: float) -> tuple[int, int]:
    for n in range(1, 10000):
        for allowed in range(n + 1):
            if (binomial_cdf(allowed, n, p_bad) <= consumer_risk
                    and binomial_cdf(allowed, n, p_good) >= 1.0 - producer_risk):
                return n, allowed
    raise ValueError("no plan found")

