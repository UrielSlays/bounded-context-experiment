# MBCX-01 r8 Executable Reconstruction Design

**Date:** 2026-08-12  
**Status:** owner-approved for inline no-paid implementation and council dispatch  
**Repository:** `<repo>`

## 1. Objective

Produce a five-artifact preregistration whose load-bearing state, packet, measurement, inference, cohort, and transport rules are executable or mechanically decidable. The repair must make the registered conclusion a function of frozen bytes rather than an implementer's later interpretation.

This round may run deterministic validators and synthetic operating-characteristic simulations. It may not implement the FD/FC/TN candidates, call a paid model endpoint, or claim an experiment result.

## 2. Governing repair principle

The r7 council's three NO-GO reports converge on one root cause: declaration presence was being tested where behavioral totality was required. r8 therefore uses the following acceptance rule:

> A normative statement that can change a scientific branch must be represented by closed data and exercised by an independent witness, or the design must say why no executable representation is possible.

Static grep or string-presence checks do not earn scientific credit.

## 3. Artifact topology

The r8 review target is:

1. `MBCX-01-EXPERIMENT-DESIGN-r7.md` — question, scope, cohorts, DAG, gates, and decisions.
2. `MBCX-01-STATE-ACTION-CONTRACT-v3.json` — closed transition and transport machines.
3. `MBCX-01-PACKET-SCHEMAS-v2.json` — closed schemas for inputs and scored outputs.
4. `MBCX-01-MEASUREMENT-CONTRACT-v2.json` — finite-range physical-work claim and full interaction grid.
5. `MBCX-01-INFERENCE-CONTRACT-v3.json` — exact mixture confidence sequence, terminal rule, synthetic OC, missingness, and cost outputs.

Supporting executables are `mbcx01_r8_reference.py` and `verify-r8-normative-bundle.py`. The latter imports and exercises the former against literal, hand-derived witnesses.

## 4. State and action machine

### 4.1 Collision-free identity

Public action IDs are opaque hashes, never delimiter-parsed strings. The identity preimage is RFC 8785/JCS over:

```json
{"schema_id":"ActionIdentityV1","scope_id":"<scope>","obligation_id":"<obligation>"}
```

The public representation is `ACT.` plus uppercase SHA-256 hex. A closed action catalog maps the public ID back to the structured scope and obligation. A witness must prove that `scope=S:A, obligation=B` and `scope=S, obligation=A:B` differ.

### 4.2 Total semantic transitions

All seventeen event types define:

- closed required payload fields and value domains;
- legal prestate predicate;
- deterministic effect;
- exact duplicate behavior under `(scope_id, semantic_operation, idempotency_key)`; and
- frozen illegal result code.

All child actions in one handoff proposal validate against the immutable originating cut. Provisional effects cannot make another child legal in the same proposal. Newly unblocked obligations require a later decision.

The writer checks the proposal against the exact TaskPacket originating cut, constructs all children, and atomically appends either all children plus one commit terminal or one rejection terminal and no children.

### 4.3 Executable pair coverage

The reference machine generates 289 ordered event-type pairs. Each fixture uses one shared scenario/scope and, where meaningful, one shared entity. The oracle records prestate, first result, intermediate state, second result, and final state. It also executes named traces for atomicity, idempotency, retroactivity, dependency cycles, handoff status, and provisional-prestate leakage.

## 5. Call ledger and retry semantics

Provider call records are separate from semantic state and follow a closed machine:

- `PREPARED -> DISPATCHED`;
- `DISPATCHED -> RESPONSE_DURABLY_RECORDED`;
- `DISPATCHED -> PROVEN_PRE_ACCEPT_FAILURE`; or
- `DISPATCHED -> ACCEPTANCE_AMBIGUOUS`.

Response bytes are durably recorded before parse. A crash after dispatch but before a durable response is `ACCEPTANCE_AMBIGUOUS`, not a presumed failure. Retry is allowed only from `PROVEN_PRE_ACCEPT_FAILURE`, unless a frozen provider contract proves exact idempotency-token and request-parameter binding. Otherwise the complete six-call pair is missing with no resample.

## 6. Closed packets and exact scoring

`DecisionPacketV3`, `TaskPacketV3`, `WorkerHandoffV3`, `A0ResultV1`, and `A1ResultV1` are closed JSON Schema 2020-12 objects. Every object in a decision packet is discriminated by `object_kind`, and every corresponding `fields` object is closed. No condition label, free text, transcript, scratch space, arbitrary config, or unbounded array reaches the model.

The conductor, not A0, deterministically builds `TaskPacketV3` from a valid `A0ResultV1`. Conditional rules require one or more proposed actions for `PROPOSE` and zero actions for `ABSTAIN` or `REJECT`.

Scoring is exact:

- A0 passes iff its selected action equals the unique frozen gold action.
- B passes iff its schema-valid proposal commits the target exactly once.
- A1 passes iff its selected set equals the independently recomputed post-commit gold set.
- Condition success is the conjunction of A0, B, and A1.
- Schema-invalid model output is condition failure, not transport missingness.

Packet hash is uppercase SHA-384 over JCS of the complete packet object with `packet_hash` omitted. Served-input hash covers the exact padded bytes. The verifier constructs a maximal schema-valid packet and proves it fits the 65,536-byte envelope.

## 7. Frozen cohort and source provenance

