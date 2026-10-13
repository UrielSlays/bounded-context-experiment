from __future__ import annotations

import copy
import unittest

import mbcx01_r11_packets as packets


class R11PacketTests(unittest.TestCase):
    def setUp(self):
        self.expected = packets.packet_fixture_manifest()
        self.valid = packets.build_scoring_fixture(self.expected, "OM")

    @staticmethod
    def _rehash_from_worker(value):
        worker = value["worker_handoff"]
        worker["worker_handoff_hash"] = packets.hash_without(worker, "worker_handoff_hash")
        b_call = value["b_call_record"]
        b_call["raw_response_utf8"] = packets.canonical_json(worker).decode("utf-8")
        b_call["raw_response_hash"] = packets.sha384(b_call["raw_response_utf8"].encode("utf-8"))
        b_call["parsed_response_hash"] = worker["worker_handoff_hash"]
        b_transaction = b_call["durability_receipt"]["transaction_id"]
        b_call["durability_receipt"] = packets.make_durability_receipt(b_call, b_transaction)
        b_call["call_record_hash"] = packets.hash_without(b_call, "call_record_hash")
        receipt = value["writer_receipt"]
        receipt["worker_handoff_hash"] = worker["worker_handoff_hash"]
        receipt["worker_call_record_hash"] = b_call["call_record_hash"]
        receipt["receipt_hash"] = packets.hash_without(receipt, "receipt_hash")
        a1_result = value["a1_result"]
        a1_result["writer_receipt_hash"] = receipt["receipt_hash"]
        a1_result["result_hash"] = packets.hash_without(a1_result, "result_hash")
        a1_call = value["a1_call_record"]
        a1_call["raw_response_utf8"] = packets.canonical_json(a1_result).decode("utf-8")
        a1_call["raw_response_hash"] = packets.sha384(a1_call["raw_response_utf8"].encode("utf-8"))
        a1_call["parsed_response_hash"] = a1_result["result_hash"]
        a1_transaction = a1_call["durability_receipt"]["transaction_id"]
        a1_call["durability_receipt"] = packets.make_durability_receipt(
            a1_call, a1_transaction)
        a1_call["call_record_hash"] = packets.hash_without(a1_call, "call_record_hash")

    def test_valid_typed_dag_scores_one(self):
        self.assertEqual(packets.validate_scorer_input(self.expected, self.valid), [])
        self.assertEqual(packets.score_exact(self.expected, self.valid), 1)
        self.assertNotEqual(self.valid["a0_packet"]["packet_hash"],
                            self.valid["task_packet"]["task_packet_hash"])
        self.assertNotEqual(self.valid["a0_packet"]["packet_hash"],
                            self.valid["a1_packet"]["packet_hash"])
        self.assertEqual(len(self.valid["b_call_record"]["served_request_hash"]), 64)
        self.assertTrue(self.valid["b_call_record"]["durability_receipt"]["fsync_completed"])

    def test_call_record_requires_structured_durability_receipt(self):
        forged = copy.deepcopy(self.valid)
        receipt = forged["b_call_record"]["durability_receipt"]
        receipt["fsync_completed"] = False
        receipt["receipt_hash"] = packets.hash_without(receipt, "receipt_hash")
        forged["b_call_record"]["call_record_hash"] = packets.hash_without(
            forged["b_call_record"], "call_record_hash")
        self.assertEqual(packets.score_exact(self.expected, forged), 0)

    def test_call_record_raw_bytes_must_parse_to_the_bound_result(self):
        forged = copy.deepcopy(self.valid)
        row = forged["b_call_record"]
        row["raw_response_utf8"] = "{}"
        row["raw_response_hash"] = packets.sha384(b"{}")
        receipt = row["durability_receipt"]
        receipt["raw_response_hash"] = row["raw_response_hash"]
        receipt["receipt_hash"] = packets.hash_without(receipt, "receipt_hash")
        row["call_record_hash"] = packets.hash_without(row, "call_record_hash")
        worker = forged["worker_handoff"]
        self.assertFalse(packets._valid_call(
            row, self.expected, "OM", "B", forged["task_packet"]["task_packet_hash"],
            worker["served_request_hash"], worker,
        ))

    def test_call_record_all_identity_fields_and_one_route_are_admitted(self):
        for field, value in (("route_contract_hash", "9" * 96),
                             ("idempotency_token", ""),
                             ("accepted_at", "NOT-A-TIME"),
                             ("provider_request_id", ""),
                             ("response_ref", "")):
            forged = copy.deepcopy(self.valid)
            row = forged["a1_call_record"]
            row[field] = value
            if field == "response_ref":
                row["durability_receipt"]["response_ref"] = value
                row["durability_receipt"]["receipt_hash"] = packets.hash_without(
                    row["durability_receipt"], "receipt_hash")
            row["call_record_hash"] = packets.hash_without(row, "call_record_hash")
            self.assertEqual(packets.score_exact(self.expected, forged), 0, field)

    def test_call_ids_are_node_unique_and_temporally_ordered(self):
        for source_field, target_field in (("idempotency_token", "idempotency_token"),
                                           ("response_ref", "response_ref"),
                                           ("provider_request_id", "provider_request_id")):
            forged = copy.deepcopy(self.valid)
            forged["a1_call_record"][target_field] = forged["b_call_record"][source_field]
            if target_field == "response_ref":
                forged["a1_call_record"]["durability_receipt"]["response_ref"] = \
                    forged["b_call_record"][source_field]
                forged["a1_call_record"]["durability_receipt"]["receipt_hash"] = \
                    packets.hash_without(forged["a1_call_record"]["durability_receipt"], "receipt_hash")
            forged["a1_call_record"]["call_record_hash"] = packets.hash_without(
                forged["a1_call_record"], "call_record_hash")
            self.assertEqual(packets.score_exact(self.expected, forged), 0, target_field)
        forged = copy.deepcopy(self.valid)
        forged["a1_call_record"]["accepted_at"] = packets.T0
        forged["a1_call_record"]["call_record_hash"] = packets.hash_without(
            forged["a1_call_record"], "call_record_hash")
        self.assertEqual(packets.score_exact(self.expected, forged), 0)

    def test_scorer_is_total_and_fail_closed_for_malformed_nested_values(self):
        for field in ("a0_packet", "worker_handoff", "writer_receipt", "a1_result"):
            forged = copy.deepcopy(self.valid)
            forged[field] = []
            self.assertEqual(packets.score_exact(self.expected, forged), 0, field)

    def test_bc_builder_has_no_unbound_selection_argument(self):
        bc = packets.build_decision_packet(self.expected, "BC", "A0_PRECOMMIT")
        om = packets.build_decision_packet(self.expected, "OM", "A0_PRECOMMIT")
        self.assertNotEqual(bc["objects"], om["objects"])
        with self.assertRaises(TypeError):
            packets.build_decision_packet(self.expected, "BC", "A0_PRECOMMIT",
                                          self.expected["gold_read_set"])

    def test_semantically_forged_gold_manifest_is_rejected(self):
        forged = copy.deepcopy(self.expected)
        forged["gold_action_id"] = "ACT." + "F" * 64
        forged["manifest_hash"] = packets.hash_without(forged, "manifest_hash")
        self.assertIn("GOLD_ACTION_INVALID", packets.validate_expected_manifest(forged))
        self.assertEqual(packets.score_exact(forged, self.valid), 0)

    def test_manifest_rejects_nonhex_route_contract_hash(self):
        forged = copy.deepcopy(self.expected)
        forged["route_contract_hash"] = "Z" * 96
        forged["manifest_hash"] = packets.hash_without(forged, "manifest_hash")
        self.assertIn("ROUTE_CONTRACT_INVALID", packets.validate_expected_manifest(forged))

    def test_worker_must_be_produced_before_b_acceptance(self):
        forged = copy.deepcopy(self.valid)
        forged["worker_handoff"]["produced_at"] = "2026-08-14T00:00:00.000000Z"
        self._rehash_from_worker(forged)
        self.assertEqual(packets.score_exact(self.expected, forged), 0)

    def test_durability_transaction_ids_are_node_unique(self):
        forged = copy.deepcopy(self.valid)
        a1_call = forged["a1_call_record"]
        transaction = forged["a0_call_record"]["durability_receipt"]["transaction_id"]
        a1_call["durability_receipt"] = packets.make_durability_receipt(a1_call, transaction)
        a1_call["call_record_hash"] = packets.hash_without(a1_call, "call_record_hash")
        self.assertEqual(packets.score_exact(self.expected, forged), 0)

    def test_schema_invalid_nested_worker_cannot_score(self):
        forged = copy.deepcopy(self.valid)
        forged["worker_handoff"]["TAINT"] = True
        forged["worker_handoff"]["worker_handoff_hash"] = packets.hash_without(
            forged["worker_handoff"], "worker_handoff_hash")
        forged["b_call_record"]["parsed_response_hash"] = forged["worker_handoff"]["worker_handoff_hash"]
        forged["b_call_record"]["call_record_hash"] = packets.hash_without(
            forged["b_call_record"], "call_record_hash")
        self.assertEqual(packets.score_exact(self.expected, forged), 0)

    def test_fake_common_packet_hash_cannot_score(self):
        forged = copy.deepcopy(self.valid)
        fake = "9" * 96
        forged["a0_result"]["input_packet_hash"] = fake
        forged["a0_result"]["result_hash"] = packets.hash_without(forged["a0_result"], "result_hash")
        forged["task_packet"]["a0_packet_hash"] = fake
        forged["task_packet"]["task_packet_hash"] = packets.hash_without(
            forged["task_packet"], "task_packet_hash")
        self.assertEqual(packets.score_exact(self.expected, forged), 0)

    def test_unbound_served_request_hash_cannot_score(self):
        forged = copy.deepcopy(self.valid)
        forged["b_call_record"]["served_request_hash"] = "7" * 64
        forged["b_call_record"]["call_record_hash"] = packets.hash_without(
            forged["b_call_record"], "call_record_hash")
        self.assertEqual(packets.score_exact(self.expected, forged), 0)

    def test_cross_scenario_b_response_cannot_score(self):
        forged = copy.deepcopy(self.valid)
        forged["b_call_record"]["scenario_id"] = "SCENARIO.UNRELATED"
        forged["b_call_record"]["call_record_hash"] = packets.hash_without(
            forged["b_call_record"], "call_record_hash")
        self.assertEqual(packets.score_exact(self.expected, forged), 0)

    def test_invented_child_event_cannot_score(self):
        forged = copy.deepcopy(self.valid)
        forged["writer_receipt"]["child_events"][0]["event_id"] = "EV." + "0" * 64
        forged["writer_receipt"]["receipt_hash"] = packets.hash_without(
            forged["writer_receipt"], "receipt_hash")
        self.assertEqual(packets.score_exact(self.expected, forged), 0)

    def test_precommit_a1_packet_cannot_score(self):
        forged = copy.deepcopy(self.valid)
        forged["a1_packet"] = copy.deepcopy(forged["a0_packet"])
        forged["a1_result"]["input_packet_hash"] = forged["a1_packet"]["packet_hash"]
        forged["a1_result"]["served_request_hash"] = packets.served_input_hash(
            packets.render_served_input(forged["a1_packet"]))
        forged["a1_result"]["result_hash"] = packets.hash_without(forged["a1_result"], "result_hash")
        self.assertEqual(packets.score_exact(self.expected, forged), 0)


if __name__ == "__main__":
    unittest.main()
