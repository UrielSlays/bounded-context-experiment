# MBCX-01 r13 Invariant-Closure Architecture

Status: governing closure of the accepted r12 experiment design, amended by bounded r13.2 council repair

Scope: one writer, one immutable experiment scope, one frozen model/route, one serial `A0 → B → writer → cold A1` episode

Non-scope: scientific redesign, concurrent writers, coordination-stage behavior, physical execution, provider/model evidence, paid calls, production readiness

## 1. Decision

r13 is a closure fold, not a new experiment design. It keeps the r12 estimand, 768-pair scientific population, 456/4 route gate, inference, candidates, controls and three-stage stop order. It applies one law across the complete instrument:

> Integrity is not authority, and local validity is not cross-component consistency.

The normative closure unit is the invariant row, not the latest council witness. `MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md` enumerates every duplicate representation of experiment truth. Each row has a positive and adversarial executable witness. Any two locally valid objects that disagree without rejection fail the bundle.

## 2. Three layers

The machine is divided into:

```text
authority acquisition → pure verification → scientific decision
```

Fixture-only authority may exercise parsers, signatures, reducers, packet joins and evaluators. It cannot establish an experiment-eligible score, physical pass, route pass or scientific result. Until separately governed production adapters exist, the explicit statuses are `STATE_AUTHORITY_UNAVAILABLE` and `PHYSICAL_HARNESS_UNAVAILABLE`.

## 3. State authority and reducer independence

The state-owner receipt binds a closed domain/version, store and namespace identity, immutable transaction/commit ID, exact prestate read/cut/hash, persisted proposal bytes/hash, exact applied child bytes/hash, postcommit readback/cut/hash, producer key/role and receipt digest/signature.

The packet builder cannot manufacture production authority. A fixture receipt is marked fixture-only and production admission rejects it. Activating production requires an independently configured state-owner root and custody policy; changing code or injecting a self-authored root is not authority.

Shared reducer code stops after closed structural admission, lexical/calendar timestamps, canonical JSON and deterministic hashes/IDs. Reference and oracle independently own replay decisions, idempotency lookup/persistence, event persistence, next sequence, observation watermark, temporal visibility, dependency/action law and every transition effect. Poisoning either finalizer must make the engines disagree; agreement is defense in depth, not external state authority.

## 4. One authoritative causal chain

```text
source provenance + exact retained-set authority
  → ExpectedScenarioManifest + canonical prestate world
  → exact manifest-cut state receipt
  → A0 packet/result/durable ledger
  → TaskPacket
  → B response/durable ledger
  → persisted proposal in state-owner prestate
  → exact committed child
  → state-owner postcommit readback
  → WriterReceipt
  → cold A1 projected from that poststate
  → A1 durable ledger
  → episode receipt
  → authenticated scenario-outcome receipt
  → inference
```

