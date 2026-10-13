# SEAT 2 (chatgpt.com sol, conversation <id>) — cohort-BUILD acceptance r2 verdict

> Banked VERBATIM by the driver from the seat thread via `browser_wait_quiesced`
> (textLen 13,720, truncated:false), 2026-08-16 ~19:50Z.

GO

EXECUTED verdict. I read MBCX-01-COHORT-BUILD-ACCEPTANCE-COUNCIL-PACKET-r2.md at commit 210f1faa12d69d594f096b2cb68a7bc2995870cb. Before reading further I independently verified the working-tree packet is 15,802 bytes with SHA-256 792244b4506d27f193b4dd7e965c1afc193e6e46189d30e1bc7625f0830b9242, exactly as commissioned. The reviewed content pin is ad713b22f9bad58e3de15df1a05bc78ebdb3728c; both commits exist, and git diff --stat ad713b22 HEAD -- '*.py' is empty. The two untracked r2 seat logs were seen by filename only and not opened.

The no-threat-model settling grep over the governing DoR again returned zero hits. I performed no ETW, Job Object, physical-harness activation, provider call, route trial, or spend.

Mandatory execution bank

EXECUTED

Cohort: python -m unittest -q test_mbcx01_build_cohort → 39/39 OK, 111.982s.

Literal full discovery: python -m unittest discover -q → 548/548 OK, 186.131s.

python verify-build-bundle.py → BUNDLE_EXIT=0.

frozen: 156 PASS

BUILD: 236 PASS

ledger: 101 invariants / 236 witnesses, two-way PASS

registration totality PASS

schemas PASS

canonical parity PASS

no-production-activation PASS

execution-posture PASS

Exact pinned reconstruction:
verify-build-pinned.ps1 -Commit ad713b22f9bad58e3de15df1a05bc78ebdb3728c -ManifestBlob bc21b78dcee2df3c20c88ddc49c9a78ec2ca4155
→ PINNED RECONSTRUCTION COMPLETE, CLEANROOM_EXIT=0.

I found no r2 finding meeting §0's wrong-number / wrong-evidence / wrong-refusal threshold.

Evidence read

Load-bearing reviewed bytes include:

MBCX-01-COHORT-BUILD-ACCEPTANCE-COUNCIL-PACKET-r2.md:10-20,29-48,50-134,146-170

mbcx01_build_cohort_packet.py:244-273 — moved observation derivation law.

mbcx01_build_cohort_packet.py:411-475 — serving-side projection recomputation + derivation binding.

mbcx01_build_cohort_packet.py:600-682 — full BUILD manifest validation.

mbcx01_build_cohort_packet.py:786-849 — actual serving boundary; full validation when context/authority exists.

mbcx01_build_cohort_generator.py:225-277 — declared signature residual, coverage semantics, per-scenario target identity.

mbcx01_build_cohort_generator.py:1157-1203 — distinct-gold census + signature×motif census.

mbcx01_build_cohort_generator.py:1288-1330 — placement-totality refusal.

mbcx01_build_cohort_generator.py:1400-1420 — derived-axis fail-loud path.

mbcx01_build_cohort_authority.py:356-374 — coverage report fields required.

verify-build-bundle.py:755-804,852-950 — declared pins beyond REQUIRED and level-b enforcement.

test_mbcx01_build_cohort.py:2549+ — bc15 serving-boundary ghost witness.

test_mbcx01_build_cohort.py:2626+ — bc16 non-derived observation witness.

test_mbcx01_build_cohort.py:2744+ onward — bc18–bc21 folds.

Six explicit rulings
1. ACCEPT — serving boundary re-derives what it serves

EXECUTED.

I reran both of my r1 deciding forgeries against freshly rebuilt, internally self-consistent candidate/provenance/authority contexts.

R1 ghost FACT:

ghost_served =
  BuildCohortPacketError
  BUILD_FACT_ROW_WITHOUT_JOURNAL_ANCESTRY

The same ghost deliberately still passes the pre-selection admission render:

ghost_admission = True []

That split is honest. Admission is the envelope/planning stage; the actual model-serving path carries a context and now invokes full semantic validation. The ghost cannot cross that boundary.

R1 self-consistent gold-bearing observation:

gold_observation_served =
  BuildCohortPacketError
  BUILD_OBSERVATION_REPRESENTATION_DIVERGENT

I then constructed the requested third shape: changed the stored observation projection's fact_row_count, freshly called the approved derivation function on that fictional projection, and rebuilt the complete record and both representations. Thus record↔projection was internally perfect:

third_record_selfderived = True

