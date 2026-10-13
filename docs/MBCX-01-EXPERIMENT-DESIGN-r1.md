# MBCX-01 — bounded-continuity kernel experiment

## Scientific design and preregistration contract — revision 1

**Status:** Design candidate for experiment-specific council review

**Date:** 2026-08-11

**Owner:** Clinton Cuzzort

**Prepared by:** Codex

**Authorization:** Design only. No paid inference is authorized by this document.

---

## 1. The question

Moonwalker needs one answer before it builds a production Munin memory layer:

> Under the same capable model, admitted observations, prompt budget, decision interface, and exact provider condition, does a bounded typed and versioned continuity kernel preserve current state and future obligations materially better than the strongest simple deterministic ledger after conversational context is gone?

This is not a test of whether “memory helps.” It is a test of whether the additional machinery in the proposed kernel earns engineering over a brutally strong simple alternative.

A positive result must be attributable to the representation and materialization contract. A negative result must give the typed kernel a fair chance. If either statement is false, the experiment is not ready to spend money.

## 2. Laboratory doctrine

MBCX-01 is a temporary scientific instrument, not a Moonwalker subsystem.

The experiment may reuse, adapt, or directly borrow useful generators, scorers, adapters, runners, and test techniques from prior work whenever that reduces implementation error or makes the comparison harder to fool. Prior art has two load-bearing jobs:

1. Determine whether the question has already been answered or can be narrowed.
2. Supply mechanisms that improve the instrument.

The experiment does not require Moonwalker production architecture, security hardening, distribution readiness, a seal chain, FIPS posture, a PR workflow, generalized child-process ownership, or independent reimplementation of every borrowed component. Those become relevant only if a mechanism survives and is selected for production.

The governing rule is:

> Borrow the mechanism; rerun the claim.

No paper's reported conclusion is treated as the answer to MBCX-01 unless its causal contrast, workloads, budgets, and outcome definition actually match this experiment.

## 3. Scope

### 3.1 In scope

- Prospective obligations triggered by later time, event, state, dependency, or monitoring cues.
- Current mutable state and explicit corrections.
- Cancellation, completion, rescheduling, and supersession.
- Appropriate non-selection of stale, completed, canceled, superseded, and wrong-scope material.
- Dependency closure and scope isolation.
- Reconstruction from persisted memory with no retained conversation.
- Bounded memory-payload construction.
- Deterministic scoring and failure classification.
- Exact observable model/provider/request controls needed to keep the comparison fair.
- Tokens, latency, and inference cost as secondary engineering outcomes.

### 3.2 Out of scope

- Production Munin or Moonwalker integration.
- Multi-conductor sharing, brain slots, leases, or concurrent memory ownership.
- Personality, emotion, relationship memory, ephemeral mood, procedural learning, or general semantic memory.
- Hostile actors, prompt-injection defense, security certification, cryptographic provenance, or distribution readiness.
- Natural-language memory writing in Stage A.
- Generality across model families or providers in Stage A.
- OS-crash durability, distributed execution, GPUs, daemons, or a general agent framework.

## 4. Two-stage causal program

### 4.1 Stage A — representation isolation

Stage A changes one causal factor: the persisted memory representation and the deterministic packet derived from it.

Both primary arms receive the same canonical admitted public events. Both memory artifacts are maintained by deterministic code. Both decision calls use the same model, exact provider endpoint, prompt envelope, payload budget, action schema, output budget, retries, and run schedule. Neither primary arm asks the decision model to rewrite memory.

Stage A answers:

> Does the richer typed continuity representation materially outperform a strong flat current-state/obligation ledger when writer quality is held equal?

### 4.2 Stage B — ecological writer and controller test

Stage B is authorized only if Stage A is not killed.

Stage B crosses two factors:

- Representation: flat ledger versus typed continuity.
- Writer: deterministic admission versus model-based natural-language admission and maintenance.

