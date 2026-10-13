MBCX-01 r9 — SEAT VERDICT
1. Top-level verdict

GO-WITH-FIXES — (P1: the certified transport budget and the missingness ceiling are mutually inconsistent at n=768; at exactly the reliability the 98,868-call soak is designed to certify, TRANSPORT_INCONCLUSIVE fires with probability 0.986. Free repair, executed candidate below. Must land before the soak is authorized.)

Every one of my five r8 findings is closed, and I verified each by execution rather than by reading the claim. The instrument now answers its question. One new defect — found only by multiplying two contracts together — would waste the soak.

2. Seat identity

Claude Opus 5, Moonwalker MCP harness (pwsh + CPython 3.13, read-only). Title: "MBCX-01-r9-OPUS5-SEAT-VERDICT-CROSS-CONTRACT-MISSINGNESS-CEILING".

Longitudinal posture, disclosed: I hold my own r7 and r8 seat context and use it — all five r8 findings are re-tested by name below, and my r8 independent implementation of Proposition 3.1 is reused. I hold no other-seat context from any round. Items in packet §2 that are not mine (the friendly-state-reference, BC/OM separate-source, and B-scoring blockers) are marked unverified-by-me. Paid inference: NONE.

3. Pin/byte verification — EXECUTED

Pin f8fa7564 is a commit and an ancestor of HEAD (which advanced 1b450e81 → a227948d mid-session; I read only pinned objects).

All ten artifacts exact — blob OID, LF bytes, lines, SHA-384. Zero mismatches.

MBCX-01-EXPERIMENT-DESIGN-r8.md        19867/180  OK    mbcx01_r9_oracle.py            16681/368   OK
MBCX-01-STATE-ACTION-CONTRACT-v4.json  16328/173  OK    mbcx01_r9_reference.py         66936/1394  OK
MBCX-01-PACKET-SCHEMAS-v3.json         14674/161  OK    verify-r9-normative-bundle.py  22271/507   OK
MBCX-01-MEASUREMENT-CONTRACT-v3.json    9551/115  OK    verify-r9-schema-ajv.mjs        3659/78    OK
MBCX-01-INFERENCE-CONTRACT-v4.json     11390/147  OK    MBCX-01-R9-NO-PAID-VERIFICATION.json 15537/429 OK

My r8 F-A is closed. The table is now headed "LF bytes," the evidence artifact hashes correctly from the Git object, and my extraction was blob-only (git cat-file blob into a temp dir) — no checkout substitution possible.

4. Evidence separation
EXECUTED — all ten pins; verify-r9-normative-bundle.py on blob-reconstructed bundle (6/6 PASS, 20.5 s); my own independent reimplementation of Prop 3.1 from contract text alone against both new reference vectors; the reliability arithmetic re-derived from scratch and bracketed at the unit; binomial tail analysis of the missingness ceiling across eight budgets; independent 400-rep confirmation of all four practical power targets at n=768; exhaustive 4⁵ = 1,024-completion enumeration testing corner attainment; unit-total arithmetic over 22 counters; 100-cell Cartesian check.
READ-ONLY — inference v4, measurement v3, state/action v4 structure.
SEARCHED (inherited, labelled) — arXiv 2512.21300, opened at origin by me in r8; the estimand premise carries forward unchanged.
UNSEARCHED — six of seven §7 lanes (DID-NOT, budget); Prop 3.1's body (COULD-NOT — see R-2).
5. Applicability

Scope accepted. No excluded surface used. My one P1 maps to two named categories: avoidable practical indecision and material cost learned only after authorization.

6. Claim scoreboard C1–C12
	Ruling	Basis
