# SEAT 1 (claude.ai, conversation <id>) — cohort-BUILD acceptance r2 verdict

> Banked VERBATIM by the driver from the seat thread via `browser_wait_quiesced`
> (textLen 19,149, truncated:false), 2026-08-16 ~19:49Z. Leading lines are interface
> turn-labels captured by the extractor; the verdict body begins at "GO".

Verifying the packet bytes before reading.

Used Moonwalker integration · 6 notes

Used Moonwalker integration · 6 notes

Now the omission attack — did any fold weaken a pre-existing witness?

Searched the web, used Moonwalker integration · 1 note

Searched the web, used Moonwalker integration · 1 note

All six items have executed evidence. Delivering the verdict.

GO

No fix class blocking. One build-list rider (closed-vocabulary membership), named below.
Label: EXECUTED.

Seat 1, sealed and independent. Read-only; four probes in %TEMP%, nothing written to the repo. I saw two untracked MBCX-01-COHORTBUILD-SEAT3-CODEX-EXEC-r2.* logs in git status and deliberately did not open them — sealed independence held.

0. Pin confirmation

Packet 210f1faa12d69d594f096b2cb68a7bc2995870cb and content ad713b22f9bad58e3de15df1a05bc78ebdb3728c, both git cat-file -e gated by me, both type commit. Packet blob 4d4c4ddadf5cc073ebe86a9794cc7f7f66318404, 15,802 bytes. I extracted the blob to a temp file and hashed it: 792244B4506D27F193B4DD7E965C1AFC193E6E46189D30E1BC7625F0830B9242 — matches the stated hash and matches the working-tree file byte for byte. git diff --stat ad713b22 HEAD -- '*.py' — EMPTY, re-run by me. Artifact pins at the tree:

Artifact	sha256 (16)	bytes	lines
mbcx01_build_cohort_generator.py	192158FCA95FCB76	75,424	1,420
mbcx01_build_cohort_authority.py	FE88E80C32E5D247	34,159	678
mbcx01_build_cohort_packet.py	65B1CE7DCAA33EAA	69,297	1,253
test_mbcx01_build_cohort.py	D5341C3B82E12B04	172,310	3,024
MBCX-01-BUILD-COHORT-GENERATOR-V1.json	1A206BC757C41B2D	1,592	1
1. Suite execution (EXECUTED, mine)
Run	Result
python -m unittest test_mbcx01_build_cohort	Ran 39 — OK, 111.978 s
python -m unittest discover	Ran 548 — OK, 185.770 s
python verify-build-bundle.py	frozen_suites: PASS · build_suites: PASS · registration_totality: PASS · invariants 101 / witnesses 236 · level_b_required 46 · level_c_governed_artifacts 48 · level_d_modules_covered 15 · top_level_readiness: BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED

Every pre-dispatch number in §14 reproduces on my run. (Discover emitted two ResourceWarnings from test_mbcx01_build_integration.py:696,703 — unclosed open() handles inside an assertion. Cosmetic, no test consequence, not a finding.)

2. Item rulings
1. Serving boundary re-derives what it serves — ACCEPT (EXECUTED)

I ran the packet's own "prove or break": forge the record and its projection consistently, so binding 1 passes by construction.

stored record: STRUCTURE_DEPTH / FACT.DEPTH.1
consistent forgery re-derives to itself: True     ← binding 1 defeated, as designed
observation_derivation_errors            -> ['BUILD_OBSERVATION_REPRESENTATION_DIVERGENT']
validate_build_manifest(forgery)         -> ['BUILD_OBSERVATION_REPRESENTATION_DIVERGENT']
extra projection field                   -> BuildCohortPacketError BUILD_OBSERVATION_PROJECTION_LEAK

The projection recompute is what catches it — exactly the load the fold puts on it. I mutated obligation_row_count by +7 and rebuilt the record around the lie; binding 1 (derive_observation_authority re-derivation) accepted it, binding 2 (projection ⟵ replayed state + variation) refused. The docstring at packet :450-456 states this division honestly and the bytes match the statement.

The interface move (generator→packet) is right, not merely harmless. The derivation law must live where the serving boundary can call it; leaving it in the generator meant the serving path could only check a record against itself, which is precisely how r1's R6 forged gold-bearing observation survived. The generator re-exports (generator:206), so no call site duplicated the law.

The declared admission limit is honest. With no context only the two observation bindings run and a ghost FACT is not gated at admission — the docstring says so, and the limit is safe because admission is a sizing gate whose refusals are conservative, while the ghost-FACT discriminator runs unconditionally on the serving path (r1: I executed that refusal). I did not execute the admission-path ghost-FACT case — read-only on that sub-point.

