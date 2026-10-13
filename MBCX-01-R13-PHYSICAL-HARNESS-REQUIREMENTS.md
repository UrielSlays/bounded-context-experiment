# MBCX-01 r13 Physical Harness and Authority Requirements

Status: required external BUILD prerequisite; not implemented or executed by r13

Synthetic rows, fixture state receipts and fixture signatures exercise conformance only. They are not state-store or OS evidence and cannot retire `STATE_AUTHORITY_UNAVAILABLE` or `PHYSICAL_HARNESS_UNAVAILABLE`.

## 1. Supported environment

The harness supports an eligible Windows host or Hyper-V root partition. A Hyper-V guest is eligible only when stopped during configuration, non-nested, explicitly granted PMU access with `Set-VMProcessor -Perfmon`, and its capability facts are signed. Nested virtualization is unsupported. Save/restore or live migration across different processor hardware is forbidden from capability capture through final receipt.

## 2. Isolation and membership

Create the candidate root suspended; create/configure the Job Object while inactive; associate the completion port; disable both breakaway modes; assign the root; then resume. Bind every root/descendant membership to PID plus process-start key and signed lifetime. Retain terminated members. Red-test WMI creation, RPC/IPC brokers, pre-existing helpers, network work and breakaway attempts.

Supervisor-owned controls enforce network denial and the declared no-external-compute boundary. Candidate-readable configuration or a constant label is not enforcement evidence.

## 3. Completion and final queries

Collect completion messages as diagnostics, establish signed terminal lifetimes for every assigned PID/start-key, confirm final active-process zero, then issue separate final queries:

- `JobObjectBasicAndIoAccountingInformation` for aggregate CPU/I/O/process accounting;
- `JobObjectExtendedLimitInformation` for peak memory and configured limit/breakaway state.

Each signed query record contains API/class identity, call success, status/error, structure version and size, raw returned bytes and raw-result digest. The 64-bit `JOBOBJECT_BASIC_AND_IO_ACCOUNTING_INFORMATION` preimage is exactly 96 bytes: four signed 64-bit time values, then four 32-bit fields (`TotalPageFaultCount`, `TotalProcesses`, `ActiveProcesses`, `TotalTerminatedProcesses`), then six unsigned 64-bit I/O counters. No padding replaces the fourth DWORD. `TotalTerminatedProcesses` counts processes killed because of a Job limit violation, not ordinary exits; a clean accepted cell requires zero. Signed terminal PID/start-key lifetimes plus final `ActiveProcesses == 0` prove member completion. Ordinary completion messages, including active-zero, remain diagnostic because delivery is not guaranteed.

## 4. ETW PMC evidence

Retired instructions use strict event-attached Windows ETW PMC:

- pinned `InstructionRetired` source/index;
- pinned `CSwitch` event attachment;
- raw capability-query and event-attachment records;
- ordered per-processor CSwitch counter observations, with every delta recomputed from consecutive values, attributed to outgoing `OldThreadId`, and joined to signed Job-member PID/start-key/TID lifetimes;
- recorded OS/hardware/privilege/virtualization capability;
- zero owner conflict, multiplexing, scaling ambiguity, `EventsLost`, `LogBuffersLost` and `RealTimeBuffersLost`.

Unsupported, lossy, incomplete or ambiguous evidence is unavailable, never diagnostic-only success.

## 5. Closed signed payload

Every row's signed preimage contains:

- envelope domain/version/algorithm/key/producer role;
- one exact grid identity: run, candidate, candidate/carrier artifact digest, generator, harness artifact/build/configuration, host/environment, signing key, producer role, fixture kind and trust policy; plus the individual cell coordinate;
- one carrier-exactness receipt bound to the pinned suite/witness set, exact carrier artifact digest and this exact grid identity; fixture exactness cannot activate production;
- root and membership receipt;
- completion diagnostics receipt;
- both final Job query receipts;
- ETW capability/configuration/attribution/loss receipt;
- external-work enforcement receipt;
- canonical scalar aggregates and their checked derivation;
- nonce, subject digest and receipt digest.

Missing, extra, cross-run, cross-cell, duplicate or substituted evidence fails before any gate is evaluated.

## 6. Trust-root activation

The fixture manifest remains `production_ready:false` and every fixture key remains `fixture_only:true`. Production activation requires a separately pinned manifest that names the authorized harness build/producer role, key validity/revocation policy and exact subject constraints.

The production signing key custodian cannot edit or approve the evaluator's trust-root manifest. Trust-root changes require an authority disjoint from the signer. Candidate and evaluator processes never receive the private key. A self-generated real key or repository edit cannot create authority.

## 7. Counters and gates

Receipts bind exact nonnegative job-wide values for user/kernel CPU ns, read/write/other operations, read/write/other transfer bytes, peak committed bytes, monotonic elapsed ns and attributed retired instructions.

H-shape thresholds for each fixed `(D,F)` are:

- retired instructions: 500,000;
- aggregate CPU: 75,000,000 ns;
- elapsed: 75,000,000 ns;
- peak committed memory: 67,108,864 bytes;
- total I/O bytes: 16,777,216;
- total I/O operations: 4,096.

Absolute affordability includes aggregate CPU ≤150,000,000 ns and remains a different verdict from boundedness. Overflow, unit ambiguity or inconsistent totals fail admission.

## 8. Completeness and next gate

One candidate/generator/harness/host/trust-root/run identity governs all 100 cells, each exactly once. No r13 fixture is physical evidence.

After council approval, the next gate is a BUILD-class review of the real state-owner adapter and one-cell Windows harness proof. Only a later explicit owner authorization may propose the 100-cell run, route qualification or scientific experiment.

[Added 2026-08-16, owner-ratified DoR reconciliation sweep (#23):] The Kernel-Process ETW provider is machine-wide; membership is enforced by downstream filtering, and a capture on a non-idle host may abort rather than degrade - an abort is the correct fail-loud outcome.