C1 decomposition	HOLDS	All four branches reachable; simpler controls retained
C2 state totality	HOLDS	17 types → 289 pairs verified; closed event_envelope/guard_catalog/effect_catalog
C3 executable independence	HOLDS	state: PASS with two engines + six killed mutants; my own reimplementation independently matched the inference core to 2.2e-16
C4 packet validity	HOLDS	Real Ajv Draft 2020-12 closure; packets: PASS
C5 cohort provenance	UNDERDETERMINED	cohort: PASS; I did not build adversarial cohort worlds
C6 physical boundedness	HOLDS	4×5×5 = 100 cells confirmed; 22 counters; every unit total strict; shape_gates added; 7 red candidates carry expected errors not labels
C7 reconstruction/isolation	UNDERDETERMINED	Correctly conditioned on a future harness; nothing to execute
C8 serial DAG/recovery	UNDERDETERMINED	call_ledger first-class; crash windows not walked by me
C9 engineering fairness	HOLDS (READ-ONLY)	Unchanged, still firewalled
C10 inference	HOLDS	Both reference vectors reproduce to ≤2.2e-16; κ freeze + sensitivity + KAPPA_OC_TUNED witness
C11 power/missingness/reliability/cost	FALSE	F-1 — see below
C12 smallest decisive instrument	HOLDS	Progress-only reporting at 96/192/384 kills the prefix problem; expected == maximum follows honestly
7. Findings
✅ First — every r8 finding of mine is closed, verified by execution
r8 finding	r9 closure	How I verified
F-A CRLF pin on the evidence artifact	Table now "LF bytes"	All 10 pins exact from blobs
F-B OC cells overstated fail-branch power by only testing OM=0.95	16 cells spanning negative-delta × OM ∈ {0.80, 0.85, 0.95}; DELTA_NEG25_OM80/_OM85 restored; required_publication includes the full curve; red witness OM95_ONLY_POWER_HEADLINE	Cell list read; power targets independently re-simulated
F-C κ = 0.25 unjustified and decisive	kappa_source_rule: SOURCE_DEFAULT_NOT_OC_TUNED; kappa_sensitivity: [0.10, 0.15, 0.25, 0.50, UNIFORM]; uniform_limit derived analytically (threshold → 2/α); red witness KAPPA_OC_TUNED	Read; sensitivity set matches the values I published in r8
F-E(i) delta_all_zero wrong by 2.35×	Now an exact interval, [-0.028724411075760736, +0.028724411075760736]	Independent reimplementation: max diff 2.220e-16
F-E(ii) "fixed interleaving" under-specified	All 84 positions now enumerated explicitly (68 zero-equal, 8 bc0/om1, 8 bc1/om0); red witness LOW_DISCORD_POSITIONS_MUTATED	Independent reimplementation: delta max diff 1.110e-16, om max diff exactly 0.0
F-F branches had no unit total	Now present at 0	Arithmetic over all 22 counters

Two of the eight new red witnesses are named after defects I reported. That is the repair loop working.

And the reliability arithmetic is exact to the unit — not approximately right, exactly right:

cell alpha = 0.05/48 = 0.0010416667 ; cell budget = 0.02/48 = 0.0004166667
ln(alpha)/ln(1-budget) = 16477.2062  ->  ceil = 16478      (contract says 16478)
CP upper at 0/16477 = 0.000416671879  >  budget   (would FAIL)
CP upper at 0/16478 = 0.000416646598  <= budget   (passes)
6 x 16478 = 98868                                  (contract says 98868)
union over 48 cells = 48 x 0.02/48 = 0.0200 == pair_missing_budget

And the n=768 sizing claim is real. My own RNG, 400 reps, all four practical targets:

OM90_EQUAL          PROMOTE   1.0000   (packet: 99.76%)   PASS
LOW_DISCORD_EQUAL   PROMOTE   1.0000   (packet: 99.84%)   PASS
DELTA_NEG20_OM90    FAIL      0.9975   (packet: 99.72%)   PASS
CEILING_OM70_EQUAL  CEILING   0.9375   (packet: 94.30%)   PASS
F-1 — P1. The certified transport budget and the missingness ceiling are mutually inconsistent at n=768. EXECUTED.

Location: MBCX-01-INFERENCE-CONTRACT-v4.json → transport_readiness.pair_missing_budget: 0.02 versus missingness.maximum_enumerated_missing_pairs: 7 / eight_or_more: "TRANSPORT_INCONCLUSIVE", with operating_characteristics.n: 768.

The 98,868-call soak certifies P(pair missing) ≤ 0.02. The inference contract declares TRANSPORT_INCONCLUSIVE at 8 missing pairs — that is 7/768 = 0.911%, less than half the certified budget. Binomial tail at n = 768:

per-pair   expected missing   P(>=8 missing)
 0.0200         15.36            0.986100     <- exactly the CERTIFIED budget
 0.0150         11.52            0.889136
 0.0100          7.68            0.502047
 0.0050          3.84            0.041758
 0.0030          2.30            0.002568
=> budget keeping P(TRANSPORT_INCONCLUSIVE) <= 5% is 0.00519, not 0.0200

