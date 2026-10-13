from __future__ import annotations

import copy
import unittest

import mbcx01_r13_packets as packets


class R13PacketTests(unittest.TestCase):
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

    def _rehash_from_transition_authority(self, value):
        authority = value["transition_authority"]
        authority["transition_authority_hash"] = packets.hash_without(
            authority, "transition_authority_hash")
        receipt = value["writer_receipt"]
        receipt["transition_authority_hash"] = authority["transition_authority_hash"]
        receipt["precommit_state_hash"] = authority["precommit_state_hash"]
        receipt["proposal_event_hash"] = authority["proposal_event_hash"]
        receipt["applied_child_event_hash"] = authority["applied_child_event_hash"]
        receipt["postcommit_cut"] = copy.deepcopy(authority["postcommit_cut"])
        receipt["postcommit_state_hash"] = authority["postcommit_state_hash"]
        receipt["receipt_hash"] = packets.hash_without(receipt, "receipt_hash")

        a1_packet = packets.build_decision_packet(
            self.expected, "OM", "A1_POSTCOMMIT",
            postcommit_cut=authority["postcommit_cut"],
            source_world=packets.project_state_world(
                authority["postcommit_state"], self.expected))
        value["a1_packet"] = a1_packet
        a1_served = packets.served_input_hash(packets.render_served_input(a1_packet))
        a1_result = value["a1_result"]
        a1_result["input_packet_hash"] = a1_packet["packet_hash"]
        a1_result["served_request_hash"] = a1_served
        a1_result["writer_receipt_hash"] = receipt["receipt_hash"]
        a1_result["result_hash"] = packets.hash_without(a1_result, "result_hash")
        value["a1_call_record"] = packets._call_record(
            self.expected, "OM", "A1", a1_packet["packet_hash"], a1_served,
            a1_result, packets.canonical_json(a1_result).decode("utf-8"))

    def _matrix(self, value=None):
        self.assertTrue(hasattr(packets, "invariant_matrix"))
        return packets.invariant_matrix(
            self.expected, value or self.valid, require_production_authority=False)

    def _rehash_a1(self, value):
        packet = value["a1_packet"]
        packet["packet_hash"] = packets.hash_without(packet, "packet_hash")
        served = packets.served_input_hash(packets.render_served_input(packet))
        result = value["a1_result"]
        result["input_packet_hash"] = packet["packet_hash"]
        result["served_request_hash"] = served
        result["result_hash"] = packets.hash_without(result, "result_hash")
        value["a1_call_record"] = packets._call_record(
            self.expected, "OM", "A1", packet["packet_hash"], served,
            result, packets.canonical_json(result).decode("utf-8"))

    def test_i01_cohort_manifest_positive(self):
        self.assertIn("cohort_authority", self.valid)
        self.assertTrue(self._matrix()["I01"])

    def test_i01_cohort_manifest_adversarial(self):
        self.assertIn("cohort_authority", self.valid)
        forged = copy.deepcopy(self.valid)
        authority = forged["cohort_authority"]
        authority["scenario_id"] = "SCENARIO.DISAGREES"
        authority["authority_hash"] = packets.hash_without(authority, "authority_hash")
        self.assertFalse(self._matrix(forged)["I01"])
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_i01_cohort_manifest_action_universe_adversarial(self):
        forged = copy.deepcopy(self.valid)
        authority = forged["cohort_authority"]
        authority["action_universe"] = ["NO_ACTION"]
        authority["authority_hash"] = packets.hash_without(authority, "authority_hash")
        self.assertFalse(self._matrix(forged)["I01"])
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_i01_self_consistent_nonmember_candidate_cannot_mint_authority(self):
        forged = copy.deepcopy(self.valid)
        authority = forged["cohort_authority"]
        authority["candidate_record"]["motif"] = "CROSS_SCOPE_COLLISION"
        authority["candidate_hash"] = packets.sha384(authority["candidate_record"])
        authority["authority_hash"] = packets.sha384(
            {key: value for key, value in authority.items() if key != "authority_hash"})
        self.assertFalse(self._matrix(forged)["I01"])

    def test_i02_manifest_authoritative_prestate_positive(self):
        self.assertIn("state_authority_receipt", self.valid)
        self.assertTrue(self._matrix()["I02"])

    def test_i02_manifest_authoritative_prestate_adversarial(self):
        self.assertTrue(hasattr(packets, "build_scoring_fixture"))
        divergent = packets.state_reference.initial_state()
        manifest = packets.packet_fixture_manifest()
        manifest["cut"] = packets.state_reference.current_cut(divergent)
        manifest["manifest_hash"] = packets.hash_without(manifest, "manifest_hash")
        with self.assertRaisesRegex(ValueError, "MANIFEST_STATE_PROJECTION_MISMATCH"):
            packets.build_scoring_fixture(manifest, "OM", authoritative_state=divergent)

        forged = copy.deepcopy(self.valid)
        transition = forged["transition_authority"]
        alternate_prestate = copy.deepcopy(transition["precommit_state"])
        alternate_prestate["scopes"][self.expected["scope_id"]]["obligations"][
            "OBL.DECOY"]["critical"] = True
        alternate_poststate, result = packets.state_reference.reference_apply(
            copy.deepcopy(alternate_prestate),
            copy.deepcopy(transition["applied_child_event"]))
        self.assertEqual(result, "APPLIED")
        alternate_receipt = packets.state_reference.make_fixture_state_authority_receipt(
            alternate_prestate, transition["proposal_event"],
            transition["applied_child_event"], alternate_poststate)
        self.assertEqual(packets.state_reference.verify_state_authority_receipt(
            alternate_receipt, require_production=False), [])
        forged["state_authority_receipt"] = alternate_receipt
        self.assertFalse(self._matrix(forged)["I02"])
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_i02_same_cut_divergent_manifest_state_receipt_is_rejected(self):
        forged = copy.deepcopy(self.valid)
        receipt = forged["manifest_cut_state_receipt"]
        state = __import__("json").loads(receipt["state_utf8"])
        state["scopes"][self.expected["scope_id"]]["obligations"]["OBL.DECOY"][
            "critical"] = True
        receipt["state_utf8"] = packets.canonical_json(state).decode("utf-8")
        receipt["state_hash"] = packets.sha384(state)
        receipt["projected_world"] = packets.project_state_world(state, self.expected)
        receipt["projected_world_hash"] = packets.sha384(receipt["projected_world"])
        receipt["receipt_hash"] = packets.hash_without(receipt, "receipt_hash")
        self.assertFalse(self._matrix(forged)["I02"])

    def test_i02_same_cut_owner_role_change_is_rejected(self):
        """Amendment-1: the canonical world binds OWNER ROLE.

        The invariant matrix section 2 lists owner role among the fields the canonical world
        carries, and `delegate_obligation` changes it as a legal same-cut transition. A state
        that differs only by a delegation must therefore not project to the same world.
        """
        forged = copy.deepcopy(self.valid)
        receipt = forged["manifest_cut_state_receipt"]
        state = __import__("json").loads(receipt["state_utf8"])
        state["scopes"][self.expected["scope_id"]]["obligations"]["OBL.DECOY"][
            "owner_role"] = "SUPERVISOR"
        receipt["state_utf8"] = packets.canonical_json(state).decode("utf-8")
        receipt["state_hash"] = packets.sha384(state)
        receipt["projected_world"] = packets.project_state_world(state, self.expected)
        receipt["projected_world_hash"] = packets.sha384(receipt["projected_world"])
        receipt["receipt_hash"] = packets.hash_without(receipt, "receipt_hash")
        self.assertFalse(self._matrix(forged)["I02"])

    def test_i02_same_cut_subject_change_is_rejected(self):
        """Amendment-1: the canonical world binds SUBJECT.

        Same rule as the owner-role witness above, for the other field the matrix names and the
        pre-amendment projection omitted.
        """
        forged = copy.deepcopy(self.valid)
        receipt = forged["manifest_cut_state_receipt"]
        state = __import__("json").loads(receipt["state_utf8"])
        state["scopes"][self.expected["scope_id"]]["obligations"]["OBL.DECOY"][
            "subject_id"] = "SUB.SUBSTITUTED"
        receipt["state_utf8"] = packets.canonical_json(state).decode("utf-8")
        receipt["state_hash"] = packets.sha384(state)
        receipt["projected_world"] = packets.project_state_world(state, self.expected)
        receipt["projected_world_hash"] = packets.sha384(receipt["projected_world"])
        receipt["receipt_hash"] = packets.hash_without(receipt, "receipt_hash")
        self.assertFalse(self._matrix(forged)["I02"])

    def test_i03_a0_manifest_positive(self):
        self.assertTrue(self._matrix()["I03"])

    def test_i03_a0_manifest_adversarial(self):
        forged = copy.deepcopy(self.valid)
        forged["a0_packet"]["observation"]["code"] = "LOCALLY.VALID.BUT.DIFFERENT"
        forged["a0_packet"]["packet_hash"] = packets.hash_without(
            forged["a0_packet"], "packet_hash")
        self.assertFalse(self._matrix(forged)["I03"])
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_i04_taskpacket_a0_positive(self):
        self.assertTrue(self._matrix()["I04"])

    def test_i04_taskpacket_a0_adversarial(self):
        forged = copy.deepcopy(self.valid)
        task = forged["task_packet"]
        task["a0_result_hash"] = "A" * 96
        task["task_packet_hash"] = packets.hash_without(task, "task_packet_hash")
        self.assertFalse(self._matrix(forged)["I04"])
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_i05_b_response_durable_ledger_positive(self):
        self.assertIn("durable_b_response_binding", self.valid)
        self.assertTrue(self._matrix()["I05"])

    def test_i05_b_response_durable_ledger_adversarial(self):
        self.assertIn("durable_b_response_binding", self.valid)
        forged = copy.deepcopy(self.valid)
        alternate_call = copy.deepcopy(forged["b_call_record"])
        alternate_call["response_ref"] = "RESPONSE.OM.B.ALTERNATE"
        transaction_id = alternate_call["durability_receipt"]["transaction_id"]
        alternate_call["durability_receipt"] = packets.make_durability_receipt(
            alternate_call, transaction_id)
        alternate_call["call_record_hash"] = packets.hash_without(
            alternate_call, "call_record_hash")
        forged["durable_b_response_binding"] = (
            packets.build_durable_b_response_binding(alternate_call))
        self.assertFalse(self._matrix(forged)["I05"])
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_i06_proposal_persisted_prestate_positive(self):
        self.assertTrue(self._matrix()["I06"])

    def test_i06_proposal_persisted_prestate_adversarial(self):
        forged = copy.deepcopy(self.valid)
        authority = forged["transition_authority"]
        proposal = authority["proposal_event"]
        proposal["idempotency_key"] = "IDEM.DIFFERENT.PROPOSAL"
        proposal["event_id"] = packets._canonical_event_id(proposal)
        authority["proposal_event_utf8"] = packets.canonical_json(proposal).decode("utf-8")
        authority["proposal_event_hash"] = packets.sha384(proposal)
        authority["transition_authority_hash"] = packets.hash_without(
            authority, "transition_authority_hash")
        self.assertFalse(self._matrix(forged)["I06"])
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_i07_commit_proposal_prestate_positive(self):
        self.assertTrue(self._matrix()["I07"])

    def test_i07_commit_proposal_prestate_adversarial(self):
        forged = copy.deepcopy(self.valid)
        authority = forged["transition_authority"]
        child = authority["applied_child_event"]
        child["payload"]["proposal_event_id"] = "EV." + "D" * 64
        child["event_id"] = packets._canonical_event_id(child)
        authority["applied_child_event_hash"] = packets.sha384(child)
        authority["transition_authority_hash"] = packets.hash_without(
            authority, "transition_authority_hash")
        self.assertFalse(self._matrix(forged)["I07"])
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_i08_poststate_writer_receipt_positive(self):
        self.assertTrue(self._matrix()["I08"])

    def test_i08_poststate_writer_receipt_adversarial(self):
        forged = copy.deepcopy(self.valid)
        receipt = forged["writer_receipt"]
        receipt["postcommit_state_hash"] = "E" * 96
        receipt["receipt_hash"] = packets.hash_without(receipt, "receipt_hash")
        self.assertFalse(self._matrix(forged)["I08"])
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_i09_poststate_a1_world_truth_positive(self):
        self.assertTrue(self._matrix()["I09"])

    def test_i09_poststate_a1_world_truth_adversarial(self):
        forged = copy.deepcopy(self.valid)
        target = next(row for row in forged["a1_packet"]["objects"]
                      if row["object_id"] == "OBL.SHARED")
        target["fields"]["lifecycle"] = "OPEN"
        self._rehash_a1(forged)
        self.assertFalse(self._matrix(forged)["I09"])
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_valid_typed_dag_scores_one(self):
        self.assertEqual(packets.validate_fixture_conformance(self.expected, self.valid), [])
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, self.valid), 1)
        self.assertIn("STATE_AUTHORITY_UNAVAILABLE",
                      packets.validate_scorer_input(self.expected, self.valid))
        self.assertEqual(packets.score_exact(self.expected, self.valid), 0)
        self.assertNotEqual(self.valid["a0_packet"]["packet_hash"],
                            self.valid["task_packet"]["task_packet_hash"])
        self.assertNotEqual(self.valid["a0_packet"]["packet_hash"],
                            self.valid["a1_packet"]["packet_hash"])
        self.assertEqual(len(self.valid["b_call_record"]["served_request_hash"]), 64)
        self.assertTrue(self.valid["b_call_record"]["durability_receipt"]["fsync_completed"])
        authority = self.valid["transition_authority"]
        self.assertEqual(
            authority["precommit_state"]["events"][authority["proposal_event"]["event_id"]],
            authority["proposal_event_hash"])
        self.assertEqual(authority["proposal_event_utf8"],
                         packets.canonical_json(authority["proposal_event"]).decode("utf-8"))
        self.assertEqual(self.valid["writer_receipt"]["child_events"],
                         [authority["applied_child_event"]])

    def test_persisted_proposal_event_bytes_are_exact(self):
        forged = copy.deepcopy(self.valid)
        authority = forged["transition_authority"]
        authority["proposal_event_utf8"] += " "
        self._rehash_from_transition_authority(forged)
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_arbitrary_persisted_proposal_id_cannot_score(self):
        forged = copy.deepcopy(self.valid)
        authority = forged["transition_authority"]
        child = authority["applied_child_event"]
        child["payload"]["proposal_event_id"] = "EV." + "A" * 64
        child["event_id"] = packets._canonical_event_id(child)
        authority["applied_child_event_hash"] = packets.sha384(child)
        forged["writer_receipt"]["child_events"] = [copy.deepcopy(child)]
        self._rehash_from_transition_authority(forged)
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_writer_child_cannot_jump_next_sequence(self):
        forged = copy.deepcopy(self.valid)
        authority = forged["transition_authority"]
        child = authority["applied_child_event"]
        child["journal_seq"] += 1000
        child["originating_cut"]["journal_seq"] = child["journal_seq"] - 1
        child["event_id"] = packets._canonical_event_id(child)
        authority["applied_child_event_hash"] = packets.sha384(child)
        authority["postcommit_cut"]["journal_seq"] = child["journal_seq"]
        forged["writer_receipt"]["child_events"] = [copy.deepcopy(child)]
        self._rehash_from_transition_authority(forged)
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_postcommit_cut_must_make_child_validly_effective(self):
        forged = copy.deepcopy(self.valid)
        authority = forged["transition_authority"]
        self.assertLess(packets.T0, authority["applied_child_event"]["valid_from"])
        authority["postcommit_cut"]["valid_time"] = packets.T0
        self._rehash_from_transition_authority(forged)
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_packet_local_child_must_equal_transition_authority_event(self):
        forged = copy.deepcopy(self.valid)
        child = copy.deepcopy(forged["writer_receipt"]["child_events"][0])
        child["idempotency_key"] = "IDEM.PACKET.LOCAL.COMMIT"
        child["event_id"] = packets._canonical_event_id(child)
        forged["writer_receipt"]["child_events"] = [child]
        forged["writer_receipt"]["receipt_hash"] = packets.hash_without(
            forged["writer_receipt"], "receipt_hash")
        a1_result = forged["a1_result"]
        a1_result["writer_receipt_hash"] = forged["writer_receipt"]["receipt_hash"]
        a1_result["result_hash"] = packets.hash_without(a1_result, "result_hash")
        a1_call = forged["a1_call_record"]
        a1_call["raw_response_utf8"] = packets.canonical_json(a1_result).decode("utf-8")
        a1_call["raw_response_hash"] = packets.sha384(
            a1_call["raw_response_utf8"].encode("utf-8"))
        a1_call["parsed_response_hash"] = a1_result["result_hash"]
        transaction = a1_call["durability_receipt"]["transaction_id"]
        a1_call["durability_receipt"] = packets.make_durability_receipt(
            a1_call, transaction)
        a1_call["call_record_hash"] = packets.hash_without(a1_call, "call_record_hash")
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_call_record_requires_structured_durability_receipt(self):
        forged = copy.deepcopy(self.valid)
        receipt = forged["b_call_record"]["durability_receipt"]
        receipt["fsync_completed"] = False
        receipt["receipt_hash"] = packets.hash_without(receipt, "receipt_hash")
        forged["b_call_record"]["call_record_hash"] = packets.hash_without(
            forged["b_call_record"], "call_record_hash")
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

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
            self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0, field)

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
            self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0, target_field)
        forged = copy.deepcopy(self.valid)
        forged["a1_call_record"]["accepted_at"] = packets.T0
        forged["a1_call_record"]["call_record_hash"] = packets.hash_without(
            forged["a1_call_record"], "call_record_hash")
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_scorer_is_total_and_fail_closed_for_malformed_nested_values(self):
        for field in ("a0_packet", "worker_handoff", "writer_receipt", "a1_result"):
            forged = copy.deepcopy(self.valid)
            forged[field] = []
            self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0, field)

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
        self.assertEqual(packets.score_fixture_conformance_exact(forged, self.valid), 0)

    def test_manifest_rejects_nonhex_route_contract_hash(self):
        forged = copy.deepcopy(self.expected)
        forged["route_contract_hash"] = "Z" * 96
        forged["manifest_hash"] = packets.hash_without(forged, "manifest_hash")
        self.assertIn("ROUTE_CONTRACT_INVALID", packets.validate_expected_manifest(forged))

    def test_worker_must_be_produced_before_b_acceptance(self):
        forged = copy.deepcopy(self.valid)
        forged["worker_handoff"]["produced_at"] = "2026-08-14T00:00:00.000000Z"
        self._rehash_from_worker(forged)
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_durability_transaction_ids_are_node_unique(self):
        forged = copy.deepcopy(self.valid)
        a1_call = forged["a1_call_record"]
        transaction = forged["a0_call_record"]["durability_receipt"]["transaction_id"]
        a1_call["durability_receipt"] = packets.make_durability_receipt(a1_call, transaction)
        a1_call["call_record_hash"] = packets.hash_without(a1_call, "call_record_hash")
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_schema_invalid_nested_worker_cannot_score(self):
        forged = copy.deepcopy(self.valid)
        forged["worker_handoff"]["TAINT"] = True
        forged["worker_handoff"]["worker_handoff_hash"] = packets.hash_without(
            forged["worker_handoff"], "worker_handoff_hash")
        forged["b_call_record"]["parsed_response_hash"] = forged["worker_handoff"]["worker_handoff_hash"]
        forged["b_call_record"]["call_record_hash"] = packets.hash_without(
            forged["b_call_record"], "call_record_hash")
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_fake_common_packet_hash_cannot_score(self):
        forged = copy.deepcopy(self.valid)
        fake = "9" * 96
        forged["a0_result"]["input_packet_hash"] = fake
        forged["a0_result"]["result_hash"] = packets.hash_without(forged["a0_result"], "result_hash")
        forged["task_packet"]["a0_packet_hash"] = fake
        forged["task_packet"]["task_packet_hash"] = packets.hash_without(
            forged["task_packet"], "task_packet_hash")
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_unbound_served_request_hash_cannot_score(self):
        forged = copy.deepcopy(self.valid)
        forged["b_call_record"]["served_request_hash"] = "7" * 64
        forged["b_call_record"]["call_record_hash"] = packets.hash_without(
            forged["b_call_record"], "call_record_hash")
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_cross_scenario_b_response_cannot_score(self):
        forged = copy.deepcopy(self.valid)
        forged["b_call_record"]["scenario_id"] = "SCENARIO.UNRELATED"
        forged["b_call_record"]["call_record_hash"] = packets.hash_without(
            forged["b_call_record"], "call_record_hash")
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_invented_child_event_cannot_score(self):
        forged = copy.deepcopy(self.valid)
        forged["writer_receipt"]["child_events"][0]["event_id"] = "EV." + "0" * 64
        forged["writer_receipt"]["receipt_hash"] = packets.hash_without(
            forged["writer_receipt"], "receipt_hash")
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_precommit_a1_packet_cannot_score(self):
        forged = copy.deepcopy(self.valid)
        forged["a1_packet"] = copy.deepcopy(forged["a0_packet"])
        forged["a1_result"]["input_packet_hash"] = forged["a1_packet"]["packet_hash"]
        forged["a1_result"]["served_request_hash"] = packets.served_input_hash(
            packets.render_served_input(forged["a1_packet"]))
        forged["a1_result"]["result_hash"] = packets.hash_without(forged["a1_result"], "result_hash")
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, forged), 0)

    def test_outcome_bits_are_recomputed_from_two_exact_scorer_graphs(self):
        state = packets._fixture_authoritative_state(self.expected)
        authority = packets.cohort_authority_for_manifest(self.expected)
        bc = packets.build_scoring_fixture(
            self.expected, "BC", authoritative_state=state, cohort_authority=authority)
        episode = packets.build_complete_episode_receipt_for_scorers(
            bc, self.valid, self.expected["retained_position"])
        receipt = packets.build_scenario_outcome_receipt(
            self.expected, bc, self.valid, episode,
            require_production_authority=False)
        self.assertEqual(packets.validate_scenario_outcome_receipt(
            receipt, episode, require_production_authority=False), [])
        forged = copy.deepcopy(receipt)
        forged["bc"] = 0
        forged["receipt_hash"] = packets.hash_without(forged, "receipt_hash")
        self.assertIn("SCENARIO_OUTCOME_AUTHORITY_INVALID",
                      packets.validate_scenario_outcome_receipt(
                          forged, episode, require_production_authority=False))

    def test_zero_outcome_is_representable_and_bound_to_the_failing_graph(self):
        state = packets._fixture_authoritative_state(self.expected)
        authority = packets.cohort_authority_for_manifest(self.expected)
        bc = packets.build_scoring_fixture(
            self.expected, "BC", authoritative_state=state, cohort_authority=authority)
        bc["a0_result"]["selected_action_ids"] = []
        self.assertEqual(packets.score_fixture_conformance_exact(self.expected, bc), 0)
        episode = packets.build_complete_episode_receipt_for_scorers(
            bc, self.valid, self.expected["retained_position"])
        receipt = packets.build_scenario_outcome_receipt(
            self.expected, bc, self.valid, episode,
            require_production_authority=False)
        self.assertEqual((receipt["bc"], receipt["om"]), (0, 1))
        self.assertEqual(packets.validate_scenario_outcome_receipt(
            receipt, episode, require_production_authority=False), [])

    def test_i10_adversarial_outcome_graph_must_equal_the_exact_episode_ledgers(self):
        state = packets._fixture_authoritative_state(self.expected)
        authority = packets.cohort_authority_for_manifest(self.expected)
        bc = packets.build_scoring_fixture(
            self.expected, "BC", authoritative_state=state, cohort_authority=authority)
        episode = packets.build_complete_episode_receipt_for_scorers(
            bc, self.valid, self.expected["retained_position"])
        alternate = copy.deepcopy(bc)
        alternate["a0_result"]["selected_action_ids"] = []
        alternate["a0_result"]["result_hash"] = packets.hash_without(
            alternate["a0_result"], "result_hash")
        call = alternate["a0_call_record"]
        call["raw_response_utf8"] = packets.canonical_json(
            alternate["a0_result"]).decode("utf-8")
        call["raw_response_hash"] = packets.sha384(
            call["raw_response_utf8"].encode("utf-8"))
        call["parsed_response_hash"] = alternate["a0_result"]["result_hash"]
        transaction = call["durability_receipt"]["transaction_id"]
        call["durability_receipt"] = packets.make_durability_receipt(call, transaction)
        call["call_record_hash"] = packets.hash_without(call, "call_record_hash")
        alternate_episode = packets.build_complete_episode_receipt_for_scorers(
            alternate, self.valid, self.expected["retained_position"])
        alternate_receipt = packets.build_scenario_outcome_receipt(
            self.expected, alternate, self.valid, alternate_episode,
            require_production_authority=False)
        self.assertEqual((alternate_receipt["bc"], alternate_receipt["om"]), (0, 1))
        self.assertIn("SCENARIO_OUTCOME_AUTHORITY_INVALID",
                      packets.validate_scenario_outcome_receipt(
                          alternate_receipt, episode,
                          require_production_authority=False))


if __name__ == "__main__":
    unittest.main()
