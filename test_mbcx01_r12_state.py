from __future__ import annotations

import copy
import unittest

import mbcx01_r12_common as common
import mbcx01_r12_state_oracle as oracle
import mbcx01_r12_state_reference as reference


class R12StateTests(unittest.TestCase):
    ENGINES = (reference.reference_apply, oracle.oracle_apply)

    def assert_engines(self, state: dict, event: dict, expected: str) -> list[dict]:
        outputs = []
        for engine in self.ENGINES:
            result_state, result = engine(copy.deepcopy(state), copy.deepcopy(event))
            self.assertEqual(result, expected, engine.__module__)
            outputs.append(result_state)
        self.assertEqual(outputs[0], outputs[1])
        return outputs

    def test_noncanonical_event_id_is_rejected(self):
        state = reference.initial_state()
        event = reference.make_event("assert_fact", {
            "subject_id": "SUB.NEW", "predicate_id": "PRED.NEW", "value_code": "VALUE.NEW"
        }, state=state)
        event["event_id"] = "EV.ARBITRARY"

        outputs = self.assert_engines(state, event, "EVENT_ID_INVALID")
        self.assertTrue(all(output == state for output in outputs))

    def test_every_event_type_rejects_wrong_payload_types_without_throwing(self):
        for event_type, required in reference.PAYLOAD_REQUIRED.items():
            state = reference.initial_state()
            payload = {name: "X" for name in required}
            payload[sorted(required)[0]] = []
            event = reference.make_event(event_type, payload, state=state)
            outputs = self.assert_engines(state, event, "SCHEMA_INVALID")
            self.assertTrue(all(output == state for output in outputs))

    def test_unserializable_envelope_is_schema_invalid_not_an_exception(self):
        state = reference.initial_state()
        event = reference.make_event("assert_fact", {
            "subject_id": "SUB.X", "predicate_id": "PRED.X", "value_code": "VALUE.X"
        }, state=state)
        event["payload"]["value_code"] = object()
        outputs = self.assert_engines(state, event, "SCHEMA_INVALID")
        self.assertTrue(all(output == state for output in outputs))

    def test_future_fact_does_not_block_current_interval(self):
        for engine in self.ENGINES:
            state = reference.initial_state()
            future = reference.make_event("assert_fact", {
                "subject_id": "SUB.TIME", "predicate_id": "PRED.TIME", "value_code": "VALUE.FUTURE"
            }, state=state, valid_from="2026-09-01T00:00:00.000000Z")
            state, result = engine(state, future)
            self.assertEqual(result, "APPLIED")
            current = reference.make_event("assert_fact", {
                "subject_id": "SUB.TIME", "predicate_id": "PRED.TIME", "value_code": "VALUE.CURRENT"
            }, state=state, valid_from="2026-08-01T00:00:00.000000Z",
                originating_cut={"journal_seq": 1, "knowledge_time": reference.T1,
                                 "valid_time": "2026-08-15T00:00:00.000000Z"})
            state, result = engine(state, current)
            self.assertEqual(result, "APPLIED")
            rows = state["scopes"]["SCOPE.SHARED"]["facts"][reference.fact_key("SUB.TIME", "PRED.TIME")]
            current_row = next(row for row in rows if row["value_code"] == "VALUE.CURRENT")
            self.assertEqual(current_row["valid_to"], "2026-09-01T00:00:00.000000Z")

    def test_explicit_fact_interval_is_not_silently_truncated_at_a_future_row(self):
        for engine in self.ENGINES:
            state = reference.initial_state()
            future = reference.make_event("assert_fact", {
                "subject_id": "SUB.TIME", "predicate_id": "PRED.TIME",
                "value_code": "VALUE.FUTURE",
            }, state=state, valid_from="2026-09-01T00:00:00.000000Z")
            state, result = engine(state, future)
            self.assertEqual(result, "APPLIED")
            authored = reference.make_event("assert_fact", {
                "subject_id": "SUB.TIME", "predicate_id": "PRED.TIME",
                "value_code": "VALUE.AUTHORED",
            }, state=state, valid_from="2026-08-01T00:00:00.000000Z",
                valid_to="2026-10-01T00:00:00.000000Z",
                originating_cut={"journal_seq": 1, "knowledge_time": reference.T1,
                                 "valid_time": "2026-08-15T00:00:00.000000Z"})
            unchanged, result = engine(state, authored)
            self.assertEqual(result, "FACT_ALREADY_EXISTS")
            self.assertEqual(unchanged, state)

    def test_finite_visible_head_can_be_corrected_without_inversion(self):
        for engine in self.ENGINES:
            state = reference.initial_state()
            parent = reference.make_event("assert_fact", {
                "subject_id": "SUB.TIME", "predicate_id": "PRED.TIME", "value_code": "VALUE.OLD"
            }, state=state, valid_from="2026-08-01T00:00:00.000000Z",
                valid_to="2026-09-01T00:00:00.000000Z")
            state, result = engine(state, parent)
            self.assertEqual(result, "APPLIED")
            correction = reference.make_event("correct_fact", {
                "subject_id": "SUB.TIME", "predicate_id": "PRED.TIME",
                "parent_event_id": parent["event_id"], "value_code": "VALUE.NEW"
            }, state=state, valid_from="2026-08-20T00:00:00.000000Z",
                originating_cut={"journal_seq": 1, "knowledge_time": reference.T1,
                                 "valid_time": "2026-08-20T00:00:00.000000Z"})
            state, result = engine(state, correction)
            self.assertEqual(result, "APPLIED")
            rows = state["scopes"]["SCOPE.SHARED"]["facts"][reference.fact_key("SUB.TIME", "PRED.TIME")]
            current_cut = {"journal_seq": 2, "knowledge_time": reference.T1,
                           "valid_time": "2026-08-20T00:00:00.000000Z"}
            self.assertEqual(reference.effective_valid_to(rows[0], current_cut),
                             "2026-08-20T00:00:00.000000Z")
            self.assertEqual(rows[1]["valid_from"], "2026-08-20T00:00:00.000000Z")
            self.assertEqual(rows[1]["valid_to"], "2026-09-01T00:00:00.000000Z")
            self.assertLess(rows[1]["valid_from"], rows[1]["valid_to"])

    def test_retro_correction_cannot_invert_interval(self):
        state = reference.initial_state()
        parent = reference.make_event("assert_fact", {
            "subject_id": "SUB.TIME", "predicate_id": "PRED.TIME", "value_code": "VALUE.OLD"
        }, state=state, valid_from="2026-09-01T00:00:00.000000Z")
        state = self.assert_engines(state, parent, "APPLIED")[0]
        correction = reference.make_event("correct_fact", {
            "subject_id": "SUB.TIME", "predicate_id": "PRED.TIME",
            "parent_event_id": parent["event_id"], "value_code": "VALUE.BAD"
        }, state=state, valid_from="2026-08-01T00:00:00.000000Z",
            originating_cut={"journal_seq": 1, "knowledge_time": reference.T1,
                             "valid_time": "2026-09-15T00:00:00.000000Z"})
        outputs = self.assert_engines(state, correction, "FACT_PARENT_NOT_HEAD")
        self.assertTrue(all(output == state for output in outputs))

    def test_proposal_requires_exact_durable_b_response_foreign_key(self):
        for engine in self.ENGINES:
            state = reference.initial_state()
            handoff = reference.make_event("open_handoff", reference.handoff_fixture_payload(), state=state)
            state, result = engine(state, handoff)
            self.assertEqual(result, "APPLIED")

            unrelated_handoff = copy.deepcopy(handoff["payload"])
            unrelated_handoff["scenario_id"] = "SCENARIO.UNRELATED"
            unrelated_payload = reference.response_fixture_payload(unrelated_handoff)
            unrelated = reference.make_event("record_call_response", unrelated_payload, state=state)
            unchanged, result = engine(state, unrelated)
            self.assertEqual(result, "CALL_RESPONSE_CONFLICT")
            self.assertEqual(unchanged, state)

            proposal = reference.make_event("propose_handoff_result", {
                "handoff_id": handoff["payload"]["handoff_id"],
                "worker_handoff_hash": unrelated_payload["worker_handoff_hash"],
                "originating_cut_hash": handoff["payload"]["originating_cut_hash"],
                "action_ids": [handoff["payload"]["action_catalog"][0]["action_id"]]
            }, state=state)
            unchanged, result = engine(state, proposal)
            self.assertEqual(result, "PROPOSAL_INVALID")
            self.assertEqual(unchanged, state)

            exact_payload = reference.response_fixture_payload(handoff["payload"])
            exact = reference.make_event("record_call_response", exact_payload, state=state)
            state, result = engine(state, exact)
            self.assertEqual(result, "APPLIED")
            proposal = reference.make_event("propose_handoff_result", {
                "handoff_id": handoff["payload"]["handoff_id"],
                "worker_handoff_hash": exact_payload["worker_handoff_hash"],
                "originating_cut_hash": handoff["payload"]["originating_cut_hash"],
                "action_ids": [handoff["payload"]["action_catalog"][0]["action_id"]]
            }, state=state)
            state, result = engine(state, proposal)
            self.assertEqual(result, "APPLIED")
            self.assertEqual(state["scopes"]["SCOPE.SHARED"]["handoffs"][handoff["payload"]["handoff_id"]]["status"], "PROPOSED")

    def test_correction_and_retraction_do_not_rewrite_historical_cut(self):
        for event_type in ("correct_fact", "retract_fact"):
            for engine in self.ENGINES:
                state = reference.initial_state()
                parent = reference.make_event("assert_fact", {
                    "subject_id": "SUB.TIME", "predicate_id": "PRED.TIME", "value_code": "VALUE.OLD"
                }, state=state, valid_from="2026-08-01T00:00:00.000000Z")
                state, self_result = engine(state, parent)
                self.assertEqual(self_result, "APPLIED")
                historical = {"journal_seq": 1, "knowledge_time": reference.T1,
                              "valid_time": "2026-08-01T18:00:00.000000Z"}
                row = state["scopes"]["SCOPE.SHARED"]["facts"][reference.fact_key("SUB.TIME", "PRED.TIME")][0]
                self.assertTrue(reference.visible_effective(row, historical))
                payload = {"subject_id": "SUB.TIME", "predicate_id": "PRED.TIME"}
                if event_type == "correct_fact":
                    payload.update(parent_event_id=parent["event_id"], value_code="VALUE.NEW")
                else:
                    payload.update(target_event_id=parent["event_id"])
                event = reference.make_event(event_type, payload, state=state,
                    valid_from="2026-08-01T12:00:00.000000Z",
                    originating_cut={"journal_seq": 1, "knowledge_time": reference.T1,
                                     "valid_time": "2026-08-01T18:00:00.000000Z"})
                state, self_result = engine(state, event)
                self.assertEqual(self_result, "APPLIED")
                row = state["scopes"]["SCOPE.SHARED"]["facts"][reference.fact_key("SUB.TIME", "PRED.TIME")][0]
                self.assertTrue(reference.visible_effective(row, historical))

    def test_stale_cut_and_overlapping_assertions_are_rejected(self):
        for engine in self.ENGINES:
            state = reference.initial_state()
            first = reference.make_event("assert_fact", {
                "subject_id": "SUB.TIME", "predicate_id": "PRED.TIME", "value_code": "VALUE.ONE"
            }, state=state, valid_from="2026-08-01T00:00:00.000000Z")
            state, result = engine(state, first)
            self.assertEqual(result, "APPLIED")
            stale = reference.make_event("assert_fact", {
                "subject_id": "SUB.TIME", "predicate_id": "PRED.TIME", "value_code": "VALUE.TWO"
            }, state=state, valid_from="2026-08-01T06:00:00.000000Z",
                originating_cut={"journal_seq": 0, "knowledge_time": reference.T1,
                                 "valid_time": "2026-08-01T06:00:00.000000Z"})
            unchanged, result = engine(state, stale)
            self.assertEqual(result, "ORIGINATING_CUT_INVALID")
            self.assertEqual(unchanged, state)

    def test_correction_requires_strictly_internal_start_and_bounded_end(self):
        for engine in self.ENGINES:
            state = reference.initial_state()
            parent = reference.make_event("assert_fact", {
                "subject_id": "SUB.TIME", "predicate_id": "PRED.TIME", "value_code": "VALUE.OLD"
            }, state=state, valid_from="2026-08-01T00:00:00.000000Z",
                valid_to="2026-08-01T12:00:00.000000Z")
            state, result = engine(state, parent)
            self.assertEqual(result, "APPLIED")
            for start, end in (("2026-08-01T00:00:00.000000Z", None),
                               ("2026-08-01T18:00:00.000000Z", "2026-08-02T00:00:00.000000Z"),
                               ("2026-08-01T06:00:00.000000Z", "2026-08-01T18:00:00.000000Z")):
                correction = reference.make_event("correct_fact", {
                    "subject_id": "SUB.TIME", "predicate_id": "PRED.TIME",
                    "parent_event_id": parent["event_id"], "value_code": "VALUE.BAD"
                }, state=state, valid_from=start, valid_to=end,
                    originating_cut={"journal_seq": 1, "knowledge_time": reference.T1,
                                     "valid_time": "2026-08-01T06:00:00.000000Z"})
                unchanged, result = engine(state, correction)
                self.assertEqual(result, "FACT_PARENT_NOT_HEAD")
                self.assertEqual(unchanged, state)

    def test_response_must_follow_matching_open_handoff_in_same_scope_and_be_unique(self):
        for engine in self.ENGINES:
            state = reference.initial_state()
            payload = reference.handoff_fixture_payload()
            preopen_response = reference.make_event("record_call_response",
                reference.response_fixture_payload(payload), state=state)
            unchanged, result = engine(state, preopen_response)
            self.assertEqual(result, "CALL_RESPONSE_CONFLICT")
            self.assertEqual(unchanged, state)
            handoff = reference.make_event("open_handoff", payload, state=state)
            state, result = engine(state, handoff)
            self.assertEqual(result, "APPLIED")
            cross_scope = reference.make_event("record_call_response",
                reference.response_fixture_payload(payload), state=state, scope_id="SCOPE.OTHER")
            unchanged, result = engine(state, cross_scope)
            self.assertEqual(result, "CALL_RESPONSE_CONFLICT")
            self.assertEqual(unchanged, state)
            response_payload = reference.response_fixture_payload(payload)
            response = reference.make_event("record_call_response", response_payload, state=state)
            state, result = engine(state, response)
            self.assertEqual(result, "APPLIED")
            duplicate = reference.make_event("record_call_response", response_payload, state=state,
                                             idempotency_key="IDEM.RESPONSE.SECOND")
            unchanged, result = engine(state, duplicate)
            self.assertEqual(result, "CALL_RESPONSE_CONFLICT")
            self.assertEqual(unchanged, state)

    def test_response_worker_hash_must_be_derived_from_durable_raw_bytes(self):
        for engine in self.ENGINES:
            state = reference.initial_state()
            payload = reference.handoff_fixture_payload()
            handoff = reference.make_event("open_handoff", payload, state=state)
            state, result = engine(state, handoff)
            self.assertEqual(result, "APPLIED")
            response_payload = reference.response_fixture_payload(payload)
            response_payload["worker_handoff_hash"] = "E" * 96
            response = reference.make_event("record_call_response", response_payload, state=state)
            unchanged, result = engine(state, response)
            self.assertEqual(result, "SCHEMA_INVALID")
            self.assertEqual(unchanged, state)

    def test_worker_scope_actions_and_manifest_are_bound_to_handoff_and_proposal(self):
        for engine in self.ENGINES:
            state = reference.initial_state()
            payload = reference.handoff_fixture_payload()
            handoff = reference.make_event("open_handoff", payload, state=state)
            state, result = engine(state, handoff)
            self.assertEqual(result, "APPLIED")
            for field, value in (("scope_id", "SCOPE.FOREIGN"),
                                 ("manifest_hash", "7" * 96),
                                 ("proposed_action_ids", ["ACT." + "9" * 64])):
                response_payload = reference.response_fixture_payload(payload)
                worker = reference.json.loads(response_payload["raw_response_utf8"])
                worker[field] = value
                worker["worker_handoff_hash"] = reference.sha384({
                    key: item for key, item in worker.items() if key != "worker_handoff_hash"})
                response_payload["raw_response_utf8"] = reference.canonical_json(worker).decode("utf-8")
                response_payload["raw_response_hash"] = reference.sha384(
                    response_payload["raw_response_utf8"].encode("utf-8"))
                response_payload["worker_handoff_hash"] = worker["worker_handoff_hash"]
                receipt = response_payload["durability_receipt"]
                receipt["raw_response_hash"] = response_payload["raw_response_hash"]
                receipt["receipt_hash"] = reference.sha384({
                    key: item for key, item in receipt.items() if key != "receipt_hash"})
                response = reference.make_event("record_call_response", response_payload, state=state,
                                                idempotency_key=f"IDEM.BAD.{field.upper()}")
                unchanged, result = engine(state, response)
                self.assertEqual(result, "CALL_RESPONSE_CONFLICT")
                self.assertEqual(unchanged, state)

    def test_handoff_catalog_must_include_its_named_target_action(self):
        for engine in self.ENGINES:
            state = reference.initial_state()
            payload = reference.handoff_fixture_payload()
            payload["action_catalog"] = [{
                "action_id": reference.action_id("SCOPE.SHARED", "OBL.PREREQ"),
                "obligation_id": "OBL.PREREQ"}]
            payload["action_catalog_hash"] = reference.sha384(payload["action_catalog"])
            handoff = reference.make_event("open_handoff", payload, state=state)
            unchanged, result = engine(state, handoff)
            self.assertEqual(result, "HANDOFF_OR_TARGET_ILLEGAL")
            self.assertEqual(unchanged, state)

    def test_handoff_rejects_a_reduced_catalog_that_disagrees_with_bound_preimages(self):
        state = reference.initial_state()
        payload = reference.handoff_fixture_payload()
        full_catalog = copy.deepcopy(payload["action_catalog"])
        full_catalog.append({
            "action_id": reference.action_id("SCOPE.SHARED", "OBL.PREREQ"),
            "obligation_id": "OBL.PREREQ",
        })
        manifest = reference.json.loads(payload["manifest_utf8"])
        manifest["action_catalog"] = full_catalog
        manifest["action_catalog_hash"] = reference.sha384(full_catalog)
        manifest["manifest_hash"] = reference.sha384({
            key: value for key, value in manifest.items() if key != "manifest_hash"})
        task = reference.json.loads(payload["task_packet_utf8"])
        task["manifest_hash"] = manifest["manifest_hash"]
        task["requested_action_catalog_hash"] = manifest["action_catalog_hash"]
        task["task_packet_hash"] = reference.sha384({
            key: value for key, value in task.items() if key != "task_packet_hash"})
        payload.update(
            action_catalog=full_catalog,
            action_catalog_hash=manifest["action_catalog_hash"],
            manifest_hash=manifest["manifest_hash"],
            manifest_utf8=reference.canonical_json(manifest).decode("utf-8"),
            task_packet_hash=task["task_packet_hash"],
            task_packet_utf8=reference.canonical_json(task).decode("utf-8"),
        )
        legal = reference.make_event("open_handoff", payload, state=state)
        self.assert_engines(state, legal, "APPLIED")

        forged = copy.deepcopy(payload)
        forged["action_catalog"] = [full_catalog[0]]
        forged["action_catalog_hash"] = reference.sha384(forged["action_catalog"])
        illegal = reference.make_event("open_handoff", forged, state=state)
        outputs = self.assert_engines(state, illegal, "HANDOFF_OR_TARGET_ILLEGAL")
        self.assertTrue(all(output == state for output in outputs))

    def test_response_refs_provider_ids_and_transactions_cannot_alias_other_bytes(self):
        for engine in self.ENGINES:
            state = reference.initial_state()
            first_payload = reference.handoff_fixture_payload()
            first_payload["handoff_id"] = "HANDOFF.ONE"
            first = reference.make_event("open_handoff", first_payload, state=state)
            state, _ = engine(state, first)
            response_one = reference.response_fixture_payload(first_payload)
            recorded = reference.make_event("record_call_response", response_one, state=state)
            state, result = engine(state, recorded)
            self.assertEqual(result, "APPLIED")
            second_payload = reference.handoff_fixture_payload()
            second_payload["handoff_id"] = "HANDOFF.TWO"
            second_payload["originating_cut_hash"] = reference.cut_hash(
                reference.current_cut(state))
            second_payload["canonical_snapshot_hash"] = reference.sha384(
                state["scopes"]["SCOPE.SHARED"]["obligations"])
            second = reference.make_event("open_handoff", second_payload, state=state)
            state, _ = engine(state, second)
            response_two = reference.response_fixture_payload(second_payload)
            worker = reference.json.loads(response_two["raw_response_utf8"])
            worker["produced_at"] = "2026-08-13T00:00:00.000001Z"
            worker["worker_handoff_hash"] = reference.sha384({
                key: item for key, item in worker.items() if key != "worker_handoff_hash"})
            response_two["raw_response_utf8"] = reference.canonical_json(worker).decode("utf-8")
            response_two["raw_response_hash"] = reference.sha384(
                response_two["raw_response_utf8"].encode("utf-8"))
            response_two["worker_handoff_hash"] = worker["worker_handoff_hash"]
            receipt = response_two["durability_receipt"]
            receipt["raw_response_hash"] = response_two["raw_response_hash"]
            receipt["receipt_hash"] = reference.sha384({
                key: item for key, item in receipt.items() if key != "receipt_hash"})
            response = reference.make_event("record_call_response", response_two, state=state,
                                            observed_at="2026-08-13T00:00:00.000001Z")
            unchanged, result = engine(state, response)
            self.assertEqual(result, "CALL_RESPONSE_CONFLICT")
            self.assertEqual(unchanged, state)

    def test_response_receipt_identity_cannot_be_replayed_for_a_second_handoff(self):
        for engine in self.ENGINES:
            state = reference.initial_state()
            first_payload = reference.handoff_fixture_payload()
            first_payload["handoff_id"] = "HANDOFF.ONE"
            state, result = engine(
                state, reference.make_event("open_handoff", first_payload, state=state))
            self.assertEqual(result, "APPLIED")
            response_one = reference.response_fixture_payload(first_payload)
            state, result = engine(
                state, reference.make_event("record_call_response", response_one, state=state))
            self.assertEqual(result, "APPLIED")

            second_payload = reference.handoff_fixture_payload()
            second_payload["handoff_id"] = "HANDOFF.TWO"
            second_payload["originating_cut_hash"] = reference.cut_hash(
                reference.current_cut(state))
            second_payload["canonical_snapshot_hash"] = reference.sha384(
                state["scopes"]["SCOPE.SHARED"]["obligations"])
            state, result = engine(
                state, reference.make_event("open_handoff", second_payload, state=state))
            self.assertEqual(result, "APPLIED")
            replayed_receipt = reference.response_fixture_payload(second_payload)
            unchanged, result = engine(
                state,
                reference.make_event("record_call_response", replayed_receipt, state=state),
            )
            self.assertEqual(result, "CALL_RESPONSE_CONFLICT")
            self.assertEqual(unchanged, state)

    def test_response_timestamps_and_node_stage_are_causal(self):
        for engine in self.ENGINES:
            state = reference.initial_state()
            payload = reference.handoff_fixture_payload()
            handoff = reference.make_event("open_handoff", payload, state=state)
            state, _ = engine(state, handoff)
            response_payload = reference.response_fixture_payload(payload)
            worker = reference.json.loads(response_payload["raw_response_utf8"])
            worker["produced_at"] = "1900-01-01T00:00:00.000000Z"
            worker["worker_handoff_hash"] = reference.sha384({
                key: item for key, item in worker.items() if key != "worker_handoff_hash"})
            response_payload["raw_response_utf8"] = reference.canonical_json(worker).decode("utf-8")
            response_payload["raw_response_hash"] = reference.sha384(
                response_payload["raw_response_utf8"].encode("utf-8"))
            response_payload["worker_handoff_hash"] = worker["worker_handoff_hash"]
            receipt = response_payload["durability_receipt"]
            receipt["raw_response_hash"] = response_payload["raw_response_hash"]
            receipt["receipt_hash"] = reference.sha384({
                key: item for key, item in receipt.items() if key != "receipt_hash"})
            response = reference.make_event("record_call_response", response_payload, state=state)
            unchanged, result = engine(state, response)
            self.assertEqual(result, "CALL_RESPONSE_CONFLICT")
            self.assertEqual(unchanged, state)
            response_payload = reference.response_fixture_payload(payload)
            response_payload["node"] = "A1"
            response = reference.make_event("record_call_response", response_payload, state=state)
            unchanged, result = engine(state, response)
            self.assertEqual(result, "SCHEMA_INVALID")
            self.assertEqual(unchanged, state)

    def test_originating_cut_cannot_claim_future_knowledge(self):
        for engine in self.ENGINES:
            state = reference.initial_state()
            event = reference.make_event("assert_fact", {
                "subject_id": "SUB.X", "predicate_id": "PRED.X", "value_code": "VALUE.X"
            }, state=state, observed_at="2026-08-12T01:00:00.000000Z",
                originating_cut={"journal_seq": 0,
                                 "knowledge_time": "2099-01-01T00:00:00.000000Z",
                                 "valid_time": "2026-08-12T01:00:00.000000Z"})
            unchanged, result = engine(state, event)
            self.assertEqual(result, "ORIGINATING_CUT_INVALID")
            self.assertEqual(unchanged, state)

    def test_retracted_future_fact_does_not_truncate_current_interval(self):
        for engine in self.ENGINES:
            state = reference.initial_state()
            future = reference.make_event("assert_fact", {
                "subject_id": "SUB.TIME", "predicate_id": "PRED.TIME", "value_code": "VALUE.FUTURE"
            }, state=state, valid_from="2026-09-01T00:00:00.000000Z")
            state, _ = engine(state, future)
            retract = reference.make_event("retract_fact", {
                "subject_id": "SUB.TIME", "predicate_id": "PRED.TIME",
                "target_event_id": future["event_id"]
            }, state=state, valid_from="2026-09-01T00:00:00.000000Z",
                originating_cut={"journal_seq": 1, "knowledge_time": reference.T1,
                                 "valid_time": "2026-09-02T00:00:00.000000Z"})
            state, result = engine(state, retract)
            self.assertEqual(result, "APPLIED")
            current = reference.make_event("assert_fact", {
                "subject_id": "SUB.TIME", "predicate_id": "PRED.TIME", "value_code": "VALUE.CURRENT"
            }, state=state, valid_from="2026-08-01T00:00:00.000000Z",
                originating_cut={"journal_seq": 2, "knowledge_time": reference.T1,
                                 "valid_time": "2026-08-15T00:00:00.000000Z"})
            state, result = engine(state, current)
            self.assertEqual(result, "APPLIED")
            rows = state["scopes"]["SCOPE.SHARED"]["facts"][reference.fact_key("SUB.TIME", "PRED.TIME")]
            row = next(item for item in rows if item["value_code"] == "VALUE.CURRENT")
            self.assertIsNone(row["valid_to"])

    def test_commit_rechecks_current_target_state(self):
        for engine in self.ENGINES:
            state = reference.initial_state()
            payload = reference.handoff_fixture_payload()
            handoff = reference.make_event("open_handoff", payload, state=state)
            state, _ = engine(state, handoff)
            response_payload = reference.response_fixture_payload(payload)
            response = reference.make_event("record_call_response", response_payload, state=state)
            state, _ = engine(state, response)
            proposal = reference.make_event("propose_handoff_result", {
                "handoff_id": payload["handoff_id"], "worker_handoff_hash": response_payload["worker_handoff_hash"],
                "originating_cut_hash": payload["originating_cut_hash"],
                "action_ids": [payload["action_catalog"][0]["action_id"]]}, state=state)
            state, result = engine(state, proposal)
            self.assertEqual(result, "APPLIED")
            cancel = reference.make_event("cancel_obligation", {
                "obligation_id": "OBL.SHARED", "cancellation_code": "OWNER_CANCELLED"}, state=state)
            state, result = engine(state, cancel)
            self.assertEqual(result, "APPLIED")
            commit = reference.make_event("commit_handoff_result", {
                "handoff_id": payload["handoff_id"], "proposal_event_id": proposal["event_id"]}, state=state)
            unchanged, result = engine(state, commit)
            self.assertEqual(result, "COMMIT_INVALID")
            self.assertEqual(unchanged, state)

    def test_late_observation_requires_the_exact_current_knowledge_cut(self):
        for engine in self.ENGINES:
            state = reference.initial_state()
            parent = reference.make_event("assert_fact", {
                "subject_id": "SUB.LATE", "predicate_id": "PRED.LATE",
                "value_code": "VALUE.PARENT",
            }, state=state, valid_from="2026-08-01T00:00:00.000000Z")
            state, result = engine(state, parent)
            self.assertEqual(result, "APPLIED")

            first_cut = reference.current_cut(
                state, valid_time="2026-08-10T00:00:00.000000Z")
            first = reference.make_event("correct_fact", {
                "subject_id": "SUB.LATE", "predicate_id": "PRED.LATE",
                "parent_event_id": parent["event_id"], "value_code": "VALUE.FIRST",
            }, state=state, valid_from="2026-08-10T00:00:00.000000Z",
                observed_at="2026-08-13T00:00:00.000001Z",
                originating_cut=first_cut)
            state, result = engine(state, first)
            self.assertEqual(result, "APPLIED")
            self.assertEqual(
                reference.current_cut(state)["knowledge_time"],
                "2026-08-13T00:00:00.000001Z",
            )

            stale_knowledge = reference.make_event("correct_fact", {
                "subject_id": "SUB.LATE", "predicate_id": "PRED.LATE",
                "parent_event_id": parent["event_id"], "value_code": "VALUE.BRANCH",
            }, state=state, valid_from="2026-08-15T00:00:00.000000Z",
                observed_at="2026-08-13T00:00:00.000002Z",
                originating_cut={"journal_seq": 2, "knowledge_time": reference.T1,
                                 "valid_time": "2026-08-15T00:00:00.000000Z"})
            unchanged, result = engine(state, stale_knowledge)
            self.assertEqual(result, "ORIGINATING_CUT_INVALID")
            self.assertEqual(unchanged, state)

            exact = reference.make_event("correct_fact", {
                "subject_id": "SUB.LATE", "predicate_id": "PRED.LATE",
                "parent_event_id": first["event_id"], "value_code": "VALUE.EXACT",
            }, state=state, valid_from="2026-08-15T00:00:00.000000Z",
                observed_at="2026-08-13T00:00:00.000002Z",
                originating_cut=reference.current_cut(
                    state, valid_time="2026-08-15T00:00:00.000000Z"))
            state, result = engine(state, exact)
            self.assertEqual(result, "APPLIED")

    def test_rejection_requires_an_exact_stored_proposal_hash(self):
        for engine in self.ENGINES:
            state = reference.initial_state()
            payload = reference.handoff_fixture_payload()
            opened = reference.make_event("open_handoff", payload, state=state)
            state, result = engine(state, opened)
            self.assertEqual(result, "APPLIED")

            no_proposal = reference.make_event("reject_handoff_result", {
                "handoff_id": payload["handoff_id"],
                "rejection_code": "TRANSITION_ILLEGAL",
                "proposal_hash": "0" * 96,
            }, state=state)
            unchanged, result = engine(state, no_proposal)
            self.assertEqual(result, "REJECTION_INVALID")
            self.assertEqual(unchanged, state)

            response_payload = reference.response_fixture_payload(payload)
            response = reference.make_event(
                "record_call_response", response_payload, state=state)
            state, result = engine(state, response)
            self.assertEqual(result, "APPLIED")
            proposal = reference.make_event("propose_handoff_result", {
                "handoff_id": payload["handoff_id"],
                "worker_handoff_hash": response_payload["worker_handoff_hash"],
                "originating_cut_hash": payload["originating_cut_hash"],
                "action_ids": [payload["action_catalog"][0]["action_id"]],
            }, state=state)
            state, result = engine(state, proposal)
            self.assertEqual(result, "APPLIED")
            exact_hash = reference.sha384(proposal)
            handoff = state["scopes"]["SCOPE.SHARED"]["handoffs"][payload["handoff_id"]]
            self.assertEqual(handoff["proposal_hash"], exact_hash)
            self.assertEqual(state["events"][proposal["event_id"]], exact_hash)

            arbitrary = reference.make_event("reject_handoff_result", {
                "handoff_id": payload["handoff_id"],
                "rejection_code": "TRANSITION_ILLEGAL",
                "proposal_hash": "1" * 96,
            }, state=state)
            unchanged, result = engine(state, arbitrary)
            self.assertEqual(result, "REJECTION_INVALID")
            self.assertEqual(unchanged, state)

            rejection = reference.make_event("reject_handoff_result", {
                "handoff_id": payload["handoff_id"],
                "rejection_code": "TRANSITION_ILLEGAL",
                "proposal_hash": exact_hash,
            }, state=state)
            state, result = engine(state, rejection)
            self.assertEqual(result, "APPLIED")
            handoff = state["scopes"]["SCOPE.SHARED"]["handoffs"][payload["handoff_id"]]
            self.assertEqual(handoff["status"], "REJECTED")
            self.assertEqual(handoff["terminal_disposition"], "TRANSITION_ILLEGAL")

    def test_oracle_semantics_survive_poisoned_shared_and_reference_helpers(self):
        helper_names = (
            "effective_valid_to", "retracted_at", "visible_effective",
            "has_path", "action_targets_legal",
        )
        self.assertTrue(all(not hasattr(common, name) for name in helper_names))
        originals = {name: getattr(reference, name) for name in helper_names}

        def poisoned(*_args, **_kwargs):
            raise AssertionError("oracle crossed the post-admission independence boundary")

        try:
            for name in helper_names:
                setattr(common, name, poisoned)
                setattr(reference, name, poisoned)

            state = common.initial_state()
            future = common.make_event("assert_fact", {
                "subject_id": "SUB.INDEPENDENT", "predicate_id": "PRED.TIME",
                "value_code": "VALUE.FUTURE",
            }, state=state, valid_from="2026-09-01T00:00:00.000000Z")
            state, result = oracle.oracle_apply(state, future)
            self.assertEqual(result, "APPLIED")
            current = common.make_event("assert_fact", {
                "subject_id": "SUB.INDEPENDENT", "predicate_id": "PRED.TIME",
                "value_code": "VALUE.CURRENT",
            }, state=state, valid_from="2026-08-01T00:00:00.000000Z",
                originating_cut=common.current_cut(
                    state, valid_time="2026-08-15T00:00:00.000000Z"))
            state, result = oracle.oracle_apply(state, current)
            self.assertEqual(result, "APPLIED")

            dependency_state = common.initial_state()
            dependency = common.make_event("link_dependency", {
                "obligation_id": "OBL.SHARED",
                "prerequisite_obligation_id": "OBL.PREREQ",
            }, state=dependency_state)
            dependency_state, result = oracle.oracle_apply(dependency_state, dependency)
            self.assertEqual(result, "APPLIED")

            handoff_state = common.initial_state()
            handoff_payload = reference.handoff_fixture_payload()
            opened = common.make_event("open_handoff", handoff_payload,
                                       state=handoff_state)
            handoff_state, result = oracle.oracle_apply(handoff_state, opened)
            self.assertEqual(result, "APPLIED")
            response_payload = reference.response_fixture_payload(handoff_payload)
            response = common.make_event("record_call_response", response_payload,
                                         state=handoff_state)
            handoff_state, result = oracle.oracle_apply(handoff_state, response)
            self.assertEqual(result, "APPLIED")
            proposal = common.make_event("propose_handoff_result", {
                "handoff_id": handoff_payload["handoff_id"],
                "worker_handoff_hash": response_payload["worker_handoff_hash"],
                "originating_cut_hash": handoff_payload["originating_cut_hash"],
                "action_ids": [handoff_payload["action_catalog"][0]["action_id"]],
            }, state=handoff_state)
            handoff_state, result = oracle.oracle_apply(handoff_state, proposal)
            self.assertEqual(result, "APPLIED")
            commit = common.make_event("commit_handoff_result", {
                "handoff_id": handoff_payload["handoff_id"],
                "proposal_event_id": proposal["event_id"],
            }, state=handoff_state)
            _, result = oracle.oracle_apply(handoff_state, commit)
            self.assertEqual(result, "APPLIED")
        finally:
            for name, implementation in originals.items():
                delattr(common, name)
                setattr(reference, name, implementation)

    def test_full_legal_event_matrix_matches_reference_byte_for_byte(self):
        seen: set[str] = set()

        def apply(state: dict, event: dict) -> dict:
            seen.add(event["event_type"])
            return self.assert_engines(state, event, "APPLIED")[0]

        state = reference.initial_state()
        asserted = reference.make_event("assert_fact", {
            "subject_id": "SUB.MATRIX", "predicate_id": "PRED.MATRIX",
            "value_code": "VALUE.ONE",
        }, state=state, valid_from="2026-08-01T00:00:00.000000Z")
        state = apply(state, asserted)
        corrected = reference.make_event("correct_fact", {
            "subject_id": "SUB.MATRIX", "predicate_id": "PRED.MATRIX",
            "parent_event_id": asserted["event_id"], "value_code": "VALUE.TWO",
        }, state=state, valid_from="2026-08-02T00:00:00.000000Z",
            originating_cut=reference.current_cut(
                state, valid_time="2026-08-02T00:00:00.000000Z"))
        state = apply(state, corrected)
        retracted = reference.make_event("retract_fact", {
            "subject_id": "SUB.MATRIX", "predicate_id": "PRED.MATRIX",
            "target_event_id": corrected["event_id"],
        }, state=state, valid_from="2026-08-03T00:00:00.000000Z",
            originating_cut=reference.current_cut(
                state, valid_time="2026-08-03T00:00:00.000000Z"))
        apply(state, retracted)

        state = reference.initial_state()
        obligation_id = "OBL.MATRIX"
        opened_obligation = reference.make_event("open_obligation", {
            "obligation_id": obligation_id, "subject_id": "SUB.MATRIX",
            "owner_role": "WORKER", "due_at": reference.T0, "critical": True,
            "completion_action_id": reference.action_id("SCOPE.SHARED", obligation_id),
            "prerequisite_obligation_ids": [],
        }, state=state)
        state = apply(state, opened_obligation)
        state = apply(state, reference.make_event("reschedule_obligation", {
            "obligation_id": obligation_id, "due_at": reference.T0,
        }, state=state))
        state = apply(state, reference.make_event("delegate_obligation", {
            "obligation_id": obligation_id, "owner_role": "REVIEWER",
        }, state=state))
        state = apply(state, reference.make_event("cancel_obligation", {
            "obligation_id": obligation_id, "cancellation_code": "OWNER_CANCELLED",
        }, state=state))
        state = apply(state, reference.make_event("reopen_obligation", {
            "obligation_id": obligation_id, "due_at": reference.T0,
            "owner_role": "WORKER",
        }, state=state))
        cut = reference.current_cut(state)
        state = apply(state, reference.make_event("complete_obligation", {
            "obligation_id": obligation_id,
            "completion_action_id": reference.action_id("SCOPE.SHARED", obligation_id),
            "originating_cut_hash": reference.cut_hash(cut),
        }, state=state, originating_cut=cut))

        state = reference.initial_state()
        edge = {"obligation_id": "OBL.SHARED",
                "prerequisite_obligation_id": "OBL.PREREQ"}
        state = apply(state, reference.make_event("link_dependency", edge, state=state))
        apply(state, reference.make_event("unlink_dependency", edge, state=state))

        def proposed_handoff() -> tuple[dict, dict, dict]:
            handoff_state = reference.initial_state()
            payload = reference.handoff_fixture_payload()
            handoff_state = apply(handoff_state, reference.make_event(
                "open_handoff", payload, state=handoff_state))
            response_payload = reference.response_fixture_payload(payload)
            handoff_state = apply(handoff_state, reference.make_event(
                "record_call_response", response_payload, state=handoff_state))
            proposal = reference.make_event("propose_handoff_result", {
                "handoff_id": payload["handoff_id"],
                "worker_handoff_hash": response_payload["worker_handoff_hash"],
                "originating_cut_hash": payload["originating_cut_hash"],
                "action_ids": [payload["action_catalog"][0]["action_id"]],
            }, state=handoff_state)
            handoff_state = apply(handoff_state, proposal)
            return handoff_state, payload, proposal

        state, payload, proposal = proposed_handoff()
        apply(state, reference.make_event("commit_handoff_result", {
            "handoff_id": payload["handoff_id"],
            "proposal_event_id": proposal["event_id"],
        }, state=state))
        state, payload, proposal = proposed_handoff()
        state = apply(state, reference.make_event("reject_handoff_result", {
            "handoff_id": payload["handoff_id"],
            "rejection_code": "TRANSITION_ILLEGAL",
            "proposal_hash": reference.sha384(proposal),
        }, state=state))
        apply(state, reference.make_event("close_handoff", {
            "handoff_id": payload["handoff_id"],
        }, state=state))

        self.assertEqual(seen, set(reference.EVENT_OPERATIONS))


if __name__ == "__main__":
    unittest.main()
