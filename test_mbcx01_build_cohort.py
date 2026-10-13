"""BUILD cohort slice witnesses (issue #17).

Design of record: `MBCX-01-BUILD-COHORT-CONTENT-DESIGN.md` r6 FINAL at commit
18d86d44d3a2cf28108022e626ea4bda1b430d86.

Two parts, deliberately separated:

* PART A — MOTIF CONTRACT PINS.  One method per §2.1 row (plus the two extra
  DELEGATION cells the row's REALIZATION column names).  Each pins the row's
  realization CONSTRUCTION against the FROZEN reducers directly — the exact
  result-code sequence, byte-identical dual-reducer states after every step, and
  the row's postcondition at the relevant cut.  These are GREEN today: they are
  the executable truth the generator (`mbcx01_build_cohort_generator.py`) will be
  built against, so the generator can never silently redefine a motif.  Nothing
  frozen is touched; the frozen reducers, `mbcx01_r13_common.make_event`, and
  `mbcx01_r13_packets.legal_action_ids_from_world` are used read-only.

* PART B — THE DESIGN WITNESSES (§4: W2, W6/W21, W7, W10, W11, W12, W13, W18,
  W19, W20), one per method, now DISCHARGED against the three cohort modules
  (`mbcx01_build_cohort_generator`, `mbcx01_build_cohort_authority`,
  `mbcx01_build_cohort_packet`).  Each method still imports its module INSIDE the
  test and still fails by NAME if the module or the symbol is gone.  Every witness
  is DISCRIMINATING: where the design names a red construction — a ghost FACT row,
  a journal-only mutation, a membership substitution, a stratum below its floor,
  a declared eligibility Boolean — the method EXECUTES the bad construction and
  asserts the named refusal, and where a frozen surface would accept the bad
  construction (the frozen projector copies FACT rows unchanged) the method
  asserts that acceptance too, so the BUILD check is provably the discriminator.

  The 960-candidate population is generated ONCE for the whole module by
  `build_generation()` below.  The cohort modules themselves hold NO module-global
  population (design §2: instance-scoped, no module-global caches); the cache is
  the TEST's, and `test_bw71_*` proves a second, independent generation is
  byte-identical to the first.

* PART C — THE SLICE-CLOSING WITNESSES (added 2026-08-16 by the registration task):
  W15's full four-class checklist, W16, W17, W1, W3, W5-supplement, W8 and W14.
  Every one is red-first against a deliberately broken in-memory variant.

Witness namespace: this module IS registered in `verify-build-bundle.py` as of
2026-08-16 — `BUILD_TEST_MODULES`, `BUILD_MODULES` (the three siblings),
`BUILD_WORK_PRODUCTS` (the design), `REQUIRED`/`PARITY_DOCUMENTS` (the committed
generator spec), `$buildSubjects` in `generate-build-pin-manifest.ps1`, and its own
repair-ledger rows.  Method names satisfy the governed `WITNESS_ID` regex, which the
same change WIDENED to `^test_mbcx01_build_[a-z]+\\.[A-Za-z0-9_]+\\.test_b[aiwc]\\d{2}_`
(the reason is recorded beside the regex).  Number allocation, because the two-digit
field is a hard ceiling:

  PART A uses the only globally-unused `bw` numbers — bw23, bw64 (gaps in
  `test_mbcx01_build_measurement.py`) and bw94–bw99 (above the highest existing,
  bw93).  PART B uses bw70–bw79, which are module-qualified reuses: the WITNESS_ID
  is `<module>.<class>.<method>`, and the bundle already reuses bw80–bw84 across
  `test_mbcx01_build_measurement.py` and `test_mbcx01_build_integration.py`.  PART C
  uses the FRESH `bc` namespace from bc01, which is what the prefix widening bought:
  no Part-A or Part-B method is renumbered, and no future cohort witness has to be a
  reuse.
"""

from __future__ import annotations

import ast
import copy
import importlib
import importlib.util
import inspect
import json
import shutil
import tempfile
import textwrap
import unittest
from pathlib import Path

import mbcx01_r13_common as common
import mbcx01_r13_inference as inference
import mbcx01_r13_measurement as measurement
import mbcx01_r13_packets as packets
import mbcx01_r13_state_oracle as oracle
import mbcx01_r13_state_reference as reference


#: A cut strictly later than the frozen `T1`, used for the "later cut" halves.
T2 = "2026-08-14T00:00:00.000000Z"

SCORED_SCOPE = "SCOPE.SHARED"
FOREIGN_SCOPE = "SCOPE.FOREIGN"

#: The ONE generated population for this module.  Held HERE, never in the cohort
#: modules (design §2: instance-scoped, no module-global caches).
_GENERATION = None


def build_generation():
    """Generate the BUILD cohort once for the whole test module."""
    global _GENERATION
    if _GENERATION is None:
        generator = importlib.import_module("mbcx01_build_cohort_generator")
        _GENERATION = generator.generate_cohort()
    return _GENERATION


def chosen_cut_of(candidate: dict) -> str:
    """The cut the frozen `choose_one_cut` picks for this candidate, recomputed."""
    authority = importlib.import_module("mbcx01_build_cohort_authority")
    return authority.choose_one_cut(candidate["scenario_id"], candidate["cut_ids"],
                                    authority.BUILD_ONE_CUT_DOMAIN)


def _unpack(result: object) -> tuple[dict, str]:
    """Unpack a reducer return defensively: the dict is the state, the str the code."""
    if isinstance(result, tuple):
        state = next((item for item in result if isinstance(item, dict)), None)
        code = next((item for item in result if isinstance(item, str)), None)
        return state, code
    raise AssertionError("reducer did not return a tuple: %r" % (type(result),))


class BuildCohortMotifContractTests(unittest.TestCase):
    """PART A — the §2.1 motif contracts, executed against the frozen reducers."""

    def setUp(self) -> None:
        self.ref_state = common.initial_state()
        self.orc_state = common.initial_state()
        self.codes: list[str] = []

    # ---- shared machinery -------------------------------------------------

    def apply_both(self, event: dict, expected: str) -> str:
        """Apply one event through BOTH frozen reducers and pin code + byte equality."""
        ref_new, ref_code = _unpack(
            reference.reference_apply(copy.deepcopy(self.ref_state), copy.deepcopy(event)))
        orc_new, orc_code = _unpack(
            oracle.oracle_apply(copy.deepcopy(self.orc_state), copy.deepcopy(event)))
        self.assertEqual(ref_code, expected, "reference result for %s" % event["event_type"])
        self.assertEqual(orc_code, expected, "oracle result for %s" % event["event_type"])
        self.assertEqual(common.canonical_json(ref_new), common.canonical_json(orc_new),
                         "dual-reducer states diverged after %s" % event["event_type"])
        self.ref_state, self.orc_state = ref_new, orc_new
        self.codes.append(ref_code)
        return ref_code

    def scored_world(self, scope_id: str = SCORED_SCOPE) -> list[dict]:
        """Project OBLIGATION world rows for one scope, in canonical world shape."""
        scope = self.ref_state["scopes"][scope_id]
        rows = [{"object_id": oid, "object_kind": "OBLIGATION",
                 "fields": {key: copy.deepcopy(obligation[key]) for key in (
                     "subject_id", "owner_role", "lifecycle", "critical", "due_at",
                     "completion_action_id", "prerequisite_obligation_ids")},
                 "source_event_ids": []}
                for oid, obligation in scope["obligations"].items()]
        rows.sort(key=lambda row: row["object_id"].encode("utf-8"))
        return rows

    @staticmethod
    def catalog_for(scope_id: str, obligation_ids: list[str]) -> list[dict]:
        rows = [{"action_id": common.action_id(scope_id, oid),
                 "action_kind": "ACT_ON_OBLIGATION",
                 "scope_id": scope_id, "obligation_id": oid} for oid in obligation_ids]
        rows.append({"action_id": "NO_ACTION", "action_kind": "NO_ACTION"})
        rows.sort(key=lambda row: row["action_id"].encode("utf-8"))
        return rows

    def visible_fact_rows(self, subject: str, predicate: str, valid_time: str) -> list[dict]:
        cut = common.current_cut(self.ref_state, valid_time=valid_time)
        rows = self.ref_state["scopes"][SCORED_SCOPE]["facts"].get(
            common.fact_key(subject, predicate), [])
        return [row for row in rows if reference.visible_effective(row, cut)]

    def open_obligation(self, obligation_id: str, *, due_at: str, critical: bool = True,
                        subject_id: str = "SUB.COHORT", owner_role: str = "WORKER",
                        prerequisites: list[str] | None = None,
                        scope_id: str = SCORED_SCOPE, valid_time: str | None = None) -> dict:
        """Open one obligation, optionally at an explicit cut valid_time."""
        cut = (common.current_cut(self.ref_state, valid_time=valid_time)
               if valid_time is not None else None)
        return common.make_event("open_obligation", {
            "obligation_id": obligation_id, "subject_id": subject_id,
            "owner_role": owner_role, "due_at": due_at, "critical": critical,
            "completion_action_id": common.action_id(scope_id, obligation_id),
            "prerequisite_obligation_ids": list(prerequisites or [])},
            state=self.ref_state, scope_id=scope_id,
            valid_from=common.T0 if valid_time is None else valid_time,
            originating_cut=cut)

    def complete_obligation(self, obligation_id: str, scope_id: str = SCORED_SCOPE) -> dict:
        cut = common.current_cut(self.ref_state)
        return common.make_event("complete_obligation", {
            "obligation_id": obligation_id,
            "completion_action_id": common.action_id(scope_id, obligation_id),
            "originating_cut_hash": common.cut_hash(cut)},
            state=self.ref_state, scope_id=scope_id, originating_cut=cut)

    def open_handoff_chain(self) -> tuple[dict, dict, dict]:
        """open_handoff -> record_call_response -> propose, all `APPLIED`."""
        payload = reference.handoff_fixture_payload()
        self.apply_both(common.make_event("open_handoff", payload, state=self.ref_state),
                        "APPLIED")
        response = reference.response_fixture_payload(payload)
        self.apply_both(common.make_event("record_call_response", response,
                                          state=self.ref_state), "APPLIED")
        proposal = common.make_event("propose_handoff_result", {
            "handoff_id": payload["handoff_id"],
            "worker_handoff_hash": response["worker_handoff_hash"],
            "originating_cut_hash": payload["originating_cut_hash"],
            "action_ids": [payload["action_catalog"][0]["action_id"]]}, state=self.ref_state)
        self.apply_both(proposal, "APPLIED")
        return payload, response, proposal

    def handoff_row(self, handoff_id: str) -> dict:
        return self.ref_state["scopes"][SCORED_SCOPE]["handoffs"][handoff_id]

    # ---- §2.1 row 1: CORRECTION_RESTORATION -------------------------------

    def test_bw94_positive_correction_restoration_reasserts_a_prior_value_at_a_later_cut(self):
        """§2.1 CORRECTION_RESTORATION: assert -> correct -> retract(correction) -> REASSERT,
        all `APPLIED`; the retraction alone leaves NOTHING visible at the later cut and the
        reassert makes the prior `value_code` visible again there."""
        assertion = common.make_event("assert_fact", {
            "subject_id": "SUB.CR", "predicate_id": "PRED.CR", "value_code": "VALUE.ONE"},
            state=self.ref_state)
        self.apply_both(assertion, "APPLIED")

        correction = common.make_event("correct_fact", {
            "subject_id": "SUB.CR", "predicate_id": "PRED.CR",
            "parent_event_id": assertion["event_id"], "value_code": "VALUE.TWO"},
            state=self.ref_state, valid_from=common.T1)
        self.apply_both(correction, "APPLIED")
        self.assertEqual([row["value_code"] for row in
                          self.visible_fact_rows("SUB.CR", "PRED.CR", common.T1)],
                         ["VALUE.TWO"], "the correction must be the visible head at T1")

        retraction = common.make_event("retract_fact", {
            "subject_id": "SUB.CR", "predicate_id": "PRED.CR",
            "target_event_id": correction["event_id"]},
            state=self.ref_state, valid_from=common.T1)
        self.apply_both(retraction, "APPLIED")

        # NEGATIVE PIN: retracting the correction restores NOTHING by itself — the
        # parent's closure survives its child's retraction (§2.6's ordering effect).
        self.assertEqual(self.visible_fact_rows("SUB.CR", "PRED.CR", common.T1), [],
                         "retract alone must leave nothing visible at the later cut")

        reassert = common.make_event("assert_fact", {
            "subject_id": "SUB.CR", "predicate_id": "PRED.CR", "value_code": "VALUE.ONE"},
            state=self.ref_state, valid_from=common.T1)
        self.apply_both(reassert, "APPLIED")

        restored = self.visible_fact_rows("SUB.CR", "PRED.CR", common.T1)
        self.assertEqual([row["value_code"] for row in restored], ["VALUE.ONE"])
        self.assertEqual([row["event_id"] for row in restored], [reassert["event_id"]],
                         "the visible row at the later cut must be the REASSERTED row")
        self.assertEqual([row["value_code"] for row in
                          self.visible_fact_rows("SUB.CR", "PRED.CR", T2)], ["VALUE.ONE"])
        self.assertEqual(self.codes, ["APPLIED"] * 4)

    # ---- §2.1 row 2: OBLIGATION_LIFECYCLE ---------------------------------

    def test_bw95_positive_obligation_lifecycle_transitions_are_observed_off_the_target(self):
        """§2.1 OBLIGATION_LIFECYCLE: open -> reschedule -> {complete | cancel} -> reopen on
        NON-target obligations, every code `APPLIED`, with the lifecycle sequence observed in
        the projected world across the cuts."""
        observed: dict[str, list[str]] = {}
        for obligation_id, terminal in (("OBL.LIFECYCLE.A", "complete_obligation"),
                                        ("OBL.LIFECYCLE.B", "cancel_obligation")):
            self.assertNotIn(obligation_id, ("OBL.SHARED",), "must not touch the scored target")
            trace: list[str] = []
            self.apply_both(self.open_obligation(obligation_id, due_at=common.T1), "APPLIED")
            trace.append(self.lifecycle_of(obligation_id))

            self.apply_both(common.make_event("reschedule_obligation", {
                "obligation_id": obligation_id, "due_at": common.T0},
                state=self.ref_state), "APPLIED")
            self.assertEqual(
                self.ref_state["scopes"][SCORED_SCOPE]["obligations"][obligation_id]["due_at"],
                common.T0, "reschedule must be observable in the projected world")
            trace.append(self.lifecycle_of(obligation_id))

            if terminal == "complete_obligation":
                self.apply_both(self.complete_obligation(obligation_id), "APPLIED")
            else:
                self.apply_both(common.make_event("cancel_obligation", {
                    "obligation_id": obligation_id, "cancellation_code": "OWNER_CANCELLED"},
                    state=self.ref_state), "APPLIED")
            trace.append(self.lifecycle_of(obligation_id))

            self.apply_both(common.make_event("reopen_obligation", {
                "obligation_id": obligation_id, "due_at": common.T1,
                "owner_role": "WORKER.REOPENED"}, state=self.ref_state), "APPLIED")
            trace.append(self.lifecycle_of(obligation_id))
            observed[obligation_id] = trace

        self.assertEqual(observed["OBL.LIFECYCLE.A"], ["OPEN", "OPEN", "COMPLETED", "OPEN"])
        self.assertEqual(observed["OBL.LIFECYCLE.B"], ["OPEN", "OPEN", "CANCELLED", "OPEN"])
        self.assertEqual(
            self.ref_state["scopes"][SCORED_SCOPE]["obligations"]["OBL.SHARED"]["lifecycle"],
            "OPEN", "§2.4: the scored target is never reopened inside the scored window")
        self.assertEqual(self.codes, ["APPLIED"] * 8)

    def lifecycle_of(self, obligation_id: str, scope_id: str = SCORED_SCOPE) -> str:
        return self.ref_state["scopes"][scope_id]["obligations"][obligation_id]["lifecycle"]

    # ---- §2.1 row 3: DEPENDENCY_REVERSAL ----------------------------------

    def test_bw96_positive_dependency_reversal_flips_the_target_on_prerequisite_order(self):
        """§2.1 DEPENDENCY_REVERSAL: link (`APPLIED`) makes the target ILLEGAL and completing
        the prerequisite (`APPLIED`) makes it LEGAL — the target absent from
        `legal_action_ids_from_world` while blocked and present after completion."""
        catalog = self.catalog_for(SCORED_SCOPE, ["OBL.SHARED", "OBL.PREREQ"])
        target_action = common.action_id(SCORED_SCOPE, "OBL.SHARED")

        legal_before = packets.legal_action_ids_from_world(
            self.scored_world(), catalog, common.current_cut(self.ref_state))
        self.assertIn(target_action, legal_before, "the target starts legal (no prerequisite)")

        self.apply_both(common.make_event("link_dependency", {
            "obligation_id": "OBL.SHARED", "prerequisite_obligation_id": "OBL.PREREQ"},
            state=self.ref_state), "APPLIED")
        legal_blocked = packets.legal_action_ids_from_world(
            self.scored_world(), catalog, common.current_cut(self.ref_state))
        self.assertNotIn(target_action, legal_blocked,
                         "the target must be BLOCKED while its prerequisite is open")

        self.apply_both(self.complete_obligation("OBL.PREREQ"), "APPLIED")
        legal_after = packets.legal_action_ids_from_world(
            self.scored_world(), catalog, common.current_cut(self.ref_state))
        self.assertIn(target_action, legal_after,
                      "the target must be DUE once the prerequisite completes")
        self.assertEqual(self.lifecycle_of("OBL.PREREQ"), "COMPLETED")
        self.assertEqual(self.codes, ["APPLIED", "APPLIED"])

    # ---- §2.1 row 4: CROSS_SCOPE_COLLISION --------------------------------

    def test_bw97_positive_cross_scope_collision_keeps_the_scored_projection_zero_foreign(self):
        """§2.1 CROSS_SCOPE_COLLISION: foreign-scope events `APPLIED` on a genuinely
        multi-scope journal, while the scored scope's projection carries ZERO foreign-scope
        objects (subject/name collision pressure held in scope)."""
        self.apply_both(self.open_obligation(
            "OBL.COLLIDE", due_at=common.T0, subject_id="SUB.SHARED"), "APPLIED")
        self.apply_both(self.open_obligation(
            "OBL.COLLIDE", due_at=common.T0, subject_id="SUB.SHARED",
            scope_id=FOREIGN_SCOPE), "APPLIED")
        self.apply_both(common.make_event("assert_fact", {
            "subject_id": "SUB.SHARED", "predicate_id": "PRED.COLLIDE",
            "value_code": "VALUE.FOREIGN"}, state=self.ref_state,
            scope_id=FOREIGN_SCOPE), "APPLIED")

        # The journal is genuinely multi-scope and the collision pressure is real.
        self.assertEqual(sorted(self.ref_state["scopes"]), [FOREIGN_SCOPE, SCORED_SCOPE])
        self.assertIn("OBL.COLLIDE", self.ref_state["scopes"][FOREIGN_SCOPE]["obligations"])
        self.assertIn("OBL.COLLIDE", self.ref_state["scopes"][SCORED_SCOPE]["obligations"])
        self.assertEqual(len(self.ref_state["scopes"][FOREIGN_SCOPE]["facts"]), 1)

        scored = self.scored_world()
        foreign_action_ids = {
            common.action_id(FOREIGN_SCOPE, oid)
            for oid in self.ref_state["scopes"][FOREIGN_SCOPE]["obligations"]}
        scored_action_ids = {row["fields"]["completion_action_id"] for row in scored}
        self.assertEqual(scored_action_ids & foreign_action_ids, set(),
                         "zero foreign-scope objects may reach the scored projection")
        for row in scored:
            self.assertEqual(row["fields"]["completion_action_id"],
                             common.action_id(SCORED_SCOPE, row["object_id"]))
        self.assertEqual(self.ref_state["scopes"][SCORED_SCOPE]["facts"], {},
                         "the foreign-scope FACT must not appear in the scored scope")
        self.assertEqual(self.codes, ["APPLIED"] * 3)

    # ---- §2.1 row 5: DELEGATION_IDEMPOTENT_HANDOFF ------------------------

    def test_bw98_positive_delegation_duplicates_are_byte_identical_replay_noops(self):
        """§2.1 DELEGATION_IDEMPOTENT_HANDOFF: owner-role rewrite visible, `record_call_response`
        carried, and duplicate proposal AND duplicate commit constructed as BYTE-IDENTICAL EVENT
        REPLAY return `DUPLICATE_NOOP` exactly, leaving state byte-unchanged."""
        payload = reference.handoff_fixture_payload()
        self.apply_both(common.make_event("open_handoff", payload, state=self.ref_state),
                        "APPLIED")

        # Owner-role rewrite, off the handoff target so the commit's unchanged-target
        # recheck still sees its originating obligations.
        self.apply_both(common.make_event("delegate_obligation", {
            "obligation_id": "OBL.PREREQ", "owner_role": "WORKER.DELEGATE"},
            state=self.ref_state), "APPLIED")
        self.assertEqual(
            self.ref_state["scopes"][SCORED_SCOPE]["obligations"]["OBL.PREREQ"]["owner_role"],
            "WORKER.DELEGATE", "the owner-role rewrite must be visible in state")

        response = reference.response_fixture_payload(payload)
        self.apply_both(common.make_event("record_call_response", response,
                                          state=self.ref_state), "APPLIED")
        self.assertEqual(len(self.ref_state["responses"]), 1, "the B-call must be recorded")

        proposal = common.make_event("propose_handoff_result", {
            "handoff_id": payload["handoff_id"],
            "worker_handoff_hash": response["worker_handoff_hash"],
            "originating_cut_hash": payload["originating_cut_hash"],
            "action_ids": [payload["action_catalog"][0]["action_id"]]}, state=self.ref_state)
        self.apply_both(proposal, "APPLIED")
        self.assertEqual(self.handoff_row(payload["handoff_id"])["status"], "PROPOSED")

        before_replay = common.canonical_json(self.ref_state)
        self.apply_both(copy.deepcopy(proposal), "DUPLICATE_NOOP")
        self.assertEqual(common.canonical_json(self.ref_state), before_replay)

        commit = common.make_event("commit_handoff_result", {
            "handoff_id": payload["handoff_id"], "proposal_event_id": proposal["event_id"]},
            state=self.ref_state)
        self.apply_both(commit, "APPLIED")
        committed = self.handoff_row(payload["handoff_id"])
        self.assertEqual(committed["status"], "COMMITTED")
        self.assertEqual(committed["terminal_disposition"], "COMMITTED",
                         "commit alone writes its literal disposition")
        self.assertEqual(self.lifecycle_of("OBL.SHARED"), "COMPLETED")

        after_commit = common.canonical_json(self.ref_state)
        self.apply_both(copy.deepcopy(commit), "DUPLICATE_NOOP")
        self.assertEqual(common.canonical_json(self.ref_state), after_commit)

        self.assertEqual(self.codes, ["APPLIED", "APPLIED", "APPLIED", "APPLIED",
                                      "DUPLICATE_NOOP", "APPLIED", "DUPLICATE_NOOP"])

    def test_bw23_negative_delegation_fresh_duplicates_are_not_duplicate_noop(self):
        """§2.1 DELEGATION_IDEMPOTENT_HANDOFF negative matrix: a FRESH duplicate propose is
        `PROPOSAL_INVALID`, a FRESH duplicate commit is `COMMIT_INVALID`, and a FRESH event
        reusing a spent idempotency key is `IDEMPOTENCY_CONFLICT` — three distinct facts that
        `DUPLICATE_NOOP` must never absorb, all four leaving state byte-unchanged."""
        payload, response, proposal = self.open_handoff_chain()
        proposed_state = common.canonical_json(self.ref_state)

        fresh_proposal = common.make_event("propose_handoff_result", {
            "handoff_id": payload["handoff_id"],
            "worker_handoff_hash": response["worker_handoff_hash"],
            "originating_cut_hash": payload["originating_cut_hash"],
            "action_ids": [payload["action_catalog"][0]["action_id"]]}, state=self.ref_state)
        self.assertNotEqual(fresh_proposal["event_id"], proposal["event_id"])
        self.assertNotEqual(fresh_proposal["idempotency_key"], proposal["idempotency_key"])
        self.apply_both(fresh_proposal, "PROPOSAL_INVALID")
        self.assertEqual(common.canonical_json(self.ref_state), proposed_state)

        reused_key = common.make_event("propose_handoff_result", {
            "handoff_id": payload["handoff_id"], "worker_handoff_hash": "A" * 96,
            "originating_cut_hash": payload["originating_cut_hash"],
            "action_ids": [payload["action_catalog"][0]["action_id"]]},
            state=self.ref_state, idempotency_key=proposal["idempotency_key"])
        self.assertNotEqual(reused_key["event_id"], proposal["event_id"])
        self.apply_both(reused_key, "IDEMPOTENCY_CONFLICT")
        self.assertEqual(common.canonical_json(self.ref_state), proposed_state)

        commit = common.make_event("commit_handoff_result", {
            "handoff_id": payload["handoff_id"], "proposal_event_id": proposal["event_id"]},
            state=self.ref_state)
        self.apply_both(commit, "APPLIED")
        committed_state = common.canonical_json(self.ref_state)

        fresh_commit = common.make_event("commit_handoff_result", {
            "handoff_id": payload["handoff_id"], "proposal_event_id": proposal["event_id"]},
            state=self.ref_state)
        self.assertNotEqual(fresh_commit["event_id"], commit["event_id"])
        self.apply_both(fresh_commit, "COMMIT_INVALID")
        self.assertEqual(common.canonical_json(self.ref_state), committed_state)

        self.assertEqual(self.codes, ["APPLIED", "APPLIED", "APPLIED", "PROPOSAL_INVALID",
                                      "IDEMPOTENCY_CONFLICT", "APPLIED", "COMMIT_INVALID"])

    def test_bw64_positive_delegation_rejection_is_applied_rejected_and_carries_its_code(self):
        """§2.1 DELEGATION_IDEMPOTENT_HANDOFF rejection realization: the TRIPLE — result code
        `APPLIED`, handoff status `REJECTED`, `terminal_disposition` == the payload's
        `rejection_code` (never result code "REJECTED"), asymmetric with commit's literal."""
        payload, _response, proposal = self.open_handoff_chain()
        rejection = common.make_event("reject_handoff_result", {
            "handoff_id": payload["handoff_id"], "rejection_code": "TRANSITION_ILLEGAL",
            "proposal_hash": common.sha384(proposal)}, state=self.ref_state)
        code = self.apply_both(rejection, "APPLIED")

        handoff = self.handoff_row(payload["handoff_id"])
        self.assertEqual(code, "APPLIED")
        self.assertNotEqual(code, "REJECTED",
                            "'REJECTED' is a handoff STATUS, never a reducer result code")
        self.assertEqual(handoff["status"], "REJECTED")
        self.assertEqual(handoff["terminal_disposition"],
                         rejection["payload"]["rejection_code"])
        self.assertNotEqual(handoff["terminal_disposition"], "COMMITTED",
                            "the commit/reject asymmetry is deliberate")
        self.assertEqual(self.lifecycle_of("OBL.SHARED"), "OPEN",
                         "a rejection completes no obligation")
        self.assertEqual(self.codes, ["APPLIED"] * 4)

    # ---- §2.1 row 6: MIXED_DELAYED_CONTINUITY -----------------------------

    def test_bw99_positive_mixed_delayed_continuity_flips_target_legality_across_cuts(self):
        """§2.1 MIXED_DELAYED_CONTINUITY: the target opened at an early cut with
        `due_at` = the chosen cut's `valid_time` (so `due_at > valid_time` there) is NOT in the
        legal set at the earlier cuts and is UNIQUELY legal at the chosen cut, with no
        reschedule of the target and every code `APPLIED`."""
        self.apply_both(self.open_obligation(
            "OBL.TARGET", due_at=common.T1, subject_id="SUB.TARGET",
            valid_time=common.T0), "APPLIED")
        self.apply_both(self.open_obligation(
            "OBL.DECOY", due_at=common.T0, critical=False, subject_id="SUB.DECOY",
            valid_time=common.T0), "APPLIED")

        catalog = self.catalog_for(SCORED_SCOPE, ["OBL.TARGET", "OBL.DECOY"])
        target_action = common.action_id(SCORED_SCOPE, "OBL.TARGET")

        def legal_at(valid_time: str) -> list[str]:
            return packets.legal_action_ids_from_world(
                self.scored_world(), catalog,
                common.current_cut(self.ref_state, valid_time=valid_time))

        self.assertEqual(legal_at(common.T0), [],
                         "target due_at > valid_time at the earlier cut ⇒ not legal")
        self.assertEqual(legal_at(common.T1), [target_action],
                         "at the chosen cut the target is UNIQUELY legal")
        self.assertEqual(legal_at(T2), [target_action])
        self.assertEqual(
            self.ref_state["scopes"][SCORED_SCOPE]["obligations"]["OBL.TARGET"]["due_at"],
            common.T1, "the target is never rescheduled after its open")
        self.assertEqual(self.codes, ["APPLIED", "APPLIED"])


