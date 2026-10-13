NO-GO

Verdict basis: **EXECUTED**. The pinned build can turn an incompletely drained ETW stream into a count, and the unexecuted physical path contains independent attribution, ABI, and provenance defects.

## Pin and review scope

At review start, `git rev-parse HEAD` returned the required packet pin `de49049c92c53f9bde7c6ba7451d4a84e1c814d9`.

During review, `HEAD` moved externally to `bc9997c3c9788c40256256298090e83781deec01`, adding only the dispatch receipt and prompt. I made no repository changes. I rechecked the packet blob and every load-bearing source blob: they still match the packet at `de49049…` and target `4c7056e524b16a8b0395d8853f71e4a9ac6982fc`. All working-tree executions therefore used bytes identical to the pinned target.

## Build-decision challenge

1. **ALREADY-BUILT — EXECUTED — SEARCHED.**  
   The packet carries a substantive internal-shelf log at `MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r4.md:278` and `MBCX-01-BUILD-SHELF-LOG.md:14`. I spot-ran its exact `EVENT_TRACE|TracePmc|CSwitch|ProcessTrace` query across `agentvault-mcp-bridge/src`, `Photon/crates`, and `Gravity/src`; all three returned zero files. No exact Job-scoped, signed Moonwalker instrument exists internally.

   The exact end-to-end instrument was not found externally either, but its raw acquisition subsystem already exists: Microsoft WPR/Xperf supports `InstructionRetired` attached to `CSwitch`, including strict registration. `wpr.exe` is installed locally as version `10.0.26100.8875`. The broad packet claim that the instrument is “bespoke by necessity” is therefore too strong: the custom authority/signing join is novel, while PMU/CSwitch acquisition should adopt or explicitly reject the named Windows mechanism. [Microsoft: Recording Hardware Performance (PMU) Events](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/recording-pmu-events)

2. **PRODUCT-FIT — READ-ONLY.**  
   Customer need, in one sentence: the experiment owner needs a verifiable, fail-loud measurement of the exact retained workload’s process tree so missing or stale evidence cannot be mistaken for a scientific result.

   That is GOVERNED POWER / FAIL-LOUD / MIRROR-NOT-COP, not a prevention or completeness promise. The intended product fit is sound; the current stop/drain implementation violates it by accepting partial evidence.

3. **BIGGER-THAN-THE-BUG — READ-ONLY — SEARCHED.**  
   The authority joins are proportional to I11/I12’s physical-evidence requirement. The hand-written ctypes ETW controller, however, is a new subsystem for a raw collection mechanism Windows already supplies through WPR/Xperf. That part should have re-entered the design gate with an adopt-or-why-not decision, rather than relying on the narrower “no exact instrument found” conclusion.

## Evidence read

Pinned or blob-confirmed target bytes:

- `MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r4.md:5`, `:45`, `:78`, `:100`, `:195`, `:239`, `:259`, `:278`, `:308`
- `MBCX-01-EXPERIMENT-DESIGN-r9.md:40`, `:50`, `:64`
- `MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md:5`, `:11`, `:20`, `:85`
- `MBCX-01-R13-CLOSURE-ARCHITECTURE.md:70`, `:108`
- `mbcx01_build_etw_consumer.py:159`, `:764`, `:937`, `:1214`, `:1285`, `:1513`, `:1614`, `:1695`, `:1731`, `:1799`, `:1857`
- `mbcx01_build_win32.py:500`, `:527`, `:683`
- `mbcx01_build_trust_anchor.py:270`, `:319`, `:436`, `:540`
- `mbcx01_build_exactness_authority.py:24`, `:149`, `:167`
- `MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md:134`
- `MBCX-01-OPEN-ISSUES.json:173`, `:199`
- `MBCX-01-BUILD-PIN-MANIFEST.json:5`, `:241`
- `verify-build-pinned.ps1:44`
- Microsoft Windows SDK 10.0.26100.0 `um/evntcons.h:51`, `:148`
- Microsoft Windows SDK 10.0.26100.0 `shared/evntrace.h:1416`, `:2147`, `:2345`

## Sweep log

Exact queries and opened sources:

- `site:learn.microsoft.com Windows ETW CSwitch kernel provider all context switch events EVENT_TRACE_FLAG_CSWITCH`  
  Opened [WPA Providers, “NT Kernel Logger” and “Command-line Usage”](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/xperf/wpa-providers), which explicitly says `CSWITCH` logs all context switches on the test system. This page is archived/previous-version documentation, so I corroborated applicability with the current [SystemTraceProvider configuration](https://learn.microsoft.com/en-us/windows/win32/etw/configuring-and-starting-a-systemtraceprovider-session) and current WPR PMU page. It changed the review: the consumer has no Job/TID filtering before handing the global stream to a function that rejects every foreign thread.

- `site:learn.microsoft.com CloseTrace ProcessTrace real time session returns after close trace handle`  
  `site:learn.microsoft.com ProcessTrace CloseTrace same thread real-time events processing`  
  `site:learn.microsoft.com ETW CloseTrace ERROR_CTX_CLOSE_PENDING`  
  Opened [CloseTrace, “Return value” and “Remarks”](https://learn.microsoft.com/en-us/windows/win32/api/evntrace/nf-evntrace-closetrace) and [ProcessTrace, “Remarks”](https://learn.microsoft.com/en-us/windows/win32/api/evntrace/nf-evntrace-processtrace). They establish that `CloseTrace` errors are meaningful and that successful pending close finishes only after queued events are processed. This made the ignored return and unchecked join timeout a scientific-completeness defect, not merely cleanup style.

- `site:learn.microsoft.com "Recording PMU Events" ETW PMC TracePmcEventListInfo`  
  `site:learn.microsoft.com Windows Performance Recorder hardware counter InstructionRetired ETW PMC`  
  Opened [Recording Hardware Performance (PMU) Events, “Collecting PMU Events on ETW Events”](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/recording-pmu-events). It confirmed named prior art: WPR/Xperf already attaches `InstructionRetired` to `CSwitch`.

- `site:learn.microsoft.com/en-us/windows/win32/api/evntcons/ns-evntcons-event_header EVENT_HEADER_FLAG_CLASSIC_HEADER`  
  `github microsoft win32metadata evntcons.h EVENT_HEADER_FLAG_CLASSIC_HEADER`  
  `site:github.com/microsoft evntrace.h ETW_PMC_COUNTER_OWNERSHIP_STATUS`  
  Opened [EVENT_HEADER, “Flags”](https://learn.microsoft.com/en-us/windows/win32/api/evntcons/ns-evntcons-event_header) and the locally installed Microsoft SDK headers. The SDK is the controlling ABI source and exposed three wrong constants plus a published counter-owner structure the source calls unpublished.

- `site:learn.microsoft.com/en-us/windows/win32/procthread/job-objects job object process accounting breakaway`  
  Opened [Job Objects, overview and resource-accounting links](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects). It confirmed Job Objects provide process grouping/accounting, but not the retired-instruction evidence or signing semantics needed here.

Stopped because each narrow load-bearing vendor question was settled by Microsoft’s current documentation or the installed Microsoft SDK header; no conflicting jurisdictional, regulatory, or research claim remained.

## Findings

1. **EXECUTED — SEARCHED — deciding: partial ETW capture becomes a count.**  
   `EtwPmcConsumer.stop()` ignores `CloseTrace`’s return, changes the handle to invalid unconditionally, joins for 30 seconds without checking whether the pump stopped, then returns loss counters (`mbcx01_build_etw_consumer.py:1513`). `capture()` checks callback faults but not pump completion (`:1857`).

   My fresh probe injected `CloseTrace → ERROR_INVALID_HANDLE`, a consumer thread still alive after the join, zero loss counters, and two complete-looking records. `stop()` and `capture()` accepted them; `consume_cswitch()` produced a signed-path-compatible retired-instruction delta of `700`. Microsoft’s contract says invalid handle is failure and a pending successful close completes only after queued events are processed. The “never a partial roster/stream presented as complete” claim is false.

2. **EXECUTED — SEARCHED — the physical consumer cannot currently complete a normal trace.**

   - `_decode_kernel_process_event()` emits every thread event with `"process_start_key": None` (`mbcx01_build_etw_consumer.py:1824`). `assemble_thread_lifetimes()` immediately normalizes that value as a required start key (`:953`). A fresh probe using the decoder’s exact emitted shape failed with `ETW_PROCESS_START_KEY_INVALID:None`.
   - The callback appends every matching CSwitch record (`:1743`). Microsoft documents this kernel flag as a system-wide context-switch stream. `consume_cswitch()` rejects any `OldThreadId` outside the Job roster as `ETW_CSWITCH_UNATTRIBUTED_THREAD` (`mbcx01_build_win32.py:527`). Normal foreign processes therefore make the live path fault.
   - These are fail-loud rather than false-number failures, but they show the physical implementation is not acceptance-ready.

3. **EXECUTED — SEARCHED — Q6’s FLAGGED-constants claim is false.**  
   The static structure-layout verifier passed, but comparison with Microsoft SDK 10.0.26100.0 found:

   - `EVENT_HEADER_FLAG_CLASSIC_HEADER`: code `0x0040`; SDK `0x0100`. `0x0040` is `EVENT_HEADER_FLAG_64_BIT_HEADER`.
   - `EVENT_HEADER_EXT_TYPE_PROCESS_START_KEY`: code `0x000A`; SDK `0x000D`.
   - `EVENT_HEADER_EXT_TYPE_EVENT_KEY`: code `0x000B`; SDK `0x000A`.
   - `EVENT_HEADER_EXT_TYPE_PMC_COUNTERS=0x0008` is correct.

   The smoke runbook’s verification set at `MBCX-01-BUILD-SMOKE-RUNBOOK.md:85` does not list the three mismatches. Additionally, `_count_counter_owners()` calls `TraceQueryInformation` with a null input and treats an opaque nonzero buffer as one conflict (`mbcx01_build_etw_consumer.py:1614`), while `evntrace.h:2345` publishes the required `ETW_PMC_COUNTER_OWNERSHIP_STATUS` input, processor number, sizing law, and output structure. The comment that this layout is unpublished is false.

4. **READ-ONLY — pin provenance does not authenticate the review target.**  
   The review target is `4c7056e…`, but `MBCX-01-BUILD-PIN-MANIFEST.json:5` governs `3527f510…`. `verify-build-pinned.ps1:55` requires the supplied commit to equal that older value and reconstructs subjects from it.

   Between those commits, `mbcx01_build_win32.py`, the ceremony, and the smoke runbook changed. For example, the manifest pins `mbcx01_build_win32.py` blob `25d04d5…`, while the target contains `7dc6096…`. The runtime-file difference is comment-only, so this does not create the scientific bypass, but the current clean-room claim is not a byte proof of the exact target.

5. **EXECUTED — Q1/Q2 joins held under fresh attacks.**  
   A rehashed retained-position substitution made I01 false and scored `0`. A six-binding receipt with two bindings reordered and both container hashes repaired was rejected as `SCENARIO_OUTCOME_AUTHORITY_INVALID`.

6. **EXECUTED — Q3/Q4/Q7 held.**  
   A fresh 17-character PEM rewrap of the committed fixture key, relabelled production, was refused as `PRODUCTION_VERIFIER_CONTEXT_FIXTURE_KEY_MATERIAL`. A production-shaped manifest evaluated at `2031-01-01T00:00:00Z` was refused as `TRUST_ROOT_VALIDITY_EXPIRED`. A receipt claiming `PASS` was refused as `CARRIER_EXACTNESS_SUITE_NOT_EXECUTED`.

7. **EXECUTED — Q8 witnesses discriminate.**  
   In-memory deliberate breaks made each selected witness red:

   - State `ba16`: one failure
   - Measurement `bw22`: one failure
   - Exactness `bw16`: one failure
   - ETW `bw34`: one failure

   No files were modified.

8. **EXECUTED — Q9 disclosure is accurate, with a procedural residual.**  
   I derived the public half of committed `FIXTURE_NON_ANCHOR_PRIVATE_KEY_PEM`; it is absent from `committed_fixture_key_material()`, and an ordinary production context accepted it. Thus gap 1 is technically real.

   The ceremony as written requires the owner root and signing keys to be freshly generated inside custody backends and expressly forbids copying committed keys (`MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md:136`, `:168`). Gaps 1 and 2 are therefore unreachable under a conformant ceremony but reachable after human procedure violation. Gap 3—raising rather than returning a code on the OS path—is fail-loud and consistent with the configuration-boundary rule. The existing disclosure is sufficient, but it is procedural, not technical closure.

9. **READ-ONLY — governing design has no threat model.**  
   A pinned grep for `threat model|adversary|attacker|untrusted|api-caller|hostile` across the experiment design, closure architecture, and invariant matrix returned zero hits. This is a scientific-validity review, not a security review. The packet’s recut is correct. Its cited `DESIGN-SHELF-MAP.md §1` does not exist at the target, so that T2-ceiling provenance cannot be spot-checked.

## Execution record

- BUILD suites: `114` tests, all OK.
- Frozen r13 suites: `145` tests, all OK.
- `verify-build-bundle.py`: exit `0`; ledger `44` invariants / `114` witnesses, two-way total true; readiness remained `BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`.
- Committed trustboot, fixture-key, and fixture-isolation probes: all exit `0`.
- Fresh Q1–Q9 probes: executed as described above.
- No ETW session, Job Object, physical authorization flag, provider call, or smoke run was started.

## Residual risks

- The owner-authorized elevated smoke run remains unexecuted; same-session delivery, platform payload offsets, actual PMU availability, and hardware behavior remain **UNDETERMINED**.
- The exactness suite runner remains deliberately unbuilt; current bytes correctly refuse to call binding-only evidence `PASS`.
- The generic in-process `object.__setattr__`/arbitrary-code actor remains accepted because no governing security threat model exists.
- The non-anchor committed-key and committed signing-key cases remain human-ceremony footguns.
- The archived WPA page’s explicit system-wide wording is old; current WPR/SystemTraceProvider material and the installed SDK corroborate the mechanism, but the physical smoke must still prove this host.

## Required fix class

**ETW stream-completion and Job-attribution correctness + vendor-ABI derivation + exact-target pin regeneration.**

The build test list must include:

- non-successful `CloseTrace`, a join timeout, and a still-running `ProcessTrace` must make capture unavailable;
- the physical decoder’s actual thread-event shape must join successfully or refuse before collection is presented as runnable;
- normal foreign system CSwitch records must not invalidate or corrupt Job attribution;
- all ETW constants and counter-owner structures must be checked against the Windows SDK ABI;
- the pin manifest and clean-room launcher must authenticate the exact accepted target commit.
