# MBCX-01 — Bounded Continuity Experiment Design r3

Status: preregistration design; no harness and no paid inference authorized  
Date: 2026-08-12  
Supersedes for future work: `MBCX-01-EXPERIMENT-DESIGN-r2.md`

## 1. Decision

Build the smallest disposable instrument that can answer:

> Under one frozen model/provider, bounded packet budget, deterministic writer, and prospective control-room workload, do typed-native continuity mechanisms improve action selection by more than `+0.03` mean scenario set-F1 over a strong cheap flat replay package when presentation is held to a render-matched native layout?

The primary comparison is **TN minus FM**. TN and FM share the native-shaped presentation; FM uses the flat replay store with typed/deprecation mechanisms neutralized. It is still a mechanism-package comparison, not a claim that storage bytes alone caused every difference.

No paid pilot is authorized by this document. r3 must pass a fresh experiment-specific council and every no-model gate.

## 2. What changed from r2

1. Replaced destructive current-only F with **F+**, an append-only flat public-event journal, deterministic replay/current index, and bounded traversal over public IDs.
2. Made **FM**, the flat replay store under a render-matched native layout, the primary flat arm; F+ and TF complete the 2×2 store/render diagnostic on 25%.
3. Froze mechanism-stratified positive and lure quotas instead of minima alone.
4. Replaced the arbitrary 512-token output cap with exact maximum-serialization derivation.
5. Added a total public-event bound, joint maximum fixtures, and exhaustive overflow classification.
6. Added artifact-swap and information-differential reconstruction witnesses.
7. Removed post-send reserve substitution from the primary estimand and added worst-case missing-pair tipping.
8. Removed the chi-square pilot SD bound. The 12-pair pilot is engineering-only.
9. Froze operating-characteristic family/support rules and simulation-acceptance uncertainty.
10. Demoted BCa/permutation to nonbinding sensitivities.
11. Deleted the paid chronological-history diagnostic and conditional SQLite path.

## 3. Scope and non-goals

Stage A includes only:

- Deterministic admission and memory maintenance.
- Stateless action-selection calls.
- A frozen bounded packet.
- Process-cold reconstruction from each arm artifact.
- Mechanical scoring.

Stage A excludes:

- Model-written memory, learned retrieval, learned controllers, archive search, and provider compaction.
- Agent frameworks, databases, services, plugins, and production orchestration.
- Security architecture, hostile actors, multitenancy, durability, authorization, and deployment.
- Cross-model/provider generalization.
- Personality, emotion, open-world semantic memory, procedural learning, or multi-agent sharing.

Those are separate experiments. They must not be smuggled into this one.

## 4. Causal program

### 4.1 Primary arms

Every arm receives byte-identical primitive public events. Deterministic code maintains the stores. Decision calls are stateless and cannot write memory.

- **FM — flat replay, matched native render:** the F+ persisted store and deterministic flat replay/traversal mechanisms rendered through the exact TN packet layout, with typed/deprecation mechanisms disabled or neutralized and only F+-derivable content populated.
- **TN — typed-native package:** immutable public evidence plus typed lifecycle, currentness, conflict, supersession, retraction, validity, and dependency relations with native bounded projection.

FM must not invent typed facts. Empty/neutral typed fields remain visibly present so layout is held constant while mechanism differs.

The single primary estimand is `mean(F1_TN - F1_FM)`.

### 4.2 Frozen 25% mechanism/render diagnostic

The confirmatory schedule is built in blocks of 12 scenarios. Exactly three scenarios per block enter the diagnostic subset. Allocation is stratified so every source-generator, pressure, update, dependency, cross-scope, and hidden-channel class is represented as evenly as integer counts allow.

- **F+ — flat replay, flat render:** the same persisted store and replay/traversal mechanisms as FM, rendered through the compact flat packet.
- **TF — typed store, flat render:** TN persistence rendered through the exact F+ packet schema and flat-compatible materializer.

Descriptive contrasts:

- `TF - F+`: typed persistence residual with flat render held fixed.
- `FM - F+`: native-layout/presentation effect with flat persistence held fixed.
- `TN - TF`: native typed exposure plus render effect with typed persistence held fixed.
- `TN - FM`: typed mechanism residual under matched native presentation; this is the primary contrast.
- Difference-in-differences: `(TN - TF) - (FM - F+)`.

These do not multiply the primary hypothesis. They receive intervals and a preregistered tipping interpretation, not independent build gates.

### 4.3 Current-only and status diagnostics

- **F0 current-only overwrite** is an unpaid deterministic ablation. It proves which public traces require retained history but is never the primary opponent.
- On the diagnostic subset, one batched, separately prompted status/abstention call per arm asks about named public `(scope_id, state_key or obligation_id)` coordinates. Responses are mechanically scored as `in_force`, `superseded_or_closed`, `unresolved`, or `absent`, with optional public evidence IDs. This probe is secondary and cannot create a primary win.

## 5. Memory packages

### 5.1 F+ persisted artifact used by F+ and FM

F+ persists only representation-neutral public material:

- An append-only ordered list of the exact admitted primitive event objects.
- A deterministic current flat index keyed by `(scope_id, state_key)`.
- Open-obligation rows with `obligation_id`, `action_id`, scope, public trigger, current status, direct prerequisite IDs, and mechanically derived `next_check_at`.
- Terminal/tombstone IDs.
- An untyped adjacency index built only from public direct-ID fields.

F+ may replay the journal and traverse adjacency to the frozen depth, width, and closure cap. It may not persist typed version objects, typed edge kinds beyond the primitive public operation, validity intervals, conflict objects, provenance closure, a supersession graph, due labels, or private gold.

### 5.2 TN persisted artifact

TN persists:

- Immutable admitted public evidence.
- Versioned scoped assertions with explicit currentness and validity.
- Obligations with typed triggers and lifecycle state.
- Typed dependency, completion, cancellation, reschedule, correction, retraction, conflict, and supersession relations.
- Public evidence references sufficient to explain currentness.

TN may not receive additional public events, private gold, extra model calls, a larger packet, a different wrapper, or a different retry policy.

### 5.3 FM render contract

FM uses the byte-exact TN outer schema, object order, field names, grouping, and neutral field positions. It may populate only facts derivable by F+ replay and bounded public-ID traversal. Typed relations, conflict objects, validity intervals, provenance closure, and supersession structure are represented by frozen neutral/empty values rather than inferred. Gate 1 proves that FM and TN differ in mechanism-bearing content, not typography, grouping, instruction wording, or schema declaration length.

### 5.3 Shared semantic contract

An implementation-independent transition table defines the effective result of every legal primitive sequence. A separately implemented reference interpreter produces canonical current state and gold. Neither F+ nor TN imports that interpreter in paid execution.

Before inference, both reducers must agree with the reference interpreter on:

- Exhaustive small-state sequences through length six.
- Hand-authored nested correction/retraction and cancellation/retraction traces.
- Link/unlink and dependency activation traces.
- Two structurally different deterministic generators.
- Random property-based traces within the frozen grammar.

Any disagreement is a generator/reducer defect, not a model result.

## 6. Primitive public evidence

Each event contains only:

- `event_id`, `observed_at`, `actor_id`, `scope_id`, and `channel_id`.
- `operation`, `subject_id`, optional `object_literal`, and optional `target_event_id`.
- Optional public trigger specification.
- Direct public dependency IDs introduced or removed at that step.
- Public action/task/channel handles introduced at that step.
- `natural_language_text`.

Allowed operations are frozen before generator implementation:

`assert`, `open_obligation`, `complete`, `cancel`, `reschedule`, `correct`, `retract`, `link_dependency`, `unlink_dependency`, and `channel_cue`.

Public bytes may name what happened and the prior public event targeted. They may not include derived `is_current`, `is_due`, `active`, `gold`, priority rank, resolved closure, canonical status, or a preassembled memory packet.

Private gold is physically separate and accessible only to generator validation, mechanical scoring, and oracle construction.

## 7. Materialization parity

F+, TF, FM, and TN must implement the following ordinary cheap operations before TN may claim typed-native value:

1. Restrict to active scope plus explicitly cross-scope obligations.
2. Suppress terminal/tombstoned obligations.
3. Select due and near-due obligations from public trigger fields and public time.
4. Select an open obligation when all direct prerequisites have become terminal/satisfied, including the reverse prerequisite-to-dependent scan.
5. Traverse direct public prerequisite IDs with breadth-first search capped at depth `3`, width `3`, and live closure `12`.
6. Include current state rows referenced by selected triggers or prerequisites.
7. Stable-sort by due tier, public trigger time, scope, and stable ID.
8. Serialize through the frozen arm schema and exact tokenizer counter.

