from __future__ import annotations

import copy
import inspect
import json
import subprocess
import unittest

import mbcx01_r13_measurement as measurement


RUN_ID = "RUN.R13.NO-PAID.TEST"
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


class R13CohortTests(unittest.TestCase):
    def test_cut_domain_is_contract_driven(self):
        cuts = ["CUT.A", "CUT.B", "CUT.C"]
        with open("MBCX-01-MEASUREMENT-CONTRACT-v7.json", encoding="utf-8") as stream:
            domain = json.load(stream)["cohort"]["one_cut_hash_domain"]
        chosen = measurement.choose_one_cut("SCENARIO.000", cuts, domain)
        self.assertEqual(chosen, measurement.choose_one_cut("SCENARIO.000", cuts, domain))
        self.assertTrue(any(
            measurement.choose_one_cut(f"SCENARIO.{index}", cuts, domain)
            != measurement.choose_one_cut(f"SCENARIO.{index}", cuts, "ALTERNATE.DOMAIN")
            for index in range(32)))
        self.assertEqual(list(inspect.signature(measurement.select_cohort).parameters),
                         ["candidates", "provenance"])

    def test_generator_digest_is_the_pinned_generator_artifact_digest(self):
        _, provenance = measurement.synthetic_candidates_r13()
        spec, expected = measurement._generator_spec()
        self.assertEqual(provenance["generator_id"], spec["generator_id"])
        self.assertEqual(provenance["generator_digest"], expected)

    def test_source_provenance_rejects_motif_and_action_substitution(self):
        candidates, provenance = measurement.synthetic_candidates_r13()
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
        candidates, provenance = measurement.synthetic_candidates_r13()
        selected = measurement.select_cohort(candidates, provenance)
        self.assertEqual(len(selected), 768)
        self.assertEqual({sum(row["motif"] == motif for row in selected)
                          for motif in measurement.MOTIFS}, {128})


