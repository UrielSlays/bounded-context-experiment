# MBCX-01 BUILD acceptance r7 — SEAT1 (outside Opus 5) verdict

Banked by the driver from the seat thread (claude.ai conversation
`<id>`, read via wait_quiesced 2026-08-16, textLen 21,000,
truncated: false). Packet `MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r7.md @ cbab20b`; review
target content pin `abcab342` (seat confirmed the pin and the records-only tail). Verdict
verbatim below (two provider-UI noise lines stripped).

---

GO-WITH-FIXES(AMENDMENT-3-BASELINE-TOTALITY · SMOKE-VERIFIER-PREFLIGHT · SPAWN-FENCE-SHAPE · UNCOUNTED-INTERRUPT-WORK-NONCLAIM)

Label: EXECUTED. AMENDMENT-3's arithmetic is right and I verified it independently. One CHANGE ruling against the unratified draft (item 1), three leaf fixes, one non-claim owed. Per §13 the item-1 CHANGE means a fold + fresh round — which is exactly why finding it now, before ratification, is the cheap outcome.

What I read and at which commit. Packet at cbab20b. I read the CODE from the working tree and confirm it matches the §2 content pin abcab34: git diff --stat abcab342 HEAD -- '*.py' is empty, and the full abcab342..HEAD diff is exactly two files — the r7 packet and the regenerated MBCX-01-BUILD-PIN-MANIFEST.json. HEAD is 8932e87 (manifest regeneration only). Three untracked seat-3 r7 artefacts sit in the tree; I opened none of them — the round is sealed.

Read-only compliance: no repository byte created, edited or deleted. Probe scripts live in %TEMP%. No ETW session, no Job Object, no MBCX01_BUILD_ALLOW_PHYSICAL, no run-smoke-cell.ps1 in any mode.

Baseline reproduced, raw: BUILD Ran 186 tests … OK exit 0 · frozen Ran 155 tests … OK exit 0 · verify-build-bundle.py real exit 0 — tests 186 / expected 155 / tests 155, invariants 72 / witnesses 186 / two_way_total true, reconciliation_performed true / subjects_reconciled 70, trust_root_activated false, readiness unchanged. §0's grep re-run at the pin blobs: 0 hits in all three governing docs. No threat model; this is a validity review.

My r6 findings, verified closed: r6-F1 (TID-reuse false refusal) — closed and executed below. r6-F2 (node preflight) — landed at run-smoke-cell.ps1:109-120 with a named SIGNATURE_VERIFIER_TOOLCHAIN_UNAVAILABLE abort plus a re-probe inside the elevated session. r6-F5 — the field is now foreign_instructions_excluded_after_first_member, which says what it counts.

Evidence read

MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r7.md:1-264@cbab20b · mbcx01_build_etw_consumer.py:1776-1827 (foreign_thread_intervals), :1829-1839 (_lifetime_contains), :1937-2023 (scope_cswitch_records_to_members, the AMENDMENT-3 capture at :1995-2001), :1773, :2344, :2424 (baseline wiring), :382/:3171-3173 (thread version gate) · mbcx01_build_win32.py:503-511 (first_member_baselines: tuple = ()), :650-686 (seeding + ETW_CSWITCH_BASELINE_INVALID), :897, :460-479 (resolve_thread_lifetime) · mbcx01_r13_measurement.py:458-468 (TRACE_KEYS), :650-664 (fixture), :969, :1016-1078 (baseline validation, seeding, baselined ⊆ observed), :520-534 (_invoke_signature_verifier) · mbcx01_build_windows_producer.py:229-233, :435-437 · mbcx01_smoke_cell.py:170-195 (node_runtime_facts), :685-707 (SMOKE_NOT_APPLICABLE_RECEIPT_CODES, SMOKE_COORDINATE_PROBE), :711-750 (_semantic_receipt_errors), :778-818 · run-smoke-cell.ps1:49, :109-120, :161 · verify-build-bundle.py:266-289 (spawn fence) · test_mbcx01_build_measurement.py:3583-3644 (bw83).

SWEEP LOG

I can reach the web this session.

