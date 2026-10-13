"""Typed r13 packet graph and exact causal scorer. No provider calls."""

from __future__ import annotations

import copy
import base64
import json
from typing import Any

from mbcx01_r13_common import (SHA384, T0, T1, _valid_utc, action_id, canonical_json,
                               make_durability_receipt, sha256, sha384,
                               valid_durability_receipt)
import mbcx01_r13_state_oracle as state_oracle
import mbcx01_r13_state_reference as state_reference
import mbcx01_r13_measurement as measurement


ENVELOPE_BYTES = 65536


def hash_without(record: dict[str, Any], field: str) -> str:
    return sha384({key: value for key, value in record.items() if key != field})


def _canonical_event_id(event: dict[str, Any]) -> str:
    return "EV." + sha256({key: value for key, value in event.items() if key != "event_id"})


def _world_map(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["object_id"]: row for row in manifest.get("canonical_world", [])
            if isinstance(row, dict) and "object_id" in row}


def _unique_gold_action(manifest: dict[str, Any]) -> str | None:
    world = _world_map(manifest)
    actions = []
    for entry in manifest.get("action_catalog", []):
        if entry.get("action_kind") != "ACT_ON_OBLIGATION":
            continue
        obligation = world.get(entry.get("obligation_id"))
        fields = obligation.get("fields", {}) if obligation else {}
        prereqs = fields.get("prerequisite_obligation_ids", [])
        legal = (obligation and obligation.get("object_kind") == "OBLIGATION"
                 and entry.get("scope_id") == manifest.get("scope_id")
                 and entry.get("action_id") == action_id(manifest["scope_id"], entry["obligation_id"])
                 and fields.get("lifecycle") == "OPEN" and fields.get("critical") is True
                 and fields.get("due_at", "") <= manifest.get("cut", {}).get("valid_time", "")
                 and all(world.get(pid, {}).get("fields", {}).get("lifecycle") == "COMPLETED"
                         for pid in prereqs))
        if legal:
            actions.append(entry["action_id"])
    return actions[0] if len(actions) == 1 else None


def _expected_gold_read_set(manifest: dict[str, Any], gold: str) -> list[str]:
    world = _world_map(manifest)
    action = next(row for row in manifest["action_catalog"] if row.get("action_id") == gold)
    target = action["obligation_id"]
    ids = {target}
    ids.update(world[target]["fields"].get("prerequisite_obligation_ids", []))
    ids.update(row["object_id"] for row in manifest["canonical_world"]
               if row["object_kind"] == "DEPENDENCY" and row["fields"].get("obligation_id") == target)
    ids.update(row["object_id"] for row in manifest["canonical_world"]
               if row["object_kind"] == "OBSERVATION")
    return sorted(ids, key=lambda value: value.encode("utf-8"))


