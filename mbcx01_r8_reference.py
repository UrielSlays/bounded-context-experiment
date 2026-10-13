"""Dependency-free executable reference for the MBCX-01 r8 preregistration.

This module is a scientific-instrument reference, not an FD/FC/TN candidate.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
import struct
from itertools import product
from pathlib import Path
from typing import Any


SCIENTIFIC_N = 384
ROOT = Path(__file__).resolve().parent


def canonical_json(value: Any) -> bytes:
    """Canonical bytes for the r8 domain (strings, booleans, safe integers)."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def load_contract(name: str) -> dict[str, Any]:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def action_id(scope_id: str, obligation_id: str) -> str:
    preimage = {"schema_id": "ActionIdentityV1", "scope_id": scope_id,
                "obligation_id": obligation_id}
    return "ACT." + hashlib.sha256(canonical_json(preimage)).hexdigest().upper()


def packet_hash(packet: dict[str, Any]) -> str:
    preimage = {key: value for key, value in packet.items() if key != "packet_hash"}
    return hashlib.sha384(canonical_json(preimage)).hexdigest().upper()


def maximal_packet() -> dict[str, Any]:
    """Construct a hand-checkable maximal DecisionPacketV3 fixture."""
    timestamp = "2026-08-12T00:00:00.000000Z"
    objects = []
    for i in range(64):
        suffix = f"{i:03d}"
        objects.append({
            "object_id": f"OBL.{suffix}", "object_kind": "OBLIGATION",
            "fields": {"scope_id": "SCOPE.MAX", "subject_id": f"SUB.{suffix}",
                       "owner_role": "WORKER", "due_at": timestamp,
                       "critical": True, "lifecycle": "OPEN",
                       "completion_action_id": f"COMPLETE.{suffix}",
                       "prerequisite_obligation_ids": [f"OBL.P{j:02d}" for j in range(16)]},
            "source_event_ids": [f"EV.{suffix}.{j:02d}" for j in range(32)]})
    catalog = []
    for i in range(16):
        oid = f"OBL.{i:03d}"
        catalog.append({"action_id": action_id("SCOPE.MAX", oid),
                        "action_kind": "ACT_ON_OBLIGATION", "scope_id": "SCOPE.MAX",
                        "obligation_id": oid})
    packet = {"schema_id": "DecisionPacketV3", "scenario_id": "SCENARIO.MAX",
              "cut": {"journal_seq": 9007199254740991, "knowledge_time": timestamp,
                      "valid_time": timestamp}, "objects": objects,
              "action_catalog": catalog,
              "available_action_ids": [entry["action_id"] for entry in catalog],
              "observation": {"observed_at": timestamp, "code": "TARGET_VISIBLE"}}
    packet["packet_hash"] = packet_hash(packet)
    return packet


def validate_worker_handoff(value: dict[str, Any]) -> bool:
    required = {"schema_id", "scenario_id", "scope_id", "input_packet_hash",
                "status_code", "proposed_action_ids", "evidence_event_ids",
                "unresolved_item_codes", "warning_codes", "produced_at"}
    if set(value) != required or value.get("schema_id") != "WorkerHandoffV3":
        return False
    actions = value.get("proposed_action_ids")
    if not isinstance(actions, list) or len(actions) > 4 or len(actions) != len(set(actions)):
        return False
    status = value.get("status_code")
    return (status == "PROPOSE" and len(actions) >= 1) or (
        status in ("ABSTAIN", "REJECT") and len(actions) == 0)


def score_condition(a0_selected: str, gold_a0: str, worker: dict[str, Any],
                    committed_actions: list[str], a1_selected: list[str],
                    gold_a1: list[str]) -> int:
    a0_ok = a0_selected == gold_a0
    b_ok = (validate_worker_handoff(worker) and worker["status_code"] == "PROPOSE"
            and worker["proposed_action_ids"] == [gold_a0]
            and committed_actions.count(gold_a0) == 1)
    a1_ok = sorted(a1_selected) == sorted(gold_a1) and len(a1_selected) == len(set(a1_selected))
    return int(a0_ok and b_ok and a1_ok)