Query: ETW TraceSetInformation TracePmcEventListInfo PMC counters CSwitch EVENT_HEADER_EXT_TYPE_PMC_COUNTERS values interpretation → OPENED at origin: randomascii.wordpress.com/2016/11/27/cpu-performance-counters-on-windows/ (Bruce Dawson; page live, modified 2021-12-15). Deciding passage: the Pmc records carry the state of the counters at that point on that CPU; because the counters are per-CPU, a parser must keep the previously seen value for each CPU to compute the delta, then attribute that delta to the thread being switched out. That is AMENDMENT-3's model exactly — including the load-bearing half: the predecessor is the previous record on that processor whoever owned it, which is precisely what first_member_baselines restores. Corroborated in the same page's comment thread by Geoff Chappell (the per-switch event "lets you keep track of which changes to the counters were caused while your thread ran on that processor") and independently by easyperf.net/blog/2019/02/23/... (subtract successive Pmc values; sum the deltas). SEARCHED — and it is the deciding external evidence for my ACCEPT on items 1 and 5.
Ceiling, stated honestly: Microsoft publishes no primary for this; TracePmcCounterListInfo is documented in one sentence. Three independent practitioner sources agreeing is the best available, and I am not going to pretend it is a vendor specification.
What it also surfaced, which the packet does not name — see F4.
PsGetThreadId TID reuse · SQLite single-writer · RFC 7468 · CWE-1291 — RECALLED from r4/r5/r6, where I opened the first two at their origins. Carried as argument; no r7 finding rests on them.
ETW event-version-as-schema-identity (item 3) — UNSEARCHED: SETTLED-BY-PINNED-BYTES. The packet's r6 sweep opened the Kernel-Process manifest at origin; the r7 question is not "what does the platform publish" but "should we refuse an unpublished version", which is our own posture call.

Why I stopped: the one new mechanism this round introduces (predecessor-baseline seeding) had exactly one external dependency — what a CSwitch-attached PMC value means — and I settled it at a source I opened, which both confirms the amendment and hands me F4.

Findings
F1 — EXECUTED · item 1 · AMENDMENT-3's arithmetic is correct

Fresh probe: two processors, foreign work before the first member record on p0, foreign work between member records on p0, and p1 where the member record is the first record on the processor.

baselines        : ({'processor': 0, 'counter_value': 1000},)
baseline_records : 2   foreign_instructions: 400
kept (p,qpc,emitted): [(0,11,1500), (0,14,1700), (1,20,5000), (1,25,5300)]
deltas           : [(0,11,500), (0,14,200), (1,20,0), (1,25,300)]
aggregate        : 1000   ground truth: 1000   MATCH
same stream, baselines dropped -> 500  (undercount of 500, SIGNS CLEAN)

prior is offset-consistent by construction — foreign_offset[p] is created at the first kept record and foreign work before it is never accumulated (:2013-2018), so the baseline is the unadjusted predecessor raw and emitted = raw. The shape rules are tight; I hit them all against the frozen validator:

A truthful (baseline 1000)              -> ACCEPT  total 700   <- ground truth
C old shape, key absent                 -> REFUSE
E orphan baseline (processor unobserved)-> REFUSE
F duplicate baseline for one processor  -> REFUSE
G negative counter_value                -> REFUSE
H baseline above the first counter      -> REFUSE
I extra key in the baseline row         -> REFUSE
J bool smuggled as processor            -> REFUSE

The migration story holds: the old shape is unrepresentable. Consequence: this fold makes a previously wrong number right — no finding against the arithmetic.

F2 — EXECUTED · item 1 + §7 · BLOCKING for ratification · WRONG NUMBER (undercount) that signs

An empty cswitch_first_member_baselines is silently ambiguous, and it reproduces exactly the defect AMENDMENT-3 exists to close.

B baselines EMPTY, first delta 0 -> ACCEPT  total 200   (ground truth 700)

The validator cannot distinguish "every processor genuinely began at its first member switch-out" from "the producer never populated the field." Both are []. And both carriers default to empty: EtwPmcSession.first_member_baselines: tuple = () (mbcx01_build_win32.py:511) and SimulatedCollection.cswitch_first_member_baselines: tuple[...] = () (mbcx01_build_windows_producer.py:233).

