# Moonwalker Bounded Continuity Experiment

## Design specification and preregistration contract

**Document status:** Approved architecture; specification awaiting owner review  
**Date:** 2026-08-11  
**Owner:** Clinton Cuzzort  
**Prepared by:** Codex (GPT-5 family; exact runtime model identifier not exposed in this task)  
**Experiment codename:** MBCX-01  
**Planned execution state:** Not implemented and not authorized to run until this specification is reviewed and approved  

---

## 1. Executive decision

Moonwalker should not begin by building a production Munin memory system and then trying to decide whether it works. The first implementation should be a standalone, provider-neutral experimental harness that can falsify the smallest central claim:

> Under an identical model, observation stream, prompt budget, reasoning configuration, and provider, a bounded typed and versioned memory projection should preserve current state and future obligations better than chronological history, a model-maintained ledger, and simple retrieval—especially after forced cold restarts.

This experiment tests the **bounded continuity kernel** only. It does not initially test shared memory among conductors, brain slotting, personality, emotion, procedural skill learning, full semantic memory, or production integration with Moonwalker. Those layers are downstream of the kernel. If the kernel cannot retain, update, reconstruct, and appropriately suppress obligations under controlled conditions, distributing it among multiple brains cannot rescue it.

The recommended implementation is a clean-room Python evaluation package using **Inspect AI** as the orchestration and logging substrate, **OpenRouter** as the first model transport, and independently implemented scenario generation, memory adapters, and deterministic scorers. No PM-Bench or AgenticSTS code will be copied into the harness unless its license is verified first.

---

## 2. Why this experiment, and why it changed after prior-art review

The initial research portfolio correctly proposed a bounded-sufficiency experiment, but a fresh footnote and prior-art search found two newer testbeds that substantially sharpen the design.

**PM-Bench** directly evaluates prospective memory: maintaining delayed intentions, acting at the right time or event, handling cross-day obligations, applying cancellations and reschedules, monitoring hidden channels, and suppressing lure actions. Its released study used one deterministic 80-step simulated week, eight model backbones, and eight scaffolds. The strongest aggregate scaffold reached only 65.1% set-F1; no scaffold dominated across model families. This is close enough to Moonwalker's obligation plane that creating a generic memory-recall benchmark from scratch would be wasteful and risk missing known failure modes.

**AgenticSTS** independently implements a bounded, typed, ablatable memory contract for long-horizon decisions. Its authors explicitly identify the matched comparison against accumulating context as an open question. That means bounded typed memory exists as an architectural pattern, but the decisive controlled comparison Moonwalker needs remains unresolved.

The experiment therefore borrows the *scientific questions* and public definitions from those papers while remaining clean-room. It adds the parts most relevant to Moonwalker and insufficiently isolated in the existing work: equal prompt budgets, identical observation admission, typed current-state materialization, exact provenance, forced process restarts, explicit stale-memory suppression, strict provider controls, and a preregistered kill criterion.

This experiment is not designed to prove that “memory helps.” It is designed to determine whether Moonwalker's proposed structure contributes enough beyond a good ledger or simple retrieval to justify further engineering.

---

## 3. Scope

### 3.1 In scope

- Prospective obligations: actions that must be performed after a later time, cue, dependency, or state transition.
- Current mutable state and versioned corrections.
- Cancellation, supersession, rescheduling, and completion.
- Appropriate non-recall: withholding stale, canceled, irrelevant, or out-of-scope information.
- Dependency closure: including the minimum prerequisite state needed to interpret a selected obligation.
- Scope isolation among projects, actors, and control-room seats.
- Provenance from every materialized state item back to admitted evidence.
- Bounded prompt construction.
- Cold reconstruction from persisted memory artifacts after conversational state is erased.
- Deterministic, auditable scoring.
- Model, provider, token, cost, latency, retry, and routing instrumentation.
- Safe foreground execution with strict cleanup and resource limits.

### 3.2 Explicitly out of scope for MBCX-01

