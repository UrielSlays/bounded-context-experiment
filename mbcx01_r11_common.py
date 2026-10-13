"""Shared r11 structural ingress and canonical primitives. No provider calls."""

from __future__ import annotations

import copy
import hashlib
import json
import re
from datetime import datetime
from typing import Any


T0 = "2026-08-12T00:00:00.000000Z"
T1 = "2026-08-13T00:00:00.000000Z"

EVENT_OPERATIONS = {
    "assert_fact": "ASSERT_FACT",
    "correct_fact": "CORRECT_FACT",
    "retract_fact": "RETRACT_FACT",
    "open_obligation": "OPEN_OBLIGATION",
    "reschedule_obligation": "RESCHEDULE_OBLIGATION",
    "delegate_obligation": "DELEGATE_OBLIGATION",
    "complete_obligation": "COMPLETE_OBLIGATION",
    "cancel_obligation": "CANCEL_OBLIGATION",
    "reopen_obligation": "REOPEN_OBLIGATION",
    "link_dependency": "LINK_DEPENDENCY",
    "unlink_dependency": "UNLINK_DEPENDENCY",
    "open_handoff": "OPEN_HANDOFF",
    "record_call_response": "RECORD_CALL_RESPONSE",
    "propose_handoff_result": "PROPOSE_HANDOFF_RESULT",
    "commit_handoff_result": "COMMIT_HANDOFF_RESULT",
    "reject_handoff_result": "REJECT_HANDOFF_RESULT",
    "close_handoff": "CLOSE_HANDOFF",
}

PAYLOAD_REQUIRED = {
    "assert_fact": {"subject_id", "predicate_id", "value_code"},
    "correct_fact": {"subject_id", "predicate_id", "parent_event_id", "value_code"},
    "retract_fact": {"subject_id", "predicate_id", "target_event_id"},
    "open_obligation": {"obligation_id", "subject_id", "owner_role", "due_at", "critical",
                        "completion_action_id", "prerequisite_obligation_ids"},
    "reschedule_obligation": {"obligation_id", "due_at"},
    "delegate_obligation": {"obligation_id", "owner_role"},
    "complete_obligation": {"obligation_id", "completion_action_id", "originating_cut_hash"},
    "cancel_obligation": {"obligation_id", "cancellation_code"},
    "reopen_obligation": {"obligation_id", "due_at", "owner_role"},
    "link_dependency": {"obligation_id", "prerequisite_obligation_id"},
    "unlink_dependency": {"obligation_id", "prerequisite_obligation_id"},
    "open_handoff": {"handoff_id", "scenario_id", "condition", "target_obligation_id",
                     "task_packet_hash", "served_request_hash", "request_parameters_hash",
                     "idempotency_token",
                     "task_packet_utf8", "manifest_utf8",
                     "originating_cut_hash", "action_catalog_hash", "canonical_snapshot_hash",
                     "route_contract_hash", "manifest_hash", "action_catalog"},
    "record_call_response": {"handoff_id", "scenario_id", "condition", "node",
                             "task_packet_hash", "served_request_hash", "request_parameters_hash",
                             "idempotency_token",
                             "raw_response_utf8", "raw_response_hash", "worker_handoff_hash",
                             "response_ref", "provider_request_id", "durability_receipt",
                             "route_contract_hash", "accepted_at"},
    "propose_handoff_result": {"handoff_id", "worker_handoff_hash", "originating_cut_hash", "action_ids"},
    "commit_handoff_result": {"handoff_id", "proposal_event_id"},
    "reject_handoff_result": {"handoff_id", "rejection_code", "proposal_hash"},
    "close_handoff": {"handoff_id"},
}

SEMANTIC_ID = re.compile(r"^[A-Z0-9][A-Z0-9:._/-]{0,127}$")
ACTION_ID = re.compile(r"^ACT\.[0-9A-F]{64}$")
SHA256 = re.compile(r"^[0-9A-F]{64}$")
SHA384 = re.compile(r"^[0-9A-F]{96}$")
UTC = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}Z$")
CALL_IDENTITY_FIELDS = ("scenario_id", "condition", "node", "task_packet_hash",
                        "served_request_hash", "request_parameters_hash", "idempotency_token",
                        "route_contract_hash")


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def sha256(value: Any) -> str:
    data = value if isinstance(value, bytes) else canonical_json(value)
    return hashlib.sha256(data).hexdigest().upper()


