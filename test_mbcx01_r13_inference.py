import copy
import json
import math
import unittest

import mbcx01_r13_inference as inference
import mbcx01_r13_measurement as measurement
import mbcx01_r13_packets as packets


class R13InferenceTests(unittest.TestCase):
    def test_i10_positive_episode_receipt_has_closed_machine_schema(self):
        with open("MBCX-01-INFERENCE-CONTRACT-v8.json", encoding="utf-8") as stream:
            schema = json.load(stream)["episode_receipt_schema"]
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(set(schema["$defs"]["episodeCallV2"]), {"oneOf"})
        self.assertFalse(schema["$defs"]["launchedEpisodeCallV2"]["additionalProperties"])
        self.assertFalse(schema["$defs"]["skippedEpisodeCallV2"]["additionalProperties"])
        self.assertFalse(schema["$defs"]["callLedgerV3"]["additionalProperties"])
        self.assertEqual(schema["properties"]["calls"]["minItems"], 6)
        self.assertEqual(schema["properties"]["calls"]["maxItems"], 6)

    def test_exact_missing_dp_matches_small_exhaustive_witnesses(self):
        base = [(1, 1)] * 380 + [(0, 0)] * 380
        for missing in ([0], [17, 401], [1, 144, 767]):
            observed = [pair for index, pair in enumerate(base + [(1, 0)] * 8)
                        if index not in set(missing)]
            dp = inference.missing_completion_bounds(observed, missing)
            exhaustive = inference.exhaustive_missing_completion_bounds(observed, missing)
            for left, right in zip(dp, exhaustive):
                self.assertAlmostEqual(left, right, places=12)

    def test_randomized_completion_property_spot_check_near_twenty_missing(self):
        missing = [3, 19, 47, 88, 121, 177, 204, 255, 300, 349,
                   402, 449, 500, 551, 603, 649, 700, 733, 750, 767]
        complete = [((index * 7) % 11 < 6, (index * 5) % 13 < 9)
                    for index in range(768)]
        complete = [(int(bc), int(om)) for bc, om in complete]
        observed = [pair for index, pair in enumerate(complete)
                    if index not in set(missing)]
        report = inference.randomized_completion_spot_check(
            observed, missing, samples=128, seed="MBCX01-R13-DP-SPOT-V1")
        self.assertEqual(report["missing_pairs"], 20)
        self.assertEqual(report["sampled_completions"], 128)
        self.assertEqual(report["claim_kind"],
                         "RANDOMIZED_PROPERTY_SPOT_CHECK_NOT_EXHAUSTIVE_PROOF")
        self.assertTrue(report["all_sampled_intervals_within_dp_hull"])
        self.assertEqual(report["violations"], 0)

    def test_randomized_spot_check_validates_sample_count(self):
        with self.assertRaises(ValueError):
            inference.randomized_completion_spot_check(
                [(1, 1)] * 748, list(range(748, 768)), samples=True)

    def test_dp_has_no_missing_count_ceiling(self):
        self.assertEqual(inference.missing_completion_bounds([], list(range(768))),
                         (-1.0, 1.0, 0.0, 1.0))

    def test_no_missing_preserves_complete_data_decision(self):
        pairs = [(1, 1)] * 768
        expected = inference.scientific_decision(*inference.paired_intervals(pairs))
        self.assertEqual(inference.decision_with_missingness(pairs, []), expected)

    def test_known_design_failure_precedes_transport(self):
        observed = [(1, 1)] * 760
        missing = list(range(760, 768))
        self.assertEqual(inference.decision_with_missingness(
            observed, missing, design_ok=False), "DESIGN_OR_IMPLEMENTATION_FAIL")

    def test_route_plan_reproduces_exact_tail_bounds(self):
        bounds = inference.route_qualification_bounds()
        self.assertAlmostEqual(bounds["bad_route_acceptance_max"],
                               0.049433329807588314, places=15)
        self.assertAlmostEqual(bounds["good_route_acceptance_min"],
                               0.9190668746549462, places=15)
        self.assertEqual(inference.smallest_reliability_plan(.02, .005, .05, .10),
                         (456, 4))

    def test_route_bound_requires_conditional_hazard_not_marginals(self):
        with self.assertRaises(ValueError):
            inference.route_acceptance_bound(
                trials=456, allowed_failures=4, probability=.02,
                direction="lower", assumption="marginal_probability")

    def test_registered_cells_remain_pointwise_planning_diagnostics(self):
        cells = inference.registered_planning_cells()
        self.assertTrue(all(cell["claim_kind"] == "DETERMINISTIC_PLANNING_FREQUENCY"
                            for cell in cells))
        diagnostic = next(cell for cell in cells if cell["id"] == "R10_COUNTEREXAMPLE")
        self.assertEqual([diagnostic[key] for key in ("p00", "p01", "p10", "p11")],
                         [0.0, 0.3, 0.1, 0.6])

    def test_binomial_cdf_validates_inputs(self):
        self.assertTrue(math.isclose(inference.binomial_cdf(4, 456, .02),
                                     0.049433329807588314,
                                     rel_tol=0, abs_tol=1e-15))
        with self.assertRaises(ValueError):
            inference.binomial_cdf(5, 4, .5)

    def test_i10_positive_ordered_partition_is_derived_from_episode_receipts(self):
        selected = measurement._pinned_retained_source()[0]
        ids = [row["scenario_id"] for row in selected]
        manifest = packets.manifest_for_retained_candidate(selected[0])
        state = packets._fixture_authoritative_state(manifest)
        authority = packets.cohort_authority_for_candidate(selected[0])
        bc = packets.build_scoring_fixture(
            manifest, "BC", authoritative_state=state, cohort_authority=authority)
        om = packets.build_scoring_fixture(
            manifest, "OM", authoritative_state=state, cohort_authority=authority)
        receipts = [measurement.episode_receipt_fixture(
            sid, index, missing_position=None if index == 0 else "BC.A0")
                    for index, sid in enumerate(ids)]
        receipts[0] = packets.build_complete_episode_receipt_for_scorers(
            bc, om, manifest["retained_position"])
        outcome = packets.build_scenario_outcome_receipt(
            manifest, bc, om, receipts[0], require_production_authority=False)
        partition = inference.derive_episode_partition(receipts, ids)
        self.assertEqual(partition["complete_ids"], [ids[0]])
        self.assertEqual(len(partition["missing_ids"]), 767)
        self.assertIsInstance(inference.ordered_decision_from_episode_receipts(
            [outcome], receipts, ids, require_production_authority=False), str)

    def test_i10_adversarial_same_scenario_outcome_from_another_episode_is_rejected(self):
        selected = measurement._pinned_retained_source()[0]
        ids = [row["scenario_id"] for row in selected]
        manifest = packets.manifest_for_retained_candidate(selected[0])
        state = packets._fixture_authoritative_state(manifest)
        authority = packets.cohort_authority_for_candidate(selected[0])
        bc = packets.build_scoring_fixture(
            manifest, "BC", authoritative_state=state, cohort_authority=authority)
        om = packets.build_scoring_fixture(
            manifest, "OM", authoritative_state=state, cohort_authority=authority)
        episodes = [measurement.episode_receipt_fixture(
            sid, index, missing_position=None if index == 0 else "BC.A0")
                    for index, sid in enumerate(ids)]
        episodes[0] = packets.build_complete_episode_receipt_for_scorers(
            bc, om, manifest["retained_position"])
        alternate = copy.deepcopy(bc)
        alternate["a0_call_record"]["response_ref"] = "RESPONSE.BC.A0.ALTERNATE"
        call = alternate["a0_call_record"]
        transaction = call["durability_receipt"]["transaction_id"]
        call["durability_receipt"] = packets.make_durability_receipt(call, transaction)
        call["call_record_hash"] = packets.hash_without(call, "call_record_hash")
        alternate_episode = packets.build_complete_episode_receipt_for_scorers(
            alternate, om, manifest["retained_position"])
        alternate_outcome = packets.build_scenario_outcome_receipt(
            manifest, alternate, om, alternate_episode,
            require_production_authority=False)
        with self.assertRaisesRegex(ValueError, "SCENARIO_OUTCOME_AUTHORITY_INVALID"):
            inference.ordered_decision_from_episode_receipts(
                [alternate_outcome], episodes, ids,
                require_production_authority=False)

    def test_i10_adversarial_caller_cannot_omit_ambiguity_or_supply_outcome(self):
        ids = sorted([f"SCENARIO.{index:03d}" for index in range(768)],
                     key=lambda value: __import__("hashlib").sha256(value.encode()).digest())
        receipts = [measurement.episode_receipt_fixture(
            sid, index, missing_position="OM.B" if index == 17 else "BC.A0")
                    for index, sid in enumerate(ids)]
        rows = [{"scenario_id": sid, "bc": 1, "om": 1} for sid in ids]
        with self.assertRaisesRegex(ValueError, "SCENARIO_OUTCOME_AUTHORITY_INVALID"):
            inference.ordered_decision_from_episode_receipts(rows, receipts, ids)
        partition = inference.derive_episode_partition(receipts, ids)
        self.assertEqual(partition["complete_ids"], [])
        self.assertEqual(len(partition["missing_ids"]), 768)
        self.assertIsInstance(inference.ordered_decision_from_episode_receipts(
            [], receipts, ids, require_production_authority=False), str)

    def test_i10_adversarial_receipt_omission_or_rehash_substitution_fails(self):
        ids = sorted([f"SCENARIO.{index:03d}" for index in range(768)],
                     key=lambda value: __import__("hashlib").sha256(value.encode()).digest())
        receipts = [measurement.episode_receipt_fixture(sid, index)
                    for index, sid in enumerate(ids)]
        with self.assertRaisesRegex(ValueError, "EPISODE_PARTITION_MISMATCH"):
            inference.derive_episode_partition(receipts[:-1], ids)
        forged = copy.deepcopy(receipts)
        forged[3]["calls"][0]["ledger_snapshot"]["scenario_id"] = "SCENARIO.OTHER"
        with self.assertRaisesRegex(ValueError, "EPISODE_PARTITION_MISMATCH"):
            inference.derive_episode_partition(forged, ids)


if __name__ == "__main__":
    unittest.main()