- Shared live memory among multiple conductors or workers.
- Brain slotting, lease transfer, or concurrent ownership.
- Personality, emotional state, relationship memory, or ephemeral mood.
- Autonomous consolidation of unstructured natural-language memories.
- Learned procedural skills or cross-task continual learning.
- Vector embeddings as a required dependency.
- Production Moonwalker or Munin integration.
- Docker, local inference servers, GPUs, background daemons, or distributed execution.
- Adversarial prompt injection. Ordinary stale, contradictory, irrelevant, and malformed observations remain in scope because they are data-quality and governance failures even without a malicious actor.

---

## 4. Experimental hypothesis and estimands

### 4.1 Primary hypothesis

At a fixed memory-payload budget, the Munin typed-projection arm will achieve higher scenario-level prospective-action set-F1 than the model-maintained ledger arm on the combined high-stress slice of cross-boundary obligations, corrections, dependency-triggered obligations, and hidden-cue obligations.

### 4.2 Secondary hypotheses

1. Typed projection will reduce execution of canceled, superseded, completed, or wrong-scope obligations.
2. Typed projection will reconstruct current state more accurately after a forced cold restart.
3. Typed projection will remain within a fixed prompt budget as trajectory length grows.
4. Typed projection will improve provenance correctness relative to chronological history, ledger, and simple retrieval.
5. Simple lexical retrieval will be competitive on explicit cue-matching cases but weaker on correction propagation and dependency closure.
6. Full chronological history will be a strong ceiling while it fits and will degrade or become infeasible under an equal bounded budget.

### 4.3 Primary estimand

For each held-out scenario, compute the difference:

`high_stress_set_f1(munin_typed) - high_stress_set_f1(todo_ledger)`

The primary estimate is the mean paired difference across scenarios. Inference is clustered at the scenario level. Individual decisions within one scenario are not treated as independent samples.

### 4.4 Secondary estimands

- Paired differences between Munin typed projection and each remaining non-oracle baseline.
- Difference in stale-action false-positive rate.
- Difference in post-restart exact reconstruction rate.
- Difference in prompt tokens, latency, and cost per correct prospective action.
- Gap from the oracle-minimal ceiling.

---

## 5. Experimental arms

Every arm receives the same system instructions, current observation, available actions, tool schema, output schema, virtual time, model configuration, and public observation envelope. The only treatment variable is the persisted memory representation and the memory payload assembled for the next decision.

### Arm A — Budgeted chronological history

Persist all admitted public observations in order. At each decision, include as much chronological history as fits within the common memory-payload budget. If the history exceeds the budget, remove the oldest complete observations first. Never silently remove text from the middle and never ask the provider to compress it.

On short calibration scenarios where the entire history fits inside the same budget, this arm is also labeled `full_history_fits`. It serves as the strongest honest full-context baseline.

### Arm B — Model-maintained TODO ledger

The decision model carries forward a compact ledger containing obligation ID, action, trigger, scope, dependencies, and status. At each step it emits both its action decision and the rewritten ledger. The ledger is persisted across cold restarts.

This is the primary baseline because PM-Bench found a ledger to be a strong low-noise scaffold and because it is the simplest plausible alternative to building Munin.

### Arm C — Simple lexical retrieval

Persist each public observation as an immutable record. At decision time, retrieve records using SQLite FTS5/BM25 plus a fixed recency allocation. Deduplicate records, preserve their original text, and assemble them under the same token budget.

No embedding model, vector database, local model server, or semantic reranker is included in MBCX-01. This keeps the baseline transparent, cheap, and reproducible. A hybrid lexical/vector adapter may be added in a later external-validity phase, but it must not retroactively alter the preregistered first comparison.

### Arm D — Munin bounded typed projection

Persist immutable evidence records and deterministically materialize a current projection containing:

- Current scoped state.
- Open obligations.
- Trigger kind and trigger specification.
- Dependency edges and required closure.
- Status: pending, due, completed, canceled, or superseded.
- Version and supersession relationships.
- Owner and scope.
- Evidence and correction provenance.

