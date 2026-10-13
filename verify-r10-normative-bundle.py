"""Adversarial no-model verifier for the MBCX-01 r10 normative bundle."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib
import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REQUIRED = [
    "MBCX-01-EXPERIMENT-DESIGN-r9.md",
    "MBCX-01-STATE-ACTION-CONTRACT-v5.json",
    "MBCX-01-PACKET-SCHEMAS-v4.json",
    "MBCX-01-MEASUREMENT-CONTRACT-v4.json",
    "MBCX-01-INFERENCE-CONTRACT-v5.json",
    "mbcx01_r10_reference.py",
    "mbcx01_r10_oracle.py",
    "verify-r10-schema-ajv.mjs",
    "MBCX-01-R10-PIN-MANIFEST.json",
    "verify-r10-pinned.ps1",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--section", choices=(
        "state", "packets", "cohort", "measurement", "inference", "integration"))
    parser.add_argument("--write-report", action="store_true")
    return parser.parse_args()


def load_json(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def require_artifacts() -> None:
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    if missing:
        raise AssertionError("missing r10 artifacts: " + ", ".join(missing))


def check_state(ref, oracle) -> dict:
    contract = load_json("MBCX-01-STATE-ACTION-CONTRACT-v5.json")
    assert contract["contract_id"].endswith("v5")
    assert contract["schema_ingress"]["independence_boundary"] == "AFTER_SHARED_SCHEMA_VALIDATION"
    assert len(contract["event_types"]) == 17

    state = ref.initial_state()
    legal = ref.make_event("reschedule_obligation", {
        "obligation_id": "OBL.SHARED", "due_at": ref.T1}, state=state)
    a, ar = ref.reference_apply(copy.deepcopy(state), copy.deepcopy(legal))
    b, br = oracle.oracle_apply(copy.deepcopy(state), copy.deepcopy(legal))
    assert (a, ar) == (b, br) and ar == "APPLIED"

    malformed = copy.deepcopy(legal)
    malformed["journal_seq"] = "1"
    assert ref.reference_apply(state, malformed)[1] == "SCHEMA_INVALID"
    assert oracle.oracle_apply(state, malformed)[1] == "SCHEMA_INVALID"
    impossible = copy.deepcopy(legal)
    impossible["observed_at"] = "2026-02-30T00:00:00.000000Z"
    assert ref.reference_apply(state, impossible)[1] == "SCHEMA_INVALID"
    assert oracle.oracle_apply(state, impossible)[1] == "SCHEMA_INVALID"

    bad_open = ref.make_event("open_obligation", {
        "obligation_id": "OBL.FORGED", "subject_id": "SUB.FORGED",
        "owner_role": "WORKER", "due_at": ref.T1, "critical": True,
        "completion_action_id": ref.action_id("SCOPE.SHARED", "OBL.OTHER"),
        "prerequisite_obligation_ids": []}, state=state)
    assert ref.reference_apply(state, bad_open)[1] == "ACTION_ID_HASH_GUARD"
    assert oracle.oracle_apply(state, bad_open)[1] == "ACTION_ID_HASH_GUARD"

    def fact_state(valid_from: str, valid_to: str | None, observed_at: str, seq: int = 1):
        s = ref.initial_state()
        key = ref.fact_key("SUB.X", "PRED.X")
        s["scopes"]["SCOPE.SHARED"]["facts"][key] = [{
            "event_id": "EV.FACT.X", "parent_event_id": None, "value_code": "VALUE.X",
            "observed_at": observed_at, "valid_from": valid_from, "valid_to": valid_to,
            "journal_seq": seq, "retracted": False}]
        s["next_seq"] = 2
        return s

    for bad_state in (
        fact_state("2026-08-10T00:00:00.000000Z", "2026-08-12T12:00:00.000000Z", ref.T0),
        fact_state("2026-08-14T00:00:00.000000Z", None, ref.T0),
        fact_state(ref.T0, None, "2026-08-14T00:00:00.000000Z"),
    ):
        cut = {"journal_seq": 1, "knowledge_time": ref.T1, "valid_time": ref.T1}
        event = ref.make_event("retract_fact", {
            "subject_id": "SUB.X", "predicate_id": "PRED.X", "target_event_id": "EV.FACT.X"},
            state=bad_state, originating_cut=cut)
        assert ref.reference_apply(bad_state, event)[1] == "FACT_TARGET_UNAVAILABLE"
        assert oracle.oracle_apply(bad_state, event)[1] == "FACT_TARGET_UNAVAILABLE"

    assert all(ref.run_r10_mutation_suite().values())
    return {"status": "PASS", "event_types": 17, "mutants": ref.run_r10_mutation_suite()}


def check_packets(ref) -> dict:
    schema_contract = load_json("MBCX-01-PACKET-SCHEMAS-v4.json")
    assert len(schema_contract["schemas"]) == 6
    compiled = subprocess.run(
        ["node", str(ROOT / "verify-r10-schema-ajv.mjs"), "--self-test"],
        cwd=ROOT, capture_output=True, text=True, check=False)
    assert compiled.returncode == 0, compiled.stderr or compiled.stdout

    manifest, world, selected = ref.packet_fixture_manifest()
    bc = ref.build_bc_packet(manifest, selected)
    om = ref.build_om_packet(manifest, manifest["gold_read_set"])
    assert bc["action_catalog"] == om["action_catalog"] == manifest["action_catalog"]
    assert not ref.validate_packet_semantics(bc, manifest)
    invented = copy.deepcopy(bc)
    invented["scenario_id"] = "SCENARIO.INVENTED"
    invented["packet_hash"] = ref.packet_hash(invented)
    assert "MANIFEST_SCENARIO_MISMATCH" in ref.validate_packet_semantics(invented, manifest)
    changed = copy.deepcopy(bc)
    changed["objects"][0]["fields"][next(iter(changed["objects"][0]["fields"]))] = "FORGED"
    changed["packet_hash"] = ref.packet_hash(changed)
    assert "CANONICAL_OBJECT_MISMATCH" in ref.validate_packet_semantics(changed, manifest)

    served = ref.render_served_input(bc)
    assert len(served) == 65536 and served.startswith(ref.canonical_json(bc))
    assert set(served[len(ref.canonical_json(bc)):]) <= {0x20}
    assert ref.served_input_hash(served) == hashlib.sha256(served).hexdigest().upper()

    a0, worker, receipt, a1 = ref.scoring_fixture(manifest)
    assert ref.score_exact(manifest, a0, worker, receipt, a1) == 1
    forged = copy.deepcopy(worker)
    forged["response_hash"] = "0" * 96
    assert ref.score_exact(manifest, a0, forged, receipt, a1) == 0
    bad_a0 = copy.deepcopy(a0)
    bad_a0["selected_action_ids"] = ["NO_ACTION"]
    assert ref.score_exact(manifest, bad_a0, worker, receipt, a1) == 0
    return {"status": "PASS", "schemas": 6, "served_bytes": len(served)}


def check_cohort(ref) -> dict:
    candidates = ref.synthetic_candidates_r10()
    selected = ref.select_cohort_r10(copy.deepcopy(candidates))
    assert len(selected) == 768
    assert len({row["scenario_id"] for row in selected}) == 768
    counts = {}
    for row in selected:
        counts[row["motif"]] = counts.get(row["motif"], 0) + 1
    assert set(counts.values()) == {128} and len(counts) == 6

    unknown = copy.deepcopy(candidates)
    unknown.append(copy.deepcopy(unknown[0]))
    unknown[-1]["motif"] = "UNKNOWN_MOTIF"
    unknown[-1]["scenario_id"] = "SCENARIO.UNKNOWN"
    for bad in (unknown,):
        try:
            ref.select_cohort_r10(bad)
            raise AssertionError("unknown motif accepted")
        except ValueError:
            pass
    duplicate = copy.deepcopy(candidates)
    duplicate[-1]["scenario_id"] = duplicate[0]["scenario_id"]
    try:
        ref.select_cohort_r10(duplicate)
        raise AssertionError("global duplicate accepted")
    except ValueError:
        pass
    return {"status": "PASS", "selected": 768, "per_motif": counts}


def check_measurement(ref) -> dict:
    contract = load_json("MBCX-01-MEASUREMENT-CONTRACT-v4.json")
    assert len(ref.measurement_grid_r10()) == 100
    baseline = ref.baseline_counter_rows_r10()
    assert ref.evaluate_counter_grid_r10(baseline) == []
    expected = {
        "ROOT_LINEAR_10H": "H_SHAPE_LIMIT",
        "HIDDEN_CHILD_LINEAR_10H": "H_SHAPE_LIMIT",
        "CHILD_ESCAPE": "DESCENDANT_ACCOUNTING_MISSING",
        "CONSTANT_OVER_BUDGET": "AFFORDABILITY_LIMIT",
    }
    for name, error in expected.items():
        assert error in ref.evaluate_counter_grid_r10(ref.execute_red_candidate_r10(name))
    five_h_errors = ref.evaluate_counter_grid_r10(ref.execute_red_candidate_r10("ROOT_LINEAR_5H"))
    assert "H_SHAPE_LIMIT" not in five_h_errors

    matrix = contract["call_ledger"]["transition_matrix"]
    for state in contract["call_ledger"]["states"]:
        for event in contract["call_ledger"]["events"]:
            assert event in matrix[state]
    ledger = ref.CallLedger.prepare("REQ." + "A" * 92, "IDEM.CALL")
    ledger = ledger.transition("DISPATCH_CONFIRMED")
    ambiguous = ledger.transition("CONNECTION_LOST_AFTER_DISPATCH")
    assert ambiguous.state == "ACCEPTANCE_AMBIGUOUS" and not ambiguous.can_retry(False)
    assert ambiguous.can_retry(True)
    return {"status": "PASS", "cells": 100, "ledger_pairs": sum(len(v) for v in matrix.values())}


def check_inference(ref) -> dict:
    contract = load_json("MBCX-01-INFERENCE-CONTRACT-v5.json")
    assert contract["sample_size_selection"]["selected_n"] == 768
    assert contract["missingness"]["algorithm"] == "EXACT_DYNAMIC_PROGRAMMING_HULL"
    for m in range(0, 6):
        observed = [(1, 1)] * (768 - m)
        dp = ref.missing_completion_bounds(observed, list(range(768 - m, 768)))
        exhaustive = ref.exhaustive_missing_completion_bounds(observed, list(range(768 - m, 768)))
        for left, right in zip(dp, exhaustive):
            assert abs(left - right) <= 1e-12

    complete = [(1, 1)] * 768
    assert ref.decision_with_missingness(complete, []) == ref.scientific_decision(
        *ref.paired_intervals(complete))
    witness = [(1, 1)] * 600 + [(0, 0)] * 160
    assert ref.decision_with_missingness(witness, list(range(760, 768))) == "TRANSPORT_INCONCLUSIVE"

    assert ref.binomial_cdf(4, 456, 0.02) <= 0.05
    assert ref.binomial_cdf(4, 456, 0.005) >= 0.90
    assert ref.smallest_reliability_plan(0.02, 0.005, 0.05, 0.10) == (456, 4)
    assert contract["transport_readiness"]["scheduled_call_positions_before_retries"] == 2736
    return {"status": "PASS", "scientific_n": 768, "transport_plan": [456, 4]}


def check_integration(ref, oracle) -> dict:
    state = ref.initial_state()
    for event_type in ref.EVENT_TYPES:
        s, event = ref.legal_fixture(event_type)
        left = ref.reference_apply(copy.deepcopy(s), copy.deepcopy(event))
        right = oracle.oracle_apply(copy.deepcopy(s), copy.deepcopy(event))
        assert left == right, event_type
    manifest, _, selected = ref.packet_fixture_manifest()
    packet = ref.build_bc_packet(manifest, selected)
    assert not ref.validate_packet_semantics(packet, manifest)
    assert len(ref.render_served_input(packet)) == 65536
    return {"status": "PASS", "differential_event_types": len(ref.EVENT_TYPES)}


def main() -> int:
    args = parse_args()
    require_artifacts()
    ref = importlib.import_module("mbcx01_r10_reference")
    oracle = importlib.import_module("mbcx01_r10_oracle")
    checks = {
        "state": lambda: check_state(ref, oracle),
        "packets": lambda: check_packets(ref),
        "cohort": lambda: check_cohort(ref),
        "measurement": lambda: check_measurement(ref),
        "inference": lambda: check_inference(ref),
        "integration": lambda: check_integration(ref, oracle),
    }
    selected = [args.section] if args.section else list(checks)
    report = {
        "report_id": "MBCX-01-R10-NO-PAID-VERIFICATION",
        "paid_calls": 0,
        "experiment_evidence": False,
        "sections": {},
    }
    for name in selected:
        report["sections"][name] = checks[name]()
        print(f"{name}: PASS")
    if args.write_report and not args.section:
        (ROOT / "MBCX-01-R10-NO-PAID-VERIFICATION.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise
