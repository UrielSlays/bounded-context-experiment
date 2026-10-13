# MBCX-01 r12 authority-closure architecture

Status: proposed governing design for no-paid verification
Scope: one writer, one immutable experiment scope, one frozen model/route, one serial A0→B→writer→cold-A1 episode
Non-scope: concurrent writers, coordination-stage behavior, physical execution, provider/model evidence, paid calls, production readiness

## 1. Design decision

r12 keeps the r11 scientific instrument and repairs four authority boundaries. It does not increase either sample, build/run the physical harness, qualify a route or call a model/provider.

```text
canonical r12 contracts
  ├─ reference state reducer
  ├─ semantically independent state oracle
  ├─ packet/DAG scorer with authoritative transition replay
  ├─ cohort/provenance implementation
  ├─ signed physical-receipt admission + evaluator
  ├─ terminal ambiguous-outcome ledger
  └─ retained inference/missingness/route kernels

normative verifier → every implementation + every repair-ledger witness
```

No r12 module imports an r8, r9, r10 or r11 runtime module. Historical artifacts remain evidence only.

## 2. State semantics and independence boundary

All r11 state rules remain governing: canonical event IDs; exact current journal/knowledge cuts; monotone observations; append-only assertion, closure and retraction evidence; nonempty half-open fact intervals; strict overlap rejection; durable same-scope B-response foreign keys; globally unique response/provider/transaction identities; complete TaskPacket/manifest/catalog binding; current-state recheck at commit; exact stored proposal evidence at rejection.

The shared state module may implement only structural admission and deterministic identity primitives: closed event shapes, lexical/calendar timestamp validation, exact primitive types, canonical JSON, SHA-256/SHA-384, event-ID derivation and construction of neutral fixtures. It may not decide temporal visibility/effectivity, correction closure, dependency reachability, action availability/target legality, lifecycle legality or transition effects.

The reference and oracle each implement those post-admission semantics independently. The oracle does not call the reference or a shared semantic helper. Verification perturbs the reference/shared semantic path and requires the oracle's registered outcomes to remain unchanged, then compares both engines over the complete event-type legal/illegal matrix and adversarial temporal/causal traces.

## 3. Authoritative writer application

The packet graph remains typed and node-distinct:

```text
ExpectedScenarioManifest
  → A0 precommit packet/result/durable call
  → B TaskPacket/worker result/durable call
  → persisted state proposal in exact authoritative precommit state
  → exact commit child applied by state reducer
  → WriterReceipt with prestate/child/poststate evidence
  → cold A1 packet at exact postcommit cut/result/durable call
  → scorer
```

The scorer's authority input includes the canonical authoritative precommit state, its exact current cut and digest, and the exact persisted proposal event bytes/hash. The WriterReceipt binds those values, the exact child event, the exact postcommit state digest and cut.

Scoring independently deep-copies the admitted prestate and applies the exact child through both r12 reducers. Success requires:

1. the proposal named by the child exists byte-for-byte in the prestate journal and its stored hash matches;
2. the supplied precommit cut is the state's exact current cut and the prestate digest verifies;
3. the child has the exact next journal sequence, an exact current originating cut and a valid/effective event time;
4. both reducers return `APPLIED` and produce byte-identical canonical poststates;
5. the produced poststate digest/current cut equal the WriterReceipt and the A1 packet cut; and
6. every existing manifest, catalog, worker, call, response and durability edge remains exact.

Canonical bytes alone never establish application. A forged proposal ID, sequence jump, stale/pre-effective child time, invented packet-local commit or postcommit-cut substitution returns score zero.

## 4. Ambiguous acceptance is terminal

The r12 call ledger has no transition from `ACCEPTANCE_AMBIGUOUS` to `PREPARED`, `DISPATCHED` or any retry state. Once transport cannot prove whether a stochastic request was accepted, that logical call becomes an explicit missing outcome. The scientific missingness path consumes its frozen scenario ID; no replacement call is launched.

`RouteAttestationV1` and any public self-hash over a sentence about idempotency have no retry authority. A future route may add replay only through a separately governed, owner-pinned provider capability whose verifier authenticates service-enforced same-token/same-parameters/first-result semantics and mismatch rejection. That would be a new design/council change, not a runtime assertion.

## 5. Signed physical receipt admission

