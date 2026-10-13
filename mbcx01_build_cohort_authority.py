"""BUILD cohort selection / provenance / retained-authority sibling (issue #17).

Design of record: `MBCX-01-BUILD-COHORT-CONTENT-DESIGN.md` r6 FINAL at commit
18d86d44d3a2cf28108022e626ea4bda1b430d86, §2 module 2 and §3.

WHAT THIS MODULE SUPERSEDES (frozen lines cited, never edited)
--------------------------------------------------------------
* `mbcx01_r13_measurement.synthetic_candidates_r13` (:243-274) — the frozen
  generator stamps ONE world across all 960 candidates and writes a DECLARED
  eligibility Boolean into `canonical_state_by_cut` (:252).  The BUILD sibling
  takes its population from `mbcx01_build_cohort_generator`, and eligibility is
  DERIVED through the packet layer's gold predicate (a callable supplied by the
  caller, so this module never imports the packet layer — see IMPORT DIRECTION).
* `mbcx01_r13_measurement.validate_source_provenance` (:277-301) — the BUILD
  sibling binds two additional sub-digests the frozen shape has no room for:
  `event_program_hash` (the replayed 17-alphabet journal) and
  `observation_authority_hash` (the §2.2 ObservationAuthorityV1 record).  A
  journal-only mutation therefore fails the BUILD provenance gate (W12).
* `mbcx01_r13_measurement.select_cohort` (:304-334) — the ARITHMETIC is adopted
  UNCHANGED BY IMPORT: `choose_one_cut` (:184-188), `framed_hash` (:176-181),
  the retention-hash sort key (:326-327), 128-per-motif (:330), and the final
  SHA-256 scenario ordering (:333-334).  What changes is the population and the
  eligibility source: `row["eligible"]` is never read back (:321); a supplied
  eligibility key is POPPED and refused by name as `DECLARED_ELIGIBILITY_BOOLEAN`.
* `mbcx01_r13_measurement.retained_cohort_authority_r13` (:348-367),
  `retained_scenario_authority` (:370-395) and
  `validate_retained_scenario_authority` (:398-412) — the frozen trio resolves
  through three MODULE-GLOBAL caches (:47-49, :337-345).  The BUILD siblings are
  INSTANCE-SCOPED: every entry point takes a `BuildRetainedAuthorityContext`,
  and no module-global holds a population.

ADVERSARY / REFUSAL POSTURE
---------------------------
This lane is a scientific measurement harness with NO threat model.  Every
refusal below stops a WRONG NUMBER — a fake population (`DECLARED_ELIGIBILITY_
BOOLEAN`, `SOURCE_PROVENANCE_MISMATCH`), a laundered predicate (a candidate that
never met the derived gold predicate reaching the retained set), a phantom
membership (`BUILD_MEMBERSHIP_SUBSTITUTED`) — never a person.

IMPORT DIRECTION (no cycles): this module imports FROZEN modules only.
`mbcx01_build_cohort_packet` imports this module; `mbcx01_build_cohort_generator`
imports both.

DECLARED BUILD-TIME CONSTANTS (§6 Item 7(a): the suite pins them; the driver
reviews them): the COMMITTED ARTIFACT `MBCX-01-BUILD-COHORT-GENERATOR-V1.json`
(2026-08-16, registration task — it supersedes the in-code dict this module
carried at the engine build) — candidate/retained counts, the new hash domain
strings, the per-motif planned-ineligible quota `k`, the generation-plan refusal
threshold (32 = 160 - 128, the floor margin), and the committed identity block
(design §3).  `load_build_cohort_spec()` reads and checks it; `BUILD_COHORT_SPEC`
is a snapshot for module-level constant reads only.  The §2.6 coverage constants
(`SEQUENCE_COVERAGE_STRENGTH`, `SEQUENCE_TARGET_SET_RULE`, `SEQUENCE_COVERED_PAIR_RULE`,
`SEQUENCE_COVERAGE_FLOOR`, `EVENT_ALPHABET`) and the `sequence_coverage` measurement
itself moved HERE from the generator by cohort-BUILD r2 FOLD A, so the validator can
RECOMPUTE the record it admits; the generator re-exports them.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable, Iterable

import mbcx01_r13_common as common
import mbcx01_r13_measurement as measurement

ROOT = Path(__file__).resolve().parent

# --- arithmetic adopted UNCHANGED, by import (design §2 module 2) -------------
framed_hash = measurement.framed_hash          # mbcx01_r13_measurement.py:176-181
choose_one_cut = measurement.choose_one_cut     # mbcx01_r13_measurement.py:184-188
sha384 = measurement.sha384
sha256 = measurement.sha256
canonical_json = measurement.canonical_json
MOTIFS = measurement.MOTIFS                     # frozen taxonomy, :20-21 (§5 coupling)

BUILD_GENERATOR_ID = "GENERATOR.BUILD.COHORT.V1"
BUILD_SOURCE_PROVENANCE_SCHEMA_ID = "BuildSourceProvenanceManifestV1"
BUILD_RETAINED_COHORT_SCHEMA_ID = "BuildRetainedCohortAuthorityV1"
BUILD_RETAINED_SCENARIO_SCHEMA_ID = "BuildRetainedScenarioAuthorityV1"

#: NEW domain strings (§2.1 "domains declared in the generator spec").  They are
#: distinct from the frozen r13 domains by construction — the frozen domains are
#: read out of `MBCX-01-MEASUREMENT-CONTRACT-v7.json` (`_selection_domains`,
#: :163-165) and are never reused here, so a BUILD retention rank can never
#: collide with an r13 one.
BUILD_DOMAIN_PREFIX = "MBCX01.BUILD.COHORT.V1"
BUILD_ONE_CUT_DOMAIN = BUILD_DOMAIN_PREFIX + ".ONE-CUT"
BUILD_RETENTION_DOMAIN = BUILD_DOMAIN_PREFIX + ".RETENTION"
BUILD_VARIATION_DOMAINS = {
    "obligation_count": BUILD_DOMAIN_PREFIX + ".OBLIGATION-COUNT",
    "prerequisite_shape": BUILD_DOMAIN_PREFIX + ".PREREQUISITE-SHAPE",
    "decoy_mix": BUILD_DOMAIN_PREFIX + ".DECOY-MIX",
    "catalog_size": BUILD_DOMAIN_PREFIX + ".CATALOG-SIZE",
    "fact_chain_depth": BUILD_DOMAIN_PREFIX + ".FACT-CHAIN-DEPTH",
    "observation_family": BUILD_DOMAIN_PREFIX + ".OBSERVATION-FAMILY",
    "event_order": BUILD_DOMAIN_PREFIX + ".EVENT-ORDER",
    "omission_configuration": BUILD_DOMAIN_PREFIX + ".OMISSION-CONFIGURATION",
    "cut_offer": BUILD_DOMAIN_PREFIX + ".CUT-OFFER",
    "joint_stratum": BUILD_DOMAIN_PREFIX + ".JOINT-STRATUM",
    "planned_ineligible": BUILD_DOMAIN_PREFIX + ".PLANNED-INELIGIBLE",
}

#: The BUILD generator spec is the COMMITTED ARTIFACT design §3 names —
#: `MBCX-01-BUILD-COHORT-GENERATOR-V1.json` — read by `load_build_cohort_spec()`
#: below exactly the way the frozen `mbcx01_r13_measurement._generator_spec`
#: (:168-173) reads `MBCX-01-R13-SYNTHETIC-COHORT-GENERATOR.json`.
#:
#: 2026-08-16, registration task: this REPLACES the in-code dict the engine build
#: carried as a recorded residual ("emitting the JSON artifact is a registration-task
#: residual, recorded, not papered over").  The artifact is now the ONE source of the
#: declared BUILD-time constants — candidate/retained counts, the new hash domains,
#: the per-motif planned-ineligible quota k, the plan-refusal margin — and the
#: committed identity block (design §3, "own `retained_set_root` in a committed
#: identity block") rides it.  `BUILD_COHORT_SPEC` is a SNAPSHOT taken at import so
#: the generator's module-level constants keep one name to read; it is never a second
#: authority, because `build_generator_spec()` re-reads the file on EVERY call.
BUILD_COHORT_SPEC_ARTIFACT = "MBCX-01-BUILD-COHORT-GENERATOR-V1.json"
BUILD_COHORT_SPEC_SCHEMA_ID = "BuildCohortGeneratorSpecV1"
BUILD_COHORT_IDENTITY_SCHEMA_ID = "BuildCohortCommittedIdentityV1"

#: The six FROZEN cohort error codes (`validate_source_provenance`, :279-301).
FROZEN_COHORT_ERROR_CODES = frozenset({
    "SOURCE_GENERATOR_INVALID",
    "SOURCE_PROVENANCE_INVALID",
    "SOURCE_PROVENANCE_MISMATCH",
    "DUPLICATE_SCENARIO_ID",
    "UNKNOWN_MOTIF",
    "WRONG_MOTIF_TOTAL",
})

#: W2 (§2.3): the name a supplied eligibility Boolean is refused BY.
DECLARED_ELIGIBILITY_BOOLEAN = "DECLARED_ELIGIBILITY_BOOLEAN"
#: Every key that would let a caller DECLARE eligibility instead of earning it.
#: `eligibility_source` is included because the frozen row writes the literal
#: string `"RECOMPUTED"` next to a Boolean it never recomputed (:317).
DECLARED_ELIGIBILITY_KEYS = ("declared_eligible", "eligibility_source", "eligible",
                             "is_eligible", "retained", "retention_hash")

BUILD_MEMBERSHIP_SUBSTITUTED = "BUILD_MEMBERSHIP_SUBSTITUTED"
BUILD_RETAINED_SCENARIO_AUTHORITY_INVALID = "BUILD_RETAINED_SCENARIO_AUTHORITY_INVALID"
BUILD_RETAINED_COHORT_AUTHORITY_INVALID = "BUILD_RETAINED_COHORT_AUTHORITY_INVALID"
BUILD_ELIGIBLE_MOTIF_SHORTFALL = "BUILD_ELIGIBLE_MOTIF_SHORTFALL"
BUILD_SELECTED_TOTAL_INVALID = "BUILD_SELECTED_TOTAL_INVALID"
BUILD_GENERATION_PLAN_REFUSED = "BUILD_GENERATION_PLAN_REFUSED"
BUILD_CANDIDATE_SCHEMA_INVALID = "BUILD_CANDIDATE_SCHEMA_INVALID"
BUILD_EVENT_PROGRAM_INVALID = "BUILD_EVENT_PROGRAM_INVALID"
BUILD_OBSERVATION_AUTHORITY_INVALID = "BUILD_OBSERVATION_AUTHORITY_INVALID"
BUILD_SEQUENCE_COVERAGE_UNREPORTED = "BUILD_SEQUENCE_COVERAGE_UNREPORTED"
#: cohort-BUILD r2 FOLD A: the coverage record ADMITTED into provenance is not the
#: record the candidate programs produce.  `BUILD_SEQUENCE_COVERAGE_UNREPORTED` is a
#: PRESENCE verdict; this is the VALUE verdict, and it is what stops a self-consistent
#: forged number from binding into the retained authority's provenance.
BUILD_SEQUENCE_COVERAGE_MISMATCH = "BUILD_SEQUENCE_COVERAGE_MISMATCH"
#: The GENERATION-side coverage refusal, declared here with the measurement it names
#: (moved from the generator by FOLD A; the generator re-exports it).
BUILD_SEQUENCE_COVERAGE_BELOW_FLOOR = "BUILD_SEQUENCE_COVERAGE_BELOW_FLOOR"
#: RAISE-ONLY, declared HERE by the cohort-BUILD r2 rider (council r2 seat 1): the
#: §2.2 derivation raises this name in `mbcx01_build_cohort_packet` and the generator
#: re-raises it as a GENERATION refusal, but the string sat outside every declared
#: vocabulary, so nothing could resolve it.  Membership below changes no behaviour —
#: no entry point RETURNS it — it only makes the name resolvable where the vocabulary
#: is declared.
BUILD_OBSERVATION_PROJECTION_LEAK = "BUILD_OBSERVATION_PROJECTION_LEAK"

#: CLOSED error vocabulary: the six frozen cohort codes plus the BUILD codes.
#: An unlisted string returned by any entry point below is itself a defect
#: (`mbcx01_build_measurement_authority._closed`, :219-224, is the house pattern).
BUILD_COHORT_ERROR_CODES = frozenset(FROZEN_COHORT_ERROR_CODES | {
    DECLARED_ELIGIBILITY_BOOLEAN,
    BUILD_MEMBERSHIP_SUBSTITUTED,
    BUILD_RETAINED_SCENARIO_AUTHORITY_INVALID,
    BUILD_RETAINED_COHORT_AUTHORITY_INVALID,
    BUILD_ELIGIBLE_MOTIF_SHORTFALL,
    BUILD_SELECTED_TOTAL_INVALID,
    BUILD_GENERATION_PLAN_REFUSED,
    BUILD_CANDIDATE_SCHEMA_INVALID,
    BUILD_EVENT_PROGRAM_INVALID,
    BUILD_OBSERVATION_AUTHORITY_INVALID,
    BUILD_SEQUENCE_COVERAGE_UNREPORTED,
    BUILD_SEQUENCE_COVERAGE_MISMATCH,
    BUILD_OBSERVATION_PROJECTION_LEAK,
})
# NOT a member, and deliberately: `BUILD_SEQUENCE_COVERAGE_BELOW_FLOOR` is a
# GENERATION-plan refusal carried inside the coverage record's own `errors` list and
# raised by `generate_cohort`; no entry point here returns it, and adding it would
# change what `_closed` keeps.  Its declaration moved with the measurement (FOLD A);
# its membership question is untouched.

#: The keys a BUILD candidate row carries.  Closed on purpose: a new key is a
#: new authority surface and must be declared here (and therefore hashed).
BUILD_CANDIDATE_KEYS = frozenset({
    "scenario_id", "motif", "scope_id", "cut_ids", "cut_by_id",
    "action_catalog", "action_ids_by_cut", "gold_action_id_by_cut",
    "canonical_state_by_cut", "canonical_world_by_cut", "observation_by_cut",
    "observation_authority_by_cut", "bc_selected_object_ids_by_cut",
    "authoritative_state_hash_by_cut", "event_program", "event_result_codes",
    "variation", "generation",
})


class BuildCohortAuthorityError(ValueError):
    """Typed, closed failure of the BUILD cohort authority."""


def canonical_artifact_bytes(document: Any) -> bytes:
    """The ONE accepted on-disk serialization of a BUILD spec artifact: canonical + LF."""
    return canonical_json(document) + b"\n"


def load_build_cohort_spec() -> dict[str, Any]:
    """Read, CHECK and return the committed BUILD generator spec artifact.

    Frozen twin: `mbcx01_r13_measurement._generator_spec` (:168-173) — same shape of
    check (`schema_id` + `generator_id`), same `sha384(parsed)` digest.  Two things
    are added, both because this artifact is written by this lane rather than
    inherited:

    * the CANONICAL-SERIALIZATION check — the file's bytes must be exactly
      `canonical_json(document) + LF`, so the committed artifact cannot drift from the
      canonical form whose digest rides provenance (a re-ordered or re-spaced file
      would hash the same PARSED document while being a different artifact);
    * CRLF normalisation before that comparison.  This repository is checked out with
      `core.autocrlf=true` (verify-build-bundle.py's module docstring records the same
      fact for the pin manifest), so a fresh checkout carries CRLF while the committed
      blob is LF.  Comparing raw bytes would fail on a legitimate checkout and would
      say nothing about content, so the digest of record stays `sha384(parsed)`.

    A refusal here stops a WRONG NUMBER — a population generated against constants
    nobody committed — never a person.
    """
    try:
        raw = (ROOT / BUILD_COHORT_SPEC_ARTIFACT).read_bytes()
        document = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        raise BuildCohortAuthorityError("SOURCE_GENERATOR_INVALID") from exc
    identity = document.get("committed_identity") if isinstance(document, dict) else None
    if (not isinstance(document, dict)
            or document.get("schema_id") != BUILD_COHORT_SPEC_SCHEMA_ID
            or document.get("generator_id") != BUILD_GENERATOR_ID
            or not isinstance(identity, dict)
            or identity.get("schema_id") != BUILD_COHORT_IDENTITY_SCHEMA_ID
            or raw.replace(b"\r\n", b"\n") != canonical_artifact_bytes(document)):
        raise BuildCohortAuthorityError("SOURCE_GENERATOR_INVALID")
    return document


#: A SNAPSHOT of the artifact, taken once at import, for the generator's module-level
#: constants.  Never an authority: every authority path goes through
#: `build_generator_spec()`, which re-reads the artifact.
BUILD_COHORT_SPEC: dict[str, Any] = load_build_cohort_spec()


def _closed(errors: Iterable[str]) -> list[str]:
    """Return the sorted closed error list; an unlisted code is itself a defect."""
    values = set(errors)
    known = {code for code in values if code in BUILD_COHORT_ERROR_CODES}
    if known != values:
        known.add(BUILD_CANDIDATE_SCHEMA_INVALID)
    return sorted(known)


def valid_scenario_id(value: Any) -> bool:
    """A scenario id is a SEMANTIC ID STRING (`mbcx01_r13_common.SEMANTIC_ID`, :67).

    The population's own ids are `scenario_id_template`-formatted
    (`SCENARIO.BUILD.{motif_index}.{index:03d}`), which is exactly that grammar, and the
    selector already treats an id as a string it can `.encode("utf-8")` and rank by
    (:618-619, :626).

    Checked BEFORE any set is built. An otherwise exact candidate row whose
    `scenario_id` was a dict passed the closed key-set test and then reached
    `set(ids)` in the duplicate check, where `TypeError: unhashable type: 'dict'`
    escaped `validate_build_source_provenance` before its CLOSED LIST could be
    returned (codex r5 P2). Same family as the `_custody_errors` key-list fold on the
    state plane and the ETW roster-row fold on the measurement plane: the posture is
    unchanged — such a population never validated — and the refusal is now named.
    """
    return isinstance(value, str) and common.SEMANTIC_ID.fullmatch(value) is not None


def hash_index(domain: str, parts: list[str], modulus: int) -> int:
    """Seedless, framed, per-candidate variation index (§2.1 `framed_hash` domains)."""
    if modulus <= 0:
        raise BuildCohortAuthorityError(BUILD_CANDIDATE_SCHEMA_INVALID)
    return int.from_bytes(framed_hash([domain] + list(parts)), "big") % modulus


def hash_rank_key(domain: str, parts: list[str]) -> bytes:
    """A total, deterministic ranking key over a framed hash (no seed, no clock)."""
    return framed_hash([domain] + list(parts))


def build_generator_spec() -> tuple[dict[str, Any], str]:
    """The BUILD spec of record and its canonical digest (frozen `_generator_spec` twin).

    The COMMITTED ARTIFACT is re-read on every call, so a drifted or hand-edited spec
    is caught here rather than shadowed by a constant cached at import.
    """
    spec = load_build_cohort_spec()
    return spec, sha384(spec)


def committed_identity() -> dict[str, Any]:
    """The committed identity block of the BUILD cohort (design §3).

    It carries ONLY candidate-derived values — `retained_set_root`, `retained_total`
    and the ordered-membership digest — never `generator_digest` or
    `provenance_hash`.  That is what keeps it non-circular: those two are digests OF
    the artifact this block lives in, while the retained root is a digest of the
    generated candidates, which no spec digest feeds.
    """
    return copy.deepcopy(load_build_cohort_spec()["committed_identity"])


def recomputed_identity(context: "BuildRetainedAuthorityContext") -> dict[str, Any]:
    """Recompute the identity block from a live generation, for W8's comparison."""
    ids = retained_membership_scenario_ids(context)
    return {"schema_id": BUILD_COHORT_IDENTITY_SCHEMA_ID,
            "retained_total": context._authority["retained_total"],
            "retained_set_root": context._authority["retained_set_root"],
            "retained_scenario_ids_hash": sha384(ids)}


