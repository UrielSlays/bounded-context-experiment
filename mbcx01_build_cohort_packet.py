"""BUILD population-dependent PACKET / SCORER / INFERENCE-INGRESS sibling (issue #17).

Design of record: `MBCX-01-BUILD-COHORT-CONTENT-DESIGN.md` r6 FINAL at commit
18d86d44d3a2cf28108022e626ea4bda1b430d86, §2 module 3 (a)-(f).

WHAT THIS MODULE SUPERSEDES (frozen lines cited, never edited)
--------------------------------------------------------------
(a) `mbcx01_r13_packets.manifest_for_retained_candidate` (:158-196) hard-codes
    scope, target action, ONE decoy, a three-row catalog, the BC selection and the
    gold — the population's second stamp.  `build_manifest_for_candidate` DERIVES
    all of them from the candidate.
(b) FACT world rows are projected from replayed state.  The frozen projector
    `project_state_world` (:68-95) rewrites OBLIGATION rows from state and CHECKS
    DEPENDENCY rows, but COPIES every other row unchanged (:81-93) — so projection
    equality is NOT a ghost-FACT discriminator.  `validate_build_manifest` re-derives
    the FACT rows from the replayed journal and refuses a row without ancestry (W21).
(c) Both observation representations (the manifest top-level `observation` and the
    world OBSERVATION rows) are derived HERE from the single §2.2
    `ObservationAuthorityV1` record, so divergence is unrepresentable (W15/§2.2).
    The §2.2 DERIVATION LAW itself lives here too as of cohort-BUILD r1 FOLD 1(b) —
    `derive_observation_authority` with `OBSERVATION_FAMILIES`,
    `OBSERVATION_FAMILY_SHORT`, `OBSERVATION_FAMILY_BASE_CARDINALITY`,
    `OBSERVATION_ALLOWED_FIELDS` and `BUILD_OBSERVATION_PROJECTION_LEAK` — because
    the SERVING boundary must RE-DERIVE the record and the import arrow runs
    generator -> packet.  The generator keeps `project_observation_inputs` (it reads
    generation state) and uses this module's law.
(d) `authoritative_state` is SUPPLIED from the replayed generation state.  The
    frozen default `_fixture_authoritative_state` (:352-376) builds from
    `initial_state()`'s hard-coded `OBL.SHARED`/`OBL.PREREQ` literals and enforces
    exact obligation-set equality, so it refuses any renamed population; it is the
    default at `build_scoring_fixture:576` and `build_transition_authority:422`
    when `authoritative_state=None`.  `build_scoring_fixture_for_candidate` never
    passes None, and witnesses `project_state_world` equality before it calls
    (W18).
(e) `verify_build_scorer_input` is the EXACT-SUBTRACTIVE wrapper on the lane's own
    shelf pattern (`mbcx01_build_state_authority.verify_production_scorer_input`,
    :1009-1044).  The frozen validators run UNMODIFIED and their verdict is never
    edited; the only permitted act is declining to re-add the cascade that the
    FROZEN POPULATION AUTHORITY caused — and only when the BUILD authority supplies
    the stronger evidence.  See `POPULATION_AUTHORITY_CASCADE_CLOSURE`.
(f) `ordered_decision_from_build_episode_receipts` is the BUILD inference ingress.
    The frozen `derive_episode_partition` (`mbcx01_r13_inference.py:141-165`) and the
    frozen numerical core `ordered_decision_with_missingness` (:122-138) run
    UNMODIFIED; only receipt ADMISSION differs, and the membership list is DERIVED
    from the BUILD pinned retained authority instead of accepted from the caller
    (`mbcx01_r13_inference.py:141-165` validates only the SUPPLIED list's internal
    ordering, which is how 768 phantom IDs reached the numerical core in gate r1).

ADVERSARY / REFUSAL POSTURE
---------------------------
No threat model.  Every refusal here stops a WRONG NUMBER: a ghost FACT row
(evidence with no journal ancestry), an unservable packet (envelope overflow), a
divergent observation (two representations of one record disagreeing), a phantom
membership (an ID list that is not the retained population), a laundered scorer
verdict (a frozen error silently dropped).  None of them stops a person.

IMPORT DIRECTION (no cycles): frozen modules + `mbcx01_build_cohort_authority`.
`mbcx01_build_cohort_generator` imports this module; this module never imports it.
"""

from __future__ import annotations

import copy
from typing import Any, Callable

import mbcx01_r13_common as common
import mbcx01_r13_inference as inference
import mbcx01_r13_measurement as measurement
import mbcx01_r13_packets as packets
import mbcx01_r13_state_oracle as state_oracle
import mbcx01_r13_state_reference as state_reference
import mbcx01_build_cohort_authority as authority

sha384 = measurement.sha384
sha256 = measurement.sha256
canonical_json = measurement.canonical_json

#: Frozen couplings this module lives inside (design §2 "Frozen couplings").
MANIFEST_SCHEMA_ID = "ExpectedScenarioManifestV3"
ROUTE_CONTRACT_HASH = "D" * 96
BUILD_SELECTOR_ID = "SELECTOR.BUILD.BC.V1"
ENVELOPE_BYTES = packets.ENVELOPE_BYTES              # 65536, `mbcx01_r13_packets.py:18`
EPISODE_NODES = ("A0", "B", "A1")
CONDITIONS = ("BC", "OM")

#: §2.5's declared shape ceiling, recorded as a constant (the measured ~190-200
#: world objects at default ID lengths is input-shape-sensitive; the BUILD
#: generator stays an order of magnitude below it and the renderer is still the
#: only admission authority).
DECLARED_WORLD_OBJECT_CEILING = 190

#: The ADMISSION binding (§2.5): envelope admission runs BEFORE selection, so the
#: retained position/root are not yet known.  The admission manifest uses the
#: LONGEST legal position and an all-F root, so the admission render is never
#: shorter than the served render.  W13 re-executes every render on the FINAL
#: served manifests of the retained 768.
ADMISSION_RETAINED_POSITION = 767
ADMISSION_DIGEST = "F" * 96

# --- closed error vocabulary --------------------------------------------------

BUILD_MANIFEST_SCHEMA_INVALID = "BUILD_MANIFEST_SCHEMA_INVALID"
BUILD_FACT_ROW_WITHOUT_JOURNAL_ANCESTRY = "BUILD_FACT_ROW_WITHOUT_JOURNAL_ANCESTRY"
BUILD_OBSERVATION_REPRESENTATION_DIVERGENT = "BUILD_OBSERVATION_REPRESENTATION_DIVERGENT"
BUILD_AUTHORITATIVE_STATE_MISMATCH = "BUILD_AUTHORITATIVE_STATE_MISMATCH"
BUILD_EVENT_PROGRAM_REPLAY_MISMATCH = "BUILD_EVENT_PROGRAM_REPLAY_MISMATCH"
BUILD_GOLD_DERIVATION_MISMATCH = "BUILD_GOLD_DERIVATION_MISMATCH"
BUILD_ACTION_CATALOG_MISMATCH = "BUILD_ACTION_CATALOG_MISMATCH"
BUILD_BC_SELECTION_DEGENERATE = "BUILD_BC_SELECTION_DEGENERATE"
BUILD_ENVELOPE_EXCEEDED = "BUILD_ENVELOPE_EXCEEDED"
BUILD_SCORER_INPUT_INVALID = "BUILD_SCORER_INPUT_INVALID"
BUILD_POPULATION_AUTHORITY_INERTNESS_FAILED = "BUILD_POPULATION_AUTHORITY_INERTNESS_FAILED"
BUILD_SCENARIO_OUTCOME_AUTHORITY_INVALID = "BUILD_SCENARIO_OUTCOME_AUTHORITY_INVALID"
BUILD_EPISODE_PARTITION_MISMATCH = "BUILD_EPISODE_PARTITION_MISMATCH"
BUILD_GOLD_READ_SET_VARIETY_BELOW_FLOOR = "BUILD_GOLD_READ_SET_VARIETY_BELOW_FLOOR"
BUILD_BC_OM_DIFFERENCE_DEGENERATE = "BUILD_BC_OM_DIFFERENCE_DEGENERATE"
BUILD_OM_ONLY_EVIDENCE_NOT_NECESSARY = "BUILD_OM_ONLY_EVIDENCE_NOT_NECESSARY"

