import math
import unittest

import mbcx01_r12_inference as inference


class R12InferenceTests(unittest.TestCase):
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
            observed, missing, samples=128, seed="MBCX01-R12-DP-SPOT-V1")
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


if __name__ == "__main__":
    unittest.main()