def validate_committed_identity(context: "BuildRetainedAuthorityContext") -> list[str]:
    """W8: the COMMITTED identity must equal the RECOMPUTED one, field for field.

    A drifted record — a root, a total or a membership digest the live population does
    not reproduce — is refused by name.
    """
    try:
        if committed_identity() != recomputed_identity(context):
            return [BUILD_RETAINED_COHORT_AUTHORITY_INVALID]
        return []
    except (KeyError, TypeError, ValueError, AttributeError):
        return [BUILD_RETAINED_COHORT_AUTHORITY_INVALID]


# --- §2.6 sequence coverage ---------------------------------------------------
# MOVED HERE from `mbcx01_build_cohort_generator` by cohort-BUILD r2 FOLD A, on the
# r1 FOLD-1 precedent: the law lives where the CHECKER can run it.  While the
# measurement lived in the generator, `validate_build_source_provenance` could only
# check that a coverage record was PRESENT and said `meets_declared_floor`, so a
# self-consistent false record bound into the retained authority's provenance.  The
# generator re-exports every name below (the same objects), so the measurement is
# still computed once, in generation order, and gated there.

#: The frozen 17-event alphabet, sorted (`mbcx01_r13_common.EVENT_OPERATIONS`).
EVENT_ALPHABET = tuple(sorted(common.EVENT_OPERATIONS))