Candidate source, build, dependency, and configuration hashes freeze before confirmatory scenario generation. Confirmatory scenario/gold code is not readable by candidate processes.

For each of six motifs, generate 80 unique scenario IDs. For each scenario, sort its cut IDs and choose exactly one cut using SHA-256 over a length-framed tuple `(scenario_id, sorted_cut_ids, "stage2-cut-r8")`. Apply eligibility to that one cut only. Retain the first 64 unique eligible scenario IDs per motif by a separate length-framed selection hash. No scenario duplication is allowed. Any shortfall is `DESIGN_OR_IMPLEMENTATION_FAIL`.

The estimand is conditional on this frozen eligible population. The design makes no unbiased-sampling claim. The manifest publishes every exclusion, motif, and registered difficulty stratum.

## 8. Measurement claim

The claim is finite-range registered physical work, not universal asymptotic boundedness. At `F=16`, test the full Cartesian product:

- `H in [128,1024,10000,100000]`;
- `D in [1,4,16,64,256]`.

Keep the separate registered F curve. Freeze the storage backend and 4096-byte page size.

All candidate descendants are charged. The closed counter catalog covers source/artifact bytes and records, pages, dependency operations, decode/materialization operations, CPU instructions, process CPU time, peak RSS, filesystem/database bytes, and implementation branches. Counter semantics include exact sampling boundaries and aggregation. Unit-total gates must be strictly below the arithmetic sum of their per-counter maxima; equality is invalid.

Red candidates include an interior H-by-D hotspot at `(10000,64)`, low-slope archive-linear work, unregistered CPU work, counter splitting, page-size substitution, and logical lookup hiding a physical scan.

## 9. Inference and synthetic OC

### 9.1 Estimands

The paired delta stream is `BC_i-OM_i` and the OM stream is `OM_i`, in the complete frozen 384-scenario SHA-256 order. Conditional means may change arbitrarily by scenario; within-pair dependence is unrestricted.

### 9.2 Confidence sequence

Use the exact mixture empirical-Bernstein confidence sequence in Proposition 3.1 of Chugg and Ramdas (2025), with `kappa=0.25` and alpha 0.025 per stream. For observations `X_i in [0,1]`:

```text
xhat_i = (0.5 + sum_{j<i} X_j) / i
psi_E(x) = -log(1-x) - x
U_t = 1/(2*kappa^2) + sum_i psi_E(abs(X_i-xhat_i))
I(y;v) = integral[-1,1] exp(y*z-v*z^2) dz
accept m iff I(sum_i X_i-t*m; U_t) < kappa*Z*sqrt(2*pi)/alpha
Z = Phi(1/kappa)-Phi(-1/kappa)
```

The primary evaluator uses stable analytic integration and fixed bisection. An independent Simpson integrator must agree within the frozen tolerance. Delta is transformed to `[0,1]` and mapped back.

### 9.3 Decision timing

Looks 96 and 192 publish diagnostics and projected cost only. They never bind a scientific branch. The only scientific decision is at n=384, so a prefix average cannot be mistaken for the full-manifest estimand.

At n=384 and after missingness sensitivity:

- promote iff delta lower > -0.10 and OM lower >= 0.80;
- interface fail iff delta upper < -0.10 and OM lower >= 0.80;
- ceiling iff OM upper < 0.80;
- otherwise inconclusive/underfunded.

Hard deterministic failures and transport inconclusive take precedence.

### 9.4 Missingness and OC

At most seven missing pairs are jointly enumerated over `{00,01,10,11}^m`; a branch is reported only if invariant over all completions. Eight missing pairs is transport inconclusive. Placement and outcome-association algorithms are exact deterministic functions of a counter-based SHA-256 stream.

No-paid OC uses the nine fixed valid paired-probability cells, 10,000 replicates, n=384, and exact categorical inverse-CDF sampling. It publishes terminal branch frequencies, interval widths, missingness sensitivity, maximum accepted calls (2,304), and expected accepted calls (also 2,304 because no scientific early stop exists). Synthetic draws are never labeled model evidence.

## 10. Verification gates

The r8 verifier must fail before the artifacts exist and pass only after it executes:

1. JSON parsing and closed-schema invariants;
2. action collision and 289 ordered transition pairs;
3. same-prestate multi-action atomicity;
4. call-ledger ambiguous-acceptance behavior;
5. maximal-packet envelope and hash witnesses;
6. source-freeze-before-cohort ordering and unique one-cut selection;
7. exact full 20-cell H-by-D grid and all measurement red candidates;
8. analytic/quadrature inference agreement and literal reference vectors;
9. terminal-only decision timing and prefix-reversal witness; and
10. deterministic OC repeatability.

## 11. Council and dispatch

The packet asks the maintained Claude and ChatGPT seats to review the pinned r8 bytes without seeing another seat's current verdict. The same owner-style two-line pointer is sent through Moonwalker. Codex EXEC is a fresh, read-only, one-shot seat. After all three are visibly accepted/running, temporary browser attachments close and the driver yields without polling.

## 12. Non-goals

- no paid call or provider soak that consumes paid inference;
- no implementation or benchmarking of FD, FC, or TN;
- no production, hostile-box, security, persistent-mind, personality, or coordination-stage claim;
- no proof beyond the frozen finite ranges;
- no rewrite or staging of unrelated untracked operational files.
