# MBCX-01 experiment-specific design council packet — round 2

> This is a **scientific-instrument review**, not a Moonwalker production-security review. Packet prose is a pointer map. Verify load-bearing claims against the pinned artifact, executed probes, and sources opened at origin.

## 0. Artifact and pin

- Artifact under review: `<repo>/MBCX-01-EXPERIMENT-DESIGN-r1.md`
- Pinned Git commit: `7fa45e092bb7db14d85761f65a63b97a3740c65e`
- Artifact SHA-384: `8D8F7B083B32C5CC4B9F682C29D759967D3A71CD4B452DEE96EEC06785189A89A42B1FC95BB864B1D574117BE4729E32`
- Artifact size: `27,182` bytes; `542` lines.
- Supporting local source map: `LOCAL-SOURCE-MANIFEST-r1.md` at the same commit.
- Canonical seat prime: `<vault>`

Read the artifact from the Git object:

`git -C <repo> show 7fa45e092bb7db14d85761f65a63b97a3740c65e:MBCX-01-EXPERIMENT-DESIGN-r1.md`

The working directory contains prior-round seat verdicts and operational receipts. They are outside this sealed first pass. Do not open or seek them. The attack set below is the driver's synthesis of useful prior findings; independently verify it.

## 1. Experiment-specific scope override

The standing council method remains useful for byte discipline, independent web search, prior art, footgun discovery, executable attacks, omission attacks, and proposal quality. Its production-oriented questions are not automatically load-bearing here.

### 1.1 Load-bearing review axes

A finding matters if it can change whether the experiment's positive or negative answer should be believed:

- Causal identification and treatment isolation.
- Strength and fairness of the simple comparator.
- Scenario/world validity and architecture privilege.
- Gold isolation.
- Equal prompt, output, maintenance, retry, and tool budgets.
- Hidden conversation, cache, checkpoint, retry, or resume state.
- Exact model/provider/request condition.
- Arm scheduling and time/order confounds.
- Paired outcome definition, sample size, uncertainty, and stopping rules.
- Mechanical scoring correctness.
- False-positive and false-negative pathways.
- Prior art that already answers the question, narrows it, supplies a stronger baseline, or offers a safer/faster instrument.
- Harness machinery only when it prevents corrupted, irreproducible, or causally ambiguous results.

### 1.2 Non-load-bearing by default

Do not spend review time on these unless you demonstrate a direct, concrete path by which one contaminates the experimental answer:

- Licensing, redistribution, commercialization, or future product incorporation.
- Clean-room implementation.
- Moonwalker production security posture, hostile-actor analysis, prompt-injection defense, FIPS/CNSA posture, or seal chains.
- PR workflow, repository delivery gates, issue tracking, or production rollout.
- Generalized PID ownership, daemon supervision, global cleanup frameworks, or sandbox design.
- Hash-algorithm posture beyond unambiguous local run identity.
- Whether the temporary harness is itself a production-quality Moonwalker component.
- Provider-family variance or multi-provider generalization; Stage A deliberately pins one capable condition.

A mandated section that is not applicable should say `NOT APPLICABLE — NON-LOAD-BEARING` and give one sentence why. Do not manufacture a finding to fill the format.

### 1.3 Prior-art doctrine

The experimental posture is:

> Borrow the mechanism; rerun the claim.

The harness may aggressively reuse accessible generators, scorers, adapters, runners, state machines, and evaluation techniques. The council's job is not to police originality. It is to determine whether existing work:

1. Already answers the causal question;
2. Makes the experiment obsolete or narrower;
3. Supplies a stronger comparator;
4. Exposes a known experimental footgun; or
5. Offers a component that reduces implementation error or cost.

## 2. Required verdict

Return exactly one top-level verdict:

- `GO`
- `GO-WITH-FIXES(<highest-priority scientific class>)`
- `NO-GO(<deciding experimental-validity reason>)`

The verdict answers:

> If Stage A says the typed kernel wins, should we believe the representation caused the win? If it loses, should we believe it received a fair test?

A defect may decide `NO-GO` only if it can plausibly cause a materially false positive, false negative, uninterpretable result, or unaffordable/uncalibrated confirmation. Production niceties cannot decide this verdict.

Then answer:

1. **WHAT WOULD YOU BUILD?** Give the smallest instrument that answers the Stage A question.
2. **WOULD YOU DESIGN IT DIFFERENTLY?** Name the alternative and why it is scientifically cleaner, faster, cheaper, or less ambiguous.
3. Is r1 implementable without filling an unstated gap that could change the experimental answer?
4. Which r0 confounds are actually closed, and which only moved?
5. What must be demonstrated before the first paid pilot call?

## 3. Scientific question and decision boundary

Primary Stage A contrast:

- **Arm L:** deterministic flat current-state/open-obligation ledger.
- **Arm T:** deterministic typed/versioned continuity kernel.

Both receive identical admitted public events and deterministic maintenance. Both produce action-only model output. One exact capable model/provider endpoint is held fixed.

Primary outcome:

`high_stress_set_f1(typed) - high_stress_set_f1(flat_ledger)`

Stage A is allowed to answer only whether the richer representation and deterministic materialization earn engineering under the frozen condition. Natural-language writing, ecological maintenance, retrieval, model-family generality, and production integration are Stage B or later.

## 4. Claimed scientific invariants

Attack each invariant. Do not assume it holds because the artifact states it.

1. Both primary arms receive byte-identical admitted public events.
2. Both primary arms use deterministic maintenance; writer quality is not correlated with representation.
3. Both decision calls use identical action-only output schema and output budget.
4. The only primary treatment is flat versus typed persisted representation and the packet deterministically derived from it.
5. Private gold never reaches either primary artifact, prompt, request, cache, or provider log.
6. The flat ledger is a strong simple comparator, not a deliberately weakened strawman.
7. Confirmatory scenarios require memory, contain enough scored opportunities for the target effect to be meaningful, and do not encode Arm T's ontology as the answer.
8. Exact model/provider endpoint, parameters, cache posture, retries, transforms, and tools remain the same across arms.
9. Arm order is counterbalanced and cannot align with wall-clock/provider state.
10. Scenario is the paired unit; decisions inside a trajectory are not counted as independent samples.
11. The pilot cannot choose a preferred direction, and the confirmatory run cannot be silently underpowered by a cost clamp.
12. Process-cold reconstruction receives only the persisted arm artifact and public cursor.
13. Mechanical scorers, not an LLM judge, decide the task outcomes.
14. A win, kill, or inconclusive result remains inside the artifact's declared non-claims.

## 5. Claims under review

### C1 — Stage A is causally identified

- **Claim:** deterministic flat versus deterministic typed changes representation rather than writer quality, parsing labor, model-call count, or output burden.
- **ADVERSARY:** a hidden arm-specific reducer, serializer, repair path, tool, provenance demand, or maintenance allowance.
- **REACHES IT VIA:** Arm T gets semantically resolved transitions or a perfect materializer while Arm L loses equivalent current information; one arm's output schema or repair budget is harder.

### C2 — Arm L is strong enough to kill the rich kernel

- **Claim:** the flat ledger is the strongest simple deterministic alternative needed for Stage A.
- **ADVERSARY:** a simpler latest-state/open-obligation projection, capped heartbeat ledger, fresh explicit current state, or another ordinary baseline outperforms L without T's machinery.
- **REACHES IT VIA:** Arm L omits fields a competent simple ledger would keep or pays an artificial serialization penalty.

### C3 — Treatment-budget symmetry is real

- **Claim:** memory payload, action output, calls, repairs, tools, retries, and maintenance are matched.
- **ADVERSARY:** the r0 512-token ledger starvation reappears through provenance/state-claim requirements, arm-specific serialization, or maximum-load behavior.
- **REACHES IT VIA:** an exact-tokenizer maximum-load fixture where one arm cannot fit or requires more output/calls.

