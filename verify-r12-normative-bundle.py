"""Adversarial, no-provider verifier for the MBCX-01 r12 governing bundle."""

from __future__ import annotations

import argparse
import ast
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import mbcx01_r12_common as common
import mbcx01_r12_inference as inference
import mbcx01_r12_integration as integration
import mbcx01_r12_measurement as measurement
import mbcx01_r12_packets as packets
import mbcx01_r12_state_oracle as oracle
import mbcx01_r12_state_reference as reference


ROOT = Path(__file__).resolve().parent
TEST_MODULES = (
    "test_mbcx01_r12_state",
    "test_mbcx01_r12_packets",
    "test_mbcx01_r12_measurement",
    "test_mbcx01_r12_inference",
    "test_mbcx01_r12_integration",
)
REQUIRED = (
    "MBCX-01-STATE-TRANSITION-CONTRACT-v7.json",
    "MBCX-01-PACKET-SCHEMAS-v6.json",
    "MBCX-01-MEASUREMENT-CONTRACT-v6.json",
    "MBCX-01-INFERENCE-CONTRACT-v7.json",
    "MBCX-01-R12-SYNTHETIC-COHORT-GENERATOR.json",
    "MBCX-01-R12-MEASUREMENT-TRUST-ROOTS.json",
    "MBCX-01-R12-REPAIR-LEDGER.json",
    "MBCX-01-R12-ARCHITECTURE-SPEC.md",
    "MBCX-01-R12-PRIOR-ART-AND-SHELF-MEMO.md",
    "MBCX-01-R12-PHYSICAL-HARNESS-REQUIREMENTS.md",
    "mbcx01_r12_common.py", "mbcx01_r12_state_reference.py",
    "mbcx01_r12_state_oracle.py", "mbcx01_r12_packets.py",
    "mbcx01_r12_measurement.py", "mbcx01_r12_inference.py",
    "mbcx01_r12_integration.py",
    *(name + ".py" for name in TEST_MODULES),
    "verify-r12-schema-ajv.mjs", "verify-r12-receipt-signature.mjs",
    "vendor/ajv-r12.bundle.cjs", "test-r12-normative-bundle.ps1",
    "verify-r12-pinned.ps1",
)
SPECIAL_WITNESSES = {
    "AJV.STRICT_COMPILE_AND_MUTANTS",
    "INTEGRATION.PINNED_BOOTSTRAP_SOURCE_GUARD",
    "INTEGRATION.REPAIR_LEDGER_TOTAL",
}


class RecordingResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.passed: set[str] = set()

    def addSuccess(self, test):  # noqa: N802
        super().addSuccess(test)
        self.passed.add(test.id())


