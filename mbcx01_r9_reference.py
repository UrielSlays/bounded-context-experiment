"""Event-journal reference implementation for the MBCX-01 r9 preregistration."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import struct
import subprocess
from decimal import Decimal, localcontext
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
T0 = "2026-08-12T00:00:00.000000Z"
T1 = "2026-08-13T00:00:00.000000Z"
ENVELOPE_KEYS = {
    "event_id", "scope_id", "event_type", "semantic_operation", "idempotency_key",
    "journal_seq", "observed_at", "valid_from", "valid_to", "originating_cut", "payload",
}


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def load_contract(name: str) -> dict[str, Any]:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def action_id(scope_id: str, obligation_id: str) -> str:
    preimage = {"schema_id": "ActionIdentityV1", "scope_id": scope_id,
                "obligation_id": obligation_id}
    return "ACT." + hashlib.sha256(canonical_json(preimage)).hexdigest().upper()


def cut_hash(cut: dict[str, Any]) -> str:
    return hashlib.sha384(canonical_json(cut)).hexdigest().upper()


def _fresh_scope() -> dict[str, Any]:
    target_action = action_id("SCOPE.SHARED", "OBL.SHARED")
    prereq_action = action_id("SCOPE.SHARED", "OBL.PREREQ")
    return {
        "facts": {},
        "obligations": {
            "OBL.SHARED": {
                "subject_id": "SUB.SHARED", "owner_role": "WORKER", "due_at": T0,
                "critical": True, "lifecycle": "OPEN", "completion_action_id": target_action,
                "prerequisite_obligation_ids": [], "terminal_event_id": None,
            },
            "OBL.PREREQ": {
                "subject_id": "SUB.PREREQ", "owner_role": "WORKER", "due_at": T0,
                "critical": True, "lifecycle": "COMPLETED", "completion_action_id": prereq_action,
                "prerequisite_obligation_ids": [], "terminal_event_id": "EV.PREREQ.COMPLETE",
            },
        },
        "dependencies": [],
        "handoffs": {},
    }


def initial_state() -> dict[str, Any]:
    return {
        "next_seq": 1,
        "journal": [],
        "event_fingerprints": {},
        "idempotency": {},
        "scopes": {"SCOPE.SHARED": _fresh_scope()},
        "responses": {},
    }


def current_cut(state: dict[str, Any], valid_time: str = T1) -> dict[str, Any]:
    return {"journal_seq": state["next_seq"] - 1, "knowledge_time": T1,
            "valid_time": valid_time}


def make_event(event_type: str, payload: dict[str, Any], *,
               state: dict[str, Any] | None = None, scope_id: str = "SCOPE.SHARED",
               event_id: str | None = None, idempotency_key: str | None = None,
               originating_cut: dict[str, Any] | None = None,
               journal_seq: int | None = None) -> dict[str, Any]:
    contract = load_contract("MBCX-01-STATE-ACTION-CONTRACT-v4.json")
    if event_type not in contract["event_types"]:
        raise ValueError(f"unknown event type {event_type}")
    seq = journal_seq if journal_seq is not None else (state["next_seq"] if state else 1)
    cut = copy.deepcopy(originating_cut or (current_cut(state) if state else {
        "journal_seq": 0, "knowledge_time": T1, "valid_time": T1}))
    body = copy.deepcopy(payload)
    if "originating_cut_hash" in body:
        body["originating_cut_hash"] = cut_hash(cut)
    return {
        "event_id": event_id or f"EV.{event_type.upper()}.{seq}",
        "scope_id": scope_id,
        "event_type": event_type,
        "semantic_operation": contract["event_types"][event_type]["semantic_operation"],
        "idempotency_key": idempotency_key or f"IDEM.{event_type.upper()}.{seq}",
        "journal_seq": seq,
        "observed_at": T1,
        "valid_from": T1,
        "valid_to": None,
        "originating_cut": cut,
        "payload": body,
    }


def _semantic_preimage(event: dict[str, Any]) -> bytes:
    return canonical_json({
        "scope_id": event["scope_id"],
        "semantic_operation": event["semantic_operation"],
        "idempotency_key": event["idempotency_key"],
        "valid_from": event["valid_from"],
        "valid_to": event["valid_to"],
        "originating_cut": event["originating_cut"],
        "payload": event["payload"],
    })


def _idempotency_slot(event: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json([
        event["scope_id"], event["semantic_operation"], event["idempotency_key"]
    ])).hexdigest().upper()


def _scope(state: dict[str, Any], scope_id: str) -> dict[str, Any]:
    return state["scopes"].setdefault(scope_id, {
        "facts": {}, "obligations": {}, "dependencies": [], "handoffs": {}})


def _fact_key(payload: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json([
        payload["subject_id"], payload["predicate_id"]])).hexdigest().upper()


def _has_path(edges: list[list[str]], start: str, target: str) -> bool:
    frontier = [start]
    visited: set[str] = set()
    adjacency: dict[str, list[str]] = {}
    for child, parent in edges:
        adjacency.setdefault(child, []).append(parent)
    while frontier:
        node = frontier.pop()
        if node == target:
            return True
        if node in visited:
            continue
        visited.add(node)
        frontier.extend(adjacency.get(node, []))
    return False


def _valid_payload(rule: dict[str, Any], payload: Any) -> bool:
    return isinstance(payload, dict) and set(payload) == set(rule["payload_schema"]["required"])


def _validate_envelope(state: dict[str, Any], event: Any,
                       contract: dict[str, Any]) -> str | None:
    if not isinstance(event, dict) or set(event) != ENVELOPE_KEYS:
        return "SCHEMA_INVALID"
    event_type = event.get("event_type")
    rule = contract["event_types"].get(event_type)
    if rule is None or event.get("semantic_operation") != rule["semantic_operation"]:
        return "SCHEMA_INVALID"
    if not _valid_payload(rule, event.get("payload")):
        return "SCHEMA_INVALID"
    fingerprint = hashlib.sha384(canonical_json(event)).hexdigest().upper()
    old_event = state["event_fingerprints"].get(event["event_id"])
    if old_event is not None:
        return "DUPLICATE_NOOP" if old_event == fingerprint else "EVENT_ID_CONFLICT"
    slot = _idempotency_slot(event)
    semantic_hash = hashlib.sha384(_semantic_preimage(event)).hexdigest().upper()
    old_semantic = state["idempotency"].get(slot)
    if old_semantic is not None:
        return "DUPLICATE_NOOP" if old_semantic == semantic_hash else "IDEMPOTENCY_CONFLICT"
    if event["journal_seq"] != state["next_seq"]:
        return "JOURNAL_SEQUENCE_INVALID"
    cut = event["originating_cut"]
    if (not isinstance(cut, dict) or set(cut) != {"journal_seq", "knowledge_time", "valid_time"}
            or cut["journal_seq"] != state["next_seq"] - 1
            or cut["knowledge_time"] > event["observed_at"]):
        return "ORIGINATING_CUT_INVALID"
    if event["valid_to"] is not None and event["valid_to"] <= event["valid_from"]:
        return "VALID_INTERVAL_INVALID"
    return None


def _record_applied(state: dict[str, Any], event: dict[str, Any]) -> None:
    fingerprint = hashlib.sha384(canonical_json(event)).hexdigest().upper()
    semantic_hash = hashlib.sha384(_semantic_preimage(event)).hexdigest().upper()
    state["journal"].append(event["event_id"])
    state["event_fingerprints"][event["event_id"]] = fingerprint
    state["idempotency"][_idempotency_slot(event)] = semantic_hash
    state["next_seq"] += 1


def _action_targets_legal(snapshot: dict[str, Any], catalog: list[dict[str, str]],
                          action_ids: list[str], valid_time: str) -> bool:
    by_id = {entry["action_id"]: entry["obligation_id"] for entry in catalog}
    if len(by_id) != len(catalog) or any(action not in by_id for action in action_ids):
        return False
    for action in action_ids:
        obligation = snapshot.get(by_id[action])
        if not obligation or obligation["lifecycle"] != "OPEN" or not obligation["critical"]:
            return False
        if obligation["due_at"] > valid_time or obligation["completion_action_id"] != action:
            return False
        if any(snapshot.get(prereq, {}).get("lifecycle") != "COMPLETED"
               for prereq in obligation["prerequisite_obligation_ids"]):
            return False
    return True


def reference_apply(state: dict[str, Any], event: dict[str, Any],
                    mutant: str | None = None) -> tuple[dict[str, Any], str]:
    """Apply one envelope by validating it, projecting its effect, then journaling it."""
    contract = load_contract("MBCX-01-STATE-ACTION-CONTRACT-v4.json")
    error = _validate_envelope(state, event, contract)
    if error is not None:
        if mutant == "PAYLOAD_HASH_IDEMPOTENCY" and error == "IDEMPOTENCY_CONFLICT":
            pass
        elif mutant == "SKIP_ORIGINATING_CUT" and error == "ORIGINATING_CUT_INVALID":
            pass
        else:
            return copy.deepcopy(state), error
    new = copy.deepcopy(state)
    event_type = event["event_type"]
    payload = event["payload"]
    rule = contract["event_types"][event_type]
    scope = _scope(new, event["scope_id"])
    obligations = scope["obligations"]
    result = "APPLIED"

    if event_type in {"assert_fact", "correct_fact", "retract_fact"}:
        key = _fact_key(payload)
        versions = scope["facts"].setdefault(key, [])
        if event_type == "assert_fact":
            active = [row for row in versions if not row["retracted"] and row["valid_to"] is None]
            if active:
                result = rule["illegal_result"]
            else:
                versions.append({"event_id": event["event_id"], "parent_event_id": None,
                                 "value_code": payload["value_code"], "observed_at": event["observed_at"],
                                 "valid_from": event["valid_from"], "valid_to": event["valid_to"],
                                 "journal_seq": event["journal_seq"], "retracted": False})
        elif event_type == "correct_fact":
            parent = next((row for row in versions if row["event_id"] == payload["parent_event_id"]), None)
            children = [row for row in versions if row["parent_event_id"] == payload["parent_event_id"]]
            if not parent or parent["retracted"] or parent["valid_to"] is not None or children:
                result = rule["illegal_result"]
            else:
                parent["valid_to"] = event["valid_from"]
                versions.append({"event_id": event["event_id"],
                                 "parent_event_id": payload["parent_event_id"],
                                 "value_code": payload["value_code"], "observed_at": event["observed_at"],
                                 "valid_from": event["valid_from"], "valid_to": event["valid_to"],
                                 "journal_seq": event["journal_seq"], "retracted": False})
        else:
            target = next((row for row in versions if row["event_id"] == payload["target_event_id"]), None)
            if not target or target["retracted"] or target["journal_seq"] > event["originating_cut"]["journal_seq"]:
                result = rule["illegal_result"]
            else:
                target["retracted"] = True

    elif event_type == "open_obligation":
        oid = payload["obligation_id"]
        prereqs = payload["prerequisite_obligation_ids"]
        if oid in obligations or any(prereq not in obligations for prereq in prereqs):
            result = rule["illegal_result"]
        else:
            obligations[oid] = {"subject_id": payload["subject_id"],
                                "owner_role": payload["owner_role"], "due_at": payload["due_at"],
                                "critical": payload["critical"], "lifecycle": "OPEN",
                                "completion_action_id": payload["completion_action_id"],
                                "prerequisite_obligation_ids": list(prereqs), "terminal_event_id": None}
            for prereq in prereqs:
                scope["dependencies"].append([oid, prereq])
            scope["dependencies"].sort()

    elif event_type in {"reschedule_obligation", "delegate_obligation", "cancel_obligation",
                        "complete_obligation", "reopen_obligation"}:
        obligation = obligations.get(payload["obligation_id"])
        if event_type == "reopen_obligation":
            if not obligation or obligation["lifecycle"] not in {"COMPLETED", "CANCELLED"}:
                result = rule["illegal_result"]
            else:
                obligation.update({"lifecycle": "OPEN", "due_at": payload["due_at"],
                                   "owner_role": payload["owner_role"], "terminal_event_id": None})
        elif not obligation or obligation["lifecycle"] != "OPEN":
            result = rule["illegal_result"]
        elif event_type == "reschedule_obligation":
            if mutant != "DROP_RESCHEDULE_EFFECT":
                obligation["due_at"] = payload["due_at"]
        elif event_type == "delegate_obligation":
            if mutant != "DROP_DELEGATE_EFFECT":
                obligation["owner_role"] = payload["owner_role"]
        elif event_type == "cancel_obligation":
            obligation["lifecycle"] = "CANCELLED"
            obligation["terminal_event_id"] = event["event_id"]
        else:
            legal = (obligation["critical"] and obligation["due_at"] <= event["originating_cut"]["valid_time"]
                     and obligation["completion_action_id"] == payload["completion_action_id"]
                     and payload["originating_cut_hash"] == cut_hash(event["originating_cut"])
                     and all(obligations.get(prereq, {}).get("lifecycle") == "COMPLETED"
                             for prereq in obligation["prerequisite_obligation_ids"]))
            if not legal:
                result = rule["illegal_result"]
            else:
                obligation["lifecycle"] = "COMPLETED"
                obligation["terminal_event_id"] = event["event_id"]

    elif event_type in {"link_dependency", "unlink_dependency"}:
        edge = [payload["obligation_id"], payload["prerequisite_obligation_id"]]
        if event_type == "link_dependency":
            endpoints = [obligations.get(value) for value in edge]
            cycle = _has_path(scope["dependencies"], edge[1], edge[0])
            if mutant == "TWO_CYCLE_ONLY":
                cycle = [edge[1], edge[0]] in scope["dependencies"]
            if (edge in scope["dependencies"] or edge[0] == edge[1] or
                    any(not row or row["lifecycle"] != "OPEN" for row in endpoints) or cycle):
                result = rule["illegal_result"]
            else:
                scope["dependencies"].append(edge)
                scope["dependencies"].sort()
                obligations[edge[0]]["prerequisite_obligation_ids"] = sorted(set(
                    obligations[edge[0]]["prerequisite_obligation_ids"] + [edge[1]]))
        elif edge not in scope["dependencies"]:
            result = rule["illegal_result"]
        else:
            scope["dependencies"].remove(edge)
            obligations[edge[0]]["prerequisite_obligation_ids"].remove(edge[1])

    elif event_type == "open_handoff":
        hid = payload["handoff_id"]
        target = obligations.get(payload["target_obligation_id"])
        if hid in scope["handoffs"] or not target or target["lifecycle"] != "OPEN":
            result = rule["illegal_result"]
        else:
            scope["handoffs"][hid] = {
                "status": "OPEN", "terminal_disposition": None,
                "target_obligation_id": payload["target_obligation_id"],
                "task_packet_hash": payload["task_packet_hash"],
                "originating_cut": copy.deepcopy(event["originating_cut"]),
                "originating_cut_hash": payload["originating_cut_hash"],
                "action_catalog": copy.deepcopy(payload["action_catalog"]),
                "originating_obligations": copy.deepcopy(obligations),
                "proposal_event_id": None, "action_ids": [],
            }

    elif event_type == "record_call_response":
        key = hashlib.sha256(canonical_json([
            payload["scenario_id"], payload["condition"], payload["node"]])).hexdigest().upper()
        prior = new["responses"].get(key)
        response = {field: payload[field] for field in payload}
        if prior is not None and prior != response:
            result = rule["illegal_result"]
        elif prior is None:
            new["responses"][key] = response

    elif event_type in {"propose_handoff_result", "commit_handoff_result",
                        "reject_handoff_result", "close_handoff"}:
        handoff = scope["handoffs"].get(payload["handoff_id"])
        if event_type == "propose_handoff_result":
            legal = (handoff and handoff["status"] == "OPEN"
                     and payload["originating_cut_hash"] == handoff["originating_cut_hash"]
                     and _action_targets_legal(handoff["originating_obligations"],
                                               handoff["action_catalog"], payload["action_ids"],
                                               handoff["originating_cut"]["valid_time"]))
            if not legal:
                result = rule["illegal_result"]
            else:
                handoff["status"] = "PROPOSED"
                handoff["proposal_event_id"] = event["event_id"]
                handoff["action_ids"] = sorted(payload["action_ids"])
        elif event_type == "commit_handoff_result":
            legal = (handoff and handoff["status"] == "PROPOSED"
                     and payload["proposal_event_id"] == handoff["proposal_event_id"]
                     and _action_targets_legal(handoff["originating_obligations"],
                                               handoff["action_catalog"], handoff["action_ids"],
                                               handoff["originating_cut"]["valid_time"]))
            if not legal:
                result = rule["illegal_result"]
            else:
                targets = {row["action_id"]: row["obligation_id"] for row in handoff["action_catalog"]}
                trial = copy.deepcopy(obligations)
                for action in handoff["action_ids"]:
                    trial[targets[action]]["lifecycle"] = "COMPLETED"
                    trial[targets[action]]["terminal_event_id"] = event["event_id"]
                scope["obligations"] = trial
                obligations = trial
                handoff = scope["handoffs"][payload["handoff_id"]]
                handoff["status"] = "COMMITTED"
                handoff["terminal_disposition"] = "COMMITTED"
        elif event_type == "reject_handoff_result":
            if not handoff or handoff["status"] != "OPEN":
                result = rule["illegal_result"]
            else:
                handoff["status"] = "REJECTED"
                handoff["terminal_disposition"] = payload["rejection_code"]
        else:
            if not handoff or handoff["status"] not in {"COMMITTED", "REJECTED"}:
                result = rule["illegal_result"]
            else:
                handoff["status"] = "CLOSED"

    if result != "APPLIED":
        return copy.deepcopy(state), result
    if mutant == "SEEN_ONLY_EFFECT":
        new = copy.deepcopy(state)
    _record_applied(new, event)
    return new, result


def fixture_payload(event_type: str, state: dict[str, Any]) -> dict[str, Any]:
    aid = action_id("SCOPE.SHARED", "OBL.SHARED")
    common: dict[str, Any] = {
        "subject_id": "SUB.SHARED", "predicate_id": "PRED.SHARED",
        "value_code": "VALUE.NEW", "parent_event_id": "EV.FACT.ROOT",
        "target_event_id": "EV.FACT.ROOT", "obligation_id": "OBL.SHARED",
        "owner_role": "WRITER", "due_at": T1, "critical": True,
        "completion_action_id": aid, "prerequisite_obligation_ids": [],
        "cancellation_code": "OWNER_CANCELLED", "prerequisite_obligation_id": "OBL.PREREQ",
        "handoff_id": "HANDOFF.SHARED", "target_obligation_id": "OBL.SHARED",
        "task_packet_hash": "A" * 96, "originating_cut_hash": "CUT",
        "action_catalog": [{"action_id": aid, "obligation_id": "OBL.SHARED"}],
        "scenario_id": "SCENARIO.SHARED", "condition": "BC", "node": "A0",
        "request_hash": "B" * 96, "response_hash": "C" * 96,
        "response_ref": "RESPONSE.SHARED", "provider_request_id": "PROVIDER.SHARED",
        "route_fingerprint": "D" * 96, "accepted_at": T1,
        "worker_handoff_hash": "E" * 96, "action_ids": [aid],
        "proposal_event_id": "EV.PROPOSAL", "rejection_code": "SCHEMA_INVALID",
        "proposal_hash": "F" * 96,
    }
    contract = load_contract("MBCX-01-STATE-ACTION-CONTRACT-v4.json")
    return {name: copy.deepcopy(common[name])
            for name in contract["event_types"][event_type]["payload_schema"]["required"]}


def legal_fixture(event_type: str) -> tuple[dict[str, Any], dict[str, Any]]:
    state = initial_state()
    scope = state["scopes"]["SCOPE.SHARED"]
    payload = fixture_payload(event_type, state)
    if event_type == "assert_fact":
        pass
    elif event_type in {"correct_fact", "retract_fact"}:
        key = _fact_key(payload)
        scope["facts"][key] = [{"event_id": "EV.FACT.ROOT", "parent_event_id": None,
                                "value_code": "VALUE.OLD", "observed_at": T0,
                                "valid_from": T0, "valid_to": None, "journal_seq": 0,
                                "retracted": False}]
    elif event_type == "open_obligation":
        payload["obligation_id"] = "OBL.NEW"
        payload["completion_action_id"] = action_id("SCOPE.SHARED", "OBL.NEW")
    elif event_type == "reopen_obligation":
        scope["obligations"]["OBL.SHARED"]["lifecycle"] = "COMPLETED"
    elif event_type == "link_dependency":
        scope["obligations"]["OBL.PREREQ"]["lifecycle"] = "OPEN"
    elif event_type == "unlink_dependency":
        scope["dependencies"] = [["OBL.SHARED", "OBL.PREREQ"]]
        scope["obligations"]["OBL.SHARED"]["prerequisite_obligation_ids"] = ["OBL.PREREQ"]
    elif event_type in {"propose_handoff_result", "commit_handoff_result",
                        "reject_handoff_result", "close_handoff"}:
        cut = current_cut(state)
        hid = "HANDOFF.SHARED"
        scope["handoffs"][hid] = {
            "status": "OPEN", "terminal_disposition": None,
            "target_obligation_id": "OBL.SHARED", "task_packet_hash": "A" * 96,
            "originating_cut": cut, "originating_cut_hash": cut_hash(cut),
            "action_catalog": copy.deepcopy(fixture_payload("open_handoff", state)["action_catalog"]),
            "originating_obligations": copy.deepcopy(scope["obligations"]),
            "proposal_event_id": None, "action_ids": [],
        }
        if event_type == "commit_handoff_result":
            scope["handoffs"][hid]["status"] = "PROPOSED"
            scope["handoffs"][hid]["proposal_event_id"] = "EV.PROPOSAL"
            scope["handoffs"][hid]["action_ids"] = [action_id("SCOPE.SHARED", "OBL.SHARED")]
        elif event_type == "close_handoff":
            scope["handoffs"][hid]["status"] = "COMMITTED"
            scope["handoffs"][hid]["terminal_disposition"] = "COMMITTED"
    return state, payload


def enumerate_ordered_pairs() -> list[dict[str, Any]]:
    from mbcx01_r9_oracle import oracle_apply

    event_types = list(load_contract("MBCX-01-STATE-ACTION-CONTRACT-v4.json")["event_types"])
    rows = []
    for first in event_types:
        for second in event_types:
            prestate, first_payload = legal_fixture(first)
            first_event = make_event(first, first_payload, state=prestate)
            reference_mid, reference_first = reference_apply(copy.deepcopy(prestate), copy.deepcopy(first_event))
            oracle_mid, oracle_first = oracle_apply(copy.deepcopy(prestate), copy.deepcopy(first_event))
            second_payload = fixture_payload(second, reference_mid)
            second_event = make_event(second, second_payload, state=reference_mid)
            reference_final, reference_second = reference_apply(reference_mid, copy.deepcopy(second_event))
            oracle_final, oracle_second = oracle_apply(oracle_mid, copy.deepcopy(second_event))
            rows.append({
                "first": first, "second": second,
                "oracle_result": [oracle_first, oracle_second],
                "reference_result": [reference_first, reference_second],
                "oracle_state": oracle_final, "reference_state": reference_final,
            })
    return rows


def run_mutation_suite() -> dict[str, bool]:
    results: dict[str, bool] = {}
    for mutant, event_type, payload in (
        ("DROP_RESCHEDULE_EFFECT", "reschedule_obligation",
         {"obligation_id": "OBL.SHARED", "due_at": "2026-08-14T00:00:00.000000Z"}),
        ("DROP_DELEGATE_EFFECT", "delegate_obligation",
         {"obligation_id": "OBL.SHARED", "owner_role": "WRITER"}),
        ("SEEN_ONLY_EFFECT", "reschedule_obligation",
         {"obligation_id": "OBL.SHARED", "due_at": "2026-08-14T00:00:00.000000Z"}),
    ):
        state = initial_state()
        event = make_event(event_type, payload, state=state)
        good, good_result = reference_apply(copy.deepcopy(state), copy.deepcopy(event))
        bad, bad_result = reference_apply(copy.deepcopy(state), copy.deepcopy(event), mutant=mutant)
        results[mutant] = (good_result == bad_result == "APPLIED" and good != bad)

    state = initial_state()
    for oid in ("OBL.A", "OBL.B", "OBL.C"):
        state["scopes"]["SCOPE.SHARED"]["obligations"][oid] = {
            "subject_id": "SUB.CYCLE", "owner_role": "WORKER", "due_at": T0,
            "critical": True, "lifecycle": "OPEN",
            "completion_action_id": action_id("SCOPE.SHARED", oid),
            "prerequisite_obligation_ids": [], "terminal_event_id": None}
    state["scopes"]["SCOPE.SHARED"]["dependencies"] = [["OBL.A", "OBL.B"], ["OBL.B", "OBL.C"]]
    event = make_event("link_dependency", {"obligation_id": "OBL.C",
        "prerequisite_obligation_id": "OBL.A"}, state=state)
    good, good_result = reference_apply(copy.deepcopy(state), copy.deepcopy(event))
    bad, bad_result = reference_apply(copy.deepcopy(state), copy.deepcopy(event), mutant="TWO_CYCLE_ONLY")
    results["TWO_CYCLE_ONLY"] = good_result == "DEPENDENCY_ILLEGAL" and bad_result == "APPLIED" and good != bad

    state = initial_state()
    event = make_event("complete_obligation", {"obligation_id": "OBL.SHARED",
        "completion_action_id": action_id("SCOPE.SHARED", "OBL.SHARED"),
        "originating_cut_hash": "CUT"}, state=state)
    event["originating_cut"]["journal_seq"] = 99
    event["payload"]["originating_cut_hash"] = cut_hash(event["originating_cut"])
    good, good_result = reference_apply(copy.deepcopy(state), copy.deepcopy(event))
    bad, bad_result = reference_apply(copy.deepcopy(state), copy.deepcopy(event), mutant="SKIP_ORIGINATING_CUT")
    results["SKIP_ORIGINATING_CUT"] = good_result == "ORIGINATING_CUT_INVALID" and bad_result == "APPLIED" and good != bad

    state = initial_state()
    first = make_event("reschedule_obligation", {"obligation_id": "OBL.SHARED", "due_at": T1}, state=state,
                       idempotency_key="IDEM.SHARED")
    applied, _ = reference_apply(state, first)
    second = make_event("reschedule_obligation", {"obligation_id": "OBL.SHARED",
        "due_at": "2026-08-14T00:00:00.000000Z"}, state=applied, idempotency_key="IDEM.SHARED")
    good, good_result = reference_apply(copy.deepcopy(applied), copy.deepcopy(second))
    bad, bad_result = reference_apply(copy.deepcopy(applied), copy.deepcopy(second), mutant="PAYLOAD_HASH_IDEMPOTENCY")
    results["PAYLOAD_HASH_IDEMPOTENCY"] = good_result == "IDEMPOTENCY_CONFLICT" and bad_result == "APPLIED" and good != bad
    return results


def packet_hash(packet: dict[str, Any]) -> str:
    preimage = {key: value for key, value in packet.items() if key != "packet_hash"}
    return hashlib.sha384(canonical_json(preimage)).hexdigest().upper()


def packet_fixture_world() -> tuple[dict[str, dict[str, Any]], dict[str, Any],
                                    list[dict[str, str]], list[str]]:
    """Return a literal cut world used by independent packet witnesses."""
    cut = {"journal_seq": 17, "knowledge_time": T1, "valid_time": T1}
    target = action_id("SCOPE.SHARED", "OBL.SHARED")
    decoy = action_id("SCOPE.SHARED", "OBL.DECOY")
    world = {
        "OBL.SHARED": {
            "object_id": "OBL.SHARED", "object_kind": "OBLIGATION",
            "fields": {"scope_id": "SCOPE.SHARED", "subject_id": "SUB.SHARED",
                       "owner_role": "WORKER", "due_at": T0, "critical": True,
                       "lifecycle": "OPEN", "completion_action_id": target,
                       "prerequisite_obligation_ids": ["OBL.PREREQ"]},
            "source_event_ids": ["EV.OBL.SHARED"],
        },
        "OBL.PREREQ": {
            "object_id": "OBL.PREREQ", "object_kind": "OBLIGATION",
            "fields": {"scope_id": "SCOPE.SHARED", "subject_id": "SUB.PREREQ",
                       "owner_role": "WORKER", "due_at": T0, "critical": True,
                       "lifecycle": "COMPLETED",
                       "completion_action_id": action_id("SCOPE.SHARED", "OBL.PREREQ"),
                       "prerequisite_obligation_ids": []},
            "source_event_ids": ["EV.OBL.PREREQ"],
        },
        "OBL.DECOY": {
            "object_id": "OBL.DECOY", "object_kind": "OBLIGATION",
            "fields": {"scope_id": "SCOPE.SHARED", "subject_id": "SUB.DECOY",
                       "owner_role": "WORKER", "due_at": T1, "critical": False,
                       "lifecycle": "OPEN", "completion_action_id": decoy,
                       "prerequisite_obligation_ids": []},
            "source_event_ids": ["EV.OBL.DECOY"],
        },
        "DEP.SHARED.PREREQ": {
            "object_id": "DEP.SHARED.PREREQ", "object_kind": "DEPENDENCY",
            "fields": {"scope_id": "SCOPE.SHARED", "obligation_id": "OBL.SHARED",
                       "prerequisite_obligation_id": "OBL.PREREQ", "satisfied": True},
            "source_event_ids": ["EV.DEP.SHARED.PREREQ"],
        },
        "OBS.SHARED": {
            "object_id": "OBS.SHARED", "object_kind": "OBSERVATION",
            "fields": {"scope_id": "SCOPE.SHARED", "observed_at": T1,
                       "code": "TARGET_VISIBLE"},
            "source_event_ids": ["EV.OBS.SHARED"],
        },
    }
    actions = [
        {"action_id": target, "action_kind": "ACT_ON_OBLIGATION",
         "scope_id": "SCOPE.SHARED", "obligation_id": "OBL.SHARED"},
        {"action_id": decoy, "action_kind": "ACT_ON_OBLIGATION",
         "scope_id": "SCOPE.SHARED", "obligation_id": "OBL.DECOY"},
        {"action_id": "NO_ACTION", "action_kind": "NO_ACTION"},
    ]
    gold_read_set = ["OBL.SHARED", "OBL.PREREQ", "DEP.SHARED.PREREQ", "OBS.SHARED"]
    return world, cut, actions, gold_read_set


def _packet_closure(world: dict[str, dict[str, Any]], selected_object_ids: list[str],
                    actions: list[dict[str, str]]) -> list[str]:
    selected = set(selected_object_ids)
    selected.update(entry["obligation_id"] for entry in actions
                    if entry["action_kind"] == "ACT_ON_OBLIGATION")
    changed = True
    while changed:
        changed = False
        for object_id in list(selected):
            row = world.get(object_id)
            if row and row["object_kind"] == "OBLIGATION":
                for prerequisite in row["fields"]["prerequisite_obligation_ids"]:
                    if prerequisite not in selected:
                        selected.add(prerequisite)
                        changed = True
    return sorted(selected, key=lambda value: value.encode("utf-8"))


def _build_decision_packet(cut: dict[str, Any], world: dict[str, dict[str, Any]],
                           selected_object_ids: list[str], actions: list[dict[str, str]]) -> dict[str, Any]:
    object_ids = _packet_closure(world, selected_object_ids, actions)
    if any(object_id not in world for object_id in object_ids):
        raise ValueError("selected object is absent from canonical cut")
    catalog = sorted(copy.deepcopy(actions), key=lambda row: row["action_id"].encode("utf-8"))
    packet: dict[str, Any] = {
        "schema_id": "DecisionPacketV3",
        "scenario_id": "SCENARIO.SHARED",
        "cut": copy.deepcopy(cut),
        "objects": [copy.deepcopy(world[object_id]) for object_id in object_ids],
        "action_catalog": catalog,
        "available_action_ids": sorted([row["action_id"] for row in catalog],
                                       key=lambda value: value.encode("utf-8")),
        "observation": {"scope_id": "SCOPE.SHARED", "observed_at": T1,
                        "code": "TARGET_VISIBLE"},
    }
    packet["packet_hash"] = packet_hash(packet)
    return packet


def build_bc_packet(cut: dict[str, Any], world: dict[str, dict[str, Any]],
                    candidate_selected_object_ids: list[str],
                    actions: list[dict[str, str]]) -> dict[str, Any]:
    """Build BC only from the candidate's frozen public object-ID selection."""
    return _build_decision_packet(cut, world, candidate_selected_object_ids, actions)