### C4 — The generated world does not privilege T

- **Claim:** scenarios stress real prospective-memory mechanisms without encoding the typed ontology as the solution.
- **ADVERSARY:** public transition fields pre-resolve status, dependency, scope, or supersession in a shape T consumes directly while L must infer or discard it.
- **REACHES IT VIA:** differential public serializers, gold-derived rejection criteria, current-observation leakage, or hand-authored scenarios that reverse the result.

### C5 — The outcome has useful resolution

- **Claim:** at least 30 high-stress opportunities make `+0.08` a multiple-decision effect rather than a one-item quantum.
- **ADVERSARY:** set-F1 remains lumpy, opportunity counts vary materially, or one scenario family dominates the metric.
- **REACHES IT VIA:** executable metric arithmetic over boundary cases and planned scenario counts.

### C6 — Reconstruction measures the named construct

- **Claim:** a fresh interpreter with only persisted arm state measures process-cold reconstruction.
- **ADVERSARY:** inherited environment, provider cache, hidden files, static singletons, scenario state, or supervisor arguments carry continuity.
- **REACHES IT VIA:** a reconstruction succeeds after deleting/withholding a supposedly required artifact, or fails for reasons unrelated to memory.

### C7 — The runner is experimentally neutral

- **Claim:** the direct runner is thin; Inspect is adopted only after conformance proves it does not add hidden state.
- **ADVERSARY:** message accumulation, local/provider cache, checkpoint warning-and-continue, sample-level retry, eager scheduling, selective reroll, or invisible request mutation.
- **REACHES IT VIA:** official framework behavior or a mock-provider differential between direct and framework paths.

### C8 — One exact model/provider condition is actually frozen

- **Claim:** provider is removed as a variable rather than estimated.
- **ADVERSARY:** base provider slug spans endpoints; account settings merge; aliases roll; parameters drop; transforms or caching mutate prompts; returned metadata cannot prove the requested route.
- **REACHES IT VIA:** current transport documentation or a mock request showing the exact endpoint cannot be bound.

### C9 — Run order and retry identity cannot mimic an effect

- **Claim:** paired, interleaved, counterbalanced order plus clean snapshots prevent wall-clock and selective-retry confounds.
- **ADVERSARY:** arm blocks run sequentially, a retry sees a dirty store, or only bad model outputs reroll.
- **REACHES IT VIA:** schedule inspection, interruption probes, or a failure path that changes the arm artifact before retry.

### C10 — The statistical plan can support win and kill claims

- **Claim:** 12 pilot pairs, conservative variance uncertainty, simulation-based sizing, minimum 48, no maximum clamp, paired bootstrap, and permutation sensitivity are proportionate and sufficient.
- **ADVERSARY:** small-pilot variance still produces unstable or unaffordable `n`; the bootstrap/permutation target differs from the win rule; stability replicates contaminate the primary; confidence rules cannot support the kill margin.
- **REACHES IT VIA:** executed sensitivity simulations over bounded/lumpy outcome distributions.

### C11 — Oracle diagnostics are scoped honestly

- **Claim:** oracle-minimal and oracle-all-relevant diagnose model/task ceilings without contaminating the primary or pretending a gold packet is deployable.
- **ADVERSARY:** the oracle packet transcribes the answer, omits model-helpful redundancy, or is used to excuse a generator defect.
- **REACHES IT VIA:** oracle policy and packet construction that make the decision trivial or paradoxically harder.

### C12 — The instrument is proportionate

- **Claim:** the design contains only machinery needed to generate, run, score, reconstruct, and preserve an interpretable experiment.
- **ADVERSARY:** a framework, database layer, lifecycle subsystem, generalized adapter platform, or Stage B mechanism is being built before Stage A earns it.
- **REACHES IT VIA:** a smaller direct instrument answers the same question with fewer hidden states and less implementation risk.

