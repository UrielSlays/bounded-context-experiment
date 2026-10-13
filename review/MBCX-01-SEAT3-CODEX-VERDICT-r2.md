NO-GO — the confirmatory decision rule is not powered for the declared win/kill claims.

The mechanism is worth testing, but r1 can produce a scientifically misleading negative or inconclusive result even when the true typed-arm improvement equals its declared `+0.08` target. Pilot inference should not begin until the statistical decision rule, metric resolution, comparator, and maximum-load contract are repaired.

## 1. Top-level verdict

**Verdict: NO-GO. EXECUTED.**

If Stage A reported a win under the current design, I would not yet believe representation caused it: Arm L lacks a strong ordinary urgency/relevance projection, and the public event grammar can pre-resolve T’s ontology.

If Stage A failed, I would not regard T as fairly tested: the `+0.08` target is also the observed-mean win threshold, so a true `+0.08` effect has approximately a 50%—not 80%—chance of clearing that part of the win rule. The separate kill precision objective can require several times more scenarios.

Build-decision challenge:

- **ALREADY-BUILT? EXECUTED — SEARCHED.** No exact prior art performs the pinned comparison: deterministic flat-current state versus deterministic typed/versioned continuity, with matched public events, prompts, budgets, provider, and prospective-action scoring. I searched the pinned repository and found no `.py`, `.js`, `.ts`, `pyproject.toml`, or requirements file at the pin. Do not build the surrounding benchmark machinery from scratch: directly adopt PM-Bench’s deterministic world/scorer patterns, AgenticSTS’s fresh-message contract, and LongHorizon-Harness’s external-state/fresh-executor pattern.

- **PRODUCT-FIT? READ-ONLY — UNSEARCHED—SETTLED-BY-PINNED-BYTES.** Customer need, in one sentence: **determine whether bounded typed continuity is worth engineering over a strong flat ledger before spending production effort.** That is governed power and fail-loud experimentation, not a completeness or “cannot be bypassed” promise. The current statistical defect violates that posture because it can turn an adequately powered significance test into an inadequately powered architecture verdict.

- **BIGGER-THAN-THE-BUG? READ-ONLY — UNSEARCHED—SETTLED-BY-PINNED-BYTES.** Generally no: this is a temporary laboratory instrument and has re-entered a design gate. Keep it that way. Do not implement the optional Inspect compatibility branch in the first instrument.

## 2. Pin/byte verification

**EXECUTED.**

- Requested commit resolved exactly to `7fa45e092bb7db14d85761f65a63b97a3740c65e`.
- Read `MBCX-01-EXPERIMENT-DESIGN-r1.md` directly from that Git object.
- Pinned artifact: 27,182 bytes.
- SHA-384: `8D8F7B083B32C5CC4B9F682C29D759967D3A71CD4B452DEE96EEC06785189A89A42B1FC95BB864B1D574117BE4729E32`.
- Current `HEAD` is newer: `84cca38157799d036bcf2e63d7e2590b6d560099`.
- The working-tree artifact is also 27,182 bytes with the same SHA-384 and is byte-identical to the pin. There is therefore no byte conflict; the owner-locked pin governs and the tree happens to match it.
- `LOCAL-SOURCE-MANIFEST-r1.md` exists at the pin and was read completely.
- Targeted Git status for the artifact and manifest was clean.
- No prior-verdict or sealed-seat file was opened.

## 3. Evidence read and probes run

Evidence read:

- `MBCX-01-EXPERIMENT-COUNCIL-PACKET-r2.md:1-364`.
- `MBCX-01-EXPERIMENT-DESIGN-r1.md:1-542@7fa45e092bb7db14d85761f65a63b97a3740c65e`.
- `LOCAL-SOURCE-MANIFEST-r1.md:1-79@7fa45e092bb7db14d85761f65a63b97a3740c65e`.
- `<vault>`, complete current bytes.
- External origins listed in §11 below.

Probes:

- **Maximum-load/token attack — EXECUTED.** I constructed compact ASCII JSON fixtures and ran them through `o200k_base` using the 199,998-entry public rank table at `niieani/gpt-tokenizer` blob `fbc14c2e1e71f5f666d5513d8a94da81381fe0be`.

