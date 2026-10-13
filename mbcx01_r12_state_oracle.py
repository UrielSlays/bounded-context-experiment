"""Independent r12 state-transition oracle.

This module intentionally shares only r12's structural ingress and canonical
primitives.  It does not import the reference reducer or any historical
implementation.
"""

from __future__ import annotations

import copy
from typing import Any, Callable

import mbcx01_r12_common as common


State = dict[str, Any]
Event = dict[str, Any]
Handler = Callable[[State, Event], str]


def _effective_valid_to(row: State, cut: State) -> str | None:
    """Derive the cut-relative interval end without shared semantic helpers."""
    candidates = [row["valid_to"]] if row.get("valid_to") is not None else []
    for closure in row.get("closure_events", []):
        known = (closure["journal_seq"] <= cut["journal_seq"]
                 and closure["observed_at"] <= cut["knowledge_time"])
        if known:
            candidates.append(closure["valid_to"])
    return min(candidates, default=None)


def _retracted_at(row: State, cut: State) -> bool:
    legacy_retraction = row.get("retracted") is True and not row.get("retraction_events")
    if legacy_retraction:
        return True
    return any(
        retraction["journal_seq"] <= cut["journal_seq"]
        and retraction["observed_at"] <= cut["knowledge_time"]
        for retraction in row.get("retraction_events", [])
    )


def _visible_effective(row: State, cut: State) -> bool:
    end = _effective_valid_to(row, cut)
    return (
        not _retracted_at(row, cut)
        and row["journal_seq"] <= cut["journal_seq"]
        and row["observed_at"] <= cut["knowledge_time"]
        and row["valid_from"] <= cut["valid_time"]
        and (end is None or cut["valid_time"] < end)
    )


def _dependency_reaches(edges: list[list[str]], start: str, target: str) -> bool:
    pending = [start]
    visited: set[str] = set()
    while pending:
        node = pending.pop()
        if node == target:
            return True
        if node in visited:
            continue
        visited.add(node)
        pending.extend(parent for child, parent in edges if child == node)
    return False


def _actions_are_legal(obligations: State, catalog: list[State],
                       action_ids: list[str], valid_time: str) -> bool:
    targets = {
        row.get("action_id"): row.get("obligation_id")
        for row in catalog if isinstance(row, dict)
    }
    if (len(action_ids) != len(set(action_ids))
            or any(action not in targets for action in action_ids)):
        return False
    for action in action_ids:
        obligation = obligations.get(targets[action])
        if (not obligation
                or obligation["lifecycle"] != "OPEN"
                or not obligation["critical"]
                or obligation["due_at"] > valid_time
                or obligation["completion_action_id"] != action
                or any(obligations.get(prerequisite, {}).get("lifecycle") != "COMPLETED"
                       for prerequisite in obligation["prerequisite_obligation_ids"])):
            return False
    return True