The Gate-1 parity oracle compares each arm’s selected semantic IDs—not its layout—to the independent reference selector at every fixture checkpoint. A false F+ omission or TN addition fails the gate.

TN may additionally expose typed currentness, unresolved conflicts, supersession/validity relations, and minimum public evidence references. Those are the treatment.

## 8. Frozen workload envelope

Scenarios describe a domain-neutral control room coordinating people, scopes, projects, and monitored channels. Specialist domain knowledge never decides an action.

| Dimension | Frozen range or maximum |
|---|---:|
| Decision steps | 48–64 |
| Primitive public events | maximum 128 |
| Scopes | 3–4 |
| Obligations created | 36–52 |
| Simultaneously open obligations | 12–28 |
| Current flat state rows | 18–40 |
| Explicit updates | 10–16 |
| Cross-scope obligations | 6–10 |
| Dependency width/depth | maximum 3 / 3 |
| Required live closure | maximum 12 nodes |
| Hidden-channel cues | 6–10 |
| Available actions per decision | 4–12 |
| Gold due actions per decision | maximum 6 |
| Public fan-out | maximum 3 subjects/relations |
| Public natural-language text | 12–80 exact-tokenizer tokens |
| Identifier/scalar field | maximum 32 exact-tokenizer tokens |

### 8.1 Exact scored composition

Every accepted scenario contains exactly 36 gold-positive `(decision_step, action_id)` pairs, assigned one exclusive primary mechanism label:

| Exclusive positive class | Count |
|---|---:|
| Ordinary due/near-due current-state action | 8 |
| Correction or supersession-sensitive | 6 |
| Retraction/restoration-sensitive | 6 |
| Dependency activation/closure | 6 |
| Cross-scope continuity | 6 |
| Hidden-channel/monitor cue | 4 |

Every accepted scenario contains exactly 24 scored lure exposures:

| Exclusive lure class | Count |
|---|---:|
| Completed/canceled/terminal duplicate | 6 |
| Superseded/stale state | 6 |
| Wrong scope | 4 |
| Premature dependency | 4 |
| Irrelevant channel/distractor | 4 |

Exclusive labels are assigned by a frozen precedence table before reducer implementation. The 24 lure exposures are the complete set of non-gold public action affordances in the scored trajectory. Additional natural-language distractors may appear only when they introduce no additional action ID.

Every scenario contains at least one correction, retraction-of-correction, cancellation, retraction-of-cancellation, completion, reschedule, link, and unlink, plus reconstruction boundaries near 25%, 50%, and 75%.

### 8.2 Source-generator composition

Each 12-scenario block contains nine scenarios from generator A and three from independently implemented generator B. Hand-authored architecture-neutral challenge traces are mandatory at Gate 0 and smoke but do not enter confirmation unless a later revision freezes their sampling frame.

Development, smoke, external-pilot, confirmatory, and pre-inference-replacement seeds are disjoint and frozen before their first call.

## 9. Binding packet and output budgets

### 9.1 Freeze order

Before Gate 1, freeze:

1. Exact model, endpoint, request wrapper, tokenizer/counter, and tokenizer version.
2. Exact F+, TN, TF, and FM packet schemas.
3. Exact output JSON schema.
4. Total-event and per-decision mandatory-object bounds.
5. Canonical minimum, moderate, pressure, joint-maximum, and overflow fixtures.
6. An exhaustive list classifying every legal maximum fixture as target/non-overflow or excluded overflow.

The schema declarations are outside the memory-payload cap but included in logged full-input tokens. Their placement and arm-neutral wording are frozen.

### 9.2 Memory-payload selection

Candidate payload budgets, in order:

`1,536`, `2,048`, `3,072`, and `4,096` exact-tokenizer tokens.

Gate 1 chooses the smallest candidate satisfying all conditions before any model outcome exists:

1. F+, TN, TF, and FM serialize every target/non-overflow joint-maximum fixture and every frozen pressure packet without truncation or `budget_failure`.
2. At every pressure checkpoint, full unfiltered flat-current serialization exceeds the candidate by at least `1.25×`, and full chronological public history exceeds it by at least `1.5×`.
3. Every primary packet is 40%–95% utilized on pressure checkpoints, and at least half of pressure decisions place at least one primary packet at 60%–95%.
4. No local/provider compression, summarization, middle-out transform, or silent truncation occurs.
5. The realized selected/live ratio and arm density are published for every maximum fixture.

If no candidate passes, redesign the world/schema and recouncil. Never choose a budget from model performance.

Every paid target is certified non-overflow. A target-cell `budget_failure`, truncation, or serialization failure stops the experiment as `DESIGN_INVALID`; it is not a favorable score, retry, or reserve trigger.

### 9.3 Output cap

There is no hard-coded 512-token cap.

After the exact tokenizer and output schema are frozen:

1. Enumerate every legal maximum output: six maximum-length action IDs, twelve maximum-length channel IDs, maximum-length ongoing choice, null variants, and JSON syntax.
2. Token-count the exact canonical serialization.
3. Set `output_cap = ceil(1.20 × maximum_legal_output_tokens)`.
4. Prove the provider accepts that cap and exact response schema at the pinned endpoint.

The same output cap and schema apply to every arm.

## 10. Primary decision interface

The decision model has no callable tool and receives no prior conversation.

```json
{
  "ongoing_choice": "public-choice-id-or-null",
  "action_ids": ["public-action-id"],
  "channel_queries": ["public-channel-id"]
}
```

Use `response_format: json_schema` with `strict: true` when the frozen endpoint supports it, plus `require_parameters: true` under OpenRouter. Invalid JSON, schema violations, duplicate IDs after canonicalization, unknown IDs, or over-limit cardinality are primary failures. A repair call may be recorded only as a non-primary diagnostic.

## 11. Process-cold reconstruction

At the three frozen boundaries for each primary arm and each diagnostic arm when scheduled:

1. Persist, fsync as supported, close, and hash the arm artifact.
2. End the parent interpreter holding reducer state.
3. Create an empty run-owned temporary working directory and sanitized environment.
4. Launch one fresh child through the same adapter entry point used at ordinary start.
5. Provide only artifact bytes/path, current public observation, and capability-limited cursor via explicit stdin/arguments.
6. Reconstruct, emit canonical state hash/fields, exit, and wait.

The child import path excludes generator, scenario registry, event log, expected-state, and test-fixture modules. Scenario IDs exposed to the child are opaque randomized handles that cannot resolve source data. No working-directory fixture, environment variable, module global, cache, network call, or parent process may supply continuity.

Mandatory witnesses:

- Artifact withheld and artifact corrupted: fail closed or mechanically disagree.
- Ambient files/environment removed: valid artifact still succeeds.
- Prefix hash or cursor mutated: fail closed.
- Two valid incompatible artifacts A/B swapped under held-constant cursor/current observation: reconstructed states swap or fail according to artifact content.
- Independent artifact state fields mutated with valid framing/hash recomputed by the test harness: predicted reconstructed fields change correspondingly.
- Information sufficiency: artifact bytes alone plus current observation/cursor allow a separate reference decoder to recover the claimed canonical state.

## 12. Runner and storage

Use a thin direct Python runner with standard-library-first dependencies.

- Plain files and NDJSON only.
- One in-flight model request.
- One exact reconstruction child at a time.
- No Inspect, Harbor, agent framework, database, plugin system, daemon, or service.
- Explicit run directory and child PID/handle ownership.
- Close files, wait for the one child, and remove only run-owned disposable files.
- Never scan, kill, or alter unrelated processes, browsers, ports, or user files.

All paid responses remain immutable raw records. Analysis code consumes copies or read-only inputs.

## 13. Model and transport condition

Freeze in the run manifest:

- Canonical non-rolling model identifier.
- Exact provider endpoint slug/variant/region.
- API endpoint/version and byte-exact request wrapper.
- Reasoning effort, temperature, supported seed, output limit, and response schema.
- Context limit, supported parameters, timeout, and retry policy.
- Observable prices and exact tokenizer/counter.

OpenRouter is permitted only if no-paid mocks and a minimal owner-approved canary prove:

