# MBCX-01 BUILD acceptance r7 — SEAT2 (ChatGPT sol) verdict

Banked by the driver from the seat thread (chatgpt.com project conversation
`<id>`, read via wait_quiesced 2026-08-16, textLen 19,410,
truncated: false, FINAL VERDICT line present). Packet
`MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r7.md @ cbab20b`; review target content pin
`abcab342` (seat confirmed the pin and the records-only tail; packet blob hash cross-checked).
Verdict verbatim below.

---

NO-GO

Verdict basis: EXECUTED. I read MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r7.md at packet commit cbab20bc81337c0a8b7c9e02eef2c4ce1f226d9f and reviewed content commit abcab342802be20ba0bb15652c54340d4dededd4.

Pin discipline is clean. abcab342… → cbab20bc… changes only the regenerated BUILD pin manifest plus the r7 packet; git diff --stat abcab342 HEAD -- '*.py' is empty; there are no tracked working-tree changes. The working-tree packet hashes to the exact pinned Git blob 8c645bb9fa4b1c3041c70189f9044ef69ba3f5b4. One untracked r7 seat log was visible by name only and I did not open it. I read source from the working tree only after confirming it matches the content pin.

Section 0 is satisfied and enforced: my independent grep of the three governing design files again produced zero threat-model/adversary hits. All findings below terminate in wrong number, wrong evidence admission, or refusal of right evidence. None depends on a malicious caller.

The r6 folds materially improved the artifact, and the core AMENDMENT-3 baseline arithmetic is correct. But AMENDMENT-3 is not ready for owner ratification: its producer boundary silently converts a missing new observation into a legitimate capture-start empty baseline and can admit a retired-instruction total wrong by 1,000,000. Separately, the lifetime-aware scope still falsely refuses a legal stop-only foreign lifetime that is actually disambiguable. I also found the claimed "exact" PowerShell spawn-fence shape is not exact.

Execution record

I independently ran the banks on the reviewed bytes:

BUILD: 186/186 OK, exit 0.

Frozen r13.2: 155/155 OK, exit 0.

verify-build-bundle.py: direct exit 0.

Clean-room verify-build-pinned.ps1 -Commit abcab342… -ManifestBlob 9fa1440d212a0a78fb1ce7eb138cc0b4af99a407: direct exit 0.

Internal no-threat-model grep: zero hits.

Internal shelf spot-run first_member_baseline|baseline_counter|TracePmc|InstructionRetired over bridge src/, Photon crates/, Gravity src/: zero files in all three.

I did not start ETW, create a Job Object, set MBCX01_BUILD_ALLOW_PHYSICAL, or execute run-smoke-cell.ps1.

Evidence read

Load-bearing bytes included:

MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r7.md:7-29,38-66,68-177,192-251@cbab20bc

MBCX-01-R13-AMENDMENT-3-FIRST-MEMBER-INTERVAL-BASELINE-2026-08-16.md:17-80,82-117@abcab342

MBCX-01-R13-CLOSURE-ARCHITECTURE.md:72-106@abcab342

mbcx01_build_etw_consumer.py:1744-2051,2272-2345,2368-2440,3165-3176@abcab342

mbcx01_build_win32.py:650-688,850-897@abcab342

mbcx01_build_windows_producer.py:164-233,387-438@abcab342

mbcx01_r13_measurement.py:949-1078@abcab342

mbcx01_smoke_cell.py:170-290,390-443,529-625,682-850@abcab342

verify-build-bundle.py:230-289@abcab342

test_mbcx01_build_measurement.py:3583-3668,3790-3920,4106-4155@abcab342

test_mbcx01_r13_measurement.py:502-580@abcab342

test_mbcx01_build_integration.py:989-1096@abcab342

WHY THIS EXISTS

