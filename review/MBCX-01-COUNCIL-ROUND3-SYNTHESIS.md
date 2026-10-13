# MBCX-01 Council Round 3 Synthesis

Date: 2026-08-12  
Adjudicated design: `MBCX-01-EXPERIMENT-DESIGN-r2.md` at commit `b5874994f89d73efde6da90a445dd5f807808375`  
Round result: **NO-GO for paid inference; repairable without building the harness first**

## 1. Seat accounting

| Seat | Report | Protocol status | Substantive verdict |
|---|---|---|---|
| Claude browser seat | `MBCX-01-SEAT1-CLAUDE-VERDICT-r3.md` | Sealed-content declaration passed. The UI selected Opus 5 Extra, while the report self-identified as Claude Opus 4.6; both facts are preserved and no exact checkpoint claim is inferred. | GO with comparator, render, and budget fixes |
| ChatGPT/Sol browser seat | `MBCX-01-SEAT2-CHATGPT-SOL-VERDICT-r3.md` | **Not countable as a sealed vote.** The seat disclosed that one over-broad tokenizer grep exposed snippets from prohibited prior verdict/synthesis/exec files. | Substantive NO-GO |
| Codex exec seat | `MBCX-01-SEAT3-CODEX-VERDICT-r3.md` | Sealed and independently pinned | NO-GO |

The formal round therefore contains two sealed independent reports plus one contaminated-but-useful technical review. The two sealed reports alone identify the weak comparator and reconstruction gap. All three independently identify ordinary flat traversal/history retention as a necessary comparator repair.

## 2. Decisive conclusion

r2 would not cleanly test typed continuity against the strongest cheap flat continuity mechanism. It would test typed history against a deliberately destructive current-only ledger. A cheap append-only journal of the same primitive public events, deterministic replay, a current flat index, and bounded traversal over already-public prerequisite IDs recovers the correction/retraction and dependency cases that r2 reserved for TN. If TN beat that F arm, the experiment could mistake “history beats overwrite” or “BFS beats no BFS” for a typed-memory result.

The primary flat arm must therefore become **F+**, a flat replay package. Current-only overwrite remains useful only as a no-model ablation showing why retained public history matters at all.

## 3. Verified blockers and dispositions

| Finding | Disposition | r3 action |
|---|---|---|
| Current-only F is not the strongest cheap flat comparator | **ACCEPT** | Replace it with append-only primitive-event history + deterministic replay/current index. |
| F is denied cheap dependency traversal over IDs it already stores | **ACCEPT** | Give F+ and TN the same bounded ID-adjacency traversal and dependency-trigger reverse scan. |
| Typed persistence versus presentation remains confounded | **ACCEPT; hold render fixed in the primary** | Make `FM`—flat replay under the exact native-shaped render—the primary flat arm. Keep only two primary arms; use F+ and TF on 25% to complete the 2×2 decomposition. |
| TF subset is not stratified/powered precisely enough | **ACCEPT** | Freeze subset allocation across every update/closure/pressure class and preregister descriptive precision/tipping rules. |
| Mechanism prevalence can move the result across `+0.03` | **ACCEPT** | Freeze exclusive positive and lure quotas by mechanism before generator implementation. |
| The 512-token output cap contradicts the legal maximum | **ACCEPT** | Derive the cap from exact served-tokenizer serialization. Eighteen 32-token IDs alone require 576 tokens; nineteen require 608, before JSON. With 20% headroom those lower bounds are 692 and 730. |
| Maximum-load/budget fixtures are underspecified | **ACCEPT** | Freeze exact schemas, total event bound, joint mandatory-set maxima, and canonical non-overflow/overflow fixtures before selecting a budget. |
| `budget_failure` scoring is ambiguous | **ACCEPT WITH NARROWER FIX** | Every paid target cell is pre-certified non-overflow. A target-cell budget failure stops the experiment as an implementation/design invalidity; it is never silently truncated, rerolled, or scored favorably. |
| Existing reconstruction witnesses prove artifact presence, not causality | **ACCEPT** | Add sanitized child execution, opaque scenario IDs, import denial, valid-artifact swap, and independent-field mutation witnesses. |
| Reserve replacement after an accepted/no-body ambiguity biases the estimand | **ACCEPT** | Preserve the frozen target cohort. Keep missing target pairs missing, apply worst-case/tipping analysis in `[-1,1]`, and allow reserves only for pre-inference generator invalidity. |
| Chi-square pilot SD upper bound is not valid for declared non-normal families | **ACCEPT** | Remove the pilot from sample-size authority. Derive inference calibration from the fully frozen score support/family grid; the 12-pair pilot is engineering-only. |
| Distribution families and Monte Carlo acceptance are underspecified | **ACCEPT** | Freeze every family parameter/support/retention rule, enumerate finite supports exactly where possible, and use one-sided binomial bounds for simulated acceptance gates. |
| BCa disagreement is binding but absent from calibration | **ACCEPT WITH SIMPLIFICATION** | Demote BCa and permutation to sensitivity reports. They cannot replace or veto the calibrated primary interval. |
| Generator ontology can mirror TN | **ACCEPT** | Publish an implementation-independent transition table/property oracle, a structurally different generator, and hand-authored challenge cases. |
| OpenRouter route/cache/transform attestation needs exact bytes | **ACCEPT** | Freeze request bytes and exact provider endpoint; enable router metadata; fail closed on missing attestation/cache/transform/fallback; prefer direct provider if conformance cannot be proved. |
| Separate chronological-history paid diagnostic remains useful | **REJECT AFTER F+** | F+ subsumes it; delete that paid branch. |
| Increase the external pilot to 24–30 or 70 | **REJECT** | A larger engineering pilot does not repair the non-normal variance-bound defect. Keep 12, remove statistical authority, and stop on instrument defects. |
| Give F only one-deep undo | **REJECT IN FAVOR OF STRONGER FIX** | One-deep history closes only selected traces. F+ replay is cheaper conceptually, complete for admitted public events, and the stronger comparator. |
| Precision and recall should be co-primary | **REJECT** | Keep one primary estimand to avoid multiplicity. Report precision, recall, action count, and false-action classes as mandatory secondary diagnostics. |
| Lower the SD floor after an empty rare-tail probe | **REJECT** | An empty probe cannot establish absent tails. The entire pilot-SD mechanism is removed instead. |
| Add a special strict-tools header | **NOT APPLICABLE** | The decision model has no callable tools. Use `response_format: json_schema`, `strict: true`, and `require_parameters: true`, with exact endpoint support asserted under current official documentation. |
| Delete conditional SQLite allowance | **ACCEPT** | Mandate plain files/NDJSON for the disposable single-in-flight runner. |

