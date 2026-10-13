import copy
import unittest

import mbcx01_r11_integration as integration
import mbcx01_r11_packets as packets


class R11IntegrationTests(unittest.TestCase):
    def test_state_cohort_packet_inference_join(self):
        result = integration.verify_pipeline_join()
        self.assertEqual(result["selected"], 768)
        self.assertEqual(result["state_result"], "APPLIED")
        self.assertTrue(result["inference_order_bound"])
        self.assertTrue(result["writer_state_event_bound"])
        self.assertTrue(result["a1_postcommit_cut_bound"])
        self.assertTrue(result["action_catalog_bound"])
        self.assertTrue(result["durability_schema_joined"])

    def test_cross_artifact_manifest_substitution_fails(self):
        current, manifest, _ = integration.joined_scenario_fixture()
        scoring = packets.build_scoring_fixture(manifest, "OM")
        forged = copy.deepcopy(scoring)
        forged["worker_handoff"]["manifest_hash"] = "9" * 96
        forged["worker_handoff"]["worker_handoff_hash"] = packets.hash_without(
            forged["worker_handoff"], "worker_handoff_hash")
        self.assertEqual(packets.score_exact(manifest, forged), 0)


if __name__ == "__main__":
    unittest.main()
