# MBCX-01 r9 Answerable Experiment Design

**Date:** 2026-08-12  
**Status:** owner-approved for inline no-paid reconstruction  
**Repository:** `<repo>`

## Objective

Repair the preregistration so it can answer the original MBCX-01 question without weakening that question: can exact selective obligation continuity remain physically bounded across the complete frozen H, D, and F ranges, and can one frozen model use the resulting bounded context without materially underperforming an oracle-minimal context?

The repair may execute deterministic local validators, generated traces, mutation tests, packet builders, measurement red candidates, reference-vector calculations, and synthetic operating-characteristic simulations. It may not implement the FD/FC/TN candidates, make paid model calls, or report an experiment result.

If the repaired instrument later falsifies bounded continuity, that falsification is an acceptable answer. The design must not narrow the range or tune statistical parameters to manufacture a favorable branch.

## Versioned r9 bundle

r8 remains immutable audit history. r9 creates:

- `MBCX-01-EXPERIMENT-DESIGN-r8.md`;
- `MBCX-01-STATE-ACTION-CONTRACT-v4.json`;
- `MBCX-01-PACKET-SCHEMAS-v3.json`;
- `MBCX-01-MEASUREMENT-CONTRACT-v3.json`;
- `MBCX-01-INFERENCE-CONTRACT-v4.json`;
- `mbcx01_r9_oracle.py`;
- `mbcx01_r9_reference.py`; and
- `verify-r9-normative-bundle.py`.

The normative five-artifact bundle is the design plus four JSON contracts. The oracle, reference, and verifier are no-paid executable witnesses and receive their own Git-object pins.

## State and event semantics

Every semantic event uses a closed `EventEnvelopeV1` with `event_id`, `scope_id`, `event_type`, `semantic_operation`, `idempotency_key`, `journal_seq`, `observed_at`, `valid_from`, optional `valid_to`, `originating_cut`, and a closed event-specific `payload`.

Idempotency is keyed only by `(scope_id, semantic_operation, idempotency_key)`. Reuse with identical canonical event meaning is `DUPLICATE_NOOP`; reuse with different meaning is `IDEMPOTENCY_CONFLICT`. Event-ID reuse with different bytes is `EVENT_ID_CONFLICT`. Scope is never hard-coded or inferred from payload text.

The v4 contract replaces prose-only guards and effects with closed `guard_id` and `effect_id` enums. A journal reducer and a separately implemented declarative oracle must agree on exact result and exact post-state. They may share serialization and contract loading, but no guard, effect, graph, cut, or idempotency implementation.

The verifier executes hand-derived traces, all 289 ordered event-type pairs, deterministic generated traces, and named mutants. At minimum it must kill reducers that ignore rescheduling, ignore delegation, check only two-node cycles, skip originating-cut checks, treat every payload hash as an idempotency key, or mutate only the `seen` set.

Full graph reachability rejects cycles of any length. Reschedule and delegation update their named fields. Fact correction/retraction uses visible bitemporal version chains. Handoff commit constructs and atomically applies the frozen child events or appends none. Exact duplicate events never change semantic or bookkeeping state.

## Packet construction and scoring

JSON Schema handles local shape. A separate semantic validator enforces cross-record meaning:

- unique object IDs and action IDs;
- exactly one catalog resolution for every available action;
- no conflicting duplicate target;
- `NO_ACTION` has the no-action discriminator and no target;
- every `ACT.*` hash recomputes from its structured scope and obligation;
- every action target and prerequisite resolves at the packet cut;
- all IDs belong to the packet scenario and scope where required;
- packet hash recomputes from canonical bytes; and
- encoded bytes are strictly below 65,536 before padding or dispatch.

The schema no longer claims that every syntactically valid cap-saturating object fits the envelope. An oversized but otherwise schema-valid object deterministically returns `PACKET_ENVELOPE_EXCEEDED`, which is `DESIGN_OR_IMPLEMENTATION_FAIL`, before any provider call. Every retained BC and OM packet must pass semantic and byte validation; the manifest publishes their sizes and maximum.

The BC builder receives the candidate's selected public semantic object IDs and renders those canonical cut objects. The OM builder receives the independent gold enumerator's read-set: the exact public semantic objects causally consulted to compute the unique gold action and post-commit gold set. Both builders use the same action universe, neutral schema, field descriptions, instructions, ordering, byte envelope, padding length, output schema, and transport settings. Neither receives a condition label, due/gold annotation, answer ID, or free text.

The Stage-2 B score is unambiguous: B passes only when the schema-valid proposal is exactly the singleton target action and the writer commits exactly that singleton once, with no extra child. The general writer may still be tested with multi-child proposals for atomicity outside the Stage-2 score.