`RetainedScenarioAuthorityV2` is recomputed from the pinned generator and deterministic selection, carries the full selected candidate record, its exact position, source provenance, and a SHA-384 retained-set root computed over the canonical ordered list of all 768 candidate hashes (a flat list digest; a Merkle tree with inclusion proofs was considered and declined - no consumer exists for per-candidate proofs) [amended 2026-08-16, owner-ratified, #23]. The manifest carries that source-owned world but cannot mint membership. `ManifestCutStateReceiptV1` proves a distinct exact state read at the manifest cut; the later proposal prestate is not substituted for it. A0 is rendered from the admitted manifest-cut projection. A1 is rendered only from the admitted poststate projection.

The scorer replays the exact child through both reducers for conformance, but experiment eligibility additionally requires production state-owner authority. Self-authored graphs can prove conformance only and return `STATE_AUTHORITY_UNAVAILABLE` at the scientific boundary.

## 5. Call ledger and episode totality

`ACCEPTANCE_AMBIGUOUS` remains terminal with no retry edge. For each frozen scenario, `EpisodeReceiptV1` binds exactly six scheduled `EpisodeCallV2` positions. A row is either a launched terminal ledger or a `NOT_LAUNCHED_UPSTREAM_TERMINAL` marker bound to the exact preceding failed ledger in that condition; the instrument never fabricates downstream launches.

Inference never accepts a caller-authored observed/missing partition as authority. It derives:

- one complete paired outcome when all six nodes have exact joined durable terminals; or
- one whole-pair-missing scenario when any node is ambiguous or lacks a valid durable terminal.

Duplicate nodes, cross-scenario identities, mismatched response/durability fields and any supplied partition that differs from the derived partition fail. Complete scenarios additionally require `ScenarioOutcomeReceiptV2`; it binds the exact episode hash and all six ordered ledger/call-record identities to the BC and OM scorer graphs before inference derives the pair. A same-scenario graph from another episode is not authority. [Added 2026-08-16, owner-ratified, #23:] The scientific population excludes target-reopen episodes by generator constraint; BC/OM is never measured over a scored-target reopen, and the A1 no-recurrence expectation is preserved by construction rather than by verifier change. Measuring the reopen class is the declared first follow-up (MBCX-02) conditional on a positive primary result.

## 6. Physical evidence and trust

The physical harness is BUILT and witness-covered but has never executed against a live ETW session; every live-platform fact remains unverified until the elevated smoke run. [Amended 2026-08-16, owner-ratified DoR reconciliation sweep (#23).] The signed receipt represents the evidence required by the prose, not Boolean claims about it:

- root/descendant PID plus process-start-key membership and process/thread QPC lifetimes;
- creation-suspended, Job assignment-before-resume and no-breakaway records;
- completion-port association and message counts as diagnostics; final active-process zero plus signed all-members-terminal lifetimes and final-query order are load bearing;
- separate final Basic+I/O and Extended-Limit query records with success/status/class/version/size/raw digest;
- Job-wide user/kernel CPU, I/O operations/bytes, peak memory and elapsed time;
- exact ETW PMC capability queries, counter/event attachment, raw ordered CSwitch observations, per-processor counter deltas, PID/start-key/TID attribution, conflict/multiplexing and loss evidence;
- supervisor-owned network/IPC/broker/external-worker enforcement evidence;
- host/environment facts, harness build digest, run/candidate/generator/cell identity.

The complete closed payload is signed. One grid identity binds run, candidate, exact candidate/carrier artifact digest, generator, harness artifact/build/configuration, host/environment, signing key, producer role, fixture kind, and trust policy across all 100 cells. Signature verification is necessary and insufficient: the root must authorize the producer role for the subject/run, and the signer must not control trust-root editing. Fixture keys structurally cannot authenticate physical evidence.

The Job decoder uses Microsoft's field semantics as well as its layout. `TotalTerminatedProcesses` counts processes terminated because of a Job limit violation; it is not normal-exit membership. A clean admitted run requires zero while signed terminal PID/start-key lifetimes and final `ActiveProcesses == 0` prove completion.

Supported PMC environments are a qualifying Windows host or Hyper-V root partition, or a stopped non-nested guest with explicit PMU exposure and recorded capability. Nested virtualization is unsupported. Cross-hardware live migration or save/restore is forbidden during measurement.

## 7. Physical gates

Absolute affordability remains separate from finite H-shape boundedness. For every fixed `(D,F)`, max-minus-min across all four H values is checked for:

1. retired instructions: 500,000;
2. aggregate user+kernel CPU: 75,000,000 ns, retained from Measurement Contract v4;
3. monotonic elapsed: 75,000,000 ns;
4. peak committed memory: 67,108,864 bytes;
5. total I/O transfer: 16,777,216 bytes;
6. total I/O operations: 4,096.

CPU and I/O totals are checked sums with exact units and overflow rejection. Missing evidence, unsupported PMC, trace loss, containment gaps or unverified external work fail loud. No fixture can retire the physical sentinel.

## 8. Engineering selection

Scientific gates do not silently encode product taste. `EngineeringCandidateEvidenceV1` embeds `CarrierExactnessReceiptV2` and signed 100-cell evidence; its hard-gate Booleans and worst-cell values are recomputed rather than accepted from a caller. Exactness binds the pinned suite/witness set, exact carrier artifact and exact full-grid identity. Fixture conformance cannot be relabeled as production authority. Only survivors enter a frozen Pareto comparison over the six axes above.

One carrier dominates another only when it is no worse on every axis and strictly better on at least one. The machine reports the full nondominated set. More than one nondominated carrier yields `OWNER_SELECTION_REQUIRED`. Any owner preference is a policy decision labeled separately from experimental evidence.

## 9. Reconstruction and retained evidence

The council pins one governing commit, one owner-pinned manifest blob and one launcher blob. The launcher is authenticated before execution and reconstructs each subject as `commit:path`, verifying Git blob, raw bytes, LF/line counts and SHA-384 before import.

The static r12 no-paid report is not a normative r13 subject. Fresh results are emitted from the authenticated verifier run. The repair ledger is two-way and maps all seventeen invariant rows to their positive/adversarial witnesses; any executed governed witness without a ledger entry or ledger witness not executed fails.

## 10. Readiness and stop boundary

Passing r13 means the no-paid closure is coherent and council may authorize the separately reviewed BUILD-class state adapter and Windows evidence producer. It does not mean those production authorities exist.

No scientific experiment, physical harness run, route qualification, provider/model request or paid call is authorized. Current readiness must remain fail-loud on absent production state and physical authority.
