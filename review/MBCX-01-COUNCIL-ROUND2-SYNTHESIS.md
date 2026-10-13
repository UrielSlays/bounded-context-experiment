# MBCX-01 Council Round 2 Synthesis

**Date:** 2026-08-11

**Status:** Round complete; r1 is not authorized for pilot

**Reviewed design:** `MBCX-01-EXPERIMENT-DESIGN-r1.md@7fa45e092bb7db14d85761f65a63b97a3740c65e`

## Bottom line

The experiment idea survives. The r1 implementation does not.

All three independent seats agreed that the typed arm was still bundled with a better packet-selection/materialization policy. A typed-arm win could therefore be caused by ordinary scope, due-date, terminal-state, and relevance filtering rather than by versioning, conflict preservation, provenance, or typed dependency structure. This is a scientific attribution defect, not a product-security or licensing issue.

The seats also converged on three additional pre-pilot blockers: the high-stress F1 estimand is underspecified, the legal workload has minima but no maxima, and the sample-size procedure is not executable as written. Codex found the strongest statistical defect: r1 powers a confidence interval against zero but separately requires the observed mean to clear `+0.08`. When the true effect is exactly `+0.08`, the probability that the observed mean is at least `+0.08` approaches 50%, not 80%, regardless of sample size. The win rule and the power target therefore answer different questions.

## Independent verdicts

- **Opus 5:** `GO-WITH-FIXES`, with two P0s: selection-policy bundling and absence of binding primary-arm budget pressure.
- **GPT-5.6 Sol:** `GO-WITH-FIXES(COMPARATOR-PARITY)`, with a strong-flat materializer, exact scorer, maximum workload, and exact sample-size method required before pilot.
- **Codex exec:** `NO-GO` for r1 because the confirmatory decision rule is not powered for the declared win/kill claims; it independently reproduced the comparator, metric, workload, reconstruction, and transport concerns.

The severity labels differ, but the technical core does not.

## Findings accepted into r2

1. **Replace weak flat serialization with the strongest cheap flat materializer.** The flat arm receives current-scope restriction, terminal suppression, due/near-due filtering from its explicit fields, direct-prerequisite inclusion, stable ordering, and deterministic budget handling.
2. **Name the treatment honestly.** The primary contrast is a typed continuity package versus the strongest flat deterministic package. It is not called pure representation isolation.
3. **Add a typed-store/flat-view mechanism diagnostic.** On a frozen subset, the typed persisted store is rendered through the same flat packet schema. This separates typed persistence value from typed packet-exposure value without burdening the full primary run with a third arm.
4. **Remove the T-favored response burden.** The primary model output contains only decisions and channel queries. `provenance_ids` and explanatory state claims are not mandatory primary outputs.
5. **Freeze the scorer.** High-stress F1 is micro-aggregated over `(decision_step, action_id)` pairs; empty gold/prediction decisions contribute no TP/FP/FN; at least 30 gold-positive pairs and at least 20 explicit lure exposures are required per scenario.
6. **Freeze a bounded workload envelope.** Steps, obligations, simultaneous live rows, scopes, dependency width/depth, text length, actions, and fan-out all receive maxima. “Maximum load” becomes constructible.
7. **Make boundedness real before inference.** A deterministic pre-run budget-selection rule chooses from a small declared candidate set using the exact tokenizer. Raw/unfiltered state must exceed the selected budget on pressure seeds, while both valid native packets must exercise substantial budget pressure without silent truncation.
8. **Add stresses that typed history can uniquely answer.** Retraction of correction and retraction of cancellation are mandatory, and every declared update mechanism must appear in every confirmatory scenario.
9. **Repair the decision rule.** The non-worthwhile boundary is `+0.03`; the design alternative is `+0.08`. Win requires the lower 95% confidence endpoint to exceed `+0.03`, not an observed mean of at least `+0.08`. Kill requires the upper endpoint to be below `+0.03` or a declared harm/failure condition.
10. **Calibrate the complete rule.** Sample size is the maximum needed for win power at true `+0.08`, kill power at true `0`, interval coverage, and a 95% one-sided pilot-SD upper bound, with rare-tail/lumpy distributions retained in the simulation envelope.
11. **Keep the pilot external.** The internal-pilot suggestion is not adopted. This is a new scientific instrument; the first 12 paid pairs may expose implementation defects and should not silently become confirmatory data.
12. **Delete the Inspect branch from Stage A.** A thin direct runner is the only substrate. This removes accumulated-message, adaptive-concurrency, checkpoint, and retry surfaces instead of building tests merely to disable them.
13. **Tighten transport identity.** OpenRouter is allowed only if exact endpoint, account/request provider intersection, response cache, transforms, fallbacks, parameters, and routing metadata pass fail-closed conformance. Otherwise use direct provider transport.
14. **Tighten retry identity.** Only provably pre-dispatch failures may retry. An ambiguous post-send failure invalidates the whole pair under a frozen reserve-seed rule; malformed schema is a primary failure, not a rescued primary result.
15. **Make process-cold reconstruction falsifiable.** The cursor is capability-limited and cannot replay history. Artifact-withheld/corrupted reconstruction must fail; artifact-present reconstruction must survive removal of unrelated ambient files and variables.
16. **Freeze oracle construction and answer separation.** Oracle packets may contain only public facts/relationships needed for reasoning and may not transcribe due labels or the target action set.
17. **Log information density.** Tokens, records, required closure, and payload utilization are reported together so a typed arm cannot hide a density tradeoff behind equal token caps.
18. **Add the explicit non-claim.** Stage A does not establish superiority over BM25/vector retrieval, learned controllers, natural-language writers, or provider-native compaction.

## Findings not adopted verbatim

- **Add the original dump-everything flat arm to every primary scenario:** rejected as unnecessary paid inference. Prior art already establishes that indiscriminate exposure and selection are separable. The owner-facing question is whether typed continuity beats a competent simple system, so the primary comparator is the strong flat package. A typed-store/flat-view subset is the more useful third condition.
- **Hard-code a 1,500-token budget now:** rejected because the exact model, tokenizer, wrapper, and final record schemas are not frozen. r2 uses a deterministic candidate-budget selection gate before any paid call.
- **Use a blinded internal pilot:** rejected for this revision. Recovering 12 scenarios is less valuable than keeping debugging/engineering observations out of confirmation.
- **Adopt provenance-heavy LongHorizon-Harness records wholesale:** rejected as too close to the treatment boundary. The flat arm may keep one public source ID per row for parity, but it does not gain provenance closure, version chains, or typed historical traversal.
- **Add lexical/vector retrieval to Stage A:** rejected as scope expansion. Retrieval remains a later comparator and an explicit non-claim.

## Authorization consequence

`MBCX-01-EXPERIMENT-DESIGN-r1.md` is sealed as a reviewed but superseded design. No paid pilot is authorized from r1. The next admissible artifact is r2 plus a fresh experiment-specific council pass. Implementation planning remains separate from harness implementation, and paid inference still requires an owner-approved frozen model/provider/cost manifest.

## Banked seat records

- `MBCX-01-SEAT1-OPUS5-VERDICT-r2.md`
- `MBCX-01-SEAT2-CHATGPT-SOL-VERDICT-r2.md`
- `MBCX-01-SEAT3-CODEX-VERDICT-r2.md`
- `MBCX-01-SEAT3-CODEX-EXEC-r2.complete.json`
