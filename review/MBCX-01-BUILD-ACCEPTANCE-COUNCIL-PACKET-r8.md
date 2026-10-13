# MBCX-01 BUILD acceptance council packet — r8 (targeted confirm: the r7 folds only)

Packet prose is a pointer map, not evidence — byte-check it.

ROUND LEDGER: council round 8 (r1: NO-GO/NO-GO/GO-WITH-FIXES · r2: 3× GO-WITH-FIXES · r3: INCOMPLETE 2/3 · r4: NO-GO/NO-GO/GO-WITH-FIXES, folded · r5: GO-WITH-FIXES/NO-GO/NO-GO, folded · r6: GO-WITH-FIXES/GO-WITH-FIXES/NO-GO, folded · r7: GO-WITH-FIXES/NO-GO/NO-GO, all EXECUTED, folded — this round confirms those folds and NOTHING else) · codex rounds 3 of 2 — a code lane; codex r4 to literal green follows a clean confirm (#1).

## 0. The one thing this round is for

**NORTH STAR unchanged: the numbers this instrument produces must be true.** No threat model
exists (the settling grep is in the r7 packet §0; driver re-ran it at this pin: zero hits).
A finding counts iff it names its wrong-number / wrong-admission / wrong-refusal consequence.
⛔ No new machines. **This is a CONFIRM round, deliberately narrow:** the four r7 fold
surfaces below and nothing else. Every other surface carries two to four EXECUTED rulings
from r6/r7 and is settled; re-litigating settled ground spends the round the folds need.
The convergence signature to watch for: findings flipping from "add X" to "delete X /
already right", seats describing the same fixed point, an empty omission attack.

## 1. Verdict contract

First line: **GO / GO-WITH-FIXES(class) / NO-GO**. Code artifact — no round-call token, skip
the design questions. Evidence read (`path:line`), SWEEP LOG, findings labelled
EXECUTED/READ-ONLY with data consequences, a RULING per item (ACCEPT / CHANGE + one line),
residual risks, fix class. Whole verdict in-thread.

## 2. Canonical bytes (path@sha pins)

Governing content commit under review: **`575fb38baf331fe8acd721c05848d59251e9c710`** (its
records successor adds only the regenerated pin manifest; resolve HEAD live and confirm
`git diff --stat 575fb38 HEAD -- '*.py'` is empty). The r7 fold arc since r7's pin
`abcab342`: one fold commit + the manifest records commit. r7 record set:
`MBCX-01-BUILD-ACCEPTANCE-ROUND-r7-SYNTHESIS.md` · the three r7 seat verdicts · the amended
`MBCX-01-R13-AMENDMENT-3-FIRST-MEMBER-INTERVAL-BASELINE-2026-08-16.md` (ratification #27).

## 3. Immutable truths / invariants

Unchanged from r7 §3 (frozen-except-amendments · matrix rule · authority modes · readiness ·
fail-loud constants · the §7 boundedness DIFFERENCE). Frozen suite now 156 (reason at
`FROZEN_TEST_TOTAL`). AMENDMENT-3 remains ratification-pending; a defect found now is still
the cheap kind.

## 4. Claims to attack — the four r7 fold surfaces, each with a RULING ask

1. **The totality rule closes the empty-vs-forgotten ambiguity without a false refusal.**
   ADVERSARY: internal-consistency — a truthful capture refused, or a forgotten field still
   signing.
   REACHES IT VIA: the scoped stream, the producer boundary, and the frozen validator.
   Bytes: the scope's unconditional baseline row (capture-start rows carry the first
   record's own counter) · `mbcx01_r13_measurement.py` `baselined != observed ⇒ refuse` ·
   `SimulatedCollection.cswitch_first_member_baselines` REQUIRED (no default) ·
   witnesses bw88 (updated), bw90, the frozen empty-set adversarial, the frozen
   capture-start positive (updated). Attack: construct a truthful capture the `==` rule
   refuses (the r7 seats' false-refusal check says none exists — break it); construct a
   forgotten-field path that still signs; check every remaining `SimulatedCollection`
   constructor passes real evidence rather than a pacifier `()`.
   **RULING ASK: ACCEPT the totality rule as the AMENDMENT-3 shape of record (⇒ recommend
   #27 ratification of the amended draft), or CHANGE.**
2. **The stop-only prefix interval excludes only what it should.**
   ADVERSARY: internal-consistency — member work moved out, or a false refusal surviving.
   REACHES IT VIA: `foreign_thread_intervals` (leading STOP ⇒ `(0, stop_qpc)`, first
   leading stop only).
   Witness bw91 (SEAT2's executed r7 shape). Attack: construct a stream where the prefix
   interval swallows MEMBER work (the member branch wins containment first — falsify that);
   a pathological multi-stop prefix; interaction with `ETW_THREAD_LIFETIME_*` faults
   downstream. **RULING ASK: ACCEPT/CHANGE.**
3. **The exact pwsh fence shape is exact — and still admits the real witness.**
   ADVERSARY: maintainer — the no-execution fence widened or silently broken.
   REACHES IT VIA: `verify-build-bundle.py` `check()` (5-part argv + payload regex).
   Driver probe banked: the real bw86 shape PERMITTED; the four r7 bypass argvs REFUSED.
   Attack with fresh argvs of your own. **RULING ASK: ACCEPT/CHANGE.**
4. **The residual declarations say what they must and no more.**
   ADVERSARY: author-blind-spot — a residual mis-stated, or a third one still unnamed.
   REACHES IT VIA: the amended AMENDMENT-3 §2 (baseline bounded only from above;
   interrupt/DPC contamination) · the runbook's fired-version-gate procedure · the F7 named
   roster fault. **RULING ASK: ACCEPT the declarations as written, or name the defect.**

## 5. Red witnesses per closed class

r7 folds red-first: the frozen empty-set adversarial (RED pre-fold under `⊆` — SEAT1's
executed case B is the banked pre-fix acceptance), bw90 (the omitting caller — SEAT2's
end-to-end probe is the banked pre-fix acceptance), bw91 (SEAT2's exact executed shape —
pre-fold the capture aborted), the fence probes (driver-banked: four bypasses accepted
pre-fold by the seats' own executions, refused post-fold). Ledger 73/188 two-way.

## 6. Executable-falsification lane — all seats

- BUILD suites (expect **188 OK**) · frozen `test_mbcx01_r13_*` (expect **156 OK**) ·
  `python verify-build-bundle.py` (REAL exit 0).
- Construct and RUN at least one fresh probe per item. EXECUTED/READ-ONLY labels; a
  READ-ONLY verdict cannot be the deciding GO. Empty probe output = broken harness.
- ⛔ No ETW session, no Job Object, no `MBCX01_BUILD_ALLOW_PHYSICAL`, no
  `run-smoke-cell.ps1 -Execute` beyond bw86's own no-node shape.

## 7. Omission attack

At least one seat: did any r7 fold make a previously-covered path unreachable, weaken a
pre-existing witness, or leave a third baseline-trust residual unnamed? Is there a
`SimulatedCollection` or session constructor anywhere that now passes a synthetic `()` just
to satisfy the required field (a pacifier — the omission shape wearing a compliance
costume)?

## 8. Non-claims

Unchanged from r7 §8 (never executed live · no security boundary · exactness runner unbuilt
· enumerated-set green · tracked opens #25 #3 #17–#23 #26 #27) **plus the two AMENDMENT-3
declared residuals** (baseline bounded only from above; interrupt/DPC contamination —
systematically upward, unknowable until the elevated run).

## 9. Why this exists (build-decision challenge)

ALREADY-BUILT: every r7 fold consumes evidence the harness already derives; nothing external
adopted; the three-repo shelf remains empty for this shape (r7 seats re-ran the queries).
PRODUCT-FIT: the folds delete an ambiguity (totality), delete a false refusal (prefix
interval), and narrow a fence — fail-loud, mirror-not-cop, no walls. One sentence: the owner
needs the one elevated session to produce a number whose supporting evidence cannot be
silently incomplete.
BIGGER-THAN-THE-BUG: the largest fold is one unconditional row plus one `==`; no machine.
PRIMARY-CONSUMER: unchanged — the inference layer and the owner defending one number; a
bounded receipt read now buys a baseline set that is provably total over observed
processors.

## 10. Search log (driver's own sweep)

No NEW prior-art claim is introduced by this confirm round; the r7 primaries govern (TID
reuse/PsGetThreadId, EVENT_DESCRIPTOR versioning, the CSwitch-attached PMC practitioner
sources now cited inside the amendment). UNSEARCHED: NOT-LOAD-BEARING — every item rests on
our own bytes and the r7 banked primaries.

## 11. Internal-shelf log (driver's own internal sweep)

QUERIES: `first_member_baseline` · `baseline_counter` · `prefix.interval` · `TracePmc` ·
`InstructionRetired` (one alternation grep over the five terms, driver-run 2026-08-16
AFTER the r7 folds landed — not carried from r7)
REPOS: agentvault-mcp-bridge (`src/`) · Photon (`crates/`) · Gravity (`src/`) — all three.
OPENED: the sweep returned ZERO files in all three repos, so there was nothing to open —
the receipt is the query set above plus the three empty result sets; this matches the r7
seats' independent same-day runs of the overlapping query set (banked in their verdicts).
The fold surfaces refine one-of-kind code (the r6-adopted scope/validator pair) whose only
sibling candidates were already opened and declined with reasons at r6 (Photon
`writer_gate.rs` / `store_open.rs` — different problem, ruling ratified r6 item 3).
STOPPED: five problem-shape terms, three repos, zero hits, and the prior rounds' openings
already adjudicated the nearest non-matches — a further pass would re-read known misses.

## 12. Seat SWEEP lane (the seats' own sweep)

SWEEP APPLIES TO: any claim resting on prior art, a standard, or vendor-documented
behaviour — go look with your own queries before you bless or refute it.
DELIVERABLE: a SWEEP LOG in your verdict — exact queries · what you OPENED (URL + deciding
section) · what it changed or confirmed · why you stopped.
LABELS: every prior-art or standards-bearing finding carries exactly one of SEARCHED /
RECALLED / UNSEARCHED (UNSEARCHED carries its reason: NOT-LOAD-BEARING ·
SETTLED-BY-PINNED-BYTES · COULD-NOT · DID-NOT).
CONSEQUENCE: an UNSEARCHED or RECALLED finding cannot be the deciding GO on a claim resting
on prior art or a standard; a round where no seat swept such a claim is incomplete.
HONEST OUT: if you cannot reach the web this session, say so plainly in one line.

## 13. Re-review trigger

A CHANGE on any of the four items ⇒ fold + fresh confirm. Four ACCEPTs ⇒ this arc advances
to the codex-CLI r4 gate (#1), and the round's verdicts ride issue #27's ratification ask.

## 14. Driver pre-dispatch execution (run before sending, at the §2 pin)

- BUILD **188/188 OK, exit 0** · frozen **156/156 OK, exit 0** · `verify-build-bundle.py`
  REAL exit **0** (73/188 two-way) · clean-room at `575fb38…`/`c4442ae1…` →
  `PINNED RECONSTRUCTION COMPLETE`, real exit 0 — witnessed on these bytes this session.
- The fence probe matrix driver-executed (real shape permitted, four bypasses refused).
- bw91's shape is SEAT2's own executed construction; the totality false-refusal check is
  SEAT1's own; this round exists to let the seats confirm their remedies landed as ordered
  — the driver checking his own fold of their findings is the blind spot you cover.
