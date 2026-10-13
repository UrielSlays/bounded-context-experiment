# MBCX-01 Executable Bounded Obligation Continuity Experiment Design r7

## 0. Status and deciding question

This is an executable preregistration design. It is not an FD/FC/TN harness implementation, a model result, or authorization for paid inference.

The deciding question is whether one logical conductor can preserve exact due-obligation continuity using a bounded decision working set while dormant archive size `H` and active-subject depth `D` vary over frozen finite ranges, which of FD, FC, or TN is the defensible engineering carrier, and whether one frozen model can use the selected packet in one serial cold `A0 -> B -> writer -> A1` episode.

The three conclusions remain separate:

1. **continuity:** at least one candidate is exact and passes registered finite-range physical-work gates;
2. **mechanism engineering:** the FD/FC/TN Pareto set under closed physical accounting; and
3. **conditional model usability:** BC is noninferior to oracle-minimal OM while OM clears the frozen floor.

TN may lose without killing continuity. Model use may fail without killing mechanical continuity. No production, universal asymptotic, cross-model, concurrent-writer, security, persistent-mind, personality, procedural-memory, or coordination-stage claim is made.

## 1. Normative bundle and executable references

At one Git commit, the experiment is governed by this design plus:

- `MBCX-01-STATE-ACTION-CONTRACT-v3.json`;
- `MBCX-01-PACKET-SCHEMAS-v2.json`;
- `MBCX-01-MEASUREMENT-CONTRACT-v2.json`; and
- `MBCX-01-INFERENCE-CONTRACT-v3.json`.

The JSON contracts govern their named domains. `mbcx01_r8_reference.py` is the dependency-free executable transcription. `verify-r8-normative-bundle.py` executes behavioral witnesses over the real artifacts. A static declaration-presence test has no scientific authority.

The five normative artifacts, reference executables, no-paid verification report, and council packet are pinned by Git object ID, byte count, line count, and SHA-384.

## 2. Build-decision challenge and controls

MBCX-01 is not evidence that a special brain object should exist. It is a kill-shot against the narrower hypothesis that exact selective obligation continuity can remain bounded by the active decision frontier rather than total dormant history.

Controls are full or rolling context where feasible; exact ordinary files; structured reconstruction; BM25; sparse+dense retrieval; namespaces or blackboard state; oracle-minimal and oracle-all-relevant packets; and deliberately unbounded raw-replay FD. If a simpler control matches exactness, reconstruction, isolation, and registered physical cost, the special mechanism earns nothing.

## 3. Canonical world and candidate mechanisms

The canonical scientific world is an append-only semantic journal plus immutable payloads. Generator, independent reference reducer, gold enumerator, packet reference, candidate producers, scorer, and inference implementation are separate components with distinct source hashes.

- **FD:** indexed derivation from journal and payload state.
- **FC:** derived materialization including segmented snapshot plus bounded tail.
- **TN:** typed derived relations, conflicts, and provenance.

Candidate projections are derived, disposable, and reconstructible. A comparator earns a fourth mechanism label only if it exposes a public semantic object unavailable to all three; branding or storage strategy is insufficient.

Candidate source, build, dependency, and closed configuration hashes freeze before confirmatory scenarios or gold are generated. A candidate child cannot read generator code, reducer, gold, reference packets, another candidate, source tree, ambient directory, or network.

## 4. Canonical state, actions, and writer

The v3 state/action contract freezes bitemporal cuts, canonical safe integers and times, scope, facts, obligations, dependencies, handoffs, seventeen semantic event types, action identity, the writer, and a separate provider-call ledger.

### 4.1 Opaque action identity

An obligation action is `ACT.` plus uppercase SHA-256 of RFC 8785/JCS over a closed `ActionIdentityV1` containing `scope_id` and `obligation_id`. Public action IDs are never delimiter-parsed. The cut-bound action catalog maps the opaque ID to its structured target. This makes `(scope=S:A, obligation=B)` different from `(scope=S, obligation=A:B)`.

### 4.2 Total transition table

Every semantic event type declares a closed payload, legal prestate, deterministic effect, exact duplicate behavior, and frozen illegal result. The executable reference runs every ordered event-type pair: 17 by 17 equals 289. Each fixture records prestate, first result, intermediate state, second result, and final state on a shared scenario and, where meaningful, a shared entity.

### 4.3 Atomic proposal semantics

Every proposed child validates independently against the immutable originating cut bound into `TaskPacketV3`. A provisional child cannot make a sibling legal. An obligation newly unblocked by a committed child requires a later packet and decision.

The writer performs schema, hash, originating-cut, scope, availability, independent transition-legality, and idempotency checks. It then atomically appends every child in UTF-8 action-ID order plus one commit terminal, or no child and exactly one rejection terminal. No outside semantic event interleaves before the immediate A1 cut.

## 5. Provider call ledger and recovery

