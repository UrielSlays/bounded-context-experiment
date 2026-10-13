# MBCX-01 COHORT-BUILD acceptance council packet — r2 (targeted confirm: the r1 folds only)

Packet prose is a pointer map, not evidence — byte-check it.

ROUND LEDGER: cohort-BUILD acceptance council round 2 (r1: GO-WITH-FIXES / NO-GO / NO-GO,
all EXECUTED, folded — this round confirms those folds and NOTHING else) · codex rounds 0
of 2 — a code lane; codex-CLI to literal green (#1) follows a clean confirm, serialized
after the seats.

## 0. The one thing this round is for

**NORTH STAR unchanged: the numbers this instrument produces must be true.** No threat
model exists (settling grep in the r1 packet §0 — driver re-ran at that pin: zero hits;
the fold arc touched no DoR file that grep covers except the cohort design doc, which
carries only dated amendment markers). A finding counts iff it names its wrong-number /
wrong-admission / wrong-refusal consequence. ⛔ No new machines. **This is a CONFIRM
round, deliberately narrow:** the six fold surfaces below and nothing else — every other
surface carries EXECUTED rulings from r1 (items 1,2,3,6,7 ruled SOUND by executing seats)
and is settled. Convergence signature to watch: findings flipping to "delete X / already
right", seats describing the same fixed point, an empty omission attack.

## 1. Verdict contract

First line: **GO / GO-WITH-FIXES(class) / NO-GO**. Code artifact — no round-call token,
skip the design questions. Evidence read (`path:line`), SWEEP LOG, findings labelled
EXECUTED/READ-ONLY with data consequences, a RULING per item (ACCEPT / CHANGE + one line),
residual risks, fix class. Whole verdict in-thread; write nothing to disk.

## 2. Canonical bytes (path@sha pins)

Governing CONTENT commit under review: **`ad713b22f9bad58e3de15df1a05bc78ebdb3728c`**
(`git cat-file -e` gated). HEAD at dispatch `e2b22398be92001a72deed52af1535174657df22`;
`git diff --stat ad713b22 HEAD -- '*.py'` is EMPTY (driver-verified — records/log commits
only), so the working tree's .py bytes ARE the pinned bytes. The r1 record set:
`MBCX-01-COHORTBUILD-ROUND-r1-SYNTHESIS.md` (adjudications + fold orders) · the three r1
seat verdicts (SEAT1/SEAT2 .md, SEAT3 stdout log) · `driver_repro_cohortbuild_r1.py`
(driver reproductions R1-R6) · fold commits `af1cc4f` (FOLDs 1+5) · `cd07ebf` (FOLDs
2-4 + ledger) · the bc14 layout fix at `ad713b22`.

## 3. Immutable truths / invariants

Unchanged from r1 §3 (frozen layer + A-1/2/3 settled; zero frozen files touched by any
fold; matrix rule; readiness `BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`;
frozen couplings; ENGINE-FIRST + no-adversary owner rulings). Driver pre-dispatch gates at
the pin: cohort **39/39** · full discover **548/548** · `verify-build-bundle.py` REAL exit
0 (ledger **101 invariants / 236 witnesses two-way**) · clean-room
`verify-build-pinned.ps1 -Commit ad713b22 -ManifestBlob bc21b78d` →
**PINNED RECONSTRUCTION COMPLETE**, real exit 0.

## 4. Claims to attack — the six r1 fold surfaces, each with a RULING ask

1. **The serving boundary re-derives what it serves (FOLD 1, seat 2's deciding class).**
   ADVERSARY: internal-consistency — semantically non-derived evidence still reaching a
   served packet, or a truthful candidate newly refused.
   REACHES IT VIA: `build_scoring_fixture_for_candidate` (runs full
   `validate_build_manifest` incl. NEW derivation binding — the observation record must
   equal `derive_observation_authority` recomputed from its own stored projection, and
   the projection must equal a recompute from replayed state + variation); the derivation
   law MOVED generator→packet (generator re-exports; an interface fold — attack the move).
   Reds banked: bc15 (R5 ghost FACT — pre-fix the serving path ADMITTED it) · bc16 (R6
   forged gold-bearing observation — pre-fix `validate_build_manifest` returned `[]`).
   Attack: forge a record AND its projection consistently (the projection recompute must
   catch it — prove or break); the DECLARED admission-path limit (no context ⇒ only the
   two observation bindings run; a ghost FACT is not gated at ADMISSION — the fold's
   docstring declares this; is the declaration honest and is the limit safe?); the rider
   `BUILD_OBSERVATION_PROJECTION_LEAK` is raise-only, not in the closed vocabulary.
   **RULING ASK: ACCEPT the boundary + the interface move + the declared admission limit,
   or CHANGE.**
2. **The retained answer key is not a constant (FOLD 2a, seat 1's finding A — and the
   driver's ruling to fold it WITHOUT a standing owner round).** Per-scenario target
   identity `OBL.TGT.<scenario_id>` (distinct by construction, no hash); 768 distinct
   golds; census reports the count against declared floor
   `ONE_DISTINCT_GOLD_ACTION_ID_PER_RETAINED_ROW`, refusal
   `RETAINED_GOLD_VARIETY_BELOW_FLOOR`. Red banked: bc18 (pre-fix: 1 distinct gold).
   ADVERSARY: internal-consistency — a degenerate answer key re-entering, or the identity
   change breaking a motif contract.
   REACHES IT VIA: `target_obligation_id()` and every parametrized construction site
   (motif witnesses, catalogs, BC selection, state summaries).
   Attack: W4 motif postconditions against the varied target; SEMANTIC_ID legality of the
   concatenated id; the driver's BEFORE-YOU-ASK §3-A ruling itself (seat 1 had said
   "owner ruling first" — the driver ruled the evidence converged; attack that call).
   **RULING ASK: ACCEPT (⇒ the ruling stands, owner sees it at merge), or CHANGE.**
3. **The motif codebook is MEASURED and DECLARED, not eliminated (FOLD 2c, seat 3's F1).**
   Census cross-tabulates signature→motif; single-motif count pinned at
   `DECLARED_SINGLE_MOTIF_SIGNATURE_RESIDUAL = 3` (15 rows at generation); ONE reshaping
   attempt executed and DISCARDED (moved the tail, 15→8 rows, still 3 signatures);
   design §2.2 carries the number and the discarded attempt. Red banked: bc19.
   ADVERSARY: author-blind-spot — the declaration hiding a live wrong-number channel.
   REACHES IT VIA: `population_census` cross-tab + `DECLARED_SINGLE_MOTIF_SIGNATURE_RESIDUAL`.
   Attack: is the no-cross-scenario-exposure argument (frozen cold-episode subject cannot
   hold population statistics) actually airtight under the r10 design's serving model?
   Is pinning the residual to a constant the right mechanism (any population change flips
   bc19 RED — deliberate, but a maintenance edge)? Would the discarded second option
   (padding to a common count floor) be cheap enough to be the honest close instead?
   **RULING ASK: ACCEPT the declared residual, or CHANGE.**
4. **The plan record cannot overstate what it achieved (FOLD 3).**
   `len(placements) != placed_total` refuses (`BUILD_GENERATION_PLAN_REFUSED`); the
   `-1` derived-axis net is GONE (`BUILD_DERIVED_AXIS_UNRECORDABLE` refuses loud; driver
   verified all four population classes record cleanly at the pin). Red banked: bc20.
   ADVERSARY: internal-consistency — the signed plan overstating the achieved placement,
   or a new refusal wrongly refusing a legitimate population.
   REACHES IT VIA: `generate_cohort` / `_plan_placements` / `_record_derived_axes`.
   Attack: construct a legitimate population shape the new refusals wrongly refuse (the
   ENVELOPE refusal class has ZERO members at this pin — an enumerated, declared gap).
   **RULING ASK: ACCEPT/CHANGE.**
5. **The coverage number now says what it counts (FOLD 4).** Numerator over ALL
   gate-checked program events (150→151); `covered_pair_rule` declared in the record and
   REQUIRED by `sequence_coverage_report_errors` (rider: the report check now also
   requires `target_set_rule`); bc06 recomputes non-mirroring. Red banked: bc21.
   ADVERSARY: internal-consistency — a coverage record whose number does not match its
   own declared rule, or a report check refusing a legitimate record.
   REACHES IT VIA: `sequence_coverage` + the authority report check.
   Attack: is counting DUPLICATE_NOOP pairs the right §2.6 semantics (r1 seats split
   3-ways on severity; the driver ruled with the fix — attack the ruling); does the
   enforced report check refuse any legitimate record?
   **RULING ASK: ACCEPT/CHANGE.**
6. **W14(b)'s difference set is DECLARED, and the witness that guards it works in every
   legitimate layout (FOLD 5 + the clean-room-caught bc14 fix).** `pinned − REQUIRED ⊆
   PIN_MANIFEST_SUBJECTS_BEYOND_REQUIRED` (30 enumerated subjects), stray refused
   `W14_PIN_MANIFEST_SUBJECT_OUTSIDE_DECLARED_SET`; design §3(b) amended to the
   implemented contract; rider: `pin_manifest_document=` injection seam (its red: the
   seam's pre-fix TypeError). And bc14's unpinned-probe file is now the PIN MANIFEST
   itself — the old probe existed only in the work tree, so the witness REFUSED A RIGHT
   RECONSTRUCTION; caught by the first pinned clean-room after it landed (pre-fix red =
   the banked clean-room failure in `cleanroom-postfold.out`'s history at `133209ac`).
   Reds banked: bc17 (stray PASS pre-fix through two injection routes) · the clean-room
   bc14 failure.
   ADVERSARY: maintainer — a future edit un-registering a subject silently, growing the
   allowlist without a declaration, or a witness refusing a right layout.
   REACHES IT VIA: `check_registration_totality` level (b) + `PIN_MANIFEST_SUBJECTS_BEYOND_REQUIRED`.
   Attack: fresh stray shapes; whether the declared set's 30 members are each actually
   deliberate; whether the allowlist can be silently grown (the constant's comment says
   an addition is a DECLARATION — is anything enforcing that beyond review?).
   **RULING ASK: ACCEPT/CHANGE.**

## 5. Red witnesses per closed class

All folds red-first, and **the driver re-ran the reds himself on hash-proven pre-fix
bytes** (bc18-21: 4/4 RED with the import proof printed, `7eb54412…` winning; bc15/16:
worker-run with byte proofs + the driver's own committed R5/R6 reproductions; bc17: probe
outputs banked in the FOLD 5 record; bc14: the clean-room failure itself). Ledger 101
invariants / 236 witnesses, two-way total, in the bundle. New rows BC-20/21/22; appends
to BC-03/BC-11/BC-19; carriers per the bundle's own carrier rule (which caught and
refused the driver's first BC-21 shape — that refusal is in the session record).

## 6. Executable-falsification lane — all seats

- Suites at the pin: `python -m unittest test_mbcx01_build_cohort` (expect **Ran 39 —
  OK**, ~110s) · full discover (expect **548 OK**, ~185s) · `python
  verify-build-bundle.py` (REAL exit 0, several minutes — it re-runs the suites).
- Construct and RUN at least one fresh probe per item you rule on; EXECUTED/READ-ONLY
  labels; a READ-ONLY verdict cannot be the deciding GO; empty probe output = broken
  harness.
- ⛔ No ETW, no Job Objects, no `MBCX01_BUILD_ALLOW_PHYSICAL`, no provider calls, no
  route trials, no spend.

## 7. Omission attack

At least one seat: did any fold make a previously-covered path unreachable or weaken a
pre-existing witness (diff `af1cc4f^..ad713b22` on the test module — every changed
existing witness is a flagged rider; verify the flags are complete)? Is there a fold
surface here whose remedy quietly gates a person rather than a number (the no-adversary
discriminator)? Did the fold arc introduce machinery the r1 round never ordered?

## 8. Non-claims

Unchanged from r1 §8 (#31 residuals · shared-reducer pseudo-oracle · never executed live
· no security posture · enumerated-green semantics) **plus:** the DECLARED single-motif
signature residual (item 3) · the DECLARED admission-path limit (item 1) · the ENVELOPE
refusal class has zero members at this pin (enumerated, not hidden).

## 9. Why this exists (build-decision challenge)

ALREADY-BUILT: every fold reuses validators/census/report machinery the engine already
had; the derivation law MOVED, not duplicated; nothing external adopted; the r1 shelf
logs govern (seats spot-ran the queries, three repos, zero hits).
PRODUCT-FIT: the folds make the instrument refuse evidence it cannot re-derive, stop the
answer key being a constant, and make three records tell the truth about themselves —
fail-loud, mirror-not-cop, no walls. One sentence: the owner needs the 768 scenarios to
measure the hypothesis, not a fixture artifact or a heuristic.
BIGGER-THAN-THE-BUG: the largest fold is one validator call at one boundary plus one
identity-derivation function; no machine.
PRIMARY-CONSUMER: unchanged — the frozen inference core and the owner defending one
number; a bounded read of the census now buys the distinct-gold count, the cross-tab, and
a coverage figure that carries both its set rules.

## 10. Search log (driver's own sweep)

No NEW external prior-art claim is introduced by the folds; the r1 primaries govern
(seat 1 opened the U-CIT constrained-coverage literature; seat 2 opened the NIST SCA
primaries — both banked in the r1 verdicts; both confirm the declared lower-bound
labelling this fold arc kept). UNSEARCHED: NOT-LOAD-BEARING — every item rests on pinned
bytes and the r1 banked primaries.

## 11. Internal-shelf log (driver's own internal sweep)

QUERIES: `sequence coverage` · `covering array` · `stratif(y|ied)` · `census` ·
`retained_set_root` · `membership.substitut` · `cohort` — the r1 packet's seven
problem-shape terms, driver-run at the r1 pin across all three repos (only `census`
matched — live-resource inventories, declined with reasons); the folds introduce no NEW
mechanism shape beyond those terms — the serve-boundary validator and the identity
derivation reuse this lane's own existing functions.
REPOS: agentvault-mcp-bridge (`src/`) · Photon (`crates/`) · Gravity (`src/`) — all
three, covered at r1; no new shape ⇒ no new query set this round.
OPENED: the r1 openings govern (bridge/Gravity/Photon census sites; Photon
`writer_gate.rs`/`store_open.rs` at design r6) — nothing new to open for a fold arc that
adds no new mechanism class.
STOPPED: a confirm round on folds that reuse in-lane machinery; a fresh three-repo sweep
would re-run the r1 queries against unchanged repos.

## 12. Seat SWEEP lane (the seats' own sweep)

SWEEP APPLIES TO: any claim resting on prior art, a standard, or vendor-documented
behaviour — go look with your own queries before you bless or refute it.
DELIVERABLE: a SWEEP LOG in your verdict — exact queries · what you OPENED (URL +
deciding section) · what it changed or confirmed · why you stopped.
LABELS: every prior-art or standards-bearing finding carries exactly one of SEARCHED /
RECALLED / UNSEARCHED (UNSEARCHED carries its reason: NOT-LOAD-BEARING ·
SETTLED-BY-PINNED-BYTES · COULD-NOT · DID-NOT).
CONSEQUENCE: an UNSEARCHED or RECALLED finding cannot be the deciding GO on a claim
resting on prior art or a standard; a round where no seat swept such a claim is
incomplete.
HONEST OUT: if you cannot reach the web this session, say so plainly in one line.

## 13. Re-review trigger

A CHANGE on any item ⇒ fold + fresh confirm. Six ACCEPTs ⇒ the arc advances to the
codex-CLI gate (#1), serialized after this round.

## 14. Driver pre-dispatch execution (run before sending, at the §2 pin)

- Cohort **39/39** · discover **548/548** · bundle REAL exit **0** (101/236 two-way) ·
  clean-room **PINNED RECONSTRUCTION COMPLETE** real exit 0 — all witnessed on these
  bytes this session (`assembly-gates-2026-08-16c.log` · `bundle-postfold.out` ·
  `cleanroom-postfold.out`).
- Driver red re-runs: bc18-21 4/4 RED on hash-proven pre-fix bytes (import proof
  printed); R5/R6 driver-reproduced pre-fold and REFUSED post-fold.
- The bundle's own gates policed the driver twice this arc: the ledger carrier rule
  refused the first BC-21 row shape; the pin-freshness arm refused the pre-regen tree.
  Both refusals were the mechanisms working.
