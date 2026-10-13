# MBCX-01 — Bounded Continuity Experiment Design r2

**Status:** council-folded design; fresh council review required before implementation planning

**Supersedes:** `MBCX-01-EXPERIMENT-DESIGN-r1.md`

**Scientific question:** whether a typed continuity package earns its complexity over the strongest cheap deterministic flat-memory package under a genuinely bounded context condition

## 1. Decision

Build a disposable, direct-runner scientific instrument. Do not build production Munin, a generalized agent framework, or a security subsystem.

Stage A compares two deterministic memory packages under the same public events, model, exact provider endpoint, prompt, memory budget, output schema, run order, and scoring. The flat package receives every cheap deterministic selection advantage available from its own fields. The typed package may earn value only from information and relationships the flat package does not persist or cannot reconstruct.

No paid pilot is authorized by this document. r2 must first survive an experiment-specific council pass and all no-model gates.

## 2. What r2 is designed to decide

The owner-facing question is:

> Under a fixed context budget, does a deterministic typed continuity package improve prospective action and current-state continuity enough to justify building it instead of a strong flat current-state/obligation ledger?

The primary result is an architecture-package comparison, not a claim that a latent storage representation alone caused every observed difference. A frozen mechanism diagnostic separates value retained in the typed store from value created by exposing typed structure in the decision packet.

The experiment must be capable of returning any of these useful answers:

1. **Build the strong flat package.** Typed continuity does not clear the minimum worthwhile effect.
2. **Build typed persistence but expose a simple flat view.** Typed history repairs corrections/retractions, while typed packet structure adds little.
3. **Build typed persistence and the native typed packet.** Both retained structure and typed exposure contribute.
4. **The experiment is underfunded or invalid.** Do not convert an inconclusive or contaminated run into an architecture verdict.

## 3. Scope override

This is an internal experiment. The only in-scope concern is whether the instrument can return a scientifically false, biased, unrepeatable, or unaffordable answer.

The following are non-load-bearing unless a reviewer demonstrates a direct path to an incorrect experiment result:

- Licensing, redistribution, clean-room implementation, or commercialization posture.
- Production cryptography, FIPS/CNSA, seal chains, multi-tenant authorization, or hostile prompt injection.
- General process registries, daemons, stale-PID discovery, fleet cleanup, or crash durability.
- PR ceremony, delivery workflow, production deployment, or support policy.
- Provider-family generality, cross-model generality, or worldwide production scaling.

Framework caches, retry behavior, hidden message state, request transforms, response caches, and endpoint routing remain in scope because they can change an arm's input or stochastic draw.

## 4. Causal program

### 4.1 Stage A — deterministic package comparison

Both primary arms receive byte-identical admitted public events. Both stores are maintained by deterministic code. Both decision calls are stateless provider requests. Neither decision model writes memory.

The primary treatment is:

- **F:** strongest cheap deterministic flat store plus flat-compatible bounded materializer.
- **TN:** deterministic typed continuity store plus its native bounded materializer.

This primary contrast is honestly reported as `typed native package - strong flat package`.

### 4.2 Stage A mechanism diagnostic

On a frozen, stratified 25% subset of confirmatory scenarios, run:

- **TF:** the typed persisted store rendered through the exact flat packet schema and flat-compatible materializer used by F.

The diagnostic contrasts are:

- `TF - F`: value of typed persistence/currentness reconstruction while the visible packet format is held flat.
- `TN - TF`: value of exposing typed relationships and native typed closure while the persisted typed store is held fixed.

These are mechanism diagnostics. They do not replace or multiply the single primary TN-versus-F decision rule.

### 4.3 Stage B — ecological writer/controller experiment

Stage B is a separate preregistration and is authorized only if Stage A is not killed. It may cross representation with deterministic versus model-written maintenance and may add retrieval or provider-native compaction. Stage A never proves that natural-language writing, learned memory management, or production Munin works.

## 5. Memory packages

### 5.1 Arm F — strong deterministic flat package

The flat reducer persists only current, scoped rows:

- Latest public value for each `(scope_id, state_key)`.
- One public `source_event_id` for each current row.
- Open obligations with `obligation_id`, `action_id`, scope, public trigger, current status, direct prerequisite IDs, and `next_check_at` when mechanically derivable.
- Explicit completion, cancellation, reschedule, and removal from the active set.
- Terminal/tombstone IDs sufficient to suppress duplicate or closed execution.
- A deterministic `unknown` state when a public retraction invalidates the current value but the overwritten value is no longer available.