But serving independently re-derived the projection from replayed state and refused it:

fictional_projection_served =
  BuildCohortPacketError
  BUILD_OBSERVATION_REPRESENTATION_DIVERGENT

The interface move is also coherent: the derivation law now lives in the packet sibling and the generator re-exports it rather than owning a divergent duplicate.

The raise-only BUILD_OBSERVATION_PROJECTION_LEAK posture is accurate: serving converts derivation/projection faults into the closed BUILD_OBSERVATION_REPRESENTATION_DIVERGENT verdict before they reach an error list.

RULING 1: ACCEPT.

2. ACCEPT — retained answer key is no longer constant

EXECUTED.

Fresh full-population result:

retained                  = 768
distinct gold action IDs  = 768
census count              = 768
declared floor            = 768
bad SEMANTIC_ID targets   = 0

target_obligation_id(scenario_id) produced a legal semantic target for every retained candidate. I also inspected one retained candidate from every motif; all six motif postconditions survived the varied target identity:

correction/restoration: prior value restored;

lifecycle: terminal/reopen behavior intact, target never reopened;

dependency reversal: blocked→due holds;

cross-scope: genuine multi-scope journal, zero foreign scored rows;

delegation: two DUPLICATE_NOOPs and role rewrite;

delayed continuity: earlier illegal / chosen-cut uniquely legal.

The r1 driver's decision to vary target identity was therefore technically correct: it removes the demonstrated constant-answer-key wrong-number channel without damaging the motif contracts or frozen layer. The owner still sees that decision at the merge gate as recorded.

RULING 2: ACCEPT.

3. ACCEPT — motif codebook is measured and honestly declared

EXECUTED / READ-ONLY.

The live census reproduces the declared residual exactly:

single-motif observation signatures = 3
retained rows carrying them          = 15
declared residual                    = 3

I then serialized all six A0/B/A1 BC/OM packet surfaces for a real retained scenario and searched those model-visible bytes:

other retained scenario IDs visible = 0
population census terms visible      = False

So the model receives the current scenario's packet, not the cross-scenario signature→motif table required to exploit the measured population statistic as such. This is consistent with the governing serial cold-episode design.

The discarded padding alternative is not an obviously superior close: it changes actual served population content merely to flatten a declared distribution tail, and the attempted bounded reshape did not eliminate the residual anyway. Pinning the measured residual means any future population change makes bc19 demand explicit reconsideration instead of silently drifting.

RULING 3: ACCEPT.

4. ACCEPT — plan record cannot overstate achieved placement

EXECUTED.

I reran the pathological helper shape from r1:

requested placements   = 12
actual _plan_placements = 1
guard_would_refuse      = True

The live fold at generator.py:1300-1310 now refuses exactly this mismatch instead of writing placed_total=12 into the signed plan.

On the real pinned population:

planned_ineligible_placed ==
len(planned_ineligible_scenarios)
for every motif = True

I also attacked the former -1 census escape by breaking a candidate's action catalog. _record_derived_axes() now fails loud:

BuildGenerationRefusal:
BUILD_DERIVED_AXIS_UNRECORDABLE

rather than inserting sentinel -1 data.

The ENVELOPE refusal class having zero live members is a coverage residual, not a hidden arithmetic bug; it is explicitly declared.

RULING 4: ACCEPT.

5. ACCEPT — coverage record now describes its actual numerator

EXECUTED / SEARCHED.

I recomputed the numerator independently from every gate-checked event in every generated program:

reported covered pairs   = 151
independent recomputation = 151
target denominator        = 289
covered_pair_rule =
  ORDERED_PAIRS_OVER_ALL_GATE_CHECKED_PROGRAM_EVENTS
target_set_rule =
  UNCONSTRAINED_ORDERED_PAIR_SQUARE_OVER_17_EVENT_ALPHABET

Deleting either declaration makes the authority report fail:

drop covered_pair_rule
→ BUILD_SEQUENCE_COVERAGE_UNREPORTED


drop target_set_rule
→ BUILD_SEQUENCE_COVERAGE_UNREPORTED

Counting a legal DUPLICATE_NOOP event is appropriate for the declared quantity: NIST defines t-way sequence coverage over ordered event sequences and uses labeled transition systems to identify valid event-sequence targets; it does not define sequence occurrence only in terms of state-mutating successes.

MBCX still honestly labels 151/289 as the unconstrained-square lower bound rather than claiming exact LTS-constrained coverage.

RULING 5: ACCEPT.

6. ACCEPT — W14(b) difference set is declared and works in both layouts

EXECUTED.

Current worktree:

registration status                      = PASS
pinned - REQUIRED count                  = 30
declared beyond-REQUIRED count           = 30
actual difference == declared set        = True

I injected a fresh undeclared subject through both pin sources:

stray in pin-manifest document
→ W14_PIN_MANIFEST_SUBJECT_OUTSIDE_DECLARED_SET


stray in generator pin list
→ W14_PIN_MANIFEST_SUBJECT_OUTSIDE_DECLARED_SET

The 30 legitimate extras are explicitly documented in verify-build-bundle.py:767-804: BUILD-side reconstruction subjects plus the frozen r13.2 dependencies the bundle re-runs. Literal equality would indeed refuse the correct reconstruction.

Most importantly, I executed the exact pinned reconstruction layout that exposed the original bc14 bug. It completed:

PINNED RECONSTRUCTION COMPLETE
CLEANROOM_EXIT=0

The allowlist can of course be changed by a future code edit; that edit is itself the declaration and remains review-visible. There is no current runtime path that silently grows it.

RULING 6: ACCEPT.

Omission attack

EXECUTED / READ-ONLY.

The fold diff changed three existing witness regions, and each change is explicitly rider-marked:

bc02's scored target lookup now derives the per-scenario target identity;

bc06's coverage recount no longer mirrors the former APPLIED-only implementation;

bc14's unpinned-layout probe now uses the pin manifest itself, which exists in both legitimate layouts.

The new bc15–bc21 tests cover the new fold surfaces. I found no previously covered route made unreachable and no new person-facing gate. The new checks stop malformed experiment evidence or false records only.

I found no omitted seventh fold surface in this targeted round.

WHY THIS EXISTS

ALREADY-BUILT — EXECUTED. The folds reuse existing replay, manifest validation, census, report and registration machinery. The observation law moved rather than being duplicated. My independent source-only sweep for ObservationAuthority, target_obligation_id, sequence coverage, retained_set_root, and membership-substitution shapes across bridge src/, Photon crates/, and Gravity src/ returned zero files in all three.

PRODUCT-FIT — READ-ONLY. Yes. Plainly: the owner needs the fixed 768 scenarios to measure BC versus OM, with every model-visible fact and answer identity derived rather than accidentally stamped by the harness.

BIGGER-THAN-THE-BUG — READ-ONLY. No. The largest repair is making an already-existing semantic validator load-bearing at the serve boundary and moving one existing derivation law to the layer that can re-run it. No new subsystem or enforcement machine appeared.

PRIMARY-CONSUMER — READ-ONLY. The BUILD scorer/inference ingress and ultimately the owner defending the scientific result consume these records. The census now tells them the answer-key variety, the declared motif-signature residual, and the exact meaning of the coverage number.

SWEEP LOG

SEARCHED.

Exact queries:

site:csrc.nist.gov sequence covering arrays event sequence testing ordered pairs t-way labeled transition system
site:csrc.nist.gov "Efficient Algorithms for T-way Test Sequence Generation"

Opened at origin:

https://csrc.nist.gov/pubs/conference/2012/10/16/efficient-algorithms-for-tway-test-sequence-genera/final — abstract, especially lines 80-87: ordered event sequences, general labeled transition systems, and valid t-way target sequences.

https://csrc.nist.gov/Projects/automated-combinatorial-testing-for-software/combinatorial-methods-in-testing/event-sequence-testing — "Need for Sequence Covering" and definition, lines 79-105: order rather than adjacency is load-bearing and sequence covering exercises t-event permutations.

This confirmed item 5's terminology and the existing lower-bound disclosure. I stopped there because items 1-4 and 6 are determined by pinned repository bytes and my own executions, not outside standards.

Residual risks

No blocking finding remains. Carried residuals are accurately named:

pre-selection admission is not a ghost-FACT gate; full semantic gating happens at the actual serve boundary;

3 of 23 observation signatures remain single-motif, covering 15/768 rows;

ENVELOPE refusals have zero live members at this pin;

sequence coverage uses the registered unconstrained 289-pair superset, so its ratio is a lower bound rather than exact LTS-constrained coverage;

W14(d) replacement sensitivity remains partly red-first discipline rather than mechanically proven by the ledger schema;

dual-reducer agreement remains a pseudo-oracle against shared semantic bugs;

no physical harness, provider route, or scientific experiment has been executed;

the existing two ResourceWarnings for fixture file readers still appear during discovery/bundle but produced no demonstrated measurement consequence.

Fix class: NONE.

All six r1 folds survive independent executable confirmation, including my two original deciding attacks and a fresh third derivation-binding attack.

FINAL VERDICT: GO.
