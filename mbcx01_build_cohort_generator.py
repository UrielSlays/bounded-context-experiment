"""BUILD cohort GENERATOR — 960 candidates as replayed event programs (issue #17).

Design of record: `MBCX-01-BUILD-COHORT-CONTENT-DESIGN.md` r6 FINAL at commit
18d86d44d3a2cf28108022e626ea4bda1b430d86, §2 module 1 and §§2.1-2.7.

WHAT THIS MODULE SUPERSEDES (frozen lines cited, never edited)
--------------------------------------------------------------
`mbcx01_r13_measurement.synthetic_candidates_r13` (:243-274) builds ONE world
(`_candidate_world`, :203-240) and stamps it on all 960 candidates, with a
declared eligibility Boolean (:252) read back under a `RECOMPUTED` label (:317).
Here every candidate is a DETERMINISTIC PROGRAM over the frozen 17-event alphabet
(`mbcx01_r13_common.EVENT_OPERATIONS`, :16-34), replayed at generation through
BOTH frozen reducers with byte equality and a legality cross-check at every
frontier (§2.7), and every projected artefact — obligation, dependency, FACT and
OBSERVATION world rows, the action catalog, the legal set, the gold — is DERIVED
from that replay.

READING OF RECORD, "17-event programs" (§2 module 1): the frozen alphabet has
exactly 17 event types, and §2.6 scores "t-way SEQUENCE coverage over the
17-event ALPHABET".  Both readings are satisfied here: every program is drawn
from the 17-event alphabet AND is exactly `PROGRAM_EVENT_COUNT = 17` steps long.

ADVERSARY / REFUSAL POSTURE
---------------------------
No threat model.  Every refusal below stops a WRONG NUMBER: a program whose two
reducers disagree, a plan whose unplanned refusals eat the floor margin
(`BUILD_GENERATION_PLAN_REFUSED`), a retained stratum that would let ONE row read
as "represented" (`RETAINED_AXIS_STRATUM_FLOOR`).  None of them stops a person.

IMPORT DIRECTION (no cycles): frozen modules + the two BUILD siblings.  Nothing
imports this module.

DECLARED BUILD-TIME CONSTANTS (§6 Item 7(a)-(c)) — the driver reviews these:
  * `PROGRAM_EVENT_COUNT` = 17
  * `PREREQUISITE_SHAPES` (6 shapes, width/depth <= 3/3), `DECOY_MECHANISMS`
  * `OMISSION_CONFIGURATIONS` (4 per motif family); `OBSERVATION_FAMILIES` (4) and
    `OBSERVATION_ALLOWED_FIELDS` (the §2.2 allowlist projection) are DECLARED in
    `mbcx01_build_cohort_packet` and re-exported here (FOLD 1(b): the serving
    boundary re-derives the observation, and the import arrow runs this way)
  * `OBSERVATION_FORBIDDEN_INPUTS` — CLOSED at build (Item 7(c): additions are
    design-round material, removals are not permitted)
  * `DECLARED_RETAINED_FLOORS`; `SEQUENCE_COVERAGE_STRENGTH` and
    `SEQUENCE_COVERAGE_FLOOR` are DECLARED in `mbcx01_build_cohort_authority` with the
    §2.6 measurement (cohort-BUILD r2 FOLD A) and re-exported here; the quota `k` is in
    `mbcx01_build_cohort_authority.BUILD_COHORT_SPEC`.
  * `TARGET_OBLIGATION_PREFIX` (the per-scenario target identity, FOLD 2(a)),
    `DECLARED_GOLD_VARIETY_FLOOR_RULE` (FOLD 2(b)),
    `OBSERVATION_SIGNATURE_FIELDS` (the census cross-tab, FOLD 2(c)) and
    `SEQUENCE_COVERED_PAIR_RULE` (the coverage NUMERATOR rule, FOLD 4 — declared in
    `mbcx01_build_cohort_authority` by r2 FOLD A, re-exported here).
"""

from __future__ import annotations

import copy
from typing import Any, Callable

import mbcx01_r13_common as common
import mbcx01_r13_measurement as measurement
import mbcx01_r13_packets as packets
import mbcx01_r13_state_oracle as state_oracle
import mbcx01_r13_state_reference as state_reference
import mbcx01_build_cohort_authority as authority
import mbcx01_build_cohort_packet as packet

sha384 = measurement.sha384
sha256 = measurement.sha256
canonical_json = measurement.canonical_json

SCOPE_ID = "SCOPE.SHARED"
FOREIGN_SCOPE_ID = "SCOPE.FOREIGN"
T0 = common.T0
T1 = common.T1
#: Strictly later than T1; the "not due at the scored cut" horizon.
T2 = "2026-08-14T00:00:00.000000Z"

PROGRAM_EVENT_COUNT = authority.BUILD_COHORT_SPEC["program_event_count"]
#: Re-export (cohort-BUILD r2 FOLD A): the frozen 17-event alphabet is DECLARED in
#: `mbcx01_build_cohort_authority` with the §2.6 measurement that reads it.
EVENT_ALPHABET = authority.EVENT_ALPHABET

#: The SCORED TARGET's identity is PER-SCENARIO (cohort-BUILD r1 FOLD 2(a)).  A
#: constant target id made `action_id = sha256([scope, obligation_id])` a CONSTANT
#: too, so all 768 retained rows shared ONE gold and a positional heuristic scored
#: at ceiling in both arms with no population knowledge — the BC/OM contrast
#: collapsed for a reason unrelated to the hypothesis.  The derivation is
#: CONCATENATIVE, not hashed: `scenario_id` is already unique per candidate, so
#: distinctness is by CONSTRUCTION and needs no collision argument.
TARGET_OBLIGATION_PREFIX = "OBL.TGT."
LIFECYCLE_OBLIGATION_ID = "OBL.LIFE"
HANDOFF_OBLIGATION_ID = "OBL.HANDOFF"
REJECT_OBLIGATION_ID = "OBL.REJECT"
#: Never in a catalog, never a prerequisite: the BC-only selected object that
#: makes the BC/OM served difference non-degenerate in BOTH directions.
BC_ONLY_OBLIGATION_ID = "OBL.SHARED"
#: The blocker used by the BLOCKED decoy mechanism; stays OPEN forever, and is
#: never BC-selected, so it never collapses the BC/OM difference.
BLOCKER_OBLIGATION_ID = "OBL.PREREQ"

# --- declared variation axes (§2.1) -------------------------------------------

#: width/depth <= 3/3, total prerequisite obligations capped at 3 so every program
#: fits the 17-step budget with room for its motif core.
PREREQUISITE_SHAPES = (
    {"label": "W1D1", "width": 1, "depth": 1,
     "nodes": (("OBL.PRQ.0", ()),), "direct": ("OBL.PRQ.0",)},
    {"label": "W1D2", "width": 1, "depth": 2,
     "nodes": (("OBL.PRQ.1", ()), ("OBL.PRQ.0", ("OBL.PRQ.1",))),
     "direct": ("OBL.PRQ.0",)},
    {"label": "W1D3", "width": 1, "depth": 3,
     "nodes": (("OBL.PRQ.2", ()), ("OBL.PRQ.1", ("OBL.PRQ.2",)),
               ("OBL.PRQ.0", ("OBL.PRQ.1",))),
     "direct": ("OBL.PRQ.0",)},
    {"label": "W2D1", "width": 2, "depth": 1,
     "nodes": (("OBL.PRQ.0", ()), ("OBL.PRQ.1", ())),
     "direct": ("OBL.PRQ.0", "OBL.PRQ.1")},
    {"label": "W2D2", "width": 2, "depth": 2,
     "nodes": (("OBL.PRQ.2", ()), ("OBL.PRQ.0", ("OBL.PRQ.2",)), ("OBL.PRQ.1", ())),
     "direct": ("OBL.PRQ.0", "OBL.PRQ.1")},
    {"label": "W3D1", "width": 3, "depth": 1,
     "nodes": (("OBL.PRQ.0", ()), ("OBL.PRQ.1", ()), ("OBL.PRQ.2", ())),
     "direct": ("OBL.PRQ.0", "OBL.PRQ.1", "OBL.PRQ.2")},
)

#: Each mechanism is ONE event and leaves the decoy permanently non-legal at the
#: scored cut AND at the post-commit cut (so `expected_a1_action_ids` stays []).
DECOY_MECHANISMS = ("NOT_CRITICAL", "NOT_DUE", "BLOCKED")
DECOY_COUNTS = (1, 2)
FACT_CHAIN_DEPTHS = (1, 2, 3)
CUT_OFFER_COUNTS = (2, 3)
EVENT_ORDERS = ("FACTS_LAST", "FACTS_FIRST")

#: The §2.2 observation law lives in the PACKET sibling (FOLD 1(b)) so the SERVING
#: boundary can re-derive a record; these names are the SAME objects, re-exported so
#: the generator's call sites and the census read as one vocabulary.
OBSERVATION_FAMILIES = packet.OBSERVATION_FAMILIES
OBSERVATION_FAMILY_SHORT = packet.OBSERVATION_FAMILY_SHORT
OBSERVATION_FAMILY_BASE_CARDINALITY = packet.OBSERVATION_FAMILY_BASE_CARDINALITY