The resulting 2×2 factorial separates representation value from writer/controller quality. Retrieval, provider-native compaction, and other ecological baselines may be added as descriptive comparisons only after the factorial is identified and costed.

Stage B is a separate design and preregistration. A Stage A win must never be reported as proof that natural-language writing, production retrieval, or end-to-end Munin works.

## 5. Stage A arms

### 5.1 Primary Arm L — deterministic flat ledger

Arm L is intentionally simple and intentionally strong.

Its deterministic reducer maintains:

- Latest public value for each `(scope, state_key)`.
- Open obligations with ID, action, trigger, scope, dependencies, and current status.
- Explicit completion, cancellation, reschedule, and removal from the active set.
- A small closed-ID set sufficient to prevent duplicate execution.

It does not maintain version chains, supersession graphs, conflict objects, provenance closure, validity intervals, or typed dependency traversal. Corrections overwrite current flat state; canceled or superseded obligations leave the active ledger.

At each decision it serializes the current flat facts and open obligations under the common memory-payload budget.

### 5.2 Primary Arm T — deterministic typed continuity kernel

Arm T persists immutable admitted evidence and deterministically materializes:

- Versioned scoped state assertions with validity.
- Obligations with typed triggers and explicit lifecycle status.
- Dependency edges and required closure.
- Completion, cancellation, reschedule, conflict, and supersession relationships.
- Evidence references and correction provenance.

At each decision it assembles a bounded packet containing current scoped state, due and near-due obligations, relevant dependency closure, active corrections or conflicts, and the minimum provenance needed to ground the decision.

If required structural closure cannot fit, Arm T returns `budget_failure`; it may not silently omit a required dependency.

### 5.3 Diagnostic controls

The following controls are diagnostic and run on a frozen subset unless the pre-run cost manifest shows they are cheap enough to run everywhere:

- **No persistent memory:** confirms that memory-required cases cannot be solved from the current observation alone.
- **Budgeted chronological history:** strongest ordinary context baseline while it fits; drops oldest complete observations only after the common budget binds.
- **Oracle-minimal:** smallest gold-derived packet logically sufficient for the current decision.
- **Oracle-all-relevant:** all gold-relevant public facts and obligations for the current decision.

Oracle arms are exempt from model-path gold isolation by definition, are clearly labeled non-deployable, and are used only to distinguish memory-selection failure from decision-model failure. Neither oracle participates in the primary causal estimate.

### 5.4 Deferred arms

Model-written TODO ledger, lexical/BM25 retrieval, vector retrieval, provider-native compaction, and active archive search are deferred from the Stage A primary family. They may be added as descriptive diagnostics if existing code makes them nearly free, but they cannot replace or weaken Arm L.

## 6. Treatment-isolation contract

Every primary cell receives identical:

- Scenario and public event stream.
- Current public observation.
- Available actions and channel-query affordances.
- Model, exact provider endpoint, parameters, reasoning configuration, tools, and timeout policy.
- Fixed system and task instructions except a short arm-neutral declaration of the supplied memory format.
- Memory-payload token budget.
- Action-only output schema and output-token budget.
- Arm-order randomization block.

The decision model returns the same JSON shape in both arms:

- `ongoing_choice`
- `action_ids`
- `channel_queries`
- `state_claims`
- `provenance_ids`

No primary-arm output contains a rewritten ledger or memory artifact. Memory maintenance happens outside the decision output for both arms. This closes the r0 writer-quality and output-burden confounds.

The primary treatment is the information structure exposed by the flat ledger versus the typed bounded packet. Any other arm-specific capability, extra call, hidden tool, tokenizer, repair allowance, or maintenance budget invalidates the causal comparison.

## 7. Public evidence, private gold, and architecture neutrality

The world produces two physically separate objects:

### 7.1 Public admitted event

- `event_id`
- `observed_at`
- `actor`
- `scope`
- `channel`
- `event_kind`
- `natural_language_text`
- public action or task handles introduced at that step
- canonical public transition fields needed by deterministic admission