def initial_reference_state() -> dict[str, Any]:
    return {"facts": {}, "obligations": {
        "OBL.SHARED": {"lifecycle": "OPEN", "due": True, "completion_action_id": "COMPLETE.SHARED",
                       "prerequisites": ["OBL.PREREQ"]},
        "OBL.PREREQ": {"lifecycle": "OPEN", "due": True, "completion_action_id": "COMPLETE.PREREQ",
                       "prerequisites": []}}, "dependencies": {("OBL.SHARED", "OBL.PREREQ")},
            "handoffs": {"HANDOFF.SHARED": {"status": "OPEN"}}, "responses": set(), "seen": set()}


def fixture_payload(event_type: str) -> dict[str, Any]:
    common = {"subject_id": "SUB.SHARED", "predicate_id": "PRED.SHARED",
              "value_code": "VALUE.SHARED", "parent_event_id": "EV.PARENT",
              "target_event_id": "EV.PARENT", "obligation_id": "OBL.SHARED",
              "owner_role": "WORKER", "due_at": "2026-08-12T00:00:00.000000Z",
              "critical": True, "completion_action_id": "COMPLETE.SHARED",
              "prerequisite_obligation_ids": [], "cancellation_code": "OWNER_CANCELLED",
              "prerequisite_obligation_id": "OBL.PREREQ", "handoff_id": "HANDOFF.SHARED",
              "target_obligation_id": "OBL.SHARED",
              "task_packet_hash": "A" * 96, "originating_cut_hash": "B" * 96,
              "scenario_id": "SCENARIO.SHARED", "condition": "BC", "node": "A0",
              "request_hash": "C" * 96, "response_hash": "D" * 96,
              "response_ref": "RESPONSE.SHARED", "provider_request_id": "PROVIDER.SHARED",
              "route_fingerprint": "E" * 96, "accepted_at": "2026-08-12T00:00:00.000000Z",
              "worker_handoff_hash": "F" * 96,
              "action_ids": [action_id("SCOPE.SHARED", "OBL.SHARED")],
              "proposal_event_id": "EV.PROPOSAL", "rejection_code": "SCHEMA_INVALID",
              "proposal_hash": "0" * 96}
    contract = load_contract("MBCX-01-STATE-ACTION-CONTRACT-v3.json")
    required = contract["event_types"][event_type]["payload_schema"]["required"]
    return {key: common[key] for key in required}