class BuildCohortRedSkeletonTests(unittest.TestCase):
    """PART B — one honest red per design witness the cohort modules will own."""

    def require_modules(self, witness: str, section: str, green: str,
                        *module_names: str) -> tuple:
        """Import the named cohort modules or FAIL naming the module and the witness."""
        loaded = []
        for name in module_names:
            try:
                loaded.append(importlib.import_module(name))
            except ModuleNotFoundError as error:
                self.fail("RED %s (design %s): module '%s' does not exist yet — %s. "
                          "GREEN will mean: %s." % (witness, section, name, error, green))
        return tuple(loaded)

    def require_symbols(self, witness: str, module, *names: str) -> None:
        missing = [name for name in names if not hasattr(module, name)]
        if missing:
            self.fail("RED %s: %s exists but does not own %s."
                      % (witness, module.__name__, ", ".join(missing)))

    def test_bw70_red_w2_declared_eligibility_boolean_is_refused_by_name(self):
        """§2.3/§4 W2: green = the cohort authority POPS a supplied eligibility Boolean and
        refuses it by name with `DECLARED_ELIGIBILITY_BOOLEAN` instead of reading it back."""
        authority, packet = self.require_modules(
            "W2 declared-Boolean refusal", "§2.3 / §4 W2",
            "a supplied eligibility Boolean is refused by name, never read back",
            "mbcx01_build_cohort_authority", "mbcx01_build_cohort_packet")
        self.require_symbols("W2 declared-Boolean refusal", authority,
                             "DECLARED_ELIGIBILITY_BOOLEAN", "pop_declared_eligibility",
                             "select_build_cohort")
        generation = build_generation()

        # The victim is a candidate the DERIVED predicate refuses.  Declaring it
        # eligible is exactly the frozen move (`mbcx01_r13_measurement.py:252`
        # writes the Boolean, `:321` reads it back under a `RECOMPUTED` label).
        victim = next(row for row in generation.candidates
                      if not packet.candidate_is_eligible(row, chosen_cut_of(row)))
        forged = copy.deepcopy(generation.candidates)
        position = [row["scenario_id"] for row in forged].index(victim["scenario_id"])
        forged[position]["eligible"] = True
        forged[position]["eligibility_source"] = "RECOMPUTED"

        popped, refusals = authority.pop_declared_eligibility(forged)
        self.assertEqual(refusals, [authority.DECLARED_ELIGIBILITY_BOOLEAN])
        self.assertNotIn("eligible", popped[position],
                         "the declared Boolean must be POPPED, not carried")
        self.assertNotIn("eligibility_source", popped[position])
        self.assertIn(authority.DECLARED_ELIGIBILITY_BOOLEAN,
                      authority.validate_build_source_provenance(
                          forged, generation.provenance))
        with self.assertRaises(authority.BuildCohortAuthorityError) as refusal:
            authority.select_build_cohort(forged, generation.provenance,
                                          packet.ELIGIBILITY_PREDICATE)
        self.assertIn(authority.DECLARED_ELIGIBILITY_BOOLEAN, str(refusal.exception))

        # DISCRIMINATING half: the Boolean is not merely refused, it is never
        # consulted — the popped row is still ineligible by DERIVATION, and the
        # honest retained set does not contain it.
        self.assertFalse(packet.candidate_is_eligible(
            popped[position], chosen_cut_of(popped[position])))
        self.assertNotIn(victim["scenario_id"],
                         authority.retained_membership_scenario_ids(generation.context))

    def test_bw71_red_w6_determinism_and_the_ghost_fact_discriminator(self):
        """§2.2/§4 W6+W21: green = byte-identical re-generation, post-generation mutation
        failing authority re-derivation, and a FACT row without journal ancestry REFUSED by the
        BUILD packet sibling (generic projection equality is not that discriminator)."""
        generator, packet, authority = self.require_modules(
            "W6 determinism + W21 ghost-FACT", "§2.2 / §4 W6+W21",
            "re-runs are byte-identical and a journal-less FACT row is refused",
            "mbcx01_build_cohort_generator", "mbcx01_build_cohort_packet",
            "mbcx01_build_cohort_authority")
        self.require_symbols("W6 determinism", generator, "generate_cohort")
        self.require_symbols("W21 ghost-FACT", packet, "validate_build_manifest")
        first = build_generation()

        # --- W6: a SECOND, independent generation is byte-identical -----------
        second = generator.generate_cohort()
        self.assertEqual(
            common.canonical_json(first.candidates),
            common.canonical_json(second.candidates),
            "the 960-candidate population must be byte-identical across runs")
        self.assertEqual(first.provenance, second.provenance)
        self.assertEqual(first.retained_set_root(), second.retained_set_root())
        self.assertEqual(common.canonical_json(first.census),
                         common.canonical_json(second.census))
        self.assertEqual(common.canonical_json(first.coverage),
                         common.canonical_json(second.coverage))

        context = first.context
        candidate = context.retained_candidates[0]
        cut_id = candidate["chosen_cut_id"]
        manifest = packet.served_manifest_for_retained_candidate(context, candidate)
        self.assertEqual(packet.validate_build_manifest(
            manifest, candidate, cut_id, context=context), [])

        # --- W21: a FACT row with NO journal ancestry -------------------------
        ghost = copy.deepcopy(manifest)
        ghost["canonical_world"].append({
            "object_id": "FACT.SUB.GHOST.PRED.GHOST", "object_kind": "FACT",
            "fields": {"subject_id": "SUB.GHOST", "predicate_id": "PRED.GHOST",
                       "value_code": "VALUE.GHOST", "valid_from": common.T0,
                       "valid_to": None},
            "source_event_ids": ["EV." + "0" * 64]})
        ghost["canonical_world"].sort(key=lambda row: row["object_id"].encode("utf-8"))
        ghost["canonical_world_hash"] = packets.sha384(ghost["canonical_world"])
        ghost["manifest_hash"] = packets.hash_without(ghost, "manifest_hash")
        state = packet.authoritative_state_for_cut(candidate, cut_id)

        # The frozen surfaces ACCEPT the ghost: `validate_expected_manifest` sees a
        # well-formed row, and `project_state_world` COPIES non-obligation rows
        # unchanged (`mbcx01_r13_packets.py:81-93`) so projection equality still
        # holds.  Generic projection equality is therefore NOT the discriminator.
        self.assertEqual(packets.validate_expected_manifest(ghost), [])
        self.assertEqual(packets.project_state_world(state, ghost),
                         ghost["canonical_world"])
        self.assertEqual(
            packet.validate_build_manifest(ghost, candidate, cut_id, context=context),
            [packet.BUILD_FACT_ROW_WITHOUT_JOURNAL_ANCESTRY])

        # --- W6: post-generation MUTATION of a real FACT row ------------------
        mutated = copy.deepcopy(manifest)
        fact_rows = [row for row in mutated["canonical_world"]
                     if row["object_kind"] == "FACT"]
        self.assertTrue(fact_rows, "the retained candidate must carry a FACT row")
        fact_rows[0]["fields"]["value_code"] = "VALUE.MUTATED"
        mutated["canonical_world_hash"] = packets.sha384(mutated["canonical_world"])
        mutated["manifest_hash"] = packets.hash_without(mutated, "manifest_hash")
        self.assertEqual(packets.validate_expected_manifest(mutated), [])
        self.assertEqual(
            packet.validate_build_manifest(mutated, candidate, cut_id, context=context),
            [packet.BUILD_FACT_ROW_WITHOUT_JOURNAL_ANCESTRY])

        # --- W6: post-generation mutation fails AUTHORITY re-derivation -------
        tampered = copy.deepcopy(candidate)
        tampered["canonical_world_by_cut"][cut_id] = ghost["canonical_world"]
        with self.assertRaises(authority.BuildCohortAuthorityError) as refusal:
            authority.retained_scenario_authority(context, tampered)
        self.assertIn(authority.BUILD_RETAINED_SCENARIO_AUTHORITY_INVALID,
                      str(refusal.exception))

    def test_bw72_red_w7_the_build_population_joins_the_build_authority_path(self):
        """§3/§4 W7: green = 768 candidates, 6x128 per motif, retained positions, retained root
        and provenance all join through the BUILD cohort authority."""
        authority, packet = self.require_modules(
            "W7 authority join", "§3 / §4 W7",
            "the BUILD population joins the BUILD authority path at 768 / 6x128 / root",
            "mbcx01_build_cohort_authority", "mbcx01_build_cohort_packet")
        self.require_symbols("W7 authority join", authority, "retained_set_root",
                             "retained_cohort_authority", "retained_scenario_authority")
        generation = build_generation()
        context = generation.context
        retained = context.retained_candidates

        self.assertEqual(len(generation.candidates), 960)
        self.assertEqual(len(retained), 768)
        self.assertEqual(
            {motif: sum(1 for row in retained if row["motif"] == motif)
             for motif in authority.MOTIFS},
            {motif: 128 for motif in authority.MOTIFS})
        self.assertEqual(authority.validate_build_source_provenance(
            generation.candidates, generation.provenance), [])

        cohort = authority.retained_cohort_authority(context)
        self.assertEqual(authority.validate_retained_cohort_authority(context, cohort), [])
        self.assertEqual(cohort["retained_total"], 768)
        self.assertEqual(cohort["generator_id"], authority.BUILD_GENERATOR_ID)
        self.assertEqual(cohort["retained_set_root"],
                         packets.sha384(cohort["retained_candidate_hashes"]))
        self.assertEqual(cohort["retained_set_root"], authority.retained_set_root(context))
        self.assertNotEqual(cohort["retained_set_root"],
                            measurement.retained_cohort_authority_r13()["retained_set_root"],
                            "the BUILD population must own its OWN retained root")

        positions = []
        for candidate in retained:
            scenario_authority = authority.retained_scenario_authority(context, candidate)
            self.assertEqual(authority.validate_retained_scenario_authority(
                context, scenario_authority), [])
            self.assertEqual(scenario_authority["retained_set_root"],
                             cohort["retained_set_root"])
            positions.append(scenario_authority["retained_position"])
        self.assertEqual(positions, list(range(768)))
        self.assertEqual(sorted(set(cohort["retained_scenario_ids"])),
                         sorted(cohort["retained_scenario_ids"]))

        # The join reaches the SERVED manifest: position and root ride it, and the
        # frozen manifest validator's `0 <= retained_position < 768` holds at both
        # frozen sites (`packets.py:222` and `measurement.py:1501`).
        sample = retained[0], retained[400], retained[767]
        for candidate in sample:
            manifest = packet.served_manifest_for_retained_candidate(context, candidate)
            self.assertEqual(packets.validate_expected_manifest(manifest), [])
            self.assertEqual(manifest["retained_set_root"], cohort["retained_set_root"])
            self.assertEqual(manifest["retained_position"],
                             context.retained_position(candidate["scenario_id"]))
            self.assertEqual(manifest["source_provenance_hash"],
                             generation.provenance["provenance_hash"])

        # A candidate that is NOT a byte-exact member is refused, by name.
        stranger = copy.deepcopy(retained[0])
        stranger["scenario_id"] = "SCENARIO.BUILD.PHANTOM"
        with self.assertRaises(authority.BuildCohortAuthorityError):
            authority.retained_scenario_authority(context, stranger)

    def test_bw73_red_w10_the_structural_half_of_the_falsification_sentinel(self):
        """§4 W10: green = gold read-sets take at least the declared number of distinct values,
        the BC/OM difference is non-degenerate, and OM-only evidence is NECESSARY for canonical
        gold derivation under the registered counterfactual (structural half only)."""
        packet, = self.require_modules(
            "W10 sentinel (structural half)", "§4 W10",
            "read-set variety, a non-degenerate BC/OM difference, and a necessary OM-only class",
            "mbcx01_build_cohort_packet")
        self.require_symbols("W10 sentinel (structural half)", packet,
                             "gold_read_set_census", "bc_om_difference",
                             "om_only_necessity_witness")
        generation = build_generation()
        context = generation.context
        retained = context.retained_candidates
        manifests = [packet.served_manifest_for_retained_candidate(context, row)
                     for row in retained]

        census = packet.gold_read_set_census(manifests)
        self.assertEqual(census["errors"], [])
        self.assertEqual(census["population"], 768)
        self.assertGreaterEqual(census["distinct_gold_read_sets"],
                                packet.DECLARED_MIN_DISTINCT_GOLD_READ_SETS)
        self.assertEqual(census["degenerate_bc_om_scenarios"], [])
        self.assertEqual(census["om_only_necessity_in_class"], 768)
        self.assertEqual(census["om_only_necessity_failures"], [])
        self.assertGreater(len(census["distinct_gold_read_set_sizes"]), 1,
                           "the measured quantity may not ride an unvaried read set")

        # The BC/OM difference is non-degenerate at BOTH levels — the read-set
        # SELECTION and the SERVED closure.
        for manifest in (manifests[0], manifests[400], manifests[767]):
            difference = packet.bc_om_difference(manifest)
            for name, value in difference.items():
                self.assertTrue(value, "%s must be non-empty" % name)

        # The registered counterfactual: flipping the OM-only prerequisite's
        # lifecycle CHANGES the canonical gold while every BC-SELECTED object is
        # byte-identical.  OM-only evidence is therefore NECESSARY for that class.
        witness = packet.om_only_necessity_witness(manifests[0])
        self.assertTrue(witness["in_class"])
        self.assertTrue(witness["necessary"])
        self.assertTrue(witness["bc_selected_evidence_unchanged"])
        self.assertIsNone(witness["counterfactual_gold"])
        self.assertEqual(witness["registered_counterfactual"],
                         packet.OM_ONLY_REGISTERED_COUNTERFACTUAL)

        # DISCRIMINATING: the necessity check is not vacuous.  Move the OM-only
        # prerequisite INTO the BC selection and the class no longer applies.
        collapsed = copy.deepcopy(manifests[0])
        gold_row = next(row for row in collapsed["action_catalog"]
                        if row.get("action_id") == collapsed["gold_action_id"])
        target_row = next(row for row in collapsed["canonical_world"]
                          if row["object_id"] == gold_row["obligation_id"])
        collapsed["bc_selected_object_ids"] = sorted(
            set(collapsed["bc_selected_object_ids"])
            | set(target_row["fields"]["prerequisite_obligation_ids"]),
            key=lambda value: value.encode("utf-8"))
        collapsed_witness = packet.om_only_necessity_witness(collapsed)
        self.assertFalse(collapsed_witness["in_class"])
        self.assertEqual(collapsed_witness["errors"],
                         [packet.BUILD_OM_ONLY_EVIDENCE_NOT_NECESSARY])

        # DISCRIMINATING: the declared read-set variety floor actually gates.
        thin = packet.gold_read_set_census(manifests[:1])
        self.assertIn(packet.BUILD_GOLD_READ_SET_VARIETY_BELOW_FLOOR, thin["errors"])

    def test_bw74_red_w11_different_catalogs_produce_different_served_manifests(self):
        """§4 W11: green = two candidates with different action catalogs render DIFFERENT served
        manifests — the manifest varies with the population instead of being stamped."""
        packet, = self.require_modules(
            "W11 manifest-varies", "§4 W11",
            "different catalogs produce different served manifests",
            "mbcx01_build_cohort_packet")
        self.require_symbols("W11 manifest-varies", packet,
                             "build_manifest_for_candidate")
        generation = build_generation()
        context = generation.context
        retained = context.retained_candidates

        by_catalog: dict[str, dict] = {}
        for candidate in retained:
            by_catalog.setdefault(packets.sha384(candidate["action_catalog"]),
                                  candidate)
        self.assertGreaterEqual(len(by_catalog), 2,
                                "the population must carry at least two catalogs")
        first, second = [by_catalog[key] for key in sorted(by_catalog)][:2]
        left = packet.served_manifest_for_retained_candidate(context, first)
        right = packet.served_manifest_for_retained_candidate(context, second)

        self.assertNotEqual(left["action_catalog"], right["action_catalog"])
        self.assertNotEqual(left["action_catalog_hash"], right["action_catalog_hash"])
        self.assertNotEqual(left["manifest_hash"], right["manifest_hash"])
        self.assertNotEqual(left["canonical_world"], right["canonical_world"])
        for manifest in (left, right):
            self.assertEqual(packets.validate_expected_manifest(manifest), [])
            self.assertEqual(
                manifest["action_catalog_hash"], packets.sha384(manifest["action_catalog"]))

        # Different catalogs must reach the SERVED bytes, not just the manifest.
        served = set()
        for candidate, manifest in ((first, left), (second, right)):
            record = packet.render_all_six_nodes(candidate, context=context,
                                                 manifest=manifest)
            self.assertTrue(record["admitted"])
            served.add(record["served_input_hashes"]["OM.A0"])
        self.assertEqual(len(served), 2, "the served A0 bytes must differ too")

        # DISCRIMINATING counter-construction: the FROZEN builder STAMPS one
        # catalog (`mbcx01_r13_packets.py:167-174` hard-codes decoy/target/NO_ACTION),
        # so two DIFFERENT frozen candidates render the SAME catalog.
        frozen = measurement._pinned_retained_source()[0]
        frozen_left = packets.manifest_for_retained_candidate(frozen[0])
        frozen_right = packets.manifest_for_retained_candidate(frozen[1])
        self.assertNotEqual(frozen[0]["scenario_id"], frozen[1]["scenario_id"])
        self.assertEqual(frozen_left["action_catalog"], frozen_right["action_catalog"])
        self.assertEqual(frozen_left["canonical_world"], frozen_right["canonical_world"])

    def test_bw75_red_w12_a_journal_only_mutation_fails_the_build_provenance_gate(self):
        """§2/§4 W12: green = mutating only the event journal (`event_program_hash`) fails the
        BUILD provenance gate, so the journal is genuinely bound into the sub-digests."""
        authority, packet = self.require_modules(
            "W12 journal binding", "§2 module 2 / §4 W12",
            "a journal-only mutation fails the BUILD provenance gate",
            "mbcx01_build_cohort_authority", "mbcx01_build_cohort_packet")
        self.require_symbols("W12 journal binding", authority, "event_program_hash",
                             "observation_authority_hash", "build_source_authority")
        generation = build_generation()
        self.assertEqual(authority.validate_build_source_provenance(
            generation.candidates, generation.provenance), [])

        # A JOURNAL-ONLY mutation: one event's payload changes and NOTHING else —
        # every projected artefact (world, catalog, gold, observation, cut) stays
        # byte-identical, so only the journal binding can catch it.
        mutated = copy.deepcopy(generation.candidates)
        victim = mutated[0]
        target = next(index for index, event in enumerate(victim["event_program"])
                      if event["event_type"] == "open_obligation")
        victim["event_program"][target]["payload"]["owner_role"] = "WORKER.TAMPERED"

        original = generation.provenance["scenario_authority"][0]
        tampered = authority.build_source_authority(victim)
        self.assertEqual(
            [key for key in sorted(set(original) | set(tampered))
             if original.get(key) != tampered.get(key)],
            ["event_program_hash"],
            "the journal mutation must show up in EXACTLY the journal sub-digest")

        errors = authority.validate_build_source_provenance(
            mutated, generation.provenance)
        self.assertEqual(errors, ["SOURCE_PROVENANCE_MISMATCH"])
        self.assertEqual(
            authority.provenance_sub_digest_diff(
                authority.build_source_provenance(
                    mutated, generation.provenance["sequence_coverage"]),
                generation.provenance),
            ["event_program_hash"])

        # §2.6 also rides provenance: the coverage NUMBER with its STRENGTH and
        # FLOOR beside it, so a 2-way figure can never read as "covered".
        self.assertEqual(
            authority.sequence_coverage_report_errors(generation.provenance), [])
        coverage = generation.provenance["sequence_coverage"]
        self.assertEqual(coverage["strength"], 2)
        self.assertEqual(coverage["declared_floor"],
                         importlib.import_module(
                             "mbcx01_build_cohort_generator").SEQUENCE_COVERAGE_FLOOR)
        self.assertTrue(coverage["alphabet_presence_complete"])
        stripped = copy.deepcopy(generation.provenance)
        stripped["sequence_coverage"] = None
        stripped["provenance_hash"] = packets.sha384(
            {key: value for key, value in stripped.items() if key != "provenance_hash"})
        self.assertIn(authority.BUILD_SEQUENCE_COVERAGE_UNREPORTED,
                      authority.validate_build_source_provenance(
                          generation.candidates, stripped))

        # SECOND, INDEPENDENT binding: the mutated journal no longer replays to the
        # recorded generation state, so the supplied-state path refuses it too.
        with self.assertRaises(packet.BuildCohortPacketError) as refusal:
            packet.authoritative_state_for_cut(victim, victim["cut_ids"][-1])
        self.assertIn(packet.BUILD_EVENT_PROGRAM_REPLAY_MISMATCH, str(refusal.exception))

        # And selection refuses the mutated population outright.
        with self.assertRaises(authority.BuildCohortAuthorityError):
            authority.select_build_cohort(mutated, generation.provenance,
                                          packet.ELIGIBILITY_PREDICATE)

    def test_bw76_red_w13_all_six_renders_succeed_across_the_retained_population(self):
        """§2.5/§4 W13: green = `render_served_input` SUCCEEDS for all six nodes (BC and OM x
        A0/B/A1) across the retained 768, with the exact-fit and A1-growth witnesses."""
        packet, = self.require_modules(
            "W13 six renders", "§2.5 / §4 W13",
            "all six nodes render for every retained candidate, exact fit included",
            "mbcx01_build_cohort_packet")
        self.require_symbols("W13 six renders", packet, "render_all_six_nodes")
        generation = build_generation()
        context = generation.context
        retained = context.retained_candidates
        expected_nodes = ["%s.%s" % (condition, node)
                          for condition in ("BC", "OM") for node in ("A0", "B", "A1")]

        a0_lengths, a1_lengths, served = [], [], set()
        for candidate in retained:
            record = packet.render_all_six_nodes(candidate, context=context)
            self.assertTrue(record["admitted"],
                            "%s: %s %s" % (candidate["scenario_id"], record["errors"],
                                           record["refusal_detail"]))
            self.assertEqual(sorted(record["unpadded_lengths"]), sorted(expected_nodes))
            for length in record["unpadded_lengths"].values():
                self.assertLessEqual(length, packet.ENVELOPE_BYTES)
            self.assertLessEqual(record["world_object_count"],
                                 packet.DECLARED_WORLD_OBJECT_CEILING)
            a0_lengths.append(record["unpadded_lengths"]["OM.A0"])
            a1_lengths.append(record["unpadded_lengths"]["OM.A1"])
            served.add(record["served_input_hashes"]["OM.A0"])
        self.assertEqual(len(a0_lengths), 768)
        self.assertGreater(len(served), 1,
                           "a stamped population would render ONE served A0")

        # A1-GROWTH witness (r3 seat 3 executed an A1 overflowing at 65,541 while
        # its A0 fit): the A1 packet is never SMALLER than its A0, so A0 fitting is
        # not evidence that A1 fits — which is why admission renders all six.
        self.assertTrue(all(a1 >= a0 for a0, a1 in zip(a0_lengths, a1_lengths)))
        self.assertGreater(max(a1_lengths), max(a0_lengths))

        # EXACT-FIT witness: the frozen renderer pads every FITTING packet to
        # exactly 65,536 and raises ONLY on `len(encoded) > ENVELOPE_BYTES`
        # (`mbcx01_r13_packets.py:302-306`), so r2's "served < 65,536" was
        # unsatisfiable and its `>=` comparator refused the legal exact fit.
        filler = packet.ENVELOPE_BYTES - len(common.canonical_json({"pad": ""}))
        exact = {"pad": "P" * filler}
        self.assertEqual(len(common.canonical_json(exact)), packet.ENVELOPE_BYTES)
        self.assertEqual(len(packets.render_served_input(exact)), packet.ENVELOPE_BYTES)
        with self.assertRaises(ValueError) as overflow:
            packets.render_served_input({"pad": "P" * (filler + 1)})
        self.assertIn("PACKET_ENVELOPE_EXCEEDED", str(overflow.exception))

    def test_bw77_red_w18_authoritative_state_is_supplied_never_defaulted(self):
        """§2/§4 W18: green = the BUILD packet SUPPLIES `authoritative_state` from the replayed
        generation state, witnessed by `project_state_world` equality, and the frozen
        `_fixture_authoritative_state` default is never reached by a BUILD candidate."""
        packet, = self.require_modules(
            "W18 supplied state", "§2 module 3(d) / §4 W18",
            "the replayed state is supplied and the frozen fixture default is never reached",
            "mbcx01_build_cohort_packet")
        self.require_symbols("W18 supplied state", packet,
                             "build_scoring_fixture_for_candidate",
                             "authoritative_state_for_cut")
        generation = build_generation()
        context = generation.context
        candidate = context.retained_candidates[0]
        cut_id = candidate["chosen_cut_id"]
        manifest = packet.served_manifest_for_retained_candidate(context, candidate)

        state = packet.authoritative_state_for_cut(candidate, cut_id, dual=True)
        self.assertEqual(packets.sha384(state),
                         candidate["authoritative_state_hash_by_cut"][cut_id],
                         "the supplied state must be the REPLAYED generation state")
        self.assertEqual(packets.project_state_world(state, manifest),
                         manifest["canonical_world"],
                         "W18: project_state_world equality against the BUILD manifest")
        self.assertEqual(common.current_cut(state), manifest["cut"])

        # The frozen DEFAULT refuses this population outright: it rebuilds from
        # `initial_state()`'s hard-coded OBL.SHARED/OBL.PREREQ literals and enforces
        # exact obligation-set equality (`mbcx01_r13_packets.py:352-376`).
        with self.assertRaises(ValueError):
            packets._fixture_authoritative_state(manifest)

        # DISCRIMINATING: the default is not merely unusable, it is never REACHED.
        # Replace it with a tripwire and run the whole BUILD scoring path.
        original = packets._fixture_authoritative_state
        reached = []

        def tripwire(_manifest):
            reached.append(_manifest["scenario_id"])
            raise AssertionError("frozen fixture default was reached")

        try:
            packets._fixture_authoritative_state = tripwire
            fixture = packet.build_scoring_fixture_for_candidate(
                candidate, "OM", context=context, manifest=manifest,
                authoritative_state=state)
        finally:
            packets._fixture_authoritative_state = original
        self.assertEqual(reached, [], "the frozen fixture default must never be reached")
        self.assertEqual(fixture["schema_id"], "ScorerInputV1")
        self.assertEqual(fixture["manifest"], manifest)
        self.assertEqual(
            json.loads(fixture["manifest_cut_state_receipt"]["state_utf8"]), state)
        self.assertEqual(
            fixture["transition_authority"]["precommit_state"]["scopes"][SCORED_SCOPE][
                "obligations"].keys(),
            state["scopes"][SCORED_SCOPE]["obligations"].keys())
        self.assertEqual(packet.verify_build_scorer_input(
            manifest, fixture, context=context, candidate=candidate), [])

        # The exact-subtractive wrapper subtracts EXACTLY the frozen population
        # cascade and nothing else.  Unwrapped, the frozen validator's ONLY
        # complaint about this BUILD input is the declared closure.
        self.assertEqual(
            set(packets.validate_scorer_input(manifest, fixture,
                                              require_production_authority=False)),
            set(packet.POPULATION_AUTHORITY_CASCADE_CLOSURE))

        # DISCRIMINATING 1 — the wrapper must NOT launder a real defect.
        corrupted = copy.deepcopy(fixture)
        corrupted["a0_result"]["selected_action_ids"] = ["NO_ACTION"]
        corrupted_errors = packet.verify_build_scorer_input(
            manifest, corrupted, context=context, candidate=candidate)
        self.assertIn("A0_RESULT_INVALID", corrupted_errors)
        self.assertEqual(packet.build_score_exact(
            manifest, corrupted, context=context, candidate=candidate), 0)

        # DISCRIMINATING 2 — I01's manifest-equality half is NOT lost by the
        # subtraction: `validate_scorer_input:1021` reports it separately, OUTSIDE
        # the declared closure, so it is always returned.
        relabelled_manifest = copy.deepcopy(manifest)
        relabelled_manifest["route_contract_hash"] = "E" * 96
        relabelled_manifest["manifest_hash"] = packets.hash_without(
            relabelled_manifest, "manifest_hash")
        self.assertEqual(packets.validate_expected_manifest(relabelled_manifest), [])
        mismatched = packet.verify_build_scorer_input(
            relabelled_manifest, fixture, context=context, candidate=candidate)
        self.assertIn("EXPECTED_MANIFEST_MISMATCH", mismatched)

        # And the wrapper stays TOTAL: an ill-matched pair that makes the frozen
        # validator raise becomes a NAMED refusal, never an escaping traceback.
        other = context.retained_candidates[1]
        other_manifest = packet.served_manifest_for_retained_candidate(context, other)
        self.assertTrue(packet.verify_build_scorer_input(
            other_manifest, fixture, context=context, candidate=other))

        # DISCRIMINATING 3 — a scorer input carrying ANOTHER retained candidate's
        # BUILD authority is refused: the subtraction is conditioned on independent
        # BUILD evidence, so a laundered population join buys nothing.
        swapped = copy.deepcopy(fixture)
        swapped["cohort_authority"] = importlib.import_module(
            "mbcx01_build_cohort_authority").retained_scenario_authority(context, other)
        self.assertIn(packet.BUILD_SCORER_INPUT_INVALID,
                      packet.verify_build_scorer_input(
                          manifest, swapped, context=context, candidate=candidate))

    def test_bw78_red_w19_the_build_inference_ingress_and_membership_substitution(self):
        """§2/§4 W19: green = a full 768-position BUILD receipt set reaches the frozen numerical
        core through `ordered_decision_from_build_episode_receipts` while the same receipts stay
        RED at the unwrapped frozen ingress, AND a same-length membership substitution or
        reordering is REFUSED (the gate-r1 768-phantom-ID discriminator)."""
        packet, authority = self.require_modules(
            "W19 inference ingress + substitution", "§2 module 3(f) / §4 W19",
            "the BUILD ingress derives membership from the pinned authority and refuses a "
            "same-length substituted or reordered ID list",
            "mbcx01_build_cohort_packet", "mbcx01_build_cohort_authority")
        self.require_symbols("W19 inference ingress + substitution", packet,
                             "ordered_decision_from_build_episode_receipts",
                             "build_scenario_outcome_receipt")
        generation = build_generation()
        context = generation.context
        membership = authority.retained_membership_scenario_ids(context)
        self.assertEqual(len(membership), 768)

        candidate = context.retained_candidates[0]
        manifest = packet.served_manifest_for_retained_candidate(context, candidate)
        position = manifest["retained_position"]
        self.assertEqual(membership[position], candidate["scenario_id"])
        bc = packet.build_scoring_fixture_for_candidate(
            candidate, "BC", context=context, manifest=manifest)
        om = packet.build_scoring_fixture_for_candidate(
            candidate, "OM", context=context, manifest=manifest)
        episode = packet.build_complete_episode_receipt(bc, om, position)
        outcome = packet.build_scenario_outcome_receipt(
            manifest, bc, om, episode, context=context, candidate=candidate)
        self.assertEqual((outcome["bc"], outcome["om"]), (1, 1))
        self.assertEqual(packet.validate_build_scenario_outcome_receipt(
            outcome, episode, context=context, candidate=candidate), [])

        # A FULL 768-position BUILD receipt set: one complete pair, 767 whole-pair
        # missing.  The frozen `derive_episode_partition` and the frozen numerical
        # core both run UNMODIFIED inside the BUILD ingress.
        receipts = [measurement.episode_receipt_fixture(
            scenario_id, index, missing_position=None if index == position else "BC.A0")
            for index, scenario_id in enumerate(membership)]
        receipts[position] = episode
        partition = inference.derive_episode_partition(receipts, membership)
        self.assertEqual(partition["complete_ids"], [candidate["scenario_id"]])
        self.assertEqual(len(partition["missing_ids"]), 767)
        decision = packet.ordered_decision_from_build_episode_receipts(
            [outcome], receipts, context=context)
        self.assertIsInstance(decision, str)
        self.assertEqual(decision, packet.ordered_decision_from_build_episode_receipts(
            [outcome], receipts, context=context, manifest_scenario_ids=membership))

        # The SAME receipts are RED at the UNWRAPPED frozen ingress — and the red is
        # the POPULATION join, not a schema label: the receipt is relabelled to the
        # frozen schema id first, so it reaches `validate_cohort_manifest_join`.
        relabelled = copy.deepcopy(outcome)
        relabelled["schema_id"] = "ScenarioOutcomeReceiptV2"
        relabelled["receipt_hash"] = packets.hash_without(relabelled, "receipt_hash")
        self.assertFalse(packets.validate_cohort_manifest_join(
            bc["cohort_authority"], manifest),
            "the frozen cohort join can never admit a BUILD candidate")
        self.assertEqual(packets.validate_scenario_outcome_receipt(
            relabelled, episode, require_production_authority=False),
            ["SCENARIO_OUTCOME_AUTHORITY_INVALID"])
        with self.assertRaises(ValueError) as frozen_red:
            inference.ordered_decision_from_episode_receipts(
                [relabelled], receipts, membership, require_production_authority=False)
        self.assertIn("SCENARIO_OUTCOME_AUTHORITY_INVALID", str(frozen_red.exception))

        # The population-substitution red (the gate-r1 768-phantom-ID discriminator).
        phantom = ["SCENARIO.PHANTOM.%03d" % index for index in range(768)]
        reordered = list(membership)
        reordered[5], reordered[6] = reordered[6], reordered[5]
        substituted = list(membership)
        substituted[9] = "SCENARIO.BUILD.PHANTOM"
        for supplied in (phantom, reordered, substituted, membership[:-1]):
            self.assertEqual(
                authority.refuse_substituted_membership(context, supplied),
                [authority.BUILD_MEMBERSHIP_SUBSTITUTED])
            with self.assertRaises(packet.BuildCohortPacketError) as refusal:
                packet.ordered_decision_from_build_episode_receipts(
                    [outcome], receipts, context=context,
                    manifest_scenario_ids=supplied)
            self.assertIn(authority.BUILD_MEMBERSHIP_SUBSTITUTED,
                          str(refusal.exception))

    def test_bw79_red_w20_a_governed_stratum_below_its_declared_floor_is_red(self):
        """§2.3/§4 W20: green = the joint census reports declared strata and a governed stratum
        with nonzero occupancy below its declared retained floor fails loud as
        `RETAINED_AXIS_STRATUM_FLOOR`."""
        generator, = self.require_modules(
            "W20 stratum floors", "§2.3 / §4 W20",
            "a nonzero stratum below its declared retained floor is refused by name",
            "mbcx01_build_cohort_generator")
        self.require_symbols("W20 stratum floors", generator,
                             "RETAINED_AXIS_STRATUM_FLOOR", "population_census",
                             "DECLARED_RETAINED_FLOORS")
        generation = build_generation()
        generated = generation.candidates
        retained = generation.context.retained_candidates

        census = generation.census
        self.assertEqual(census["errors"], [])
        self.assertEqual(census["retained_total"], 768)
        self.assertEqual(census["joint_axes"], list(generator.CENSUS_JOINT_AXES))
        self.assertGreaterEqual(len(census["retained_joint_occupancy"]), 6 * 16 - 6)
        self.assertEqual(census["missing_joint_strata"], [])
        self.assertEqual(census["joint_strata_below_floor"], [])

        def joint_key(row):
            values = generator._axis_values(row)
            return "|".join(str(values[name]) for name in generator.CENSUS_JOINT_AXES)

        target = sorted(census["retained_joint_occupancy"],
                        key=lambda key: (census["retained_joint_occupancy"][key], key))[-1]

        # RED 1 — NONZERO BUT BELOW THE FLOOR: one retained row must not read as
        # "represented".  Keep exactly one member of a governed stratum.
        thinned, kept = [], False
        for row in retained:
            if joint_key(row) == target:
                if kept:
                    continue
                kept = True
            thinned.append(row)
        thin_census = generator.population_census(generated, thinned)
        self.assertEqual(thin_census["retained_joint_occupancy"][target], 1)
        self.assertIn(generator.RETAINED_AXIS_STRATUM_FLOOR, thin_census["errors"])
        self.assertIn("%s:1" % target, thin_census["joint_strata_below_floor"])

        # RED 2 — the MARGINAL-PRESERVING joint deletion (r3 seats 1+3): delete one
        # JOINT tuple entirely and every marginal VALUE is still present, so a
        # marginal-only census reads clean while a joint stratum has vanished.
        deleted = [row for row in retained if joint_key(row) != target]
        joint_census = generator.population_census(generated, deleted)
        self.assertIn(generator.RETAINED_AXIS_STRATUM_MISSING, joint_census["errors"])
        self.assertIn(target, joint_census["missing_joint_strata"])
        for axis in generator.CENSUS_JOINT_AXES:
            for value in joint_census["generated_marginals"][axis]:
                self.assertGreater(joint_census["retained_marginals"][axis].get(value, 0), 0,
                                   "%s=%s must survive the joint deletion" % (axis, value))

        # The floor is DECLARED, and it is the floor that gates.
        self.assertEqual(generator.DECLARED_RETAINED_FLOORS["joint"], 2)
        permissive = generator.population_census(generated, thinned,
                                                 floors={"joint": 1, "marginal": 1})
        self.assertNotIn(generator.RETAINED_AXIS_STRATUM_FLOOR, permissive["errors"])