F does not persist version chains, historical evidence sets, conflict objects, supersession graphs, validity intervals, typed multi-hop dependency traversal, or provenance closure.

### 5.2 Arm TN — deterministic typed-native package

The typed reducer persists immutable admitted public evidence and materializes:

- Versioned scoped assertions with explicit currentness and validity.
- Obligations with typed triggers and lifecycle state.
- Dependency edges and required typed closure.
- Completion, cancellation, reschedule, correction, retraction, conflict, and supersession relationships.
- Public evidence references sufficient to explain currentness.
- Restoration of a prior valid value or obligation when a later correction/cancellation is retracted.

TN may not receive private gold, more resolved public events, extra model calls, a larger token budget, or a different retry policy.

### 5.3 Arm TF — typed store, flat view

TF uses TN's persisted bytes but collapses them into the exact F packet schema before the decision call. It may use typed history to determine the correct current value, status, or direct prerequisite, but it may not expose versions, conflicts, provenance closure, validity intervals, supersession graphs, or multi-hop typed closure to the model.

### 5.4 Shared flat-compatible materializer

F and TF use the same implementation and rules:

1. Restrict to the active scope plus explicitly cross-scope obligations.
2. Suppress terminal/tombstoned obligations.
3. Select due and near-due obligations from public trigger fields and the current public time.
4. Include direct prerequisites explicitly stored on a selected obligation.
5. Include current state rows referenced by selected triggers or direct prerequisites.
6. Stable-sort by due tier, public trigger time, scope, and stable ID.
7. Serialize through the same compact schema and exact tokenizer counter.
8. If the mandatory selected set cannot fit, return `budget_failure`; never silently truncate a mandatory item.

TN performs the same first five cheap operations, then may add only typed-native currentness, conflict preservation, multi-hop required closure, validity/supersession relationships, and minimum public evidence references. Any ordinary cheap operation available from F's own fields must be exercised by F before TN is allowed to claim an advantage.

### 5.5 Treatment parity

Every primary cell receives identical scenario bytes, current observation, available public actions, channel-query affordances, system/task instructions, exact model/provider/parameters, timeout policy, memory-payload cap, output cap, and run-order block. The only prompt difference is a short arm-neutral declaration of the supplied packet schema. The decision model receives no callable tool; a requested channel query becomes a mechanically processed public action at the next world step.

### 5.6 Primary decision output

The primary model response is genuinely action-only:

```json
{
  "ongoing_choice": "string-or-null",
  "action_ids": ["public-action-id"],
  "channel_queries": ["public-channel-id"]
}
```

`provenance_ids`, explanatory state claims, rewritten ledgers, chain-of-thought, and memory-maintenance output are not required. Invalid JSON or invalid IDs are primary failures; a repair call may be run only as a separately labeled diagnostic and never replaces the first response in primary scoring.

### 5.7 Diagnostic controls

On frozen costed subsets, run:

- **No persistent memory:** current observation and available actions only.
- **Budgeted chronological history:** oldest-complete-event truncation under the same payload cap.
- **Oracle-minimal and oracle-all-relevant:** defined in §14 and excluded from every primary estimate.

Lexical/BM25 retrieval, vector retrieval, model-written ledgers, learned memory controllers, provider-native compaction, and archive search remain deferred.

## 6. Public evidence and architecture neutrality

### 6.1 Primitive public event

The world emits one public object containing only observed primitives:

- `event_id`
- `observed_at`
- `actor_id`
- `scope_id`
- `channel_id`
- `operation`
- `subject_id`
- optional `object_literal`
- optional `target_event_id`
- optional public trigger specification
- public action/task/channel handles introduced at that step
- `natural_language_text`

Allowed operations are frozen before generator implementation: assertion, open obligation, completion, cancellation, reschedule, correction, retraction, dependency link/unlink, and channel cue.

The public object may identify what was observed or which prior public event was referenced. It may not contain `is_current`, `is_due`, `active`, `gold`, `priority_rank`, resolved dependency closure, correct action set, private status, or a preassembled packet.

