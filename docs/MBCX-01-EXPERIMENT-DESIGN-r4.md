# MBCX-01 — Staged Bounded Obligation Continuity Experiment Design r4

Status: preregistration design; no harness and no paid inference authorized

Date: 2026-08-12
Supersedes for future review: `MBCX-01-EXPERIMENT-DESIGN-r3.md`

## 1. Decision and correction of the experimental question

MBCX-01 must answer three different questions without allowing one answer to substitute for another:

1. **Continuity:** can a fresh logical conductor receive an exact, bounded decision packet that preserves current state, critical obligations, scope, provenance, and corrections while dormant history grows, without hiding archive-linear resolver work?
2. **Mechanism selection:** among strong flat-derived replay, coarse materialization, and typed-native materialization, which mechanisms satisfy the same continuity contract, and does any more elaborate mechanism earn its write/read/storage complexity?
3. **Model usability:** after the deterministic contract passes, can one frozen model use that validated packet through a process-cold A→B→A handoff without losing or duplicating an obligation?

The original North Star is question 1. Question 2 is nested inside it. A typed-native mechanism may fail to earn its complexity while bounded Moonwalker continuity still succeeds through a simpler mechanism.

The old primary contrast `TN - FM` is retired. It became degenerate when a strong flat replay arm could derive the same public semantics, and it risked killing Moonwalker merely because typing did not improve action F1.

No paid inference is authorized by this document. Stages 0 and 1, a frozen paid-stage cost envelope, and a fresh sealed council must pass before the owner may authorize Stage 2.

## 2. Scope and non-goals

MBCX-01 includes only:

- one append-only public event universe and one deterministic single-writer commit boundary;
- exact obligation lifecycle, correction, scope, dependency, and handoff semantics;
- deterministic reference state, materialization, reconstruction, and scoring;
- flat-derived, coarse-materialized, and typed-native candidate mechanisms;
- archive-size and active-frontier scaling as separate axes;
- one frozen model/provider for a conditional same-model A→B→A handoff;
- mechanical outputs, bounded inference, transport accounting, and complete cleanup.

MBCX-01 excludes:

- concurrent canonical writers, consensus, distributed transactions, or multi-writer merge policy;
- cross-model worker interchangeability or model-family generalization;
- learned/model-written memory, learned retrieval, procedural learning, personality, affect, or relationship memory;
- provider-native hidden/KV-state mount claims;
- production orchestration, deployment, licensing, patents, commercialization, hostile actors, or security architecture.

Benign wrong-scope collisions remain in scope because scope isolation is part of the scientific continuity claim. They are not a threat-model study.

## 3. Three-stage causal program

### Stage 0 — executable instrument proof, no model

Freeze and verify:

- the public event schema and total transition algebra;
- a reference reducer that defines gold independently of every candidate mechanism;
- the complete available-action universe and scorer at every decision;
- workload generation, exact manifests, archive-padding twins, and hand-authored traces;
- packet, handoff, reconstruction, tokenizer, transport, statistical, and cost contracts.

Stage 0 answers whether the proposed experiment is executable. It cannot establish memory value.

### Stage 1 — deterministic continuity and mechanism bakeoff, no model

Every candidate consumes byte-identical public events and must materialize the same reference semantics. Stage 1 tests exactness, archive independence at fixed active frontier, reconstruction, and the write/read/storage Pareto frontier.

Stage 1 answers the Moonwalker continuity question and the mechanism-selection question without stochastic model behavior.

### Stage 2 — conditional same-model A→B→A usability screen

Only a Stage-1-eligible bounded packet enters paid inference. Fresh call A establishes the next obligation-bearing decision, fresh call B receives only the declarative task packet and returns a typed proposal, and fresh call A reconciles the committed result after another process-cold restart. All calls use one frozen model/provider configuration.

Stage 2 asks whether the model can use the externally validated state. It does not prove cross-model worker interchangeability, concurrent coordination, or model-independent behavior.

## 4. Canonical public universe and single-writer boundary

### 4.1 Canonical record

The sole canonical experimental record is an append-only, hash-linked public event journal plus referenced public payload objects. Every candidate projection is rebuildable from it.

