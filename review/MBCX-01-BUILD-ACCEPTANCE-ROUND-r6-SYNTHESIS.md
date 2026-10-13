# MBCX-01 BUILD acceptance round r6 — synthesis

Round complete at **3/3, every verdict EXECUTED**. Third complete round in this lane, first on
the folded tree (issue #24). Packet `b56892e`; review target `396752a`.

| Seat | Verdict | First-order shape |
|---|---|---|
| SEAT1 Opus 5 | GO-WITH-FIXES(SMOKE-PREFLIGHT-NODE · LIVE-PATH-TID-REUSE-PROVENANCE · CONTRACT-SEMANTIC-RIPPLE · LEDGER-NAME-COVERAGE) | two false-refusals + two records gaps; all 7 rulings answered |
| SEAT2 ChatGPT sol | GO-WITH-FIXES(ETW_CSWITCH_SCOPE_TID_REUSE_DISAMBIGUATION + ETW_THREAD_EVENT_VERSION_GATE + SMOKE_PER_RECEIPT_SEMANTIC_VALIDATION) | one false-refusal + two wrong-evidence admissions; all 7 rulings answered |
| SEAT3 codex-exec | **NO-GO** | an EXECUTED wrong-number: the build signs 100 retired instructions when the stream proves 1,000,100 |

**Outcome: NO-GO governs until the folds land.** Every finding below that enters a fold was
REPRODUCED BY THE DRIVER at the byte before it was written here (probe transcripts in this
session's record; the seat-3 headline reproduced with the scope's own dataclass:
kept `[1000100, 1000200]`, `excluded: 1`, `foreign_instructions: 0`, `baseline_records: 1` ⇒
downstream aggregate 100 against true member work 1,000,100).

## Convergence (as strong a signal as disagreement)

- **TID-reuse in the CSwitch scope** — ALL THREE seats, independently, each EXECUTED: the
  scoper keeps any roster-TID row regardless of QPC (`:1855`), then `consume_cswitch` faults
  `ETW_CSWITCH_UNATTRIBUTED_THREAD` and the whole capture dies on an ordinary Windows reuse
  event. Driver-reproduced (kept qpcs `[11, 90]` for a lifetime `[10,40]`).
- **The smoke conjunction's first half is too weak** — SEAT2 (membership_complete=False) and
  SEAT3 (tampered retired_instructions) executed the SAME class through different fields: a
  re-signed, semantically-invalid receipt passes smoke while the harness's own full validator
  refuses it. Two different instances of one class — stronger than either alone.
- **Node preflight** — SEAT1 and SEAT3 independently executed the missing-`node` failure; the
  one-shot elevated session would be burned by a PATH difference.
- **Stale prose naming ProcessStartKey** — SEAT1 (contract v7 `:42` + issue #12 text) and
  SEAT3 (contract + open-issues row) converge; driver byte-confirmed the sentence.

## Conflicts, adjudicated at the byte — named winners

1. **Item 1, the signed accumulator (SEAT1 ACCEPT · SEAT2 ACCEPT · SEAT3 CHANGE).** Both are
   right about different things, and the split resolves without averaging: the ACCEPTs hold
   for the IN-STREAM arithmetic (driver + both seats verified delta = raw(this) − raw(prev)
   with foreign intervals correctly subtracted — the accumulator is the only true reading of
   the one existing slot); SEAT3's CHANGE holds for the FIRST-MEMBER-INTERVAL DISCARD, an axis
   neither ACCEPT seat varied. SEAT3 constructed and RAN it; the driver reproduced it: the
   discarded interval is real member work of unbounded magnitude (1,000,000 in the probe,
   twice the §3.6 threshold), invisible to provenance (`foreign_instructions: 0`), and every
   validator plus smoke stays green over it. **A constructed executed bypass outranks any
   number of passes that never aimed at it (the #368 rule). SEAT3 governs: the undercount is
   a wrong-number defect.** Because the frozen delta rule hard-codes first-record = 0, the
   fix is a FROZEN-LAYER change — **AMENDMENT-3**, drafted this arc, owner ratifies (the
   merge gate is the ratification surface; the amendment doc says so on its face).
   ⚠ SEAT2's "F1 is a scope-classification defect, not evidence the signed field needs a
   raw-counter slot" is NOT overruled — it was answering the TID-reuse finding, not this one;
   SEAT2's own residual list carries the first-interval discard as an undercount it did not
   further probe.
2. **TID-reuse remedy (SEAT1: provenance counter only · SEAT2/SEAT3: lifetime-aware scope).**
   SEAT1's premise — "the two cases are indistinguishable from inside the stream" — is
   FALSIFIED for the known-reuse case by SEAT2's executed construction:
   `partition_job_member_events()` already separates the foreign incarnation's lifetime; the
   scope simply never consumes that evidence. Using an already-derived fact where it is
   needed is not new machinery. **SEAT2's remedy governs**, composed with SEAT1's counter:
   member-containment ⇒ member; known-foreign-containment ⇒ excluded/baseline;
   roster-TID outside BOTH ⇒ keep the fail-loud fault AND count it in provenance (SEAT1's
   counter, for the case that genuinely is ambiguous).
3. **Item 2 spelling (SEAT1/SEAT2 ACCEPT-keep-spelling · SEAT3 CHANGE-rename).** 2-v-1 and
   the merits agree: renaming a signed field family to fix prose is the larger change; the
   auditor-misled harm is discharged by correcting the false SENTENCE (contract v7 `:42`) and
   the #12 issue text. **Keep the spelling; fix the prose — SEAT1/SEAT2 govern.** SEAT3's
   concern survives as the nomenclature-debt residual SEAT2 named.
4. **Item 7 receipt slot (SEAT1/SEAT2 ACCEPT-residual · SEAT3 CHANGE-amend-now).** SEAT2
   executed the discriminating probe: materially different foreign-exclusion histories yield
   the identical signed member number — the counts are diagnostics, not scientific evidence.
   **ACCEPT as named residual (SEAT1/SEAT2 govern)**; the part of SEAT3's concern that was
   load-bearing (arithmetic invisibility) is answered by AMENDMENT-3's baseline evidence, not
   by a diagnostics slot. F5's denominator fix and the F1 provenance counter land first.

## The seven rulings of record (settled by the round)

1. Accumulator semantics ACCEPTED; first-interval undercount → **AMENDMENT-3** (owner
   ratifies).
2. ProcessSequenceNumber as root identity ACCEPTED, spelling retained; contract v7 sentence +
   issue #12 text corrected (the sentence correction rides AMENDMENT-3's document — it is
   frozen-layer prose).
3. **No writer door** — SQLite serialization + in-transaction allocation + unique index,
   confirmed by two independent multi-process executions (SEAT2: three processes, sequences
   `[1,2,3]`). #25 (raw OperationalError escape) stays the honest completion — tracked, red
   owed there.
4. All six AMENDMENT-2 judgment calls **ACCEPTED** as built. No new witness owed on (3) —
   the INCOMPLETE name is already pinned (`test_mbcx01_build_measurement.py:3013-3017`,
   driver-confirmed); a repair-ledger ROW for the name is owed instead (SEAT1 F4,
   driver-confirmed absent).
5. Fixture-key gaps: (1) ACCEPT-residual · (2) **already closed at the bytes** —
   `PRODUCTION_SIGNING_KEY_FIXTURE_MATERIAL` exists and is pinned
   (`mbcx01_build_measurement_authority.py:375`, test `:1749`, driver-confirmed; issue #14
   text corrected) · (3) ACCEPT-residual (raise-channel asymmetry noted; optional leaf catch
   is the owner's call, not blocking).
6. Smoke conjunction ACCEPTED with its first half strengthened: independent validity =
   structure + signature + **the existing per-receipt semantic validator** (SEAT2 executed
   the positive control — no false refusal introduced) + `node`/verifier preflight before any
   elevated run + persist-raw-evidence-before-sign (SEAT3 F5).
7. Exclusion counts: ACCEPT as named diagnostic residual (see conflict 4).

## Driver defects this round (recorded, not hidden)

- The packet carried TWO stale claims inherited from issue text written before the codex
  folds: "no banked test asserts ETW_THREAD_LIFETIME_INCOMPLETE" (false — it was pinned in
  the codex arc) and #14's framing of gap (2) as open (false — closed by name in the codex
  arc). Two seats caught both. Inheriting an issue body without re-checking it against the
  current bytes is the same class as inheriting a packet premise — the issues get corrected
  and #16 gets a note.
- SEAT1 flagged the SQLite citation's applicability gap on its own (locking page describes
  rollback mode; the store pins WAL) — carried into the fold as a to-verify note, not a
  blocker (SEAT2's three-process execution ran against the real store path).

## Fold plan (red-first, disjoint files, driver assembles and re-gates)

- **FOLD-A (`mbcx01_build_etw_consumer.py` + measurement tests):** lifetime-aware CSwitch
  scope + ambiguous-keep provenance counter; thread-event version gate consuming
  `KERNEL_THREAD_PAYLOAD_VERSIONS_VERIFIED`; provenance denominator naming (F5).
- **FOLD-B (`mbcx01_smoke_cell.py` + tests):** per-receipt semantic validation in the
  independent-valid half (grid/admission-policy checks excluded); `node` + verifier-script
  preflight probes; persist-raw-evidence-before-sign ordering.
- **AMENDMENT-3 (driver, frozen layer):** per-processor baseline evidence + first-member-
  interval accounting in both recomputations; contract v7 containment-sentence correction;
  `FROZEN_TEST_TOTAL` moves with its reason; **status DRAFTED — OWNER RATIFICATION PENDING,
  veto = revert**. Red witnesses: pre-fix signs 100 for a proven 1,000,100; capture-start
  (no predecessor) stays delta-0 and declared; baseline-mismatched receipt refused by name.
- **Records:** ledger row for the INCOMPLETE name; issues #8, #14 closed with rulings;
  #12/#16/#24/#25 updated.

Per packet §13, FOLD-A changes admission semantics and AMENDMENT-3 changes frozen semantics
⇒ the folded bytes come back to a fresh round (r7) before codex-CLI r4.