## 6. Inherited attack set — verify, do not echo

The previous design round surfaced the following potentially useful findings. r1 claims to close or narrow them. Attempt to falsify the closure:

1. **Writer confound:** deterministic T versus model-written ledger did not isolate representation.
2. **Output-cap confound:** Arm B's mandatory rewritten ledger could exceed the shared 512-token cap while other arms emitted only decisions.
3. **Weak comparator:** no strong deterministic simple ledger existed.
4. **History budget not binding:** r0 could call a full-context arm “bounded” without forcing the budget to matter.
5. **Hidden runner state:** Inspect messages, cache, checkpoint, and retry semantics could preserve continuity or selectively reroll cells.
6. **Provider ambiguity:** “one named provider” could cover multiple endpoints or merged account settings.
7. **Missing order control:** arm order could align with time/provider state.
8. **Fragile sizing:** four pilot scenarios plus a `[24,48]` clamp could underpower the experiment while claiming 80% power.
9. **False cold-restart label:** same-process close/reopen was not process-cold reconstruction.
10. **Oracle/gold contradiction:** gold-derived packets were described as never entering a model prompt.
11. **Generator privilege:** T's ontology could be embedded in public structured events and rejection rules.
12. **Production-doctrine leakage:** child registries and multi-step shutdown machinery answered risks the lab did not create.

For each, report `CLOSED`, `PARTIALLY CLOSED`, `OPEN`, or `MOVED`, with the exact r1 mechanism.

## 7. Required independent prior-art and footgun sweep

Use native search first, then Moonwalker locator/fetch/download tools when native search returns snippets, refuses an origin, or misses a regional source. A snippet is not a source. Open the paper, repository, official documentation, standard, or implementation at origin.

Do not confine discovery to US/UK institutions or English-only keywords. Search named institutions, authors, repositories, and benchmark terms across regions, including at least one non-US/non-UK research surface relevant to long-horizon agents, memory, prospective action, state tracking, or evaluation methodology. This is not a country scoreboard; stop when the mechanism space is sufficiently covered.

### 7.1 Question A — has the experiment already been answered?

Search for:

- Prospective-memory agents, delayed intentions, cue/action timing, cancellations, reschedules, and lures.
- Bounded typed memory versus accumulating context or flat state.
- Memory-grounded tool use and long-horizon action benchmarks.
- Externalized state, fresh executors, event sourcing, state machines, and obligation tracking in agents.
- Controlled writer×representation factorials.

Start from, but do not limit yourself to:

- PM-Bench.
- AgenticSTS.
- LongHorizon-Harness.
- Mem2ActBench.
- LongMemEval-V2.
- CAME-Bench/STITCH, MAGE/MemoryArena, Remember When It Matters, and newer directly relevant work found independently.

Decide whether any opened work makes Stage A obsolete, narrower, or differently factored.

### 7.2 Question B — what should be borrowed?

Search for reusable:

- World/scenario generators.
- Deterministic prospective-action scorers.
- Typed state/obligation representations.
- Fresh-message/external-state runners.
- Paired run scheduling.
- Checkpoint and reconstruction patterns.
- Mock-provider conformance testing.

Compare at least two harness paths, such as direct HTTP runner, Inspect, Harbor, OpenAI Evals, tau2-bench, or another current framework. The decision axis is implementation error and hidden experimental state—not originality or distribution.

### 7.3 Question C — framework and transport footguns

Search current primary documentation or code for:

- Message accumulation.
- Local and provider prompt caching.
- Hidden cache markers or request mutation.
- Checkpoint failure policy.
- Retry/resume granularity.
- Eager scheduling and concurrency.
- Exact endpoint selection versus base provider selection.
- Account-level provider-setting merges.
- Fallback defaults, parameter dropping, transforms, aliases, and returned routing metadata.

### 7.4 Question D — experimental-design footguns