Model calls cannot write canonical state. They return proposals. The deterministic harness validates and either commits or rejects each proposal as a new event.

### 4.2 Total public event algebra

Every event has:

```text
event_id
event_type
scope_id
actor_role
observed_at
valid_from
valid_to_or_null
subject_id_or_null
obligation_id_or_null
action_id_or_null
dependency_ids[]
supersedes_event_id_or_null
payload_ref
source_event_ids[]
idempotency_key
```

The frozen event types are:

```text
assert_fact
correct_fact
retract_fact
open_obligation
reschedule_obligation
delegate_obligation
complete_obligation
cancel_obligation
reopen_obligation
link_dependency
unlink_dependency
open_handoff
propose_handoff_result
commit_handoff_result
reject_handoff_result
close_handoff
```

For every legal `(state, event)` pair, the transition table specifies:

- admissibility;
- exact next state;
- terminal/current/conflict status;
- obligation owner, due state, prerequisites, and permitted actions;
- supersession, restoration, and retraction behavior;
- source/provenance closure;
- duplicate/idempotent behavior;
- the error for every illegal transition.

No reducer-specific interpretation may define gold. A separate reference implementation and an independently written small-trace enumerator must agree before candidate reducers are tested.

### 4.3 Obligation contract

Obligations are exact prospective state, not semantic retrieval results.

At each canonical cut, the reference reducer enumerates:

```text
O_active
O_due(now)
O_blocked(now)
O_terminal
```

Every active obligation has exactly one accountable owner. Delegation is an explicit durable transition. Cancellation, completion, and rejection are terminal unless a legal `reopen_obligation` event names the terminal event being reopened. Duplicate delivery may not create a second obligation or external action.

The Stage-1 packet must include every due critical obligation in the mounted scope. If the live due frontier exceeds the declared packet frontier, the correct result is `FRONTIER_LIMIT` before model dispatch—not silent omission.

## 5. Candidate mechanisms

All candidates share the public journal, generic public-ID indexes, selector policy, packet schema, ordering, object caps, and semantic reference packet.

### FD — flat-derived replay

Persists only primitive events, payload refs, and generic indexes by scope, subject, obligation ID, dependency endpoint, and time. Currentness, restoration, conflict, terminal state, and provenance closure are derived at read time.

### FC — flat plus coarse materialization

Uses FD plus rebuildable current/terminal/superseded flags, current-value pointers, obligation status, and direct dependency readiness. It has no persisted version interval graph, conflict objects, or precomputed transitive provenance closure.

### TN — typed-native materialization

Uses the same public journal plus rebuildable typed lifecycle rows, version/valid-time relations, explicit conflict objects, restoration links, obligation/dependency state, and provenance closure.

### Required parity

Under the generous reference execution envelope, all three candidates must emit the same `DecisionPacketV1` semantic objects in the same canonical order.

If FD, FC, and TN are byte-identical after canonical serialization, there is no information treatment. Stage 2 makes one model call for that unique packet and maps the result to every mechanism that produced it. It may not spend three calls and call stochastic variation a mechanism effect.

If a fixed operational envelope causes packets to differ, the exact residual must be declared before inference as one of:

- required object omitted;
- required status/provenance field unavailable;
- explicit `PAGE_FAULT` or `FRONTIER_LIMIT`;
- serialization overflow;
- materialization timeout/work-budget exhaustion.

No mechanism may be credited for semantics that the public event algebra failed to expose to another candidate.

## 6. Reference packet and selective handoff contracts

### 6.1 `DecisionPacketV1`

```text
packet_version
canonical_cut
active_scope_manifest
current_public_state[]
due_obligations[]
blocked_obligations[]
direct_and_required_dependency_closure[]
unresolved_conflicts[]
applicable_procedure_versions[]
evidence_manifest[]
missing_or_denied[]
page_faults[]
materialization_manifest
```

Every object carries its public semantic ID and source event IDs. Empty fields mean the reference reducer proved the set empty; they never mean a candidate failed to derive it.

### 6.2 `TaskPacketV1`

Fresh worker B receives only:

- the applicable `DecisionPacketV1`;
- current observation and current time;
- the complete available action set;
- task identity, handoff identity, output schema, and idempotency key.

B receives no A transcript, hidden reasoning, worker scratch, or provider conversation chain.

### 6.3 `WorkerHandoffV1`

```text
handoff_id
worker_role
task_id
input_packet_hash
input_scope_manifest
started_at
ended_at
result_status
proposed_action_ids[]
evidence_event_ids[]
proposed_claims[]
proposed_mutations[]
new_obligations[]
discharged_obligations[]
unresolved_items[]
warnings[]
model_runtime_fingerprint
idempotency_key
```

The handoff is a proposal, never a fact merely because a model emitted it. The deterministic commit boundary validates public IDs, scope, transition legality, action availability, and idempotency before appending a commit or rejection event.

## 7. Workload

### 7.1 Deterministic core cohort

The frozen generator creates `240` independent scenario seeds: six motif families × forty seeds.

Motif families:

1. correction, retraction, and restoration;
2. obligation open/reschedule/cancel/complete/reopen;
3. dependency link/unlink and reverse activation;
4. benign same-name/cross-scope collision;
5. delegation, duplicate proposal, rejection, and idempotent commit;
6. mixed A→B→A continuity with delayed due state.

Each scenario contains 24 scored decision cuts and enough dormant padding events for the assigned scale cells. Gold is private to the harness and never serialized into candidate artifacts or prompts.

### 7.2 Archive-size axis

For each seed, construct archive-padding twins at:

```text
H = 128, 1,024, 10,000, 100,000 public events
```

The twins have identical active scopes, live obligations, required dependency closure, current public state, current observation, available actions, and gold. Added events are dormant but syntactically and semantically realistic.

For the archive-size claim:

- active scopes `<= 4`;
- live obligations `<= 16`;
- due critical obligations `<= 4`;
- required dependency closure `<= 32` objects.

Model-visible semantic packets must be byte-identical across each twin family.

### 7.3 Active-frontier axis

Hold archive size at `100,000` and vary live obligation/dependency frontier:

```text
F = 1, 4, 16, 64, 256
```

This axis is reported separately. The experiment does not claim a fixed packet for an unbounded true decision frontier. Packet size and resolver work may grow with `F`; silent omission may not.

### 7.4 Hand-authored traces

Before generated workloads, run explicit minimal traces for every event type and every two-event interaction, plus:

- correction → retraction → restoration;
- cancellation → duplicate cancellation → legal reopen;
- completion → stale duplicate proposal;
- link → unlink → reverse prerequisite activation;
- A creates obligation → B proposes completion → duplicate B proposal → A resumes;
- wrong-scope near-duplicate state that must remain absent.

## 8. Complete action universe and mechanical scoring

At every scored cut the generator emits a complete `available_action_ids[]` list of 8–16 IDs. The reference reducer derives a gold subset of 1–3 IDs or the explicit `NO_ACTION` ID.

The dataset manifest records the actual exposure counts after generation. Motif quotas constrain the cohort-level stratification; they are not contradictory per-scenario totals.

### Deterministic contract outcomes

- exact reference state equality;
- critical due-obligation recall;
- stale/terminal suppression;
- wrong-scope admission count;
- dependency-closure completeness;
- exact reconstruction equality;
- duplicate-effect count;
- packet semantic and byte identity;
- declared page fault/frontier-limit correctness;
- primitive objects inspected, index operations, bytes, latency, and artifact size.

### Paid usability outcome

For each scenario, `contract_success = 1` only if every scored handoff decision:

- selects every critical due action;
- selects no stale, terminal, premature, or wrong-scope action;
- produces a schema-valid handoff;
- survives deterministic commit/rejection without a duplicate effect.

Otherwise `contract_success = 0`.

Action set precision, recall, F1, per-motif accuracy, abstention/page-fault use, invalid output, and latency are secondary. No LLM judge may override a mechanical score.

## 9. Stage-1 hard gates and conclusions

### 9.1 Universal hard gates

Across the frozen deterministic cohort and hand-authored traces:

- `0` lost critical due obligations;
- `0` wrong-scope semantic admissions;
- `0` stale terminal/corrected resurrection after the propagation barrier;
- `0` duplicate committed effects;
- `100%` exact deterministic reconstruction;
- `100%` declared legal-transition agreement with the reference reducer;
- `100%` complete action-universe and scorer validation;
- no undeclared overflow, omission, or hidden fallback.

