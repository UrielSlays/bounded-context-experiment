# MBCX-01 BUILD acceptance r8 — SEAT2 (ChatGPT sol) verdict

Banked by the driver from the seat thread (chatgpt.com project conversation
`<id>`, read via wait_quiesced 2026-08-16, textLen 15,333,
truncated: false, FINAL VERDICT line present). Packet
`MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r8.md @ dc06bae`; review target content pin
`575fb38`. Verdict verbatim below.

---

NO-GO

EXECUTED verdict. I read <repo>-build\MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r8.md at full packet commit dc06baeff1fb3f26f984f2f8ce2e542f842b17e0 and reviewed the content pinned by §2 at 575fb38baf331fe8acd721c05848d59251e9c710.

Pin discipline is clean. After 575fb38…, the reviewed Python is unchanged; git diff --stat 575fb38 HEAD -- '*.py' is empty, there are no tracked worktree changes, and the working-tree r8 packet exactly matches its pinned blob 6ca6426f1b18bc3ba889218695b5aa0928c299a4. Three untracked r8 seat/helper files were visible by name only and were not opened. The no-threat-model grep again returned zero hits.

The exact clean-room pair named by the packet, 575fb38… / c4442ae145709751cebc17af632cacacf33db135, reconstructs with exit 0. A deliberately mixed-generation probe using the packet commit's newer manifest blob failed, as it should; I did not count that as evidence against the artifact.

Execution gates

BUILD: 188/188 OK, exit 0.

Frozen: 156/156 OK, exit 0.

verify-build-bundle.py: exit 0.

Pinned reconstruction 575fb38… / c4442ae1…: exit 0.

Internal shelf spot-run:
first_member_baseline|baseline_counter|prefix\.interval|TracePmc|InstructionRetired
over bridge src/, Photon crates/, Gravity src/: zero files in all three.

No live ETW session, Job Object, physical enable variable, or smoke execution.

The r7 totality fold is correct. The stop-only prefix fold fixes its intended r7 false refusal. However, a member/foreign lifetime contradiction is silently accepted, and the supposedly exact PowerShell fence still admits unrelated payloads. Those are fresh shapes outside the 188/156 bank.

Evidence read

Load-bearing pinned bytes:

MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r8.md:7-16,25-74,84-106,108-159@dc06bae

mbcx01_build_etw_consumer.py:1776-1848,1968-2041,2428-2443@575fb38

mbcx01_build_windows_producer.py:164-238,387-442@575fb38

mbcx01_r13_measurement.py:1018-1090@575fb38

mbcx01_build_win32.py:460-490,830-915@575fb38

verify-build-bundle.py:271-302@575fb38

MBCX-01-R13-AMENDMENT-3-FIRST-MEMBER-INTERVAL-BASELINE-2026-08-16.md:65-97@575fb38

MBCX-01-BUILD-SMOKE-RUNBOOK.md:62-91@575fb38

test_mbcx01_build_measurement.py:390-438@575fb38

MBCX-01-BUILD-ACCEPTANCE-ROUND-r7-SYNTHESIS.md:48-92@575fb38

WHY THIS EXISTS

ALREADY-BUILT — EXECUTED / SEARCHED. The underlying Windows capability exists: Microsoft documents event-attached PMC values, including InstructionRetired on CSwitch; the bespoke component remains MBCX's signed member-attribution/evidence join. My required internal shelf spot-run independently returned zero matching files in all three Moonwalker repositories, so there is no missed internal baseline/scope implementation to adopt.

PRODUCT-FIT — READ-ONLY / UNSEARCHED — SETTLED-BY-PINNED-BYTES. Yes. This remains fail-loud scientific measurement, not prevention. Customer need: produce a number whose supporting physical evidence is complete and internally consistent, or explicitly refuse the number.

BIGGER-THAN-THE-BUG — READ-ONLY / UNSEARCHED — SETTLED-BY-PINNED-BYTES. No. The reviewed folds are narrow changes to existing scope, validator, producer, and verifier-fence code. The fixes below remain leaf/bounded changes.

PRIMARY-CONSUMER — READ-ONLY / UNSEARCHED — SETTLED-BY-PINNED-BYTES. The inference/engineering layer and owner consume the signed physical receipt. Total baseline coverage now lets them reproduce every observed processor's first delta rather than confusing absence with capture-start.

Findings
F1 — EXECUTED / SEARCHED — member/foreign TID lifetime overlap is silently admitted

Data consequence: ADMITS WRONG EVIDENCE and can attribute a counter delta under mutually contradictory thread ownership.

The r7 stop-only fold correctly derives a leading foreign ThreadStop as capture-prefix lifetime (0, stop_qpc). Microsoft establishes the two load-bearing facts behind that derivation: a TID is system-wide unique while its thread exists, and it may be reused only after termination; Microsoft also explicitly models threads already running when collection begins.

The new scope then gives the member branch precedence when both a member and foreign interval contain the CSwitch QPC.

I constructed:

foreign stop-only TID 900:
    derived lifetime 0..50

member TID 900:
    lifetime 40..80

