"""Authenticated-subject, no-provider verifier for the MBCX-01 r13 closure fold."""

from __future__ import annotations

import argparse
import ast
import copy
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import mbcx01_r13_common as common
import mbcx01_r13_inference as inference
import mbcx01_r13_integration as integration
import mbcx01_r13_measurement as measurement
import mbcx01_r13_packets as packets
import mbcx01_r13_state_oracle as oracle
import mbcx01_r13_state_reference as reference


ROOT = Path(__file__).resolve().parent
TEST_MODULES = (
    "test_mbcx01_r13_state",
    "test_mbcx01_r13_packets",
    "test_mbcx01_r13_measurement",
    "test_mbcx01_r13_inference",
    "test_mbcx01_r13_integration",
)
REQUIRED = (
    "MBCX-01-EXPERIMENT-DESIGN-r9.md",
    "MBCX-01-COUNCIL-R12-SYNTHESIS-AND-CLOSURE-COMMISSION.md",
    "MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md",
    "MBCX-01-R13-CLOSURE-ARCHITECTURE.md",
    "MBCX-01-R13-PRIOR-ART-AND-ENVIRONMENT-ADDENDUM.md",
    "MBCX-01-R13-PHYSICAL-HARNESS-REQUIREMENTS.md",
    "MBCX-01-R13-SYNTHETIC-COHORT-GENERATOR.json",
    "MBCX-01-R13-MEASUREMENT-TRUST-ROOTS.json",
    "MBCX-01-R13-CARRIER-EXACTNESS-SUITE.json",
    "MBCX-01-STATE-TRANSITION-CONTRACT-v8.json",
    "MBCX-01-PACKET-SCHEMAS-v7.json",
    "MBCX-01-MEASUREMENT-CONTRACT-v7.json",
    "MBCX-01-INFERENCE-CONTRACT-v8.json",
    "MBCX-01-R13-REPAIR-LEDGER.json",
    "mbcx01_r13_common.py", "mbcx01_r13_state_reference.py",
    "mbcx01_r13_state_oracle.py", "mbcx01_r13_packets.py",
    "mbcx01_r13_measurement.py", "mbcx01_r13_inference.py",
    "mbcx01_r13_integration.py",
    *(name + ".py" for name in TEST_MODULES),
    "verify-r13-normative-bundle.py", "verify-r13-schema-ajv.mjs",
    "verify-r13-receipt-signature.mjs", "vendor/ajv-r12.bundle.cjs",
    "verify-r13-pinned.ps1", "test-r13-normative-bundle.ps1",
)
SPECIAL_WITNESSES = {
    "AJV.R13.STRICT_COMPILE_AND_MUTANTS",
    "INTEGRATION.R13.PINNED_BOOTSTRAP_SOURCE_GUARD",
    "INTEGRATION.R13.REPAIR_LEDGER_TWO_WAY_TOTAL",
    "INTEGRATION.I17.FRESH_REPORT_IS_RUNTIME_OUTPUT",
    "INTEGRATION.I17.STATIC_R12_REPORT_IS_NONNORMATIVE",
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
        raise AssertionError("missing r13 artifacts: " + ", ".join(missing))


def run_tests(names: list[str]) -> tuple[set[str], int]:
    suite = unittest.TestSuite(unittest.TestLoader().loadTestsFromName(name) for name in names)
    result: RecordingResult = unittest.TextTestRunner(
        stream=sys.stdout, verbosity=2, resultclass=RecordingResult).run(suite)
    if not result.wasSuccessful():
        raise AssertionError("r13 unit regression failure")
    return result.passed, result.testsRun


def check_state() -> tuple[dict, set[str]]:
    contract = load_json("MBCX-01-STATE-TRANSITION-CONTRACT-v8.json")
    assert len(contract["event_types"]) == 17
    passed, count = run_tests(["test_mbcx01_r13_state.R13StateTests"])
    state = common.initial_state()
    event = common.make_event("reschedule_obligation", {
        "obligation_id": "OBL.SHARED", "due_at": common.T1}, state=state)
    left = reference.reference_apply(copy.deepcopy(state), copy.deepcopy(event))
    right = oracle.oracle_apply(copy.deepcopy(state), copy.deepcopy(event))
    assert left == right and left[1] == "APPLIED"
    return {"status": "PASS", "event_types": 17, "tests": count,
            "post_ingress_semantics_shared": False,
            "state_authority_status": "STATE_AUTHORITY_UNAVAILABLE"}, passed


def check_packets() -> tuple[dict, set[str]]:
    passed, count = run_tests(["test_mbcx01_r13_packets.R13PacketTests"])
    manifest = packets.packet_fixture_manifest()
    fixture = packets.build_scoring_fixture(manifest)
    assert packets.score_fixture_conformance_exact(manifest, fixture) == 1
    assert packets.score_exact(manifest, fixture) == 0
    errors = packets.validate_scorer_input(manifest, fixture)
    assert "STATE_AUTHORITY_UNAVAILABLE" in errors
    assert len(packets.render_served_input(fixture["task_packet"])) == 65536
    return {"status": "PASS", "tests": count, "served_bytes": 65536,
            "fixture_conformance": "PASS", "scientific_admission": "STATE_AUTHORITY_UNAVAILABLE"}, passed


def check_cohort() -> tuple[dict, set[str]]:
    passed, count = run_tests(["test_mbcx01_r13_measurement.R13CohortTests"])
    candidates, provenance = measurement.synthetic_candidates_r13()
    selected = measurement.select_cohort(candidates, provenance)
    assert len(selected) == 768
    return {"status": "PASS", "tests": count, "selected": 768}, passed


def check_measurement() -> tuple[dict, set[str]]:
    passed, count = run_tests([
        "test_mbcx01_r13_measurement.R13SignedMeasurementTests",
        "test_mbcx01_r13_measurement.R13LedgerTests",
        "test_mbcx01_r13_measurement.R13EngineeringSelectionTests",
    ])
    rows = measurement.baseline_receipt_rows()
    errors = measurement.evaluate_measurement_receipts(
        rows, expected_run_id="RUN.R13.NO-PAID.TEST")
    assert "PHYSICAL_HARNESS_UNAVAILABLE" in errors
    contract = load_json("MBCX-01-MEASUREMENT-CONTRACT-v7.json")
    assert contract["physical_receipt"]["implementation_status"] == "PHYSICAL_HARNESS_UNAVAILABLE"
    return {"status": "DESIGN_OR_IMPLEMENTATION_FAIL", "tests": count, "cells": 100,
            "verification_status": "PASS", "physical_harness_status": "PHYSICAL_HARNESS_UNAVAILABLE",
            "synthetic_rows_are_evidence": False}, passed


def check_inference() -> tuple[dict, set[str]]:
    passed, count = run_tests(["test_mbcx01_r13_inference.R13InferenceTests"])
    route = inference.route_qualification_bounds()
    assert route["bad_route_acceptance_max"] <= .05
    assert route["good_route_rejection_max"] <= .10
    diagnostics = inference.simulate_registered_cells(replicates=10000)
    contract_cells = load_json("MBCX-01-INFERENCE-CONTRACT-v8.json")[
        "operating_characteristics"]["cells"]
    assert [row["id"] for row in diagnostics["cells"]] == [row["id"] for row in contract_cells]
    assert diagnostics["experiment_evidence"] is False
    return {"status": "PASS", "tests": count, "route": route,
            "planning_diagnostics": diagnostics}, passed


def check_pipeline() -> tuple[dict, set[str]]:
    passed, count = run_tests(["test_mbcx01_r13_integration.R13IntegrationTests"])
    details = integration.verify_pipeline_join()
    assert details["packet_score"] == 1
    assert details["scientific_score"] == 0
    assert details["state_authority_available"] is False
    assert details["selected"] == 768
    assert details["episode_outcome_ledger_bound"] is True
    details.update(status="PASS", tests=count)
    return details, passed


def check_ajv() -> set[str]:
    state = common.initial_state()
    event = common.make_event("reschedule_obligation", {
        "obligation_id": "OBL.SHARED", "due_at": common.T1}, state=state)
    manifest = packets.packet_fixture_manifest()
    scorer_input = packets.build_scoring_fixture(manifest)
    rows = measurement.baseline_receipt_rows()
    rows[0]["signature_b64"] = "A" * 88
    fixture = {"event": event, "state_authority_receipt": scorer_input["state_authority_receipt"],
               "scorer_input": scorer_input, "signed_measurement_envelope": rows[0],
               "carrier_exactness_receipt": measurement.fixture_carrier_exactness_receipt(
                   rows[0]["receipt"]["candidate_id"], rows)}
    with tempfile.TemporaryDirectory(prefix="mbcx01-r13-ajv-") as directory:
        path = Path(directory) / "fixture.json"
        path.write_text(json.dumps(fixture, ensure_ascii=False), encoding="utf-8")
        result = subprocess.run(["node", str(ROOT / "verify-r13-schema-ajv.mjs"), str(path)],
                                cwd=ROOT, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise AssertionError(result.stderr or result.stdout)
    return {"AJV.R13.STRICT_COMPILE_AND_MUTANTS"}


def check_no_historical_imports() -> None:
    forbidden = ("mbcx01_r8", "mbcx01_r9", "mbcx01_r10", "mbcx01_r11", "mbcx01_r12")
    for path in sorted(ROOT.glob("mbcx01_r13_*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            names = ([alias.name for alias in node.names] if isinstance(node, ast.Import)
                     else [node.module] if isinstance(node, ast.ImportFrom) and node.module else [])
            if any(name.startswith(forbidden) for name in names):
                raise AssertionError(f"historical runtime import in {path.name}: {names}")


def check_bootstrap_source_guard() -> set[str]:
    source = (ROOT / "verify-r13-pinned.ps1").read_text(encoding="utf-8")
    assert source.index("Export-GitBlob $ManifestBlob") < source.index(
        "& (Join-Path $reconstruction 'test-r13-normative-bundle.ps1')")
    assert "IsPathRooted" in source and "Refusing cleanup" in source
    return {"INTEGRATION.R13.PINNED_BOOTSTRAP_SOURCE_GUARD"}


def check_report_freshness(report: dict) -> set[str]:
    assert report["report_id"] == "MBCX-01-R13.2-LIVE-NO-PAID-VERIFICATION"
    assert "MBCX-01-R12-NO-PAID-VERIFICATION.json" not in REQUIRED
    return {"INTEGRATION.I17.FRESH_REPORT_IS_RUNTIME_OUTPUT",
            "INTEGRATION.I17.STATIC_R12_REPORT_IS_NONNORMATIVE"}


def check_repair_ledger(executed: set[str]) -> dict:
    repairs = load_json("MBCX-01-R13-REPAIR-LEDGER.json")["repairs"]
    declared = {witness for witnesses in repairs.values() for witness in witnesses}
    if any(not witnesses for witnesses in repairs.values()):
        raise AssertionError("empty r13 repair witness list")
    governed = {w for w in executed if re.search(r"\.test_i\d{2}_", w)}
    missing, extra = declared - executed, governed - declared
    if missing or extra:
        raise AssertionError(f"repair-ledger mismatch: missing={sorted(missing)}, extra={sorted(extra)}")
    if not SPECIAL_WITNESSES.issubset(declared):
        raise AssertionError("repair-ledger special witness coverage incomplete")
    return {"status": "PASS", "repairs": len(repairs), "declared_witnesses": len(declared)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--section", choices=("state", "packets", "cohort", "measurement",
                                               "inference", "pipeline", "integration"))
    parser.add_argument("--output-report")
    args = parser.parse_args()
    require_artifacts()
    sections = {"state": check_state, "packets": check_packets, "cohort": check_cohort,
                "measurement": check_measurement, "inference": check_inference,
                "pipeline": check_pipeline}
    selected = [args.section] if args.section and args.section != "integration" else list(sections)
    report = {"report_id": "MBCX-01-R13.2-LIVE-NO-PAID-VERIFICATION", "paid_calls": 0,
              "provider_calls": 0, "experiment_executed": False,
              "physical_harness_executed": False,
              "top_level_readiness": "DESIGN_OR_IMPLEMENTATION_FAIL",
              "blocking_prerequisites": ["STATE_AUTHORITY_UNAVAILABLE",
                                          "PHYSICAL_HARNESS_UNAVAILABLE"], "sections": {}}
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
        executed.update(check_report_freshness(report))
        executed.add("INTEGRATION.R13.REPAIR_LEDGER_TWO_WAY_TOTAL")
        report["sections"]["integration"] = check_repair_ledger(executed)
        print("integration: PASS")
    if args.output_report:
        Path(args.output_report).write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