def build_om_packet(cut: dict[str, Any], world: dict[str, dict[str, Any]],
                    independent_gold_read_set: list[str],
                    actions: list[dict[str, str]]) -> dict[str, Any]:
    """Build OM from the independent gold enumerator's frozen causal read-set."""
    return _build_decision_packet(cut, world, independent_gold_read_set, actions)


def validate_packet_schema(packet: dict[str, Any]) -> list[str]:
    """Execute the pinned Ajv Draft 2020-12 validator over one packet."""
    script = ROOT / "verify-r9-schema-ajv.mjs"
    environment = os.environ.copy()
    completed = subprocess.run(
        ["node", str(script), packet.get("schema_id", "")],
        input=canonical_json(packet), capture_output=True, cwd=ROOT, env=environment,
        timeout=20, check=False)
    if completed.returncode not in (0, 1):
        raise RuntimeError(completed.stderr.decode("utf-8", errors="replace"))
    response = json.loads(completed.stdout.decode("utf-8"))
    return [str(item) for item in response["errors"]]


def validate_packet_semantics(packet: dict[str, Any],
                              canonical_world: dict[str, dict[str, Any]]) -> list[str]:
    """Validate cross-record meaning and the pre-dispatch byte envelope."""
    errors: list[str] = []
    schema_errors = validate_packet_schema(packet)
    if schema_errors:
        errors.append("SCHEMA_INVALID")
    objects = packet.get("objects") if isinstance(packet.get("objects"), list) else []
    object_ids = [row.get("object_id") for row in objects if isinstance(row, dict)]
    if len(object_ids) != len(set(object_ids)):
        errors.append("DUPLICATE_OBJECT_ID")
    packet_objects = {row.get("object_id"): row for row in objects if isinstance(row, dict)}

    catalog = packet.get("action_catalog") if isinstance(packet.get("action_catalog"), list) else []
    action_ids = [row.get("action_id") for row in catalog if isinstance(row, dict)]
    if len(action_ids) != len(set(action_ids)):
        errors.append("DUPLICATE_ACTION_ID")
    for entry in catalog:
        if not isinstance(entry, dict):
            continue
        if entry.get("action_id") == "NO_ACTION":
            if set(entry) != {"action_id", "action_kind"} or entry.get("action_kind") != "NO_ACTION":
                errors.append("NO_ACTION_KIND_MISMATCH")
            continue
        required = {"action_id", "action_kind", "scope_id", "obligation_id"}
        if (set(entry) != required or entry.get("action_kind") != "ACT_ON_OBLIGATION"
                or entry.get("action_id") != action_id(str(entry.get("scope_id")),
                                                        str(entry.get("obligation_id")))):
            errors.append("ACTION_HASH_MISMATCH")
        target = packet_objects.get(entry.get("obligation_id"))
        if target is None or target.get("object_kind") != "OBLIGATION":
            errors.append("ACTION_TARGET_UNRESOLVED")
        elif target.get("fields", {}).get("scope_id") != entry.get("scope_id"):
            errors.append("SCOPE_MISMATCH")

    available = packet.get("available_action_ids") if isinstance(
        packet.get("available_action_ids"), list) else []
    if any(value not in action_ids for value in available):
        errors.append("AVAILABLE_ACTION_UNRESOLVED")
    if any(value not in available for value in action_ids):
        errors.append("CATALOG_ACTION_UNAVAILABLE")
    for row in objects:
        if not isinstance(row, dict):
            continue
        if row.get("object_kind") == "OBLIGATION":
            for prerequisite in row.get("fields", {}).get("prerequisite_obligation_ids", []):
                target = packet_objects.get(prerequisite)
                if target is None or target.get("object_kind") != "OBLIGATION":
                    errors.append("PREREQUISITE_UNRESOLVED")
        canonical = canonical_world.get(row.get("object_id"))
        if canonical is not None and canonical != row:
            errors.append("CANONICAL_OBJECT_MISMATCH")
    if packet.get("packet_hash") != packet_hash(packet):
        errors.append("PACKET_HASH_MISMATCH")
    envelope = load_contract("MBCX-01-PACKET-SCHEMAS-v3.json")["renderer"]["fixed_byte_envelope"]
    if len(canonical_json(packet)) >= envelope:
        errors.append("PACKET_ENVELOPE_EXCEEDED")
    return sorted(set(errors))