CSwitch:
    qpc 45, TID 900
    qpc 70, TID 900

That raw evidence is internally impossible: the same system-wide TID says a foreign thread remains alive through 50 while the member thread already owns it from 40.

Current full capture/session assembly:

foreign_intervals = {900: [(0, 50)]}
member_lifetime   = TID 900, 40..80

scoped_records = [qpc 45, qpc 70]
excluded       = []

SESSION_ADMITTED_OVERLAP = True
deltas = [0, 300]

No downstream roster fault sees it, because the contradictory foreign interval is discarded from the signed evidence after scope classification.

The member-first rule succeeds at its narrow goal—it never moves member work out—but it masks an impossible ownership overlap instead of naming it. There is no actor-evasion premise here: this is an internally contradictory trace being accepted as measurement input.

Fix class: ETW_MEMBER_FOREIGN_TID_INTERVAL_DISJOINTNESS.

Bounded fix: when member and known-foreign intervals for the same TID overlap, refuse the contradictory trace by name before CSwitch attribution. No new machine or schema.

F2 — EXECUTED / UNSEARCHED — SETTLED-BY-PINNED-BYTES — the "exact" pwsh fence still accepts unrelated PowerShell execution

Data consequence: ADMITS WRONG BUILD-VERIFICATION EVIDENCE.

verify-build-bundle.py:282-300 says pwsh is permitted for exactly the bw86 witness shape. The fold now checks five argv parts and a fullmatch payload regex, but the regex contains:

'[^']*run-smoke-cell\.ps1'
...
-Execute .*

Fresh direct probes against ExecutionPosture.check():

real witness-shaped argv:
    ACCEPT

different script:
    C:\repo\evilrun-smoke-cell.ps1
    ACCEPT

real script followed by another command:
    ... run-smoke-cell.ps1 -Execute -X 1; Write-Output EXTRA
    ACCEPT

wrong -File argv:
    REFUSE

extra sixth argv:
    REFUSE

Thus the fold closed the r7 argv-count/switch bypasses but not script identity or single-command identity. A benign maintainer/test change can execute a different script whose filename merely ends in run-smoke-cell.ps1, or append another PowerShell statement, while verify-build-bundle.py still reports a clean execution posture.

This is not a malicious-child-process argument. The verifier claims what it itself executed was within the reviewed set; these bytes prove that claim false.

Fix class: EXECUTION_POSTURE_PWSH_SCRIPT_IDENTITY_AND_SINGLE_COMMAND.

Leaf fix: bind the allowance to the actual reviewed launcher path/command grammar, not a suffix plus unrestricted tail.

Item 1 — totality fold: no finding

Fresh two-processor probe:

processor 0:
    predecessor 100
    first member 600
    next member 800

processor 1:
    capture begins at first member 4000
    next member 4050

baselines:
    p0 = 100
    p1 = 4000

observed processor set = [0,1]
baseline processor set = [0,1]
deltas = [(0,500), (0,200), (1,0), (1,50)]

The capture-start case is now explicit rather than absent: its baseline is its own first counter.

I removed cswitch_first_member_baselines from an otherwise complete SimulatedCollection construction. Current code refused immediately:

TypeError: missing required positional argument:
'cswitch_first_member_baselines'

I also removed all baseline rows from a signed receipt that still had observations; the current semantic validator returned INSTRUCTION_ACCOUNTING_INCOMPLETE.

The constructor census found only two SimulatedCollection(...) creation paths. The fixture path copies the baseline evidence from the trace (test_mbcx01_build_measurement.py:427-428); the smoke path uses **collection, and win32.collect() returns session.first_member_baselines after close_trace_window() has run the scope finalizer (mbcx01_build_win32.py:865-908; consumer :2438-2442). I found no synthetic pacifier () at the producer boundary.

EtwPmcSession.first_member_baselines still has an initial () default because the live session exists before the trace is finalized, but the production order fills it at the terminal barrier before consume_cswitch(). Frozen totality would in any case reject an observed processor lacking its baseline.

Item 4 — residual declarations: confirmed

Baseline trust residual — EXECUTED. I reproduced the declaration precisely. Starting from a valid receipt:

lower the baseline and recompute the first delta/aggregate consistently → _receipt_errors() returns []; the signed count inflates;

baseline above the first counter → INSTRUCTION_ACCOUNTING_INCOMPLETE.

So the amended document is correct that the receipt can bound a bad baseline from above but cannot prove the source baseline was not too low; the raw predecessor truth is outside the receipt.

DPC/ISR residual — READ-ONLY / SEARCHED. Bruce Dawson's first-hand CSwitch-PMC implementation describes per-CPU differencing against the outgoing thread and specifically warns that interrupts/DPCs dirty those counters. Microsoft independently exposes -exc_dpcisr specifically to remove DPC/ISR time from process/thread reports derived from context-switch data. The declaration therefore states a real measurement contaminant and appropriately does not pretend the current harness can quantify it before the physical run.

Version-gate residual — READ-ONLY / SEARCHED. The runbook now explicitly says a new real thread-event version consumes the run, then requires TDH inspection of that host's template, witnessed extension of the verified set, and a fresh council round. Microsoft documents currently-running-thread enumeration at session start and event types separately; refusing an unverified schema rather than guessing remains consistent with the previously settled gate.

