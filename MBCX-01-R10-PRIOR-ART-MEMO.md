# MBCX-01 r10 prior-art memo

Date: 2026-08-12  
Status: architectural input, not experimental evidence  
Paid model calls performed: 0

## Bottom line

The r9 failures do not require a novel statistical theory. They are recognizable instances of existing engineering disciplines. r10 therefore borrows the smallest established mechanism for each boundary instead of hiding uncertainty behind more calls.

1. **Temporal truth:** keep valid time and recorded/known time distinct, then make visibility and effectivity explicit predicates. This follows the bitemporal distinction in Jensen and Snodgrass: valid time models when a fact is true in the modeled world, while transaction/record time models when it is present or known in the database ([Temporal Data Management](https://www.researchgate.net/publication/3296807_Temporal_data_management)).
2. **Schema enforcement:** compile and execute the real schemas at ingress. JSON Schema 2020-12 distinguishes format annotation from assertion and requires implementations that support assertion to validate the complete format syntax ([JSON Schema validation](https://json-schema.org/draft/2020-12/json-schema-validation)); Ajv strict mode also requires an applicable type for keywords such as `minItems` ([Ajv strict mode](https://ajv.js.org/strict-mode.html)).
3. **Retry safety:** a retry is safe only when the caller supplies a stable token and the service binds that token to the same request parameters and prior result. AWS describes the atomic token-plus-operation pattern and rejects token reuse with different parameters ([Making retries safe](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)); Stripe likewise returns the first result for a reused key and errors on parameter mismatch ([Stripe idempotent requests](https://docs.stripe.com/api/idempotent_requests)).
4. **Process-tree work:** measure the process tree, not the root process. Windows Job Objects aggregate accounting for associated processes, including terminated children, while breakaway and nested-job rules must be controlled ([Microsoft Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)).
5. **Transport qualification:** use a binomial reliability-demonstration plan with declared producer and consumer risks. NIST describes exact binomial limits by cumulative-binomial inversion ([NIST exact binomial limits](https://itl.nist.gov/div898/software/dataplot/refman2/auxillar/exacbino.htm)); NASA reliability-demonstration guidance treats sample size and allowable failures as an acceptance plan with both risks declared ([NASA/TP-2010-216447](https://ntrs.nasa.gov/api/citations/20100038453/downloads/20100038453.pdf)).
6. **Missing outcomes:** report what is identified over all possible completions instead of assuming missing at random. This is the partial-identification stance associated with worst-case missing-data bounds ([Manski, 2005](https://www.sciencedirect.com/science/article/pii/S0888613X04001124)).
7. **Reconstruction:** pin subjects and dependencies by digest and reconstruct the bytes before execution. This is the same consumer-verification shape used by SLSA provenance ([SLSA build provenance](https://slsa.dev/spec/v1.2-rc2/build-provenance)); Git exposes exact object contents with `git cat-file` ([Git cat-file](https://git-scm.com/docs/git-cat-file)).

## Transport plan derived from the scientific endpoint

The scientific unit is a complete pair, and one pair requires six scheduled call positions. The transport gate should therefore qualify the complete six-call route, not 48 mode-by-position cells with separate zero-failure budgets.

Freeze two operating points:

- unacceptable full-pair missing probability: `p_bad = 0.02`;
- acceptable full-pair missing probability: `p_good = 0.005`.

An exhaustive integer search of exact binomial tails gives the smallest plan satisfying both frozen risks:

- launch `n = 456` independent, representative full-route trials;
- accept transport readiness when failures are `<= 4`;
- consumer risk: `P(accept | p = 0.02) = 0.049433329807588314 <= 0.05`;
- producer success probability: `P(accept | p = 0.005) = 0.9190668746549462 >= 0.90`.

This schedules 2,736 call positions before retries, versus r9's 98,868. More calls now buy a quantifiable reliability decision; they do not buy scientific evidence. No soak is executed in this design round.

## Deliberate non-claims

- The Job Object design does not prove asymptotic complexity. It supports a preregistered finite-range practical-boundedness decision over the 100 frozen `(H,D,F)` cells.
- Idempotency cannot be manufactured by the client when provider acceptance is ambiguous. A route lacking a frozen, attested idempotency contract must mark that pair missing.
- Worst-case missingness bounds do not recover unknowable outcomes. They make the scientific branch only when every permitted completion yields the same branch.
- The 456-trial calculation assumes representative independent Bernoulli trials at the frozen route and retry policy. Drift requires requalification.