A run that exactly meets the reliability guarantee the soak is built to buy is 98.6% likely to be declared TRANSPORT_INCONCLUSIVE. The soak certifies the wrong number.

Cause — a scaling miss, not a modelling error. At r8's n = 384, 7/384 = 1.82% ≈ the 2% budget and the two contracts agreed. n doubled to 768; the absolute ceiling of 7 did not move, because it is pinned to computational tractability: 4⁷ = 16,384 enumerable completions, while 2% of 768 needs m = 15 → 4¹⁵ = 1,073,741,824.

False-result / avoidable-indecision path: the owner authorizes 98,868 soak calls plus 4,608 scientific calls; transport performs exactly at contract; the run returns TRANSPORT_INCONCLUSIVE and the entire scientific sample is discarded. Both categories the packet names as load-bearing, and it is invisible in either contract read alone.

Smallest repair — and I executed the candidate. Replace 4^m exhaustive enumeration with uniform-corner completions. Over all 1,024 completions at m = 5 on a realistic OM90 dataset:

delta_lower MIN -0.049239330  at ((0,1),(0,1),(0,1),(0,1),(0,1))   uniform corner: True
delta_lower MAX -0.036149010  at ((1,0),(1,0),(1,0),(1,0),(1,0))   uniform corner: True

Both extremes sit at uniform corners. If that holds generally, 4 completions suffice instead of 4^m, the m ≤ 7 ceiling disappears entirely, and 15+ missing pairs become tolerable at constant cost. ⚠ Honest limit: I demonstrated corner attainment on one instance at m = 5; I did not prove monotonicity of the CS endpoint in the completion. Named proof obligation: show the endpoint is monotone in ΣX given the induced U_t, or bound the U_t variation.

Fallback repair if that proof fails: tighten pair_missing_budget to 0.005. New soak size: budget/cell = 0.005/48 → n ≥ ln(0.00104167)/ln(1 − 1.0417e−4) ≈ 65,919 per position ≈ 395,514 total calls, a 4× cost increase. That number should be on the authorization sheet either way.

F-2 — P3. The t₀ premise remains unstated. READ-ONLY (inherited from my r8 F-D).

The source's coverage statement is indexed from an initial peeking time t₀; MBCX-01-INFERENCE-CONTRACT-v4.json names no t₀. Downgraded from r8's P2 to P3 because r9 collapsed to a single terminal look at n = 768, so the premise binds only if t₀ > 768, which is implausible. Repair: one clause in method.source.

F-3 — P3. The records unit total is strict by exactly 1. READ-ONLY.

records: sum of per-counter maxima = 41, gate = 40. Technically strict (my r8 F-2 lineage) and it does catch any 41-summing split, but a one-unit margin on a two-counter class is the least robust gate in the table; every other class carries 20–35% headroom. Repair: 32, matching r8's value.

8. Attacks A–J
	Input	Method	Output	Interpretation	Limitation