def sha384(value: Any) -> str:
    data = value if isinstance(value, bytes) else canonical_json(value)
    return hashlib.sha384(data).hexdigest().upper()


def action_id(scope_id: str, obligation_id: str) -> str:
    return "ACT." + sha256([scope_id, obligation_id])


def fact_key(subject_id: str, predicate_id: str) -> str:
    return sha256([subject_id, predicate_id])


def cut_hash(cut: dict[str, Any]) -> str:
    return sha384(cut)


def current_cut(state: dict[str, Any], valid_time: str = T1) -> dict[str, Any]:
    knowledge_time = max(T1, state.get("last_observed_at", T1))
    return {"journal_seq": state["next_seq"] - 1,
            "knowledge_time": knowledge_time, "valid_time": valid_time}


def canonical_event_id(event: dict[str, Any]) -> str:
    return "EV." + sha256({key: value for key, value in event.items() if key != "event_id"})


def _valid_utc(value: Any) -> bool:
    if not isinstance(value, str) or UTC.fullmatch(value) is None:
        return False
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        return False
    return parsed.strftime("%Y-%m-%dT%H:%M:%S.%fZ") == value


def fresh_scope() -> dict[str, Any]:
    return {"facts": {}, "obligations": {}, "dependencies": [], "handoffs": {}}


def initial_state() -> dict[str, Any]:
    scope = fresh_scope()
    for oid in ("OBL.SHARED", "OBL.PREREQ"):
        scope["obligations"][oid] = {
            "subject_id": "SUB.SHARED", "owner_role": "WORKER", "due_at": T0,
            "critical": True, "lifecycle": "OPEN", "completion_action_id": action_id("SCOPE.SHARED", oid),
            "prerequisite_obligation_ids": [], "terminal_event_id": None,
        }
    return {"next_seq": 1, "last_observed_at": T0,
            "scopes": {"SCOPE.SHARED": scope}, "responses": [],
            "events": {}, "idempotency": {}}


def make_event(event_type: str, payload: dict[str, Any], *, state: dict[str, Any],
               scope_id: str = "SCOPE.SHARED", idempotency_key: str | None = None,
               observed_at: str = T1, valid_from: str = T0, valid_to: str | None = None,
               originating_cut: dict[str, Any] | None = None) -> dict[str, Any]:
    if event_type not in EVENT_OPERATIONS:
        raise ValueError("unknown event type")
    seq = state["next_seq"]
    event = {
        "event_id": "",
        "scope_id": scope_id,
        "event_type": event_type,
        "semantic_operation": EVENT_OPERATIONS[event_type],
        "idempotency_key": idempotency_key or f"IDEM.{event_type.upper()}.{seq}",
        "journal_seq": seq,
        "observed_at": observed_at,
        "valid_from": valid_from,
        "valid_to": valid_to,
        "originating_cut": copy.deepcopy(originating_cut or current_cut(state)),
        "payload": copy.deepcopy(payload),
    }
    event["event_id"] = canonical_event_id(event)
    return event