At each decision, assemble a bounded working packet containing current scoped state, due and near-due obligations, relevant dependency closure, active corrections or conflicts, provenance identifiers, and any public monitoring affordances. The packet builder must fail closed if it cannot preserve required structural closure within the budget. It may not silently omit a required dependency.

The first confirmatory experiment tests the automatically supplied bounded packet, not an additional free-form memory search tool. Active archive discovery is a later ablation after the projection itself survives.

### Arm E — Oracle-minimal ceiling

Assemble the smallest gold-derived packet sufficient to make the correct current decision. This arm is never considered a deployable system. It estimates the remaining reasoning error when retrieval and state selection are perfect.

### Calibration-only arm — No persistent memory

Clear all prior observations between decisions. This arm is used only to confirm that generated scenarios genuinely require memory and is excluded from the primary confirmatory comparison.

---

## 6. Fairness contract

### 6.1 Identical public evidence

The generator emits a **public observation envelope** and a separate **private gold envelope**.

The public envelope may contain:

- `event_id`
- `observed_at`
- `actor`
- `scope`
- `channel`
- `event_kind`
- `natural_language_text`
- Public task or action handles introduced at that step

The private gold envelope may contain:

- The correct due-action set.
- Hidden channel contents not yet queried.
- Canonical current state.
- Canonical obligation status.
- Scoring labels and stress strata.

Memory adapters receive only the public envelope. The scorer receives both. Gold objects must be stored behind a separate interface and never serialized into prompts, logs visible to the model, retrieval indices, or memory stores.

### 6.2 Equal prompt budget

The fixed system prompt and current observation are common overhead. Each arm receives a maximum memory payload of **6,000 tokens measured with the selected model's tokenizer or the provider's documented tokenizer-compatible counter**. Output is limited to 512 tokens and must follow a strict JSON schema.

Any arm that exceeds its memory budget must report a structured `budget_failure`. Silent provider truncation, middle-out compression, or unlogged local truncation invalidates the cell.

### 6.3 Equal model conditions

For a confirmatory block, all arms must use the same:

- Canonical model slug, not a rolling `latest` alias.
- Provider endpoint.
- Reasoning effort.
- Temperature and supported seed.
- Maximum output tokens.
- Tool definitions.
- System instructions other than the arm-neutral description of the supplied memory format.
- Request timeout, retry policy, and concurrency.

### 6.4 Treatment isolation

The current decision model must not write the Munin projection during the architecture-isolation stage. The environment emits structured public events and the deterministic memory adapter materializes them. This intentionally isolates persistence, update semantics, retrieval, and packet assembly from natural-language extraction.

If Arm D passes, a separate end-to-end write experiment will replace deterministic admission with model-based extraction. A win in the isolation stage must never be reported as proof that the write path is solved.

---

## 7. Scenario generator

### 7.1 Domain

Scenarios simulate a Moonwalker-like control room handling several people, projects, or conductor seats. The language should remain ordinary and domain-neutral enough that success depends on memory structure rather than specialist knowledge.

### 7.2 Scenario shape

Each confirmatory scenario contains 36–48 decision steps and, at minimum:

- Three distinct scopes.
- Twelve prospective obligations.
- Four cross-boundary obligations introduced well before execution.
- Four explicit updates: at least one cancellation, one reschedule, one supersession, and one value correction.
- Three hidden-channel triggers that require a monitoring decision.
- Two dependency-triggered obligations.
- Two intentionally similar but wrong-scope obligations.
- Two completed obligations that later reappear as lures.
- Naturalistic distractor observations between creation and execution.
- Three forced restart boundaries near 25%, 50%, and 75% of the trajectory.

Exact counts may vary within a preregistered range, but each scenario must satisfy the same minimum stress coverage.

### 7.3 Deterministic generation

Generation is deterministic from a seed and configuration hash. The generator uses rejection sampling until all invariants pass. Scenario seeds are divided into:

- Development seeds, visible during implementation.
- Calibration seeds, used for smoke tests and then retired.
- Pilot seeds, used only to estimate paired variance and operating cost.
- Confirmatory seeds, frozen and never inspected manually before the run except through automated invariant reports.