Reachability, stated fairly: the live capture path is wired at both scope call sites (mbcx01_build_etw_consumer.py:2344, :2424), so this is latent, not live, on today's bytes. That is why it is a CHANGE against a draft rather than a NO-GO. But the field is signed evidence whose absence is indistinguishable from its correct absence, and the packet's own §7 asks this question — the answer is that it is not acceptable while the fix costs one token.

The fix is inside the amendment, not a new machine. Note from my own probe: baseline_records = 2 but only one baseline row — p1 was capture-start. Make the row set total: emit a row for every processor at its first kept record, using prior if prior is not None else raw (a capture-start row's counter_value equals its first observation's, so its delta stays the declared 0 and no number moves), then strengthen the validator's baselined_processors <= observed_processors at mbcx01_r13_measurement.py:1074 to ==. Case B becomes unrepresentable; every accepted case above is unchanged. False-refusal check: a processor carrying observations always has a first kept record, so a row can always be emitted — the == cannot refuse a truthful capture.

F3 — EXECUTED · item 1 · WRONG NUMBER (overcount) that signs · residual to declare, not fixable in the receipt
D baseline understated to 0 -> ACCEPT  total 1700   (ground truth 700)

Nothing bounds the baseline from below. expected_delta < 0 catches a baseline that is too high; a baseline that is too low inflates the first interval and signs. This channel did not exist before AMENDMENT-3 — the first delta was pinned to 0, so no baseline could inflate anything. The plausible honest-bug shape is concrete: the scope's comment at :2014-2016 reasons explicitly about the boundary "foreign switches before this processor's first member switch are already outside the emitted chain"; get that boundary off by one and the baseline becomes the processor's first raw rather than the predecessor's, sweeping all pre-member foreign work into the member total.

Against closure-architecture §7 this is the direction that matters. The physical claim is max-minus-min across H per (D,F); an undercount that hits all cells alike partly cancels in a difference, while an overcount concentrated in one cell does not — it can flip the boundedness verdict. F2's fix does not close F3, and no receipt-internal check can. This is the price of AMENDMENT-3 and it belongs in front of the owner before ratification, as a line in the amendment and a §8 non-claim: the baseline is trusted evidence, checked only for shape and for non-negative first delta.

F4 — SEARCHED (deciding source opened at origin) · §7 omission attack · WRONG NUMBER (overcount) · non-claim owed

Interrupt and DPC work executed on the processor while a member thread was current is counted as member work, and nothing anywhere says so.

Dawson's post states it plainly as a caveat to this exact technique — ISRs and DPCs run in the context of whatever was on the CPU and therefore dirty the performance counters, and adjusting for it is left to the reader. Chappell's comment on the same page makes the same point in more detail: hardware interrupts, deferred procedure calls, and the scheduler code that traces these very switches all run and are counted.

This is a property of CSwitch-attached PMC measurement, not a defect in the fold — but it is a real perturbation of the number this instrument signs, it is not in §8's non-claims, and AMENDMENT-3 marginally increases the exposure by counting one more interval per processor. Magnitude is unknowable until the elevated run. Fix class: documentation only — one non-claim in §8 and one line in the amendment. Naming it is exactly the mirror-not-cop posture; leaving it unnamed means the owner defends a number whose known contaminant is unstated.

F5 — EXECUTED · item 6(b) · admits wrong evidence about the bundle's own no-execution claim · leaf

The pwsh allowance at verify-build-bundle.py:282-285 is a substring test over any command part:

pwsh -File C:/repo/run-smoke-cell.ps1 -Execute            fence=True   endswith-variant=True
pwsh -Command "…'see run-smoke-cell.ps1 for details'…"     fence=True   endswith-variant=False
pwsh -Command Get-Process                                  fence=False  endswith-variant=False

An honest test that merely mentions the filename in a message string silently acquires a pwsh allowance it was never meant to have, and the bundle then reports PASS on a no-execution claim that is weaker than stated. In-model: this is a maintainer accident, not evasion. One-token narrowing — require a part that ends with run-smoke-cell.ps1 (a path, not a mention). bw86's real shape passes either way.

F6 — EXECUTED · item 4(c) · REFUSES RIGHT EVIDENCE / burns the elevated session · leaf

My r6 F2 landed for node — and stopped half-way. node_runtime_facts() probes only the interpreter:

node facts keys: ['error','exit_code','probe','requested','resolvable','resolved_path','runnable','version']
VERIFIER exists on disk: True | probed by preflight: False