def project_state_world(state: dict[str, Any], manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """Project only registered experiment objects from one exact state snapshot."""
    scope = state["scopes"][manifest["scope_id"]]
    obligations = scope["obligations"]
    dependencies = scope["dependencies"]
    registered_obligations = {row["object_id"] for row in manifest["canonical_world"]
                              if row["object_kind"] == "OBLIGATION"}
    registered_dependencies = sorted([
        [row["fields"]["obligation_id"], row["fields"]["prerequisite_obligation_id"]]
        for row in manifest["canonical_world"] if row["object_kind"] == "DEPENDENCY"])
    if set(obligations) != registered_obligations or sorted(dependencies) != registered_dependencies:
        raise ValueError("MANIFEST_STATE_PROJECTION_MISMATCH")
    projected = []
    for source in manifest["canonical_world"]:
        row = copy.deepcopy(source)
        if row["object_kind"] == "OBLIGATION":
            obligation = obligations[row["object_id"]]
            row["fields"] = {key: copy.deepcopy(obligation[key]) for key in (
                "subject_id", "owner_role",
                "lifecycle", "critical", "due_at", "completion_action_id",
                "prerequisite_obligation_ids")}
        elif row["object_kind"] == "DEPENDENCY":
            fields = row["fields"]
            if [fields["obligation_id"], fields["prerequisite_obligation_id"]] not in dependencies:
                raise ValueError("MANIFEST_STATE_PROJECTION_MISMATCH")
        projected.append(row)
    projected.sort(key=lambda row: row["object_id"].encode("utf-8"))
    return projected


def legal_action_ids_from_world(world: list[dict[str, Any]],
                                action_catalog: list[dict[str, Any]],
                                cut: dict[str, Any]) -> list[str]:
    objects = {row["object_id"]: row for row in world}
    legal = []
    for action in action_catalog:
        if action.get("action_kind") != "ACT_ON_OBLIGATION":
            continue
        obligation = objects.get(action.get("obligation_id"), {})
        fields = obligation.get("fields", {})
        if (obligation.get("object_kind") == "OBLIGATION"
                and fields.get("lifecycle") == "OPEN"
                and fields.get("critical") is True
                and fields.get("due_at", "") <= cut["valid_time"]
                and all(objects.get(prereq, {}).get("fields", {}).get("lifecycle") == "COMPLETED"
                        for prereq in fields.get("prerequisite_obligation_ids", []))):
            legal.append(action["action_id"])
    return sorted(legal, key=lambda value: value.encode("utf-8"))


def cohort_authority_for_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    """Resolve authority from the pinned retained source, never from manifest content."""
    matches = [row for row in measurement._pinned_retained_source()[0]
               if row["scenario_id"] == manifest.get("scenario_id")]
    if len(matches) != 1:
        raise ValueError("RETAINED_SCENARIO_AUTHORITY_INVALID")
    return measurement.retained_scenario_authority(matches[0])


def cohort_authority_for_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    return measurement.retained_scenario_authority(candidate)


def validate_cohort_manifest_join(authority: Any, manifest: dict[str, Any]) -> bool:
    if measurement.validate_retained_scenario_authority(authority):
        return False
    try:
        candidate = authority["candidate_record"]
        chosen = candidate["chosen_cut_id"]
        cut = {key: copy.deepcopy(value) for key, value in candidate["cut_by_id"][chosen].items()
               if key != "cut_id"}
        return (
            manifest["scenario_id"] == candidate["scenario_id"]
            and manifest["motif"] == candidate["motif"]
            and manifest["cut"] == cut
            and manifest["scope_id"] == candidate["canonical_state_by_cut"][chosen]["scope_id"]
            and manifest["canonical_world"] == candidate["canonical_world_by_cut"][chosen]
            and manifest["observation"] == candidate["observation_by_cut"][chosen]
            and legal_action_ids_from_world(manifest["canonical_world"],
                                            manifest["action_catalog"], manifest["cut"])
            == candidate["action_ids_by_cut"][chosen]
            and manifest["gold_action_id"] == candidate["gold_action_id_by_cut"][chosen]
            and manifest["source_candidate_hash"] == authority["candidate_hash"]
            and manifest["source_provenance_hash"] == authority["source_provenance_hash"]
            and manifest["retained_set_root"] == authority["retained_set_root"]
            and manifest["retained_position"] == authority["retained_position"])
    except (KeyError, TypeError, ValueError):
        return False


def manifest_for_retained_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    authority = measurement.retained_scenario_authority(candidate)
    chosen = candidate["chosen_cut_id"]
    cut = {key: copy.deepcopy(value) for key, value in candidate["cut_by_id"][chosen].items()
           if key != "cut_id"}
    scope = "SCOPE.SHARED"
    target_action = action_id(scope, "OBL.SHARED")
    decoy_action = action_id(scope, "OBL.DECOY")
    world = copy.deepcopy(candidate["canonical_world_by_cut"][chosen])
    actions = [
        {"action_id": decoy_action, "action_kind": "ACT_ON_OBLIGATION",
         "scope_id": scope, "obligation_id": "OBL.DECOY"},
        {"action_id": target_action, "action_kind": "ACT_ON_OBLIGATION",
         "scope_id": scope, "obligation_id": "OBL.SHARED"},
        {"action_id": "NO_ACTION", "action_kind": "NO_ACTION"},
    ]
    actions.sort(key=lambda row: row["action_id"].encode("utf-8"))
    manifest = {
        "schema_id": "ExpectedScenarioManifestV3", "scenario_id": candidate["scenario_id"],
        "scope_id": scope, "motif": candidate["motif"],
        "cut": cut,
        "observation": copy.deepcopy(candidate["observation_by_cut"][chosen]),
        "canonical_world": world, "canonical_world_hash": sha384(world),
        "action_catalog": actions, "action_catalog_hash": sha384(actions),
        "route_contract_hash": "D" * 96,
        "candidate_selector_id": "SELECTOR.FD.V1",
        "bc_selected_object_ids": ["OBL.SHARED", "OBS.SHARED"],
        "bc_selection_hash": "", "gold_read_set": [], "gold_action_id": target_action,
        "expected_a1_action_ids": [],
        "source_candidate_hash": authority["candidate_hash"],
        "source_provenance_hash": authority["source_provenance_hash"],
        "retained_set_root": authority["retained_set_root"],
        "retained_position": authority["retained_position"],
    }
    manifest["bc_selection_hash"] = sha384([
        manifest["candidate_selector_id"], manifest["bc_selected_object_ids"]])
    manifest["gold_read_set"] = _expected_gold_read_set(manifest, target_action)
    manifest["manifest_hash"] = hash_without(manifest, "manifest_hash")
    return manifest


def packet_fixture_manifest() -> dict[str, Any]:
    return manifest_for_retained_candidate(measurement._pinned_retained_source()[0][0])


MANIFEST_KEYS = {"schema_id", "scenario_id", "scope_id", "motif", "cut", "observation",
                 "canonical_world", "canonical_world_hash", "action_catalog", "action_catalog_hash",
                 "route_contract_hash",
                 "candidate_selector_id", "bc_selected_object_ids", "bc_selection_hash",
                 "gold_read_set", "gold_action_id", "expected_a1_action_ids",
                 "source_candidate_hash", "source_provenance_hash", "retained_set_root",
                 "retained_position", "manifest_hash"}


def validate_expected_manifest(manifest: Any) -> list[str]:
    errors: set[str] = set()
    if not isinstance(manifest, dict) or set(manifest) != MANIFEST_KEYS:
        return ["MANIFEST_SCHEMA_INVALID"]
    if (manifest.get("schema_id") != "ExpectedScenarioManifestV3"
            or manifest.get("motif") not in measurement.MOTIFS
            or any(SHA384.fullmatch(str(manifest.get(name, ""))) is None for name in
                   ("source_candidate_hash", "source_provenance_hash", "retained_set_root"))
            or not isinstance(manifest.get("retained_position"), int)
            or isinstance(manifest.get("retained_position"), bool)
            or not 0 <= manifest["retained_position"] < 768):
        errors.add("MANIFEST_SCHEMA_INVALID")
    world = manifest.get("canonical_world")
    if not isinstance(world, list) or any(not isinstance(row, dict)
                                          or set(row) != {"object_id", "object_kind", "fields", "source_event_ids"}
                                          for row in world):
        errors.add("MANIFEST_SCHEMA_INVALID")
        world = []
    ids = [row.get("object_id") for row in world]
    if len(ids) != len(set(ids)):
        errors.add("DUPLICATE_OBJECT_ID")
    if manifest.get("canonical_world_hash") != sha384(world):
        errors.add("CANONICAL_WORLD_HASH_MISMATCH")
    if manifest.get("action_catalog_hash") != sha384(manifest.get("action_catalog")):
        errors.add("ACTION_CATALOG_HASH_MISMATCH")
    if (not isinstance(manifest.get("route_contract_hash"), str)
            or SHA384.fullmatch(manifest["route_contract_hash"]) is None):
        errors.add("ROUTE_CONTRACT_INVALID")
    if manifest.get("bc_selection_hash") != sha384([
            manifest.get("candidate_selector_id"), manifest.get("bc_selected_object_ids")]):
        errors.add("BC_SELECTION_HASH_MISMATCH")
    if any(name not in set(ids) for name in manifest.get("bc_selected_object_ids", [])):
        errors.add("BC_SELECTION_INVALID")
    gold = _unique_gold_action(manifest)
    if gold is None or manifest.get("gold_action_id") != gold:
        errors.add("GOLD_ACTION_INVALID")
    elif manifest.get("gold_read_set") != _expected_gold_read_set(manifest, gold):
        errors.add("GOLD_READ_SET_INVALID")
    if manifest.get("expected_a1_action_ids") != []:
        errors.add("EXPECTED_A1_INVALID")
    if manifest.get("manifest_hash") != hash_without(manifest, "manifest_hash"):
        errors.add("MANIFEST_HASH_MISMATCH")
    return sorted(errors)


def _object_closure(manifest: dict[str, Any], selected: list[str]) -> list[str]:
    world = _world_map(manifest)
    result = set(selected)
    result.update(row["obligation_id"] for row in manifest["action_catalog"]
                  if row.get("action_kind") == "ACT_ON_OBLIGATION")
    changed = True
    while changed:
        changed = False
        for object_id in list(result):
            row = world.get(object_id)
            if row and row["object_kind"] == "OBLIGATION":
                for prereq in row["fields"].get("prerequisite_obligation_ids", []):
                    if prereq not in result:
                        result.add(prereq); changed = True
    if any(name not in world for name in result):
        raise ValueError("selected object absent from manifest")
    return sorted(result, key=lambda value: value.encode("utf-8"))


def build_decision_packet(manifest: dict[str, Any], condition: str, stage: str,
                          *, postcommit_cut: dict[str, Any] | None = None,
                          source_world: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    if validate_expected_manifest(manifest):
        raise ValueError("invalid expected manifest")
    if condition not in {"BC", "OM"} or stage not in {"A0_PRECOMMIT", "A1_POSTCOMMIT"}:
        raise ValueError("invalid condition or stage")
    selected = (manifest["bc_selected_object_ids"] if condition == "BC" else manifest["gold_read_set"])
    ids = _object_closure(manifest, selected)
    if stage == "A1_POSTCOMMIT" and source_world is None:
        raise ValueError("authoritative postcommit world required")
    source_world_map = _world_map(manifest) if source_world is None else {
        row["object_id"]: row for row in source_world}
    packet = {
        "schema_id": "DecisionPacketV5", "stage": stage, "condition": condition,
        "scenario_id": manifest["scenario_id"], "scope_id": manifest["scope_id"],
        "cut": copy.deepcopy(postcommit_cut if stage == "A1_POSTCOMMIT" else manifest["cut"]),
        "objects": [copy.deepcopy(source_world_map[name]) for name in ids],
        "action_catalog": copy.deepcopy(manifest["action_catalog"]),
        "observation": copy.deepcopy(manifest["observation"]),
        "manifest_hash": manifest["manifest_hash"],
    }
    packet["packet_hash"] = hash_without(packet, "packet_hash")
    return packet


def render_served_input(packet: dict[str, Any]) -> bytes:
    encoded = canonical_json(packet)
    if len(encoded) > ENVELOPE_BYTES:
        raise ValueError("PACKET_ENVELOPE_EXCEEDED")
    return encoded + b" " * (ENVELOPE_BYTES - len(encoded))


def served_input_hash(served: bytes) -> str:
    if len(served) != ENVELOPE_BYTES:
        raise ValueError("served input must be exactly 65536 bytes")
    return sha256(served)


def _result_hash(record: dict[str, Any]) -> str:
    return hash_without(record, "result_hash")


def _call_record(manifest: dict[str, Any], condition: str, node: str, task_hash: str,
                 served_hash: str, parsed: dict[str, Any], raw_response_utf8: str) -> dict[str, Any]:
    raw_hash = sha384(raw_response_utf8.encode("utf-8"))
    response_ref = f"RESPONSE.{condition}.{node}"
    row = {"schema_id": "DurableCallRecordV1", "scenario_id": manifest["scenario_id"],
           "condition": condition, "node": node, "handoff_id": f"HANDOFF.{condition}",
           "task_packet_hash": task_hash,
           "served_request_hash": served_hash, "request_parameters_hash": sha384([task_hash, served_hash]),
           "idempotency_token": f"IDEM.{manifest['scenario_id']}.{condition}.{node}",
           "route_contract_hash": manifest["route_contract_hash"], "raw_response_utf8": raw_response_utf8,
           "raw_response_hash": raw_hash,
           "parsed_response_hash": parsed["result_hash"] if "result_hash" in parsed else parsed["worker_handoff_hash"],
           "response_ref": response_ref, "provider_request_id": f"PROVIDER.{condition}.{node}",
           "accepted_at": T1}
    row["durability_receipt"] = make_durability_receipt(
        row, f"TXN.{manifest['scenario_id']}.{condition}.{node}")
    row["call_record_hash"] = hash_without(row, "call_record_hash")
    return row


def build_task_packet(manifest: dict[str, Any], condition: str, a0_packet: dict[str, Any],
                      a0_result: dict[str, Any], a0_call_record: dict[str, Any]) -> dict[str, Any]:
    task = {"schema_id": "TaskPacketV1", "scenario_id": manifest["scenario_id"],
            "scope_id": manifest["scope_id"], "condition": condition,
            "manifest_hash": manifest["manifest_hash"], "a0_packet_hash": a0_packet["packet_hash"],
            "a0_served_request_hash": a0_result["served_request_hash"],
            "a0_result_hash": a0_result["result_hash"],
            "a0_call_record_hash": a0_call_record["call_record_hash"],
            "requested_action_catalog_hash": manifest["action_catalog_hash"]}
    task["task_packet_hash"] = hash_without(task, "task_packet_hash")
    return task


def _fixture_authoritative_state(manifest: dict[str, Any]) -> dict[str, Any]:
    state = state_reference.initial_state()
    complete = state_reference.make_event("complete_obligation", {
        "obligation_id": "OBL.PREREQ",
        "completion_action_id": state_reference.action_id(manifest["scope_id"], "OBL.PREREQ"),
        "originating_cut_hash": state_reference.cut_hash(state_reference.current_cut(state)),
    }, state=state)
    state, result = state_reference.reference_apply(state, complete)
    world = _world_map(manifest)
    obligations = state["scopes"][manifest["scope_id"]]["obligations"]
    for object_id, row in world.items():
        if row["object_kind"] != "OBLIGATION":
            continue
        existing = obligations.get(object_id, {
            "subject_id": "SUB.SHARED", "owner_role": "WORKER", "terminal_event_id": None})
        existing.update(copy.deepcopy(row["fields"]))
        obligations[object_id] = existing
    state["scopes"][manifest["scope_id"]]["dependencies"] = sorted([
        [row["fields"]["obligation_id"], row["fields"]["prerequisite_obligation_id"]]
        for row in manifest["canonical_world"] if row["object_kind"] == "DEPENDENCY"])
    if result != "APPLIED" or state_reference.current_cut(state) != manifest["cut"]:
        raise ValueError("default authoritative state does not match manifest cut")
    if project_state_world(state, manifest) != manifest["canonical_world"]:
        raise ValueError("MANIFEST_STATE_PROJECTION_MISMATCH")
    return state


def _transition_payloads(manifest: dict[str, Any], condition: str,
                         task: dict[str, Any], worker: dict[str, Any],
                         b_call: dict[str, Any], state: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    action = next(row for row in manifest["action_catalog"]
                  if row.get("action_id") == manifest["gold_action_id"])
    handoff = {
        "handoff_id": f"HANDOFF.{condition}", "scenario_id": manifest["scenario_id"],
        "condition": condition, "target_obligation_id": action["obligation_id"],
        "task_packet_hash": task["task_packet_hash"],
        "served_request_hash": worker["served_request_hash"],
        "request_parameters_hash": b_call["request_parameters_hash"],
        "idempotency_token": b_call["idempotency_token"],
        "task_packet_utf8": canonical_json(task).decode("utf-8"),
        "manifest_utf8": canonical_json(manifest).decode("utf-8"),
        "originating_cut_hash": state_reference.cut_hash(state_reference.current_cut(state)),
        "action_catalog_hash": manifest["action_catalog_hash"],
        "canonical_snapshot_hash": sha384(
            state["scopes"][manifest["scope_id"]]["obligations"]),
        "route_contract_hash": manifest["route_contract_hash"],
        "manifest_hash": manifest["manifest_hash"],
        "action_catalog": copy.deepcopy(manifest["action_catalog"]),
    }
    response = {
        "handoff_id": handoff["handoff_id"], "scenario_id": manifest["scenario_id"],
        "condition": condition, "node": "B", "task_packet_hash": task["task_packet_hash"],
        "served_request_hash": worker["served_request_hash"],
        "request_parameters_hash": b_call["request_parameters_hash"],
        "idempotency_token": b_call["idempotency_token"],
        "raw_response_utf8": b_call["raw_response_utf8"],
        "raw_response_hash": b_call["raw_response_hash"],
        "worker_handoff_hash": worker["worker_handoff_hash"],
        "response_ref": b_call["response_ref"],
        "provider_request_id": b_call["provider_request_id"],
        "durability_receipt": copy.deepcopy(b_call["durability_receipt"]),
        "route_contract_hash": manifest["route_contract_hash"], "accepted_at": T1,
    }
    return handoff, response


def build_transition_authority(manifest: dict[str, Any], condition: str,
                               task: dict[str, Any], worker: dict[str, Any],
                               b_call: dict[str, Any], *,
                               authoritative_state: dict[str, Any] | None = None) -> dict[str, Any]:
    reference_state = copy.deepcopy(authoritative_state or _fixture_authoritative_state(manifest))
    oracle_state = copy.deepcopy(reference_state)
    if state_reference.current_cut(reference_state) != manifest["cut"]:
        raise ValueError("authoritative state cut does not match manifest")
    try:
        projected_prestate = project_state_world(reference_state, manifest)
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("MANIFEST_STATE_PROJECTION_MISMATCH") from exc
    if projected_prestate != manifest["canonical_world"]:
        raise ValueError("MANIFEST_STATE_PROJECTION_MISMATCH")
    handoff_payload, response_payload = _transition_payloads(
        manifest, condition, task, worker, b_call, reference_state)
    events = [
        state_reference.make_event("open_handoff", handoff_payload, state=reference_state),
    ]
    for event in events:
        reference_state, ref_result = state_reference.reference_apply(reference_state, event)
        oracle_state, ora_result = state_oracle.oracle_apply(oracle_state, event)
        if ref_result != "APPLIED" or ora_result != "APPLIED" or reference_state != oracle_state:
            raise ValueError("state reducers disagree before proposal")
    response = state_reference.make_event("record_call_response", response_payload,
                                          state=reference_state)
    reference_state, ref_result = state_reference.reference_apply(reference_state, response)
    oracle_state, ora_result = state_oracle.oracle_apply(oracle_state, response)
    if ref_result != "APPLIED" or ora_result != "APPLIED" or reference_state != oracle_state:
        raise ValueError("state reducers disagree on durable response")
    proposal = state_reference.make_event("propose_handoff_result", {
        "handoff_id": handoff_payload["handoff_id"],
        "worker_handoff_hash": worker["worker_handoff_hash"],
        "originating_cut_hash": handoff_payload["originating_cut_hash"],
        "action_ids": [manifest["gold_action_id"]],
    }, state=reference_state)
    reference_state, ref_result = state_reference.reference_apply(reference_state, proposal)
    oracle_state, ora_result = state_oracle.oracle_apply(oracle_state, proposal)
    if ref_result != "APPLIED" or ora_result != "APPLIED" or reference_state != oracle_state:
        raise ValueError("state reducers disagree on proposal")
    prestate = copy.deepcopy(reference_state)
    precommit_cut = state_reference.current_cut(prestate)
    child = state_reference.make_event("commit_handoff_result", {
        "handoff_id": handoff_payload["handoff_id"],
        "proposal_event_id": proposal["event_id"],
    }, state=prestate, valid_from=T1)
    ref_post, ref_result = state_reference.reference_apply(copy.deepcopy(prestate), child)
    ora_post, ora_result = state_oracle.oracle_apply(copy.deepcopy(prestate), child)
    if ref_result != "APPLIED" or ora_result != "APPLIED" or ref_post != ora_post:
        raise ValueError("state reducers disagree on commit")
    postcommit_cut = state_reference.current_cut(ref_post)
    authority = {
        "schema_id": "TransitionAuthorityV1",
        "precommit_state": prestate,
        "precommit_state_hash": sha384(prestate),
        "precommit_cut": precommit_cut,
        "proposal_event": proposal,
        "proposal_event_utf8": canonical_json(proposal).decode("utf-8"),
        "proposal_event_hash": sha384(proposal),
        "applied_child_event": child,
        "applied_child_event_hash": sha384(child),
        "postcommit_state": ref_post,
        "postcommit_state_hash": sha384(ref_post),
        "postcommit_cut": postcommit_cut,
    }
    authority["transition_authority_hash"] = hash_without(
        authority, "transition_authority_hash")
    return authority


def _state_authority_receipt(authority: dict[str, Any], condition: str) -> dict[str, Any]:
    return state_reference.make_fixture_state_authority_receipt(
        authority["precommit_state"], authority["proposal_event"],
        authority["applied_child_event"], authority["postcommit_state"],
        transaction_commit_id=f"TXN.MBCX01.FIXTURE.{condition}")


MANIFEST_CUT_RECEIPT_KEYS = {
    "schema_id", "authority_mode", "scenario_id", "manifest_hash",
    "source_candidate_hash", "retained_set_root", "state_utf8", "state_hash",
    "cut", "projected_world", "projected_world_hash", "receipt_hash",
}


def _manifest_cut_state_receipt(state: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    projected = project_state_world(state, manifest)
    receipt = {
        "schema_id": "ManifestCutStateReceiptV1",
        "authority_mode": "FIXTURE_CONFORMANCE",
        "scenario_id": manifest["scenario_id"],
        "manifest_hash": manifest["manifest_hash"],
        "source_candidate_hash": manifest["source_candidate_hash"],
        "retained_set_root": manifest["retained_set_root"],
        "state_utf8": canonical_json(state).decode("utf-8"),
        "state_hash": sha384(state),
        "cut": copy.deepcopy(state_reference.current_cut(state)),
        "projected_world": projected,
        "projected_world_hash": sha384(projected),
    }
    receipt["receipt_hash"] = hash_without(receipt, "receipt_hash")
    return receipt


def validate_manifest_cut_state_receipt(receipt: Any, manifest: dict[str, Any], *,
                                        require_production: bool = True) -> list[str]:
    errors: set[str] = set()
    try:
        if (not _shape(receipt, MANIFEST_CUT_RECEIPT_KEYS, "ManifestCutStateReceiptV1")
                or receipt["authority_mode"] != "FIXTURE_CONFORMANCE"
                or receipt["scenario_id"] != manifest["scenario_id"]
                or receipt["manifest_hash"] != manifest["manifest_hash"]
                or receipt["source_candidate_hash"] != manifest["source_candidate_hash"]
                or receipt["retained_set_root"] != manifest["retained_set_root"]
                or receipt["receipt_hash"] != hash_without(receipt, "receipt_hash")):
            raise ValueError
        state = json.loads(receipt["state_utf8"])
        projected = project_state_world(state, manifest)
        if (receipt["state_hash"] != sha384(state)
                or receipt["cut"] != manifest["cut"]
                or state_reference.current_cut(state) != manifest["cut"]
                or receipt["projected_world"] != projected
                or receipt["projected_world_hash"] != sha384(projected)
                or projected != manifest["canonical_world"]):
            raise ValueError
    except (KeyError, TypeError, ValueError, AttributeError, json.JSONDecodeError):
        errors.add("MANIFEST_CUT_STATE_MISMATCH")
    if require_production:
        errors.add("STATE_AUTHORITY_UNAVAILABLE")
    return sorted(errors)


def build_durable_b_response_binding(b_call: dict[str, Any]) -> dict[str, Any]:
    """Build the one exact durable-ledger snapshot that owns the packet B response."""
    ledger = _durable_call_ledger(b_call)
    return measurement.bind_durable_b_response(ledger, b_call)


def _durable_call_ledger(call_record: dict[str, Any]) -> measurement.CallLedger:
    """Reconstruct one durable terminal ledger from the exact call-record bytes."""
    ledger = measurement.CallLedger.prepare(
        call_record["scenario_id"], call_record["condition"], call_record["node"],
        call_record["task_packet_hash"], call_record["served_request_hash"],
        call_record["request_parameters_hash"], call_record["idempotency_token"],
        call_record["route_contract_hash"], handoff_id=call_record["handoff_id"])
    ledger = ledger.transition("DISPATCH_CONFIRMED")
    ledger = ledger.transition(
        "RESPONSE_BYTES_FSYNCED",
        response_bytes=call_record["raw_response_utf8"].encode("utf-8"),
        response_ref=call_record["response_ref"],
        provider_request_id=call_record["provider_request_id"],
        durability_receipt=copy.deepcopy(call_record["durability_receipt"]))
    return ledger


def build_scoring_fixture(manifest: dict[str, Any], condition: str = "OM", *,
                          authoritative_state: dict[str, Any] | None = None,
                          cohort_authority: dict[str, Any] | None = None,
                          durable_b_response_binding: dict[str, Any] | None = None) -> dict[str, Any]:
    manifest_state = copy.deepcopy(authoritative_state or _fixture_authoritative_state(manifest))
    manifest_cut_receipt = _manifest_cut_state_receipt(manifest_state, manifest)
    a0_packet = build_decision_packet(manifest, condition, "A0_PRECOMMIT")
    a0_served = served_input_hash(render_served_input(a0_packet))
    a0_result = {"schema_id": "A0ResultV3", "input_packet_hash": a0_packet["packet_hash"],
                 "served_request_hash": a0_served, "manifest_hash": manifest["manifest_hash"],
                 "selected_action_ids": [manifest["gold_action_id"]]}
    a0_result["result_hash"] = _result_hash(a0_result)
    a0_raw = canonical_json(a0_result).decode("utf-8")
    a0_call = _call_record(manifest, condition, "A0", a0_packet["packet_hash"], a0_served,
                           a0_result, a0_raw)
    task = build_task_packet(manifest, condition, a0_packet, a0_result, a0_call)
    b_served = served_input_hash(render_served_input(task))
    worker = {"schema_id": "WorkerHandoffV5", "scenario_id": manifest["scenario_id"],
              "scope_id": manifest["scope_id"], "condition": condition,
              "task_packet_hash": task["task_packet_hash"], "served_request_hash": b_served,
              "manifest_hash": manifest["manifest_hash"], "status_code": "PROPOSE",
              "proposed_action_ids": [manifest["gold_action_id"]], "produced_at": T1}
    worker["worker_handoff_hash"] = hash_without(worker, "worker_handoff_hash")
    worker_raw = canonical_json(worker).decode("utf-8")
    b_call = _call_record(manifest, condition, "B", task["task_packet_hash"], b_served,
                          worker, worker_raw)
    if durable_b_response_binding is None:
        durable_b_response_binding = build_durable_b_response_binding(b_call)
    authority = build_transition_authority(
        manifest, condition, task, worker, b_call,
        authoritative_state=manifest_state)
    state_authority_receipt = _state_authority_receipt(authority, condition)
    child = copy.deepcopy(authority["applied_child_event"])
    final_cut = copy.deepcopy(authority["postcommit_cut"])
    post_world = project_state_world(authority["postcommit_state"], manifest)
    expected_a1_truth = legal_action_ids_from_world(
        post_world, manifest["action_catalog"], authority["postcommit_cut"])
    if expected_a1_truth != manifest["expected_a1_action_ids"]:
        raise ValueError("POSTSTATE_A1_TRUTH_MISMATCH")
    receipt = {"schema_id": "WriterReceiptV2", "manifest_hash": manifest["manifest_hash"],
               "worker_handoff_hash": worker["worker_handoff_hash"],
               "worker_call_record_hash": b_call["call_record_hash"], "status_code": "COMMITTED",
               "committed_action_ids": [manifest["gold_action_id"]], "child_events": [child],
               "transition_authority_hash": authority["transition_authority_hash"],
               "state_authority_receipt_hash": state_authority_receipt["receipt_hash"],
               "precommit_state_hash": authority["precommit_state_hash"],
               "proposal_event_hash": authority["proposal_event_hash"],
               "applied_child_event_hash": authority["applied_child_event_hash"],
               "postcommit_cut": final_cut,
               "postcommit_state_hash": authority["postcommit_state_hash"],
               "postcommit_world_hash": sha384(post_world)}
    receipt["receipt_hash"] = hash_without(receipt, "receipt_hash")
    a1_packet = build_decision_packet(
        manifest, condition, "A1_POSTCOMMIT", postcommit_cut=final_cut,
        source_world=post_world)
    a1_served = served_input_hash(render_served_input(a1_packet))
    a1_result = {"schema_id": "A1ResultV3", "input_packet_hash": a1_packet["packet_hash"],
                 "served_request_hash": a1_served, "manifest_hash": manifest["manifest_hash"],
                 "writer_receipt_hash": receipt["receipt_hash"],
                 "selected_action_ids": copy.deepcopy(manifest["expected_a1_action_ids"])}
    a1_result["result_hash"] = _result_hash(a1_result)
    a1_raw = canonical_json(a1_result).decode("utf-8")
    a1_call = _call_record(manifest, condition, "A1", a1_packet["packet_hash"], a1_served,
                           a1_result, a1_raw)
    return {"schema_id": "ScorerInputV1", "condition": condition,
            "manifest": copy.deepcopy(manifest), "a0_packet": a0_packet,
            "a0_call_record": a0_call, "a0_result": a0_result, "task_packet": task,
            "b_call_record": b_call, "worker_handoff": worker,
             "cohort_authority": copy.deepcopy(
                 cohort_authority or cohort_authority_for_manifest(manifest)),
             "durable_b_response_binding": copy.deepcopy(durable_b_response_binding),
             "manifest_cut_state_receipt": manifest_cut_receipt,
             "transition_authority": authority,
             "state_authority_receipt": state_authority_receipt,
             "writer_receipt": receipt,
            "a1_packet": a1_packet, "a1_call_record": a1_call, "a1_result": a1_result}


TOP_KEYS = {"schema_id", "condition", "manifest", "cohort_authority",
            "a0_packet", "a0_call_record", "a0_result",
            "task_packet", "b_call_record", "worker_handoff", "transition_authority",
            "durable_b_response_binding", "manifest_cut_state_receipt",
            "state_authority_receipt",
            "writer_receipt", "a1_packet",
            "a1_call_record", "a1_result"}
PACKET_KEYS = {"schema_id", "stage", "condition", "scenario_id", "scope_id", "cut", "objects",
               "action_catalog", "observation", "manifest_hash", "packet_hash"}
A0_KEYS = {"schema_id", "input_packet_hash", "served_request_hash", "manifest_hash",
           "selected_action_ids", "result_hash"}
TASK_KEYS = {"schema_id", "scenario_id", "scope_id", "condition", "manifest_hash", "a0_packet_hash",
             "a0_served_request_hash", "a0_result_hash", "a0_call_record_hash",
             "requested_action_catalog_hash", "task_packet_hash"}
WORKER_KEYS = {"schema_id", "scenario_id", "scope_id", "condition", "task_packet_hash",
               "served_request_hash", "manifest_hash", "status_code", "proposed_action_ids",
               "produced_at", "worker_handoff_hash"}
CALL_KEYS = {"schema_id", "scenario_id", "condition", "node", "task_packet_hash",
             "handoff_id",
             "served_request_hash", "request_parameters_hash", "idempotency_token",
             "route_contract_hash", "raw_response_utf8", "raw_response_hash", "parsed_response_hash",
             "response_ref", "provider_request_id", "durability_receipt", "accepted_at",
             "call_record_hash"}
RECEIPT_KEYS = {"schema_id", "manifest_hash", "worker_handoff_hash", "worker_call_record_hash",
                 "status_code", "committed_action_ids", "child_events", "postcommit_cut",
                 "transition_authority_hash", "state_authority_receipt_hash",
                 "precommit_state_hash", "proposal_event_hash",
                 "applied_child_event_hash", "postcommit_state_hash",
                 "postcommit_world_hash", "receipt_hash"}
AUTHORITY_KEYS = {"schema_id", "precommit_state", "precommit_state_hash", "precommit_cut",
                   "proposal_event", "proposal_event_utf8", "proposal_event_hash", "applied_child_event",
                  "applied_child_event_hash", "postcommit_state", "postcommit_state_hash",
                  "postcommit_cut", "transition_authority_hash"}
A1_KEYS = {"schema_id", "input_packet_hash", "served_request_hash", "manifest_hash",
           "writer_receipt_hash", "selected_action_ids", "result_hash"}


def _shape(record: Any, keys: set[str], schema_id: str) -> bool:
    return isinstance(record, dict) and set(record) == keys and record.get("schema_id") == schema_id


def _valid_call(row: dict[str, Any], manifest: dict[str, Any], condition: str, node: str,
                task_hash: str, served_hash: str, parsed: dict[str, Any]) -> bool:
    if not _shape(row, CALL_KEYS, "DurableCallRecordV1") or not isinstance(parsed, dict):
        return False
    parsed_hash = parsed.get("result_hash", parsed.get("worker_handoff_hash"))
    return (row["scenario_id"] == manifest["scenario_id"] and row["condition"] == condition
            and row["node"] == node and row["task_packet_hash"] == task_hash
            and row["handoff_id"] == f"HANDOFF.{condition}"
            and row["served_request_hash"] == served_hash
            and row["request_parameters_hash"] == sha384([task_hash, served_hash])
            and row["idempotency_token"] == f"IDEM.{manifest['scenario_id']}.{condition}.{node}"
            and row["route_contract_hash"] == manifest["route_contract_hash"]
            and row["response_ref"] == f"RESPONSE.{condition}.{node}"
            and row["provider_request_id"] == f"PROVIDER.{condition}.{node}"
            and _valid_utc(row["accepted_at"])
            and row["raw_response_utf8"] == canonical_json(parsed).decode("utf-8")
            and row["raw_response_hash"] == sha384(row["raw_response_utf8"].encode("utf-8"))
            and row["parsed_response_hash"] == parsed_hash
            and valid_durability_receipt(row["durability_receipt"], row)
            and row["call_record_hash"] == hash_without(row, "call_record_hash"))


def _valid_cut(value: Any) -> bool:
    return (isinstance(value, dict)
            and set(value) == {"journal_seq", "knowledge_time", "valid_time"}
            and isinstance(value["journal_seq"], int)
            and not isinstance(value["journal_seq"], bool)
            and _valid_utc(value["knowledge_time"])
            and _valid_utc(value["valid_time"]))


def _valid_state_event(value: Any, event_type: str, scope_id: str) -> bool:
    keys = {"event_id", "scope_id", "event_type", "semantic_operation",
            "idempotency_key", "journal_seq", "observed_at", "valid_from",
            "valid_to", "originating_cut", "payload"}
    return (isinstance(value, dict) and set(value) == keys
            and value.get("event_id") == _canonical_event_id(value)
            and value.get("scope_id") == scope_id
            and value.get("event_type") == event_type
            and isinstance(value.get("journal_seq"), int)
            and not isinstance(value.get("journal_seq"), bool)
            and _valid_utc(value.get("observed_at"))
            and _valid_utc(value.get("valid_from"))
            and (value.get("valid_to") is None or _valid_utc(value.get("valid_to")))
            and _valid_cut(value.get("originating_cut")))


def _valid_transition_authority(manifest: dict[str, Any], condition: str,
                                task: dict[str, Any], worker: dict[str, Any],
                                b_call: dict[str, Any], authority: Any,
                                receipt: dict[str, Any]) -> bool:
    """Fail closed unless the receipt is an exact replay of one authoritative commit."""
    if not _shape(authority, AUTHORITY_KEYS, "TransitionAuthorityV1"):
        return False
    prestate = authority["precommit_state"]
    poststate = authority["postcommit_state"]
    precommit_cut = authority["precommit_cut"]
    postcommit_cut = authority["postcommit_cut"]
    proposal = authority["proposal_event"]
    child = authority["applied_child_event"]
    if (not isinstance(prestate, dict) or not isinstance(poststate, dict)
            or not _valid_cut(precommit_cut) or not _valid_cut(postcommit_cut)
            or authority["precommit_state_hash"] != sha384(prestate)
            or authority["postcommit_state_hash"] != sha384(poststate)
            or authority["proposal_event_utf8"] != canonical_json(proposal).decode("utf-8")
            or authority["proposal_event_hash"]
            != sha384(authority["proposal_event_utf8"].encode("utf-8"))
            or authority["applied_child_event_hash"] != sha384(child)
            or authority["transition_authority_hash"]
            != hash_without(authority, "transition_authority_hash")):
        return False
    if (state_reference.current_cut(prestate) != precommit_cut
            or state_reference.current_cut(poststate) != postcommit_cut):
        return False
    scope_id = manifest["scope_id"]
    if (not _valid_state_event(proposal, "propose_handoff_result", scope_id)
            or proposal.get("semantic_operation") != "PROPOSE_HANDOFF_RESULT"
            or not _valid_state_event(child, "commit_handoff_result", scope_id)
            or child.get("semantic_operation") != "COMMIT_HANDOFF_RESULT"):
        return False
    proposal_payload = proposal.get("payload")
    child_payload = child.get("payload")
    if (not isinstance(proposal_payload, dict)
            or set(proposal_payload) != {"handoff_id", "worker_handoff_hash",
                                         "originating_cut_hash", "action_ids"}
            or not isinstance(child_payload, dict)
            or set(child_payload) != {"handoff_id", "proposal_event_id"}):
        return False
    handoff_id = f"HANDOFF.{condition}"
    proposal_id = proposal["event_id"]
    if (proposal_payload != {
            "handoff_id": handoff_id,
            "worker_handoff_hash": worker.get("worker_handoff_hash"),
            "originating_cut_hash": state_reference.cut_hash(manifest["cut"]),
            "action_ids": [manifest["gold_action_id"]],
        }
            or child_payload != {"handoff_id": handoff_id,
                                 "proposal_event_id": proposal_id}
            or child["journal_seq"] != prestate.get("next_seq")
            or child["originating_cut"] != precommit_cut
            or proposal["journal_seq"] >= child["journal_seq"]):
        return False
    if (postcommit_cut["journal_seq"] != child["journal_seq"]
            or postcommit_cut["knowledge_time"] < child["observed_at"]
            or postcommit_cut["valid_time"] < child["valid_from"]
            or (child["valid_to"] is not None
                and postcommit_cut["valid_time"] >= child["valid_to"])):
        return False

    try:
        scope = prestate["scopes"][scope_id]
        handoff = scope["handoffs"][handoff_id]
        persisted_proposal_hash = prestate["events"][proposal_id]
    except (KeyError, TypeError):
        return False
    expected_handoff_fields = {
        "status": "PROPOSED",
        "scenario_id": manifest["scenario_id"],
        "condition": condition,
        "target_obligation_id": next(
            row["obligation_id"] for row in manifest["action_catalog"]
            if row.get("action_id") == manifest["gold_action_id"]),
        "task_packet_hash": task.get("task_packet_hash"),
        "served_request_hash": worker.get("served_request_hash"),
        "request_parameters_hash": b_call.get("request_parameters_hash"),
        "idempotency_token": b_call.get("idempotency_token"),
        "task_packet_utf8": canonical_json(task).decode("utf-8"),
        "manifest_utf8": canonical_json(manifest).decode("utf-8"),
        "route_contract_hash": manifest["route_contract_hash"],
        "manifest_hash": manifest["manifest_hash"],
        "originating_cut": manifest["cut"],
        "originating_cut_hash": state_reference.cut_hash(manifest["cut"]),
        "scope_id": scope_id,
        "action_catalog": manifest["action_catalog"],
        "proposal_event_id": proposal_id,
        "proposal_hash": authority["proposal_event_hash"],
        "worker_handoff_hash": worker.get("worker_handoff_hash"),
        "action_ids": [manifest["gold_action_id"]],
    }
    if (persisted_proposal_hash != authority["proposal_event_hash"]
            or not isinstance(handoff, dict)
            or any(handoff.get(key) != expected
                   for key, expected in expected_handoff_fields.items())):
        return False
    matching_responses = [row for row in prestate.get("responses", [])
                          if isinstance(row, dict)
                          and row.get("handoff_id") == handoff_id
                          and row.get("scenario_id") == manifest["scenario_id"]
                          and row.get("condition") == condition
                          and row.get("node") == "B"]
    if len(matching_responses) != 1:
        return False
    response = matching_responses[0]
    expected_response_fields = {
        "task_packet_hash": task.get("task_packet_hash"),
        "served_request_hash": worker.get("served_request_hash"),
        "request_parameters_hash": b_call.get("request_parameters_hash"),
        "idempotency_token": b_call.get("idempotency_token"),
        "raw_response_utf8": b_call.get("raw_response_utf8"),
        "raw_response_hash": b_call.get("raw_response_hash"),
        "worker_handoff_hash": worker.get("worker_handoff_hash"),
        "response_ref": b_call.get("response_ref"),
        "provider_request_id": b_call.get("provider_request_id"),
        "durability_receipt": b_call.get("durability_receipt"),
        "route_contract_hash": manifest["route_contract_hash"],
        "accepted_at": b_call.get("accepted_at"),
        "scope_id": scope_id,
        "parsed_proposed_action_ids": [manifest["gold_action_id"]],
    }
    if any(response.get(key) != expected
           for key, expected in expected_response_fields.items()):
        return False

    ref_post, ref_result = state_reference.reference_apply(copy.deepcopy(prestate), child)
    ora_post, ora_result = state_oracle.oracle_apply(copy.deepcopy(prestate), child)
    if (ref_result != "APPLIED" or ora_result != "APPLIED"
            or canonical_json(ref_post) != canonical_json(ora_post)
            or canonical_json(ref_post) != canonical_json(poststate)
            or state_reference.current_cut(ref_post) != postcommit_cut):
        return False
    return (receipt.get("child_events") == [child]
            and receipt.get("transition_authority_hash")
            == authority["transition_authority_hash"]
            and receipt.get("precommit_state_hash") == authority["precommit_state_hash"]
            and receipt.get("proposal_event_hash") == authority["proposal_event_hash"]
            and receipt.get("applied_child_event_hash")
            == authority["applied_child_event_hash"]
            and receipt.get("postcommit_state_hash") == authority["postcommit_state_hash"]
            and receipt.get("postcommit_cut") == postcommit_cut)


def invariant_matrix(expected_manifest: dict[str, Any], value: Any, *,
                     require_production_authority: bool = True) -> dict[str, bool]:
    matrix = {f"I{index:02d}": False for index in range(1, 10)}
    try:
        if not isinstance(value, dict):
            return matrix
        manifest = value["manifest"]
        condition = value["condition"]
        a0_packet, a0_result, a0_call = (
            value["a0_packet"], value["a0_result"], value["a0_call_record"])
        task = value["task_packet"]
        worker, b_call = value["worker_handoff"], value["b_call_record"]
        transition = value["transition_authority"]
        manifest_cut_receipt = value["manifest_cut_state_receipt"]
        state_receipt = value["state_authority_receipt"]
        writer = value["writer_receipt"]
        a1_packet, a1_result = value["a1_packet"], value["a1_result"]

        matrix["I01"] = (manifest == expected_manifest
                         and validate_cohort_manifest_join(
                             value["cohort_authority"], manifest))

        ref_authority_errors = state_reference.verify_state_authority_receipt(
            state_receipt, require_production=require_production_authority)
        ora_authority_errors = state_oracle.verify_state_authority_receipt(
            state_receipt, require_production=require_production_authority)
        prestate = json.loads(state_receipt["prestate_read"]["state_utf8"])
        poststate = json.loads(state_receipt["postcommit_readback"]["state_utf8"])
        proposal = json.loads(state_receipt["proposal_persistence"]["event_utf8"])
        child = json.loads(state_receipt["applied_child"]["event_utf8"])
        pre_world = project_state_world(prestate, manifest)
        post_world = project_state_world(poststate, manifest)
        manifest_cut_errors = validate_manifest_cut_state_receipt(
            manifest_cut_receipt, manifest,
            require_production=require_production_authority)
        manifest_cut_state = json.loads(manifest_cut_receipt["state_utf8"])
        matrix["I02"] = (not manifest_cut_errors
                         and not ref_authority_errors and not ora_authority_errors
                         and manifest_cut_receipt["cut"] == manifest["cut"]
                         and manifest_cut_receipt["projected_world"]
                         == manifest["canonical_world"]
                         and state_reference.current_cut(manifest_cut_state) == manifest["cut"]
                         and canonical_json(prestate)
                         == canonical_json(transition["precommit_state"])
                         and state_receipt["prestate_read"]["state_hash"]
                         == transition["precommit_state_hash"]
                         and state_receipt["prestate_read"]["cut"]
                         == transition["precommit_cut"]
                         and pre_world == manifest["canonical_world"]
                         and sha384(pre_world) == manifest["canonical_world_hash"])

        expected_a0 = build_decision_packet(manifest, condition, "A0_PRECOMMIT")
        expected_a0_served = served_input_hash(render_served_input(expected_a0))
        matrix["I03"] = (a0_packet == expected_a0
                         and a0_result.get("input_packet_hash") == a0_packet["packet_hash"]
                         and a0_result.get("served_request_hash") == expected_a0_served
                         and a0_result.get("manifest_hash") == manifest["manifest_hash"]
                         and a0_result.get("selected_action_ids")
                         == [manifest["gold_action_id"]]
                         and a0_result.get("result_hash") == _result_hash(a0_result)
                         and _valid_call(
                             a0_call, manifest, condition, "A0",
                             a0_packet["packet_hash"], expected_a0_served, a0_result))
        matrix["I04"] = task == build_task_packet(
            manifest, condition, a0_packet, a0_result, a0_call)

        binding_errors = measurement.validate_b_response_ledger_binding(
            value["durable_b_response_binding"], b_call)
        matrix["I05"] = (not binding_errors
                         and b_call.get("parsed_response_hash")
                         == worker.get("worker_handoff_hash")
                         and b_call.get("raw_response_utf8")
                         == canonical_json(worker).decode("utf-8")
                         and b_call.get("durability_receipt")
                         == value["durable_b_response_binding"]["ledger_snapshot"][
                             "durability_receipt"])

        proposal_row = state_receipt["proposal_persistence"]
        matrix["I06"] = (
            proposal == transition["proposal_event"]
            and proposal_row["event_hash"] == transition["proposal_event_hash"]
            and prestate.get("events", {}).get(proposal["event_id"])
            == proposal_row["event_hash"])
        child_row = state_receipt["applied_child"]
        ref_post, ref_result = state_reference.reference_apply(
            copy.deepcopy(prestate), copy.deepcopy(child))
        ora_post, ora_result = state_oracle.oracle_apply(
            copy.deepcopy(prestate), copy.deepcopy(child))
        matrix["I07"] = (
            child == transition["applied_child_event"]
            and child_row["event_hash"] == transition["applied_child_event_hash"]
            and child["payload"]["proposal_event_id"] == proposal["event_id"]
            and child["journal_seq"] == prestate["next_seq"]
            and child["originating_cut"] == state_receipt["prestate_read"]["cut"]
            and ref_result == ora_result == "APPLIED"
            and canonical_json(ref_post) == canonical_json(ora_post)
            and canonical_json(ref_post) == canonical_json(poststate)
            and canonical_json(poststate)
            == canonical_json(transition["postcommit_state"])
            and state_receipt["postcommit_readback"]["state_hash"]
            == transition["postcommit_state_hash"]
            and state_receipt["postcommit_readback"]["cut"]
            == transition["postcommit_cut"])
        matrix["I08"] = (
            writer.get("state_authority_receipt_hash") == state_receipt["receipt_hash"]
            and writer.get("child_events") == [child]
            and writer.get("postcommit_state_hash")
            == state_receipt["postcommit_readback"]["state_hash"]
            and writer.get("postcommit_cut")
            == state_receipt["postcommit_readback"]["cut"]
            and writer.get("postcommit_world_hash") == sha384(post_world))

        selected = (manifest["bc_selected_object_ids"] if condition == "BC"
                    else manifest["gold_read_set"])
        ids = _object_closure(manifest, selected)
        expected_a1_objects = [_world_map({"canonical_world": post_world})[name]
                               for name in ids]
        actual_truth = legal_action_ids_from_world(
            post_world, manifest["action_catalog"], writer["postcommit_cut"])
        matrix["I09"] = (
            a1_packet.get("objects") == expected_a1_objects
            and a1_packet.get("cut") == writer["postcommit_cut"]
            and a1_packet.get("action_catalog") == manifest["action_catalog"]
            and actual_truth == manifest["expected_a1_action_ids"]
            and a1_result.get("selected_action_ids") == actual_truth
            and a1_result.get("writer_receipt_hash") == writer.get("receipt_hash"))
        return matrix
    except (AttributeError, KeyError, TypeError, ValueError, UnicodeError,
            json.JSONDecodeError):
        return matrix


def validate_scorer_input(expected_manifest: dict[str, Any], value: Any, *,
                          require_production_authority: bool = True) -> list[str]:
    errors: set[str] = set(validate_expected_manifest(expected_manifest))
    if errors:
        return sorted(errors)
    if not isinstance(value, dict) or set(value) != TOP_KEYS or value.get("schema_id") != "ScorerInputV1":
        return sorted(errors | {"SCORER_INPUT_SCHEMA_INVALID"})
    if value["manifest"] != expected_manifest:
        errors.add("EXPECTED_MANIFEST_MISMATCH")
    errors.update(validate_manifest_cut_state_receipt(
        value.get("manifest_cut_state_receipt"), expected_manifest,
        require_production=require_production_authority))
    shapes = (("a0_packet", PACKET_KEYS, "DecisionPacketV5"),
              ("a0_call_record", CALL_KEYS, "DurableCallRecordV1"),
              ("a0_result", A0_KEYS, "A0ResultV3"),
              ("task_packet", TASK_KEYS, "TaskPacketV1"),
              ("b_call_record", CALL_KEYS, "DurableCallRecordV1"),
              ("worker_handoff", WORKER_KEYS, "WorkerHandoffV5"),
              ("transition_authority", AUTHORITY_KEYS, "TransitionAuthorityV1"),
              ("writer_receipt", RECEIPT_KEYS, "WriterReceiptV2"),
              ("a1_packet", PACKET_KEYS, "DecisionPacketV5"),
              ("a1_call_record", CALL_KEYS, "DurableCallRecordV1"),
              ("a1_result", A1_KEYS, "A1ResultV3"))
    if any(not _shape(value[name], keys, schema_id) for name, keys, schema_id in shapes):
        return sorted(errors | {"SCORER_INPUT_SCHEMA_INVALID"})
    condition = value.get("condition")
    if condition not in {"BC", "OM"}:
        errors.add("CONDITION_INVALID")
        return sorted(errors)
    a0_packet, a0_result, a0_call = value["a0_packet"], value["a0_result"], value["a0_call_record"]
    expected_a0 = build_decision_packet(expected_manifest, condition, "A0_PRECOMMIT") if not errors else None
    if not _shape(a0_packet, PACKET_KEYS, "DecisionPacketV5") or a0_packet != expected_a0:
        errors.add("A0_PACKET_INVALID")
    a0_served = served_input_hash(render_served_input(a0_packet)) if _shape(a0_packet, PACKET_KEYS, "DecisionPacketV5") else ""
    if (not _shape(a0_result, A0_KEYS, "A0ResultV3")
            or a0_result.get("result_hash") != _result_hash(a0_result)
            or a0_result.get("input_packet_hash") != a0_packet.get("packet_hash")
            or a0_result.get("served_request_hash") != a0_served
            or a0_result.get("manifest_hash") != expected_manifest["manifest_hash"]
            or a0_result.get("selected_action_ids") != [expected_manifest["gold_action_id"]]):
        errors.add("A0_RESULT_INVALID")
    if not _valid_call(a0_call, expected_manifest, condition, "A0", a0_packet.get("packet_hash"),
                       a0_served, a0_result):
        errors.add("A0_CALL_INVALID")
    task = value["task_packet"]
    if (not _shape(task, TASK_KEYS, "TaskPacketV1")
            or task.get("task_packet_hash") != hash_without(task, "task_packet_hash")
            or task.get("scenario_id") != expected_manifest["scenario_id"]
            or task.get("scope_id") != expected_manifest["scope_id"] or task.get("condition") != condition
            or task.get("manifest_hash") != expected_manifest["manifest_hash"]
            or task.get("a0_packet_hash") != a0_packet.get("packet_hash")
            or task.get("a0_served_request_hash") != a0_served
            or task.get("a0_result_hash") != a0_result.get("result_hash")
            or task.get("a0_call_record_hash") != a0_call.get("call_record_hash")
            or task.get("requested_action_catalog_hash") != expected_manifest["action_catalog_hash"]):
        errors.add("TASK_PACKET_INVALID")
    worker, b_call = value["worker_handoff"], value["b_call_record"]
    b_served = served_input_hash(render_served_input(task)) if _shape(task, TASK_KEYS, "TaskPacketV1") else ""
    if (not _shape(worker, WORKER_KEYS, "WorkerHandoffV5")
            or worker.get("worker_handoff_hash") != hash_without(worker, "worker_handoff_hash")
            or worker.get("scenario_id") != expected_manifest["scenario_id"]
            or worker.get("scope_id") != expected_manifest["scope_id"] or worker.get("condition") != condition
            or worker.get("task_packet_hash") != task.get("task_packet_hash")
            or worker.get("served_request_hash") != b_served
            or worker.get("manifest_hash") != expected_manifest["manifest_hash"]
            or worker.get("status_code") != "PROPOSE"
            or not _valid_utc(worker.get("produced_at"))
            or worker.get("proposed_action_ids") != [expected_manifest["gold_action_id"]]):
        errors.add("WORKER_HANDOFF_INVALID")
    if not _valid_call(b_call, expected_manifest, condition, "B", task.get("task_packet_hash"),
                       b_served, worker):
        errors.add("B_CALL_INVALID")
    elif worker.get("produced_at") > b_call.get("accepted_at"):
        errors.add("B_CALL_TEMPORAL_ORDER_INVALID")
    receipt = value["writer_receipt"]
    authority = value["transition_authority"]
    try:
        post_world = project_state_world(authority["postcommit_state"], expected_manifest)
    except (KeyError, TypeError, ValueError):
        post_world = []
    child_ok = False
    if isinstance(receipt, dict) and isinstance(receipt.get("child_events"), list) and len(receipt["child_events"]) == 1:
        child = receipt["child_events"][0]
        child_keys = {"event_id", "scope_id", "event_type", "semantic_operation",
                      "idempotency_key", "journal_seq", "observed_at", "valid_from",
                      "valid_to", "originating_cut", "payload"}
        child_cut = child.get("originating_cut", {}) if isinstance(child, dict) else {}
        child_payload = child.get("payload", {}) if isinstance(child, dict) else {}
        postcommit_cut = receipt.get("postcommit_cut", {}) if isinstance(receipt, dict) else {}
        child_ok = (isinstance(child, dict)
                    and set(child) == child_keys
                    and child["event_id"] == _canonical_event_id(child)
                    and child["scope_id"] == expected_manifest["scope_id"]
                    and child["event_type"] == "commit_handoff_result"
                    and child["semantic_operation"] == "COMMIT_HANDOFF_RESULT"
                    and isinstance(child["journal_seq"], int)
                    and not isinstance(child["journal_seq"], bool)
                    and _valid_utc(child["observed_at"]) and _valid_utc(child["valid_from"])
                    and child["valid_to"] is None
                    and isinstance(child_cut, dict)
                    and set(child_cut) == {"journal_seq", "knowledge_time", "valid_time"}
                    and isinstance(child_payload, dict)
                    and set(child_payload) == {"handoff_id", "proposal_event_id"}
                    and child_payload["handoff_id"] == f"HANDOFF.{condition}"
                    and isinstance(child_payload["proposal_event_id"], str)
                    and child_payload["proposal_event_id"].startswith("EV.")
                    and isinstance(postcommit_cut, dict)
                    and set(postcommit_cut) == {"journal_seq", "knowledge_time", "valid_time"}
                    and postcommit_cut["journal_seq"] == child["journal_seq"]
                    and _valid_utc(postcommit_cut["knowledge_time"])
                    and _valid_utc(postcommit_cut["valid_time"])
                    and postcommit_cut["knowledge_time"] >= child["observed_at"])
    authority_ok = _valid_transition_authority(
        expected_manifest, condition, task, worker, b_call, authority, receipt)
    if not authority_ok:
        errors.add("TRANSITION_AUTHORITY_INVALID")
    if (not _shape(receipt, RECEIPT_KEYS, "WriterReceiptV2") or not child_ok
            or not authority_ok
            or receipt.get("manifest_hash") != expected_manifest["manifest_hash"]
            or receipt.get("worker_handoff_hash") != worker.get("worker_handoff_hash")
            or receipt.get("worker_call_record_hash") != b_call.get("call_record_hash")
            or receipt.get("status_code") != "COMMITTED"
            or receipt.get("committed_action_ids") != [expected_manifest["gold_action_id"]]
            or receipt.get("state_authority_receipt_hash")
            != value["state_authority_receipt"].get("receipt_hash")
            or receipt.get("postcommit_world_hash") != sha384(post_world)
            or receipt.get("receipt_hash") != hash_without(receipt, "receipt_hash")):
        errors.add("WRITER_RECEIPT_INVALID")
    a1_packet, a1_result, a1_call = value["a1_packet"], value["a1_result"], value["a1_call_record"]
    expected_a1 = (build_decision_packet(
        expected_manifest, condition, "A1_POSTCOMMIT",
        postcommit_cut=receipt.get("postcommit_cut"), source_world=post_world)
        if not validate_expected_manifest(expected_manifest) else None)
    if not _shape(a1_packet, PACKET_KEYS, "DecisionPacketV5") or a1_packet != expected_a1:
        errors.add("A1_PACKET_INVALID")
    a1_served = served_input_hash(render_served_input(a1_packet)) if _shape(a1_packet, PACKET_KEYS, "DecisionPacketV5") else ""
    if (not _shape(a1_result, A1_KEYS, "A1ResultV3")
            or a1_result.get("result_hash") != _result_hash(a1_result)
            or a1_result.get("input_packet_hash") != a1_packet.get("packet_hash")
            or a1_result.get("served_request_hash") != a1_served
            or a1_result.get("manifest_hash") != expected_manifest["manifest_hash"]
            or a1_result.get("writer_receipt_hash") != receipt.get("receipt_hash")
            or a1_result.get("selected_action_ids") != expected_manifest["expected_a1_action_ids"]):
        errors.add("A1_RESULT_INVALID")
    if not _valid_call(a1_call, expected_manifest, condition, "A1", a1_packet.get("packet_hash"),
                       a1_served, a1_result):
        errors.add("A1_CALL_INVALID")
    elif child_ok and a1_call.get("accepted_at") < child.get("observed_at"):
        errors.add("A1_CALL_TEMPORAL_ORDER_INVALID")
    if (_shape(a0_call, CALL_KEYS, "DurableCallRecordV1")
            and _shape(b_call, CALL_KEYS, "DurableCallRecordV1")
            and _shape(a1_call, CALL_KEYS, "DurableCallRecordV1")
            and not (a0_call["accepted_at"] <= b_call["accepted_at"] <= a1_call["accepted_at"])):
        errors.add("CALL_TEMPORAL_ORDER_INVALID")
    for identity in ("idempotency_token", "response_ref", "provider_request_id"):
        if len({a0_call[identity], b_call[identity], a1_call[identity]}) != 3:
            errors.add("CALL_IDENTITY_REUSE")
    transactions = [row.get("durability_receipt", {}).get("transaction_id")
                    for row in (a0_call, b_call, a1_call)]
    if len(set(transactions)) != 3:
        errors.add("CALL_IDENTITY_REUSE")
    matrix = invariant_matrix(
        expected_manifest, value,
        require_production_authority=require_production_authority)
    for invariant, holds in matrix.items():
        if not holds:
            errors.add(f"{invariant}_INVARIANT_INVALID")
    if require_production_authority:
        receipt_authority = value.get("state_authority_receipt")
        authority_errors = set(state_reference.verify_state_authority_receipt(
            receipt_authority, require_production=True))
        authority_errors.update(state_oracle.verify_state_authority_receipt(
            receipt_authority, require_production=True))
        errors.update(authority_errors)
    return sorted(errors)


def score_exact(expected_manifest: dict[str, Any], scorer_input: dict[str, Any]) -> int:
    try:
        return int(not validate_scorer_input(expected_manifest, scorer_input))
    except (AttributeError, KeyError, TypeError, ValueError, UnicodeError):
        return 0


def validate_fixture_conformance(expected_manifest: dict[str, Any],
                                 scorer_input: dict[str, Any]) -> list[str]:
    """No-paid conformance only; this result is never scientific admission."""
    return validate_scorer_input(
        expected_manifest, scorer_input, require_production_authority=False)


def score_fixture_conformance_exact(expected_manifest: dict[str, Any],
                                    scorer_input: dict[str, Any]) -> int:
    try:
        return int(not validate_fixture_conformance(expected_manifest, scorer_input))
    except (AttributeError, KeyError, TypeError, ValueError, UnicodeError):
        return 0


OUTCOME_RECEIPT_KEYS = {
    "schema_id", "scenario_id", "manifest_hash", "retained_set_root",
    "episode_hash", "call_bindings", "call_binding_set_hash",
    "bc_scorer_input", "bc_scorer_input_hash", "om_scorer_input",
    "om_scorer_input_hash", "authority_mode", "bc", "om", "receipt_hash",
}
OUTCOME_CALL_BINDING_KEYS = {"position", "ledger_hash", "call_record_hash"}


def build_complete_episode_receipt_for_scorers(
        bc_scorer_input: dict[str, Any], om_scorer_input: dict[str, Any],
        manifest_position: int) -> dict[str, Any]:
    """Build the exact six-ledger episode owned by two scorer graphs."""
    try:
        if (bc_scorer_input.get("condition") != "BC"
                or om_scorer_input.get("condition") != "OM"
                or bc_scorer_input["manifest"] != om_scorer_input["manifest"]):
            raise ValueError
        calls = []
        for scorer_input in (bc_scorer_input, om_scorer_input):
            for name in ("a0_call_record", "b_call_record", "a1_call_record"):
                calls.append(_durable_call_ledger(scorer_input[name]))
        return measurement.build_episode_receipt(
            bc_scorer_input["manifest"]["scenario_id"], manifest_position, calls)
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        raise ValueError("SCENARIO_OUTCOME_AUTHORITY_INVALID") from exc


def _outcome_episode_call_bindings(
        episode_receipt: dict[str, Any], bc_scorer_input: dict[str, Any],
        om_scorer_input: dict[str, Any]) -> list[dict[str, Any]]:
    try:
        manifest = bc_scorer_input["manifest"]
        if (om_scorer_input["manifest"] != manifest
                or episode_receipt.get("scenario_id") != manifest["scenario_id"]
                or episode_receipt.get("manifest_position") != manifest["retained_position"]
                or episode_receipt.get("terminal_class") != "COMPLETE_PAIR"
                or episode_receipt.get("missing_positions") != []
                or measurement.validate_episode_receipt(
                    episode_receipt, manifest["scenario_id"], manifest["retained_position"])):
            raise ValueError
        records = [
            bc_scorer_input["a0_call_record"], bc_scorer_input["b_call_record"],
            bc_scorer_input["a1_call_record"], om_scorer_input["a0_call_record"],
            om_scorer_input["b_call_record"], om_scorer_input["a1_call_record"],
        ]
        bindings = []
        for position, row, call_record in zip(
                measurement.EPISODE_POSITIONS, episode_receipt["calls"], records):
            if (row.get("position") != position or row.get("launch_status") != "LAUNCHED"):
                raise ValueError
            ledger = measurement.CallLedger.recover(
                canonical_json(row["ledger_snapshot"]).decode("utf-8"))
            if (ledger.state != "RESPONSE_DURABLY_RECORDED"
                    or row.get("ledger_hash") != ledger.ledger_hash
                    or any(call_record.get(field) != getattr(ledger, field)
                           for field in measurement.CALL_IDENTITY_FIELDS)
                    or call_record.get("raw_response_hash") != ledger.raw_response_hash
                    or call_record.get("response_ref") != ledger.response_ref
                    or call_record.get("provider_request_id") != ledger.provider_request_id
                    or call_record.get("durability_receipt") != ledger.durability_receipt
                    or base64.b64decode(ledger.raw_response_b64 or "", validate=True)
                    != call_record.get("raw_response_utf8", "").encode("utf-8")):
                raise ValueError
            bindings.append({"position": position, "ledger_hash": ledger.ledger_hash,
                             "call_record_hash": call_record["call_record_hash"]})
        return bindings
    except (AttributeError, KeyError, TypeError, ValueError,
            UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("SCENARIO_OUTCOME_AUTHORITY_INVALID") from exc


def build_scenario_outcome_receipt(manifest: dict[str, Any],
                                   bc_scorer_input: dict[str, Any],
                                   om_scorer_input: dict[str, Any],
                                   episode_receipt: dict[str, Any], *,
                                   require_production_authority: bool = True) -> dict[str, Any]:
    scorer = score_exact if require_production_authority else score_fixture_conformance_exact
    for condition, value in (("BC", bc_scorer_input), ("OM", om_scorer_input)):
        if (not isinstance(value, dict) or value.get("condition") != condition
                or value.get("manifest") != manifest
                or not validate_cohort_manifest_join(value.get("cohort_authority"), manifest)
                or validate_manifest_cut_state_receipt(
                    value.get("manifest_cut_state_receipt"), manifest,
                    require_production=require_production_authority)
                or state_reference.verify_state_authority_receipt(
                    value.get("state_authority_receipt"),
                    require_production=require_production_authority)
                or state_oracle.verify_state_authority_receipt(
                    value.get("state_authority_receipt"),
                    require_production=require_production_authority)):
            raise ValueError("SCENARIO_OUTCOME_AUTHORITY_INVALID")
    call_bindings = _outcome_episode_call_bindings(
        episode_receipt, bc_scorer_input, om_scorer_input)
    receipt = {
        "schema_id": "ScenarioOutcomeReceiptV2",
        "scenario_id": manifest["scenario_id"],
        "manifest_hash": manifest["manifest_hash"],
        "retained_set_root": manifest["retained_set_root"],
        "episode_hash": episode_receipt["episode_hash"],
        "call_bindings": call_bindings,
        "call_binding_set_hash": sha384(call_bindings),
        "bc_scorer_input": copy.deepcopy(bc_scorer_input),
        "bc_scorer_input_hash": sha384(bc_scorer_input),
        "om_scorer_input": copy.deepcopy(om_scorer_input),
        "om_scorer_input_hash": sha384(om_scorer_input),
        "authority_mode": ("PRODUCTION" if require_production_authority
                           else "FIXTURE_CONFORMANCE"),
        "bc": scorer(manifest, bc_scorer_input),
        "om": scorer(manifest, om_scorer_input),
    }
    receipt["receipt_hash"] = hash_without(receipt, "receipt_hash")
    return receipt


def validate_scenario_outcome_receipt(receipt: Any, episode_receipt: dict[str, Any], *,
                                      require_production_authority: bool = True) -> list[str]:
    try:
        if (not _shape(receipt, OUTCOME_RECEIPT_KEYS, "ScenarioOutcomeReceiptV2")
                or receipt["authority_mode"] != ("PRODUCTION" if require_production_authority
                                                  else "FIXTURE_CONFORMANCE")
                or type(receipt["bc"]) is not int or receipt["bc"] not in (0, 1)
                or type(receipt["om"]) is not int or receipt["om"] not in (0, 1)
                or receipt["receipt_hash"] != hash_without(receipt, "receipt_hash")
                or receipt["episode_hash"] != episode_receipt.get("episode_hash")
                or not isinstance(receipt["call_bindings"], list)
                or len(receipt["call_bindings"]) != 6
                or any(not isinstance(row, dict)
                       or set(row) != OUTCOME_CALL_BINDING_KEYS
                       for row in receipt["call_bindings"])
                or receipt["call_binding_set_hash"] != sha384(receipt["call_bindings"])
                or receipt["bc_scorer_input_hash"] != sha384(receipt["bc_scorer_input"])
                or receipt["om_scorer_input_hash"] != sha384(receipt["om_scorer_input"])):
            raise ValueError
        bc_input = receipt["bc_scorer_input"]
        om_input = receipt["om_scorer_input"]
        manifest = bc_input["manifest"]
        if (om_input["manifest"] != manifest
                or receipt["scenario_id"] != manifest["scenario_id"]
                or receipt["manifest_hash"] != manifest["manifest_hash"]
                or receipt["retained_set_root"] != manifest["retained_set_root"]
                or bc_input["condition"] != "BC" or om_input["condition"] != "OM"):
            raise ValueError
        for value in (bc_input, om_input):
            if (not validate_cohort_manifest_join(value.get("cohort_authority"), manifest)
                    or validate_manifest_cut_state_receipt(
                        value.get("manifest_cut_state_receipt"), manifest,
                        require_production=require_production_authority)
                    or state_reference.verify_state_authority_receipt(
                        value.get("state_authority_receipt"),
                        require_production=require_production_authority)
                    or state_oracle.verify_state_authority_receipt(
                        value.get("state_authority_receipt"),
                        require_production=require_production_authority)):
                raise ValueError
        exact_bindings = _outcome_episode_call_bindings(
            episode_receipt, bc_input, om_input)
        if receipt["call_bindings"] != exact_bindings:
            raise ValueError
        scorer = score_exact if require_production_authority else score_fixture_conformance_exact
        derived_bc = scorer(manifest, bc_input)
        derived_om = scorer(manifest, om_input)
        if (receipt["bc"], receipt["om"]) != (derived_bc, derived_om):
            raise ValueError
        return []
    except (AttributeError, KeyError, TypeError, ValueError, UnicodeError):
        return ["SCENARIO_OUTCOME_AUTHORITY_INVALID"]


def scenario_outcome_pair(receipt: dict[str, Any], episode_receipt: dict[str, Any], *,
                          require_production_authority: bool = True) -> tuple[int, int]:
    errors = validate_scenario_outcome_receipt(
        receipt, episode_receipt,
        require_production_authority=require_production_authority)
    if errors:
        raise ValueError(",".join(errors))
    return receipt["bc"], receipt["om"]