def structural_error(state: dict[str, Any], event: Any) -> str | None:
    if not isinstance(event, dict):
        return "SCHEMA_INVALID"
    required = {"event_id", "scope_id", "event_type", "semantic_operation", "idempotency_key",
                "journal_seq", "observed_at", "valid_from", "valid_to", "originating_cut", "payload"}
    if set(event) != required:
        return "SCHEMA_INVALID"
    event_type = event.get("event_type")
    if event_type not in EVENT_OPERATIONS or event.get("semantic_operation") != EVENT_OPERATIONS.get(event_type):
        return "SCHEMA_INVALID"
    try:
        expected_event_id = canonical_event_id(event)
    except (TypeError, ValueError, OverflowError):
        return "SCHEMA_INVALID"
    if event.get("event_id") != expected_event_id:
        return "EVENT_ID_INVALID"
    if any(SEMANTIC_ID.fullmatch(event.get(field, "")) is None for field in ("scope_id", "idempotency_key")):
        return "SCHEMA_INVALID"
    if not isinstance(event.get("journal_seq"), int) or isinstance(event.get("journal_seq"), bool):
        return "SCHEMA_INVALID"
    if event["journal_seq"] < 0:
        return "SCHEMA_INVALID"
    if not _valid_utc(event.get("observed_at")) or not _valid_utc(event.get("valid_from")):
        return "SCHEMA_INVALID"
    if event.get("valid_to") is not None and (not _valid_utc(event["valid_to"])
                                                or event["valid_to"] <= event["valid_from"]):
        return "SCHEMA_INVALID"
    cut = event.get("originating_cut")
    if not isinstance(cut, dict) or set(cut) != {"journal_seq", "knowledge_time", "valid_time"}:
        return "SCHEMA_INVALID"
    if (not isinstance(cut["journal_seq"], int) or isinstance(cut["journal_seq"], bool)
            or not _valid_utc(cut["knowledge_time"]) or not _valid_utc(cut["valid_time"])):
        return "SCHEMA_INVALID"
    payload = event.get("payload")
    if not isinstance(payload, dict) or set(payload) != PAYLOAD_REQUIRED[event_type]:
        return "SCHEMA_INVALID"
    if not valid_payload_shape(event_type, payload):
        return "SCHEMA_INVALID"
    if event["event_id"] in state.get("events", {}):
        return None
    exact_cut = current_cut(state, cut["valid_time"])
    if (event["journal_seq"] != state.get("next_seq")
            or cut != exact_cut
            or cut["knowledge_time"] > event["observed_at"]
            or event["observed_at"] < state.get("last_observed_at", T0)):
        return "ORIGINATING_CUT_INVALID"
    payload = event["payload"]
    if event_type == "open_handoff":
        if (payload["condition"] not in {"BC", "OM"}
                or any(SHA384.fullmatch(payload[name]) is None for name in (
                    "task_packet_hash", "request_parameters_hash", "originating_cut_hash",
                    "action_catalog_hash", "canonical_snapshot_hash", "route_contract_hash",
                    "manifest_hash"))
                or SHA256.fullmatch(payload["served_request_hash"]) is None
                or SEMANTIC_ID.fullmatch(payload["idempotency_token"]) is None
                or not isinstance(payload["task_packet_utf8"], str)
                or not payload["task_packet_utf8"]
                or not isinstance(payload["manifest_utf8"], str)
                or not payload["manifest_utf8"]
                or not isinstance(payload["action_catalog"], list) or not payload["action_catalog"]):
            return "SCHEMA_INVALID"
    if event_type == "record_call_response":
        receipt = payload["durability_receipt"]
        try:
            parsed_worker = json.loads(payload["raw_response_utf8"])
        except (TypeError, ValueError):
            parsed_worker = None
        worker_keys = {"schema_id", "scenario_id", "scope_id", "condition",
                       "task_packet_hash", "served_request_hash", "manifest_hash",
                       "status_code", "proposed_action_ids", "produced_at",
                       "worker_handoff_hash"}
        worker_hash = (sha384({key: value for key, value in parsed_worker.items()
                               if key != "worker_handoff_hash"})
                       if isinstance(parsed_worker, dict) else None)
        if (payload["condition"] not in {"BC", "OM"} or payload["node"] != "B"
                or any(SHA384.fullmatch(payload[name]) is None for name in (
                    "task_packet_hash", "request_parameters_hash", "raw_response_hash",
                    "worker_handoff_hash", "route_contract_hash"))
                or SHA256.fullmatch(payload["served_request_hash"]) is None
                or not isinstance(payload["raw_response_utf8"], str) or not payload["raw_response_utf8"]
                or sha384(payload["raw_response_utf8"].encode("utf-8")) != payload["raw_response_hash"]
                or not isinstance(parsed_worker, dict) or set(parsed_worker) != worker_keys
                or parsed_worker.get("schema_id") != "WorkerHandoffV5"
                or parsed_worker.get("worker_handoff_hash") != worker_hash
                or payload["worker_handoff_hash"] != worker_hash
                or parsed_worker.get("scenario_id") != payload["scenario_id"]
                or parsed_worker.get("condition") != payload["condition"]
                or parsed_worker.get("task_packet_hash") != payload["task_packet_hash"]
                or parsed_worker.get("served_request_hash") != payload["served_request_hash"]
                or parsed_worker.get("status_code") != "PROPOSE"
                or SEMANTIC_ID.fullmatch(parsed_worker.get("scope_id", "")) is None
                or SHA384.fullmatch(parsed_worker.get("manifest_hash", "")) is None
                or not _valid_utc(parsed_worker.get("produced_at"))
                or not isinstance(parsed_worker.get("proposed_action_ids"), list)
                or not parsed_worker["proposed_action_ids"]
                or len(parsed_worker["proposed_action_ids"]) != len(set(parsed_worker["proposed_action_ids"]))
                or any(ACTION_ID.fullmatch(value) is None
                       for value in parsed_worker["proposed_action_ids"])
                or SEMANTIC_ID.fullmatch(payload["response_ref"]) is None
                or SEMANTIC_ID.fullmatch(payload["provider_request_id"]) is None
                or SEMANTIC_ID.fullmatch(payload["idempotency_token"]) is None
                or not valid_durability_receipt(receipt, payload)):
            return "SCHEMA_INVALID"
    if event_type == "propose_handoff_result":
        if (SHA384.fullmatch(payload["worker_handoff_hash"]) is None
                or SHA384.fullmatch(payload["originating_cut_hash"]) is None
                or not isinstance(payload["action_ids"], list) or not payload["action_ids"]
                or any(ACTION_ID.fullmatch(value) is None for value in payload["action_ids"])):
            return "SCHEMA_INVALID"
    return None


