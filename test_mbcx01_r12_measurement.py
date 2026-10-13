from __future__ import annotations

import copy
import inspect
import json
import subprocess
import unittest

import mbcx01_r12_measurement as measurement


RUN_ID = "RUN.R12.NO-PAID.TEST"
TEST_PRIVATE_KEY_PEM = """-----BEGIN PRIVATE KEY-----
MC4CAQAwBQYDK2VwBCIEIJ1hsZ3v/VpguoRK9JLsLMREScVpezJpGXA7rAMcrn9g
-----END PRIVATE KEY-----
"""


def sign_no_paid_test_envelopes(envelopes):
    for envelope in envelopes:
        if envelope["fixture_kind"] != "NO_PAID_TEST_FIXTURE":
            raise ValueError("test signer refuses non-fixture envelopes")
        measurement.refresh_receipt_hash(envelope)
    source = ("const {createPrivateKey,sign}=require('node:crypto');"
              "let d='';process.stdin.setEncoding('utf8');"
              "process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{"
              "const r=JSON.parse(d),k=createPrivateKey(r.k);"
              "process.stdout.write(JSON.stringify(r.ps.map(p=>sign(null,"
              "Buffer.from(p,'base64'),k).toString('base64'))));});")
    request = {"k": TEST_PRIVATE_KEY_PEM,
               "ps": [envelope["receipt_preimage_b64"] for envelope in envelopes]}
    result = subprocess.run(["node", "-e", source], input=json.dumps(request), text=True,
                            capture_output=True, timeout=15, check=True)
    for envelope, signature in zip(envelopes, json.loads(result.stdout)):
        envelope["signature_b64"] = signature
    return envelopes


class R12CohortTests(unittest.TestCase):
    def test_cut_domain_is_contract_driven(self):
        cuts = ["CUT.A", "CUT.B", "CUT.C"]
        chosen = measurement.choose_one_cut("SCENARIO.000", cuts, "stage2-cut-r12")
        self.assertNotEqual(chosen, measurement.choose_one_cut(
            "SCENARIO.000", cuts, "stage2-cut-r9"))
        self.assertEqual(list(inspect.signature(measurement.select_cohort).parameters),
                         ["candidates", "provenance"])

    def test_generator_digest_is_the_pinned_generator_artifact_digest(self):
        _, provenance = measurement.synthetic_candidates_r12()
        spec, expected = measurement._generator_spec()
        self.assertEqual(provenance["generator_id"], spec["generator_id"])
        self.assertEqual(provenance["generator_digest"], expected)

    def test_source_provenance_rejects_motif_and_action_substitution(self):
        candidates, provenance = measurement.synthetic_candidates_r12()
        self.assertEqual(measurement.validate_source_provenance(candidates, provenance), [])
        forged = copy.deepcopy(candidates)
        forged[0]["motif"] = forged[160]["motif"]
        self.assertIn("SOURCE_PROVENANCE_MISMATCH",
                      measurement.validate_source_provenance(forged, provenance))
        forged = copy.deepcopy(candidates)
        forged[0]["action_ids_by_cut"][forged[0]["cut_ids"][0]] = ["ACT." + "F" * 64]
        self.assertIn("SOURCE_PROVENANCE_MISMATCH",
                      measurement.validate_source_provenance(forged, provenance))

    def test_cohort_selects_six_by_128_with_bound_provenance(self):
        candidates, provenance = measurement.synthetic_candidates_r12()
        selected = measurement.select_cohort(candidates, provenance)
        self.assertEqual(len(selected), 768)
        self.assertEqual({sum(row["motif"] == motif for row in selected)
                          for motif in measurement.MOTIFS}, {128})