#: §2.1's per-candidate mechanism-OMISSION configuration (bounded swarm form).
#: The DELEGATION family omits parts of its own handoff core; every other family
#: omits optional blocks.  The duplicate-replay pair is NEVER omitted: it is the
#: only construction that reaches `DUPLICATE_NOOP` (§2.1 row 5).
OMISSION_CONFIGURATIONS = ("OMIT_NONE", "OMIT_A", "OMIT_B", "OMIT_A_AND_B")
DELEGATION_OMISSIONS = {
    "OMIT_NONE": (),
    "OMIT_A": ("REJECT_CHAIN",),
    "OMIT_B": ("CLOSE_HANDOFF",),
    "OMIT_A_AND_B": ("REJECT_CHAIN", "CLOSE_HANDOFF"),
}
GENERAL_OMISSIONS = {
    "OMIT_NONE": (),
    "OMIT_A": ("FOREIGN",),
    "OMIT_B": ("RELINK",),
    "OMIT_A_AND_B": ("FOREIGN", "RELINK"),
}

INELIGIBLE_STRATA = tuple(authority.BUILD_COHORT_SPEC["planned_ineligible_strata"])

# --- §2.2 the allowlist projection --------------------------------------------

#: The ONLY fields the observation derivation rule may read.  The projection
#: function returns exactly these keys and the derivation asserts exactly these
#: keys, so a forbidden input cannot REACH the rule — unrepresentable, not merely
#: detected (§2.2, r3 seat-1 PROPOSE adopted at r4).  DECLARED in the packet sibling
#: (FOLD 1(b)) with the derivation rule it governs; the SAME tuple, re-exported.
OBSERVATION_ALLOWED_FIELDS = packet.OBSERVATION_ALLOWED_FIELDS

#: CLOSED at build (§6 Item 7(c)).  Additions are design-round material; removals
#: are not permitted.  The last group is the gold-DETERMINING field set of the
#: scored target and its prerequisites — those leak gold EXISTENCE, and relabeling
#: invariance cannot see a value-preserving leak.
OBSERVATION_FORBIDDEN_INPUTS = (
    "motif",
    "gold_action_id",
    "action_id",
    "action_catalog",
    "candidate_selector_id",
    "bc_selected_object_ids",
    "retained_position",
    "retained_set_root",
    "target_lifecycle",
    "target_critical",
    "target_due_at",
    "prerequisite_lifecycles",
)

# --- §2.3 census floors -------------------------------------------------------

RETAINED_AXIS_STRATUM_FLOOR = "RETAINED_AXIS_STRATUM_FLOOR"
RETAINED_AXIS_STRATUM_MISSING = "RETAINED_AXIS_STRATUM_MISSING"
RETAINED_AXIS_VALUE_MISSING = "RETAINED_AXIS_VALUE_MISSING"
#: FOLD 2(b): the retained population's ANSWER KEY must not be a constant.  A
#: population whose rows share a gold action id is scorable by a positional
#: heuristic with no population knowledge, which is a WRONG NUMBER on both arms.
RETAINED_GOLD_VARIETY_BELOW_FLOOR = "RETAINED_GOLD_VARIETY_BELOW_FLOOR"
#: The DECLARED floor rule for that count.  With the per-scenario target identity
#: (FOLD 2(a)) the golds are distinct BY CONSTRUCTION, so the honest floor is the
#: retained total itself — anything less means two retained rows collided.
DECLARED_GOLD_VARIETY_FLOOR_RULE = "ONE_DISTINCT_GOLD_ACTION_ID_PER_RETAINED_ROW"
BUILD_DERIVED_AXIS_UNRECORDABLE = "BUILD_DERIVED_AXIS_UNRECORDABLE"
BUILD_PROGRAM_REDUCER_DISAGREEMENT = "BUILD_PROGRAM_REDUCER_DISAGREEMENT"
BUILD_PROGRAM_STEP_CODE_MISMATCH = "BUILD_PROGRAM_STEP_CODE_MISMATCH"
BUILD_PROGRAM_LENGTH_INVALID = "BUILD_PROGRAM_LENGTH_INVALID"
BUILD_LEGALITY_FRONTIER_DISAGREEMENT = "BUILD_LEGALITY_FRONTIER_DISAGREEMENT"
#: Re-export (cohort-BUILD r2 FOLD A): declared with the §2.6 measurement that emits
#: it, in `mbcx01_build_cohort_authority`; raised HERE as a generation refusal.
BUILD_SEQUENCE_COVERAGE_BELOW_FLOOR = authority.BUILD_SEQUENCE_COVERAGE_BELOW_FLOOR
#: Declared with the derivation law in the packet sibling (FOLD 1(b)); re-exported
#: because `project_observation_inputs` — which stays HERE, it reads generation
#: state — raises it as a GENERATION refusal.
BUILD_OBSERVATION_PROJECTION_LEAK = packet.BUILD_OBSERVATION_PROJECTION_LEAK

#: "one retained row must not read as represented" (§2.3): a GOVERNED stratum with
#: nonzero retained occupancy below 2 is refused by name.
DECLARED_RETAINED_FLOORS = {"joint": 2, "marginal": 2}

#: The census axes (§2.3, "censused across every declared semantic axis").
CENSUS_AXES = ("motif", "observation_family", "omission_configuration",
               "catalog_size", "prerequisite_shape", "fact_chain_depth",
               "decoy_mix", "cut_offer_count", "event_order",
               "gold_read_set_size", "bc_om_difference_size")
#: The joint tuple whose occupancy the census reports (r3 seats 1+3: two joint
#: strata can vanish while every marginal stays present).
CENSUS_JOINT_AXES = ("motif", "observation_family", "omission_configuration")
#: DECLARED absences: a planned-ineligible shape is generated ON PURPOSE and MUST
#: be absent from the retained set, so its axis is not censused for presence.
DECLARED_ABSENT_AXES = ("planned_ineligible_stratum",)

#: FOLD 2(c): the fields of an OBSERVATION SIGNATURE.  The census cross-tabulates
#: signature against motif so a signature that identifies ONE motif is a NUMBER in
#: the record rather than a thing a reader has to go and compute.  MEASURED, not
#: gated: the residual it reports is declared in the design doc §2.2, and gating it
#: would refuse the whole build over a population tail.
OBSERVATION_SIGNATURE_FIELDS = ("family", "code", "cardinality", "order")
#: The DECLARED residual (design §2.2, cohort-BUILD r1 fold 2): the number of
#: retained observation signatures that identify exactly ONE motif.  ONE bounded
#: reshaping attempt was made and DISCARDED (0-2 hash-derived non-legal PAD
#: obligations per candidate): it moved the distribution tail without reaching zero
#: (3 single-motif signatures either way, affected rows 15 -> 8), so the honest label
#: is carried here and in the design doc instead of machinery.  `test_bc19_*` pins
#: this constant to the census's own measurement, so the number cannot drift in
#: silence.
DECLARED_SINGLE_MOTIF_SIGNATURE_RESIDUAL = 3

# --- §2.6 sequence coverage ---------------------------------------------------
# RE-EXPORTS (cohort-BUILD r2 FOLD A).  The measurement and its four declared
# constants MOVED to `mbcx01_build_cohort_authority` — the same move the r1 FOLD 1
# made for the §2.2 derivation law — because `validate_build_source_provenance` has
# to RECOMPUTE the coverage record it admits, and it cannot import this module.  The
# names below are the SAME objects; the gate stays here, in generation order.

SEQUENCE_COVERAGE_STRENGTH = authority.SEQUENCE_COVERAGE_STRENGTH
SEQUENCE_TARGET_SET_RULE = authority.SEQUENCE_TARGET_SET_RULE
SEQUENCE_COVERED_PAIR_RULE = authority.SEQUENCE_COVERED_PAIR_RULE
SEQUENCE_COVERAGE_FLOOR = authority.SEQUENCE_COVERAGE_FLOOR


class BuildGenerationRefusal(ValueError):
    """A refusal of the GENERATION PLAN itself (never a refusal of a person)."""


def target_obligation_id(scenario_id: str) -> str:
    """THE scored target's obligation id for one candidate (FOLD 2(a)).

    `mbcx01_r13_common.SEMANTIC_ID` admits `[A-Z0-9][A-Z0-9:._/-]{0,127}`, and every
    `scenario_id` this generator issues comes from the committed
    `scenario_id_template` (`SCENARIO.BUILD.<motif>.<index>`), so the concatenation is
    a legal semantic id and is DISTINCT for every candidate by construction.
    """
    return TARGET_OBLIGATION_PREFIX + scenario_id


# =============================================================================
# the replay harness — §2.7's three-check gate
# =============================================================================

