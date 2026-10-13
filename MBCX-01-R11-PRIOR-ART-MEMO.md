# MBCX-01 r11 prior-art and orthogonal-method memo

Date: 2026-08-13  
Purpose: decide whether r10's architectural failures should be repaired with established primitives or whether the experiment should be abandoned.

## Findings that changed r11

### Windows process-tree evidence

Microsoft documents that Job Objects aggregate accounting for associated processes, including terminated processes, and exposes `JOBOBJECT_BASIC_AND_IO_ACCOUNTING_INFORMATION`. It also documents the two breakaway flags and warns that completion-port association should occur while the job is inactive to reduce missed state transitions. ETW exposes sampled profile sources/counters, but configuring and attributing those events is a separate harness obligation. r11 therefore requires assignment-before-resume, no-breakaway flags, job-wide CPU/I/O accounting, active-zero completion, a drained completion port, a final accounting query and pinned retired-instruction attribution rather than accepting candidate-authored counters. These documents define the harness requirement; they do not make the unimplemented harness pass.

Primary origins:

- https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects
- https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_and_io_accounting_information
- https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_associate_completion_port
- https://learn.microsoft.com/en-us/windows/win32/api/evntrace/ne-evntrace-trace_query_info_class

### Idempotency and durable response identity

AWS's idempotent-API design binds a caller-provided token to one logical request and treats same-token/different-intent reuse as a mismatch. Stripe persists the first result for an idempotency key and compares later parameters. r11 borrows the stable token + exact parameter binding but adds the experiment-specific raw-response/durability evidence and restart digest.

Primary origins:

- https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/
- https://docs.stripe.com/api/idempotent_requests

### Acceptance sampling and dependence

NIST's `(n,c)` OC construction explicitly says “if we are willing to assume that binomial sampling is valid.” NIST's software-testing report separately names constant probability and independence as assumptions and suggests randomized or stratified sampling from a defined test population. This confirms the council's diagnosis: a frozen schedule helps define representativeness but cannot by itself create independence.

r11 takes an orthogonal path. It replaces the marginal iid premise with full-past conditional-failure hypotheses and a finite-horizon conditional-expectation recursion. At each history, the probability of ending with at most four failures is monotone decreasing in the next conditional failure probability. Recursing backward therefore places the bad-route maximum acceptance at a `.02` hazard at every history and the good-route minimum acceptance at `.005` at every history. This proves the same two binomial CDF bounds without iid and without silently assuming a regular conditional generative representation for arbitrary full-history spaces. It plainly refuses a guarantee for processes having only the same marginal rate.

Primary origins and comparison literature:

- https://itl.nist.gov/div898/handbook/pmc/section2/pmc232.htm
- https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nistir6129.pdf
- https://arxiv.org/abs/math/0512301 (related binomial tail bounds for bounded supermartingales; r11 uses the finite-horizon recursion stated above)

### Temporal intervals

The r10 fact defects are ordinary temporal-integrity defects: treating `valid_to is null` as “head” is not equivalent to visibility/effectivity, and a correction must preserve nonempty/nonoverlapping half-open intervals. r11 makes those interval invariants executable rather than relying on a nullable endpoint convention.

Primary origins:

- https://www.postgresql.org/docs/current/ddl-temporal-constraints.html
- https://github.com/xocolatl/periods

### Artifact verification

SLSA artifact verification begins from configured trust material and checks that the subject digest matches the artifact being used. r11 therefore moves launcher extraction to the council-pinned Git blob before execution and vendors the schema-validator runtime inside the governed subject set.

Primary origin:

- https://slsa.dev/spec/v1.2/verifying-artifacts

## Findings that did not change r11

The Chugg/Ramdas exact-mixture empirical-Bernstein method remains applicable to bounded adapted observations with varying conditional means, and the exact missing-completion DP survived independent differential attacks. r11 ports those reviewed primitives into its own module but does not change the ruler solely to gain a few fixed-terminal-sample points. The scientific result is still evaluated once at 768; the time-uniform method is conservative but already validated and supports the registered filtration.

Primary origin:

- https://arxiv.org/abs/2512.21300

## Cost conclusion

Prior art supports repairing r10, not deleting the experiment. Every blocking failure except physical-harness realization is a no-paid contract/implementation repair. The power defect is repaired by narrowing an overbroad planning claim to explicit joint cells, not by purchasing 384 extra scenario pairs. The next council should specifically attack the conditional-hazard route redesign and the end-to-end identity graph; those are the two r11 judgments most likely to benefit from adversarial review.
