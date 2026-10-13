"""Independent declarative state oracle for the MBCX-01 r9 preregistration.

This implementation deliberately does not call the journal reducer or any of its
guard/effect helpers. The two implementations share only canonical serialization,
contract loading, and the public state representation used for differential checks.
"""

from __future__ import annotations

import copy
import hashlib
from typing import Any, Callable

from mbcx01_r9_reference import canonical_json, cut_hash, load_contract


EXPECTED_ENVELOPE = {
    "event_id", "scope_id", "event_type", "semantic_operation", "idempotency_key",
    "journal_seq", "observed_at", "valid_from", "valid_to", "originating_cut", "payload",
}


def _event_digest(event: dict[str, Any]) -> str:
    return hashlib.sha384(canonical_json(event)).hexdigest().upper()


def _meaning_digest(event: dict[str, Any]) -> str:
    meaning = {name: event[name] for name in (
        "scope_id", "semantic_operation", "idempotency_key", "valid_from", "valid_to",
        "originating_cut", "payload")}
    return hashlib.sha384(canonical_json(meaning)).hexdigest().upper()


def _idem_address(event: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json((event["scope_id"], event["semantic_operation"],
                                          event["idempotency_key"]))).hexdigest().upper()


def _fact_address(payload: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json((payload["subject_id"],
                                          payload["predicate_id"]))).hexdigest().upper()


def _get_scope(state: dict[str, Any], scope_id: str) -> dict[str, Any]:
    if scope_id not in state["scopes"]:
        state["scopes"][scope_id] = {
            "facts": {}, "obligations": {}, "dependencies": [], "handoffs": {}}
    return state["scopes"][scope_id]


def _check_envelope(state: dict[str, Any], event: Any,
                    rules: dict[str, Any]) -> str | None:
    if not isinstance(event, dict) or set(event) != EXPECTED_ENVELOPE:
        return "SCHEMA_INVALID"
    event_type = event.get("event_type")
    rule = rules.get(event_type)
    if rule is None or rule["semantic_operation"] != event.get("semantic_operation"):
        return "SCHEMA_INVALID"
    if not isinstance(event.get("payload"), dict) or set(event["payload"]) != set(
            rule["payload_schema"]["required"]):
        return "SCHEMA_INVALID"
    previous_event = state["event_fingerprints"].get(event["event_id"])
    if previous_event is not None:
        return "DUPLICATE_NOOP" if previous_event == _event_digest(event) else "EVENT_ID_CONFLICT"
    previous_meaning = state["idempotency"].get(_idem_address(event))
    if previous_meaning is not None:
        return "DUPLICATE_NOOP" if previous_meaning == _meaning_digest(event) else "IDEMPOTENCY_CONFLICT"
    if event["journal_seq"] != state["next_seq"]:
        return "JOURNAL_SEQUENCE_INVALID"
    cut = event["originating_cut"]
    expected_cut_keys = {"journal_seq", "knowledge_time", "valid_time"}
    if (not isinstance(cut, dict) or set(cut) != expected_cut_keys
            or cut["journal_seq"] != state["next_seq"] - 1
            or cut["knowledge_time"] > event["observed_at"]):
        return "ORIGINATING_CUT_INVALID"
    if event["valid_to"] is not None and event["valid_to"] <= event["valid_from"]:
        return "VALID_INTERVAL_INVALID"
    return None


