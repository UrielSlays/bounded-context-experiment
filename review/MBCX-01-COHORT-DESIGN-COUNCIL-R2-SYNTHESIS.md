# Cohort-content design council r2 — synthesis and disposition (2026-08-16)

Round: 3/3 COMPLETE — SEAT1 GO-WITH-FIXES (EXECUTED) · SEAT2 NO-GO (EXECUTED) · SEAT3 NO-GO
(EXECUTED). All three: the r2 architecture core STANDS (journal replay, three-sibling shape,
quota, admission-at-generation, journal-bound provenance) and every remaining fix is a bounded
specification correction inside the slice. R4's motif postconditions were executed by two
seats this round — including the four contracts seat 1 declared un-run, which seat 3 ran
(non-target lifecycle chain, foreign-scope zero rows, delayed due, owner-role rewrite, B-call,
rejection path, blocked→due) — and CORRECTION_RESTORATION's full reassert chain now has an
executed witness (seat 1), closing the driver's own P1 gap. Driver byte-verifications this
synthesis: `render_served_input` padding + `>` comparator (`mbcx01_r13_packets.py:302-306`),
`MANIFEST_KEYS` closed set + frozen-motif + position couplings (`:203-222`),
`_fixture_authoritative_state` literals + projection equality (`:352-376`).

## Adjudications (differing labels, complementary evidence — nothing averaged)

- **R1 observation authority — FOLD BOTH HALVES.** Seat 1 attacked CONSISTENCY (sound: no
  constructible divergence W15 misses; `observation_authority_hash` correctly routed around
  the closed `MANIFEST_KEYS`). Seats 2+3 attacked SEMANTICS (defective: a consistent
  observation can carry the gold literal — executed, served four times). Not a conflict —
  two halves of one law. r3: closed observation grammar with FORBIDDEN INPUTS (motif label,
  gold, selector output, retained position, action identity), non-leakage witness
  (relabeling invariance + no gold/action encoding), consistency machinery kept as-is.
- **R2 quota — FOLD the census + total-admission.** Seat 1 sound-with-residual; seats 2+3
  defective (family-deletion counterexample; envelope refusals uncounted). r3: quota composes
  over ALL refusal classes; multivariate retained/rejected census across every declared
  semantic axis, not world size alone.
- **R3 — CONVERGENT 3/3, the round's strongest class, now FOUR surfaces deep.** Seats 2+3:
  the frozen scorer/outcome joins hard-wire frozen retained authority (executed:
  `I01_INVARIANT_INVALID`). Seat 1: `_fixture_authoritative_state` on the DEFAULT scoring
  path hard-codes the frozen obligation literals (executed both failure branches). r3: module
  3 becomes the cohort PACKET/SCORER sibling — owns the manifest, supplies
  `authoritative_state` from the replayed generation state (witnessed against
  `project_state_world`), and carries the exact-subtractive scorer/outcome wrapper on the
  named internal pattern (`mbcx01_build_state_authority.verify_production_scorer_input`).
  W16 pushes one retained BUILD candidate through scorer-input/I01 + scenario-outcome
  validation end-to-end.
- **R4 — SOUND on realizability (2 seats executed), DEFECTIVE on contract TEXT (seat 1's
  duplicate matrix).** r3: every motif contract carries postcondition + legal realization
  CONSTRUCTION + exact expected result-code sequence; W4 asserts codes
  (`DUPLICATE_NOOP` ≠ `PROPOSAL_INVALID`/`COMMIT_INVALID`/`IDEMPOTENCY_CONFLICT`, all of
  which leave state byte-unchanged — a state-only witness is non-discriminating).
- **R5 — CONVERGENT 3/3.** Sequence coverage, not event×position. r3: constrained sequence
  covering arrays over the 17-event alphabet (reducer-legal, reducers as the LTS; ordered
  pairs minimum) as the PRIMARY provenance number; event×position secondary; composes with
  the omission-configuration axis (which generates the orderings the SCA scores).
- **R6 — the comparator was wrong twice over (seats 2+3 executed; driver byte-verified).**
  Padding makes "served < 65,536" unsatisfiable and `≥` refuses the legal exact-fit. r3:
  admission = both BC and OM renders SUCCEED (delegate to the frozen renderer); stated
  algebraically over UNPADDED canonical length ≤ 65,536; W13 restated.
- **R7 — FOLD BOTH.** Seats 2+3: decision relevance (executed: diversity + gold-leak coexist;
  OM-only row decision-redundant with `prerequisite_obligation_ids`). Seat 1: record W10's
  honest limit (structural half only; statistical power unknowable pre-run). r3: W10 =
  diversity + a model-free relevance condition (for a declared coverage class, OM-only
  evidence is NECESSARY for gold derivation under a registered counterfactual) + the stated
  limit in the design's non-claims.
- **R8 — FOLD both residuals.** Seat 3: JSON/artifact namespace totality (cohort spec +
  provenance manifests get a named glob-checked namespace). Seat 1: module-to-witness
  coverage (every `BUILD_MODULES` entry exercised by ≥1 declared witness). Pin discipline
  verified working by all three seats.
- **Frozen couplings recorded as design constraints:** `MANIFEST_KEYS` is closed (no new
  manifest key without an amendment); the motif taxonomy is frozen to the six
  (`validate_expected_manifest:217`); `retained_position < 768` (`:222`).

## Round-shape check (ANTI-DRIFT §1)

Findings are narrowing and flipping toward "delete / use the simpler existing form" (comparator
delegation, contract text carrying construction, census instead of proxy) — the convergence
signature forming, not self-inflicted machinery: no fold this round added surface a seat then
attacked; every r2 fix class traces to a frozen byte that predates the lane. Round 3 carries
the binding ROUND CALL.

## Disposition

Design r3 (same file, r3 header); round 3 to the same three seats, blind, ROUND LEDGER
carrying r1 (3×NO-GO) and r2 (GWF/NO-GO/NO-GO). Round 3 verdict FIRST LINE is GO-TO-CODE or
CONTINUE-DESIGN per the card; GO-TO-CODE outranks further design findings, and remaining
mechanically-testable leftovers become the BUILD's red-witness list.