SEQUENCE_COVERAGE_STRENGTH = 2
#: The registered denominator: the ORDERED PAIR SQUARE over the 17-event alphabet,
#: 289 pairs, identity = SHA-384 over the sorted pair list.
#:
#: HONEST LIMIT (design §2.6 asks for the LTS-CONSTRAINED reducer-legal target
#: set): the LTS-constrained reduction is NOT computed here.  The unconstrained
#: square is a SUPERSET of the reducer-legal set, so the ratio reported below is a
#: LOWER BOUND on LTS-constrained coverage and can never overstate it.  Carried as
#: a named residual, not papered over.
SEQUENCE_TARGET_SET_RULE = "UNCONSTRAINED_ORDERED_PAIR_SQUARE_OVER_17_EVENT_ALPHABET"
#: The NUMERATOR rule, declared BESIDE the number (r1 FOLD 4).  The record declared its
#: denominator and not its numerator, and the numerator counted pairs over APPLIED
#: events only — but a `DUPLICATE_NOOP` is a LEGAL executed program event under
#: §2.6's sequence semantics (it is the only construction that reaches that code, and
#: every program event passed the §2.7 replay gate against its EXPECTED code), so the
#: applied-only count was false by one pair in the conservative direction.
SEQUENCE_COVERED_PAIR_RULE = "ORDERED_PAIRS_OVER_ALL_GATE_CHECKED_PROGRAM_EVENTS"
#: BUILD-time declared floor, gating (§6 Item 7(b): gate-or-report is a build call;
#: this build GATES).  A 2-way figure must never read as "covered": the strength
#: and floor ride beside the number in provenance (§2.6, Kuhn/NIST lineage).
SEQUENCE_COVERAGE_FLOOR = 0.40


