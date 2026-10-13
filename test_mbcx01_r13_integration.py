import copy
import unittest

import mbcx01_r13_integration as integration
import mbcx01_r13_packets as packets


class R13IntegrationTests(unittest.TestCase):
    def test_full_valid_authoritative_transition_join(self):
        result = integration.verify_pipeline_join()
        self.assertEqual(result["selected"], 768)
        self.assertEqual(result["state_result"], "APPLIED")
        self.assertTrue(result["inference_order_bound"])
        self.assertTrue(result["writer_state_event_bound"])
        self.assertTrue(result["a1_postcommit_cut_bound"])
        self.assertTrue(result["action_catalog_bound"])
        self.assertTrue(result["durability_schema_joined"])
        self.assertTrue(result["episode_partition_authority_bound"])
        self.assertTrue(result["proposal_authority_bound"])
        self.assertTrue(result["dual_reducer_replay_bound"])
        self.assertTrue(result["postcommit_state_hash_bound"])
        self.assertEqual(result["packet_score"], 1)
        self.assertEqual(result["scientific_score"], 0)
        self.assertFalse(result["state_authority_available"])

    def test_packet_child_must_equal_actually_applied_integration_event(self):
        execution = integration.build_joined_execution()
        forged = copy.deepcopy(execution["scoring"])
        child = forged["writer_receipt"]["child_events"][0]
        child["idempotency_key"] = "IDEM.PACKET.LOCAL.INTEGRATION"
        child["event_id"] = packets._canonical_event_id(child)
        forged["writer_receipt"]["receipt_hash"] = packets.hash_without(
            forged["writer_receipt"], "receipt_hash")
        self.assertFalse(integration.execution_binding_matches(
            forged, execution["actual_child_event"], execution["actual_poststate"]))

    def test_cross_artifact_manifest_substitution_fails(self):
        current, manifest, _ = integration.joined_scenario_fixture()
        scoring = packets.build_scoring_fixture(manifest, "OM")
        forged = copy.deepcopy(scoring)
        forged["worker_handoff"]["manifest_hash"] = "9" * 96
        forged["worker_handoff"]["worker_handoff_hash"] = packets.hash_without(
            forged["worker_handoff"], "worker_handoff_hash")
        self.assertEqual(packets.score_fixture_conformance_exact(manifest, forged), 0)


if __name__ == "__main__":
    unittest.main()