class R13SignedMeasurementTests(unittest.TestCase):
    def setUp(self):
        self.rows = sign_no_paid_test_envelopes(
            measurement.baseline_receipt_rows(run_id=RUN_ID))

    def _resign(self, rows):
        return sign_no_paid_test_envelopes(rows)

    def test_signed_no_paid_fixture_verifies_but_cannot_establish_physical_pass(self):
        self.assertEqual(measurement.evaluate_measurement_receipts(
            self.rows, expected_run_id=RUN_ID), ["PHYSICAL_HARNESS_UNAVAILABLE"])

    def test_contract_publishes_a_closed_nested_envelope_schema(self):
        with open("MBCX-01-MEASUREMENT-CONTRACT-v7.json", encoding="utf-8") as stream:
            schema = json.load(stream)["signed_measurement_envelope_schema"]
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertFalse(schema["additionalProperties"])
        self.assertFalse(schema["$defs"]["measurementReceiptV3"]["additionalProperties"])
        self.assertFalse(schema["$defs"]["jobReceiptV3"]["additionalProperties"])
        for definition in ("physicalEvidenceV1", "processMembershipEvidenceV1",
                           "jobQueryEvidenceV1", "completionEvidenceV1",
                           "externalEnforcementEvidenceV1", "environmentEvidenceV1"):
            self.assertFalse(schema["$defs"][definition]["additionalProperties"], definition)
        self.assertEqual(set(schema["required"]), set(schema["properties"]))

    def test_trust_root_is_separately_loaded_closed_and_fixture_only(self):
        roots = measurement._load_trust_roots()
        self.assertEqual(set(roots), {measurement.TEST_KEY_ID})
        self.assertTrue(roots[measurement.TEST_KEY_ID]["fixture_only"])
        self.assertEqual(roots[measurement.TEST_KEY_ID]["authorized_producer_role"],
                         "NO_PAID_TEST_HARNESS")
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
        replay[0]["run_id"] = "RUN.R13.REPLAY"
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
        row["receipt"]["job_receipt"]["evidence"]["job_queries"] = \
            measurement._query_evidence(row["receipt"]["job_receipt"])
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
        row["receipt"]["job_receipt"]["evidence"]["job_queries"] = \
            measurement._query_evidence(row["receipt"]["job_receipt"])
        measurement.refresh_receipt_hash(row)
        self._resign(forged)
        errors = measurement.evaluate_measurement_receipts(forged, expected_run_id=RUN_ID)
        self.assertIn("H_SHAPE_LIMIT", errors)
        self.assertNotIn("AFFORDABILITY_LIMIT", errors)

    def test_i12_positive_all_promised_gates_accept_bounded_fixture(self):
        self.assertEqual(measurement.evaluate_measurement_receipts(
            self.rows, expected_run_id=RUN_ID), ["PHYSICAL_HARNESS_UNAVAILABLE"])

    def test_i12_adversarial_aggregate_cpu_user_plus_kernel_h_shape_is_executed(self):
        forged = copy.deepcopy(self.rows)
        row = next(envelope for envelope in forged
                   if (envelope["receipt"]["H"], envelope["receipt"]["D"],
                       envelope["receipt"]["F"]) == (100000, 1, 1))
        row["receipt"]["job_receipt"]["user_time_ns"] = 80_000_000
        row["receipt"]["job_receipt"]["evidence"]["job_queries"] = \
            measurement._query_evidence(row["receipt"]["job_receipt"])
        measurement.refresh_receipt_hash(row)
        self._resign(forged)
        errors = measurement.evaluate_measurement_receipts(forged, expected_run_id=RUN_ID)
        self.assertIn("H_SHAPE_LIMIT", errors)
        self.assertNotIn("AFFORDABILITY_LIMIT", errors)

    def test_i11_positive_complete_nested_evidence_is_representable_and_checked(self):
        evidence = self.rows[0]["receipt"]["job_receipt"]["evidence"]
        self.assertEqual(evidence["process_membership"]["processes"][0][
            "process_start_key"], "0000000000000001")
        self.assertEqual(evidence["job_queries"]["basic_and_io"][
            "information_class"], "JobObjectBasicAndIoAccountingInformation")
        self.assertEqual(evidence["job_queries"]["extended_limit"][
            "structure_size_bytes"], 144)
        self.assertEqual(measurement.evaluate_measurement_receipts(
            self.rows, expected_run_id=RUN_ID), ["PHYSICAL_HARNESS_UNAVAILABLE"])

    def test_i11_adversarial_omitted_or_replaced_signed_evidence_is_fatal(self):
        cases = []
        omitted = copy.deepcopy(self.rows)
        del omitted[0]["receipt"]["job_receipt"]["evidence"]["completion"]
        cases.append((omitted, "PHYSICAL_EVIDENCE_INCOMPLETE"))
        replaced = copy.deepcopy(self.rows)
        replaced[0]["receipt"]["job_receipt"]["evidence"][
            "process_membership"]["processes"][0]["process_start_key"] = "0000000000000002"
        cases.append((replaced, "PROCESS_MEMBERSHIP_INVALID"))
        for rows, expected in cases:
            measurement.refresh_receipt_hash(rows[0])
            self._resign(rows)
            self.assertIn(expected, measurement.evaluate_measurement_receipts(
                rows, expected_run_id=RUN_ID))

    def test_i11_adversarial_raw_cswitch_delta_is_recomputed(self):
        forged = copy.deepcopy(self.rows)
        forged[0]["receipt"]["job_receipt"]["evidence"]["trace"][
            "cswitch_observations"][1]["delta_from_previous"] += 1
        measurement.refresh_receipt_hash(forged[0]); self._resign(forged)
        self.assertIn("INSTRUCTION_ACCOUNTING_INCOMPLETE",
                      measurement.evaluate_measurement_receipts(
                          forged, expected_run_id=RUN_ID))

    def test_i12_job_query_bytes_are_fatal_but_completion_messages_are_diagnostic(self):
        forged = copy.deepcopy(self.rows)
        query = forged[0]["receipt"]["job_receipt"]["evidence"][
            "job_queries"]["basic_and_io"]
        query["raw_bytes_sha384"] = "F" * 96
        measurement.refresh_receipt_hash(forged[0]); self._resign(forged)
        self.assertIn("JOB_QUERY_EVIDENCE_INVALID",
                      measurement.evaluate_measurement_receipts(
                          forged, expected_run_id=RUN_ID))
        forged = copy.deepcopy(self.rows)
        completion = forged[0]["receipt"]["job_receipt"]["evidence"]["completion"]
        completion["active_zero_message_seen"] = False
        completion["new_process_messages"] = 0
        completion["exit_process_messages"] = 0
        completion["diagnostic_messages_complete"] = False
        measurement.refresh_receipt_hash(forged[0]); self._resign(forged)
        self.assertEqual(measurement.evaluate_measurement_receipts(
            forged, expected_run_id=RUN_ID), ["PHYSICAL_HARNESS_UNAVAILABLE"])

    def test_i12_windows_job_basic_accounting_uses_four_dwords(self):
        import base64
        import struct
        query = self.rows[0]["receipt"]["job_receipt"]["evidence"][
            "job_queries"]["basic_and_io"]
        raw = base64.b64decode(query["raw_bytes_b64"])
        self.assertEqual(len(raw), 96)
        values = struct.unpack("<qqqqIIIIQQQQQQ", raw)
        self.assertEqual(values[4:8], (0, 1, 0, 0))

    def test_i12_normal_exit_does_not_require_a_limit_violation_termination(self):
        job = self.rows[0]["receipt"]["job_receipt"]
        self.assertEqual(job["total_processes"], 1)
        self.assertEqual(job["active_processes_at_final_query"], 0)
        self.assertEqual(job["total_terminated_processes"], 0)
        self.assertEqual(job["evidence"]["process_membership"]["processes"][0][
            "terminal_status"], "EXITED")
        self.assertEqual(measurement.evaluate_measurement_receipts(
            self.rows, expected_run_id=RUN_ID), ["PHYSICAL_HARNESS_UNAVAILABLE"])

    def test_i12_adversarial_grid_identity_mismatch_is_fatal(self):
        forged = copy.deepcopy(self.rows)
        forged[0]["receipt"]["job_receipt"]["evidence"]["harness_identity"][
            "harness_configuration_digest"] = "F" * 96
        measurement.refresh_receipt_hash(forged[0]); self._resign(forged)
        self.assertIn("GRID_IDENTITY_MISMATCH",
                      measurement.evaluate_measurement_receipts(
                          forged, expected_run_id=RUN_ID))

    def test_i12_adversarial_environment_and_external_enforcement_are_fatal(self):
        forged = copy.deepcopy(self.rows)
        env = forged[0]["receipt"]["job_receipt"]["evidence"]["environment"]
        env["nested_virtualization"] = True
        measurement.refresh_receipt_hash(forged[0]); self._resign(forged)
        self.assertIn("UNSUPPORTED_MEASUREMENT_ENVIRONMENT",
                      measurement.evaluate_measurement_receipts(
                          forged, expected_run_id=RUN_ID))
        forged = copy.deepcopy(self.rows)
        forged[0]["receipt"]["job_receipt"]["evidence"][
            "external_enforcement"]["deny_outbound_network"] = False
        measurement.refresh_receipt_hash(forged[0]); self._resign(forged)
        self.assertIn("EXTERNAL_WORK_UNMEASURED",
                      measurement.evaluate_measurement_receipts(
                          forged, expected_run_id=RUN_ID))

    def test_i13_positive_fixture_root_binds_role_policy_subject_and_environment(self):
        row = self.rows[0]
        root = measurement._load_trust_roots()[row["signing_key_id"]]
        self.assertEqual(row["producer_role"], root["authorized_producer_role"])
        self.assertEqual(row["trust_policy_digest"], root["trust_policy_digest"])
        self.assertEqual(row["subject_digest"], measurement.sha384(row["receipt"]))
        self.assertEqual(row["environment_digest"], row["receipt"]["job_receipt"][
            "evidence"]["harness_identity"]["host_environment_digest"])

    def test_i13_adversarial_manifest_edit_cannot_activate_production_authority(self):
        document = measurement._load_json("MBCX-01-R13-MEASUREMENT-TRUST-ROOTS.json")
        forged = copy.deepcopy(document)
        forged["production_ready"] = True
        with self.assertRaisesRegex(ValueError, "production authority unavailable"):
            measurement._validate_trust_root_document(forged)
        self.assertEqual(document["retirement_policy"]["fail_loud_sentinel"],
                         "PHYSICAL_HARNESS_UNAVAILABLE")
        self.assertNotEqual(document["retirement_policy"]["signer_custodian_role"],
                            document["retirement_policy"]["trust_root_editor_role"])

    # --- AMENDMENT-2 (2026-08-15): a thread lives in ONE process incarnation,
    # --- and a thread id is unique only within its own lifetime ---------------

    def _evidence(self):
        job = copy.deepcopy(self.rows[0]["receipt"]["job_receipt"])
        return job, job["evidence"]

    def test_i11_adversarial_thread_lifetime_outside_its_process_is_refused(self):
        """A thread must NEST inside the incarnation whose start key it claims.

        The validator checked that (process_id, process_start_key) is a member
        pair and that the thread's own interval is monotonic — never that the
        interval lies INSIDE the process's. A PID is reused, so a thread
        observed while that incarnation was not alive is a different process's
        thread, and admitting it sums a stranger's retired instructions into a
        member's total. Both directions of the escape are refused.
        """
        for label, started, ended in (("starts before the process", 0, 29),
                                      ("ends after the process", 2, 31)):
            with self.subTest(case=label):
                job, evidence = self._evidence()
                process = evidence["process_membership"]["processes"][0]
                self.assertEqual((process["started_qpc"], process["ended_qpc"]),
                                 (1, 30))
                lifetime = evidence["trace"]["thread_lifetimes"][0]
                lifetime["started_qpc"] = started
                lifetime["ended_qpc"] = ended
                self.assertIn("INSTRUCTION_ACCOUNTING_INCOMPLETE",
                              measurement._validate_physical_evidence(job, evidence))
        # CONTROL — the untouched fixture nests, and still validates clean.
        job, evidence = self._evidence()
        self.assertEqual(measurement._validate_physical_evidence(job, evidence), set())

    def test_i11_positive_a_reused_thread_id_carries_one_lifetime_per_use(self):
        """Windows reuses a TID after the thread exits; the validator must read it.

        Keying the thread roster by TID alone made a legal capture unadmissible
        — the second lifetime was dropped as a duplicate and the whole receipt
        failed INSTRUCTION_ACCOUNTING_INCOMPLETE, which REFUSES RIGHT EVIDENCE.
        Two disjoint lifetimes for one TID are admitted, and each observation is
        attributed to the lifetime whose interval CONTAINS its QPC.
        """
        job, evidence = self._evidence()
        threads = evidence["trace"]["thread_lifetimes"]
        first = threads[0]
        first["started_qpc"], first["ended_qpc"] = 2, 12
        threads.append(dict(first, started_qpc=15, ended_qpc=29))
        observations = evidence["trace"]["cswitch_observations"]
        self.assertEqual([row["qpc"] for row in observations], [10, 20])
        self.assertEqual(len({row["old_thread_id"] for row in observations}), 1)
        self.assertEqual(measurement._validate_physical_evidence(job, evidence), set())
        # An observation in the GAP between the two lives is attributable to
        # neither, and is refused rather than joined to the nearer one.
        observations[1]["qpc"] = 13
        self.assertIn("INSTRUCTION_ACCOUNTING_INCOMPLETE",
                      measurement._validate_physical_evidence(job, evidence))

    def test_i11_adversarial_overlapping_lifetimes_for_one_thread_id_are_refused(self):
        """Reuse is sequential: one TID is never alive twice at the same instant.

        If it were, an observation inside the overlap could be attributed to
        either row, and the join would stop being a function. Overlapping and
        merely TOUCHING intervals are both refused, so containment resolves to
        exactly one lifetime.
        """
        for label, second in (("overlapping", (10, 29)),
                              ("touching at one instant", (12, 29))):
            with self.subTest(case=label):
                job, evidence = self._evidence()
                threads = evidence["trace"]["thread_lifetimes"]
                first = threads[0]
                first["started_qpc"], first["ended_qpc"] = 2, 12
                threads.append(dict(first, started_qpc=second[0],
                                    ended_qpc=second[1]))
                self.assertIn("INSTRUCTION_ACCOUNTING_INCOMPLETE",
                              measurement._validate_physical_evidence(job, evidence))

    # ------------------------------------------------------------------
    # AMENDMENT-3 (2026-08-16): the first member interval per processor is
    # counted from a predecessor baseline instead of a hard-coded zero.
    # Pre-amendment RED, driver-banked on hash-proven bytes (blob eb795387…):
    # the undercounting shape below validated with ZERO errors — aggregate
    # 100 accepted where the stream proved 1,000,100, twice the closure
    # architecture's 500,000 boundedness threshold.
    # ------------------------------------------------------------------

    def _seat3_stream(self, job, evidence):
        """The r6 NO-GO shape: predecessor at raw 100 (excluded as foreign),
        first member switch-out at raw 1,000,100, second at 1,000,200."""
        trace = evidence["trace"]
        observations = trace["cswitch_observations"]
        observations[0]["counter_value"] = 1000100
        observations[1]["counter_value"] = 1000200
        observations[1]["delta_from_previous"] = 100
        return trace, observations

    def test_i12_adversarial_a_baselineless_undercounting_trace_is_refused(self):
        """The pre-amendment acceptance is the defect; its shape now refuses.

        RED pre-amendment: this exact receipt — no baseline field, first delta
        zero, aggregate 100 — returned an EMPTY error set while the stream
        proved 1,000,100 instructions of member work. The exact TRACE_KEYS set
        now refuses the shape outright, which is also the migration story: no
        pre-amendment receipt exists (the harness has never run live).
        """
        job, evidence = self._evidence()
        trace, observations = self._seat3_stream(job, evidence)
        del trace["cswitch_first_member_baselines"]
        observations[0]["delta_from_previous"] = 0
        trace["aggregate_retired_instructions"] = 100
        job["retired_instructions"] = 100
        self.assertIn("INSTRUCTION_ACCOUNTING_INCOMPLETE",
                      measurement._validate_physical_evidence(job, evidence))

    def test_i12_positive_the_first_member_interval_is_counted_from_the_baseline(self):
        """With the predecessor baseline the truthful receipt is accepted.

        RED pre-amendment (unknown trace key refused the whole shape); GREEN
        after: delta = counter_value − baseline = 1,000,000 on the first
        observation, aggregate 1,000,100.
        """
        job, evidence = self._evidence()
        trace, observations = self._seat3_stream(job, evidence)
        trace["cswitch_first_member_baselines"] = [
            {"processor": 0, "counter_value": 100}]
        observations[0]["delta_from_previous"] = 1000000
        trace["aggregate_retired_instructions"] = 1000100
        job["retired_instructions"] = 1000100
        self.assertEqual(measurement._validate_physical_evidence(job, evidence),
                         set())

    def test_i12_adversarial_an_undercount_cannot_hide_behind_a_present_baseline(self):
        """GUARD (recorded as such): trivially green pre-amendment via the key
        refusal; its discrimination begins now — a baseline on the record with
        a zero first delta is a delta mismatch, refused by name."""
        job, evidence = self._evidence()
        trace, observations = self._seat3_stream(job, evidence)
        trace["cswitch_first_member_baselines"] = [
            {"processor": 0, "counter_value": 100}]
        observations[0]["delta_from_previous"] = 0
        trace["aggregate_retired_instructions"] = 100
        job["retired_instructions"] = 100
        self.assertIn("INSTRUCTION_ACCOUNTING_INCOMPLETE",
                      measurement._validate_physical_evidence(job, evidence))

    def test_i12_positive_capture_start_stays_a_declared_zero_truncation(self):
        """A capture-start processor's row carries its FIRST record's own
        counter (r7 totality), so the first delta stays zero — the original,
        small-by-construction trace-start rule, now expressed as an explicit
        observation instead of an absence. RED pre-amendment (unknown key)."""
        job, evidence = self._evidence()
        self.assertEqual(evidence["trace"]["cswitch_first_member_baselines"],
                         [{"processor": 0, "counter_value": 100}])
        self.assertEqual(
            evidence["trace"]["cswitch_observations"][0]["counter_value"], 100)
        self.assertEqual(
            evidence["trace"]["cswitch_observations"][0]["delta_from_previous"], 0)
        self.assertEqual(measurement._validate_physical_evidence(job, evidence),
                         set())

    def test_i12_adversarial_an_empty_baseline_set_beside_observations_is_refused(self):
        """The r7 totality rule: baselined processors must EQUAL observed
        processors. An empty list beside observations is the forgotten-field
        shape — the one that silently reproduced the pre-amendment undercount
        (three seats convergent; SEAT2 pushed it through full production
        admission wrong by 1,000,000). RED pre-r7-fold: the ⊆ rule accepted it."""
        job, evidence = self._evidence()
        evidence["trace"]["cswitch_first_member_baselines"] = []
        self.assertIn("INSTRUCTION_ACCOUNTING_INCOMPLETE",
                      measurement._validate_physical_evidence(job, evidence))

    def test_i12_adversarial_malformed_baselines_are_refused_by_shape(self):
        """A baseline above the first counter (negative interval), a baseline
        for a processor with no observations, a duplicate processor row and a
        wrong-shaped row each refuse — never a silent zero."""
        cases = (
            [{"processor": 0, "counter_value": 10 ** 9}],
            [{"processor": 7, "counter_value": 5}],
            [{"processor": 0, "counter_value": 1},
             {"processor": 0, "counter_value": 2}],
            [{"processor": 0}],
            [{"processor": 0, "counter_value": -1}],
            [{"processor": True, "counter_value": 1}],
        )
        for rows in cases:
            with self.subTest(rows=rows):
                job, evidence = self._evidence()
                evidence["trace"]["cswitch_first_member_baselines"] = rows
                self.assertIn(
                    "INSTRUCTION_ACCOUNTING_INCOMPLETE",
                    measurement._validate_physical_evidence(job, evidence))