class R12SignedMeasurementTests(unittest.TestCase):
    def setUp(self):
        self.rows = sign_no_paid_test_envelopes(
            measurement.baseline_receipt_rows(run_id=RUN_ID))

    def _resign(self, rows):
        return sign_no_paid_test_envelopes(rows)

    def test_signed_no_paid_fixture_verifies_but_cannot_establish_physical_pass(self):
        self.assertEqual(measurement.evaluate_measurement_receipts(
            self.rows, expected_run_id=RUN_ID), ["PHYSICAL_HARNESS_UNAVAILABLE"])

    def test_contract_publishes_a_closed_nested_envelope_schema(self):
        with open("MBCX-01-MEASUREMENT-CONTRACT-v6.json", encoding="utf-8") as stream:
            schema = json.load(stream)["signed_measurement_envelope_schema"]
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertFalse(schema["additionalProperties"])
        self.assertFalse(schema["$defs"]["measurementReceiptV2"]["additionalProperties"])
        self.assertFalse(schema["$defs"]["jobReceiptV2"]["additionalProperties"])
        self.assertEqual(set(schema["required"]), set(schema["properties"]))

    def test_trust_root_is_separately_loaded_closed_and_fixture_only(self):
        roots = measurement._load_trust_roots()
        self.assertEqual(set(roots), {measurement.TEST_KEY_ID})
        self.assertTrue(roots[measurement.TEST_KEY_ID]["fixture_only"])
        self.assertNotIn("PRIVATE", roots[measurement.TEST_KEY_ID]["public_key_pem"])

    def test_unsigned_receipts_are_not_admissible(self):
        unsigned = [copy.deepcopy(row["receipt"]) for row in self.rows]
        errors = measurement.evaluate_measurement_receipts(unsigned, expected_run_id=RUN_ID)
        self.assertIn("MEASUREMENT_ENVELOPE_INVALID", errors)
        self.assertIn("PHYSICAL_HARNESS_UNAVAILABLE", errors)

    def test_receipt_mutation_without_resigning_breaks_signature(self):
        forged = copy.deepcopy(self.rows)
        forged[0]["receipt"]["candidate_id"] = "CANDIDATE.FORGED"
        measurement.refresh_receipt_hash(forged[0])
        self.assertIn("MEASUREMENT_SIGNATURE_INVALID",
                      measurement.evaluate_measurement_receipts(
                          forged, expected_run_id=RUN_ID))

    def test_fixture_kind_is_inside_the_signed_preimage(self):
        forged = copy.deepcopy(self.rows)
        forged[0]["fixture_kind"] = "PHYSICAL_HARNESS_RECEIPT"
        measurement.refresh_receipt_hash(forged[0])
        self.assertIn("MEASUREMENT_SIGNATURE_INVALID",
                      measurement.evaluate_measurement_receipts(
                          forged, expected_run_id=RUN_ID))

    def test_test_key_cannot_sign_a_physical_harness_receipt(self):
        forged = copy.deepcopy(self.rows)
        for envelope in forged:
            envelope["fixture_kind"] = "PHYSICAL_HARNESS_RECEIPT"
            measurement.refresh_receipt_hash(envelope)
        # Use the low-level test signer intentionally: evaluator must still reject
        # a cryptographically valid signature from the wrong trust-root class.
        source = ("const {createPrivateKey,sign}=require('node:crypto');let d='';"
                  "process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{"
                  "const r=JSON.parse(d),k=createPrivateKey(r.k);"
                  "process.stdout.write(JSON.stringify(r.ps.map(p=>sign(null,"
                  "Buffer.from(p,'base64'),k).toString('base64'))));});")
        request = {"k": TEST_PRIVATE_KEY_PEM,
                   "ps": [row["receipt_preimage_b64"] for row in forged]}
        result = subprocess.run(["node", "-e", source], input=json.dumps(request),
                                text=True, capture_output=True, check=True)
        for envelope, signature in zip(forged, json.loads(result.stdout)):
            envelope["signature_b64"] = signature
        errors = measurement.evaluate_measurement_receipts(forged, expected_run_id=RUN_ID)
        self.assertIn("MEASUREMENT_ENVELOPE_INVALID", errors)
        self.assertIn("PHYSICAL_HARNESS_UNAVAILABLE", errors)

    def test_receipt_supplied_or_unknown_key_cannot_become_a_trust_root(self):
        forged = copy.deepcopy(self.rows)
        forged[0]["signing_key_id"] = "ATTACKER.SELF.AUTHORED"
        forged[0]["public_key_pem"] = "ATTACKER-CONTROLLED"
        forged[0]["signature_b64"] = "AA=="
        errors = measurement.evaluate_measurement_receipts(forged, expected_run_id=RUN_ID)
        self.assertIn("MEASUREMENT_ENVELOPE_INVALID", errors)
        self.assertIn("PHYSICAL_HARNESS_UNAVAILABLE", errors)

    def test_run_and_cell_identities_are_signed_and_anti_replay_checked(self):
        replay = copy.deepcopy(self.rows)
        replay[0]["run_id"] = "RUN.R12.REPLAY"
        measurement.refresh_receipt_hash(replay[0])
        self._resign(replay)
        errors = measurement.evaluate_measurement_receipts(replay, expected_run_id=RUN_ID)
        self.assertIn("MEASUREMENT_REPLAY_IDENTITY_MISMATCH", errors)

    def test_mixed_candidate_grid_is_rejected_even_when_test_signed(self):
        forged = copy.deepcopy(self.rows)
        for index, envelope in enumerate(forged):
            envelope["receipt"]["candidate_id"] = f"CANDIDATE.{index}"
            measurement.refresh_receipt_hash(envelope)
        self._resign(forged)
        self.assertIn("CANDIDATE_ID_MISMATCH",
                      measurement.evaluate_measurement_receipts(
                          forged, expected_run_id=RUN_ID))

    def test_boolean_axis_is_rejected(self):
        forged = copy.deepcopy(self.rows)
        forged[0]["receipt"]["D"] = True
        measurement.refresh_receipt_hash(forged[0])
        self._resign(forged)
        self.assertIn("MEASUREMENT_SCHEMA_INVALID",
                      measurement.evaluate_measurement_receipts(
                          forged, expected_run_id=RUN_ID))

    def test_missing_io_or_job_completion_is_rejected(self):
        forged = copy.deepcopy(self.rows)
        del forged[0]["receipt"]["job_receipt"]["read_transfer_bytes"]
        measurement.refresh_receipt_hash(forged[0])
        self._resign(forged)
        self.assertIn("MEASUREMENT_SCHEMA_INVALID",
                      measurement.evaluate_measurement_receipts(
                          forged, expected_run_id=RUN_ID))
        forged = copy.deepcopy(self.rows)
        forged[0]["receipt"]["job_receipt"]["active_processes_at_final_query"] = 1
        measurement.refresh_receipt_hash(forged[0])
        self._resign(forged)
        self.assertIn("DESCENDANT_ACCOUNTING_MISSING",
                      measurement.evaluate_measurement_receipts(
                          forged, expected_run_id=RUN_ID))

    def test_unmeasured_external_work_is_rejected(self):
        forged = copy.deepcopy(self.rows)
        forged[0]["receipt"]["external_work_policy"] = "EXTERNAL_ALLOWED_UNMEASURED"
        measurement.refresh_receipt_hash(forged[0])
        self._resign(forged)
        self.assertIn("EXTERNAL_WORK_UNMEASURED",
                      measurement.evaluate_measurement_receipts(
                          forged, expected_run_id=RUN_ID))

    def test_instruction_mode_is_exactly_pinned_and_unsupported_is_fatal(self):
        forged = copy.deepcopy(self.rows)
        job = forged[0]["receipt"]["job_receipt"]
        job["instruction_backend"] = "ETW_PMC_SAMPLED_PROFILE_V1"
        measurement.refresh_receipt_hash(forged[0])
        self._resign(forged)
        self.assertIn("INSTRUCTION_ACCOUNTING_UNSUPPORTED",
                      measurement.evaluate_measurement_receipts(
                          forged, expected_run_id=RUN_ID))

    def test_etw_loss_or_incomplete_attribution_is_fatal(self):
        for field, value in (("etw_events_lost", 1),
                             ("etw_attribution_complete", False),
                             ("etw_counter_owner_conflict_count", 1),
                             ("etw_pmc_strict_mode", False),
                             ("etw_pmc_multiplexing_detected", True)):
            forged = copy.deepcopy(self.rows)
            forged[0]["receipt"]["job_receipt"][field] = value
            measurement.refresh_receipt_hash(forged[0])
            self._resign(forged)
            self.assertIn("INSTRUCTION_ACCOUNTING_INCOMPLETE",
                          measurement.evaluate_measurement_receipts(
                              forged, expected_run_id=RUN_ID), field)

    def test_total_io_transfer_has_an_h_shape_gate(self):
        forged = copy.deepcopy(self.rows)
        row = next(envelope for envelope in forged
                   if (envelope["receipt"]["H"], envelope["receipt"]["D"],
                       envelope["receipt"]["F"]) == (100000, 1, 1))
        row["receipt"]["job_receipt"]["write_transfer_bytes"] = 20_000_000
        measurement.refresh_receipt_hash(row)
        self._resign(forged)
        errors = measurement.evaluate_measurement_receipts(forged, expected_run_id=RUN_ID)
        self.assertIn("H_SHAPE_LIMIT", errors)
        self.assertNotIn("AFFORDABILITY_LIMIT", errors)

    def test_total_io_operations_have_an_h_shape_gate(self):
        forged = copy.deepcopy(self.rows)
        row = next(envelope for envelope in forged
                   if (envelope["receipt"]["H"], envelope["receipt"]["D"],
                       envelope["receipt"]["F"]) == (100000, 1, 1))
        row["receipt"]["job_receipt"]["other_operations"] = 5000
        measurement.refresh_receipt_hash(row)
        self._resign(forged)
        errors = measurement.evaluate_measurement_receipts(forged, expected_run_id=RUN_ID)
        self.assertIn("H_SHAPE_LIMIT", errors)
        self.assertNotIn("AFFORDABILITY_LIMIT", errors)