Any violation is `DESIGN_OR_IMPLEMENTATION_FAIL`; it is not averaged away.

### 9.2 Bounded-history gate

For every archive-padding twin family at fixed active frontier:

- canonical packet bytes and semantic IDs are identical;
- the set of primitive domain objects inspected by the materializer is identical;
- any additional work is limited to explicitly logged index metadata operations;
- no candidate enumerates the dormant journal, expands a recursive summary, or follows an archive-proportional pointer chain;
- p95 materialization latency and index operations are reported at every `H`, without claiming asymptotic proof from finite points.

If no candidate passes, bounded continuity is falsified for this workload. If at least one passes, the bounded-history principle survives regardless of whether TN wins mechanism selection.

### 9.3 Mechanism recommendation

Eligible mechanisms are compared after one unmeasured warm-up and 30 measured local materializations per frozen seed/scale cell on the same otherwise idle host. They are compared on:

- exactness and declared failure rate;
- maximum-archive p95 primitive reads and index operations;
- cumulative write/update work;
- p95 materialization latency;
- artifact bytes and reconstruction time;
- implementation surface measured as frozen reducer/materializer branches, not subjective elegance.

Report the Pareto frontier. A more elaborate mechanism earns a recommendation only by strict dominance on at least one load-bearing dimension without regression on the other frozen dimensions. If mechanisms are byte- and cost-equivalent within measurement resolution, prefer the order `FD`, then `FC`, then `TN` and record that typing did not earn its complexity.

## 10. Process-cold reconstruction

Every candidate artifact is reconstructed by a fresh child process with:

- a sanitized working directory and environment;
- no generator, reference reducer, scenario module, or prior process cache importable;
- opaque randomized scenario IDs;
- only the candidate artifact, frozen decoder, schema, and explicit configuration available;
- network disabled during deterministic reconstruction;
- exact child PID capture, timeout, wait, termination, and cleanup.

Required witnesses:

1. artifact withheld → reconstruction fails;
2. artifact corrupted → reconstruction fails loudly;
3. ambient source directory renamed → valid artifact still reconstructs;
4. valid artifacts swapped between opaque scenario IDs → decoded state swaps;
5. one independent field mutation → only the causally dependent decoded field changes;
6. nonce-only artifact → fails the information-sufficiency witness.

## 11. Conditional paid A→B→A stage

### 11.1 Deterministic primary packet selection

Before any model output exists, select one Stage-1-eligible primary bounded mechanism lexicographically by:

1. minimum p95 primitive objects inspected at `H = 100,000`, `F <= 16`;
2. minimum p95 materialization latency;
3. minimum cumulative write work;
4. minimum artifact bytes;
5. tie-break order `FD`, `FC`, `TN`.

The full Pareto frontier remains reported. Selection cannot use model outcomes.

If another mechanism emits byte-identical packets, its Stage-2 result is the same shared call and cannot support a mechanism claim.

### 11.2 Primary paid comparison

The primary comparison is the selected bounded packet `BC` against oracle-minimal `OM`. OM contains exactly the public semantic objects required for the decision, in the same packet schema, without due labels or answer IDs.

The estimand is the paired mean of:

```text
delta_i = contract_success_i(BC) - contract_success_i(OM)
```

This is a usability/noninferiority screen, not a typed-versus-flat contest.

### 11.3 Diagnostic conditions

On a frozen 25% subset, also run:

- **LR:** exact due-obligation enumerator + current observation + recent public window + BM25 public evidence, with coarse terminal suppression;
- **EF:** complete public evidence in canonical order where it fits the target context;
- **XT:** EF plus process-residue/tool-trace distractors under the same maximum input-token envelope, using frozen oldest-residue-first truncation;
- **CO:** current observation and available actions only.

EF and XT are separate because complete evidence and operational exhaust are different baselines. Diagnostic cells cannot create the primary conclusion.

### 11.4 Same-model handoff discipline

