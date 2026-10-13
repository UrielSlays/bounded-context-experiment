# MBCX-01 Answerable Bounded Obligation Continuity Experiment Design r8

## 0. Status, question, and decision order

This is an executable preregistration and instrument-validation bundle. It is not an FD, FC, or TN implementation, a model result, or authorization for paid inference. Its retained verification uses zero paid calls and is not experiment evidence.

The original question is unchanged: can one logical conductor preserve exact due-obligation continuity with physical work bounded by the active decision frontier across the complete frozen ranges of dormant history `H`, active depth `D`, and fan-out `F`; which of FD, FC, or TN is the defensible engineering carrier; and can one frozen model use the resulting bounded-context packet without materially underperforming an independently constructed oracle-minimal packet in one serial cold `A0 -> B -> writer -> A1` episode?

The conclusions stay separate:

1. **continuity:** at least one candidate is exact and passes every registered finite-range physical-work gate;
2. **mechanism engineering:** the FD/FC/TN Pareto set under closed physical accounting, with carrier selection separately labeled; and
3. **conditional model usability:** bounded context BC is noninferior to oracle-minimal OM while OM clears the frozen performance floor.

The terminal precedence is `DESIGN_OR_IMPLEMENTATION_FAIL`, then `TRANSPORT_INCONCLUSIVE`, then the scientific branches. Transport trouble cannot hide a locally known broken instrument. If every candidate fails exactness or boundedness, `BOUNDED_CONTINUITY_FALSIFIED` is an acceptable answer. The design must not narrow the question or tune a statistical control to manufacture success.

## 1. Normative bundle and authority

At one Git commit, the five normative artifacts are:

- `MBCX-01-EXPERIMENT-DESIGN-r8.md`;
- `MBCX-01-STATE-ACTION-CONTRACT-v4.json`;
- `MBCX-01-PACKET-SCHEMAS-v3.json`;
- `MBCX-01-MEASUREMENT-CONTRACT-v3.json`; and
- `MBCX-01-INFERENCE-CONTRACT-v4.json`.

The JSON contracts govern their named domains. `mbcx01_r9_oracle.py` and `mbcx01_r9_reference.py` are deliberately different executable transcriptions. `verify-r9-schema-ajv.mjs` authenticates and executes the frozen JSON Schema validator runtime closure. `verify-r9-normative-bundle.py` executes behavioral, differential, mutation, numerical, and synthetic witnesses over the real artifacts. A declaration-presence test has no scientific authority.

The council packet pins every governing and supporting artifact by commit, Git blob, LF byte count, line count, and SHA-384. Reconstruction operates from committed Git objects rather than trusting working-tree bytes.

## 2. Build-decision challenge and controls

MBCX-01 is not evidence that a special brain object should exist. It is a kill-shot against the narrower hypothesis that exact selective obligation continuity can remain bounded by the active decision frontier instead of total dormant history.

Simpler controls remain eligible to win: full or rolling context where feasible, ordinary exact files, structured reconstruction, BM25, sparse+dense retrieval, namespaces or blackboard state, oracle-minimal and oracle-all-relevant packets, and deliberately unbounded raw replay. If a simpler control matches exactness, isolation, reconstruction, and registered physical cost, the special mechanism earns nothing.

The candidate families are:

- **FD:** indexed derivation from the canonical journal and payload state;
- **FC:** derived materialization including a segmented snapshot plus bounded tail; and
- **TN:** typed derived relations, conflicts, and provenance.

Candidate projections are derived, disposable, and reconstructible. A fourth label requires a public semantic object unavailable to all three; branding or storage strategy is insufficient.

## 3. Canonical state and independent semantics

The canonical scientific world is an append-only semantic journal plus immutable payloads. Each event uses a closed `EventEnvelopeV1` with event and scope identities, semantic operation, idempotency key, sequence, observed and valid times, originating cut, and a closed event-specific payload.

Seventeen event types cover facts, corrections and retractions, obligation lifecycle, rescheduling, delegation, dependencies, handoffs, and responses. Every event type names a guard, effect, legal prestate, exact duplicate behavior, and frozen illegal result.

Two implementations must agree:

- the reference projects an event journal; and
- the oracle dispatches direct immutable state transformations.

The verifier executes every ordered event-type pair, `17 x 17 = 289`, and compares result plus complete state. It separately executes rescheduling, delegation, exact duplicate replay, conflicting idempotency reuse, and a three-node dependency cycle. Named mutants delete reschedule or delegation effects, substitute payload-only identity, suppress effects after recording, ignore the originating cut, or detect only two-cycles. Every mutant must die.