| Objects | Arm L | Strong L+ | Arm T | Common output |
|---:|---:|---:|---:|---:|
| 24 | 1,367 tokens | 2,160 | 2,946 | 779 |
| 60 | 3,383 | 5,364 | 7,302 | 1,907 |
| 120 | 6,743 | 10,704 | 14,568 | — |
| 240 | 13,463 | 21,384 | 29,091 | — |

  These are fixture counts, not predictions of realized requests. They prove that r1’s minima do not define a “maximum-load” case and that the 512-token output limit is not provably sufficient. The actual provider tokenizer remains deliberately unfrozen in r1.

- **Metric-granularity attack — EXECUTED.**

| High-stress composition | One/two decision change |
|---|---:|
| 1 due singleton + 29 empty; recover the miss | `+1.0000` |
| 30 due singletons; recover one miss | `+0.01695` |
| 10 due + 20 empty; recover one miss | `+0.05263` |
| 10 due + 20 empty; recover two misses | `+0.11111` |
| 30 due; suppress one false action | `+0.01639` |

  Thus “30 due or non-due opportunities” does not make `+0.08` intrinsically a multiple-decision effect.

- **Statistical attack — EXECUTED.** I ran 5,000 seeded repetitions per cell over three bounded/lumpy paired-delta distributions. The interval was a normal-approximation sensitivity interval, not a simulation of r1’s unspecified bootstrap flavor.

| True distribution, mean `+0.08` | n | CI excludes zero | Full win component: CI > 0 and observed mean ≥ `+0.08` |
|---|---:|---:|---:|
| Tight, SD ≈ `.10` | 48 | 99.98% | 49.90% |
| Tight, SD ≈ `.10` | 800 | 100% | 49.68% |
| Two-point, SD `.30` | 112 | 80.40% | 52.82% |
| Two-point, SD `.30` | 800 | 100% | 51.50% |
| Rare `1` with probability `.08` | 112 | 98.30% | 54.20% |
| Rare `1` with probability `.08` | 800 | 100% | 51.74% |

  The roughly 50% ceiling is structural: when the true mean equals the point-estimate threshold, increasing `n` concentrates the estimate around that threshold rather than placing 80% of estimates above it.

  Normal-approximation sizing at SD `.30` was 111 scenarios for superiority of `.08` versus zero, but 785 for a `.03` upper-bound precision objective. At SD `.50`, the corresponding counts were 307 and 2,181.

  For a rare-effect distribution, a 12-pair pilot has a 36.77% probability of observing all zeroes and a 75.13% probability of observing no more than one positive. A variance upper multiplier cannot recover an unseen mixture component from an all-zero pilot.

- **Architecture-privilege attack — EXECUTED.** I built a public supersession event containing `status_after`, a typed dependency trigger, dependency closure, stable IDs, and an action handle. Private-field canaries and byte-identical adapter input passed, while the public grammar already expressed T’s native ontology. The only intended catches are the undefined “representation-blind invariant” and manual review at lines 200–202.

- **Strong flat comparator — EXECUTED.** Constructed L+ keeps current scoped state plus `obligation_id`, `action_id`, trigger, status, `dependencies_remaining`, `next_check_at`, last public event, and a deterministic stable relevance projection. Lines 100–109 contain the first five concepts but not the latter four. Arm L therefore does not yet contain this comparator.

- **Reconstruction attack — EXECUTED.** I withheld the artifact and replayed a public cursor carrying prior public history; current state reconstructed successfully. R1 does not define the cursor schema or forbid that capability, so the named process-cold construct is not yet enforced.

- **Production differential — not executable.** No r1 harness or production counterpart exists at the pin. No paid inference was run.

## 4. Experiment-specific applicability ruling

**READ-ONLY.**

I excluded licensing, distribution, production cryptography, multi-tenant authorization, malicious-user threat modeling, seal chains, crash durability, broad process lifecycle management, PR ceremony, and Moonwalker delivery workflow. The artifact expressly limits reconstruction to process-cold reopening and rejects a generalized lifecycle subsystem at lines 253–268; the scope override permits a finding only when it reaches a false experimental answer.