- A and B are role labels on fresh stateless calls to the same frozen endpoint.
- No provider conversation/thread chain is reused.
- A never receives B scratch or hidden reasoning.
- B receives only `TaskPacketV1` and returns only `WorkerHandoffV1`.
- The deterministic writer commits or rejects B's proposal.
- The final A call reconstructs from the committed artifact after another process-cold restart.

## 12. Paid-stage inference and cost discipline

### 12.1 Cohort and looks

Run in frozen blocks of 24 independent scenarios. Evaluate the primary paired endpoint only at cumulative `n = 96, 192, 384`. The 25% diagnostic allocation is frozen before dispatch.

### 12.2 Primary interval

`delta_i` is bounded in `[-1,1]`. Use the predictable plug-in empirical-Bernstein confidence-sequence construction for bounded means from Waudby-Smith and Ramdas, with two-sided family level `95%`, implemented from a pinned audited reference or independently verified against published examples.

Before paid inference, Gate 5 must verify by exact enumeration and simulation that:

- coverage is at least 95% over the attainable paired binary support;
- optional stopping at the three looks preserves coverage;
- missing-pair rules preserve the claimed interval;
- the implementation matches an independent reference on hand-computed and randomized fixtures.

No Student-t, normality, pilot variance authority, post-hoc distribution family, or unbounded grid is permitted.

### 12.3 Decision rule

The operational noninferiority margin for this first usability screen is `-0.10` on scenario contract success.

- `PROMOTE_TO_COORDINATION_STAGE` if the 95% lower confidence-sequence bound for `mean(delta)` is greater than `-0.10` and every deterministic hard gate still holds.
- `MODEL_INTERFACE_FAIL` if the 95% upper bound is less than `-0.10` while OM performance is above the frozen oracle floor.
- `MODEL_OR_INTERFACE_CEILING` if OM performance is below the oracle floor.
- otherwise `INCONCLUSIVE_OR_UNDERFUNDED` at `n = 384`.

The oracle floor is `0.80` scenario contract success, frozen before dispatch and checked by a separate schema/interface engineering smoke; it cannot be learned from confirmatory outcomes. The `0.80` floor and `0.10` margin are explicitly owner/operator tolerances for a first-stage usability screen, not universal scientific constants.

### 12.4 Missingness

- Retry only failures proven to occur before request acceptance.
- Any accepted/no-body ambiguity makes the whole paired scenario missing.
- No reserve scenario substitutes into the frozen cohort.
- Report arm/order/pressure association.
- Apply worst-case bounds by assigning every missing pair both `-1` and `+1`; the decision must be unchanged.
- Stop as `TRANSPORT_INCONCLUSIVE` if missing pairs reach 5% or association/correlation can tip the decision.

### 12.5 Cost authorization

Before any paid engineering smoke or confirmatory call, produce a complete table for `n = 96, 192, 384` covering:

- BC and OM calls for every scenario;
- LR/EF/XT/CO calls on 25%;
- exact maximum input/output tokens;
- target provider/model price;
- expected and worst-case retry/missing overhead;
- deterministic reconstruction starts;
- total dollar ceiling and wall-clock estimate.

No run begins without a separate owner authorization naming the endpoint and maximum spend.

## 13. Transport and runner

The paid runner is a direct single-in-flight files/HTTPS program, not an agent framework, service, database, daemon, or plugin.

Before dispatch freeze and hash:

- exact model slug and provider endpoint;
- provider allowlist and `allow_fallbacks = false` equivalent;
- required parameter/structured-output support;
- tokenizer and request serializer;
- system/user messages and packet bytes;
- temperature, seed if supported, max output, and timeout;
- cache/session identifiers and policy;
- routing, transform, fallback, and response metadata fields required for cell identity.

An endpoint/provider/transform/cache mismatch is not silently accepted as another draw. It is a missing pair under section 12.4.

## 14. No-model gates

### Gate 0 — source and original-question traceability

- Every design claim maps to continuity, mechanism selection, or model usability.
- Typed-mechanism failure cannot kill bounded continuity.
- Multi-writer, cross-model, procedural, and production claims remain excluded.

### Gate 1 — algebra, generator, and scorer