Rider, build-list not CHANGE: BUILD_OBSERVATION_PROJECTION_LEAK in auth.BUILD_COHORT_ERROR_CODES → False. It is raise-only (packet :248, :440; generator :632) and never flows through _closed, so the closed-vocabulary discipline at authority :148-150 does not cover it. Consequence: wrong-refusal reporting — a refusal issued under a name no consumer of the declared vocabulary can resolve. Not a wrong number; the raise is fail-loud and aborts generation. One-line addition, red-first.

2. The retained answer key is not a constant — ACCEPT (EXECUTED)
distinct golds over 768 : 768
sample target id        : OBL.TGT.SCENARIO.BUILD.1.130 (28 chars) | distinct: 768
SEMANTIC_ID illegal ids : 0   | max len 28  (regex admits 128)
duplicate-gold injection -> census errors: ['RETAINED_GOLD_VARIETY_BELOW_FLOOR']

My r1 finding A is closed at the byte. Three things I checked beyond the count. The floor is the strictest form available — gold_variety_floor = len(retained) (generator :1163), i.e. all-distinct, not a threshold. The count is measured off a recomputed _admission_cut (:1161), not read back off the chosen_cut_id enrichment, so it measures the population rather than what a caller stamped on it. And target_obligation_id is a pure concatenation with no hash (:277), so distinctness is by construction rather than by collision-resistance — the strongest available guarantee and the cheapest to verify. Motif contracts survive: 39/39 and 548/548 green with the parametrized target.

On the driver's BEFORE-YOU-ASK ruling — attacked, and I concede it. My r1 "owner ruling first" was the wrong call. My reasoning was that the design of record did not claim gold variety, so changing it re-entered the design gate. That reasoning fails on inspection: the DoR's silence was an omission, not a decision. Nothing in it asserts or relies on a constant answer key, and the whole anti-fixture doctrine — §2.1's "every eligible candidate ≥1 non-gold action", the entire content arc that existed to un-stamp the population — presupposes the opposite. Folding an omission back toward the doctrine it already states is not a design change. The fold is also not architecture or interface: a module constant became a pure function of an existing field, which is squarely the "localized code fold" the r1 §13 trigger assigns to red-first folding. And the estimand does not reference gold identity — n=768, the missingness hull and the BC/OM contrast are untouched, and the frozen inference core ran unmodified. An owner round would have ratified an executable fact, not made a judgement call. The driver ruled correctly; the owner sees it at merge, which is where it belongs. Being over-cautious about who may decide is its own failure mode, and I was.

3. Motif codebook measured and declared — ACCEPT (EXECUTED)
distinct signatures: 23 | single-motif: 3 | declared: 3 | rows under them: 15
census: single_motif_observation_signature_list =
  ['COUNT_SUMMARY|POPULATION.COUNT.9|1|ASCENDING',
   'COUNT_SUMMARY|POPULATION.COUNT.9|2|ASCENDING',
   'STRUCTURE_DEPTH|FACT.DEPTH.4|2|ASCENDING']

Reproduces the declared number exactly, and the census does not merely count them — it names them, which is what makes the declaration auditable rather than a number to trust. On the packet's three attacks: the no-cross-scenario-exposure argument holds under the serving model I verified in r1 — the subject is a cold six-call episode with no channel to population statistics, so a signature→motif mapping that exists only in the aggregate cannot be read by any single episode; the leak would require the subject to hold the cross-tab, which the serving path cannot give it. Pinning the residual to a constant is the right mechanism because it is brittle: any population change flips bc19 RED and forces a re-declaration, which is a tripwire, not a maintenance defect — the alternative (a threshold) would let the residual drift silently. And the discarded padding option is correctly discarded: it moved the tail (15→8 rows) without changing the signature count (still 3), so it bought presentation, not truth, at the cost of a real variation axis. Measuring and naming beats eliminating-by-flattening.

4. Plan record cannot overstate what it achieved — ACCEPT (EXECUTED)

My r1 fix B landed as written. The guard is at generator :1306 with the reasoning in the comment at :1301-1305. The underlying cap I demonstrated in r1 still exists and I re-confirmed it: _plan_placements(40, [], 40) → 16. At the committed constants placed_total=12 ≤ 16, so the guard is dormant and the record is honest:

plan per_motif: candidates 160, unplanned_refusals 0, planned_ineligible_placed 12,
                planned_ineligible_scenarios {12 entries}, admitted_eligible_lower_bound 148

Twelve stated, twelve named — the scalar and the set now agree by construction rather than by luck. The -1 net is gone: candidates with gold_read_set_size == -1: 0 and BUILD_DERIVED_AXIS_UNRECORDABLE exists as a loud refusal.

On the wrongly-refuses attack: refusing generation when the placer under-places is the correct direction. A plan that cannot place its quota means the stratification the census depends on was not achieved, so signing a number the population never realized would be the worse outcome. The refusal is a refusal of the plan, never of a person (the class name at generator :266 says so).

