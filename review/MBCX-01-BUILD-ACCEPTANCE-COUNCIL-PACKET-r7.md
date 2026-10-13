# MBCX-01 BUILD acceptance council packet — r7 (the r6 folds + AMENDMENT-3, on the folded bytes)

Packet prose is a pointer map, not evidence — byte-check it.

ROUND LEDGER: council round 7 (r1: NO-GO/NO-GO/GO-WITH-FIXES · r2: 3× GO-WITH-FIXES · r3: INCOMPLETE 2/3 · r4: NO-GO/NO-GO/GO-WITH-FIXES, folded · r5: GO-WITH-FIXES/NO-GO/NO-GO, folded · r6: GO-WITH-FIXES/GO-WITH-FIXES/NO-GO, all EXECUTED, folded — this round reviews those folds) · codex rounds 3 of 2 — a code lane; the cap governs docs-only diffs; codex r4 to literal green follows this round (#1).

## 0. The one thing this round is for

**NORTH STAR: the numbers this instrument produces must be true.** MBCX-01 is a measurement
harness for a scientific experiment. No network service, no production runtime, no external
submitter; every caller is the harness and its own tests. The design of record carries **no
threat model** — verify in one command from the repository root:

```
grep -niE "threat model|adversary|attacker|untrusted|api-caller|hostile" \
  MBCX-01-EXPERIMENT-DESIGN-r9.md MBCX-01-R13-CLOSURE-ARCHITECTURE.md \
  MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md
```

(Zero hits — driver re-verified at the §2 pin.)

⛔⛔ **THE FILTER, unchanged and enforced:** a finding counts iff you can name how it makes
the experiment **produce a wrong number, admit wrong evidence, or refuse right evidence** —
state that consequence on every finding. Actor-evasion hardening is out of model and will be
ruled out. ⛔ No new machines/subsystems; a fix bigger than its defect stops at the owner.

This is a TARGETED re-round: r6's folds changed admission semantics (the CSwitch scope) and
frozen semantics (AMENDMENT-3), which is exactly the r6 packet's §13 trigger. Attack the
folds; the surfaces r6 ruled and left unchanged are settled unless a fold moved them.

## 1. Verdict contract

First line: **GO / GO-WITH-FIXES(class) / NO-GO**. Code artifact — no round-call token, skip
the two design questions. Then: evidence read (`path:line`), SWEEP LOG, findings labelled
EXECUTED or READ-ONLY each with its data consequence, explicit rulings on the items below
(ACCEPT / CHANGE + one line), residual risks, fix class. Whole verdict in-thread.

## 2. Canonical bytes (path@sha pins)

Governing content commit under review: **`abcab342802be20ba0bb15652c54340d4dededd4`** (its
records successor `98a4af4…` adds only the regenerated pin manifest, whose `governing_commit`
names `abcab342…`; equal to origin at dispatch). The fold arc since r6's pin `396752a`:
- `0d1a6a7` — the r6 folds + AMENDMENT-3 (the content commit; full map in its message and in
  `MBCX-01-BUILD-ACCEPTANCE-ROUND-r6-SYNTHESIS.md`).
- two spawn-fence shape fixes on `verify-build-bundle.py` (node.exe; the pwsh bw86 launcher
  shape — §4 item 6).

Governing design: the invariant matrix · design r9 · closure architecture · AMENDMENT-1 ·
AMENDMENT-2 · **AMENDMENT-3 (`MBCX-01-R13-AMENDMENT-3-FIRST-MEMBER-INTERVAL-BASELINE-2026-08-16.md`,
status DRAFTED — OWNER RATIFICATION PENDING at the merge gate; ratification tracked as issue
#27)**.

Ledger: `MBCX-01-BUILD-REPAIR-LEDGER.json` — 72 invariants / 186 witnesses, `two_way_total`.

## 3. Immutable truths / invariants

1. The r13.2 design is frozen except where the three amendments moved it. AMENDMENT-3 is
   implemented but NOT yet owner-ratified — a finding that it is WRONG is a finding against
   an unratified draft, maximally cheap to act on now. The frozen suite must stay green (155,
   reason at `FROZEN_TEST_TOTAL`).
2. The matrix rule §1; §3 authority modes; readiness
   `BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`; unverifiable platform constants
   fault loudly. All unchanged.
3. Closure-architecture §7: the physical claim is max-minus-min retired instructions across H
   per (D,F) against 500,000 — an attribution or arithmetic error can flip the experiment's
   answer. Judge every finding against that.

## 4. Claims to attack (construct-the-bypass) — each ends in a RULING ask

1. **AMENDMENT-3's arithmetic is now TRUE — and complete.**
   ADVERSARY: internal-consistency — the amended delta rule producing a wrong member total in
   either direction.
   REACHES IT VIA: the scoped CSwitch stream and the two recomputations.
   Bytes: `mbcx01_build_etw_consumer.py` (`CswitchMemberScope.first_member_baselines`, the
   capture at the first-kept-record branch), `mbcx01_build_win32.py`
   (`consume_cswitch` seeding + `ETW_CSWITCH_BASELINE_INVALID`),
   `mbcx01_r13_measurement.py` (`TRACE_KEYS`, baseline validation + seeding + the
   baselined⊆observed check), `mbcx01_build_windows_producer.py` (trace field),
   `MBCX-01-MEASUREMENT-CONTRACT-v7.json` (schema + corrected containment sentence).
   Witnesses: BUILD bw87–bw89; frozen `test_i12` baseline family (RED transcripts banked in
   the amendment doc §4 — the headline pre-fix RED: aggregate 100 validated `[]` where the
   stream proved 1,000,100).
   Attack: construct a stream where the baseline-seeded arithmetic still under- or
   over-counts member work (multi-processor, foreign work straddling the first member record,
   baseline interacting with the foreign-offset subtraction, backwards raw counters across
   the baseline boundary); attack the frozen validation's shape rules (duplicate/orphan/
   negative baselines); attack the migration story (the old shape must be unrepresentable).
   **RULING ASK: is AMENDMENT-3 correct and sufficient as drafted — ACCEPT (recommend owner
   ratification) or CHANGE (name the defect now, while it is a draft)?**
2. **The lifetime-aware scope refuses only what it should.**
   ADVERSARY: internal-consistency — a capture aborted or a record misclassified by the new
   containment rules.
   REACHES IT VIA: the machine-wide CSwitch + process/thread streams.
   Bytes: `scope_cswitch_records_to_members` + `foreign_thread_intervals` +
   `_lifetime_contains`; witnesses bw75/bw76. Four builder judgment calls the round must rule
   rather than inherit: (a) a foreign ThreadStop with NO observed START yields no interval —
   such a record stays ambiguous/counted rather than excluded on a guessed start
   (conservative: can leave a record ambiguous, can never move member work out); (b) a roster
   row with no interval covers the whole capture (the pre-fold TID-only behavior; production
   rosters always carry both ends); (c) a newly-foreign record now takes the foreign branch's
   backwards-counter check (`ETW_PMC_COUNTER_WENT_BACKWARDS` where it was previously kept);
   (d) `kept_roster_tid_outside_any_lifetime` counts the residual ambiguous case.
   **RULING ASK: four explicit ACCEPT/CHANGE calls.**
3. **The thread-event version gate faults only what it should.**
   ADVERSARY: internal-consistency — an unverified layout decoded, or a verified one refused.
   REACHES IT VIA: the ThreadStart/ThreadStop decode branch.
   Bytes: the gate consuming `KERNEL_THREAD_PAYLOAD_VERSIONS_VERIFIED`;
   `ETW_KERNEL_THREAD_VERSION_UNVERIFIED`; witnesses bw77/bw78. Judgment call: a FUTURE real
   Windows thread-event version now aborts the capture by name rather than decoding at
   unverified offsets — the ordered fail-loud posture, and a new way for a real capture to
   refuse. **RULING ASK: ACCEPT/CHANGE.**
4. **The strengthened smoke criterion cannot false-refuse the real run.**
   ADVERSARY: internal-consistency — the one-shot elevated session burned by our own gate.
   REACHES IT VIA: `mbcx01_smoke_cell.py` (`_semantic_receipt_errors`,
   `SMOKE_NOT_APPLICABLE_RECEIPT_CODES`, `SMOKE_COORDINATE_PROBE`, preflight toolchain
   probes, `_persist_unsigned_evidence`) + `run-smoke-cell.ps1`.
   The builder MEASURED the false-refusal risk: unmodified, the semantic check refused the
   runbook's own default cell (`MEASUREMENT_SCHEMA_INVALID` — the registration test
   short-circuits every other check) and smoke's own enforcement record
   (`EXTERNAL_WORK_UNMEASURED` — the record declares on its face it installs nothing). Four
   judgment calls to rule: (a) `EXTERNAL_WORK_UNMEASURED` held NOT-APPLICABLE by name,
   reported never dropped; (b) the unregistered coordinate is normalized on a SHALLOW COPY
   probe (subtracting the code instead would disable EVERY semantic check for the published
   invocation; bw83-integration asserts the receipt digest is unchanged and that a semantic
   defect still refuses); (c) the ps1 probes `node` in the pre-elevation shell but does NOT
   re-check the verifier script path (one frozen constant, not two driftable ones); (d)
   unsigned `UNSIGNED-INCOMPLETE-*` copies are KEPT after a successful run.
   Witnesses bw80–bw86. **RULING ASK: four explicit ACCEPT/CHANGE calls, judged against the
   real elevated invocation.**