Framework cache, retry, hidden-history, and routing behavior stayed in scope because each can directly alter arm inputs, selectively reroll cells, or change the provider condition.

## 5. Claim scoreboard C1–C12

| Claim | Ruling | Basis |
|---|---|---|
| C1 — Stage A is causally identified | **UNDERDETERMINED** | `READ-ONLY`; public semantic transitions and arm-specific materializers remain unresolved. **UNSEARCHED—SETTLED-BY-PINNED-BYTES.** |
| C2 — Arm L is strong enough | **FALSE** | `EXECUTED`; L+ adds ordinary urgency/relevance fields and selection policy absent at lines 100–109. **SEARCHED.** |
| C3 — Treatment-budget symmetry is real | **FALSE** | `EXECUTED`; exact-token fixtures cross the budgets, while r1 supplies no maximum cardinalities. **SEARCHED.** |
| C4 — Generated world does not privilege T | **UNDERDETERMINED** | `EXECUTED`; constructed T-shaped public event passes concrete byte checks; the governing neutrality test is undefined. **SEARCHED.** |
| C5 — Outcome has useful resolution | **FALSE** | `EXECUTED`; opportunity count alone does not bound the F1 quantum. **UNSEARCHED—SETTLED-BY-PINNED-BYTES.** |
| C6 — Reconstruction measures named construct | **UNDERDETERMINED** | `EXECUTED`; cursor authority is not defined, and cursor-only replay can reconstruct state. **UNSEARCHED—SETTLED-BY-PINNED-BYTES.** |
| C7 — Runner is experimentally neutral | **HOLDS as a design rule** | `READ-ONLY`; direct runner is default and Inspect is gated, but runtime conformance remains unproved. **SEARCHED.** |
| C8 — Exact model/provider is frozen | **UNDERDETERMINED** | `READ-ONLY`; the manifest contract is sound, but no actual model, endpoint, wrapper, or returned metadata is frozen yet. **SEARCHED.** |
| C9 — Order/retry identity cannot mimic effect | **HOLDS as a design rule** | `READ-ONLY`; pairing, counterbalancing, frozen schedule, clean snapshots, and no reroll are explicit at lines 319–330. **UNSEARCHED—SETTLED-BY-PINNED-BYTES.** |
| C10 — Statistical plan supports win and kill | **FALSE** | `EXECUTED`; the power target differs from the composite win rule and kill precision objective. **SEARCHED.** |
| C11 — Oracle diagnostics are honestly scoped | **UNDERDETERMINED** | `READ-ONLY`; use is scoped, but “smallest logically sufficient” lacks a construction rule and may transcribe the answer. **SEARCHED.** |
| C12 — Instrument is proportionate | **HOLDS** | `READ-ONLY`; direct runner and one-child supervisor are appropriately small. Defer the optional Inspect branch. **SEARCHED.** |

## 6. r0 closure table