Both primary adapters receive the exact same public object. Arm T may not receive a more semantically resolved event than Arm L.

### 7.2 Private gold

- Correct due-action set.
- Canonical current state and obligation status.
- Hidden channel contents not yet queried.
- Stress stratum and scoring labels.
- Oracle-selection metadata.

Private gold is accessible only to scenario validation, oracle diagnostics, and scoring. It never enters either primary memory artifact, prompt, request, cache, retrieval index, or provider log.

### 7.3 Architecture-privilege tests

Before paid inference, the generator must pass:

- Byte-level canaries proving private fields cannot enter public serialization.
- Differential tests proving both primary adapters receive byte-identical admitted events.
- A current-observation-only solver check for every memory-required item.
- A representation-blind scenario invariant check.
- Held-out hand-authored challenge scenarios that were not generated from Arm T's ontology.
- A review showing that public transition fields do not encode the correct action set or precompute Arm T's packet.

## 8. Scenario design

Scenarios simulate a domain-neutral control room coordinating multiple people, scopes, or projects. Specialist knowledge must not decide the task.

Each confirmatory scenario contains 40–60 decision steps and must include:

- At least three scopes.
- At least 24 prospective obligations.
- At least six cross-boundary obligations.
- At least six explicit updates spanning cancellation, completion, reschedule, supersession, and value correction.
- At least four dependency-triggered obligations.
- At least four hidden-channel or monitoring cues.
- At least four wrong-scope lures.
- At least four completed/canceled/superseded lures.
- Naturalistic distractors between creation and execution.
- At least 30 scored high-stress due or non-due opportunities.
- Three reconstruction boundaries near 25%, 50%, and 75% of the trajectory.

The minimum of 30 high-stress opportunities makes the target +0.08 set-F1 effect roughly equivalent to multiple changed decisions rather than a single lucky obligation.

The generator is deterministic from configuration and seed. Development, engineering-pilot, and confirmatory seeds are disjoint. Confirmatory seeds are frozen before inference and are not manually inspected beyond automated invariant summaries.

Every scenario must prove:

- Stable unique identifiers.
- Realizable triggers and available due actions.
- Valid update targets.
- Correct cancellation, reschedule, supersession, and completion state.
- Dependency graph validity.
- Correct non-due lures.
- No memory-required decision is solvable from only the current observation.
- Chronological public history exceeds the common memory budget by a declared factor on the budget-pressure slice.
- Oracle-minimal and oracle-all-relevant policies recover the expected gold action set before any model call.

## 9. Budget contract

The initial common memory-payload budget is 6,000 tokens. The exact tokenizer or provider-compatible counter is frozen in the run manifest and verified against actual request accounting before confirmation.

The common system prompt and current observation are outside the memory payload but identical across arms. Both primary arms receive the same action-only output limit, initially 512 tokens.

Gate 0 renders maximum-load payloads and output fixtures for every arm and proves:

- The action schema fits with equal headroom.
- No primary arm pays an arm-specific maintenance-output tax.
- Every over-budget path fails explicitly.
- No local or provider middle-out compression, silent truncation, or arm-specific summarization occurs.

Realized input, memory-payload, output, and any cache-read/write tokens are logged per request.

## 10. Reconstruction construct

Every decision call is a fresh provider request assembled from the fixed prompt, current observation, and persisted arm artifact. No prior chat transcript is supplied unless the arm itself is the chronological diagnostic.

At each reconstruction boundary:

1. Persist and close the arm artifact.
2. End the current decision process.
3. Start a fresh interpreter process through a tiny synchronous supervisor.
4. Reopen only the designated persisted artifact and public scenario cursor.
5. Reconstruct the next payload through the same adapter entry point used at ordinary start.
6. Record a reconstruction audit before the next decision.

This measures **process-cold reconstruction from the arm artifact**. It does not claim power-loss durability, host-crash recovery, or distributed failover.