5. **The banked-expectation change in bw83-measurement is the TRUE arithmetic.**
   ADVERSARY: maintainer — an amendment quietly rewriting a banked test's numbers.
   REACHES IT VIA: `test_mbcx01_build_measurement.py`
   (`test_bw83_positive_foreign_switches_are_baselines_never_member_deltas`).
   The expectation moved `[0, 200, 0, 50]` → `[500, 200, 0, 50]` (sum 250 → 750): the old
   first-delta zero encoded exactly the undercount AMENDMENT-3 closes, and the change is
   recorded in-test. Verify from the fixture's own raw counters that 500 = 1500 − 1000 is
   member work under CSwitch semantics and that processor 1's capture-start zero is right.
   **RULING ASK: ACCEPT the corrected expectation or show the old one was true.**
6. **The two spawn-fence allowances weaken nothing.**
   ADVERSARY: maintainer — a no-execution fence quietly widened.
   REACHES IT VIA: `verify-build-bundle.py` (`check`, the permitted set).
   (a) `node.exe` joins bare `node` (same binary, Windows extension via `shutil.which`);
   (b) pwsh is permitted for EXACTLY the command shape that targets `run-smoke-cell.ps1`
   (bw86's launcher-refusal witness; the launcher aborts pre-elevation in a System32-only
   PATH) — any other pwsh spawn still fails the fence.
   **RULING ASK: ACCEPT both allowances or name the narrower shape.**