| # | Inherited finding | r1 status | Exact r1 mechanism |
|---:|---|---|---|
| 1 | Writer confound | **CLOSED — READ-ONLY** | Both primary reducers are deterministic; no rewritten memory appears in model output, lines 96–123 and 161. |
| 2 | Output-cap confound | **PARTIALLY CLOSED — EXECUTED** | Common action schema replaces ledger rewriting, but output cardinality/headroom remains undefined, lines 150–161 and 244–249. |
| 3 | Weak comparator | **PARTIALLY CLOSED — EXECUTED** | Arm L exists but omits a frozen heartbeat/urgency/relevance projection, lines 100–109. |
| 4 | History budget not binding | **CLOSED — READ-ONLY** | Budget-pressure slice must exceed the common budget by a declared factor, line 235. |
| 5 | Hidden runner state | **MOVED — READ-ONLY** | Shifted to direct-runner default and Inspect conformance gate, lines 272–298 and 469–476; no implementation yet proves closure. |
| 6 | Provider ambiguity | **PARTIALLY CLOSED — READ-ONLY** | Exact endpoint, no fallback/transforms, and returned metadata are required, lines 300–317; actual transport is deferred. |
| 7 | Missing order control | **CLOSED — READ-ONLY** | Paired, counterbalanced, interleaved, frozen schedule, lines 319–329. |
| 8 | Fragile sizing | **OPEN — EXECUTED** | Minimum 48/no clamp is better, but the actual win/kill operating characteristics are not powered, lines 373–424. |
| 9 | False cold restart | **PARTIALLY CLOSED — EXECUTED** | Fresh interpreter is required, but cursor authority and artifact-withheld negative tests are missing, lines 257–266. |
| 10 | Oracle/gold contradiction | **CLOSED — READ-ONLY** | Oracle exemption and non-primary diagnostic status are explicit, lines 125–134. |
| 11 | Generator privilege | **PARTIALLY CLOSED — EXECUTED** | Several tests were added, but “representation-blind” is not operationalized, lines 193–202. |
| 12 | Production-doctrine leakage | **CLOSED — READ-ONLY** | Supervisor owns one child; generalized lifecycle machinery is excluded, lines 268 and 498. |

## 7. Findings

### P0 — Confirmatory decision calibration is internally inconsistent