class ProgramReplay:
    """Applies one program step at a time through BOTH frozen reducers.

    §2.7, stated honestly: dual-reducer agreement is CONSISTENCY (a differential
    pseudo-oracle), not correctness — a SHARED legality bug is invisible to it.
    That residual is carried, not papered over.  The third check is a legality
    cross-check at every frontier between two INDEPENDENT frozen predicates: the
    packet layer's `legal_action_ids_from_world` (:98-115) and the reducer layer's
    `action_targets_legal` (`mbcx01_r13_state_reference.py:65-78`).
    """

    def __init__(self) -> None:
        self.reference = common.initial_state()
        self.oracle = common.initial_state()
        self.events: list[dict[str, Any]] = []
        self.codes: list[str] = []
        self.blocks: list[str] = []
        self.snapshots: list[dict[str, Any]] = [copy.deepcopy(self.reference)]
        self.frontier_legality: list[list[str]] = []

    def apply(self, event: dict[str, Any], expected: str, block: str) -> None:
        reference_state, reference_code = state_reference.reference_apply(
            self.reference, copy.deepcopy(event))
        oracle_state, oracle_code = state_oracle.oracle_apply(
            self.oracle, copy.deepcopy(event))
        if reference_code != oracle_code or canonical_json(
                reference_state) != canonical_json(oracle_state):
            raise BuildGenerationRefusal(
                "%s at %s/%s: %s vs %s" % (BUILD_PROGRAM_REDUCER_DISAGREEMENT, block,
                                           event["event_type"], reference_code,
                                           oracle_code))
        if reference_code != expected:
            raise BuildGenerationRefusal(
                "%s at %s/%s: expected %s got %s" % (
                    BUILD_PROGRAM_STEP_CODE_MISMATCH, block, event["event_type"],
                    expected, reference_code))
        self.reference, self.oracle = reference_state, oracle_state
        self.events.append(copy.deepcopy(event))
        self.codes.append(reference_code)
        self.blocks.append(block)
        self.snapshots.append(copy.deepcopy(self.reference))
        self.frontier_legality.append(self._legality_frontier())

    def _legality_frontier(self) -> list[str]:
        """The DoR legality predicate at this frontier, cross-checked two ways."""
        state = self.reference
        obligations = state["scopes"][SCOPE_ID]["obligations"]
        catalog = [{"action_id": common.action_id(SCOPE_ID, oid),
                    "action_kind": "ACT_ON_OBLIGATION",
                    "scope_id": SCOPE_ID, "obligation_id": oid}
                   for oid in sorted(obligations)]
        cut = common.current_cut(state)
        world = packet.obligation_world_rows(state, SCOPE_ID)
        from_world = packets.legal_action_ids_from_world(world, catalog, cut)
        from_reducer = sorted(
            (row["action_id"] for row in catalog
             if state_reference.action_targets_legal(
                 obligations, catalog, [row["action_id"]], cut["valid_time"])),
            key=lambda value: value.encode("utf-8"))
        if from_world != from_reducer:
            raise BuildGenerationRefusal(BUILD_LEGALITY_FRONTIER_DISAGREEMENT)
        return from_world

    def journal_seq(self) -> int:
        return self.reference["next_seq"] - 1


# =============================================================================
# event constructors
# =============================================================================

def _open_obligation(state: dict[str, Any], obligation_id: str, *, due_at: str,
                     critical: bool = True, subject_id: str = "SUB.BUILD",
                     owner_role: str = "WORKER",
                     prerequisites: tuple[str, ...] = (),
                     scope_id: str = SCOPE_ID) -> dict[str, Any]:
    return common.make_event("open_obligation", {
        "obligation_id": obligation_id, "subject_id": subject_id,
        "owner_role": owner_role, "due_at": due_at, "critical": critical,
        "completion_action_id": common.action_id(scope_id, obligation_id),
        "prerequisite_obligation_ids": list(prerequisites)},
        state=state, scope_id=scope_id)


def _complete_obligation(state: dict[str, Any], obligation_id: str) -> dict[str, Any]:
    cut = common.current_cut(state)
    return common.make_event("complete_obligation", {
        "obligation_id": obligation_id,
        "completion_action_id": common.action_id(SCOPE_ID, obligation_id),
        "originating_cut_hash": common.cut_hash(cut)},
        state=state, originating_cut=cut)


def _handoff_payload(state: dict[str, Any], handoff_id: str, scenario_id: str,
                     condition: str, target_obligation_id: str) -> dict[str, Any]:
    cut = common.current_cut(state)
    actions = [{"action_id": common.action_id(SCOPE_ID, target_obligation_id),
                "obligation_id": target_obligation_id}]
    manifest = {"schema_id": "StateManifestAuthorityV1", "scenario_id": scenario_id,
                "scope_id": SCOPE_ID, "action_catalog": actions,
                "action_catalog_hash": common.sha384(actions)}
    manifest["manifest_hash"] = common.sha384(manifest)
    task = {"schema_id": "StateTaskAuthorityV1", "scenario_id": scenario_id,
            "scope_id": SCOPE_ID, "manifest_hash": manifest["manifest_hash"],
            "requested_action_catalog_hash": manifest["action_catalog_hash"]}
    task["task_packet_hash"] = common.sha384(task)
    return {"handoff_id": handoff_id, "scenario_id": scenario_id,
            "condition": condition, "target_obligation_id": target_obligation_id,
            "task_packet_hash": task["task_packet_hash"],
            "served_request_hash": "B" * 64, "request_parameters_hash": "C" * 96,
            "idempotency_token": "IDEM.%s.MOTIF" % handoff_id,
            "task_packet_utf8": common.canonical_json(task).decode("utf-8"),
            "manifest_utf8": common.canonical_json(manifest).decode("utf-8"),
            "originating_cut_hash": common.cut_hash(cut),
            "action_catalog_hash": manifest["action_catalog_hash"],
            "canonical_snapshot_hash": common.sha384(
                state["scopes"][SCOPE_ID]["obligations"]),
            "route_contract_hash": "D" * 96,
            "manifest_hash": manifest["manifest_hash"], "action_catalog": actions}


def _response_payload(handoff: dict[str, Any], suffix: str) -> dict[str, Any]:
    worker = {"schema_id": "WorkerHandoffV5", "scenario_id": handoff["scenario_id"],
              "scope_id": SCOPE_ID, "condition": handoff["condition"],
              "task_packet_hash": handoff["task_packet_hash"],
              "served_request_hash": handoff["served_request_hash"],
              "manifest_hash": handoff["manifest_hash"], "status_code": "PROPOSE",
              "proposed_action_ids": [row["action_id"]
                                      for row in handoff["action_catalog"]],
              "produced_at": T1}
    worker["worker_handoff_hash"] = common.sha384(worker)
    raw = common.canonical_json(worker).decode("utf-8")
    response = {"handoff_id": handoff["handoff_id"],
                "scenario_id": handoff["scenario_id"],
                "condition": handoff["condition"], "node": "B",
                "task_packet_hash": handoff["task_packet_hash"],
                "served_request_hash": handoff["served_request_hash"],
                "request_parameters_hash": handoff["request_parameters_hash"],
                "idempotency_token": handoff["idempotency_token"],
                "raw_response_utf8": raw,
                "raw_response_hash": common.sha384(raw.encode("utf-8")),
                "worker_handoff_hash": worker["worker_handoff_hash"],
                "response_ref": "RESPONSE.MOTIF.%s" % suffix,
                "provider_request_id": "PROVIDER.MOTIF.%s" % suffix,
                "route_contract_hash": handoff["route_contract_hash"],
                "accepted_at": T1}
    response["durability_receipt"] = common.make_durability_receipt(
        response, "TXN.MOTIF.%s" % suffix)
    return response


# =============================================================================
# §2.1 the motif programs — postcondition + REALIZATION + exact codes
# =============================================================================

def _fact_block(replay: ProgramReplay, subject: str, predicate: str,
                depth: int, block: str) -> None:
    """assert -> correct -> retract(correction) -> REASSERT, truncated to `depth`.

    depth 3 IS the §2.1 CORRECTION_RESTORATION realization, pinned green by
    `test_mbcx01_build_cohort.test_bw94_*`: the retraction alone restores NOTHING
    (the parent's closure survives its child's retraction) and only the REASSERT
    makes the prior `value_code` visible again at the later cut.
    """
    assertion = common.make_event("assert_fact", {
        "subject_id": subject, "predicate_id": predicate, "value_code": "VALUE.ONE"},
        state=replay.reference)
    replay.apply(assertion, "APPLIED", block)
    if depth < 2:
        return
    correction = common.make_event("correct_fact", {
        "subject_id": subject, "predicate_id": predicate,
        "parent_event_id": assertion["event_id"], "value_code": "VALUE.TWO"},
        state=replay.reference, valid_from=T1)
    replay.apply(correction, "APPLIED", block)
    if depth < 3:
        return
    retraction = common.make_event("retract_fact", {
        "subject_id": subject, "predicate_id": predicate,
        "target_event_id": correction["event_id"]},
        state=replay.reference, valid_from=T1)
    replay.apply(retraction, "APPLIED", block)
    reassert = common.make_event("assert_fact", {
        "subject_id": subject, "predicate_id": predicate, "value_code": "VALUE.ONE"},
        state=replay.reference, valid_from=T1)
    replay.apply(reassert, "APPLIED", block)


def _lifecycle_block(replay: ProgramReplay, terminal: str) -> None:
    """§2.1 OBLIGATION_LIFECYCLE: open -> reschedule -> {complete|cancel} -> reopen,
    every code `APPLIED`, on a NON-target obligation (§2.4 governs the target).

    The reopen restores lifecycle OPEN with `due_at = T2`, so the reopened row can
    never become legal at the scored cut or the post-commit cut.
    """
    replay.apply(_open_obligation(replay.reference, LIFECYCLE_OBLIGATION_ID,
                                  due_at=T0, subject_id="SUB.LIFE"),
                 "APPLIED", "MOTIF_CORE")
    replay.apply(common.make_event("reschedule_obligation", {
        "obligation_id": LIFECYCLE_OBLIGATION_ID, "due_at": T1},
        state=replay.reference), "APPLIED", "MOTIF_CORE")
    if terminal == "complete_obligation":
        replay.apply(_complete_obligation(replay.reference, LIFECYCLE_OBLIGATION_ID),
                     "APPLIED", "MOTIF_CORE")
    else:
        replay.apply(common.make_event("cancel_obligation", {
            "obligation_id": LIFECYCLE_OBLIGATION_ID,
            "cancellation_code": "OWNER.CANCELLED"},
            state=replay.reference), "APPLIED", "MOTIF_CORE")
    replay.apply(common.make_event("reopen_obligation", {
        "obligation_id": LIFECYCLE_OBLIGATION_ID, "due_at": T2,
        "owner_role": "WORKER.REOPENED"}, state=replay.reference),
        "APPLIED", "MOTIF_CORE")