A	10 pins	Blob-only extraction + SHA-384	0 mismatches; verifier 6/6 PASS in 20.5 s on the reconstructed bundle	Pin discipline now uniform; stale-checkout substitution impossible	—
B	state v4	Structural read + verifier	17 types → 289 pairs; closed envelope/guard/effect catalogs; 6 mutants killed	r8 blocker closed	I built no fresh traces; C2 rests partly on their witnesses
C	schemas v3	Verifier's authenticated Ajv closure	packets: PASS	Real runtime validation, not declaration	I did not run Ajv separately
D	cohort	Verifier only	cohort: PASS; 960 → 768, 128/motif, supplied booleans discarded	Not independently attacked	Not executed — C5 UNDERDETERMINED
E	measurement v3	Arithmetic over 22 counters + 100 cells	Full 4×5×5 Cartesian confirmed; all totals strict; shape_gates present; 7 candidates with expected errors	My r7 F-6 and r8 F-F both closed	No candidate exists to build a false-pass against
F	inference v4	Independent reimplementation from contract text	2.220e-16 and 1.110e-16 and 0.0 against the three published endpoints	Reference is not a mirror; vectors are correct	Prop 3.1 body unread (R-2)
G	power targets	Own RNG, 400 reps, n=768	1.0000 / 1.0000 / 0.9975 / 0.9375 — all four PASS	n=768 genuinely answers the practical alternatives	400 reps, not 10,000
H	missingness + reliability	Re-derived CP from scratch; binomial tails; 1,024-completion enumeration	16,478 exact to the unit; F-1; corner attainment	Reliability math right, cross-contract coupling wrong	Corner result is one instance, not a proof
I	branches/cost	Read + G	4,608 = 6×768 ✓; 1,536 = 2×768 ✓; DESIGN now precedes TRANSPORT in precedence	Costs recompute exactly	—
J	—	—	See §13	—	—
9. Orthogonal-method answers
Prop 3.1 coverage → HELPFUL WITH A NAMED FIX. Estimand matches the source's μ_t = t⁻¹Σ E[X_j|F_{j−1}] (SEARCHED at origin in r8). Fix: state t₀ (F-2).
100-cell sufficiency → HELPFUL. With claim_scope narrowed to the frozen finite ranges, all totals strict, shape_gates added, and LOW_SLOPE_ARCHIVE_LINEAR_10X now emitting real counter rows and expected to fail with H_SHAPE_LIMIT, I could not construct an evader inside the registered cells. This closes my r7 F-6 completely.
Two engines independent enough → HELPFUL. Strongest evidence is not theirs but mine: I wrote the inference core from the contract text with no sight of their code and matched to 2.2e-16, and the verifier kills six mutants. No stronger oracle is needed — I decline to name one, because I cannot name a reachable shared-error path it would close.
Is n=768 smallest defensible → HELPFUL WITH A NAMED FIX. Confirmed: 384 misses (~56/67/50/39%), 768 clears all four targets. But F-1 means 768 is currently not reachable — at the certified transport budget the run dies before the intervals are computed. Fix is F-1's, not a sizing change.
48-cell simultaneous gate → HELPFUL WITH A NAMED FIX. The gate measures a real need and its arithmetic is exact. But it certifies 0.02 while the inference contract enforces 0.00911. The less expensive dependence-safe contract is not a different gate — it is removing the ceiling via corner completions, after which 0.02 is genuinely the right target and 98,868 calls buy exactly what they claim.
10. What would you build?

Three repairs, all free, all before authorization:

Replace 4^m enumeration with uniform-corner completions and delete maximum_enumerated_missing_pairs. Discharge the monotonicity proof obligation, or fall back to pair_missing_budget = 0.005 and publish the resulting ~395,514-call soak on the authorization sheet (F-1).
Add a cross-contract consistency witness — a red witness asserting pair_missing_budget × n < maximum_enumerated_missing_pairs. Every defect I have found in r7, r8 and r9 that survived the verifier lived between two contracts, not inside one. This is the class the verifier structurally cannot see.
Name t₀; set the records total to 32 (F-2, F-3).
11. Would you design it differently?

No. I withdraw my r8 recommendation to publish OC as surfaces rather than cells — r9's negative-delta × OM curve plus OM95_ONLY_POWER_HEADLINE achieves the same guarantee more cheaply, and the four registered practical targets with an explicit indifference region is a better instrument than a heat map. (Inherited-and-withdrawn, labelled.)

The one thing I would add is structural, not statistical: the verifier validates each contract against its own reference; nothing validates the contracts against each other. F-1 is the third finding in three rounds to live in that gap. That is where the next round's effort belongs.

12. Plain-language answer

Does the experiment now have a fair chance to answer its question? Yes — with the F-1 fix. I confirmed independently that at n = 768 all four practical alternatives resolve above 90%: a clearly usable oracle with no BC loss promotes ~100% of the time, a BC that is genuinely 20 points worse is caught ~99.8% of the time, and an oracle genuinely below the floor hits the ceiling branch ~94%. At n = 384 those same cases were coin flips. The instrument went from "returns INCONCLUSIVE on questions you actually care about" to "returns an answer."

What do 4,608 scientific calls buy? They buy the decision itself — six calls per pair over 768 pairs, one terminal interval, no early stopping. Against 2,304 at n = 384, the extra 2,304 calls convert roughly 40–50% branch probability into 94–100% on the four practical alternatives. That is the entire difference between an experiment that concludes and one that shrugs.

What would 98,868 route-soak calls buy? Simultaneous evidence — across 8 failure modes × 6 call positions, Bonferroni-allocated at 0.05/48 per cell — that transport will not silently erase the 768-pair sample. They buy zero scientific power. And as currently specified they buy the wrong guarantee: they certify 2% pair-missing, while the inference contract kills the run at 0.91%. Fix F-1 first, or those calls are spent certifying a threshold the experiment cannot use.