- Exact endpoint selection; no base-slug ambiguity.
- `allow_fallbacks: false`.
- `require_parameters: true`.
- Response caching disabled and cache status not a hit.
- Message transforms/context compression disabled.
- Router metadata explicitly enabled and returned.
- Returned requested model, selected provider/endpoint, attempt count, and pipeline match the frozen condition.
- Exact structured-output support survives at the selected endpoint.

Missing attestation, a cache hit, transform, fallback, second provider attempt, or endpoint mismatch invalidates the whole pair. If OpenRouter cannot prove the condition, use direct-provider transport.

## 14. Order, retry, and missing target pairs

- Pair FM and TN on the same scenario.
- Randomize and counterbalance order within each block.
- Freeze and hash the entire schedule before the first paid call.
- Run F+/TF only on the frozen diagnostic subset.
- Never reroll a valid response.
- Retry only when the client proves the request was never accepted or processed.
- A retry uses the clean pre-attempt artifact snapshot and same attempt lineage.
- Malformed valid responses are scored as failures, not retried.

A post-send accepted/no-body ambiguity makes the scheduled target pair missing. The pair remains part of the frozen target cohort and is never replaced in the primary estimand.

Pre-inference seed replacement is allowed only when no model request has been sent and a seed fails frozen generator invariants. Those replacements come from a frozen list and are logged.

For every analysis:

1. Report missingness by arm order, endpoint attempt, pressure, source generator, payload utilization, and failure stage.
2. Compute a worst-case/tipping interval assigning each missing target delta any value in `[-1,1]`.
3. A build or kill decision is allowed only if it is unchanged across that interval.
4. Stop as `TRANSPORT_INCONCLUSIVE` if missingness is associated with arm/order/pressure, if the decision tips, or if missing target pairs reach `5%` of the frozen cohort.

## 15. Mechanical outcomes

### 15.1 Primary scorer

For each scenario’s exactly 36 gold positives and 24 scored lures:

- `TP`: predicted action is gold due.
- `FP`: predicted action is one of the 24 scored non-gold available action exposures.
- `FN`: gold-due action not predicted.

Deduplicate IDs before scoring. An unknown ID, schema violation, or over-limit cardinality makes that arm's scenario response mechanically invalid and assigns scenario F1 `0`; it is never repaired or rerolled for the primary result.

`scenario_f1 = 2TP / (2TP + FP + FN)`

`delta_i = scenario_f1(TN) - scenario_f1(FM)`

The primary estimand is the arithmetic mean over the frozen independent target scenarios, subject to the missing-pair tipping rule. Decisions within a trajectory are not independent samples.

### 15.2 Mandatory secondary reports

- Precision, recall, prediction count, and overall due-action micro-F1.
- False actions by terminal, stale/superseded, wrong-scope, premature dependency, and distractor class.
- Per-positive-class hit rate.
- Duplicate execution.
- Exact reconstruction field accuracy.
- Payload utilization, record/relationship density, latency, retries, invalid/missing pairs, and cost.
- F+/TF/FM/TN store/render contrasts.
- Batched status/abstention diagnostic.
- Current-observation-only and oracle gaps.

No LLM judge may override a task score.

## 16. Oracle and memory-necessity controls

- **Current observation only:** proves each primary item actually requires history beyond the immediate observation.
- **Oracle-minimal:** smallest public facts/relationships required for the decision, without a due label or answer set.
- **Oracle-all-relevant:** all public relevant facts/conflicts/obligations, including redundancy.

A deterministic reference reasoner must solve each oracle fixture before inference, while a mechanical extractor given oracle memory without current time/observation/available actions must not directly recover the answer set.

Poor oracle performance makes the experiment `MODEL_OR_INTERFACE_CEILING`; it does not indict memory representation.

## 17. Pilot, inference, and decision rule

### 17.1 External engineering pilot

After every no-model gate and fresh council closure, propose 12 held-out paired FM/TN scenarios. Pilot scenarios never enter confirmation.

The pilot estimates only:

- Served request/response conformance.
- Cost, latency, malformed-output rate, route invalidity, and realized payload pressure.
- Whether the instrument behaves as frozen.

