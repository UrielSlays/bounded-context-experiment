# MBCX-01 — Executable Bounded Obligation Continuity Experiment Design r5

Status: preregistration design; no harness implementation and no paid inference authorized

Date: 2026-08-12

Supersedes for future review: `MBCX-01-EXPERIMENT-DESIGN-r4.md`

Normative companion contracts:

- `MBCX-01-STATE-ACTION-CONTRACT-v1.json`
- `MBCX-01-INFERENCE-CONTRACT-v1.json`

If explanatory prose conflicts with a normative companion contract, the contract governs and Stage 0 must log the conflict before implementation.

## 1. Decisions and revision boundary

MBCX-01 answers three questions without letting one answer substitute for another:

1. **Continuity:** can a fresh logical conductor receive an exact, bounded decision packet that preserves current public state and every due critical obligation while dormant archive size and active-subject history depth grow, without hiding archive-linear work?
2. **Mechanism selection:** among strong flat-derived replay, coarse materialization, and typed-native materialization, which mechanisms meet the same contract, and does added mechanism complexity earn a measured engineering advantage?
3. **Model usability:** after a deterministic mechanism passes, can one frozen model use the validated packet through one process-cold A→B→A episode without losing, duplicating, or resurrecting an obligation?

The North Star is question 1. Question 2 is nested inside it. A typed-native loss does not falsify bounded continuity if FD or FC passes. Question 3 is conditional on questions 1 and 2 and cannot rescue a deterministic failure.

Council r5 agreed that this causal architecture is correct. r5 repairs the executable preregistration: it freezes the state/action and inference contracts, separates Stage-1 and Stage-2 cohorts, adds active-depth and physical-work gates, pins one paid-call DAG, and removes paid diagnostics that cannot create the primary conclusion.

No model outcome may be described as a mechanism effect when candidate packets are byte-identical.

## 2. Scope and non-goals

MBCX-01 includes only:

- one append-only public journal;
- one single-threaded canonical commit boundary enforced by construction;
- exact bitemporal fact, obligation, dependency, scope, action, and handoff semantics;
- deterministic reference reduction, independent enumeration, materialization, reconstruction, and scoring;
- FD, FC, and TN candidate families;
- dormant archive `H`, active-subject depth `D`, and live frontier `F` as separate axes;
- one frozen model/provider for one same-model cold A→B→A episode per condition per Stage-2 scenario;
- two bounded confidence sequences, mechanical decisions, exact transport accounting, and cleanup.

MBCX-01 excludes:

- concurrent canonical writers, consensus, distributed transactions, or merge policy;
- cross-model handoff or model-family generalization;
- learned/model-written memory, learned retrieval, procedural learning, personality, affect, or relationship memory;
- provider-native hidden/KV-state claims;
- production orchestration, deployment, security architecture, licensing, patents, or commercialization.

Benign wrong-scope collision remains in scope because scope isolation affects the scientific result.

## 3. Three-stage causal program

### Stage 0 — executable instrument proof, no model

Freeze and hash:

- the two normative contracts;
- the reference reducer and independent small-state enumerator;
- the deterministic Stage-1 and disjoint confirmatory Stage-2 manifests;
- canonical packet, handoff, artifact, scorer, and serializer schemas;
- candidate-producer isolation and reconstruction witnesses;
- physical resource counters, aggregation, indifference bands, and cost ceilings;
- the exact six-call-per-scenario primary request DAG;
- the audited confidence-sequence implementation and operating-characteristic report;
- transport fixtures, write-ahead response replay, and cleanup tests.

Stage 0 answers whether the instrument can be implemented without answer-changing discretion. It cannot establish memory value.

### Stage 1 — deterministic continuity and mechanism bakeoff, no model

Every candidate consumes byte-identical public journal events and is judged against the independent reference. Stage 1 tests exactness, dormant-archive independence, active-depth independence, frontier behavior, reconstruction, and the read/write/storage Pareto set.

Stage 1 answers the continuity and mechanism-selection questions without stochastic model behavior.

### Stage 2 — conditional same-model A→B→A usability screen

Only one Stage-1-eligible bounded packet carrier enters Stage 2. Each condition on each scenario executes exactly:

```text
fresh A0 -> fresh B -> deterministic writer -> process-cold fresh A1
```

BC and OM are paired conditions. They use one frozen endpoint and differ only in mounted semantic content. Stage 2 asks whether the model can use externally validated state. It does not test mechanism effects, cross-model portability, or concurrent coordination.

