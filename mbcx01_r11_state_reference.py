"""r11 reference state reducer. Post-ingress semantics are owned here."""

from __future__ import annotations

import copy
from typing import Any

from mbcx01_r11_common import *  # re-export the public fixture primitives


def _scope(state: dict[str, Any], scope_id: str) -> dict[str, Any]:
    return state["scopes"].setdefault(scope_id, fresh_scope())


def _response_key(payload: dict[str, Any]) -> str:
    return sha256([payload["scope_id"], payload["handoff_id"], payload["scenario_id"],
                   payload["condition"], payload["node"]])


def _fact_insert_bounds(state: dict[str, Any], versions: list[dict[str, Any]],
                        event: dict[str, Any]) -> str | None:
    start = event["valid_from"]
    explicit_end = event["valid_to"]
    known_cut = _current_fact_cut(state, event)
    future_starts = [row["valid_from"] for row in versions
                     if not retracted_at(row, known_cut) and row["valid_from"] > start]
    end = explicit_end if explicit_end is not None else min(future_starts, default=None)
    if end is not None and end <= start:
        raise ValueError("fact interval must be nonempty")
    return end


def _intervals_overlap(a_start: str, a_end: str | None,
                       b_start: str, b_end: str | None) -> bool:
    return (b_end is None or a_start < b_end) and (a_end is None or b_start < a_end)