F7 roster fault — EXECUTED. Fresh malformed rows no longer leak raw KeyError/TypeError:

{'thread_id':900}
 → CollectorFault ETW_THREAD_ROSTER_ROW_INVALID:KeyError(...)

None
 → CollectorFault ETW_THREAD_ROSTER_ROW_INVALID:TypeError(...)

missing ended_qpc
 → CollectorFault ETW_THREAD_ROSTER_ROW_INVALID:KeyError(...)

Posture unchanged, fault now named.

Four explicit rulings

1. ACCEPT — totality rule. Every observed processor now has an explicit baseline, capture-start is represented by a self-baseline, baseline-set equality is enforced, and omission at the producer boundary faults before signing. My item-1 vote supports owner ratification of the amended AMENDMENT-3 totality/arithmetic shape on issue #27.

2. CHANGE — stop-only prefix classification. The intended stop-only case is fixed and multi-stop ambiguity remains fail-loud, but a known foreign prefix overlapping a member lifetime for the same TID is silently resolved in favor of the member instead of refusing the impossible evidence.

3. CHANGE — exact pwsh fence. Five-part argv tightening landed, but the script regex accepts evilrun-smoke-cell.ps1 and accepts extra commands after the launcher invocation. It is not yet exact.

4. ACCEPT — residual declarations. The downward-baseline trust residual, DPC/ISR contamination, version-gate-fired procedure, and F7 named roster fault all match the current bytes and my fresh probes.

SWEEP LOG

Exact queries:

site:learn.microsoft.com ETW ThreadStart ThreadStop DCStart thread already running trace start Thread_V2
site:learn.microsoft.com PsGetThreadId thread ID reused after thread terminated
site:learn.microsoft.com EVENT_HEADER_EXT_TYPE_PMC_COUNTERS current counter values CSwitch InstructionRetired
Bruce Dawson CPU performance counters interrupts DPC context switch PMC Windows
easyperf Windows performance counters DPC interrupts context process counters CSwitch

Opened at origin:

learn.microsoft.com/.../nf-ntddk-psgetthreadid — Remarks: TID is system-wide unique and can be reused after termination. Deciding source for F1.

learn.microsoft.com/en-us/windows/win32/etw/thread-v2 — Remarks / event types: END identifies thread termination and collection-start events enumerate threads already running. Supports the stop-only prefix model.

learn.microsoft.com/en-us/windows/win32/api/evntcons/ns-evntcons-event_header_extended_data_item — PMC_COUNTERS carries current counter values. Confirms AMENDMENT-3's differencing basis.

learn.microsoft.com/.../windows-hardware/test/wpt/cswitch — -exc_dpcisr explicitly excludes DPC/ISR from process/thread context-switch reports. Supports the declared contamination residual.

randomascii.wordpress.com/2016/11/27/cpu-performance-counters-on-windows/ — first-hand CSwitch-PMC implementation: per-CPU previous-value differencing, outgoing-thread attribution, and DPC/interrupt counter contamination.

easyperf.net/blog/2019/02/23/How-to-collect-performance-counters-on-Windows — independent practitioner reproduction of PMC+CSwitch differencing on Windows.

I stopped because the only external facts needed by these four narrow surfaces were settled. Totality and the pwsh fence are pure pinned-byte questions; additional web material would not change them.

Omission attack

I found no third producer-baseline omission path: all SimulatedCollection constructors either receive real trace evidence or fail construction; the live session's temporary empty baseline is populated before consumption and frozen equality prevents it becoming a valid receipt.

I did find the unbanked member/foreign-overlap shape in F1 and the still-open regex boundary in F2. Those are the omission attack's material results.

Two source comments still describe capture-start as "no baseline row" despite the r7 totality fold now emitting a self-baseline. That prose is stale, but it has no wrong-number/admission/refusal consequence and therefore does not qualify as a §0 finding.

Residual risks

The consumer remains untested against a live ETW/PMC session. PMU availability, same-session behavior, event loss, real host versions, and actual DPC/ISR magnitude remain physical-smoke questions.

AMENDMENT-3's baseline is still trusted source evidence: too-low source data can inflate the first interval and no receipt-internal check can reconstruct the raw predecessor. That is now accurately declared.

DPC/ISR contamination remains systematic upward noise in the CSwitch-PMC attribution model and is likewise accurately declared.

Fix classes

ETW_MEMBER_FOREIGN_TID_INTERVAL_DISJOINTNESS

EXECUTION_POSTURE_PWSH_SCRIPT_IDENTITY_AND_SINGLE_COMMAND

Both are bounded changes to existing functions. Neither needs a new machine, schema, or subsystem.

Because item 2 and item 3 are CHANGE rulings, packet §13 requires fold + fresh confirm. The r7 totality remedy itself is confirmed and my item-1 ruling supports AMENDMENT-3 ratification, but this r8 arc is not yet clean enough to advance to the codex gate.

FINAL VERDICT: NO-GO.
