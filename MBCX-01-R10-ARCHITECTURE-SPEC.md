# MBCX-01 r10 architecture repair

Date: 2026-08-12  
Authority: proposed successor to the r9 normative bundle  
Evidence class: preregistration and executable no-model verification only

## 1. Decision in plain language

r10 keeps the experiment because the research question remains answerable. It stops pretending every kind of uncertainty can be repaired by buying calls. The scientific run stays at 768 paired scenarios. We first prove that state reconstruction, packets, scoring, cohort selection, physical accounting, and inference execute exactly as preregistered. Separately, a much smaller route qualification asks whether the actual six-call pair can be delivered reliably enough. If transport is not qualified, there is no paid scientific run.

## 2. Normative bundle

The governing commit contains and the pin manifest hashes:

- this architecture and the prior-art memo;
- state/action contract v5;
- packet schemas v4;
- measurement contract v4;
- inference contract v5;
- two structurally independent state engines;
- the r10 verifier and strict-Ajv verifier;
- the Git-object reconstruction wrapper;
- the no-paid verification report.

The council packet pins both the governing commit and the manifest blob. The wrapper reconstructs every listed subject from `git cat-file`, verifies SHA-384 and byte counts, then executes only the reconstructed verifier.

## 3. State and action semantics

There is one shared schema ingress boundary. Independence is claimed only after an event has passed the same compiled schema. Both reducers then implement the transition semantics using different control structures.

An event is usable only when its envelope and event-specific payload pass JSON Schema 2020-12, its UTC timestamps are real calendar instants at microsecond precision, and its event ID matches the canonical event preimage.

At cut `C`, a fact is visible exactly when:

`journal_seq <= C.journal_seq AND observed_at <= C.knowledge_time`

and effective exactly when:

`valid_from <= C.valid_time AND (valid_to IS NULL OR C.valid_time < valid_to)`.

Retracted facts are excluded. Opening a handoff must bind the deterministic action ID, originating cut hash, action-catalog hash, and canonical snapshot hash. Recording a response must bind the handoff ID, request hash, response hash, and schema-preserving response bytes. Forged values are rejected rather than normalized.

## 4. Packets, served bytes, and scoring

Six closed schemas are compiled with Ajv strict mode: cut, decision packet, worker handoff, writer receipt, scorer input, and experiment packet manifest. Conditional array constraints carry explicit array types.

The experiment manifest is the only authority for scenario ID, scope ID, cut, observation, action universe, and canonical world hashes. BC and OM builders receive that same manifest and cannot substitute an action universe. Semantic validation rejects invented or changed objects even when they are structurally valid.

The served model input is deterministic canonical UTF-8 padded with ASCII spaces to exactly 65,536 bytes. Overflow is a pre-dispatch design failure. The manifest records the SHA-256 of those exact served bytes. Exact scoring consumes validated A0, worker response B, writer receipt, A1, and the expected manifest; the success predicate is `A0 AND B AND A1`, with all identity and hash links checked first.

## 5. Cohort

Before selection, reject an unknown motif, duplicate scenario ID anywhere, the wrong motif totals, or a declared eligibility Boolean that is being used as authority. Choose one cut deterministically before recomputing eligibility from canonical state. The selected cohort is exactly six motifs times 128 scenarios = 768 pairs.

## 6. Finite-range physical-work gate

The claim is finite-range practical boundedness, not big-O. Measure all 100 frozen cells:

- `H in {128, 1024, 10000, 100000}`;
- `D,F in {1,4,16,64,256}`.

For each `(D,F)`, aggregate root and descendant instructions, CPU time, wall time, and peak committed memory with a non-breakaway Windows Job Object. A candidate fails boundedness when aggregate work is missing, a child escapes, any required cell is absent, or the preregistered H-range tolerance is exceeded. It fails affordability separately when absolute budgets are exceeded. Under the frozen instruction tolerance of 500,000, a `5*H` diagnostic spans 499,360 and is inside tolerance; a root or hidden-child `10*H` diagnostic spans 998,720 and must fail. A constant four-million-instruction candidate may be bounded but unaffordable. No claim that all linear functions fail, or that logarithmic functions pass, is made.

## 7. Provider-call state machine

Every logical call advances through an executable transition matrix over:

`PREPARED -> DISPATCHED -> RESPONSE_DURABLY_RECORDED`

or terminates as `PROVEN_PRE_ACCEPT_FAILURE` or `ACCEPTANCE_AMBIGUOUS`. Response bytes and their hash are durably recorded before parsing. A retry is permitted only after a proven pre-accept failure and must reuse the identical request hash and idempotency token. Ambiguous acceptance is terminal missing unless the frozen route attests exact idempotent replay and parameter-mismatch rejection. Every state/event pair and crash window is tested.

## 8. Missingness and scientific decision

There is no arbitrary maximum missing-pair count. For each stream, an exact dynamic-programming hull enumerates all reachable prefix sums while retaining the maximum self-normalizer needed for the future confidence-sequence boundary. Delta missing increments are `{0, 0.5, 1}` and OM missing increments are `{0,1}`. The implementation returns the minimum lower endpoint and maximum upper endpoint over every completion.

A substantive branch is reported only when that same branch is certified for every legal completion. Otherwise the result is `TRANSPORT_INCONCLUSIVE`. With no missing outcomes, the ordinary inconclusive result remains ordinary `INCONCLUSIVE`. The DP is checked against exhaustive enumeration for small missing counts and against a branch-flip witness.

## 9. Frozen inference and indifference region

The single scientific look remains `n=768`. The numerical operating-characteristic promise is restricted to clear regions:

- promote assurance: `delta >= 0` and `OM >= 0.90`;
- interface-fail assurance: `delta <= -0.20` and `OM >= 0.90`;
- ceiling assurance: `OM <= 0.70`.

Exact thresholds, `0.70 < OM < 0.90`, and delta transition values carry no 90% assurance promise. The former `delta=-0.25, OM=0.85` cell is diagnostic only. This makes the ±0.10 OM indifference band explicit without inflating the scientific run merely to force a decision near the threshold.

## 10. Transport readiness

One soak trial runs the exact frozen six-call pair route and retry policy. Failure means any position does not produce one unique, route-attested, schema-preserving response. Every launched trial remains in the denominator, including DNS, connection, authentication, refusal, timeout, and `OTHER_UNCLASSIFIED` failures.

Transport is ready only after 456 representative independent trials with at most four failed pairs. The exact-binomial design has consumer risk below 0.05 at a 2% bad-pair rate and at least 90% pass probability at a 0.5% good-pair rate. Mode and call position are diagnostics, not separate deciding cells. This gate schedules 2,736 calls before retries and is never conflated with the 4,608 scheduled scientific call positions.

## 11. Stop/go order

1. No-model verifier and Git-object reconstruction pass.
2. Council returns no blocking defect.
3. Physical harness passes boundedness and affordability.
4. Transport soak passes the frozen 456/4 rule within a separately frozen raw-attempt and dollar ceiling.
5. Only then may the owner authorize the 768-pair paid experiment.

Any earlier failure stops the program without spending the later budget.