_invoke_signature_verifier (mbcx01_r13_measurement.py:522-528) maps a missing verifier script to the same ValueError that a missing node produces, which becomes VERIFIER_UNAVAILABLE → valid=False → the conjunction fails — but inside the elevated session rather than before it. One os.path.exists(VERIFIER) alongside the node probe closes the other half of the same door.

F7 — EXECUTED · item 2(b) downstream · refuses right evidence in the wrong shape · leaf

The (0, None) fallback for a roster row with no interval (:1950-1955) is sound inside the scope — the member branch wins over any foreign interval, so it can never move member work out (probe: kept 3, ambiguous 0). But such a row then reaches the joiner:

resolve_thread_lifetime([{"thread_id":700,"process_id":1,"process_start_key":"x"}], 700, 50)
  -> RAW KeyError: 'started_qpc'   (not a named EtwConsumerFault)

A malformed roster produces a traceback rather than a named code. Production rosters always carry both ends, so this is a nuisance, not a data risk — but it is the one place in this fold where the fail-loud posture is loud without being named.

Verified closed (no finding)

r6-F1 is CLOSED. With the recycling host thread's lifetime observed, the record is excluded and the capture proceeds; without it, the record stays ambiguous, is counted, and aborts by name:

foreign START 80 / STOP 95 for TID 700   kept=2 excluded=1 ambiguous=0  -> consume OK, total 100
foreign STOP 95 only (no START)          kept=3 excluded=0 ambiguous=1  -> ETW_CSWITCH_UNATTRIBUTED_THREAD
no foreign events at all                 kept=3 excluded=0 ambiguous=1  -> ETW_CSWITCH_UNATTRIBUTED_THREAD

Item 4(b) digest invariance — EXECUTED. _semantic_receipt_errors left the receipt byte-identical (receipt digest unchanged: True), and a validation fault becomes MEASUREMENT_SEMANTIC_VALIDATION_FAULT, never a pass.

The six rulings

1 — AMENDMENT-3: CHANGE (narrowly), then ratify.
The arithmetic and the shape rules are correct and I verified both independently (F1); the single defect is that an empty baseline set is indistinguishable from a forgotten one and silently reproduces the pre-amendment undercount (F2) — make the row set total over observed processors and tighten ⊆ to ==. Declare F3 and F4 in the amendment as what the baseline is: trusted evidence bounded only from above.

2 — the four scope judgment calls:
(a) foreign ThreadStop with no START yields no interval — ACCEPT. Refusing beats guessing when a wrong guess can move member work out, and roster_tid_outside_any_lifetime makes the abort diagnosable. Named alternative for the owner, since a fold is happening anyway: a stop-without-start could yield (0, ended_qpc) — the lower bound is known, not guessed, and the member branch already wins over any foreign interval, so it cannot move member work out. It would remove one live false-refusal class. That is a CHANGE and belongs bundled with item 1's, or not at all.
(b) a roster row with no interval covers the whole capture — ACCEPT; it preserves pre-fold behaviour and production rosters always carry both ends. F7's leaf is owed so the malformed case is named rather than a traceback.
(c) a newly-foreign record takes the foreign branch's backwards check — ACCEPT. Either branch faults on a backwards counter; only the name differs, and the foreign name is the truthful one now that the record is classified foreign.
(d) kept_roster_tid_outside_any_lifetime counts the residual — ACCEPT. This is my r6 F1 fix landing, and my probes show the counter separating exactly the two cases it was built to separate.

3 — thread-event version gate: ACCEPT, with a residual the runbook should carry.
Decoding at unverified offsets is a wrong number; refusing is right under §7. Residual: unlike node, this cannot be preflighted — the version is only known once events flow — so it is a new way the one-shot elevated session can die, and the runbook should say what to do when it fires (record the version, verify offsets via TDH, extend KERNEL_THREAD_PAYLOAD_VERSIONS_VERIFIED, re-round).