The pilot does **not** set or shrink confirmatory `n` through a chi-square SD bound. Any prompt, generator, reducer, materializer, scorer, transport, or outcome change after pilot results requires a new design revision and new pilot set.

### 17.2 Primary interval

The primary 95% interval remains the frozen two-sided Student-t interval over independent scenario deltas:

`mean(delta) ± t_ppf(0.975, n - 1) × sd(delta) / sqrt(n)`.

It is permitted only if the complete operating-characteristic gate below certifies it on the frozen support/family envelope. BCa bootstrap and paired permutation are reported sensitivities; they cannot replace or veto the primary interval after results exist.

### 17.3 Full-rule operating-characteristic gate

Before any pilot:

1. Enumerate the exact attainable per-arm F1 lattice from 36 positives and 24 lures and derive the attainable delta support in `[-1,1]`.
2. Freeze every distribution family, support point, mixture weight, target-mean construction, SD grid point, and retention rule in a machine-readable manifest.
3. Include smooth truncated, full score-lattice, symmetric/asymmetric two-point, three-point, and rare-tail mixtures with tail masses `0.01`, `0.025`, `0.05`, `0.10`, `0.15`, and `0.20` at attainable extreme and near-extreme support.
4. Cover SD from `0.05` in increments of `0.05` through the exact maximum feasible at each target mean, plus every discontinuity/extremum found by the lattice search. Do not stop at `0.40`.
5. Enumerate finite two-point/binomial cases exactly. For simulated cells, use at least 100,000 replicates and require a one-sided 95% Clopper-Pearson bound—not the raw Monte Carlo proportion—to satisfy each acceptance threshold.
6. Search candidate `n` in increments of 12, never below 48, with no silent maximum clamp.

`+0.03` is the minimum worthwhile boundary. `+0.08` is a planning alternative, not an observed-mean gate.

For every retained family at the relevant mean, chosen `n` must satisfy:

1. At true mean `+0.08`, lower primary endpoint exceeds `+0.03` with probability at least `0.80` using the conservative simulation bound.
2. At true mean `+0.03`, false-win probability is at most `0.05` using the conservative bound.
3. At true mean `0`, upper primary endpoint is below `+0.03` with probability at least `0.80`.
4. At true mean `+0.08`, false-kill probability is at most `0.05`.
5. Primary interval coverage is at least `0.94`.

If no affordable `n` passes the full feasible envelope, report `UNDERFUNDED` or revise the inferential method and recouncil. Do not narrow the distribution envelope after seeing pilot outcomes.

### 17.4 Cost gate

Before the pilot, publish call and dollar envelopes for every candidate `n`, including:

- Two primary calls per step.
- F+ and TF on exactly 25%.
- One batched status probe per diagnostic arm/scenario.
- Frozen oracle/control fractions.
- Three reconstruction boundaries.
- Expected missing-pair cost without counting replacements as target evidence.
- Exact input/output/cache token assumptions and current prices.

Owner approval is required for a maximum spend. An unaffordable design returns `UNDERFUNDED`.

### 17.5 Build, kill, and inconclusive

**BUILD typed Stage B** only if all hold:

1. Lower primary 95% endpoint for `TN-FM` exceeds `+0.03` across the missing-pair tipping interval.
2. TN is not more than `0.02` worse on overall due-action F1 than FM or the best non-oracle deterministic control.
3. Upper endpoint for excess stale/wrong-scope/duplicate actions is below `+0.02`.
4. Reconstruction meets the frozen 95% required-field criterion and every causal witness.
5. TN stays inside the frozen packet budget.
6. No generator, route, cache, transform, retry, hidden-history, or scoring violation exists.
7. Diagnostics do not reveal a schema/materializer mismatch; presentation is already held fixed in the primary FM/TN comparison.

**KILL typed-native action package for this envelope** if the upper primary endpoint is below `+0.03` across the missing-pair tipping interval, or if TN adds material stale/wrong-scope/duplicate harm, cannot fit, or fails the preregistered parity/validity gates.

A kill means only that TN did not earn complexity for prospective action selection here. A material predeclared status/abstention benefit authorizes a smaller follow-up audit/conflict experiment; it does not overturn the action result.

Everything else is `INCONCLUSIVE`, `UNDERFUNDED`, `DESIGN_INVALID`, `TRANSPORT_INCONCLUSIVE`, or `MODEL_OR_INTERFACE_CEILING`.

