#!/usr/bin/env python3
"""Execute behavioral witnesses over the MBCX-01 r9 normative bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import copy
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parent
REQUIRED = [
    "MBCX-01-EXPERIMENT-DESIGN-r8.md",
    "MBCX-01-STATE-ACTION-CONTRACT-v4.json",
    "MBCX-01-PACKET-SCHEMAS-v3.json",
    "MBCX-01-MEASUREMENT-CONTRACT-v3.json",
    "MBCX-01-INFERENCE-CONTRACT-v4.json",
]
SECTIONS = ("state", "packets", "cohort", "measurement", "inference", "integration")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--section", action="append", choices=SECTIONS)
    parser.add_argument("--oc-reps", type=int, default=100)
    parser.add_argument("--report", type=Path)
    return parser.parse_args()


SECTION_ARTIFACTS = {
    "state": ["MBCX-01-STATE-ACTION-CONTRACT-v4.json"],
    "packets": ["MBCX-01-PACKET-SCHEMAS-v3.json"],
    "cohort": ["MBCX-01-MEASUREMENT-CONTRACT-v3.json"],
    "measurement": ["MBCX-01-MEASUREMENT-CONTRACT-v3.json"],
    "inference": ["MBCX-01-INFERENCE-CONTRACT-v4.json"],
    "integration": REQUIRED,
}


def require_artifacts(selected: list[str]) -> None:
    names = sorted({name for section in selected for name in SECTION_ARTIFACTS[section]})
    missing = [name for name in names if not (ROOT / name).is_file()]
    if missing:
        raise AssertionError(f"missing r9 artifacts: {missing}")


def not_implemented(section: str) -> dict[str, object]:
    raise AssertionError(f"{section} r9 witness not implemented")


def check_state() -> dict[str, object]:
    from mbcx01_r9_oracle import oracle_apply
    from mbcx01_r9_reference import (
        enumerate_ordered_pairs,
        initial_state,
        make_event,
        reference_apply,
        run_mutation_suite,
    )

    contract = json.loads((ROOT / "MBCX-01-STATE-ACTION-CONTRACT-v4.json").read_text(
        encoding="utf-8"))
    assert len(contract["event_types"]) == 17
    envelope = contract["event_envelope"]
    assert envelope["additionalProperties"] is False
    assert set(("event_id", "scope_id", "event_type", "semantic_operation",
                "idempotency_key", "journal_seq", "observed_at", "valid_from",
                "valid_to", "originating_cut", "payload")) == set(envelope["required"])
    for event_type, rule in contract["event_types"].items():
        assert rule["payload_schema"]["additionalProperties"] is False, event_type
        assert rule["guard_id"] in contract["guard_catalog"], event_type
        assert rule["effect_id"] in contract["effect_catalog"], event_type

    state = initial_state()
    event = make_event("reschedule_obligation", {
        "obligation_id": "OBL.SHARED",
        "due_at": "2026-08-14T00:00:00.000000Z",
    })
    oracle_state, oracle_result = oracle_apply(copy.deepcopy(state), copy.deepcopy(event))
    reference_state, reference_result = reference_apply(copy.deepcopy(state), copy.deepcopy(event))
    assert oracle_result == reference_result == "APPLIED"
    assert oracle_state == reference_state
    assert reference_state["scopes"]["SCOPE.SHARED"]["obligations"]["OBL.SHARED"]["due_at"] == event["payload"]["due_at"]

    delegated, result = reference_apply(initial_state(), make_event(
        "delegate_obligation", {"obligation_id": "OBL.SHARED", "owner_role": "WRITER"}))
    assert result == "APPLIED"
    assert delegated["scopes"]["SCOPE.SHARED"]["obligations"]["OBL.SHARED"]["owner_role"] == "WRITER"

    cycle_state = initial_state()
    for obligation_id in ("OBL.A", "OBL.B", "OBL.C"):
        cycle_state, result = reference_apply(cycle_state, make_event(
            "open_obligation", {"obligation_id": obligation_id,
            "subject_id": "SUB.CYCLE", "owner_role": "WORKER",
            "due_at": "2026-08-13T00:00:00.000000Z", "critical": True,
            "completion_action_id": "ACT." + "A" * 64,
            "prerequisite_obligation_ids": []}, state=cycle_state))
        assert result == "APPLIED"
    for child, parent in (("OBL.A", "OBL.B"), ("OBL.B", "OBL.C")):
        cycle_state, result = reference_apply(cycle_state, make_event(
            "link_dependency", {"obligation_id": child,
            "prerequisite_obligation_id": parent}, state=cycle_state))
        assert result == "APPLIED"
    unchanged = copy.deepcopy(cycle_state)
    cycle_state, result = reference_apply(cycle_state, make_event(
        "link_dependency", {"obligation_id": "OBL.C",
        "prerequisite_obligation_id": "OBL.A"}, state=cycle_state))
    assert result == "DEPENDENCY_ILLEGAL" and cycle_state == unchanged

    duplicate_source = initial_state()
    duplicate_event = make_event("reschedule_obligation", {
        "obligation_id": "OBL.SHARED", "due_at": "2026-08-14T00:00:00.000000Z"})
    applied, result = reference_apply(duplicate_source, duplicate_event)
    assert result == "APPLIED"
    replayed, result = reference_apply(applied, copy.deepcopy(duplicate_event))
    assert result == "DUPLICATE_NOOP" and replayed == applied
    conflicting = copy.deepcopy(duplicate_event)
    conflicting["event_id"] = "EV.CONFLICT"
    conflicting["journal_seq"] += 1
    conflicting["payload"]["due_at"] = "2026-08-15T00:00:00.000000Z"
    conflict_state, result = reference_apply(applied, conflicting)
    assert result == "IDEMPOTENCY_CONFLICT" and conflict_state == applied

    pairs = enumerate_ordered_pairs()
    assert len(pairs) == 289
    assert all(row["oracle_result"] == row["reference_result"] and
               row["oracle_state"] == row["reference_state"] for row in pairs)
    mutations = run_mutation_suite()
    assert mutations and all(mutations.values()), mutations
    return {
        "event_types": 17,
        "ordered_pairs_differential": 289,
        "reschedule_effect": "EXECUTED",
        "delegate_effect": "EXECUTED",
        "three_node_cycle": "REJECTED",
        "exact_duplicate": "NO_STATE_CHANGE",
        "idempotency_conflict": "REJECTED",
        "mutants_killed": sorted(mutations),
    }


def check_packets() -> dict[str, object]:
    from mbcx01_r9_reference import (
        action_id,
        build_bc_packet,
        build_om_packet,
        canonical_json,
        packet_fixture_world,
        packet_hash,
        score_condition,
        validate_packet_schema,
        validate_packet_semantics,
    )

    contract = json.loads((ROOT / "MBCX-01-PACKET-SCHEMAS-v3.json").read_text(
        encoding="utf-8"))
    assert contract["json_schema_draft"] == "https://json-schema.org/draft/2020-12/schema"
    world, cut, actions, gold_read_set = packet_fixture_world()
    bc = build_bc_packet(cut, world, sorted(world), actions)
    om = build_om_packet(cut, world, gold_read_set, actions)
    assert validate_packet_schema(bc) == []
    assert validate_packet_schema(om) == []
    assert validate_packet_semantics(bc, world) == []
    assert validate_packet_semantics(om, world) == []
    assert bc["available_action_ids"] == om["available_action_ids"]
    assert bc["packet_hash"] == packet_hash(bc)
    assert om["packet_hash"] == packet_hash(om)
    assert len(canonical_json(bc)) < contract["renderer"]["fixed_byte_envelope"]
    assert len(canonical_json(om)) < contract["renderer"]["fixed_byte_envelope"]

    duplicate_object = copy.deepcopy(bc)
    duplicate_object["objects"].append(copy.deepcopy(duplicate_object["objects"][0]))
    duplicate_object["packet_hash"] = packet_hash(duplicate_object)
    assert "DUPLICATE_OBJECT_ID" in validate_packet_semantics(duplicate_object, world)

    alias = copy.deepcopy(bc)
    alias["action_catalog"].append({
        "action_id": alias["action_catalog"][0]["action_id"],
        "action_kind": "ACT_ON_OBLIGATION",
        "scope_id": "SCOPE.SHARED",
        "obligation_id": "OBL.DECOY",
    })
    alias["packet_hash"] = packet_hash(alias)
    assert "DUPLICATE_ACTION_ID" in validate_packet_semantics(alias, world)

    bogus = copy.deepcopy(bc)
    bogus["action_catalog"][0]["action_id"] = "ACT." + "F" * 64
    bogus["available_action_ids"][0] = "ACT." + "F" * 64
    bogus["packet_hash"] = packet_hash(bogus)
    assert "ACTION_HASH_MISMATCH" in validate_packet_semantics(bogus, world)

    missing_catalog = copy.deepcopy(bc)
    missing_catalog["action_catalog"] = missing_catalog["action_catalog"][:-1]
    missing_catalog["packet_hash"] = packet_hash(missing_catalog)
    assert "AVAILABLE_ACTION_UNRESOLVED" in validate_packet_semantics(missing_catalog, world)

    bad_no_action = copy.deepcopy(bc)
    no_action = next(row for row in bad_no_action["action_catalog"]
                     if row["action_id"] == "NO_ACTION")
    no_action["action_kind"] = "ACT_ON_OBLIGATION"
    no_action["scope_id"] = "SCOPE.SHARED"
    no_action["obligation_id"] = "OBL.SHARED"
    bad_no_action["packet_hash"] = packet_hash(bad_no_action)
    assert "NO_ACTION_KIND_MISMATCH" in validate_packet_semantics(bad_no_action, world)

    oversized = copy.deepcopy(bc)
    exemplar = oversized["objects"][0]
    oversized["objects"] = []
    for index in range(64):
        row = copy.deepcopy(exemplar)
        row["object_id"] = "O" + str(index).zfill(3) + "." + "X" * 120
        row["source_event_ids"] = ["E" + str(j).zfill(3) + "." + "Y" * 120
                                   for j in range(32)]
        oversized["objects"].append(row)
    oversized["packet_hash"] = packet_hash(oversized)
    assert len(canonical_json(oversized)) >= contract["renderer"]["fixed_byte_envelope"]
    assert "PACKET_ENVELOPE_EXCEEDED" in validate_packet_semantics(oversized, world)

    target = action_id("SCOPE.SHARED", "OBL.SHARED")
    extra = action_id("SCOPE.SHARED", "OBL.DECOY")
    worker = {"status_code": "PROPOSE", "proposed_action_ids": [target]}
    assert score_condition(target, worker, [target], [], []) == 1
    assert score_condition(target, {"status_code": "PROPOSE",
                                    "proposed_action_ids": [target, extra]},
                           [target, extra], [], []) == 0
    return {
        "schema_validator": contract["validator_runtime"],
        "bc_packet_bytes": len(canonical_json(bc)),
        "om_packet_bytes": len(canonical_json(om)),
        "oversized_packet_bytes": len(canonical_json(oversized)),
        "semantic_mutants_rejected": 6,
        "bc_om_builders": "EXECUTED",
        "stage2_b_score": "EXACT_SINGLETON_TARGET",
    }


def check_cohort() -> dict[str, object]:
    from mbcx01_r9_reference import (
        evaluate_eligibility,
        select_cohort,
        synthetic_candidates,
    )

    contract = json.loads((ROOT / "MBCX-01-MEASUREMENT-CONTRACT-v3.json").read_text(
        encoding="utf-8"))
    freeze = contract["source_and_cohort_freeze"]
    order = freeze["order"]
    for instrument_item in ("generator_spec_hash", "distribution_parameters_hash",
                            "gold_enumerator_hash", "eligibility_evaluator_hash"):
        assert order.index(instrument_item) < order.index("candidate_source_hashes")
    assert order.index("candidate_config_hashes") < order.index("fresh_confirmatory_seed")
    assert order.index("fresh_confirmatory_seed") < order.index("generated_candidates")
    assert order.index("one_cut_selection") < order.index("eligibility_recomputation")

    candidates = synthetic_candidates()
    assert len(candidates) == 960
    for row in candidates:
        row["supplied_eligible"] = False
    selected = select_cohort(candidates)
    assert len(selected) == 768
    assert len({row["scenario_id"] for row in selected}) == 768
    assert all(row["eligible"] and row["eligibility_source"] == "RECOMPUTED"
               for row in selected)
    counts: dict[str, int] = {}
    for row in selected:
        counts[row["motif"]] = counts.get(row["motif"], 0) + 1
    assert set(counts.values()) == {128}

    witness = selected[0]
    eligible, reason = evaluate_eligibility(
        witness["canonical_state_by_cut"][witness["chosen_cut_id"]],
        witness["cut_by_id"][witness["chosen_cut_id"]],
        witness["action_ids_by_cut"][witness["chosen_cut_id"]],
        witness["gold_action_id_by_cut"][witness["chosen_cut_id"]])
    assert eligible and reason == "ELIGIBLE"
    return {
        "generated_candidates": len(candidates),
        "retained_unique_scenarios": len(selected),
        "motif_counts": counts,
        "supplied_eligibility_ignored": True,
        "one_cut_before_eligibility": True,
    }


def check_measurement() -> dict[str, object]:
    from mbcx01_r9_reference import (
        baseline_counter_rows,
        evaluate_counter_grid,
        execute_red_candidate,
        measurement_grid,
    )

    contract = json.loads((ROOT / "MBCX-01-MEASUREMENT-CONTRACT-v3.json").read_text(
        encoding="utf-8"))
    grid = measurement_grid()
    expected_grid = {(h, d, f) for h in contract["axis_values"]["H"]
                     for d in contract["axis_values"]["D"]
                     for f in contract["axis_values"]["F"]}
    assert grid == expected_grid and len(grid) == 100
    assert (10000, 64, 256) in grid
    assert evaluate_counter_grid(baseline_counter_rows()) == []

    observed: dict[str, str] = {}
    for name, declaration in contract["red_candidates"].items():
        rows = execute_red_candidate(name)
        assert len(rows) == 100 and {(row["H"], row["D"], row["F"])
                                    for row in rows} == grid
        errors = evaluate_counter_grid(rows)
        expected = declaration["expected_error"]
        assert expected in errors, (name, expected, errors)
        observed[name] = expected
    assert "H_SHAPE_LIMIT" in evaluate_counter_grid(
        execute_red_candidate("LOW_SLOPE_ARCHIVE_LINEAR_10X"))
    assert "PAGE_BYTE_INCONSISTENT" in evaluate_counter_grid(
        execute_red_candidate("PAGE_BYTE_MISMATCH"))
    return {
        "unique_required_cells": len(grid),
        "full_cartesian_product": True,
        "registered_counters": len(contract["counter_catalog"]),
        "red_candidates_executed": observed,
    }


def check_inference(oc_reps: int = 100) -> dict[str, object]:
    from mbcx01_r9_reference import (
        kappa_sensitivity,
        clopper_pearson_upper,
        low_discord_pairs,
        mixture_interval,
        paired_intervals,
        reliability_cell_alpha,
        reliability_cell_budget,
        scientific_decision,
        scientific_look,
        simulate_oc,
        transport_readiness,
        zero_failure_min_trials,
    )

    contract = json.loads((ROOT / "MBCX-01-INFERENCE-CONTRACT-v4.json").read_text(
        encoding="utf-8"))
    method = contract["method"]
    assert method["kappa"] == 0.25
    assert method["kappa_source_rule"] == "SOURCE_DEFAULT_NOT_OC_TUNED"
    assert method["common_mean_assumption"] is False
    assert contract["looks"] == {"768": "TERMINAL_SCIENTIFIC_DECISION"}
    assert scientific_look(768) == "TERMINAL_SCIENTIFIC_DECISION"
    for forbidden in (96, 192, 384):
        try:
            scientific_look(forbidden)
        except ValueError:
            pass
        else:
            raise AssertionError(f"scientific interval still available at n={forbidden}")

    zero_delta = paired_intervals([(0, 0)] * 768)
    zero_half_width = zero_delta[0][1]
    assert abs(zero_half_width - 0.028724411075760736) < 1e-12
    analytic = paired_intervals(low_discord_pairs(), method="analytic")
    simpson = paired_intervals(low_discord_pairs(), method="simpson")
    decimal = paired_intervals(low_discord_pairs(), method="decimal")
    parity = max(abs(left - right) for reference in (simpson, decimal)
                 for analytic_stream, reference_stream in zip(analytic, reference)
                 for left, right in zip(analytic_stream, reference_stream))
    assert parity <= method["parity_tolerance_interval_endpoint"]
    vector = contract["reference_vectors"]["low_discord_deterministic"]
    expected_vector = (tuple(vector["expected_delta_interval"]),
                       tuple(vector["expected_om_interval"]))
    literal_error = max(abs(left - right) for actual_stream, expected_stream in zip(
        analytic, expected_vector) for left, right in zip(actual_stream, expected_stream))
    assert literal_error <= 1e-15
    assert scientific_decision(*analytic) == "PROMOTE_TO_COORDINATION_STAGE"

    sensitivity = kappa_sensitivity(low_discord_pairs())
    assert [row["kappa"] for row in sensitivity] == [0.10, 0.15, 0.25, 0.50, "UNIFORM"]
    assert all(row["n"] == 768 and "delta_interval" in row and "om_interval" in row
               for row in sensitivity)

    modes = len(contract["transport_readiness"]["failure_modes"])
    cell_alpha = reliability_cell_alpha(modes)
    cell_budget = reliability_cell_budget(modes)
    assert abs(cell_alpha * (6 * modes) - 0.05) < 1e-15
    assert abs(cell_budget * (6 * modes) - 0.02) < 1e-15
    min_trials = zero_failure_min_trials(modes)
    zero_reference = contract["transport_readiness"]["zero_failure_reference"]
    assert min_trials == zero_reference["trials_per_call_position"] == 16478
    assert 6 * min_trials == zero_reference["accepted_calls_across_six_positions"]
    assert clopper_pearson_upper(0, min_trials, cell_alpha) <= cell_budget
    assert clopper_pearson_upper(0, min_trials - 1, cell_alpha) > cell_budget
    readiness_contract = contract["transport_readiness"]
    counts = {(mode, position): (0, min_trials)
              for mode in readiness_contract["failure_modes"]
              for position in readiness_contract["call_positions"]}
    ready, bounds = transport_readiness(counts)
    assert ready and len(bounds) == 6 * modes
    assert contract["decision"]["precedence"][0] == "DESIGN_OR_IMPLEMENTATION_FAIL"

    cells = contract["operating_characteristics"]["cells"]
    negative = {(round(cell["delta"], 2), round(cell["om"], 2)) for cell in cells
                if cell["delta"] < 0}
    for delta in (-0.25, -0.12, -0.10):
        assert {(delta, 0.80), (delta, 0.85), (delta, 0.95)} <= negative
    first = simulate_oc(oc_reps)
    second = simulate_oc(oc_reps)
    assert first == second and first["experiment_evidence"] is False
    assert all(row["replicates"] == oc_reps for row in first["cells"])
    target_by_cell = {row["cell_id"]: row for row in contract["power_targets"]}
    observed_by_cell = {row["id"]: row for row in first["cells"]}
    if oc_reps >= 1000:
        for cell_id, target in target_by_cell.items():
            observed = observed_by_cell[cell_id]["branch_counts"].get(target["branch"], 0) / oc_reps
            assert observed >= target["minimum_probability"], (cell_id, observed, target)
    return {
        "delta_all_zero_half_width": zero_half_width,
        "three_way_endpoint_error": parity,
        "literal_reference_endpoint_error": literal_error,
        "kappa_sensitivity": sensitivity,
        "reliability_mode_count": modes,
        "reliability_cell_alpha": cell_alpha,
        "reliability_cell_budget": cell_budget,
        "zero_failure_trials_per_mode_position": min_trials,
        "synthetic_oc": first,
    }


def check_integration() -> dict[str, object]:
    design = (ROOT / "MBCX-01-EXPERIMENT-DESIGN-r8.md").read_text(encoding="utf-8")
    exact = {
        "MBCX-01-EXPERIMENT-DESIGN-r8.md",
        "MBCX-01-STATE-ACTION-CONTRACT-v4.json",
        "MBCX-01-PACKET-SCHEMAS-v3.json",
        "MBCX-01-MEASUREMENT-CONTRACT-v3.json",
        "MBCX-01-INFERENCE-CONTRACT-v4.json",
    }
    assert all(f"`{name}`" in design for name in exact)
    for stale in ("STATE-ACTION-CONTRACT-v3", "PACKET-SCHEMAS-v2",
                  "MEASUREMENT-CONTRACT-v2", "INFERENCE-CONTRACT-v3"):
        assert stale not in design
    assert "100 unique cells" in design
    assert "768" in design and "4,608" in design
    assert "DESIGN_OR_IMPLEMENTATION_FAIL" in design
    assert "TRANSPORT_INCONCLUSIVE" in design
    assert design.index("DESIGN_OR_IMPLEMENTATION_FAIL") < design.index(
        "TRANSPORT_INCONCLUSIVE")
    assert "zero paid calls" in design.lower()
    return {
        "normative_artifacts": sorted(exact),
        "full_hdf_cells": 100,
        "decision_precedence": "DESIGN_FAILURE_BEFORE_TRANSPORT",
        "evidence_class": "INSTRUMENT_VALIDATION_NOT_EXPERIMENT_RESULT",
    }


CHECKS: dict[str, Callable[[], dict[str, object]]] = {
    section: (lambda name=section: not_implemented(name)) for section in SECTIONS
}
CHECKS["state"] = check_state
CHECKS["packets"] = check_packets
CHECKS["cohort"] = check_cohort
CHECKS["measurement"] = check_measurement
CHECKS["inference"] = lambda: check_inference(100)
CHECKS["integration"] = check_integration


def main() -> int:
    args = parse_args()
    selected = args.section or list(SECTIONS)
    report: dict[str, object] = {
        "schema_id": "MBCX01R9NoPaidVerificationV1",
        "experiment_evidence": False,
        "paid_calls": 0,
        "evidence_class": "INSTRUMENT_VALIDATION_NOT_EXPERIMENT_RESULT",
        "sha384": {},
        "sections": {},
    }
    failed = False
    try:
        require_artifacts(selected)
    except AssertionError as exc:
        print(f"RED: {exc}", file=sys.stderr)
        return 1
    hash_names = [*REQUIRED, "mbcx01_r9_oracle.py", "mbcx01_r9_reference.py",
                  "verify-r9-normative-bundle.py", "verify-r9-schema-ajv.mjs"]
    report["sha384"] = {name: hashlib.sha384((ROOT / name).read_bytes()).hexdigest().upper()
                         for name in hash_names}
    sections = report["sections"]
    assert isinstance(sections, dict)
    for name in selected:
        try:
            details = check_inference(args.oc_reps) if name == "inference" else CHECKS[name]()
            sections[name] = {"status": "PASS", **details}
            print(f"{name}: PASS")
        except Exception as exc:  # verifier reports every requested section
            sections[name] = {"status": "FAIL", "error": repr(exc)}
            print(f"{name}: FAIL: {exc!r}", file=sys.stderr)
            failed = True
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