def _finish(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    state["journal"].append(event["event_id"])
    state["event_fingerprints"][event["event_id"]] = _event_digest(event)
    state["idempotency"][_idem_address(event)] = _meaning_digest(event)
    state["next_seq"] = event["journal_seq"] + 1
    return state


def _cycle_if_added(edges: list[list[str]], child: str, parent: str) -> bool:
    outgoing: dict[str, set[str]] = {}
    for left, right in edges + [[child, parent]]:
        outgoing.setdefault(left, set()).add(right)
    colors: dict[str, int] = {}

    def visit(node: str) -> bool:
        color = colors.get(node, 0)
        if color == 1:
            return True
        if color == 2:
            return False
        colors[node] = 1
        for neighbor in outgoing.get(node, set()):
            if visit(neighbor):
                return True
        colors[node] = 2
        return False

    return any(visit(node) for node in list(outgoing))


def _targets_are_legal(handoff: dict[str, Any], actions: list[str]) -> bool:
    catalog: dict[str, str] = {}
    for entry in handoff["action_catalog"]:
        if entry["action_id"] in catalog:
            return False
        catalog[entry["action_id"]] = entry["obligation_id"]
    if any(action not in catalog for action in actions):
        return False
    obligations = handoff["originating_obligations"]
    at_time = handoff["originating_cut"]["valid_time"]
    for action in actions:
        obligation = obligations.get(catalog[action])
        if not obligation:
            return False
        if (obligation["lifecycle"] != "OPEN" or not obligation["critical"]
                or obligation["due_at"] > at_time
                or obligation["completion_action_id"] != action):
            return False
        for prerequisite in obligation["prerequisite_obligation_ids"]:
            if obligations.get(prerequisite, {}).get("lifecycle") != "COMPLETED":
                return False
    return True


def _fact_handler(state: dict[str, Any], event: dict[str, Any],
                  rule: dict[str, Any]) -> str:
    scope = _get_scope(state, event["scope_id"])
    payload = event["payload"]
    versions = scope["facts"].setdefault(_fact_address(payload), [])
    event_type = event["event_type"]
    if event_type == "assert_fact":
        if any(not version["retracted"] and version["valid_to"] is None for version in versions):
            return rule["illegal_result"]
        versions.append({
            "event_id": event["event_id"], "parent_event_id": None,
            "value_code": payload["value_code"], "observed_at": event["observed_at"],
            "valid_from": event["valid_from"], "valid_to": event["valid_to"],
            "journal_seq": event["journal_seq"], "retracted": False,
        })
        return "APPLIED"
    if event_type == "correct_fact":
        parent = None
        for version in versions:
            if version["event_id"] == payload["parent_event_id"]:
                parent = version
        has_child = any(version["parent_event_id"] == payload["parent_event_id"]
                        for version in versions)
        if parent is None or parent["retracted"] or parent["valid_to"] is not None or has_child:
            return rule["illegal_result"]
        parent["valid_to"] = event["valid_from"]
        versions.append({
            "event_id": event["event_id"], "parent_event_id": payload["parent_event_id"],
            "value_code": payload["value_code"], "observed_at": event["observed_at"],
            "valid_from": event["valid_from"], "valid_to": event["valid_to"],
            "journal_seq": event["journal_seq"], "retracted": False,
        })
        return "APPLIED"
    target = None
    for version in versions:
        if version["event_id"] == payload["target_event_id"]:
            target = version
    if (target is None or target["retracted"]
            or target["journal_seq"] > event["originating_cut"]["journal_seq"]):
        return rule["illegal_result"]
    target["retracted"] = True
    return "APPLIED"


def _obligation_handler(state: dict[str, Any], event: dict[str, Any],
                        rule: dict[str, Any]) -> str:
    scope = _get_scope(state, event["scope_id"])
    obligations = scope["obligations"]
    payload = event["payload"]
    event_type = event["event_type"]
    if event_type == "open_obligation":
        oid = payload["obligation_id"]
        prerequisites = payload["prerequisite_obligation_ids"]
        if oid in obligations or any(item not in obligations for item in prerequisites):
            return rule["illegal_result"]
        obligations[oid] = {
            "subject_id": payload["subject_id"], "owner_role": payload["owner_role"],
            "due_at": payload["due_at"], "critical": payload["critical"], "lifecycle": "OPEN",
            "completion_action_id": payload["completion_action_id"],
            "prerequisite_obligation_ids": list(prerequisites), "terminal_event_id": None,
        }
        scope["dependencies"].extend([[oid, item] for item in prerequisites])
        scope["dependencies"].sort()
        return "APPLIED"
    obligation = obligations.get(payload["obligation_id"])
    if event_type == "reopen_obligation":
        if obligation is None or obligation["lifecycle"] not in {"COMPLETED", "CANCELLED"}:
            return rule["illegal_result"]
        obligation["lifecycle"] = "OPEN"
        obligation["due_at"] = payload["due_at"]
        obligation["owner_role"] = payload["owner_role"]
        obligation["terminal_event_id"] = None
        return "APPLIED"
    if obligation is None or obligation["lifecycle"] != "OPEN":
        return rule["illegal_result"]
    if event_type == "reschedule_obligation":
        obligation["due_at"] = payload["due_at"]
    elif event_type == "delegate_obligation":
        obligation["owner_role"] = payload["owner_role"]
    elif event_type == "cancel_obligation":
        obligation["lifecycle"] = "CANCELLED"
        obligation["terminal_event_id"] = event["event_id"]
    else:
        prerequisites_complete = all(
            obligations.get(item, {}).get("lifecycle") == "COMPLETED"
            for item in obligation["prerequisite_obligation_ids"])
        legal = (obligation["critical"]
                 and obligation["due_at"] <= event["originating_cut"]["valid_time"]
                 and obligation["completion_action_id"] == payload["completion_action_id"]
                 and payload["originating_cut_hash"] == cut_hash(event["originating_cut"])
                 and prerequisites_complete)
        if not legal:
            return rule["illegal_result"]
        obligation["lifecycle"] = "COMPLETED"
        obligation["terminal_event_id"] = event["event_id"]
    return "APPLIED"


def _dependency_handler(state: dict[str, Any], event: dict[str, Any],
                        rule: dict[str, Any]) -> str:
    scope = _get_scope(state, event["scope_id"])
    payload = event["payload"]
    child = payload["obligation_id"]
    parent = payload["prerequisite_obligation_id"]
    edge = [child, parent]
    if event["event_type"] == "unlink_dependency":
        if edge not in scope["dependencies"]:
            return rule["illegal_result"]
        scope["dependencies"].remove(edge)
        scope["obligations"][child]["prerequisite_obligation_ids"].remove(parent)
        return "APPLIED"
    endpoints = [scope["obligations"].get(child), scope["obligations"].get(parent)]
    if (edge in scope["dependencies"] or child == parent
            or any(item is None or item["lifecycle"] != "OPEN" for item in endpoints)
            or _cycle_if_added(scope["dependencies"], child, parent)):
        return rule["illegal_result"]
    scope["dependencies"].append(edge)
    scope["dependencies"].sort()
    old = scope["obligations"][child]["prerequisite_obligation_ids"]
    scope["obligations"][child]["prerequisite_obligation_ids"] = sorted(set(old + [parent]))
    return "APPLIED"


def _open_handoff(state: dict[str, Any], event: dict[str, Any],
                  rule: dict[str, Any]) -> str:
    scope = _get_scope(state, event["scope_id"])
    payload = event["payload"]
    target = scope["obligations"].get(payload["target_obligation_id"])
    if (payload["handoff_id"] in scope["handoffs"] or target is None
            or target["lifecycle"] != "OPEN"):
        return rule["illegal_result"]
    scope["handoffs"][payload["handoff_id"]] = {
        "status": "OPEN", "terminal_disposition": None,
        "target_obligation_id": payload["target_obligation_id"],
        "task_packet_hash": payload["task_packet_hash"],
        "originating_cut": copy.deepcopy(event["originating_cut"]),
        "originating_cut_hash": payload["originating_cut_hash"],
        "action_catalog": copy.deepcopy(payload["action_catalog"]),
        "originating_obligations": copy.deepcopy(scope["obligations"]),
        "proposal_event_id": None, "action_ids": [],
    }
    return "APPLIED"


def _record_response(state: dict[str, Any], event: dict[str, Any],
                     rule: dict[str, Any]) -> str:
    payload = event["payload"]
    address = hashlib.sha256(canonical_json((payload["scenario_id"], payload["condition"],
                                             payload["node"]))).hexdigest().upper()
    record = {key: payload[key] for key in payload}
    previous = state["responses"].get(address)
    if previous is not None and previous != record:
        return rule["illegal_result"]
    if previous is None:
        state["responses"][address] = record
    return "APPLIED"


def _handoff_terminal_handler(state: dict[str, Any], event: dict[str, Any],
                              rule: dict[str, Any]) -> str:
    scope = _get_scope(state, event["scope_id"])
    payload = event["payload"]
    handoff = scope["handoffs"].get(payload["handoff_id"])
    event_type = event["event_type"]
    if event_type == "propose_handoff_result":
        if (handoff is None or handoff["status"] != "OPEN"
                or payload["originating_cut_hash"] != handoff["originating_cut_hash"]
                or not _targets_are_legal(handoff, payload["action_ids"])):
            return rule["illegal_result"]
        handoff["status"] = "PROPOSED"
        handoff["proposal_event_id"] = event["event_id"]
        handoff["action_ids"] = sorted(payload["action_ids"])
        return "APPLIED"
    if event_type == "commit_handoff_result":
        if (handoff is None or handoff["status"] != "PROPOSED"
                or payload["proposal_event_id"] != handoff["proposal_event_id"]
                or not _targets_are_legal(handoff, handoff["action_ids"])):
            return rule["illegal_result"]
        action_targets = {row["action_id"]: row["obligation_id"]
                          for row in handoff["action_catalog"]}
        replacement = copy.deepcopy(scope["obligations"])
        for action in handoff["action_ids"]:
            replacement[action_targets[action]]["lifecycle"] = "COMPLETED"
            replacement[action_targets[action]]["terminal_event_id"] = event["event_id"]
        scope["obligations"] = replacement
        handoff = scope["handoffs"][payload["handoff_id"]]
        handoff["status"] = "COMMITTED"
        handoff["terminal_disposition"] = "COMMITTED"
        return "APPLIED"
    if event_type == "reject_handoff_result":
        if handoff is None or handoff["status"] != "OPEN":
            return rule["illegal_result"]
        handoff["status"] = "REJECTED"
        handoff["terminal_disposition"] = payload["rejection_code"]
        return "APPLIED"
    if handoff is None or handoff["status"] not in {"COMMITTED", "REJECTED"}:
        return rule["illegal_result"]
    handoff["status"] = "CLOSED"
    return "APPLIED"


HANDLERS: dict[str, Callable[[dict[str, Any], dict[str, Any], dict[str, Any]], str]] = {
    "assert_fact": _fact_handler,
    "correct_fact": _fact_handler,
    "retract_fact": _fact_handler,
    "open_obligation": _obligation_handler,
    "reschedule_obligation": _obligation_handler,
    "delegate_obligation": _obligation_handler,
    "complete_obligation": _obligation_handler,
    "cancel_obligation": _obligation_handler,
    "reopen_obligation": _obligation_handler,
    "link_dependency": _dependency_handler,
    "unlink_dependency": _dependency_handler,
    "open_handoff": _open_handoff,
    "record_call_response": _record_response,
    "propose_handoff_result": _handoff_terminal_handler,
    "commit_handoff_result": _handoff_terminal_handler,
    "reject_handoff_result": _handoff_terminal_handler,
    "close_handoff": _handoff_terminal_handler,
}


def oracle_apply(state: dict[str, Any], event: dict[str, Any]) -> tuple[dict[str, Any], str]:
    """Apply one event using declarative handler dispatch independent of the reducer."""
    contract = load_contract("MBCX-01-STATE-ACTION-CONTRACT-v4.json")
    rules = contract["event_types"]
    error = _check_envelope(state, event, rules)
    if error is not None:
        return copy.deepcopy(state), error
    trial = copy.deepcopy(state)
    result = HANDLERS[event["event_type"]](trial, event, rules[event["event_type"]])
    if result != "APPLIED":
        return copy.deepcopy(state), result
    return _finish(trial, event), result
