# Cohort-content design council r1 — synthesis and disposition (2026-08-16)

Round: 3/3 COMPLETE, all EXECUTED — SEAT1 (new-account claude seat, provenance deviations in its
bank file) NO-GO · SEAT2 (ChatGPT) NO-GO · SEAT3 (codex-exec, r1b after a verdictless first
death) NO-GO. Every disposition below rests on a driver reproduction
(`MBCX-01-COHORT-R1-DRIVER-REPRODUCTIONS.md`) or a driver byte-read named inline — no seat's
word is banked bare. The design core (journal-as-state, dual-reducer replay at generation,
derived eligibility, seedless framed-hash determinism, adopt-the-frozen-selection) survived all
three seats intact; the NO-GOs are completeness and invariant defects, every fix a
SPECIFICATION correction, none a new machine.

## Conflicts adjudicated at the byte (never averaged)

- **C3 (seat2 SOUND vs seats 1+3 DEFECTIVE): DEFECTIVE governs.** Seat 1's exact binomial
  reproduced by the driver to four decimals (`p=0.20 ⇒ P(motif shortfall)=0.4529, any-of-6
  =0.9732`): threshold placement breaks the ≥128 floor at exactly the ineligible rates that
  make filtering meaningful. Seat 2 attacked the predicate (sound) but never priced the floor.
  Fold: QUOTA placement — exactly k ineligible per motif, declared constant ≤ 32, ranked by
  framed_hash, stratified across the three ineligible shapes; floor becomes arithmetic;
  distribution witness on retained-vs-rejected world size (the bias half).
- **C6 (seats 1+2 SOUND vs seat 3 DEFECTIVE): both right; the remedy is seat 3's.** The bound
  is input-shape-sensitive (seat 3 overflowed BC by 14 bytes at 30 obligations with 4 source
  events/row + 128-char IDs; seats 1/2 measured fits with smaller shapes; real ceiling ≈190-200
  world objects). Fold: BC and OM rendered AT GENERATION, envelope fit an ADMISSION condition
  pre-selection; measured bound recorded as a declared constant; served-size witness added.
- **C7 (seats 1+3 DEFECTIVE vs seat 2 conditional-SOUND): DEFECTIVE governs.** Seat 2's SOUND
  was expressly conditional on perfect registration; seat 1 traced the tuple-scope bypass and
  the driver's P5 read confirmed `reconcile_pin_manifest` never equates the manifest subject
  set with `REQUIRED`. Fold: glob-vs-tuple two-way totality (modules + test modules, both
  directions) + REQUIRED == manifest-subjects assertion + `BUILD_WORK_PRODUCTS` named in the
  registration list, with a witness.

## Convergent findings (model-diverse, multiply-executed — the strongest signal)

1. **Motif = semantic contract, not event vocabulary** (all three seats; driver P1 executed:
   assert→correct→retract leaves NOTHING visible — the correction's closure survives the
   retraction). CORRECTION_RESTORATION's "retract restores the head" claim is DELETED;
   restoration is realized as explicit reassertion with the postcondition "a prior value_code
   is visible again at a later cut." Every motif gains an observable postcondition; witnesses
   assert postconditions, not token presence.
2. **Observation/FACT authority** (all three; driver P2 executed: ghost FACT + contradictory
   observation → zero manifest errors). New ObservationAuthorityV1: one deterministic record
   per scenario/cut from which BOTH the top-level observation and the world OBSERVATION row
   derive; observation becomes a declared variation axis; FACT world rows become endogenous
   (derived from replayed state in the BUILD manifest sibling); both witnessed.
3. **The SECOND stamp** (seat 1 primary F1; seat 3's catalog finding is the same organ; driver
   P3 executed: one catalog hash across all 768, no candidate carries a catalog).
   `manifest_for_retained_candidate` hard-codes scope/target/decoy/catalog/BC-selection.
   Fold: the slice becomes THREE named BUILD siblings — generator · cohort authority/selector ·
   manifest builder — landing TOGETHER (a generator-only slice would turn every witness green
   over a still-stamped served packet; seat 1: "green is exactly what stops the next person
   looking").
4. **Journal not bound in provenance** (seat 1 F3, executed; resolves design Item 7c AGAINST
   the design). Fold: `event_program_hash` + `observation_authority_hash` sub-digests in the
   BUILD provenance sibling + a journal-only-mutation red witness.
5. **Coverage invariant inverted** (seats 1+2+3): stated against the 17-event ALPHABET with
   named, reasoned exclusions (`record_call_response` enters via the handoff family's B-call
   record); measured 1-way and 2-way over (event × lifecycle-position) and REPORTED in
   provenance, not merely asserted. Seat 1's swarm-layer proposal (Groce et al., ISSTA 2012,
   SEARCHED at origin) is adopted in bounded form: per-candidate hash-derived mechanism-omission
   configurations WITHIN families, six motifs kept as named anchors — not a repartition.
6. **The sentinel gets its witness** (seat 1 F4): W10 — gold read-set variance across the
   retained 768 with a non-degenerate BC/OM difference. Red today by construction.
7. **I15 restated** (seat 1 C2b): dual-reducer agreement is CONSISTENCY, not correctness; the
   generation gate keeps it and adds the DoR legality predicate as a third check at the
   frontier. Seat 1's omission-set item "no seat executed a replay pair" is discharged: the
   DRIVER executed the pair in P1 (both engines, byte-identical states).
8. **Cross-scope collision restated** (seat 1 sub-finding): the projection is scope-local, so
   the motif's observable work is (a) in-scope subject/name collision pressure and (b) the
   postcondition that the scored projection carries ZERO foreign-scope objects while the
   journal is genuinely multi-scope.
9. **C4 caveat recorded**: the reopen constraint is a POPULATION EXCLUSION (BC/OM is never
   measured over target-reopen), stated in the design's non-claims, not only a #23 note.

## Driver defects this round, on the record

- The fabricated 40-hex pin (all three seats caught it; seat 1 additionally showed
  `git rev-parse --verify` echoes a bad 40-hex without erroring). Standing fix: pins only as
  emitted by `git rev-parse`; `git cat-file -e` gate before every dispatch.
- The r1 dispatch to seat 1 was owner-relayed into an unprimed conversation after the account
  death (no card, no read-probe, no model-at-mint check by the driver). The verdict's evidence
  quality (pinned blob hashes, executed probes, reproduced findings) is what admits it; the
  deviation is recorded in the bank file and this line, and the r2 dispatch to that seat
  carries the card first.

## Disposition

Design returns to draft as **r2** (same file, revision block; new pin at the r2 commit).
Round 2 goes to the SAME three seats, blind, with the ROUND LEDGER carrying r1's three NO-GOs.
The re-review trigger fired legitimately (candidate shape and authority surface changed);
mechanically-testable leftovers (exact k values, envelope constant, mechanism minimums) are
BUILD test material, not round fuel.