5. Coverage number says what it counts — ACCEPT (EXECUTED + SEARCHED)

First, my own error. My initial probe passed the coverage record to sequence_coverage_report_errors, which takes the provenance and reads provenance["sequence_coverage"] (authority :356, :365). It returned BUILD_SEQUENCE_COVERAGE_UNREPORTED on the real record and I nearly wrote that up as a defect. Corrected call:

real provenance                -> []
stripped covered_pair_rule     -> ['BUILD_SEQUENCE_COVERAGE_UNREPORTED']
stripped target_set_rule       -> ['BUILD_SEQUENCE_COVERAGE_UNREPORTED']
stripped covered_pair_count    -> ['BUILD_SEQUENCE_COVERAGE_UNREPORTED']
stripped strength              -> ['BUILD_SEQUENCE_COVERAGE_UNREPORTED']
floor not met                  -> ['BUILD_SEQUENCE_COVERAGE_UNREPORTED']
non-dict                       -> ['BUILD_SEQUENCE_COVERAGE_UNREPORTED']
151/289 = 0.5225 (floor 0.4, strength 2)
covered_pair_rule: ORDERED_PAIRS_OVER_ALL_GATE_CHECKED_PROGRAM_EVENTS
target_set_rule  : UNCONSTRAINED_ORDERED_PAIR_SQUARE_OVER_17_EVENT_ALPHABET

Total, discriminating, and it refuses no legitimate record I could construct.

On the DUPLICATE_NOOP semantics — the driver's ruling is right, and the prior art decides it. A t-way sequence covering array is a set of event sequences in which every possible event sequence of length t appears at least once — appears, not "took effect". NIST's empirical basis is explicit that the critical condition for triggering failures was generally whether a particular event had occurred prior to a second one, not necessarily back to back. Occurrence is the criterion. A DUPLICATE_NOOP event was submitted, gate-checked and adjudicated by both reducers — it occurred. The pre-fold applied-only numerator was the non-standard restriction and undercounted; 150→151 moves toward the definition, not away from it. Naming the rule in the record (covered_pair_rule) is what makes the number readable at all — r1's version declared its denominator rule and left the numerator unwritten, which is exactly how an applied-only count read as "the covered pairs" for a whole round.

6. W14(b) difference set declared, witness works in every legitimate layout — ACCEPT (EXECUTED)
declared beyond-REQUIRED subjects : 30
duplicates                        : 0
declared-but-absent on disk       : []
REQUIRED count                    : 46 | overlap decl & REQUIRED: 0
verify-build-bundle.py in REQUIRED: True

All thirty are real files, none duplicated, and the set is genuinely disjoint from REQUIRED — zero overlap, so it is a difference set rather than padding that would let a REQUIRED subject hide inside it.

On the packet's sharpest question — is anything enforcing the "an addition is a DECLARATION" comment beyond review? Yes, and it is structural. PIN_MANIFEST_SUBJECTS_BEYOND_REQUIRED lives in verify-build-bundle.py (:767), and verify-build-bundle.py is itself a REQUIRED pin subject. Growing the allowlist changes that file's hash, which the pin manifest covers, which forces a manifest regeneration — a deliberate, reviewable, gated act. The allowlist cannot grow silently; it can only grow loudly. The bc14 fix is the right shape too: pointing the unpinned-probe at the pin manifest itself means the witness now uses an artifact that exists in every legitimate layout, which is what made it refuse a right reconstruction before.

3. Omission attack — near-empty, which is the convergence signature

Diff of the test module across the whole fold arc, af1cc4f^..ad713b22: 601 lines added, 8 removed. Zero def lines removed. Zero self.assert lines removed. No witness deleted, no assertion weakened, no path made unreachable. The eight removed lines are: the TARGET_OBLIGATION_ID constant reference (item 2's fold), one docstring line, one packet filename (item 6's bc14 fix), and a five-line block computing pairs from if code == "APPLIED" — which is item 5's fold and is a strengthening: that block made the test mirror the implementation's applied-only rule, and a probe built from the code under test is the bw28 class the packet itself warns about. Removing the mirror is the fix.

No fold's remedy gates a person — every one gates a number, a record, or a plan. No machinery appeared that r1 did not order: the largest fold is one validator call at one boundary plus one identity function, and both reuse existing in-lane machinery.

4. WHY-THIS-EXISTS

ALREADY-BUILT — EXECUTED. Every fold reuses machinery the engine already had; the derivation law moved rather than duplicating (generator :206 re-exports the packet constants, so there is one law and one call site family). Nothing external adopted. r1 shelf logs govern and I spot-ran their shape at this pin.

PRODUCT-FIT — EXECUTED. One sentence: the owner needs 768 scenarios that measure the hypothesis rather than a fixture artifact or a heuristic. The folds do exactly three things — refuse evidence the instrument cannot re-derive, stop the answer key being a constant, and make three records tell the truth about themselves. All fail-loud, all mirror-not-cop. Every refusal I triggered stops a wrong number; none gates a person.

