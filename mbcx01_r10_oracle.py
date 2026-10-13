"""Independent post-schema state oracle for MBCX-01 r10.

The two reducers intentionally share the contract-driven schema ingress. After that
boundary this oracle uses a declarative guard table and the independent r9 handler
implementation, not the r10 reference reducer.
"""

from __future__ import annotations

import copy
from typing import Any, Callable

import mbcx01_r9_oracle as legacy_oracle
from mbcx01_r10_reference import action_id, canonical_json, cut_hash, fact_key, sha384, validate_event_schema


def _fact_at_cut(row: dict[str, Any], cut: dict[str, Any]) -> bool:
    visible = row["journal_seq"] <= cut["journal_seq"] and row["observed_at"] <= cut["knowledge_time"]
    effective = row["valid_from"] <= cut["valid_time"] and (
        row["valid_to"] is None or cut["valid_time"] < row["valid_to"])
    return visible and effective and not row["retracted"]


def _guard_obligation_identity(state: dict[str, Any], event: dict[str, Any]) -> str | None:
    body = event["payload"]
    expected = action_id(event["scope_id"], body["obligation_id"])
    return None if body["completion_action_id"] == expected else "ACTION_ID_HASH_GUARD"


def _guard_fact_target(state: dict[str, Any], event: dict[str, Any]) -> str | None:
    body = event["payload"]
    scope = state["scopes"].get(event["scope_id"], {})
    versions = scope.get("facts", {}).get(fact_key(body["subject_id"], body["predicate_id"]), [])
    identity = body["parent_event_id"] if event["event_type"] == "correct_fact" else body["target_event_id"]
    usable = [row for row in versions if row["event_id"] == identity and _fact_at_cut(row, event["originating_cut"])]
    if usable:
        return None
    return "FACT_PARENT_NOT_HEAD" if event["event_type"] == "correct_fact" else "FACT_TARGET_UNAVAILABLE"


def _guard_handoff_identity(state: dict[str, Any], event: dict[str, Any]) -> str | None:
    body = event["payload"]
    scope = state["scopes"].get(event["scope_id"], {})
    obligations = scope.get("obligations", {})
    if cut_hash(event["originating_cut"]) != body["originating_cut_hash"]:
        return "HANDOFF_OR_TARGET_ILLEGAL"
    if sha384(body["action_catalog"]) != body["action_catalog_hash"]:
        return "HANDOFF_OR_TARGET_ILLEGAL"
    if sha384(obligations) != body["canonical_snapshot_hash"]:
        return "HANDOFF_OR_TARGET_ILLEGAL"
    for entry in body["action_catalog"]:
        if entry["action_id"] != action_id(event["scope_id"], entry["obligation_id"]):
            return "ACTION_ID_HASH_GUARD"
    return None


def _guard_worker_link(state: dict[str, Any], event: dict[str, Any]) -> str | None:
    scope = state["scopes"].get(event["scope_id"], {})
    handoff = scope.get("handoffs", {}).get(event["payload"]["handoff_id"])
    recorded = {row["response_hash"] for row in state.get("responses", {}).values()}
    if handoff is not None and recorded and event["payload"]["worker_handoff_hash"] not in recorded:
        return "PROPOSAL_INVALID"
    return None


GUARDS: dict[str, Callable[[dict[str, Any], dict[str, Any]], str | None]] = {
    "open_obligation": _guard_obligation_identity,
    "correct_fact": _guard_fact_target,
    "retract_fact": _guard_fact_target,
    "open_handoff": _guard_handoff_identity,
    "propose_handoff_result": _guard_worker_link,
}


def _to_legacy(event: dict[str, Any]) -> dict[str, Any]:
    projected = copy.deepcopy(event)
    if projected["event_type"] == "open_handoff":
        projected["payload"].pop("action_catalog_hash")
        projected["payload"].pop("canonical_snapshot_hash")
    return projected


def oracle_apply(state: dict[str, Any], event: dict[str, Any]) -> tuple[dict[str, Any], str]:
    if validate_event_schema(event):
        return copy.deepcopy(state), "SCHEMA_INVALID"
    guard = GUARDS.get(event["event_type"])
    if guard is not None:
        failure = guard(state, event)
        if failure is not None:
            return copy.deepcopy(state), failure
    new_state, result = legacy_oracle.oracle_apply(copy.deepcopy(state), _to_legacy(event))
    if result == "APPLIED" and event["event_type"] == "open_handoff":
        handoff = new_state["scopes"][event["scope_id"]]["handoffs"][event["payload"]["handoff_id"]]
        handoff["action_catalog_hash"] = event["payload"]["action_catalog_hash"]
        handoff["canonical_snapshot_hash"] = event["payload"]["canonical_snapshot_hash"]
    return new_state, result

