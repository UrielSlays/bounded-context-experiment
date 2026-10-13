# MBCX-01 r7 Repair Design

**Date:** 2026-08-12

**Status:** owner-approved design; implementation remains gated by written-spec review

**Repository:** `<repo>`
**Current reviewed bundle:** commit `08421f49c39c8c79c14f1ad9ba1789a2a96bcf4a`

## 1. Objective

Repair the MBCX-01 scientific instrument so the next pinned bundle can be implemented literally without an unstated choice that changes:

1. whether bounded due-obligation continuity survives;
2. the FD/FC/TN engineering Pareto result or carrier selection; or
3. the frozen model's BC-versus-OM outcome in one serial cold `A0 -> B -> writer -> A1` episode.

This round repairs the preregistration and its no-paid red witnesses. It does not implement FD, FC, TN, the model harness, or paid inference.

## 2. Council evidence and authority

The repair synthesis consumes these banked r6 reports:

- Codex EXEC: independent `NO-GO`;
- ChatGPT/Sol: longitudinal-seat `NO-GO`;
- Claude Opus 5: longitudinal-seat `GO-WITH-FIXES`.

A finding is adopted when the governing bytes or an executable witness establish a reachable false-result, non-total-contract, hidden-work, or unpriced-cost path. Seat count alone neither accepts nor rejects it. Proposals remain pointers until bypass-constructed against the experiment.

The owner has ruled that browser seats are persistent council lanes. Longitudinal context is intentional. Future packets must distinguish:

- **longitudinal continuity:** a browser seat retains its own earlier rounds;
- **lateral seal:** a seat must not inspect another seat's current-round verdict before answering;
- **fresh execution:** Codex EXEC remains a one-shot ephemeral seat for each round.

No browser seat may claim fresh-round independence merely because it receives a new packet. Its report must disclose retained prior-round context. That disclosure does not disqualify the maintained seat.

## 3. Alternatives considered

### A. Consensus-only repair

Repair only defects independently named by at least two seats. This is smaller, but it knowingly leaves byte-verified single-seat defects such as unsafe JSON integers, call-response journaling gaps, multi-gold guessing, and packet-schema absence.

### B. Verified-defect closure — selected

Repair every answer-changing defect independently reproducible from the pinned bytes, while rejecting remedy suggestions that weaken inference or broaden the scientific question. This costs one larger normative revision but gives the next council a coherent target.

### C. Replace MBCX-01 with a simpler experiment

Collapse the design to files/RAG or a one-stage model comparison. This would abandon the still-supported continuity/mechanism separation before the instrument has received a fair test.

## 4. Artifact topology

The next review target is a five-artifact normative bundle:

1. `MBCX-01-EXPERIMENT-DESIGN-r6.md` — scientific question, stages, cohorts, invocation DAG, gates, and decisions.
2. `MBCX-01-STATE-ACTION-CONTRACT-v2.json` — canonical reducer, writer algorithm, action executor, response journal, gold selection, serialization, and mandatory traces.
3. `MBCX-01-PACKET-SCHEMAS-v1.json` — closed JSON Schemas for `DecisionPacketV2`, `TaskPacketV2`, and `WorkerHandoffV2`, plus deterministic render rules.
4. `MBCX-01-MEASUREMENT-CONTRACT-v1.json` — charged-counter catalog, units, bounds, aggregation, crossed-axis cells, preprocessing rules, and resource reporting.
5. `MBCX-01-INFERENCE-CONTRACT-v2.json` — estimands, valid sequential method, feasible OC manifest, missingness, stopping, source pins, reference vectors, and authorization-facing operating characteristics.

The council delivery layer adds:

- `MBCX-01-COUNCIL-R6-SYNTHESIS-AND-DISPOSITION.md`;
- `MBCX-01-EXPERIMENT-COUNCIL-PACKET-r7.md`;
- `MBCX-01-BROWSER-SEAT-PROMPT-r7.txt`;
- r7 Codex prompt generator, watcher, dispatch test, and receipt.

## 5. State, action, and packet repairs

### 5.1 Total identity and serialization

- Idempotency uniqueness is the tuple `(scope_id, semantic_operation, idempotency_key)`.
- Duplicate detection uses that exact tuple; a key reused in another scope is not a duplicate.
- Every integer admitted into RFC 8785 canonical JSON is within `[-9007199254740991, 9007199254740991]`. Larger numeric identities are canonical decimal strings.
- Every catalog referenced by a guard is a closed, named array in the normative contract.