def _cross_scope_block(replay: ProgramReplay, target_id: str) -> None:
    """§2.1 CROSS_SCOPE_COLLISION: a genuinely multi-scope journal whose SCORED
    projection carries ZERO foreign-scope objects (the collision is by NAME).

    The colliding NAME is the candidate's own per-scenario target id (FOLD 2(a)), so
    the collision stays a collision after the target's identity started varying.
    """
    replay.apply(_open_obligation(replay.reference, target_id, due_at=T0,
                                  subject_id="SUB.BUILD",
                                  scope_id=FOREIGN_SCOPE_ID),
                 "APPLIED", "MOTIF_CORE")
    replay.apply(common.make_event("assert_fact", {
        "subject_id": "SUB.BUILD", "predicate_id": "PRED.FOREIGN",
        "value_code": "VALUE.FOREIGN"}, state=replay.reference,
        scope_id=FOREIGN_SCOPE_ID), "APPLIED", "MOTIF_CORE")


def _delegation_block(replay: ProgramReplay, scenario_id: str,
                      omissions: tuple[str, ...]) -> None:
    """§2.1 DELEGATION_IDEMPOTENT_HANDOFF, with its EXACT code sequence.

    The duplicates are BYTE-IDENTICAL EVENT REPLAY, the only construction that
    reaches `DUPLICATE_NOOP` (`mbcx01_r13_state_reference.py:20-29`); a FRESH
    duplicate returns `PROPOSAL_INVALID`/`COMMIT_INVALID`/`IDEMPOTENCY_CONFLICT`
    instead — three distinct facts, pinned by `test_bw23_*`.  The rejection
    realization is result code `APPLIED` with status `REJECTED` and
    `terminal_disposition` = the payload's `rejection_code` (pinned by `test_bw64_*`).
    """
    replay.apply(_open_obligation(replay.reference, HANDOFF_OBLIGATION_ID, due_at=T0,
                                  subject_id="SUB.HANDOFF"), "APPLIED", "MOTIF_CORE")
    if "REJECT_CHAIN" not in omissions:
        replay.apply(_open_obligation(replay.reference, REJECT_OBLIGATION_ID,
                                      due_at=T0, subject_id="SUB.REJECT"),
                     "APPLIED", "MOTIF_CORE")
    replay.apply(common.make_event("delegate_obligation", {
        "obligation_id": BC_ONLY_OBLIGATION_ID, "owner_role": "WORKER.DELEGATE"},
        state=replay.reference), "APPLIED", "MOTIF_CORE")

    payload = _handoff_payload(replay.reference, "HANDOFF.MOTIF.1", scenario_id,
                               "BC", HANDOFF_OBLIGATION_ID)
    replay.apply(common.make_event("open_handoff", payload, state=replay.reference),
                 "APPLIED", "MOTIF_CORE")
    response = _response_payload(payload, "1")
    replay.apply(common.make_event("record_call_response", response,
                                   state=replay.reference), "APPLIED", "MOTIF_CORE")
    proposal = common.make_event("propose_handoff_result", {
        "handoff_id": payload["handoff_id"],
        "worker_handoff_hash": response["worker_handoff_hash"],
        "originating_cut_hash": payload["originating_cut_hash"],
        "action_ids": [payload["action_catalog"][0]["action_id"]]},
        state=replay.reference)
    replay.apply(proposal, "APPLIED", "MOTIF_CORE")
    replay.apply(copy.deepcopy(proposal), "DUPLICATE_NOOP", "MOTIF_CORE")
    commit = common.make_event("commit_handoff_result", {
        "handoff_id": payload["handoff_id"], "proposal_event_id": proposal["event_id"]},
        state=replay.reference)
    replay.apply(commit, "APPLIED", "MOTIF_CORE")
    replay.apply(copy.deepcopy(commit), "DUPLICATE_NOOP", "MOTIF_CORE")
    if "CLOSE_HANDOFF" not in omissions:
        replay.apply(common.make_event("close_handoff", {
            "handoff_id": payload["handoff_id"]}, state=replay.reference),
            "APPLIED", "MOTIF_CORE")
    if "REJECT_CHAIN" in omissions:
        return
    second = _handoff_payload(replay.reference, "HANDOFF.MOTIF.2", scenario_id,
                              "OM", REJECT_OBLIGATION_ID)
    replay.apply(common.make_event("open_handoff", second, state=replay.reference),
                 "APPLIED", "MOTIF_CORE")
    second_response = _response_payload(second, "2")
    replay.apply(common.make_event("record_call_response", second_response,
                                   state=replay.reference), "APPLIED", "MOTIF_CORE")
    second_proposal = common.make_event("propose_handoff_result", {
        "handoff_id": second["handoff_id"],
        "worker_handoff_hash": second_response["worker_handoff_hash"],
        "originating_cut_hash": second["originating_cut_hash"],
        "action_ids": [second["action_catalog"][0]["action_id"]]},
        state=replay.reference)
    replay.apply(second_proposal, "APPLIED", "MOTIF_CORE")
    replay.apply(common.make_event("reject_handoff_result", {
        "handoff_id": second["handoff_id"], "rejection_code": "TRANSITION.ILLEGAL",
        "proposal_hash": common.sha384(second_proposal)},
        state=replay.reference), "APPLIED", "MOTIF_CORE")


_FILLER_ROTATION = ("DELEGATE", "RESCHEDULE", "FACT", "FOREIGN")


def _filler_step(replay: ProgramReplay, ordinal: int) -> None:
    kind = _FILLER_ROTATION[ordinal % len(_FILLER_ROTATION)]
    if kind == "DELEGATE":
        replay.apply(common.make_event("delegate_obligation", {
            "obligation_id": BLOCKER_OBLIGATION_ID,
            "owner_role": "WORKER.PAD.%d" % ordinal}, state=replay.reference),
            "APPLIED", "FILLER")
    elif kind == "RESCHEDULE":
        replay.apply(common.make_event("reschedule_obligation", {
            "obligation_id": BLOCKER_OBLIGATION_ID, "due_at": T0},
            state=replay.reference), "APPLIED", "FILLER")
    elif kind == "FACT":
        replay.apply(common.make_event("assert_fact", {
            "subject_id": "SUB.PAD.%d" % ordinal, "predicate_id": "PRED.PAD",
            "value_code": "VALUE.PAD"}, state=replay.reference), "APPLIED", "FILLER")
    else:
        replay.apply(common.make_event("assert_fact", {
            "subject_id": "SUB.PAD.%d" % ordinal, "predicate_id": "PRED.PAD",
            "value_code": "VALUE.PAD"}, state=replay.reference,
            scope_id=FOREIGN_SCOPE_ID), "APPLIED", "FILLER")


# =============================================================================
# §2.2 the observation authority — allowlist projection then derivation
# =============================================================================

def project_observation_inputs(state: dict[str, Any], cut: dict[str, Any],
                               event_program: list[dict[str, Any]],
                               family_selector: int) -> dict[str, Any]:
    """THE projection function.  Its output keys ARE `OBSERVATION_ALLOWED_FIELDS`.

    Nothing else can reach the derivation rule: no motif, no gold, no action
    identity, no selector output, no retained position, and none of the
    gold-DETERMINING fields of the scored target or its prerequisites.
    """
    facts = packet.fact_world_rows_from_state(state, SCOPE_ID, cut, event_program)
    projection = {
        "scope_id": SCOPE_ID,
        "cut_knowledge_time": cut["knowledge_time"],
        "cut_valid_time": cut["valid_time"],
        "obligation_row_count": len(state["scopes"][SCOPE_ID]["obligations"]),
        "fact_row_count": len(facts),
        "distinct_subject_count": len({row["fields"]["subject_id"] for row in facts}),
        "observation_family_selector": family_selector,
    }
    if set(projection) != set(OBSERVATION_ALLOWED_FIELDS):
        raise BuildGenerationRefusal(BUILD_OBSERVATION_PROJECTION_LEAK)
    return projection


#: The §2.2 derivation rule, OWNED by the packet sibling (FOLD 1(b)) and used here.
#: The generator does not keep a second copy: the serving boundary re-derives every
#: served record with THIS function, so one law with two implementations is exactly
#: the drift the fold removes.  `project_observation_inputs` above stays here — it
#: reads generation state, which the packet layer never has.
derive_observation_authority = packet.derive_observation_authority


# =============================================================================
# candidate construction
# =============================================================================