## 4. Canonical universe and executable oracle

### 4.1 Canonical record and time

The sole canonical record is an append-only, hash-linked public event journal plus immutable referenced public payload objects. `MBCX-01-STATE-ACTION-CONTRACT-v1.json` governs the full record shape and semantics.

Every query cut is the tuple:

```text
(journal_seq, knowledge_time, valid_time)
```

An event participates only when it is visible at `knowledge_time` and effective at `valid_time`. Retroactive fact correction is legal, but an event observed after an earlier cut never rewrites that earlier cut. Obligation, dependency, and handoff transitions are transaction-time events with `valid_from == observed_at`.

The single writer assigns contiguous `journal_seq` values. A single mutex/serialized event loop guards validate-and-append. A second proposal cannot be in flight against the same obligation. Multi-writer behavior is a later experiment.

### 4.2 State and action totality

The normative contract freezes:

- all 17 event payloads, guards, effects, and illegal outcomes, including `record_handoff_response`;
- linear correction ancestry, restoration after retraction, and cycle rejection;
- exact obligation lifecycle, due/blocking rules, terminal reopening, delegation, and immutable scope;
- acyclic same-scope dependency edges;
- handoff response recording, proposal, commit, rejection, close, and idempotency;
- the complete action super-universe, availability rule, gold rule, and scenario contract-success rule;
- RFC 8785 serialization and stable ordering.

The available action list is not supplied by generator intuition. It is enumerated from the state contract. Gold is independently derived from every mounted due critical obligation. A legal scored cut may contain four gold obligation actions; the old `1–3` cap is retired.

### 4.3 Independent oracle proof

Stage 0 must produce two independently written executables:

1. the reference reducer/scorer;
2. an exhaustive small-state enumerator that does not import the reducer.

They must agree over every tractable event sequence, every ordered two-event type pair, every mandatory contract fixture, and all hand-authored long traces. Any ambiguity yields `ALGEBRA_UNDERSPECIFIED` and halts before candidate testing. It is never scored as a mechanism residual.

## 5. Candidate mechanisms

All candidates share the same journal, public payloads, scope selector, packet schema, serializer, object caps, and governed dependency-read API.

### FD — flat-derived replay

FD persists primitive events, payload refs, and generic indexes. Subject indexes are keyed by `(scope_id, subject_id)`; obligation indexes by `(scope_id, obligation_id)`; dependency indexes by same-scope endpoint tuples. Currentness, restoration, conflict, terminal status, and provenance closure are derived at read time.

### FC — flat plus coarse materialization

FC adds rebuildable current/terminal/superseded flags, current-value pointers, obligation status, direct dependency readiness, and segmented active-scope snapshots with a bounded delta tail. The snapshot/tail implementation is part of FC, not a fourth semantic arm. Its contract must prevent a checkpoint ceiling from silently restoring full replay.

### TN — typed-native materialization

TN adds rebuildable typed lifecycle rows, version/valid-time relations, explicit conflict/restoration links, obligation/dependency state, and provenance closure.

### Parity and legitimate residuals

Under the generous reference envelope, all three candidates must emit the same semantic `DecisionPacketV2` in the same canonical order. Byte-identical packets share one paid call and one stochastic result.

An operationally bounded candidate may differ only through a preregistered, explicit result:

- required object omitted;
- required status/provenance unavailable;
- `PAGE_FAULT`;
- `FRONTIER_LIMIT`;
- serialization overflow;
- materialization work-budget exhaustion.

`ALGEBRA_UNDERSPECIFIED`, hidden fallback, or unregistered dependency access is a design failure, not a candidate result.

## 6. Packet and handoff contracts

### 6.1 `DecisionPacketV2`

```text
packet_version
canonical_cut
active_scope_manifest
state_objects[]
obligation_objects[]
dependency_objects[]
conflict_objects[]
procedure_objects[]
evidence_objects[]
missing_or_denied[]
page_faults[]
materialization_manifest
```

Every object carries a public semantic ID, a neutral `object_kind`, public fields, and source event IDs. Neither key names nor descriptions mark an object as gold. Empty arrays mean the reference proved the set empty.

### 6.2 Presentation-matched BC and OM

BC and oracle-minimal OM use byte-identical:

- outer keys and key order;
- field descriptions and system/user instructions;
- action list and action order;
- output schema;
- maximum token envelope and padding policy;
- serialization and transport settings.