def _current_fact_cut(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    return {"journal_seq": state["next_seq"] - 1, "knowledge_time": event["observed_at"],
            "valid_time": event["valid_from"]}


def _apply_effect(new: dict[str, Any], event: dict[str, Any]) -> str:
    event_type, payload = event["event_type"], event["payload"]
    scope = _scope(new, event["scope_id"])
    obligations = scope["obligations"]

    if event_type in {"assert_fact", "correct_fact", "retract_fact"}:
        key = fact_key(payload["subject_id"], payload["predicate_id"])
        versions = scope["facts"].setdefault(key, [])
        cut = event["originating_cut"]
        if event_type == "assert_fact":
            if any(visible_effective(row, cut) for row in versions):
                return "FACT_ALREADY_EXISTS"
            end = _fact_insert_bounds(new, versions, event)
            known_cut = _current_fact_cut(new, event)
            for row in versions:
                row_end = effective_valid_to(row, known_cut)
                if (not retracted_at(row, known_cut)
                        and row["journal_seq"] <= known_cut["journal_seq"]
                        and row["observed_at"] <= known_cut["knowledge_time"]
                        and _intervals_overlap(event["valid_from"], end, row["valid_from"], row_end)):
                    return "FACT_ALREADY_EXISTS"
            versions.append({"event_id": event["event_id"], "parent_event_id": None,
                             "value_code": payload["value_code"], "observed_at": event["observed_at"],
                             "valid_from": event["valid_from"], "valid_to": end,
                             "journal_seq": event["journal_seq"], "retracted": False,
                             "closure_events": [], "retraction_events": []})
            versions.sort(key=lambda row: (row["valid_from"], row["journal_seq"]))
            return "APPLIED"
        target_name = "parent_event_id" if event_type == "correct_fact" else "target_event_id"
        target = next((row for row in versions if row["event_id"] == payload[target_name]), None)
        if target is None or not visible_effective(target, cut):
            return "FACT_PARENT_NOT_HEAD" if event_type == "correct_fact" else "FACT_TARGET_UNAVAILABLE"
        if event_type == "retract_fact":
            target.setdefault("retraction_events", []).append({
                "event_id": event["event_id"], "journal_seq": event["journal_seq"],
                "observed_at": event["observed_at"]})
            return "APPLIED"
        if any(row["parent_event_id"] == target["event_id"] and visible_effective(row, cut)
               for row in versions):
            return "FACT_PARENT_NOT_HEAD"
        old_end = effective_valid_to(target, cut)
        if event["valid_from"] <= target["valid_from"]:
            return "FACT_PARENT_NOT_HEAD"
        if old_end is not None and event["valid_from"] >= old_end:
            return "FACT_PARENT_NOT_HEAD"
        child_end = event["valid_to"] if event["valid_to"] is not None else old_end
        if (child_end is not None and child_end <= event["valid_from"]
                or old_end is not None and child_end is not None and child_end > old_end):
            return "FACT_PARENT_NOT_HEAD"
        known_cut = _current_fact_cut(new, event)
        for row in versions:
            if row is target:
                continue
            row_end = effective_valid_to(row, known_cut)
            if (not retracted_at(row, known_cut) and row["journal_seq"] <= known_cut["journal_seq"]
                    and row["observed_at"] <= known_cut["knowledge_time"]
                    and _intervals_overlap(event["valid_from"], child_end,
                                           row["valid_from"], row_end)):
                return "FACT_PARENT_NOT_HEAD"
        target.setdefault("closure_events", []).append({
            "event_id": event["event_id"], "journal_seq": event["journal_seq"],
            "observed_at": event["observed_at"], "valid_to": event["valid_from"]})
        versions.append({"event_id": event["event_id"], "parent_event_id": target["event_id"],
                         "value_code": payload["value_code"], "observed_at": event["observed_at"],
                         "valid_from": event["valid_from"], "valid_to": child_end,
                         "journal_seq": event["journal_seq"], "retracted": False,
                         "closure_events": [], "retraction_events": []})
        versions.sort(key=lambda row: (row["valid_from"], row["journal_seq"]))
        return "APPLIED"

    if event_type == "open_obligation":
        oid = payload["obligation_id"]
        prereqs = payload["prerequisite_obligation_ids"]
        if (oid in obligations or any(p not in obligations for p in prereqs)
                or payload["completion_action_id"] != action_id(event["scope_id"], oid)):
            return "OBLIGATION_ALREADY_EXISTS_OR_BAD_PREREQUISITE"
        obligations[oid] = {"subject_id": payload["subject_id"], "owner_role": payload["owner_role"],
                            "due_at": payload["due_at"], "critical": payload["critical"],
                            "lifecycle": "OPEN", "completion_action_id": payload["completion_action_id"],
                            "prerequisite_obligation_ids": sorted(prereqs), "terminal_event_id": None}
        scope["dependencies"].extend([[oid, p] for p in prereqs])
        scope["dependencies"].sort()
        return "APPLIED"

    if event_type in {"reschedule_obligation", "delegate_obligation", "complete_obligation",
                      "cancel_obligation", "reopen_obligation"}:
        obligation = obligations.get(payload["obligation_id"])
        if event_type == "reopen_obligation":
            if not obligation or obligation["lifecycle"] not in {"COMPLETED", "CANCELLED"}:
                return "OBLIGATION_NOT_TERMINAL"
            obligation.update(lifecycle="OPEN", due_at=payload["due_at"], owner_role=payload["owner_role"],
                              terminal_event_id=None)
            return "APPLIED"
        if not obligation or obligation["lifecycle"] != "OPEN":
            return "OBLIGATION_NOT_OPEN"
        if event_type == "reschedule_obligation":
            obligation["due_at"] = payload["due_at"]
        elif event_type == "delegate_obligation":
            obligation["owner_role"] = payload["owner_role"]
        elif event_type == "cancel_obligation":
            obligation.update(lifecycle="CANCELLED", terminal_event_id=event["event_id"])
        else:
            cut = event["originating_cut"]
            legal = (obligation["critical"] and obligation["due_at"] <= cut["valid_time"]
                     and obligation["completion_action_id"] == payload["completion_action_id"]
                     and payload["originating_cut_hash"] == cut_hash(cut)
                     and all(obligations.get(p, {}).get("lifecycle") == "COMPLETED"
                             for p in obligation["prerequisite_obligation_ids"]))
            if not legal:
                return "OBLIGATION_NOT_DUE_AT_ORIGINATING_CUT"
            obligation.update(lifecycle="COMPLETED", terminal_event_id=event["event_id"])
        return "APPLIED"

    if event_type in {"link_dependency", "unlink_dependency"}:
        edge = [payload["obligation_id"], payload["prerequisite_obligation_id"]]
        if event_type == "link_dependency":
            if (edge in scope["dependencies"] or edge[0] == edge[1]
                    or any(obligations.get(x, {}).get("lifecycle") != "OPEN" for x in edge)
                    or has_path(scope["dependencies"], edge[1], edge[0])):
                return "DEPENDENCY_ILLEGAL"
            scope["dependencies"].append(edge); scope["dependencies"].sort()
            obligations[edge[0]]["prerequisite_obligation_ids"] = sorted(set(
                obligations[edge[0]]["prerequisite_obligation_ids"] + [edge[1]]))
            return "APPLIED"
        if edge not in scope["dependencies"]:
            return "DEPENDENCY_NOT_FOUND"
        scope["dependencies"].remove(edge)
        obligations[edge[0]]["prerequisite_obligation_ids"].remove(edge[1])
        return "APPLIED"

    if event_type == "open_handoff":
        hid = payload["handoff_id"]
        target = obligations.get(payload["target_obligation_id"])
        if hid in scope["handoffs"] or not target or target["lifecycle"] != "OPEN":
            return "HANDOFF_OR_TARGET_ILLEGAL"
        try:
            task_packet = json.loads(payload["task_packet_utf8"])
            manifest = json.loads(payload["manifest_utf8"])
        except (TypeError, ValueError):
            return "HANDOFF_OR_TARGET_ILLEGAL"
        authority_ok = (
            isinstance(task_packet, dict) and isinstance(manifest, dict)
            and payload["task_packet_utf8"] == canonical_json(task_packet).decode("utf-8")
            and payload["manifest_utf8"] == canonical_json(manifest).decode("utf-8")
            and task_packet.get("task_packet_hash") == payload["task_packet_hash"]
            and task_packet.get("task_packet_hash") == sha384({
                key: value for key, value in task_packet.items() if key != "task_packet_hash"})
            and task_packet.get("scenario_id") == payload["scenario_id"]
            and task_packet.get("scope_id") == event["scope_id"]
            and task_packet.get("manifest_hash") == payload["manifest_hash"]
            and task_packet.get("requested_action_catalog_hash") == payload["action_catalog_hash"]
            and manifest.get("manifest_hash") == payload["manifest_hash"]
            and manifest.get("manifest_hash") == sha384({
                key: value for key, value in manifest.items() if key != "manifest_hash"})
            and manifest.get("scenario_id") == payload["scenario_id"]
            and manifest.get("scope_id") == event["scope_id"]
            and manifest.get("action_catalog_hash") == payload["action_catalog_hash"]
            and manifest.get("action_catalog") == payload["action_catalog"])
        target_action = action_id(event["scope_id"], payload["target_obligation_id"])
        if (not authority_ok
                or payload["originating_cut_hash"] != cut_hash(event["originating_cut"])
                or payload["action_catalog_hash"] != sha384(payload["action_catalog"])
                or payload["canonical_snapshot_hash"] != sha384(obligations)
                or not any(row["action_id"] == target_action
                           and row["obligation_id"] == payload["target_obligation_id"]
                           for row in payload["action_catalog"]
                           if row.get("obligation_id") is not None)
                or any(row.get("action_id") != action_id(event["scope_id"], row["obligation_id"])
                       or ("scope_id" in row and row["scope_id"] != event["scope_id"])
                       for row in payload["action_catalog"]
                       if row.get("obligation_id") is not None)):
            return "HANDOFF_OR_TARGET_ILLEGAL"
        scope["handoffs"][hid] = {
            "status": "OPEN", "terminal_disposition": None, "scenario_id": payload["scenario_id"],
            "condition": payload["condition"], "target_obligation_id": payload["target_obligation_id"],
            "task_packet_hash": payload["task_packet_hash"], "served_request_hash": payload["served_request_hash"],
            "request_parameters_hash": payload["request_parameters_hash"],
            "idempotency_token": payload["idempotency_token"],
            "task_packet_utf8": payload["task_packet_utf8"],
            "manifest_utf8": payload["manifest_utf8"],
            "route_contract_hash": payload["route_contract_hash"],
            "manifest_hash": payload["manifest_hash"],
            "originating_cut": copy.deepcopy(event["originating_cut"]),
            "originating_cut_hash": payload["originating_cut_hash"],
            "scope_id": event["scope_id"], "opened_journal_seq": event["journal_seq"],
            "opened_observed_at": event["observed_at"],
            "action_catalog": copy.deepcopy(payload["action_catalog"]),
            "originating_obligations": copy.deepcopy(obligations),
            "proposal_event_id": None, "proposal_hash": None,
            "worker_handoff_hash": None, "action_ids": [],
        }
        return "APPLIED"

    if event_type == "record_call_response":
        handoff = scope["handoffs"].get(payload["handoff_id"])
        worker = json.loads(payload["raw_response_utf8"])
        exact_handoff = (handoff and handoff["status"] == "OPEN"
                         and handoff["scope_id"] == event["scope_id"]
                         and handoff["scenario_id"] == payload["scenario_id"]
                         and handoff["condition"] == payload["condition"]
                         and handoff["task_packet_hash"] == payload["task_packet_hash"]
                         and handoff["served_request_hash"] == payload["served_request_hash"]
                         and handoff["request_parameters_hash"] == payload["request_parameters_hash"]
                         and handoff["idempotency_token"] == payload["idempotency_token"]
                         and handoff["route_contract_hash"] == payload["route_contract_hash"]
                         and worker["scope_id"] == event["scope_id"]
                         and worker["manifest_hash"] == handoff["manifest_hash"]
                         and worker["proposed_action_ids"] == [
                             action_id(event["scope_id"], handoff["target_obligation_id"])]
                         and worker["produced_at"] >= handoff["opened_observed_at"]
                         and worker["produced_at"] <= payload["accepted_at"] <= event["observed_at"]
                         and event["journal_seq"] > handoff["opened_journal_seq"])
        if not exact_handoff:
            return "CALL_RESPONSE_CONFLICT"
        record = {**copy.deepcopy(payload), "scope_id": event["scope_id"],
                  "record_event_id": event["event_id"], "journal_seq": event["journal_seq"],
                  "parsed_proposed_action_ids": copy.deepcopy(worker["proposed_action_ids"])}
        key = _response_key(record)
        if (any(_response_key(row) == key for row in new["responses"])
                or any(row["response_ref"] == payload["response_ref"]
                       or row["provider_request_id"] == payload["provider_request_id"]
                       or row["durability_receipt"]["transaction_id"]
                       == payload["durability_receipt"]["transaction_id"]
                       for row in new["responses"])):
            return "CALL_RESPONSE_CONFLICT"
        new["responses"].append(record)
        return "APPLIED"

    handoff = scope["handoffs"].get(payload.get("handoff_id"))
    if event_type == "propose_handoff_result":
        if not handoff or handoff["status"] != "OPEN":
            return "PROPOSAL_INVALID"
        key = sha256([event["scope_id"], payload["handoff_id"], handoff["scenario_id"],
                      handoff["condition"], "B"])
        matches = [row for row in new["responses"] if _response_key(row) == key]
        response = matches[0] if len(matches) == 1 else None
        exact = (response and response["worker_handoff_hash"] == payload["worker_handoff_hash"]
                 and response["task_packet_hash"] == handoff["task_packet_hash"]
                 and response["served_request_hash"] == handoff["served_request_hash"]
                 and response["request_parameters_hash"] == handoff["request_parameters_hash"]
                 and response["route_contract_hash"] == handoff["route_contract_hash"]
                 and response["parsed_proposed_action_ids"] == payload["action_ids"])
        target_action = action_id(event["scope_id"], handoff["target_obligation_id"])
        if (not exact or payload["originating_cut_hash"] != handoff["originating_cut_hash"]
                or payload["action_ids"] != [target_action]
                or not action_targets_legal(handoff["originating_obligations"], handoff["action_catalog"],
                                            payload["action_ids"], handoff["originating_cut"]["valid_time"])):
            return "PROPOSAL_INVALID"
        handoff.update(status="PROPOSED", proposal_event_id=event["event_id"],
                       proposal_hash=sha384(event),
                       worker_handoff_hash=payload["worker_handoff_hash"],
                       action_ids=sorted(payload["action_ids"]))
        return "APPLIED"
    if event_type == "commit_handoff_result":
        if (not handoff or handoff["status"] != "PROPOSED"
                or payload["proposal_event_id"] != handoff["proposal_event_id"]):
            return "COMMIT_INVALID"
        targets = {row["action_id"]: row["obligation_id"] for row in handoff["action_catalog"]
                   if row.get("obligation_id") is not None}
        current_legal = action_targets_legal(obligations, handoff["action_catalog"],
                                             handoff["action_ids"],
                                             handoff["originating_cut"]["valid_time"])
        unchanged_targets = all(obligations.get(targets[aid])
                                == handoff["originating_obligations"].get(targets[aid])
                                for aid in handoff["action_ids"])
        if (not action_targets_legal(handoff["originating_obligations"], handoff["action_catalog"],
                                     handoff["action_ids"], handoff["originating_cut"]["valid_time"])
                or not current_legal or not unchanged_targets):
            return "COMMIT_INVALID"
        for aid in handoff["action_ids"]:
            obligations[targets[aid]].update(lifecycle="COMPLETED", terminal_event_id=event["event_id"])
        handoff.update(status="COMMITTED", terminal_disposition="COMMITTED")
        return "APPLIED"
    if event_type == "reject_handoff_result":
        stored_hash = handoff.get("proposal_hash") if handoff else None
        persisted_hash = (new["events"].get(handoff.get("proposal_event_id"))
                          if handoff else None)
        if (not handoff or handoff["status"] != "PROPOSED"
                or payload["proposal_hash"] != stored_hash
                or stored_hash != persisted_hash):
            return "REJECTION_INVALID"
        handoff.update(status="REJECTED", terminal_disposition=payload["rejection_code"])
        return "APPLIED"
    if event_type == "close_handoff":
        if not handoff or handoff["status"] not in {"COMMITTED", "REJECTED"}:
            return "HANDOFF_NOT_TERMINAL"
        handoff["status"] = "CLOSED"
        return "APPLIED"
    return "SCHEMA_INVALID"


def reference_apply(state: dict[str, Any], event: dict[str, Any]) -> tuple[dict[str, Any], str]:
    error = structural_error(state, event)
    if error:
        return copy.deepcopy(state), error
    replay = preflight_replay(state, event)
    if replay:
        return copy.deepcopy(state), replay
    new = copy.deepcopy(state)
    result = _apply_effect(new, event)
    if result != "APPLIED":
        return copy.deepcopy(state), result
    return finish_applied(new, event), result


def handoff_fixture_payload() -> dict[str, Any]:
    state = initial_state()
    cut = current_cut(state)
    actions = [{"action_id": action_id("SCOPE.SHARED", "OBL.SHARED"),
                "obligation_id": "OBL.SHARED"}]
    manifest = {"schema_id": "StateManifestAuthorityV1", "scenario_id": "SCENARIO.SHARED",
                "scope_id": "SCOPE.SHARED", "action_catalog": actions,
                "action_catalog_hash": sha384(actions)}
    manifest["manifest_hash"] = sha384(manifest)
    task = {"schema_id": "StateTaskAuthorityV1", "scenario_id": "SCENARIO.SHARED",
            "scope_id": "SCOPE.SHARED", "manifest_hash": manifest["manifest_hash"],
            "requested_action_catalog_hash": manifest["action_catalog_hash"]}
    task["task_packet_hash"] = sha384(task)
    return {"handoff_id": "HANDOFF.SHARED", "scenario_id": "SCENARIO.SHARED", "condition": "BC",
            "target_obligation_id": "OBL.SHARED", "task_packet_hash": task["task_packet_hash"],
            "served_request_hash": "B" * 64, "request_parameters_hash": "C" * 96,
            "idempotency_token": "IDEM.SCENARIO.SHARED.BC.B",
            "task_packet_utf8": canonical_json(task).decode("utf-8"),
            "manifest_utf8": canonical_json(manifest).decode("utf-8"),
            "originating_cut_hash": cut_hash(cut), "action_catalog_hash": sha384(actions),
            "canonical_snapshot_hash": sha384(state["scopes"]["SCOPE.SHARED"]["obligations"]),
            "route_contract_hash": "D" * 96, "manifest_hash": manifest["manifest_hash"],
            "action_catalog": actions}


def response_fixture_payload(handoff: dict[str, Any]) -> dict[str, Any]:
    worker = {"schema_id": "WorkerHandoffV5", "scenario_id": handoff["scenario_id"],
              "scope_id": "SCOPE.SHARED", "condition": handoff["condition"],
              "task_packet_hash": handoff["task_packet_hash"],
              "served_request_hash": handoff["served_request_hash"],
              "manifest_hash": handoff["manifest_hash"],
              "status_code": "PROPOSE",
              "proposed_action_ids": [row["action_id"] for row in handoff["action_catalog"]],
              "produced_at": T1}
    worker["worker_handoff_hash"] = sha384(worker)
    raw = canonical_json(worker).decode("utf-8")
    raw_hash = sha384(raw.encode("utf-8"))
    response_ref = "RESPONSE.SHARED"
    response = {"handoff_id": handoff["handoff_id"], "scenario_id": handoff["scenario_id"],
            "condition": handoff["condition"], "node": "B", "task_packet_hash": handoff["task_packet_hash"],
            "served_request_hash": handoff["served_request_hash"],
            "request_parameters_hash": handoff["request_parameters_hash"],
            "idempotency_token": handoff["idempotency_token"],
            "raw_response_utf8": raw, "raw_response_hash": raw_hash,
            "worker_handoff_hash": worker["worker_handoff_hash"],
            "response_ref": response_ref, "provider_request_id": "PROVIDER.SHARED",
            "accepted_at": T1}
    response["route_contract_hash"] = handoff["route_contract_hash"]
    response["durability_receipt"] = make_durability_receipt(response, "TXN.SHARED")
    return response