### 7.4 Invariants

Every scenario must pass machine checks for:

- Unique and stable IDs.
- Acyclic dependency graph unless a cycle is intentionally labeled unsatisfiable and excluded from scoring.
- Every trigger is realizable.
- Every update references an existing obligation or state item.
- No reschedule silently moves an obligation into an already elapsed period.
- Every due action is available when due.
- Every lure is non-due at the step where it appears.
- No final decision can be solved from the current observation alone on a memory-required item.
- No private gold field appears in a public serialization.
- Oracle-minimal packets reproduce the exact gold action set.

The generator writes an invariant ledger for every scenario. A failed invariant excludes the scenario before any model call and produces no experimental result.

---

## 8. Cold-restart protocol

At each restart boundary:

1. Close the active model conversation.
2. Discard all ephemeral solver state.
3. Flush and close the arm's persistent artifact.
4. Reopen the artifact through the same public adapter used after a real process start.
5. Create a fresh model conversation with only the fixed system prompt, the current observation, and that arm's reconstructed memory payload.
6. Record a reconstruction audit before the next action.

Each arm may persist only its designated artifact:

- Chronological arm: admitted public transcript.
- Ledger arm: latest emitted ledger plus immutable step log.
- Retrieval arm: immutable indexed observations.
- Munin arm: immutable evidence plus typed materialization.
- Oracle arm: no production artifact; the harness assembles the ceiling packet.

The restart is a real close-and-reopen of files and in-memory objects, but it must occur inside the same foreground harness process during MBCX-01. Process-level crash recovery can be added after the in-process reconstruction semantics are validated.

---

## 9. Memory data model for Arm D

### 9.1 Evidence record

An immutable observation admitted from the public envelope:

- `evidence_id`
- `event_id`
- `observed_at`
- `source_actor`
- `scope`
- `channel`
- `payload`
- `payload_hash`

### 9.2 State assertion

- `state_key`
- `scope`
- `value`
- `version`
- `valid_from`
- `valid_to`
- `status`
- `supersedes`
- `superseded_by`
- `evidence_refs`

### 9.3 Obligation

- `obligation_id`
- `owner`
- `scope`
- `action`
- `trigger_kind`: time, event, state, dependency, or recurring
- `trigger_spec`
- `status`: pending, due, completed, canceled, or superseded
- `dependencies`
- `created_at`
- `updated_at`
- `supersedes`
- `superseded_by`
- `evidence_refs`

### 9.4 Dependency edge

- `from_id`
- `to_id`
- `edge_kind`
- `scope`
- `validity`
- `evidence_refs`

### 9.5 Packet audit

Every assembled packet records:

- Selected record IDs.
- Selection reason for each record.
- Dependency-closure traversal.
- Records considered but rejected.
- Token count before and after serialization.
- Any collision, conflict, or budget failure.
- Packet hash.

The projection is reconstructible from immutable evidence. Materialized tables may be deleted and rebuilt without changing the canonical result.

---

## 10. Output and scoring

### 10.1 Model output schema

The decision model returns exactly one JSON object containing:

- `ongoing_choice`
- `action_ids`
- `channel_queries`
- `state_claims`
- `provenance_ids`
- `ledger` only for the ledger arm

Malformed output receives one schema-repair attempt using the same model and provider. The repair request, response, and cost are logged. Persistent malformed output is scored as an execution failure, not silently parsed by an LLM judge.

### 10.2 Deterministic metrics

For each scenario, compute:

- Set-level true positives, false positives, and false negatives over due actions.
- Macro prospective-action set-F1.
- High-stress set-F1.
- Cross-boundary obligation hit rate.
- Update-sensitive hit rate.
- Hidden-channel hit rate.
- Wrong-scope action rate.
- Canceled or superseded action rate.
- Duplicate execution rate.
- Exact state-field reconstruction rate after restart.
- Provenance precision and recall.
- Monitoring queries per correct hidden-channel action.
- Input tokens, output tokens, latency, retries, and cost.
- Memory payload p50, p95, and maximum tokens.