class R13LedgerTests(unittest.TestCase):
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

    @staticmethod
    def _durable(condition="BC", node="B", scenario="SCENARIO.SHARED"):
        ledger = measurement.CallLedger.prepare(
            scenario, condition, node, "A" * 96, "B" * 64, "C" * 96,
            f"IDEM.{scenario}.{condition}.{node}", "D" * 96,
            handoff_id=f"HANDOFF.{scenario}.{condition}")
        dispatched = ledger.transition("DISPATCH_CONFIRMED")
        raw = b'{"ok":true}'
        return dispatched.transition(
            "RESPONSE_BYTES_FSYNCED", response_bytes=raw,
            response_ref=f"RESPONSE.{scenario}.{condition}.{node}",
            provider_request_id=f"PROVIDER.{scenario}.{condition}.{node}",
            durability_receipt=measurement.durability_receipt_fixture(
                dispatched, raw, f"RESPONSE.{scenario}.{condition}.{node}",
                f"PROVIDER.{scenario}.{condition}.{node}"))

    @staticmethod
    def _response(ledger):
        return {**measurement._ledger_identity(ledger),
                "raw_response_utf8": json.loads(json.dumps(
                    __import__("base64").b64decode(ledger.raw_response_b64).decode("utf-8"))),
                "raw_response_hash": ledger.raw_response_hash,
                "response_ref": ledger.response_ref,
                "provider_request_id": ledger.provider_request_id,
                "durability_receipt": copy.deepcopy(ledger.durability_receipt)}

    def test_i05_positive_b_response_and_durable_ledger_are_exactly_bound(self):
        ledger = self._durable()
        response = self._response(ledger)
        binding = measurement.bind_durable_b_response(ledger, response)
        self.assertEqual(measurement.validate_b_response_ledger_binding(
            binding, response), [])
        self.assertEqual(binding["ledger_snapshot"]["handoff_id"],
                         response["handoff_id"])

    def test_i05_adversarial_cross_scenario_or_node_replay_fails(self):
        ledger = self._durable()
        response = self._response(ledger)
        binding = measurement.bind_durable_b_response(ledger, response)
        for field, replacement in (("scenario_id", "SCENARIO.OTHER"), ("node", "A0"),
                                   ("handoff_id", "HANDOFF.OTHER.BC"),
                                   ("response_ref", "RESPONSE.OTHER")):
            forged = copy.deepcopy(response); forged[field] = replacement
            self.assertIn("B_LEDGER_MISMATCH",
                          measurement.validate_b_response_ledger_binding(binding, forged), field)

    def test_i10_positive_episode_receipt_derives_complete_partition(self):
        ledgers = [self._durable(condition, node) for condition in ("BC", "OM")
                   for node in ("A0", "B", "A1")]
        receipt = measurement.build_episode_receipt("SCENARIO.SHARED", 7, ledgers)
        self.assertEqual(receipt["terminal_class"], "COMPLETE_PAIR")
        self.assertEqual(measurement.validate_episode_receipt(
            receipt, "SCENARIO.SHARED", 7), [])

    def test_i10_adversarial_ambiguity_is_terminal_whole_pair_missing(self):
        receipt = measurement.episode_receipt_fixture(
            "SCENARIO.SHARED", 7, missing_position="OM.B")
        self.assertEqual(receipt["terminal_class"], "WHOLE_PAIR_MISSING")
        self.assertEqual(receipt["calls"][5]["launch_status"],
                         "NOT_LAUNCHED_UPSTREAM_TERMINAL")
        self.assertEqual(receipt["calls"][5]["upstream_terminal_position"], "OM.B")
        forged = copy.deepcopy(receipt); forged["terminal_class"] = "COMPLETE_PAIR"
        forged["episode_hash"] = measurement.sha384(
            {k: v for k, v in forged.items() if k != "episode_hash"})
        self.assertIn("EPISODE_PARTITION_MISMATCH",
                      measurement.validate_episode_receipt(forged, "SCENARIO.SHARED", 7))


