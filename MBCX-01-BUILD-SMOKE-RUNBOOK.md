# MBCX-01 BUILD — operator runbook for LATER AUTHORIZED smoke testing

Status: BUILD work-product 10. ⛔ Nothing in this runbook is authorized by the BUILD itself.
Executing ANY step in §3 requires a separate, explicit, bounded owner authorization naming
the exact binary, host, cells, evidence destination, cleanup, and expected side effects
(handoff r13.2, Explicit prohibitions). This document exists so that authorization request
can be specific.

## 1. What the BUILD leaves ready

- BUILD A: `mbcx01_build_state_store.py` (durable SQLite store) + adapter + operator-B +
  `mbcx01_build_state_authority.py` (V2 verification / production admission). Fully
  exercisable with fixture keys today — no smoke run needed for BUILD A beyond the suite;
  its "physical" step is only the custody ceremony (see MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md).
- BUILD B: `mbcx01_build_windows_producer.py` (envelope assembly + signing seam, fully
  fixture-tested) and `mbcx01_build_win32.py` (the REAL collector — reviewable code, never
  executed in the BUILD task).
- BUILD B, added 2026-08-14: `mbcx01_build_etw_consumer.py` — the ETW PMC consumer that
  supplies `collect(etw_session_factory=...)`. Until it existed the collector was
  reviewable but UNRUNNABLE and §3 below could not execute at all
  (`MBCX01-BUILD-B-ETW-CONSUMER-UNBUILT`). It is split into a PURE layer (ordering, the
  CSwitch→PMC join, lifetime assembly, the availability rules, the environment gate),
  which the BUILD witness suite exercises against synthetic streams, and an OS layer
  (`EtwPmcConsumer`: `StartTraceW` *without* the CSwitch flag → the two
  `TraceSetInformation` PMC calls → `ControlTraceW(EVENT_TRACE_CONTROL_UPDATE)` enabling
  CSwitch *after* the counter is attached *(sequence corrected 2026-08-17, codex r8 P1 —
  the earlier spelling buffered pre-attachment switches that rejected the whole run)* →
  `EnableTraceEx2` → `OpenTraceW`/`ProcessTrace` on its own thread → `ControlTraceW`
  QUERY/STOP) which — like the collector — was NEVER executed in the BUILD task.
- `mbcx01_smoke_cell.py` + `run-smoke-cell.ps1` — the operator runner for §3, with three
  modes: `selftest` (pure logic + static ABI, no OS state; the ONLY mode the BUILD ran),
  `preflight` (read-only host probes; starts nothing — *as of 2026-08-17, codex r9: it also
  runs ONE read-only WMI query, `Win32_ComputerSystem.HypervisorPresent`, for runtime
  hypervisor evidence, and ABORTS `HYPERVISOR_RUNTIME_POSTURE_UNDETERMINED` if the probe
  cannot answer — an unanswerable probe never signs a bare-metal claim; and it refuses a
  `--command-line` inconsistent with the fixed candidate identity,
  `SMOKE_COMMAND_INCONSISTENT_WITH_CANDIDATE_IDENTITY` — the default and every documented
  spelling are guard-proven untouched*), `execute` (the §3 step).

## 2. Execution guards on the real collector (defense against accidental runs)

`mbcx01_build_win32.collect(...)` refuses to run unless BOTH hold:

1. environment variable `MBCX01_BUILD_ALLOW_PHYSICAL=1`;
2. an authorization-file path argument pointing at a readable owner authorization document
   that contains the literal marker line `MBCX01-BUILD-B-PHYSICAL-COLLECTION-AUTHORIZED`
   (enforced at `mbcx01_build_win32.py`; a file without the marker is refused).

The BUILD task, its tests, and its verifiers never set either. CI-style runs cannot trip it.

## 3. The one-cell smoke proof (the next gate after BUILD review; owner-authorized)

Scope: ONE candidate, ONE cell, on a supported environment (bare-metal Windows or Hyper-V
root partition; a guest needs the explicit PMU capability receipt; nested virtualization is
unsupported and must abort). ⛔ Not the 100-cell grid, not route qualification, not the
experiment.

1. Preconditions: pinned harness build digests recorded (BUILD shelf log / harness_identity);
   PMU capability probe (`TracePmcCounterListInfo` query) succeeds; host facts collected for
   `environment_digest`; **the signing toolchain resolves in the ELEVATED session — preflight
   probes `node` and the frozen verifier script and aborts
   `SIGNATURE_VERIFIER_TOOLCHAIN_UNAVAILABLE` before any ETW/Job work (r6 fold: elevation
   commonly changes PATH resolution, and a missing node after a perfect collection would burn
   the one-shot session); the launcher additionally refuses a shell with no `node` before
   elevation**; fixture signing key ONLY (production signing still requires the
   custody ceremony — a smoke run is fixture-kind evidence by definition and must be labeled
   so; it can NEVER clear production admission, by design).
2. Run: elevated session (ETW kernel PMC needs it), `MBCX01_BUILD_ALLOW_PHYSICAL=1`,
   authorization file in place; invoke the collector for the named candidate binary with the
   cell's H/D/F parameters; the collector enforces suspended-create → job configure →
   completion port → breakaway disabled → assign → resume, and fails FAULT-not-verdict on any
   native error.
