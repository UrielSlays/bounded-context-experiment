# Cohort-BUILD acceptance council r1 — synthesis (2026-08-16)

Round: COMPLETE, 3/3, every verdict EXECUTED. **Outcome: NO-GO**
(SEAT1 Claude GO-WITH-FIXES · SEAT2 ChatGPT-sol NO-GO · SEAT3 codex NO-GO).
Packet `MBCX-01-COHORT-BUILD-ACCEPTANCE-COUNCIL-PACKET-r1.md@8432132`; content pin
`f35851e`. Verdicts banked verbatim beside this file (SEAT1/SEAT2 .md, SEAT3 stdout log).
**Every finding below was reproduced by the driver at the byte before this synthesis was
written** — `driver_repro_cohortbuild_r1.py` (committed; both runs' outputs quoted below;
the first run's R5 failure was the DRIVER's harness — raw candidate passed where the
context indexes the enriched retained copy — recorded per the broken-harness law).

## Driver reproductions (all confirmed)

- **R1 (S1-A):** distinct `gold_action_id` over the retained 768 = **1**
  (`ACT.F0BAE0DD…`), exact hash matches seat 1's.
- **R2 (S3-F1):** 23 chosen-cut observation signatures; **3 map to exactly one motif; 15
  retained rows** carry a single-motif signature — exact counts match seat 3.
- **R3 (S3-F2):** coverage numerator APPLIED-only **150** vs all-executed-events **151**;
  the missing pair is `commit_handoff_result > commit_handoff_result`.
- **R4 (S1-B/S3-F3):** `_plan_placements` requested 12 on a one-stratum draft set →
  returned **1**; the plan record would sign 12.
- **R5 (S2-F1):** ghost FACT with rebuilt self-consistent provenance/context:
  `validate_build_manifest` refuses (`BUILD_FACT_ROW_WITHOUT_JOURNAL_ANCESTRY`) but
  `build_scoring_fixture_for_candidate` BUILDS, the ghost is in BC A0, and
  `render_all_six_nodes` admits — the validator is not on the serving path.
- **R6 (S2-F2):** forged observation record carrying the literal gold action id, rehashed:
  record validates, **`validate_build_manifest` returns `[]`**, gold serves as observation,
  all six renders admit; fresh `derive_observation_authority` on the record's own stored
  projection disagrees (`FACT.DEPTH.1`) — admission checks self-consistency, not derivation.
- **W14(b) byte check:** `verify-build-bundle.py:922-926` implements `REQUIRED ⊆ pinned`
  and self-reports the difference (`level_b_pin_manifest_is_subset_not_equal`) — the design
  sentence says equality; both seats' halves are true.

## Adjudications (conflicts ruled at the byte, not averaged)

1. **Coverage numerator (S3 DEFECTIVE vs S1/S2 conservative-and-declared):** ruled WITH
   S3 on the fix, WITH S1/S2 on severity. The record declares its DENOMINATOR rule
   (`target_set_rule`) but not its NUMERATOR rule; a `DUPLICATE_NOOP` is a legal executed
   program event under design §2.6's sequence semantics, so the natural reading of
   `covered_pair_count` is false by one pair, in the conservative direction. Fold: count
   pairs over ALL gate-checked program events (150→151) AND declare the numerator rule in
   the record; make bc06's recomputation non-mirroring.