class _OracleReducer:
    """Apply one already-admitted event to a private working state."""

    def __init__(self, state: State) -> None:
        self.state = state
        self._handlers: dict[str, Handler] = {
            "assert_fact": self._assert_fact,
            "correct_fact": self._correct_fact,
            "retract_fact": self._retract_fact,
            "open_obligation": self._open_obligation,
            "reschedule_obligation": self._reschedule_obligation,
            "delegate_obligation": self._delegate_obligation,
            "complete_obligation": self._complete_obligation,
            "cancel_obligation": self._cancel_obligation,
            "reopen_obligation": self._reopen_obligation,
            "link_dependency": self._link_dependency,
            "unlink_dependency": self._unlink_dependency,
            "open_handoff": self._open_handoff,
            "record_call_response": self._record_call_response,
            "propose_handoff_result": self._propose_handoff_result,
            "commit_handoff_result": self._commit_handoff_result,
            "reject_handoff_result": self._reject_handoff_result,
            "close_handoff": self._close_handoff,
        }

    def apply(self, event: Event) -> str:
        handler = self._handlers.get(event["event_type"])
        return handler(self.state, event) if handler is not None else "SCHEMA_INVALID"

    @staticmethod
    def _scope(state: State, event: Event) -> State:
        return state["scopes"].setdefault(event["scope_id"], common.fresh_scope())

    @classmethod
    def _facts(cls, state: State, event: Event) -> list[State]:
        payload = event["payload"]
        key = common.fact_key(payload["subject_id"], payload["predicate_id"])
        return cls._scope(state, event)["facts"].setdefault(key, [])

    @staticmethod
    def _visible_row(rows: list[State], event_id: str, cut: State) -> State | None:
        return next(
            (row for row in rows
             if row["event_id"] == event_id and _visible_effective(row, cut)),
            None,
        )

    @staticmethod
    def _new_fact_row(event: Event, *, parent_event_id: str | None,
                      valid_to: str | None) -> State:
        return {
            "event_id": event["event_id"],
            "parent_event_id": parent_event_id,
            "value_code": event["payload"]["value_code"],
            "observed_at": event["observed_at"],
            "valid_from": event["valid_from"],
            "valid_to": valid_to,
            "journal_seq": event["journal_seq"],
            "retracted": False,
            "closure_events": [],
            "retraction_events": [],
        }

    @staticmethod
    def _sort_facts(rows: list[State]) -> None:
        rows.sort(key=lambda row: (row["valid_from"], row["journal_seq"]))

    @staticmethod
    def _known_fact_cut(state: State, event: Event) -> State:
        return {
            "journal_seq": state["next_seq"] - 1,
            "knowledge_time": event["observed_at"],
            "valid_time": event["valid_from"],
        }

    @staticmethod
    def _intervals_overlap(first_start: str, first_end: str | None,
                           second_start: str, second_end: str | None) -> bool:
        return ((second_end is None or first_start < second_end)
                and (first_end is None or second_start < first_end))

    @classmethod
    def _overlaps_known_row(cls, rows: list[State], state: State, event: Event,
                            start: str, end: str | None,
                            *, excluded: State | None = None) -> bool:
        known_cut = cls._known_fact_cut(state, event)
        for row in rows:
            if row is excluded:
                continue
            row_end = _effective_valid_to(row, known_cut)
            if (not _retracted_at(row, known_cut)
                    and row["journal_seq"] <= known_cut["journal_seq"]
                    and row["observed_at"] <= known_cut["knowledge_time"]
                    and cls._intervals_overlap(start, end, row["valid_from"], row_end)):
                return True
        return False

    def _assert_fact(self, state: State, event: Event) -> str:
        rows = self._facts(state, event)
        if any(_visible_effective(row, event["originating_cut"]) for row in rows):
            return "FACT_ALREADY_EXISTS"

        start = event["valid_from"]
        future_starts = [
            row["valid_from"] for row in rows
            if not _retracted_at(row, self._known_fact_cut(state, event))
            and row["valid_from"] > start
        ]
        end = (event["valid_to"] if event["valid_to"] is not None
               else min(future_starts, default=None))
        if self._overlaps_known_row(rows, state, event, start, end):
            return "FACT_ALREADY_EXISTS"
        rows.append(self._new_fact_row(event, parent_event_id=None, valid_to=end))
        self._sort_facts(rows)
        return "APPLIED"

    def _correct_fact(self, state: State, event: Event) -> str:
        rows = self._facts(state, event)
        parent_id = event["payload"]["parent_event_id"]
        parent = self._visible_row(rows, parent_id, event["originating_cut"])
        if parent is None:
            return "FACT_PARENT_NOT_HEAD"
        if any(row["parent_event_id"] == parent_id
               and _visible_effective(row, event["originating_cut"])
               for row in rows):
            return "FACT_PARENT_NOT_HEAD"

        old_end = _effective_valid_to(parent, event["originating_cut"])
        if event["valid_from"] <= parent["valid_from"]:
            return "FACT_PARENT_NOT_HEAD"
        if old_end is not None and event["valid_from"] >= old_end:
            return "FACT_PARENT_NOT_HEAD"
        child_end = event["valid_to"] if event["valid_to"] is not None else old_end
        if (child_end is not None and child_end <= event["valid_from"]
                or old_end is not None and child_end is not None and child_end > old_end):
            return "FACT_PARENT_NOT_HEAD"
        if self._overlaps_known_row(
            rows, state, event, event["valid_from"], child_end, excluded=parent
        ):
            return "FACT_PARENT_NOT_HEAD"

        parent.setdefault("closure_events", []).append({
            "event_id": event["event_id"],
            "journal_seq": event["journal_seq"],
            "observed_at": event["observed_at"],
            "valid_to": event["valid_from"],
        })
        rows.append(self._new_fact_row(event, parent_event_id=parent_id, valid_to=child_end))
        self._sort_facts(rows)
        return "APPLIED"

    def _retract_fact(self, state: State, event: Event) -> str:
        rows = self._facts(state, event)
        target = self._visible_row(
            rows, event["payload"]["target_event_id"], event["originating_cut"]
        )
        if target is None:
            return "FACT_TARGET_UNAVAILABLE"
        target.setdefault("retraction_events", []).append({
            "event_id": event["event_id"],
            "journal_seq": event["journal_seq"],
            "observed_at": event["observed_at"],
        })
        return "APPLIED"

    @classmethod
    def _obligations(cls, state: State, event: Event) -> State:
        return cls._scope(state, event)["obligations"]

    def _open_obligation(self, state: State, event: Event) -> str:
        payload = event["payload"]
        obligations = self._obligations(state, event)
        obligation_id = payload["obligation_id"]
        prerequisites = payload["prerequisite_obligation_ids"]
        if (obligation_id in obligations
                or any(item not in obligations for item in prerequisites)
                or payload["completion_action_id"] != common.action_id(
                    event["scope_id"], obligation_id
                )):
            return "OBLIGATION_ALREADY_EXISTS_OR_BAD_PREREQUISITE"

        obligations[obligation_id] = {
            "subject_id": payload["subject_id"],
            "owner_role": payload["owner_role"],
            "due_at": payload["due_at"],
            "critical": payload["critical"],
            "lifecycle": "OPEN",
            "completion_action_id": payload["completion_action_id"],
            "prerequisite_obligation_ids": sorted(prerequisites),
            "terminal_event_id": None,
        }
        dependencies = self._scope(state, event)["dependencies"]
        dependencies.extend([[obligation_id, item] for item in prerequisites])
        dependencies.sort()
        return "APPLIED"

    def _open_obligation_row(self, state: State, event: Event) -> State | None:
        obligation = self._obligations(state, event).get(event["payload"]["obligation_id"])
        return obligation if obligation and obligation["lifecycle"] == "OPEN" else None

    def _reschedule_obligation(self, state: State, event: Event) -> str:
        obligation = self._open_obligation_row(state, event)
        if obligation is None:
            return "OBLIGATION_NOT_OPEN"
        obligation["due_at"] = event["payload"]["due_at"]
        return "APPLIED"

    def _delegate_obligation(self, state: State, event: Event) -> str:
        obligation = self._open_obligation_row(state, event)
        if obligation is None:
            return "OBLIGATION_NOT_OPEN"
        obligation["owner_role"] = event["payload"]["owner_role"]
        return "APPLIED"

    def _complete_obligation(self, state: State, event: Event) -> str:
        obligation = self._open_obligation_row(state, event)
        if obligation is None:
            return "OBLIGATION_NOT_OPEN"
        payload = event["payload"]
        cut = event["originating_cut"]
        obligations = self._obligations(state, event)
        legal = (
            obligation["critical"]
            and obligation["due_at"] <= cut["valid_time"]
            and obligation["completion_action_id"] == payload["completion_action_id"]
            and payload["originating_cut_hash"] == common.cut_hash(cut)
            and all(
                obligations.get(item, {}).get("lifecycle") == "COMPLETED"
                for item in obligation["prerequisite_obligation_ids"]
            )
        )
        if not legal:
            return "OBLIGATION_NOT_DUE_AT_ORIGINATING_CUT"
        obligation.update(lifecycle="COMPLETED", terminal_event_id=event["event_id"])
        return "APPLIED"

    def _cancel_obligation(self, state: State, event: Event) -> str:
        obligation = self._open_obligation_row(state, event)
        if obligation is None:
            return "OBLIGATION_NOT_OPEN"
        obligation.update(lifecycle="CANCELLED", terminal_event_id=event["event_id"])
        return "APPLIED"

    def _reopen_obligation(self, state: State, event: Event) -> str:
        payload = event["payload"]
        obligation = self._obligations(state, event).get(payload["obligation_id"])
        if not obligation or obligation["lifecycle"] not in {"COMPLETED", "CANCELLED"}:
            return "OBLIGATION_NOT_TERMINAL"
        obligation.update(
            lifecycle="OPEN",
            due_at=payload["due_at"],
            owner_role=payload["owner_role"],
            terminal_event_id=None,
        )
        return "APPLIED"

    def _link_dependency(self, state: State, event: Event) -> str:
        payload = event["payload"]
        edge = [payload["obligation_id"], payload["prerequisite_obligation_id"]]
        scope = self._scope(state, event)
        obligations = scope["obligations"]
        dependencies = scope["dependencies"]
        if (edge in dependencies
                or edge[0] == edge[1]
                or any(obligations.get(item, {}).get("lifecycle") != "OPEN" for item in edge)
                or _dependency_reaches(dependencies, edge[1], edge[0])):
            return "DEPENDENCY_ILLEGAL"
        dependencies.append(edge)
        dependencies.sort()
        obligation = obligations[edge[0]]
        obligation["prerequisite_obligation_ids"] = sorted(set(
            obligation["prerequisite_obligation_ids"] + [edge[1]]
        ))
        return "APPLIED"

    def _unlink_dependency(self, state: State, event: Event) -> str:
        payload = event["payload"]
        edge = [payload["obligation_id"], payload["prerequisite_obligation_id"]]
        scope = self._scope(state, event)
        if edge not in scope["dependencies"]:
            return "DEPENDENCY_NOT_FOUND"
        scope["dependencies"].remove(edge)
        scope["obligations"][edge[0]]["prerequisite_obligation_ids"].remove(edge[1])
        return "APPLIED"

    def _open_handoff(self, state: State, event: Event) -> str:
        payload = event["payload"]
        scope = self._scope(state, event)
        obligations = scope["obligations"]
        target = obligations.get(payload["target_obligation_id"])
        if (payload["handoff_id"] in scope["handoffs"]
                or not target or target["lifecycle"] != "OPEN"):
            return "HANDOFF_OR_TARGET_ILLEGAL"

        catalog = payload["action_catalog"]
        try:
            task_packet = common.json.loads(payload["task_packet_utf8"])
            manifest = common.json.loads(payload["manifest_utf8"])
        except (TypeError, ValueError):
            return "HANDOFF_OR_TARGET_ILLEGAL"
        authority_ok = (
            isinstance(task_packet, dict) and isinstance(manifest, dict)
            and payload["task_packet_utf8"] == common.canonical_json(task_packet).decode("utf-8")
            and payload["manifest_utf8"] == common.canonical_json(manifest).decode("utf-8")
            and task_packet.get("task_packet_hash") == payload["task_packet_hash"]
            and task_packet.get("task_packet_hash") == common.sha384({
                key: value for key, value in task_packet.items() if key != "task_packet_hash"})
            and task_packet.get("scenario_id") == payload["scenario_id"]
            and task_packet.get("scope_id") == event["scope_id"]
            and task_packet.get("manifest_hash") == payload["manifest_hash"]
            and task_packet.get("requested_action_catalog_hash") == payload["action_catalog_hash"]
            and manifest.get("manifest_hash") == payload["manifest_hash"]
            and manifest.get("manifest_hash") == common.sha384({
                key: value for key, value in manifest.items() if key != "manifest_hash"})
            and manifest.get("scenario_id") == payload["scenario_id"]
            and manifest.get("scope_id") == event["scope_id"]
            and manifest.get("action_catalog_hash") == payload["action_catalog_hash"]
            and manifest.get("action_catalog") == catalog)
        actionable = [row for row in catalog if row.get("obligation_id") is not None]
        invalid_binding = any(
            row.get("action_id") != common.action_id(event["scope_id"], row["obligation_id"])
            or ("scope_id" in row and row["scope_id"] != event["scope_id"])
            for row in actionable
        )
        target_action = common.action_id(event["scope_id"], payload["target_obligation_id"])
        if (not authority_ok
                or payload["originating_cut_hash"] != common.cut_hash(event["originating_cut"])
                or payload["action_catalog_hash"] != common.sha384(catalog)
                or payload["canonical_snapshot_hash"] != common.sha384(obligations)
                or not any(row["action_id"] == target_action
                           and row["obligation_id"] == payload["target_obligation_id"]
                           for row in actionable)
                or invalid_binding):
            return "HANDOFF_OR_TARGET_ILLEGAL"

        scope["handoffs"][payload["handoff_id"]] = {
            "status": "OPEN",
            "terminal_disposition": None,
            "scenario_id": payload["scenario_id"],
            "condition": payload["condition"],
            "target_obligation_id": payload["target_obligation_id"],
            "task_packet_hash": payload["task_packet_hash"],
            "served_request_hash": payload["served_request_hash"],
            "request_parameters_hash": payload["request_parameters_hash"],
            "idempotency_token": payload["idempotency_token"],
            "task_packet_utf8": payload["task_packet_utf8"],
            "manifest_utf8": payload["manifest_utf8"],
            "route_contract_hash": payload["route_contract_hash"],
            "manifest_hash": payload["manifest_hash"],
            "originating_cut": copy.deepcopy(event["originating_cut"]),
            "originating_cut_hash": payload["originating_cut_hash"],
            "scope_id": event["scope_id"],
            "opened_journal_seq": event["journal_seq"],
            "opened_observed_at": event["observed_at"],
            "action_catalog": copy.deepcopy(catalog),
            "originating_obligations": copy.deepcopy(obligations),
            "proposal_event_id": None,
            "proposal_hash": None,
            "worker_handoff_hash": None,
            "action_ids": [],
        }
        return "APPLIED"

    @staticmethod
    def _response_key(payload: State) -> str:
        return common.sha256([
            payload["scope_id"], payload["handoff_id"], payload["scenario_id"],
            payload["condition"], payload["node"]
        ])

    def _record_call_response(self, state: State, event: Event) -> str:
        payload = event["payload"]
        scope = self._scope(state, event)
        handoff = scope["handoffs"].get(payload["handoff_id"])
        worker = common.json.loads(payload["raw_response_utf8"])
        exact_handoff = (
            handoff
            and handoff["status"] == "OPEN"
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
                common.action_id(event["scope_id"], handoff["target_obligation_id"])]
            and worker["produced_at"] >= handoff["opened_observed_at"]
            and worker["produced_at"] <= payload["accepted_at"] <= event["observed_at"]
            and event["journal_seq"] > handoff["opened_journal_seq"]
        )
        if not exact_handoff:
            return "CALL_RESPONSE_CONFLICT"

        record = {
            **copy.deepcopy(payload),
            "scope_id": event["scope_id"],
            "record_event_id": event["event_id"],
            "journal_seq": event["journal_seq"],
            "parsed_proposed_action_ids": copy.deepcopy(worker["proposed_action_ids"]),
        }
        key = self._response_key(record)
        if (any(self._response_key(row) == key for row in state["responses"])
                or any(row["response_ref"] == payload["response_ref"]
                       or row["provider_request_id"] == payload["provider_request_id"]
                       or row["durability_receipt"]["transaction_id"]
                       == payload["durability_receipt"]["transaction_id"]
                       for row in state["responses"])):
            return "CALL_RESPONSE_CONFLICT"
        state["responses"].append(record)
        return "APPLIED"

    @classmethod
    def _handoff(cls, state: State, event: Event) -> State | None:
        return cls._scope(state, event)["handoffs"].get(event["payload"].get("handoff_id"))

    def _propose_handoff_result(self, state: State, event: Event) -> str:
        payload = event["payload"]
        handoff = self._handoff(state, event)
        if not handoff or handoff["status"] != "OPEN":
            return "PROPOSAL_INVALID"

        response_key = common.sha256([
            event["scope_id"], payload["handoff_id"], handoff["scenario_id"],
            handoff["condition"], "B"
        ])
        response_matches = [
            row for row in state["responses"] if self._response_key(row) == response_key
        ]
        response = response_matches[0] if len(response_matches) == 1 else None
        exact_response = (
            response
            and response["worker_handoff_hash"] == payload["worker_handoff_hash"]
            and response["task_packet_hash"] == handoff["task_packet_hash"]
            and response["served_request_hash"] == handoff["served_request_hash"]
            and response["request_parameters_hash"] == handoff["request_parameters_hash"]
            and response["route_contract_hash"] == handoff["route_contract_hash"]
            and response["parsed_proposed_action_ids"] == payload["action_ids"]
        )
        legal_actions = _actions_are_legal(
            handoff["originating_obligations"],
            handoff["action_catalog"],
            payload["action_ids"],
            handoff["originating_cut"]["valid_time"],
        )
        target_action = common.action_id(event["scope_id"], handoff["target_obligation_id"])
        if (not exact_response
                or payload["originating_cut_hash"] != handoff["originating_cut_hash"]
                or payload["action_ids"] != [target_action]
                or not legal_actions):
            return "PROPOSAL_INVALID"

        handoff.update(
            status="PROPOSED",
            proposal_event_id=event["event_id"],
            proposal_hash=common.sha384(event),
            worker_handoff_hash=payload["worker_handoff_hash"],
            action_ids=sorted(payload["action_ids"]),
        )
        return "APPLIED"

    def _commit_handoff_result(self, state: State, event: Event) -> str:
        payload = event["payload"]
        handoff = self._handoff(state, event)
        if (not handoff or handoff["status"] != "PROPOSED"
                or payload["proposal_event_id"] != handoff["proposal_event_id"]):
            return "COMMIT_INVALID"

        originally_legal = _actions_are_legal(
            handoff["originating_obligations"],
            handoff["action_catalog"],
            handoff["action_ids"],
            handoff["originating_cut"]["valid_time"],
        )
        obligations = self._obligations(state, event)
        currently_legal = _actions_are_legal(
            obligations,
            handoff["action_catalog"],
            handoff["action_ids"],
            handoff["originating_cut"]["valid_time"],
        )
        targets = {row["action_id"]: row["obligation_id"] for row in handoff["action_catalog"]
                   if row.get("obligation_id") is not None}
        targets_unchanged = all(
            obligations.get(targets[action])
            == handoff["originating_obligations"].get(targets[action])
            for action in handoff["action_ids"]
        )
        if not originally_legal or not currently_legal or not targets_unchanged:
            return "COMMIT_INVALID"

        for action in handoff["action_ids"]:
            obligations[targets[action]].update(
                lifecycle="COMPLETED", terminal_event_id=event["event_id"]
            )
        handoff.update(status="COMMITTED", terminal_disposition="COMMITTED")
        return "APPLIED"

    def _reject_handoff_result(self, state: State, event: Event) -> str:
        handoff = self._handoff(state, event)
        stored_hash = handoff.get("proposal_hash") if handoff else None
        persisted_hash = (state["events"].get(handoff.get("proposal_event_id"))
                          if handoff else None)
        if (not handoff or handoff["status"] != "PROPOSED"
                or event["payload"]["proposal_hash"] != stored_hash
                or stored_hash != persisted_hash):
            return "REJECTION_INVALID"
        handoff.update(
            status="REJECTED", terminal_disposition=event["payload"]["rejection_code"]
        )
        return "APPLIED"

    def _close_handoff(self, state: State, event: Event) -> str:
        handoff = self._handoff(state, event)
        if not handoff or handoff["status"] not in {"COMMITTED", "REJECTED"}:
            return "HANDOFF_NOT_TERMINAL"
        handoff["status"] = "CLOSED"
        return "APPLIED"


def oracle_apply(state: State, event: Event) -> tuple[State, str]:
    """Return the independently computed next state and transition result."""
    ingress_error = common.structural_error(state, event)
    if ingress_error:
        return copy.deepcopy(state), ingress_error

    replay_result = common.preflight_replay(state, event)
    if replay_result:
        return copy.deepcopy(state), replay_result

    working = copy.deepcopy(state)
    result = _OracleReducer(working).apply(event)
    if result != "APPLIED":
        return copy.deepcopy(state), result
    return common.finish_applied(working, event), result