# =============================================================================
# PART C — the slice-closing witnesses (registration task, 2026-08-16)
#
# Namespace `bc` (BUILD-COHORT), numbers bc01 upward; `verify-build-bundle.py`'s
# WITNESS_ID class was widened `b[aiw]` -> `b[aiwc]` in the same change and the
# reason is recorded beside the regex.  NO existing method is renumbered.
#
# RED-FIRST: every witness below was first run against a DELIBERATELY BROKEN
# in-memory variant of the thing it checks, and the verbatim red is recorded in the
# method.  A witness that only ever ran green is not evidence.
# =============================================================================


def cohort_modules():
    """The three cohort siblings, imported by name so a missing one fails loudly."""
    return (importlib.import_module("mbcx01_build_cohort_generator"),
            importlib.import_module("mbcx01_build_cohort_authority"),
            importlib.import_module("mbcx01_build_cohort_packet"))


def observation_derivation_inputs(candidate: dict, cut_id: str) -> tuple:
    """The EXACT inputs the generator hands the §2.2 derivation, re-derived here.

    `(state, cut, event_prefix, family_selector)` — nothing else reaches the rule,
    which is the whole point of the allowlist projection.
    """
    packet = importlib.import_module("mbcx01_build_cohort_packet")
    step = candidate["generation"]["frontier_step_by_cut"][cut_id]
    state = packet.replay_event_program(candidate, step)
    return (state, common.current_cut(state), candidate["event_program"][:step],
            candidate["variation"]["observation_family_selector"])