1. ALREADY-BUILT? — EXECUTED / SEARCHED. Basic acquisition is already-built Windows capability: Microsoft's WPR/WPT documentation explicitly supports attaching InstructionRetired hardware counters to CSwitch. What is first-of-kind here is MBCX's signed, Job-member-scoped evidentiary join. The packet carries the required internal-shelf log, and my independent spot-run found no TracePmc/InstructionRetired/baseline sibling in the three Moonwalker repos. No missing library/subsystem should replace these folds.

2. PRODUCT-FIT? — READ-ONLY / UNSEARCHED — SETTLED-BY-PINNED-BYTES. Yes: fail loud when the measurement cannot be defended; do not pretend to make execution impossible or globally complete. The customer need in one sentence is: produce a defensible bounded-work measurement for each experimental cell, or explicitly refuse to claim a number.

3. BIGGER-THAN-THE-BUG? — READ-ONLY / UNSEARCHED — SETTLED-BY-PINNED-BYTES. No. AMENDMENT-3 is one new signed trace fact plus seeded arithmetic. The fixes below remain changes inside existing producer/scope/fence functions. No new engine, lock service, or evidence subsystem is warranted.

4. PRIMARY-CONSUMER? — READ-ONLY / UNSEARCHED — SETTLED-BY-PINNED-BYTES. The inference/engineering-selection layer and ultimately the owner consume the signed physical receipt. The bounded read buys them the physical gate result, including the 500,000-instruction max-minus-min H threshold at fixed (D,F) (MBCX-01-R13-CLOSURE-ARCHITECTURE.md:89-106).

Findings
F1 — EXECUTED / UNSEARCHED — SETTLED-BY-PINNED-BYTES — AMENDMENT-3 silently defaults a missing baseline observation

Data consequence: PRODUCES AND ADMITS A WRONG NUMBER.

AMENDMENT-3 says the old shape is unrepresentable and that a missing baseline cannot silently recreate the old undercount. The frozen receipt does require cswitch_first_member_baselines. The producer boundary does not.

mbcx01_build_windows_producer.SimulatedCollection says at :168-173 that observations may never be substituted, defaulted, or estimated. Yet at :229-233:

cswitch_first_member_baselines: tuple[...] = ()

The real smoke path converts win32.collect() output with:

producer.SimulatedCollection(**collection)

at mbcx01_smoke_cell.py:429-430.

I first exercised the actual scoped arithmetic from a raw stream:

foreign predecessor : raw 100
first member switch : raw 1,000,100
second member switch: raw 1,100,100

derived baseline = [{processor:0, counter_value:100}]
truthful deltas  = [1,000,000, 100,000]
truthful total   = 1,100,000

That part is correct. Microsoft's ETW documentation says the PMC extended item carries the current counter values, and OldThreadId is the previous/outgoing thread, so differencing those event-attached values is the right basic arithmetic.

Then I reconstructed the pre-AMENDMENT-3 internal caller shape: omit the new constructor argument entirely, retain the same scoped counters, use the former first-delta-zero arithmetic, and let the current producer construct and sign it.

Executed result:

truthful receipt:
  baseline = 100
  retired  = 1,100,000
  semantic errors = []

old caller shape:
  baseline argument OMITTED
  SimulatedCollection silently supplies ()
  deltas   = [0, 100,000]
  retired  = 100,000
  semantic errors = []

wrong by = 1,000,000

I then substituted this exact old-shape cell into the otherwise valid 100-cell production-shaped grid, configured the normal independent test-production anchor, signed it through the current producer, and ran full admission:

full_production_admission_errors = []

That is twice the frozen 500,000 boundedness threshold. This is not an attacker bypass. It is precisely an internal harness caller forgetting a newly required observation, which the producer currently converts into the semantically distinct statement "there was no predecessor because this was capture-start."

Fix class: AMENDMENT3_BASELINE_OBSERVATION_REQUIRED_AT_PRODUCER_BOUNDARY.

Smallest repair: make cswitch_first_member_baselines a required collection field rather than a default, and bank the migration red: a pre-AM3 caller omitting it must fail before signing. An explicitly observed legitimate () remains representable for actual capture-start.

