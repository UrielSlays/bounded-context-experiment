# MBCX-01 prior-art sweep — FULL REPORT (verbatim, 2026-08-16)

> Committed on the owner's direct order ("I want this bot's full report committed to the repo
> docs for further research, links etc."). This is the research agent's report VERBATIM as
> returned to the driver 2026-08-16; the driver added only this header block. The condensed
> lane-root memo (`MBCX-01-NOVELTY-SWEEP-MEMO-2026-08-16.md`) now points here as its verbatim
> source. Research input, not experimental evidence; preprint peer-review status per the
> provenance caution in section (d).

---

# MBCX-01 prior-art sweep memo — "Did someone already do it, and to this precision?"

**Date:** 2026-08-16
**Sweep type:** external literature, open sources, opened at origin
**Status:** research input. Not experimental evidence. No paid model calls performed. Nothing in this memo authorizes BUILD or a run.
**Scope note:** this memo covers the *external* literature. The lane's mechanism-level prior art (Windows Job Objects, ETW `TRACE_QUERY_INFO_CLASS`, SLSA, AWS/Stripe idempotency, NIST binomial plans, Manski partial identification, Chugg/Ramdas, PostgreSQL temporal constraints, Jensen/Snodgrass bitemporality) is already recorded in `MBCX-01-R10-PRIOR-ART-MEMO.md`, `MBCX-01-R11-PRIOR-ART-MEMO.md`, `MBCX-01-R12-PRIOR-ART-AND-SHELF-MEMO.md`, and `MBCX-01-R13-PRIOR-ART-AND-ENVIRONMENT-ADDENDUM.md`, and is **not re-derived here**. What those memos did **not** cover — and what this sweep targeted — is the agent/LLM-memory evaluation literature, the LLM-evaluation statistics literature, and the performance-evaluation-rigor literature.

---

## 0. The composition being tested against

MBCX-01 (read at the byte this session: `MBCX-01-EXPERIMENT-DESIGN-r9.md`, `MBCX-01-R10-ARCHITECTURE-SPEC.md`, `MBCX-01-R13-CLOSURE-ARCHITECTURE.md`) composes six things at once. Every "lacks" statement below is measured against these six and nothing else.

| Axis | MBCX-01's specific form |
|---|---|
| **A. Exactness gate** | Success predicate is conjunctive `A0 AND B AND A1` over schema-validated, identity- and hash-linked artifacts. Schema-invalid model output is *observed failure*, not missingness. No graded credit, no judge. |
| **B. Physical boundedness** | Retired instructions via Windows ETW PMC, per grid cell, over 100 frozen `(H,D,F)` cells (`H ∈ {128, 1024, 10000, 100000}`, `D,F ∈ {1,4,16,64,256}`), with a preregistered max-minus-min tolerance of **500,000 retired instructions** across the H range at fixed `(D,F)`, plus five further absolute axes (CPU ns, elapsed ns, peak committed bytes, I/O bytes, I/O ops), inside a non-breakaway Job Object with signed process-tree evidence. |
| **C. Preregistration** | Whole instrument frozen at a pinned Git commit with a hashed manifest; one terminal scientific look at `n=768`; explicit deliberate non-claims; "more calls" ruled out as an escape. |
| **D. Non-inferiority** | Margin `-0.10` on the BC−OM delta, OM floor `0.80`, **family error 0.05 across two streams**, with an exact dynamic-programming missingness hull enumerating every legal completion and reporting a substantive branch only if every completion yields it. |
| **E. Cryptographic reconstruction** | Subjects reconstructed as `commit:path` via `git cat-file`, SHA-384 + raw byte + LF/line-count verification **before import**; Merkle-style SHA-384 root over all 768 ordered candidate hashes; signer/trust-root separation. |
| **F. Bitemporal obligation semantics** | Three-coordinate cut (journal seq, knowledge time, valid time); visibility and effectivity as separate executable predicates; obligations/handoffs bind cut hash, catalog hash, snapshot hash, deterministic action ID. |

One honest framing caveat before anything else: **MBCX-01 has executed nothing.** It is a preregistration-stage design with zero paid calls, an unimplemented physical harness, and explicit `STATE_AUTHORITY_UNAVAILABLE` / `PHYSICAL_HARNESS_UNAVAILABLE` statuses. Every work below has actually run. The comparison in this memo is therefore *design composition vs. executed work*, and that asymmetry cuts against MBCX-01, not for it.

---

## (a) The closest works

All fifteen were **SEARCHED** — opened at origin this session via the URL given. Where the abstract page was insufficient I additionally opened the full-text HTML, noted inline.

---

### Lane 1 — Agent/LLM memory systems and their evaluations

**1. PM-Bench: Evaluating Prospective Memory in LLM Agents** — SEARCHED
Genglin Liu, Saadia Gabriel. arXiv:2607.12385, submitted 2026-07-14.
https://arxiv.org/abs/2607.12385 (abs) · https://arxiv.org/html/2607.12385v1 (full text)

*What it is:* A Virtual-Week-derived benchmark asking whether an agent executes a deferred intention at the right future cue or state while other activity is ongoing, over a seven-day schedule with event-based and time-based tasks, cross-day obligations, rescheduling, cancellations, and hidden state channels requiring active monitoring.

*Shares with MBCX-01:* This is the closest published work on the *subject matter* — due obligations that must survive across time and be discharged at the correct moment. Its scoring is **programmatic, not judged**: `Set-F1 = 2TP/(2TP+FP+FN)` accumulated over all steps against the canonical due-set, with true positives being correctly selected due actions, false positives selected-but-not-due, false negatives missed-due. Scenarios are validated by a solver policy and accepted only if every non-cancelled task can be completed on time. Best result reported is 65.1% F1 (GPT-5.4) across eight models × eight configurations.

*Lacks vs MBCX-01:*
- **Exactness gate:** graded, not conjunctive. Set-F1 awards partial credit for a partially-correct due set; MBCX-01's `A0 AND B AND A1` awards none. A step that discharges three of four due obligations scores 0.857 in PM-Bench and 0 in MBCX-01.
- **Physical measurement:** none. The full text reports no tokens, latency, FLOPs, CPU, or memory. It counts state *queries* (monitoring frequency), which is an information-access count, not a work measurement.
- **Preregistration:** none stated. No power analysis, no sample-size justification, no confidence intervals, no significance test. Results are point estimates over 64 runs.
- **Non-inferiority:** no bounded-vs-oracle contrast. The hidden-channel design tests *whether* an agent queries, not whether a bounded carrier matches an oracle-memory carrier.
- **Cryptographic pinning:** not stated.

**2. LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory** — SEARCHED
Di Wu, Hongwei Wang, Wenhao Yu, Yuwei Zhang, Kai-Wei Chang, Dong Yu. arXiv:2410.10813 (v1 2024-10-14, v2 2025-03-04), ICLR 2025.
https://arxiv.org/abs/2410.10813 (abs) · https://arxiv.org/html/2410.10813v2 (full text)

