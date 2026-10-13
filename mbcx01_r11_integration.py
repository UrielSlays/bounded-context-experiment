"""Executable joins between r11 state, cohort, packets, and inference."""

from __future__ import annotations

import copy
from typing import Any

import mbcx01_r11_inference as inference
import mbcx01_r11_measurement as measurement
import mbcx01_r11_packets as packets
import mbcx01_r11_state_reference as state


def joined_scenario_fixture() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    candidates, provenance = measurement.synthetic_candidates_r11()
    selected = measurement.select_cohort(candidates, provenance)
    current = state.initial_state()
    complete = state.make_event("complete_obligation", {
        "obligation_id": "OBL.PREREQ",
        "completion_action_id": state.action_id("SCOPE.SHARED", "OBL.PREREQ"),
        "originating_cut_hash": state.cut_hash(state.current_cut(current)),
    }, state=current)
    current, result = state.reference_apply(current, complete)
    if result != "APPLIED":
        raise AssertionError("joined prerequisite fixture failed")

    manifest = packets.packet_fixture_manifest()
    candidate = selected[0]
    manifest["scenario_id"] = candidate["scenario_id"]
    obligations = current["scopes"]["SCOPE.SHARED"]["obligations"]
    chosen = candidate["chosen_cut_id"]
    manifest["cut"] = {key: value for key, value in candidate["cut_by_id"][chosen].items()
                       if key != "cut_id"}
    if manifest["cut"] != state.current_cut(current):
        raise AssertionError("cohort cut and state cut disagree")
    for row in manifest["canonical_world"]:
        if row["object_kind"] == "OBLIGATION" and row["object_id"] in obligations:
            source = obligations[row["object_id"]]
            row["fields"] = {key: copy.deepcopy(source[key]) for key in
                             ("lifecycle", "critical", "due_at", "completion_action_id",
                              "prerequisite_obligation_ids")}
    manifest["canonical_world_hash"] = state.sha384(manifest["canonical_world"])
    manifest["gold_read_set"] = packets._expected_gold_read_set(
        manifest, manifest["gold_action_id"])
    manifest["manifest_hash"] = packets.hash_without(manifest, "manifest_hash")

    authority = candidate["canonical_state_by_cut"][chosen]
    if (authority["scope_id"] != manifest["scope_id"]
            or authority["target_obligation_id"] != "OBL.SHARED"
            or authority["target_lifecycle"] != obligations["OBL.SHARED"]["lifecycle"]
            or authority["prerequisite_lifecycle"] != obligations["OBL.PREREQ"]["lifecycle"]
            or candidate["gold_action_id_by_cut"][chosen] != manifest["gold_action_id"]):
        raise AssertionError("cohort authority and packet/state truth disagree")
    return current, manifest, {"candidate": candidate, "provenance": provenance,
                               "selected_ids": [row["scenario_id"] for row in selected]}


def apply_scoring_child(state_before: dict[str, Any], manifest: dict[str, Any],
                        scoring: dict[str, Any]) -> tuple[dict[str, Any], str, dict[str, Any]]:
    target_action = manifest["gold_action_id"]
    target = next(row["obligation_id"] for row in manifest["action_catalog"]
                  if row.get("action_id") == target_action)
    handoff_payload = {
        "handoff_id": f"HANDOFF.{scoring['condition']}",
        "scenario_id": manifest["scenario_id"], "condition": scoring["condition"],
        "target_obligation_id": target,
        "task_packet_hash": scoring["task_packet"]["task_packet_hash"],
        "served_request_hash": scoring["worker_handoff"]["served_request_hash"],
        "request_parameters_hash": scoring["b_call_record"]["request_parameters_hash"],
        "idempotency_token": scoring["b_call_record"]["idempotency_token"],
        "task_packet_utf8": state.canonical_json(scoring["task_packet"]).decode("utf-8"),
        "manifest_utf8": state.canonical_json(manifest).decode("utf-8"),
        "originating_cut_hash": state.cut_hash(state.current_cut(state_before)),
        "action_catalog_hash": manifest["action_catalog_hash"],
        "canonical_snapshot_hash": state.sha384(
            state_before["scopes"]["SCOPE.SHARED"]["obligations"]),
        "route_contract_hash": manifest["route_contract_hash"],
        "manifest_hash": manifest["manifest_hash"],
        "action_catalog": copy.deepcopy(manifest["action_catalog"]),
    }
    working = copy.deepcopy(state_before)
    opened = state.make_event("open_handoff", handoff_payload, state=working)
    working, result = state.reference_apply(working, opened)
    if result != "APPLIED":
        return working, result, {}
    response = {
        "handoff_id": handoff_payload["handoff_id"], "scenario_id": manifest["scenario_id"],
        "condition": scoring["condition"], "node": "B",
        "task_packet_hash": scoring["task_packet"]["task_packet_hash"],
        "served_request_hash": scoring["worker_handoff"]["served_request_hash"],
        "request_parameters_hash": scoring["b_call_record"]["request_parameters_hash"],
        "idempotency_token": scoring["b_call_record"]["idempotency_token"],
        "raw_response_utf8": scoring["b_call_record"]["raw_response_utf8"],
        "raw_response_hash": scoring["b_call_record"]["raw_response_hash"],
        "worker_handoff_hash": scoring["worker_handoff"]["worker_handoff_hash"],
        "response_ref": scoring["b_call_record"]["response_ref"],
        "provider_request_id": scoring["b_call_record"]["provider_request_id"],
        "durability_receipt": copy.deepcopy(scoring["b_call_record"]["durability_receipt"]),
        "route_contract_hash": manifest["route_contract_hash"], "accepted_at": state.T1,
    }
    recorded = state.make_event("record_call_response", response, state=working)
    working, result = state.reference_apply(working, recorded)
    if result != "APPLIED":
        return working, result, {}
    proposed = state.make_event("propose_handoff_result", {
        "handoff_id": handoff_payload["handoff_id"],
        "worker_handoff_hash": scoring["worker_handoff"]["worker_handoff_hash"],
        "originating_cut_hash": handoff_payload["originating_cut_hash"],
        "action_ids": [target_action],
    }, state=working)
    working, result = state.reference_apply(working, proposed)
    if result != "APPLIED":
        return working, result, {}
    committed = state.make_event("commit_handoff_result", {
        "handoff_id": handoff_payload["handoff_id"], "proposal_event_id": proposed["event_id"]
    }, state=working)
    after, result = state.reference_apply(working, committed)
    return after, result, committed


