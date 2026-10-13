# MBCX-01 methodology positions (owner-commissioned via the ratified #23 sweep, Group C3 — 2026-08-16)

Two positions the novelty sweep (`docs/MBCX-01-NOVELTY-SWEEP-FULL-REPORT-2026-08-16.md`)
showed this lane holds against published practice. Each is now argued rather than assumed.
Rationale addenda — no frozen scientific content changes.

## 1. Freeze-and-attest, not setup randomization

The measurement-bias literature's published remedy (Mytkowicz et al., ASPLOS 2009) is to
RANDOMIZE experimental setup so that setup-correlated bias averages out of point estimates.
This lane FREEZES the environment and ATTESTS it (signed host/environment facts, harness build
digest, no migration or save/restore during measurement) instead. The argument: the
preregistered physical claim is not a point estimate — it is a TOLERANCE ON A DIFFERENCE
(max−min retired instructions across the H range at fixed (D,F), threshold 500,000) computed
WITHIN one attested environment. Setup bias that is constant within the environment cancels in
the difference; randomization defends a quantity this design does not register.
Cross-environment generalization of the physical numbers is deliberately NOT claimed — the
attestation marks the boundary instead of hiding it. Residual stated honestly: within-run
nondeterminism (interrupt/DPC contamination, counter noise) does NOT cancel in the difference
and is carried as the declared A-3 residuals; the tolerance's magnitude is the allowance for
it, and the smoke run is what measures whether the allowance is realistic.

## 2. One-sided non-inferiority margin, not two-sided TOST equivalence

Gringras (arXiv:2603.10044) runs two-sided TOST equivalence at ±2pp — a stricter, symmetric
claim than this design's one-sided −0.10 margin. The positions differ because the QUESTIONS
differ: TOST answers "are these two the same?"; this experiment asks "is bounded context NOT
MATERIALLY WORSE than oracle memory?" — a directional question. BC OUTPERFORMING OM is not a
failure mode the research question needs to exclude; it would be a (surprising, reportable)
substantive branch, and the design's enumerated outcomes already carry it. Adopting the
symmetric form would spend statistical power excluding an outcome nobody needs excluded, at
fixed n=768. The one-sided margin at declared family error 0.05 across both streams is the
correct match of inference shape to question shape. Residual stated honestly: the margin's
VALUE (−0.10) is a design choice, not a derived quantity; it was frozen at preregistration
and its justification is operational (a 10-point drop is the smallest difference the owner
would act on), not statistical.

*Citation base: the novelty sweep full report (docs/), entries 11, 12, 18, 21.*