This is instrument validation, not proof of the future FD/FC/TN candidates. Candidate implementations and the gold path remain separate components with separate source hashes.

## 4. Actions, writer, and provider-call recovery

An obligation action is `ACT.` plus uppercase SHA-256 over the closed JCS `ActionIdentityV1` containing `scope_id` and `obligation_id`. Public action IDs are opaque and never delimiter-parsed. The cut-bound action catalog maps each ID to a structured target.

Every proposed child validates independently against the immutable originating cut in `TaskPacketV3`. A provisional child cannot make a sibling legal. The writer performs schema, hash, cut, scope, availability, transition-legality, and idempotency checks, then atomically appends all children in UTF-8 action-ID order plus one commit terminal, or appends no child and one rejection terminal. No outside semantic event interleaves before the immediate A1 cut.

Each provider call is keyed by `(scenario_id, condition, node)`. Immutable response bytes and their hash become durable before parse. Recovery reuses those bytes and never resamples. Retry is legal only after a proven pre-acceptance failure. Unknown acceptance makes the full six-call pair missing unless a separately frozen provider contract binds an idempotency token to every request parameter.

## 5. Closed packets, builders, and exact scoring

`DecisionPacketV3`, `A0ResultV1`, `TaskPacketV3`, `WorkerHandoffV3`, and `A1ResultV1` are closed Draft 2020-12 schemas. The actual Ajv 8.20.0 code and its four transitive dependency trees are content-pinned and authenticated before validation; the semantic validator then enforces identity and cross-record meaning that JSON Schema alone cannot express.

Packet hash is uppercase SHA-384 over canonical packet bytes with `packet_hash` omitted. The semantic gate rejects duplicate object or action IDs, forged action hashes, unresolved catalogs, invalid `NO_ACTION`, unresolved prerequisites or targets, scope mismatches, canonical-object changes, packet-hash changes, and byte-envelope overflow.

BC and OM share the scenario, cut, action universe, neutral schema, instructions, field descriptions, ordering, output schema, fixed 65,536-byte served envelope, and transport settings. They differ only in the source of public semantic object IDs:

- BC renders the candidate's frozen selected IDs; and
- OM renders the independent gold enumerator's causal read-set.

Neither builder receives a condition label, gold label, due annotation, answer ID, free text, transcript, or scratch space. A syntactically valid packet may be too large; `PACKET_ENVELOPE_EXCEEDED` is then a pre-dispatch design failure rather than a model result or paid call.

Each condition runs A0, deterministic task construction, B, deterministic writer, cold reconstruction, and A1. A0 passes only on the unique frozen gold action. Stage-2 B passes only if its valid proposal is exactly the singleton target and the writer commits exactly that singleton once with no extra child. A1 passes only if its selected set exactly equals independently recomputed post-commit gold. The paired binary condition succeeds only if all three pass. Schema-invalid model output is observed failure, not transport missingness.

## 6. Source, generator, and cohort freeze

The generator specification, distribution parameters, gold enumerator, eligibility evaluator, and their hashes freeze before candidate implementation is inspected. Candidate source, build, dependency, and closed configuration hashes freeze next. Only then is a fresh confirmatory seed minted. Candidates cannot read that seed, generator code, reducer, gold, reference packets, another candidate, ambient source tree, or network.

The six motifs are correction/restoration, obligation lifecycle, dependency reversal, cross-scope collision, delegation/idempotent handoff, and mixed delayed continuity. Generate 160 unique scenario IDs per motif, for 960 total.

For every scenario, choose exactly one cut by the frozen length-framed hash before eligibility. Eligibility is recomputed from canonical state at that cut. It requires exactly one mounted, open, critical obligation due by the cut's valid time; that obligation's completion action must be the unique gold action; and at least one distinct non-gold action must be available. Any supplied eligibility Boolean is discarded. Retain the first 128 eligible unique scenarios per motif by a separate frozen retention hash. A shortfall or global duplicate is a design failure.

The final 768-scenario estimand is conditional on this frozen eligible retained manifest. All exclusions, chosen cuts, recomputed reasons, motifs, difficulty strata, and hashes are published. No unbiased-sampling claim is made.

## 7. Mechanical exactness and reconstruction

Across every deterministic scenario, cut, required axis cell, mandatory trace, and red candidate, hard failure includes a lost due obligation, wrong-scope admission or gold, stale resurrection, duplicate effect, state/action/scorer/packet/reconstruction disagreement, taint, hidden work, fallback, or undeclared overflow.