def verify_pipeline_join() -> dict[str, Any]:
    current, manifest, source = joined_scenario_fixture()
    if packets.validate_expected_manifest(manifest):
        raise AssertionError("joined manifest is invalid")
    selected_ids = source["selected_ids"]
    if manifest["scenario_id"] not in selected_ids:
        raise AssertionError("packet scenario absent from retained manifest")
    preliminary = packets.build_scoring_fixture(manifest, "OM")
    preliminary_after, preliminary_result, committed = apply_scoring_child(
        current, manifest, preliminary)
    if preliminary_result != "APPLIED":
        raise AssertionError("preliminary state transition failed")
    postcommit_cut = state.current_cut(preliminary_after)
    scoring = packets.build_scoring_fixture(
        manifest, "OM", writer_child_event=committed, postcommit_cut=postcommit_cut)
    if packets.score_exact(manifest, scoring) != 1:
        raise AssertionError("joined packet did not score")
    after, result, applied_event = apply_scoring_child(current, manifest, scoring)
    if result != "APPLIED" or after["scopes"]["SCOPE.SHARED"]["obligations"][
            "OBL.SHARED"]["lifecycle"] != "COMPLETED":
        raise AssertionError("writer receipt did not drive the state transition")
    if (scoring["writer_receipt"]["child_events"] != [applied_event]
            or scoring["writer_receipt"]["postcommit_cut"] != state.current_cut(after)
            or scoring["a1_packet"]["cut"] != state.current_cut(after)
            or scoring["task_packet"]["requested_action_catalog_hash"]
            != manifest["action_catalog_hash"]
            or state.sha384(manifest["action_catalog"])
            != manifest["action_catalog_hash"]):
        raise AssertionError("state writer/A1/catalog edge is not exact")
    b_call = scoring["b_call_record"]
    ledger = measurement.CallLedger.prepare(
        b_call["scenario_id"], b_call["condition"], b_call["node"],
        b_call["task_packet_hash"], b_call["served_request_hash"],
        b_call["request_parameters_hash"], b_call["idempotency_token"],
        b_call["route_contract_hash"])
    ledger = ledger.transition("DISPATCH_CONFIRMED")
    ledger = ledger.transition(
        "RESPONSE_BYTES_FSYNCED", response_bytes=b_call["raw_response_utf8"].encode("utf-8"),
        response_ref=b_call["response_ref"], provider_request_id=b_call["provider_request_id"],
        durability_receipt=b_call["durability_receipt"])
    if ledger.durability_receipt != b_call["durability_receipt"]:
        raise AssertionError("packet and call-ledger durability receipts diverge")
    rows = [{"scenario_id": sid, "bc": 1, "om": 1} for sid in selected_ids]
    inference.ordered_paired_intervals(rows, selected_ids)
    return {"scenario_id": manifest["scenario_id"], "selected": len(selected_ids),
            "packet_score": 1, "state_result": result, "inference_order_bound": True,
            "writer_state_event_bound": True, "a1_postcommit_cut_bound": True,
            "action_catalog_bound": True, "durability_schema_joined": True}
