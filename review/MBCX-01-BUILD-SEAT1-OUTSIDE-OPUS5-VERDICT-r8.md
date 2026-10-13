# MBCX-01 BUILD acceptance r8 — SEAT1 (outside Opus 5) verdict

Banked by the driver from the seat thread (claude.ai conversation
`<id>`, read via wait_quiesced 2026-08-16, textLen 15,565,
truncated: false). Packet `MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r8.md @ dc06bae`; review
target content pin `575fb38` (seat confirmed pin + records-only tail; seal note recorded —
it deliberately did not open the committed r7 sibling verdicts). Verdict verbatim below
(two provider-UI noise lines stripped).

---

GO-WITH-FIXES(LEAF: UNWITNESSED-FAULT-NAME · RECORDS-CORRECTION-TO-MY-OWN-r7-VERDICT)

Label: EXECUTED. All four rulings are ACCEPT. Neither fix is a fold to the four surfaces and neither blocks the codex gate — one is a missing witness for a fault name my own r7 finding created, and one is a correction to a false residual I banked at r7.

What I read and at which commit. Packet at dc06bae (dc06baeff1fb3f26f984f2f8ce2e542f842b17e0). I read the CODE from the working tree and confirm it matches the §2 content pin 575fb38: git diff --stat 575fb38 HEAD -- '*.py' is empty, and the full 575fb38..HEAD diff is exactly the r8 packet plus the regenerated pin manifest. HEAD is 1bfa34c. Three untracked seat-3 r8 artefacts sit in the tree; I opened none.

Seal note. MBCX-01-BUILD-SEAT1-OUTSIDE-OPUS5-VERDICT-r7.md and MBCX-01-BUILD-SEAT2-CHATGPT-SOL-VERDICT-r7.md are now committed at this pin. I deliberately did not open either. The packet tells me which shapes came from which seat, which is enough; reading another seat's reasoning would make this pass a review of their verdict rather than of the bytes. Everything below is my own construction.

Read-only compliance: no repository byte created, edited or deleted. Probes in %TEMP%. No ETW session, no Job Object, no MBCX01_BUILD_ALLOW_PHYSICAL, no launcher invocation of any kind — the fence probes drive ExecutionPosture.check() over synthetic argv lists, spawning nothing.

Baseline reproduced, raw: BUILD Ran 188 tests … OK exit 0 · frozen Ran 156 tests … OK exit 0 · verify-build-bundle.py real exit 0 — tests 188 / expected 156 / tests 156, invariants 73 / witnesses 188 / two_way_total true, subjects_reconciled 70, trust_root_activated false, readiness unchanged.

Evidence read

MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r8.md:1-169@dc06bae · fold diff abcab342..575fb38 in full · mbcx01_build_etw_consumer.py:1785-1798 (prefix-interval docstring), :1819-1838 (set(starts)|set(stops), the leading-stop branch, if rows:), :2005-2019 (unconditional baseline row) · mbcx01_r13_measurement.py:650-660 (fixture now carries a capture-start row), :1074-1086 (baselined_processors != observed_processors) · mbcx01_build_windows_producer.py:226-236 (field REQUIRED, no default) · mbcx01_build_win32.py:473-489 (ETW_THREAD_ROSTER_ROW_INVALID), :522 (session default still ()), :666, :908 · verify-build-bundle.py:98-105 (FROZEN_TEST_TOTAL = 156 + dated reason), :282-297 (the 5-part argv + payload regex) · MBCX-01-R13-AMENDMENT-3-…-2026-08-16.md (r7 amendment block + the two declared residuals) · MBCX-01-BUILD-SMOKE-RUNBOOK.md step 4b · mbcx01_smoke_cell.py:170-195, :205-225, :271-272 · MBCX-01-BUILD-REPAIR-LEDGER.json.

SWEEP LOG

I can reach the web this session.

