# MBCX-01 design council packet — round 1

> Packet prose is orientation, not evidence. Byte-check every load-bearing claim against the pinned artifact and sources. This is a **DESIGN / PROPOSE** lane. It is read-only. Do not edit files or run paid inference.

## 0. Artifact and pin

- Artifact under review: `<repo>/MBCX-01-DESIGN-SPEC-r0.md`
- Pinned Git commit: `5c7ccfe72d0aa84141f7296f185b9c022c6fe294`
- Artifact SHA-384: `B1D907E2C7D6B247D109B5E192541442ED07B51EAFA18A28ADCFC418B72494FBCD588B55C0504D4F44ACB2F3333007CE`
- Required local source map: `<repo>/LOCAL-SOURCE-MANIFEST-r1.md` at the commit supplied with this packet.
- Canonical seat prime: `<vault>`

Byte-check the artifact with `git -C <repo> show 5c7ccfe72d0aa84141f7296f185b9c022c6fe294:MBCX-01-DESIGN-SPEC-r0.md`. Do not rely on an unpinned working-tree read when adjudicating a claim.

## 1. Required verdict

Return exactly one top-level verdict:

- `GO`
- `GO-WITH-FIXES(<highest-priority class>)`
- `NO-GO(<deciding reason>)`

Then answer:

1. **WHAT WOULD YOU BUILD?** Give the smallest implementation architecture that can actually answer the experiment.
2. **WOULD YOU DESIGN IT DIFFERENTLY?** Name the alternative and why it is scientifically cleaner, cheaper, or more executable.
3. Is the present artifact implementable without filling unstated design gaps that could change the result?
4. Does it test a real architectural claim, or does it confound memory representation with parsing, write quality, provider behavior, or extra compute?

## 2. Why this exists

Moonwalker needs evidence for or against one narrow proposition before it builds a production Munin memory layer: can bounded, versioned, typed current state plus prospective obligations outperform simpler alternatives under equal model and prompt conditions, especially after reconstruction?

The intended decision is not “does memory help?” It is whether this particular kernel earns engineering over a strong ledger and simple retrieval. A fair negative result must be able to kill or narrow the design.

### Shelf Zero

This artifact should exist only if PM-Bench, AgenticSTS, ordinary context/compaction, lexical retrieval, or another existing harness cannot already answer the same causal question with a small adaptation. Search that question before accepting the custom harness.

### Product fit

MBCX-01 is a standalone laboratory instrument. It is not production Munin, not shared multi-agent memory, and not a security testbed. A surviving mechanism may later become a Moonwalker module; the experiment itself must not accidentally become a shadow production architecture.

### Bigger than the bug

Reject any harness machinery whose main effect is to recreate Moonwalker production controls, a general agent framework, or a full memory platform before the causal question is answered.

## 3. Immutable truths and declared non-claims

### Claimed invariants

1. Private gold never reaches any memory adapter, model prompt, provider request, retrieval index, or arm artifact.
2. Every arm receives the same admitted public observation and common non-memory prompt envelope.
3. Confirmatory comparisons use one pinned model/provider/runtime condition and one fixed memory-payload budget.
4. Exact current state, obligation status, due actions, scope, and provenance are scored mechanically; an LLM judge cannot override them.
5. Each scenario is the clustering/paired unit; decisions inside a trajectory are not independent samples.
6. A result is invalid if the provider changes model/provider, applies an unlogged transform, or silently truncates/compresses context.
7. MBCX-01 does not authorize production integration or paid execution.

### Non-claims

- No claim that general agent memory, personality, emotion, procedural learning, multi-agent sharing, or brain slotting is solved.
- No claim that deterministic structured event admission proves a natural-language write path.
- No claim that an in-process close/reopen proves OS-process crash recovery.
- No claim that a bounded prompt proves bounded total retrieval or maintenance work.
- No hostile actor is assumed. Stale/canceled/wrong-scope material is a scientific validity stressor, not “poisoning.”
- No claim that OpenRouter exposes a hidden model checkpoint or guarantees deterministic output.
- No claim that one model-family result generalizes to other families.

## 4. Claims under review and how they can fail

### C1 — the experiment is the smallest decisive next test