*What it is:* 500 curated questions over freely scalable chat histories, targeting information extraction, multi-session reasoning, temporal reasoning, knowledge updates, and abstention.

*Shares with MBCX-01:* Knowledge-update and temporal-reasoning categories probe the same failure mode MBCX-01's bitemporal cut is built to prevent — an assistant answering from a superseded fact. Its three-stage indexing/retrieval/reading decomposition is the same seam MBCX-01 splits into selector-vs-gold-read-set.

*Lacks vs MBCX-01:*
- **Exactness gate:** LLM-judged. Verbatim from the full text: *"LongMemEval employs a LLM to assess response quality. Specifically, we prompt-engineer the gpt-4o-2024-08-06 model via the OpenAI API,"* with *"more than 97% agreement with human experts."* 97% agreement is not exactness; it is a 3% judge error floor sitting under every reported number.
- **Physical measurement:** none. The only effort figure in the paper is human annotation labor (*"approximately 400 human hours... and 150 hours"*), not system work.
- **Preregistration / non-inferiority:** none. No confidence intervals, no significance tests, no multiple-comparison correction. Raw accuracy percentages only.
- **Cryptographic pinning:** not stated.

**3. Evaluating Very Long-Term Conversational Memory of LLM Agents (LoCoMo)** — SEARCHED
Adyasha Maharana, Dong-Ho Lee, Sergey Tulyakov, Mohit Bansal, Francesco Barbieri, Yuwei Fang. arXiv:2402.17753, 2024-02-27.
https://arxiv.org/abs/2402.17753

*What it is:* Conversations averaging 300 turns / 9K tokens over up to 35 sessions, generated by a machine-human pipeline grounded on personas and temporal event graphs, with QA, event summarization, and multimodal dialogue tasks.

*Shares with MBCX-01:* The temporal-event-graph grounding is a generator-side ancestor of MBCX-01's pinned scenario generator; both derive a gold answer set from a structure rather than from annotator judgment.

*Lacks vs MBCX-01:* the abs page did not state the scoring method, cost measurement, or statistical treatment, and I did not open the full text. **Recorded as: not established at origin this session.** I am not asserting absence for this work on those three axes. What I can state: nothing on the abs page indicates preregistration, non-inferiority framing, or physical-work measurement.

**4. MemGPT: Towards LLMs as Operating Systems** — SEARCHED
Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, Joseph E. Gonzalez. arXiv:2310.08560 (v1 2023-10-12, v2 2024-02-12). Now the Letta lineage.
https://arxiv.org/abs/2310.08560

*What it is:* Virtual context management — a tiered core/recall/archival memory where the agent pages information into and out of a bounded context window via tool calls and interrupts.

*Shares with MBCX-01:* This is the direct architectural ancestor of the "bounded carrier" idea. MBCX-01's FD/FC/TN carriers are all instances of the same wager MemGPT makes — that a bounded, self-selected in-context working set can substitute for unbounded history.

*Lacks vs MBCX-01:*
- **Physical boundedness:** MemGPT bounds the *context window* (a token budget), which is an input-size bound, not a work bound. It makes no claim and takes no measurement about the CPU work required to *produce* that bounded context from a growing history. MBCX-01's entire physical gate is about exactly that second quantity.
- **Exactness gate, preregistration, non-inferiority:** the abs page states two evaluation domains (document analysis, multi-session chat) but no metric definitions, no statistical framing, and no cost accounting. I did not open the full text; **recorded as not established at origin** rather than absent.

**5. Zep: A Temporal Knowledge Graph Architecture for Agent Memory** — SEARCHED
Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, Daniel Chalef. arXiv:2501.13956, 2025-01-20. (Graphiti is the open-source engine.)
https://arxiv.org/abs/2501.13956 (abs) · https://arxiv.org/html/2501.13956v1 (full text)

*What it is:* A temporally-aware knowledge-graph memory engine with an episode subgraph of raw events and a fact layer carrying four timestamps.

*Shares with MBCX-01 — this is the genuine bitemporal overlap.* Verbatim from the full text: *"t′created and t′expired ∈ T′ monitor when facts are created or invalidated in the system, while tvalid and tinvalid ∈ T track the temporal range during which facts held true."* T′ is transaction/ingestion order; T is chronological event order. That is the same valid-time/knowledge-time separation MBCX-01 builds its cut on, applied to agent memory, published January 2025. Zep also invalidates rather than deletes superseded facts — MBCX-01's retraction-exclusion rule. And Zep reports a bounded-vs-full-context contrast with a cost number: **2.58 s vs 28.9 s latency on LongMemEval with gpt-4o**, ~90% latency reduction.

*Lacks vs MBCX-01:*
- **Third coordinate:** Zep is bi-temporal (two timelines). MBCX-01 cuts on **three** coordinates — journal sequence, knowledge time, valid time — and separates *visibility* (`journal_seq ≤ C.journal_seq AND observed_at ≤ C.knowledge_time`) from *effectivity* (`valid_from ≤ C.valid_time AND (valid_to IS NULL OR C.valid_time < valid_to)`) as two independently executable predicates. Zep's fact model does not carry a journal-sequence coordinate as a separate cut dimension.
- **Exactness gate:** LLM-judged on both benchmarks. Verbatim: DMR — *"An LLM judge compared the agent's responses to the provided golden answers"*; LongMemEval — *"we employed GPT-4o with the question-specific prompts provided in [7]."*
- **Physical measurement:** latency in seconds, wall-clock, on unstated hardware under unstated contention. Not retired instructions, not per-cell, no tolerance, no counter-capability check, no process-tree containment, no signed receipt. Latency conflates provider queue time with local work; MBCX-01's instruction count deliberately does not.
- **Preregistration / non-inferiority:** none. Point estimates, no confidence intervals, no significance testing, no equivalence margin. The 94.8% vs 93.4% DMR result is reported as a difference with no uncertainty attached to it.
- **Boundedness claim:** Zep demonstrates a *faster* result on the benchmarks it ran. It does not claim, and does not test, that per-operation work stays bounded as history scales — no H-range grid, no max-minus-min tolerance.

**6. Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory** — SEARCHED
Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, Deshraj Yadav. arXiv:2504.19413, 2025-04-28.
https://arxiv.org/abs/2504.19413

*What it is:* A memory-centric architecture that extracts, consolidates, and retrieves salient information from ongoing conversations, with a graph-memory variant.

*Shares with MBCX-01:* This is the closest published work on the **bounded-carrier-vs-full-context comparison** as an *engineering* proposition. It runs the exact contrast shape — bounded memory vs full-context baseline — and reports both quality and cost: *"91% lower p95 latency"* and *"saves more than 90% token cost,"* with six baseline families including full-context. p95 rather than mean is a real rigor choice.