Re-opened at origin THIS round: learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntddk/nf-ntddk-psgetthreadid, Remarks (page live, last updated 2024-02-24). Two sentences, and item 2 turns on both: a thread ID is unique system-wide among live threads, and reuse happens only after termination. The folded docstring at mbcx01_build_etw_consumer.py:1789-1793 infers from exactly this that every in-capture switch naming a TID before its observed terminal stop belongs to the pre-existing incarnation. The primary carries that inference exactly — nothing is guessed, the stop time is observed and the lower bound is a property of the OS allocator, not an assumption. SEARCHED — and this is the deciding external evidence for my ACCEPT on item 2, so it needed to be opened this round rather than recalled.
CSwitch-attached PMC semantics (Dawson / Chappell / easyperf) — RECALLED, opened by me at r7. They are now cited inside the amendment as residual #2's basis; I byte-checked that citation rather than re-opening the sources, and it states them accurately, including that Microsoft publishes no primary for this surface.
No new prior-art claim is introduced by this confirm round. Items 1, 3 and 4 rest on our own bytes, arithmetic, and owner rulings — UNSEARCHED: NOT-LOAD-BEARING, reason stated.

Why I stopped: exactly one item in this round rests on vendor behaviour, and it is settled at a Microsoft primary I opened today. A second pass would re-read a 120-word page.

Findings
F1 — EXECUTED · item 1 · the totality rule closes the ambiguity and cannot false-refuse

Randomised false-refusal hunt, 200 synthetic truthful captures (1–4 processors, member/foreign interleaving, capture-start and predecessor cases mixed):

truthful captures checked: 190   would-be false refusals: 0

For every one, the scope's baselined processor set equalled the observed set. That is the structural reason: a baseline row is now emitted unconditionally at each processor's first kept record (:2013-2019), and every kept record becomes an observation — so == is an identity on truthful output, not a constraint.

The forgotten-field path, end to end:

scope emits baselines: ({'processor': 0, 'counter_value': 1000},)
session WIRED (truthful)        total=700   frozen validator -> ACCEPT
session DEFAULT () (forgetful)  total=200   frozen validator -> REFUSE ['INSTRUCTION_ACCOUNTING_INCOMPLETE']

My r7 F2 is closed. The undercount that signed at r7 is now unsignable.

Pacifier check (§7): exactly one SimulatedCollection construction site in the tree (test_mbcx01_build_measurement.py:427), passing tuple(...) of real scope output; zero occurrences of a literal () or [] passed to the field anywhere. No compliance costume.

F2 — EXECUTED · item 1 residual · no wrong number reaches a signature; the refusal arrives late and generic

EtwPmcSession.first_member_baselines: tuple = () at mbcx01_build_win32.py:522 kept its default while the producer's field became required. The asymmetry is defensible — the frozen == catches it, as the probe above shows — but consume_cswitch itself emits the undercounted observation set without complaint, and the refusal surfaces two layers later as the generic INSTRUCTION_ACCOUNTING_INCOMPLETE rather than the collector's own ETW_CSWITCH_BASELINE_INVALID. Consequence: none to the number (nothing signs). Optional leaf; I am not asking for it, only recording that the last defaulted carrier is here and that the totality rule is what makes it harmless.

F3 — EXECUTED · item 2 · the prefix interval cannot swallow member work — falsification attempted and failed

Interval shapes, all as documented:

leading STOP only             -> {700: [(0, 50)]}
leading STOP then START       -> {700: [(0, 50), (60, None)]}
TWO leading STOPs, no START   -> {700: [(0, 50)]}          <- second unmatched stop yields nothing
START before STOP (normal)    -> {700: [(10, 50)]}
STOP, START, STOP             -> {700: [(0, 5), (10, 50)]}
START only (open)             -> {700: [(10, None)]}

The adversarial construction the packet asked for: member TID 700 alive [10,40], and a foreign leading STOP at qpc 50 producing a prefix (0,50) that fully covers the member's entire life:

kept qpcs: [20, 30]   excluded qpcs: [5, 45]   ambiguous: 0
baselines: ({'processor': 0, 'counter_value': 100},)
deltas: [(20,200), (30,200)]   total: 400
ground truth for member work inside [10,40]: (300-100)+(500-300) = 400

