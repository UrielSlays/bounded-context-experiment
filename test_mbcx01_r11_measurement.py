from __future__ import annotations

import copy
import inspect
import json
import unittest

import mbcx01_r11_measurement as measurement


class R11CohortTests(unittest.TestCase):
    def test_cut_domain_is_contract_driven(self):
        cuts = ["CUT.A", "CUT.B", "CUT.C"]
        chosen = measurement.choose_one_cut("SCENARIO.000", cuts, "stage2-cut-r11")
        self.assertEqual(chosen, "CUT.B")
        self.assertNotEqual(chosen, measurement.choose_one_cut("SCENARIO.000", cuts, "stage2-cut-r9"))
        self.assertEqual(list(inspect.signature(measurement.select_cohort).parameters),
                         ["candidates", "provenance"])

    def test_generator_digest_is_the_pinned_generator_artifact_digest(self):
        _, provenance = measurement.synthetic_candidates_r11()
        spec, expected = measurement._generator_spec()
        self.assertEqual(provenance["generator_id"], spec["generator_id"])
        self.assertEqual(provenance["generator_digest"], expected)

    def test_source_provenance_rejects_motif_and_action_substitution(self):
        candidates, provenance = measurement.synthetic_candidates_r11()
        self.assertEqual(measurement.validate_source_provenance(candidates, provenance), [])
        forged = copy.deepcopy(candidates)
        forged[0]["motif"] = forged[160]["motif"]
        self.assertIn("SOURCE_PROVENANCE_MISMATCH",
                      measurement.validate_source_provenance(forged, provenance))
        for field in ("canonical_state_by_cut", "gold_action_id_by_cut", "cut_by_id"):
            forged = copy.deepcopy(candidates)
            forged[0][field] = {"FORGED": True}
            self.assertIn("SOURCE_PROVENANCE_MISMATCH",
                          measurement.validate_source_provenance(forged, provenance), field)
        forged_provenance = copy.deepcopy(provenance)
        forged_provenance["generator_digest"] = "NOT-A-DIGEST"
        forged_provenance["provenance_hash"] = measurement.sha384({
            key: value for key, value in forged_provenance.items() if key != "provenance_hash"})
        self.assertIn("SOURCE_PROVENANCE_INVALID",
                      measurement.validate_source_provenance(candidates, forged_provenance))
        forged = copy.deepcopy(candidates)
        forged[0]["action_ids_by_cut"][forged[0]["cut_ids"][0]] = ["ACT." + "F" * 64]
        self.assertIn("SOURCE_PROVENANCE_MISMATCH",
                      measurement.validate_source_provenance(forged, provenance))

    def test_cohort_selects_six_by_128_with_bound_provenance(self):
        candidates, provenance = measurement.synthetic_candidates_r11()
        selected = measurement.select_cohort(candidates, provenance)
        self.assertEqual(len(selected), 768)
        self.assertEqual({sum(row["motif"] == motif for row in selected)
                          for motif in measurement.MOTIFS}, {128})
        self.assertEqual(selected, sorted(selected,
            key=lambda row: measurement.hashlib.sha256(
                row["scenario_id"].encode("utf-8")).digest()))


class R11MeasurementTests(unittest.TestCase):
    def setUp(self):
        self.rows = measurement.baseline_receipt_rows()

    def test_synthetic_receipts_cannot_establish_a_physical_pass(self):
        self.assertEqual(measurement.evaluate_measurement_receipts(self.rows),
                         ["PHYSICAL_HARNESS_UNAVAILABLE"])

    def test_measurement_evaluator_is_total_for_nondict_rows(self):
        self.assertIn("MEASUREMENT_SCHEMA_INVALID",
                      measurement.evaluate_measurement_receipts([None] * 100))

    def test_mixed_candidate_grid_is_rejected(self):
        forged = copy.deepcopy(self.rows)
        for index, row in enumerate(forged):
            row["candidate_id"] = f"CANDIDATE.{index}"
            measurement.refresh_receipt_hash(row)
        self.assertIn("CANDIDATE_ID_MISMATCH",
                      measurement.evaluate_measurement_receipts(forged))

    def test_boolean_axis_is_rejected(self):
        forged = copy.deepcopy(self.rows)
        for row in forged:
            if row["D"] == 1:
                row["D"] = True
                measurement.refresh_receipt_hash(row)
        self.assertIn("MEASUREMENT_SCHEMA_INVALID",
                      measurement.evaluate_measurement_receipts(forged))

    def test_missing_io_or_job_completion_is_rejected(self):
        forged = copy.deepcopy(self.rows)
        del forged[0]["job_receipt"]["read_transfer_bytes"]
        measurement.refresh_receipt_hash(forged[0])
        self.assertIn("MEASUREMENT_SCHEMA_INVALID",
                      measurement.evaluate_measurement_receipts(forged))
        forged = copy.deepcopy(self.rows)
        forged[0]["job_receipt"]["active_processes_at_final_query"] = 1
        measurement.refresh_receipt_hash(forged[0])
        self.assertIn("DESCENDANT_ACCOUNTING_MISSING",
                      measurement.evaluate_measurement_receipts(forged))

    def test_unmeasured_external_work_is_rejected(self):
        forged = copy.deepcopy(self.rows)
        forged[0]["external_work_policy"] = "EXTERNAL_ALLOWED_UNMEASURED"
        measurement.refresh_receipt_hash(forged[0])
        self.assertIn("EXTERNAL_WORK_UNMEASURED",
                      measurement.evaluate_measurement_receipts(forged))

    def test_instruction_backend_and_candidate_identity_are_not_self_asserted_blanks(self):
        forged = copy.deepcopy(self.rows)
        forged[0]["job_receipt"]["instruction_backend"] = ""
        forged[0]["job_receipt"]["instruction_attribution"] = ""
        measurement.refresh_receipt_hash(forged[0])
        self.assertIn("INSTRUCTION_ACCOUNTING_MISSING",
                      measurement.evaluate_measurement_receipts(forged))
        forged = copy.deepcopy(self.rows)
        for row in forged:
            row["candidate_id"] = ""
            measurement.refresh_receipt_hash(row)
        self.assertIn("MEASUREMENT_SCHEMA_INVALID",
                      measurement.evaluate_measurement_receipts(forged))