No LLM judge may override these metrics. If a later natural-language quality measure requires a judge, it must be secondary, blinded to arm identity, and reported separately.

### 10.3 Appropriate non-recall

For canceled, completed, superseded, and wrong-scope lures, the correct behavior is non-selection. This is not treated as “forgetting” in the sense of deleting evidence. Evidence remains auditable; its current validity prevents it from controlling behavior.

---

## 11. Preregistered analysis and decision rules

### 11.1 Pilot and sample size

Run four pilot scenarios per arm after the engineering smoke test. Pilot scenarios are excluded from confirmatory claims. Use only the paired standard deviation—not the observed direction or preferred arm—to choose confirmatory sample size for a target paired effect of 0.08 set-F1, two-sided alpha 0.05, and power 0.80:

`n = ceil(((z_0.975 + z_0.80) * paired_sd / 0.08)^2)`

Clamp the confirmatory scenario count to a minimum of 24 and maximum of 48. Freeze the resulting `n`, confirmatory seeds, model manifest, arm configurations, dataset hashes, and analysis script before running confirmatory inference.

### 11.2 Primary comparison

Arm D versus Arm B on scenario-level high-stress set-F1. Report the paired mean difference, 95% confidence interval, effect size, and raw scenario pairs.

### 11.3 Secondary comparisons

If the primary comparison passes, test Arm D against Arms A and C using Holm correction across those two comparisons. Comparisons with the oracle are descriptive and do not consume the confirmatory family-wise error budget.

### 11.4 Win condition

MBCX-01 supports continued investment in the bounded typed kernel only if all of the following hold:

1. The point improvement over the ledger is at least +0.08 high-stress set-F1.
2. The paired 95% confidence interval for that difference excludes zero.
3. Overall set-F1 is not more than 0.02 below the strongest non-oracle baseline.
4. The upper confidence bound for excess stale, canceled, or wrong-scope actions is below +0.02.
5. Exact post-restart state-field reconstruction is at least 95%, with the Wilson lower bound reported.
6. Every valid Munin packet respects the 6,000-token payload limit.
7. No unlogged provider transformation, fallback model, fallback provider, or gold leakage occurred.

### 11.5 Kill condition

Stop treating the current typed-projection kernel as justified if any of the following occurs:

- The upper 95% confidence bound for improvement over the ledger is below +0.03.
- Restart reconstruction is below 90%.
- The arm materially increases stale or wrong-scope actions.
- Required structural closure cannot be retained within the fixed packet budget.
- The measured benefit exists only because private gold information entered the public path.

### 11.6 Ambiguous condition

Any result between the win and kill regions is inconclusive. It may justify one preregistered replication or a targeted mechanism ablation, but it must not be described as a successful architecture.

No optional stopping or result-driven addition of scenarios is permitted inside the confirmatory block.

### 11.7 Stability audit

Randomly select 20% of confirmatory scenario-arm cells before inference and run two additional replicates. Use supported model seeds where available. Report within-cell variance and any arm-by-nondeterminism interaction separately from the primary single-run paired result.

---

## 12. Harness architecture

### 12.1 Substrate

Use Inspect AI for:

- Task and dataset registration.
- Stateful custom solver execution.
- Model-provider abstraction.
- Structured event and sample logging.
- Retryable interrupted evaluations.
- Exportable run configuration.
- Custom deterministic scorers.
- Token, latency, and model-usage records.

One Inspect sample represents one complete scenario trajectory. Each decision step is logged as a structured event within that sample.

### 12.2 Logical modules

The future implementation should separate:

- `world`: deterministic scenario generation and validation.
- `protocol`: observation, action, channel-query, and restart semantics.
- `memory`: one adapter per experimental arm.
- `packet`: model-specific token counting and bounded assembly.
- `solver`: identical decision loop with arm injection.
- `scoring`: deterministic trajectory and reconstruction metrics.
- `providers`: canonical model and OpenRouter routing manifests.
- `analysis`: preregistered paired statistics and plots.
- `safety`: locks, limits, signal handling, child-process ownership, and cleanup audit.