Each call key is `(scenario_id, condition, node)`, where node is A0, B, or A1. The non-semantic call ledger follows:

```text
PREPARED -> DISPATCHED -> RESPONSE_DURABLY_RECORDED
                       -> PROVEN_PRE_ACCEPT_FAILURE
                       -> ACCEPTANCE_AMBIGUOUS
```

Immutable response bytes and their hash become durable before parse. Recovery reuses those bytes and never resamples. A retry is legal only from `PROVEN_PRE_ACCEPT_FAILURE`. A crash or disconnect after dispatch without a contractual receipt is `ACCEPTANCE_AMBIGUOUS`, makes the complete six-call pair missing, and cannot retry unless the frozen provider route documents idempotency-token binding over every request parameter.

## 6. Closed packets, DAG, and scoring

`DecisionPacketV3`, `A0ResultV1`, `TaskPacketV3`, `WorkerHandoffV3`, and `A1ResultV1` are closed JSON Schema 2020-12 objects. Each decision object is discriminated by kind and has a closed fields object. No condition label, free-text reasoning, transcript, scratch space, arbitrary config, or unbounded array reaches the model.

Packet hash is uppercase SHA-384 over JCS of the complete packet with `packet_hash` omitted. Served-input hash covers the exact padded bytes. A constructed maximum schema-valid packet must fit within the frozen 65,536-byte envelope.

Each condition executes three accepted calls:

1. A0 receives `DecisionPacketV3` and emits only `A0ResultV1`.
2. The deterministic conductor resolves the selected action through the catalog and builds `TaskPacketV3`.
3. B receives only `TaskPacketV3` and emits `WorkerHandoffV3`.
4. After response journaling, the deterministic writer commits or rejects.
5. A1 receives a cold reconstructed `DecisionPacketV3` and emits `A1ResultV1`.

`PROPOSE` requires at least one proposed action. `ABSTAIN` and `REJECT` require zero. Exact scoring is:

- A0 correct iff the selected action equals the unique frozen gold;
- B correct iff its valid proposal commits the target exactly once;
- A1 correct iff its selected set equals independently recomputed post-commit gold; and
- condition success iff A0, B, and A1 are all correct.

Schema-invalid model output is observed condition failure, not transport missingness. BC and OM yield one paired binary outcome.

## 7. Frozen workloads and confirmatory cohort

Stage 1 uses the six frozen motifs: correction/restoration, obligation lifecycle, dependency reversal, cross-scope collision, delegation/idempotent handoff, and mixed delayed continuity. Generator, reducer, scorer, and red-candidate hashes freeze before execution.

For Stage 2, after candidate source/build/configuration freeze, generate eighty unique scenario IDs per motif. For each scenario:

1. UTF-8 sort its unique cut IDs;
2. select exactly one cut by SHA-256 over an exact 8-byte-length-framed tuple of scenario ID, every sorted cut ID, and `stage2-cut-r8`;
3. apply eligibility to that chosen cut only; and
4. sort eligible unique scenarios by a separate length-framed retention hash and retain the first 64 per motif.

Eligibility requires exactly one mounted critical due obligation and at least one non-gold action. A shortfall is `DESIGN_OR_IMPLEMENTATION_FAIL`. The final manifest has 384 globally unique scenario IDs, one cut each. All exclusions, motifs, difficulty strata, and selection hashes are published.

The model estimand is conditional on this frozen eligible manifest. No unbiased-sampling claim is made.

## 8. Mechanical exactness and reconstruction gates

Across every deterministic scenario, cut, required axis cell, mandatory trace, and red candidate, a hard failure is any lost due obligation, wrong-scope admission or gold, stale resurrection, duplicate effect, reducer/action/scorer/packet/reconstruction disagreement, taint, unregistered read or work, hidden fallback, or undeclared overflow.

A fresh sanitized child must:

- fail on withheld, corrupt, or nonce-only artifacts;
- survive source-directory rename;
- swap decoded state when artifacts are swapped;
- change only causally affected output after a field mutation; and
- rebuild projection and packet bytes identically from the canonical journal.

Every descendant PID is captured, charged, awaited, terminated if required, and verified absent. No result from these gates is fabricated by the preregistration.

## 9. Finite-range measurement design

The boundedness claim is registered physical work over frozen finite ranges, not a theorem for unbounded H or D.

- `H = [128, 1024, 10000, 100000]`;
- `D = [1, 4, 16, 64, 256]`; and
- `F = [1, 4, 16, 64, 256]`.

At `F=16`, execute the full H-by-D Cartesian product: twenty unique cells, including the previously absent interior `(H=10000,D=64)`. Retain the separate F curve at `H=100000,D=16`.

The storage backend, rollback-journal mode, and 4096-byte database/filesystem page size are frozen. The closed catalog charges source, artifact, filesystem, and database bytes; records; pages; dependency/decode/materialization operations; root and child CPU instructions and CPU time; peak RSS and allocated bytes; and implementation/fallback branches.