Both reducers receive the exact same serialized bytes. A retraction refers to the retracted public event and does not repeat the previous valid value; recovering that value is therefore a legitimate test of retained structure.

### 6.2 Private gold

Private gold contains the correct due-action set, canonical state/lifecycle, hidden channel content, scoring strata, and oracle selection metadata. It is physically separate and accessible only to generator validation, scoring, and oracle construction.

Private gold never enters a primary store, materializer, prompt, request, cache key, transport record, or provider log.

### 6.3 Architecture-privilege gate

Before any paid call, the generator must pass:

- Private-field byte canaries.
- Byte-identical public input tests for F, TF, and TN.
- A field-denylist proving no derived currentness, due-ness, closure, or answer labels exist in public bytes.
- A replay test proving public events are sufficient to compute gold only when the full public history is available.
- A current-observation-only solver failure for every memory-required item.
- Independently hand-authored challenges not produced from TN's implementation schema.
- A materialization-parity differential proving F exercises every cheap operation available from its own fields.
- A constructed counterexample showing that the flat reducer cannot recover a retracted overwritten value without retaining forbidden history, while TF/TN can.

## 7. Frozen scenario envelope

Scenarios model a domain-neutral control room coordinating people, scopes, projects, and monitored channels. Specialist domain knowledge must never decide the task.

Every confirmatory scenario satisfies all of these bounds:

| Dimension | Frozen range or maximum |
|---|---:|
| Decision steps | 48–64 |
| Scopes | 3–4 |
| Prospective obligations created | 36–52 |
| Simultaneously open obligations | 12–28 |
| Current flat state rows | 18–40 |
| Explicit updates | 10–16 |
| Cross-scope obligations | 6–10 |
| Dependency width | maximum 3 |
| Dependency depth | maximum 3 |
| Required live closure | maximum 12 nodes |
| Hidden-channel/monitoring cues | 6–10 |
| Available actions per decision | 4–12 |
| Gold due actions per decision | maximum 6 |
| Public event fan-out | maximum 3 subjects/relations |
| Natural-language public text | 12–80 exact-tokenizer tokens |
| Identifier or scalar field | maximum 32 exact-tokenizer tokens |

Each scenario also contains:

- At least 30 gold-positive high-stress `(decision_step, action_id)` pairs.
- Between 20 and 36 explicit lure action exposures, including wrong-scope and completed/canceled/superseded lures.
- At least one cancellation, completion, reschedule, supersession, correction, retraction-of-correction, and retraction-of-cancellation.
- At least two nested or chained update cases.
- At least six dependency-triggered obligations.
- Naturalistic distractors between creation, update, and execution.
- Reconstruction boundaries near 25%, 50%, and 75%.

Every declared update mechanism appears at least once in every confirmatory scenario. The generator reports realized cardinalities and rejects any seed outside the envelope.

Development, smoke, external-pilot, confirmatory, and reserve seeds are disjoint and frozen before their respective first model call. Confirmatory content is not manually inspected beyond invariant summaries.

## 8. Binding budget contract

### 8.1 Memory budget selection

The candidate memory-payload budgets are, in order:

`1,536`, `2,048`, `3,072`, and `4,096` exact-tokenizer tokens.

After the exact model, tokenizer/counter, request wrapper, schemas, and scenario generator are frozen—but before any paid inference—Gate 1 selects the smallest candidate satisfying all of the following on maximum-load fixtures and frozen no-model pressure seeds:

1. F, TF, and TN serialize every non-overflow maximum-load fixture and every frozen pressure-seed packet without `budget_failure`; separately designated overflow fixtures must fail explicitly and symmetrically.
2. At each pressure checkpoint, the full unfiltered flat-current serialization exceeds the candidate by at least `1.25×` and chronological public history exceeds it by at least `1.5×` in every frozen pressure scenario.
3. On the pressure stratum, every primary native packet is between 40% and 95% utilization, and at least half of high-stress decisions place at least one primary packet between 60% and 95% utilization.
4. Neither primary packet exceeds the candidate without an explicit `budget_failure`.
5. No local or provider middle-out compression, silent truncation, or summarization occurs.

If no candidate satisfies the contract, the world/schema must be redesigned and re-counseled before inference. The budget is never chosen from model performance.

At least half of confirmatory scenarios belong to the pressure stratum; the remainder are moderate-load cases. Primary results report both strata and the pooled preregistered mean.