### 12.3 Adapter boundary

Every memory arm implements the same conceptual interface:

- `admit(public_observation)`
- `assemble(current_public_observation, token_budget)`
- `checkpoint()`
- `close()`
- `reopen(checkpoint_ref)`
- `audit()`

The scorer never calls arm-specific internals. The solver never receives private gold.

### 12.4 Storage

Use SQLite for immutable evidence, FTS5 retrieval, typed projections, and run metadata. Enable transactional writes and explicit checkpoints. A human-readable JSONL mirror records public events and decisions for audit. Each run writes into a unique run directory and never overwrites another run.

---

## 13. Model and OpenRouter controls

### 13.1 Canonical model manifest

Immediately before a run, resolve and freeze:

- Requested canonical model slug.
- Actual model returned by the provider.
- Provider slug and endpoint.
- Context length.
- Supported parameters.
- Input, output, reasoning, and cache prices.
- Reasoning configuration.
- Structured-output support.
- Seed support.
- Retrieval timestamp and raw model-metadata hash.

Do not use `auto`, `free`, or rolling `latest` aliases in confirmatory runs.

### 13.2 Routing controls

Every OpenRouter request must:

- Restrict routing to one named provider.
- Set `allow_fallbacks: false`.
- Set `require_parameters: true`.
- Disable context-compression plugins explicitly.
- Request strict JSON-schema output where supported.
- Opt into router metadata.
- Record the returned model, provider, attempt count, and pipeline transformations.

A cell is invalid if a different model or provider served the request, if context compression occurred, or if an undisclosed pipeline transformation changed the prompt.

### 13.3 Retry and timeout controls

Initial safe defaults:

- Model connections: 1 during calibration; maximum 2 during confirmation.
- Adaptive concurrency: disabled.
- Request retries: maximum 2 retries after the initial attempt.
- Attempt timeout: 90 seconds.
- Total decision timeout: 240 seconds.
- Schema repair: maximum 1 model call.
- Scenario time limit: 30 minutes.
- Output limit: 512 tokens per decision.

Transport retries that receive no model output may remain in the cell only if the same canonical model and provider served the successful attempt. All attempts and costs remain logged. A fallback or transformed attempt invalidates the cell; it is not silently substituted.

### 13.4 API-key safety

- Read credentials from the process environment only.
- Never print, persist, hash into public logs, or copy an API key.
- Use a dedicated experimental OpenRouter key with a user-approved hard spending limit and model/provider allowlist.
- Do not auto-top-up or change account settings.
- Refuse to start if the dedicated limit cannot be verified or the estimated run exceeds the approved cap.

---

## 14. Cost, resource, and process safety

### 14.1 Preflight

Before any paid run, produce a dry-run bill of materials containing:

- Number of scenarios, arms, steps, and expected calls.
- Expected input and output tokens by arm.
- Low, expected, and high cost estimates using the frozen price manifest.
- Expected wall-clock range.
- Approved hard cost cap.
- Disk-space estimate.

The user must explicitly approve the cost cap before inference begins.

### 14.2 CPU and concurrency limits

MBCX-01 runs as one foreground Python process with:

- `max_tasks = 1`
- `max_connections = 1` for pilot and no more than 2 for confirmatory work
- Adaptive connections disabled
- `max_subprocesses = 1`
- No sandbox provider
- No Docker
- No local model server
- No GPU workload
- No background control server kept alive after evaluation
- No automatically launched log viewer

Dataset generation and scoring must be single-process and bounded. Any optional analysis capable of parallel execution defaults to one worker.

### 14.3 Run ownership

At startup, create a run lock containing the harness PID, start time, run ID, and exact output directory. The harness maintains a registry of child PIDs it creates. Cleanup may act only on registered children whose parentage and creation time still match the run. Never kill processes by broad name, port, wildcard, or directory enumeration.

### 14.4 Shutdown and cleanup

On success, exception, timeout, or first Ctrl+C:

1. Stop scheduling new requests.
2. Await or cancel current network work within a bounded grace period.
3. Flush Inspect logs, JSONL, and SQLite transactions.
4. Close file and database handles.
5. Ask registered child processes to exit.
6. After a bounded grace period, terminate only surviving registered children.
7. Remove the run lock and run-owned temporary directory.
8. Verify that no registered child remains.
9. Write `cleanup-report.json` with every resource created, closed, removed, or left intentionally.

A second Ctrl+C may force immediate termination but must still avoid broad process killing. On the next start, a stale-lock audit reports recoverable logs and any matching run-owned child before taking action.

### 14.5 Persistent artifacts versus temporary artifacts

Keep:

- Frozen configuration.
- Dataset and hashes.
- Prompts and packet audits.
- Model responses and provider metadata.
- Inspect evaluation logs.
- SQLite run database.
- Scoring and analysis outputs.
- Cleanup report.

Remove after successful packaging:

- Temporary token-count files.
- Partial download fragments.
- Run-owned caches that are reproducible from frozen inputs.
- Empty temporary directories.
- PID and lock files.

---

## 15. Run identity and reproducibility

Every run and report must include:

- `run_id`
- Experiment codename and specification version
- Harness commit hash
- Dataset manifest hash
- Scenario seed
- Arm name
- Model family and canonical model slug
- Provider
- Harness name and version
- Agent/researcher name responsible for the run
- Machine OS and Python version
- Start and end timestamps in UTC
- Prompt and packet hashes
- Generation parameters
- Token, latency, retry, and cost totals
- Exit status and cleanup status

Run IDs must be collision-resistant and may not depend only on a human-readable model name.

---

## 16. Execution gates

### Gate 0 — Static verification

- Unit tests for generator invariants.
- Property tests for obligation state transitions.
- Golden tests for cancellations, reschedules, supersessions, dependencies, and scope isolation.
- Packet-budget tests.
- Gold-leakage canaries.
- Exact scorer fixtures.
- Restart reconstruction tests.
- Cleanup tests using harmless short-lived child processes created by the test itself.

No model calls.

### Gate 1 — Engineering smoke test

- Two calibration scenarios.
- All arms, including no-memory and oracle.
- One inexpensive capable model or mocked provider.
- Verify logs, scoring, provider metadata, cost accounting, interruption recovery, and cleanup.
- Discard results from scientific analysis.

### Gate 2 — Pilot

- Four held-out pilot scenarios per arm.
- One pinned high-capability model and provider.
- Estimate paired variance, tokens, cost, latency, and malformed-output rate.
- Freeze confirmatory sample size and cap.
- Pilot outcomes cannot be used as confirmatory evidence.

### Gate 3 — Confirmatory kernel experiment

- Frozen scenario seeds and sample size.
- Arms A–E.
- One pinned high-capability model/provider block.
- Preregistered primary and secondary analysis.
- No code, prompt, metric, or routing changes after the first confirmatory response.

### Gate 4 — Model-family normalization

Only if Gate 3 is not killed, repeat the highest-information subset on a second model family. This tests whether the effect belongs to the memory contract or to one backbone's preferred scaffold.

### Gate 5 — End-to-end write path

Only if typed projection wins under identical structured admission, replace deterministic event admission with natural-language extraction. Score write precision, write recall, correction linkage, and downstream action separately.

### Gate 6 — External validity

Only after the kernel and write path survive:

- Adapter for PM-Bench prospective-memory protocol.
- Adapter for Mem2ActBench memory-grounded tool use.
- Adapter for LongMemEval-V2 experienced-colleague recall.
- Multi-conductor sharing and brain-slotting experiment.

---

## 17. Failure classification

Every failed decision receives one primary failure label and optional secondary labels:

- `write_missing`
- `write_incorrect`
- `update_not_applied`
- `stale_memory_selected`
- `wrong_scope_selected`
- `dependency_missing`
- `retrieval_miss`
- `packet_budget_failure`
- `reasoning_failure_with_sufficient_packet`
- `monitoring_failure`
- `schema_failure`
- `provider_failure`
- `provider_transformation`
- `harness_failure`
- `gold_leakage`