def score_condition(target_action_id: str, worker: dict[str, Any],
                    committed_actions: list[str], a1_selected: list[str],
                    gold_a1: list[str]) -> int:
    """Score B as exactly one target and no extra semantic child."""
    b_ok = (worker.get("status_code") == "PROPOSE"
            and worker.get("proposed_action_ids") == [target_action_id]
            and committed_actions == [target_action_id])
    a1_ok = (len(a1_selected) == len(set(a1_selected))
             and sorted(a1_selected) == sorted(gold_a1))
    return int(b_ok and a1_ok)


def framed_hash(parts: list[str]) -> bytes:
    framed = b"".join(len(part.encode("utf-8")).to_bytes(8, "big")
                      + part.encode("utf-8") for part in parts)
    return hashlib.sha256(framed).digest()


def choose_one_cut(scenario_id: str, cut_ids: list[str]) -> str:
    ordered = sorted(cut_ids, key=lambda value: value.encode("utf-8"))
    if not ordered or len(ordered) != len(set(ordered)):
        raise ValueError("cut_ids must be nonempty and unique")
    digest = framed_hash([scenario_id, *ordered, "stage2-cut-r9"])
    return ordered[int.from_bytes(digest, "big") % len(ordered)]


def evaluate_eligibility(canonical_state: dict[str, Any], cut: dict[str, Any],
                         action_ids: list[str], gold_action_id: str) -> tuple[bool, str]:
    """Recompute eligibility only from canonical state at the selected cut."""
    if len(action_ids) != len(set(action_ids)) or gold_action_id not in action_ids:
        return False, "ACTION_UNIVERSE_INVALID"
    if not any(value != gold_action_id for value in action_ids):
        return False, "NON_GOLD_ACTION_ABSENT"
    due = []
    for scope in canonical_state.get("scopes", {}).values():
        for obligation in scope.get("obligations", {}).values():
            if (obligation.get("mounted") is True
                    and obligation.get("critical") is True
                    and obligation.get("lifecycle") == "OPEN"
                    and obligation.get("due_at", "") <= cut.get("valid_time", "")):
                due.append(obligation)
    if len(due) != 1:
        return False, "UNIQUE_DUE_OBLIGATION_REQUIRED"
    if due[0].get("completion_action_id") != gold_action_id:
        return False, "GOLD_ACTION_MISMATCH"
    return True, "ELIGIBLE"