BC contains all semantics selected by the bounded mechanism. OM contains the minimal public semantic objects required for the selected cut, but uses the same neutral containers and labels. Neither contains answer IDs, due/gold flags, or prose that points at the target. A render-only discriminator must remain at chance in the Stage-0 blinding fixture.

### 6.3 `TaskPacketV2` and `WorkerHandoffV2`

Fresh B receives the condition packet, current observation/time, complete action set, IDs, output schema, and idempotency key. B receives no A transcript, hidden reasoning, scratch, or provider thread chain.

`WorkerHandoffV2` contains only public IDs, enumerated status/reason codes, timestamps, hashes, and capped arrays specified by the state/action contract. It has zero free-text fields. The deterministic writer validates scope, hash binding, transition legality, action availability, and idempotency.

### 6.4 Write-ahead response rule

Immediately after any accepted provider response arrives, before parsing or validation, the runner appends `record_handoff_response` with immutable raw response bytes and request/route hashes. Recovery parses and adjudicates those recorded bytes. It may not resample an accepted call. A crash after receipt and before response journaling is transport-ambiguous and makes the pair missing.

## 7. Frozen workloads

### 7.1 Stage-1 deterministic cohort

Stage 1 uses 240 independent scenarios: six motif families × forty seeds. Each scenario contains 24 scored deterministic cuts. The manifest includes exact scenario/cut IDs, motif, generator version, journal hash, action-universe hash, and gold hash.

Motifs are correction/restoration; obligation lifecycle; dependency reversal; cross-scope collision; delegation/idempotent handoff; and mixed delayed A→B→A continuity.

### 7.2 Stage-2 confirmatory cohort

Stage 2 uses 384 independent scenarios disjoint from Stage 1: six motifs × sixty-four seeds. Each has exactly one paid cut chosen by the normative hash rule. A scenario is Stage-2-eligible only when that cut has at least one mounted due critical obligation and one non-gold action.

The analysis order is SHA-256 order of frozen scenario ID. Looks are the first `96`, `192`, and `384` IDs. No reserve substitutes for a missing scenario.

### 7.3 Dormant archive axis `H`

At fixed active state, depth, and frontier, construct twins at:

```text
H = 128, 1,024, 10,000, 100,000 public events
```

Added events are realistic but do not touch any active subject, obligation, dependency, handoff, or mounted scope. Packet bytes and semantics must remain identical.

### 7.4 Active-subject depth axis `D`

At fixed `H = 1,024` and `F <= 16`, vary valid correction/supersession and lifecycle depth on active subjects:

```text
D = 1, 4, 16, 64, 256
```

The final state, live obligations, dependency closure, observation, actions, and gold remain identical. This axis makes the boundedness claim falsifiable against deep history on objects that still matter.

### 7.5 Active-frontier axis `F`

At fixed `H = 100,000` and `D = 16`, vary the live obligation/dependency frontier:

```text
F = 1, 4, 16, 64, 256
```

This is a curve, not a fixed-packet claim. `F=64/256` cells are deterministic resource tests and may exceed the paid action envelope. Silent omission is forbidden; bounded mechanisms return `FRONTIER_LIMIT` before model dispatch when required.

### 7.6 Mandatory long traces

In addition to the normative enumerator checks, Stage 0 includes retroactive correction at two knowledge cuts; cross-scope delegation rejection; four simultaneous due critical obligations; crash after raw response record; duplicate response/proposal/commit; candidate source rename; journal rebuild; and checkpoint/tail overflow without full replay.

## 8. Mechanical outcomes

### 8.1 Deterministic outcomes

- exact reference state/action/packet equality;
- due-critical recall and wrong-scope/stale suppression;
- duplicate committed effects;
- reconstruction and journal-rebuild equality;
- packet identity and explicit limit correctness;
- physical records/pages/bytes read and written;
- comparisons/probes, cache hits/misses, background maintenance, open/decode/rebuild work;
- latency, artifact bytes, and peak temporary bytes.

Every dependency that can affect output must pass through the governed physical-read API. Direct journal/index/file reads outside it are taint failures. No operation is exempt as “metadata.”

### 8.2 Paid outcome

Each condition has exactly three scored decisions (`k = 3`): A0 target/task selection, B proposal, and cold A1 reconciliation/action. `contract_success` is the exact conjunction in the normative state/action contract.

The primary pair is:

```text
delta_i = contract_success_i(BC) - contract_success_i(OM)
```