## 18. No-model gates

### Gate 0 — world, transition semantics, and scorer

- Exact quotas and bounds for both generators.
- Independent transition-table and property tests.
- Exhaustive short traces and hand-authored nested challenges.
- Gold-taint canaries and byte-identical public inputs.
- Current-observation-only failure for every memory-required positive.
- Exact scorer, deduplication, malformed-output, and one-action-quantum fixtures.

### Gate 1 — comparator, render, packets, and budgets

- F+ replay restores every legal retraction/cancellation trace.
- F+, FM, TF, and TN all perform bounded BFS and reverse dependency activation.
- Semantic-ID parity against independent selector.
- FM render-matching, neutralization, and no-invented-typing tests.
- Exact schemas/tokenizer and canonical joint maxima.
- Exhaustive non-overflow/overflow classification.
- Candidate packet selection and derived maximum output cap.

### Gate 2 — reconstruction

- Artifact withheld/corrupt and ambient-removal witnesses.
- Sanitized directory/environment/import path.
- Opaque scenario IDs.
- Valid-artifact swap and independent-field mutation witnesses.
- Child cleanup and exact wait/termination.

### Gate 3 — transport and cell identity

- Mock transcript of exact request bytes.
- Endpoint/provider/cache/fallback/transform/parameter assertions.
- Router-metadata and structured-output conformance canary.
- Pre-dispatch retry, post-send ambiguity, malformed response, timeout, and interruption injection.
- Missing-pair tipping and correlation injection.

### Gate 4 — statistics and cost

- Exact score/delta support enumeration.
- Frozen family/grid/retention manifest.
- Exact finite-support and conservative Monte Carlo acceptance fixtures.
- Complete decision-rule operating characteristics.
- Exact diagnostic fractions and cost table.

### Gate 5 — engineering smoke

- Two non-confirmatory scenarios through all scheduled arms, controls, reconstruction, transport, scoring, audit, and cleanup.
- Mock provider or explicitly owner-approved inexpensive endpoint.
- Zero leaked process, watcher, daemon, or temporary run-owned artifact after cleanup verification.

Only after all gates pass and a fresh sealed council finds no P0/P1 scientific blocker may the 12-pair pilot be proposed.

## 19. Run artifacts and cleanup

Retain:

- Frozen manifest, design hash, schedule, target cohort, and pre-inference replacement list.
- Generator versions, seeds, public events, protected private gold, and quota audits.
- Reducer/materializer versions and semantic-parity audits.
- Exact requests/responses and route metadata.
- Arm artifacts and reconstruction causal-witness results.
- Raw scores, missing-pair bounds, analysis outputs, and operating-characteristic evidence.
- Token, density, latency, invalidity, and cost logs.

Temporary files live beneath one explicit run-owned directory. The runner closes files, waits for or terminates only its own recorded child, removes only run-owned disposable files, and leaves no daemon or watcher.

## 20. Prior art used as method, not answer

- [StateFuse](https://arxiv.org/abs/2607.05844): strong flat/raw-log baselines with matched resolver and verification policies.
- [Presentation, Not Mechanism](https://arxiv.org/abs/2607.16019): render-matched control separating layout from mechanism; FM applies this lesson to the primary comparator.
- PM-Bench: prospective actions, lures, and set-F1 framing.
- Mem2ActBench: memory-necessity/current-input leakage checks.
- AgenticSTS and LongHorizon-Harness: fresh-context/fresh-executor discipline.
- NIST SD guidance: normality limitation of chi-square SD intervals.
- Current OpenRouter official docs: exact endpoint, `require_parameters`, cache, transform, and opt-in routing metadata controls.

No reviewed work answers this exact FM-versus-TN question under matched deterministic writing and presentation, frozen mechanism quotas, a binding packet, process-cold artifact-causal reconstruction, route controls, and prospective action scoring.

## 21. Authorization

r3 authorizes only:

1. Fresh sealed experiment-specific council review.
2. If that closes with no P0/P1 scientific blocker, a separate harness implementation plan.

Separate owner approval is required for harness implementation, model/provider/tokenizer choice, any canary or paid inference, pilot manifest/spend, and confirmation manifest/spend.
