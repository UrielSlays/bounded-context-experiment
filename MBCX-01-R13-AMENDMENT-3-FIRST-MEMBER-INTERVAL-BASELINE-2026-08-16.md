# MBCX-01 r13.2 — AMENDMENT 3: the first member interval is counted from a per-processor baseline

**Status:** RATIFIED — owner-ruled 2026-08-16 in live chat via the #23 reconciliation sweep, Group B (verbatim: "Anyways, ratify. And then continue."). Implemented on the branch with red
witnesses on the A-1/A-2 pattern; the owner-only merge gate is the ratification surface, and
the veto is a revert of this amendment's commits. Nothing here has run against a live ETW
session; no banked scientific result exists that this could alter.
**AMENDED IN PLACE AT r7 (2026-08-16, three seats convergent — SEAT2 executed the omission
end-to-end through full production admission, wrong by 1,000,000):** the draft's original
"no baseline row at capture-start" shape made an EMPTY baseline set indistinguishable from a
FORGOTTEN one. The draft now carries the **TOTALITY RULE**: the scope emits a baseline row
for EVERY observed processor (capture-start rows carry the first record's own counter, so
their delta stays the declared zero); the frozen validator requires baselined processors to
EQUAL observed processors; and the producer's `cswitch_first_member_baselines` field has NO
default, so an omitting caller faults at construction, before signing. §2's non-claims and
§7's declared residuals were extended the same round.
**Amends:** the frozen r13.2 layer (`mbcx01_r13_measurement.py` — `TRACE_KEYS`, the
`_validate_physical_evidence` delta arithmetic, the fixture trace builder) and the BUILD lane
(`mbcx01_build_etw_consumer.py` scope output, `mbcx01_build_win32.py` delta recomputation,
`mbcx01_build_windows_producer.py` trace construction,
`MBCX-01-MEASUREMENT-CONTRACT-v7.json` trace schema + one false prose sentence). THIRD
amendment to the freeze; AMENDMENT-1 and AMENDMENT-2 stand unchanged beside it.
**Origin:** BUILD acceptance council r6 (2026-08-16), SEAT3 finding 1, EXECUTED — the round's
NO-GO. Reproduced at the byte by the driver on hash-proven pre-fix bytes before this document
was written.

## 1. The defect, plainly

When the machine-wide CSwitch stream is scoped to Job members, the interval that ends at a
processor's FIRST member switch-out is real member work — the member thread was the one
running — but the frozen delta rule hard-codes the first emitted record's delta to zero:

> `mbcx01_r13_measurement.py:1032` (pre-amendment) —
> `expected_delta = 0 if prior is None else observation["counter_value"] - prior`

and the scoping (`scope_cswitch_records_to_members`) discards the foreign predecessor whose
raw counter is the only baseline that interval could be measured against. The magnitude of
the discarded interval is unbounded, the provenance reports `foreign_instructions: 0` for it,
and every validator plus the smoke criterion stays green over the loss.

**Driver reproduction, pre-amendment (frozen bytes hash-proven `eb795387…` = HEAD blob):**

```
stream (one processor): foreign switch-out at raw 100 ·
                        first member switch-out at raw 1,000,100 ·
                        second member switch-out at raw 1,000,200
receipt as the build signs it: deltas [0, 100] · aggregate 100 · retired_instructions 100
_validate_physical_evidence(...) -> []            (ACCEPTED)
true member work proven by the stream: >= 1,000,100
```

The accepted number is wrong by 1,000,000 — **twice the closure architecture's 500,000
boundedness threshold (§7)** — and the boundedness verdict is a max-minus-min DIFFERENCE
across H values, so a per-cell error of this size can flip a carrier's verdict in either
direction. This is the experiment producing a wrong number; it is exactly the class the
no-adversary yardstick exists to stop.

**Why three review rounds and two seats' fresh probes missed it:** the in-stream arithmetic
is CORRECT (verified independently by two seats and the driver — every delta after the first
equals `raw(this) − raw(previous)` with foreign work properly subtracted), and the
first-record rule was a DECLARED undercount inherited from the original contract, where the
discarded interval was capture-start truncation. Scoping silently changed WHICH interval the
rule discards — from "trace start to first switch" to "last pre-member switch to first member
switch-out", which is member work. Declared is not the same as bounded.

## 2. What is NOT claimed

- **No banked result is wrong.** The physical harness has never executed
  (`physical_harness_executed: false`); no measured total exists that this rule ever touched.
- **No estimand, route, inference, cohort or n=768 change.**
- **Not a security finding.** No threat model exists in this lane; this is the instrument
  lying to itself about arithmetic.
- **No new subsystem.** One trace field, seeded arithmetic in the two existing
  recomputations, and the builders that emit the trace. No new machine.