def load_json(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def require_artifacts() -> None:
    missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
    if missing:
        raise AssertionError("missing r12 artifacts: " + ", ".join(missing))


def run_tests(names: list[str]) -> tuple[set[str], int]:
    suite = unittest.TestSuite(unittest.TestLoader().loadTestsFromName(name) for name in names)
    result: RecordingResult = unittest.TextTestRunner(
        stream=sys.stdout, verbosity=2, resultclass=RecordingResult).run(suite)
    if not result.wasSuccessful():
        raise AssertionError("r12 unit regression failure")
    return result.passed, result.testsRun


def check_state() -> tuple[dict, set[str]]:
    contract = load_json("MBCX-01-STATE-TRANSITION-CONTRACT-v7.json")
    assert len(contract["event_types"]) == 17
    passed, count = run_tests(["test_mbcx01_r12_state.R12StateTests"])
    state = common.initial_state()
    event = common.make_event("reschedule_obligation", {
        "obligation_id": "OBL.SHARED", "due_at": common.T1}, state=state)
    left = reference.reference_apply(copy.deepcopy(state), copy.deepcopy(event))
    right = oracle.oracle_apply(copy.deepcopy(state), copy.deepcopy(event))
    assert left == right and left[1] == "APPLIED"
    return {"status": "PASS", "event_types": 17, "tests": count,
            "post_ingress_semantics_shared": False}, passed


def check_packets() -> tuple[dict, set[str]]:
    passed, count = run_tests(["test_mbcx01_r12_packets.R12PacketTests"])
    manifest = packets.packet_fixture_manifest()
    fixture = packets.build_scoring_fixture(manifest)
    assert packets.score_exact(manifest, fixture) == 1
    assert len(packets.render_served_input(fixture["task_packet"])) == 65536
    return {"status": "PASS", "tests": count, "served_bytes": 65536,
            "authoritative_dual_reducer_replay": True}, passed


def check_cohort() -> tuple[dict, set[str]]:
    passed, count = run_tests(["test_mbcx01_r12_measurement.R12CohortTests"])
    candidates, provenance = measurement.synthetic_candidates_r12()
    selected = measurement.select_cohort(candidates, provenance)
    assert len(selected) == 768
    return {"status": "PASS", "tests": count, "selected": 768}, passed


def check_measurement() -> tuple[dict, set[str]]:
    passed, count = run_tests([
        "test_mbcx01_r12_measurement.R12SignedMeasurementTests",
        "test_mbcx01_r12_measurement.R12LedgerTests",
    ])
    rows = measurement.baseline_receipt_rows()
    # Unsigned local fixtures cannot establish physical readiness.
    errors = measurement.evaluate_measurement_receipts(rows,
                                                       expected_run_id="RUN.R12.NO-PAID.TEST")
    assert "PHYSICAL_HARNESS_UNAVAILABLE" in errors
    contract = load_json("MBCX-01-MEASUREMENT-CONTRACT-v6.json")
    assert contract["physical_receipt"]["implementation_status"] == "PHYSICAL_HARNESS_UNAVAILABLE"
    return {"status": "DESIGN_OR_IMPLEMENTATION_FAIL", "tests": count, "cells": 100,
            "verification_status": "PASS", "evaluator_status": "PASS",
            "physical_harness_status": "PHYSICAL_HARNESS_UNAVAILABLE",
            "synthetic_rows_are_evidence": False}, passed


def check_inference() -> tuple[dict, set[str]]:
    passed, count = run_tests(["test_mbcx01_r12_inference.R12InferenceTests"])
    route = inference.route_qualification_bounds()
    assert route["bad_route_acceptance_max"] <= .05
    assert route["good_route_rejection_max"] <= .10
    diagnostics = inference.simulate_registered_cells(replicates=10000)
    contract_cells = load_json("MBCX-01-INFERENCE-CONTRACT-v7.json")[
        "operating_characteristics"]["cells"]
    assert [row["id"] for row in diagnostics["cells"]] == [row["id"] for row in contract_cells]
    assert diagnostics["experiment_evidence"] is False
    return {"status": "PASS", "tests": count, "route": route,
            "planning_diagnostics": diagnostics}, passed


def check_pipeline() -> tuple[dict, set[str]]:
    passed, count = run_tests(["test_mbcx01_r12_integration.R12IntegrationTests"])
    details = integration.verify_pipeline_join()
    assert all(details[name] for name in (
        "writer_state_event_bound", "a1_postcommit_cut_bound",
        "proposal_authority_bound", "dual_reducer_replay_bound",
        "postcommit_state_hash_bound"))
    details.update(status="PASS", tests=count)
    return details, passed


def check_ajv() -> set[str]:
    event = common.make_event("reschedule_obligation", {
        "obligation_id": "OBL.SHARED", "due_at": common.T1}, state=common.initial_state())
    manifest = packets.packet_fixture_manifest()
    rows = measurement.baseline_receipt_rows()
    # Schema admission does not require a valid signature, only its closed representation.
    rows[0]["signature_b64"] = "A" * 88
    fixture = {"event": event, "scorer_input": packets.build_scoring_fixture(manifest),
               "signed_measurement_envelope": rows[0]}
    with tempfile.TemporaryDirectory(prefix="mbcx01-r12-ajv-") as directory:
        path = Path(directory) / "fixture.json"
        path.write_text(json.dumps(fixture, ensure_ascii=False), encoding="utf-8")
        result = subprocess.run(["node", str(ROOT / "verify-r12-schema-ajv.mjs"), str(path)],
                                cwd=ROOT, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise AssertionError(result.stderr or result.stdout)
    return {"AJV.STRICT_COMPILE_AND_MUTANTS"}


def check_no_historical_imports() -> None:
    forbidden = ("mbcx01_r8", "mbcx01_r9", "mbcx01_r10", "mbcx01_r11")
    for path in sorted(ROOT.glob("mbcx01_r12_*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            names = ([alias.name for alias in node.names] if isinstance(node, ast.Import)
                     else [node.module] if isinstance(node, ast.ImportFrom) and node.module else [])
            if any(name.startswith(forbidden) for name in names):
                raise AssertionError(f"historical runtime import in {path.name}: {names}")


def check_bootstrap_source_guard() -> set[str]:
    source = (ROOT / "verify-r12-pinned.ps1").read_text(encoding="utf-8")
    assert source.index("Export-GitBlob $ManifestBlob") < source.index(
        "& (Join-Path $reconstruction 'test-r12-normative-bundle.ps1')")
    assert "IsPathRooted" in source and "Refusing cleanup" in source
    return {"INTEGRATION.PINNED_BOOTSTRAP_SOURCE_GUARD"}


def check_repair_ledger(executed: set[str]) -> dict:
    repairs = load_json("MBCX-01-R12-REPAIR-LEDGER.json")["repairs"]
    for repair, witnesses in repairs.items():
        if not witnesses or any(witness not in executed for witness in witnesses):
            raise AssertionError(f"unexecuted or empty witnesses for {repair}: {witnesses}")
    declared = {witness for witnesses in repairs.values() for witness in witnesses}
    executed_tests = {witness for witness in executed if witness.startswith("test_mbcx01_r12")}
    declared_tests = {witness for witness in declared if witness.startswith("test_mbcx01_r12")}
    if executed_tests != declared_tests:
        raise AssertionError(
            f"repair-ledger mismatch: missing={sorted(executed_tests-declared_tests)}, "
            f"unexecuted={sorted(declared_tests-executed_tests)}")
    if SPECIAL_WITNESSES != {witness for witness in declared if witness in SPECIAL_WITNESSES}:
        raise AssertionError("repair-ledger special witness coverage incomplete")
    return {"status": "PASS", "repairs": len(repairs),
            "declared_witnesses": sum(len(rows) for rows in repairs.values())}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--section", choices=("state", "packets", "cohort", "measurement",
                                               "inference", "pipeline", "integration"))
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    require_artifacts()
    sections = {"state": check_state, "packets": check_packets, "cohort": check_cohort,
                "measurement": check_measurement, "inference": check_inference,
                "pipeline": check_pipeline}
    selected = [args.section] if args.section and args.section != "integration" else list(sections)
    report = {"report_id": "MBCX-01-R12-NO-PAID-VERIFICATION", "paid_calls": 0,
              "provider_calls": 0, "experiment_executed": False,
              "physical_harness_executed": False,
              "top_level_readiness": "DESIGN_OR_IMPLEMENTATION_FAIL",
              "blocking_prerequisite": "PHYSICAL_HARNESS_UNAVAILABLE", "sections": {}}
    executed: set[str] = set()
    for name in selected:
        details, witnesses = sections[name]()
        report["sections"][name] = details
        executed.update(witnesses)
        print(f"{name}: PASS")
    if args.section in (None, "integration"):
        check_no_historical_imports()
        executed.update(check_bootstrap_source_guard())
        executed.update(check_ajv())
        executed.add("INTEGRATION.REPAIR_LEDGER_TOTAL")
        if args.section == "integration":
            for check in sections.values():
                _, witnesses = check()
                executed.update(witnesses)
        report["sections"]["integration"] = check_repair_ledger(executed)
        print("integration: PASS")
    if args.write_report:
        if args.section:
            raise ValueError("--write-report requires complete verifier")
        (ROOT / "MBCX-01-R12-NO-PAID-VERIFICATION.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