- Claim: a five-arm custom trajectory harness is justified before production Munin work.
- ADVERSARY (scientific): an existing benchmark or a smaller factorial answers the same question.
- REACHES IT VIA: PM-Bench adaptation, AgenticSTS accumulating-context control, or CANTOR's oracle-boundary grid.

### C2 — treatment isolation is real

- Claim: memory representation is the only causal treatment in the confirmatory kernel comparison.
- ADVERSARY (scientific): arm-specific construction quality, schema privilege, output burden, or tool access.
- REACHES IT VIA: Arm D gets deterministic typed admission while Arm B must rewrite a ledger with the decision model; one arm may consume structured event fields or extra calls that another does not.

### C3 — the baseline set is strong enough to kill the idea

- Claim: chronological history, model ledger, FTS5/BM25, and oracle-minimal cover the strongest simple alternatives needed for the first decision.
- ADVERSARY (scientific): provider-native compaction, fresh explicit current state, deterministic ledger, or an adapted PM-Bench scaffold matches Arm D.
- REACHES IT VIA: omitted high-performing ordinary baseline or deliberately weak maintenance path.

### C4 — Inspect AI is a neutral and workable substrate

- Claim: one Inspect sample can safely represent a whole scenario while preserving exact arm isolation and recoverable logs.
- ADVERSARY (scientific/operational): Inspect automatically appends `TaskState.messages`, retries only at completed-sample granularity, injects provider-specific cache markers, or hides request transforms from the eval snapshot.
- REACHES IT VIA: accidental growing conversation, warm cache/state across restarts, mid-sample retry replay, partial artifact reuse, or provider wrapper behavior.

### C5 — OpenRouter can be frozen tightly enough

- Claim: model/provider/parameter/transform controls are sufficient for causal comparison.
- ADVERSARY (scientific): backend routing, unsupported parameter dropping, prompt caching, aliases, or provider transformation.
- REACHES IT VIA: incomplete `provider` allowlist/order, `allow_fallbacks`, `require_parameters`, cache markers, middle-out transform, unrecorded backend metadata, or provider drift over a long sequential run.

### C6 — the statistical plan can support the stated verdict

- Claim: four pilot scenarios, a paired-normal sample-size formula, 24-48 confirmatory scenarios, one run per main cell, and 20% triplicate cells produce decision-grade uncertainty for bounded set-F1.
- ADVERSARY (scientific): unstable pilot variance, bounded/non-normal outcomes, provider drift, order effects, seed heterogeneity, multiplicity, or too few independent trajectories.
- REACHES IT VIA: underpowered or miscalibrated intervals and an arbitrary +0.08 threshold.

### C7 — restart is represented honestly

- Claim: fresh provider conversation plus close/reopen of arm files measures reconstruction.
- ADVERSARY (scientific): same-process caches, retained objects, Inspect task history, or provider prefix cache preserve hidden continuity; failure recovery reruns a whole scenario against dirty artifacts.
- REACHES IT VIA: unreset state surface or idempotence gap.

### C8 — the generated world is valid and non-privileging

- Claim: deterministic scenarios exercise prospective obligations, corrections, dependencies, hidden cues, wrong scopes, and appropriate non-recall without leaking their solution.
- ADVERSARY (scientific): event schemas make Arm D trivial, hidden-channel rules differ by arm, current observations solve tasks, or gold-derived rejection criteria encode answer cues.
- REACHES IT VIA: public/private envelope mistake, serializer asymmetry, generation shortcut, or test contamination.

### C9 — the implementation burden is proportionate

- Claim: Python + SQLite + Inspect is the smallest shelf-first build.
- ADVERSARY (engineering): Inspect adds more lifecycle/state complexity than a direct async HTTP harness; SQLite projection layers reproduce a memory system before testing the premise.
- REACHES IT VIA: framework impedance, resume semantics, debugging surface, packaging/licensing, or unnecessary process-safety code.

### C10 — reproducibility fields are complete without importing production security architecture

- Claim: manifests, hashes, frozen configs, raw outputs, and cleanup reports are sufficient.
- ADVERSARY (scientific/operational): missing arm order, provider time/block, tokenizer/version, wrapper version, environment/library lock, cache state, or price snapshot makes reruns incomparable.
- REACHES IT VIA: incomplete run record. Separately adjudicate whether Moonwalker-owned manifest IDs should use the house SHA-384 posture; do not expand this into seal-chain design.