- **The capture-start truncation is retained, now honestly scoped:** a processor whose first
  record EVER is a member switch-out has no predecessor; its first interval remains
  uncounted, declared, and small by construction (trace-start boundary), exactly as the
  original contract intended. Post-r7, that fact is an EXPLICIT observation (a baseline row
  whose counter equals the first record's own), never an absence.
- **Two DECLARED residuals the r7 round priced (SEAT1, both EXECUTED/SEARCHED — declared,
  deliberately not mechanized under the no-adversary law):**
  1. **The baseline is trusted evidence bounded only from above.** A baseline that is too
     HIGH refuses (negative first delta); a baseline that is too LOW inflates the first
     interval and signs — an overcount channel that did not exist when the first delta was
     pinned to zero, and one no receipt-internal check can close (the truth lives in the
     raw stream the receipt does not carry). An overcount concentrated in one cell does not
     cancel in the max-minus-min difference, so this is the direction that can flip a
     boundedness verdict. The producer's baseline arithmetic is therefore load-bearing and
     unverified downstream — every future round should treat it so.
  2. **Interrupt and DPC work is counted as member work.** ISRs, DPCs and the scheduler's
     own tracing run in the context of whatever thread is current and dirty its counters —
     a property of CSwitch-attached PMC measurement itself (practitioner primaries: Bruce
     Dawson's CPU-performance-counters write-up, corroborated by Geoff Chappell in its
     thread and independently at easyperf.net; Microsoft publishes no primary for this
     surface). The magnitude is unknowable until the elevated run and is systematically
     upward. AMENDMENT-3 marginally increases the exposure by counting one more interval
     per processor. The signed number's known contaminant is hereby stated rather than
     silent.

## 3. The change

| File | Change |
|---|---|
| `mbcx01_r13_measurement.py` (FROZEN) | `TRACE_KEYS` gains `cswitch_first_member_baselines`; the field is a list of `{processor, counter_value}` rows (exact keys, non-negative ints, unique processors, every baselined processor must appear among the observations); `_validate_physical_evidence` seeds `previous_by_processor` from the baselines, so the first observation on a baselined processor carries `delta = counter_value − baseline` (negative ⇒ refused by the existing check); the fixture trace builder emits the field |
| `mbcx01_build_etw_consumer.py` | `scope_cswitch_records_to_members` additionally returns, per processor, the offset-consistent raw counter of the record immediately preceding the first member record (absent when the first record on that processor is the member — capture-start) |
| `mbcx01_build_win32.py` | the live delta recomputation seeds `previous_by_processor` from the same baselines |
| `mbcx01_build_windows_producer.py` | the signed trace carries `cswitch_first_member_baselines` |
| `MBCX-01-MEASUREMENT-CONTRACT-v7.json` | trace schema gains the field (required, `additionalProperties: false` row shape); **and the false containment sentence is corrected** — signed membership binds the ETW-published `ProcessSequenceNumber` (the council's item-2 ruling of record; the historical `process_start_key` field-name family is retained deliberately — renaming a signed field to fix prose is the larger change) |
| `test_mbcx01_r13_measurement.py` | new frozen witnesses (§4) |
| `verify-build-bundle.py` | `FROZEN_TEST_TOTAL` moves with its reason recorded at the constant |

## 4. Red witnesses (the contract, not a formality)

Written and run against PRE-FIX bytes loaded from the HEAD blob into a scratch directory at
`sys.path[0]`, module `__file__` and Git blob hash printed and asserted before any red was
trusted.

- **THE RED — `a baselineless undercounting trace is refused`:** the §1 receipt (aggregate
  100 for a stream proving 1,000,100, no baseline field) must fail
  `INSTRUCTION_ACCOUNTING_INCOMPLETE`. **PRE-FIX: it validated `[]` — the banked wrong-number
  acceptance.** POST-FIX: refused (the exact key set does the refusing, which is also the
  migration story: no pre-amendment receipt shape survives, and none exists to migrate).
- **`the truthful receipt is accepted`:** same stream with
  `cswitch_first_member_baselines: [{processor: 0, counter_value: 100}]`, first delta
  1,000,000, aggregate 1,000,100 — accepted. PRE-FIX: refused (unknown key) — RED.
- **`an undercount cannot hide behind a present baseline`:** baseline present, deltas still
  `[0, 100]` — refused (delta mismatch). Post-fix discriminator; trivially green pre-fix via
  the key refusal, recorded as a GUARD, not a red.
- **`capture-start stays a declared truncation`:** a processor with no predecessor carries
  a baseline row whose counter is its OWN first observation, so its first delta is 0 — the
  original trace-start rule, expressed as an explicit observation. ⚠ **Corrected at r8: this
  bullet previously read "empty baseline list — first delta 0 accepted," which described the
  pre-totality draft and is FALSE against the r7 bytes — an empty list beside observations is
  now refused. Two source comments carried the same stale sentence and were corrected in the
  same commit. The seats caught the prose, not the code; the code was right.**
- **`a baseline above the first counter is refused`** (negative interval) and **`a baseline
  for a processor with no observations is refused`** — adversarial shape witnesses.

(Executed transcripts land in the amendment fold's commit alongside this document; gate
results in §5.)

## 5. Gates

Recorded at the amendment fold's commit — BUILD suite, frozen suite (new
`FROZEN_TEST_TOTAL`), `verify-build-bundle.py` real exit 0, pin manifest regenerated. A
future reader who finds `FROZEN_TEST_TOTAL` moved should expect this document beside it,
exactly as AMENDMENT-1 and AMENDMENT-2 established.

## 6. Re-review

This amends the frozen layer's arithmetic — the amended bytes go back to the council (r7)
with the other r6 folds before the codex-CLI gate, per the r6 packet's §13 trigger.