def semantic_preimage(event: dict[str, Any]) -> str:
    return sha384({key: value for key, value in event.items()
                   if key not in {"event_id", "journal_seq", "observed_at"}})


def idempotency_slot(event: dict[str, Any]) -> str:
    return sha256([event["scope_id"], event["semantic_operation"], event["idempotency_key"]])


def preflight_replay(state: dict[str, Any], event: dict[str, Any]) -> str | None:
    prior_event = state.get("events", {}).get(event.get("event_id"))
    if prior_event is not None:
        return "DUPLICATE_NOOP" if prior_event == sha384(event) else "EVENT_ID_CONFLICT"
    prior_idem = state.get("idempotency", {}).get(idempotency_slot(event))
    if prior_idem is not None:
        return "DUPLICATE_NOOP" if prior_idem == semantic_preimage(event) else "IDEMPOTENCY_CONFLICT"
    return None


def finish_applied(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    state["events"][event["event_id"]] = sha384(event)
    state["idempotency"][idempotency_slot(event)] = semantic_preimage(event)
    state["next_seq"] = event["journal_seq"] + 1
    state["last_observed_at"] = event["observed_at"]
    return state


def effective_valid_to(row: dict[str, Any], cut: dict[str, Any]) -> str | None:
    bounds = [row["valid_to"]] if row.get("valid_to") is not None else []
    bounds.extend(change["valid_to"] for change in row.get("closure_events", [])
                  if change["journal_seq"] <= cut["journal_seq"]
                  and change["observed_at"] <= cut["knowledge_time"])
    return min(bounds, default=None)


def retracted_at(row: dict[str, Any], cut: dict[str, Any]) -> bool:
    if row.get("retracted") is True and not row.get("retraction_events"):
        return True
    return any(change["journal_seq"] <= cut["journal_seq"]
               and change["observed_at"] <= cut["knowledge_time"]
               for change in row.get("retraction_events", []))


def visible_effective(row: dict[str, Any], cut: dict[str, Any]) -> bool:
    end = effective_valid_to(row, cut)
    return (not retracted_at(row, cut) and row["journal_seq"] <= cut["journal_seq"]
            and row["observed_at"] <= cut["knowledge_time"]
            and row["valid_from"] <= cut["valid_time"]
            and (end is None or cut["valid_time"] < end))


def call_identity_hash(record: dict[str, Any]) -> str:
    return sha384({key: record[key] for key in CALL_IDENTITY_FIELDS})


def make_durability_receipt(record: dict[str, Any], transaction_id: str) -> dict[str, Any]:
    receipt = {"schema_id": "DurabilityReceiptV1",
               "ledger_identity_hash": call_identity_hash(record),
               "raw_response_hash": record["raw_response_hash"],
               "response_ref": record["response_ref"],
               "provider_request_id": record["provider_request_id"],
               "transaction_id": transaction_id,
               "fsync_completed": True, "commit_completed": True}
    receipt["receipt_hash"] = sha384(receipt)
    return receipt


def valid_durability_receipt(receipt: Any, record: dict[str, Any]) -> bool:
    required = {"schema_id", "ledger_identity_hash", "raw_response_hash", "response_ref",
                "provider_request_id", "transaction_id",
                "fsync_completed", "commit_completed", "receipt_hash"}
    return (isinstance(receipt, dict) and set(receipt) == required
            and receipt["schema_id"] == "DurabilityReceiptV1"
            and receipt["ledger_identity_hash"] == call_identity_hash(record)
            and receipt["raw_response_hash"] == record["raw_response_hash"]
            and receipt["response_ref"] == record["response_ref"]
            and receipt["provider_request_id"] == record["provider_request_id"]
            and SEMANTIC_ID.fullmatch(receipt["transaction_id"]) is not None
            and receipt["fsync_completed"] is True and receipt["commit_completed"] is True
            and receipt["receipt_hash"] == sha384({key: value for key, value in receipt.items()
                                                   if key != "receipt_hash"}))


def valid_payload_shape(event_type: str, payload: dict[str, Any]) -> bool:
    semantic = lambda value: isinstance(value, str) and SEMANTIC_ID.fullmatch(value) is not None
    event_id = lambda value: isinstance(value, str) and re.fullmatch(r"^EV\.[0-9A-F]{64}$", value) is not None
    action = lambda value: isinstance(value, str) and ACTION_ID.fullmatch(value) is not None
    semantic_lists = lambda value: (isinstance(value, list)
                                    and len(value) == len(set(value))
                                    and all(semantic(item) for item in value))
    if event_type == "assert_fact":
        return all(semantic(payload[name]) for name in ("subject_id", "predicate_id", "value_code"))
    if event_type == "correct_fact":
        return (all(semantic(payload[name]) for name in ("subject_id", "predicate_id", "value_code"))
                and event_id(payload["parent_event_id"]))
    if event_type == "retract_fact":
        return (all(semantic(payload[name]) for name in ("subject_id", "predicate_id"))
                and event_id(payload["target_event_id"]))
    if event_type == "open_obligation":
        return (all(semantic(payload[name]) for name in
                    ("obligation_id", "subject_id", "owner_role"))
                and _valid_utc(payload["due_at"]) and isinstance(payload["critical"], bool)
                and action(payload["completion_action_id"])
                and semantic_lists(payload["prerequisite_obligation_ids"]))
    if event_type == "reschedule_obligation":
        return semantic(payload["obligation_id"]) and _valid_utc(payload["due_at"])
    if event_type == "delegate_obligation":
        return semantic(payload["obligation_id"]) and semantic(payload["owner_role"])
    if event_type == "complete_obligation":
        return (semantic(payload["obligation_id"]) and action(payload["completion_action_id"])
                and isinstance(payload["originating_cut_hash"], str)
                and SHA384.fullmatch(payload["originating_cut_hash"]) is not None)
    if event_type == "cancel_obligation":
        return semantic(payload["obligation_id"]) and semantic(payload["cancellation_code"])
    if event_type == "reopen_obligation":
        return (semantic(payload["obligation_id"]) and _valid_utc(payload["due_at"])
                and semantic(payload["owner_role"]))
    if event_type in {"link_dependency", "unlink_dependency"}:
        return semantic(payload["obligation_id"]) and semantic(payload["prerequisite_obligation_id"])
    if event_type == "open_handoff":
        catalog = payload["action_catalog"]
        def valid_catalog_row(row: Any) -> bool:
            if not isinstance(row, dict):
                return False
            if set(row) == {"action_id", "obligation_id"}:
                return action(row["action_id"]) and semantic(row["obligation_id"])
            if set(row) == {"action_id", "action_kind", "scope_id", "obligation_id"}:
                return (row["action_kind"] == "ACT_ON_OBLIGATION"
                        and semantic(row["scope_id"]) and action(row["action_id"])
                        and semantic(row["obligation_id"]))
            return (set(row) == {"action_id", "action_kind"}
                    and row["action_id"] == "NO_ACTION"
                    and row["action_kind"] == "NO_ACTION")
        return (all(semantic(payload[name]) for name in
                    ("handoff_id", "scenario_id", "target_obligation_id"))
                and payload["condition"] in {"BC", "OM"}
                and all(isinstance(payload[name], str) and SHA384.fullmatch(payload[name]) is not None
                        for name in ("task_packet_hash", "request_parameters_hash",
                                     "originating_cut_hash", "action_catalog_hash",
                                     "canonical_snapshot_hash", "route_contract_hash",
                                     "manifest_hash"))
                and isinstance(payload["served_request_hash"], str)
                and SHA256.fullmatch(payload["served_request_hash"]) is not None
                and semantic(payload["idempotency_token"])
                and isinstance(payload["task_packet_utf8"], str)
                and bool(payload["task_packet_utf8"])
                and isinstance(payload["manifest_utf8"], str)
                and bool(payload["manifest_utf8"])
                and isinstance(catalog, list) and bool(catalog)
                and all(valid_catalog_row(row) for row in catalog))
    if event_type == "record_call_response":
        return (all(semantic(payload[name]) for name in
                    ("handoff_id", "scenario_id", "idempotency_token",
                     "response_ref", "provider_request_id"))
                and _valid_utc(payload["accepted_at"]))
    if event_type == "propose_handoff_result":
        return (semantic(payload["handoff_id"])
                and isinstance(payload["worker_handoff_hash"], str)
                and SHA384.fullmatch(payload["worker_handoff_hash"]) is not None
                and isinstance(payload["originating_cut_hash"], str)
                and SHA384.fullmatch(payload["originating_cut_hash"]) is not None
                and isinstance(payload["action_ids"], list) and bool(payload["action_ids"])
                and len(payload["action_ids"]) == len(set(payload["action_ids"]))
                and all(action(value) for value in payload["action_ids"]))
    if event_type == "commit_handoff_result":
        return semantic(payload["handoff_id"]) and event_id(payload["proposal_event_id"])
    if event_type == "reject_handoff_result":
        return (semantic(payload["handoff_id"]) and semantic(payload["rejection_code"])
                and isinstance(payload["proposal_hash"], str)
                and SHA384.fullmatch(payload["proposal_hash"]) is not None)
    if event_type == "close_handoff":
        return semantic(payload["handoff_id"])
    return False


def action_targets_legal(obligations: dict[str, Any], catalog: list[dict[str, str]],
                         action_ids: list[str], valid_time: str) -> bool:
    targets = {row.get("action_id"): row.get("obligation_id") for row in catalog
               if isinstance(row, dict) and row.get("obligation_id") is not None}
    if len(action_ids) != len(set(action_ids)) or any(action not in targets for action in action_ids):
        return False
    for action in action_ids:
        obligation = obligations.get(targets[action])
        if (not obligation or obligation["lifecycle"] != "OPEN" or not obligation["critical"]
                or obligation["due_at"] > valid_time or obligation["completion_action_id"] != action
                or any(obligations.get(p, {}).get("lifecycle") != "COMPLETED"
                       for p in obligation["prerequisite_obligation_ids"])):
            return False
    return True


def has_path(edges: list[list[str]], start: str, target: str) -> bool:
    frontier, seen = [start], set()
    while frontier:
        node = frontier.pop()
        if node == target:
            return True
        if node in seen:
            continue
        seen.add(node)
        frontier.extend(parent for child, parent in edges if child == node)
    return False