### 5.2 Total writer and action executor

- `ACT:{scope_id}:{obligation_id}` maps to exactly one `complete_obligation` event.
- The executor obtains `completion_action_id` from the addressed obligation and places it in the transition payload. The public ACT ID is never substituted for that value.
- The contract freezes event construction, child-event order, journal assignment, atomicity, and idempotency for commit.
- If a parsed B proposal fails schema, scope, hash, availability, or transition validation, the writer emits exactly one `reject_handoff_result` with the matching frozen rejection code. It does not first attempt an illegal proposal transition.

### 5.3 Call-level response journal

Replace handoff-only response recording with `record_call_response`, keyed by `(scenario_id, condition, node)` where node is `A0`, `B`, or `A1`. It has no handoff-status guard. Every accepted response is journaled before parsing, and recovery reuses the recorded bytes without provider resampling.

### 5.4 Packet contracts

The schema artifact uses JSON Schema 2020-12 with `additionalProperties: false`, closed enums, array caps, byte/string caps, safe integer domains, canonical array ordering, and zero free-text reasoning fields. The state/action contract references only `DecisionPacketV2`, `TaskPacketV2`, and `WorkerHandoffV2`.

The renderer freezes key order, descriptions, instructions, action order, padding, serialization, token envelope, and transport settings. The no-paid discriminator uses only deterministic render features and must remain at preregistered chance tolerance under repeated ID permutation.

### 5.5 Paid-cut eligibility

Stage-2 paid cuts require exactly one mounted critical due obligation and at least one non-gold available action. `A0_target` is therefore unique without a hidden tie-break. The frozen generator overproduces `6 x 80` candidates and selects the first 64 eligible per motif by SHA-256 order. Eligibility decisions and rejected candidate IDs are hashed into the manifest.

`F=16`, `F=64`, and `F=256` are deterministic resource cells and are exempt from the paid 8-to-16 action envelope.

### 5.6 Retroactivity and enumerator strength

The fact reducer explicitly permits a retroactive correction to attach to the visible chain head at knowledge time while carrying an earlier validity interval. Current value is resolved by walking the single parent chain at the queried bitemporal cut. The contract removes unreachable duplicate wording.

Ordered-pair tests use shared-entity pre/post-state vectors for every load-bearing pair; disjoint-object legality does not satisfy interaction coverage.

## 6. Measurement repairs

The measurement contract defines a closed set of counters. Each counter has an ID, layer, unit, sampling boundary, cold/warm applicability, aggregation rule, and absolute permitted range.

Unit classes are not normalized against one dimensionless threshold. Counts, pages, bytes, operations, and branch counts each receive explicit absolute allowances. The contract also applies a total-charge bound within each unit class so work cannot be hidden by splitting one counter into many. Adding an unregistered counter is a Stage-0 failure.

The exactness grid crosses:

- every `H` value at `D=16` and `D=256`;
- every `D` value at `H=1024` and `H=100000`;
- the existing `F` curve; and
- the combined stress corner.

The mandatory red candidate is constant on both original marginal slices but archive-linear only when `H` and `D` are simultaneously high. It must fail.

Candidate config is a closed schema. It cannot contain selected event IDs, precomputed packets, gold, reference state, or arbitrary paths. All preprocessing, index construction, checkpoint rollover, background work, open/decode work, and governed dependency reads are charged. Jitter is measured per counter from frozen no-op/calibration fixtures; latency never substitutes for deterministic physical work.

## 7. Inference repairs

### 7.1 Estimands and validity

The target population is the frozen, motif-balanced Stage-2 manifest. The delta estimand is the average conditional mean of `BC_i - OM_i` over that manifest in its frozen SHA-256 order. The OM estimand is the corresponding average conditional success probability.

The selected confidence-sequence construction must explicitly cover independent bounded observations with potentially time-varying conditional means. A common-mean method is not admissible unless the generator enforces and verifies that assumption. The contract pins the deciding theorem, exact formula, implementation, independent transcription, and numerical fixtures.

The OM floor remains inferential. It is not replaced with a bare point-estimate threshold. The contract publishes the inconclusive region, per-look feasibility, and operating characteristics before paid authorization.

### 7.2 Stopping and looks