### 8.2 Output and information density

The initial output cap is 512 tokens and must pass a maximum of six action IDs, twelve channel queries, and maximum-length legal IDs with at least 20% tokenizer headroom.

Every request logs:

- Full input tokens and memory-payload tokens.
- Output, cache-read, and cache-write tokens.
- Payload utilization.
- Records and relationships exposed.
- Required-closure cardinality.
- `budget_failure`, truncation, or serialization failure.

Equal token caps do not imply equal information density. Density is reported as a mechanism/cost result, not hidden.

## 9. Process-cold reconstruction

Every decision call is a new stateless provider request. No prior chat transcript is supplied.

At each reconstruction boundary:

1. Persist and close the arm artifact.
2. End the decision process.
3. Start one fresh interpreter child through a tiny synchronous supervisor.
4. Give the child only the designated arm artifact, the current public observation, and a capability-limited cursor.
5. Reconstruct through the same adapter entry point used at ordinary start.
6. Record the reconstructed packet and state audit.
7. Exit the child and wait for it.

The cursor contains only `scenario_id`, `next_step_index`, and a public-prefix hash commitment. It cannot open or resolve the scenario event log and carries no replayable history or state rows.

No-model negative witnesses are mandatory:

- Withhold or corrupt the arm artifact while keeping cursor/current observation intact: reconstruction must fail or mechanically disagree.
- Keep the arm artifact while removing unrelated ambient files and non-required environment variables: reconstruction must still succeed.
- Change the public-prefix hash: reconstruction must fail closed.

This measures process-cold reconstruction from the arm artifact. It does not claim host-crash, power-loss, or distributed durability.

## 10. Runner and storage

Use a thin direct Python runner. Stage A does not use Inspect, Harbor, an agent framework, a plugin architecture, or a generalized evaluation substrate.

The runner owns only:

- Deterministic world playback.
- Pure reducers and materializers.
- One stateless HTTP request builder.
- One mechanical scorer/analysis package.
- JSONL audit logs and arm artifacts.
- One exact reconstruction child at a time.

Plain files/JSONL are preferred. SQLite is allowed only if it is demonstrably simpler for transactional test fixtures; no database abstraction is an objective.

The runner executes one model request at a time. It closes files, waits for its one child, removes only run-owned disposable files, and never scans or kills unrelated processes or ports.

## 11. Model and transport condition

Stage A intentionally freezes one capable model on one exact provider endpoint. The run manifest contains:

- Canonical non-rolling model identifier.
- Exact provider endpoint/slug, not merely a provider family.
- Reasoning effort, temperature, supported seed, output limit, and tool schema.
- Request wrapper and API version.
- Context limit and supported parameters.
- Cache posture.
- Timeout and retry policy.
- Observable price used for the cost envelope.
- Exact tokenizer or provider-compatible counter and version.

The direct runner may call OpenRouter only if no-paid/mocked and smoke conformance proves:

- Exact endpoint selection and the effective intersection of account-wide and request-level provider allowlists.
- Fallbacks disabled.
- `require_parameters` enabled.
- Message transforms/context compression disabled.
- Response caching disabled.
- Prompt-cache behavior either disabled or identically logged and arm-neutral.
- Returned model/provider/endpoint metadata present and equal to the frozen condition.
- A cache hit or missing route attestation invalidates the cell.

If OpenRouter cannot prove the exact condition, use direct provider transport. Provider variance is removed, not estimated.

## 12. Order, retries, and cell identity

- Pair F and TN on the same scenario.
- Randomize and counterbalance F/TN order within scenario.
- Interleave scenarios and freeze the complete schedule.
- Run TF only on the frozen stratified 25% diagnostic subset.
- Use one in-flight request.
- Never selectively reroll a valid model response.
- Retry only when the client can prove the request was not accepted or processed.
- A post-send ambiguous connection failure invalidates the entire F/TN pair.
- Invalid pairs are replaced by the next seed in a frozen reserve list; neither arm's result from the invalid pair is retained in primary analysis.
- A retry begins from the clean pre-attempt artifact snapshot and keeps the same attempt lineage.
- Malformed primary output is scored as failure; repair output is diagnostic only.
- Any hidden conversation, dirty resume, local response cache, provider response cache, transform, fallback, or endpoint mismatch invalidates the pair.