- Complete transition table and illegal-transition errors.
- Independent reducer/enumerator agreement.
- Exhaustive small traces and hand-authored long interactions.
- SAT/enumerator proof that every generated world satisfies cardinality and action-universe constraints.
- Gold-taint canaries and exact manifest hashes.

### Gate 2 — mechanism parity and strong-simple controls

- FD/FC/TN generous-envelope semantic and byte parity.
- Coarse-invalidation and strong flat-derived paths exercised.
- Unique-packet deduplication proven.
- No empty field asserts absence unless reference-proven.
- Pareto accounting and lexicographic primary selection reproduced independently.

### Gate 3 — archive/frontier and reconstruction

- Archive-padding twin packet identity.
- Primitive-object inspection identity at fixed frontier.
- Separate frontier-width curve and explicit `FRONTIER_LIMIT` behavior.
- All six artifact-causal reconstruction witnesses.
- Exact process wait/termination and zero child leakage.

### Gate 4 — handoff and idempotency

- Task/handoff schema exactness.
- No transcript/scratch inheritance.
- Duplicate, stale, rejected, and committed proposal traces.
- Exactly-once governed transition or demonstrably idempotent equivalent.
- A→B→A deterministic replay equality.

### Gate 5 — inference, transport, and cost

- Independent bounded-mean confidence-sequence validation.
- Exact paired-support and missingness fixtures.
- Mock transcripts for transport identity, ambiguity, malformed output, and fallback.
- Exact call/token/dollar table and hard ceiling.
- Two non-confirmatory end-to-end smoke scenarios only after owner authorization.

Only after all gates pass and a fresh sealed council finds no P0/P1 scientific blocker may Stage 2 be proposed for owner authorization.

## 15. Run artifacts and cleanup

Each run writes into one run-owned directory containing:

- frozen config and source hashes;
- world/action/gold manifest hashes;
- public journals and candidate artifacts;
- reference/candidate packets and materialization manifests;
- reconstruction witness logs;
- exact request/response bytes and transport metadata;
- mechanical scores, confidence-sequence state, and decision trace;
- cost ledger and cleanup manifest.

Cleanup must prove:

- every child process was waited and terminated;
- no watcher, daemon, browser session, or helper remains;
- no run-owned temporary directory remains outside the declared run root;
- no unrelated user file or process was modified.

## 16. Interpretation boundaries

A Stage-1 pass means bounded external operational continuity is feasible for the frozen workload and active-frontier envelope. It does not mean an immortal model mind exists.

A TN mechanism win means typed materialization earned an engineering advantage under the frozen cost dimensions. It does not mean typing universally improves model accuracy.

An FD or FC recommendation means Moonwalker should use the simpler mechanism until another workload demonstrates a typed advantage. It does not mean the memory program failed.

A Stage-2 pass means one frozen model can use a validated selective packet through a cold logical handoff within the declared margin. It does not prove different models are interchangeable or that concurrent workers coordinate correctly.

The next experiments, only after MBCX-01, are:

1. cross-model selective worker inheritance and procedural transfer;
2. concurrent worker proposals, adjudication replay, and multi-writer semantics;
3. shared discovery/scoped promotion;
4. long-horizon hot/cold continuity and larger active-frontier scaling.

## 17. Prior art used as method, not answer

The design borrows:

- append-only evidence plus rebuildable projections from event sourcing and the Muninn ground truth;
- durable logical identity and prospective obligations from virtual actors and durable workflows;
- dependency registration and clean-rebuild oracles from build systems and incremental computation;
- matched strong-flat and projection-time controls from StateFuse and render-confound work;
- module/phase decomposition from agent-native memory-system evaluations and phase-aware profiling;
- selective declarative handoff rather than transcript inheritance from shared selective persistent memory;
- typed proposal/reference execution separation from Text2Mem-style contracts;
- bounded-mean sequential inference from Waudby-Smith and Ramdas.

No cited work establishes this exact conjunction: exact due-obligation continuity, bounded archive-independent materialization, strong flat/coarse/typed mechanism parity, artifact-causal reconstruction, and same-model A→B→A selective handoff under one preregistered instrument.

## 18. Authorization

This is a design artifact only. It authorizes no harness implementation, browser mutation, external message, paid model call, or experiment run.