## 5. Driver's pre-dispatch attack

These are risks, not conclusions. Independently verify them rather than echoing them.

1. **Ledger/D confound:** Arm B's decision model maintains memory while Arm D receives deterministic state transitions. This may test write-path fluency versus a perfect parser rather than ledger versus typed projection.
2. **Inspect hidden history:** Inspect's documented `generate()` appends messages to `TaskState`; the solver must explicitly construct a fresh message list for every decision or the “fresh reconstruction” condition is false.
3. **Inspect cache mutation:** current Inspect documentation says OpenRouter Anthropic routes inject `cache_control` markers by default and those markers do not appear in the `.eval` request snapshot. `cache_prompt=False` and explicit cache-state accounting may be required.
4. **Retry granularity:** `eval-retry` preserves completed samples, but one scenario is one sample. Mid-trajectory interruption may rerun the whole scenario. The arm store therefore needs atomic fresh-run identity or explicit resume semantics; “retryable interrupted evaluations” is not free.
5. **Run order:** the specification does not visibly randomize/interleave arm execution. Sequential arms can confound provider drift, outages, rate limits, or time-of-day behavior with architecture.
6. **Pilot and effect threshold:** four scenarios provide a fragile paired-SD estimate; the +0.08 engineering effect has no explicit cost/value derivation.
7. **Restart label:** same-process close/reopen is a serialization test, not process-cold recovery. The report must use the narrower label unless a subprocess/crash panel is actually added.
8. **Baseline omission:** a deterministic compact obligation ledger and a fresh explicit-current-state baseline may be cheaper and more diagnostic than a model-rewritten TODO ledger alone.
9. **PM-Bench code license:** the repository page did not expose a license in the driver's pass. Treat definitions/paper as prior art; do not copy code or data until licensing is resolved.
10. **Hash posture:** the r0 data model says `payload_hash` and packet hash without an algorithm. If promoted as Moonwalker-owned formats, bind SHA-384; if kept disposable, state that the lab hash is identity-only and non-normative.
11. **Status contradiction:** line 5 calls the architecture approved while the same document says it awaits owner review and is not authorized. Fix the status vocabulary.

## 6. Omission attack required from every seat

Name at least:

- one omitted prior-art comparator;
- one unmeasured confound;
- one implementation footgun that could silently bias results;
- one piece of harness machinery you would delete;
- one missing artifact/test without which you would refuse to run paid inference;
- one way the experiment could produce a persuasive but false positive;
- one way it could kill a useful kernel unfairly.

## 7. Required independent sweep

Use your own web search and primary sources. At minimum cover:

1. PM-Bench and AgenticSTS design, released code, limitations, and licenses.
2. Inspect custom solvers, `TaskState.messages`, OpenRouter provider behavior, cache behavior, retry/resume semantics, logging, concurrency, and checkpointing.
3. OpenRouter provider pinning, parameter enforcement, transforms, router metadata, and model metadata.
4. Statistical design for paired bounded outcomes and pilot-based sample-size estimation.
5. At least two alternative harness architectures or existing eval frameworks.
6. Search terms around prospective memory, obligation/action-timing benchmarks, state-tracking benchmarks, and memory-grounded tool use that could make this design obsolete or narrower.

Report:

- exact query;
- exact opened URL;
- `SEARCHED`, `RECALLED`, or `UNSEARCHED`;
- what changed;
- why you stopped.

No opened source means no source. Snippets are locator evidence only.

## 8. Required output shape

1. Verdict.
2. Pin/byte verification.
3. Sources actually read.
4. Claim scoreboard C1-C10: holds / false / underdetermined.
5. Findings ordered by `P0`, `P1`, `P2`, `P3`, each with exact artifact line(s), mechanism, experimental consequence, and fix class.
6. `WHAT WOULD YOU BUILD?`
7. `WOULD YOU DESIGN IT DIFFERENTLY?`
8. Omission attack.
9. Sweep log.
10. Residual risks and explicit non-claims.
11. Seat capability report: model name, harness, tool/search reach, and limitations.

Do not solve leaf implementation details unless they change architecture or validity. The goal is a design that can answer the question, not a larger checklist.