- **Artifact:** `MBCX-01-EXPERIMENT-DESIGN-r1.md:373-424@7fa45e…`
- **Mechanism:** sizing targets 80% power for `.08` versus zero, while win also requires the observed mean to be at least `.08`. At a true `.08`, the latter condition is crossed only about half the time. Kill uses a different `.03` upper-bound precision objective.
- **Consequence:** false negative or persistent inconclusive outcome for a genuinely useful T; inability to make the declared kill decision at the funded `n`.
- **Fix class:** **preregistered decision-rule and operating-characteristic calibration**—simulate the complete win/kill/inconclusive rule across a frozen bounded/lumpy distribution envelope, separate superiority power from kill precision, freeze the interval method, and impose a variance/distribution floor independent of the 12-pair pilot.
- **EXECUTED — SEARCHED.** Small-pilot variance uncertainty is a documented methods problem, and bootstrap method choice matters for skewed means. The percentile bootstrap can materially under-cover skewed means; paired permutation is suitable for paired F1-like statistics but answers the null-test question, not the `.08` win threshold. [Safe variance reassessment](https://journals.sagepub.com/doi/10.1177/25152459231212128), [percentile-bootstrap coverage](https://journals.sagepub.com/doi/full/10.1177/2515245920911881), [paired permutation for structured/F1 statistics](https://aclanthology.org/anthology-files/pdf/naacl/2022.naacl-main.360.pdf).

### P1 — “Thirty opportunities” does not guarantee metric resolution

- **Artifact:** `MBCX-01-EXPERIMENT-DESIGN-r1.md:208-224,332-340,398-410@7fa45e…`
- **Mechanism:** r1 counts due **or non-due opportunities**, but does not define aggregation, empty-set behavior, or a minimum TP/FN/FP denominator.
- **Consequence:** a single decision can move scenario F1 by `1.0`, `.0526`, or another large quantum, making `+0.08` incomparable across scenario families.
- **Fix class:** **scorer estimand/cardinality contract**—freeze aggregation and empty-set conventions, require minimum positive and eligible false-positive exposures, and precompute the maximum one-decision quantum.
- **EXECUTED — UNSEARCHED—SETTLED-BY-PINNED-BYTES.**

### P1 — Arm L is not yet the strongest simple comparator

- **Artifact:** `MBCX-01-EXPERIMENT-DESIGN-r1.md:96-109,121-123@7fa45e…`
- **Mechanism:** L keeps current facts and open obligations but lacks a frozen `next_check_at`/heartbeat rule, remaining-dependency count, stable relevance horizon, and deterministic bounded projection. T gets due/near-due/relevant-closure selection.
- **Consequence:** persuasive false positive for T caused by selection/materialization policy rather than typed/versioned representation.
- **Fix class:** **comparator-strength and materializer-parity specification**—promote L+ to the primary comparator or add it as a primary/sensitivity arm.
- **EXECUTED — SEARCHED.** PM-Bench exposes TODO-ledger and heartbeat variants and reports that no scaffold dominates; selective intervention likewise outperforms passive or always-on memory exposure. [PM-Bench paper](https://arxiv.org/html/2607.12385), [PM-Bench repository](https://github.com/genglinliu/PMBench), [Remember When It Matters](https://arxiv.org/abs/2607.08716).

### P1 — Architecture-neutrality gate is not executable as written

- **Artifact:** `MBCX-01-EXPERIMENT-DESIGN-r1.md:169-202@7fa45e…`
- **Mechanism:** “canonical public transition fields” may encode status, dependency closure, supersession, and scope in T-native form. Byte equality proves both arms received the same privilege; it does not prove neutrality.
- **Consequence:** false positive for T from generator/ontology alignment.
- **Fix class:** **public-schema architecture-neutrality test**—restrict public events to independently justified primitive observations or compile identical worlds through independently shaped public encodings and require invariant arm conclusions; retain hand-authored strata.
- **EXECUTED — SEARCHED.** Mem2ActBench uses lexical checks plus a blinded query-only solvability discriminator because field-name canaries cannot detect semantic leakage; STITCH demonstrates that scope/event/entity structure materially changes retrieval. [Mem2ActBench](https://aclanthology.org/2026.acl-long.370.pdf), [STITCH/CAME](https://arxiv.org/abs/2601.10702).

### P1 — “Maximum load” is undefined, so budget parity cannot be gated

- **Artifact:** `MBCX-01-EXPERIMENT-DESIGN-r1.md:204-251,460-467@7fa45e…`
- **Mechanism:** scenarios provide minima but no maximum open obligations, facts, dependencies, action IDs, claims, or provenance IDs.
- **Consequence:** T can be unfairly killed by required closure overhead, or T can be favored if its materializer filters while L serializes the full ledger; the common 512-token output can also become impossible.
- **Fix class:** **bounded-domain/cardinality grammar and target-tokenizer contract**.
- **EXECUTED — SEARCHED.** The no-cost `o200k_base` counts came from the opened rank-table origin, but this is only an appropriate sensitivity tokenizer until the actual provider counter is frozen. [Rank data](https://github.com/niieani/gpt-tokenizer/blob/main/data/o200k_base.tiktoken).

### P2 — Public cursor authority can defeat process-cold reconstruction

- **Artifact:** `MBCX-01-EXPERIMENT-DESIGN-r1.md:253-266,460-476@7fa45e…`
- **Mechanism:** “public scenario cursor” is not defined as an opaque index/capability. If it carries or resolves history, the arm artifact is unnecessary.
- **Consequence:** hidden confound favoring L by erasing the value of T’s persisted reconstruction state.
- **Fix class:** **reconstruction boundary/capability specification plus artifact-withheld negative test**.
- **EXECUTED — UNSEARCHED—SETTLED-BY-PINNED-BYTES.**

### P2 — Provider/framework conformance needs exact rejection assertions

- **Artifact:** `MBCX-01-EXPERIMENT-DESIGN-r1.md:270-330,469-476@7fa45e…`
- **Mechanism:** Inspect preserves messages/state and checkpoint behavior unless configured; routing layers can fall back, cache, transform, or omit proof metadata.
- **Consequence:** either arm can inherit history, receive a modified prompt, or get a selectively retried provider path.
- **Fix class:** **mock-transport conformance and fail-closed route-attestation contract**.
- **READ-ONLY — SEARCHED.** Inspect documents accumulated `TaskState.messages`, local/provider caching, checkpoint restoration, warning-and-continue failure behavior, and adaptive concurrency. OpenRouter defaults to load balancing/fallback, supports middle-message compression, uses provider sticky caching, and omits routing metadata on response-cache hits. [Inspect solvers](https://inspect.aisi.org.uk/solvers.html), [caching](https://inspect.aisi.org.uk/caching.html), [checkpointing](https://inspect.aisi.org.uk/checkpointing.html), [model concurrency](https://inspect.aisi.org.uk/models-concurrency.html), [OpenRouter routing](https://openrouter.ai/docs/guides/routing/provider-selection), [message transforms](https://openrouter.ai/docs/guides/features/message-transforms), [router metadata](https://openrouter.ai/docs/guides/features/router-metadata).

### P2 — Oracle-minimal is not a frozen policy

- **Artifact:** `MBCX-01-EXPERIMENT-DESIGN-r1.md:125-134,226-236@7fa45e…`
- **Mechanism:** “smallest gold-derived packet logically sufficient” can transcribe an action answer or remove redundancy the model needs.
- **Consequence:** an artificially perfect or artificially poor oracle can misdiagnose the model/task ceiling and change interpretation under lines 512–514.
- **Fix class:** **oracle construction and answer-separation specification**.
- **READ-ONLY — SEARCHED.** Mem2ActBench’s blinded discriminator provides a directly borrowable pattern for proving current-input insufficiency without placing the target action into the input. [Mem2ActBench appendix](https://aclanthology.org/2026.acl-long.370.pdf).

## 8. WHAT WOULD YOU BUILD?

**READ-ONLY.**

A small direct laboratory instrument:

1. A frozen primitive public-event grammar and deterministic seeded world generator/scorer adapted from PM-Bench. **SEARCHED.**
2. Two pure reducers over identical event bytes:
   - L+: current scoped facts, open obligations, remaining dependencies, explicit next-check/heartbeat time, and stable deterministic bounded projection.
   - T: immutable evidence, versions, typed lifecycle/dependencies, and bounded closure.
3. Stateless packet builders and a direct HTTP request builder with concurrency one.
4. A capability-limited cursor containing only scenario identity, next-step index, and a hash commitment—not replayable history.
5. A mock provider that records exact bytes and injects pre-body, post-body, timeout, malformed-schema, cache-header, and interruption failures.
6. Process-spawn reconstruction tests, JSONL audit logs, and one frozen mechanical scorer/analysis script.

Prior art to borrow:

- PM-Bench’s deterministic scenario generation, replay scoring, lures, updates, channels, ledger, and heartbeat variants. **SEARCHED.**
- AgenticSTS’s fresh-message/no-transcript contract and layer ablation discipline. **SEARCHED.**
- LongHorizon-Harness’s external state and fresh-executor separation. **SEARCHED.**
- Mem2ActBench’s current-input leakage discriminator. **SEARCHED.**

No database abstraction, plugin platform, generalized supervisor, or Inspect compatibility layer belongs in the first build.

## 9. WOULD YOU DESIGN IT DIFFERENTLY?

**READ-ONLY — yes.**

I would first run a no-model differential phase proving that L+ and T agree on all common current-state/obligation semantics and documenting exactly which T-native information L+ cannot represent.

For the paid phase I would use:

- Primary: L+ native projection versus T native bounded packet, honestly named a **representation-plus-materialization package** comparison.
- Diagnostic: T persisted state projected through the L+ packet format. This distinguishes gains from T’s persisted semantics from gains created only by its privileged selector/serializer.
- A hand-authored scenario stratum reported separately from generated cases.
- A decision rule whose full win/kill/inconclusive operating characteristics—not merely a zero-null significance test—meet preregistered targets.

This is narrower and more causally legible than claiming the current two-arm result isolates “representation” alone.

## 10. Omission attack

- **Omitted strong comparator — EXECUTED:** L+ with deterministic urgency/heartbeat and relevance projection.
- **Hidden confound favoring L — EXECUTED:** cursor or scenario loader exposes replayable public history, erasing the value of T’s artifact.
- **Hidden confound favoring T — EXECUTED:** canonical public transitions pre-resolve T’s status/dependency/supersession ontology.
- **Framework/provider footgun — READ-ONLY, SEARCHED:** accumulated Inspect messages or OpenRouter fallback/cache/context compression silently changes requests.
- **Persuasive false positive — EXECUTED:** weak L selection plus T-shaped events produces a clean paired advantage falsely attributed to representation.
- **Unfairly kill useful T — EXECUTED:** a rare/lumpy true effect is underestimated by the 12-pair pilot, or T fails an undefined maximum-load case; the composite win then has only about 50% power at the declared target.
- **Delete — READ-ONLY:** optional Inspect replacement work from the first Stage A implementation.
- **Missing no-paid test — EXECUTED:** artifact-withheld, cursor-only reconstruction must fail. I also require raw request-byte equality and route/cache/transform rejection before pilot.
- **Prior-art mechanism to borrow — READ-ONLY, SEARCHED:** PM-Bench deterministic world/replay scorer plus AgenticSTS fresh-message assembly.

## 11. Sweep log

All research papers were checked for status and applicability. ArXiv work is current primary research evidence, not a controlling standard; ACL papers provide peer-reviewed benchmark methods. No law or regulator bears directly on whether this experiment returns a false answer.

| Exact query family | Origins opened; decisive section | Change/confirmation; stop rule |
|---|---|---|
| `"PM-Bench" prospective memory deterministic scenario TODO ledger heartbeat`; `"AgenticSTS" fresh message typed memory ablation`; `"Mem2ActBench" memory action evaluation query-only discriminator`; `"LongHorizon-Harness" fresh context durable verified state` | [PM-Bench §3–4](https://arxiv.org/html/2607.12385) and [repo README](https://github.com/genglinliu/PMBench); [AgenticSTS abstract](https://arxiv.org/abs/2607.02255) and [repo](https://github.com/AlayaLab/AgenticSTS); [Mem2ActBench §3.4/§4 and appendix](https://aclanthology.org/2026.acl-long.370.pdf); [LongHorizon-Harness abstract](https://arxiv.org/abs/2608.01964) and [repo “Three roles”](https://github.com/AMAP-ML/LongHorizon-Harness) | Confirmed reusable generator/scorer, fresh-message, leakage-check, and external-state mechanisms. None answers the exact L-versus-T comparison. |
| `"LongMemEval-V2" AgentRunbook memory controller accuracy latency`; `"Remember When It Matters" proactive memory selective intervention`; `"MAGE" hierarchical execution-state tree agent memory`; `"STITCH" contextual intent scope event entity memory` | [LongMemEval-V2 Evaluation/AgentRunbook](https://xiaowu0162.github.io/longmemeval-v2/); [Remember When It Matters abstract](https://arxiv.org/abs/2607.08716) and [repo Architecture](https://github.com/yifannnwu/proactive-memory-agent); [MAGE execution-state tree](https://arxiv.org/abs/2606.06090); [STITCH abstract/§2](https://arxiv.org/abs/2601.10702) | Confirmed that selection/intervention, structured scope, and controller latency are load-bearing. This strengthened the L+ finding and narrowed external-validity claims. |
| `deterministic flat state ledger typed versioned memory controlled experiment LLM agent benchmark`; `factorial experiment memory representation retrieval policy long horizon LLM agent benchmark`; `synthetic benchmark generator bias architecture-specific representation evaluation LLM agents`; `benchmark construct validity synthetic generated tasks architecture privilege machine learning evaluation` | Opened the above primary papers/repositories plus their cited project pages where relevant | Reworded around the mechanism after no exact match. Stopped because multiple adjacent systems were found but none implements the pinned matched comparison; the experiment is not obsolete. |
| `pilot study sample size variance uncertainty upper confidence bound sample size re-estimation paired trial methodology`; `paired bootstrap confidence interval mean skewed bounded data coverage percentile bootstrap methodology`; `exact paired permutation test difference F1 NLP systems`; `counterbalancing order effects paired crossover experiment methodology` | [Safe variance reassessment](https://journals.sagepub.com/doi/10.1177/25152459231212128), especially sample-size/variance sections; [percentile-bootstrap coverage simulation](https://journals.sagepub.com/doi/full/10.1177/2515245920911881); [exact paired permutation, Appendix B/F1](https://aclanthology.org/anthology-files/pdf/naacl/2022.naacl-main.360.pdf); [Better bootstrap-t intervals](https://arxiv.org/abs/2508.10083) | Confirmed small-pilot and bootstrap-footgun concerns. Stopped because executed arithmetic independently settles the composite-win inconsistency. |
| `site:inspect.aisi.org.uk TaskState messages checkpoint failure caching model concurrency official`; `site:inspect.aisi.org.uk checkpoint warning continue max_consecutive_failures official`; `site:openrouter.ai/docs provider routing allow_fallbacks require_parameters only official`; `site:openrouter.ai/docs prompt caching response caching message transforms router metadata official` | [Inspect solvers](https://inspect.aisi.org.uk/solvers.html), [caching](https://inspect.aisi.org.uk/caching.html), [checkpointing](https://inspect.aisi.org.uk/checkpointing.html), [concurrency](https://inspect.aisi.org.uk/models-concurrency.html); [routing](https://openrouter.ai/docs/guides/routing/provider-selection), [prompt caching](https://openrouter.ai/docs/guides/best-practices/prompt-caching), [response caching](https://openrouter.ai/docs/guides/features/response-caching), [transforms](https://openrouter.ai/docs/guides/features/message-transforms), [metadata](https://openrouter.ai/docs/guides/features/router-metadata) | Confirmed current default/optional behavior and exact no-paid assertions. Stopped at the official current documentation because it controls the narrow behavior question. |
| `online tokenizer API count tokens OpenAI o200k_base endpoint`; `tiktoken web API encode tokens public endpoint`; `Hugging Face tokenizer API count tokens OpenAI GPT-4o tokenizer` | [gpt-tokenizer `o200k_base` rank data](https://github.com/niieani/gpt-tokenizer/blob/main/data/o200k_base.tiktoken) and token-split regex source | Enabled an actual in-memory tokenizer probe after local packages and outbound package installation were unavailable. Stopped after rank count and fixture execution succeeded. |

## 12. Residual risks and explicit non-claims

- **EXECUTED:** No implemented r1 harness exists, so no end-to-end mock-provider, interruption, or direct-versus-framework differential could be run.
- **EXECUTED:** Token probes used synthetic ASCII fixtures and `o200k_base`; they do not replace the later exact provider counter and realized request accounting.
- **EXECUTED:** Statistical simulations used a normal-interval sensitivity approximation. They do not establish coverage for the eventual bootstrap method; that method is itself unfrozen. The decisive threshold mismatch does not depend on this approximation.
- **READ-ONLY:** One model/provider and synthetic domain-neutral scenarios cannot establish cross-model, natural-language-writer, production, or open-world generality.
- **READ-ONLY, SEARCHED:** Router metadata cannot attest cache-hit provenance because OpenRouter documents that cache hits omit it. Route verification therefore needs explicit cache rejection, not metadata alone.
- **READ-ONLY:** Oracle success will not prove deployability; oracle failure will not automatically prove a representation defect.
- **READ-ONLY:** This verdict makes no claim about licensing, distribution, production security, durability, multi-agent memory, emotional/personality memory, or delivery readiness.
- **READ-ONLY:** Residual after fixes: a positive Stage A would support only the tested representation-plus-materializer package under the frozen model/provider, not a universal typed-memory substrate.

## 13. Seat capability report

- **Model:** OpenAI Codex, GPT-5 family; exact deployment identifier was not exposed to this seat.
- **Harness:** Codex workspace session with persistent Node-backed local execution and web search.
- **Local reach:** direct pinned Git-object reads, hashing, targeted Git inspection, exact local path reads, and child-process Git/PowerShell execution.
- **Search reach:** general web search/open plus GitHub connector; official documentation, paper origins, and repository origins were reachable. Some publisher pages returned internal/403 errors and were not used as deciding evidence.
- **Execution reach:** deterministic JavaScript fixtures, an in-memory `o200k_base` tokenizer, seeded Monte Carlo sensitivity, metric arithmetic, public-event privilege construction, flat-ledger comparison, and cursor-only reconstruction.
- **Limitations:** no Python runtime, no installed tokenizer package, no in-app browser session, no direct outbound npm/Git network, no implemented MBCX harness, and no paid inference. No file was edited or verdict written to disk.