The supervisor owns only the one explicit child it starts, waits for it, and terminates that exact child after a bounded grace period if necessary. No generalized PID registry, broad process killing, stale-process census, daemon, or production lifecycle subsystem belongs in MBCX-01.

## 11. Harness substrate

### 11.1 Default

Stage A uses a thin Python runner with:

- Deterministic scenario loader and validator.
- One adapter interface shared by Arm L and Arm T.
- Stateless request builder.
- Direct asynchronous provider client with concurrency one by default.
- Append-only JSONL event/request/response log.
- SQLite or simple files only where they reduce implementation risk.
- Deterministic scorer and frozen analysis script.

Existing code from PM-Bench, AgenticSTS, LongHorizon-Harness, Inspect, Harbor, or another framework may be reused where it shortens this instrument without changing the comparison.

### 11.2 Inspect acceptance gate

Inspect may replace the direct runner only if a no-paid-inference conformance test proves:

- Every decision receives a freshly constructed message list.
- `TaskState.messages` or equivalent hidden history cannot reach the request.
- Local and provider prompt caching is disabled or demonstrably identical and non-contaminating.
- Raw observable request content is equivalent across the direct and Inspect paths.
- A mid-cell interruption cannot silently reuse a dirty arm artifact or selectively reroll a completed decision.
- Checkpoint failure is fatal, not warning-and-continue.
- Actual retry and resume identity is explicit in the log.

If the test fails or requires a large compatibility layer, use the direct runner. Framework adoption is an engineering convenience, not an experimental objective.

## 12. Model and provider condition

Stage A intentionally uses one capable model on one exact provider endpoint. It does not estimate provider variance or cross-model generality.

The pre-run manifest freezes:

- Canonical model identifier, never `auto`, `free`, or a rolling alias.
- Exact routable provider endpoint, not only a base provider family.
- Reasoning effort, temperature, supported seed, output limit, and tool schema.
- Request wrapper and API version.
- Context length and supported parameters.
- Cache posture.
- Timeout and retry policy.
- Observable pricing used for the cost estimate.

Every request disables fallbacks and context-compression or message-transform plugins, requires supported parameters, and records returned model/provider/endpoint and transformation metadata.

If the transport cannot reliably bind the exact endpoint, MBCX-01 uses a direct provider transport that can. A cell is invalid if the exact condition did not hold. Provider drift is not analyzed; it is removed or invalidates the cell.

## 13. Run order, retries, and hidden-state controls

- Pair by scenario: both primary arms run the same world.
- Randomize and counterbalance Arm L/T order within scenario.
- Interleave scenarios so wall-clock position cannot identify an arm.
- Freeze the complete schedule before the first confirmatory response.
- Default to one in-flight model request; any increase must preserve the frozen order blocks.
- Retry only transport failures that produced no model output.
- A retry keeps the same cell identity and clean pre-attempt artifact snapshot.
- A model response is never selectively rerolled.
- One schema-repair call is permitted only if identical for both arms and counted as failure/cost metadata.
- Any hidden conversation, local cache hit, provider transform, fallback, or dirty resume invalidates the affected cell.

## 14. Outcomes and scoring

### 14.1 Primary outcome

For each confirmatory scenario:

`delta = high_stress_set_f1(typed) - high_stress_set_f1(flat_ledger)`

The scenario is the paired unit. Decisions within a trajectory are not independent samples.

### 14.2 Secondary outcomes

- Overall due-action set-F1.
- Stale/canceled/superseded/wrong-scope false-action rate.
- Cross-boundary hit rate.
- Update-sensitive hit rate.
- Dependency-trigger hit rate.
- Hidden-channel monitoring and action rate.
- Exact current-state and obligation-state reconstruction.
- Duplicate execution rate.
- Provenance precision/recall, reported as a mechanism diagnostic rather than an automatic win.
- Payload tokens, total input/output tokens, latency, retries, and cost per correct action.
- Oracle gaps.

All task outcomes are scored mechanically. No LLM judge may override them.

## 15. Pilot, sample size, and decision rule