BIGGER-THAN-THE-BUG — READ-ONLY. One validator call at one boundary plus one identity-derivation function. Against 601 added test lines, the production delta is 259/185/12 across three modules. Proportionate; no new subsystem.

PRIMARY-CONSUMER — EXECUTED. Unchanged: the frozen inference core, and behind it the owner defending one number. A bounded read of the census now buys the distinct-gold count against a named floor, the signature×motif cross-tab with the three residual signatures listed by name, and a coverage figure carrying both its set rules. That record is now honest about its own construction in a way it was not at r1.

5. SWEEP LOG
Query	Opened at origin	Deciding section	Effect
sequence covering array coverage definition event appears before another in test sequence counted regardless of outcome	arxiv.org/pdf/1602.06599 · csrc.nist.rip/groups/SNS/acts/sequence_cov_arrays.html · tsapps.nist.gov/publication/get_pdf.cfm?pub_id=906770 · mdpi.com/2073-8994/10/5/146	SCA definition ("appears at least once"); NIST's empirical basis ("whether a particular event had occurred prior to a second one")	Decided item 5's numerator semantics in the fold's favour — occurrence, not effect, is the criterion

SEARCHED (this round): SCA numerator/occurrence semantics.
RECALLED (carried from r1/the design arc, where I opened them at origin): U-CIT constrained-coverage denominators; Kuhn t-way detection rates; differential pseudo-oracle. None decides anything new here.
UNSEARCHED(SETTLED-BY-PINNED-BYTES): items 1, 2, 3, 4, 6 — all decided by executed bytes.
Stopped when the one live prior-art question had a controlling definition and NIST's own empirical rationale opened at origin.

6. Evidence read

MBCX-01-COHORT-BUILD-ACCEPTANCE-COUNCIL-PACKET-r2.md@210f1fa (full) · mbcx01_build_cohort_generator.py:48, 85, 192-206, 229-238, 258, 265-300, 612-632, 1083, 1150-1175, 1298-1315, 1419 · mbcx01_build_cohort_authority.py:148-163, 356-372, 423 · mbcx01_build_cohort_packet.py:23, 124, 148-160, 238-262, 425-455 · verify-build-bundle.py:20, 752, 764-767, 913-923, 1006 · mbcx01_r13_common.py:67 · git diff af1cc4f^..ad713b22 -- test_mbcx01_build_cohort.py (full removed-line set).

Probes (read-only, %TEMP%): consistent record+projection forgery vs both bindings · projection-field leak · closed-vocabulary membership · gold variety + SEMANTIC_ID legality + duplicate-gold injection · signature×motif cross-tab recomputation · _plan_placements strata cap + -1 census · coverage report check across six mutations · pin-manifest declared-set enumeration and REQUIRED overlap.

7. Residual risks
BUILD_OBSERVATION_PROJECTION_LEAK outside the closed vocabulary — build-list, one line, red-first.
Two refusal branches dormant at this pin — the ENVELOPE refusal class has zero members (enumerated in §8, not hidden) and the new len(placements) != placed_total guard never fires at k=12 against 16 strata. Both are correct code on unexercised paths; carried.
Single-motif residual pinned to 3 — a deliberate tripwire that flips bc19 RED on any population change. Right mechanism, real maintenance edge; declared.
W14(d) replacement sensitivity — self-declared non-mechanical by the bundle; unchanged.
Shared-reducer pseudo-oracle and the SCA lower-bound denominator — unchanged, both correctly declared.
8. Omission set — what this seat did NOT do
Did not run the clean-room verify-build-pinned.ps1. The packet's PINNED RECONSTRUCTION COMPLETE is driver-reported and I took it as a premise; item 6's bc14 fix was caught by that mechanism, so my ACCEPT there rests partly on a claim I did not reproduce.
Did not execute the admission-path ghost-FACT limit (item 1's declared gap) — read the declaration, did not drive it.
Did not exercise the ENVELOPE refusal branch or drive the plan-shortfall guard to a red.
Did not read the r1 synthesis, the other seats' verdicts, or the two SEAT3 codex logs sitting untracked in the work tree — sealed independence, deliberate. Where the packet cites seat 2's FOLD-1 class or seat 3's F1, I verified the bytes myself but took the attributions on trust.
Did not re-run the §0 no-threat-model grep — third consecutive round carrying that premise on the packet's word. It is now my longest-standing unverified assumption and I flag it as such.
Did not re-verify r1's settled items (1, 2, 3, 6, 7) — correct for a confirm round, but it means this verdict inherits their EXECUTED status rather than re-establishing it.

Six ACCEPTs. Per §13 the arc advances to the codex-CLI gate.