*Lacks vs MBCX-01:*
- **Exactness gate:** the headline is explicitly an LLM-as-a-Judge metric (*"26% relative improvements in the LLM-as-a-Judge metric over OpenAI"*). The dependent variable is a judge score, not a conjunctive artifact-identity predicate.
- **Physical measurement:** tokens and p95 latency. Tokens are a *provider billing* proxy and latency is a wall-clock proxy; neither isolates the local work of maintaining the carrier from provider-side variance. No instruction counts, no CPU accounting, no process-tree containment, no per-cell grid, no preregistered tolerance.
- **Non-inferiority:** the framing is *superiority* ("outperform all existing memory systems"), which is the opposite hypothesis shape. MBCX-01's question is whether BC is **not materially worse** than OM — a claim superiority testing cannot make, because failing to reject a difference is not evidence of equivalence.
- **Preregistration:** none stated. No statistical significance testing, no confidence intervals.
- **Bounded-work claim:** cost reduction on the benchmark ran is demonstrated; boundedness across a history-scale range is not claimed or tested.

**7. Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions (MemoryAgentBench)** — SEARCHED
Yuanzhe Hu, Yu Wang, Julian McAuley. arXiv:2507.05257.
https://arxiv.org/abs/2507.05257

*What it is:* A benchmark decomposing memory into four competencies — accurate retrieval, test-time learning, long-range understanding, selective forgetting — delivered as multi-turn incremental interaction rather than a static long context.

*Shares with MBCX-01:* the incremental/streaming delivery model is the same premise as MBCX-01's append-only journal: state arrives over time and the carrier must survive the arrival, not be handed a finished transcript. "Conflict resolution / selective forgetting" is the same territory as MBCX-01's retraction and knowledge-update semantics.

*Lacks vs MBCX-01:* scoring method, cost measurement, statistical treatment, and baseline structure were **not established at origin** — the abs page does not state them and I did not open the full text. Not asserted absent. Nothing on the abs page indicates preregistration or physical-work measurement.

**8. STATE-Bench (Microsoft, open-source)** — SEARCHED
Microsoft Open Source Blog, 2026-05-19. Repo: `github.com/microsoft/STATE-Bench`.
https://opensource.microsoft.com/blog/2026/05/19/introducing-state-bench-a-benchmark-for-ai-agent-memory/

*What it is:* A benchmark asking whether agents improve with experience on realistic enterprise tasks, with a bring-your-own-memory interface.

*Shares with MBCX-01:* it is the only work in this sweep that runs a **deterministic environment-state scorer** alongside a judge — *"For state-mutating tasks, a deterministic scorer compares the final environment state to ground truth."* That is structurally MBCX-01's writer-receipt/poststate replay. It also reports a reliability metric with a conjunctive flavor — **Pass^5**, the percentage of tasks succeeding on *all five* runs — and measures efficiency as turns, unnecessary tool calls, and all input/output/retrieval tokens.

*Lacks vs MBCX-01:*
- **Exactness gate:** mixed, not uniform. Procedural and informational tasks use *"an LLM judge evaluates whether the agent followed the expected process"* and the user-experience dimension is a 1–5 LLM rubric. The deterministic scorer covers only the state-mutating subset, so the headline is a blend of exact and judged components.
- **Physical measurement:** tokens and tool-call counts. No CPU, no instructions, no hardware counters, no containment.
- **Preregistration / non-inferiority:** neither mentioned in the announcement. Baseline is "GPT-5.1 without memory" — a no-memory floor, not an oracle-memory ceiling, so the contrast is memory-vs-nothing rather than bounded-vs-oracle.

**9. Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers** — SEARCHED
Pengfei Du. arXiv:2603.07670, 2026-03-08.
https://arxiv.org/abs/2603.07670 (abs) · https://arxiv.org/html/2603.07670v1 (full text)

*What it is:* A survey of agent memory covering 2022 through early 2026 — write/manage/read loop, a three-dimensional taxonomy, five mechanism families, and four recent benchmarks.

*Shares with MBCX-01 — this is the memo's most useful bounding source, not a competitor.* It is a field-scope read of exactly the literature MBCX-01 sits next to, and its own diagnosis matches the gap MBCX-01 targets. Verbatim from §5.5: *"Evaluation must include cost. A memory system that achieves 5% higher accuracy but triples latency and storage cost may not be an improvement,"* followed by: **"None of the current benchmarks systematically report efficiency metrics alongside effectiveness."**

*What the survey does not contain (as read this session):* no mention of preregistration, non-inferiority, or formal statistical testing; no mention of bitemporal modeling or formal exactness/continuity guarantees. §7.3 handles "temporal versioning" pragmatically rather than formally. This is one author's survey and its coverage is its own claim, not a proof of absence — but it is independent testimony from inside the field that the cost axis is systematically unreported.

---

### Lane 2 — The statistics: preregistration and non-inferiority in model evaluation

**10. Progressive Disclosure for LLM-Maintained Wiki Knowledge Bases: a Preregistered Ablation** — SEARCHED
Theodore O. Cochran. arXiv:2607.04576, 2026-07-06.
https://arxiv.org/abs/2607.04576 (abs) · https://arxiv.org/html/2607.04576v1 (full text)

**This is the single closest work in the sweep on statistical composition, and it should be credited plainly.** It is the only work found that puts preregistration, a non-inferiority margin, a frozen byte-identical corpus, and cost measurement into one design.

*What it did, at origin:*
- Preregistered on OSF (`https://osf.io/feka7`, DOI 10.17605/OSF.IO/FEKA7), with the plan *"frozen at git tag `exp/prereg-v1`"* before confirmatory runs.
- Corpus frozen as immutable annotated git tags (`exp/corpus-2026-07-03`, `exp/arm-a1-recent`, `exp/arm-a2-summaries`, `exp/arm-a3-retrieval`), with a content-parity gate verifying *"all 709 content-page bodies are byte-identical across arms."*
- Non-inferiority margin δ = 0.5 on an 0–8 composite quality scale, declared if the upper bound of the 95% CI for (A0 − A3) is below 0.5; linear mixed-effects model `composite ~ arm + condition + (1 | question)`; bootstrap CIs, B=5000.
- 960 runs (40 questions × 4 arms × 3 conditions × 2 replicates); replicate count preregistered.
- Cost measured three ways: provider-reported `total_cost_usd`, logical context tokens, and a "new-token burden" excluding cache reads.
- Result: *"Quality is non-inferior (the retrieval arm matches the index baseline within the preregistered margin)... while cost falls in every regime, from about a third for a self-routing agent to well over half."*