def _variation_for(scenario_id: str, motif: str, motif_rank: int) -> dict[str, Any]:
    """Per-candidate, hash-derived variation (§2.1) over the declared domains.

    The JOINT stratum (family x omission configuration) is assigned from a
    framed-hash RANK rather than a raw modulus so the 16 joint cells of each motif
    are balanced by construction — an unbalanced hash draw is how a governed
    stratum silently falls under its retained floor (§2.3 / W20).
    """
    domains = authority.BUILD_VARIATION_DOMAINS
    joint = motif_rank % (len(OBSERVATION_FAMILIES) * len(OMISSION_CONFIGURATIONS))
    family = OBSERVATION_FAMILIES[joint % len(OBSERVATION_FAMILIES)]
    omission = OMISSION_CONFIGURATIONS[joint // len(OBSERVATION_FAMILIES)]
    delegation = motif == "DELEGATION_IDEMPOTENT_HANDOFF"
    shape = (PREREQUISITE_SHAPES[0] if delegation else PREREQUISITE_SHAPES[
        authority.hash_index(domains["prerequisite_shape"], [scenario_id],
                             len(PREREQUISITE_SHAPES))])
    # The DELEGATION family spends its whole 17-step budget on its handoff core, so
    # its non-gold catalog action is `OBL.HANDOFF` — an obligation the core ALREADY
    # completes — and it opens no separate decoy.
    decoy_count = (0 if delegation else DECOY_COUNTS[authority.hash_index(
        domains["decoy_mix"], [scenario_id], len(DECOY_COUNTS))])
    mechanisms = tuple(
        DECOY_MECHANISMS[authority.hash_index(
            domains["decoy_mix"], [scenario_id, str(index)], len(DECOY_MECHANISMS))]
        for index in range(decoy_count))
    catalog_decoys = (1 if delegation else 1 + authority.hash_index(
        domains["catalog_size"], [scenario_id], decoy_count))
    fact_depth = FACT_CHAIN_DEPTHS[authority.hash_index(
        domains["fact_chain_depth"], [scenario_id], len(FACT_CHAIN_DEPTHS))]
    if motif == "CORRECTION_RESTORATION":
        fact_depth = 3
    cut_offers = CUT_OFFER_COUNTS[authority.hash_index(
        domains["cut_offer"], [scenario_id], len(CUT_OFFER_COUNTS))]
    order = EVENT_ORDERS[authority.hash_index(
        domains["event_order"], [scenario_id], len(EVENT_ORDERS))]
    family_selector = authority.hash_index(
        domains["observation_family"], [scenario_id], 8)
    # The family is a GOVERNED census stratum, so it is the joint assignment that
    # decides it; the hash selector only drives cardinality and order inside it.
    family_selector = (family_selector // len(OBSERVATION_FAMILIES)
                       ) * len(OBSERVATION_FAMILIES) + OBSERVATION_FAMILIES.index(family)
    return {"motif": motif,
            "prerequisite_shape": shape["label"],
            "decoy_mix": "+".join(mechanisms) if mechanisms else "NONE",
            "catalog_size": 2 + catalog_decoys,
            "fact_chain_depth": fact_depth,
            "observation_family": family,
            "observation_family_selector": family_selector,
            "omission_configuration": omission,
            "cut_offer_count": cut_offers,
            "event_order": order}


def _build_program(scenario_id: str, motif: str, variation: dict[str, Any],
                   ineligible_stratum: str | None) -> ProgramReplay:
    """Assemble and REPLAY one candidate's 17-step program (§2.1 + §2.7)."""
    shape = next(row for row in PREREQUISITE_SHAPES
                 if row["label"] == variation["prerequisite_shape"])
    target_id = target_obligation_id(scenario_id)
    delegation = motif == "DELEGATION_IDEMPOTENT_HANDOFF"
    omissions = (DELEGATION_OMISSIONS if delegation else GENERAL_OMISSIONS)[
        variation["omission_configuration"]]
    mechanisms = (() if variation["decoy_mix"] == "NONE"
                  else tuple(variation["decoy_mix"].split("+")))
    replay = ProgramReplay()

    # --- prerequisites, then the target, then the completions -----------------
    for node, prerequisites in shape["nodes"]:
        replay.apply(_open_obligation(replay.reference, node, due_at=T0,
                                      subject_id="SUB.PRQ",
                                      prerequisites=prerequisites),
                     "APPLIED", "PREREQ_OPEN")
    target_due = T2 if ineligible_stratum == "TARGET_NOT_DUE" else (
        T1 if motif == "MIXED_DELAYED_CONTINUITY" else T0)
    reversal = motif == "DEPENDENCY_REVERSAL"
    replay.apply(_open_obligation(
        replay.reference, target_id, due_at=target_due,
        subject_id="SUB.TARGET",
        prerequisites=() if reversal else shape["direct"]), "APPLIED", "TARGET_OPEN")
    if reversal:
        # §2.1 DEPENDENCY_REVERSAL: the link makes the target ILLEGAL, and only the
        # prerequisite completion makes it DUE — a pure ordering effect.
        for node in shape["direct"]:
            replay.apply(common.make_event("link_dependency", {
                "obligation_id": target_id,
                "prerequisite_obligation_id": node}, state=replay.reference),
                "APPLIED", "MOTIF_CORE")
        blocked_frontier = replay.frontier_legality[-1]
    else:
        blocked_frontier = None
    # `nodes` is already in dependency order (deepest first), which is BOTH the
    # only legal open order and the only legal completion order: the frozen reducer
    # refuses `complete_obligation` with `OBLIGATION_NOT_DUE_AT_ORIGINATING_CUT`
    # while any prerequisite is still open (`state_reference.py:229-235`).
    for node, _prerequisites in shape["nodes"]:
        replay.apply(_complete_obligation(replay.reference, node),
                     "APPLIED", "PREREQ_COMPLETE")

    # --- decoys ---------------------------------------------------------------
    decoy_ids: list[str] = []
    for index, mechanism in enumerate(mechanisms):
        decoy_id = "OBL.DECOY.%d" % index
        if mechanism == "NOT_CRITICAL":
            event = _open_obligation(replay.reference, decoy_id, due_at=T0,
                                     critical=False, subject_id="SUB.DECOY")
        elif mechanism == "NOT_DUE":
            event = _open_obligation(replay.reference, decoy_id, due_at=T2,
                                     subject_id="SUB.DECOY")
        else:
            event = _open_obligation(replay.reference, decoy_id, due_at=T0,
                                     subject_id="SUB.DECOY",
                                     prerequisites=(BLOCKER_OBLIGATION_ID,))
        replay.apply(event, "APPLIED", "DECOY")
        decoy_ids.append(decoy_id)

    # --- the motif core -------------------------------------------------------
    if motif == "CORRECTION_RESTORATION":
        _fact_block(replay, "SUB.CR", "PRED.CR", 3, "MOTIF_CORE")
    elif motif == "OBLIGATION_LIFECYCLE":
        _lifecycle_block(replay, "complete_obligation"
                         if variation["event_order"] == "FACTS_LAST"
                         else "cancel_obligation")
    elif motif == "CROSS_SCOPE_COLLISION":
        _cross_scope_block(replay, target_id)
    elif motif == "DELEGATION_IDEMPOTENT_HANDOFF":
        _delegation_block(replay, scenario_id, omissions)
    elif motif == "MIXED_DELAYED_CONTINUITY":
        replay.apply(common.make_event("reschedule_obligation", {
            "obligation_id": BLOCKER_OBLIGATION_ID, "due_at": T1},
            state=replay.reference), "APPLIED", "MOTIF_CORE")

    # --- optional blocks, in declared priority order, inside the budget -------
    optional: list[tuple[str, int, Callable[[], None]]] = []
    if motif != "CORRECTION_RESTORATION" and not delegation:
        optional.append(("FACT", (1, 2, 4)[variation["fact_chain_depth"] - 1],
                         lambda: _fact_block(replay, "SUB.F", "PRED.F",
                                             variation["fact_chain_depth"], "FACT")))
    if "RELINK" not in omissions and not delegation:
        optional.append(("RELINK", 2, lambda: _relink_block(replay)))
    if "FOREIGN" not in omissions and not delegation:
        optional.append(("FOREIGN", 2, lambda: _foreign_block(replay)))
    if variation["event_order"] == "FACTS_FIRST":
        optional.reverse()
    # The last `cut_offer_count` steps of every program are reserved for FILLER, so
    # every OFFERED frontier sits on a structurally settled world.  Without this
    # reserve a frontier can land INSIDE a two-step block — e.g. between RELINK's
    # `link_dependency` and its `unlink_dependency`, where `OBL.SHARED` carries a
    # transient open prerequisite — and the scored cut would then measure a
    # half-applied mechanism.
    optional_ceiling = PROGRAM_EVENT_COUNT - variation["cut_offer_count"]
    included: list[str] = []
    for name, cost, runner in optional:
        if len(replay.events) + cost <= optional_ceiling:
            runner()
            included.append(name)

    # --- filler to EXACTLY 17 -------------------------------------------------
    ordinal = 0
    while len(replay.events) < PROGRAM_EVENT_COUNT:
        _filler_step(replay, ordinal)
        ordinal += 1
    if len(replay.events) != PROGRAM_EVENT_COUNT:
        raise BuildGenerationRefusal(BUILD_PROGRAM_LENGTH_INVALID)
    replay.decoy_ids = decoy_ids            # type: ignore[attr-defined]
    replay.included_blocks = included       # type: ignore[attr-defined]
    replay.blocked_frontier = blocked_frontier   # type: ignore[attr-defined]
    return replay


def _relink_block(replay: ProgramReplay) -> None:
    replay.apply(common.make_event("link_dependency", {
        "obligation_id": BC_ONLY_OBLIGATION_ID,
        "prerequisite_obligation_id": BLOCKER_OBLIGATION_ID},
        state=replay.reference), "APPLIED", "RELINK")
    replay.apply(common.make_event("unlink_dependency", {
        "obligation_id": BC_ONLY_OBLIGATION_ID,
        "prerequisite_obligation_id": BLOCKER_OBLIGATION_ID},
        state=replay.reference), "APPLIED", "RELINK")


def _foreign_block(replay: ProgramReplay) -> None:
    replay.apply(_open_obligation(replay.reference, "OBL.FOREIGN", due_at=T0,
                                  subject_id="SUB.FOREIGN",
                                  scope_id=FOREIGN_SCOPE_ID), "APPLIED", "FOREIGN")
    replay.apply(common.make_event("assert_fact", {
        "subject_id": "SUB.FOREIGN", "predicate_id": "PRED.FOREIGN",
        "value_code": "VALUE.FOREIGN"}, state=replay.reference,
        scope_id=FOREIGN_SCOPE_ID), "APPLIED", "FOREIGN")


def _action_catalog(decoy_ids: list[str], variation: dict[str, Any],
                    motif: str, ineligible_stratum: str | None,
                    target_id: str) -> list[dict[str, Any]]:
    """The FULL action catalog, derived from the candidate's own decoys.

    The three planned-ineligible shapes (§2.3) are realized HERE or in the target's
    `due_at`, and none of them costs an event — so a planned ineligible is the SAME
    17-step program as its eligible sibling, differing only in the declared shape:
      * `MISSING_NON_GOLD` — the catalog keeps only the gold and `NO_ACTION`;
      * `AMBIGUOUS_GOLD` — a second, genuinely LEGAL obligation joins the catalog
        (`OBL.SHARED` is OPEN, critical and due at T0 in every program), so the
        frozen `_unique_gold_action` returns None for two legal actions;
      * `TARGET_NOT_DUE` — the target's `due_at` is T2 (`_build_program`).
    """
    delegation = motif == "DELEGATION_IDEMPOTENT_HANDOFF"
    catalog_decoys = [HANDOFF_OBLIGATION_ID] if delegation else decoy_ids[
        :variation["catalog_size"] - 2]
    if ineligible_stratum == "MISSING_NON_GOLD":
        catalog_decoys = []
    if ineligible_stratum == "AMBIGUOUS_GOLD":
        catalog_decoys = list(catalog_decoys) + [BC_ONLY_OBLIGATION_ID]
    rows = [{"action_id": common.action_id(SCOPE_ID, oid),
             "action_kind": "ACT_ON_OBLIGATION", "scope_id": SCOPE_ID,
             "obligation_id": oid}
            for oid in [target_id] + list(catalog_decoys)]
    rows.append({"action_id": "NO_ACTION", "action_kind": "NO_ACTION"})
    rows.sort(key=lambda row: row["action_id"].encode("utf-8"))
    return rows


def _bc_selection(world: list[dict[str, Any]], catalog: list[dict[str, Any]],
                  target_id: str) -> list[str]:
    """The BUILD BC selector (§2 3(a)).  Declared rule, deterministic.

    It deliberately selects ONE observation row, the never-catalogued
    `OBL.SHARED`, and the first catalog decoy — so the BC/OM difference is
    non-degenerate in BOTH directions (see `packet.bc_om_difference`).
    """
    observations = [row["object_id"] for row in world
                    if row["object_kind"] == "OBSERVATION"]
    decoys = [row["obligation_id"] for row in catalog
              if row.get("action_kind") == "ACT_ON_OBLIGATION"
              and row["obligation_id"] != target_id]
    selected = {observations[0], BC_ONLY_OBLIGATION_ID}
    if decoys:
        selected.add(sorted(decoys)[0])
    return sorted(selected, key=lambda value: value.encode("utf-8"))


def build_candidate(motif: str, motif_index: int, index: int, motif_rank: int,
                    ineligible_stratum: str | None = None) -> dict[str, Any]:
    """One BUILD candidate: a replayed program plus everything DERIVED from it."""
    spec, _digest = authority.build_generator_spec()
    scenario_id = spec["scenario_id_template"].format(motif_index=motif_index,
                                                      index=index)
    variation = _variation_for(scenario_id, motif, motif_rank)
    target_id = target_obligation_id(scenario_id)
    replay = _build_program(scenario_id, motif, variation, ineligible_stratum)
    catalog = _action_catalog(replay.decoy_ids, variation, motif, ineligible_stratum,
                              target_id)

    frontiers: list[int] = []
    seen: set[int] = set()
    for step in range(len(replay.events), 0, -1):
        journal_seq = replay.snapshots[step]["next_seq"] - 1
        if journal_seq in seen:
            continue
        seen.add(journal_seq)
        frontiers.append(step)
        if len(frontiers) >= variation["cut_offer_count"]:
            break
    frontiers.sort()

    cut_ids: list[str] = []
    cut_by_id: dict[str, Any] = {}
    world_by_cut: dict[str, Any] = {}
    actions_by_cut: dict[str, Any] = {}
    gold_by_cut: dict[str, Any] = {}
    state_summary_by_cut: dict[str, Any] = {}
    observation_by_cut: dict[str, Any] = {}
    observation_authority_by_cut: dict[str, Any] = {}
    bc_by_cut: dict[str, Any] = {}
    state_hash_by_cut: dict[str, str] = {}
    frontier_step_by_cut: dict[str, int] = {}

    for ordinal, step in enumerate(frontiers):
        cut_id = spec["cut_id_template"].format(index=index, label="F%d" % ordinal)
        state = replay.snapshots[step]
        cut = common.current_cut(state)
        record = derive_observation_authority(
            scenario_id, cut_id,
            project_observation_inputs(state, cut, replay.events[:step],
                                       variation["observation_family_selector"]))
        world = packet.canonical_world_from_state(
            state, SCOPE_ID, cut, record, replay.events[:step])
        view = {"scope_id": SCOPE_ID, "cut": cut, "canonical_world": world,
                "action_catalog": catalog}
        gold = packets._unique_gold_action(view)
        cut_ids.append(cut_id)
        cut_by_id[cut_id] = {"cut_id": cut_id, **copy.deepcopy(cut)}
        world_by_cut[cut_id] = world
        actions_by_cut[cut_id] = packets.legal_action_ids_from_world(world, catalog, cut)
        gold_by_cut[cut_id] = gold
        observation_authority_by_cut[cut_id] = record
        observation_by_cut[cut_id] = packet.observation_manifest_representation(record)
        bc_by_cut[cut_id] = _bc_selection(world, catalog, target_id)
        state_hash_by_cut[cut_id] = sha384(state)
        frontier_step_by_cut[cut_id] = step
        obligations = state["scopes"][SCOPE_ID]["obligations"]
        target = obligations.get(target_id, {})
        state_summary_by_cut[cut_id] = {
            "scope_id": SCOPE_ID,
            "target_obligation_id": target_id,
            "obligation_count": len(obligations),
            "dependency_count": len(state["scopes"][SCOPE_ID]["dependencies"]),
            "fact_object_count": sum(1 for row in world if row["object_kind"] == "FACT"),
            "observation_object_count": sum(1 for row in world
                                            if row["object_kind"] == "OBSERVATION"),
            "target_prerequisite_ids": list(
                target.get("prerequisite_obligation_ids", [])),
        }

    candidate = {
        "scenario_id": scenario_id, "motif": motif, "scope_id": SCOPE_ID,
        "cut_ids": cut_ids, "cut_by_id": cut_by_id,
        "action_catalog": catalog,
        "action_ids_by_cut": actions_by_cut,
        "gold_action_id_by_cut": gold_by_cut,
        "canonical_state_by_cut": state_summary_by_cut,
        "canonical_world_by_cut": world_by_cut,
        "observation_by_cut": observation_by_cut,
        "observation_authority_by_cut": observation_authority_by_cut,
        "bc_selected_object_ids_by_cut": bc_by_cut,
        "authoritative_state_hash_by_cut": state_hash_by_cut,
        "event_program": replay.events,
        "event_result_codes": replay.codes,
        "variation": variation,
        "generation": {
            "program_blocks": replay.blocks,
            "included_optional_blocks": replay.included_blocks,
            "frontier_step_by_cut": frontier_step_by_cut,
            "planned_ineligible_stratum": ineligible_stratum,
            "motif_witness": _motif_witness(motif, replay, cut_ids, gold_by_cut,
                                            world_by_cut, catalog, target_id),
            "envelope_admitted": None,
            "envelope_refusal": [],
            "refusal_class": None,
            "gold_read_set_size": 0,
            "bc_om_difference_size": 0,
            "world_object_count": len(world_by_cut[cut_ids[-1]]) if cut_ids else 0,
        },
    }
    return candidate


def _motif_witness(motif: str, replay: ProgramReplay, cut_ids: list[str],
                   gold_by_cut: dict[str, Any], world_by_cut: dict[str, Any],
                   catalog: list[dict[str, Any]],
                   target_id: str) -> dict[str, Any]:
    """The row's POSTCONDITION, recorded from the replay (§2.1's first column)."""
    witness: dict[str, Any] = {"motif": motif,
                               "result_code_sequence": list(replay.codes)}
    state = replay.reference
    if motif == "CORRECTION_RESTORATION":
        cut = common.current_cut(state)
        rows = packet.fact_world_rows_from_state(state, SCOPE_ID, cut, replay.events)
        witness["restored_value_codes"] = [row["fields"]["value_code"] for row in rows
                                           if row["fields"]["subject_id"] == "SUB.CR"]
    elif motif == "OBLIGATION_LIFECYCLE":
        row = state["scopes"][SCOPE_ID]["obligations"].get(LIFECYCLE_OBLIGATION_ID, {})
        witness["lifecycle_terminal"] = row.get("lifecycle")
        witness["target_never_reopened"] = state["scopes"][SCOPE_ID]["obligations"][
            target_id]["lifecycle"] == "OPEN"
    elif motif == "DEPENDENCY_REVERSAL":
        target_action = common.action_id(SCOPE_ID, target_id)
        witness["blocked_frontier_excludes_target"] = (
            replay.blocked_frontier is not None
            and target_action not in replay.blocked_frontier)
        witness["due_after_prerequisite_completion"] = all(
            gold_by_cut[cut_id] == target_action for cut_id in cut_ids)
    elif motif == "CROSS_SCOPE_COLLISION":
        foreign = state["scopes"].get(FOREIGN_SCOPE_ID, {"obligations": {}, "facts": {}})
        scored_ids = {row["object_id"] for row in world_by_cut[cut_ids[-1]]}
        witness["journal_is_multi_scope"] = bool(foreign["obligations"])
        witness["scored_projection_zero_foreign"] = not any(
            row["fields"].get("completion_action_id")
            == common.action_id(FOREIGN_SCOPE_ID, row["object_id"])
            for row in world_by_cut[cut_ids[-1]]
            if row["object_kind"] == "OBLIGATION")
        witness["collision_object_id_in_both_scopes"] = (
            target_id in foreign["obligations"]
            and target_id in scored_ids)
    elif motif == "DELEGATION_IDEMPOTENT_HANDOFF":
        handoffs = state["scopes"][SCOPE_ID]["handoffs"]
        witness["duplicate_noop_count"] = replay.codes.count("DUPLICATE_NOOP")
        witness["handoff_terminal_dispositions"] = {
            key: row["terminal_disposition"] for key, row in sorted(handoffs.items())}
        witness["owner_role_rewritten"] = state["scopes"][SCOPE_ID]["obligations"][
            BC_ONLY_OBLIGATION_ID]["owner_role"]
    elif motif == "MIXED_DELAYED_CONTINUITY":
        world = world_by_cut[cut_ids[-1]]
        target_action = common.action_id(SCOPE_ID, target_id)
        early = packets.legal_action_ids_from_world(
            world, catalog, {"journal_seq": 0, "knowledge_time": T1, "valid_time": T0})
        late = packets.legal_action_ids_from_world(
            world, catalog, {"journal_seq": 0, "knowledge_time": T1, "valid_time": T1})
        witness["target_illegal_at_earlier_cut"] = target_action not in early
        witness["target_uniquely_legal_at_chosen_cut"] = late == [target_action]
        witness["target_never_rescheduled"] = not any(
            event["event_type"] == "reschedule_obligation"
            and event["payload"]["obligation_id"] == target_id
            for event in replay.events)
    return witness


# =============================================================================
# §2.3 the SEQUENCED plan, §2.6 coverage, §2.3 census
# =============================================================================

#: Re-export (cohort-BUILD r2 FOLD A): the §2.6 measurement is DECLARED in
#: `mbcx01_build_cohort_authority` so the provenance validator can recompute the
#: record it admits.  Same object, same number, one measurement.
sequence_coverage = authority.sequence_coverage


def _axis_values(candidate: dict[str, Any]) -> dict[str, Any]:
    values = {name: candidate["variation"].get(name) for name in CENSUS_AXES}
    for name in ("gold_read_set_size", "bc_om_difference_size"):
        values[name] = candidate["generation"].get(name)
    return values


def population_census(generated: list[dict[str, Any]],
                      retained: list[dict[str, Any]], *,
                      floors: dict[str, int] | None = None) -> dict[str, Any]:
    """The §2.3 census: marginals AND joint occupancy, with declared floors.

    A marginal-preserving deletion of one JOINT tuple is caught by
    `RETAINED_AXIS_STRATUM_MISSING` (r3 seats 1+3: two joint strata can vanish
    while every marginal stays present).  A stratum with NONZERO occupancy below
    its declared floor is caught by `RETAINED_AXIS_STRATUM_FLOOR` — one retained
    row must not read as represented.
    """
    floors = dict(DECLARED_RETAINED_FLOORS if floors is None else floors)
    eligible = [row for row in generated
                if row["generation"].get("planned_ineligible_stratum") is None]

    def marginals(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
        table: dict[str, dict[str, int]] = {name: {} for name in CENSUS_AXES}
        for row in rows:
            for name, value in _axis_values(row).items():
                key = str(value)
                table[name][key] = table[name].get(key, 0) + 1
        return {name: dict(sorted(values.items())) for name, values in table.items()}

    def joints(rows: list[dict[str, Any]]) -> dict[str, int]:
        table: dict[str, int] = {}
        for row in rows:
            values = _axis_values(row)
            key = "|".join(str(values[name]) for name in CENSUS_JOINT_AXES)
            table[key] = table.get(key, 0) + 1
        return dict(sorted(table.items()))

    generated_marginals = marginals(eligible)
    retained_marginals = marginals(retained)
    generated_joint = joints(eligible)
    retained_joint = joints(retained)

    errors: set[str] = set()
    missing_values = []
    for name, values in generated_marginals.items():
        for value in values:
            if retained_marginals[name].get(value, 0) == 0:
                missing_values.append("%s=%s" % (name, value))
    below_floor = []
    for name, values in retained_marginals.items():
        for value, count in values.items():
            if 0 < count < floors["marginal"]:
                below_floor.append("%s=%s:%d" % (name, value, count))
    missing_joint = [key for key in generated_joint if retained_joint.get(key, 0) == 0]
    joint_below_floor = [
        "%s:%d" % (key, count) for key, count in retained_joint.items()
        if 0 < count < floors["joint"]]
    if missing_values:
        errors.add(RETAINED_AXIS_VALUE_MISSING)
    if missing_joint:
        errors.add(RETAINED_AXIS_STRATUM_MISSING)
    if below_floor or joint_below_floor:
        errors.add(RETAINED_AXIS_STRATUM_FLOOR)

    # --- FOLD 2(b): the ANSWER KEY's variety, with its DECLARED floor -----------
    # The served cut is RECOMPUTED here (`_admission_cut`) rather than read back off
    # an enrichment key, so the count is a measurement of the population and not of
    # whatever a caller stamped on it.
    distinct_golds = {row["gold_action_id_by_cut"][_admission_cut(row)]
                      for row in retained}
    gold_variety_floor = len(retained)
    if len(distinct_golds) < gold_variety_floor:
        errors.add(RETAINED_GOLD_VARIETY_BELOW_FLOOR)

    # --- FOLD 2(c): the SIGNATURE x MOTIF cross-tab, MEASURED ------------------
    signature_motifs: dict[str, set[str]] = {}
    signature_rows: dict[str, int] = {}
    for row in retained:
        record = row["observation_authority_by_cut"][_admission_cut(row)]
        key = "|".join(str(record[field]) for field in OBSERVATION_SIGNATURE_FIELDS)
        signature_motifs.setdefault(key, set()).add(row["motif"])
        signature_rows[key] = signature_rows.get(key, 0) + 1
    single_motif = sorted(key for key, motifs in signature_motifs.items()
                          if len(motifs) == 1)
    single_motif_rows = sum(signature_rows[key] for key in single_motif)

    return {"schema_id": "BuildPopulationCensusV1",
            "generated_total": len(generated),
            "generated_eligible_total": len(eligible),
            "retained_total": len(retained),
            "declared_absent_axes": list(DECLARED_ABSENT_AXES),
            "declared_floors": floors,
            "census_axes": list(CENSUS_AXES),
            "joint_axes": list(CENSUS_JOINT_AXES),
            "generated_marginals": generated_marginals,
            "retained_marginals": retained_marginals,
            "generated_joint_occupancy": generated_joint,
            "retained_joint_occupancy": retained_joint,
            "missing_axis_values": sorted(missing_values),
            "missing_joint_strata": sorted(missing_joint),
            "marginals_below_floor": sorted(below_floor),
            "joint_strata_below_floor": sorted(joint_below_floor),
            "distinct_gold_action_ids": len(distinct_golds),
            "declared_gold_variety_floor": gold_variety_floor,
            "declared_gold_variety_floor_rule": DECLARED_GOLD_VARIETY_FLOOR_RULE,
            "observation_signature_fields": list(OBSERVATION_SIGNATURE_FIELDS),
            "observation_signature_total": len(signature_motifs),
            "single_motif_observation_signatures": len(single_motif),
            "rows_carrying_a_single_motif_signature": single_motif_rows,
            "single_motif_observation_signature_list": single_motif,
            "errors": sorted(errors)}


# =============================================================================
# the generation entry point
# =============================================================================

class BuildCohortGeneration:
    """The instance-scoped result of one generation run.  No module global holds it."""

    __slots__ = ("candidates", "provenance", "context", "plan", "coverage",
                 "census", "admission", "spec")

    def __init__(self, candidates: list[dict[str, Any]], provenance: dict[str, Any],
                 context: authority.BuildRetainedAuthorityContext,
                 plan: dict[str, Any], coverage: dict[str, Any],
                 census: dict[str, Any], admission: dict[str, Any],
                 spec: dict[str, Any]) -> None:
        self.candidates = candidates
        self.provenance = provenance
        self.context = context
        self.plan = plan
        self.coverage = coverage
        self.census = census
        self.admission = admission
        self.spec = spec

    def retained(self) -> list[dict[str, Any]]:
        return self.context.retained_candidates

    def retained_set_root(self) -> str:
        return authority.retained_set_root(self.context)


def generate_cohort(*, gate_census: bool = True,
                    gate_sequence_coverage: bool = True) -> BuildCohortGeneration:
    """Generate the 960-candidate BUILD population and pin its retained 768.

    §2.3's SEQUENCED total-admission arithmetic, in generation order:

      1. build all 160 candidates of a motif and RENDER each one's six nodes;
      2. count `e` = the unplanned refusals (envelope overflow OR a shape the
         derived gold predicate refuses) — every refusal class, not a subset;
      3. `e > 32` REFUSES the generation plan (a shape whose unplanned refusals
         alone exceed the floor margin cannot honestly reach 128);
      4. place EXACTLY `max(0, min(k, 32 - e))` planned ineligibles, stratified
         across `TARGET_NOT_DUE` / `AMBIGUOUS_GOLD` / `MISSING_NON_GOLD` and spread
         at most one per joint census stratum;
      5. admitted-eligible per motif is then `160 - e - placed >= 128` BY ARITHMETIC.
    """
    spec, _digest = authority.build_generator_spec()
    per_motif = spec["candidate_count_per_motif"]
    quota = spec["planned_ineligible_quota_k"]
    margin = spec["refusal_margin"]
    candidates: list[dict[str, Any]] = []
    admission: dict[str, Any] = {"schema_id": "BuildEnvelopeAdmissionSummaryV1",
                                 "per_motif": {}, "refusals": []}
    plan: dict[str, Any] = {"schema_id": "BuildGenerationPlanV1", "per_motif": {},
                            "quota_k": quota, "refusal_margin": margin}

    for motif_index, motif in enumerate(authority.MOTIFS):
        drafts = [build_candidate(motif, motif_index, index, index)
                  for index in range(per_motif)]
        unplanned: list[str] = []
        for position, candidate in enumerate(drafts):
            cut_id = _admission_cut(candidate)
            record = packet.render_all_six_nodes(candidate, cut_id=cut_id)
            candidate["generation"]["envelope_admitted"] = record["admitted"]
            candidate["generation"]["envelope_refusal"] = record["errors"]
            if not record["admitted"]:
                # §2.5: a non-servable draft is REFUSED, not silently served.  It
                # is rebuilt as a shape the DERIVED gold predicate itself refuses,
                # so nothing downstream has to read an admission flag back, and it
                # is counted in `e`.
                unplanned.append(candidate["scenario_id"])
                admission["refusals"].append(
                    {"scenario_id": candidate["scenario_id"], "class": "ENVELOPE",
                     "errors": record["errors"], "detail": record["refusal_detail"]})
                replacement = build_candidate(motif, motif_index, position, position,
                                              ineligible_stratum="MISSING_NON_GOLD")
                replacement["generation"]["envelope_admitted"] = False
                replacement["generation"]["envelope_refusal"] = record["errors"]
                replacement["generation"]["refusal_class"] = "ENVELOPE"
                drafts[position] = replacement
                continue
            if not packet.candidate_is_eligible(candidate, cut_id):
                unplanned.append(candidate["scenario_id"])
                admission["refusals"].append(
                    {"scenario_id": candidate["scenario_id"], "class": "DERIVED_GOLD",
                     "errors": ["DERIVED_GOLD_PREDICATE_REFUSED"], "detail": ""})
                candidate["generation"]["refusal_class"] = "DERIVED_GOLD"
        refused = len(unplanned)
        if refused > margin:
            raise BuildGenerationRefusal(
                "%s: motif %s unplanned refusals e=%d exceed the floor margin %d"
                % (authority.BUILD_GENERATION_PLAN_REFUSED, motif, refused, margin))
        placed_total = max(0, min(quota, margin - refused))
        placements = _plan_placements(drafts, unplanned, placed_total)
        # FOLD 3: the plan RECORD signs `placed_total`; a placer that under-places
        # (one joint stratum for every draft, at most one placement per stratum)
        # would leave the record signing a number the population never realized.
        # The arithmetic that reaches `admitted_eligible_lower_bound` is only honest
        # if the two agree, so the plan is REFUSED rather than written down wrong.
        if len(placements) != placed_total:
            raise BuildGenerationRefusal(
                "%s: motif %s requested %d planned-ineligible placements, achieved %d"
                % (authority.BUILD_GENERATION_PLAN_REFUSED, motif, placed_total,
                   len(placements)))
        for index, stratum in sorted(placements.items()):
            drafts[index] = build_candidate(motif, motif_index, index, index,
                                            ineligible_stratum=stratum)
            cut_id = _admission_cut(drafts[index])
            record = packet.render_all_six_nodes(drafts[index], cut_id=cut_id)
            drafts[index]["generation"]["envelope_admitted"] = record["admitted"]
            drafts[index]["generation"]["envelope_refusal"] = record["errors"]
            drafts[index]["generation"]["refusal_class"] = "PLANNED"
            # A DELIBERATE ineligible shape that the derived predicate still admits
            # is a plan defect, not a population: it would take a retained slot the
            # arithmetic already spent.  Verified here, at generation.
            if packet.candidate_is_eligible(drafts[index], cut_id):
                raise BuildGenerationRefusal(
                    "%s: planned ineligible %s (%s) is still eligible"
                    % (authority.BUILD_GENERATION_PLAN_REFUSED,
                       drafts[index]["scenario_id"], stratum))
        plan["per_motif"][motif] = {
            "candidates": per_motif, "unplanned_refusals": refused,
            "planned_ineligible_placed": placed_total,
            "planned_ineligible_scenarios": {
                drafts[index]["scenario_id"]: stratum
                for index, stratum in sorted(placements.items())},
            "admitted_eligible_lower_bound": per_motif - refused - placed_total}
        admission["per_motif"][motif] = {"unplanned_refusals": refused,
                                         "planned_ineligible": placed_total}
        candidates.extend(drafts)

    for candidate in candidates:
        _record_derived_axes(candidate)

    # §2.6: the coverage measurement is computed BEFORE provenance, because it
    # RIDES provenance (`MANIFEST_KEYS` is a closed frozen set, so all BUILD-side
    # identities ride provenance) with its strength t and its floor beside it.
    coverage = sequence_coverage(candidates)
    if gate_sequence_coverage and coverage["errors"]:
        raise BuildGenerationRefusal(",".join(coverage["errors"]))
    provenance = authority.build_source_provenance(candidates, coverage)
    context = authority.BuildRetainedAuthorityContext(
        candidates, provenance, packet.ELIGIBILITY_PREDICATE)
    retained = context.retained_candidates
    census = population_census(candidates, retained)
    if gate_census and census["errors"]:
        raise BuildGenerationRefusal(",".join(census["errors"]))
    return BuildCohortGeneration(candidates, provenance, context, plan, coverage,
                                 census, admission, spec)


def _admission_cut(candidate: dict[str, Any]) -> str:
    """The cut §2.5's admission render uses: the one `choose_one_cut` WILL pick.

    The arithmetic is the frozen `choose_one_cut`, imported; the authority
    recomputes it independently at selection, and disagreement would surface as a
    manifest/authority mismatch.
    """
    return authority.choose_one_cut(candidate["scenario_id"], candidate["cut_ids"],
                                    authority.BUILD_ONE_CUT_DOMAIN)


def _plan_placements(drafts: list[dict[str, Any]], unplanned: list[str],
                     placed_total: int) -> dict[int, str]:
    """Rank by framed hash, stratify across the three ineligible classes, and place
    at most ONE per joint census stratum so no governed stratum is emptied."""
    refused = set(unplanned)
    ranked = sorted(
        (index for index, row in enumerate(drafts)
         if row["scenario_id"] not in refused),
        key=lambda index: authority.hash_rank_key(
            authority.BUILD_VARIATION_DOMAINS["planned_ineligible"],
            [drafts[index]["scenario_id"]]))
    placements: dict[int, str] = {}
    used_strata: set[str] = set()
    for index in ranked:
        if len(placements) >= placed_total:
            break
        values = _axis_values(drafts[index])
        key = "|".join(str(values[name]) for name in CENSUS_JOINT_AXES)
        if key in used_strata:
            continue
        used_strata.add(key)
        placements[index] = INELIGIBLE_STRATA[len(placements) % len(INELIGIBLE_STRATA)]
    return placements


def _record_derived_axes(candidate: dict[str, Any]) -> None:
    """Record the two manifest-level census axes (§2.3) on the candidate.

    FOLD 3: this used to write `-1` on ANY failure, which is a census VALUE — a
    sentinel that a marginal counts and a reader reads as a stratum.  Every class
    the population actually contains was checked at the pin before the net was
    removed (`refusal_class` x `planned_ineligible_stratum`: (None, None),
    (PLANNED, AMBIGUOUS_GOLD), (PLANNED, MISSING_NON_GOLD), (PLANNED,
    TARGET_NOT_DUE)) — all four build a manifest and record cleanly, planned
    ineligibles included (their gold is None and their read set is empty, which is
    a RECORDED zero, not a failure), and zero candidates carried `-1`.  There is
    therefore no legitimate path into this handler, and an unexpected one is a
    WRONG NUMBER: it is refused by name instead of censused as `-1`.
    """
    cut_id = _admission_cut(candidate)
    try:
        manifest = packet.build_manifest_for_candidate(candidate, cut_id)
        difference = packet.bc_om_difference(manifest)
        candidate["generation"]["gold_read_set_size"] = len(manifest["gold_read_set"])
        candidate["generation"]["bc_om_difference_size"] = (
            len(difference["om_only_served"]) + len(difference["bc_only_served"]))
    except (KeyError, TypeError, ValueError, StopIteration,
            packet.BuildCohortPacketError) as exc:
        raise BuildGenerationRefusal(
            "%s: %s (%s) at cut %s: %s: %s"
            % (BUILD_DERIVED_AXIS_UNRECORDABLE, candidate["scenario_id"],
               candidate["motif"], cut_id, type(exc).__name__, exc)) from exc