def strings_in(value, found=None) -> list:
    """Every string anywhere in a JSON-shaped value, KEYS INCLUDED."""
    found = [] if found is None else found
    if isinstance(value, str):
        found.append(value)
    elif isinstance(value, dict):
        for key, item in value.items():
            found.append(key)
            strings_in(item, found)
    elif isinstance(value, list):
        for item in value:
            strings_in(item, found)
    return found


def executable_source(*functions) -> str:
    """The EXECUTABLE source of some functions: docstrings and comments removed.

    A raw `inspect.getsource` scan cannot be used to prove a forbidden input never
    reaches the derivation rule, because the rule's own docstring NAMES every
    forbidden input in order to document the exclusion.  `ast.unparse` of a tree with
    the docstring expressions dropped leaves exactly the code that runs.
    """
    parts = []
    for function in functions:
        tree = ast.parse(textwrap.dedent(inspect.getsource(function)))
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                                 ast.AsyncFunctionDef)):
                body = getattr(node, "body", None)
                if (body and isinstance(body[0], ast.Expr)
                        and isinstance(body[0].value, ast.Constant)
                        and isinstance(body[0].value.value, str)):
                    body.pop(0)
        parts.append(ast.unparse(tree))
    return "\n".join(parts)


def relabel_declared_names(value):
    """A meaning-PRESERVING relabelling of declared identifiers (W15 RELABEL_DRIFT).

    Obligation, subject, predicate and value identifiers are all authored by the
    generator, so renaming every one of them consistently changes no declared
    meaning.  The SCOPE id is deliberately NOT renamed: it is an ALLOWED projection
    input and the SCOPE_DIGEST family's value is a digest of it, so moving it SHOULD
    move the observation and W15 never claims otherwise.
    """
    if isinstance(value, str):
        out = value
        for prefix in ("OBL.", "SUB.", "PRED.", "VALUE."):
            out = out.replace(prefix, prefix + "RELABELLED.")
        return out
    if isinstance(value, dict):
        return {relabel_declared_names(key): relabel_declared_names(item)
                for key, item in value.items()}
    if isinstance(value, list):
        return [relabel_declared_names(item) for item in value]
    return value


def relabel_state_and_program(state: dict, events: list) -> tuple:
    """Relabel a replayed state and its journal together, keeping FACT keys valid.

    `state["scopes"][...]["facts"]` is keyed by `fact_key(subject, predicate)`, a
    SHA-256 digest (`mbcx01_r13_common.py:101-102`), so a string relabelling leaves
    the key untouched while moving the pair it digests.  The keys are therefore
    RECOMPUTED from the relabelled pair; without that the ancestry check would fault
    and the witness would be measuring its own harness instead of the rule.
    """
    packet = importlib.import_module("mbcx01_build_cohort_packet")
    ancestry = packet.journal_fact_ancestry(events, SCORED_SCOPE)
    key_map = {}
    for source in ancestry.values():
        key_map[common.fact_key(source["subject_id"], source["predicate_id"])] = (
            common.fact_key(relabel_declared_names(source["subject_id"]),
                            relabel_declared_names(source["predicate_id"])))
    relabelled_state = relabel_declared_names(copy.deepcopy(state))
    facts = relabelled_state["scopes"][SCORED_SCOPE]["facts"]
    relabelled_state["scopes"][SCORED_SCOPE]["facts"] = {
        key_map.get(key, key): value for key, value in facts.items()}
    return relabelled_state, relabel_declared_names(copy.deepcopy(events))


class BuildCohortObservationNonLeakageWitnesses(unittest.TestCase):
    """§2.2 / §4 W15 — the FULL four-class checklist, one class per method.

    §2.2 defers to this checklist NORMATIVELY ("never a two-arm subset"), so the four
    classes design §4 names each get their own witness: LITERAL_LEAK ·
    DERIVABLE_ENCODING · RELABEL_DRIFT · CARDINALITY_OR_ORDER_CODEBOOK.
    """

    @staticmethod
    def observation_surface(packet, candidate: dict, cut_id: str) -> list:
        """EVERY observation-derived surface of one (scenario, cut), as strings.

        All three: the authority RECORD, the manifest's top-level representation and
        the world OBSERVATION rows.  A leak in any one of them is a leak.
        """
        record = candidate["observation_authority_by_cut"][cut_id]
        return (strings_in(record)
                + strings_in(candidate["observation_by_cut"][cut_id])
                + strings_in(packet.observation_manifest_representation(record))
                + strings_in(packet.observation_world_rows(record)))

    @classmethod
    def action_literals_found(cls, packet, candidate: dict, cut_id: str) -> list:
        """Any gold or catalog action id appearing ANYWHERE in the observation."""
        literals = {row["action_id"] for row in candidate["action_catalog"]}
        literals.add(candidate["gold_action_id_by_cut"][cut_id])
        literals.discard(None)
        surface = cls.observation_surface(packet, candidate, cut_id)
        return sorted({"%s@%s:%s" % (candidate["scenario_id"], cut_id, literal)
                       for literal in literals
                       for text in surface if literal in text})

    def test_bc01_adversarial_no_observation_field_carries_an_action_literal(self):
        """W15 class LITERAL_LEAK: no observation field, on any surface, contains the
        gold action id or ANY catalog action id — executed over the whole retained set
        and every offered cut, not a sample.

        RED-FIRST, recorded 2026-08-16.  BROKEN VARIANT: an in-memory projection that
        carries the scored target's `completion_action_id` and a derivation that folds it
        into the observation code.  This witness FAILED:

            AssertionError: Lists differ: ['SCENARIO.BUILD.1.130@CUT.BUILD.130.F0:AC
            [210053 chars]0EF'] != []
            First list contains 1910 additional elements.
            First extra element 0:
            'SCENARIO.BUILD.1.130@CUT.BUILD.130.F0:ACT.F0BAE0DDBD7241C5488A1343180DA18
            D27FFF20E1FF54C27F04AE2A3000F80EF'
            : LITERAL_LEAK: an action id reached an observation field
        """
        generator, _authority, packet = cohort_modules()
        generation = build_generation()
        leaks = []
        for candidate in generation.context.retained_candidates:
            for cut_id in candidate["cut_ids"]:
                leaks.extend(self.action_literals_found(packet, candidate, cut_id))
        self.assertEqual(leaks, [],
                         "LITERAL_LEAK: an action id reached an observation field")

        # DISCRIMINATING: the scan is not vacuous.  Fold the gold action id into the
        # observation code of ONE candidate and the same scan names it.
        victim = copy.deepcopy(generation.context.retained_candidates[0])
        cut_id = victim["chosen_cut_id"]
        gold = victim["gold_action_id_by_cut"][cut_id]
        self.assertIsNotNone(gold)
        victim["observation_authority_by_cut"][cut_id]["code"] = "SCOPE." + gold
        self.assertEqual(len(self.action_literals_found(packet, victim, cut_id)), 1)

        # And the ALLOWLIST is why: no forbidden name is spelled in the EXECUTABLE
        # source of the projection function or the derivation rule.  (Their
        # DOCSTRINGS name every forbidden input, deliberately, to document the
        # exclusion — which is why the scan runs on docstring-stripped code.)
        source = executable_source(generator.project_observation_inputs,
                                   generator.derive_observation_authority)
        for forbidden in generator.OBSERVATION_FORBIDDEN_INPUTS:
            self.assertNotIn(forbidden, source,
                             "%s is named inside the derivation path" % forbidden)

    def test_bc02_adversarial_perturbing_each_forbidden_input_moves_no_observation(self):
        """W15 class DERIVABLE_ENCODING: with the ALLOWED PROJECTION HELD FIXED, EACH
        forbidden input is perturbed INDEPENDENTLY and the observation family and value
        must not move.  Every name in `OBSERVATION_FORBIDDEN_INPUTS` is covered: the
        four that live in the replayed STATE are perturbed there and the projection is
        re-run; the rest cannot reach the rule at all, which is asserted structurally
        against the projection's own signature and output keys.

        RED-FIRST, recorded 2026-08-16.  BROKEN VARIANT: an in-memory
        `project_observation_inputs` that adds 1 to the family selector when the scored
        target's lifecycle is CANCELLED.  This witness FAILED:

            AssertionError: {'sco[173 chars] 'distinct_subject_count': 1,
            'observation_family_selector': 3} != {'sco[173 chars]
            'distinct_subject_count': 1, 'observation_family_selector': 2}
            -  'observation_family_selector': 3,
            +  'observation_family_selector': 2,
            : target_lifecycle reached the ALLOWED projection
        """
        generator, _authority, packet = cohort_modules()
        generation = build_generation()
        candidate = generation.context.retained_candidates[0]
        cut_id = candidate["chosen_cut_id"]
        state, cut, events, selector = observation_derivation_inputs(candidate, cut_id)
        baseline_projection = generator.project_observation_inputs(
            state, cut, events, selector)
        baseline = generator.derive_observation_authority(
            candidate["scenario_id"], cut_id, baseline_projection)
        self.assertEqual(baseline, candidate["observation_authority_by_cut"][cut_id],
                         "the witness must re-derive the SAME record the generator did")

        obligations = state["scopes"][SCORED_SCOPE]["obligations"]
        # RIDER (cohort-BUILD r1 FOLD 2(a)): the scored target's identity is now
        # PER-SCENARIO, so the witness derives it instead of reading one constant.
        # The witness's MEANING is unchanged — it still perturbs the four
        # state-resident forbidden inputs ON THE SCORED TARGET of this candidate.
        target_id = generator.target_obligation_id(candidate["scenario_id"])
        self.assertIn(target_id, obligations)
        prerequisites = list(obligations[target_id]["prerequisite_obligation_ids"])
        self.assertTrue(prerequisites, "the target must have a prerequisite to perturb")

        def perturb_lifecycle(value):
            row = value["scopes"][SCORED_SCOPE]["obligations"][target_id]
            row["lifecycle"] = "CANCELLED" if row["lifecycle"] != "CANCELLED" else "OPEN"

        def perturb_critical(value):
            row = value["scopes"][SCORED_SCOPE]["obligations"][target_id]
            row["critical"] = not row["critical"]

        def perturb_due_at(value):
            value["scopes"][SCORED_SCOPE]["obligations"][target_id]["due_at"] = T2

        def perturb_prerequisite_lifecycles(value):
            for prerequisite in prerequisites:
                value["scopes"][SCORED_SCOPE]["obligations"][prerequisite][
                    "lifecycle"] = "CANCELLED"

        state_resident = {"target_lifecycle": perturb_lifecycle,
                          "target_critical": perturb_critical,
                          "target_due_at": perturb_due_at,
                          "prerequisite_lifecycles": perturb_prerequisite_lifecycles}
        for name, perturbation in sorted(state_resident.items()):
            perturbed = copy.deepcopy(state)
            perturbation(perturbed)
            self.assertNotEqual(common.canonical_json(perturbed),
                                common.canonical_json(state),
                                "%s: the perturbation must change the state" % name)
            projection = generator.project_observation_inputs(
                perturbed, common.current_cut(perturbed), events, selector)
            self.assertEqual(projection, baseline_projection,
                             "%s reached the ALLOWED projection" % name)
            record = generator.derive_observation_authority(
                candidate["scenario_id"], cut_id, projection)
            self.assertEqual(record["family"], baseline["family"],
                             "DERIVABLE_ENCODING: perturbing %s moved the observation "
                             "family" % name)
            self.assertEqual(record, baseline,
                             "DERIVABLE_ENCODING: perturbing %s moved the observation "
                             "record" % name)

        # The remaining forbidden inputs are UNREPRESENTABLE rather than merely
        # unused: they are not parameters of the projection, not keys of its output,
        # and perturbing them on the candidate and the served manifest leaves every
        # observation surface byte-identical.
        parameters = set(inspect.signature(
            generator.project_observation_inputs).parameters)
        self.assertEqual(parameters, {"state", "cut", "event_program",
                                      "family_selector"})
        self.assertEqual(sorted(baseline_projection),
                         sorted(generator.OBSERVATION_ALLOWED_FIELDS))
        for forbidden in generator.OBSERVATION_FORBIDDEN_INPUTS:
            self.assertNotIn(forbidden, baseline_projection)

        manifest = packet.served_manifest_for_retained_candidate(
            generation.context, candidate)
        other_motif = next(motif for motif in measurement.MOTIFS
                           if motif != candidate["motif"])
        mutations = {
            "motif": lambda row, doc: row.update({"motif": other_motif}),
            "gold_action_id": lambda row, doc: doc.update(
                {"gold_action_id": "ACT." + "E" * 64}),
            "action_id": lambda row, doc: doc["action_catalog"][0].update(
                {"action_id": "ACT." + "D" * 64}),
            "action_catalog": lambda row, doc: doc["action_catalog"].append(
                {"action_id": "ACT." + "C" * 64, "action_kind": "NO_ACTION"}),
            "candidate_selector_id": lambda row, doc: doc.update(
                {"candidate_selector_id": "SELECTOR.OTHER"}),
            "bc_selected_object_ids": lambda row, doc: doc.update(
                {"bc_selected_object_ids": []}),
            "retained_position": lambda row, doc: doc.update(
                {"retained_position": (doc["retained_position"] + 1) % 768}),
            "retained_set_root": lambda row, doc: doc.update(
                {"retained_set_root": "A" * 96}),
        }
        for name, mutation in sorted(mutations.items()):
            row = copy.deepcopy(candidate)
            doc = copy.deepcopy(manifest)
            mutation(row, doc)
            self.assertNotEqual(common.canonical_json([row, doc]),
                                common.canonical_json([candidate, manifest]),
                                "%s: the perturbation must change something" % name)
            self.assertEqual(
                packet.observation_manifest_representation(
                    row["observation_authority_by_cut"][cut_id]),
                manifest["observation"],
                "DERIVABLE_ENCODING: perturbing %s moved the observation" % name)
            self.assertEqual(
                generator.project_observation_inputs(state, cut, events, selector),
                baseline_projection)

    def test_bc03_positive_relabelling_identifiers_leaves_the_observation_unchanged(self):
        """W15 class RELABEL_DRIFT: an identifier/action relabelling that preserves the
        observation's declared meaning leaves the family and the value unchanged
        (r2 seat-2's semantic-noninterference form), executed over one candidate per
        observation family so no family is exempt.

        RED-FIRST, recorded 2026-08-16.  BROKEN VARIANT: an in-memory derivation whose
        code carries a digest of the sorted obligation NAMES.  This witness FAILED:

            AssertionError: 'POPULATION.COUNT.5.NAMES.E8A145' !=
            'POPULATION.COUNT.5.NAMES.5DA815'
            : RELABEL_DRIFT: COUNT_SUMMARY moved under a meaning-preserving relabelling
        """
        generator, _authority, _packet = cohort_modules()
        generation = build_generation()
        by_family = {}
        for candidate in generation.context.retained_candidates:
            by_family.setdefault(candidate["variation"]["observation_family"], candidate)
        self.assertEqual(sorted(by_family), sorted(generator.OBSERVATION_FAMILIES),
                         "every declared observation family must be exercised")

        for family, candidate in sorted(by_family.items()):
            cut_id = candidate["chosen_cut_id"]
            state, cut, events, selector = observation_derivation_inputs(
                candidate, cut_id)
            baseline = generator.derive_observation_authority(
                candidate["scenario_id"], cut_id,
                generator.project_observation_inputs(state, cut, events, selector))
            self.assertEqual(baseline["family"], family)

            relabelled_state, relabelled_events = relabel_state_and_program(
                state, events)
            self.assertNotEqual(common.canonical_json(relabelled_state),
                                common.canonical_json(state),
                                "the relabelling must actually rename something")
            relabelled = generator.derive_observation_authority(
                candidate["scenario_id"], cut_id,
                generator.project_observation_inputs(
                    relabelled_state, common.current_cut(relabelled_state),
                    relabelled_events, selector))
            self.assertEqual(relabelled["code"], baseline["code"],
                             "RELABEL_DRIFT: %s moved under a meaning-preserving "
                             "relabelling" % family)
            self.assertEqual(relabelled, baseline,
                             "RELABEL_DRIFT: %s moved under a meaning-preserving "
                             "relabelling" % family)

        # DISCRIMINATING: the relabelling is not a no-op, and the ONE identifier that
        # SHOULD move the observation does — the scope, which is an ALLOWED input and
        # is the SCOPE_DIGEST family's whole value.
        candidate = by_family["SCOPE_DIGEST"]
        cut_id = candidate["chosen_cut_id"]
        state, cut, events, selector = observation_derivation_inputs(candidate, cut_id)
        projection = generator.project_observation_inputs(state, cut, events, selector)
        baseline = generator.derive_observation_authority(
            candidate["scenario_id"], cut_id, projection)
        moved = generator.derive_observation_authority(
            candidate["scenario_id"], cut_id,
            dict(projection, scope_id="SCOPE.OTHER"))
        self.assertNotEqual(moved["code"], baseline["code"],
                            "an ALLOWED input must be able to move the observation, "
                            "or this witness proves nothing")

    def test_bc04_adversarial_observation_families_are_not_a_cardinality_codebook(self):
        """W15 class CARDINALITY_OR_ORDER_CODEBOOK: the observation family distribution
        is driven ONLY by the allowed projection.  Three assertions carry it: the family
        is a FUNCTION of the allowed selector alone; candidates that share an allowed
        projection share their observation EVEN WHEN their catalog size differs; and the
        family/catalog-size and family/event-order cross-tabulations are full, so the
        family is not a codebook over catalog cardinality or event order.

        RED-FIRST, recorded 2026-08-16.  BROKEN VARIANT: an in-memory `_variation_for`
        that chooses the observation family BY CATALOG SIZE.  This witness FAILED:

            AssertionError: 1 not greater than or equal to 2 : catalog size 3 must not
            select ONE family (CARDINALITY_OR_ORDER_CODEBOOK)
        """
        generator, _authority, _packet = cohort_modules()
        generation = build_generation()
        retained = generation.context.retained_candidates

        families_by_projection = {}
        families_by_selector = {}
        families_by_catalog_size = {}
        catalog_sizes_by_family = {}
        families_by_event_order = {}
        for candidate in retained:
            cut_id = candidate["chosen_cut_id"]
            record = candidate["observation_authority_by_cut"][cut_id]
            selector = record["projection"]["observation_family_selector"]
            family = record["family"]
            self.assertEqual(
                family,
                generator.OBSERVATION_FAMILIES[
                    selector % len(generator.OBSERVATION_FAMILIES)],
                "the family must be a FUNCTION of the allowed selector alone")
            families_by_selector.setdefault(selector, set()).add(family)
            size = candidate["variation"]["catalog_size"]
            families_by_catalog_size.setdefault(size, set()).add(family)
            catalog_sizes_by_family.setdefault(family, set()).add(size)
            families_by_event_order.setdefault(
                candidate["variation"]["event_order"], set()).add(family)
            key = common.canonical_json(record["projection"])
            families_by_projection.setdefault(key, []).append(
                (candidate["scenario_id"], size, record["family"], record["code"]))

        for selector, families in sorted(families_by_selector.items()):
            self.assertEqual(len(families), 1,
                             "selector %s selects more than one family" % selector)

        for size, families in sorted(families_by_catalog_size.items()):
            self.assertGreaterEqual(
                len(families), 2,
                "catalog size %s must not select ONE family "
                "(CARDINALITY_OR_ORDER_CODEBOOK)" % size)
        for family, sizes in sorted(catalog_sizes_by_family.items()):
            self.assertGreaterEqual(
                len(sizes), 2,
                "family %s must not encode ONE catalog size "
                "(CARDINALITY_OR_ORDER_CODEBOOK)" % family)
        for order, families in sorted(families_by_event_order.items()):
            self.assertEqual(
                sorted(families), sorted(generator.OBSERVATION_FAMILIES),
                "event order %s must not select a family subset "
                "(CARDINALITY_OR_ORDER_CODEBOOK)" % order)

        # The strongest form, kept LAST because it is the most specific: an IDENTICAL
        # allowed projection must produce an IDENTICAL observation even when the
        # candidates differ in catalog size.  A codebook over catalog cardinality
        # cannot survive this — and it cannot even produce such a group, which is why
        # the cross-tabulations above are asserted first.
        spanning = [rows for rows in families_by_projection.values()
                    if len({row[1] for row in rows}) > 1]
        self.assertGreaterEqual(len(spanning), 2,
                                "the population must contain projection groups that "
                                "span more than one catalog size, or this witness "
                                "cannot discriminate")
        for rows in spanning:
            self.assertEqual(len({(row[2], row[3]) for row in rows}), 1,
                             "one allowed projection produced more than one "
                             "observation: %s" % rows[:4])