The oracle-minimal arm distinguishes reasoning failure from memory selection failure. Packet audit logs distinguish missing storage from missing retrieval or structural closure.

---

## 18. What a positive result would and would not mean

A positive result would justify implementing the bounded typed obligation and current-state kernel as a serious Munin prototype. It would support the claim that versioned structure, validity, scope, provenance, and deterministic materialization offer measurable value beyond a good ledger or simple retrieval under bounded context and cold restart.

It would not prove that Moonwalker has solved general memory, episodic memory, personality, emotion, procedural learning, shared cognition, or brain slotting. It would not prove that the write path works on arbitrary conversation. It would not prove robustness across every model family. Those remain separate experiments.

## 19. What a negative result would mean

If the ledger matches the typed projection within the kill margin, Moonwalker should not build the current Munin kernel merely because it is architecturally elegant. The next move would be to identify whether the product needs a durable ledger rather than a more general memory substrate, or whether the experiment omitted an essential open-world discovery requirement.

If the oracle performs poorly, the bottleneck is the decision model or task interface, not memory. If the architecture-isolation stage passes but the write-path stage fails, engineering should focus on admission and correction extraction rather than retrieval. If lexical retrieval matches typed projection except on correction and scope cases, typed structure may be retained only for those narrow planes.

---

## 20. Pre-run approval checklist

Before the first paid inference call, the owner reviews and approves:

- Final specification version.
- Harness implementation review.
- Frozen model/provider manifest.
- Dedicated key and hard cost cap.
- Dry-run token and cost estimate.
- Scenario and invariant summary.
- Confirmatory seed commitment hashes.
- Analysis script and thresholds.
- Process limits and cleanup test result.
- Exact output directory.

The command that begins paid inference must require an explicit confirmation flag referencing the approved run manifest. Absence of approval fails closed.

---

## 21. Prior-art and operational references

1. Genglin Liu and Saadia Gabriel, **PM-Bench: Evaluating Prospective Memory in LLM Agents** (2026): https://arxiv.org/html/2607.12385v1
2. PM-Bench public repository and released scenario/run description: https://github.com/genglinliu/PMBench
3. Xiangchen Cheng et al., **AgenticSTS: A Bounded-Memory Testbed for Long-Horizon LLM Agents** (2026): https://arxiv.org/abs/2607.02255
4. AgenticSTS public repository and bounded-memory contract: https://github.com/AlayaLab/AgenticSTS
5. Di Wu et al., **LongMemEval-V2: Evaluating Long-Term Agent Memory Toward Experienced Colleagues** (2026): https://github.com/xiaowu0162/LongMemEval-V2
6. Yifeng Shen et al., **Mem2ActBench: A Benchmark for Evaluating Long-Term Memory Utilization in Task-Oriented Autonomous Agents** (2026): https://aclanthology.org/2026.acl-long.370/
7. UK AI Security Institute, **Inspect AI documentation**: https://inspect.aisi.org.uk/
8. Inspect AI parallelism and resource controls: https://inspect.aisi.org.uk/parallelism.html
9. Inspect AI evaluation logs and reproducible run configuration: https://inspect.aisi.org.uk/eval-logs.html
10. OpenRouter provider routing controls: https://openrouter.ai/docs/guides/routing/provider-selection
11. OpenRouter router metadata: https://openrouter.ai/docs/guides/features/router-metadata
12. OpenRouter message transforms and context compression: https://openrouter.ai/docs/guides/features/message-transforms
13. OpenRouter guardrails and API-key budgets: https://openrouter.ai/docs/guides/features/guardrails/overview

---

## 22. Owner-review decision

After reviewing this specification, choose one outcome:

- **Approve for implementation planning:** write a separate step-by-step implementation plan; do not run inference yet.
- **Revise:** change the experiment before implementation.
- **Reject:** do not build the harness.

Approval of this document authorizes implementation planning only. Building the harness and running paid inference remain separate gates.
