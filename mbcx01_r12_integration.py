"""Executable joins between r12 state, cohort, packets, and inference."""

from __future__ import annotations

import copy
from typing import Any

import mbcx01_r12_inference as inference
import mbcx01_r12_measurement as measurement
import mbcx01_r12_packets as packets
import mbcx01_r12_state_oracle as state_oracle
import mbcx01_r12_state_reference as state


def joined_scenario_fixture() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    candidates, provenance = measurement.synthetic_candidates_r12()
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


def build_joined_execution() -> dict[str, Any]:
    """Build one causal chain; the scored child is the child actually replayed here."""
    current, manifest, source = joined_scenario_fixture()
    scoring = packets.build_scoring_fixture(
        manifest, "OM", authoritative_state=current)
    authority = scoring["transition_authority"]
    actual_child = copy.deepcopy(authority["applied_child_event"])
    exact_prestate = copy.deepcopy(authority["precommit_state"])
    ref_post, ref_result = state.reference_apply(
        copy.deepcopy(exact_prestate), actual_child)
    ora_post, ora_result = state_oracle.oracle_apply(
        copy.deepcopy(exact_prestate), actual_child)
    if (ref_result != "APPLIED" or ora_result != "APPLIED"
            or ref_post != ora_post
            or ref_post != authority["postcommit_state"]):
        raise AssertionError("dual state reducers did not apply the authoritative child exactly")
    return {
        "initial_state": current,
        "manifest": manifest,
        "source": source,
        "scoring": scoring,
        "actual_child_event": actual_child,
        "actual_poststate": ref_post,
        "reference_result": ref_result,
        "oracle_result": ora_result,
    }


def execution_binding_matches(scoring: dict[str, Any], actual_child_event: dict[str, Any],
                              actual_poststate: dict[str, Any]) -> bool:
    """Check the packet, receipt, A1 cut, and both reducers name one exact execution."""
    try:
        manifest = scoring["manifest"]
        authority = scoring["transition_authority"]
        receipt = scoring["writer_receipt"]
        prestate = authority["precommit_state"]
        ref_post, ref_result = state.reference_apply(
            copy.deepcopy(prestate), copy.deepcopy(actual_child_event))
        ora_post, ora_result = state_oracle.oracle_apply(
            copy.deepcopy(prestate), copy.deepcopy(actual_child_event))
        exact_cut = state.current_cut(actual_poststate)
        return (packets.score_exact(manifest, scoring) == 1
                and ref_result == "APPLIED" and ora_result == "APPLIED"
                and ref_post == ora_post == actual_poststate
                and authority["applied_child_event"] == actual_child_event
                and authority["applied_child_event_hash"] == state.sha384(actual_child_event)
                and authority["postcommit_state"] == actual_poststate
                and authority["postcommit_state_hash"] == state.sha384(actual_poststate)
                and authority["postcommit_cut"] == exact_cut
                and receipt["child_events"] == [actual_child_event]
                and receipt["applied_child_event_hash"] == state.sha384(actual_child_event)
                and receipt["postcommit_state_hash"] == state.sha384(actual_poststate)
                and receipt["postcommit_cut"] == exact_cut
                and scoring["a1_packet"]["cut"] == exact_cut)
    except (AttributeError, KeyError, TypeError, ValueError):
        return False


def verify_pipeline_join() -> dict[str, Any]:
    execution = build_joined_execution()
    manifest = execution["manifest"]
    source = execution["source"]
    scoring = execution["scoring"]
    after = execution["actual_poststate"]
    applied_event = execution["actual_child_event"]
    result = execution["reference_result"]
    if packets.validate_expected_manifest(manifest):
        raise AssertionError("joined manifest is invalid")
    selected_ids = source["selected_ids"]
    if manifest["scenario_id"] not in selected_ids:
        raise AssertionError("packet scenario absent from retained manifest")
    if packets.score_exact(manifest, scoring) != 1:
        raise AssertionError("joined packet did not score")
    if result != "APPLIED" or after["scopes"]["SCOPE.SHARED"]["obligations"][
            "OBL.SHARED"]["lifecycle"] != "COMPLETED":
        raise AssertionError("writer receipt did not drive the state transition")
    if (not execution_binding_matches(scoring, applied_event, after)
            or scoring["writer_receipt"]["child_events"] != [applied_event]
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
            "action_catalog_bound": True, "durability_schema_joined": True,
            "proposal_authority_bound": True, "dual_reducer_replay_bound": True,
            "postcommit_state_hash_bound": True}