class R12LedgerTests(unittest.TestCase):
    @staticmethod
    def _prepared():
        return measurement.CallLedger.prepare(
            "SCENARIO.SHARED", "BC", "B", "A" * 96, "B" * 64,
            "C" * 96, "IDEM.SHARED", "D" * 96)

    def test_empty_identity_is_rejected(self):
        with self.assertRaises(ValueError):
            measurement.CallLedger.prepare("", "BC", "B", "", "", "", "", "")

    def test_durable_transition_requires_exact_response_evidence(self):
        ledger = self._prepared().transition("DISPATCH_CONFIRMED")
        with self.assertRaises(ValueError):
            ledger.transition("RESPONSE_BYTES_FSYNCED")
        durable = ledger.transition(
            "RESPONSE_BYTES_FSYNCED", response_bytes=b'{"ok":true}',
            response_ref="RESPONSE.SHARED", provider_request_id="PROVIDER.SHARED",
            durability_receipt=measurement.durability_receipt_fixture(
                ledger, b'{"ok":true}'))
        self.assertEqual(durable.state, "RESPONSE_DURABLY_RECORDED")
        self.assertEqual(durable, measurement.CallLedger.recover(durable.serialize()))

    def test_corrupt_restart_is_rejected(self):
        raw = json.loads(self._prepared().serialize())
        raw["request_parameters_hash"] = "E" * 96
        with self.assertRaises(ValueError):
            measurement.CallLedger.recover(json.dumps(
                raw, sort_keys=True, separators=(",", ":")))

    def test_acceptance_ambiguity_is_terminal_missing_and_never_retryable(self):
        ledger = self._prepared().transition("DISPATCH_CONFIRMED").transition(
            "CONNECTION_LOST_AFTER_DISPATCH")
        self.assertEqual(ledger.terminal_missing_reason(), "ACCEPTANCE_AMBIGUOUS")
        self_authored = {
            "schema_id": "RouteAttestationV1",
            "route_contract_hash": ledger.route_contract_hash,
            "request_parameters_hash": ledger.request_parameters_hash,
            "idempotency_token": ledger.idempotency_token,
            "semantic_guarantee": "SAME_TOKEN_SAME_PARAMETERS_RETURNS_FIRST_RESULT",
        }
        self_authored["attestation_hash"] = measurement.sha384(self_authored)
        with self.assertRaises(ValueError):
            ledger.transition("RETRY_REQUESTED", route_attestation=self_authored)
        with self.assertRaises(ValueError):
            ledger.transition("RESPONSE_BYTES_FSYNCED", response_bytes=b'{"ok":true}',
                              response_ref="RESPONSE.SHARED",
                              provider_request_id="PROVIDER.SHARED")

    def test_durable_response_is_immutable(self):
        ledger = self._prepared().transition("DISPATCH_CONFIRMED")
        durable = ledger.transition(
            "RESPONSE_BYTES_FSYNCED", response_bytes=b'{"ok":true}',
            response_ref="RESPONSE.SHARED", provider_request_id="PROVIDER.SHARED",
            durability_receipt=measurement.durability_receipt_fixture(
                ledger, b'{"ok":true}'))
        with self.assertRaises(ValueError):
            durable.transition("RESPONSE_BYTES_FSYNCED", response_bytes=b'{"other":true}')


if __name__ == "__main__":
    unittest.main()