The member branch wins containment first (:1996-2001), so the prefix took only the two records outside the member's life. And the same stream pre-fold: kept 4, ambiguous 2 -> ETW_CSWITCH_UNATTRIBUTED_THREAD. The fold converts a false refusal into a correct measurement. The two-leading-stops case stays conservative — a record between the two stops belongs to an unobserved second incarnation and is refused, which is right.

One honesty note, closed: the delta rule assumes each processor's switch stream is complete; a lost CSwitch would silently widen a member interval. That is already refused — any nonzero EventsLost/LogBuffersLost/RealTimeBuffersLost raises ETW_EVENT_LOSS_DETECTED (mbcx01_build_win32.py, verified at r6). Not a finding.

F4 — EXECUTED · item 3 · the fence is exact, admits the witness, and my r7 F5 is closed

Fresh argvs of my own against ExecutionPosture.check():

REAL bw86 shape                       -> PERMITTED
6 parts (extra -NoLogo)               -> REFUSED
filename only mentioned in a string   -> REFUSED   <- my r7 F5, closed
right shape, wrong verb order         -> REFUSED
payload without the PATH prefix       -> REFUSED
double-quoted PATH instead of single  -> REFUSED
trailing payload after -Execute       -> PERMITTED
newline-smuggled tail (DOTALL)        -> PERMITTED

The two PERMITTED cases both require a payload that already invokes the launcher with -Execute and then appends. That is deliberate authorship — actor-evasion, out of model under §0 — so I record it as a residual and not a finding, and I note it is also the loose end that lets a benign payload-tail edit (; exit $LASTEXITCODE) keep passing.

The in-model risk runs the other way: parts 1–3 and the payload prefix are now exact, so a benign edit to bw86 — adding -NoLogo, reordering the switches, changing PATH quoting — breaks the bundle with unexpected spawned process. Consequence: refuses right evidence. It is loud, immediate, and recoverable in one line, and the alternative (loose matching) is what r7 removed. Accept the coupling; know it will fire.

F5 — EXECUTED · MY r7 FINDING F6 WAS WRONG, and I am correcting it on the record

I reported at r7 that "node is preflighted, the verifier script path is not." False at the byte. signature_verifier_facts() was introduced in the r6 fold 0d1a6a7, existed at the r7 pin abcab342, and is called from preflight at mbcx01_smoke_cell.py:272 — directly beside node_runtime_facts() at :271. Both execute clean here:

node_runtime_facts       : {"probe":"SHUTIL_WHICH_THEN_VERSION","resolvable":true,"runnable":true,"error":null}
signature_verifier_facts : {"probe":"ISFILE_AND_DIGEST","verifier_path":"…verify-r13-receipt-signature.mjs","present":true}

My r7 probe ran only node_runtime_facts() and my grep window stopped 35 lines short of its sibling; I inferred absence from one function's output instead of reading the preflight report's assembly. The r7 fold was right not to act on it. Consequence: none to the artifact — but a banked seat verdict carries a false residual, and MBCX-01-BUILD-ACCEPTANCE-ROUND-r7-SYNTHESIS.md should record F6 as withdrawn-by-the-seat-that-raised-it. That is the fix I am asking for.

F6 — EXECUTED · item 4 · a new fault name with no witness and no ledger row

The r7 fold created ETW_THREAD_ROSTER_ROW_INVALID (mbcx01_build_win32.py:487) from my own F7. It has zero hits in any test file and no ledger row, while its siblings do:

bw90 : 1 test hit | in ledger: True
bw91 : 1 test hit | in ledger: True
ETW_THREAD_ROSTER_ROW_INVALID : 0 test hits | in ledger: False

Consequence: none for the data — the posture is unchanged and a malformed roster still attributes nothing. But it is unpinned vocabulary: a future refactor could drop the name and every suite stays green. This is precisely the shape I ruled on at r6 item 4(3), now on a name I caused. Leaf: one red witness + one ledger row.

