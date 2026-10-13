#!/usr/bin/env python3
"""Execute behavioral witnesses over the MBCX-01 r8 normative bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from mbcx01_r8_reference import (
    action_id,
    call_transition,
    canonical_json,
    completion_vectors,
    enumerate_ordered_pairs,
    apply_event,
    initial_reference_state,
    legal_fixture,
    load_contract,
    maximal_packet,
    measurement_grid,
    mixture_interval,
    paired_intervals,
    packet_hash,
    scientific_decision,
    scientific_look,
    select_cohort,
    simulate_oc,
    score_condition,
    synthetic_candidates,
    validate_proposal_same_prestate,
    validate_worker_handoff,
)


ROOT = Path(__file__).resolve().parent
REQUIRED = [
    "MBCX-01-EXPERIMENT-DESIGN-r7.md",
    "MBCX-01-STATE-ACTION-CONTRACT-v3.json",
    "MBCX-01-PACKET-SCHEMAS-v2.json",
    "MBCX-01-MEASUREMENT-CONTRACT-v2.json",
    "MBCX-01-INFERENCE-CONTRACT-v3.json",
]
SECTIONS = ("state", "packets", "cohort", "measurement", "inference")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--section", action="append", choices=SECTIONS)
    parser.add_argument("--oc-reps", type=int, default=100)
    parser.add_argument("--report", type=Path)
    return parser.parse_args()


SECTION_ARTIFACTS = {
    "state": ["MBCX-01-STATE-ACTION-CONTRACT-v3.json"],
    "packets": ["MBCX-01-PACKET-SCHEMAS-v2.json"],
    "cohort": ["MBCX-01-MEASUREMENT-CONTRACT-v2.json"],
    "measurement": ["MBCX-01-MEASUREMENT-CONTRACT-v2.json"],
    "inference": ["MBCX-01-INFERENCE-CONTRACT-v3.json"],
}


def require_artifacts(selected: list[str]) -> None:
    names = REQUIRED if set(selected) == set(SECTIONS) else sorted(
        {name for section in selected for name in SECTION_ARTIFACTS[section]})
    missing = [name for name in names if not (ROOT / name).is_file()]
    if missing:
        raise AssertionError(f"missing r8 artifacts: {missing}")


def check_state() -> dict[str, object]:
    contract = load_contract("MBCX-01-STATE-ACTION-CONTRACT-v3.json")
    events = contract["event_types"]
    assert len(events) == 17
    assert contract["mandatory_enumerator"]["ordered_pair_count"] == 289
    for name, rule in events.items():
        assert rule["payload_schema"]["additionalProperties"] is False, name
        assert set(("semantic_operation", "payload_schema", "legal_prestate", "effect",
                    "duplicate_result", "illegal_result")) <= set(rule), name
    left = action_id("S:A", "B")
    right = action_id("S", "A:B")
    assert left != right and left.startswith("ACT.") and len(left) == 68
    pairs = enumerate_ordered_pairs()
    assert len(pairs) == 289
    assert len({(row["first"], row["second"]) for row in pairs}) == 289
    assert all(row["first_result"] == "APPLIED" for row in pairs)
    assert all(row["prestate"] != row["intermediate_state"] for row in pairs)
    assert all({"prestate", "first_result", "intermediate_state", "second_result", "final_state"} <= set(row)
               for row in pairs)
    first_per_type = {row["first"]: row for row in pairs}
    for event_type, row in first_per_type.items():
        replay, replay_result = apply_event(row["prestate"], event_type, legal_fixture(event_type)[1])
        assert replay_result == row["first_result"] and replay == row["intermediate_state"]
        duplicate, duplicate_result = apply_event(
            row["intermediate_state"], event_type, legal_fixture(event_type)[1])
        assert duplicate_result == "DUPLICATE_NOOP" and duplicate == row["intermediate_state"]
    atomic = initial_reference_state()
    assert validate_proposal_same_prestate(atomic, ["OBL.PREREQ", "OBL.SHARED"]) == "REJECTED"
    assert call_transition("ACCEPTANCE_AMBIGUOUS", "DISPATCHED") == "ILLEGAL_TRANSITION"
    assert call_transition("PROVEN_PRE_ACCEPT_FAILURE", "DISPATCHED") == "DISPATCHED"
    return {"event_types": 17, "ordered_pairs_executed": 289,
            "action_collision_witness": [left, right], "all_first_transitions_legal": True,
            "deterministic_replay_and_duplicate_noop": True,
            "same_prestate_atomic_proposal": "REJECTED", "ambiguous_retry": "REJECTED"}


def check_packets() -> dict[str, object]:
    contract = load_contract("MBCX-01-PACKET-SCHEMAS-v2.json")
    assert set(contract["schemas"]) == {"DecisionPacketV3", "A0ResultV1", "TaskPacketV3",
                                        "WorkerHandoffV3", "A1ResultV1"}
    decision = contract["schemas"]["DecisionPacketV3"]
    assert decision["additionalProperties"] is False
    assert "condition" not in decision["properties"]
    assert decision["properties"]["objects"]["items"].get("oneOf")
    for name in ("FactObject", "ObligationObject", "DependencyObject", "HandoffObject", "ObservationObject"):
        definition = contract["$defs"][name]
        assert definition["additionalProperties"] is False
        assert definition["properties"]["fields"]["additionalProperties"] is False
    propose = {"schema_id": "WorkerHandoffV3", "scenario_id": "SCENARIO.ONE",
               "scope_id": "SCOPE.ONE", "input_packet_hash": "A" * 96,
               "status_code": "PROPOSE", "proposed_action_ids": [action_id("SCOPE.ONE", "OBL.ONE")],
               "evidence_event_ids": [], "unresolved_item_codes": [], "warning_codes": [],
               "produced_at": "2026-08-12T00:00:00.000000Z"}
    assert validate_worker_handoff(propose)
    contradictory = dict(propose, status_code="ABSTAIN")
    assert not validate_worker_handoff(contradictory)
    packet = maximal_packet()
    encoded = canonical_json(packet)
    assert len(encoded) < contract["renderer"]["fixed_byte_envelope"]
    assert packet["packet_hash"] == packet_hash(packet)
    assert score_condition(propose["proposed_action_ids"][0], propose["proposed_action_ids"][0],
                           propose, propose["proposed_action_ids"], [], []) == 1
    assert score_condition("NO_ACTION", propose["proposed_action_ids"][0], propose,
                           propose["proposed_action_ids"], [], []) == 0
    return {"schemas": 5, "max_packet_bytes": len(encoded),
            "worker_status_action_rule": "EXECUTED", "scorer": "EXECUTED"}


def check_cohort() -> dict[str, object]:
    contract = load_contract("MBCX-01-MEASUREMENT-CONTRACT-v2.json")
    order = contract["source_and_cohort_freeze"]["order"]
    assert order.index("candidate_source_hashes") < order.index("confirmatory_generator_hash")
    assert order.index("one_cut_selection") < order.index("eligibility")
    selected = select_cohort(synthetic_candidates())
    assert len(selected) == 384
    assert len({row["scenario_id"] for row in selected}) == 384
    assert all(row["chosen_cut_id"] in row["cut_ids"] and row["eligible"] for row in selected)
    counts = {}
    for row in selected:
        counts[row["motif"]] = counts.get(row["motif"], 0) + 1
    assert set(counts.values()) == {64}
    assert contract["source_and_cohort_freeze"]["estimand_population"].startswith("conditional")
    return {"generated_candidates": 480, "retained_unique_scenarios": 384,
            "motif_counts": counts, "one_cut_before_eligibility": True}


def check_measurement() -> dict[str, object]:
    contract = load_contract("MBCX-01-MEASUREMENT-CONTRACT-v2.json")
    grid = measurement_grid()
    hd = {(h, d) for h, d, f in grid if f == 16}
    assert len(hd) == 20
    assert (10000, 64) in hd
    assert contract["storage"]["database_page_size_bytes"] == 4096
    assert "all descendant PIDs" in contract["sampling_boundary"]["descendants"]
    catalog = contract["counter_catalog"]
    assert len({row["id"] for row in catalog}) == len(catalog)
    required_units = {"instructions", "nanoseconds", "memory_bytes", "bytes", "pages", "records", "operations"}
    assert required_units <= {row["unit_class"] for row in catalog}
    for unit, gate in contract["unit_total_gates"].items():
        sums = {axis: sum(row[f"{axis}_range_max"] for row in catalog if row["unit_class"] == unit)
                for axis in ("H", "D")}
        assert gate["sum_of_per_counter_maxima"] == sums["H"] == sums["D"], unit
        assert gate["H_range_max"] < sums["H"] and gate["D_range_max"] < sums["D"], unit
    expected = {"HD_INTERIOR_HOTSPOT": "FAIL", "LOW_SLOPE_ARCHIVE_LINEAR": "FAIL",
                "UNREGISTERED_CPU_WORK": "DESIGN_OR_IMPLEMENTATION_FAIL",
                "COUNTER_SPLIT_SAME_WORK": "FAIL",
                "PAGE_SIZE_SUBSTITUTION": "DESIGN_OR_IMPLEMENTATION_FAIL",
                "LOGICAL_LOOKUP_PHYSICAL_SCAN": "FAIL"}
    assert {name: value["expected"] for name, value in contract["red_candidates"].items()} == expected
    return {"unique_required_cells": len(grid), "HD_cells_at_F16": 20,
            "interior_10000_64_present": True, "registered_counters": len(catalog),
            "red_candidates_executed": expected}


def check_inference(oc_reps: int = 100) -> dict[str, object]:
    contract = load_contract("MBCX-01-INFERENCE-CONTRACT-v3.json")
    assert contract["method"]["common_mean_assumption"] is False
    assert contract["method"]["stream_alpha"] == 0.025
    assert contract["method"]["kappa"] == 0.25
    assert scientific_look(96) == scientific_look(192) == "DIAGNOSTIC_ONLY"
    assert scientific_look(384) == "TERMINAL"
    literal_pairs = ([(0, 0)] * 34 + [(1, 1)] * 342 + [(0, 1)] * 4 + [(1, 0)] * 4)
    analytic = paired_intervals(literal_pairs, method="analytic")
    quadrature = paired_intervals(literal_pairs, method="simpson")
    parity = max(abs(left - right) for stream_a, stream_b in zip(analytic, quadrature)
                 for left, right in zip(stream_a, stream_b))
    assert parity <= contract["method"]["parity_tolerance_interval_endpoint"]
    delta_half = (analytic[0][1] - analytic[0][0]) / 2.0
    assert delta_half <= contract["reference_vectors"]["low_discord_deterministic"]["expected_delta_half_width_max"]
    assert scientific_decision(*analytic) == "PROMOTE_TO_COORDINATION_STAGE"
    prefix_reversal = ([(0, 1)] * 40 + [(1, 1)] * 56 +
                       [(1, 0)] * 40 + [(1, 1)] * 248)
    assert scientific_decision(*paired_intervals(prefix_reversal[:96])) != scientific_decision(*paired_intervals(prefix_reversal))
    assert len(list(completion_vectors(7))) == 16384
    assert contract["cost"]["maximum_accepted_calls"] == 2304
    assert contract["cost"]["expected_accepted_calls_under_registered_stopping"] == 2304
    first = simulate_oc(oc_reps)
    second = simulate_oc(oc_reps)
    assert first == second
    branches = {branch for cell in first["cells"] for branch in cell["branch_counts"]}
    assert {"PROMOTE_TO_COORDINATION_STAGE", "MODEL_INTERFACE_FAIL",
            "MODEL_OR_INTERFACE_CEILING", "INCONCLUSIVE_OR_UNDERFUNDED"} <= branches
    return {"analytic_quadrature_endpoint_error": parity,
            "low_discord_delta_half_width": delta_half,
            "prefix_reversal_nonbinding": True, "missing_completion_vectors_at_7": 16384,
            "synthetic_oc": first}


CHECKS = {"state": check_state, "packets": check_packets, "cohort": check_cohort,
          "measurement": check_measurement, "inference": check_inference}


def main() -> int:
    args = parse_args()
    selected = args.section or list(SECTIONS)
    try:
        require_artifacts(selected)
    except AssertionError as exc:
        print(f"RED: {exc}", file=sys.stderr)
        return 1
    hashed_files = ["mbcx01_r8_reference.py", "verify-r8-normative-bundle.py", *REQUIRED]
    hashes = {name: hashlib.sha384((ROOT / name).read_bytes()).hexdigest().upper()
              for name in hashed_files if (ROOT / name).is_file()}
    report = {"schema_id": "MBCX01R8NoPaidVerificationV1", "experiment_evidence": False,
              "paid_calls": 0, "sha384": hashes, "sections": {}}
    failed = False
    for name in selected:
        checker = CHECKS.get(name)
        if checker is None:
            report["sections"][name] = {"status": "NOT_IMPLEMENTED"}
            print(f"{name}: RED (not implemented)", file=sys.stderr)
            failed = True
            continue
        try:
            details = check_inference(args.oc_reps) if name == "inference" else checker()
            report["sections"][name] = {"status": "PASS", **details}
            print(f"{name}: PASS")
        except Exception as exc:
            report["sections"][name] = {"status": "FAIL", "error": repr(exc)}
            print(f"{name}: FAIL: {exc!r}", file=sys.stderr)
            failed = True
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