4 — the four smoke judgment calls:
(a) EXTERNAL_WORK_UNMEASURED held NOT-APPLICABLE by name and always reported — ACCEPT. The split is computed both ways (raised - NOT_APPLICABLE and raised & NOT_APPLICABLE) and both land in the report, so nothing is dropped. (READ-ONLY on the split itself — the fixture raised neither code, so I did not exercise it.)
(b) shallow-copy coordinate probe — ACCEPT, executed. The digest is unchanged, the probe is recorded, and subtracting the code instead would have disabled every semantic check for the published invocation.
(c) the ps1 probes node but not the verifier script — ACCEPT the reasoning, F6 leaf owed. One frozen constant is the right call; probing its existence still costs one line and closes the other half of the door my r6 F2 opened.
(d) UNSIGNED-INCOMPLETE-* copies kept — ACCEPT. Naming unsigned evidence on its face and keeping it is the fail-loud posture; deleting it would destroy the only artefact available if the signed half is refused.

5 — the bw83 expectation [0,200,0,50] → [500,200,0,50]: ACCEPT, verified from the raw counters.
p0: foreign @qpc12 raw 1000 → member @qpc14 raw 1500 = 500, the interval thread 900 actually ran; @qpc16 raw 2500 → @qpc18 raw 2700 = 200; the 1000 between qpc14 and qpc16 is foreign and counted nowhere. p1: raw 5000 is the first record on that processor — no predecessor, so 0 is right, not an undercount; then 5050−5000 = 50. Sum 750. The old expectation encoded the r6 NO-GO's undercount, and Dawson's rule (delta against the previously seen value on that CPU, attributed to the outgoing thread) is the external confirmation.

6 — the two fence allowances: (a) node.exe — ACCEPT, same binary, same permission as git.exe. (b) pwsh for the launcher shape — ACCEPT the intent, CHANGE the shape to an endswith path match (F5); the current substring test admits any pwsh command that merely mentions the filename.

Residual risks
F3 is permanent. After F2's fix the baseline is still unverifiable downward. Every future round should treat "the signed total" as resting on the producer's baseline arithmetic, which no validator checks.
F4's magnitude is unknown until the elevated run, and it is systematically upward.
Two unpreflightable session-burners remain: the thread-event version gate (ruling 3) and #3's machine-wide provider abort risk. F6 closes the last preflightable one.
Item 4(a)'s split is READ-ONLY — I read the mechanism but did not drive a receipt that raises EXTERNAL_WORK_UNMEASURED.
My sweep's ceiling: the CSwitch/PMC semantics that AMENDMENT-3 depends on rest on three agreeing practitioner sources, not a Microsoft specification. If any seat can find a vendor primary, it should replace mine.
Unchanged and tracked: #25 (OperationalError red owed) · #23 · #26 · #27.
Fix class
#	Class	Scope	Gate
F2	AMENDMENT-3-BASELINE-TOTALITY — a baseline row for every processor at first-kept (capture-start uses raw); <= → == at mbcx01_r13_measurement.py:1074; one red witness on the empty-baselines shape	scope + frozen validator + producer + witness	CHANGE ⇒ §13 fold + fresh round. Cheapest now: the amendment is unratified.
F4	UNCOUNTED-INTERRUPT-WORK-NONCLAIM — one §8 non-claim + one line in the amendment	docs	Bundle with F2's fold; owner ratifies.
F3	declare in the amendment as a named residual (no code)	docs	Owner ratifies with F2.
F6	SMOKE-VERIFIER-PREFLIGHT — os.path.exists(VERIFIER) beside the node probe	mbcx01_smoke_cell.py preflight + witness	Leaf. Before the elevated run.
F5	SPAWN-FENCE-SHAPE — substring → endswith	verify-build-bundle.py:283	Leaf; codex r4.
F7	named fault instead of a raw KeyError for an intervalless roster row	mbcx01_build_win32.py:476-479	Leaf; codex r4.

On the GO. EXECUTED, so this can be a deciding vote. GO-WITH-FIXES rather than NO-GO because AMENDMENT-3 is correct — it turns a real undercount into a true number, and I verified that against both the bytes and an external source — and F2 is a bounded tightening of a draft that has not yet been ratified. My vote on issue #27 is: do not ratify AMENDMENT-3 as drafted; ratify it with F2's totality rule and F3/F4 declared. And if any part of this round is read as authorising the elevated smoke run, my vote is NO-GO until F6 lands — the session is one-shot, and it now has three ways to die that have nothing to do with the measurement.