def sequence_coverage(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    """t=2 SEQUENCE coverage over the 17-event alphabet (§2.6), with t and floor
    reported BESIDE the number: a 2-way figure must never read as "covered"."""
    target_pairs = sorted((first, second) for first in EVENT_ALPHABET
                          for second in EVENT_ALPHABET)
    covered: set[tuple[str, str]] = set()
    for candidate in candidates:
        # FOLD 4: ALL program events, not the APPLIED subset.  Every event in the
        # program was replayed through both frozen reducers and matched its EXPECTED
        # result code at generation (§2.7), so a `DUPLICATE_NOOP` is an executed
        # program event and its ordered pairs are covered pairs.
        executed = [event["event_type"] for event in candidate["event_program"]]
        for position, first in enumerate(executed):
            for second in executed[position + 1:]:
                covered.add((first, second))
    present = sorted({event["event_type"] for candidate in candidates
                      for event in candidate["event_program"]})
    ratio = len(covered) / len(target_pairs)
    return {"schema_id": "BuildSequenceCoverageV1",
            "strength": SEQUENCE_COVERAGE_STRENGTH,
            "alphabet_size": len(EVENT_ALPHABET),
            "alphabet_present": present,
            "alphabet_presence_complete": present == list(EVENT_ALPHABET),
            "target_set_rule": SEQUENCE_TARGET_SET_RULE,
            "target_pair_count": len(target_pairs),
            "target_set_identity": sha384([("%s>%s" % pair) for pair in target_pairs]),
            "covered_pair_rule": SEQUENCE_COVERED_PAIR_RULE,
            "covered_pair_count": len(covered),
            "coverage_ratio": ratio,
            "declared_floor": SEQUENCE_COVERAGE_FLOOR,
            "meets_declared_floor": ratio >= SEQUENCE_COVERAGE_FLOOR,
            "errors": ([] if ratio >= SEQUENCE_COVERAGE_FLOOR
                       else [BUILD_SEQUENCE_COVERAGE_BELOW_FLOOR])}


# --- provenance sub-digests ---------------------------------------------------

def event_program_hash(candidate: dict[str, Any]) -> str:
    """SHA-384 over the candidate's replayed 17-alphabet journal AND its result codes.

    W12: the journal is bound into provenance here and nowhere else, so a
    journal-only mutation — one that leaves every projected artefact byte-identical
    — still fails `validate_build_source_provenance`.
    """
    return sha384({"schema_id": "BuildEventProgramDigestV1",
                   "event_program": candidate["event_program"],
                   "event_result_codes": candidate["event_result_codes"],
                   "authoritative_state_hash_by_cut":
                       candidate["authoritative_state_hash_by_cut"]})


def observation_authority_hash(candidate: dict[str, Any]) -> str:
    """SHA-384 over the §2.2 ObservationAuthorityV1 records, one per offered cut."""
    return sha384({"schema_id": "BuildObservationAuthorityDigestV1",
                   "observation_authority_by_cut":
                       candidate["observation_authority_by_cut"]})


def build_source_authority(row: dict[str, Any]) -> dict[str, Any]:
    """BUILD twin of the frozen `_source_authority` (:191-200), plus two sub-digests."""
    return {"scenario_id": row["scenario_id"], "motif": row["motif"],
            "cut_ids": copy.deepcopy(row["cut_ids"]),
            "cut_set_hash": sha384(row["cut_ids"]),
            "action_universe_hash": sha384(row["action_ids_by_cut"]),
            "action_catalog_hash": sha384(row["action_catalog"]),
            "gold_authority_hash": sha384(row["gold_action_id_by_cut"]),
            "canonical_state_hash": sha384(row["canonical_state_by_cut"]),
            "canonical_world_hash": sha384(row["canonical_world_by_cut"]),
            "observation_hash": sha384(row["observation_by_cut"]),
            "cut_authority_hash": sha384(row["cut_by_id"]),
            "bc_selection_hash": sha384(row["bc_selected_object_ids_by_cut"]),
            "variation_hash": sha384(row["variation"]),
            "event_program_hash": event_program_hash(row),
            "observation_authority_hash": observation_authority_hash(row)}


def build_source_provenance(candidates: list[dict[str, Any]],
                            sequence_coverage: Any = None) -> dict[str, Any]:
    """The BUILD provenance manifest.

    §2.6 requires the sequence-coverage number to be REPORTED IN PROVENANCE with
    its strength t and its floor BESIDE it (a 2-way figure must never read as
    "covered").  `MANIFEST_KEYS` is a closed frozen set, so it rides HERE, inside
    the provenance hash.  The record is still INJECTED by the caller (the generator
    computes and GATES it in generation order), but as of cohort-BUILD r2 FOLD A the
    measurement itself is `sequence_coverage` ABOVE, so what is injected here is
    re-derivable — and `validate_build_source_provenance` re-derives it.  This
    function does no checking: it hashes what it is handed, which is exactly why the
    admission check had to move to the validator.
    """
    spec, digest = build_generator_spec()
    provenance = {"schema_id": BUILD_SOURCE_PROVENANCE_SCHEMA_ID,
                  "generator_id": spec["generator_id"], "generator_digest": digest,
                  "sequence_coverage": copy.deepcopy(sequence_coverage),
                  "scenario_authority": [build_source_authority(row) for row in candidates]}
    provenance["provenance_hash"] = sha384(provenance)
    return provenance


def sequence_coverage_report_errors(provenance: Any) -> list[str]:
    """The coverage record must carry its NUMBER, its STRENGTH, its FLOOR and BOTH
    of its set rules.

    `covered_pair_rule` is REQUIRED here as of the cohort-BUILD r1 FOLD 4: the record
    declared its DENOMINATOR rule (`target_set_rule`) and left the NUMERATOR rule
    unwritten, and an unwritten numerator rule is how an applied-only count read as
    "the covered pairs" for a whole round.
    """
    record = provenance.get("sequence_coverage") if isinstance(provenance, dict) else None
    required = {"strength", "coverage_ratio", "declared_floor", "target_pair_count",
                "target_set_identity", "covered_pair_count", "meets_declared_floor",
                "target_set_rule", "covered_pair_rule"}
    if (not isinstance(record, dict) or not required <= set(record)
            or record.get("meets_declared_floor") is not True):
        return [BUILD_SEQUENCE_COVERAGE_UNREPORTED]
    return []


# --- declared-eligibility refusal (W2) ---------------------------------------

def pop_declared_eligibility(candidates: list[dict[str, Any]]
                             ) -> tuple[list[dict[str, Any]], list[str]]:
    """POP every declared-eligibility key BY NAME; never read one back.

    Returns the popped rows and the refusal list.  The frozen selector reads
    `state.get("eligible") is True` (:321) and stamps `"RECOMPUTED"` beside it
    (:317); this refuses the whole shape instead.
    """
    popped: list[dict[str, Any]] = []
    refusals: set[str] = set()
    for source in candidates:
        row = copy.deepcopy(source)
        if not isinstance(row, dict):
            refusals.add(BUILD_CANDIDATE_SCHEMA_INVALID)
            continue
        for key in DECLARED_ELIGIBILITY_KEYS:
            if key in row:
                row.pop(key)
                refusals.add(DECLARED_ELIGIBILITY_BOOLEAN)
        for name in ("canonical_state_by_cut",):
            by_cut = row.get(name)
            if name in row and not isinstance(by_cut, dict):
                # A CUT MAP THAT IS NOT A MAP IS A SCHEMA REFUSAL, NOT A CRASH
                # (codex-CLI r6 SEAT1 F4). `(row.get(name) or {}).values()` read
                # `.values()` off whatever the caller supplied, so a scalar
                # `canonical_state_by_cut` raised a raw `AttributeError` out of a
                # validator that promises a closed error list — and the FALSY
                # non-dict spellings (`[]`, `0`, `""`) never crashed but were
                # only ever caught downstream as an opaque
                # SOURCE_PROVENANCE_MISMATCH. Both are named here.
                refusals.add(BUILD_CANDIDATE_SCHEMA_INVALID)
                continue
            for cut_state in (by_cut or {}).values():
                if not isinstance(cut_state, dict):
                    continue
                for key in DECLARED_ELIGIBILITY_KEYS:
                    if key in cut_state:
                        cut_state.pop(key)
                        refusals.add(DECLARED_ELIGIBILITY_BOOLEAN)
        popped.append(row)
    return popped, sorted(refusals)


#: The exception classes a MALFORMED CALLER INPUT produces when it reaches code that
#: expected a well-formed one. Same enumeration as this lane's shelf pattern
#: (`mbcx01_build_cohort_packet.verify_build_scorer_input`'s `frozen_verdict`,
#: :1010-1025 — "a gate that crashes is not a gate") and as
#: `mbcx01_build_state_authority.MALFORMED_CALLER_INPUT_EXCEPTIONS`.
#:
#: ⚠ IT IS DELIBERATELY NOT `Exception`. An `AssertionError`, a `MemoryError` or any
#: class outside this tuple is THIS MODULE'S OWN DEFECT, and a validator that answered
#: "your population is malformed" when it means "I am broken" would be reporting a
#: wrong number about itself. Those still fault loud, and so does this module's own
#: `BuildCohortAuthorityError` (a `ValueError` subclass), which is re-raised.
MALFORMED_CALLER_INPUT_EXCEPTIONS = (AttributeError, IndexError, KeyError,
                                     StopIteration, TypeError, UnicodeError,
                                     ValueError)


def validate_build_source_provenance(candidates: list[dict[str, Any]],
                                     provenance: dict[str, Any]) -> list[str]:
    """BUILD twin of the frozen `validate_source_provenance` (:277-301).

    THE CLOSED LIST IS TOTAL AT THIS BOUNDARY (codex-CLI r6 SEAT1 F4 — the third
    round in which a malformed caller JSON escaped a documented closed list as a raw
    traceback). bc23 closed the unhashable scenario id at its site and the next
    unanticipated shape simply found the next site (`pop_declared_eligibility`
    reading `.values()` off a scalar `canonical_state_by_cut`). So the class is
    closed as a COMPLEMENT here: every `MALFORMED_CALLER_INPUT_EXCEPTIONS` member
    raised under this call becomes `BUILD_CANDIDATE_SCHEMA_INVALID`, the same code
    this validator already returns for a population whose rows are not candidates.
    The per-site guards STAY — they say WHICH shape was wrong, and this says only
    that one was.
    """
    try:
        return _validate_build_source_provenance(candidates, provenance)
    except BuildCohortAuthorityError:
        raise
    except MALFORMED_CALLER_INPUT_EXCEPTIONS:
        return _closed({BUILD_CANDIDATE_SCHEMA_INVALID})


def _validate_build_source_provenance(candidates: list[dict[str, Any]],
                                      provenance: dict[str, Any]) -> list[str]:
    try:
        spec, digest = build_generator_spec()
    except (OSError, ValueError, TypeError):
        return [ "SOURCE_GENERATOR_INVALID" ]
    if (not isinstance(provenance, dict)
            or provenance.get("schema_id") != BUILD_SOURCE_PROVENANCE_SCHEMA_ID
            or provenance.get("generator_id") != spec["generator_id"]
            or provenance.get("generator_digest") != digest
            or provenance.get("provenance_hash") != sha384(
                {key: value for key, value in provenance.items()
                 if key != "provenance_hash"})):
        return ["SOURCE_PROVENANCE_INVALID"]
    errors: set[str] = set(sequence_coverage_report_errors(provenance))
    rows, eligibility_refusals = pop_declared_eligibility(candidates)
    errors.update(eligibility_refusals)
    for row in rows:
        if (not isinstance(row, dict) or set(row) != set(BUILD_CANDIDATE_KEYS)
                or not valid_scenario_id(row.get("scenario_id"))):
            errors.add(BUILD_CANDIDATE_SCHEMA_INVALID)
    if BUILD_CANDIDATE_SCHEMA_INVALID not in errors:
        try:
            derived = [build_source_authority(row) for row in rows]
        except (KeyError, TypeError, ValueError):
            derived = None
            errors.add(BUILD_CANDIDATE_SCHEMA_INVALID)
        if derived is not None and derived != provenance.get("scenario_authority", []):
            errors.add("SOURCE_PROVENANCE_MISMATCH")
        # cohort-BUILD r2 FOLD A: the coverage record is RECOMPUTED from the popped
        # candidate rows and must BYTE-EQUAL the supplied one.  Without this join the
        # record was bound into provenance (and from there into the retained
        # authority) on nothing but its own field presence, so a forged 289/289 was
        # indistinguishable from the population's true number.  Canonical bytes, not
        # `==`: `289` and `289.0` are the same value and a different record.
        try:
            recomputed = canonical_json(sequence_coverage(rows))
            supplied = canonical_json(provenance.get("sequence_coverage"))
        except (AttributeError, KeyError, TypeError, ValueError):
            errors.add(BUILD_SEQUENCE_COVERAGE_MISMATCH)
        else:
            if supplied != recomputed:
                errors.add(BUILD_SEQUENCE_COVERAGE_MISMATCH)
    ids = [row.get("scenario_id") for row in rows]
    # Uniqueness is a question about IDS: it is asked only once every id is one
    # (`valid_scenario_id` above has already named the population otherwise).
    if all(valid_scenario_id(value) for value in ids) and len(ids) != len(set(ids)):
        errors.add("DUPLICATE_SCENARIO_ID")
    if any(row.get("motif") not in MOTIFS for row in rows):
        errors.add("UNKNOWN_MOTIF")
    expected = spec["candidate_count_per_motif"]
    if any(sum(row.get("motif") == motif for row in rows) != expected for motif in MOTIFS):
        errors.add("WRONG_MOTIF_TOTAL")
    return _closed(errors)


def provenance_sub_digest_diff(left: dict[str, Any],
                               right: dict[str, Any]) -> list[str]:
    """Name the sub-digest fields that differ between two provenance manifests.

    Used by the W12 witness so the red NAMES the binding that caught the journal
    mutation instead of reporting an opaque mismatch.
    """
    names: set[str] = set()
    left_rows = left.get("scenario_authority", []) if isinstance(left, dict) else []
    right_rows = right.get("scenario_authority", []) if isinstance(right, dict) else []
    if len(left_rows) != len(right_rows):
        return ["scenario_authority_length"]
    for lrow, rrow in zip(left_rows, right_rows):
        for key in sorted(set(lrow) | set(rrow)):
            if lrow.get(key) != rrow.get(key):
                names.add(key)
    return sorted(names)


# --- selection ----------------------------------------------------------------

def select_build_cohort(candidates: list[dict[str, Any]], provenance: dict[str, Any],
                        eligibility_predicate: Callable[[dict[str, Any], str], bool],
                        ) -> list[dict[str, Any]]:
    """BUILD twin of the frozen `select_cohort` (:304-334).

    The arithmetic is the frozen arithmetic, imported: `choose_one_cut` for the one
    scored cut, `framed_hash` for the retention rank, the same
    `(retention_hash, scenario_id)` byte sort, the same 128-per-motif cut, the same
    768 total, and the same final SHA-256 scenario ordering.

    What differs, and only this: eligibility is DERIVED by `eligibility_predicate`
    — the packet layer's gold predicate, injected so this module never imports the
    packet layer — and any supplied eligibility key is popped and refused by name.

    THE SAME COMPLEMENT AS `validate_build_source_provenance`, because this is the
    OTHER public door onto the same population (codex-CLI r6 SEAT1 F4). It reaches
    `pop_declared_eligibility` BEFORE the validator runs, so the boundary put on the
    validator alone would leave this door raw: a malformed population is
    `BuildCohortAuthorityError(BUILD_CANDIDATE_SCHEMA_INVALID)` here, which is this
    function's own refusal contract, never a traceback. The honesty constraint is
    the constant's: the enumerated tuple only, and this module's own error re-raised.
    """
    try:
        return _select_build_cohort(candidates, provenance, eligibility_predicate)
    except BuildCohortAuthorityError:
        raise
    except MALFORMED_CALLER_INPUT_EXCEPTIONS:
        # Implicit chaining kept: the operator still sees WHAT the malformed input
        # did, under a refusal that names WHY the run stopped.
        raise BuildCohortAuthorityError(BUILD_CANDIDATE_SCHEMA_INVALID)


def _select_build_cohort(candidates: list[dict[str, Any]], provenance: dict[str, Any],
                         eligibility_predicate: Callable[[dict[str, Any], str], bool],
                         ) -> list[dict[str, Any]]:
    rows, eligibility_refusals = pop_declared_eligibility(candidates)
    errors = set(validate_build_source_provenance(candidates, provenance))
    errors.update(eligibility_refusals)
    if errors:
        raise BuildCohortAuthorityError(",".join(sorted(errors)))
    spec, _digest = build_generator_spec()
    selected: list[dict[str, Any]] = []
    for motif in MOTIFS:
        eligible = []
        for source in (row for row in rows if row["motif"] == motif):
            row = copy.deepcopy(source)
            chosen = choose_one_cut(row["scenario_id"], row["cut_ids"],
                                    spec["one_cut_hash_domain"])
            row["chosen_cut_id"] = chosen
            row["eligibility_source"] = "DERIVED_THROUGH_PACKET_GOLD_PREDICATE"
            row["eligible"] = bool(eligibility_predicate(source, chosen))
            row["retention_hash"] = framed_hash(
                [spec["retention_hash_domain"], motif, row["scenario_id"], chosen]
            ).hex().upper()
            if row["eligible"]:
                eligible.append(row)
        eligible.sort(key=lambda row: (bytes.fromhex(row["retention_hash"]),
                                       row["scenario_id"].encode("utf-8")))
        if len(eligible) < spec["retained_count_per_motif"]:
            raise BuildCohortAuthorityError(BUILD_ELIGIBLE_MOTIF_SHORTFALL)
        selected.extend(eligible[:spec["retained_count_per_motif"]])
    if len(selected) != spec["retained_total"]:
        raise BuildCohortAuthorityError(BUILD_SELECTED_TOTAL_INVALID)
    return sorted(selected,
                  key=lambda row: hashlib.sha256(row["scenario_id"].encode("utf-8")).digest())


# --- instance-scoped retained authority --------------------------------------

class BuildRetainedAuthorityContext:
    """The BUILD pinned retained population, held by an INSTANCE, never a module global.

    The frozen trio resolves through `_RETAINED_SOURCE_CACHE` /
    `_RETAINED_INDEX_CACHE` / `_RETAINED_AUTHORITY_CACHE`
    (`mbcx01_r13_measurement.py:47-49`).  Two populations cannot coexist in one
    process behind those globals; two `BuildRetainedAuthorityContext` objects can.
    """

    __slots__ = ("_retained", "_provenance", "_index", "_authority", "_candidates")

    def __init__(self, candidates: list[dict[str, Any]], provenance: dict[str, Any],
                 eligibility_predicate: Callable[[dict[str, Any], str], bool]) -> None:
        retained = select_build_cohort(candidates, provenance, eligibility_predicate)
        # A REFERENCE, not a copy: the generated population is large and the context
        # exposes it through a copying accessor.
        self._candidates = candidates
        self._retained = retained
        self._provenance = copy.deepcopy(provenance)
        self._index = {row["scenario_id"]: (position, row, sha384(row))
                       for position, row in enumerate(retained)}
        candidate_hashes = [sha384(row) for row in retained]
        authority = {
            "schema_id": BUILD_RETAINED_COHORT_SCHEMA_ID,
            "generator_id": self._provenance["generator_id"],
            "generator_digest": self._provenance["generator_digest"],
            "source_provenance_hash": self._provenance["provenance_hash"],
            "retained_total": len(retained),
            "retained_scenario_ids": [row["scenario_id"] for row in retained],
            "retained_candidate_hashes": candidate_hashes,
            "retained_set_root": sha384(candidate_hashes),
        }
        authority["authority_hash"] = sha384(authority)
        self._authority = authority

    # -- read-only views -------------------------------------------------------

    @property
    def generated_candidates(self) -> list[dict[str, Any]]:
        return copy.deepcopy(self._candidates)

    @property
    def retained_candidates(self) -> list[dict[str, Any]]:
        return copy.deepcopy(self._retained)

    @property
    def provenance(self) -> dict[str, Any]:
        return copy.deepcopy(self._provenance)

    def retained_position(self, scenario_id: str) -> int | None:
        indexed = self._index.get(scenario_id)
        return None if indexed is None else indexed[0]

    def _indexed(self, scenario_id: Any) -> tuple[int, dict[str, Any], str] | None:
        return self._index.get(scenario_id)


def retained_cohort_authority(context: BuildRetainedAuthorityContext) -> dict[str, Any]:
    """BUILD twin of `retained_cohort_authority_r13` (:348-367); instance-scoped."""
    return copy.deepcopy(context._authority)


def retained_set_root(context: BuildRetainedAuthorityContext) -> str:
    """The BUILD population's own retained-set root (design §3, own identity block)."""
    return context._authority["retained_set_root"]


def retained_membership_scenario_ids(context: BuildRetainedAuthorityContext) -> list[str]:
    """The ONE ordered membership list.  The inference ingress DERIVES from this.

    Already in the frozen SHA-256 scenario order (`select_build_cohort` returns it
    sorted that way), which is exactly what the frozen
    `mbcx01_r13_inference.derive_episode_partition` (:144-148) demands.
    """
    return list(context._authority["retained_scenario_ids"])


def retained_scenario_authority(context: BuildRetainedAuthorityContext,
                                candidate: dict[str, Any]) -> dict[str, Any]:
    """Issue authority only for one BYTE-EXACT member of the BUILD retained set."""
    candidate_hash = sha384(candidate)
    indexed = context._indexed(candidate.get("scenario_id")
                               if isinstance(candidate, dict) else None)
    cohort = context._authority
    if (indexed is None or indexed[1] != candidate or indexed[2] != candidate_hash
            or cohort["retained_candidate_hashes"][indexed[0]] != candidate_hash):
        raise BuildCohortAuthorityError(BUILD_RETAINED_SCENARIO_AUTHORITY_INVALID)
    authority = {
        "schema_id": BUILD_RETAINED_SCENARIO_SCHEMA_ID,
        "generator_id": cohort["generator_id"],
        "generator_digest": cohort["generator_digest"],
        "source_provenance_hash": cohort["source_provenance_hash"],
        "retained_set_root": cohort["retained_set_root"],
        "retained_total": cohort["retained_total"],
        "retained_position": indexed[0],
        "candidate_record": copy.deepcopy(candidate),
        "candidate_hash": candidate_hash,
    }
    authority["authority_hash"] = sha384(authority)
    return authority


BUILD_SCENARIO_AUTHORITY_KEYS = frozenset({
    "schema_id", "generator_id", "generator_digest", "source_provenance_hash",
    "retained_set_root", "retained_total", "retained_position",
    "candidate_record", "candidate_hash", "authority_hash"})


def validate_retained_scenario_authority(context: BuildRetainedAuthorityContext,
                                         authority: Any) -> list[str]:
    """BUILD twin of `validate_retained_scenario_authority` (:398-412)."""
    try:
        if (not isinstance(authority, dict)
                or set(authority) != set(BUILD_SCENARIO_AUTHORITY_KEYS)
                or authority.get("schema_id") != BUILD_RETAINED_SCENARIO_SCHEMA_ID
                or authority.get("candidate_hash") != sha384(authority["candidate_record"])
                or authority.get("authority_hash") != sha384(
                    {key: value for key, value in authority.items()
                     if key != "authority_hash"})
                or retained_scenario_authority(
                    context, authority["candidate_record"]) != authority):
            raise BuildCohortAuthorityError(BUILD_RETAINED_SCENARIO_AUTHORITY_INVALID)
        return []
    except (KeyError, TypeError, ValueError, AttributeError):
        return [BUILD_RETAINED_SCENARIO_AUTHORITY_INVALID]


def validate_retained_cohort_authority(context: BuildRetainedAuthorityContext,
                                       authority: Any) -> list[str]:
    """Recompute the cohort authority from the context and demand byte equality."""
    try:
        recomputed = retained_cohort_authority(context)
        if (not isinstance(authority, dict) or authority != recomputed
                or authority["authority_hash"] != sha384(
                    {key: value for key, value in authority.items()
                     if key != "authority_hash"})
                or authority["retained_set_root"] != sha384(
                    authority["retained_candidate_hashes"])
                or authority["retained_total"] != len(authority["retained_scenario_ids"])
                or len(set(authority["retained_scenario_ids"]))
                != authority["retained_total"]):
            raise BuildCohortAuthorityError(BUILD_RETAINED_COHORT_AUTHORITY_INVALID)
        return []
    except (KeyError, TypeError, ValueError, AttributeError, IndexError):
        return [BUILD_RETAINED_COHORT_AUTHORITY_INVALID]


def refuse_substituted_membership(context: BuildRetainedAuthorityContext,
                                  supplied: Any) -> list[str]:
    """Refuse ANY membership list that is not the derived one, byte for byte.

    The gate-r1 discriminator: 768 phantom IDs with valid missing receipts reached
    the frozen numerical core because `mbcx01_r13_inference.py:141-165` validates
    only the SUPPLIED list's internal ordering.  A same-length substitution or a
    reordering is refused here by identity, not by shape.
    """
    derived = retained_membership_scenario_ids(context)
    if supplied is None:
        return []
    if not isinstance(supplied, list) or list(supplied) != derived:
        return [BUILD_MEMBERSHIP_SUBSTITUTED]
    return []