Looks at 96 and 192 may stop only for a branch that the frozen rule proves reachable at that look. The contract states whether each branch is binding, futility-only, or diagnostic at each look. If no branch fires, execution continues to 384. Cost manifests show maximum and expected calls under the same stopping law.

### 7.3 Feasible operating-characteristic manifest

OC cells are parameterized by valid paired probabilities `(p00, p01, p10, p11)` that are nonnegative and sum to one. Delta, discordance, and OM rate are derived fields. The complete frozen cell manifest is generated and hashed before simulation. No impossible Cartesian cell may be silently filtered at run time.

Missingness is an integer count with frozen placement and association modes. For every incomplete pair, sensitivity jointly enumerates feasible completions of BC and OM. The scientific branch must be invariant across all feasible completions or the result is `TRANSPORT_INCONCLUSIVE`.

### 7.4 Source and vector reproducibility

- Correct upstream Git blobs are `f7c3b4bf17411596d1434e3330796f3e8c8ff884` and `89f433fd24274e7c74d7d93fe054399fb87cfaca` at commit `5ffe733ca2447a2e28c2c91f3b00086173f2ab2c`.
- SHA-384 and byte counts are computed over Git blob content, not an HTTP response body.
- The import graph and inner defaults are asserted from the pinned source.
- Every reference-vector input array, indexing convention, generator, interpreter version, and dependency version is frozen and hashed.
- A disagreement between the reference and independent implementation blocks Gate 5; neither implementation is presumed correct.

### 7.5 Transport readiness

The pre-paid transport soak measures accepted/no-body, route-identity, fallback, cache, and transform failure rates against the six-node pair-missingness budget. The authorization manifest publishes the implied per-call reliability requirement, not just the pair ceiling.

## 8. Red-witness suite

Before r7 dispatch, no-paid tests must demonstrate that the repaired contracts reject:

1. cross-scope idempotency suppression;
2. unsafe JSON integer aliasing;
3. ACT-ID/completion-ID substitution;
4. invalid-proposal path divergence;
5. unjournaled A0/A1 accepted responses;
6. multi-gold A0 guessing;
7. render-length, key-order, position, or ID leakage;
8. config-carried precomputed packets or selected events;
9. counter splitting and H-by-D interaction growth;
10. impossible paired-probability cells;
11. one-pair OM completion changing the branch;
12. unfrozen periodic-vector indexing;
13. wrong Git blob identities; and
14. a reference/independent inference mismatch.

The tests validate the contracts and preregistration only. They do not fabricate FD/FC/TN results.

## 9. Council delivery and wait protocol

The browser-seat payload is exactly the owner-style pointer:

```text
Hey homie, can you help me out? Read this and execute:
<repo>\MBCX-01-EXPERIMENT-COUNCIL-PACKET-r7.md
```

The same pointer is sent through Moonwalker CDP to:

- the maintained Claude conversation on port <council-browser-port>;
- the maintained ChatGPT project conversation on port <council-browser-port>.

Codex EXEC receives a one-shot prompt built from the canonical role-prime card plus the same packet pointer. After all three dispatches are verified as accepted/running, the driver closes only temporary Moonwalker attachments, leaves provider tabs/processes alive, creates no polling loop, and yields. The owner wakes the driver when the seats are complete.

## 10. Acceptance criteria

The repaired round is ready for council dispatch only when:

- every new normative JSON file parses and passes its schema/invariant tests;
- all fourteen red witnesses fail the old contract or their isolated old behavior and pass the repaired contract;
- the r6 synthesis maps every r6 finding to `ADOPT`, `ADOPT-WITH-MODIFICATION`, `REJECT`, or `DEFER`, with a byte-level rationale;
- the pinned bundle table is generated from committed Git objects and independently reverified;
- the r7 packet contains no stale r1-r6 bundle pin or prompt pointer;
- the two browser seats are attached through Moonwalker to the exact maintained conversation IDs;
- Codex EXEC is read-only and ephemeral; and
- no harness implementation or paid inference occurs.

## 11. Explicit non-goals

- No production authorization, hostile-box, FIPS/CNSA, deployment, fleet, PR, licensing, or commercialization design.
- No concurrent canonical writers, federation, consensus, or next-stage coordination experiment.
- No cross-model, personality, procedural-memory, or affect claim.
- No new semantic comparator unless the next council demonstrates a public semantic object outside FD/FC/TN.
- No deletion, staging, or rewriting of preserved untracked operational files.