*Lacks vs MBCX-01:*
- **Exactness gate:** the dependent variable is an **LLM judge** (OpenAI gpt-5) scoring four rubric dimensions 0–2 for a 0–8 composite. Blinded and randomized, which is good practice — but the paper's own human audit of a stratified 15% subsample (144 runs) returned **Cohen's κ = 0.23, below its own preregistered 0.60 threshold.** By its own preregistered criterion the judge did not validate. MBCX-01's `A0 AND B AND A1` has no judge and therefore no κ to fall below.
- **Physical measurement:** dollars, tokens, and unreported wall-clock. Explicitly **no CPU instruction counts and no hardware counters**. Dollars are a provider pricing artifact; MBCX-01's instruction count is a property of the machine.
- **Family error:** bootstrap CIs with **no explicit family-wise correction**. MBCX-01 declares 0.05 family error across the delta and OM streams jointly.
- **Missingness:** no worst-case completion hull. If a run is missing, this design has no stated machinery to certify that every legal completion yields the same branch.
- **Obligation state:** none. This is a document-retrieval ablation. There is no bitemporal model, no obligation continuity, no state-transition replay, no exact-state receipt.
- **Comparison shape:** the "forced" condition preloads a routing artifact; the paper's own framing is that this is *not* a full-oracle comparison. MBCX-01's OM arm is constructed from an independent gold read-set, which is a stricter ceiling.

**11. Safety Under Scaffolding: How Evaluation Conditions Shape Measured Safety** — SEARCHED
David Gringras. arXiv:2603.10044 (v1 2026-03-08, v2 2026-06-03).
https://arxiv.org/abs/2603.10044 (abs) · https://arxiv.org/html/2603.10044v2 (full text)

*What it is:* *"N = 62,808 blinded, pre-registered, equivalence-tested evaluations across four safety benchmarks."* Preregistered on OSF (DOI 10.17605/OSF.IO/CJW92; a Phase-2 mechanistic component separately at 10.17605/OSF.IO/WA9Y7).

*Shares with MBCX-01 — the strongest overlap on the inference machinery specifically:*
- *"Hypotheses H1–H4, the primary statistical model, all secondary specifications, scoring rubrics, equivalence margins, and the full specification curve were registered on the Open Science Framework before data collection."*
- **TOST with a pre-specified ±2 percentage-point equivalence margin** across all primary comparisons.
- **Holm-Bonferroni correction on pairwise comparisons**, cluster-robust (sandwich) standard errors clustered by case — i.e. genuine family error control, which #10 lacks.
- Power stated: ~10,468 observations per model-configuration cell giving ~80% power at 2.5 pp.
- **80.9% of observations deterministically scored** — *"TruthfulQA, BBQ, AI Factual Recall use deterministic MC answer extraction against ground-truth keys"* — with LLM-judge scoring confined to 19.1% (XSTest/OR-Bench).
- Responses sanitized with *"UUID randomisation and hash verification on OSF"* before scoring.

*Lacks vs MBCX-01:*
- **Exactness gate:** the 80.9% deterministic portion is multiple-choice answer extraction against a key — exact per item, but not a *conjunctive chain* across three model nodes plus a writer receipt with identity and hash links checked first. And 19.1% of the corpus is judged, so the family-level estimand is not exact.
- **Physical measurement:** none reported. No tokens, no latency, no CPU, no counters.
- **Boundedness / continuity:** entirely out of scope. This studies how *scaffolding configuration* (direct API, ReAct, multi-agent critic, map-reduce) shifts measured safety. There is no memory carrier, no state continuity, no obligation model, no history-scale range.
- **Equivalence vs non-inferiority:** TOST two-sided equivalence at ±2 pp is a *stricter* symmetric claim than MBCX-01's one-sided −0.10 margin. This is a place where the published work is more demanding than MBCX-01 on its own axis, and that should be said plainly.
- **Cryptographic reconstruction:** hash verification of sanitized response files on OSF. Not a Merkle root over an ordered cohort, not `git cat-file` clean-room reconstruction with SHA-384 + byte + line-count verification before import.

**12. Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations** — SEARCHED
Evan Miller. arXiv:2411.00640, 2024-11-01.
https://arxiv.org/abs/2411.00640

*What it is:* The reference methodological argument that *"evaluations are experiments"* and that the eval literature has ignored the experiment-analysis and planning literature from other sciences. Provides formulas for analyzing eval data, measuring differences between two models, and planning an eval experiment; recommends CIs, paired tests, and power analysis.

*Shares with MBCX-01:* the paired-comparison framing is exactly MBCX-01's design — BC and OM share scenario, cut, observation, action universe, schema, instructions, padding, output schema, and transport, differing **only** in object selection. That is a textbook paired design and Miller's paired-test recommendation is its methodological warrant.

*Lacks vs MBCX-01:* the abstract and listing do **not** name equivalence testing, non-inferiority, or preregistration. It is a recommendation paper, not an executed experiment — it prescribes error bars and power analysis for *difference* detection, and stops short of the non-inferiority/equivalence framing MBCX-01 needs. It carries no physical-cost axis at all.

**13. NeurIPS Workshops on Pre-registration in Machine Learning (PMLR v148, v181)** — SEARCHED
v148 eds. Bertinetto, Henriques, Albanie, Paganini, Varol — NeurIPS 2020 workshop, 2020-12-11, published 2021-07-08. v181 — NeurIPS 2021 workshop, 2021-12-13, published 2022-10-05.
https://proceedings.mlr.press/v148/ · https://proceedings.mlr.press/v181/

*What it is:* The institutional precedent for ML preregistration — papers reviewed on protocol before results exist.

*Shares with MBCX-01:* the identical core discipline — the protocol is judged before the numbers, and negative results are publishable. MBCX-01's "publish every registered result" and its enumerated valid final outcomes (carrier rejection, design failure, transport inconclusive, ceiling, interface failure, promotion, scientifically inconclusive) are that norm made executable.

*Lacks vs MBCX-01:* these are a publication *venue* and a norm, not a measurement standard. Nothing in the volumes read this session imposes an exactness gate, a physical-work bound, or cryptographic subject pinning. The sampled v148 titles are conventional ML topics (active learning, self-supervised skeleton action recognition, domain adaptation), not memory-continuity work.

---

### Lane 3 — Systems: bounded incremental work, and cryptographic experimental integrity

**14. DBSP: Automatic Incremental View Maintenance for Rich Query Languages** — SEARCHED
Mihai Budiu, Frank McSherry, Leonid Ryzhyk, Val Tannen. arXiv:2203.16684, 2022-03-30; PVLDB 16; VLDB Journal 2025.
https://arxiv.org/abs/2203.16684

*What it is:* A stream-computation language plus a general algorithm that mechanically derives the incremental version of an arbitrary DBSP program, covering full relational algebra, sets/multisets, nested relations, aggregation, flatmap, monotonic and non-monotonic recursion, and streaming aggregation.

*Shares with MBCX-01:* this is the strongest systems-side statement of MBCX-01's core wager — that a correct answer can be maintained by work proportional to the *change* rather than the *history*. The general IVM lineage (differential dataflow, DBSP) is where "bounded work, exact result" is a theorem rather than an aspiration.