The manifest freezes reserve seeds and the maximum invalid-pair rate. If more than 5% of attempted confirmatory pairs are invalid, stop and return to design/transport review rather than silently consuming more reserves.

## 13. Outcomes and exact scorer

### 13.1 Primary estimand

For each scenario, define the high-stress universe as all eligible `(decision_step, public_action_id)` pairs in the frozen stress strata.

Across that universe:

- `TP`: predicted action is gold due.
- `FP`: predicted action is not gold due, including explicit lures.
- `FN`: gold-due action is not predicted.
- True negatives are not counted.

If `TP = FP = FN = 0`, the scenario is invalid because the generator failed the minimum-positive contract. There is no empty-set scoring convention left to choose after results exist.

`high_stress_set_f1 = 2TP / (2TP + FP + FN)`.

The scenario-level paired delta is:

`delta_i = F1_i(TN) - F1_i(F)`.

The primary estimand is the arithmetic mean of `delta_i` over valid independent confirmatory scenarios. Decisions inside one trajectory are not independent samples.

With at least 30 gold-positive pairs, one corrected action cannot by itself move a scenario from zero performance to `+0.08`; scorer fixtures calculate and publish the exact one-action quantum at all declared boundary cases.

### 13.2 Secondary and mechanism outcomes

- Overall due-action micro-F1.
- Stale/canceled/superseded/wrong-scope false-action rate.
- Cross-scope, update-sensitive, dependency, retraction, and hidden-channel hit rates.
- Exact artifact-state reconstruction.
- Duplicate execution.
- Payload utilization, density, latency, retries, invalid pairs, and cost per correct action.
- Oracle gaps.
- On the diagnostic subset: `TF-F` and `TN-TF` paired deltas with intervals reported descriptively.

All task outcomes are mechanical. No LLM judge may override the scorer.

## 14. Oracle diagnostics

Oracle arms are non-deployable diagnostics and never enter the primary estimate.

- **Oracle-minimal:** includes the smallest set of public facts, obligation records, and public relationships needed to reason about the current decision. It may not include a due/not-due label, the target action set, a gold status, or a precomputed answer.
- **Oracle-all-relevant:** includes all public gold-relevant facts, conflicts, redundancy, and obligations, including information that may make reasoning harder.

Every oracle fixture must pass answer separation: a mechanical extractor given the oracle memory alone, without the current time/observation and available-action list, cannot recover the gold action set. Both oracle policies must reproduce the correct result when combined with a deterministic reference reasoner before any model call.

Poor oracle performance identifies a decision-model, action-interface, or scenario ceiling; it does not prove a memory representation failure.

## 15. Pilot, sample size, and decision rule

### 15.1 External engineering pilot

After every no-model gate passes, run 12 held-out paired F/TN scenarios. Pilot scenarios remain excluded from confirmation because this is a new instrument and pilot execution may expose implementation defects.

The pilot estimates variance, cost, latency, schema failures, invalid-pair rate, and realized budget pressure. If any prompt, generator, reducer, materializer, scorer, transport rule, or outcome changes after pilot outcomes are visible, create a new design revision and use a new pilot set.

### 15.2 Executable variance bound

For pilot paired deltas with sample SD `s` and `m = 12`, compute the one-sided 95% upper variance bound:

`s_upper = s * sqrt((m - 1) / chi2_ppf(0.05, m - 1))`.

Use `s_design = max(0.20, s_upper)`. The floor prevents an all-zero or tail-missing pilot from claiming negligible variance. The pilot may increase, never remove, the preregistered rare-tail/lumpy distribution families.

### 15.3 Primary interval

The primary 95% confidence interval is the two-sided Student-t interval over independent scenario deltas:

`mean(delta) ± t_ppf(0.975, n - 1) * sd(delta) / sqrt(n)`.

This exact algorithm is frozen and easy to audit. A 50,000-resample scenario-level BCa bootstrap interval and paired-permutation test are sensitivity analyses. If the primary and BCa intervals cross the `+0.03` decision boundary in opposite directions, the result is inconclusive rather than selectively choosing the favorable interval.

Every other confidence endpoint used by a win or kill gate uses the same two-sided 95% scenario-level Student-t construction on the relevant paired scenario difference. Descriptive metrics may use additional intervals but cannot replace a frozen gate endpoint.

