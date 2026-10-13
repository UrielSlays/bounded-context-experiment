# MBCX-01 r8 Orthogonal Methods and Open Questions

**Date:** 2026-08-12  
**Status:** research disposition for no-paid reconstruction; not experiment evidence and not paid authorization

## Bottom line

The repeated council failures do not invalidate the original research question. They expose a recurring category error: prose was allowed to stand in for an executable scientific instrument. The r8 repair therefore borrows mature machinery from four neighboring fields while keeping the MBCX-01 estimand unchanged.

The useful transfers are:

1. a variance-adaptive, time-uniform empirical-Bernstein confidence sequence for heterogeneous bounded outcomes;
2. a full H-by-D factorial grid because the grid has only twenty cells and interactions are part of the claim;
3. property-oriented finite-state-machine testing for executable transition witnesses; and
4. explicit idempotent-request and unknown-acceptance states for provider transport.

None of those transfers authorizes paid inference or makes the mechanism claim broader.

## 1. Sequential inference: use the paired variance instead of discarding it

The r7 Hoeffding interval is valid for the registered average conditional mean, but its terminal delta radius is approximately 0.169 at n=384. That is wider than the 0.10 noninferiority margin and gives nearly no useful promotion power under the registered equal, low-discordance cells. Buying more calls would be paying to compensate for an unnecessarily blunt ruler.

Chugg and Ramdas, *Closed-form empirical Bernstein confidence sequences for scalars and matrices*, gives a time-uniform empirical-Bernstein confidence sequence for bounded observations and explicitly targets the running average of possibly changing conditional means. Proposition 3.1 supplies an exact mixture boundary with a predictable estimate and no common-mean assumption. Source: <https://arxiv.org/abs/2512.21300>.

### Transfer into r8

- Map each paired delta observation `BC_i - OM_i` from `[-1,1]` to `Y_i=(delta_i+1)/2` in `[0,1]`.
- Use Proposition 3.1's exact mixture set with `kappa=0.25` and `alpha=0.025` independently for the delta and OM streams.
- Invert the mixture numerically by deterministic bisection; independently verify the integral by deterministic Simpson quadrature.
- Use only the terminal n=384 result for the scientific branch. The 96 and 192 prefixes are diagnostics and cost telemetry, never binding evidence about the full frozen manifest.

A no-paid prototype already shows why this matters: deterministic samples from the registered `LOW_DISCORD_EQUAL` and `OM90_EQUAL` cells give terminal half-widths near 0.063 for delta and 0.090 for OM, respectively, which makes promotion reachable at n=384. That prototype is feasibility evidence for the ruler, not an experiment result.

### Open council question

Does Proposition 3.1, as transcribed in the r8 executable reference, cover the registered heterogeneous average-conditional-mean estimands with the stated two-stream alpha allocation? If not, name the exact violated premise and a replacement that preserves that estimand.

## 2. Experimental design: stop screening where interactions decide the claim

NIST distinguishes low-resolution screening designs from higher-resolution or full designs when interactions matter. The MBCX-01 boundedness claim explicitly depends on excluding H-by-D interaction growth. Sources: <https://www.itl.nist.gov/div898/handbook/pri/section3/pri3345.htm> and <https://www.itl.nist.gov/div898/handbook/pri/section4/pri43.htm>.

### Transfer into r8

- Run the complete four-by-five H-by-D grid at fixed `F=16`: 20 cells.
- Keep the separate F curve.
- Scope the result to the frozen H, D, and F ranges. Do not call a finite grid a universal asymptotic theorem.
- Add an interior-hotspot red candidate at `(H=10000,D=64)` plus a low-slope archive-linear candidate. Both must fail.

The extra deterministic cells are cheap compared with paid model inference and eliminate the most obvious aliasing hole.

### Open council question

Is the complete 20-cell grid sufficient for the finite-range claim, or is there a concrete interaction pattern inside the registered ranges that can evade it without violating another deterministic gate?

## 3. State semantics: make the contract a small executable machine

Huang, Krafczyk, and Peleska show how symbolic finite-state models can drive property-directed test generation and provide the oracle, rather than relying on declaration-presence checks. Sources: <https://www.sciencedirect.com/science/article/pii/S0167642323000874> and the technical report at <https://zenodo.org/records/5719524>.

### Transfer into r8

- Every one of the seventeen semantic event types gets a closed payload, precondition, effect, duplicate behavior, and illegal result.
- A dependency-free Python reference reducer executes the contract.
- The 289 ordered event-type pairs are generated against shared-entity fixtures from the machine, and the oracle checks intermediate state, final state, atomicity, and idempotency.
- Specific adversarial traces cover action-ID delimiter collision, provisional-prestate leakage, exact TaskPacket originating-cut guards, and response-journal recovery.

This is deliberately modest: it validates the normative reference machine, not a future FD/FC/TN implementation.

### Open council question

Which remaining answer-changing state behavior cannot be expressed or decided by the closed event/payload/guard/effect table and its executable oracle?

## 4. Provider transport: distinguish failure from unknown acceptance

AWS's idempotency guidance uses caller-provided request identifiers and parameter binding so a retry can return the same semantic result rather than repeat a mutation. Source: <https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/>.

### Transfer into r8

The call ledger has explicit states:

`PREPARED -> DISPATCHED -> RESPONSE_DURABLY_RECORDED`

or

`PREPARED -> DISPATCHED -> PROVEN_PRE_ACCEPT_FAILURE`

or

`PREPARED -> DISPATCHED -> ACCEPTANCE_AMBIGUOUS`.

Only a proven pre-acceptance failure may retry. An ambiguous post-dispatch outcome is a whole missing pair with no resampling unless the exact provider route has a frozen, documented idempotency-token contract that binds all request parameters.

### Open council question

Does the selected provider route actually expose a contractual acceptance receipt or idempotency binding strong enough to move an ambiguous call out of the missing-pair branch? Browser observations alone do not count.

## 5. Local prior-art alignment

The original MBCX design and the local worldwide prior-art synthesis already point toward event sourcing, checkpoints/materialized views, durable workflows, cold reconstruction, exact evaluators, and a thin domain contract. r8 does not introduce a new mechanism family. It makes those earlier recommendations operational:

- canonical evidence stays append-only;
- candidate projections remain derived and disposable;
- cold reconstruction remains mandatory;
- deterministic validators outrank model judgment;
- the least-cost no-paid kill remains ahead of inference spend.

## 6. Explicit non-transfers

- No common-mean paired-binomial test replaces the heterogeneous average-conditional-mean estimand.
- No finite grid is marketed as proof for unbounded H or D.
- No formal-method citation upgrades the executable reference into a proof of an unimplemented candidate.
- No idempotency pattern is assumed to exist at the provider unless the route contract says so.
- No synthetic OC run is reported as a model result.

## 7. Council request

Review the r8 bundle as an executable preregistration. For each borrowed method, answer `HELPFUL`, `NOT HELPFUL`, or `HELPFUL WITH A NAMED FIX`, and tie every objection to a reachable false-result path or an unmet theorem premise. Preference for another method is not a blocker unless it exposes such a path.