Action precision/recall, per-step success, latency, and the two discordant-pair frequencies are secondary. No LLM judge may override the mechanical score.

## 9. Stage-1 gates and recommendation

### 9.1 Universal zero-loss gates

Across the complete Stage-1 manifest and mandatory traces:

- zero lost due critical obligations;
- zero wrong-scope gold/admissions;
- zero stale terminal/corrected resurrection at any canonical cut;
- zero duplicate committed effects;
- 100% legal-transition, action-universe, scorer, packet, and reconstruction agreement;
- zero gold/reference/generator taint in candidate producers;
- zero unregistered read, hidden fallback, or undeclared overflow.

Any violation is `DESIGN_OR_IMPLEMENTATION_FAIL` and is not averaged away.

### 9.2 Numerical boundedness gate

For `H` and `D` twin families at fixed `F`, the packet is byte-identical. For every deterministic charged counter, compute:

```text
normalized_range = (maximum counter - minimum counter) / (maximum axis value - minimum axis value)
```

The gate requires `normalized_range <= 0.0001` charged units per added event on both axes. Because deterministic counters are integers, the `D=1..256` gate permits no extra charged unit; the `H=128..100,000` gate permits at most nine. This admits a small bounded index-height change but rejects archive/depth-linear work. Every intermediate scale must lie within the same minimum-to-maximum counter envelope.

Cold artifact open, decode, materialization, and background work are included. Warm and cold latency are reported separately; latency does not substitute for the deterministic counter gate. A candidate that scans one metadata element per archive event fails.

The `F` axis is reported as a curve with correct `FRONTIER_LIMIT`; it is not subject to the zero-slope claim.

If no candidate passes `H`, `D`, and the zero-loss gates, bounded continuity is falsified for the frozen workload. If at least one passes, the principle survives regardless of TN.

### 9.3 Bounded performance schedule

Exactness runs once over every Stage-1 scenario/cut/axis cell plus the combined stress corner `H=100,000, D=256, F=16`. Performance repetitions run only on a preregistered 10% stratified subset selected by lowest SHA-256 within every `(motif, axis, scale)` cell: one warm-up plus 30 cold measured materializations per selected cell. Candidate order is a frozen Latin-square rotation; caches are dropped or the inability to do so is reported and the host is not used for cold claims.

Within each cell, p95 is Hyndman–Fan type 7 over the 30 measurements. Across cells, the comparison metric is the maximum cell p95, never a pooled quantile or a mean of cell quantiles. Measurement resolution is the greater of the calibrated timer tick and the median absolute repeated no-op difference.

The run root has a 20 GiB hard ceiling. Journal/payload bytes are shared across candidates; candidate artifacts are deleted only after hashes and required measurements are retained. Crossing the ceiling halts Stage 1 without deleting unrelated files.

### 9.4 Engineering output and Stage-2 carrier

The engineering result is the Pareto set over exactness, physical reads/writes, cumulative maintenance work, cold p95 latency, artifact bytes, rebuild time, and implementation branch count.

Frozen indifference bands are: physical counters `max(1%, absolute jitter band)`, latency `5%`, artifact bytes `1%`, branch count `1 branch`. A mechanism is strictly recommended only if it improves at least one load-bearing dimension beyond its band and regresses on none beyond its band. Otherwise the owner receives the Pareto set with `NO_UNIQUE_ENGINEERING_WINNER`.

Stage-2 carrier selection is separate and has no engineering authority: at the combined stress corner, among bounded exact candidates choose the minimum maximum-cell p95 physical reads, then minimum maximum-cell p95 latency, then FD/FC/TN. Byte-identical candidates share the carrier call.

## 10. Producer isolation and process-cold reconstruction

Candidate production runs in a child process whose allowlist contains only the public journal/payload root, normative schema, candidate implementation, governed dependency API, output path, and explicit config. It cannot import or read the generator, reference reducer, reference packets, action gold, scenario secrets, other candidates, network, or ambient working directory.

Taint canaries place unique tokens in forbidden modules/packets and prove they do not appear in imports, reads, artifacts, logs, or packets.

Every artifact is reconstructed by a second fresh child with a sanitized environment and no source tree. Required witnesses:

1. withheld artifact fails;
2. corrupt artifact fails loudly;
3. source-directory rename does not change reconstruction;
4. swapped opaque artifacts swap decoded state;
5. one field mutation changes only its causal dependent output;
6. nonce-only artifact fails information sufficiency;
7. projection rebuilt from the canonical journal equals the persisted projection and decoded packet.