### 15.4 Full-rule operating-characteristic calibration

`+0.03` is the minimum worthwhile boundary. `+0.08` is the planning alternative used for power; it is not a second observed-mean cutoff.

Before confirmation, simulate the complete frozen decision rule—not merely a test against zero—over bounded scenario deltas in `[-1, 1]`. The envelope includes:

- Smooth truncated distributions.
- Scorer-quantized/lattice distributions.
- Symmetric and asymmetric two-point distributions.
- Mixtures with 5% and 10% total rare-tail mass at or near the bounds.

Each family is calibrated at the pilot `s_design` and at SD sensitivity values `0.10`, `0.20`, `0.30`, and `0.40` that are not below `s_design`. Use at least 100,000 simulated experiments per family/candidate `n` with a frozen RNG seed.

Choose the smallest `n`, in increments of 12 and never below 48, satisfying all of these for every retained family at the relevant mean:

1. At true mean `+0.08`, probability that the lower primary 95% endpoint exceeds `+0.03` is at least 0.80.
2. At true mean `+0.03`, false-win probability is at most 0.05.
3. At true mean `0`, probability that the upper primary 95% endpoint is below `+0.03` is at least 0.80.
4. At true mean `+0.08`, false-kill probability is at most 0.05.
5. Empirical coverage of the primary interval is at least 0.94.

The confirmatory `n` is the maximum required by this calibration and the pilot-SD upper-bound calibration. There is no maximum clamp.

Before the pilot, publish a cost envelope for SD `0.10`, `0.20`, `0.30`, and `0.40`, including two primary calls per step, the 25% TF diagnostic subset, oracle/control subsets, reconstruction calls, and invalid-pair reserve. After pilot, publish the frozen required `n` and exact cap. If unaffordable, report `UNDERFUNDED`; do not run a smaller confirmation and call a null result decisive.

### 15.5 Win

Continue investment in the typed package only if all hold:

1. The lower primary 95% confidence endpoint for `TN-F` exceeds `+0.03`.
2. Overall due-action F1 is not more than 0.02 below F or the best non-oracle diagnostic baseline.
3. The upper confidence endpoint for excess stale/wrong-scope actions is below `+0.02`.
4. Process-cold reconstruction succeeds for at least 95% of required state fields with uncertainty reported.
5. TN remains inside budget without silent loss of mandatory closure.
6. No leakage, hidden history, cache, fallback, transform, retry, endpoint, or generator-privilege violation invalidates the comparison.
7. Primary and BCa intervals do not disagree across the `+0.03` boundary.

The observed mean and its relation to the planning alternative `+0.08` are reported, but an observed `+0.08` cutoff is not added to the rule.

### 15.6 Kill

Prefer the strong flat package and do not build the current rich kernel merely for elegance if any holds:

- The upper primary 95% confidence endpoint is below `+0.03`.
- TN materially increases stale/wrong-scope or duplicate actions.
- Required typed closure repeatedly cannot fit the selected budget under the frozen valid workload.
- A purported advantage disappears in TF/F or TN/TF decomposition in a way showing only an ordinary flat-compatible selector was needed.
- The result depends on contamination, gold leakage, architecture-privileged generation, hidden context, caching, fallback, transforms, or unfair retry.

### 15.7 Inconclusive

Anything between win and kill is inconclusive. Underfunded, invalid, conflicting-interval, excessive-invalid-pair, and oracle-ceiling outcomes are also inconclusive. They may authorize one targeted preregistered repair or replication, never a success claim.

## 16. No-model and no-cost gates

### Gate 0 — world and scorer

- Generator bounds and transition property tests.
- Mandatory update-taxonomy coverage, including both retraction types.
- Gold-taint canaries and current-observation-only failure tests.
- Exact TP/FP/FN, empty-case, aggregation, and one-action-quantum fixtures.
- Hand-authored architecture-independent challenge set.
- Oracle policy and answer-separation fixtures.

### Gate 1 — comparator, packets, and budget

- Byte-identical admitted public events.
- Field-denylist and architecture-neutrality tests.
- F/TF shared-materializer golden and differential tests.
- Constructed retraction case proving the intended representational boundary.
- Candidate-budget selection with the exact tokenizer.
- Maximum-load payload/output tests and explicit overflow paths.
- No arm-specific model call, tool, repair budget, or maintenance output.