class R13EngineeringSelectionTests(unittest.TestCase):
    @staticmethod
    def _evidence(candidate):
        rows = sign_no_paid_test_envelopes(measurement.baseline_receipt_rows(candidate))
        exactness = measurement.fixture_carrier_exactness_receipt(candidate, rows)
        return measurement.derive_engineering_candidate_evidence(
            exactness, rows, expected_run_id=RUN_ID,
            require_production_authority=False)

    def test_i16_positive_hard_gates_precede_complete_pareto_set(self):
        reports = [self._evidence("CANDIDATE.A"), self._evidence("CANDIDATE.B")]
        result = measurement.engineering_selection(
            reports, require_production_authority=False)
        self.assertEqual(result["nondominated_candidate_ids"],
                         ["CANDIDATE.A", "CANDIDATE.B"])
        self.assertEqual(result["status"], "OWNER_SELECTION_REQUIRED")
        self.assertEqual(result["evidence_claim"], "NO_OWNER_PREFERENCE_IN_EVIDENCE")

    def test_i16_adversarial_owner_preference_or_dominated_preference_is_rejected(self):
        report = self._evidence("CANDIDATE.A")
        report["preferred"] = True
        with self.assertRaisesRegex(ValueError, "ENGINEERING_SELECTION_INVALID"):
            measurement.engineering_selection(
                [report], require_production_authority=False)

    def test_i16_adversarial_caller_metric_substitution_is_rejected(self):
        report = self._evidence("CANDIDATE.A")
        report["worst_cell_metrics"]["retired_instructions"] = 1
        report["evidence_hash"] = measurement.sha384(
            {key: value for key, value in report.items() if key != "evidence_hash"})
        with self.assertRaisesRegex(ValueError, "ENGINEERING_SELECTION_INVALID"):
            measurement.engineering_selection(
                [report], require_production_authority=False)

    def test_i16_adversarial_self_authored_exactness_pass_has_no_authority(self):
        rows = sign_no_paid_test_envelopes(
            measurement.baseline_receipt_rows("CANDIDATE.A"))
        exactness = measurement.fixture_carrier_exactness_receipt("CANDIDATE.A", rows)
        forged = copy.deepcopy(exactness)
        forged["suite_artifact_hash"] = "E" * 96
        forged["witness_set_hash"] = "F" * 96
        forged["receipt_hash"] = measurement.sha384(
            {key: value for key, value in forged.items() if key != "receipt_hash"})
        with self.assertRaisesRegex(ValueError, "ENGINEERING_SELECTION_INVALID"):
            measurement.derive_engineering_candidate_evidence(
                forged, rows, expected_run_id=RUN_ID,
                require_production_authority=False)
        promoted = copy.deepcopy(exactness)
        promoted["authority_mode"] = "PRODUCTION"
        promoted["receipt_hash"] = measurement.sha384(
            {key: value for key, value in promoted.items() if key != "receipt_hash"})
        with self.assertRaisesRegex(ValueError,
                                    "CARRIER_EXACTNESS_AUTHORITY_UNAVAILABLE"):
            measurement.derive_engineering_candidate_evidence(
                promoted, rows, expected_run_id=RUN_ID,
                require_production_authority=True)

    def test_i16_adversarial_exactness_receipt_cannot_replay_across_builds(self):
        rows = sign_no_paid_test_envelopes(
            measurement.baseline_receipt_rows("CANDIDATE.A"))
        exactness = measurement.fixture_carrier_exactness_receipt("CANDIDATE.A", rows)
        rebuilt = copy.deepcopy(rows)
        for envelope in rebuilt:
            envelope["receipt"]["candidate_artifact_digest"] = "F" * 96
            envelope["receipt"]["job_receipt"]["evidence"]["harness_identity"][
                "harness_build_digest"] = "E" * 96
        sign_no_paid_test_envelopes(rebuilt)
        with self.assertRaisesRegex(ValueError, "ENGINEERING_SELECTION_INVALID"):
            measurement.derive_engineering_candidate_evidence(
                exactness, rebuilt, expected_run_id=RUN_ID,
                require_production_authority=False)


if __name__ == "__main__":
    unittest.main()