class R11LedgerTests(unittest.TestCase):
    def test_empty_identity_is_rejected(self):
        with self.assertRaises(ValueError):
            measurement.CallLedger.prepare("", "BC", "B", "", "", "", "", "")

    def test_durable_transition_requires_exact_response_evidence(self):
        ledger = measurement.CallLedger.prepare(
            "SCENARIO.SHARED", "BC", "B", "A" * 96, "B" * 64,
            "C" * 96, "IDEM.SHARED", "D" * 96)
        ledger = ledger.transition("DISPATCH_CONFIRMED")
        with self.assertRaises(ValueError):
            ledger.transition("RESPONSE_BYTES_FSYNCED")
        durable = ledger.transition("RESPONSE_BYTES_FSYNCED", response_bytes=b'{"ok":true}',
                                    response_ref="RESPONSE.SHARED",
                                    provider_request_id="PROVIDER.SHARED",
                                    durability_receipt=measurement.durability_receipt_fixture(
                                        ledger, b'{"ok":true}'))
        self.assertEqual(durable.state, "RESPONSE_DURABLY_RECORDED")
        self.assertEqual(durable, measurement.CallLedger.recover(durable.serialize()))

    def test_corrupt_restart_is_rejected(self):
        ledger = measurement.CallLedger.prepare(
            "SCENARIO.SHARED", "BC", "B", "A" * 96, "B" * 64,
            "C" * 96, "IDEM.SHARED", "D" * 96)
        raw = json.loads(ledger.serialize())
        raw["request_parameters_hash"] = "E" * 96
        with self.assertRaises(ValueError):
            measurement.CallLedger.recover(json.dumps(raw, sort_keys=True, separators=(",", ":")))
        raw = json.loads(ledger.serialize())
        raw["scenario_id"] = ""
        raw["ledger_hash"] = measurement.sha384({
            key: value for key, value in raw.items() if key != "ledger_hash"})
        with self.assertRaises(ValueError):
            measurement.CallLedger.recover(json.dumps(raw, sort_keys=True, separators=(",", ":")))

    def test_ambiguous_retry_requires_structured_exact_attestation(self):
        ledger = measurement.CallLedger.prepare(
            "SCENARIO.SHARED", "BC", "B", "A" * 96, "B" * 64,
            "C" * 96, "IDEM.SHARED", "D" * 96)
        ledger = ledger.transition("DISPATCH_CONFIRMED").transition("CONNECTION_LOST_AFTER_DISPATCH")
        with self.assertRaises(ValueError):
            ledger.transition("RETRY_REQUESTED", route_attestation=True)
        attestation = measurement.route_attestation_fixture(ledger)
        retried = ledger.transition("RETRY_REQUESTED", route_attestation=attestation)
        self.assertEqual(retried.state, "PREPARED")

    def test_durable_response_is_immutable_and_preaccept_retry_is_prohibited(self):
        ledger = measurement.CallLedger.prepare(
            "SCENARIO.SHARED", "BC", "B", "A" * 96, "B" * 64,
            "C" * 96, "IDEM.SHARED", "D" * 96).transition("DISPATCH_CONFIRMED")
        durable = ledger.transition("RESPONSE_BYTES_FSYNCED", response_bytes=b'{"ok":true}',
            response_ref="RESPONSE.SHARED", provider_request_id="PROVIDER.SHARED",
            durability_receipt=measurement.durability_receipt_fixture(ledger, b'{"ok":true}'))
        with self.assertRaises(ValueError):
            durable.transition("RESPONSE_BYTES_FSYNCED", response_bytes=b'{"other":true}',
                response_ref="RESPONSE.OTHER", provider_request_id="PROVIDER.OTHER",
                durability_receipt=measurement.durability_receipt_fixture(ledger, b'{"other":true}'))
        failure = ledger.transition("PROVEN_NOT_ACCEPTED",
                                    preaccept_failure_receipt=measurement.preaccept_failure_fixture(ledger))
        with self.assertRaises(ValueError):
            failure.transition("RETRY_REQUESTED")
        with self.assertRaises(ValueError):
            ledger.transition("PROVEN_NOT_ACCEPTED")


if __name__ == "__main__":
    unittest.main()