Omission attack — run, and empty
The if rows: change is behaviour-neutral: _lifetime_contains reads intervals.get(tid, ()), so an absent key and an empty list are indistinguishable to every consumer.
set(starts) | set(stops) widens the iteration domain but every added TID produces a prefix row or nothing — no previously-covered path became unreachable.
The fixture's baselines moved [] → [{processor:0, counter_value:100}], which changes fixture receipt digests; 188/156 green and the bundle's two-way totality hold, so no banked constant was orphaned.
No third baseline-trust residual found beyond the two declared.

I report that honestly as the packet's own convergence signature: my r7 findings came back as "already right" (F5) and "delete the residual" (F4's mention-only case), and the omission pass returned nothing.

The four rulings

1 — the totality rule as the AMENDMENT-3 shape of record: ACCEPT. 190 randomised truthful captures produce zero would-be false refusals because == is an identity on the scope's own output, and the forgetful path that signed 200-instead-of-700 at r7 is now refused end-to-end — I recommend #27 ratification of the amended draft.

2 — the stop-only prefix interval: ACCEPT. I built the worst case — a prefix covering the member's entire lifetime — and the member branch still won every contained record, total exactly ground truth, while the identical pre-fold stream aborted; the "first leading stop only" restriction keeps a second unobserved incarnation ambiguous rather than guessed, and PsGetThreadId's Remarks (opened today) carry the lower bound as an OS property rather than an assumption.

3 — the exact pwsh fence shape: ACCEPT. The real witness is permitted and five fresh bypass argvs of my own are refused including the mention-only case that motivated the change; the trailing .* only widens for a payload that already invokes the launcher, which is out of model, and the brittleness on parts 1–3 is a fail-loud coupling I would rather have than the substring test.

4 — the residual declarations: ACCEPT. Both AMENDMENT-3 residuals state the direction, the mechanism, the reason no receipt-internal check can close them, and the §7 consequence; the runbook's step 4b gives a mechanical fired-gate procedure that forbids widening the verified set without a TDH dump; the F7 named fault exists in the bytes. Two corrections owed, neither a fold to this surface: F6's missing witness and ledger row, and F5's withdrawal of my own r7 F6 from the synthesis record.

Residual risks
Unchanged and permanent: the baseline is trusted evidence bounded only from above; ISR/DPC work is counted as member work. Both now declared — which is the whole of what this round could do about them.
F4's coupling: the next benign edit to bw86's argv breaks the bundle. Expected, loud, one-line fix.
F2: EtwPmcSession.first_member_baselines is the last defaulted carrier; harmless only because the frozen == exists.
The version gate remains unpreflightable — step 4b tells the operator what to do when it spends the capture, which is the honest ceiling.
My own error rate is now on the record. One of my six r7 findings was false, and it was false because I inferred absence from a single function's output. A seat that costs the lane a phantom residual is a cost the lane should price; I would weight my future "X is not present" claims accordingly, and so should the driver.
Unchanged tracked opens: #25 · #3 · #17–#23 · #26 · #27.
Fix class
#	Class	Scope	Gate
F6	UNWITNESSED-FAULT-NAME — one red witness asserting ETW_THREAD_ROSTER_ROW_INVALID + one ledger row	test_mbcx01_build_measurement.py, MBCX-01-BUILD-REPAIR-LEDGER.json	Leaf; codex r4. Not a re-round.
F5	RECORDS-CORRECTION — mark r7 F6 withdrawn by the seat that raised it	MBCX-01-BUILD-ACCEPTANCE-ROUND-r7-SYNTHESIS.md	Records.
F2	optional: drop the = () default on EtwPmcSession.first_member_baselines, or name the collector-side refusal	mbcx01_build_win32.py:522	Owner's call; not requested.

On the GO. EXECUTED, so this can be a deciding vote. Four ACCEPTs — per §13 this arc advances to the codex-CLI r4 gate, and my ruling 1 rides #27's ratification ask as a recommendation to ratify. I am filing GO-WITH-FIXES rather than GO only because two small items are genuinely owed and one of them is mine; neither touches the four fold surfaces, neither blocks the codex gate, and neither is a reason to hold the elevated run.
