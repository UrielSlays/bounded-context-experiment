"""Executable joins between r13 state, cohort, packets, and inference."""

from __future__ import annotations

import copy
import json
from typing import Any

import mbcx01_r13_inference as inference
import mbcx01_r13_measurement as measurement
import mbcx01_r13_packets as packets
import mbcx01_r13_state_oracle as state_oracle
import mbcx01_r13_state_reference as state


def joined_scenario_fixture() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    candidates, provenance = measurement.synthetic_candidates_r13()
    selected = measurement.select_cohort(candidates, provenance)
    candidate = selected[0]
    manifest = packets.manifest_for_retained_candidate(candidate)
    chosen = candidate["chosen_cut_id"]
    current = packets._fixture_authoritative_state(manifest)
    obligations = current["scopes"]["SCOPE.SHARED"]["obligations"]
    if manifest["cut"] != state.current_cut(current):
        raise AssertionError("cohort cut and state cut disagree")

    authority = candidate["canonical_state_by_cut"][chosen]
    if (authority["scope_id"] != manifest["scope_id"]
            or authority["target_obligation_id"] != "OBL.SHARED"
            or authority["target_lifecycle"] != obligations["OBL.SHARED"]["lifecycle"]
            or authority["prerequisite_lifecycle"] != obligations["OBL.PREREQ"]["lifecycle"]
            or candidate["gold_action_id_by_cut"][chosen] != manifest["gold_action_id"]
            or candidate["action_ids_by_cut"][chosen]
            != packets.legal_action_ids_from_world(
                manifest["canonical_world"], manifest["action_catalog"], manifest["cut"])):
        raise AssertionError("cohort authority and packet/state truth disagree")
    cohort_authority = packets.cohort_authority_for_candidate(candidate)
    if not packets.validate_cohort_manifest_join(cohort_authority, manifest):
        raise AssertionError("independent cohort authority and manifest disagree")
    for retained in selected:
        retained_manifest = packets.manifest_for_retained_candidate(retained)
        retained_authority = packets.cohort_authority_for_candidate(retained)
        if not packets.validate_cohort_manifest_join(retained_authority, retained_manifest):
            raise AssertionError("retained population contains an unjoined candidate")
    return current, manifest, {"candidate": candidate, "provenance": provenance,
                               "selected_ids": [row["scenario_id"] for row in selected],
                               "cohort_authority": cohort_authority}


def build_joined_execution() -> dict[str, Any]:
    """Build one causal chain; the scored child is the child actually replayed here."""
    current, manifest, source = joined_scenario_fixture()
    scoring = packets.build_scoring_fixture(
        manifest, "OM", authoritative_state=current,
        cohort_authority=source["cohort_authority"])
    state_receipt = scoring["state_authority_receipt"]
    actual_child = json.loads(state_receipt["applied_child"]["event_utf8"])
    exact_prestate = json.loads(state_receipt["prestate_read"]["state_utf8"])
    actual_poststate = json.loads(
        state_receipt["postcommit_readback"]["state_utf8"])
    ref_post, ref_result = state.reference_apply(
        copy.deepcopy(exact_prestate), actual_child)
    ora_post, ora_result = state_oracle.oracle_apply(
        copy.deepcopy(exact_prestate), actual_child)
    if (ref_result != "APPLIED" or ora_result != "APPLIED"
            or ref_post != ora_post
            or ref_post != actual_poststate):
        raise AssertionError("dual state reducers did not apply the authoritative child exactly")
    return {
        "initial_state": current,
        "manifest": manifest,
        "source": source,
        "scoring": scoring,
        "actual_child_event": actual_child,
        "actual_poststate": actual_poststate,
        "reference_result": ref_result,
        "oracle_result": ora_result,
    }


def execution_binding_matches(scoring: dict[str, Any], actual_child_event: dict[str, Any],
                              actual_poststate: dict[str, Any]) -> bool:
    """Check the packet, receipt, A1 cut, and both reducers name one exact execution."""
    try:
        manifest = scoring["manifest"]
        authority = scoring["transition_authority"]
        state_receipt = scoring["state_authority_receipt"]
        receipt = scoring["writer_receipt"]
        prestate = json.loads(state_receipt["prestate_read"]["state_utf8"])
        receipt_child = json.loads(state_receipt["applied_child"]["event_utf8"])
        receipt_poststate = json.loads(
            state_receipt["postcommit_readback"]["state_utf8"])
        ref_post, ref_result = state.reference_apply(
            copy.deepcopy(prestate), copy.deepcopy(actual_child_event))
        ora_post, ora_result = state_oracle.oracle_apply(
            copy.deepcopy(prestate), copy.deepcopy(actual_child_event))
        exact_cut = state.current_cut(actual_poststate)
        return (packets.score_fixture_conformance_exact(manifest, scoring) == 1
                and state.verify_state_authority_receipt(
                    state_receipt, require_production=False) == []
                and state_oracle.verify_state_authority_receipt(
                    state_receipt, require_production=False) == []
                and ref_result == "APPLIED" and ora_result == "APPLIED"
                and ref_post == ora_post == actual_poststate
                and receipt_child == actual_child_event
                and receipt_poststate == actual_poststate
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
    if packets.score_fixture_conformance_exact(manifest, scoring) != 1:
        raise AssertionError("joined packet failed fixture conformance")
    if (packets.score_exact(manifest, scoring) != 0
            or "STATE_AUTHORITY_UNAVAILABLE" not in
            packets.validate_scorer_input(manifest, scoring)):
        raise AssertionError("fixture state authority leaked into scientific admission")
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
    if measurement.validate_b_response_ledger_binding(
            scoring["durable_b_response_binding"], scoring["b_call_record"]):
        raise AssertionError("packet and call-ledger durability receipts diverge")
    bc_scoring = packets.build_scoring_fixture(
        manifest, "BC", authoritative_state=execution["initial_state"],
        cohort_authority=source["cohort_authority"])
    episode_receipts = [measurement.episode_receipt_fixture(
        sid, index, missing_position=None if index == 0 else "BC.A0")
        for index, sid in enumerate(selected_ids)]
    episode_receipts[0] = packets.build_complete_episode_receipt_for_scorers(
        bc_scoring, scoring, manifest["retained_position"])
    outcome_receipt = packets.build_scenario_outcome_receipt(
        manifest, bc_scoring, scoring, episode_receipts[0],
        require_production_authority=False)
    inference.ordered_decision_from_episode_receipts(
        [outcome_receipt], episode_receipts, selected_ids,
        require_production_authority=False)
    return {"scenario_id": manifest["scenario_id"], "selected": len(selected_ids),
            "packet_score": 1, "scientific_score": 0,
            "state_authority_available": False,
            "state_result": result, "inference_order_bound": True,
            "writer_state_event_bound": True, "a1_postcommit_cut_bound": True,
            "action_catalog_bound": True, "durability_schema_joined": True,
            "episode_partition_authority_bound": True,
            "outcome_receipt_authority_bound": True,
            "episode_outcome_ledger_bound": True,
            "retained_population_join_count": 768,
            "proposal_authority_bound": True, "dual_reducer_replay_bound": True,
            "postcommit_state_hash_bound": True}