### 15.1 Engineering pilot

Run 12 held-out paired scenarios after all no-model gates pass. Pilot scenarios are excluded from confirmation.

The pilot may estimate:

- Paired outcome variance.
- Token/cost/latency range.
- Schema and harness failure rates.
- Realized budget pressure.

Pilot direction or preferred-arm performance may not change prompts, outcomes, thresholds, or scenario inclusion. Any design repair after seeing pilot outcomes creates a new revision and a new pilot set.

### 15.2 Confirmatory sample size

Use a simulation-based paired power analysis over the bounded scenario outcome, with target effect `+0.08`, two-sided alpha `0.05`, and power `0.80`. Use a conservative upper uncertainty bound for pilot paired variance rather than treating the 12-pair estimate as known.

The confirmatory minimum is 48 paired scenarios. There is no silent maximum clamp. If the estimated requirement exceeds the approved inference budget, do not run an underpowered confirmation and call a negative result. Instead, before confirmation begins, either:

- Increase scored opportunities per scenario and repeat the pilot;
- Reduce non-primary diagnostic inference;
- Approve the required budget; or
- Report that the decisive experiment is presently underfunded.

Freeze sample size, seeds, schedule, model/provider manifest, prompts, adapters, scorer, and analysis code before the first confirmatory response.

### 15.3 Primary interval and sensitivity analysis

Report:

- Mean paired delta.
- Scenario-clustered paired bootstrap 95% confidence interval.
- Raw scenario pairs.
- An exact or Monte Carlo paired-permutation sensitivity test.
- Preselected stability replicates for 20% of cells, reported separately from the primary one-run-per-cell estimate.

No optional stopping or result-driven scenario addition is permitted.

### 15.4 Win

Continue investment in the typed kernel only if all hold:

1. Mean primary improvement is at least `+0.08` high-stress set-F1.
2. The 95% paired interval excludes zero.
3. Overall set-F1 is not more than `0.02` below the best non-oracle diagnostic baseline.
4. The upper confidence bound for excess stale/wrong-scope actions is below `+0.02`.
5. Process-cold reconstruction succeeds on at least 95% of required state fields, with uncertainty reported.
6. Typed packets stay within budget without silent loss of structural closure.
7. No gold leakage, hidden-history contamination, fallback, or transform invalidated the comparison.

The `+0.08` target is tied to the scenario minimum of 30 high-stress opportunities: it represents multiple changed decisions, not one isolated obligation.

### 15.5 Kill

Do not build the current rich kernel merely for architectural elegance if any holds:

- The upper 95% confidence bound for improvement over the strong flat ledger is below `+0.03`.
- The typed arm materially increases stale or wrong-scope actions.
- Required closure repeatedly cannot fit the fixed payload budget.
- The apparent advantage disappears when writer quality and output burden are matched.
- The result depends on gold leakage, architecture-privileged generation, hidden context, caching, fallback, transforms, or an unfair retry policy.

### 15.6 Inconclusive

Anything between win and kill is inconclusive. It may justify one new preregistered replication or a targeted ablation, but it is not a successful architecture.

## 16. Failure classes

Each failed decision receives one primary label and optional secondary labels:

- `admission_mismatch`
- `update_not_applied`
- `stale_memory_selected`
- `wrong_scope_selected`
- `dependency_missing`
- `packet_budget_failure`
- `reasoning_failure_with_sufficient_packet`
- `monitoring_failure`
- `schema_failure`
- `provider_condition_violation`
- `hidden_state_contamination`
- `retry_identity_failure`
- `harness_failure`
- `gold_leakage`

Packet and adapter audits must make storage, materialization, selection, and reasoning failures distinguishable.

## 17. No-model and no-cost gates

Before any paid inference:

### Gate 0 — world and scorer

- Generator invariants and state-transition property tests.
- Gold-taint canaries.
- Hand-authored ontology-independent challenge scenarios.
- Exact scorer fixtures.
- Current-observation-only failure checks.
- Oracle-minimal and oracle-all-relevant policy checks.