What uncertainty remains unavoidable? Exact-threshold truth. If BC is worse by precisely 0.10, or the oracle sits precisely at 0.80, no finite experiment can return a strict branch — and r9 is right to name that an explicit indifference region rather than promise a decision. Beyond that: this is one frozen model, one cold episode, one scope. It cannot tell you about a second model, a second writer, or the coordination stage, and it correctly does not claim to.

13. Omission and bypass, sweep, residuals, cleanup

Omission/bypass:

Strong omitted comparator: NONE.
Legal two-answer trace: NONE after execution — my r8 "fixed interleaving" ambiguity is closed by explicit position enumeration.
False continuity pass / false kill: none found — shape gates plus strict totals close my r7 low-slope path.
False mechanism preference: none found.
False model-usability / false ceiling story: none found — my r8 F-B is closed by the OM curve and its red witness.
Bypass not caught by the verifier: F-1. The verifier checks each contract against its reference. It cannot fail when two contracts are individually correct and jointly incoherent.
No-paid test without which I refuse implementation: a binomial-tail check that P(missing ≥ ceiling+1 | n, pair_missing_budget) ≤ 0.05. Costs microseconds.
Mechanism to borrow: uniform-corner extremal completions in place of exhaustive 4^m.
Artifact/stage to delete: NONE — ALL LOAD-BEARING.
Boundary to the coordination experiment: MBCX-01 ends at one logical conductor, one immutable scope, one cold A0→B→writer→A1 episode against a single immutable originating cut. The next experiment begins at the first trace with a second scope or a second concurrent writer. Drawn in the pinned bytes; no leak found.

Sweep log. One lane, inherited-SEARCHED: arXiv 2512.21300 (Chugg & Ramdas), opened at origin by me in r8 — abstract and §1 confirm the estimand μ_t = t⁻¹Σ_{j≤t}E[X_j|X_1,…,X_{j−1}], X_t ∈ [0,1], time-uniform coverage. Carried forward unchanged; the contract's estimand block still matches. Stop reason: applicability was settled; no r9 change touches it. Declared incompleteness: lanes 2–7 (§7) are UNSEARCHED — DID-NOT; indifference-zone sizing, benchmark leakage, JCS/2020-12 runtimes, workflow idempotency, and current provider price/receipt behaviour all need another seat. No prior-art-bearing finding of mine is a deciding vote; my verdict rests on executed arithmetic over pinned bytes.

Residual risks: R-1 Attacks D and the C8 crash windows not executed — C5, C7, C8 stand UNDERDETERMINED. R-2 Prop 3.1's constants remain verified-for-internal-consistency, not verified-against-source-body. R-3 My corner-attainment result is one instance at m = 5, not a proof. R-4 The magnitudes of the 22 frozen counter allowances remain unchallenged by me.

Non-claims: no claim about FD/FC/TN; none about reconstruction isolation; none about provider behaviour; and no claim that any of this is model evidence — experiment_evidence=false, paid_calls=0, correctly stated by the bundle and by me.

Capability, seal, side effects, cleanup: lateral seal intact — no other-seat r9 output, log, stdout, or marker opened; I consulted only my own r7/r8 verdicts and only to re-test my own named findings, all labelled. HEAD advanced twice during the session; I inspected no new commits. Paid inference: NONE. No repository writes; the 26 dirty entries are not mine. All work in %TEMP%\mbcx9 on blob extractions; directory fully removed and verified absent — unlike r8, no locked shell remains.

Short version, <user>: r9 closed all five things I flagged in r8, and I checked every one the hard way — re-derived the reliability figure from scratch (16,478 is exact to the unit; 16,477 genuinely fails), re-implemented the estimator from the contract text and matched both new reference vectors to sixteen decimal places, and re-simulated the four power targets with my own RNG. n=768 really does buy the decision; 384 really was a coin flip. One new thing, and it only shows up if you multiply two contracts together: your soak certifies 2% pair-missing, but the inference contract kills the run at 8 missing pairs out of 768, which is 0.91%. At exactly the reliability you're paying 98,868 calls to certify, you get TRANSPORT_INCONCLUSIVE 98.6% of the time. The fix is free — the branch extremes sit at uniform corners, so you need 4 completions, not 4^m, and the ceiling can go away entirely. Land that before you authorize the soak and I'd sign a clean GO.
