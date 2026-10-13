"""Assembly: repair-ledger rows for the cohort-BUILD r1 folds (driver-owned edit).

Adds bc15-bc21 to the two-way ledger: three new rows, three appended rows, totals
recomputed from the ledger itself (never hand-arithmetic).
"""
import json

PATH = "MBCX-01-BUILD-REPAIR-LEDGER.json"
W = "test_mbcx01_build_cohort.BuildCohortSliceClosingWitnesses."
SRC = ("MBCX-01-COHORTBUILD-ROUND-r1-SYNTHESIS.md (cohort-BUILD acceptance council r1, "
       "2026-08-16; packet @8432132, folds on @af1cc4f)")

led = json.load(open(PATH, encoding="utf-8"))
inv = led["invariants"]

# --- appended rows -----------------------------------------------------------
row = inv["BC-19_REGISTRATION_TOTALITY_AT_FOUR_LEVELS"]
bc17 = W + "test_bc17_adversarial_a_stray_pin_only_subject_fails_by_name"
assert bc17 not in row["adversarial"]
row["adversarial"].append(bc17)
row["requirement"] += (" Level (b)'s difference set (pinned beyond REQUIRED) is DECLARED,"
                       " not free: every such subject is named in"
                       " PIN_MANIFEST_SUBJECTS_BEYOND_REQUIRED and a stray pin-only"
                       " subject is refused by name as"
                       " W14_PIN_MANIFEST_SUBJECT_OUTSIDE_DECLARED_SET"
                       " (cohort-BUILD r1 adjudication 2).")

row = inv["BC-03_SEQUENCED_TOTAL_ADMISSION_ARITHMETIC"]
bc20 = W + "test_bc20_red_a_placement_shortfall_refuses_the_plan"
row["adversarial"].append(bc20)
row["requirement"] += (" The placement loop is TOTAL against its own record:"
                       " len(placements) != placed_total REFUSES the plan"
                       " (BUILD_GENERATION_PLAN_REFUSED naming requested vs achieved),"
                       " so the signed plan cannot overstate the achieved stratified"
                       " placement (cohort-BUILD r1 fold 3).")

row = inv["BC-11_SEQUENCE_COVERAGE_AGAINST_A_REGISTERED_DENOMINATOR"]
bc21 = W + "test_bc21_red_the_coverage_numerator_counts_legal_noop_events"
row["positive"].append(bc21)
row["requirement"] += (" The NUMERATOR rule is declared beside the number"
                       " (covered_pair_rule = ORDERED_PAIRS_OVER_ALL_GATE_CHECKED_"
                       "PROGRAM_EVENTS): a DUPLICATE_NOOP is a legal executed program"
                       " event, so pairs are counted over ALL gate-checked events, and"
                       " a record missing either set rule is refused"
                       " BUILD_SEQUENCE_COVERAGE_UNREPORTED (cohort-BUILD r1 fold 4).")

# --- new rows ----------------------------------------------------------------
inv["BC-20_THE_SERVING_BOUNDARY_RE_DERIVES_WHAT_IT_SERVES"] = {
    "adversarial": [
        W + "test_bc15_adversarial_ghost_fact_cannot_reach_the_serving_boundary",
        W + "test_bc16_adversarial_a_non_derived_observation_record_cannot_serve",
    ],
    "modules": ["mbcx01_build_cohort_packet.py"],
    "note": ("The positive half is the honest serving path succeeding end-to-end,"
             " declared once in BC-08's scorer-join witness, so no witness is counted"
             " twice. The observation derivation law lives in the packet sibling as of"
             " this fold (moved from the generator; the generator re-exports it)."),
    "positive": [],
    "positive_covered_by": "BC-08_SCORER_JOIN_END_TO_END_ON_THE_BUILD_PATH",
    "requirement": ("Model-visible evidence must survive independent re-derivation at"
                    " the serving boundary: build_scoring_fixture_for_candidate runs the"
                    " full BUILD manifest validation (FACT journal ancestry, observation"
                    " representation consistency, derivation binding - the observation"
                    " record must equal derive_observation_authority recomputed from its"
                    " own stored projection, and the projection must equal a recompute"
                    " from the replayed state and variation) before the frozen builder is"
                    " called. A candidate does not become model-visible merely because"
                    " its candidate/provenance/authority bytes are mutually"
                    " self-consistent (council r1 seat 2, F1/F2, driver-reproduced R5/R6)."),
    "source": SRC,
}

inv["BC-21_THE_RETAINED_ANSWER_KEY_IS_NOT_A_CONSTANT"] = {
    "adversarial": [
        W + "test_bc18_red_the_retained_population_carries_distinct_gold_answers",
    ],
    "modules": ["mbcx01_build_cohort_generator.py"],
    "note": ("The single witness carries both halves: the positive (768 distinct gold"
             " action ids, one per retained row, reported in the census with its"
             " declared floor rule) and the adversarial (a forced constant-gold retained"
             " set is refused RETAINED_GOLD_VARIETY_BELOW_FLOOR)."),
    "positive": [],
    "requirement": ("The scored target's obligation identity is PER-SCENARIO"
                    " (TARGET_OBLIGATION_PREFIX + scenario_id, distinct by construction),"
                    " so the retained population's answer key is not a constant and a"
                    " positional heuristic cannot score at ceiling in both arms; the"
                    " census reports the distinct-gold count against the declared floor"
                    " ONE_DISTINCT_GOLD_ACTION_ID_PER_RETAINED_ROW and refuses below it"
                    " (council r1 seat 1 finding A, driver-reproduced R1)."),
    "source": SRC,
}

inv["BC-22_OBSERVATION_SIGNATURE_CROSSTAB_MEASURED"] = {
    "accepted_residual": ("DECLARED_SINGLE_MOTIF_SIGNATURE_RESIDUAL = 3: three retained"
                          " observation signatures identify exactly one motif (15 rows"
                          " at generation; design section 2.2 carries the number and the"
                          " discarded reshaping attempt). MEASURED and pinned, not gated:"
                          " eliminating it requires equalizing per-motif count support,"
                          " which is machinery the no-adversary rule forbids; the"
                          " exploitation path requires cross-scenario population"
                          " statistics a frozen cold-episode subject does not have."),
    "adversarial": [],
    "adversarial_covered_by": "BC-16_OBSERVATION_NON_LEAKAGE_FOUR_CLASS_CHECKLIST",
    "modules": ["mbcx01_build_cohort_generator.py"],
    "note": ("The adversarial leakage half (literal, derivable-encoding, relabeling,"
             " codebook classes) is declared once in BC-16; this row owns the"
             " POPULATION-LEVEL cross-tab measurement those per-candidate checks"
             " structurally cannot see (council r1 seat 3 F1, driver-reproduced R2)."),
    "positive": [
        W + "test_bc19_red_the_census_reports_the_signature_motif_crosstab",
    ],
    "requirement": ("The census cross-tabulates every retained chosen-cut observation"
                    " signature (family, code, cardinality, order) against motif and"
                    " REPORTS the single-motif signature count and affected-row count,"
                    " pinned to the declared residual constant so the number cannot"
                    " drift silently."),
    "source": SRC,
}

# --- totals recomputed from the ledger itself --------------------------------
witnesses = set()
for row in inv.values():
    witnesses.update(row.get("positive") or [])
    witnesses.update(row.get("adversarial") or [])
led["totals"] = {"invariants": len(inv), "witnesses": len(witnesses)}
print("totals:", led["totals"])

with open(PATH, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(led, fh, indent=1, sort_keys=True)
    fh.write("\n")
print("written")