def legal_fixture(event_type: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return a prestate/payload making the named first transition legal."""
    state = initial_reference_state()
    payload = fixture_payload(event_type)
    if event_type == "open_obligation":
        payload["obligation_id"] = "OBL.NEW"
    elif event_type in ("complete_obligation", "unlink_dependency"):
        state["obligations"]["OBL.PREREQ"]["lifecycle"] = "COMPLETED"
    elif event_type == "reopen_obligation":
        state["obligations"]["OBL.SHARED"]["lifecycle"] = "COMPLETED"
    elif event_type == "link_dependency":
        state["dependencies"].clear()
        payload["prerequisite_obligation_id"] = "OBL.PREREQ"
    elif event_type == "open_handoff":
        payload["handoff_id"] = "HANDOFF.NEW"
    elif event_type == "commit_handoff_result":
        state["handoffs"]["HANDOFF.SHARED"]["status"] = "PROPOSED"
    elif event_type == "close_handoff":
        state["handoffs"]["HANDOFF.SHARED"]["status"] = "COMMITTED"
    elif event_type in ("correct_fact", "retract_fact"):
        state["facts"][(payload["subject_id"], payload["predicate_id"])] = {
            "value": "VALUE.PRIOR", "retracted": False}
    return state, payload


def apply_event(state: dict[str, Any], event_type: str,
                payload: dict[str, Any]) -> tuple[dict[str, Any], str]:
    """Small executable oracle for the transition properties r8 adjudicates."""
    contract = load_contract("MBCX-01-STATE-ACTION-CONTRACT-v3.json")
    rule = contract["event_types"].get(event_type)
    if rule is None:
        raise ValueError(f"unknown event type {event_type}")
    if set(payload) != set(rule["payload_schema"]["required"]):
        return copy.deepcopy(state), "SCHEMA_INVALID"
    new = copy.deepcopy(state)
    identity = ("SCOPE.SHARED", rule["semantic_operation"], canonical_json(payload))
    if identity in new["seen"]:
        return new, "DUPLICATE_NOOP"
    new["seen"].add(identity)
    oid = payload.get("obligation_id", "OBL.SHARED")
    obligation = new["obligations"].get(oid)
    result = "APPLIED"
    if event_type == "open_obligation":
        if obligation is not None:
            result = rule["illegal_result"]
        else:
            new["obligations"][oid] = {"lifecycle": "OPEN", "due": True,
                                        "completion_action_id": payload["completion_action_id"],
                                        "prerequisites": list(payload["prerequisite_obligation_ids"])}
    elif event_type in ("reschedule_obligation", "delegate_obligation", "cancel_obligation"):
        if not obligation or obligation["lifecycle"] != "OPEN":
            result = rule["illegal_result"]
        elif event_type == "cancel_obligation":
            obligation["lifecycle"] = "CANCELLED"
    elif event_type == "complete_obligation":
        blocked = any(new["obligations"].get(p, {}).get("lifecycle") != "COMPLETED"
                      for p in obligation.get("prerequisites", [])) if obligation else True
        if (not obligation or obligation["lifecycle"] != "OPEN" or blocked or
                payload["completion_action_id"] != obligation["completion_action_id"]):
            result = rule["illegal_result"]
        else:
            obligation["lifecycle"] = "COMPLETED"
    elif event_type == "reopen_obligation":
        if not obligation or obligation["lifecycle"] not in ("COMPLETED", "CANCELLED"):
            result = rule["illegal_result"]
        else:
            obligation["lifecycle"] = "OPEN"
    elif event_type == "link_dependency":
        edge = (oid, payload["prerequisite_obligation_id"])
        reverse = (payload["prerequisite_obligation_id"], oid)
        if edge in new["dependencies"] or reverse in new["dependencies"] or oid == payload["prerequisite_obligation_id"]:
            result = rule["illegal_result"]
        else:
            new["dependencies"].add(edge)
    elif event_type == "unlink_dependency":
        edge = (oid, payload["prerequisite_obligation_id"])
        if edge not in new["dependencies"]:
            result = rule["illegal_result"]
        else:
            new["dependencies"].remove(edge)
    elif event_type == "open_handoff":
        hid = payload["handoff_id"]
        if hid in new["handoffs"] or not obligation or obligation["lifecycle"] != "OPEN":
            result = rule["illegal_result"]
        else:
            new["handoffs"][hid] = {"status": "OPEN"}
    elif event_type in ("propose_handoff_result", "reject_handoff_result", "close_handoff",
                        "commit_handoff_result"):
        handoff = new["handoffs"].get(payload["handoff_id"])
        wanted = {"propose_handoff_result": "OPEN", "reject_handoff_result": "OPEN",
                  "commit_handoff_result": "PROPOSED", "close_handoff": "TERMINAL"}[event_type]
        legal = bool(handoff) and (handoff["status"] == wanted or
                                  (wanted == "TERMINAL" and handoff["status"] in ("COMMITTED", "REJECTED")))
        if not legal:
            result = rule["illegal_result"]
        else:
            handoff["status"] = {"propose_handoff_result": "PROPOSED",
                                  "reject_handoff_result": "REJECTED",
                                  "commit_handoff_result": "COMMITTED",
                                  "close_handoff": "CLOSED"}[event_type]
    elif event_type == "record_call_response":
        key = (payload["scenario_id"], payload["condition"], payload["node"])
        if key in new["responses"]:
            result = rule["illegal_result"]
        else:
            new["responses"].add(key)
    elif event_type in ("assert_fact", "correct_fact", "retract_fact"):
        key = (payload["subject_id"], payload["predicate_id"])
        if event_type == "assert_fact" and key in new["facts"]:
            result = rule["illegal_result"]
        elif event_type == "assert_fact":
            new["facts"][key] = {"value": payload["value_code"], "retracted": False}
        elif key not in new["facts"]:
            result = rule["illegal_result"]
        elif event_type == "correct_fact":
            new["facts"][key]["value"] = payload["value_code"]
        else:
            new["facts"][key]["retracted"] = True
    return new, result


def enumerate_ordered_pairs() -> list[dict[str, Any]]:
    events = list(load_contract("MBCX-01-STATE-ACTION-CONTRACT-v3.json")["event_types"])
    records = []
    for first in events:
        for second in events:
            pre, first_payload = legal_fixture(first)
            mid, first_result = apply_event(pre, first, first_payload)
            final, second_result = apply_event(mid, second, fixture_payload(second))
            records.append({"first": first, "second": second, "prestate": pre,
                            "first_result": first_result, "intermediate_state": mid,
                            "second_result": second_result, "final_state": final})
    return records


def validate_proposal_same_prestate(state: dict[str, Any], action_obligations: list[str]) -> str:
    """Validate every child against the immutable prestate, then commit atomically."""
    snapshot = copy.deepcopy(state)
    for obligation_id in action_obligations:
        obligation = snapshot["obligations"].get(obligation_id)
        if not obligation or obligation["lifecycle"] != "OPEN":
            return "REJECTED"
        if any(snapshot["obligations"].get(prereq, {}).get("lifecycle") != "COMPLETED"
               for prereq in obligation.get("prerequisites", [])):
            return "REJECTED"
    return "COMMITTED"


CALL_TRANSITIONS = {
    "PREPARED": {"DISPATCHED"},
    "DISPATCHED": {"RESPONSE_DURABLY_RECORDED", "PROVEN_PRE_ACCEPT_FAILURE", "ACCEPTANCE_AMBIGUOUS"},
    "RESPONSE_DURABLY_RECORDED": set(),
    "PROVEN_PRE_ACCEPT_FAILURE": {"DISPATCHED"},
    "ACCEPTANCE_AMBIGUOUS": set(),
}


def call_transition(state: str, target: str) -> str:
    if target not in CALL_TRANSITIONS.get(state, set()):
        return "ILLEGAL_TRANSITION"
    return target


def framed_hash(parts: list[str]) -> bytes:
    framed = b"".join(len(part.encode("utf-8")).to_bytes(8, "big") + part.encode("utf-8")
                      for part in parts)
    return hashlib.sha256(framed).digest()


def choose_one_cut(scenario_id: str, cut_ids: list[str]) -> str:
    ordered = sorted(cut_ids, key=lambda value: value.encode("utf-8"))
    if not ordered or len(ordered) != len(set(ordered)):
        raise ValueError("cut_ids must be nonempty and unique")
    digest = framed_hash([scenario_id, *ordered, "stage2-cut-r8"])
    return ordered[int.from_bytes(digest, "big") % len(ordered)]


def select_cohort(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    contract = load_contract("MBCX-01-MEASUREMENT-CONTRACT-v2.json")
    freeze = contract["source_and_cohort_freeze"]
    motifs = freeze["motifs"]
    generated = freeze["generated_unique_scenarios_per_motif"]
    retained = freeze["retained_unique_scenarios_per_motif"]
    selected = []
    for motif in motifs:
        rows = [copy.deepcopy(row) for row in candidates if row["motif"] == motif]
        if len(rows) != generated or len({row["scenario_id"] for row in rows}) != generated:
            raise ValueError(f"{motif} must have {generated} unique scenarios")
        eligible = []
        for row in rows:
            chosen = choose_one_cut(row["scenario_id"], row["cut_ids"])
            row["chosen_cut_id"] = chosen
            row["eligible"] = bool(row["eligibility_by_cut"].get(chosen, False))
            row["retention_hash"] = framed_hash(
                [motif, row["scenario_id"], chosen, "stage2-retain-r8"]).hex().upper()
            if row["eligible"]:
                eligible.append(row)
        eligible.sort(key=lambda row: (bytes.fromhex(row["retention_hash"]),
                                       row["scenario_id"].encode("utf-8")))
        if len(eligible) < retained:
            raise ValueError(f"DESIGN_OR_IMPLEMENTATION_FAIL: {motif} shortfall")
        selected.extend(eligible[:retained])
    if len({row["scenario_id"] for row in selected}) != len(selected):
        raise ValueError("scenario IDs must be globally unique")
    return selected


def measurement_grid() -> set[tuple[int, int, int]]:
    contract = load_contract("MBCX-01-MEASUREMENT-CONTRACT-v2.json")
    axes = contract["axis_values"]
    cells = {(h, d, 16) for h in axes["H"] for d in axes["D"]}
    f_curve = contract["required_cells"]["F_curve_at"]
    cells.update((f_curve["H"], f_curve["D"], f) for f in f_curve["F"])
    return cells


def synthetic_candidates() -> list[dict[str, Any]]:
    motifs = load_contract("MBCX-01-MEASUREMENT-CONTRACT-v2.json")["source_and_cohort_freeze"]["motifs"]
    rows = []
    for motif_index, motif in enumerate(motifs):
        for index in range(80):
            scenario_id = f"SCENARIO.{motif_index}.{index:03d}"
            cut_ids = [f"CUT.{scenario_id}.{cut:02d}" for cut in range(3)]
            rows.append({"motif": motif, "scenario_id": scenario_id, "cut_ids": cut_ids,
                         "eligibility_by_cut": {cut_id: True for cut_id in cut_ids}})
    return rows


def psi_e(x: float) -> float:
    if not 0.0 <= x < 1.0:
        raise ValueError("psi_E input must be in [0,1)")
    return -math.log1p(-x) - x


def stream_statistics(xs: list[float], kappa: float = 0.25) -> tuple[float, float]:
    if not xs or any(not 0.0 <= x <= 1.0 for x in xs):
        raise ValueError("observations must be a nonempty sequence in [0,1]")
    total = 1.0 / (2.0 * kappa * kappa)
    prefix = 0.0
    for index, value in enumerate(xs, 1):
        estimate = (0.5 + prefix) / index
        total += psi_e(abs(value - estimate))
        prefix += value
    return prefix, total


def mixture_integral_analytic(y: float, variance: float) -> float:
    if variance <= 0.0:
        raise ValueError("variance must be positive")
    root = math.sqrt(variance)
    shift = y / (2.0 * variance)
    difference = math.erf(root * (1.0 - shift)) - math.erf(root * (-1.0 - shift))
    return (math.exp(y * y / (4.0 * variance)) * math.sqrt(math.pi)
            * difference / (2.0 * root))


def mixture_integral_simpson(y: float, variance: float, intervals: int = 16384) -> float:
    if intervals <= 0 or intervals % 2:
        raise ValueError("Simpson intervals must be positive and even")
    width = 2.0 / intervals
    total = math.exp(-y - variance) + math.exp(y - variance)
    for index in range(1, intervals):
        z = -1.0 + index * width
        total += (4.0 if index % 2 else 2.0) * math.exp(y * z - variance * z * z)
    return total * width / 3.0


def mixture_boundary(variance: float, alpha: float = 0.025, kappa: float = 0.25,
                     method: str = "analytic") -> float:
    z_normalizer = math.erf(1.0 / (kappa * math.sqrt(2.0)))
    threshold = kappa * z_normalizer * math.sqrt(2.0 * math.pi) / alpha
    integral = mixture_integral_analytic if method == "analytic" else mixture_integral_simpson
    low, high = 0.0, 1.0
    while integral(high, variance) < threshold:
        high *= 2.0
        if high > 4096.0:
            raise ArithmeticError("failed to bracket mixture boundary")
    for _ in range(80):
        mid = (low + high) / 2.0
        if integral(mid, variance) < threshold:
            low = mid
        else:
            high = mid
    return (low + high) / 2.0


def mixture_interval(xs: list[float], alpha: float = 0.025,
                     kappa: float = 0.25, method: str = "analytic") -> tuple[float, float]:
    total, variance = stream_statistics(xs, kappa)
    half_width = mixture_boundary(variance, alpha, kappa, method) / len(xs)
    mean = total / len(xs)
    return max(0.0, mean - half_width), min(1.0, mean + half_width)


def paired_intervals(pairs: list[tuple[int, int]], method: str = "analytic") -> tuple[tuple[float, float], tuple[float, float]]:
    transformed_delta = [(bc - om + 1.0) / 2.0 for bc, om in pairs]
    delta_unit = mixture_interval(transformed_delta, method=method)
    delta = (2.0 * delta_unit[0] - 1.0, 2.0 * delta_unit[1] - 1.0)
    om = mixture_interval([float(pair[1]) for pair in pairs], method=method)
    return delta, om


def scientific_decision(delta_interval: tuple[float, float],
                        om_interval: tuple[float, float]) -> str:
    if om_interval[1] < 0.80:
        return "MODEL_OR_INTERFACE_CEILING"
    if delta_interval[1] < -0.10 and om_interval[0] >= 0.80:
        return "MODEL_INTERFACE_FAIL"
    if delta_interval[0] > -0.10 and om_interval[0] >= 0.80:
        return "PROMOTE_TO_COORDINATION_STAGE"
    return "INCONCLUSIVE_OR_UNDERFUNDED"


def completion_vectors(missing_count: int):
    if not 0 <= missing_count <= 7:
        raise ValueError("zero through seven missing pairs are enumerable")
    yield from product(((0, 0), (0, 1), (1, 0), (1, 1)), repeat=missing_count)


def sensitivity_decision(observed: list[tuple[int, int] | None]) -> str:
    positions = [index for index, pair in enumerate(observed) if pair is None]
    if len(positions) >= 8:
        return "TRANSPORT_INCONCLUSIVE"
    branches = set()
    for completion in completion_vectors(len(positions)):
        complete = list(observed)
        for position, pair in zip(positions, completion):
            complete[position] = pair
        intervals = paired_intervals([pair for pair in complete if pair is not None])
        branches.add(scientific_decision(*intervals))
        if len(branches) > 1:
            return "TRANSPORT_INCONCLUSIVE"
    return branches.pop()


def _counter_uniforms(seed_parts: list[str], count: int):
    seed = b"".join(len(part.encode("utf-8")).to_bytes(8, "big") + part.encode("utf-8")
                    for part in seed_parts)
    produced = 0
    counter = 0
    denominator = float(1 << 64)
    while produced < count:
        digest = hashlib.sha256(seed + counter.to_bytes(8, "big")).digest()
        for integer in struct.unpack(">QQQQ", digest):
            if produced >= count:
                break
            yield integer / denominator
            produced += 1
        counter += 1


def _draw_pair(value: float, cell: dict[str, Any]) -> tuple[int, int]:
    p00 = cell["p00"]
    p01 = p00 + cell["p01"]
    p10 = p01 + cell["p10"]
    if value < p00:
        return 0, 0
    if value < p01:
        return 0, 1
    if value < p10:
        return 1, 0
    return 1, 1


def simulate_oc(replicates: int = 100, seed: str = "MBCX01-R8-OC-V1") -> dict[str, Any]:
    if replicates <= 0:
        raise ValueError("replicates must be positive")
    contract = load_contract("MBCX-01-INFERENCE-CONTRACT-v3.json")
    cells_out = []
    for cell in contract["operating_characteristics"]["cells"]:
        probabilities = [cell[key] for key in ("p00", "p01", "p10", "p11")]
        if any(value < 0.0 for value in probabilities) or abs(sum(probabilities) - 1.0) > 1e-12:
            raise ValueError(f"invalid OC cell {cell['id']}")
        branches: dict[str, int] = {}
        delta_widths, om_widths = [], []
        for replicate in range(replicates):
            pairs = [_draw_pair(value, cell) for value in
                     _counter_uniforms([seed, cell["id"], str(replicate)], SCIENTIFIC_N)]
            delta_ci, om_ci = paired_intervals(pairs)
            branch = scientific_decision(delta_ci, om_ci)
            branches[branch] = branches.get(branch, 0) + 1
            delta_widths.append(delta_ci[1] - delta_ci[0])
            om_widths.append(om_ci[1] - om_ci[0])
        delta_widths.sort()
        om_widths.sort()
        p95_index = max(0, math.ceil(0.95 * replicates) - 1)
        cells_out.append({"id": cell["id"], "replicates": replicates,
                          "branch_counts": dict(sorted(branches.items())),
                          "mean_delta_width": sum(delta_widths) / replicates,
                          "p95_delta_width": delta_widths[p95_index],
                          "mean_om_width": sum(om_widths) / replicates,
                          "p95_om_width": om_widths[p95_index]})
    return {"schema_id": "MBCX01R8SyntheticOCV1", "experiment_evidence": False,
            "seed": seed, "n": SCIENTIFIC_N, "replicates_per_cell": replicates,
            "maximum_accepted_calls": SCIENTIFIC_N * 6,
            "expected_accepted_calls": SCIENTIFIC_N * 6, "cells": cells_out}


def scientific_look(n: int) -> str:
    """Return whether a registered prefix can bind the scientific branch."""
    if n not in (96, 192, 384):
        raise ValueError("n must be one of 96, 192, or 384")
    return "TERMINAL" if n == SCIENTIFIC_N else "DIAGNOSTIC_ONLY"