### Gate 2 — reconstruction

- F, TF, and TN reconstruction goldens.
- Artifact-withheld/corrupt negative witnesses.
- Ambient-removal positive witness.
- Cursor hash and no-history capability tests.
- Exact-child wait/termination and temporary-file cleanup.

### Gate 3 — transport and identity

- Mock-provider transcript of exact request bytes.
- Endpoint/provider/cache/fallback/transform/parameter assertions.
- Pre-dispatch retry, post-send ambiguity, malformed schema, timeout, and interruption injection.
- Frozen pair invalidation and reserve-seed replay.
- Hidden-message and local-response-cache absence.

### Gate 4 — statistics and cost

- Frozen primary interval and BCa sensitivity fixtures.
- Structural demonstration that the r1 50% threshold bug is gone.
- 100,000-run operating-characteristic simulations over every envelope family.
- Exact pilot SD-upper-bound fixture, including `s = 0`.
- Four-point pre-pilot cost envelope.

### Gate 5 — engineering smoke

- Two non-confirmatory scenarios through F, TF, TN, controls, reconstruction, and scoring.
- Mock provider or explicitly owner-approved inexpensive endpoint.
- Logs, density accounting, cleanup, and invalid-pair handling verified.

Only after all six gates pass and a fresh council closes r2 may the 12-pair paid pilot be proposed to the owner.

## 17. Run artifacts and cleanup

Every run retains only the files required to reproduce and audit the scientific result:

- Frozen manifest, design hash, schedule, and reserve list.
- Scenario config, seeds, public events, and separately protected private gold.
- Reducer/materializer versions and packet audits.
- Observable requests/responses and exact route metadata.
- Arm artifacts and reconstruction audits.
- Raw mechanical scores, analysis code/output, and operating-characteristic simulation.
- Token, record-density, latency, retry, invalid-pair, cache, and cost logs.

Temporary files live under one explicit run directory. The runner closes its own files, waits for or terminates only its one explicit reconstruction child, and removes only run-owned disposable files. It leaves no daemon or watcher.

## 18. Interpretation and non-claims

A positive primary result supports only this sentence:

> Under the frozen model/provider, workload, and token budget, the typed-native continuity package beat the strongest cheap deterministic flat package by more than the minimum worthwhile boundary.

The TF diagnostic may indicate whether value came from retained typed history, native typed packet exposure, or both. It does not turn a package experiment into universal representation proof.

Stage A does not establish superiority over:

- Lexical/BM25 or vector retrieval.
- Model-written memory or learned memory controllers.
- Provider-native compaction or archive search.
- Natural-language admission/maintenance.
- Cross-model/provider conditions.
- Open-world semantic memory, procedural learning, personality, emotion, or multi-agent sharing.
- Production durability, authorization, or hostile-input safety.

If F matches TN within the kill boundary, Moonwalker should prefer F unless a predeclared diagnostic slice identifies a narrow typed mechanism worth a smaller follow-up experiment.

## 19. Prior-art mechanisms to borrow

The implementation plan may borrow mechanisms, not wholesale systems:

- PM-Bench: deterministic prospective-memory worlds, updates, lures, heartbeat/ledger scaffolds, and replay scoring.
- AgenticSTS: fresh-message assembly and bounded named memory layers.
- StateFuse: matched resolver/materializer discipline for representation comparisons.
- LongHorizon-Harness: external-state/fresh-executor separation.
- Mem2ActBench: current-input leakage/solvability checks for memory-grounded action.
- tau2-bench: state/outcome scoring instead of privileging one reference action path.

No reviewed prior art performs this exact F-versus-TN comparison under matched deterministic writing, binding token budget, process-cold reconstruction, exact route controls, and prospective-action scoring. MBCX-01 is therefore not obsolete, but it is narrower than a general-memory experiment.

## 20. Authorization gates

This r2 document authorizes only:

1. Fresh experiment-specific council review.
2. If that review closes with no P0/P1 scientific blocker, a separate implementation plan.

Separate owner approval is required for:

1. Harness implementation.
2. Frozen model/provider/tokenizer choice.
3. The pilot manifest and exact cost cap.
4. Any paid pilot inference.
5. The confirmatory manifest and exact cost cap.
6. Confirmatory execution.
