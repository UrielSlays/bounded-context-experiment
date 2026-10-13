"""Typed r12 packet graph and exact causal scorer. No provider calls."""

from __future__ import annotations

import copy
from typing import Any

from mbcx01_r12_common import (SHA384, T0, T1, _valid_utc, action_id, canonical_json,
                               make_durability_receipt, sha256, sha384,
                               valid_durability_receipt)
import mbcx01_r12_state_oracle as state_oracle
import mbcx01_r12_state_reference as state_reference


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


def packet_fixture_manifest() -> dict[str, Any]:
    scope = "SCOPE.SHARED"
    target_action = action_id(scope, "OBL.SHARED")
    decoy_action = action_id(scope, "OBL.DECOY")
    world = [
        {"object_id": "DEP.SHARED.PREREQ", "object_kind": "DEPENDENCY",
         "fields": {"obligation_id": "OBL.SHARED", "prerequisite_obligation_id": "OBL.PREREQ"},
         "source_event_ids": ["SOURCE.DEP"]},
        {"object_id": "OBL.DECOY", "object_kind": "OBLIGATION",
         "fields": {"lifecycle": "OPEN", "critical": False, "due_at": T0,
                    "completion_action_id": decoy_action, "prerequisite_obligation_ids": []},
         "source_event_ids": ["SOURCE.DECOY"]},
        {"object_id": "OBL.PREREQ", "object_kind": "OBLIGATION",
         "fields": {"lifecycle": "COMPLETED", "critical": True, "due_at": T0,
                    "completion_action_id": action_id(scope, "OBL.PREREQ"),
                    "prerequisite_obligation_ids": []},
         "source_event_ids": ["SOURCE.PREREQ"]},
        {"object_id": "OBL.SHARED", "object_kind": "OBLIGATION",
         "fields": {"lifecycle": "OPEN", "critical": True, "due_at": T0,
                    "completion_action_id": target_action,
                    "prerequisite_obligation_ids": ["OBL.PREREQ"]},
         "source_event_ids": ["SOURCE.TARGET"]},
        {"object_id": "OBS.SHARED", "object_kind": "OBSERVATION",
         "fields": {"code": "TARGET_VISIBLE", "observed_at": T1},
         "source_event_ids": ["SOURCE.OBS"]},
    ]
    world.sort(key=lambda row: row["object_id"].encode("utf-8"))
    actions = [
        {"action_id": decoy_action, "action_kind": "ACT_ON_OBLIGATION",
         "scope_id": scope, "obligation_id": "OBL.DECOY"},
        {"action_id": target_action, "action_kind": "ACT_ON_OBLIGATION",
         "scope_id": scope, "obligation_id": "OBL.SHARED"},
        {"action_id": "NO_ACTION", "action_kind": "NO_ACTION"},
    ]
    actions.sort(key=lambda row: row["action_id"].encode("utf-8"))
    manifest = {
        "schema_id": "ExpectedScenarioManifestV2", "scenario_id": "SCENARIO.SHARED",
        "scope_id": scope,
        "cut": {"journal_seq": 1, "knowledge_time": T1, "valid_time": T1},
        "observation": {"scope_id": scope, "observed_at": T1, "code": "TARGET_VISIBLE"},
        "canonical_world": world, "canonical_world_hash": sha384(world),
        "action_catalog": actions, "action_catalog_hash": sha384(actions),
        "route_contract_hash": "D" * 96,
        "candidate_selector_id": "SELECTOR.FD.V1",
        "bc_selected_object_ids": ["OBL.SHARED", "OBS.SHARED"],
        "bc_selection_hash": "", "gold_read_set": [], "gold_action_id": target_action,
        "expected_a1_action_ids": [],
    }
    manifest["bc_selection_hash"] = sha384([
        manifest["candidate_selector_id"], manifest["bc_selected_object_ids"]])
    manifest["gold_read_set"] = _expected_gold_read_set(manifest, target_action)
    manifest["manifest_hash"] = hash_without(manifest, "manifest_hash")
    return manifest


MANIFEST_KEYS = {"schema_id", "scenario_id", "scope_id", "cut", "observation",
                 "canonical_world", "canonical_world_hash", "action_catalog", "action_catalog_hash",
                 "route_contract_hash",
                 "candidate_selector_id", "bc_selected_object_ids", "bc_selection_hash",
                 "gold_read_set", "gold_action_id", "expected_a1_action_ids", "manifest_hash"}


def validate_expected_manifest(manifest: Any) -> list[str]:
    errors: set[str] = set()
    if not isinstance(manifest, dict) or set(manifest) != MANIFEST_KEYS:
        return ["MANIFEST_SCHEMA_INVALID"]
    if manifest.get("schema_id") != "ExpectedScenarioManifestV2":
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