This finding means CHANGE AMENDMENT-3; do not ratify the current draft as complete.

F2 — EXECUTED / SEARCHED — stop-only foreign lifetime is falsely classified as unknowable

Data consequence: REFUSES RIGHT EVIDENCE.

foreign_thread_intervals() at mbcx01_build_etw_consumer.py:1776-1826 intentionally creates no lifetime for a foreign ThreadStop that has no observed ThreadStart.

That is too conservative for the capture prefix.

Windows thread IDs are system-wide unique while the thread is live and may be reused after termination. Microsoft also defines a thread END event as the end of a thread and separately has a data-collection-start event for threads already running when collection begins.

Fresh production-path shape:

foreign host TID 900 existed before trace
foreign ThreadStop: tid=900, qpc=50

later measured member:
  ThreadStart tid=900 qpc=60
  ThreadStop  tid=900 qpc=90

CSwitch:
  qpc=40 tid=900   # foreign pre-existing thread
  qpc=70 tid=900   # measured member

The first event is not ambiguous: at QPC 40 the later member does not yet exist, the foreign incarnation terminates at 50, and Windows does not simultaneously assign one live TID to another thread. The ID can be reused only after termination.

Current full CapturedTrace → build_etw_pmc_session → consume_cswitch result:

scoped_records:
  qpc 40 / tid 900
  qpc 70 / tid 900

excluded_foreign_cswitch_records = 0
kept_roster_tid_outside_any_lifetime = 1

CollectorFault:
  ETW_CSWITCH_UNATTRIBUTED_THREAD

So the first real smoke can still be destroyed by an ordinary thread that predates trace start and whose ID is later reused by the measured process.

The fold already has the required evidence. This needs no new source or subsystem: represent a start-less foreign stop as a capture-prefix interval through its stop, then classify matching earlier-in-capture switches as foreign. If ETW reports event loss, the whole measurement already faults elsewhere, so this need not guess across missing data.

Fix class: ETW_FOREIGN_STOP_ONLY_PREFIX_INTERVAL.

This is a CHANGE to the scope classification rules, so packet §13 independently requires another targeted round.

F3 — EXECUTED / UNSEARCHED — SETTLED-BY-PINNED-BYTES — PowerShell spawn allowance is broader than its claimed exact shape

Data consequence: ADMITS WRONG BUILD-VERIFICATION EVIDENCE.

verify-build-bundle.py:277-285 says PowerShell is allowed for exactly the bw86 launcher-refusal command shape and that a blanket allowance would gut the execution fence.

The implementation is:

name is pwsh/pwsh.exe
AND any argument contains "run-smoke-cell.ps1"

I invoked the fence's own check() directly with recorded command arrays—no subprocesses were run:

ACCEPTED:
  pwsh -NoProfile -File run-smoke-cell.ps1

also ACCEPTED:
  pwsh -NoProfile -Command "Write-Output harmless" run-smoke-cell.ps1

also ACCEPTED:
  pwsh -NoProfile -File totally-other-script.ps1 run-smoke-cell.ps1

All three return an execution-posture PASS. Thus a verification run can execute an unrelated PowerShell target and still bank evidence saying its process posture was clean merely because another argument contains the launcher filename.

No hostile actor is needed; a test or maintainer can accidentally acquire an unrelated pwsh subprocess and the gate will fail to report it.

Fix class: EXECUTION_POSTURE_PWSH_EXACT_ARGV_SHAPE.

Leaf repair: recognize the actual -File <reviewed run-smoke-cell.ps1> invocation shape/path, not a filename substring anywhere in argv.

Rulings — all six agenda items
1. AMENDMENT-3 baseline arithmetic

CHANGE. The arithmetic itself is correct and my raw-stream probe independently reproduced the intended [1,000,000, 100,000] result, but the producer's default () makes a missing new observation indistinguishable from real capture-start and admitted a total wrong by 1,000,000. Do not ratify AMENDMENT-3 in its current form.

2. Lifetime-aware CSwitch scope