*Lacks vs MBCX-01:*
- **Domain:** relational views over data streams, not agent obligation state. No bitemporal cut, no knowledge/valid separation, no handoff/action-identity binding, no model in the loop.
- **Bounded-memory claim:** I could not establish at origin from the abs page whether the paper claims bounded memory or proves incremental-equals-from-scratch equality. Secondary sources describe bounded-memory evaluation of stateful SQL over unbounded streams; **I did not verify that at origin and do not assert it.**
- **Physical measurement:** no empirical measurement, in any unit, was visible on the abs page. Even where IVM literature does measure, the unit is throughput/latency, not per-cell retired instructions against a preregistered tolerance.
- **Preregistration / non-inferiority:** not applicable to this work's genre; absent.

**15. Is Agent Memory a Database? Rethinking Data Foundations for Long-Term AI Agent Memory** — SEARCHED
Abdelghny Orogat, Essam Mansour. arXiv:2605.26252, 2026-05-25.
https://arxiv.org/abs/2605.26252

*What it is:* Argues agent memory is a data-management workload rather than storage; introduces "Governed Evolving Memory (GEM)" and a `MemState` property-graph prototype. Names four failure modes: *"unregulated growth, missing semantic revision, capacity-driven forgetting, and read-only retrieval."*

*Shares with MBCX-01:* the position itself — that agent memory needs database foundations, not vector-store heuristics — is MBCX-01's premise. More sharply: it argues **correctness should be evaluated at the state-trajectory level rather than individual records**, which is the same move MBCX-01 makes when it scores a whole episode `A0 AND B AND A1` rather than a per-answer hit rate.

*Lacks vs MBCX-01:* the abstract does not reference bitemporal modeling, event sourcing, incremental view maintenance, or exactness guarantees. It is a vision/position paper with a feasibility prototype that *"validates feasibility and exposes the gap to a native engine"* — no correctness metric, no experimental methodology, no cost measurement stated in the abstract. No preregistration, no non-inferiority, no physical measurement.

**16. Computer Science Conferences Should Require Nonrepudiable Experimental Results** — SEARCHED
Mamadou K. Keita, Christopher Homan. arXiv:2605.08586, 2026-05-09.
https://arxiv.org/abs/2605.08586

*What it is:* A position paper: *"computer science conferences should require tamper-evident, nonrepudiable attestations of experimental results."* Reference implementation **K-Veritas** *"produces signed reports without accessing training data."*

*Shares with MBCX-01:* the same threat model MBCX-01's `SignedMeasurementReceiptV1` and signer/trust-root separation address — that a self-reported number is not evidence that the reported code produced it. Both separate content integrity from producer authority.

*Lacks vs MBCX-01:* it is a **proposal for a norm, not an executed instrument**. The page does not mention hashes, commitments, preregistration, or artifact pinning as concrete mechanisms. It attests that a computation ran; it does not gate the *scientific admission* of a result on that attestation, does not define an exactness predicate, and carries no physical-measurement or inference machinery. That the field is publishing position papers arguing for attestation in mid-2026 is itself the signal: MBCX-01's signed-receipt design is ahead of the norm, not behind it.

---

### Lane 4 — Measurement precision: how close does published best practice get?

**17. Can Hardware Performance Counters be Trusted?** — SEARCHED
Vincent M. Weaver, Sally A. McKee. IISWC 2008. Tech report CSL-TR-2008-1051.
https://web.eece.maine.edu/~vweaver/papers/iiswc08/

*What it is:* An investigation of how deterministic the **retired instruction** counter is across nine x86 implementations, over full SPEC CPU2000 and CPU2006, with workarounds that reduce variation on x86 Linux.

*Shares with MBCX-01 — this is the direct methodological ancestor of MBCX-01's instruction tolerance, and the lane should cite it.* It establishes that retired-instruction counts are the *right* quantity to use when you want a low-variance, platform-comparable work measure, and simultaneously that they are **not** free of noise: named causes are address-space randomization, unintentional binary/OS non-determinism (changing the number of environment variables perturbs the count), and processor errata.

*Note on the numbers:* the project page I opened at origin does **not** carry the variation figures. The coefficient-of-variation figures widely attributed to this work (≈1.07% unprepared, <0.002% after setup control) came from a search snippet in this session and I did **not** verify them at origin. They should be verified from `iiswc08_inst.pdf` or the tech report before being quoted in any committed artifact.

*Lacks vs MBCX-01:* it is x86 **Linux**, not Windows/ETW — MBCX-01's PMU-availability constraints (Windows 10 1809 / Server 2019 default, Hyper-V guest `Set-VMProcessor -Perfmon`, nested virtualization unsupported, no cross-hardware save/restore) are a different environment with different failure modes, already documented in the r13 addendum. It measures counter determinism *as a subject*; it does not gate an experiment's admission on a preregistered per-cell tolerance, and there is no LLM, no obligation state, no non-inferiority.