Open/decode/rebuild work is charged to the candidate. Every child PID is captured, bounded, waited, terminated if necessary, and verified absent.

## 11. Exact Stage-2 invocation DAG

Each Stage-2 scenario runs BC and OM in a frozen balanced order. Each condition has exactly three accepted calls:

1. **A0:** receives condition packet, observation/time, and action universe; emits exactly one target action plus `TaskPacketV2`.
2. **B:** receives only `TaskPacketV2`; emits `WorkerHandoffV2`.
3. **A1:** after write-ahead response recording, deterministic commit/rejection, child teardown, and process-cold reconstruction, receives the reconstructed condition packet and emits the exact post-handoff action set.

Thus the primary maximum before transport overhead is:

| n | BC calls | OM calls | total accepted calls | child reconstructions |
|---:|---:|---:|---:|---:|
| 96 | 288 | 288 | 576 | 192 |
| 192 | 576 | 576 | 1,152 | 384 |
| 384 | 1,152 | 1,152 | 2,304 | 768 |

All 24 scenario cuts remain deterministic Stage-1 tests. LR, EF, XT, and CO are deferred to a separately pinned diagnostic extension and cannot be silently added to this primary run.

## 12. Inference and missingness

`MBCX-01-INFERENCE-CONTRACT-v1.json` is normative. It freezes the upstream commit/source hashes, exact function, `Y=(delta+1)/2` transform, `alpha=0.025` for the delta CS, `alpha=0.025` for the OM CS, truncation `0.5`, running intersection, reference vectors, operating-characteristic grid, and branch precedence.

The primary noninferiority margin is `-0.10`. The OM floor is `0.80`. Both are owner/operator thresholds for the first usability screen, not universal constants.

- `PROMOTE_TO_COORDINATION_STAGE` requires delta lower bound `> -0.10`, OM lower bound `>= 0.80`, and all deterministic gates.
- `MODEL_INTERFACE_FAIL` requires delta upper bound `< -0.10`, OM lower bound `>= 0.80`, and all deterministic gates.
- `MODEL_OR_INTERFACE_CEILING` requires OM upper bound `< 0.80`.
- otherwise the result is `INCONCLUSIVE_OR_UNDERFUNDED` at 384.

Worst-case missing-pair assignments must yield the same branch. Eight missing pairs by 384 (more than 2%), a route-associated missingness pattern that can tip the branch, or branch disagreement under worst-case assignments yields `TRANSPORT_INCONCLUSIVE`. No reserve scenario substitutes into the manifest.

Before paid authorization, Gate 5 must execute every reference vector and every branch, reproduce the independent implementation, and publish coverage/power/inconclusive behavior over the full frozen grid. The owner sees the operating characteristics before deciding whether the spend is worthwhile.

## 13. Transport, cost, and authorization

The paid runner is a direct single-in-flight HTTPS/files program. It is not an agent framework, service, daemon, database, or plugin.

Before dispatch freeze and hash:

- exact model slug, provider endpoint, tokenizer, serializer, prompts, and schemas;
- one provider, fallbacks off, required parameter and structured-output support;
- response cache off; no server preset, tools, transforms, or hidden conversation chain;
- temperature, seed if supported, token maxima, timeout, and one pre-acceptance retry maximum;
- session/routing fingerprint held constant across paired arms where supported;
- route/response metadata required on every uncached response;
- exact request DAG, request hashes, response hashes, and accepted/no-body policy;
- current price sheet and a hard maximum bill.

Missing route identity or a cache/fallback/transform mismatch makes the full pair missing. An accepted call is never retried or resampled; its raw result is write-ahead recorded.

The preauthorization manifest must prove:

```text
384 unique Stage-2 IDs
× 1 paid cut
× 2 conditions
× 3 fresh calls
= 2,304 accepted primary calls maximum before missing/pre-acceptance retry overhead
```

It must also state exact maximum input/output tokens, price, expected/worst-case pre-acceptance retry overhead, 768 reconstruction starts, wall-clock estimate, and dollar ceiling. No paid engineering smoke or confirmatory call begins without a separate owner authorization naming the endpoint and maximum spend.

## 14. No-model gates

### Gate 0 — question and pin traceability

