import math
import unittest

import mbcx01_r11_inference as inference


class R11InferenceTests(unittest.TestCase):
    def test_exact_missing_dp_matches_small_exhaustive_witnesses(self):
        base = [(1, 1)] * 380 + [(0, 0)] * 380
        for missing in ([0], [17, 401], [1, 144, 767]):
            observed = [pair for index, pair in enumerate(base + [(1, 0)] * 8)
                        if index not in set(missing)]
            dp = inference.missing_completion_bounds(observed, missing)
            exhaustive = inference.exhaustive_missing_completion_bounds(observed, missing)
            for left, right in zip(dp, exhaustive):
                self.assertAlmostEqual(left, right, places=12)

    def test_dp_has_no_missing_count_ceiling(self):
        bounds = inference.missing_completion_bounds([], list(range(768)))
        self.assertEqual(bounds, (-1.0, 1.0, 0.0, 1.0))

    def test_no_missing_preserves_complete_data_decision(self):
        pairs = [(1, 1)] * 768
        expected = inference.scientific_decision(*inference.paired_intervals(pairs))
        self.assertEqual(inference.decision_with_missingness(pairs, []), expected)

    def test_known_design_failure_precedes_transport(self):
        observed = [(1, 1)] * 760
        missing = list(range(760, 768))
        self.assertEqual(
            inference.decision_with_missingness(observed, missing, design_ok=False),
            "DESIGN_OR_IMPLEMENTATION_FAIL",
        )
        for poisoned in ("NO", 1, object()):
            with self.assertRaises(ValueError):
                inference.decision_with_missingness(observed, missing, design_ok=poisoned)

    def test_route_plan_reproduces_exact_tail_bounds(self):
        bounds = inference.route_qualification_bounds()
        self.assertAlmostEqual(bounds["bad_route_acceptance_max"],
                               0.049433329807588314, places=15)
        self.assertAlmostEqual(bounds["good_route_acceptance_min"],
                               0.9190668746549462, places=15)
        self.assertAlmostEqual(bounds["good_route_rejection_max"],
                               0.08093312534505381, places=15)
        self.assertEqual(inference.smallest_reliability_plan(.02, .005, .05, .10),
                         (456, 4))

    def test_route_bound_requires_conditional_hazard_not_marginals(self):
        with self.assertRaises(ValueError):
            inference.route_acceptance_bound(
                trials=456, allowed_failures=4, probability=.02,
                direction="lower", assumption="marginal_probability",
            )

    def test_registered_cells_are_pointwise_planning_diagnostics(self):
        cells = inference.registered_planning_cells()
        self.assertGreaterEqual(len(cells), 4)
        self.assertTrue(all(cell["claim_kind"] == "DETERMINISTIC_PLANNING_FREQUENCY"
                            for cell in cells))
        diagnostic = next(cell for cell in cells if cell["id"] == "R10_COUNTEREXAMPLE")
        self.assertEqual(
            [diagnostic[key] for key in ("p00", "p01", "p10", "p11")],
            [0.0, 0.3, 0.1, 0.6],
        )
        self.assertEqual(diagnostic["expected_branch"], "MODEL_INTERFACE_FAIL")

    def test_counter_stream_planning_simulation_is_reproducible_and_not_evidence(self):
        first = inference.simulate_registered_cells(replicates=16, seed="R11-TEST")
        second = inference.simulate_registered_cells(replicates=16, seed="R11-TEST")
        self.assertEqual(first, second)
        self.assertFalse(first["experiment_evidence"])
        self.assertEqual(first["claim_kind"], "DETERMINISTIC_PLANNING_FREQUENCY")
        self.assertTrue(all(sum(cell["branch_counts"].values()) == 16
                            for cell in first["cells"]))

    def test_binomial_cdf_validates_inputs(self):
        self.assertTrue(math.isclose(inference.binomial_cdf(4, 456, .02),
                                     0.049433329807588314, rel_tol=0, abs_tol=1e-15))
        with self.assertRaises(ValueError):
            inference.binomial_cdf(5, 4, .5)

    def test_pairs_reject_booleans_and_ordered_records_bind_manifest(self):
        with self.assertRaises(ValueError):
            inference.paired_intervals([(True, True)] * 768)
        ids = [f"SCENARIO.{index:03d}" for index in range(768)]
        ids.sort(key=lambda value: inference.hashlib.sha256(value.encode("utf-8")).digest())
        rows = [{"scenario_id": sid, "bc": 1, "om": 1} for sid in ids]
        self.assertEqual(inference.ordered_paired_intervals(rows, ids),
                         inference.paired_intervals([(1, 1)] * 768))
        rows.reverse()
        with self.assertRaises(ValueError):
            inference.ordered_paired_intervals(rows, ids)
        missing_id = ids[100]
        observed = [{"scenario_id": sid, "bc": 1, "om": 1}
                    for sid in ids if sid != missing_id]
        self.assertIn(inference.ordered_decision_with_missingness(
            observed, [missing_id], ids), inference.DECISION_BRANCHES)
        observed.reverse()
        with self.assertRaises(ValueError):
            inference.ordered_decision_with_missingness(observed, [missing_id], ids)
        poisoned = [{"scenario_id": sid, "bc": True, "om": True}
                    for sid in ids if sid != missing_id]
        with self.assertRaises(ValueError):
            inference.ordered_decision_with_missingness(poisoned, [missing_id], ids)


if __name__ == "__main__":
    unittest.main()
