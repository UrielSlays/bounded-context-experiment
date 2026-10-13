# MBCX-01 r13 Prior-Art and Environment Addendum

Status: supporting evidence; does not authorize BUILD or experiment execution

## 1. Windows job accounting and CPU

Microsoft's `JOBOBJECT_BASIC_ACCOUNTING_INFORMATION` documents total user and kernel execution time for active and terminated processes associated with a Job Object, in 100-nanosecond units:

https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_accounting_information

The Job Objects overview states that job accounting includes terminated members, that final accounting is retrieved with `QueryInformationJobObject`, that ordinary completion-port messages are not guaranteed, and that breakaway/WMI creation paths require explicit treatment:

https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects

The same official structure definition fixes the ABI order after the four `LARGE_INTEGER` fields as four consecutive `DWORD` values: `TotalPageFaultCount`, `TotalProcesses`, `ActiveProcesses`, and `TotalTerminatedProcesses`. Its Members section defines the last value as processes terminated because of a limit violation, not normally exited membership. `JOBOBJECT_BASIC_AND_IO_ACCOUNTING_INFORMATION` then appends six 64-bit I/O counters, producing the 96-byte Windows 64-bit preimage used by r13.2. No synthetic padding may replace the fourth DWORD; clean normal-exit fixtures use zero and rely on signed lifetimes plus final active zero for completion.

Microsoft's completion-port structure page explicitly says ordinary Job messages are notifications whose delivery is not guaranteed:

https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_associate_completion_port

Disposition: use aggregate user+kernel CPU as a required absolute and H-shape coordinate. Completion message counts and active-zero notification are diagnostics; signed terminal lifetimes plus final query evidence are authoritative. Record process-start identities and explicitly deny/measure breakaway and broker paths.

## 2. PMU execution environment

Microsoft's `TRACE_QUERY_INFO_CLASS` defines `TracePmcEventListInfo` and `TracePmcCounterListInfo` as the event and profiling-source configuration used to collect PMC values on selected system events:

https://learn.microsoft.com/en-us/windows/win32/api/evntrace/ne-evntrace-trace_query_info_class

Microsoft documents that Windows hosts have access to performance monitoring hardware by default beginning with Windows Server 2019 and Windows 10 1809. Hyper-V guests do not have access by default, may receive it through `Set-VMProcessor -Perfmon`, and the documented guest requirement excludes nested virtualization. Microsoft also warns against migration or save/restore across different Intel hardware because counters may be non-architectural:

https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/performance-monitoring-hardware

Disposition:

- supported by default: eligible Windows host or Hyper-V root partition;
- conditionally supported: stopped, non-nested Hyper-V guest with explicit PMU exposure and recorded host capability;
- unsupported: nested virtualization;
- forbidden during a run: cross-hardware migration or save/restore;
- unavailable or incomplete PMC evidence remains fail-loud and never silently changes the estimand.

## 3. Idempotency and ambiguity

AWS's Builders' Library requires a caller-provided request identity, same-intent parameter binding, and an atomic server-side operation joining token persistence with mutation. Client-side hashes or attestations are not a substitute:

https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/

Disposition: retain terminal ambiguity until a frozen provider exposes an authenticated replay/idempotency capability. Derive whole-pair missingness from the actual call ledgers so the scientific layer cannot ignore a terminal ambiguity.

## 4. Artifact and producer authority

SLSA's artifact-verification model separates signature verification from trusted producer identity, subject identity and expected parameters:

https://slsa.dev/spec/v1.2/verifying-artifacts

Disposition: apply the same separation to state and measurement receipts. A cryptographically valid envelope from a fixture or root editor is integrity evidence, not production authority. Production activation requires an independently configured root and signer/editor separation.

## 5. Internal shelf

The r12 shelf dispositions remain:

- Photon: adopt terminal ambiguity/non-retry doctrine; do not import its larger adjudication subsystem.
- Gravity: adopt Ed25519 verifier/test shape, not key custody.
- Gravity/bridge Job Object work: reuse containment scaffolding, not measurement evidence.

No internal shelf artifact supplies the exact MBCX state-owner transaction/readback receipt, six-call episode join, or complete signed Windows evidence producer. Those remain explicit BUILD prerequisites, not invented no-paid evidence.