2. **W14(b) (S3 DEFECTIVE vs S2 defective-as-worded/non-blocking):** ruled BOTH-halves.
   The subset is deliberate and right (equality would refuse legitimate frozen-dependency
   pins — S2), and the unconstrained difference set silently carries a stray pin-only
   subject (S3's executed injection). Fold: constrain `pinned − REQUIRED` to a DECLARED
   allowlist (named refusal on a stray), and amend the design §3(b) sentence to the
   implemented + constrained contract.
3. **Items 4/5 (S1/S3 SOUND vs S2 DEFECTIVE):** not a conflict — complementary depth.
   S1/S3 ruled the DISCRIMINATOR sound (it is); S2 constructed the stronger probe showing
   the discriminator is not INVOKED on the serving path. S2's finding governs.
4. **Population content (S1's constant gold · S3's motif codebook):** one class, two
   independent instances — model-diverse convergence on POPULATION DEGENERACY, stronger
   than either alone. Gold constancy is the deciding wrong-number channel: a positional
   heuristic ("the second action in sorted order") scores at ceiling in BOTH arms with no
   population knowledge, collapsing the BC/OM contrast for a reason unrelated to the
   hypothesis. The motif codebook violates §2.2's own declared forbidden-input law at the
   population level; its live exploitation path is weaker (requires cross-scenario
   statistics a frozen cold-episode subject does not have), so it folds as: measure the
   cross-tab in the census (truth in the record), reshape generation cheaply if a small
   tweak clears it, and otherwise DECLARE the residual with its measured count — no
   machinery beyond one census key and one witness.
5. **S1's "owner ruling first" on gold variety:** ruled per BEFORE-YOU-ASK §3-A — the
   evidence converges (three seats + driver reproduction + the estimand's own arithmetic;
   no defensible position argues FOR a constant answer key), so the driver rules it:
   **vary the target obligation identity per scenario** inside the existing hash-derived
   variation machinery. Recorded here for the owner's visibility; the r2 re-round attacks
   the ruling; the owner's merge gate remains the final check. The cohort content design
   doc (BUILD-class, this lane's own) is amended in the same fold — the frozen layer is
   NOT touched.
6. **Serve-boundary re-derivation vs the no-adversary law:** passes the discriminator —
   it stops a WRONG NUMBER (any drift/bug between generation and serving would today serve
   unverified evidence silently); it gates no person; it reuses the validators that already
   exist. This is the I01-I17 philosophy (every join mechanically reproduced) applied at
   the one boundary that reaches the model.

## Fold orders (all red-first; frozen layer untouched by every one of them)

- **FOLD 1 — SERVE-BOUNDARY SEMANTIC RE-DERIVATION (S2's class, deciding):**
  (a) `validate_build_manifest` gains derivation-binding: the observation record must
  EQUAL `derive_observation_authority(scenario_id, cut_id, record.projection)` recomputed,
  and the stored projection must equal a recompute from the replayed state + variation;
  (b) the derivation law (pure function + its constants) moves to the packet sibling so
  the check has no import cycle (generator already imports packet; generator adopts
  packet's law — an interface fold, named for the r2 round per §13);
  (c) `build_scoring_fixture_for_candidate` / `render_all_six_nodes` run
  `validate_build_manifest` (full BUILD semantic validation) before serving.
  Reds: R5 and R6 (both currently ADMIT through the serving path).
- **FOLD 2 — POPULATION CONTENT:** per-scenario hash-derived target obligation identity
  (768 distinct golds); census/provenance gains distinct-gold count with a declared floor
  + witness; population cross-tab (signature→motif) measured in the census; single-motif
  signatures reshaped away if a bounded tweak achieves it, else declared with the number.
  Reds: R1 (distinct golds = 1) and R2 (3 single-motif signatures) as pre-fix witnesses.
- **FOLD 3 — PLAN-RECORD TOTALITY:** `len(placements) == placed_total` or the plan is
  REFUSED (`BUILD_GENERATION_PLAN_REFUSED`); `_record_derived_axes` refuses loud instead
  of writing −1. Red: R4's one-stratum shape.
- **FOLD 4 — COVERAGE NUMERATOR:** all-events numerator + declared numerator rule in the
  record + non-mirroring bc06. Red: R3 (150 vs 151).
- **FOLD 5 — W14(b):** declared allowlist for `pinned − REQUIRED`; stray pin-only subject
  fails by name; design §3(b) sentence amended to the implemented contract.
  Red: S3's injected pin-only subject (currently PASS).

## Non-findings that stand (all three seats, executed)

Replay gate · eligibility derivation (enrichment loop closed at `BUILD_CANDIDATE_KEYS`) ·
envelope admission (delta ∈ {0,1,2}, never negative; exact-fit safe both ways) ·
exact-subtractive wrapper (inertness control held under both seats' forgeries) ·
inference ingress (duplicates/missing/substitution all die by name) · census delimiter
(unreachable at closed enum domains) · spec-artifact canonical serialization (both ways).

## Residuals carried (homes unchanged: #31 unless noted)

SCA unconstrained-denominator lower bound (S1 opened the U-CIT literature; conservative,
correctly labelled) · W14(d) half-mechanical · 8/12 forbidden inputs structural · W10
selection-level · shared-reducer pseudo-oracle · T1-pinned cuts · frozen private-name
dependency · two ResourceWarnings in `test_mbcx01_build_integration.py` (S2; no
measurement consequence found — build-list note).

## Next

Fold 1-5 red-first (workers, disjoint scopes, driver re-runs every red) → gates
(cohort/discover/bundle) → **r2 re-round on the folded bytes** (§13: FOLD 1's interface
move + FOLD 2's design amendment are exactly what a fresh round must attack) → codex-CLI
to literal green (#1) serialized after the seats.