## Workload and cohort freeze

The owner freezes the generator specification, distribution parameters, gold enumerator, eligibility evaluator, and their source hashes before candidate implementation is inspected. Candidate source, build, dependencies, and configuration then freeze. Only afterward is a fresh confirmatory seed minted and kept unreadable by candidates while the 960 scenarios are generated.

One cut is selected before eligibility. Eligibility is recomputed from canonical state at that cut and requires exactly one mounted critical due obligation plus at least one non-gold action. The selector rejects any supplied eligibility Boolean. Retention is 128 unique eligible scenarios per motif and 768 globally unique scenarios.

## Physical-work measurement

The boundedness claim covers the full Cartesian product of the frozen axes: four H values, five D values, and five F values, for exactly 100 unique cells. The previous 20-cell plane plus F curve is insufficient for this claim.

The evaluator consumes actual per-cell counter records. It enforces per-counter ranges, same-unit totals, registered shape gates, descendant accounting, and cross-counter coherence. Database read and write byte counters are separate. `PAGES_READ=ceil(DATABASE_BYTES_READ/4096)` and `PAGES_WRITTEN=ceil(DATABASE_BYTES_WRITTEN/4096)`; inconsistent page/byte reports are design failures.

Every named red candidate is executable and produces counter records over the real 100-cell grid. The `LOW_SLOPE_ARCHIVE_LINEAR_10X` candidate performs `10*H` root CPU instructions and must fail the registered H-shape gate. Other required mutants cover an H-D-F hotspot, hidden child CPU, counter splitting, page-size substitution, and a logical lookup backed by a physical scan. The verifier must call the evaluator on each candidate and observe its specified failure; comparing declaration strings earns no credit.

## Inference, power, and reliability

The primary interval remains Proposition 3.1's exact mixture confidence sequence for average conditional means. Proposition 3.1 permits every `kappa > 0`; r9 freezes `kappa=0.25` before outcomes because the source authors use it as their stated default. It is not tuned to MBCX-01 operating characteristics. A nonbinding sensitivity table at `kappa` 0.10, 0.15, 0.25, 0.50, and the uniform-mixture limit publishes terminal interval widths and branch reachability.

Only n=768 computes scientific intervals. The former n=96, n=192, and n=384 intervals are deleted; operational progress and projected-cost counters may remain. This sample is the smallest tested value among 384, 512, 768, and 1024 expected to clear 90% at the registered practical promote, interface-fail, and ceiling alternatives; exact and near cutoffs remain an explicit indifference region.

The OC grid restores near-floor power visibility. Negative-delta cells are crossed with OM marginals 0.80, 0.85, and 0.95, and the publication reports the full curve. No single OM=0.95 cell may headline interface-failure power. Fixed equal, ceiling, positive-delta, and discordance cells remain for branch coverage.

Reference vectors freeze exact sequences, including the positions of every discordant pair. Expected endpoints are produced independently by the analytic implementation, Simpson quadrature, and a high-precision decimal integration witness. Any disagreement above the frozen tolerance fails verification.

Transport readiness freezes the missingness failure-mode catalog and six call positions. For `M` modes, each mode-position cell receives confidence error `0.05/(6M)` and failure budget `0.02/(6M)`. The deciding gate requires every one-sided exact upper bound to fit its cell budget, giving simultaneous 95% familywise coverage and a union-bounded pair-missing probability no greater than 0.02.

Local `DESIGN_OR_IMPLEMENTATION_FAIL` precedes `TRANSPORT_INCONCLUSIVE`, so transport cannot hide a known broken instrument.

## Verification and dispatch

Tests are behavioral and test-first. The verifier must initially fail on r8's known false greens, then pass only after the versioned r9 artifacts and implementations exist. Full verification runs from the working tree and again from extracted pinned Git blobs.

The no-paid report identifies working-tree evidence separately from Git-object evidence. Council packet hashes and byte counts are generated only from `git cat-file` output for the named commit, preventing CRLF checkout bytes from masquerading as Git blobs.

After local verification, r9 is sent to the same maintained Claude and ChatGPT seats through Moonwalker and to one fresh read-only Codex EXEC seat. The driver confirms all three accepted the r9 packet, closes only temporary Moonwalker attachments, and then yields. No paid experiment call is authorized by council dispatch.

## Non-goals

- No weakening to the old 24 measured triples.
- No formal model checker or proof assistant unless the two independent implementations still disagree.
- No FD/FC/TN candidate implementation or benchmark.
- No paid inference, provider soak with nonzero cost, or experiment result.
- No production, security, hostile-box, persistent-mind, personality, procedural-memory, or coordination claim.
- No modification or deletion of unrelated untracked files and operational logs.