## 5. Red witnesses per closed class

Every r6 fold class carries a discriminating probe RED on hash-proven pre-fix bytes and GREEN
after — the worker reports' transcripts and the amendment doc §4 carry them verbatim; the
ledger maps all 16 new witnesses two ways (72/186). The driver re-ran FOLD-A's five and
FOLD-B's module independently, reproduced the AMENDMENT-3 pre-fix RED with its own probe
(hash-asserted scratch imports), and re-ran the frozen witnesses against pre-fix bytes
(3 RED / 2 labelled guards). Re-run them yourself — §6.

## 6. Executable-falsification lane — all seats

- `python -m unittest test_mbcx01_build_state test_mbcx01_build_measurement
  test_mbcx01_build_integration` (expect 186 OK) · the frozen `test_mbcx01_r13_*` set
  (expect 155 OK) · `python verify-build-bundle.py` (REAL exit 0 — read the code, not a
  pipe).
- Construct and RUN at least one fresh probe per item you rule on. EXECUTED/READ-ONLY labels;
  a READ-ONLY verdict cannot be the deciding GO.
- ⚠ Empty probe output is a broken-harness signal, never a pass.
- ⛔ No ETW session, no Job Object, no `MBCX01_BUILD_ALLOW_PHYSICAL`, no
  `run-smoke-cell.ps1 -Execute` outside bw86's own no-node shape.

## 7. Omission attack

At least one seat: what, un-named above, could the FOLDS have broken or left open that makes
a wrong number possible? Candidates deliberately under-weighted: the interaction of
AMENDMENT-3 baselines with `foreign_instructions_excluded_after_first_member`'s meaning; the
producer path's baseline plumbing (`SimulatedCollection` default `()` — can a caller that
FORGETS the field sign a truthful-looking undercount, and is that acceptable given the frozen
validator seeds only from what the trace CARRIES?); whether any pre-existing witness now
passes for a weaker reason than it did at r6.

## 8. Non-claims

1. **No claim the consumer works live** — never executed against a real ETW session; the
   smoke run remains the only discharge for the platform facts.
2. **No security boundary against in-process actors** — validity review only.
3. **No exactness-execution claim** (#7 unbuilt).
4. **Enumerated-set green only** — 186 + 155 tests, 72 ledger rows; "no failure seen in the
   shapes this net covers".
5. **Known open, tracked:** #25 (OperationalError red owed) · #3 (machine-wide provider
   abort risk, gating the smoke run) · #17–#22 (the engine's producing half, zero lines by
   design) · #23 (DoR reconciliation) · #26 (relocation) · #27 (AMENDMENT-3 ratification —
   owner gate, not this round's to grant).

## 9. Why this exists (build-decision challenge)