## 4. Independent checks performed during synthesis

- Exact scorer arithmetic confirms the maximum one-FN recovery at 30 positives is `2/31 = 0.064516`, below the `+0.08` planning alternative.
- The generator-mixture attack is real: one missed positive out of 30 gives an F1 gap of about `0.01695`; two missed positives give `0.03448`, crossing the `+0.03` boundary. Mechanism quotas are therefore load-bearing.
- The missing-pair construction is real: three `-1` scenarios and fifty-seven `+0.08` scenarios have scheduled mean `0.026`; replacing only the three hard scenarios yields `0.08`, a `+0.054` shift.
- A mean-zero asymmetric two-point distribution with 15% mass at `-1` has SD about `0.420084`, so the old arbitrary `0.40` ceiling did not cover the legal bounded support.
- The old chi-square SD bound is based on approximate normality and is explicitly sensitive to non-normality in [NIST’s standard-deviation interval guidance](https://itl.nist.gov/div898/software/dataplot/refman1/auxillar/sdconfli.htm).
- The render-confound result is real: [Presentation, Not Mechanism](https://arxiv.org/abs/2607.16019) reports that a render-matched control reduces the apparent fine-mechanism residual to roughly `+0.021`–`+0.025` in its evaluated setting.
- The strong-flat comparator precedent is real: [StateFuse](https://arxiv.org/abs/2607.05844) compares typed/conflict-preserving memory with flat multi-value, raw-log, provenance-style, and collapsed baselines under matched resolver and verification policies.
- Current [OpenRouter structured-output documentation](https://openrouter.ai/docs/guides/features/structured-outputs) says endpoint support varies and instructs callers to use `require_parameters: true`; [router metadata](https://openrouter.ai/docs/guides/features/router-metadata) is opt-in and absent on cache hits.

## 5. Resulting r3 architecture

The next design uses two primary packages:

1. **FM — strong flat replay under matched native presentation:** append-only primitive public events, deterministic replay, current flat projection, terminal set, bounded public-ID traversal, and the exact TN-shaped layout with typed/deprecation mechanisms neutralized.
2. **TN — typed native under the same presentation:** immutable evidence, typed lifecycle/currentness/conflict/supersession/dependency relations, and native bounded projection.

On a frozen 25% subset it adds the other two cells of the store × render matrix:

- **F+:** flat replay store through the compact flat render.
- **TF:** typed store through the exact F+ flat render.

Current-only overwrite is an unpaid deterministic ablation. A batched status/abstention probe on the diagnostic subset prevents an action-accuracy null from being misreported as proof that typed continuity has no audit/conflict value; it cannot trigger the primary build verdict.

## 6. What the next council must attack

The next sealed pass must try to break:

1. Whether F+ persistence/replay is now genuinely the strongest cheap deterministic flat mechanism.
2. Whether FM holds presentation fixed without smuggling in typed facts or unfair neutral-field overhead.
3. Whether exact mechanism quotas remove generator-mixture discretion.
4. Whether the joint maximum fixture makes budget selection executable without choosing a winner.
5. Whether reconstruction is information-causal on the artifact.
6. Whether missing-pair tipping prevents route-correlated selection bias.
7. Whether the revised full-support operating-characteristic calibration is executable and affordable.

No paid inference is authorized by this synthesis.