A fresh sanitized child must fail on withheld, corrupt, or nonce-only artifacts; survive source-directory rename; swap decoded state when artifacts are swapped; change only causally affected output after field mutation; and rebuild projection plus packet bytes identically from the canonical journal. Every descendant process is captured, charged, awaited, terminated if required, and verified absent.

These gates define what the future harness must execute. Passing the preregistration's reference witnesses does not fabricate a candidate result.

## 8. Complete finite-range physical-work measurement

The claim concerns registered physical work over frozen finite ranges, not an asymptotic theorem:

- `H = [128, 1024, 10000, 100000]`;
- `D = [1, 4, 16, 64, 256]`; and
- `F = [1, 4, 16, 64, 256]`.

Every candidate runs the full Cartesian product: exactly 100 unique cells. No plane or curve substitutes for this coverage.

The backend is SQLite rollback-journal mode on local NTFS with a 4096-byte database page. The closed catalog separately charges source, artifact, filesystem, and database read/write bytes; records; read/write pages; dependency, decode, and materialization operations; root and child CPU instructions and CPU time; peak RSS and allocated bytes; and implementation and fallback branches.

At each literal counter row the evaluator enforces exact cell coverage, the closed counter set, nonnegative safe integers, absolute maxima, per-counter conditional H/D/F ranges, same-unit totals, registered shape gates, page size, descendant accounting, and absence of unregistered work. Page counters are not independently asserted: `PAGES_READ=ceil(DATABASE_BYTES_READ/4096)` and `PAGES_WRITTEN=ceil(DATABASE_BYTES_WRITTEN/4096)`.

Every red candidate produces real rows over all 100 cells and is judged by the evaluator rather than by its declared expected label. The set includes an H-D-F interior hotspot, `10*H` root CPU instructions that must fail the H-shape gate despite a modest slope, hidden child CPU, counter splitting, page-size substitution, a logical lookup backed by physical scan, and page/byte mismatch.

The engineering output is an exactness-filtered Pareto set over registered physical work, cold p95, artifact bytes, rebuild time, maintenance, and branches. Carrier selection remains separately labeled and has no scientific authority.

## 9. Conditional model inference

### 9.1 Estimands and exact mixture interval

In frozen 768-scenario order, delta is the average conditional mean of `BC_i-OM_i`; OM is the average conditional mean of `OM_i`. Scenario conditional means may vary arbitrarily and within-pair dependence is unrestricted. Future provider randomness is unavailable at the current call.

The primary interval is Proposition 3.1's exact-mixture empirical-Bernstein confidence sequence from Chugg and Ramdas, with alpha 0.025 per stream. Delta is transformed into `[0,1]`, inverted, and mapped back. The common-mean assumption is false.

`kappa=0.25` is frozen because the source authors present it as their default, not because it makes MBCX-01 look favorable. In plain language, kappa changes how wide the caution band is for different observed patterns; it does not change the observations. The report therefore publishes nonbinding terminal sensitivity at 0.10, 0.15, 0.25, 0.50, and the uniform-mixture limit. The primary branch never changes settings after seeing outcomes.

The analytic integral, 16,384-panel binary64 Simpson quadrature, and a precision-60 Decimal 4,096-panel quadrature must agree within `1e-9`. Reference vectors freeze every low-discord pair position. For 768 zero deltas, the mapped delta half-width is `0.028724411075760736` at kappa 0.25.

### 9.2 One scientific look

Only n=768 has a scientific interval. At n=96, n=192, and n=384 the system may report completed calls and projected cost, but no interval or branch. At 768:

- promote if delta lower is greater than -0.10 and OM lower is at least 0.80;
- model/interface fail if delta upper is below -0.10 and OM lower is at least 0.80;
- model/interface ceiling if OM upper is below 0.80; or
- inconclusive/underfunded otherwise.

### 9.3 Missingness

Any unresolved transport state in one of a scenario's six calls makes the whole BC/OM pair missing. Through seven missing pairs, enumerate all paired completions from `{00,01,10,11}^m` at the exact missing positions. Report a scientific branch only if invariant across all completions. Eight missing pairs or any branch change is transport inconclusive. There is no resampling or substitution.

### 9.4 Honest synthetic operating characteristics

Before paid authorization, run 10,000 deterministic synthetic replicates per registered cell with the frozen SHA-256 counter stream and inverse-CDF sampler. These are instrument operating characteristics, never model evidence.

