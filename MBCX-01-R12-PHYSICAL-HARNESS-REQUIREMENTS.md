# MBCX-01 r12 physical harness and signed-evidence requirement

Status: **required external prerequisite; not implemented or executed by the no-paid r12 bundle**

Synthetic rows and test-key signatures exercise admission/evaluation only. They are not OS evidence and cannot establish a candidate pass or retire `PHYSICAL_HARNESS_UNAVAILABLE`.

## 1. Isolation and membership

A future separately governed Windows harness must create the candidate root suspended, create and configure a named Job Object while inactive, associate the completion port, disable both breakaway modes, assign the root and only then resume it. It must bind every process to a process-start key as well as PID, retain terminated-member evidence, and define/test the boundary against at least WMI `Win32_Process.Create`, RPC/IPC launch brokers, pre-existing helpers and network work. A Job Object alone is not accepted as proof that those escape surfaces were unavailable.

The harness must enforce network egress denial and the declared no-external-compute policy using supervisor-owned controls. Candidate-readable configuration or a constant string is not enforcement evidence.

## 2. Completion and final accounting

The harness must collect completion-port messages and their diagnostics, wait for active-process-zero, drain the port, and then perform final queries. Completion messages support membership/lifecycle evidence but are not treated as guaranteed delivery.

At minimum the final signed evidence binds separate results from:

- `QueryInformationJobObject(JobObjectBasicAndIoAccountingInformation)` for aggregate CPU/I/O/process accounting; and
- `QueryInformationJobObject(JobObjectExtendedLimitInformation)` for peak job memory and configured limit/breakaway state.

The receipt records call success/status, query class, returned structure version/size and canonical extracted fields. The active-process-zero observation and final query order are explicit.

## 3. Retired instructions

The backend is exact and fail-loud:

- provider: Windows ETW/WPR PMC;
- counter: retired instructions from the explicitly pinned platform counter name/index;
- mode: one pinned event-attached or sampled mode, never an unspecified mixture;
- attribution: process-start-key membership joined to the Job Object root/descendant set, including terminated members;
- capability: hardware/OS/privilege/virtualization support recorded before candidate execution;
- integrity: sampling interval/event set, multiplexing/scaling status and `EventsLost`, `LogBuffersLost` and `RealTimeBuffersLost` recorded;
- admission: any unsupported counter, loss, ambiguous attribution or scaling forbidden by the contract returns `PHYSICAL_HARNESS_UNAVAILABLE`.

Retired instructions are not silently downgraded to diagnostic-only because they are a primary physical boundedness coordinate.

## 4. Signed receipt envelope

Every 100-cell row is wrapped in `SignedMeasurementReceiptV1`. The complete canonical receipt and run/cell identity are domain-separated and signed with Ed25519. The envelope includes algorithm, domain, schema version, signing-key ID, receipt digest, run ID, nonce and signature.

The production verification key is pinned as a normative trust-root artifact. The private key is outside the candidate and evaluator security domains. The evaluator rejects unknown keys, signature/digest mismatch, wrong domain/version/algorithm, duplicate run/cell/nonce identity, missing fields, extra fields and unsigned receipts before evaluating any physical value.

No repository test key, fixture signature or self-generated key may be promoted into the production trust-root manifest. Replacing the trust root is a governed bundle change.

## 5. Required counters and gates

Each receipt binds exact non-Boolean values for job-wide:

- user and kernel CPU nanoseconds;
- read/write/other operation counts;
- read/write/other transfer bytes;
- peak job committed memory;
- monotonic elapsed nanoseconds; and
- attributed root-plus-descendant retired instructions.

The evaluator computes checked totals for CPU, I/O operations and I/O bytes. H-shape boundedness gates cover retired instructions, CPU, elapsed, peak memory, total I/O operations and total I/O bytes. Absolute affordability budgets remain separate. Counter overflow, negative values, inconsistent subtotals or unit ambiguity fails admission.

## 6. Run completeness

One candidate ID, generator digest, harness build digest, trust-root ID and run ID govern all 100 registered H-D-F cells. Every cell appears exactly once. Missing, duplicate, replayed, mixed-candidate, mixed-generator or mixed-harness cells fail. The harness freezes environment/host facts needed to interpret the measurements and records any unsupported capability as an explicit prerequisite failure.

## 7. Current status and next gate

r12 contains the schema, verifier shape and adversarial no-paid tests only. It does not contain or run the Windows harness and therefore must report `PHYSICAL_HARNESS_UNAVAILABLE` and top-level `DESIGN_OR_IMPLEMENTATION_FAIL`.

After a council GO, the next gate is a separate BUILD-class review of the harness implementation, signer custody, isolation controls, exact ETW configuration and red receipt-forgery/replay tests. Only after that gate passes may a real 100-cell physical validation be proposed. That still does not authorize model/provider or route calls.

Primary platform references:

- https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects
- https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_and_io_accounting_information
- https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information
- https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_associate_completion_port
- https://learn.microsoft.com/en-us/windows/win32/api/evntrace/ne-evntrace-trace_query_info_class
- https://learn.microsoft.com/en-us/windows/win32/api/evntrace/ns-evntrace-event_trace_properties