def serve_mutated_retained_candidate(mutate) -> tuple:
    """Apply a mutation to a COPY of the cached population, rebuild its provenance and
    a fresh retained authority context, and return the ENRICHED retained twin.

    `mutate(candidates, generation)` mutates the RAW candidate list in place and
    returns the scenario id it touched.  The mutation must be applied BEFORE the
    context is built: the context indexes the ENRICHED retained copy (it adds
    `chosen_cut_id` / `eligible` / `retention_hash`), so mutating a raw draft and then
    serving it proves nothing — the retained twin the serving path takes would be the
    honest row.  That is exactly how the driver's first r1 probe failed, and it is
    recorded here so the harness cannot silently regress into it.

    No second generation: the ONE cached population is copied, which is why this costs
    a provenance rebuild and a selection pass, not a 960-candidate regeneration.
    """
    _generator, authority, packet = cohort_modules()
    generation = build_generation()
    candidates = copy.deepcopy(generation.candidates)
    scenario_id = mutate(candidates, generation)
    provenance = authority.build_source_provenance(candidates, generation.coverage)
    context = authority.BuildRetainedAuthorityContext(
        candidates, provenance, packet.ELIGIBILITY_PREDICATE)
    victim = next(row for row in context.retained_candidates
                  if row["scenario_id"] == scenario_id)
    return context, victim, victim["chosen_cut_id"]