**18. Producing Wrong Data Without Doing Anything Obviously Wrong!** — SEARCHED
Todd Mytkowicz, Amer Diwan, Matthias Hauswirth, Peter Sweeney. ASPLOS '09.
https://sape.inf.usi.ch/publications/asplos09
*(The ACM DL page `dl.acm.org/doi/10.1145/1508284.1508275` returned HTTP 403 to this session; the authors' group page at USI was used as origin instead.)*

*What it is:* Demonstrates that measurement bias is significant and commonplace — an innocuous change to experimental setup flips conclusions — across the architectures and compilers tested. Surveyed **133 recent ASPLOS/PACT/PLDI/CGO papers** and found *"none of the papers with experimental results adequately consider measurement bias."* Proposes causal analysis (detection) and setup randomization (avoidance).

*Shares with MBCX-01:* the ancestor argument for why MBCX-01 freezes the environment, the harness build digest, host/environment facts, and the run/candidate/generator/cell identity, and why it forbids migration and save/restore during measurement. Also the ancestor of the tolerance idea — a difference smaller than measurement bias is not a result.

*Lacks vs MBCX-01:* it is a critique and a pair of remedies, not an instrument. It contains no preregistration, no exactness gate, no non-inferiority, no cryptographic pinning. It also prescribes **setup randomization**, which is a *different* strategy from MBCX-01's **setup freezing plus signed environment attestation** — a genuine methodological divergence the lane should be able to defend, because randomization is the published remedy and freezing is not.

**19. SIGPLAN Empirical Evaluation Checklist** — SEARCHED
SIGPLAN Executive Committee.
https://www.sigplan.org/Resources/EmpiricalEvaluation/

*What it is:* The field's canonical best-practice checklist for empirical evaluation in PL research, organized into seven categories with examples, created in response to inadequacies in PLDI/POPL/OOPSLA papers. Framed as *"meant to support informed judgment, not supplant it."*

*Lacks vs MBCX-01:* on the landing page read this session, the checklist **does not require preregistration, does not require hardware-counter or instruction-count measurement, and does not mention cryptographic pinning of the subject cohort.** (Caveat: the seven category names are in the linked PDF, which I did not open; I am reporting the landing page only, so this is "not present in what was read," not "absent from the checklist.") This is the relevant ceiling: the discipline's own published standard for empirical rigor sits below all three of MBCX-01's precision axes.

**20. ACM Artifact Review and Badging v1.1** — SEARCHED (via secondary origin)
ACM policy v1.1, dated 2020-08-24. Canonical page `acm.org/publications/policies/artifact-review-and-badging-current` returned **HTTP 403** to this session; definitions were read at the EuroSys Systems Research Artifacts site, which quotes them verbatim: https://sysartifacts.github.io/eurosys2024/badges

*Definitions read at origin:* **Artifacts Available** — *"Author-created artifacts relevant to this paper have been placed on a publicly accessible archival repository. A DOI or link to this repository along with a unique identifier for the object is provided."* **Artifacts Evaluated – Functional** — *"documented, consistent, complete, exercisable, and include appropriate evidence of verification and validation."* **Results Reproduced** — *"The main results of the paper have been obtained in a subsequent study by a person or team other than the authors, using, in part, artifacts provided by the author."*

*Lacks vs MBCX-01:* **none of the badges require cryptographic digest pinning, preregistration, or a measurement-precision tolerance.** The checklists ask that dependencies come *"from well-known sources"* and that external changes be *"clearly separated."* A DOI plus a unique identifier is a *location* guarantee; MBCX-01 requires a *content* guarantee — reconstruct `commit:path` from `git cat-file`, verify Git blob, raw bytes, LF/line counts and SHA-384, then import. That is a strictly stronger property than any ACM badge asks for.

**21. How Efficient is LLM-Generated Code? A Rigorous & High-Standard Benchmark (ENAMEL)** — SEARCHED
Ruizhong Qiu, Weiliang Will Zeng, James Ezick, Christopher Lott, Hanghang Tong. arXiv:2406.06647, 2024-06-10, rev. 2025-02-19; ICLR 2025.
https://arxiv.org/abs/2406.06647

*What it is:* The most statistically careful efficiency benchmark for LLM output found in this sweep. Proposes `eff@k`, generalizing `pass@k` from correctness to efficiency and *"appropriately handl[ing] right-censored execution time,"* with an *"unbiased and variance-reduced estimator of eff@k via Rao–Blackwellization"* and a numerically stable implementation.

*Shares with MBCX-01:* it treats the measurement of computational cost as a **statistical estimation problem with censoring**, not as a number you read off a stopwatch. That is the same seriousness MBCX-01 applies to its missingness hull, applied to the cost axis.

*Lacks vs MBCX-01:*
- **Unit:** **execution time**, not retired instructions. It handles hardware fluctuation *statistically* (weighted averaging across difficulty levels, censoring-aware estimation) rather than by moving to a lower-variance physical quantity. MBCX-01 chooses the physical quantity; ENAMEL chooses the estimator. Both are defensible; they are different bets, and ENAMEL's is the published one.
- **Subject:** generated code, not agent memory or obligation continuity. No state model, no bitemporal cut, no carrier.
- **Preregistration / non-inferiority:** not indicated on the abs page.

**22. Compress the Context, Keep the Commitments: A Formal Framework for Verifiable LLM Context Compression** — SEARCHED
Natalia Trukhina, Vadim Vashkelis. arXiv:2605.17304, 2026-05-17.
https://arxiv.org/abs/2605.17304

*What it is:* Included because its title states MBCX-01's thesis almost verbatim. "Context Codec" represents dialogue state as *"typed, source-grounded semantic atoms with canonical identity, equivalence, conflict, confidence, risk, and evidence spans,"* across five separated concerns (extraction, normalization, representation, rendering, verification), with metrics Critical Atom Recall, Weighted Atom Recall, Commitment Density, and round-trip recoverability, plus a taxonomy of semantic compression errors.

*Shares with MBCX-01:* canonical identity for state atoms; the explicit claim that *commitments* specifically must survive compression; a verification stage as a first-class concern.

*Lacks vs MBCX-01 — and the gap is wide:*
- **Exactness gate:** the metrics are **recall-based and graded** (Critical Atom Recall, Weighted Atom Recall). Recall of commitments is not preservation of commitments. MBCX-01's gate does not accept 0.98 recall as a pass.
- **Empirical basis:** *"a small diagnostic study"* comparing their notation against prose and JSON — explicitly **not a full benchmarked evaluation**.
- **Proof:** despite "formal framework" in the title, the abstract carries **no proof and no bounded-work claim**.
- **Preregistration, non-inferiority, physical measurement:** none mentioned.

---

## (b) Overlaps — what was genuinely done first, credited plainly

These are real. MBCX-01 is not first at any of them and should say so in its own prior-art record.

1. **Bitemporal fact modeling applied to agent memory, in production, published: Zep/Graphiti (Jan 2025).** Four timestamps separating system transaction order from world validity, with invalidation rather than deletion. MBCX-01 adds a third cut coordinate (journal sequence) and splits visibility from effectivity as separate executable predicates, but the *idea* of bitemporal agent memory is Zep's in the agent literature and Jensen/Snodgrass's in the database literature (the latter already credited in the r10 memo).

2. **Bounded-carrier vs full-context comparison with cost reported alongside quality: Mem0 (Apr 2025) and Zep (Jan 2025).** Mem0 reports 91% lower p95 latency and >90% token savings against a full-context baseline; Zep reports 2.58 s vs 28.9 s. MBCX-01 is not first to ask "does the bounded thing keep up while costing less." It is asking with a different dependent variable and a different cost unit.

3. **Preregistration + non-inferiority + a byte-identical frozen corpus at immutable git tags + cost measurement, in one LLM study: Cochran, arXiv:2607.04576 (Jul 2026).** This is the closest single composition found and it predates any MBCX-01 execution. It reached the non-inferiority conclusion MBCX-01 is designed to test the shape of, in a document-retrieval domain.

4. **Preregistered equivalence testing at scale with family error control in LLM evaluation: Gringras, arXiv:2603.10044 (Mar 2026).** OSF-registered hypotheses, statistical model, rubrics, margins and specification curve before data collection; TOST at ±2 pp; Holm-Bonferroni; cluster-robust SEs; ~80.9% deterministically scored; hash verification of sanitized responses. On the pure inference axis this is at or above MBCX-01's declared machinery, and its two-sided ±2 pp equivalence margin is a stricter claim than MBCX-01's one-sided −0.10.

5. **Programmatic, non-judged scoring of due-obligation discharge in LLM agents: PM-Bench (Jul 2026).** Set-F1 against a solver-validated due set, with cross-day obligations, rescheduling, cancellation and hidden channels. MBCX-01 is not first to score obligation discharge without a judge.

6. **Deterministic environment-state scoring plus a conjunctive reliability metric in an agent memory benchmark: STATE-Bench (May 2026).** Pass^5 — success on all five runs — is a published conjunctive gate in this space.

7. **Retired instructions as the low-variance work measure, with its non-determinism characterized: Weaver & McKee (IISWC 2008).** MBCX-01's choice of retired instructions over wall time is theirs, not the lane's.

8. **Measurement bias as a first-class threat in systems evaluation: Mytkowicz et al. (ASPLOS 2009).** Their 133-paper survey is the reason a tolerance and a frozen environment are defensible at all — and their prescribed remedy (setup randomization) differs from MBCX-01's (setup freezing plus attestation), which is a divergence the lane owes an argument for.

9. **Bounded incremental work with exact results as a general algorithmic result: the differential-dataflow/DBSP lineage (2022–2025).** MBCX-01's "exact continuity under bounded work" is not a new class of claim in computing; it is a known class being asked in a new domain.

10. **Cryptographic attestation of experimental results as a proposed publication requirement: Keita & Homan, arXiv:2605.08586 (May 2026).** The norm is being argued for publicly, independently of this lane.

11. **The field's own diagnosis that cost is unreported: Du, arXiv:2603.07670 §5.5 (Mar 2026)** — *"None of the current benchmarks systematically report efficiency metrics alongside effectiveness."* MBCX-01 did not discover this gap; a survey named it five months earlier.

---

## (c) Verdict

**Question 1 — did someone already do it?**

Every *component* of MBCX-01 has a published predecessor, and several are recent and strong. Bitemporal agent memory: Zep. Bounded-vs-full-context with cost: Mem0, Zep. Programmatic obligation-discharge scoring: PM-Bench. Deterministic state scoring plus a conjunctive run gate: STATE-Bench. Preregistered non-inferiority with a frozen byte-identical corpus and cost measurement: Cochran 2607.04576. Preregistered TOST equivalence with Holm-Bonferroni family control at N≈63k: Gringras 2603.10044. Retired-instruction determinism: Weaver & McKee. Bounded-work exact incremental maintenance: DBSP. Cryptographic result attestation: Keita & Homan.

**The composition, however, was not found in the shapes this sweep covered.** In the 22 works opened at origin, no single work combines (i) a conjunctive exactness gate over a multi-node episode with identity/hash-linked artifacts, (ii) a preregistered *physical* work bound measured in retired instructions per grid cell with a declared tolerance across a history-scale range, (iii) preregistration of the whole instrument at a pinned commit with a single terminal look, (iv) a non-inferiority estimand with declared family error and an exact worst-case missingness hull, and (v) clean-room reconstruction of every subject from cryptographically pinned objects before execution.

The nearest approaches, and exactly how far each gets:
- **Cochran 2607.04576** reaches (iii), (iv, partially — no family correction, no missingness hull) and (v, partially — git tags and byte-parity, no digest-verified reconstruction), but scores with an LLM judge whose own preregistered validation threshold it missed (κ = 0.23 vs 0.60), and measures cost in dollars and tokens with no CPU or counter measurement.
- **Gringras 2603.10044** reaches (iii) and (iv) with genuine family control, and 80.9% deterministic scoring, but has no memory carrier, no continuity claim, and no cost measurement of any kind.
- **PM-Bench** reaches the closest thing to (i) in the obligation domain, but grades partially and takes no cost measurement, no preregistration, and no statistics.
- **Zep and Mem0** are the only works that pair a bounded carrier against a full-context ceiling with a cost number, and both use LLM judges and wall-clock/token proxies with no uncertainty quantification.

**Question 2 — did they do it to this level of precision?**

On the axes MBCX-01 defines, the honest answer is split.

*Where MBCX-01 is more precise than anything opened:* the exactness gate (no work found scores an agent-memory carrier by a conjunctive multi-node identity-and-hash predicate with schema-invalid output counted as failure rather than missingness); the physical measurement (no work found in the agent-memory literature measures retired instructions at all, let alone per-cell against a preregistered tolerance with process-tree containment and a signed receipt — and the field's own survey says cost is systematically unreported); and the reconstruction discipline (ACM's own badging policy, read at origin, requires a DOI and a unique identifier, not digest-verified clean-room reconstruction; the SIGPLAN checklist landing page requires neither preregistration nor counter-level measurement nor cohort pinning).

*Where published work is at or above MBCX-01:* Gringras's two-sided ±2 pp TOST with Holm-Bonferroni and cluster-robust SEs is a stricter inference claim than MBCX-01's one-sided −0.10 margin; ENAMEL's Rao-Blackwellized, censoring-aware `eff@k` is a more sophisticated *estimator* for cost than MBCX-01's direct-measurement approach (MBCX-01 bets on a better physical quantity instead, which is a different and unproven trade); and Mytkowicz's prescribed remedy for measurement bias is randomization, not freezing, so MBCX-01's freeze-and-attest strategy is a departure from the published remedy that it should argue for rather than assume.

*The load-bearing caveat:* MBCX-01 has run nothing. Precision of *design* is not precision of *result*. Cochran, Gringras, PM-Bench, Zep, Mem0, STATE-Bench and ENAMEL all produced numbers. MBCX-01's r13 closure explicitly holds `STATE_AUTHORITY_UNAVAILABLE` and `PHYSICAL_HARNESS_UNAVAILABLE`. Until the harness exists and the 456/4 route gate passes, the correct comparative statement is that MBCX-01 *specifies* a stricter instrument than anything this sweep opened, not that it *has* one.

**Claim shape.** This sweep covered: agent/LLM memory systems and benchmarks (MemGPT/Letta lineage, LoCoMo, LongMemEval, MemoryAgentBench, STATE-Bench, BEAM, Mem0, Zep/Graphiti, plus one 2022–early-2026 survey), prospective-memory and obligation-tracking evaluation (PM-Bench), context compression with commitment preservation, LLM-evaluation statistics (error bars, equivalence/non-inferiority, ML preregistration venues), incremental view maintenance and event-sourcing for agent state, performance-evaluation rigor (retired-instruction determinism, measurement bias, SIGPLAN checklist, ACM badging, ENAMEL), and cryptographic experimental integrity. **Not found in the shapes this sweep covered** is not the same as does not exist. Specifically unswept or under-swept: non-English literature; patent filings; industrial internal evaluations; formal-methods venues (CAV/POPL) for continuity proofs; the OSF registry itself searched directly for unpublished LLM preregistrations; ACM DL and IEEE Xplore full text (both returned 403 or were not queried this session); and the full texts of LoCoMo, MemGPT, MemoryAgentBench and DBSP, whose scoring/cost/statistics properties are recorded above as **not established at origin** rather than absent.

---

## (d) Sweep log

**Local reads (byte-level, this session).** All under `<repo>-build/`:
`MBCX-01-EXPERIMENT-DESIGN-r9.md` (74 lines, full) · `MBCX-01-R10-ARCHITECTURE-SPEC.md` (full) · `MBCX-01-R13-CLOSURE-ARCHITECTURE.md` (full) · `MBCX-01-R10-PRIOR-ART-MEMO.md` (full) · `MBCX-01-R11-PRIOR-ART-MEMO.md` (full) · `MBCX-01-R12-PRIOR-ART-AND-SHELF-MEMO.md` (full) · `MBCX-01-R13-PRIOR-ART-AND-ENVIRONMENT-ADDENDUM.md` (full). Directory listing taken to locate exact filenames (`ls -la | grep -i -E "PRIOR-ART|R10-ARCH|R13-CLOS"`).

**Queries issued (verbatim), in order:**
1. `MemGPT Letta agent memory paper arXiv virtual context management`
2. `LongMemEval benchmark long-term memory chat assistants arXiv`
3. `LoCoMo benchmark very long-term conversational memory evaluating arXiv 2402`
4. `Zep Graphiti temporal knowledge graph agent memory bi-temporal arXiv`
5. `prospective memory benchmark LLM agents deferred intention obligation tracking evaluation`
6. `preregistration non-inferiority trial design large language model evaluation methodology`
7. `"non-inferiority" margin LLM evaluation benchmark statistical power sample size preregistered`
8. `"Adding Error Bars to Evals" statistical approach language model evaluations Miller arXiv`
9. `preregistration machine learning experiments NeurIPS preregistration workshop registered reports ML`
10. `"Producing Wrong Data Without Doing Anything Obviously Wrong" measurement bias Mytkowicz ASPLOS`
11. `Weaver Dongarra "can hardware performance counters be trusted" retired instructions determinism`
12. `ACM artifact review badging v1.1 "Results Reproduced" "Artifacts Available" policy definitions`
13. `Mem0 scalable long-term memory production AI agents arXiv 2504 LoCoMo latency token savings`
14. `differential dataflow incremental view maintenance agent state LLM memory bounded work`
15. `DBSP automatic incremental view maintenance rich query languages arXiv Budiu bounded memory streaming`
16. `MemoryAgentBench evaluating memory in LLM agents incremental multi-turn interactions arXiv 2507`
17. `agent memory benchmark efficiency token cost FLOPs measurement "memory operations" evaluation 2026`
18. `BEAM benchmark agent memory 1M 10M tokens arXiv 2026`
19. `equivalence testing TOST machine learning model comparison "non-inferiority" NLP evaluation statistics`
20. `preregistered study large language model evaluation OSF registration protocol frozen model snapshot`
21. `hardware performance counters retired instructions ETW measurement LLM agent system evaluation`
22. `LLMLingua prompt compression evaluation compressed context vs full context accuracy retention`
23. `ENAMEL EffiBench LLM code efficiency benchmark instruction count hardware counter measurement rigorous`
24. `event sourcing append-only journal bounded frontier read agent obligation state exact replay guarantee`
25. `"working set" bounded memory agent "exact" state continuity proof measured CPU instructions preregistered experiment`

**Opened at origin (25 successful fetches, 22 distinct works):**
`arxiv.org/abs/2410.10813` · `arxiv.org/html/2410.10813v2` · `arxiv.org/abs/2310.08560` · `arxiv.org/abs/2402.17753` · `arxiv.org/abs/2607.12385` · `arxiv.org/html/2607.12385v1` · `arxiv.org/abs/2501.13956` · `arxiv.org/html/2501.13956v1` · `arxiv.org/abs/2504.19413` · `arxiv.org/abs/2507.05257` · `arxiv.org/abs/2603.07670` · `arxiv.org/html/2603.07670v1` · `arxiv.org/abs/2605.26252` · `arxiv.org/abs/2605.17304` · `arxiv.org/abs/2607.04576` · `arxiv.org/html/2607.04576v1` · `arxiv.org/abs/2603.10044` · `arxiv.org/html/2603.10044v2` · `arxiv.org/abs/2411.00640` · `arxiv.org/abs/2406.06647` · `arxiv.org/abs/2505.23471` · `arxiv.org/abs/2605.08586` · `arxiv.org/abs/2203.16684` · `proceedings.mlr.press/v148/` · `sigplan.org/Resources/EmpiricalEvaluation/` · `web.eece.maine.edu/~vweaver/papers/iiswc08/` · `sape.inf.usi.ch/publications/asplos09` · `sysartifacts.github.io/eurosys2024/badges` · `opensource.microsoft.com/blog/2026/05/19/introducing-state-bench-a-benchmark-for-ai-agent-memory/`

**Fetches that failed and how handled:**
- `dl.acm.org/doi/10.1145/1508284.1508275` — HTTP 403. Substituted the authors' USI group page for the Mytkowicz abstract and survey findings.
- `acm.org/publications/policies/artifact-review-and-badging-current` — HTTP 403. Substituted the EuroSys 2024 systems-artifacts badge page, which quotes ACM v1.1 verbatim. **The canonical ACM policy page was not read at origin this session**; badge definitions are quoted from the secondary origin.
- `users.cs.northwestern.edu/.../mytkowicz-wrong-data.pdf` — fetched (486 KB) but PDF text extraction failed; not used.

**Existence verification.** Search results returned a substantial number of 2026-dated arXiv IDs. Every 2026-dated work cited in section (a) was opened at its `arxiv.org/abs/` page and confirmed to exist with title, authors and submission date matching: 2603.07670, 2603.10044, 2605.08586, 2605.17304, 2605.26252, 2607.04576, 2607.12385. Search-result titles that were *not* opened (e.g. `2605.29630`, `2606.29914`, `2606.14571`, `2605.01847`, `2602.06052`, `2606.24775`, `2604.05137`, `2607.07619`) are **not cited** in this memo and their existence is **unverified**.

**Provenance caution on cited works.** Four of the strongest 2026 hits — 2607.04576 (single author), 2603.10044 (single author), 2605.17304 (two authors), 2605.08586 (two authors) — are arXiv preprints whose peer-review status I did **not** establish. I verified existence, title, authors, date, and the quoted methodological content at origin. I did not verify their claims, their data, or that they were reviewed. Weight accordingly before citing them as settled precedent in a committed artifact.

**Why I stopped.** Four independent stopping signals converged: (1) the agent-memory lane began returning the same six systems (MemGPT, Zep, Mem0, LoCoMo, LongMemEval, MemoryAgentBench) across unrelated queries; (2) an independent survey of 2022–early-2026 opened at origin states that no current benchmark in this field systematically reports efficiency alongside effectiveness, which converges with what the primary sources showed one at a time; (3) the statistics lane produced its two strongest hits (2607.04576, 2603.10044) and further queries returned clinical-trial methodology rather than ML work; (4) the measurement-rigor lane bottomed out at the field's own published standards — SIGPLAN's checklist and ACM's badging policy — which are the ceiling of institutional best practice and sit below all three of MBCX-01's precision axes. Continuing would have accumulated more instances of the same shapes rather than changing the verdict. The unswept surfaces are enumerated in section (c) and should be treated as open, not as searched-and-empty.