The curve crosses negative deltas -0.25, -0.12, and -0.10 with OM marginals 0.80, 0.85, and 0.95. It also retains equal-effect, below-floor, positive-delta, high-discordance, low-discordance, and the practical interface-failure alternative delta=-0.20 with OM=0.90. Publication includes every branch count and interval-width summary; an OM=0.95 cell cannot stand in for near-floor power.

The 384-pair design was rejected after its own OC map showed only about 56% promotion for equal performance at OM=0.90, about 50% interface-failure detection at delta=-0.20/OM=0.90, and about 39% ceiling detection at OM=0.70. A frozen compact sizing comparison at n=384, 512, 768, and 1024 selected the smallest tested sample expected to clear 90% at all registered practical alternatives: n=768. The retained 10,000-replicate run must confirm that target for equal and low-discord promotion at OM=0.90, interface failure at delta=-0.20/OM=0.90, and ceiling at OM=0.70. Exact-cutoff and near-cutoff cases remain an honest indifference region rather than a promise of decisiveness.

Because only n=768 decides, 768 complete pairs require exactly 4,608 accepted scientific calls and 1,536 cold reconstructions before any proven pre-acceptance retry. The extra 2,304 calls buy useful power at the registered practical alternatives; they do not guarantee a branch when truth lies on a cutoff. More scientific calls are not silently authorized and do not change the frozen estimand.

## 10. Reliability evidence and what more calls buy

Transport readiness freezes eight failure modes and six call positions. Each of the 48 mode-position cells receives confidence error `0.05/48` and failure budget `0.02/48`. Every one-sided exact Clopper-Pearson upper bound must fit its cell budget. Bonferroni allocation gives simultaneous familywise coverage of at least 95%, and a union bound holds the complete-pair missing budget to 0.02 without assuming independence.

With zero observed failures, this stringent gate needs 16,478 observations at each call position, or 98,868 accepted route-soak calls across the six positions. Those extra calls buy evidence that the route is reliable enough not to distort the 768-pair experiment; they do not improve the model-effect estimate or rescue a bad mechanism. If the frozen route has no genuinely zero-price primitive, the soak is paid work and remains behind a separate owner decision.

No paid action is authorized until endpoint, provider, snapshot, tokenizer, maximum tokens, prices, attempt count, retry semantics, time, reconstruction count, and dollar ceiling are frozen. A cheaper reliability design requires a new preregistered argument; it cannot be improvised after observing failures.

## 11. Required no-model gates

1. **Bundle:** exact committed artifacts, Git-object pins, authenticated validator closure, scoped claims, and no stale authority.
2. **State:** seventeen event types, 289 differential pairs, targeted traces, exact replay, cycle rejection, and every named mutant killed.
3. **Packets:** real Draft 2020-12 execution, semantic identity attacks, independent BC/OM builders, exact singleton B score, and pre-dispatch overflow failure.
4. **Cohort:** generator and evaluator freeze before candidate inspection, candidate freeze before fresh seed, one cut before recomputation, 960 generated and 768 retained unique scenarios.
5. **Mechanics:** reconstruction and isolation witnesses, exact 100-cell H-D-F coverage, coherent physical counters, and every executable red candidate rejected for its intended mechanism.
6. **Inference:** terminal-only interval, three-way numerical parity, literal reference vectors, kappa sensitivity, complete near-floor OC curve, simultaneous reliability arithmetic, and explicit cost.
7. **Authorization:** frozen provider route, prices, reliability evidence, and a separate owner decision.

Failure blocks the next stage. No unregistered mid-run repair is allowed.

## 12. Program decisions and non-claims

Primary program outcomes are `DESIGN_OR_IMPLEMENTATION_FAIL`, `BOUNDED_CONTINUITY_FALSIFIED`, or `BOUNDED_CONTINUITY_SURVIVES` with an exactness-filtered Pareto set. Conditional model outcomes are promote, model/interface fail, model/interface ceiling, transport inconclusive, or inconclusive/underfunded.

TN may lose without killing continuity. Model use may fail without killing mechanical continuity. Oracle failure may indicate a model/task ceiling rather than a representation defect. A surviving candidate supports only the tested finite domain, workloads, implementation, route, and model.

No result establishes universal asymptotic boundedness, production readiness, concurrent-writer safety, hostile-box security, persistent mind, personality, affect, procedural memory, cross-model generality, or success in the later coordination experiment.