#: RAISE-ONLY, and deliberately NOT in `BUILD_PACKET_ERROR_CODES`: it is the
#: derivation's own allowlist assertion (§2.2), not a manifest verdict.  Moved here
#: with the derivation law by cohort-BUILD r1 FOLD 1(b); the derivation binding
#: converts it into `BUILD_OBSERVATION_REPRESENTATION_DIVERGENT` before it can reach
#: a caller's error list.
#:
#: cohort-BUILD r2 rider (council r2 seat 1): the STRING is now DECLARED in
#: `mbcx01_build_cohort_authority`'s closed-vocabulary block and is a member of
#: `BUILD_COHORT_ERROR_CODES`, so a raised name resolves in a declared vocabulary
#: instead of nowhere.  Nothing else changes: it stays raise-only here, and it stays
#: out of `BUILD_PACKET_ERROR_CODES` for the reason above.
BUILD_OBSERVATION_PROJECTION_LEAK = authority.BUILD_OBSERVATION_PROJECTION_LEAK

#: The frozen manifest/scorer codes this module may PASS THROUGH unedited.
FROZEN_MANIFEST_ERROR_CODES = frozenset({
    "MANIFEST_SCHEMA_INVALID", "DUPLICATE_OBJECT_ID", "CANONICAL_WORLD_HASH_MISMATCH",
    "ACTION_CATALOG_HASH_MISMATCH", "ROUTE_CONTRACT_INVALID",
    "BC_SELECTION_HASH_MISMATCH", "BC_SELECTION_INVALID", "GOLD_ACTION_INVALID",
    "GOLD_READ_SET_INVALID", "EXPECTED_A1_INVALID", "MANIFEST_HASH_MISMATCH",
})

BUILD_PACKET_ERROR_CODES = frozenset(FROZEN_MANIFEST_ERROR_CODES | {
    BUILD_MANIFEST_SCHEMA_INVALID,
    BUILD_FACT_ROW_WITHOUT_JOURNAL_ANCESTRY,
    BUILD_OBSERVATION_REPRESENTATION_DIVERGENT,
    BUILD_AUTHORITATIVE_STATE_MISMATCH,
    BUILD_EVENT_PROGRAM_REPLAY_MISMATCH,
    BUILD_GOLD_DERIVATION_MISMATCH,
    BUILD_ACTION_CATALOG_MISMATCH,
    BUILD_BC_SELECTION_DEGENERATE,
    BUILD_ENVELOPE_EXCEEDED,
    BUILD_SCORER_INPUT_INVALID,
    BUILD_POPULATION_AUTHORITY_INERTNESS_FAILED,
    BUILD_SCENARIO_OUTCOME_AUTHORITY_INVALID,
    BUILD_EPISODE_PARTITION_MISMATCH,
    BUILD_GOLD_READ_SET_VARIETY_BELOW_FLOOR,
    BUILD_BC_OM_DIFFERENCE_DEGENERATE,
    BUILD_OM_ONLY_EVIDENCE_NOT_NECESSARY,
})

#: W10 declared constants (BUILD-time values; the suite pins them).
DECLARED_MIN_DISTINCT_GOLD_READ_SETS = 16
OM_ONLY_NECESSITY_COVERAGE_CLASS = "TARGET_PREREQUISITE_LIFECYCLE"
OM_ONLY_REGISTERED_COUNTERFACTUAL = "PREREQUISITE_LIFECYCLE_COMPLETED_TO_OPEN"


class BuildCohortPacketError(ValueError):
    """Typed, closed failure of the BUILD packet/scorer/ingress sibling."""


def _closed(errors: Any) -> list[str]:
    values = set(errors)
    known = {code for code in values if code in BUILD_PACKET_ERROR_CODES}
    if known != values:
        known.add(BUILD_MANIFEST_SCHEMA_INVALID)
    return sorted(known)


# =============================================================================
# (c) observation — BOTH representations from the ONE authority record
# =============================================================================

OBSERVATION_AUTHORITY_SCHEMA_ID = "ObservationAuthorityV1"
OBSERVATION_AUTHORITY_KEYS = frozenset({
    "schema_id", "scenario_id", "cut_id", "family", "code", "observed_at",
    "cardinality", "order", "rows", "projection", "projection_hash", "record_hash"})


def observation_manifest_representation(record: dict[str, Any]) -> dict[str, Any]:
    """The manifest's top-level `observation`, derived from the record ALONE."""
    return {"scope_id": record["projection"]["scope_id"],
            "observed_at": record["observed_at"],
            "family": record["family"],
            "code": record["code"],
            "cardinality": record["cardinality"],
            "order": record["order"]}


def observation_world_rows(record: dict[str, Any]) -> list[dict[str, Any]]:
    """The world OBSERVATION rows, derived from the SAME record ALONE."""
    rows = [{"object_id": row["object_id"], "object_kind": "OBSERVATION",
             "fields": {"code": row["code"], "observed_at": record["observed_at"],
                        "family": record["family"], "ordinal": row["ordinal"]},
             "source_event_ids": []}
            for row in record["rows"]]
    return sorted(rows, key=lambda row: row["object_id"].encode("utf-8"))


def observation_record_hash(record: dict[str, Any]) -> str:
    return sha384({key: value for key, value in record.items() if key != "record_hash"})


def validate_observation_authority_record(record: Any) -> bool:
    """SELF-CONSISTENCY only: shape, cardinality and the record's own two hashes.

    This is NOT a derivation check — a record rebuilt consistently around any value
    passes it.  `observation_derivation_errors` is the derivation half.
    """
    return (isinstance(record, dict) and set(record) == set(OBSERVATION_AUTHORITY_KEYS)
            and record.get("schema_id") == OBSERVATION_AUTHORITY_SCHEMA_ID
            and isinstance(record.get("rows"), list) and bool(record["rows"])
            and record.get("cardinality") == len(record["rows"])
            and record.get("record_hash") == observation_record_hash(record)
            and record.get("projection_hash") == sha384(record.get("projection")))


# --- §2.2 the derivation law (moved here from the generator, FOLD 1(b)) -------

OBSERVATION_FAMILIES = ("COUNT_SUMMARY", "TEMPORAL_WINDOW", "STRUCTURE_DEPTH",
                        "SCOPE_DIGEST")
OBSERVATION_FAMILY_SHORT = {"COUNT_SUMMARY": "CNT", "TEMPORAL_WINDOW": "TMP",
                            "STRUCTURE_DEPTH": "STR", "SCOPE_DIGEST": "SCP"}
OBSERVATION_FAMILY_BASE_CARDINALITY = {"COUNT_SUMMARY": 1, "TEMPORAL_WINDOW": 2,
                                       "STRUCTURE_DEPTH": 2, "SCOPE_DIGEST": 1}

#: The ONLY fields the observation derivation rule may read.  The generator's
#: `project_observation_inputs` returns exactly these keys and the derivation asserts
#: exactly these keys, so a forbidden input cannot REACH the rule — unrepresentable,
#: not merely detected (§2.2).  `OBSERVATION_FORBIDDEN_INPUTS` stays in the generator
#: beside the generation-time projection it documents.
OBSERVATION_ALLOWED_FIELDS = (
    "scope_id",
    "cut_knowledge_time",
    "cut_valid_time",
    "obligation_row_count",
    "fact_row_count",
    "distinct_subject_count",
    "observation_family_selector",
)