2(a) CHANGE. A foreign ThreadStop with no observed START should describe the in-capture prefix through that stop, not "no interval." Current choice falsely refuses a legal pre-existing foreign thread when its TID is later reused.

2(b) ACCEPT. A roster row lacking interval fields retaining whole-capture behavior is acceptable as a compatibility/fail-safe fallback. The real production roster produced by assemble_thread_lifetimes() always carries both endpoints, so this fallback does not weaken the physical path.

2(c) ACCEPT. A counter that goes backwards on a newly classified foreign interval must remain a fault. My fresh member→known-foreign negative-step probe still returned ETW_PMC_COUNTER_WENT_BACKWARDS; that is correct because the baseline arithmetic cannot be defended from a decreasing current-counter sequence.

2(d) ACCEPT, conditional on 2(a)'s correction. kept_roster_tid_outside_any_lifetime is useful provenance for genuinely unplaceable roster-TID events. My fresh unknown-life probe incremented it to 1 and kept the event for downstream refusal. After 2(a), stop-only prefix cases that are actually placeable must no longer enter this bucket.

3. Thread event version gate

ACCEPT. Fresh probe:

verified versions = [0,1]

version 0 → admitted
version 1 → admitted
version 2 → ETW_KERNEL_THREAD_VERSION_UNVERIFIED
version 9 → ETW_KERNEL_THREAD_VERSION_UNVERIFIED

Microsoft says provider + event ID + event version identifies the manifest event schema and a version change can change field type or add fields. Refusing unverified future versions is therefore the correct fail-loud behavior, not a false refusal of verified evidence.

4. Strengthened smoke criterion

4(a) ACCEPT. Holding only EXTERNAL_WORK_UNMEASURED as one-cell-smoke N/A is narrow and explicit. It is recorded in semantic_not_applicable; a membership defect remains fatal.

4(b) ACCEPT. The registered-coordinate probe on a shallow copy is correct. Fresh real-smoke-shape probe with signed coordinate [0,0,0] returned:

pass = True
semantic_errors = []
not_applicable = [EXTERNAL_WORK_UNMEASURED]
coordinate_probe = [128,1,1]
receipt_unchanged = True

Flipping membership_complete=False on that same shape and re-signing still produced PROCESS_MEMBERSHIP_INVALID and pass=False.

4(c) ACCEPT. The PowerShell launcher checking node before elevation while the elevated Python preflight reads the verifier path directly from frozen measurement.VERIFIER is the right one-source-of-truth split. Fresh probe confirmed signature_verifier_facts()['verifier_path'] == str(measurement.VERIFIER) and the current verifier is present.

4(d) ACCEPT. I executed the persistence sequence in a transient directory: all four UNSIGNED-INCOMPLETE-* artifacts remained after the certified signed-envelope.json was written. The README carries certified:false, and the filename itself marks the artifacts as incomplete. Retaining the raw pre-certification evidence does not admit it as a signed measurement.

5. Banked bw83 expectation / AMENDMENT-3 first interval

ACCEPT. The new [500,200,0,50] expectation is correct.

Fresh stream:

processor 0:
  foreign raw 1000
  member  raw 1500  -> first member delta 500
  foreign raw 2500
  member  raw 2700  -> member delta 200

processor 1:
  first record is member raw 5000 -> no predecessor, delta 0
  next member raw 5050            -> delta 50

total = 750

Microsoft documents event-attached InstructionRetired counters on CSwitch, the extended data contains the current PMC counter values, and CSwitch OldThreadId is the previous/outgoing thread. That makes 1500 - 1000 = 500 the correct first member interval on processor 0.

6. Spawn-fence allowances

6(a) ACCEPT. node.exe joining node is a filename-spelling allowance for the same verifier runtime on Windows; the fence remains closed to other executables.

6(b) CHANGE. The pwsh rule is not "exactly the launcher command shape." My fresh argv probes demonstrated it accepts arbitrary -Command or another -File target whenever any argument contains run-smoke-cell.ps1. Tighten the existing leaf fence to the actual launcher argv/path.

