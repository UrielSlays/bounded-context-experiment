# NO-GO(treatment isolation is false)

**READ-ONLY design verdict, supported by an EXECUTED statistical adversary.**

Arm D receives deterministic typed state transitions, while Arm B makes the decision model parse, maintain, compact, and re-emit its own ledger. Arm B also has an arm-specific output field. Therefore D-versus-B changes writer quality and output burden as well as representation. A D win cannot support the preregistered causal claim that typed representation caused the improvement.

This revision should not proceed to implementation planning or paid inference. It is repairable through the **causal-identification / matched-baseline** fix class.

## Pin and byte verification

**EXECUTED — UNSEARCHED (SETTLED-BY-PINNED-BYTES).**

- Packet commit resolved exactly to `95c2b359afb59b1f4e1b096d402a3106c44da339`.
- Artifact commit resolved exactly to `5c7ccfe72d0aa84141f7296f185b9c022c6fe294`.
- Pinned artifact length: 36,869 bytes.
- Calculated SHA-384:

  `B1D907E2C7D6B247D109B5E192541442ED07B51EAFA18A28ADCFC418B72494FBCD588B55C0504D4F44ACB2F3333007CE`

  This exactly matches the packet.
- Current `HEAD` was `7b54f442c569bc80b2f38a779cfe82148fcb8d23`.
- The working-tree artifact and packet were byte-identical to their pins. I relied on the pinned Git objects.
- Every hash-bearing source in `LOCAL-SOURCE-MANIFEST-r1.md` matched its expected SHA-384.
- A final `git status --short` showed one unrelated untracked verdict file that appeared after an earlier clean check. I did not open or read it, and it played no part in this review. I issued no write/edit command.

Pinned-byte conflicts and winners:

- “Only treatment variable” at artifact line 106 loses to the specific arm mechanics at 114–141, 199–203, and 354–361. Those mechanics govern.
- “Forced process restarts” at line 34 loses to the concrete protocol at line 277: same foreground process. The actual construct is same-process serialization/reopen.
- “Approved architecture” at line 5 loses to lines 10 and 785–793, which require owner review and approval. The artifact is not approved.

## Build-decision challenge

### 1. ALREADY-BUILT?

**READ-ONLY — SEARCHED.**

No opened system answers the exact causal question, but most of the proposed harness already exists in pieces:

- PM-Bench already supplies the 80-step prospective-memory world, delayed/canceled/rescheduled obligations, hidden channels, lures, deterministic replay scoring, and a direct runner. Its paper reports the ledger as a strong low-noise scaffold, but does not isolate deterministic ledger versus deterministic typed projection. The repository exposed no root license file; direct `LICENSE` and `LICENSE.md` paths returned 404, so its definitions are adoptable as prior art but its code/data should not be copied without permission or clarified licensing. [PM-Bench paper](https://arxiv.org/html/2607.12385v1), [repository](https://github.com/genglinliu/PMBench).
- AgenticSTS supplies a bounded, typed, ablatable contract and explicitly leaves the matched accumulating-context comparison open. Its agent code is Apache-2.0, its mod AGPL-3.0, and its data CC-BY-4.0. [AgenticSTS repository](https://github.com/AlayaLab/AgenticSTS).
- τ-bench, OpenAI Evals, and Concordia already provide reusable simulation/evaluation runners, although none is as small as a direct two-arm runner for this question. [τ-bench](https://github.com/sierra-research/tau2-bench), [OpenAI Evals](https://github.com/openai/evals), [Concordia](https://github.com/google-deepmind/concordia).

Conclusion: build a small causal adapter/runner, not this five-arm experimental subsystem. Adopt PM-Bench’s public task/scorer concepts and mature storage/statistics primitives; do not rebuild a general memory platform.

### 2. PRODUCT-FIT?

**READ-ONLY — UNSEARCHED (NOT-LOAD-BEARING: product posture is owner-locked by the packet).**

Customer need, in one sentence:

> Moonwalker needs a cheap, auditable experiment that tells the owner whether bounded typed current state and obligations earn further engineering over a simple deterministic ledger under reconstruction.

That need fits **GOVERNED POWER / FAIL-LOUD / MIRROR-NOT-COP**: the win, kill, and inconclusive regions give the owner a knob. The present comparison does not fit that posture, because its writer confound can manufacture an authoritative-looking false positive.

### 3. BIGGER-THAN-THE-BUG?

**READ-ONLY — UNSEARCHED (SETTLED-BY-PINNED-BYTES).**

Yes. The artifact introduces nine modules, Inspect integration, SQLite projections, JSONL mirroring, a provider abstraction, PID ownership, child-process registries, signal handling, stale-lock recovery, and cleanup reporting (`:444–490`, `:552–623`) before the two-arm causal question is established.

It has correctly reached a design gate, but that gate should reject the current scope. Delete the general `safety`/child-process cleanup subsystem and preferably Inspect itself from the first decisive experiment.

## Evidence actually read

All paths below were read from their required pins or hash-verified local bytes:

- `MBCX-01-DESIGN-COUNCIL-PACKET-r1.md:1–195@95c2b359...`
- `MBCX-01-DESIGN-SPEC-r0.md:1–793@5c7ccfe...`
- `LOCAL-SOURCE-MANIFEST-r1.md:1–82@95c2b359...`
- `MOONWALKER-MEMORY-LAYER-EXPANSION-COMPOSABLE-SCOPED-MULTITIMESCALE-MEMORY-2026-08-10.md:1–217`, especially `:21–23,163–173`
- `DECISIVE-EXPERIMENT-PORTFOLIO-AXIOM-...md:1–597`, especially `:24–35,64–198,382–443,536–548`
- `CAPABILITY-NORMALIZED-EXPERIMENT-PROTOCOL-HELIOS-...R04.md:1–429`, especially `:25–46,247–257,325–341`
- `EXPERIMENTS-AND-FALSIFICATION-THRESHOLDS-CANTOR-...md:1–235`
- `research-notes/experimental-protocol.md:1–82`
- `VIRTUALIZED-MODULAR-MEMORY-RESEARCH-2026-08-09.md:21–62,189–245,526–745,875–981,1182–1446`
- `agent-degradation-taxonomy-and-llm-judge-reliability-2026-07-30.md:79–105,149–167,217–241,276–328`
- `<vault>`

The local portfolio explicitly requires fresh explicit current state, provider-native state/context, deterministic materialization, oracle-minimal and oracle-all-relevant baselines, counterbalanced order, scenario clustering, and true process-cold reconstruction. Those requirements are absent or narrowed in the reviewed artifact.

## Claim scoreboard

| Claim | Result | Mode/source label | Deciding evidence |
|---|---|---|---|
| C1 — smallest decisive test | **False** | READ-ONLY · SEARCHED | PM-Bench already owns most world/scorer mechanics; the exact gap needs a smaller factorial, not five arms plus lifecycle machinery. |
| C2 — treatment isolation | **False** | READ-ONLY · UNSEARCHED (SETTLED-BY-PINNED-BYTES) | `:106,114–141,199–203,354–361,404` change writer and output burden with representation. |
| C3 — baselines can kill the idea | **False** | READ-ONLY · SEARCHED | No deterministic compact ledger, fresh explicit-current-state arm, provider-native compaction, or oracle-all-relevant arm. |
| C4 — Inspect is neutral/workable | **False as specified** | READ-ONLY · SEARCHED | Message accumulation, default cache mutation, development-only checkpointing, and retry semantics require result-changing choices not in the spec. |
| C5 — OpenRouter sufficiently frozen | **False as specified** | READ-ONLY · SEARCHED | Strong routing controls exist, but cache state, exact wrapper behavior, endpoint identity, and arm schedule are not frozen or recorded. |
| C6 — statistics support verdict | **False** | EXECUTED · SEARCHED | Four-pilot variance can collapse to zero; CI construction is unspecified; 24–48 clamp can miss target power. |
| C7 — restart represented honestly | **False** | READ-ONLY · UNSEARCHED (SETTLED-BY-PINNED-BYTES) | `:18,34` say cold/process restart while `:277` says same foreground process. |
| C8 — generated world non-privileging | **Undetermined** | READ-ONLY · UNSEARCHED (COULD-NOT: no generator/test bytes exist) | Invariants are prose only; structured public fields may privilege D, and gold-derived rejection cannot yet be inspected. |
| C9 — burden proportionate | **False** | READ-ONLY · SEARCHED | Existing direct runners are smaller; `:463–490,552–623` recreate lifecycle/platform controls. |
| C10 — reproducibility complete | **False** | READ-ONLY · SEARCHED | `:627–648` omit arm order, cache state, Inspect/wrapper/tokenizer lock, endpoint block, and provider-time snapshot. |

## Findings

### P0 — Primary comparison is not causally identified

**READ-ONLY — UNSEARCHED (SETTLED-BY-PINNED-BYTES).**

- **Lines:** `:106,114–141,180–203,354–361,404`
- **Mechanism:** Arm B’s decision model must update and emit a ledger. Arm D receives deterministic structured events and a deterministically materialized projection. Only B spends output tokens and error probability on memory maintenance.
- **Consequence:** A persuasive D win may mean “perfect parser beats model writer,” “shorter action output beats action-plus-ledger,” or “structured schema beats prose extraction.” It cannot establish the claimed representation effect.
- **Fix class:** **CAUSAL-IDENTIFICATION / MATCHED-ADMISSION FACTORIAL.**
- **Required design correction:** Make the primary comparison deterministic flat ledger versus deterministic typed projection with identical admitted events, storage engine, packet budget, serializer burden, and action-only model output. Test writer choice separately as a second factor.

### P1 — The baseline set cannot fairly kill the kernel

**READ-ONLY — SEARCHED.**

- **Lines:** `:108–149,404–408`
- **Mechanism:** The “strong ledger” is specifically the confounded model-written ledger. The design omits deterministic compact current-state/obligation state, fresh explicit current state, provider-native compaction, and oracle-all-relevant.
- **Consequence:** D can win against a weakened ledger, while a useful D can also be killed by a bad single-model scaffold preference. PM-Bench found scaffold rankings model-dependent; AgenticSTS reports backbone sensitivity and calls the matched accumulating-context comparison open. [PM-Bench §4.2](https://arxiv.org/html/2607.12385v1), [AgenticSTS limitations/results](https://github.com/AlayaLab/AgenticSTS).
- **Fix class:** **BASELINE-COMPLETENESS / MODEL-NORMALIZATION.**

### P1 — Four-pilot sample sizing is demonstrably fragile

**EXECUTED — SEARCHED.**

- **Lines:** `:392–440`
- **Fresh adversarial input run against the pinned rule:** scenario difference \(X=0.4\) with probability 0.2, otherwise \(X=0\). This is bounded, has mean 0.08 and SD 0.16.
- **Executed result:**
  - Probability all four pilot differences are zero: **40.96%**.
  - In that event the observed pilot SD is zero and the spec clamps to **n=24**.
  - The same formula using the true SD gives **n=32**.
  - Under a conventional two-sided paired-t interval, exact binomial enumeration gave approximately **73.6%** rejection probability at n=24, below the promised 80%.
- **Additional defect:** The artifact never specifies the CI estimator whose exclusion of zero controls the win and kill rules.
- **External evidence:** Pilot-variance literature shows that treating pilot variance as known understates uncertainty; exact paired-permutation methods exist for structured metrics including F1. The clinical papers establish the uncertainty mechanism, not a universal minimum pilot size. [PLOS One sample-size study](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0262804), [Teare et al. simulation study](https://trialsjournal.biomedcentral.com/articles/10.1186/1745-6215-15-264), [exact paired-permutation paper](https://arxiv.org/abs/2205.01416).
- **Consequence:** The experiment can enter confirmation underpowered, then report an avoidably inconclusive or unstable result.
- **Fix class:** **STATISTICAL-PREREGISTRATION.** Use simulation-based power over plausible bounded/stratified scenario distributions, account for variance-estimate uncertainty, predeclare the CI/test, and do not impose a maximum n that silently defeats the target power.

### P1 — Inspect introduces unclosed hidden state and retry semantics

**READ-ONLY — SEARCHED.**

- **Lines:** `:448–459,515–525,527–540,667–680`
- **Mechanism:**
  - Inspect documents `TaskState.messages` as accumulated chat history and documents that `generate(state)` appends the assistant message. A custom solver must construct a fresh message sequence for every decision. [Inspect solvers](https://inspect.aisi.org.uk/solvers.html).
  - For `openrouter/anthropic/*`, Inspect currently enables prompt caching by default, injects `cache_control` immediately before OpenRouter, and does not include those markers in the `.eval` request snapshot. [Inspect providers](https://inspect.aisi.org.uk/providers.html).
  - Mid-sample checkpointing currently requires Inspect’s development version, custom-agent support, and does not save arbitrary process state or external effects. Checkpoint failures merely warn by default. [Inspect checkpointing](https://inspect.aisi.org.uk/checkpointing.html).
  - `eval-retry` preserves completed samples; one whole scenario is one sample. [Inspect logs](https://inspect.aisi.org.uk/eval-logs.html).
- **Consequence:** An implementation can silently retain conversation history, use warm prefix state, restart against dirty artifacts, or rerun a whole paid trajectory with ambiguous store identity.
- **Fix class:** **SUBSTRATE-CONFORMANCE / DEPENDENCY-PIN / ATOMIC-CELL-IDENTITY.**
- **Refusal condition:** No paid call until a mock-provider conformance artifact proves fresh messages, `cache_prompt=false`, raw request equivalence, strict checkpoint failure, and clean resume/rerun identity.

### P1 — “Cold restart” is a false label

**READ-ONLY — UNSEARCHED (SETTLED-BY-PINNED-BYTES).**

- **Lines:** `:18,34,258–277`
- **Mechanism:** The concrete protocol closes and reopens files while remaining inside the same process.
- **Consequence:** Module globals, singleton clients, tokenizer caches, open provider state, and accidentally retained objects can survive. The result measures serialization/reopen, not process-cold reconstruction.
- **Fix class:** **CONSTRUCT-VALIDITY / PROCESS-BOUNDARY.**
- **Required correction:** Either relabel it everywhere as in-process reconstruction or have a small supervisor spawn a fresh child for each post-boundary segment and pass only the persisted arm artifact plus public observation.

### P1 — Arm order and cache state can correlate with architecture

**READ-ONLY — SEARCHED.**

- **Lines:** `:438–440,515–525,627–648,683–689`
- **Mechanism:** The spec randomizes which cells receive replicates, but never commits or records arm execution order. OpenRouter’s default behavior is dynamic load balancing; Inspect eagerly schedules samples and may maintain prompt caches. [OpenRouter provider routing](https://openrouter.ai/docs/guides/routing/provider-selection), [Inspect parallelism](https://inspect.aisi.org.uk/parallelism.html).
- **Consequence:** Provider drift, rate limits, outages, time of day, or warm-cache state can line up with a particular arm and mimic an architectural effect.
- **Fix class:** **RANDOMIZATION/BLOCKING / REPRODUCIBILITY.** Commit a blocked, counterbalanced/interleaved arm schedule before calls and record cache reads/writes, cache mode, endpoint metadata, and wall-clock block.

### P2 — Generator validity and gold isolation remain unproved

**READ-ONLY — UNSEARCHED (COULD-NOT: generator bytes and fixtures do not exist).**

- **Lines:** `:157–178,211–254,654–665`
- **Mechanism:** The public envelope exposes `scope`, `event_kind`, handles, and timing fields that are directly aligned with D’s ontology. Rejection sampling uses private invariants, but no executable serializer-differential or taint test exists.
- **Consequence:** A generator designed around D’s schema can produce a benchmark on which D appears uniquely capable, even if the advantage disappears on ordinary observations.
- **Fix class:** **GENERATOR/ORACLE-VALIDITY.** Require held-out generator families, byte-level gold-taint canaries, serializer parity tests, and an independently generated challenge set before paid inference.

### P2 — Oracle-minimal is not necessarily a ceiling

**READ-ONLY — UNSEARCHED (SETTLED-BY-PINNED-BYTES).**

- **Lines:** `:143–145,408,730`
- **Mechanism:** The smallest logically sufficient packet may omit redundancy or cues a stochastic model needs. The local source portfolio explicitly distinguishes oracle-minimal from oracle-all-relevant.
- **Consequence:** Weak oracle-minimal performance can be misclassified as “reasoning failure,” unfairly killing a useful selection kernel.
- **Fix class:** **ORACLE-VALIDATION.** Include both oracle-minimal and oracle-all-relevant, and require exact gold-state equivalence before behavioral interpretation.

### P2 — Harness scope and run identity are oversized yet incomplete

**READ-ONLY — SEARCHED.**

- **Lines:** `:444–490,552–648`
- **Mechanism:** The design adds platform-like process governance but omits scientifically material identity fields: arm order, cache state, exact Inspect commit, package lock, tokenizer implementation/version, OpenRouter wrapper version, endpoint/quantization block, and provider metadata timestamp.
- **Consequence:** High implementation burden without corresponding rerun comparability.
- **Fix class:** **SCOPE REDUCTION / REPRODUCIBILITY MANIFEST.**
- **Delete:** `safety` child-PID registry, stale-lock recovery, cleanup report subsystem, and generalized temporary-cache cleanup from the first experiment.

The τ-bench project’s July 2026 grading fix made earlier and later results incomparable, demonstrating why exact task and harness versions are load-bearing. [τ-bench README/version notice](https://github.com/sierra-research/tau2-bench).

### P3 — Governance status and hashes are ambiguous

**READ-ONLY — UNSEARCHED (SETTLED-BY-PINNED-BYTES).**

- **Lines:** `:5,10,294,344,785–793`
- **Mechanism:** “Approved architecture” conflicts with awaiting review and owner decision. `payload_hash` and packet hash name no algorithm.
- **Consequence:** Approval scope can be misread; identical field names may later acquire incompatible hash semantics.
- **Fix class:** **GOVERNANCE-VOCABULARY / FORMAT-IDENTITY.**
- If disposable, declare hashes identity-only and non-normative. If promoted into Moonwalker-owned formats, bind SHA-384. Do not turn this into seal-chain work.

## WHAT WOULD YOU BUILD?

**READ-ONLY — SEARCHED.**

I would build the recommended first option below.

1. **Direct two-arm causal runner — recommended.** Clean-room adaptation of PM-Bench’s public scenario and deterministic-scoring concepts, with no copied PM-Bench code until licensing is resolved.

2. **PM-Bench adapter.** Cheapest if the repository receives an explicit compatible license; still requires new matched adapters and counterbalanced execution.

3. **Inspect-backed runner.** Acceptable only after a no-cost conformance spike proves message reset, cache disabling, exact request capture, strict checkpointing, and atomic retry semantics. Otherwise Inspect adds more state than it removes.

The minimum mechanism:

- One deterministic generator produces separately stored public events and private gold.
- Both primary arms consume the same canonical admitted events:
  - deterministic flat current-state/obligation ledger;
  - deterministic typed projection.
- Both use the same storage technology, tokenizer, packet budget, common serializer envelope, and action-only model output.
- Writer choice becomes a later factorial: deterministic writer versus model writer crossed with flat versus typed representation.
- Calibration baselines: no memory, full history when it fits, fresh explicit current state, and oracle-minimal plus oracle-all-relevant. Add BM25 or provider-native compaction only after the primary causal contrast is sound.
- A direct async HTTP client sends one request at a time, with a committed counterbalanced arm schedule, `cache_prompt=false`, one allowed provider/endpoint, fallbacks disabled, parameter enforcement, transforms disabled, and raw request/response plus router metadata retained.
- A tiny parent supervisor starts a fresh child at a restart boundary. The child receives only the persisted arm artifact and current public observation.
- Scenario is the paired unit. The analysis and power simulation are frozen before calls, including the CI/test and precision rule.
- One SQLite file per cell is sufficient. No general memory service, Inspect lifecycle layer, PID registry, sandbox, background viewer, or production cleanup engine.

Prior art taken: PM-Bench’s prospective task/scorer structure, AgenticSTS’s bounded typed contract, τ-bench’s versioned simulation lesson, and exact paired evaluation methods—all **SEARCHED** this session.

## WOULD YOU DESIGN IT DIFFERENTLY?

**READ-ONLY — SEARCHED.**

Yes. I would use a staged factorial rather than the current five-arm monolith:

1. Deterministic flat ledger versus deterministic typed projection.
2. Only if representation survives, cross writer type with representation.
3. Only then add retrieval, provider-native compaction, and a second model family.
4. Only after that test natural-language admission and external benchmarks.

This is scientifically cleaner because each stage changes one causal factor; cheaper because a negative first stage kills the project before most paid cells; and more executable because it avoids Inspect’s hidden state.

Direct answers to the packet’s two implementation questions:

- **Is the artifact implementable without filling gaps that could change the result? No.** Message reset, caching, checkpoint version, retry identity, arm order, CI method, endpoint identity, and gold-isolation mechanics are unstated.
- **Does it presently test the real architectural claim? No.** It primarily confounds representation with parsing/write quality and output burden.

## Required omission attack

- **Omitted prior-art comparator — READ-ONLY · SEARCHED:** a separate structured memory/intervention agent, as in *Remember When It Matters*, which selectively injects reminders and reports gains on Terminal-Bench and τ²-Bench. It costs extra model compute, so it belongs in a capability-normalized secondary panel, not the primary arm. [Paper](https://arxiv.org/abs/2607.08716).
- **Unmeasured confound — READ-ONLY · SEARCHED:** arm order × provider time/cache/backend drift.
- **Silent implementation footgun — READ-ONLY · SEARCHED:** Inspect appends `TaskState.messages` and injects cache markers not visible in the `.eval` request snapshot.
- **Machinery to delete — READ-ONLY · UNSEARCHED (SETTLED-BY-PINNED-BYTES):** generalized child-PID ownership, stale-lock recovery, cleanup-report subsystem, and preferably Inspect for stage one.
- **Missing pre-paid artifact/test — READ-ONLY · SEARCHED:** a substrate-conformance transcript from a mock provider proving fresh per-decision messages, cache disabled, raw request bytes, strict checkpoint failure, and atomic resume/rerun identity.
- **Persuasive false positive — READ-ONLY · UNSEARCHED (SETTLED-BY-PINNED-BYTES):** D wins because its writer is deterministic and B’s writer is the decision model, then the report attributes the gain to typed representation.
- **Unfair kill — READ-ONLY · SEARCHED:** Gate 3 kills on one model family, while Gate 4 tests another family only if Gate 3 survives. PM-Bench and AgenticSTS both show scaffold/backbone interaction, so the kernel could be useful on another deployment-relevant model and never receive that test.

## Sweep log

### Prospective memory, state tracking, and prior art

Exact queries:

- `PM-Bench Evaluating Prospective Memory in LLM Agents official paper code GitHub license`
- `AgenticSTS bounded memory testbed official paper GitHub license accumulating context`
- `prospective memory LLM agents benchmark delayed intentions action timing cancellations reschedules benchmark`
- `memory grounded tool use agent benchmark obligations state tracking long horizon official paper`
- `"Remember When It Matters" proactive memory agent official GitHub Terminal-Bench tau2`
- `MAGE hierarchical execution state tree MemoryArena official paper code 2026`
- `LongMemEval-V2 official GitHub memory experienced colleagues benchmark`
- `CAME-Bench context-aware agent memory event state tracking official code`
- `site:arxiv.org/abs/2607.08716 "Remember When It Matters" proactive memory agent`
- `site:arxiv.org/abs/2606.06090 MAGE hierarchical execution state tree MemoryArena`
- `site:arxiv.org/abs/2601.10702 CAME-Bench context-aware agent memory`
- `site:github.com/xiaowu0162/LongMemEval-V2 benchmark`

Opened:

- [PM-Bench paper](https://arxiv.org/html/2607.12385v1): §§3.1–3.3, 4.1–4.2 and task/scoring tables.
- [PM-Bench repository](https://github.com/genglinliu/PMBench): root tree and README; root license paths absent.
- [AgenticSTS repository](https://github.com/AlayaLab/AgenticSTS): bounded contract, matched-context limitation, operational caveats, licensing.
- [AgenticSTS project](https://alayalab.github.io/AgenticSTS/).
- [Mem2ActBench](https://aclanthology.org/2026.acl-long.370/): abstract and benchmark scope.
- [LongMemEval-V2](https://github.com/xiaowu0162/LongMemEval-V2): overview, memory backends, harness, Apache-2.0 license.
- [Remember When It Matters](https://arxiv.org/abs/2607.08716): introduction, method, results, calibration failure.
- [MAGE](https://arxiv.org/abs/2606.06090): execution-state tree and MemoryArena results.
- [CAME-Bench/STITCH](https://arxiv.org/abs/2601.10702): contextual-intent schema, synthetic generation, error analysis.

Changed/confirmed: PM-Bench makes a generic new world/scorer unnecessary; AgenticSTS confirms the exact matched comparison is still open; newer work adds intervention, execution-tree, and intent-index comparators but does not supply the required deterministic writer×representation factorial.

Stopped because these primary project/paper origins covered prospective action timing, typed bounded state, contextual retrieval, execution state, tool use, and experienced-colleague memory, while converging on the remaining narrow gap.

### Inspect behavior and footguns

Exact queries:

- `site:inspect.aisi.org.uk custom solver TaskState messages generate appends messages Inspect AI`
- `site:inspect.aisi.org.uk OpenRouter cache_prompt cache_control Anthropic request snapshot`
- `site:inspect.aisi.org.uk eval-retry completed samples resume checkpoint custom solver`
- `site:inspect.aisi.org.uk eval logs concurrency parallelism max_connections checkpoint`

Opened:

- [Solvers](https://inspect.aisi.org.uk/solvers.html): TaskState and custom-solvers sections.
- [Providers](https://inspect.aisi.org.uk/providers.html): OpenRouter and prompt-caching sections.
- [Checkpointing](https://inspect.aisi.org.uk/checkpointing.html): status, saved state, custom agents, failure policy, limitations.
- [Eval logs](https://inspect.aisi.org.uk/eval-logs.html): retry and sample-preservation sections.
- [Parallelism](https://inspect.aisi.org.uk/parallelism.html): eager scheduling and resource limits.
- [Model concurrency](https://inspect.aisi.org.uk/models-concurrency.html): connection and adaptive behavior.

Changed/confirmed: Inspect can host the experiment, but current checkpointing is development-version functionality and none of message reset, cache disabling, or resume semantics is free.

Stopped because the official current documentation directly governs present Inspect behavior. Its current-version status is applicable only after the artifact pins an Inspect commit/version.

### OpenRouter routing and transformations

Exact queries:

- `site:openrouter.ai/docs provider routing order allow_fallbacks require_parameters official`
- `site:openrouter.ai/docs transforms middle-out compression plugins official OpenRouter`
- `site:openrouter.ai/docs response provider metadata model provider generation id official`
- `site:openrouter.ai/docs models supported parameters tokenizer context length provider metadata`

Opened:

- [Provider selection](https://openrouter.ai/docs/guides/routing/provider-selection): defaults, order/only, endpoint targeting, fallbacks, parameter enforcement.
- [Message transforms](https://openrouter.ai/docs/guides/features/message-transforms): middle-out/context compression and disabling it.
- [Router metadata](https://openrouter.ai/docs/guides/features/router-metadata): attempts and pipeline stages.
- [Model metadata](https://openrouter.ai/docs/guides/overview/models): canonical slugs and endpoint metadata.
- [Generation metadata](https://openrouter.ai/docs/api/api-reference/generations/get-request-&-usage-metadata-for-a-generation): returned provider/request usage fields.

Changed/confirmed: the artifact’s routing controls are mostly real, but they do not freeze hidden weights or provider drift and do not close Inspect’s caching layer or missing run order.

Stopped because the official vendor documentation settled all requested routing fields. No claim was made that OpenRouter exposes an immutable checkpoint.

### Statistics and pilot sizing

Exact queries:

- `pilot study four subjects standard deviation sample size estimation uncertainty primary paper confidence interval`
- `sample size re-estimation pilot standard deviation uncertainty n=4 paired continuous outcome paper`
- `bounded outcome paired mean confidence interval cluster bootstrap few clusters primary paper`
- `paired bounded outcomes F1 score statistical test permutation bootstrap scenario clusters sample size`
- `paired bounded outcome bootstrap confidence interval primary paper scenario clusters`
- `paired permutation test exact confidence interval primary paper randomized paired data`
- `pilot variance sample size estimation four pilot subjects uncertainty primary study`

Opened:

- [Sample size determination with a pilot study](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0262804): standard method, variance uncertainty, small-sample behavior.
- [Teare et al.](https://trialsjournal.biomedcentral.com/articles/10.1186/1745-6215-15-264): simulation results and conclusion on imprecise small-pilot variance.
- [Exact Paired-Permutation Testing](https://arxiv.org/abs/2205.01416): paired design, distribution-free test, structured F1 extension.
- [BMJ pilot tutorial](https://www.bmj.com/content/390/bmj-2024-083405): variance uncertainty and upper-confidence/sample-inflation approaches.

Changed/confirmed: four pilot scenarios are not defensible as if the SD were known. I did not transplant clinical sample-size numbers; the executed bounded adversary directly established the failure for this formula.

Stopped after primary methodological sources plus the fresh enumeration agreed on the load-bearing mechanism.

### Alternative harnesses and versioning footguns

Exact queries:

- `official agent evaluation framework stateful multi turn trajectories open source GitHub license eval runner`
- `OpenAI Evals GitHub custom eval framework license official`
- `DeepMind Concordia benchmark framework agent evaluation environment GitHub license`
- `tau bench official GitHub agent benchmark environment evaluation runner license`

Opened:

- [OpenAI Evals](https://github.com/openai/evals): custom eval framework and MIT license.
- [τ-bench](https://github.com/sierra-research/tau2-bench): simulation runner, MIT license, task schemas, July 2026 comparability warning.
- [Concordia](https://github.com/google-deepmind/concordia): simulation engine/components and Apache-2.0 license.

Changed/confirmed: mature runners exist, but they are not automatically smaller than a direct loop. τ-bench’s task-fix incident materially strengthened the requirement to pin task and harness bytes.

Stopped after three distinct primary implementations covered generic eval registry, tool-agent simulator, and generative simulation engine.

### Regulatory/standards scope

**UNSEARCHED (NOT-LOAD-BEARING: the artifact makes no legal, regulatory, cryptographic-standard, or jurisdictional claim).** SHA-384 here is a Moonwalker format-posture choice, not a claim about a mandated standard.

## Residual risks and explicit non-claims

- No generator, adapter, scorer, or production counterpart exists to execute differentially. The generator-validity finding remains **READ-ONLY/UNDERDETERMINED**.
- No paid inference was run.
- Even a repaired result would not prove general memory, open-world sufficiency, personality, emotion, procedural learning, multi-agent sharing, or brain slotting.
- Deterministic admission would not prove the natural-language write path.
- In-process reopen would not prove crash recovery; even subprocess reconstruction would not prove host/OS crash durability.
- A bounded packet would not prove bounded total admission, retrieval, or maintenance work.
- OpenRouter metadata cannot prove an immutable hidden checkpoint or deterministic output.
- One or two model-family results would remain conditional on those model/provider/runtime blocks.
- Closed-world synthetic generators can overfit their ontology even with no literal gold leak.
- Oracle-minimal may not be a behavioral ceiling.
- PM-Bench code/data reuse remains blocked on license clarification.
- The design assumes no hostile actor; none of this is a security evaluation.
- Hash fields are identity mechanisms unless explicitly elevated; they are not seals or provenance chains.

## Fix classes

The required classes, without leaf patches, are:

1. **CAUSAL-IDENTIFICATION / MATCHED-ADMISSION FACTORIAL** — deciding P0.
2. **BASELINE-COMPLETENESS / MODEL-NORMALIZATION.**
3. **STATISTICAL-PREREGISTRATION.**
4. **SUBSTRATE-CONFORMANCE / DEPENDENCY-PIN / ATOMIC-CELL-IDENTITY.**
5. **CONSTRUCT-VALIDITY / PROCESS-BOUNDARY.**
6. **RANDOMIZATION/BLOCKING / REPRODUCIBILITY.**
7. **GENERATOR/ORACLE-VALIDITY.**
8. **SCOPE REDUCTION.**
9. **GOVERNANCE-VOCABULARY / FORMAT-IDENTITY.**

## Seat capability report

- **Model:** Codex, GPT-5 family; exact served runtime identifier unavailable.
- **Harness:** read-only API session using pinned Git-object reads, SHA-384 computation, transient JavaScript enumeration, and independent web search.
- **Reach:** all mapped local sources, arbitrary Git-object inspection, current primary vendor documentation, papers, and public repositories.
- **Limitations:** the native shell launcher failed twice with `CreateProcessWithLogonW failed: 2`; a read-only Node/Git fallback provided complete local inspection and execution. No implementation existed to run. No other council seat or verdict was consulted or read.
- **Authority:** no file was created, edited, deleted, committed, pushed, labeled, or merged.