def derive_observation_authority(scenario_id: str, cut_id: str,
                                 projection: dict[str, Any]) -> dict[str, Any]:
    """The §2.2 derivation rule.  It reads the PROJECTION and nothing else."""
    if set(projection) != set(OBSERVATION_ALLOWED_FIELDS):
        raise BuildCohortPacketError(BUILD_OBSERVATION_PROJECTION_LEAK)
    selector = projection["observation_family_selector"]
    family = OBSERVATION_FAMILIES[selector % len(OBSERVATION_FAMILIES)]
    cardinality = OBSERVATION_FAMILY_BASE_CARDINALITY[family] + (selector // 4) % 2
    order = "ASCENDING" if selector % 2 == 0 else "DESCENDING"
    if family == "COUNT_SUMMARY":
        code = "POPULATION.COUNT.%d" % projection["obligation_row_count"]
    elif family == "TEMPORAL_WINDOW":
        code = "WINDOW.%s" % projection["cut_valid_time"][:10].replace("-", ".")
    elif family == "STRUCTURE_DEPTH":
        code = "FACT.DEPTH.%d" % projection["fact_row_count"]
    else:
        code = "SCOPE.%s" % sha256([projection["scope_id"]])[:8]
    ordinals = (list(range(cardinality)) if order == "ASCENDING"
                else list(reversed(range(cardinality))))
    rows = [{"object_id": "OBS.%s.%d" % (OBSERVATION_FAMILY_SHORT[family], ordinal),
             "ordinal": ordinal,
             "code": "%s.%d" % (code, ordinal)} for ordinal in ordinals]
    record = {"schema_id": OBSERVATION_AUTHORITY_SCHEMA_ID,
              "scenario_id": scenario_id, "cut_id": cut_id, "family": family,
              "code": code, "observed_at": projection["cut_knowledge_time"],
              "cardinality": cardinality, "order": order, "rows": rows,
              "projection": copy.deepcopy(projection),
              "projection_hash": sha384(projection), "record_hash": ""}
    record["record_hash"] = observation_record_hash(record)
    return record


# =============================================================================
# (b)/(d) replay — the authoritative state and the endogenous FACT rows
# =============================================================================

def replay_event_program(candidate: dict[str, Any], step_count: int,
                         *, dual: bool = False) -> dict[str, Any]:
    """Replay the candidate's journal prefix and return the exact generation state.

    At GENERATION the program is replayed through BOTH frozen reducers with byte
    equality at every step (§2.7, `mbcx01_build_cohort_generator`).  Here the
    replay is a RE-DERIVATION of an already-gated journal, so the reference reducer
    alone is run by default and the result is bound by the recorded state digest
    (`authoritative_state_hash_by_cut`); `dual=True` re-runs the full gate.
    """
    state = common.initial_state()
    program = candidate["event_program"]
    codes = candidate["event_result_codes"]
    if step_count > len(program):
        raise BuildCohortPacketError(BUILD_EVENT_PROGRAM_REPLAY_MISMATCH)
    for index in range(step_count):
        event = copy.deepcopy(program[index])
        new_state, result = state_reference.reference_apply(state, event)
        if dual:
            oracle_state, oracle_result = state_oracle.oracle_apply(
                copy.deepcopy(state), copy.deepcopy(event))
            if (oracle_result != result
                    or canonical_json(oracle_state) != canonical_json(new_state)):
                raise BuildCohortPacketError(BUILD_EVENT_PROGRAM_REPLAY_MISMATCH)
        if result != codes[index]:
            raise BuildCohortPacketError(BUILD_EVENT_PROGRAM_REPLAY_MISMATCH)
        state = new_state
    return state


def authoritative_state_for_cut(candidate: dict[str, Any], cut_id: str,
                                *, dual: bool = False) -> dict[str, Any]:
    """The replayed generation state at one offered cut, bound by its recorded digest."""
    step_count = candidate["generation"]["frontier_step_by_cut"][cut_id]
    state = replay_event_program(candidate, step_count, dual=dual)
    if sha384(state) != candidate["authoritative_state_hash_by_cut"][cut_id]:
        raise BuildCohortPacketError(BUILD_EVENT_PROGRAM_REPLAY_MISMATCH)
    return state


def journal_fact_ancestry(event_program: list[dict[str, Any]],
                          scope_id: str) -> dict[str, dict[str, str]]:
    """Map every fact-writing EVENT ID in the journal to its (subject, predicate).

    This IS the ancestry relation.  `state["scopes"][...]["facts"]` is keyed by
    `fact_key(subject, predicate)` (`mbcx01_r13_common.py:101-102`) — a one-way
    digest — and `state["events"]` stores only a digest, so the pair cannot be read
    back out of state at all.  It is read out of the JOURNAL, which is exactly why a
    FACT row with no journal ancestor is unrepresentable here (W21).
    """
    ancestry: dict[str, dict[str, str]] = {}
    for event in event_program:
        if (event.get("scope_id") != scope_id
                or event.get("event_type") not in {"assert_fact", "correct_fact"}):
            continue
        payload = event["payload"]
        ancestry[event["event_id"]] = {"subject_id": payload["subject_id"],
                                       "predicate_id": payload["predicate_id"]}
    return ancestry


def fact_world_rows_from_state(state: dict[str, Any], scope_id: str,
                               cut: dict[str, Any],
                               event_program: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Project FACT rows ENDOGENOUSLY: only rows VISIBLE in the replayed journal.

    A row that no journal event ever asserted cannot be produced here, which is why
    this — not `project_state_world` (:81-93 copies non-obligation rows unchanged)
    — is the ghost-FACT discriminator (W21).
    """
    ancestry = journal_fact_ancestry(event_program, scope_id)
    rows = []
    for key, versions in state["scopes"][scope_id]["facts"].items():
        for version in versions:
            if not state_reference.visible_effective(version, cut):
                continue
            source = ancestry.get(version["event_id"])
            if source is None or state["events"].get(version["event_id"]) is None:
                raise BuildCohortPacketError(BUILD_FACT_ROW_WITHOUT_JOURNAL_ANCESTRY)
            if common.fact_key(source["subject_id"], source["predicate_id"]) != key:
                raise BuildCohortPacketError(BUILD_FACT_ROW_WITHOUT_JOURNAL_ANCESTRY)
            rows.append({
                "object_id": "FACT.%s.%s" % (source["subject_id"], source["predicate_id"]),
                "object_kind": "FACT",
                "fields": {"subject_id": source["subject_id"],
                           "predicate_id": source["predicate_id"],
                           "value_code": version["value_code"],
                           "valid_from": version["valid_from"],
                           "valid_to": version["valid_to"]},
                "source_event_ids": [version["event_id"]]})
    return sorted(rows, key=lambda row: row["object_id"].encode("utf-8"))


def obligation_world_rows(state: dict[str, Any], scope_id: str) -> list[dict[str, Any]]:
    """OBLIGATION rows for EVERY obligation in the scored scope.

    Totality is forced by the frozen projector: `project_state_world` (:78) raises
    `MANIFEST_STATE_PROJECTION_MISMATCH` unless the registered obligation set equals
    the scope's obligation set, so the world can never hide a population member.
    """
    obligations = state["scopes"][scope_id]["obligations"]
    rows = [{"object_id": oid, "object_kind": "OBLIGATION",
             "fields": {key: copy.deepcopy(row[key]) for key in (
                 "subject_id", "owner_role", "lifecycle", "critical", "due_at",
                 "completion_action_id", "prerequisite_obligation_ids")},
             "source_event_ids": [row["terminal_event_id"]] if row.get("terminal_event_id")
             else []}
            for oid, row in obligations.items()]
    return sorted(rows, key=lambda row: row["object_id"].encode("utf-8"))


def dependency_world_rows(state: dict[str, Any], scope_id: str) -> list[dict[str, Any]]:
    rows = [{"object_id": "DEP.%s.%s" % (child, parent), "object_kind": "DEPENDENCY",
             "fields": {"obligation_id": child, "prerequisite_obligation_id": parent},
             "source_event_ids": []}
            for child, parent in state["scopes"][scope_id]["dependencies"]]
    return sorted(rows, key=lambda row: row["object_id"].encode("utf-8"))


def canonical_world_from_state(state: dict[str, Any], scope_id: str,
                               cut: dict[str, Any],
                               observation_record: dict[str, Any],
                               event_program: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The whole world: obligations + dependencies + ENDOGENOUS facts + observations."""
    world = (obligation_world_rows(state, scope_id)
             + dependency_world_rows(state, scope_id)
             + fact_world_rows_from_state(state, scope_id, cut, event_program)
             + observation_world_rows(observation_record))
    return sorted(world, key=lambda row: row["object_id"].encode("utf-8"))


# --- the DERIVATION BINDING (cohort-BUILD r1 FOLD 1(a)) ----------------------

def observation_projection_from_state(candidate: dict[str, Any], cut_id: str,
                                      state: dict[str, Any]) -> dict[str, Any]:
    """Recompute the §2.2 allowlist projection from the REPLAYED state.

    The generator's `project_observation_inputs` computes the same seven fields at
    generation from the same replayed state; this is the serving-side recompute, so a
    stored projection that describes a world the journal never produced is caught.
    The event PREFIX is not needed: `fact_world_rows_from_state` reads ancestry by
    event id and the state already stops at the cut, so the full program yields the
    same rows (the same reason `validate_build_manifest` passes the full program).
    """
    scope_id = candidate["scope_id"]
    cut = {key: value for key, value in candidate["cut_by_id"][cut_id].items()
           if key != "cut_id"}
    facts = fact_world_rows_from_state(state, scope_id, cut,
                                       candidate["event_program"])
    projection = {
        "scope_id": scope_id,
        "cut_knowledge_time": cut["knowledge_time"],
        "cut_valid_time": cut["valid_time"],
        "obligation_row_count": len(state["scopes"][scope_id]["obligations"]),
        "fact_row_count": len(facts),
        "distinct_subject_count": len({row["fields"]["subject_id"] for row in facts}),
        "observation_family_selector": candidate["variation"][
            "observation_family_selector"],
    }
    if set(projection) != set(OBSERVATION_ALLOWED_FIELDS):
        raise BuildCohortPacketError(BUILD_OBSERVATION_PROJECTION_LEAK)
    return projection


def observation_derivation_errors(candidate: dict[str, Any], cut_id: str,
                                  state: dict[str, Any]) -> set[str]:
    """The observation record must BE the derivation, and its projection BE reality.

    Two bindings, one name (`BUILD_OBSERVATION_REPRESENTATION_DIVERGENT`):

    1. RE-DERIVATION — the stored record must byte-equal
       `derive_observation_authority(scenario_id, cut_id, record["projection"])`
       recomputed fresh.  `validate_observation_authority_record` only checks the
       record against ITSELF, so a record rebuilt consistently around any value
       (cohort-BUILD r1 R6: the literal gold action id) passes it.
    2. PROJECTION — the stored projection must byte-equal the recompute from the
       replayed state and the candidate's declared variation, so the derivation
       cannot be fed a fiction it will then faithfully reproduce.

    TOTAL by construction: every fault, including the derivation's own allowlist
    refusal, becomes the named divergence instead of a traceback.
    """
    try:
        record = candidate["observation_authority_by_cut"][cut_id]
        if not validate_observation_authority_record(record):
            return {BUILD_OBSERVATION_REPRESENTATION_DIVERGENT}
        projection = record["projection"]
        if derive_observation_authority(candidate["scenario_id"], cut_id,
                                        projection) != record:
            return {BUILD_OBSERVATION_REPRESENTATION_DIVERGENT}
        if observation_projection_from_state(candidate, cut_id, state) != projection:
            return {BUILD_OBSERVATION_REPRESENTATION_DIVERGENT}
    except (BuildCohortPacketError, AttributeError, IndexError, KeyError, TypeError,
            ValueError):
        return {BUILD_OBSERVATION_REPRESENTATION_DIVERGENT}
    return set()


# =============================================================================
# eligibility — DERIVED through the frozen gold predicate (§2.3)
# =============================================================================

def gold_predicate_view(candidate: dict[str, Any], cut_id: str) -> dict[str, Any]:
    """The minimal manifest view the FROZEN gold predicate reads (:34-52)."""
    cut = {key: value for key, value in candidate["cut_by_id"][cut_id].items()
           if key != "cut_id"}
    return {"scope_id": candidate["scope_id"],
            "cut": cut,
            "canonical_world": candidate["canonical_world_by_cut"][cut_id],
            "action_catalog": candidate["action_catalog"]}


def candidate_gold_action(candidate: dict[str, Any], cut_id: str) -> str | None:
    """The gold, derived by the FROZEN `_unique_gold_action` — never declared."""
    return packets._unique_gold_action(gold_predicate_view(candidate, cut_id))


def non_gold_action_ids(candidate: dict[str, Any], gold: str | None) -> list[str]:
    return sorted(row["action_id"] for row in candidate["action_catalog"]
                  if row.get("action_kind") == "ACT_ON_OBLIGATION"
                  and row.get("action_id") != gold)


def candidate_is_eligible(candidate: dict[str, Any], cut_id: str) -> bool:
    """§2.3's derived predicate: unique gold AND at least one non-gold action.

    This callable is what `mbcx01_build_cohort_authority.select_build_cohort` is
    given; it is the ONLY eligibility source in the BUILD lane, and it reads NO
    stored Boolean — not even the envelope-admission record.  §2.5's envelope
    refusal is enforced STRUCTURALLY instead: the generator rebuilds a
    non-servable draft as a shape this predicate itself refuses, and counts it in
    the plan's `e`.  Reading an admission flag back here would be exactly the
    declared-Boolean move W2 refuses.
    """
    try:
        gold = candidate_gold_action(candidate, cut_id)
        if gold is None:
            return False
        return bool(non_gold_action_ids(candidate, gold))
    except (KeyError, TypeError, ValueError, AttributeError):
        return False


# =============================================================================
# (a) manifest derivation FROM the candidate
# =============================================================================

def build_manifest_for_candidate(candidate: dict[str, Any], cut_id: str, *,
                                 context: authority.BuildRetainedAuthorityContext | None = None,
                                 scenario_authority: dict[str, Any] | None = None
                                 ) -> dict[str, Any]:
    """Derive the served manifest from the candidate — scope, target, decoys, FULL
    catalog, gold, read set and BC selection all come from the population (§2 3(a)).

    With `context` (or an explicit `scenario_authority`) the retained position/root
    are the BUILD pinned authority's.  Without either, the ADMISSION binding is used
    (§2.5): envelope admission runs before selection exists.
    """
    if scenario_authority is None and context is not None:
        scenario_authority = authority.retained_scenario_authority(context, candidate)
    if scenario_authority is None:
        source_candidate_hash = sha384(candidate)
        source_provenance_hash = ADMISSION_DIGEST
        retained_set_root = ADMISSION_DIGEST
        retained_position = ADMISSION_RETAINED_POSITION
    else:
        source_candidate_hash = scenario_authority["candidate_hash"]
        source_provenance_hash = scenario_authority["source_provenance_hash"]
        retained_set_root = scenario_authority["retained_set_root"]
        retained_position = scenario_authority["retained_position"]
    record = candidate["observation_authority_by_cut"][cut_id]
    cut = {key: value for key, value in candidate["cut_by_id"][cut_id].items()
           if key != "cut_id"}
    world = copy.deepcopy(candidate["canonical_world_by_cut"][cut_id])
    catalog = copy.deepcopy(candidate["action_catalog"])
    manifest = {
        "schema_id": MANIFEST_SCHEMA_ID,
        "scenario_id": candidate["scenario_id"],
        "scope_id": candidate["scope_id"],
        "motif": candidate["motif"],
        "cut": cut,
        "observation": observation_manifest_representation(record),
        "canonical_world": world,
        "canonical_world_hash": sha384(world),
        "action_catalog": catalog,
        "action_catalog_hash": sha384(catalog),
        "route_contract_hash": ROUTE_CONTRACT_HASH,
        "candidate_selector_id": BUILD_SELECTOR_ID,
        "bc_selected_object_ids": copy.deepcopy(
            candidate["bc_selected_object_ids_by_cut"][cut_id]),
        "bc_selection_hash": "",
        "gold_read_set": [],
        "gold_action_id": candidate["gold_action_id_by_cut"][cut_id],
        "expected_a1_action_ids": [],
        "source_candidate_hash": source_candidate_hash,
        "source_provenance_hash": source_provenance_hash,
        "retained_set_root": retained_set_root,
        "retained_position": retained_position,
    }
    manifest["bc_selection_hash"] = sha384([
        manifest["candidate_selector_id"], manifest["bc_selected_object_ids"]])
    if manifest["gold_action_id"] is not None:
        manifest["gold_read_set"] = packets._expected_gold_read_set(
            manifest, manifest["gold_action_id"])
    manifest["manifest_hash"] = packets.hash_without(manifest, "manifest_hash")
    return manifest


def served_manifest_for_retained_candidate(
        context: authority.BuildRetainedAuthorityContext,
        candidate: dict[str, Any]) -> dict[str, Any]:
    """The served manifest of one RETAINED BUILD candidate (its chosen cut)."""
    return build_manifest_for_candidate(candidate, candidate["chosen_cut_id"],
                                        context=context)


# =============================================================================
# manifest validation — the BUILD half the frozen validator structurally cannot do
# =============================================================================

def validate_build_manifest(manifest: Any, candidate: dict[str, Any], cut_id: str, *,
                            context: authority.BuildRetainedAuthorityContext | None = None,
                            authoritative_state: dict[str, Any] | None = None
                            ) -> list[str]:
    """Frozen manifest validation UNMODIFIED, plus the five BUILD-owned bindings.

    1. FACT ancestry (W21) — every FACT row re-derived from the replayed journal.
    2. Observation consistency (§2.2) — both representations from ONE record.
    2b. Observation DERIVATION (FOLD 1(a)) — the record re-derived from its own
       stored projection, and that projection recomputed from the replayed state.
    3. Supplied-state binding (W18) — `project_state_world` equality against the
       state the journal actually produced, digest-bound.
    4. Population bindings — gold, catalog, legal set and BC selection all equal the
       candidate's own derived values, and the BC/OM difference is non-degenerate.
    """
    errors: set[str] = set(packets.validate_expected_manifest(manifest))
    if not isinstance(manifest, dict):
        return _closed(errors | {BUILD_MANIFEST_SCHEMA_INVALID})
    try:
        record = candidate["observation_authority_by_cut"][cut_id]
        if not validate_observation_authority_record(record):
            errors.add(BUILD_OBSERVATION_REPRESENTATION_DIVERGENT)
        elif (manifest.get("observation") != observation_manifest_representation(record)
                or [row for row in manifest.get("canonical_world", [])
                    if isinstance(row, dict) and row.get("object_kind") == "OBSERVATION"]
                != observation_world_rows(record)):
            errors.add(BUILD_OBSERVATION_REPRESENTATION_DIVERGENT)

        state = (authoritative_state if authoritative_state is not None
                 else authoritative_state_for_cut(candidate, cut_id))
        errors |= observation_derivation_errors(candidate, cut_id, state)
        cut = {key: value for key, value in candidate["cut_by_id"][cut_id].items()
               if key != "cut_id"}
        derived_facts = fact_world_rows_from_state(
            state, candidate["scope_id"], cut, candidate["event_program"])
        manifest_facts = [row for row in manifest.get("canonical_world", [])
                          if isinstance(row, dict) and row.get("object_kind") == "FACT"]
        if manifest_facts != derived_facts:
            errors.add(BUILD_FACT_ROW_WITHOUT_JOURNAL_ANCESTRY)

        if state_reference.current_cut(state) != manifest.get("cut"):
            errors.add(BUILD_AUTHORITATIVE_STATE_MISMATCH)
        else:
            try:
                if packets.project_state_world(state, manifest) != manifest["canonical_world"]:
                    errors.add(BUILD_AUTHORITATIVE_STATE_MISMATCH)
            except (KeyError, TypeError, ValueError):
                errors.add(BUILD_AUTHORITATIVE_STATE_MISMATCH)

        if manifest.get("action_catalog") != candidate["action_catalog"]:
            errors.add(BUILD_ACTION_CATALOG_MISMATCH)
        gold = candidate_gold_action(candidate, cut_id)
        legal = packets.legal_action_ids_from_world(
            manifest.get("canonical_world", []), manifest.get("action_catalog", []),
            manifest.get("cut", {}))
        if (gold is None or manifest.get("gold_action_id") != gold
                or gold != candidate["gold_action_id_by_cut"][cut_id]
                or legal != candidate["action_ids_by_cut"][cut_id]
                or not non_gold_action_ids(candidate, gold)):
            errors.add(BUILD_GOLD_DERIVATION_MISMATCH)
        if manifest.get("bc_selected_object_ids") != candidate[
                "bc_selected_object_ids_by_cut"][cut_id]:
            errors.add(BUILD_BC_SELECTION_DEGENERATE)
        elif not errors:
            difference = bc_om_difference(manifest)
            if not difference["bc_only_selected"] or not difference["om_only_selected"] \
                    or not difference["om_only_served"] or not difference["bc_only_served"]:
                errors.add(BUILD_BC_OM_DIFFERENCE_DEGENERATE)
        if context is not None:
            scenario_authority = authority.retained_scenario_authority(context, candidate)
            if (manifest.get("source_candidate_hash") != scenario_authority["candidate_hash"]
                    or manifest.get("source_provenance_hash")
                    != scenario_authority["source_provenance_hash"]
                    or manifest.get("retained_set_root")
                    != scenario_authority["retained_set_root"]
                    or manifest.get("retained_position")
                    != scenario_authority["retained_position"]):
                errors.add(BUILD_MANIFEST_SCHEMA_INVALID)
    except BuildCohortPacketError as exc:
        errors.add(str(exc))
    except (KeyError, TypeError, ValueError, AttributeError, IndexError):
        errors.add(BUILD_MANIFEST_SCHEMA_INVALID)
    return _closed(errors)


# =============================================================================
# W10 — the structural half of the falsification sentinel
# =============================================================================

def bc_om_difference(manifest: dict[str, Any]) -> dict[str, Any]:
    """The BC/OM difference at BOTH levels: the READ-SET SELECTION and the SERVED packet.

    HONEST LIMIT (byte reason): the frozen `_object_closure` (:257-273) pads BOTH
    served packets with every catalog obligation AND its transitive prerequisites,
    so the target's prerequisite is in the served BC packet no matter what BC
    selected.  The necessity claim of W10 is therefore made over the READ-SET
    SELECTION; the served difference is reported separately and is non-degenerate
    through the DEPENDENCY rows and the unselected OBSERVATION rows.
    """
    bc_selected = set(manifest["bc_selected_object_ids"])
    om_selected = set(manifest["gold_read_set"])
    bc_served = set(packets._object_closure(manifest, manifest["bc_selected_object_ids"]))
    om_served = set(packets._object_closure(manifest, manifest["gold_read_set"]))
    return {"bc_only_selected": sorted(bc_selected - om_selected),
            "om_only_selected": sorted(om_selected - bc_selected),
            "bc_only_served": sorted(bc_served - om_served),
            "om_only_served": sorted(om_served - bc_served)}


def om_only_necessity_witness(manifest: dict[str, Any]) -> dict[str, Any]:
    """Registered counterfactual over the OM-only READ-SET evidence (§4 W10).

    Coverage class `TARGET_PREREQUISITE_LIFECYCLE`: the gold target's prerequisite
    is in the gold read set and NOT in the BC selection.  The registered
    counterfactual flips exactly that prerequisite's lifecycle COMPLETED -> OPEN.
    Necessity holds when the canonical gold derivation CHANGES while every
    BC-SELECTED object is byte-identical in both worlds.
    """
    gold = manifest["gold_action_id"]
    action = next(row for row in manifest["action_catalog"]
                  if row.get("action_id") == gold)
    target = action["obligation_id"]
    world_map = {row["object_id"]: row for row in manifest["canonical_world"]}
    prerequisites = [pid for pid in world_map[target]["fields"]["prerequisite_obligation_ids"]
                     if pid in manifest["gold_read_set"]
                     and pid not in manifest["bc_selected_object_ids"]]
    if not prerequisites:
        return {"coverage_class": OM_ONLY_NECESSITY_COVERAGE_CLASS,
                "in_class": False, "necessary": False,
                "errors": [BUILD_OM_ONLY_EVIDENCE_NOT_NECESSARY]}
    mutated = copy.deepcopy(manifest)
    for row in mutated["canonical_world"]:
        if row["object_id"] == prerequisites[0]:
            row["fields"]["lifecycle"] = "OPEN"
    counterfactual_gold = packets._unique_gold_action(mutated)
    bc_before = [world_map[name] for name in manifest["bc_selected_object_ids"]]
    mutated_map = {row["object_id"]: row for row in mutated["canonical_world"]}
    bc_after = [mutated_map[name] for name in manifest["bc_selected_object_ids"]]
    necessary = counterfactual_gold != gold and bc_before == bc_after
    return {"coverage_class": OM_ONLY_NECESSITY_COVERAGE_CLASS,
            "in_class": True,
            "registered_counterfactual": OM_ONLY_REGISTERED_COUNTERFACTUAL,
            "mutated_object_id": prerequisites[0],
            "gold": gold, "counterfactual_gold": counterfactual_gold,
            "bc_selected_evidence_unchanged": bc_before == bc_after,
            "necessary": necessary,
            "errors": [] if necessary else [BUILD_OM_ONLY_EVIDENCE_NOT_NECESSARY]}


def gold_read_set_census(manifests: list[dict[str, Any]], *,
                         declared_minimum: int = DECLARED_MIN_DISTINCT_GOLD_READ_SETS
                         ) -> dict[str, Any]:
    """W10's structural half over a population of served manifests."""
    read_sets = sorted({sha384(manifest["gold_read_set"]) for manifest in manifests})
    sizes = sorted({len(manifest["gold_read_set"]) for manifest in manifests})
    differences = [bc_om_difference(manifest) for manifest in manifests]
    degenerate = [manifest["scenario_id"] for manifest, difference
                  in zip(manifests, differences)
                  if not difference["bc_only_selected"] or not difference["om_only_selected"]
                  or not difference["bc_only_served"] or not difference["om_only_served"]]
    necessity = [om_only_necessity_witness(manifest) for manifest in manifests]
    in_class = [row for row in necessity if row["in_class"]]
    not_necessary = [row for row in necessity if row["in_class"] and not row["necessary"]]
    errors: set[str] = set()
    if len(read_sets) < declared_minimum:
        errors.add(BUILD_GOLD_READ_SET_VARIETY_BELOW_FLOOR)
    if degenerate:
        errors.add(BUILD_BC_OM_DIFFERENCE_DEGENERATE)
    if not in_class or not_necessary:
        errors.add(BUILD_OM_ONLY_EVIDENCE_NOT_NECESSARY)
    return {"population": len(manifests),
            "distinct_gold_read_sets": len(read_sets),
            "declared_minimum_distinct_gold_read_sets": declared_minimum,
            "distinct_gold_read_set_sizes": sizes,
            "degenerate_bc_om_scenarios": degenerate,
            "om_only_necessity_coverage_class": OM_ONLY_NECESSITY_COVERAGE_CLASS,
            "om_only_necessity_in_class": len(in_class),
            "om_only_necessity_failures": [row.get("mutated_object_id")
                                           for row in not_necessary],
            "errors": _closed(errors)}


# =============================================================================
# (d)/(e) scoring — supplied state, and the exact-subtractive wrapper
# =============================================================================

def build_scoring_fixture_for_candidate(
        candidate: dict[str, Any], condition: str, *,
        context: authority.BuildRetainedAuthorityContext | None = None,
        cut_id: str | None = None,
        manifest: dict[str, Any] | None = None,
        authoritative_state: dict[str, Any] | None = None,
        scenario_authority: dict[str, Any] | None = None) -> dict[str, Any]:
    """Frozen `build_scoring_fixture` with `authoritative_state` ALWAYS SUPPLIED (W18),
    behind the BUILD SEMANTIC VALIDATION of what is about to be served.

    The frozen default path is never reached: `_fixture_authoritative_state`
    (:352-376) rebuilds from `initial_state()`'s two literal obligations and
    enforces exact obligation-set equality, so it refuses every BUILD population by
    construction.  The supplied state is the replayed generation state and its
    `project_state_world` equality against the manifest is witnessed HERE, before
    the frozen builder is called.

    THE SERVING BOUNDARY (cohort-BUILD r1 FOLD 1(c)).  `validate_build_manifest` used
    to be reachable and unreached: r1's R5/R6 both built and served evidence the
    validator refuses.  It now runs HERE, and the check that runs is DECLARED, in two
    honest halves:

      * SERVED path (`context` or `scenario_authority` present) — the FULL
        `validate_build_manifest`, including the frozen validator, the FACT-ancestry
        re-derivation, the observation derivation binding and the population bindings.
      * ADMISSION path (both None) — the observation DERIVATION + PROJECTION bindings
        only, beside the state/cut witnesses this path already had.  §2.5's envelope
        admission runs BEFORE selection and DELIBERATELY renders shapes the gold
        predicate refuses (the planned-ineligible strata), so running the population
        bindings here would refuse the population the plan is built on — this split is
        a semantic requirement first and a cost saving second (admission renders all
        960 candidates).

    HONEST LIMIT of that split: admission is NOT a ghost-FACT gate.  The FACT-ancestry
    re-derivation runs on the SERVED path only, which is the boundary evidence crosses
    to reach the model; at admission the candidate was built from the replayed state
    moments earlier by the generator itself.
    """
    if cut_id is None:
        cut_id = candidate.get("chosen_cut_id") or candidate["cut_ids"][0]
    if manifest is None:
        manifest = build_manifest_for_candidate(
            candidate, cut_id, context=context, scenario_authority=scenario_authority)
    state = (authoritative_state if authoritative_state is not None
             else authoritative_state_for_cut(candidate, cut_id))
    if packets.project_state_world(state, manifest) != manifest["canonical_world"]:
        raise BuildCohortPacketError(BUILD_AUTHORITATIVE_STATE_MISMATCH)
    if state_reference.current_cut(state) != manifest["cut"]:
        raise BuildCohortPacketError(BUILD_AUTHORITATIVE_STATE_MISMATCH)
    if context is not None or scenario_authority is not None:
        refusals = validate_build_manifest(manifest, candidate, cut_id, context=context,
                                           authoritative_state=state)
    else:
        refusals = sorted(observation_derivation_errors(candidate, cut_id, state))
    if refusals:
        raise BuildCohortPacketError(",".join(refusals))
    cohort_authority = scenario_authority
    if cohort_authority is None and context is not None:
        cohort_authority = authority.retained_scenario_authority(context, candidate)
    if cohort_authority is None:
        cohort_authority = copy.deepcopy(BUILD_POPULATION_AUTHORITY_SENTINEL)
    return packets.build_scoring_fixture(
        manifest, condition, authoritative_state=state,
        cohort_authority=cohort_authority)


def render_all_six_nodes(candidate: dict[str, Any], *,
                         context: authority.BuildRetainedAuthorityContext | None = None,
                         cut_id: str | None = None,
                         manifest: dict[str, Any] | None = None,
                         scenario_authority: dict[str, Any] | None = None
                         ) -> dict[str, Any]:
    """§2.5 envelope admission: `render_served_input` must SUCCEED for ALL SIX nodes.

    The frozen renderer (:302-306) pads every FITTING packet to exactly 65,536 bytes
    and raises only on `len(encoded) > ENVELOPE_BYTES`, so the legal EXACT FIT is
    admitted and "served < 65,536" is unsatisfiable.  Admission delegates to it; the
    unpadded canonical lengths are reported so the exact-fit and A1-growth edges are
    visible in the record.

    Every node goes through `build_scoring_fixture_for_candidate`, so this INHERITS
    that function's serving-boundary validation (FOLD 1(c)): a BUILD refusal arrives
    as a named code in `errors` with its detail in `refusal_detail`, never as an
    escaping traceback and never as an admission.
    """
    if cut_id is None:
        cut_id = candidate.get("chosen_cut_id") or candidate["cut_ids"][0]
    if manifest is None:
        manifest = build_manifest_for_candidate(
            candidate, cut_id, context=context, scenario_authority=scenario_authority)
    lengths: dict[str, int] = {}
    served_hashes: dict[str, str] = {}
    errors: list[str] = []
    detail = ""
    try:
        state = authoritative_state_for_cut(candidate, cut_id)
        for condition in CONDITIONS:
            fixture = build_scoring_fixture_for_candidate(
                candidate, condition, context=context, cut_id=cut_id, manifest=manifest,
                authoritative_state=state, scenario_authority=scenario_authority)
            for node, packet in (("A0", fixture["a0_packet"]),
                                 ("B", fixture["task_packet"]),
                                 ("A1", fixture["a1_packet"])):
                encoded = canonical_json(packet)
                served = packets.render_served_input(packet)
                if len(served) != ENVELOPE_BYTES:
                    raise BuildCohortPacketError(BUILD_ENVELOPE_EXCEEDED)
                lengths["%s.%s" % (condition, node)] = len(encoded)
                served_hashes["%s.%s" % (condition, node)] = packets.served_input_hash(served)
    except (ValueError, KeyError, TypeError) as exc:
        detail = "%s: %s" % (type(exc).__name__, exc)
        errors.append(BUILD_ENVELOPE_EXCEEDED if "PACKET_ENVELOPE_EXCEEDED" in str(exc)
                      else BUILD_SCORER_INPUT_INVALID)
    return {"schema_id": "BuildEnvelopeAdmissionV1",
            "refusal_detail": detail,
            "scenario_id": candidate["scenario_id"], "cut_id": cut_id,
            "nodes": ["%s.%s" % (condition, node)
                      for condition in CONDITIONS for node in EPISODE_NODES],
            "unpadded_lengths": lengths, "served_input_hashes": served_hashes,
            "envelope_bytes": ENVELOPE_BYTES,
            "world_object_count": len(candidate["canonical_world_by_cut"][cut_id]),
            "declared_world_object_ceiling": DECLARED_WORLD_OBJECT_CEILING,
            "admitted": not errors and len(lengths) == 6,
            "errors": sorted(set(errors))}


#: The neutral placeholder that occupies the frozen `cohort_authority` slot in the
#: CONTROL run of the exact-subtractive wrapper.  It carries no authority at all —
#: that is the point: the BUILD authority must be provably INERT to the frozen
#: validator, so it cannot be the thing that silences a frozen check.
BUILD_POPULATION_AUTHORITY_SENTINEL: dict[str, Any] = {
    "schema_id": "BuildPopulationAuthoritySentinelV1",
    "reason": "FROZEN_COHORT_AUTHORITY_IS_SCOPED_TO_THE_FROZEN_POPULATION",
}

#: The ONLY frozen error codes this wrapper may decline to re-add, and only when
#: the BUILD authority evidence is clean AND the BUILD authority object is inert.
#:
#: `I01` is `manifest == expected_manifest AND validate_cohort_manifest_join(...)`
#: (`mbcx01_r13_packets.py:900-902`).  Its manifest-equality half is NOT lost by the
#: subtraction: `validate_scorer_input:1021` independently adds
#: `EXPECTED_MANIFEST_MISMATCH`, which is OUTSIDE this closure and therefore always
#: returned.  What is subtracted is exactly the frozen population join, which
#: resolves through `measurement._pinned_retained_source()` (:120-124) and can never
#: admit a BUILD scenario id.
POPULATION_AUTHORITY_CASCADE_CLOSURE = frozenset({"I01_INVARIANT_INVALID"})


def validate_build_population_join(context: authority.BuildRetainedAuthorityContext,
                                   candidate: dict[str, Any],
                                   expected_manifest: dict[str, Any],
                                   cohort_authority: Any) -> list[str]:
    """The INDEPENDENT BUILD evidence the subtraction is conditioned on.

    This is the BUILD twin of the frozen `validate_cohort_manifest_join` (:131-155):
    the manifest must match the BUILD scenario authority's candidate record at the
    chosen cut, field for field, and the authority must itself re-derive.
    """
    errors: set[str] = set()
    try:
        if authority.validate_retained_scenario_authority(context, cohort_authority):
            return [BUILD_SCORER_INPUT_INVALID]
        record = cohort_authority["candidate_record"]
        chosen = record["chosen_cut_id"]
        cut = {key: value for key, value in record["cut_by_id"][chosen].items()
               if key != "cut_id"}
        if (record != candidate
                or expected_manifest["scenario_id"] != record["scenario_id"]
                or expected_manifest["motif"] != record["motif"]
                or expected_manifest["cut"] != cut
                or expected_manifest["scope_id"] != record["scope_id"]
                or expected_manifest["canonical_world"]
                != record["canonical_world_by_cut"][chosen]
                or expected_manifest["action_catalog"] != record["action_catalog"]
                or expected_manifest["observation"] != observation_manifest_representation(
                    record["observation_authority_by_cut"][chosen])
                or packets.legal_action_ids_from_world(
                    expected_manifest["canonical_world"],
                    expected_manifest["action_catalog"], expected_manifest["cut"])
                != record["action_ids_by_cut"][chosen]
                or expected_manifest["gold_action_id"]
                != record["gold_action_id_by_cut"][chosen]
                or expected_manifest["source_candidate_hash"]
                != cohort_authority["candidate_hash"]
                or expected_manifest["source_provenance_hash"]
                != cohort_authority["source_provenance_hash"]
                or expected_manifest["retained_set_root"]
                != cohort_authority["retained_set_root"]
                or expected_manifest["retained_position"]
                != cohort_authority["retained_position"]):
            errors.add(BUILD_SCORER_INPUT_INVALID)
    except (KeyError, TypeError, ValueError, AttributeError):
        errors.add(BUILD_SCORER_INPUT_INVALID)
    return sorted(errors)


def verify_build_scorer_input(expected_manifest: dict[str, Any], scorer_input: Any, *,
                              context: authority.BuildRetainedAuthorityContext,
                              candidate: dict[str, Any],
                              require_production_authority: bool = False) -> list[str]:
    """EXACT-SUBTRACTIVE production admission for one BUILD scorer input.

    Pattern of record: `mbcx01_build_state_authority.verify_production_scorer_input`
    (:1009-1044).  The FROZEN `mbcx01_r13_packets.validate_scorer_input` runs twice,
    unmodified, and its verdict is never edited.  The only permitted act is to
    decline to re-add `POPULATION_AUTHORITY_CASCADE_CLOSURE`, and only when all
    three hold:

      * the BUILD authority object is INERT to the frozen validator — the run with
        the real BUILD authority and the run with the neutral sentinel produce the
        IDENTICAL frozen error set, so a forged authority cannot silence a frozen
        check to buy itself the subtraction;
      * the observed frozen error set is a subset of the declared closure;
      * the INDEPENDENT BUILD population evidence (`validate_build_population_join`)
        is clean.

    Anything else returns the frozen verdict unedited, unioned with the BUILD errors.
    """
    def frozen_verdict(value: Any) -> set[str]:
        """Run the FROZEN validator unmodified, and stay TOTAL.

        The frozen validator is not total against every ill-matched pair — e.g.
        an expected manifest whose gold read set names an object absent from the
        supplied packet world raises `KeyError` at `mbcx01_r13_packets.py:293`.
        A gate that crashes is not a gate, so an unexpected traceback becomes the
        named refusal `BUILD_SCORER_INPUT_INVALID` instead of escaping.
        """
        try:
            return set(packets.validate_scorer_input(
                expected_manifest, value,
                require_production_authority=require_production_authority))
        except (AttributeError, IndexError, KeyError, StopIteration, TypeError,
                UnicodeError, ValueError):
            return {BUILD_SCORER_INPUT_INVALID}

    supplied = frozen_verdict(scorer_input)
    control_input = copy.deepcopy(scorer_input)
    if isinstance(control_input, dict) and "cohort_authority" in control_input:
        control_input["cohort_authority"] = copy.deepcopy(BUILD_POPULATION_AUTHORITY_SENTINEL)
    control = frozen_verdict(control_input)
    build_errors = set(validate_build_population_join(
        context, candidate, expected_manifest,
        scorer_input.get("cohort_authority") if isinstance(scorer_input, dict) else None))
    if supplied != control:
        return sorted(supplied | build_errors | {BUILD_POPULATION_AUTHORITY_INERTNESS_FAILED})
    if build_errors or not supplied <= POPULATION_AUTHORITY_CASCADE_CLOSURE:
        return sorted(supplied | build_errors)
    return sorted(supplied - POPULATION_AUTHORITY_CASCADE_CLOSURE)


def build_score_exact(expected_manifest: dict[str, Any], scorer_input: Any, *,
                      context: authority.BuildRetainedAuthorityContext,
                      candidate: dict[str, Any],
                      require_production_authority: bool = False) -> int:
    try:
        return int(not verify_build_scorer_input(
            expected_manifest, scorer_input, context=context, candidate=candidate,
            require_production_authority=require_production_authority))
    except (AttributeError, KeyError, TypeError, ValueError, UnicodeError):
        return 0


# =============================================================================
# (e) the scenario-outcome seam
# =============================================================================

BUILD_OUTCOME_RECEIPT_SCHEMA_ID = "BuildScenarioOutcomeReceiptV1"
BUILD_OUTCOME_RECEIPT_KEYS = frozenset({
    "schema_id", "scenario_id", "manifest_hash", "retained_set_root",
    "episode_hash", "call_bindings", "call_binding_set_hash",
    "bc_scorer_input", "bc_scorer_input_hash", "om_scorer_input",
    "om_scorer_input_hash", "authority_mode", "bc", "om", "receipt_hash"})


def build_scenario_outcome_receipt(manifest: dict[str, Any],
                                   bc_scorer_input: dict[str, Any],
                                   om_scorer_input: dict[str, Any],
                                   episode_receipt: dict[str, Any], *,
                                   context: authority.BuildRetainedAuthorityContext,
                                   candidate: dict[str, Any],
                                   require_production_authority: bool = False
                                   ) -> dict[str, Any]:
    """BUILD twin of the frozen `build_scenario_outcome_receipt` (:1285-1325).

    The frozen builder raises `SCENARIO_OUTCOME_AUTHORITY_INVALID` for every BUILD
    candidate at :1294 (`validate_cohort_manifest_join` against the frozen pinned
    population).  This twin runs the frozen `_outcome_episode_call_bindings`
    (:1241-1282) UNMODIFIED — it reads only the episode receipt and the call records
    and is population-agnostic — and takes its two scores from the exact-subtractive
    wrapper.
    """
    for condition, value in (("BC", bc_scorer_input), ("OM", om_scorer_input)):
        if (not isinstance(value, dict) or value.get("condition") != condition
                or value.get("manifest") != manifest
                or validate_build_population_join(
                    context, candidate, manifest, value.get("cohort_authority"))
                or packets.validate_manifest_cut_state_receipt(
                    value.get("manifest_cut_state_receipt"), manifest,
                    require_production=require_production_authority)
                or state_reference.verify_state_authority_receipt(
                    value.get("state_authority_receipt"),
                    require_production=require_production_authority)
                or state_oracle.verify_state_authority_receipt(
                    value.get("state_authority_receipt"),
                    require_production=require_production_authority)):
            raise BuildCohortPacketError(BUILD_SCENARIO_OUTCOME_AUTHORITY_INVALID)
    call_bindings = packets._outcome_episode_call_bindings(
        episode_receipt, bc_scorer_input, om_scorer_input)
    receipt = {
        "schema_id": BUILD_OUTCOME_RECEIPT_SCHEMA_ID,
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
        "bc": build_score_exact(manifest, bc_scorer_input, context=context,
                                candidate=candidate,
                                require_production_authority=require_production_authority),
        "om": build_score_exact(manifest, om_scorer_input, context=context,
                                candidate=candidate,
                                require_production_authority=require_production_authority),
    }
    receipt["receipt_hash"] = packets.hash_without(receipt, "receipt_hash")
    return receipt


def validate_build_scenario_outcome_receipt(
        receipt: Any, episode_receipt: dict[str, Any], *,
        context: authority.BuildRetainedAuthorityContext,
        candidate: dict[str, Any],
        require_production_authority: bool = False) -> list[str]:
    """BUILD twin of the frozen `validate_scenario_outcome_receipt` (:1328-1379)."""
    try:
        if (not isinstance(receipt, dict)
                or set(receipt) != set(BUILD_OUTCOME_RECEIPT_KEYS)
                or receipt["schema_id"] != BUILD_OUTCOME_RECEIPT_SCHEMA_ID
                or receipt["authority_mode"] != ("PRODUCTION" if require_production_authority
                                                 else "FIXTURE_CONFORMANCE")
                or type(receipt["bc"]) is not int or receipt["bc"] not in (0, 1)
                or type(receipt["om"]) is not int or receipt["om"] not in (0, 1)
                or receipt["receipt_hash"] != packets.hash_without(receipt, "receipt_hash")
                or receipt["episode_hash"] != episode_receipt.get("episode_hash")
                or not isinstance(receipt["call_bindings"], list)
                or len(receipt["call_bindings"]) != 6
                or receipt["call_binding_set_hash"] != sha384(receipt["call_bindings"])
                or receipt["bc_scorer_input_hash"] != sha384(receipt["bc_scorer_input"])
                or receipt["om_scorer_input_hash"] != sha384(receipt["om_scorer_input"])):
            raise BuildCohortPacketError(BUILD_SCENARIO_OUTCOME_AUTHORITY_INVALID)
        bc_input, om_input = receipt["bc_scorer_input"], receipt["om_scorer_input"]
        manifest = bc_input["manifest"]
        if (om_input["manifest"] != manifest
                or receipt["scenario_id"] != manifest["scenario_id"]
                or receipt["manifest_hash"] != manifest["manifest_hash"]
                or receipt["retained_set_root"] != manifest["retained_set_root"]
                or bc_input["condition"] != "BC" or om_input["condition"] != "OM"):
            raise BuildCohortPacketError(BUILD_SCENARIO_OUTCOME_AUTHORITY_INVALID)
        for value in (bc_input, om_input):
            if (validate_build_population_join(
                    context, candidate, manifest, value.get("cohort_authority"))
                    or packets.validate_manifest_cut_state_receipt(
                        value.get("manifest_cut_state_receipt"), manifest,
                        require_production=require_production_authority)
                    or state_reference.verify_state_authority_receipt(
                        value.get("state_authority_receipt"),
                        require_production=require_production_authority)
                    or state_oracle.verify_state_authority_receipt(
                        value.get("state_authority_receipt"),
                        require_production=require_production_authority)):
                raise BuildCohortPacketError(BUILD_SCENARIO_OUTCOME_AUTHORITY_INVALID)
        if receipt["call_bindings"] != packets._outcome_episode_call_bindings(
                episode_receipt, bc_input, om_input):
            raise BuildCohortPacketError(BUILD_SCENARIO_OUTCOME_AUTHORITY_INVALID)
        derived = (build_score_exact(manifest, bc_input, context=context,
                                     candidate=candidate,
                                     require_production_authority=require_production_authority),
                   build_score_exact(manifest, om_input, context=context,
                                     candidate=candidate,
                                     require_production_authority=require_production_authority))
        if (receipt["bc"], receipt["om"]) != derived:
            raise BuildCohortPacketError(BUILD_SCENARIO_OUTCOME_AUTHORITY_INVALID)
        return []
    except (AttributeError, KeyError, TypeError, ValueError, UnicodeError):
        return [BUILD_SCENARIO_OUTCOME_AUTHORITY_INVALID]


def build_complete_episode_receipt(bc_scorer_input: dict[str, Any],
                                   om_scorer_input: dict[str, Any],
                                   manifest_position: int) -> dict[str, Any]:
    """The frozen six-ledger episode builder (:1222-1238), unchanged — it is
    population-agnostic and reads only the six call records."""
    return packets.build_complete_episode_receipt_for_scorers(
        bc_scorer_input, om_scorer_input, manifest_position)


# =============================================================================
# (f) THE BUILD INFERENCE INGRESS
# =============================================================================

def build_membership_scenario_ids(context: authority.BuildRetainedAuthorityContext
                                  ) -> list[str]:
    """The ordered membership, DERIVED from the BUILD pinned retained authority."""
    return authority.retained_membership_scenario_ids(context)


def ordered_decision_from_build_episode_receipts(
        outcome_receipts: list[dict[str, Any]],
        episode_receipts: list[dict[str, Any]], *,
        context: authority.BuildRetainedAuthorityContext,
        candidates_by_scenario_id: dict[str, dict[str, Any]] | None = None,
        manifest_scenario_ids: Any = None,
        design_ok: bool = True,
        require_production_authority: bool = False) -> str:
    """The BUILD inference ingress (§2 module 3(f), W19).

    Membership is DERIVED from the BUILD pinned retained authority.  A caller MAY
    pass `manifest_scenario_ids`, but only as an ASSERTION: a same-length
    substitution or a reordering is refused `BUILD_MEMBERSHIP_SUBSTITUTED` before
    any numerical work, which is the gate-r1 768-phantom-ID discriminator.

    The frozen `derive_episode_partition` and the frozen numerical core
    `ordered_decision_with_missingness` run UNMODIFIED.  Only receipt ADMISSION is
    BUILD-specific: estimand, missingness hull, n=768 and every formula stay frozen.
    """
    membership = build_membership_scenario_ids(context)
    substitution = authority.refuse_substituted_membership(context, manifest_scenario_ids)
    if substitution:
        raise BuildCohortPacketError(authority.BUILD_MEMBERSHIP_SUBSTITUTED)
    partition = inference.derive_episode_partition(episode_receipts, membership)
    expected_complete = partition["complete_ids"]
    if not isinstance(outcome_receipts, list):
        raise BuildCohortPacketError(BUILD_EPISODE_PARTITION_MISMATCH)
    episode_by_scenario = {receipt["scenario_id"]: receipt for receipt in episode_receipts}
    index = {row["scenario_id"]: row for row in context.retained_candidates}
    if candidates_by_scenario_id:
        index.update(candidates_by_scenario_id)
    rows = []
    for receipt in outcome_receipts:
        if (not isinstance(receipt, dict)
                or receipt.get("schema_id") != BUILD_OUTCOME_RECEIPT_SCHEMA_ID):
            raise BuildCohortPacketError(BUILD_SCENARIO_OUTCOME_AUTHORITY_INVALID)
        scenario_id = receipt.get("scenario_id")
        episode_receipt = episode_by_scenario.get(scenario_id)
        if episode_receipt is None or scenario_id not in expected_complete:
            raise BuildCohortPacketError(BUILD_EPISODE_PARTITION_MISMATCH)
        candidate = index.get(scenario_id)
        if candidate is None:
            raise BuildCohortPacketError(BUILD_EPISODE_PARTITION_MISMATCH)
        if validate_build_scenario_outcome_receipt(
                receipt, episode_receipt, context=context, candidate=candidate,
                require_production_authority=require_production_authority):
            raise BuildCohortPacketError(BUILD_SCENARIO_OUTCOME_AUTHORITY_INVALID)
        rows.append({"scenario_id": scenario_id, "bc": receipt["bc"], "om": receipt["om"]})
    if [row["scenario_id"] for row in rows] != expected_complete:
        raise BuildCohortPacketError(BUILD_EPISODE_PARTITION_MISMATCH)
    return inference.ordered_decision_with_missingness(
        rows, partition["missing_ids"], membership, design_ok=design_ok)


#: The eligibility callable handed to `select_build_cohort`; named so the
#: generator's wiring reads as one pointer instead of a lambda.
ELIGIBILITY_PREDICATE: Callable[[dict[str, Any], str], bool] = candidate_is_eligible
