# MBCX-01 r12 prior-art and internal-shelf memo

Date: 2026-08-13
Purpose: repair r11's remaining authority seams with existing mechanisms and record the required build-decision sweep.

## 1. External primary sources

### Service-enforced idempotency

AWS describes safe mutating retries as a service property: the service recognizes a caller request ID, stores/binds that ID with the operation, and rejects reuse with changed intent. Stripe likewise stores the first result for an idempotency key and compares subsequent parameters. Neither source supports a client granting itself retry authority by hashing a semantic sentence.

r12 disposition: ambiguous acceptance is terminal missing. MBCX-01 has no pinned provider-specific capability, so the route ledger exposes no ambiguity-to-retry edge.

- https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/
- https://docs.stripe.com/api/idempotent_requests

### Signed artifact verification

SLSA verification starts from configured roots of trust, verifies an authenticated envelope/provenance, and matches the signed subject digest and expected identity. The general pattern separates content integrity from authority.

r12 disposition: a measurement self-hash remains useful for corruption detection but never proves OS origin. `SignedMeasurementReceiptV1` adds a separately pinned Ed25519 verification key, domain/version/algorithm, complete preimage digest and anti-replay identity.

- https://slsa.dev/spec/v1.2/verifying-artifacts

### Windows Job Objects and ETW

Microsoft documents Job Object process-tree/accounting behavior and also the boundary that a process created through WMI `Win32_Process.Create` is not automatically associated with the caller's job. Completion-port notification is useful but delivery is not a complete proof, making active-process-zero and final accounting queries load-bearing. Basic/I/O accounting and Extended Limit information expose different required fields. ETW distinguishes trace query/configuration modes and exposes loss counters; an unspecified `retired_instructions` integer is not enough.

r12 disposition: the future harness must combine enforced containment/egress controls, start-key process attribution, completion diagnostics, active-zero, separate final query evidence, exact PMC configuration and loss/capability checks. Unsupported/lossy evidence fails loud.

- https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects
- https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_and_io_accounting_information
- https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information
- https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_associate_completion_port
- https://learn.microsoft.com/en-us/windows/win32/api/evntrace/ne-evntrace-trace_query_info_class
- https://learn.microsoft.com/en-us/windows/win32/api/evntrace/ns-evntrace-event_trace_properties

### Retained inference and reliability sources

The Chugg/Ramdas average-conditional-mean ruler, PostgreSQL-style half-open temporal integrity, NIST acceptance-sampling comparison and SLSA/Git reconstruction conclusions from r11 are unchanged. The route theorem is stated with a finite-horizon conditional-expectation recursion, not iid and not a full-history uniform representation.

- https://arxiv.org/abs/2512.21300
- https://www.postgresql.org/docs/current/ddl-temporal-constraints.html
- https://itl.nist.gov/div898/handbook/pmc/section2/pmc232.htm

## 2. Internal-shelf sweep log

The sweep was read-only. No code was copied wholesale and no internal artifact was treated as evidence that MBCX-01's harness already exists.

### Query A — ambiguous dispatch/retry

Exact query:

```text
rg -n "ACK_AMBIGUOUS|ISSUANCE_UNKNOWN|No retry|no retry|adjudicat|readback" C:\Users\Kingo\source\Photon\crates\aruna\src
```

Opened:

- `C:\Users\Kingo\source\Photon\crates\aruna\src\attempt.rs`, especially lines 150–151, 1158 and 1800.

Found: Photon's attempt grammar explicitly omits retry from `ACK_AMBIGUOUS`/`ISSUANCE_UNKNOWN`; only proven pre-send/no-effect outcomes can retry, while unknown outcomes go to adjudication.

Disposition: **ADOPT the fail-closed state rule.** MBCX-01 is simpler than Photon because it does not need operational adjudication: the frozen scenario becomes explicit missing. **DO NOT ADOPT** Photon's larger attempt/adjudication subsystem; it is unnecessary for a one-run scientific instrument.

### Query B — authenticated evidence envelope

Exact query:

```text
rg -n "Ed25519|compact JWS|createPrivateKey|createPublicKey|signature|verify" C:\Users\Kingo\source\Gravity\src\evidence\EvidenceSigner.ts C:\Users\Kingo\source\Gravity\src\evidence\EvidenceSigner.test.ts
```

Opened:

- `C:\Users\Kingo\source\Gravity\src\evidence\EvidenceSigner.ts`;
- `C:\Users\Kingo\source\Gravity\src\evidence\EvidenceSigner.test.ts`.

Found: Node built-in `crypto` Ed25519 compact-JWS signing/verification plus round-trip, payload/signature tamper, wrong-key, algorithm-confusion and malformed-input tests.

Disposition: **ADOPT the no-new-package Ed25519 verification shape and adversarial tests.** **DO NOT ADOPT** local private-key placement/reuse: MBCX-01 requires the production private key outside both candidate and evaluator domains and keeps repository keys fixture-only.

### Query C — Windows containment/accounting

Exact query:

```text
rg -n "Job Object|CreateJobObject|SetInformationJobObject|AssignProcessToJobObject|ExtendedLimit|JOB_OBJECT" C:\Users\Kingo\source\Gravity\spikes\110-sentinel-slice0c C:\Users\Kingo\source\agentvault-mcp-bridge\docs\167-3b-live-wiring-DESIGN-v10-2026-08-05.md
```

Opened:

- `C:\Users\Kingo\source\Gravity\spikes\110-sentinel-slice0c\Program.cs`;
- `C:\Users\Kingo\source\Gravity\spikes\110-sentinel-slice0c\README.md`;
- `C:\Users\Kingo\source\agentvault-mcp-bridge\docs\167-3b-live-wiring-DESIGN-v10-2026-08-05.md`, especially the supervisor-owned Job Object section near lines 895–906.

Found: existing supervisor-owned Job creation/configuration/assignment patterns and spike evidence for Extended Limit/KILL_ON_JOB_CLOSE behavior.

Disposition: **REUSE as implementation scaffolding in the later BUILD gate.** **DO NOT CLAIM** those patterns already supply MBCX-01's completion, ETW, external-work or signed-receipt evidence; the physical harness remains unimplemented.

### Query D — evidence authority and laundering

Exact query:

```text
rg -n "evidence laundering|side-effect|signer|signature|custody|authority" C:\Users\Kingo\source\agentvault-mcp-bridge\VERIFICATION_GATES_RESEARCH.md C:\Users\Kingo\source\agentvault-mcp-bridge\research\handoff-briefings-supervisor-reconstruction-report.md
```

Opened:

- `C:\Users\Kingo\source\agentvault-mcp-bridge\VERIFICATION_GATES_RESEARCH.md`, especially the deterministic-gate, attestation, side-effect recheck and evidence-laundering sections;
- `C:\Users\Kingo\source\agentvault-mcp-bridge\research\handoff-briefings-supervisor-reconstruction-report.md`, especially the verified-state/authority and independent-finalizer conclusions.

Found: a proposer/worker may supply candidate evidence but does not thereby certify authority; high-consequence acceptance should bind authoritative pre/post state and independently retrievable receipts.

Disposition: **ADOPT directly** for writer replay and signed physical evidence. The scorer replays the exact transition from the authoritative prestate; the physical evaluator verifies a trust-root signature before consuming counters.

## 3. Build decision

Shelf-Zero: the experiment should still exist because r11's science, missingness, cohort and route theorem survived adversarial review, and the remaining failures have bounded no-paid repairs.

Build-versus-borrow:

- borrow Photon's terminal ambiguity policy;
- borrow Gravity's Ed25519 verifier/test shape but not its key custody;
- reuse the existing Job Object scaffolding only when building the later physical harness;
- implement the small MBCX-specific state replay join because no shelf component owns this experiment's exact proposal/prestate/child/poststate semantics.

Stop reason: these sources cover every r11 controlling finding. Further search would not change the r12 no-paid repair set and would risk substituting literature collection for executable closure.

## 4. Explicit non-claims

This memo does not prove the future Windows harness works, that ETW retired-instruction collection is available on the owner's host, that any provider supplies safe idempotent replay, or that a signed fixture is physical evidence. Those remain explicit gates.