SWEEP LOG

Exact searches:

site:learn.microsoft.com Windows ETW CSwitch OldThreadId previous thread InstructionRetired hardware counters CSwitch
site:learn.microsoft.com EVENT_DESCRIPTOR Version provider event ID version schema ETW
site:learn.microsoft.com PsGetThreadId operating system may reuse thread ID after terminated
site:learn.microsoft.com ETW ThreadStart ThreadStop threads already running at trace start DCStart Thread_V2
site:learn.microsoft.com EVENT_HEADER_EXTENDED_DATA_ITEM PMC_COUNTERS current counter values performance monitoring counters

Opened at origin:

learn.microsoft.com/en-us/windows-hardware/test/wpt/counters — Example explicitly attaches InstructionRetired and TotalCycles to CSwitch; confirmed the acquisition prior art and item 5's event attachment.

learn.microsoft.com/.../windows/win32/etw/cswitch — Properties, especially OldThreadId = Previous thread ID; confirmed which thread owns the interval ending at a switch.

learn.microsoft.com/en-us/windows/win32/api/evntcons/ns-evntcons-event_header_extended_data_item — EVENT_HEADER_EXT_TYPE_PMC_COUNTERS contains the current PMC counter values; confirmed difference-of-observations basis for AMENDMENT-3.

learn.microsoft.com/en-us/windows/win32/api/evntprov/ns-evntprov-event_descriptor — Id/Version; provider + ID + version uniquely identifies a manifest event field schema, and version can alter field details. Confirmed item 3.

learn.microsoft.com/.../windows-hardware/drivers/ddi/ntddk/nf-ntddk-psgetthreadid — Remarks: TID is system-wide unique while live and may be reused after termination. Deciding support for item 2(a).

learn.microsoft.com/en-us/windows/win32/etw/thread-v2 — Remarks/event-type table: END is an end-thread event; data-collection start enumerates already-running threads. I use this only to confirm the Windows thread-lifecycle model, not as a claim that this classic provider is the exact manifest provider decoded by MBCX.

I stopped because the vendor questions load-bearing to this targeted round were settled at Microsoft primary sources. The remaining platform questions—actual PMU grant, live session coexistence, loss behavior, host payloads—still require the owner-authorized elevated smoke and cannot be answered by more documentation.

Residual risks

The physical ETW/PMC path remains unexecuted. Same-session behavior, actual PMU availability/ownership, live loss behavior, root-event delivery, and remaining platform facts stay explicit smoke residuals.

AMENDMENT-3 still treats an explicitly supplied empty baseline list as evidence of capture-start. After F1's fix, that fact remains producer-owned rather than independently reconstructible from the signed scoped stream. I did not find a current honest physical route that supplies false empty data—the current win32.collect plumbing carries session.first_member_baselines—so I am naming this as a residual, not escalating it into another mechanism.

The stop-only prefix classification in F2 assumes an otherwise lossless admitted trace. That is appropriate because any ETW loss already makes the entire measurement unavailable; no inference over a known-loss stream is required.

AMENDMENT-3 remains owner-ratification-pending. On these bytes, my ruling is do not ratify yet.

Fix classes

AMENDMENT3_BASELINE_OBSERVATION_REQUIRED_AT_PRODUCER_BOUNDARY — eliminate the default for the new load-bearing collection observation; omission must fault before signing.

ETW_FOREIGN_STOP_ONLY_PREFIX_INTERVAL — classify stop-only pre-existing foreign TID evidence over the captured prefix through its stop.

EXECUTION_POSTURE_PWSH_EXACT_ARGV_SHAPE — make the PowerShell exception actually match only the intended launcher invocation.

The first is a CHANGE to AMENDMENT-3 and the second is a CHANGE to scope classification. Under packet §13 either one independently triggers fold + fresh council round. The third is leaf-sized.

FINAL VERDICT: NO-GO.