The physical harness remains absent. r12 defines the future machine boundary so that implementing it cannot silently turn candidate-authored data into evidence.

`SignedMeasurementReceiptV1` is a closed envelope containing:

- one complete canonical `MeasurementReceiptV2` preimage and its SHA-384;
- fixed signature domain, schema version and `Ed25519` algorithm;
- a pinned signing-key ID resolved by a separately governed trust-root manifest;
- unique run ID plus candidate/generator/H/D/F cell identity and nonce for anti-replay;
- the signature over the domain-separated canonical envelope preimage.

The evaluator verifies the envelope with the separately pinned public key before reading counters. Unknown keys, wrong algorithms/domains, invalid signatures, digest mismatch, duplicate run/cell/nonce identities, unsigned rows or extra fields fail closed. Test private keys are marked fixture-only and can exercise the verifier but cannot establish physical readiness. Candidate and evaluator processes never receive the production private key.

The signed payload binds machine evidence for:

- root creation suspended, Job Object assignment before resume and both breakaway flags disabled;
- process-start-key membership for root and every observed descendant, including terminated members;
- completion-port association, messages/loss diagnostics, active-process-zero and final queries;
- separate final `JobObjectBasicAndIoAccountingInformation` and `JobObjectExtendedLimitInformation` evidence;
- job-wide user/kernel CPU, read/write/other operations and transfer bytes, peak job memory and monotonic elapsed time;
- exact ETW PMC mode/event/counter configuration, root/descendant attribution and trace loss/multiplexing/capability status;
- enforced network/IPC/external-worker boundary and its independent enforcement receipt.

Retired instructions remain a primary axis. Unsupported PMC, lossy/unattributed ETW, containment gaps or unverified external-work denial return `PHYSICAL_HARNESS_UNAVAILABLE`/design failure, never a diagnostic-only pass.

In addition to absolute affordability limits, H-shape boundedness tests cover retired instructions, CPU, elapsed time, peak committed memory, total I/O transfer bytes and total I/O operation count. Each total is the checked sum of read/write/other fields.

## 6. Cohort, inference and planning

The r11 cohort authority and scientific rule are unchanged: pinned generator content, contract-owned domains, complete scenario/cut/state/gold/action authority, six motifs × 128 retained scenarios, final SHA-256 order, 768 paired outcomes and a single terminal analysis.

The exact-mixture intervals and arbitrary-position missing-completion dynamic program remain unchanged. Exhaustive completion comparison remains a certifying oracle only for small missing counts. r12 additionally samples deterministic random completions near `m=20` and asserts every brute evaluated completion lies inside the DP extrema. This is a property spot check, not an exhaustive proof.

All operating-characteristic outputs remain deterministic planning frequencies for explicitly registered complete joint cells. No true-probability lower bound or rectangular assurance region is implied. The `(0,.3,.1,.6)` counterexample remains published.

## 7. Route qualification

The 456-trial, accept-at-most-four route gate and finite-horizon conditional-expectation proof remain unchanged. The contract requires full-past conditional failure probability at least `.02` for the bad class or at most `.005` for the good class; it does not assume iid or promise anything for hazards between/crossing those bounds. Abort, incomplete and unclassified launches count as failures; no replacement and no early acceptance are permitted.

r12 does not execute this qualification.

## 8. Reconstruction, normative boundary and repair retention

The council pins a governing commit, an owner-pinned manifest blob and a launcher blob. The extracted launcher is authenticated before execution, reconstructs every subject as `commit:path` and verifies Git blob, bytes, LF/line counts and SHA-384 before import or execution.

Implementation plans and council verdicts are evidence/history, not normative runtime subjects. The normative set contains the experiment design, r11 synthesis, r12 architecture/prior-art/harness requirements, current contracts, r12 implementations/tests/verifiers, signed-receipt verifier/trust-root fixture, repair ledger and no-paid report.

The repair ledger is two-way: every adopted repair must name executed witnesses and every governed repair witness must map back to a repair. It includes all retained r11 witnesses plus the r12 authority-seam attacks.

## 9. Stop conditions

`PHYSICAL_HARNESS_UNAVAILABLE` remains the top-level blocking prerequisite. No scientific experiment, FD/FC/TN physical run, route qualification, provider/model request or paid call is authorized by r12 or its council dispatch. After council approval, the next action is a separately reviewed BUILD-class physical-harness implementation and validation—not the experiment.