Search primary methodological sources for:

- Paired bounded/discrete outcomes.
- Small-pilot variance uncertainty.
- Internal-pilot or blinded sample-size re-estimation.
- Clustered paired bootstrap and paired permutation methods.
- Measurement granularity and effect-size interpretation.
- Counterbalancing and order effects in sequential experiments.
- Synthetic benchmark generator bias and benchmark contamination.

### 7.5 Sweep record

For every search family report:

- Exact query.
- Exact opened URL.
- Section or mechanism that decided it.
- `SEARCHED`, `RECALLED`, or `UNSEARCHED`.
- What changed or confirmed.
- Why further searching was unlikely to change the design decision.

Licensing/distribution analysis is explicitly outside this sweep.

## 8. Required executable/no-cost attacks

There is no implemented MBCX r1 harness yet, so execute what is actually executable and do not pretend a prose review is a runtime test.

At minimum:

1. Verify pin, bytes, and source-manifest availability.
2. Construct maximum-load Arm L and Arm T payload/output fixtures and estimate tokens with at least one appropriate tokenizer; state limitations.
3. Execute metric-granularity arithmetic for 30 high-stress opportunities and adversarial TP/FP/FN states.
4. Execute sample-size sensitivity over at least three plausible paired-SD or lumpy bounded distributions; include a case where the 12-pair pilot misleads.
5. Construct one scenario/event shape that privileges T and show which r1 invariant would catch or miss it.
6. Construct one strong flat-ledger design that could plausibly match T; determine whether Arm L already contains it.
7. If recommending Inspect, show the exact no-paid mock-provider probes required to admit it. If recommending direct HTTP, name the hidden-state and retry liabilities it still has.

Label every conclusion `EXECUTED` or `READ-ONLY`. An unexecuted bypass remains a hypothesis.

## 9. Required omission attack

Name at least:

- One omitted strong simple comparator.
- One hidden confound capable of favoring L.
- One hidden confound capable of favoring T.
- One framework/provider footgun that could silently change the result.
- One way r1 could produce a persuasive false positive.
- One way r1 could unfairly kill a useful typed kernel.
- One piece of machinery you would delete.
- One missing no-paid test without which you refuse pilot inference.
- One prior-art mechanism you would directly borrow.

If an item is genuinely not applicable, say so and why. Do not invent filler.

## 10. Required output shape

1. Top-level verdict.
2. Pin/byte verification.
3. Evidence actually read and probes actually run.
4. Experiment-specific applicability ruling: what production-council doctrine you excluded and why.
5. Claim scoreboard C1–C12: `HOLDS`, `FALSE`, or `UNDERDETERMINED`.
6. r0 closure table for inherited findings 1–12.
7. Findings ordered `P0` through `P3`, each with:
   - exact artifact line/section;
   - mechanism;
   - false-positive or false-negative consequence;
   - fix class;
   - `EXECUTED` or `READ-ONLY`;
   - search label when prior art bears on it.
8. `WHAT WOULD YOU BUILD?`
9. `WOULD YOU DESIGN IT DIFFERENTLY?`
10. Omission attack.
11. Sweep log.
12. Residual risks and explicit non-claims.
13. Seat capability report: model name, harness, local reach, search reach, execution reach, and limitations.

## 11. Review discipline

- Be adversarial about science, not ceremonial about production.
- Do not downgrade a causal defect because the harness is temporary.
- Do not upgrade a production nicety into a causal defect because the standing role card mentions it.
- A prior-art search is valuable even when the answer is “reuse their mechanism and continue.”
- A negative result is useful only if the typed kernel received a fair test.
- A positive result is useful only if the representation, not writer quality, extra compute, hidden state, or provider behavior, caused it.
- Do not solve leaf implementation details unless they change architecture, cost, or experimental validity.
- Do not run paid inference.
- Deliver the entire verdict in-thread. Do not write the verdict to disk; banking is the driver's job.