def _postcommit_world(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    world = copy.deepcopy(manifest["canonical_world"])
    action = next(row for row in manifest["action_catalog"]
                  if row.get("action_id") == manifest["gold_action_id"])
    target = next(row for row in world if row["object_id"] == action["obligation_id"])
    target["fields"]["lifecycle"] = "COMPLETED"
    return world


def build_decision_packet(manifest: dict[str, Any], condition: str, stage: str,
                          *, postcommit_cut: dict[str, Any] | None = None) -> dict[str, Any]:
    if validate_expected_manifest(manifest):
        raise ValueError("invalid expected manifest")
    if condition not in {"BC", "OM"} or stage not in {"A0_PRECOMMIT", "A1_POSTCOMMIT"}:
        raise ValueError("invalid condition or stage")
    selected = (manifest["bc_selected_object_ids"] if condition == "BC" else manifest["gold_read_set"])
    ids = _object_closure(manifest, selected)
    source_world = _world_map(manifest)
    if stage == "A1_POSTCOMMIT":
        source_world = {row["object_id"]: row for row in _postcommit_world(manifest)}
    packet = {
        "schema_id": "DecisionPacketV5", "stage": stage, "condition": condition,
        "scenario_id": manifest["scenario_id"], "scope_id": manifest["scope_id"],
        "cut": copy.deepcopy(postcommit_cut if stage == "A1_POSTCOMMIT" else manifest["cut"]),
        "objects": [copy.deepcopy(source_world[name]) for name in ids],
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
           "condition": condition, "node": node, "task_packet_hash": task_hash,
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
    if result != "APPLIED" or state_reference.current_cut(state) != manifest["cut"]:
        raise ValueError("default authoritative state does not match manifest cut")
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


def build_scoring_fixture(manifest: dict[str, Any], condition: str = "OM", *,
                          authoritative_state: dict[str, Any] | None = None) -> dict[str, Any]:
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
    authority = build_transition_authority(
        manifest, condition, task, worker, b_call,
        authoritative_state=authoritative_state)
    child = copy.deepcopy(authority["applied_child_event"])
    final_cut = copy.deepcopy(authority["postcommit_cut"])
    post_world = _postcommit_world(manifest)
    receipt = {"schema_id": "WriterReceiptV2", "manifest_hash": manifest["manifest_hash"],
               "worker_handoff_hash": worker["worker_handoff_hash"],
               "worker_call_record_hash": b_call["call_record_hash"], "status_code": "COMMITTED",
               "committed_action_ids": [manifest["gold_action_id"]], "child_events": [child],
               "transition_authority_hash": authority["transition_authority_hash"],
               "precommit_state_hash": authority["precommit_state_hash"],
               "proposal_event_hash": authority["proposal_event_hash"],
               "applied_child_event_hash": authority["applied_child_event_hash"],
               "postcommit_cut": final_cut,
               "postcommit_state_hash": authority["postcommit_state_hash"],
               "postcommit_world_hash": sha384(post_world)}
    receipt["receipt_hash"] = hash_without(receipt, "receipt_hash")
    a1_packet = build_decision_packet(
        manifest, condition, "A1_POSTCOMMIT", postcommit_cut=final_cut)
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
            "transition_authority": authority, "writer_receipt": receipt,
            "a1_packet": a1_packet, "a1_call_record": a1_call, "a1_result": a1_result}


TOP_KEYS = {"schema_id", "condition", "manifest", "a0_packet", "a0_call_record", "a0_result",
            "task_packet", "b_call_record", "worker_handoff", "transition_authority",
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
             "served_request_hash", "request_parameters_hash", "idempotency_token",
             "route_contract_hash", "raw_response_utf8", "raw_response_hash", "parsed_response_hash",
             "response_ref", "provider_request_id", "durability_receipt", "accepted_at",
             "call_record_hash"}
RECEIPT_KEYS = {"schema_id", "manifest_hash", "worker_handoff_hash", "worker_call_record_hash",
                 "status_code", "committed_action_ids", "child_events", "postcommit_cut",
                 "transition_authority_hash", "precommit_state_hash", "proposal_event_hash",
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


def validate_scorer_input(expected_manifest: dict[str, Any], value: Any) -> list[str]:
    errors: set[str] = set(validate_expected_manifest(expected_manifest))
    if errors:
        return sorted(errors)
    if not isinstance(value, dict) or set(value) != TOP_KEYS or value.get("schema_id") != "ScorerInputV1":
        return sorted(errors | {"SCORER_INPUT_SCHEMA_INVALID"})
    if value["manifest"] != expected_manifest:
        errors.add("EXPECTED_MANIFEST_MISMATCH")
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
    post_world = _postcommit_world(expected_manifest)
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
            or receipt.get("postcommit_world_hash") != sha384(post_world)
            or receipt.get("receipt_hash") != hash_without(receipt, "receipt_hash")):
        errors.add("WRITER_RECEIPT_INVALID")
    a1_packet, a1_result, a1_call = value["a1_packet"], value["a1_result"], value["a1_call_record"]
    expected_a1 = (build_decision_packet(
        expected_manifest, condition, "A1_POSTCOMMIT",
        postcommit_cut=receipt.get("postcommit_cut"))
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
    return sorted(errors)


def score_exact(expected_manifest: dict[str, Any], scorer_input: dict[str, Any]) -> int:
    try:
        return int(not validate_scorer_input(expected_manifest, scorer_input))
    except (AttributeError, KeyError, TypeError, ValueError, UnicodeError):
        return 0
