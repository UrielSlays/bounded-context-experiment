# MBCX-01 BUILD acceptance round r7 — synthesis

Round complete at **3/3, every verdict EXECUTED**. Fourth complete round; first on the r6
folds + AMENDMENT-3. Packet `cbab20b`; review target `abcab342`.

| Seat | Verdict |
|---|---|
| SEAT1 Opus 5 | GO-WITH-FIXES(AMENDMENT-3-BASELINE-TOTALITY · SMOKE-VERIFIER-PREFLIGHT · SPAWN-FENCE-SHAPE · UNCOUNTED-INTERRUPT-WORK-NONCLAIM) |
| SEAT2 ChatGPT sol | NO-GO |
| SEAT3 codex-exec | NO-GO |

**Outcome: NO-GO governs; fold + fresh targeted round (r8) per the packet's own §13** — the
item-1 and item-2(a) rulings are CHANGEs.

## Three-seat convergence (both real classes, three independent executions each)

1. **A missing baseline is indistinguishable from a true capture-start, and it signs the old
   undercount.** SEAT3 executed it at the producer default; SEAT1 executed it at the frozen
   validator (empty list accepted, total 200 for a ground truth of 700); SEAT2 executed it
   END TO END — the old caller shape signed, entered an otherwise-valid 100-cell grid, and
   cleared FULL PRODUCTION ADMISSION with zero errors, wrong by 1,000,000. The packet's own
   §7 asked exactly this question; the answer is a CHANGE to the AMENDMENT-3 draft.
   **Remedy of record (SEAT1's totality rule + SEAT2/SEAT3's required boundary, composed):**
   (a) the scope emits a baseline row for EVERY processor at its first kept record —
   `prior` when a predecessor exists, the record's own raw when capture-start (its delta
   stays the declared 0; no number moves); (b) the frozen validator's `baselined ⊆ observed`
   tightens to `==`, making an empty-but-forgotten baseline set unrepresentable whenever
   observations exist; (c) `SimulatedCollection.cswitch_first_member_baselines` loses its
   default — an omitting caller faults at construction, before signing. SEAT1's false-refusal
   check holds: a processor with observations always has a first kept record, so a row can
   always be emitted and `==` cannot refuse a truthful capture.
2. **The pwsh fence allowance is substring-matchable.** Three seats, three different bypass
   argvs, all accepted by the fence's own `check()`. Remedy: match the launcher's REAL argv
   shape (the exact bw86 invocation), not a filename substring anywhere in the parts.

## Conflicts, adjudicated at the byte — named winners

- **Stop-only foreign lifetime (item 2a): SEAT2 CHANGE governs.** SEAT2 executed a
  reachable false refusal (a host thread that predates the trace stops at QPC 50; the
  MEMBER later receives the recycled TID; the pre-existing thread's switch at QPC 40 is
  unplaceable and the capture aborts) and grounded the disambiguation in Microsoft primaries
  (a TID is unique while live; reuse only after termination; the platform itself models
  pre-existing threads via data-collection-start events). SEAT1 independently proposed the
  SAME fix as its named alternative ("the lower bound is known, not guessed... bundle it
  with item 1's fold"), and a fold is happening. SEAT3's ACCEPT rested on conservatism that
  the executed shape falsifies — the record is not ambiguous, and the refusal costs the
  one-shot session. **Remedy: a leading foreign STOP with no observed START yields a
  capture-prefix interval through its stop.** It can never move member work out — the member
  branch wins containment, and the member's own lifetime begins after the foreign stop by
  the OS's own reuse rule.
- **⚠ WITHDRAWN BY ITS OWN SEAT AT r8 — SEAT1 F6.** At r8 SEAT1 re-read the bytes,
  confirmed `signature_verifier_facts()` has been called from `preflight` since the r6 fold,
  and withdrew this finding on the record: *"My r7 probe ran only `node_runtime_facts()` and
  my grep window stopped 35 lines short of its sibling; I inferred absence from one
  function's output."* The adjudication below stands unchanged and is now confirmed by the
  seat that raised it. Recorded here so the banked r7 verdict does not carry a live
  phantom residual.
- **Verifier preflight (SEAT1 F6): FALSIFIED AT THE BYTE — no fold.**
  `mbcx01_smoke_cell.preflight` :271-272 calls `node_runtime_facts()` AND
  `signature_verifier_facts()` and aborts `SIGNATURE_VERIFIER_TOOLCHAIN_UNAVAILABLE` when
  either half is missing (`["signature_verifier"]["present"]` is in the abort condition).
  SEAT2's executed 4(c) confirms; the driver re-read the bytes. Named winner: SEAT2 + the
  bytes. SEAT1's probe harness examined something other than the current preflight.
- **F3 (baseline unverifiable downward) and F4 (interrupt/DPC contamination), SEAT1:**
  ACCEPTED as DECLARE-not-fix — both land in the AMENDMENT-3 document as named residuals
  and in the next packet's non-claims. F4 carries SEAT1's practitioner primary (Dawson;
  corroborated twice) for the CSwitch-attached PMC model itself — the same source that
  independently confirms the amendment's arithmetic. No mechanism is built for either
  (no-adversary law: the honest move is the named residual).
- **F7 (raw KeyError for an intervalless roster row at `resolve_thread_lifetime`):** leaf
  fold — named fault, posture unchanged.
- **Ruling-3 residual (SEAT1 + SEAT2 concur):** the thread-event version gate cannot be
  preflighted; the runbook gains the fired-gate procedure (record the version → verify
  offsets via TDH → extend the verified set → re-round).

## Also settled this round

- AMENDMENT-3's ARITHMETIC is confirmed by all three seats (two independent oracles matched;
  SEAT1 opened the practitioner primary for the per-CPU delta model). The CHANGE is to the
  boundary, not the math.
- bw83's corrected expectation `[500, 200, 0, 50]` ACCEPTED 3/3, verified from raw counters.
- The version gate, all four smoke calls, roster fallback (2b), foreign backwards check
  (2c), ambiguous counter (2d, conditional on 2a), and the `node.exe` fence allowance:
  ACCEPTED.
- SEAT3's r7 promptfile pointed at the WRONG pin (my patch silently no-opped and I never
  grepped the output — the third instance of the silent-no-op class this lane has paid for,
  this one mine). The seat resolved correctly via the packet bytes. Recorded on #16's class.
- SEAT3's WPR note adopted as a future differential-oracle option (no build).

## Fold plan (r7 → r8)

1. Baseline totality + `==` + required producer field + witnesses (frozen + BUILD).
2. Stop-only foreign prefix interval + SEAT2's exact shape as the red witness.
3. pwsh fence exact argv shape + the three bypass argvs as refusal probes.
4. F7 named fault.
5. AMENDMENT-3 doc: totality rule folded in; F3/F4 declared as residuals; ratification ask
   (#27) updated to the amended draft.
6. Runbook: version-gate-fired procedure.
7. Ledger rows; pin manifest; full gates; then the r8 targeted confirm round; then codex r4.