def select_cohort(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    contract = load_contract("MBCX-01-MEASUREMENT-CONTRACT-v3.json")
    freeze = contract["source_and_cohort_freeze"]
    selected: list[dict[str, Any]] = []
    for motif in freeze["motifs"]:
        rows = [copy.deepcopy(row) for row in candidates if row.get("motif") == motif]
        generated = freeze["generated_unique_scenarios_per_motif"]
        retained = freeze["retained_unique_scenarios_per_motif"]
        if len(rows) != generated or len({row.get("scenario_id") for row in rows}) != generated:
            raise ValueError(f"{motif} must have {generated} unique scenarios")
        eligible_rows = []
        for row in rows:
            chosen = choose_one_cut(row["scenario_id"], row["cut_ids"])
            eligible, reason = evaluate_eligibility(
                row["canonical_state_by_cut"][chosen], row["cut_by_id"][chosen],
                row["action_ids_by_cut"][chosen], row["gold_action_id_by_cut"][chosen])
            row.pop("eligible", None)
            row.pop("supplied_eligible", None)
            row["chosen_cut_id"] = chosen
            row["eligible"] = eligible
            row["eligibility_reason"] = reason
            row["eligibility_source"] = "RECOMPUTED"
            row["retention_hash"] = framed_hash(
                [motif, row["scenario_id"], chosen, "stage2-retain-r9"]).hex().upper()
            if eligible:
                eligible_rows.append(row)
        eligible_rows.sort(key=lambda row: (bytes.fromhex(row["retention_hash"]),
                                             row["scenario_id"].encode("utf-8")))
        if len(eligible_rows) < retained:
            raise ValueError(f"DESIGN_OR_IMPLEMENTATION_FAIL: {motif} shortfall")
        selected.extend(eligible_rows[:retained])
    if len({row["scenario_id"] for row in selected}) != len(selected):
        raise ValueError("scenario IDs must be globally unique")
    return selected


def synthetic_candidates() -> list[dict[str, Any]]:
    motifs = load_contract("MBCX-01-MEASUREMENT-CONTRACT-v3.json")[
        "source_and_cohort_freeze"]["motifs"]
    rows: list[dict[str, Any]] = []
    for motif_index, motif in enumerate(motifs):
        for index in range(load_contract("MBCX-01-MEASUREMENT-CONTRACT-v3.json")[
                "source_and_cohort_freeze"]["generated_unique_scenarios_per_motif"]):
            scenario_id = f"SCENARIO.{motif_index}.{index:03d}"
            cut_ids = [f"CUT.{scenario_id}.{cut_index:02d}" for cut_index in range(3)]
            canonical_state_by_cut: dict[str, Any] = {}
            cut_by_id: dict[str, Any] = {}
            action_ids_by_cut: dict[str, Any] = {}
            gold_action_id_by_cut: dict[str, Any] = {}
            for cut_index, cut_id in enumerate(cut_ids):
                scope_id = f"SCOPE.{scenario_id}"
                target_id = f"OBL.{scenario_id}.{cut_index}"
                decoy_id = f"OBL.{scenario_id}.DECOY.{cut_index}"
                gold = action_id(scope_id, target_id)
                decoy = action_id(scope_id, decoy_id)
                cut = {"journal_seq": cut_index + 1, "knowledge_time": T1,
                       "valid_time": T1}
                cut_by_id[cut_id] = cut
                canonical_state_by_cut[cut_id] = {
                    "scopes": {scope_id: {"obligations": {
                        target_id: {"mounted": True, "critical": True,
                                    "lifecycle": "OPEN", "due_at": T0,
                                    "completion_action_id": gold},
                        decoy_id: {"mounted": True, "critical": False,
                                   "lifecycle": "OPEN", "due_at": T1,
                                   "completion_action_id": decoy},
                    }}}
                }
                action_ids_by_cut[cut_id] = [gold, decoy, "NO_ACTION"]
                gold_action_id_by_cut[cut_id] = gold
            rows.append({
                "motif": motif, "difficulty_stratum": index % 4,
                "scenario_id": scenario_id, "cut_ids": cut_ids,
                "canonical_state_by_cut": canonical_state_by_cut,
                "cut_by_id": cut_by_id, "action_ids_by_cut": action_ids_by_cut,
                "gold_action_id_by_cut": gold_action_id_by_cut,
            })
    return rows


def measurement_grid() -> set[tuple[int, int, int]]:
    axes = load_contract("MBCX-01-MEASUREMENT-CONTRACT-v3.json")["axis_values"]
    return {(h, d, f) for h in axes["H"] for d in axes["D"] for f in axes["F"]}


def _baseline_counters() -> dict[str, int]:
    return {
        "SOURCE_BYTES_READ": 2048,
        "ARTIFACT_BYTES_READ": 2048,
        "ARTIFACT_BYTES_WRITTEN": 1024,
        "FILESYSTEM_BYTES_READ": 4096,
        "FILESYSTEM_BYTES_WRITTEN": 4096,
        "DATABASE_BYTES_READ": 4096,
        "DATABASE_BYTES_WRITTEN": 0,
        "SOURCE_RECORDS_READ": 4,
        "INDEX_RECORDS_READ": 8,
        "PAGES_READ": 1,
        "PAGES_WRITTEN": 0,
        "DEPENDENCY_OPERATIONS": 4,
        "DECODE_OPERATIONS": 4,
        "MATERIALIZATION_OPERATIONS": 2,
        "PROCESS_CPU_INSTRUCTIONS": 1000000,
        "CHILD_CPU_INSTRUCTIONS": 0,
        "PROCESS_CPU_TIME_NS": 20000000,
        "CHILD_CPU_TIME_NS": 0,
        "PEAK_RSS_BYTES": 33554432,
        "PEAK_ALLOCATED_BYTES": 16777216,
        "IMPLEMENTATION_BRANCHES": 3,
        "UNREGISTERED_FALLBACK_BRANCHES": 0,
    }


def baseline_counter_rows(candidate_id: str = "BASELINE") -> list[dict[str, Any]]:
    return [{"candidate_id": candidate_id, "H": h, "D": d, "F": f,
             "database_page_size_bytes": 4096, "descendant_accounted": True,
             "unregistered_work": False, "counters": _baseline_counters()}
            for h, d, f in sorted(measurement_grid())]


def _conditional_ranges(rows: list[dict[str, Any]], value) -> dict[str, int]:
    result: dict[str, int] = {}
    for axis, others in (("H", ("D", "F")), ("D", ("H", "F")),
                         ("F", ("H", "D"))):
        groups: dict[tuple[int, int], list[int]] = {}
        for row in rows:
            groups.setdefault((row[others[0]], row[others[1]]), []).append(value(row))
        result[axis] = max(max(values) - min(values) for values in groups.values())
    return result


def evaluate_counter_grid(rows: list[dict[str, Any]]) -> list[str]:
    contract = load_contract("MBCX-01-MEASUREMENT-CONTRACT-v3.json")
    errors: set[str] = set()
    expected_cells = measurement_grid()
    cells = [(row.get("H"), row.get("D"), row.get("F")) for row in rows]
    if len(rows) != len(expected_cells) or set(cells) != expected_cells or len(cells) != len(set(cells)):
        errors.add("COVERAGE_INVALID")
    catalog = {entry["id"]: entry for entry in contract["counter_catalog"]}
    required_row_keys = set(contract["counter_row_schema"]["required"])
    valid_rows = []
    for row in rows:
        if set(row) != required_row_keys:
            errors.add("COUNTER_SCHEMA_INVALID")
            continue
        counters = row.get("counters")
        if not isinstance(counters, dict) or set(counters) != set(catalog):
            errors.add("COUNTER_SET_INVALID")
            continue
        if any(not isinstance(value, int) or isinstance(value, bool) or value < 0
               for value in counters.values()):
            errors.add("COUNTER_VALUE_INVALID")
            continue
        valid_rows.append(row)
        if row["database_page_size_bytes"] != contract["storage"]["database_page_size_bytes"]:
            errors.add("PAGE_SIZE_MISMATCH")
        if row["descendant_accounted"] is not True:
            errors.add("DESCENDANT_ACCOUNTING_MISSING")
        if row["unregistered_work"] is not False:
            errors.add("UNREGISTERED_WORK")
        if counters["PAGES_READ"] != math.ceil(counters["DATABASE_BYTES_READ"] / 4096):
            errors.add("PAGE_BYTE_INCONSISTENT")
        if counters["PAGES_WRITTEN"] != math.ceil(counters["DATABASE_BYTES_WRITTEN"] / 4096):
            errors.add("PAGE_BYTE_INCONSISTENT")
        for counter_id, rule in catalog.items():
            if counters[counter_id] > rule["absolute_max"]:
                errors.add("COUNTER_ABSOLUTE_LIMIT")
    if len(valid_rows) != len(expected_cells):
        return sorted(errors)

    for counter_id, rule in catalog.items():
        ranges = _conditional_ranges(valid_rows, lambda row, key=counter_id: row["counters"][key])
        if any(ranges[axis] > rule[f"{axis}_range_max"] for axis in ("H", "D", "F")):
            errors.add("COUNTER_RANGE_LIMIT")
    units = sorted(set(rule["unit_class"] for rule in catalog.values()))
    for unit in units:
        ids = [counter_id for counter_id, rule in catalog.items() if rule["unit_class"] == unit]
        gate = contract["unit_total_gates"][unit]
        total = lambda row, keys=ids: sum(row["counters"][key] for key in keys)
        if any(total(row) > gate["absolute_max"] for row in valid_rows):
            errors.add("UNIT_TOTAL_LIMIT")
        ranges = _conditional_ranges(valid_rows, total)
        if any(ranges[axis] > gate[f"{axis}_range_max"] for axis in ("H", "D", "F")):
            errors.add("UNIT_TOTAL_LIMIT")
    axes = contract["axis_values"]
    for gate in contract["shape_gates"]:
        axis = gate["axis"]
        other_axes = [name for name in ("H", "D", "F") if name != axis]
        indexed = {(row["H"], row["D"], row["F"]): row for row in valid_rows}
        for first in axes[other_axes[0]]:
            for second in axes[other_axes[1]]:
                coordinates = {other_axes[0]: first, other_axes[1]: second,
                               axis: gate["lower"]}
                lower = indexed[(coordinates["H"], coordinates["D"], coordinates["F"])][
                    "counters"][gate["counter_id"]]
                coordinates[axis] = gate["upper"]
                upper = indexed[(coordinates["H"], coordinates["D"], coordinates["F"])][
                    "counters"][gate["counter_id"]]
                if upper - lower > gate["max_increase"]:
                    errors.add(gate["error"])
    return sorted(errors)


def execute_red_candidate(name: str) -> list[dict[str, Any]]:
    declared = load_contract("MBCX-01-MEASUREMENT-CONTRACT-v3.json")["red_candidates"]
    if name not in declared:
        raise ValueError(f"unknown red candidate: {name}")
    rows = baseline_counter_rows(name)
    if name == "HDF_INTERIOR_HOTSPOT":
        target = next(row for row in rows if (row["H"], row["D"], row["F"])
                      == (10000, 64, 256))
        target["counters"]["SOURCE_BYTES_READ"] = 12000
    elif name == "LOW_SLOPE_ARCHIVE_LINEAR_10X":
        for row in rows:
            row["counters"]["PROCESS_CPU_INSTRUCTIONS"] = 10 * row["H"]
    elif name == "HIDDEN_CHILD_CPU":
        rows[0]["descendant_accounted"] = False
    elif name == "COUNTER_SPLIT_SAME_WORK":
        for row in rows:
            row["counters"]["PROCESS_CPU_INSTRUCTIONS"] = 2000000
            row["counters"]["CHILD_CPU_INSTRUCTIONS"] = 2000000
    elif name == "PAGE_SIZE_SUBSTITUTION":
        for row in rows:
            row["database_page_size_bytes"] = 8192
    elif name == "LOGICAL_LOOKUP_PHYSICAL_SCAN":
        for row in rows:
            row["counters"]["DATABASE_BYTES_READ"] = row["D"] * 4096
            row["counters"]["PAGES_READ"] = row["D"]
    elif name == "PAGE_BYTE_MISMATCH":
        rows[0]["counters"]["PAGES_READ"] += 1
    return rows


SCIENTIFIC_N = 768


def psi_e(value: float) -> float:
    if not 0.0 <= value < 1.0:
        raise ValueError("psi_E input must be in [0,1)")
    return -math.log1p(-value) - value


def stream_statistics(xs: list[float], kappa: float | str = 0.25) -> tuple[float, float]:
    if not xs or any(not 0.0 <= value <= 1.0 for value in xs):
        raise ValueError("observations must be a nonempty sequence in [0,1]")
    if kappa == "UNIFORM":
        variance = 0.0
    else:
        if not isinstance(kappa, (int, float)) or kappa <= 0.0:
            raise ValueError("kappa must be positive or UNIFORM")
        variance = 1.0 / (2.0 * float(kappa) * float(kappa))
    prefix = 0.0
    for index, value in enumerate(xs, 1):
        estimate = (0.5 + prefix) / index
        variance += psi_e(abs(value - estimate))
        prefix += value
    return prefix, variance


def stream_statistics_decimal(xs: list[float], kappa: float | str) -> tuple[Decimal, Decimal]:
    decimal_xs = [Decimal(str(value)) for value in xs]
    if not decimal_xs or any(not Decimal(0) <= value <= Decimal(1) for value in decimal_xs):
        raise ValueError("observations must be a nonempty sequence in [0,1]")
    if kappa == "UNIFORM":
        variance = Decimal(0)
    else:
        decimal_kappa = Decimal(str(kappa))
        if decimal_kappa <= 0:
            raise ValueError("kappa must be positive or UNIFORM")
        variance = Decimal(1) / (Decimal(2) * decimal_kappa * decimal_kappa)
    prefix = Decimal(0)
    for index, value in enumerate(decimal_xs, 1):
        estimate = (Decimal("0.5") + prefix) / Decimal(index)
        distance = abs(value - estimate)
        variance += -(Decimal(1) - distance).ln() - distance
        prefix += value
    return prefix, variance


def mixture_integral_analytic(y: float, variance: float) -> float:
    if variance < 0.0:
        raise ValueError("variance must be nonnegative")
    if variance == 0.0:
        return 2.0 if y == 0.0 else 2.0 * math.sinh(y) / y
    root = math.sqrt(variance)
    shift = y / (2.0 * variance)
    difference = math.erf(root * (1.0 - shift)) - math.erf(root * (-1.0 - shift))
    return (math.exp(y * y / (4.0 * variance)) * math.sqrt(math.pi)
            * difference / (2.0 * root))


def mixture_integral_simpson(y: float, variance: float, intervals: int = 16384) -> float:
    if variance < 0.0 or intervals <= 0 or intervals % 2:
        raise ValueError("nonnegative variance and positive even intervals required")
    width = 2.0 / intervals
    total = math.exp(-y - variance) + math.exp(y - variance)
    for index in range(1, intervals):
        z = -1.0 + index * width
        total += (4.0 if index % 2 else 2.0) * math.exp(y * z - variance * z * z)
    return total * width / 3.0


def mixture_integral_decimal(y: Decimal, variance: Decimal,
                             intervals: int = 4096) -> Decimal:
    if variance < 0 or intervals <= 0 or intervals % 2:
        raise ValueError("nonnegative variance and positive even intervals required")
    width = Decimal(2) / Decimal(intervals)
    total = (-y - variance).exp() + (y - variance).exp()
    for index in range(1, intervals):
        z = Decimal(-1) + Decimal(index) * width
        total += (Decimal(4) if index % 2 else Decimal(2)) * (
            y * z - variance * z * z).exp()
    return total * width / Decimal(3)


def _mixture_threshold(alpha: float, kappa: float | str) -> float:
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be in (0,1)")
    if kappa == "UNIFORM":
        return 2.0 / alpha
    value = float(kappa)
    if value <= 0.0:
        raise ValueError("kappa must be positive")
    normalizer = math.erf(1.0 / (value * math.sqrt(2.0)))
    return value * normalizer * math.sqrt(2.0 * math.pi) / alpha


def _decimal_threshold(alpha: float, kappa: float | str,
                       intervals: int = 4096) -> Decimal:
    decimal_alpha = Decimal(str(alpha))
    if kappa == "UNIFORM":
        return Decimal(2) / decimal_alpha
    decimal_kappa = Decimal(str(kappa))
    width = Decimal(2) / Decimal(intervals)
    def density(z: Decimal) -> Decimal:
        return (-(z * z) / (Decimal(2) * decimal_kappa * decimal_kappa)).exp()
    total = density(Decimal(-1)) + density(Decimal(1))
    for index in range(1, intervals):
        z = Decimal(-1) + Decimal(index) * width
        total += (Decimal(4) if index % 2 else Decimal(2)) * density(z)
    return total * width / Decimal(3) / decimal_alpha


def _decimal_boundary(variance: Decimal, alpha: float,
                      kappa: float | str) -> Decimal:
    threshold = _decimal_threshold(alpha, kappa)
    low, high = Decimal(0), Decimal(1)
    while mixture_integral_decimal(high, variance) < threshold:
        high *= 2
        if high > 4096:
            raise ArithmeticError("failed to bracket decimal mixture boundary")
    for _ in range(80):
        mid = (low + high) / 2
        if mixture_integral_decimal(mid, variance) < threshold:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def mixture_boundary(variance: float, alpha: float = 0.025,
                     kappa: float | str = 0.25, method: str = "analytic") -> float:
    threshold = _mixture_threshold(alpha, kappa)
    if method == "decimal":
        with localcontext() as context:
            context.prec = 60
            return float(_decimal_boundary(Decimal(str(variance)), alpha, kappa))
    if method not in ("analytic", "simpson"):
        raise ValueError("method must be analytic, simpson, or decimal")
    integral = mixture_integral_analytic if method == "analytic" else mixture_integral_simpson
    low, high = 0.0, 1.0
    while integral(high, variance) < threshold:
        high *= 2.0
        if high > 4096.0:
            raise ArithmeticError("failed to bracket mixture boundary")
    for _ in range(80):
        mid = (low + high) / 2.0
        if integral(mid, variance) < threshold:
            low = mid
        else:
            high = mid
    return (low + high) / 2.0


def mixture_interval(xs: list[float], alpha: float = 0.025,
                     kappa: float | str = 0.25,
                     method: str = "analytic") -> tuple[float, float]:
    if method == "decimal":
        with localcontext() as context:
            context.prec = 60
            total_decimal, variance_decimal = stream_statistics_decimal(xs, kappa)
            half_width_decimal = _decimal_boundary(
                variance_decimal, alpha, kappa) / Decimal(len(xs))
            mean_decimal = total_decimal / Decimal(len(xs))
            lower = max(Decimal(0), mean_decimal - half_width_decimal)
            upper = min(Decimal(1), mean_decimal + half_width_decimal)
            return float(lower), float(upper)
    total, variance = stream_statistics(xs, kappa)
    half_width = mixture_boundary(variance, alpha, kappa, method) / len(xs)
    mean = total / len(xs)
    return max(0.0, mean - half_width), min(1.0, mean + half_width)


def paired_intervals(pairs: list[tuple[int, int]], method: str = "analytic",
                     kappa: float | str = 0.25) -> tuple[tuple[float, float], tuple[float, float]]:
    if len(pairs) != SCIENTIFIC_N:
        raise ValueError("scientific intervals exist only at n=768")
    transformed_delta = [(bc - om + 1.0) / 2.0 for bc, om in pairs]
    delta_unit = mixture_interval(transformed_delta, kappa=kappa, method=method)
    delta = (2.0 * delta_unit[0] - 1.0, 2.0 * delta_unit[1] - 1.0)
    om = mixture_interval([float(pair[1]) for pair in pairs], kappa=kappa, method=method)
    return delta, om


def scientific_decision(delta_interval: tuple[float, float],
                        om_interval: tuple[float, float]) -> str:
    if om_interval[1] < 0.80:
        return "MODEL_OR_INTERFACE_CEILING"
    if delta_interval[1] < -0.10 and om_interval[0] >= 0.80:
        return "MODEL_INTERFACE_FAIL"
    if delta_interval[0] > -0.10 and om_interval[0] >= 0.80:
        return "PROMOTE_TO_COORDINATION_STAGE"
    return "INCONCLUSIVE_OR_UNDERFUNDED"


def scientific_look(n: int) -> str:
    if n != SCIENTIFIC_N:
        raise ValueError("scientific intervals are defined only at n=768")
    return "TERMINAL_SCIENTIFIC_DECISION"


def low_discord_pairs() -> list[tuple[int, int]]:
    vector = load_contract("MBCX-01-INFERENCE-CONTRACT-v4.json")[
        "reference_vectors"]["low_discord_deterministic"]
    pairs = [(1, 1)] * SCIENTIFIC_N
    occupied: set[int] = set()
    assignments = (
        (vector["zero_equal_positions_zero_based"], (0, 0)),
        (vector["bc0_om1_positions_zero_based"], (0, 1)),
        (vector["bc1_om0_positions_zero_based"], (1, 0)),
    )
    for positions, pair in assignments:
        for position in positions:
            if not isinstance(position, int) or not 0 <= position < SCIENTIFIC_N or position in occupied:
                raise ValueError("invalid or duplicate frozen low-discord position")
            occupied.add(position)
            pairs[position] = pair
    if len(vector["bc0_om1_positions_zero_based"]) != 8 or len(
            vector["bc1_om0_positions_zero_based"]) != 8:
        raise ValueError("low-discord vector must contain eight pairs in each direction")
    return pairs


def kappa_sensitivity(pairs: list[tuple[int, int]]) -> list[dict[str, Any]]:
    rows = []
    for kappa in (0.10, 0.15, 0.25, 0.50, "UNIFORM"):
        delta, om = paired_intervals(pairs, kappa=kappa)
        rows.append({"kappa": kappa, "n": SCIENTIFIC_N,
                     "delta_interval": list(delta), "om_interval": list(om),
                     "branch": scientific_decision(delta, om)})
    return rows


def reliability_cell_alpha(mode_count: int) -> float:
    if mode_count <= 0:
        raise ValueError("mode_count must be positive")
    return 0.05 / (6 * mode_count)


def reliability_cell_budget(mode_count: int) -> float:
    if mode_count <= 0:
        raise ValueError("mode_count must be positive")
    return 0.02 / (6 * mode_count)


def clopper_pearson_upper(failures: int, trials: int, alpha: float) -> float:
    """One-sided exact binomial upper confidence endpoint."""
    if not 0 <= failures <= trials or trials <= 0 or not 0.0 < alpha < 1.0:
        raise ValueError("invalid binomial count or alpha")
    if failures == trials:
        return 1.0
    if failures == 0:
        return 1.0 - alpha ** (1.0 / trials)

    def cdf(probability: float) -> float:
        if probability <= 0.0:
            return 1.0
        if probability >= 1.0:
            return 0.0
        term = math.exp(trials * math.log1p(-probability))
        total = term
        odds = probability / (1.0 - probability)
        for index in range(1, failures + 1):
            term *= (trials - index + 1) / index * odds
            total += term
        return min(1.0, total)

    low, high = failures / trials, 1.0
    for _ in range(80):
        mid = (low + high) / 2.0
        if cdf(mid) > alpha:
            low = mid
        else:
            high = mid
    return (low + high) / 2.0


def zero_failure_min_trials(mode_count: int) -> int:
    alpha = reliability_cell_alpha(mode_count)
    budget = reliability_cell_budget(mode_count)
    return math.ceil(math.log(alpha) / math.log1p(-budget))


def transport_readiness(counts: dict[tuple[str, str], tuple[int, int]]) -> tuple[bool, dict[str, float]]:
    contract = load_contract("MBCX-01-INFERENCE-CONTRACT-v4.json")["transport_readiness"]
    modes = contract["failure_modes"]
    positions = contract["call_positions"]
    expected = {(mode, position) for mode in modes for position in positions}
    if set(counts) != expected:
        raise ValueError("mode-position count matrix must be complete and exact")
    alpha = reliability_cell_alpha(len(modes))
    budget = reliability_cell_budget(len(modes))
    bounds = {f"{mode}:{position}": clopper_pearson_upper(
        counts[(mode, position)][0], counts[(mode, position)][1], alpha)
              for mode, position in sorted(expected)}
    return all(bound <= budget for bound in bounds.values()), bounds


def _counter_uniforms(seed_parts: list[str], count: int):
    seed = b"".join(len(part.encode("utf-8")).to_bytes(8, "big")
                    + part.encode("utf-8") for part in seed_parts)
    produced = 0
    counter = 0
    denominator = float(1 << 64)
    while produced < count:
        digest = hashlib.sha256(seed + counter.to_bytes(8, "big")).digest()
        for integer in struct.unpack(">QQQQ", digest):
            if produced >= count:
                break
            yield integer / denominator
            produced += 1
        counter += 1


def _draw_pair(value: float, cell: dict[str, Any]) -> tuple[int, int]:
    p00 = cell["p00"]
    p01 = p00 + cell["p01"]
    p10 = p01 + cell["p10"]
    if value < p00:
        return 0, 0
    if value < p01:
        return 0, 1
    if value < p10:
        return 1, 0
    return 1, 1


def simulate_oc(replicates: int = 100,
                seed: str = "MBCX01-R9-OC-V1") -> dict[str, Any]:
    if replicates <= 0:
        raise ValueError("replicates must be positive")
    contract = load_contract("MBCX-01-INFERENCE-CONTRACT-v4.json")
    cells_out = []
    for cell in contract["operating_characteristics"]["cells"]:
        probabilities = [cell[key] for key in ("p00", "p01", "p10", "p11")]
        if any(value < 0.0 for value in probabilities) or abs(sum(probabilities) - 1.0) > 1e-12:
            raise ValueError(f"invalid OC cell {cell['id']}")
        if abs((cell["p10"] - cell["p01"]) - cell["delta"]) > 1e-12:
            raise ValueError(f"delta annotation mismatch in {cell['id']}")
        if abs((cell["p01"] + cell["p11"]) - cell["om"]) > 1e-12:
            raise ValueError(f"OM annotation mismatch in {cell['id']}")
        branches: dict[str, int] = {}
        delta_widths: list[float] = []
        om_widths: list[float] = []
        for replicate in range(replicates):
            pairs = [_draw_pair(value, cell) for value in
                     _counter_uniforms([seed, cell["id"], str(replicate)], SCIENTIFIC_N)]
            delta_interval, om_interval = paired_intervals(pairs)
            branch = scientific_decision(delta_interval, om_interval)
            branches[branch] = branches.get(branch, 0) + 1
            delta_widths.append(delta_interval[1] - delta_interval[0])
            om_widths.append(om_interval[1] - om_interval[0])
        delta_widths.sort()
        om_widths.sort()
        p95_index = max(0, math.ceil(0.95 * replicates) - 1)
        cells_out.append({
            "id": cell["id"], "delta": cell["delta"], "om": cell["om"],
            "replicates": replicates, "branch_counts": dict(sorted(branches.items())),
            "mean_delta_width": sum(delta_widths) / replicates,
            "p95_delta_width": delta_widths[p95_index],
            "mean_om_width": sum(om_widths) / replicates,
            "p95_om_width": om_widths[p95_index],
        })
    return {"schema_id": "MBCX01R9SyntheticOCV1", "experiment_evidence": False,
            "seed": seed, "n": SCIENTIFIC_N, "replicates_per_cell": replicates,
            "maximum_accepted_calls": SCIENTIFIC_N * 6,
            "expected_accepted_calls": SCIENTIFIC_N * 6, "cells": cells_out}