Every unit-total range maximum is strictly less than the sum of its per-counter maxima. Counter splitting, renaming, or new unregistered work fails. Red candidates cover the interior hotspot, low-slope archive-linear work, unregistered CPU work, counter splitting, page-size substitution, and a logical lookup hiding a physical scan.

The engineering result is a Pareto set over exactness, registered physical work, maintenance, cold p95, artifact bytes, rebuild time, and branches. Carrier selection is separately labeled and has no scientific authority.

## 10. Conditional model inference

### 10.1 Estimands and method

In the frozen 384-scenario SHA-256 order, the paired delta stream is `BC_i-OM_i`; the OM stream is `OM_i`. Scenario conditional means may vary arbitrarily and within-pair dependence is unrestricted.

The primary confidence sequence is the exact-mixture empirical-Bernstein construction in Proposition 3.1 of Chugg and Ramdas (2025), with `kappa=0.25` and alpha 0.025 per stream. Delta is transformed to `[0,1]` and mapped back. Its analytic integral and an independent 16,384-panel Simpson transcription must agree within `1e-9` at interval endpoints.

No common-mean assumption or fixed-look Bonferroni correction is used. The method's time-uniform guarantee covers the registered running average of heterogeneous conditional means.

### 10.2 Decision timing

The n=96 and n=192 prefixes are diagnostic and cost telemetry only. They never bind a scientific branch about the complete manifest. The only scientific decision is at n=384:

- **promote:** delta lower > -0.10 and OM lower >= 0.80;
- **model/interface fail:** delta upper < -0.10 and OM lower >= 0.80;
- **model/interface ceiling:** OM upper < 0.80; or
- **inconclusive/underfunded:** otherwise.

Transport inconclusive and deterministic design/implementation failure take precedence.

### 10.3 Missingness

Any unresolved transport state in one of a scenario's six calls makes the entire pair missing. Through seven missing pairs, jointly enumerate all paired completions from `{00,01,10,11}^m` at the exact missing positions. A scientific branch is reported only if invariant across all completions. Eight missing pairs, or any branch variation, is `TRANSPORT_INCONCLUSIVE`. There is no substitution or resampling.

### 10.4 Synthetic operating characteristics and cost

Before paid authorization, execute the nine valid paired-probability cells with 10,000 synthetic replicates each using the frozen SHA-256 counter stream and inverse-CDF sampler. Publish branch frequencies, interval widths, reachability, inconclusive rates, seeds, implementation hash, and cost. These draws are instrument validation, never model evidence.

Because no scientific early stop exists, 384 complete pairs require exactly 2,304 accepted calls and 768 cold reconstructions before any proven pre-acceptance retry. Maximum and expected accepted calls are both 2,304.

## 11. Transport readiness and authorization

The call ledger distinguishes pre-accept failure from unknown acceptance. Transport reliability is assessed with a frozen one-sided exact Clopper-Pearson 95% upper confidence bound for each registered endpoint failure mode and a dependence-safe union bound across six call positions. The independence calculation `1-(1-0.02)^(1/6)` is published only as orientation and does not decide the gate.

A route soak is called no-paid only if the selected provider route offers a genuinely zero-price primitive. Otherwise its endpoint, model snapshot, maximum tokens, prices, attempt count, and ceiling belong in the later paid authorization manifest.

No paid call occurs without separate owner authorization naming endpoint, provider, snapshot, tokenizer, maximum accepted calls, retry semantics, token maxima, time, prices, reconstructions, and dollar ceiling.

## 12. No-model gates

1. **Bundle:** five committed pinned artifacts, executable verifier, scoped claims, and no stale pins.
2. **State:** total transition table, 289 executed ordered pairs, collision-free actions, atomic writer, and ambiguous-acceptance witness.
3. **Packets/cohort:** five closed schemas, exact scorer, maximum envelope, source freeze, 480 generated unique scenarios, one cut each, and 384 retained unique IDs.
4. **Mechanics:** independent reducer/enumerator, FD/FC/TN parity, isolation, reconstruction, all 20 H-by-D cells, F curve, closed counters, and all red candidates.
5. **Inference:** analytic/quadrature parity, terminal-only decision, prefix reversal, 16,384 seven-missing completion vectors, deterministic OC, and explicit cost.
6. **Authorization:** frozen route/reliability/prices and separate owner approval.

Failure blocks the next stage. No unregistered mid-run fix is allowed.

## 13. Decisions and non-claims

Primary decisions are:

- `DESIGN_OR_IMPLEMENTATION_FAIL`;
- `BOUNDED_CONTINUITY_FALSIFIED`;
- `BOUNDED_CONTINUITY_SURVIVES` with Pareto set; and
- conditional inference: promote, model/interface fail, model/interface ceiling, transport inconclusive, or inconclusive/underfunded.

No result is a persistent mind, latent transfer, universal memory, production readiness, hostile-box validation, or coordination-stage success.