### Gate 1 — arm parity

- Byte-identical admitted events reach both primary arms.
- Maximum-load payload and output-budget tests.
- Flat and typed reconstruction golden tests.
- Arm-order schedule generation and replay.
- Retry from a clean snapshot.
- No arm-specific model calls, tools, repair budget, or maintenance output.

### Gate 2 — transport/substrate conformance

- Mock-provider transcript of exact request bytes.
- Exact model/provider endpoint controls represented in the request.
- Fallbacks/transforms disabled.
- Cache posture verified.
- Hidden message/history absence verified.
- Interrupted-cell identity and fail-loud behavior verified.

### Gate 3 — engineering smoke

- Two non-confirmatory scenarios through all primary paths.
- Mock provider or inexpensive model.
- Logs, scorer, cost accounting, reconstruction child, and temporary cleanup verified.

Only after these gates pass may the 12-pair pilot begin.

## 18. Artifacts and cleanup

Every run keeps only what is needed to understand and reproduce the scientific result:

- Frozen run manifest and schedule.
- Scenario configuration and seeds.
- Public events and separately protected private gold.
- Prompts, observable requests/responses, endpoint metadata, and packet audits.
- Arm artifacts and reconstruction audits.
- Raw mechanical scores and frozen analysis outputs.
- Token, latency, retry, cache, and cost accounting.

Temporary files live in one explicit run directory. The foreground runner closes its database/files, waits for or terminates only its one explicit reconstruction child, and removes run-owned disposable files. It never broadly kills processes, touches unrelated ports, or leaves a daemon. This is ordinary experiment hygiene, not a production lifecycle subsystem.

## 19. Interpretation

### 19.1 Positive Stage A

A positive result supports building a serious prototype of the typed current-state/obligation kernel. It says the richer representation contributed measurable value beyond a strong deterministic simple ledger under the tested model/provider condition.

It does not prove natural-language writing, production retrieval, general memory, personality, emotion, procedural learning, multi-agent sharing, open-world sufficiency, or cross-model generality. Those remain separate experiments.

### 19.2 Negative Stage A

If the flat ledger matches the typed kernel within the kill margin, Moonwalker should prefer the simpler mechanism unless a predeclared stress slice shows a narrow typed advantage worth isolating. The result may justify typed structure only for corrections, dependency closure, or scope isolation rather than as a universal memory substrate.

### 19.3 Poor oracle performance

If oracle diagnostics perform poorly, the bottleneck is the decision model, action interface, or scenario—not the memory representation. The kernel comparison must not be interpreted as decisive.

## 20. Prior-art targets

The experiment-specific council must independently search beyond this list. Known high-value starting points include:

- PM-Bench prospective-memory world, scoring, scaffolds, updates, lures, and ledger behavior.
- AgenticSTS bounded typed memory, fresh-message assembly, and ablation structure.
- LongHorizon-Harness externalized state and fresh-executor pattern.
- Mem2ActBench memory-grounded action evaluation.
- LongMemEval-V2 controller/accuracy/latency tradeoffs.
- Inspect message accumulation, caching, checkpoint, retry, and logging behavior.
- OpenRouter exact provider routing, transforms, caching, and returned metadata.
- Paired bounded-outcome inference, internal-pilot variance uncertainty, bootstrap, and permutation methods.
- Evaluation-framework alternatives such as direct runners, Harbor, Inspect, OpenAI Evals, and tau2-bench.

Prior-art review is complete only when it answers whether the experiment is obsolete, narrower than proposed, missing a stronger comparator, or needlessly rebuilding an experimental mechanism.

## 21. Authorization gates

This document, if approved, authorizes only implementation planning and experiment-specific council review.

Separate owner approval is required for:

1. Harness implementation.
2. The frozen pilot run manifest and cost cap.
3. Any paid pilot inference.
4. The frozen confirmatory manifest and cost cap.
5. Confirmatory execution.