- every claim maps to continuity, mechanism selection, or model usability;
- typed-mechanism failure cannot kill bounded continuity;
- both companion contract hashes and every source pin are present;
- excluded multi-writer, cross-model, procedural, production, and security claims remain excluded.

### Gate 1 — executable algebra and generator

- independent reducer/enumerator agreement;
- every normative mandatory fixture and long trace passes;
- action super-universe completeness is independently enumerated;
- Stage-1 240 and disjoint Stage-2 384 manifests are exact and hashed;
- all 384 paid cuts are eligible under the normative cut selector;
- gold/action/manifest taint canaries pass.

### Gate 2 — mechanism parity and isolation

- FD/FC/TN generous-envelope semantic and byte parity;
- FC segmented snapshot-plus-tail overflow path exercised;
- unique-packet dedupe proven;
- producer allowlist and taint canaries proven;
- Pareto and carrier rules reproduced independently.

### Gate 3 — resource boundedness and reconstruction

- `H` and `D` zero-slope gates pass or fail explicitly;
- physical read/write/cache/background/open/decode counters cover every layer;
- `F` curve and `FRONTIER_LIMIT` are correct;
- all seven reconstruction witnesses pass;
- exact child wait/termination and zero leakage.

### Gate 4 — handoff and replay

- exact `TaskPacketV2`/`WorkerHandoffV2` schemas and caps;
- zero free-text or transcript/scratch inheritance;
- write-ahead raw response replay after crash;
- duplicate, stale, wrong-scope, rejected, committed, and closed traces;
- exactly-once governed effect and deterministic A→B→A replay equality.

### Gate 5 — inference, transport, and cost

- pinned confidence-sequence code/hash/reference-vector parity;
- independent implementation and full operating-characteristic grid;
- all decision and missingness branches exercised;
- presentation-blinding fixture at chance;
- exact zero-inference 2,304-call manifest dry run;
- mock transport identity, response-cache, ambiguity, malformed-output, fallback, preset, and write-ahead fixtures;
- exact call/token/dollar ceiling and owner authorization form.

A fresh sealed design council with no P0/P1 scientific blocker is required before the owner may authorize harness implementation. After implementation, Gates 0–5 and the Stage-1 deterministic results must pass before Stage 2 can be proposed. Stage 2 still requires separate owner authorization naming the endpoint and maximum spend.

## 15. Run artifacts and cleanup

Each run owns one bounded root containing config/source/contract/manifests hashes; journal and candidate artifacts; reference/candidate packets; physical-work ledgers; reconstruction and taint logs; exact request/response bytes and route metadata; scores and confidence-sequence state; cost ledger; and cleanup manifest.

Cleanup proves every child/helper PID was waited and terminated, no watcher/daemon/browser session remains, no run-owned temporary path remains outside the run root, and no unrelated user file/process was changed.

The fixed temporary `confseq` checkout used while drafting the r5 reference vectors was validated under `<home>\AppData\Local\Temp`, removed after hashing/execution, and left no process or directory behind.

## 16. Interpretation boundaries

A Stage-1 pass means bounded external obligation continuity is feasible for the frozen workload across measured `H`, `D`, and the declared `F` envelope. Finite points do not prove universal asymptotics.

A TN win means typed materialization earned a measured engineering advantage. An FD/FC result means Moonwalker should prefer the simpler eligible mechanism until another workload demonstrates otherwise. Neither result decides model usability.

A Stage-2 pass means one frozen model can use a validated selectively mounted packet through one cold serial handoff within the declared margin. It says nothing about different models, concurrent writers, swarms, or procedural transfer.

Later experiments may address cross-model selective inheritance, concurrent proposals and adjudication, shared discovery/scoped promotion, and long-horizon hot/cold continuity.

## 17. Prior art used as method, not answer

The instrument borrows append-only journals/rebuildable projections from event sourcing and Muninn; durable identity and recorded non-deterministic results from virtual actors and durable workflows; registered dependencies from build systems; checkpoint-plus-bounded-tail implementation from database/incremental systems; matched presentation controls from render-confound work; selective declarative handoff from shared selective persistent memory; typed schema/validation boundaries from Text2Mem; prospective obligation motifs from PM-Bench; interference-heavy active-depth stress from MINTEval; and bounded-mean sequential inference from Waudby-Smith/Ramdas and the pinned `confseq` implementation.

No cited work establishes the full conjunction tested here.

## 18. Authorization

This design authorizes no harness implementation, browser mutation beyond council dispatch, external experiment message, paid model call, or experiment run.