3. Evidence destination: a NEW directory named in the authorization; the signed envelope(s),
   raw query buffers, and the collector's transcript land there and nowhere else. **The
   collected raw evidence is additionally persisted BEFORE the signer runs, as
   `UNSIGNED-INCOMPLETE-*` artifacts whose README states they are uncertified and must never
   be reported as a measurement (r6 fold: a post-collection signer failure can no longer
   destroy the capture); after a successful run the unsigned copies remain beside the signed
   set so a reader can see what signing added.**
4. Verify: run the BUILD verifier over the produced envelope with the fixture manifest,
   passing the REAL evaluation instant to the trust-root validity check
   (`evaluation_instant`) — the deterministic default exists for suite reproducibility and
   is NOT a production freshness check —
   expected result: the envelope is INDEPENDENTLY VALID — structure **+ signature + complete
   per-receipt physical semantics (the existing `_receipt_errors` validator; presence/shape
   alone certified nothing — r6 fold)** — AND admission still red with the honest sentinel(s)
   (fixture kind; no production roots). The pass criterion is that CONJUNCTION, and a failed
   criterion exits nonzero. Named not-applicable exclusions (`EXTERNAL_WORK_UNMEASURED` for
   the smoke enforcement record; the unregistered-coordinate probe) are reported in the
   verification output, never silently dropped.
4b. **If the thread-event version gate fires** (`ETW_KERNEL_THREAD_VERSION_UNVERIFIED:<id>,
   <version>` — a Windows build shipping a ThreadStart/ThreadStop revision outside the
   verified set; this cannot be preflighted, the version is only known once events flow):
   the capture is spent, and the procedure is mechanical — record the refused version from
   the fault, dump the provider's versioned template via TDH on THIS host (the codex-r3
   fold's dump method), verify the offsets of the two fields the decoder reads, extend
   `KERNEL_THREAD_PAYLOAD_VERSIONS_VERIFIED` with a witness, and take the change through a
   council round before the next elevated attempt. Never widen the set without the TDH
   dump — decoding at unverified offsets is exactly the wrong number the gate exists to
   refuse (r7 ruling 3, its named residual).
5. Cleanup: terminate/close job handles (terminate-on-close covers descendants), stop the ETW
   session, remove any temp artifacts outside the evidence destination, and record the
   cleanup in the smoke report.
6. Report: bank the transcript + envelope digests beside the authorization; note any
   capability gaps (unsupported PMU, losses) verbatim — they are findings, not failures to
   hide.

Operator invocation (each step refuses rather than proceeding if its precondition fails):

```powershell
# no elevation needed, touches nothing:
.\run-smoke-cell.ps1 -SelfTest
# elevated, read-only probes, starts nothing:
.\run-smoke-cell.ps1 -Preflight -OperatorConfirmsNotNested
# elevated, THE run (sets MBCX01_BUILD_ALLOW_PHYSICAL=1 in its own process only):
.\run-smoke-cell.ps1 -Execute -OperatorConfirmsNotNested -ReportPath <path>
```

⚠ What the BUILD suite CANNOT tell you, and this run can (record each verbatim):

- whether ONE `EVENT_TRACE_SYSTEM_LOGGER_MODE` session accepts BOTH the SystemTraceProvider
  CSwitch stream and the manifest provider `Microsoft-Windows-Kernel-Process`. The
  `EtwPmcSession` contract requires the SAME session; no Microsoft page opened during the
  build confirms a system logger accepts manifest providers, and "NT Kernel Logger
  Constants" states the deprecated kernel logger does NOT. The consumer ATTEMPTS the
  documented single-session configuration and FAULTS on refusal — it never falls back to a
  second session, because that would silently void the same-session evidence claim;
- whether `ProcessTelemetryIdInformation = 64` is the right ordinal;
- whether `EVENT_HEADER_EXT_TYPE_PMC_COUNTERS = 0x0008` is right (Microsoft names the
  constant but publishes no value). A wrong value makes every CSwitch look like it carries
  no counter, which surfaces as `ETW_PMC_EXTENDED_DATA_ABSENT` — a fault, never a zero;
- whether the platform grants `InstructionRetired`, how many counters it grants, and
  whether another owner already holds them;
- the real ProcessStart/ProcessStop payload offsets of the Kernel-Process manifest on this
  OS build;
- whether ProcessStart for a CREATE_SUSPENDED root is delivered inside the trace window.
  The trace window is opened before `collect()` runs and closed at the terminal barrier by
  `session.close_trace_window()`, so it should be — but only a run can show it. If it is
  not, `assemble_member_lifetimes()` raises `ETW_PROCESS_LIFETIME_ROOT_ABSENT` and the
  collection aborts rather than signing a roster that is missing its own root.

## 4. What comes after smoke (each its own authorization)

custody ceremony (production keys/roots) → production one-cell re-proof under a production
root → 100-cell grid → route qualification → experiment. None of these is authorized by this
document, the BUILD, or the smoke proof.