class BuildCohortSliceClosingWitnesses(unittest.TestCase):
    """§4 W16, W17, W1, W3, W5, W8 and W14 — the witnesses the engine build left
    undischarged, each red-first against a deliberately broken variant.

    bc15/bc16 (added 2026-08-16 by the cohort-BUILD r1 FOLD 1) close the class
    COHORT_SERVE_BOUNDARY_SEMANTIC_REDERIVATION: the two constructions the council
    reproduced through the SERVING path, not merely through the validator."""

    def test_bc05_positive_one_retained_candidate_scores_end_to_end_on_the_build_path(self):
        """§4 W16 (dedicated): ONE retained BUILD candidate through the whole scoring
        seam — supplied-state `build_scoring_fixture`, the exact-subtractive scorer
        wrapper, the episode receipt and scenario-outcome VALIDATION — green on the
        BUILD path, and RED with a NAMED frozen error at each of the three unwrapped
        frozen doors.

        RED-FIRST, recorded 2026-08-16.  BROKEN VARIANT: the exact-subtractive wrapper
        replaced in memory by the FROZEN `validate_scorer_input`.  This witness FAILED:

            AssertionError: Lists differ: ['I01_INVARIANT_INVALID'] != []
            First list contains 1 additional elements.
            First extra element 0: 'I01_INVARIANT_INVALID'
        """
        _generator, authority, packet = cohort_modules()
        generation = build_generation()
        context = generation.context
        candidate = context.retained_candidates[3]
        cut_id = candidate["chosen_cut_id"]
        manifest = packet.served_manifest_for_retained_candidate(context, candidate)
        state = packet.authoritative_state_for_cut(candidate, cut_id, dual=True)

        # --- the BUILD path, end to end ---------------------------------------
        fixtures = {}
        for condition in ("BC", "OM"):
            fixtures[condition] = packet.build_scoring_fixture_for_candidate(
                candidate, condition, context=context, manifest=manifest,
                authoritative_state=state)
            self.assertEqual(fixtures[condition]["schema_id"], "ScorerInputV1")
            self.assertEqual(fixtures[condition]["manifest"], manifest)
            self.assertEqual(packet.verify_build_scorer_input(
                manifest, fixtures[condition], context=context,
                candidate=candidate), [])
            self.assertEqual(packet.build_score_exact(
                manifest, fixtures[condition], context=context, candidate=candidate), 1)
        episode = packet.build_complete_episode_receipt(
            fixtures["BC"], fixtures["OM"], manifest["retained_position"])
        outcome = packet.build_scenario_outcome_receipt(
            manifest, fixtures["BC"], fixtures["OM"], episode,
            context=context, candidate=candidate)
        self.assertEqual(packet.validate_build_scenario_outcome_receipt(
            outcome, episode, context=context, candidate=candidate), [])
        self.assertEqual((outcome["bc"], outcome["om"]), (1, 1))
        self.assertEqual(outcome["retained_set_root"],
                         authority.retained_set_root(context))
        self.assertEqual(outcome["scenario_id"], candidate["scenario_id"])

        # --- the SAME candidate at the three UNWRAPPED frozen doors ------------
        # 1. the DEFAULT authoritative state (`_fixture_authoritative_state`, the
        #    frozen literals at `mbcx01_r13_packets.py:352-376`).
        with self.assertRaises(ValueError) as default_state:
            packets.build_scoring_fixture(manifest, "OM")
        self.assertIn(str(default_state.exception),
                      ("MANIFEST_STATE_PROJECTION_MISMATCH",
                       "default authoritative state does not match manifest cut"))
        # 2. the frozen SCORER-INPUT validator: exactly the declared population
        #    cascade closure, nothing else — the subtraction is honest.
        self.assertEqual(
            set(packets.validate_scorer_input(manifest, fixtures["OM"],
                                              require_production_authority=False)),
            set(packet.POPULATION_AUTHORITY_CASCADE_CLOSURE))
        self.assertEqual(sorted(packet.POPULATION_AUTHORITY_CASCADE_CLOSURE),
                         ["I01_INVARIANT_INVALID"])
        # 3. the frozen SCENARIO-OUTCOME builder, which is the fifth surface: it
        #    re-runs `validate_cohort_manifest_join` against the FROZEN pinned
        #    population and can never admit a BUILD candidate.
        with self.assertRaises(ValueError) as frozen_outcome:
            packets.build_scenario_outcome_receipt(
                manifest, fixtures["BC"], fixtures["OM"], episode,
                require_production_authority=False)
        self.assertEqual(str(frozen_outcome.exception),
                         "SCENARIO_OUTCOME_AUTHORITY_INVALID")
        self.assertFalse(packets.validate_cohort_manifest_join(
            fixtures["BC"]["cohort_authority"], manifest))

        # DISCRIMINATING: the BUILD path is not a rubber stamp.  A corrupted A0
        # result scores 0 on the SAME wrapper that scored the honest input 1.
        corrupted = copy.deepcopy(fixtures["OM"])
        corrupted["a0_result"]["selected_action_ids"] = ["NO_ACTION"]
        self.assertIn("A0_RESULT_INVALID", packet.verify_build_scorer_input(
            manifest, corrupted, context=context, candidate=candidate))
        self.assertEqual(packet.build_score_exact(
            manifest, corrupted, context=context, candidate=candidate), 0)
        broken_outcome = copy.deepcopy(outcome)
        broken_outcome["om"] = 0
        broken_outcome["receipt_hash"] = packets.hash_without(
            broken_outcome, "receipt_hash")
        self.assertEqual(
            packet.validate_build_scenario_outcome_receipt(
                broken_outcome, episode, context=context, candidate=candidate),
            [packet.BUILD_SCENARIO_OUTCOME_AUTHORITY_INVALID])

    def test_bc06_positive_coverage_recomputes_against_the_registered_denominator(self):
        """§2.6 / §4 W17 (dedicated): the coverage record in PROVENANCE carries the
        NUMBER, its STRENGTH t, its declared FLOOR and the DENOMINATOR IDENTITY, and
        recomputing coverage in this witness against that registered denominator
        reproduces the number exactly.  The denominator's honest limit (unconstrained
        square, a LOWER BOUND on LTS-constrained coverage) is asserted as DECLARED, so
        a 2-way figure can never read as 'covered'.

        RED-FIRST, recorded 2026-08-16.  BROKEN VARIANT: coverage measured in memory over
        a 16-event alphabet (256 pairs) instead of the registered 17-event square.  This
        witness FAILED:

            AssertionError: 256 != 289
        """
        generator, authority, _packet = cohort_modules()
        generation = build_generation()
        coverage = generation.provenance["sequence_coverage"]

        # (1) the record REPORTS all four, and the authority agrees it is reported.
        self.assertEqual(authority.sequence_coverage_report_errors(
            generation.provenance), [])
        self.assertEqual(coverage["strength"], generator.SEQUENCE_COVERAGE_STRENGTH)
        self.assertEqual(coverage["strength"], 2)
        self.assertEqual(coverage["declared_floor"], generator.SEQUENCE_COVERAGE_FLOOR)
        self.assertEqual(coverage["target_set_rule"], generator.SEQUENCE_TARGET_SET_RULE)
        self.assertIn("UNCONSTRAINED", coverage["target_set_rule"],
                      "the honest limit must be DECLARED beside the number")

        # (2) the REGISTERED denominator, rebuilt here from the 17-event alphabet.
        alphabet = tuple(sorted(common.EVENT_OPERATIONS))
        self.assertEqual(len(alphabet), 17)
        pairs = sorted((first, second) for first in alphabet for second in alphabet)
        self.assertEqual(len(pairs), 289)
        self.assertEqual(coverage["target_pair_count"], len(pairs))
        self.assertEqual(coverage["target_set_identity"],
                         packets.sha384(["%s>%s" % pair for pair in pairs]))

        # (3) the NUMBER, recomputed against that denominator, independently of the
        #     generator's own helper.
        #     RIDER (cohort-BUILD r1 FOLD 4): this recount used to MIRROR the
        #     generator's APPLIED-only filter, which is why it could not see the
        #     undercount.  It now counts pairs over ALL gate-checked program events —
        #     the declared numerator rule — and asserts the record declares it.
        self.assertEqual(coverage["covered_pair_rule"],
                         generator.SEQUENCE_COVERED_PAIR_RULE)
        covered = set()
        for candidate in generation.candidates:
            executed = [event["event_type"] for event in candidate["event_program"]]
            for position, first in enumerate(executed):
                for second in executed[position + 1:]:
                    covered.add((first, second))
        self.assertTrue(covered <= set(pairs), "coverage escaped the denominator")
        self.assertEqual(len(covered), coverage["covered_pair_count"])
        self.assertEqual(len(covered) / len(pairs), coverage["coverage_ratio"])
        self.assertGreaterEqual(coverage["coverage_ratio"], coverage["declared_floor"])
        self.assertIs(coverage["meets_declared_floor"], True)
        self.assertEqual(coverage["errors"], [])
        self.assertTrue(coverage["alphabet_presence_complete"])
        self.assertEqual(coverage["alphabet_present"], list(alphabet))

        # DISCRIMINATING 1 — the DENOMINATOR is load-bearing: the same numerator over
        # a 16-event denominator is a different, higher number, so a coverage figure
        # without its registered denominator says nothing.
        smaller = sorted((first, second) for first in alphabet[:16]
                         for second in alphabet[:16])
        self.assertNotEqual(len(smaller), len(pairs))
        smaller_covered = {pair for pair in covered if pair in set(smaller)}
        self.assertGreater(len(smaller_covered) / len(smaller),
                           coverage["coverage_ratio"])
        self.assertNotEqual(packets.sha384(["%s>%s" % pair for pair in smaller]),
                            coverage["target_set_identity"])

        # DISCRIMINATING 2 — the FLOOR gates: a record that does not meet it is
        # refused by name, and the generator itself refuses to return such a run.
        below = copy.deepcopy(generation.provenance)
        below["sequence_coverage"]["meets_declared_floor"] = False
        self.assertEqual(authority.sequence_coverage_report_errors(below),
                         [authority.BUILD_SEQUENCE_COVERAGE_UNREPORTED])
        floored = generator.sequence_coverage(generation.candidates[:1])
        self.assertLess(floored["coverage_ratio"], generator.SEQUENCE_COVERAGE_FLOOR)
        self.assertEqual(floored["errors"],
                         [generator.BUILD_SEQUENCE_COVERAGE_BELOW_FLOOR])

    def test_bc07_adversarial_dropping_or_substituting_one_member_fails_the_root(self):
        """§4 W1 (membership discrimination): drop ONE retained candidate, or
        SUBSTITUTE one, and the retained root no longer reproduces — the BUILD
        authority path refuses both by name, even when the doctored authority is
        internally self-consistent (its own root and authority hash recomputed).

        RED-FIRST, recorded 2026-08-16.  BROKEN VARIANT: an in-memory
        `validate_retained_cohort_authority` that checks only INTERNAL self-consistency —
        the property a doctored authority satisfies by construction.  This witness FAILED:

            AssertionError: Lists differ: [] != ['BUILD_RETAINED_COHORT_AUTHORITY_INVALID']
            Second list contains 1 additional elements.
            First extra element 0: 'BUILD_RETAINED_COHORT_AUTHORITY_INVALID'
        """
        _generator, authority, _packet = cohort_modules()
        generation = build_generation()
        context = generation.context
        cohort = authority.retained_cohort_authority(context)
        self.assertEqual(authority.validate_retained_cohort_authority(context, cohort),
                         [])
        self.assertEqual(cohort["retained_total"], 768)

        def sealed(document):
            """Re-seal a doctored authority so it is INTERNALLY consistent."""
            document["retained_total"] = len(document["retained_scenario_ids"])
            document["retained_set_root"] = packets.sha384(
                document["retained_candidate_hashes"])
            document["authority_hash"] = packets.sha384(
                {key: value for key, value in document.items()
                 if key != "authority_hash"})
            return document

        # --- DROP one retained member ----------------------------------------
        dropped = sealed(copy.deepcopy(cohort))
        del dropped["retained_scenario_ids"][400]
        del dropped["retained_candidate_hashes"][400]
        sealed(dropped)
        self.assertEqual(dropped["retained_total"], 767)
        self.assertNotEqual(dropped["retained_set_root"], cohort["retained_set_root"])
        self.assertEqual(
            authority.validate_retained_cohort_authority(context, dropped),
            [authority.BUILD_RETAINED_COHORT_AUTHORITY_INVALID])
        self.assertEqual(
            authority.refuse_substituted_membership(
                context, dropped["retained_scenario_ids"]),
            [authority.BUILD_MEMBERSHIP_SUBSTITUTED])

        # --- SUBSTITUTE one retained member, same length ----------------------
        substituted = copy.deepcopy(cohort)
        substituted["retained_scenario_ids"][12] = "SCENARIO.BUILD.PHANTOM"
        substituted["retained_candidate_hashes"][12] = packets.sha384(
            {"schema_id": "PhantomCandidate"})
        sealed(substituted)
        self.assertEqual(substituted["retained_total"], 768)
        self.assertNotEqual(substituted["retained_set_root"],
                            cohort["retained_set_root"])
        self.assertEqual(
            authority.validate_retained_cohort_authority(context, substituted),
            [authority.BUILD_RETAINED_COHORT_AUTHORITY_INVALID])
        self.assertEqual(
            authority.refuse_substituted_membership(
                context, substituted["retained_scenario_ids"]),
            [authority.BUILD_MEMBERSHIP_SUBSTITUTED])

        # --- a REORDERING keeps the multiset and still fails -------------------
        reordered = copy.deepcopy(cohort)
        for name in ("retained_scenario_ids", "retained_candidate_hashes"):
            reordered[name][5], reordered[name][6] = reordered[name][6], reordered[name][5]
        sealed(reordered)
        self.assertEqual(sorted(reordered["retained_scenario_ids"]),
                         sorted(cohort["retained_scenario_ids"]))
        self.assertEqual(
            authority.validate_retained_cohort_authority(context, reordered),
            [authority.BUILD_RETAINED_COHORT_AUTHORITY_INVALID])

        # DISCRIMINATING: the doctored documents are INTERNALLY consistent — root and
        # authority hash both recompute — so what refuses them is the recomputation
        # from the pinned population, not a shape check.
        for doctored in (dropped, substituted, reordered):
            self.assertEqual(doctored["retained_set_root"],
                             packets.sha384(doctored["retained_candidate_hashes"]))
            self.assertEqual(doctored["authority_hash"], packets.sha384(
                {key: value for key, value in doctored.items()
                 if key != "authority_hash"}))
        # And an untouched member of the real set still issues authority, so the
        # refusal is about the SET, not about the row.
        member = context.retained_candidates[400]
        self.assertEqual(authority.validate_retained_scenario_authority(
            context, authority.retained_scenario_authority(context, member)), [])

    def test_bc08_positive_the_planned_ineligible_quota_is_exact_and_stratified(self):
        """§2.3 / §4 W3: the SEQUENCED total-admission arithmetic, checked as numbers.
        Per motif the planned-ineligible count is EXACTLY k=12, stratified across the
        three declared classes, each placement in a DISTINCT joint census stratum, and
        `160 - e - placed >= 128` holds by arithmetic over the whole plan.  Every
        planned ineligible is ineligible BY DERIVATION and absent from the retained set.

        RED-FIRST, recorded 2026-08-16.  BROKEN VARIANT: an in-memory `_plan_placements`
        that places one fewer than the declared quota.  This witness FAILED:

            AssertionError: 11 != 12
        """
        generator, authority, packet = cohort_modules()
        generation = build_generation()
        spec, _digest = authority.build_generator_spec()
        quota = spec["planned_ineligible_quota_k"]
        margin = spec["refusal_margin"]
        self.assertEqual((quota, margin), (12, 32))
        self.assertLessEqual(quota, margin)
        strata = list(spec["planned_ineligible_strata"])
        self.assertEqual(sorted(strata),
                         sorted(["TARGET_NOT_DUE", "AMBIGUOUS_GOLD",
                                 "MISSING_NON_GOLD"]))
        retained_ids = set(authority.retained_membership_scenario_ids(
            generation.context))

        for motif in authority.MOTIFS:
            row = generation.plan["per_motif"][motif]
            refusals = row["unplanned_refusals"]
            placed = row["planned_ineligible_placed"]
            self.assertLessEqual(refusals, margin,
                                 "%s: e must never exceed the floor margin" % motif)
            self.assertEqual(placed, max(0, min(quota, margin - refusals)),
                             "%s: the placement is the SEQUENCED formula" % motif)
            self.assertEqual(placed, quota,
                             "%s: this build places exactly k=%d" % (motif, quota))
            self.assertEqual(len(row["planned_ineligible_scenarios"]), placed)
            counts = {stratum: sum(
                1 for value in row["planned_ineligible_scenarios"].values()
                if value == stratum) for stratum in strata}
            self.assertEqual(counts, {stratum: placed // len(strata)
                                      for stratum in strata},
                             "%s: the quota must be stratified, not clustered" % motif)
            self.assertEqual(
                row["admitted_eligible_lower_bound"],
                row["candidates"] - refusals - placed)
            self.assertGreaterEqual(row["admitted_eligible_lower_bound"], 128,
                                    "%s: the arithmetic must reach the floor" % motif)

            joint = set()
            for scenario_id, stratum in sorted(
                    row["planned_ineligible_scenarios"].items()):
                candidate = next(c for c in generation.candidates
                                 if c["scenario_id"] == scenario_id)
                self.assertEqual(
                    candidate["generation"]["planned_ineligible_stratum"], stratum)
                self.assertFalse(
                    packet.candidate_is_eligible(candidate, chosen_cut_of(candidate)),
                    "%s: a PLANNED ineligible the derived predicate admits would take "
                    "a retained slot the arithmetic already spent" % scenario_id)
                self.assertNotIn(scenario_id, retained_ids)
                values = generator._axis_values(candidate)
                key = "|".join(str(values[name])
                               for name in generator.CENSUS_JOINT_AXES)
                self.assertNotIn(key, joint,
                                 "%s: two planned ineligibles in one joint census "
                                 "stratum would empty it" % motif)
                joint.add(key)

        # The whole plan, as one number: 6 motifs x 12 = 72 planned ineligibles, and
        # every one of them is outside the retained 768.
        planned = {scenario_id
                   for row in generation.plan["per_motif"].values()
                   for scenario_id in row["planned_ineligible_scenarios"]}
        self.assertEqual(len(planned), len(authority.MOTIFS) * quota)
        self.assertEqual(planned & retained_ids, set())
        self.assertEqual(len(generation.candidates), 960)
        self.assertEqual(len(retained_ids), 768)

    def test_bc09_adversarial_thirty_three_unplanned_refusals_refuse_the_plan(self):
        """§2.3 / §4 W3 (the e=33 red, banked BUILD material): a shape whose unplanned
        refusals alone exceed the floor margin cannot honestly reach 128, so the
        GENERATION PLAN itself is refused — `BUILD_GENERATION_PLAN_REFUSED`, named,
        before any selection runs.  e=32 is admitted at the boundary; e=33 is not.

        RED-FIRST, recorded 2026-08-16.  BROKEN VARIANT: an in-memory spec whose
        `refusal_margin` is widened to 33, so e=33 no longer exceeds it.  This witness
        FAILED:

            AssertionError: BuildGenerationRefusal not raised
        """
        generator, authority, packet = cohort_modules()
        honest = packet.candidate_is_eligible

        def refuse_first(count):
            """Make exactly `count` candidates of the FIRST motif fail the derived
            predicate — an UNPLANNED refusal class, counted in `e`."""
            victims = {"SCENARIO.BUILD.0.%03d" % index for index in range(count)}

            def predicate(candidate, cut_id):
                if candidate["scenario_id"] in victims:
                    return False
                return honest(candidate, cut_id)
            return predicate

        try:
            packet.candidate_is_eligible = refuse_first(33)
            with self.assertRaises(generator.BuildGenerationRefusal) as refusal:
                generator.generate_cohort()
        finally:
            packet.candidate_is_eligible = honest
        message = str(refusal.exception)
        self.assertIn(authority.BUILD_GENERATION_PLAN_REFUSED, message)
        self.assertIn("e=33", message)
        self.assertIn("32", message)
        self.assertIn("CORRECTION_RESTORATION", message)

        # DISCRIMINATING: the refusal is the MARGIN, not the mere presence of
        # refusals.  At e=32 the plan is admitted and the arithmetic still reaches
        # the floor: 160 - 32 - max(0, min(12, 32-32)) = 128.
        self.assertEqual(max(0, min(12, 32 - 32)), 0)
        self.assertEqual(160 - 32 - 0, 128)
        spec, _digest = authority.build_generator_spec()
        self.assertEqual(spec["refusal_margin"],
                         spec["candidate_count_per_motif"]
                         - spec["retained_count_per_motif"])

    def test_bc10_adversarial_an_illegal_event_program_faults_with_the_reducer_code(self):
        """§2.7 / §4 W5 (supplement): an ILLEGAL event program does not quietly produce
        a smaller population — the generation replay gate faults at the offending step
        and the fault carries THE REDUCER'S OWN CODE, so the refusal names what the
        reducers actually said.

        RED-FIRST, recorded 2026-08-16.  BROKEN VARIANT: an in-memory
        `ProgramReplay.apply` with the expected-result-code arm removed, so the illegal
        step is absorbed and the program continues.  This witness FAILED:

            AssertionError: BuildGenerationRefusal not raised
        """
        generator, _authority, _packet = cohort_modules()
        replay = generator.ProgramReplay()

        # The illegal step: completing an obligation that was never opened.  BOTH
        # frozen reducers answer OBLIGATION_NOT_OPEN, so this is a legality fault and
        # not a dual-reducer disagreement — the witness pins which one it is.
        illegal = generator._complete_obligation(replay.reference, "OBL.NEVER.OPENED")
        reference_code = reference.reference_apply(
            copy.deepcopy(replay.reference), copy.deepcopy(illegal))[1]
        oracle_code = oracle.oracle_apply(
            copy.deepcopy(replay.oracle), copy.deepcopy(illegal))[1]
        self.assertEqual(reference_code, "OBLIGATION_NOT_OPEN")
        self.assertEqual(oracle_code, reference_code,
                         "the reducers AGREE, so this is a legality fault")

        with self.assertRaises(generator.BuildGenerationRefusal) as refusal:
            replay.apply(illegal, "APPLIED", "W5_SUPPLEMENT")
        message = str(refusal.exception)
        self.assertIn(generator.BUILD_PROGRAM_STEP_CODE_MISMATCH, message)
        self.assertIn("OBLIGATION_NOT_OPEN", message,
                      "the fault must carry the REDUCER'S OWN code")
        self.assertIn("complete_obligation", message)
        self.assertIn("W5_SUPPLEMENT", message)

        # The refused step left NOTHING behind: no event, no code, no snapshot.
        self.assertEqual(replay.events, [])
        self.assertEqual(replay.codes, [])
        self.assertEqual(len(replay.snapshots), 1)

        # DISCRIMINATING: the same gate ADMITS the legal construction, and the three
        # checks are all live — dual-reducer byte equality, the expected code, and the
        # legality frontier cross-check.
        legal = generator._open_obligation(
            replay.reference, "OBL.W5", due_at=common.T0)
        replay.apply(legal, "APPLIED", "W5_SUPPLEMENT")
        self.assertEqual(replay.codes, ["APPLIED"])
        self.assertEqual(common.canonical_json(replay.reference),
                         common.canonical_json(replay.oracle))
        self.assertEqual(len(replay.frontier_legality), 1)

    def test_bc11_positive_the_committed_identity_equals_the_recomputed_root(self):
        """§3 / §4 W8: the COMMITTED identity block in
        `MBCX-01-BUILD-COHORT-GENERATOR-V1.json` equals the identity RECOMPUTED from a
        live generation — root, total and ordered-membership digest — and the spec the
        authority reads is that committed artifact, canonical bytes and all.

        RED-FIRST, recorded 2026-08-16.  BROKEN VARIANT: a temporary copy of the
        committed artifact whose identity root drifts by ONE character.  This witness
        FAILED:

            AssertionError: Lists differ: ['BUILD_RETAINED_COHORT_AUTHORITY_INVALID'] != []
            First list contains 1 additional elements.
            First extra element 0: 'BUILD_RETAINED_COHORT_AUTHORITY_INVALID'
        """
        _generator, authority, _packet = cohort_modules()
        generation = build_generation()
        context = generation.context

        self.assertEqual(authority.validate_committed_identity(context), [])
        committed = authority.committed_identity()
        self.assertEqual(committed["schema_id"],
                         authority.BUILD_COHORT_IDENTITY_SCHEMA_ID)
        self.assertEqual(committed["retained_total"], 768)
        self.assertEqual(committed["retained_set_root"],
                         authority.retained_set_root(context))
        self.assertEqual(committed["retained_scenario_ids_hash"], packets.sha384(
            authority.retained_membership_scenario_ids(context)))
        self.assertEqual(committed,
                         authority.recomputed_identity(context))

        # The ARTIFACT is the spec source, read on every call, and its digest is what
        # rides provenance.
        spec, digest = authority.build_generator_spec()
        self.assertEqual(spec["generator_id"], authority.BUILD_GENERATOR_ID)
        self.assertEqual(digest, packets.sha384(spec))
        self.assertEqual(generation.provenance["generator_digest"], digest)
        self.assertEqual(generation.provenance["generator_id"],
                         authority.BUILD_GENERATOR_ID)
        path = authority.ROOT / authority.BUILD_COHORT_SPEC_ARTIFACT
        raw = path.read_bytes().replace(b"\r\n", b"\n")
        self.assertEqual(raw, authority.canonical_artifact_bytes(spec),
                         "the committed artifact must BE the canonical serialization")
        self.assertEqual(json.loads(raw.decode("utf-8")), spec)

        # NON-CIRCULARITY, asserted rather than assumed: the identity block is a digest
        # of the CANDIDATES, and no candidate carries the generator digest, so writing
        # the block into the spec cannot move the root it records.
        self.assertNotIn("generator_digest", json.dumps(committed))
        self.assertNotIn("provenance_hash", json.dumps(committed))
        for candidate in context.retained_candidates[:8]:
            blob = common.canonical_json(candidate).decode("utf-8")
            self.assertNotIn(digest, blob)
            self.assertNotIn(generation.provenance["provenance_hash"], blob)

    def test_bc12_adversarial_a_drifted_generator_spec_artifact_is_refused(self):
        """§3 / §4 W8 (the red half): every way the committed spec artifact can drift
        is refused by name — a drifted identity root, a non-canonical serialization, a
        foreign generator id, a missing identity block, and a changed BUILD-time
        constant (which moves the digest and therefore fails the provenance gate).

        RED-FIRST, recorded 2026-08-16.  BROKEN VARIANT: `load_build_cohort_spec`
        replaced in memory by the PRE-REGISTRATION in-code constant, so the artifact is
        never read and every drift is invisible.  This witness FAILED:

            AssertionError: Lists differ: [] != ['BUILD_RETAINED_COHORT_AUTHORITY_INVALID']
            Second list contains 1 additional elements.
            First extra element 0: 'BUILD_RETAINED_COHORT_AUTHORITY_INVALID'
        """
        _generator, authority, _packet = cohort_modules()
        generation = build_generation()
        original_root = authority.ROOT
        spec, digest = authority.build_generator_spec()

        def with_artifact(document, *, canonical=True):
            """Point the authority at a TEMPORARY artifact and return the module."""
            directory = tempfile.mkdtemp(prefix="mbcx01-build-cohort-spec-")
            self.addCleanup(shutil.rmtree, directory, True)
            payload = (authority.canonical_artifact_bytes(document) if canonical
                       else (json.dumps(document, indent=2) + "\n").encode("utf-8"))
            (Path(directory) / authority.BUILD_COHORT_SPEC_ARTIFACT).write_bytes(payload)
            authority.ROOT = Path(directory)
            self.addCleanup(setattr, authority, "ROOT", original_root)
            return authority

        try:
            # 1. DRIFTED IDENTITY: the committed root is not the one the population
            #    reproduces.
            drifted = copy.deepcopy(spec)
            root = drifted["committed_identity"]["retained_set_root"]
            drifted["committed_identity"]["retained_set_root"] = (
                ("B" if root[0] != "B" else "C") + root[1:])
            with_artifact(drifted)
            self.assertEqual(
                authority.validate_committed_identity(generation.context),
                [authority.BUILD_RETAINED_COHORT_AUTHORITY_INVALID])

            # 2. NON-CANONICAL SERIALIZATION: same parsed document, different bytes.
            with_artifact(copy.deepcopy(spec), canonical=False)
            with self.assertRaises(authority.BuildCohortAuthorityError) as refusal:
                authority.build_generator_spec()
            self.assertIn("SOURCE_GENERATOR_INVALID", str(refusal.exception))

            # 3. FOREIGN generator id.
            foreign = copy.deepcopy(spec)
            foreign["generator_id"] = "GENERATOR.R13.SYNTHETIC"
            with_artifact(foreign)
            with self.assertRaises(authority.BuildCohortAuthorityError):
                authority.build_generator_spec()

            # 4. MISSING identity block.
            headless = copy.deepcopy(spec)
            headless.pop("committed_identity")
            with_artifact(headless)
            with self.assertRaises(authority.BuildCohortAuthorityError):
                authority.build_generator_spec()
            self.assertEqual(
                authority.validate_build_source_provenance(
                    generation.candidates, generation.provenance),
                ["SOURCE_GENERATOR_INVALID"])

            # 5. A CHANGED BUILD-TIME CONSTANT moves the digest, so the provenance
            #    manifest this population was generated under no longer validates.
            retuned = copy.deepcopy(spec)
            retuned["planned_ineligible_quota_k"] = 11
            with_artifact(retuned)
            changed_spec, changed_digest = authority.build_generator_spec()
            self.assertNotEqual(changed_digest, digest)
            self.assertEqual(changed_spec["planned_ineligible_quota_k"], 11)
            self.assertEqual(
                authority.validate_build_source_provenance(
                    generation.candidates, generation.provenance),
                ["SOURCE_PROVENANCE_INVALID"])
        finally:
            authority.ROOT = original_root

        # And the real artifact is still the one on disk, unharmed.
        self.assertEqual(authority.build_generator_spec(), (spec, digest))
        self.assertEqual(authority.validate_build_source_provenance(
            generation.candidates, generation.provenance), [])

    # ---- W14, the four registration-totality levels -------------------------

    @staticmethod
    def bundle_verifier():
        """Import `verify-build-bundle.py` BY PATH (its name is not an identifier)."""
        path = Path(__file__).resolve().parent / "verify-build-bundle.py"
        spec = importlib.util.spec_from_file_location(
            "mbcx01_build_bundle_verifier", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_bc13_positive_registration_totality_holds_at_all_four_levels(self):
        """§3 / §4 W14: the four-level registration totality the BUNDLE enforces —
        (a) glob-vs-registration two-way for modules and test modules, (b) every
        REQUIRED artifact registered for pinning and pinned, (c) the governed artifact
        namespace derived from the UNION OF THE REGISTRATION LISTS and present on
        disk, (d) every production module named by a ledger row that states a
        behaviour and carries a witness.  This witness runs the bundle's own check.

        RED-FIRST, recorded 2026-08-16.  BROKEN VARIANT: the registration lists AS THEY
        WERE before this task — the three cohort modules and the cohort suite on disk and
        in git, named by no list.  This witness FAILED:

            VerificationFailure: W14_MODULE_GLOB_VS_REGISTRATION_MISMATCH: on disk but
            registered nowhere=['mbcx01_build_cohort_authority.py',
            'mbcx01_build_cohort_generator.py', 'mbcx01_build_cohort_packet.py'];
            registered but not on disk=[]
        """
        bundle = self.bundle_verifier()
        section = bundle.check_registration_totality()
        self.assertEqual(section["status"], "PASS")

        # (a) the globs and the lists agree, both directions, and the cohort files
        #     are on BOTH sides of that agreement.
        for name in ("mbcx01_build_cohort_authority.py",
                     "mbcx01_build_cohort_generator.py",
                     "mbcx01_build_cohort_packet.py"):
            self.assertIn(name, bundle.BUILD_MODULES)
            self.assertTrue((Path(__file__).resolve().parent / name).is_file())
        self.assertIn("test_mbcx01_build_cohort", bundle.BUILD_TEST_MODULES)
        self.assertEqual(section["level_a_module_glob_two_way"],
                         len(set(bundle.BUILD_MODULES)
                             | {n for n in bundle.BUILD_FIXTURE_SUPPORT
                                if n.endswith(".py")}
                             | set(bundle.BUILD_RED_WITNESS_PROBES)))
        self.assertEqual(section["level_a_test_glob_two_way"],
                         len(bundle.BUILD_TEST_MODULES))

        # (b) REQUIRED is a SUBSET of the pinned subject set, never equal to it: the
        #     manifest also pins documents and frozen contracts this bundle does not
        #     import. The check states which, rather than claiming an equality the
        #     manifest does not have.
        self.assertTrue(section["level_b_pin_manifest_is_subset_not_equal"])
        self.assertIn(bundle.BUILD_COHORT_SPEC_ARTIFACT, bundle.REQUIRED)
        self.assertIn("test_mbcx01_build_cohort.py", bundle.REQUIRED)

        # (b, rider) the pin generator's subject list is PARSED, and a parser that
        # scoops English prose out of a comment would enlarge exactly the side that
        # hides a missing registration.  Every parsed entry must be a real file.
        # RED, recorded 2026-08-16, against the pre-fix parser (no comment stripping):
        #     non-existent entries: ["s committed generator spec, its three\n    #
        #     production siblings and its witness suite. verify-build-bundle.py"]
        parsed = self.pinning_list(bundle)
        self.assertEqual(
            [name for name in parsed
             if not (Path(__file__).resolve().parent / name).is_file()], [],
            "the pin generator's subject list must parse to real paths only")
        for name in ("MBCX-01-BUILD-COHORT-GENERATOR-V1.json",
                     "mbcx01_build_cohort_authority.py",
                     "mbcx01_build_cohort_generator.py",
                     "mbcx01_build_cohort_packet.py",
                     "test_mbcx01_build_cohort.py"):
            self.assertIn(name, parsed)

        # (c) the namespace is DERIVED from the lists, never globbed.
        self.assertEqual(section["level_c_derivation"],
                         "UNION_OF_THE_REGISTRATION_LISTS_NEVER_A_GLOB")
        self.assertGreaterEqual(section["level_c_governed_artifacts"],
                                len(set(bundle.REQUIRED)))

        # (d) every production module is named by a row that states a behaviour, and
        #     the half this check CANNOT enforce is declared, not implied.
        self.assertGreaterEqual(section["level_d_modules_covered"],
                                len(bundle.BUILD_MODULES))
        self.assertIn("REPLACEMENT_SENSITIVITY_IS_NOT_MECHANICALLY_CHECKED",
                      section["level_d_nontriviality_not_enforced"])

    def test_bc14_adversarial_every_registration_totality_level_fails_by_name(self):
        """§3 / §4 W14 (the red half): each of the four levels is driven to failure
        with a perturbed registration list and must fail with ITS OWN name.  A totality
        check nobody has seen fail is a claim, not a check.

        RED-FIRST, recorded 2026-08-16.  BROKEN VARIANT: `check_registration_totality`
        replaced in memory by a stub that always returns PASS.  This witness FAILED:

            AssertionError: VerificationFailure not raised
        """
        bundle = self.bundle_verifier()
        ledger = bundle.load_json(bundle.LEDGER)

        def refusal(**overrides):
            with self.assertRaises(bundle.VerificationFailure) as caught:
                bundle.check_registration_totality(**overrides)
            return str(caught.exception)

        # (a) a module on disk that no list names — the exact shape the cohort slice
        #     landed in — and a listed module that is not on disk.
        self.assertIn(bundle.W14_MODULE_GLOB_MISMATCH, refusal(
            build_modules=[name for name in bundle.BUILD_MODULES
                           if "cohort" not in name]))
        self.assertIn("mbcx01_build_cohort_authority.py", refusal(
            build_modules=[name for name in bundle.BUILD_MODULES
                           if "cohort" not in name]))
        self.assertIn(bundle.W14_MODULE_GLOB_MISMATCH, refusal(
            build_modules=list(bundle.BUILD_MODULES) + ["mbcx01_build_phantom.py"]))
        self.assertIn(bundle.W14_TEST_GLOB_MISMATCH, refusal(
            test_modules=[name for name in bundle.BUILD_TEST_MODULES
                          if name != "test_mbcx01_build_cohort"]))

        # (b) REQUIRED but not registered for pinning, and REQUIRED-and-committed but
        #     not actually pinned.
        self.assertIn(bundle.W14_NOT_REGISTERED_FOR_PINNING, refusal(
            required=list(bundle.REQUIRED) + ["MBCX-01-BUILD-NEVER-REGISTERED.json"]))
        # The probe file must be on disk and unpinned in BOTH legitimate layouts.  The
        # pin manifest itself is the one file with that property everywhere: committed
        # (so it exists at the governing commit in a git work tree) yet deliberately
        # never a subject of itself, and EXPORTED into a pinned reconstruction.  The
        # previous probe (a council-packet .md) existed only in the work tree, so this
        # witness refused a RIGHT reconstruction — caught by the first pinned clean-room
        # run after it landed (2026-08-16, cohort-BUILD r1 assembly; the pre-fix red is
        # the clean-room failure banked in cleanroom-postfold.out).
        older = bundle.PIN_MANIFEST
        self.assertTrue((Path(__file__).resolve().parent / older).is_file())
        message = refusal(
            required=list(bundle.REQUIRED) + [older],
            registered_for_pinning=self.pinning_list(bundle) + [older])
        self.assertIn(bundle.W14_UNPINNED_AT_GOVERNING_COMMIT, message)
        self.assertIn(older, message)

        # (c) a governed artifact named by a list and absent from disk.  It is not a
        #     `.py` file, so it passes level (a) and reaches level (c) — which is the
        #     point: the namespace is wider than the module glob.
        self.assertIn(bundle.W14_ARTIFACT_ABSENT_FROM_DISK, refusal(
            fixture_support=list(bundle.BUILD_FIXTURE_SUPPORT)
            + ["MBCX-01-BUILD-GHOST.fixture.json"]))

        # (d) the three level-(d) failures: an unregistered module named by a row, a
        #     row that claims a module without stating a behaviour, and a production
        #     module no row names at all.
        unknown = copy.deepcopy(ledger)
        row = sorted(unknown["invariants"])[0]
        unknown["invariants"][row]["modules"] = ["mbcx01_build_phantom.py"]
        self.assertIn(bundle.W14_UNKNOWN_MODULE_IN_LEDGER,
                      refusal(ledger_document=unknown))

        silent = copy.deepcopy(ledger)
        named = next(name for name, value in sorted(silent["invariants"].items())
                     if value.get("modules"))
        silent["invariants"][named]["requirement"] = "   "
        self.assertIn(bundle.W14_ROW_WITHOUT_BEHAVIOUR,
                      refusal(ledger_document=silent))

        stripped = copy.deepcopy(ledger)
        for value in stripped["invariants"].values():
            value.pop("modules", None)
        message = refusal(ledger_document=stripped)
        self.assertIn(bundle.W14_MODULE_WITHOUT_WITNESS, message)
        self.assertIn("mbcx01_build_cohort_generator.py", message)

    def test_bc17_adversarial_a_stray_pin_only_subject_fails_by_name(self):
        """§3 W14 level (b), the constrained difference: a subject that is PINNED but is
        neither REQUIRED nor named in `PIN_MANIFEST_SUBJECTS_BEYOND_REQUIRED` is refused
        by name, through EITHER pin source (the generator's subject list and the
        committed manifest).  Level (b) stays a SUBSET relation — equality would refuse a
        right reconstruction, which deliberately pins the frozen r13.2 layer — so the
        difference is DECLARED rather than free.

        RED-FIRST, recorded 2026-08-16 (cohort-BUILD council r1, seat 3's executed
        injection; driver adjudication 2).  BROKEN VARIANT: the pre-fix bytes of
        `verify-build-bundle.py`, sha256
        1f9ebbb98d2c7fe0fcce67189aeae5d8d64bcef77f9422185c4b0c8dd5016bec, where the
        difference was reported and not constrained.  A synthetic pin-only subject
        injected into the manifest LEFT THE SECTION AT PASS:

            ---- stray in the committed pin manifest ----
            RESULT status                              : PASS
            level_b_pin_manifest_is_subset_not_equal(n): 31
              stray inside that reported difference    : True

        and the `pin_manifest_document=` seam did not exist at all:

            TypeError: check_registration_totality() got an unexpected keyword
            argument 'pin_manifest_document'
        """
        bundle = self.bundle_verifier()
        stray = "MBCX-01-BUILD-STRAY-PIN-ONLY-SUBJECT.md"
        self.assertNotIn(stray, bundle.REQUIRED)
        self.assertNotIn(stray, bundle.PIN_MANIFEST_SUBJECTS_BEYOND_REQUIRED)

        # The difference is real and non-empty (seat 2's half: equality is WRONG here),
        # and every member of it is declared.
        section = bundle.check_registration_totality()
        difference = section["level_b_pin_manifest_is_subset_not_equal"]
        self.assertTrue(difference)
        self.assertEqual(sorted(set(difference)
                                - set(bundle.PIN_MANIFEST_SUBJECTS_BEYOND_REQUIRED)), [])
        self.assertEqual(section["level_b_declared_pins_beyond_required"],
                         sorted(bundle.PIN_MANIFEST_SUBJECTS_BEYOND_REQUIRED))

        def refusal(**overrides):
            with self.assertRaises(bundle.VerificationFailure) as caught:
                bundle.check_registration_totality(**overrides)
            return str(caught.exception)

        # (1) stray in the COMMITTED PIN MANIFEST — seat 3's literal shape.
        manifest = json.loads(
            (bundle.ROOT / bundle.PIN_MANIFEST).read_text(encoding="utf-8"))
        strayed = copy.deepcopy(manifest)
        row = copy.deepcopy(strayed["subjects"][0])
        row["path"] = stray
        strayed["subjects"].append(row)
        message = refusal(pin_manifest_document=strayed)
        self.assertIn(bundle.W14_PIN_SUBJECT_OUTSIDE_DECLARED_SET, message)
        self.assertIn(stray, message)

        # (2) stray in the GENERATOR's subject list — the other pin source, which is
        #     what the NEXT regeneration would write into the manifest.
        message = refusal(registered_for_pinning=self.pinning_list(bundle) + [stray])
        self.assertIn(bundle.W14_PIN_SUBJECT_OUTSIDE_DECLARED_SET, message)
        self.assertIn(stray, message)

        # (3) it is an ALLOWLIST and not a mute button: the SAME strayed manifest is
        #     admitted once the subject is DECLARED, and the declaration is the only
        #     thing that changed.
        original = bundle.PIN_MANIFEST_SUBJECTS_BEYOND_REQUIRED
        try:
            bundle.PIN_MANIFEST_SUBJECTS_BEYOND_REQUIRED = tuple(original) + (stray,)
            section = bundle.check_registration_totality(pin_manifest_document=strayed)
        finally:
            bundle.PIN_MANIFEST_SUBJECTS_BEYOND_REQUIRED = original
        self.assertEqual(section["status"], "PASS")
        self.assertIn(stray, section["level_b_declared_pins_beyond_required"])
        self.assertIn(stray, section["level_b_pin_manifest_is_subset_not_equal"])

    def test_bc15_adversarial_ghost_fact_cannot_reach_the_serving_boundary(self):
        """FOLD 1(c) (cohort-BUILD r1 R5): a ghost FACT row — evidence with NO journal
        ancestry — inside a REBUILT, self-consistent candidate/provenance/context is
        refused by the SERVING boundary, not merely by a validator nobody calls.

        RED-FIRST, recorded 2026-08-16 against the pre-fix bytes
        (`mbcx01_build_cohort_packet.py` at e768725): `validate_build_manifest` named
        the ghost, but `build_scoring_fixture_for_candidate` BUILT it, the ghost object
        was in the served BC A0 packet and `render_all_six_nodes` ADMITTED.  This
        witness FAILED:

            AssertionError: BuildCohortPacketError not raised
        """
        _generator, _authority, packet = cohort_modules()
        ghost_id = "FACT.GHOST.NO.JOURNAL"

        def plant_ghost(candidates, generation):
            twin = generation.context.retained_candidates[0]
            scenario_id, cut_id = twin["scenario_id"], twin["chosen_cut_id"]
            row = next(item for item in candidates
                       if item["scenario_id"] == scenario_id)
            world = row["canonical_world_by_cut"][cut_id]
            world.append({"object_id": ghost_id, "object_kind": "FACT",
                          "fields": {"subject_id": "SUB.GHOST",
                                     "predicate_id": "PRED.GHOST",
                                     "value_code": "VALUE.GHOST",
                                     "valid_from": common.T0, "valid_to": None},
                          "source_event_ids": []})
            world.sort(key=lambda item: item["object_id"].encode("utf-8"))
            selected = set(row["bc_selected_object_ids_by_cut"][cut_id])
            selected.add(ghost_id)
            row["bc_selected_object_ids_by_cut"][cut_id] = sorted(
                selected, key=lambda value: value.encode("utf-8"))
            return scenario_id

        context, victim, cut_id = serve_mutated_retained_candidate(plant_ghost)
        manifest = packet.build_manifest_for_candidate(victim, cut_id, context=context)

        # The population is self-consistent around the ghost: the rebuilt provenance
        # and the fresh context both ISSUE authority for this candidate, so nothing
        # upstream of the serving boundary refuses it.
        self.assertEqual(
            packet.observation_world_rows(
                victim["observation_authority_by_cut"][cut_id]),
            [row for row in manifest["canonical_world"]
             if row["object_kind"] == "OBSERVATION"])
        self.assertIn(ghost_id, [row["object_id"] for row in manifest["canonical_world"]])

        # THE SERVING BOUNDARY: the fixture builder itself refuses, by name.
        with self.assertRaises(packet.BuildCohortPacketError) as refusal:
            packet.build_scoring_fixture_for_candidate(
                victim, "BC", context=context, cut_id=cut_id)
        self.assertIn(packet.BUILD_FACT_ROW_WITHOUT_JOURNAL_ANCESTRY,
                      str(refusal.exception))

        # And the six-node render INHERITS the refusal: named in `errors`, detailed in
        # `refusal_detail`, never an escaping traceback and never an admission.
        record = packet.render_all_six_nodes(victim, context=context, cut_id=cut_id)
        self.assertFalse(record["admitted"])
        self.assertEqual(record["errors"], [packet.BUILD_SCORER_INPUT_INVALID])
        self.assertIn(packet.BUILD_FACT_ROW_WITHOUT_JOURNAL_ANCESTRY,
                      record["refusal_detail"])
        self.assertEqual(record["served_input_hashes"], {})

        # DISCRIMINATING: the validator saw the ghost all along — the fold is that the
        # SERVING path now runs it.  And the honest twin still serves.
        self.assertIn(packet.BUILD_FACT_ROW_WITHOUT_JOURNAL_ANCESTRY,
                      packet.validate_build_manifest(manifest, victim, cut_id,
                                                     context=context))
        honest_context = build_generation().context
        honest = honest_context.retained_candidates[0]
        self.assertTrue(packet.render_all_six_nodes(
            honest, context=honest_context)["admitted"])

    def test_bc16_adversarial_a_non_derived_observation_record_cannot_serve(self):
        """FOLD 1(a)+(b) (cohort-BUILD r1 R6): an observation authority record whose
        `code` was replaced with the literal gold action id and REHASHED — rows and both
        representations rebuilt consistently — is refused at the serving boundary,
        because the record is RE-DERIVED from its own stored projection instead of being
        checked for self-consistency.

        RED-FIRST, recorded 2026-08-16 against the pre-fix bytes
        (`mbcx01_build_cohort_packet.py` at e768725): the record passed
        `validate_observation_authority_record`, `validate_build_manifest` returned
        `[]`, the gold action id served as the observation and all six renders
        ADMITTED.  This witness FAILED:

            AssertionError: BuildCohortPacketError not raised
        """
        generator, _authority, packet = cohort_modules()

        def forge_observation(candidates, generation):
            twin = next(row for row in generation.context.retained_candidates
                        if row["gold_action_id_by_cut"][row["chosen_cut_id"]])
            scenario_id, cut_id = twin["scenario_id"], twin["chosen_cut_id"]
            row = next(item for item in candidates
                       if item["scenario_id"] == scenario_id)
            gold = row["gold_action_id_by_cut"][cut_id]
            record = row["observation_authority_by_cut"][cut_id]
            record["code"] = gold
            for ordinal, observation_row in enumerate(record["rows"]):
                observation_row["code"] = "%s.%d" % (gold, ordinal)
            record["record_hash"] = packet.observation_record_hash(record)
            row["observation_by_cut"][cut_id] = (
                packet.observation_manifest_representation(record))
            world = [item for item in row["canonical_world_by_cut"][cut_id]
                     if item["object_kind"] != "OBSERVATION"]
            world += packet.observation_world_rows(record)
            world.sort(key=lambda item: item["object_id"].encode("utf-8"))
            row["canonical_world_by_cut"][cut_id] = world
            return scenario_id

        context, victim, cut_id = serve_mutated_retained_candidate(forge_observation)
        record = victim["observation_authority_by_cut"][cut_id]
        gold = victim["gold_action_id_by_cut"][cut_id]
        self.assertEqual(record["code"], gold)

        # The forged record is INTERNALLY consistent: shape, cardinality, projection
        # hash and record hash all agree, so self-consistency is not the discriminator.
        self.assertTrue(packet.validate_observation_authority_record(record))
        fresh = generator.derive_observation_authority(
            victim["scenario_id"], cut_id, record["projection"])
        self.assertNotEqual(fresh["code"], record["code"],
                            "the forgery must actually disagree with the derivation, "
                            "or this witness proves nothing")

        # THE SERVING BOUNDARY: re-derivation from the record's own stored projection.
        with self.assertRaises(packet.BuildCohortPacketError) as refusal:
            packet.build_scoring_fixture_for_candidate(
                victim, "BC", context=context, cut_id=cut_id)
        self.assertIn(packet.BUILD_OBSERVATION_REPRESENTATION_DIVERGENT,
                      str(refusal.exception))

        # The ADMISSION path (no context, no scenario authority — §2.5 renders before
        # selection exists) runs the SAME two bindings: they are pure and cheap, so the
        # declared split costs the observation nothing.
        with self.assertRaises(packet.BuildCohortPacketError) as admission:
            packet.build_scoring_fixture_for_candidate(victim, "BC", cut_id=cut_id)
        self.assertIn(packet.BUILD_OBSERVATION_REPRESENTATION_DIVERGENT,
                      str(admission.exception))

        record_six = packet.render_all_six_nodes(victim, context=context, cut_id=cut_id)
        self.assertFalse(record_six["admitted"])
        self.assertEqual(record_six["errors"], [packet.BUILD_SCORER_INPUT_INVALID])
        self.assertIn(packet.BUILD_OBSERVATION_REPRESENTATION_DIVERGENT,
                      record_six["refusal_detail"])

        # The manifest validator names it too — the derivation binding lives THERE and
        # the serving boundary runs it.
        manifest = packet.build_manifest_for_candidate(victim, cut_id, context=context)
        self.assertEqual(
            packet.validate_build_manifest(manifest, victim, cut_id, context=context),
            [packet.BUILD_OBSERVATION_REPRESENTATION_DIVERGENT])

        # FOLD 1(b): the derivation law lives in the PACKET sibling — the side of the
        # import arrow the serving path can reach — and the generator uses THAT law.
        self.assertIs(generator.derive_observation_authority,
                      packet.derive_observation_authority)
        self.assertEqual(generator.OBSERVATION_ALLOWED_FIELDS,
                         packet.OBSERVATION_ALLOWED_FIELDS)
        # The moved law keeps its own allowlist refusal, under the packet's typed
        # failure: a projection that is not exactly the allowlist cannot reach the rule.
        self.assertEqual(generator.BUILD_OBSERVATION_PROJECTION_LEAK,
                         packet.BUILD_OBSERVATION_PROJECTION_LEAK)
        with self.assertRaises(packet.BuildCohortPacketError) as leak:
            packet.derive_observation_authority(
                victim["scenario_id"], cut_id,
                dict(record["projection"], gold_action_id=gold))
        self.assertIn(packet.BUILD_OBSERVATION_PROJECTION_LEAK, str(leak.exception))

        # DISCRIMINATING: a candidate whose stored projection is a fiction is refused
        # the same way, so the binding is to REALITY (the replayed state) and not only
        # to the record's own arithmetic.
        def falsify_projection(candidates, generation):
            twin = generation.context.retained_candidates[1]
            scenario_id, cut = twin["scenario_id"], twin["chosen_cut_id"]
            row = next(item for item in candidates
                       if item["scenario_id"] == scenario_id)
            stored = row["observation_authority_by_cut"][cut]["projection"]
            projection = dict(stored, fact_row_count=stored["fact_row_count"] + 7)
            rebuilt = generator.derive_observation_authority(scenario_id, cut, projection)
            row["observation_authority_by_cut"][cut] = rebuilt
            row["observation_by_cut"][cut] = (
                packet.observation_manifest_representation(rebuilt))
            world = [item for item in row["canonical_world_by_cut"][cut]
                     if item["object_kind"] != "OBSERVATION"]
            world += packet.observation_world_rows(rebuilt)
            world.sort(key=lambda item: item["object_id"].encode("utf-8"))
            row["canonical_world_by_cut"][cut] = world
            return scenario_id

        other_context, other, other_cut = serve_mutated_retained_candidate(
            falsify_projection)
        self.assertTrue(packet.validate_observation_authority_record(
            other["observation_authority_by_cut"][other_cut]))
        with self.assertRaises(packet.BuildCohortPacketError) as second:
            packet.build_scoring_fixture_for_candidate(
                other, "BC", context=other_context, cut_id=other_cut)
        self.assertIn(packet.BUILD_OBSERVATION_REPRESENTATION_DIVERGENT,
                      str(second.exception))

    def test_bc18_red_the_retained_population_carries_distinct_gold_answers(self):
        """cohort-BUILD r1 FOLD 2(a)/(b), class POPULATION_ANSWER_KEY_DEGENERACY: the
        retained population's ANSWER KEY varies with the row.  Three halves: the golds
        are distinct one-per-row (the modal gold covers exactly ONE retained row, so a
        constant-answer heuristic scores 1/768 rather than at ceiling), the CENSUS
        reports the count with its DECLARED floor, and a population whose golds are
        forced constant is refused BY NAME.

        RED-FIRST against the pre-fix bytes at `af1cc4f`
        (`mbcx01_build_cohort_generator.py`,
        sha256 7eb5441245472f5f1f71defef67edae076c0b78a8f77b33bb353d0e998a2e156),
        where `TARGET_OBLIGATION_ID` was the constant `"OBL.TARGET"` and
        `action_id = sha256([scope, obligation_id])` therefore produced ONE gold for
        all 768 rows.  This witness FAILED:

            AssertionError: 1 != 768 : the retained golds must be one-per-row
        """
        generator, _authority, _packet = cohort_modules()
        generation = build_generation()
        retained = generation.context.retained_candidates
        census = generation.census

        # (1) the population itself — recomputed here, not read off the census.
        golds = {}
        for candidate in retained:
            gold = candidate["gold_action_id_by_cut"][candidate["chosen_cut_id"]]
            self.assertIsNotNone(gold, "a retained row must have a gold")
            golds.setdefault(gold, []).append(candidate["scenario_id"])
        self.assertEqual(len(golds), len(retained),
                         "the retained golds must be one-per-row")
        modal = max(golds, key=lambda key: len(golds[key]))
        self.assertEqual(
            len(golds[modal]), 1,
            "a CONSTANT-ANSWER heuristic must not cover more than one retained row")
        # the identity is per-scenario BY CONSTRUCTION, and it is the target that varies
        for candidate in retained[:8]:
            cut_id = candidate["chosen_cut_id"]
            expected = generator.target_obligation_id(candidate["scenario_id"])
            self.assertEqual(
                candidate["canonical_state_by_cut"][cut_id]["target_obligation_id"],
                expected)
            self.assertEqual(candidate["gold_action_id_by_cut"][cut_id],
                             common.action_id(SCORED_SCOPE, expected))

        # (2) the CENSUS reports it, with its DECLARED floor.
        self.assertIn("distinct_gold_action_ids", census,
                      "the census must REPORT the retained gold variety (FOLD 2(b))")
        self.assertEqual(census["distinct_gold_action_ids"], len(golds))
        self.assertEqual(census["declared_gold_variety_floor"], census["retained_total"])
        self.assertEqual(census["declared_gold_variety_floor_rule"],
                         generator.DECLARED_GOLD_VARIETY_FLOOR_RULE)
        self.assertNotIn(generator.RETAINED_GOLD_VARIETY_BELOW_FLOOR, census["errors"])

        # (3) DISCRIMINATING — a constant-gold retained set is refused BY NAME.  This
        #     is the pre-fix population's shape, executed against the post-fix census.
        constant = copy.deepcopy(retained)
        one_gold = constant[0]["gold_action_id_by_cut"][constant[0]["chosen_cut_id"]]
        for candidate in constant:
            for cut_id in candidate["cut_ids"]:
                candidate["gold_action_id_by_cut"][cut_id] = one_gold
        degenerate = generator.population_census(generation.candidates, constant)
        self.assertEqual(degenerate["distinct_gold_action_ids"], 1)
        self.assertIn(generator.RETAINED_GOLD_VARIETY_BELOW_FLOOR,
                      degenerate["errors"])

    def test_bc19_red_the_census_reports_the_signature_motif_crosstab(self):
        """cohort-BUILD r1 FOLD 2(c), class POPULATION_MOTIF_CODEBOOK: the census
        CROSS-TABULATES the observation signature (family, code, cardinality, order)
        against the motif and reports how many signatures identify exactly ONE motif,
        and how many retained rows carry one.  The residual is DECLARED with its
        measured number (`DECLARED_SINGLE_MOTIF_SIGNATURE_RESIDUAL`, design §2.2), so
        a drift in the population breaks this witness instead of the record.

        The bounded reshaping attempt is recorded rather than shipped: 0-2
        hash-derived non-legal PAD obligations per candidate moved the count
        distributions but did NOT reach zero single-motif signatures — it moved the
        tail (POPULATION.COUNT.9 -> POPULATION.COUNT.10/11 for OBLIGATION_LIFECYCLE,
        STRUCTURE_DEPTH FACT.DEPTH.4 -> FACT.DEPTH.3 for MIXED_DELAYED_CONTINUITY),
        3 single-motif signatures either way, affected rows 15 -> 8.  The tweak was
        DISCARDED and the residual declared, per the no-machinery law.

        RED-FIRST against the pre-fix bytes at `af1cc4f`
        (`mbcx01_build_cohort_generator.py`,
        sha256 7eb5441245472f5f1f71defef67edae076c0b78a8f77b33bb353d0e998a2e156),
        whose census carried no cross-tab at all.  This witness FAILED:

            AssertionError: 'observation_signature_total' not found in {...}
            : the census must REPORT the signature x motif cross-tab (FOLD 2(c))
        """
        generator, _authority, _packet = cohort_modules()
        generation = build_generation()
        retained = generation.context.retained_candidates
        census = generation.census

        for key in ("observation_signature_total",
                    "single_motif_observation_signatures",
                    "rows_carrying_a_single_motif_signature",
                    "single_motif_observation_signature_list"):
            self.assertIn(key, census,
                          "the census must REPORT the signature x motif cross-tab "
                          "(FOLD 2(c))")

        # Recomputed INDEPENDENTLY here, from the retained rows themselves.
        motifs_by_signature = {}
        rows_by_signature = {}
        for candidate in retained:
            record = candidate["observation_authority_by_cut"][
                candidate["chosen_cut_id"]]
            signature = "|".join(str(record[field]) for field
                                 in generator.OBSERVATION_SIGNATURE_FIELDS)
            motifs_by_signature.setdefault(signature, set()).add(candidate["motif"])
            rows_by_signature[signature] = rows_by_signature.get(signature, 0) + 1
        single = sorted(key for key, motifs in motifs_by_signature.items()
                        if len(motifs) == 1)
        rows = sum(rows_by_signature[key] for key in single)

        self.assertEqual(census["observation_signature_total"],
                         len(motifs_by_signature))
        self.assertEqual(census["single_motif_observation_signatures"], len(single))
        self.assertEqual(census["rows_carrying_a_single_motif_signature"], rows)
        self.assertEqual(census["single_motif_observation_signature_list"], single)

        # The DECLARED residual: the number in the design doc IS the number here.
        self.assertEqual(len(single),
                         generator.DECLARED_SINGLE_MOTIF_SIGNATURE_RESIDUAL)
        self.assertLess(rows, len(retained) // 10,
                        "the declared residual must stay a population TAIL")

        # DISCRIMINATING — the cross-tab MEASURES rather than reporting a constant: a
        # retained set drawn from ONE motif has every signature identifying that
        # motif, and the census says so.
        skewed = [candidate for candidate in retained
                  if candidate["motif"] == retained[0]["motif"]]
        self.assertGreater(len(skewed), 0)
        skewed_census = generator.population_census(generation.candidates, skewed)
        self.assertEqual(skewed_census["single_motif_observation_signatures"],
                         skewed_census["observation_signature_total"])
        self.assertEqual(skewed_census["rows_carrying_a_single_motif_signature"],
                         len(skewed))
        self.assertNotEqual(skewed_census["single_motif_observation_signatures"],
                            census["single_motif_observation_signatures"])

    def test_bc20_red_a_placement_shortfall_refuses_the_plan(self):
        """cohort-BUILD r1 FOLD 3, class PLAN_RECORD_TOTALITY: the plan record signs
        `planned_ineligible_placed`, and `_plan_placements` can return FEWER than it
        was asked for (one placement per JOINT census stratum, so a draft set that
        occupies ONE joint stratum yields ONE placement for any request).  The
        generation now REFUSES that plan by name instead of writing the requested
        number into the record.

        RED-FIRST against the pre-fix bytes at `af1cc4f`
        (`mbcx01_build_cohort_generator.py`,
        sha256 7eb5441245472f5f1f71defef67edae076c0b78a8f77b33bb353d0e998a2e156),
        which under-placed silently.  This witness FAILED:

            AssertionError: BuildGenerationRefusal not raised
        """
        generator, authority, _packet = cohort_modules()
        generation = build_generation()

        # (1) THE DEFECT, executed: 12 drafts in ONE joint stratum -> ONE placement.
        one_stratum = []
        for index in range(12):
            draft = copy.deepcopy(generation.candidates[0])
            draft["scenario_id"] = "SCENARIO.PLACEMENT.PROBE.%03d" % index
            one_stratum.append(draft)
        keys = {"|".join(str(generator._axis_values(draft)[axis])
                         for axis in generator.CENSUS_JOINT_AXES)
                for draft in one_stratum}
        self.assertEqual(len(keys), 1, "the probe drafts must share ONE joint stratum")
        placements = generator._plan_placements(one_stratum, [], 12)
        self.assertEqual(len(placements), 1,
                         "the shortfall must be REAL, or this witness is theatre")

        # (2) THE REFUSAL: a placer that under-places refuses the GENERATION, and the
        #     refusal names the requested and the achieved totals.
        original = generator._plan_placements

        def under_placing(drafts, unplanned, placed_total):
            full = original(drafts, unplanned, placed_total)
            return dict(sorted(full.items())[:1]) if full else full

        try:
            generator._plan_placements = under_placing
            with self.assertRaises(generator.BuildGenerationRefusal) as refusal:
                generator.generate_cohort()
        finally:
            generator._plan_placements = original
        message = str(refusal.exception)
        self.assertIn(authority.BUILD_GENERATION_PLAN_REFUSED, message)
        self.assertIn("requested 12", message)
        self.assertIn("achieved 1", message)

        # DISCRIMINATING — the honest run places EXACTLY what it requested, so the
        # refusal is not a blanket one.
        for motif, row in sorted(generation.plan["per_motif"].items()):
            self.assertEqual(len(row["planned_ineligible_scenarios"]),
                             row["planned_ineligible_placed"],
                             "%s: the plan record must sign what it placed" % motif)
            self.assertEqual(row["planned_ineligible_placed"],
                             generation.spec["planned_ineligible_quota_k"])

    def test_bc21_red_the_coverage_numerator_counts_legal_noop_events(self):
        """cohort-BUILD r1 FOLD 4, class COVERAGE_NUMERATOR_RULE: the §2.6 numerator
        counts ordered pairs over ALL gate-checked program events, and the record
        DECLARES that rule beside the number.  A `DUPLICATE_NOOP` is a legal executed
        program event (it is the only construction that reaches that code, and every
        program event was matched against its EXPECTED code at generation), so an
        applied-only numerator undercounts.

        The recount below is written INLINE and shares no filter with
        `sequence_coverage`.

        RED-FIRST against the pre-fix bytes at `af1cc4f`
        (`mbcx01_build_cohort_generator.py`,
        sha256 7eb5441245472f5f1f71defef67edae076c0b78a8f77b33bb353d0e998a2e156),
        whose numerator counted APPLIED events only (150) and whose record carried no
        numerator rule.  This witness FAILED:

            AssertionError: 'covered_pair_rule' not found in {...}
            : the coverage record must DECLARE its numerator rule (FOLD 4)
        """
        generator, authority, _packet = cohort_modules()
        generation = build_generation()
        coverage = generation.provenance["sequence_coverage"]

        self.assertIn("covered_pair_rule", coverage,
                      "the coverage record must DECLARE its numerator rule (FOLD 4)")
        self.assertEqual(coverage["covered_pair_rule"],
                         generator.SEQUENCE_COVERED_PAIR_RULE)
        self.assertIn("ALL", coverage["covered_pair_rule"])

        # The INDEPENDENT recount: every event of every program, no code filter.
        all_events = set()
        applied_only = set()
        noop_seen = 0
        for candidate in generation.candidates:
            program = candidate["event_program"]
            codes = candidate["event_result_codes"]
            self.assertEqual(len(program), len(codes))
            noop_seen += sum(1 for code in codes if code == "DUPLICATE_NOOP")
            for first in range(len(program)):
                for second in range(first + 1, len(program)):
                    pair = (program[first]["event_type"],
                            program[second]["event_type"])
                    all_events.add(pair)
                    if codes[first] == "APPLIED" and codes[second] == "APPLIED":
                        applied_only.add(pair)
        self.assertGreater(noop_seen, 0,
                           "the population must contain DUPLICATE_NOOP events, or "
                           "this witness cannot discriminate")
        self.assertEqual(coverage["covered_pair_count"], len(all_events))
        self.assertEqual(coverage["coverage_ratio"],
                         len(all_events) / coverage["target_pair_count"])

        # DISCRIMINATING 1 — the applied-only numerator is STRICTLY smaller, and the
        # pairs it drops are pairs of legal executed events.
        self.assertLess(len(applied_only), len(all_events))
        self.assertIn(("commit_handoff_result", "commit_handoff_result"),
                      all_events - applied_only)

        # DISCRIMINATING 2 — the numerator rule is REQUIRED, not decorative: a record
        # without it is refused by name.
        stripped = copy.deepcopy(generation.provenance)
        stripped["sequence_coverage"].pop("covered_pair_rule")
        self.assertEqual(authority.sequence_coverage_report_errors(stripped),
                         [authority.BUILD_SEQUENCE_COVERAGE_UNREPORTED])
        self.assertEqual(
            authority.sequence_coverage_report_errors(generation.provenance), [])

    def test_bc22_red_a_false_coverage_record_cannot_bind_into_retained_authority(self):
        """cohort-BUILD r2 FOLD A (council r2 seat 3 F1), class
        COVERAGE_RECORD_UNBOUND_TO_CANDIDATES: the §2.6 coverage record that rides
        provenance must be the record the CANDIDATE PROGRAMS produce.

        `build_source_provenance` hashes whatever record it is handed, and
        `sequence_coverage_report_errors` checks FIELD PRESENCE plus the floor Boolean
        — neither one ever recomputes the number.  A SELF-CONSISTENT FORGERY (289/289
        claimed where the 960 programs cover 151/289) therefore rode into the retained
        authority's own provenance, which is a WRONG NUMBER in the record every
        downstream reader trusts.  The join added here RECOMPUTES the record from the
        POPPED candidate rows and refuses a divergent one BY NAME.

        RED-FIRST, recorded 2026-08-16 against the PRE-FIX bytes at HEAD
        530b5d031df99a683c527abf35000637e7596ecb, loaded with `git show HEAD:` into a
        private directory and hash-asserted before the run
        (`mbcx01_build_cohort_authority.py` sha256
        fe88e80c32e5d247fe4cc9eba4af22f521183d7aa109b04bab9760a980fcde6a;
        `mbcx01_build_cohort_generator.py`
        192158fca95fcb76a22264c7ce420656eca4a8bbb5dd50adcfa2359eeec0be3a;
        `mbcx01_build_cohort_packet.py`
        65b1ce7dcaa33eaa4e4d2d017a45dbacdfb21b34fbdca5803ff190fd99a4ab89).  The
        records-only commit db90852 landed on top during the fold and left all three
        blobs byte-identical (49dfcfb / 526560f / 8f988fe at BOTH commits), so the
        pre-fix bytes cited here are also the pre-fix bytes at db90852.
        This witness FAILED — failures=3, errors=1:

            FAIL [the validator recomputes and names the divergence]
            AssertionError: 'BUILD_SEQUENCE_COVERAGE_MISMATCH' not found in []

            FAIL [the retained authority refuses the forged provenance]
            AssertionError: the retained authority ADMITTED the forged record:
            retained=768, coverage bound into the admitted provenance=289/289

            FAIL [the closed vocabulary carries both names]
            AssertionError: None != 'BUILD_SEQUENCE_COVERAGE_MISMATCH'

            ERROR [the coverage law moved to where the validator can run it]
            AttributeError: module 'mbcx01_build_cohort_authority' has no attribute
            'sequence_coverage'
        """
        generator, authority, packet = cohort_modules()
        generation = build_generation()
        honest = generation.provenance["sequence_coverage"]

        # THE FORGERY: the same shape, the same DECLARED rules, and a NUMBER the 960
        # programs do not produce — the whole 289-pair square claimed as covered.
        forged = copy.deepcopy(honest)
        forged["covered_pair_count"] = forged["target_pair_count"]
        forged["coverage_ratio"] = 1.0
        forged["meets_declared_floor"] = True
        forged["errors"] = []
        self.assertLess(honest["covered_pair_count"], forged["covered_pair_count"],
                        "the forged record must claim MORE than the population "
                        "covers, or this witness cannot discriminate")
        forged_provenance = authority.build_source_provenance(
            generation.candidates, forged)

        # The presence-only check ADMITS the forgery — that is exactly the hole, and
        # it stays the field-presence check it was; the VALUE check is the new join.
        self.assertEqual(
            authority.sequence_coverage_report_errors(forged_provenance), [],
            "the forged record is self-consistent by construction")

        # Resolved defensively so the PRE-FIX red reads as the ADMISSION it is rather
        # than as an AttributeError on the first line; the symbol's own existence is
        # asserted in the closed-vocabulary subtest below.
        mismatch = getattr(authority, "BUILD_SEQUENCE_COVERAGE_MISMATCH",
                           "BUILD_SEQUENCE_COVERAGE_MISMATCH")

        with self.subTest("the validator recomputes and names the divergence"):
            self.assertIn(mismatch, authority.validate_build_source_provenance(
                generation.candidates, forged_provenance))

        with self.subTest("the retained authority refuses the forged provenance"):
            try:
                admitted = authority.BuildRetainedAuthorityContext(
                    generation.candidates, forged_provenance,
                    packet.ELIGIBILITY_PREDICATE)
            except authority.BuildCohortAuthorityError as refusal:
                self.assertIn(mismatch, str(refusal))
            else:
                bound = admitted.provenance["sequence_coverage"]
                self.fail("the retained authority ADMITTED the forged record: "
                          "retained=%d, coverage bound into the admitted "
                          "provenance=%s/%s"
                          % (len(admitted.retained_candidates),
                             bound["covered_pair_count"], bound["target_pair_count"]))

        with self.subTest("the closed vocabulary carries both names"):
            self.assertEqual(
                getattr(authority, "BUILD_SEQUENCE_COVERAGE_MISMATCH", None),
                "BUILD_SEQUENCE_COVERAGE_MISMATCH")
            self.assertIn(mismatch, authority.BUILD_COHORT_ERROR_CODES)
            # The r2 seat-1 rider: a raise-only code outside the DECLARED vocabulary
            # is a name nothing can resolve.  It stays raise-only; membership only
            # makes it resolvable where the vocabulary is declared.
            self.assertIn(packet.BUILD_OBSERVATION_PROJECTION_LEAK,
                          authority.BUILD_COHORT_ERROR_CODES)
            self.assertIs(generator.BUILD_OBSERVATION_PROJECTION_LEAK,
                          packet.BUILD_OBSERVATION_PROJECTION_LEAK)

        with self.subTest("the coverage law moved to where the validator can run it"):
            # FOLD-1 precedent: the law lives where the checker runs it, and the
            # generator re-exports the SAME object, so there is one measurement.
            self.assertIs(generator.sequence_coverage, authority.sequence_coverage)
            self.assertIs(generator.EVENT_ALPHABET, authority.EVENT_ALPHABET)
            self.assertIs(generator.SEQUENCE_COVERAGE_FLOOR,
                          authority.SEQUENCE_COVERAGE_FLOOR)

        # DISCRIMINATING: the HONEST record still admits, and the honest population
        # still binds — the join refuses a divergent record, not a coverage report.
        self.assertEqual(authority.validate_build_source_provenance(
            generation.candidates, generation.provenance), [])
        self.assertEqual(
            len(authority.retained_membership_scenario_ids(generation.context)), 768)

    def test_bc23_red_an_unhashable_scenario_id_refuses_by_name(self):
        """codex r5 P2: `validate_build_source_provenance` promises a CLOSED ERROR LIST,
        and the duplicate-id test broke that promise for a row it never checked.

        A candidate row whose `scenario_id` is a dict has an EXACT key set, so it clears
        the closed key-set check and reaches `set(ids)` — where
        `TypeError: unhashable type: 'dict'` escapes the validator before any verdict is
        returned.  The quieter half is the same shape the state plane's ba43 found: an
        id that is hashable but is not an id (an integer, a lower-case string) raised
        nothing and was never refused either.  Ids are type/grammar-checked BEFORE any
        set is built; the posture is unchanged (such a population never validated) and
        the refusal is now named.

        RED against the PRE-FIX bytes (`git show HEAD:mbcx01_build_cohort_authority.py`,
        sha256 aedc4279fb77665b261ffe6dfd0f7ea914a33329d74f47aa0c9929d984b73548, loaded
        under the real module name and hash-asserted before the run):

            ERROR [dict scenario_id]
            File "mbcx01_build_cohort_authority.py", line 552,
              in validate_build_source_provenance
                if len(ids) != len(set(ids)):
            TypeError: unhashable type: 'dict'
        """
        _generator, authority, packet = cohort_modules()
        generation = build_generation()
        honest = generation.candidates
        self.assertEqual(authority.validate_build_source_provenance(
            honest, generation.provenance), [])

        for label, value in (("dict scenario_id", {"scenario_id": "SCENARIO.BUILD.0.003"}),
                             ("list scenario_id", ["SCENARIO.BUILD.0.003"]),
                             ("integer scenario_id", 3),
                             ("None scenario_id", None),
                             ("lower-case scenario_id", "scenario.build.0.003")):
            with self.subTest(label):
                forged = copy.deepcopy(honest)
                forged[3]["scenario_id"] = value
                self.assertEqual(set(forged[3]), set(authority.BUILD_CANDIDATE_KEYS),
                                 "the row's key set must stay EXACT, or this witness "
                                 "is caught by the key-set check instead")
                self.assertEqual(
                    authority.validate_build_source_provenance(
                        forged, generation.provenance),
                    [authority.BUILD_CANDIDATE_SCHEMA_INVALID])
                with self.assertRaises(authority.BuildCohortAuthorityError) as caught:
                    authority.select_build_cohort(forged, generation.provenance,
                                                  packet.ELIGIBILITY_PREDICATE)
                self.assertIn(authority.BUILD_CANDIDATE_SCHEMA_INVALID, str(caught.exception))

        # DISCRIMINATING — the uniqueness question is still ASKED, and still answered by
        # name, for a population whose ids are all ids: the guard orders the two checks,
        # it does not remove one.
        duplicated = copy.deepcopy(honest)
        duplicated[4]["scenario_id"] = duplicated[3]["scenario_id"]
        self.assertIn("DUPLICATE_SCENARIO_ID", authority.validate_build_source_provenance(
            duplicated, generation.provenance))
        self.assertTrue(authority.valid_scenario_id(honest[3]["scenario_id"]))
        self.assertFalse(authority.valid_scenario_id({}))

    def test_bc24_red_a_cut_map_that_is_not_a_map_refuses_by_name(self):
        """codex-CLI r6 SEAT1 F4 (`mbcx01_build_cohort_authority.py:516`): the
        declared-eligibility pop reads `.values()` off a caller-supplied value.

        `for cut_state in (row.get(name) or {}).values()` assumed
        `canonical_state_by_cut` was a mapping. A row whose value is a scalar has an
        EXACT key set — so it clears the closed key-set check the same way bc23's
        unhashable id did — and `AttributeError: 'int' object has no attribute
        'values'` escaped both public doors before any verdict was returned.

        The FALSY non-mapping spellings never crashed at all: `[]` is falsy, so
        `[] or {}` swallowed it and the row was only ever caught downstream as an
        opaque `SOURCE_PROVENANCE_MISMATCH` — a refusal, but one that names the
        provenance hash rather than the row that is not a candidate. Both are the
        named schema refusal now.

        RED against the PRE-FIX bytes (`git show
        HEAD:mbcx01_build_cohort_authority.py`, sha256
        266433740f72e123931d479c943be56a5b1359afbb23f77edc2fd9d16351bda4, exported to
        a scratch tree and hash-asserted before the run):

            ERROR [canonical_state_by_cut is an int]
            File "mbcx01_build_cohort_authority.py", line 543,
              in validate_build_source_provenance
                rows, eligibility_refusals = pop_declared_eligibility(candidates)
            File "mbcx01_build_cohort_authority.py", line 516,
              in pop_declared_eligibility
                for cut_state in (row.get(name) or {}).values():
            AttributeError: 'int' object has no attribute 'values'

            ERROR [canonical_state_by_cut is a string]  (same frames)
            AttributeError: 'str' object has no attribute 'values'

            ERROR [canonical_state_by_cut is a boolean]  (same frames)
            AttributeError: 'bool' object has no attribute 'values'

            FAIL [canonical_state_by_cut is a list] / [... is null]  -- the QUIET half
            AssertionError: Lists differ:
              ['SOURCE_PROVENANCE_MISMATCH'] != ['BUILD_CANDIDATE_SCHEMA_INVALID']
        """
        _generator, authority, packet = cohort_modules()
        generation = build_generation()
        honest = generation.candidates
        self.assertEqual(authority.validate_build_source_provenance(
            honest, generation.provenance), [])

        for label, value in (("int", 5), ("string", "STATE"), ("list", []),
                             ("null", None), ("boolean", True)):
            with self.subTest(label):
                forged = copy.deepcopy(honest)
                forged[3]["canonical_state_by_cut"] = value
                self.assertEqual(set(forged[3]), set(authority.BUILD_CANDIDATE_KEYS),
                                 "the row's key set must stay EXACT, or this witness "
                                 "is caught by the key-set check instead")
                self.assertEqual(
                    authority.validate_build_source_provenance(
                        forged, generation.provenance),
                    [authority.BUILD_CANDIDATE_SCHEMA_INVALID])
                # The OTHER public door reaches the same pop before it validates.
                with self.assertRaises(authority.BuildCohortAuthorityError) as caught:
                    authority.select_build_cohort(forged, generation.provenance,
                                                  packet.ELIGIBILITY_PREDICATE)
                self.assertIn(authority.BUILD_CANDIDATE_SCHEMA_INVALID,
                              str(caught.exception))

        # DISCRIMINATING: the guard reads the cut map's TYPE, not its contents, so an
        # honest population still validates clean (asserted above) and an EMPTY cut
        # map — a mapping, just with nothing in it — is not refused by this guard.
        # It is still refused, by the provenance hash it no longer matches, which is
        # the check that owns that question.
        empty = copy.deepcopy(honest)
        empty[3]["canonical_state_by_cut"] = {}
        empty_verdict = authority.validate_build_source_provenance(
            empty, generation.provenance)
        self.assertIn("SOURCE_PROVENANCE_MISMATCH", empty_verdict)
        self.assertNotIn(authority.BUILD_CANDIDATE_SCHEMA_INVALID, empty_verdict)

    def test_bc25_red_the_closed_verdict_covers_shapes_nobody_enumerated(self):
        """codex-CLI r6 SEAT1 F3/F4 WHOLESALE CLOSE: the closed error list is a
        property of the BOUNDARY, not of the shapes three rounds of findings named.

        bc23 closed an unhashable scenario id at its site; bc24 closed a non-mapping
        cut map at its site; each time the next unanticipated shape found the next
        site. The complement closes the class at both public doors, and the shape
        below is constructed for this witness precisely because NO per-site guard
        anticipates it: the malformation is in the POPULATION CONTAINER, not in any
        row, so every row-level guard is bypassed by construction.

        RED against the PRE-FIX bytes (`git show
        HEAD:mbcx01_build_cohort_authority.py`, sha256
        266433740f72e123931d479c943be56a5b1359afbb23f77edc2fd9d16351bda4):

            ERROR [candidates is None]
            File "mbcx01_build_cohort_authority.py", line 543,
              in validate_build_source_provenance
                rows, eligibility_refusals = pop_declared_eligibility(candidates)
            File "mbcx01_build_cohort_authority.py", line 506,
              in pop_declared_eligibility
                for source in candidates:
            TypeError: 'NoneType' object is not iterable

            ERROR [candidates is an int]  (same frames)
            TypeError: 'int' object is not iterable

        ⚠ HONESTY, ASSERTED NOT MERELY DOCUMENTED: the complement catches the
        enumerated tuple and nothing else. An internal defect outside it still
        escapes LOUD, and this module's own `BuildCohortAuthorityError` is re-raised
        rather than answered as a caller schema code.
        """
        _generator, authority, packet = cohort_modules()
        generation = build_generation()

        for label, population in (("candidates is None", None),
                                  ("candidates is an int", 7),
                                  ("candidates is a set", {"SCENARIO.BUILD.0.003"})):
            with self.subTest(label):
                verdict = authority.validate_build_source_provenance(
                    population, generation.provenance)
                self.assertIsInstance(verdict, list)
                self.assertTrue(all(isinstance(code, str) for code in verdict))
                self.assertIn(authority.BUILD_CANDIDATE_SCHEMA_INVALID, verdict)
                with self.assertRaises(authority.BuildCohortAuthorityError) as caught:
                    authority.select_build_cohort(population, generation.provenance,
                                                  packet.ELIGIBILITY_PREDICATE)
                self.assertIn(authority.BUILD_CANDIDATE_SCHEMA_INVALID,
                              str(caught.exception))

        # The complement is EXACTLY the enumerated tuple, and the enumeration is the
        # lane's own (`mbcx01_build_cohort_packet`'s `frozen_verdict`).
        self.assertEqual(
            (AttributeError, IndexError, KeyError, StopIteration, TypeError,
             UnicodeError, ValueError),
            authority.MALFORMED_CALLER_INPUT_EXCEPTIONS)

        # HONESTY: a defect of THIS module is not a caller-shaped refusal, and the
        # module's own named error is raised, not converted.
        original = authority._validate_build_source_provenance
        for raised, expected in (
                (AssertionError("WITNESS_INTERNAL_DEFECT"), AssertionError),
                (authority.BuildCohortAuthorityError("WITNESS_MODULE_FAULT"),
                 authority.BuildCohortAuthorityError)):
            with self.subTest(raised=type(raised).__name__):
                def broken(*args, _raised=raised, **kwargs):
                    raise _raised

                authority._validate_build_source_provenance = broken
                try:
                    with self.assertRaises(expected) as caught:
                        authority.validate_build_source_provenance(
                            generation.candidates, generation.provenance)
                finally:
                    authority._validate_build_source_provenance = original
                self.assertIs(raised, caught.exception)

        # DISCRIMINATING: the complement did not turn the validator into a black box.
        # The honest population still validates clean, and a population that is WRONG
        # rather than malformed still gets its own specific code.
        self.assertEqual([], authority.validate_build_source_provenance(
            generation.candidates, generation.provenance))
        duplicated = copy.deepcopy(generation.candidates)
        duplicated[4]["scenario_id"] = duplicated[3]["scenario_id"]
        verdict = authority.validate_build_source_provenance(
            duplicated, generation.provenance)
        self.assertIn("DUPLICATE_SCENARIO_ID", verdict)
        self.assertNotIn(authority.BUILD_CANDIDATE_SCHEMA_INVALID, verdict)

    @staticmethod
    def pinning_list(bundle) -> list:
        """The pin generator's own subject list, read the way the bundle reads it."""
        source = (Path(__file__).resolve().parent
                  / bundle.PIN_MANIFEST_GENERATOR).read_text(encoding="utf-8")
        return (bundle._ps1_string_list(source, "buildSubjects")
                + bundle._ps1_string_list(source, "frozenDependencies"))


if __name__ == "__main__":
    unittest.main()