ALREADY-BUILT: every fold is a bounded edit inside existing functions consuming evidence the
harness ALREADY derives (the partition's foreign lifetimes; the declared version set; the
existing `_receipt_errors` validator; the predecessor's raw counter). The three-repo ETW
query still returns zero files (§11); nothing external was adopted because nothing external
carries the signed-evidence join.
PRODUCT-FIT: fail-loud measurement, mirror-not-cop — the folds make the instrument accept
more true evidence (TID reuse, real smoke shapes), refuse more wrong evidence (unverified
versions, semantic smoke defects), and stop lying to itself (the first-interval undercount).
One sentence: the owner needs the one elevated session to certify a producer whose numbers
are true, and every fold serves exactly that.
BIGGER-THAN-THE-BUG: AMENDMENT-3 is one trace field plus seeded arithmetic — the smallest
change that makes the signed number true; the writer-door and receipt-slot machines r6
declined remain NOT built.
PRIMARY-CONSUMER: the inference layer and the owner defending one number consume the signed
receipt; a bounded read now buys them a retired-instruction total that includes the first
member interval, with the baseline evidence to reproduce the subtraction.

## 10. Search log (driver's own sweep)

This round's load-bearing vendor questions were settled in r6 at primaries opened at origin
(PsGetThreadId TID reuse; EVENT_DESCRIPTOR version-as-schema-identity; the Kernel-Process
manifest's field lists; SQLite single-writer; RFC 7468) — carried as SETTLED-BY-PINNED-BYTES
for the folds those sources ordered; no NEW prior-art claim is introduced by this packet. The
one new mechanism (predecessor-baseline seeding) is arithmetic on our own bytes, verified by
execution (§5); UNSEARCHED: NOT-LOAD-BEARING (rests on our own bytes and the banked r6
primaries).

## 11. Internal-shelf log (driver's own internal sweep)

QUERIES: `InstructionRetired` · `TracePmc` · `CSwitch` · `ProcessSequenceNumber` ·
`first_member_baseline` · `baseline_counter`
REPOS: agentvault-mcp-bridge (`src/`) · Photon (`crates/`) · Gravity (`src/`) — all three.
OPENED: the r6 sweep's findings stand (writer_gate.rs/store_open.rs read and declined with
reasons the r6 round ratified); the ETW/PMC shape still returns zero files in all three
repos; no sibling repo carries a PMC baseline-seeding precedent (the mechanism is one-of-kind
with the consumer it repairs).
STOPPED: the fold shapes resolve to our own r6-ratified bytes; nothing new to adopt.

## 12. Seat SWEEP lane (the seats' own sweep)

SWEEP APPLIES TO: any claim resting on prior art, a standard, or vendor-documented behaviour
(CSwitch/PMC semantics, ETW event versioning, RFC 7468, SQLite) — go look with your own
queries before you bless or refute it.
DELIVERABLE: a SWEEP LOG in your verdict — exact queries · what you OPENED (URL + deciding
section) · what it changed or confirmed · why you stopped.
LABELS: every prior-art or standards-bearing finding carries exactly one of SEARCHED /
RECALLED / UNSEARCHED (UNSEARCHED carries its reason: NOT-LOAD-BEARING ·
SETTLED-BY-PINNED-BYTES · COULD-NOT · DID-NOT).
CONSEQUENCE: an UNSEARCHED or RECALLED finding cannot be the deciding GO on a claim resting
on prior art or a standard; a round where no seat swept such a claim is incomplete.
HONEST OUT: if you cannot reach the web this session, say so plainly in one line — a
capability report, not a discharge.

## 13. Re-review trigger

A CHANGE ruling on AMENDMENT-3 or on the scope's classification rules ⇒ fold + fresh round.
ACCEPT rulings + leaf fixes ⇒ fold and advance to the codex-CLI r4 gate (#1). Anything
needing a new subsystem stops at the owner.

## 14. Driver pre-dispatch execution (run before sending, at the §2 pin)

- BUILD **186/186 OK, exit 0** · frozen **155/155 OK, exit 0** · `verify-build-bundle.py`
  REAL exit **0** (72/186 two-way, reconciliation PASS, readiness unchanged) · clean-room
  `verify-build-pinned.ps1 -Commit abcab342… -ManifestBlob 9fa1440d…` →
  `PINNED RECONSTRUCTION COMPLETE`, real exit 0 — all witnessed on THESE bytes this session.
- The AMENDMENT-3 differentials driver-executed: truthful accepted · undercount-with-baseline
  refused · old shape refused · capture-start accepted · orphan/negative/duplicate baselines
  refused · mixed foreign-between-members arithmetic exact.
- The judgment calls in items 2(a-d), 4(a-d) and the two fence shapes are the builders' and
  the driver's own — ruling them is this round's job, and the author checking his own calls
  is the blind spot you exist to cover.
