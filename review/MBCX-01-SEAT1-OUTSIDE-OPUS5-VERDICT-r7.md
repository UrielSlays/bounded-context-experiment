MBCX-01 r7 — SEAT VERDICT
1. Top-level verdict

NO-GO — the inference contract is arithmetically incapable of returning its own primary success branch. PROMOTE_TO_COORDINATION_STAGE fires 0 times in 20,000 replicates in all nine of the contract's own operating-characteristic cells, including the most favourable one. Three further load-bearing defects (C2, C3, C6) each independently admit an answer-changing unstated choice.

2. Seat identity

Claude Opus 5, Moonwalker MCP harness (pwsh + Python 3.13 probes, read-only), report title "MBCX-01-r7-OPUS5-SEAT-VERDICT-ARITHMETIC-UNREACHABILITY". Longitudinal posture: I carry own-lane context from the OCR-modernization council rounds in this same thread; I have no prior MBCX-01 context — this is my first round on this bundle, so no r1–r6 recommendation below is inherited. Paid inference: NONE.

3. Pin verification — all five artifacts, EXECUTED

Repo is a git worktree. HEAD at read time was 52592a2a, not the pin; 6cf58b4a verified as an ancestor of HEAD, and all reads were taken from the pinned objects, not the working tree.

Artifact	blob	bytes	lines	SHA-384
MBCX-01-EXPERIMENT-DESIGN-r6.md	✅ 124e4be7	✅ 10,660	✅ 134	✅
MBCX-01-STATE-ACTION-CONTRACT-v2.json	✅ e1d8f598	✅ 8,481	✅ 142	✅
MBCX-01-PACKET-SCHEMAS-v1.json	✅ d31a9aae	✅ 6,356	✅ 95	✅
MBCX-01-MEASUREMENT-CONTRACT-v1.json	✅ 095f24be	✅ 4,630	✅ 85	✅
MBCX-01-INFERENCE-CONTRACT-v2.json	✅ 907d3f65	✅ 7,869	✅ 116	✅

Working copy of all five is byte-identical to the pin (git diff empty). ⚠ HEAD moved from 52592a2a → aa00f7ba during my session — the repo is being written concurrently. I did not read those commits.

4. Evidence separation
EXECUTED — pin/hash verification; independent re-derivation of every radius and reference vector; 20,000-replicate OC branch simulation over all nine cells under the contract's exact stopping law; minimum-n solve; variance-adaptive comparison; unit-total-gate arithmetic; event-type and 17²=289 enumeration check.
READ-ONLY — all five artifacts read end to end at the pin; C2/C3/C5/C6/C8 structural findings.
SEARCHED — one lane (sequential inference for bounded means). Opened at origin.
UNSEARCHED — six of the packet's seven §5 lanes (DID-NOT, budget). Consequence declared in §12.
5. Applicability ruling

Scope accepted as written. Exclusions honoured — no licensing, hostile-actor, FIPS, fleet, or coordination-stage finding below. No excluded surface is smuggled in: every finding below has a direct false-result path in the packet's own list (false model/inconclusive branch, non-total contract, invalid inference, cost discovered after authorization).

6. Claim scoreboard
Claim	Ruling	Basis
C1 North Star / decomposition	UNDERDETERMINED	Arms 1–2 coherent; arm 3 unreachable (F-1), so "three separate conclusions" is really two
C2 total state/action/writer	FALSE	F-4: writer's O_due guard cut is unspecified
C3 schemas / presentation parity	FALSE	F-3: objects[].fields is an unconstrained JSON object
C4 FD/FC/TN completeness	UNDERDETERMINED	No omitted public semantic mechanism proved; not executed
C5 cohort / unique paid target	UNDERDETERMINED	Selection rule sound on its face; F-5 breaks one sub-claim
C6 physical boundedness	FALSE	F-2 (total gates vacuous) + F-6 (linear-in-H passes)
C7 isolation / reconstruction	UNDERDETERMINED	No implementation exists to execute the seven witnesses
C8 serial handoff / replay	FALSE	F-5 + F-7
C9 engineering / carrier fairness	HOLDS (READ-ONLY)	Pareto output + separately labelled carrier with no engineering authority is correctly firewalled
C10 inference validity	FALSE	F-1
C11 OC / missingness / transport / cost	FALSE	F-8 (interim missingness ceiling) + F-9 (cost after authorization)
C12 smallest decisive instrument	FALSE	F-10: the three-look structure is a strict net loss
7. Findings
F-1 — P0. The primary success branch is arithmetically unreachable. EXECUTED.

MBCX-01-INFERENCE-CONTRACT-v2.json → method.delta_radius, decision_thresholds.

Delta support is [-1,0,1], so the Hoeffding radius carries range 2. At the terminal look:

look_alpha = 0.008333333333333333   (0.05 / 2 streams / 3 looks)   ✓ matches contract
n=384:  delta_radius = 0.168952639495     om_radius = 0.084476319748

All nine reference_vectors.method_radius_vectors entries reproduce from an independently written evaluator to max |diff| = 4.7e-13, inside the contract's own 1e-12 tolerance. The formula is right. The consequence is fatal:

PROMOTE requires   n= 96: delta_hat > 0.237905  AND om_hat >= 0.968953
                   n=192: delta_hat > 0.138935  AND om_hat >= 0.919468
                   n=384: delta_hat > 0.068953  AND om_hat >= 0.884476

The radius (0.169) is 1.69× the noninferiority margin (0.10). So "BC is not worse than OM by more than 10 points" can only be declared when BC beats OM by 6.9 points. That is a noninferiority test that requires superiority.

20,000 replicates per cell, contract's own cells, contract's own stopping law and precedence:

CELL                  dlt    om |  PROMOTE MDL_FAIL  CEILING  INCONCL | stop 96/192/384
OM70_EQUAL            0.00  0.70 |   0.0000   0.0000   0.7456   0.2545 | .068/.211/.721
OM80_EQUAL            0.00  0.80 |   0.0000   0.0000   0.0001   0.9999 | .000/.000/1.00
OM90_EQUAL            0.00  0.90 |   0.0000   0.0000   0.0000   1.0000 | .000/.000/1.00
DELTA_NEG25          -0.25  0.85 |   0.0000   0.0163   0.0000   0.9837 | .000/.000/1.00
DELTA_NEG12          -0.12  0.83 |   0.0000   0.0000   0.0000   1.0000 | .000/.000/1.00
DELTA_NEG10          -0.10  0.85 |   0.0000   0.0000   0.0000   1.0000 | .000/.000/1.00
DELTA_POS10           0.10  0.75 |   0.0000   0.0000   0.0643   0.9357 | .005/.012/.984
HIGH_DISCORD_EQUAL    0.00  0.50 |   0.0000   0.0000   1.0000   0.0000 | .995/.005/.000
LOW_DISCORD_EQUAL     0.00  0.90 |   0.0000   0.0000   0.0000   1.0000 | .000/.000/1.00

PROMOTE: 0.0000 everywhere. MODEL_INTERFACE_FAIL is also near-dead — 0.0163 only when the true delta is −0.25, i.e. 2.5× past the margin; at −0.12 and −0.10 it is 0.0000. Seven of nine cells return INCONCLUSIVE with probability ≥ 0.93. The only reachable positive conclusion is CEILING — the instrument can conclude "the model is bad" and can never conclude "the model is fine."

False-result mechanism: every paid dollar is spent on a branch that cannot fire; the owner authorizes a run whose modal outcome is INCONCLUSIVE_OR_UNDERFUNDED by construction, and a genuinely usable model is reported as inconclusive.

Smallest repair (one of): (a) replace the range-2 Hoeffding delta bound with a variance-adaptive bound — the contract already pins the machinery it demoted (see §12); (b) test the delta on the discordant subset only (McNemar structure: concordant pairs carry no information, and LOW_DISCORD_EQUAL has 2% discordance while the bound assumes worst-case 100%); or (c) raise n — solved exactly: n ≥ 1097 for the radius to fall below the margin at all, n ≥ 4385 for usable margin, i.e. 6,582–26,310 accepted calls against a budgeted 2,304.

⚠ The contract mandates the computation that catches this — operating_characteristics.replicates_per_cell_mode: 10000 and power_and_authorization.publish_before_paid_run includes "branch probability by OC cell and look" and "inconclusive probability." Either it was not run, or it was run and not read. That is the finding behind the finding.

F-2 — P1. Same-unit total gates are vacuous. EXECUTED (arithmetic).

MBCX-01-MEASUREMENT-CONTRACT-v1.json → unit_class_total_gates. Every total gate equals exactly the sum of its per-counter maxima:

bytes:      0 + 4096 + 4096 = 8192  = gate 8192
records:    9 + 32           = 41    = gate 41   (D: 0 + 32 = 32 = gate 32)
operations: 16 + 4           = 20    = gate 20
pages:      4                = 4     = gate 4
branches:   0                = 0     = gate 0

Since max(Σ) ≤ Σ(max) always, a total gate set at Σ(max) can never fail a run the per-counter gates pass. The r7 repair "same-unit total gates" is present and non-binding. Worse, it legalizes the split it exists to catch: a candidate whose true records range is 41 splits it 32/9 across INDEX_RECORDS_READ and SOURCE_RECORDS_READ and passes both gates and the total — buying 9 records of archive-linear growth. Smallest repair: set each unit total strictly below Σ(per-counter max) — records total 32, bytes total 4096.

F-3 — P1. objects[].fields is an unconstrained JSON object. READ-ONLY.

MBCX-01-PACKET-SCHEMAS-v1.json → DecisionPacketV2.properties.objects.items.properties.fields = {"type": "object"}. Every other object in the bundle carries additionalProperties: false. This one carries nothing: no additionalProperties, no maxProperties, no value-type constraint, no depth bound, no string maxLength.

C3 asserts "No packet admits free-text reasoning, transcript, scratch, arbitrary config, or unbounded arrays." fields admits all four, and it is precisely where BC and OM differ, so the leak channel is the semantic payload itself. SafeInteger also does not reach inside fields, so the r7 "safe JSON integers" repair stops at the packet skeleton.

Second-order: with objects maxItems 256 and fields unbounded, canonical JSON can exceed fixed_byte_envelope: 65536, at which point "append U+0020 to the fixed byte envelope" is undefined. A schema-valid DecisionPacketV2 can be unpaddable. No overflow code exists for this (FRONTIER_LIMIT covers action count, not byte count). Smallest repair: additionalProperties: false with an enumerated field-value grammar, maxProperties, string maxLength, and a serialized-length precondition that fails loudly before render.

F-4 — P1. The writer's complete_obligation guard has no specified evaluation cut. READ-ONLY. This is the "one legal trace with two answers."

STATE-ACTION-v2 → event_types.complete_obligation.guard requires OPEN and O_due. O_due is defined in state.derived_sets as OPEN AND due_at <= cut.valid_time AND not O_blocked — a function of a cut. The writer runs after A0 → B, at no named cut. query_clock.prior_cut_rule governs reads, not the writer's guard.

not O_blocked can flip in both directions between the A0 packet cut and commit (a prerequisite completing, or a link_dependency arriving). So the same B proposal validates or rejects depending on an unstated choice, and the two paths differ observably: commit_handoff_result versus reject_handoff_result with a frozen code — which is the scored outcome. Smallest repair: name the guard cut explicitly as TaskPacketV2.input_packet_hash's originating cut, and add a red witness where a prerequisite completes between packet render and commit.

F-5 — P1. A1_gold contradicts reopen_obligation. READ-ONLY.

paid_handoff_gold.A1_gold = "recompute after deterministic writer terminal; committed target cannot recur." But event_types.reopen_obligation sets a COMPLETED obligation back to OPEN with a new due_at, retaining prerequisites. If a frozen scenario's journal contains a reopen visible at the A1 cut, the committed target legally recurs in O_due and A1's gold is the same ACT ID again. Motif 2 is literally "obligation lifecycle." The rule is asserted as an invariant with no generator constraint enforcing it. Smallest repair: either forbid post-commit reopen of the target in Stage-2 eligibility, or delete the "cannot recur" clause and let A1 gold be recomputed without it.

F-6 — P1. Linear-in-H work passes the boundedness gate. EXECUTED (arithmetic over the pinned grid).

H = [128, 1024, 10000, 100000] — four points, stopping at 10⁵. SOURCE_RECORDS_READ allows an H-range of 9. A candidate with cost exactly H/12500 reads 0.01 records at H=128 and 8 at H=100000: range 8, passes — and it is strictly archive-linear. The gate tests magnitude at four points, not shape. C6 claims it "rejects archive/depth-linear work"; it rejects archive-linear work only above a coefficient threshold set by constants (9, 32, 4096, 16, 4) for which the contract offers no derivation — the packet's own Attack E asks whether the allowances are "justified rather than merely frozen," and they are merely frozen. Smallest repair: add H=10⁶ (a fifth point costs nothing — it is a generated journal) and gate on fitted slope across the grid, not on max−min.

F-7 — P2. Retry has no billed-call reconciliation. READ-ONLY.

record_call_response.key = (scenario_id, condition, node), guard "key has no accepted response." Design §8 permits one retry when "route policy classifies the failure pre-acceptance." If that classification is wrong — the provider accepted and billed, the client saw no body — the retry writes under a key the journal believes empty. Two paid samples, one journaled, undetectable from the journal side. transport_soak.measures includes accepted_no_body, so the design knows the mode exists; nothing reconciles provider-side billed calls against journal-side accepted responses. Smallest repair: require provider_request_id reconciliation against the provider's own usage record in the authorization report.

F-8 — P2. The interim missingness ceiling is unspecified. READ-ONLY.

missingness.hard_ceiling_count_at_n384: 7 and hard_ceiling_fraction: 0.02 (7/384 = 1.8%). terminal_rule names only the absolute count, with no look qualifier. At look 96, 7 missing pairs is 7.3% — four times the stated fraction — and still inside budget. Two stated ceilings disagree at interim looks and only one is operative. Since a CEILING decision at look 96 is binding, missingness can move a terminal branch at a look where the budget was never defined. Smallest repair: state the ceiling per look as floor(0.02 · n).

F-9 — P2. Cost is learned after authorization. EXECUTED (follows from F-1).

The preauthorization_manifest names "maximum and expected calls" at n=384 → 2,304. If F-1 is repaired by raising n, the true requirement is 6,582–26,310 calls — 2.9× to 11.4× the authorized ceiling, discovered only when the OC simulation is finally run. That is the packet's own load-bearing criterion "cost discovered after authorization," triggered by the artifact as pinned.

F-10 — P2. The three-look structure is a strict net loss. EXECUTED.
3-look Bonferroni @384: delta 0.168953 vs 1-look 0.151073  (11.8% wider)
                        om    0.084476 vs 0.075537  (11.8% wider)
PROMOTE needs delta_hat > 0.0690 (3-look) vs > 0.0511 (1-look)
             om_hat   >= 0.8845 (3-look) vs >= 0.8755 (1-look)

The interim looks widen the terminal interval by 11.8% and purchase early stopping in 2 of 9 cells — both of which stop into CEILING, the branch that needs no help. In the seven cells where early stopping would be valuable, stop@96 = 0.000. C12 ("every retained stage can change a primary result") is false for the interim looks: delete them and every primary result improves.

8. Attacks A–J
	Input	Method	Output	Interpretation	Limitation
A	9 OC cells × stopping law	20k-rep simulation	Only CEILING and (barely) MODEL_FAIL reachable; PROMOTE 0.0000	Decisions are not distinctly scoped — 4 of 6 branches are dead	Simulated i.i.d. pairs; real heterogeneity only widens INCONCLUSIVE
B	STATE-ACTION-v2	Read + enumeration	17 event types ✓, 17²=289 ✓; F-4 guard-cut hole; F-5 reopen contradiction	Contract is not total	Reducer not implemented; pair fixtures not executed
C	PACKET-SCHEMAS-v1	Schema read + envelope arithmetic	F-3 fields open; unpaddable-packet path; 2 of 5 discriminator features (served_byte_length, padding_length) are constant by construction under a fixed 65536 envelope	Strict-schema closure has a hole at the payload	No validator run against generated fixtures (none exist)
D	Cohort rules	Read	Selection/hash rule sound; F-5 breaks A1 uniqueness	Cohort mostly holds	Fixtures do not exist
E	MEASUREMENT-v1	Arithmetic over gates and grid	F-2 vacuous totals; F-6 linear-passes	Boundedness gate is weaker than claimed in both directions	No candidate to run
F	Isolation spec	Read	Config allowlist/denylist coherent; witnesses not runnable	Cannot rule	Exact missing surface: candidate implementation + governed dependency API
G	DAG + journal	Read	F-5, F-7	One scored conjunction not guaranteed	Not executed
H	INFERENCE-v2	Independent formula derivation + simulation	Radii reproduce to 4.7e-13; F-1; interim-look estimand switch (below)	Method is correctly implemented and wrongly chosen	OC enumeration over completions not run
I	Transport/cost	Read + F-1 arithmetic	F-7, F-9	Cost not bounded as authorized	Soak not runnable
J	14 red witnesses	Read	See below	String-presence is indeed insufficient	Only the inference witnesses executable

Attack H, additional — the estimand switches at interim looks. estimands.population = "the frozen motif-balanced Stage-2 manifest" (all 384), while heterogeneity = "conditional means may vary arbitrarily by scenario and motif." At look 96 the Hoeffding interval covers the mean of scenarios 1–96, not of the manifest. Those are different fixed numbers under arbitrary heterogeneity, and no finite-population correction or permutation-exchangeability argument is offered for the SHA-256 prefix. A binding decision at look 96 is made about a quantity the interval does not cover. (At n=384 the manifest is fully observed and the bound is correct-and-conservative — the defect is confined to the interim looks, which F-10 says to delete anyway.)

Attack J — the witnesses I could execute. INFERENCE_IMPLEMENTATION_MISMATCH: closed correctly, EXECUTED — my independent evaluator matched all nine vectors to 4.7e-13. PERIODIC_INDEX_AMBIGUITY: closed, READ-ONLY (zero_based_indices_0_10_20 is unambiguous). Alternative bypass against both: they verify the formula is implemented faithfully; neither can fail when the formula is the wrong estimator — which is F-1. The remaining twelve are READ-ONLY; COUNTER_SPLIT is present-but-defeated by F-2, and HD_INTERACTION is defeated by F-6.

9. What would you build?

Keep the instrument; replace one estimator and delete one stage.

Variance-adaptive delta bound. The contract already pins gostevehoward/confseq @ 5ffe733c and then demotes it to "historical comparator only." That demotion is the defect. SEARCHED: Waudby-Smith & Ramdas, Estimating means of bounded random variables by betting, arXiv 2010.09686 / JRSS-B 86(1) — opened at origin; the deciding sentence is that empirical-Bernstein methods "outperform Hoeffding's method for low-variance distributions" and the betting bounds are "adaptive to the unknown variance… empirically vastly outperform existing approaches based on Hoeffding." Under LOW_DISCORD_EQUAL (2% discordance) my comparison gives ~0.052 versus Hoeffding's 0.169 — PROMOTE becomes reachable at n=384 without one extra paid call.
Score the delta on discordant pairs only. Concordant pairs contribute exactly 0 to delta and consume the full range-2 penalty. The paired structure is already in the OC parameterization (p01, p10); use it.
Single terminal look at n=384. Recovers 11.8% of interval width, removes the interim-estimand switch (Attack H), removes the interim missingness-ceiling ambiguity (F-8), and costs an early-stop probability that is 0.000 in seven of nine cells.
Close fields with an enumerated grammar, and add a serialized-length precondition before padding.
Name the writer's guard cut.
Set unit totals strictly below Σ(per-counter max), and add H=10⁶ with a slope-based gate.

The paid budget stays 2,304 calls. Nothing here is a new subsystem.

10. Would you design it differently?

Two structural changes.

Run the OC simulation as Gate 0, not Gate 5. It is currently the last gate before authorization, and it is the artifact that falsifies the design. Every hour spent on schemas, counters, and journaling in rounds r1–r6 was spent on an instrument whose primary branch had probability zero — and a 40-line simulation, already mandated by the contract, would have shown that before r2. The cheapest gate in the bundle is running last.

Do not couple the model arm to the mechanism arm through one authorization. Arms 1 and 2 (continuity, engineering Pareto) are deterministic, no-paid, and — as far as I can tell — sound. Arm 3 is stochastic, paid, and broken. Bundling them means a repair to arm 3 re-opens the whole preregistration. Split the manifest: ship arms 1–2 now under the existing gates; give arm 3 its own preregistration once the estimator is fixed and the OC table shows a reachable PROMOTE.

11. Omission and bypass attack
Strong comparator omitted: NONE — §2's control list (full/rolling context, ordinary files, BM25, sparse+dense RAG, namespaces/blackboard, oracle-minimal/all-relevant, unbounded raw-replay FD) is genuinely strong, and §3's "public semantic object unavailable to all three" test correctly refuses branding as a mechanism.
One legal trace with two answers: F-4 (writer guard cut).
One false continuity pass: F-6 — strictly linear-in-H work with coefficient < 9/10⁵ passes.
One false kill: F-3 — a legal packet that exceeds the 65536 envelope has no defined outcome and would surface as DESIGN_OR_IMPLEMENTATION_FAIL against a candidate that did nothing wrong.
One false mechanism preference: F-2 — a counter-splitting candidate wins the Pareto set on registered work it actually performs.
One false model-usability: F-1 — a model with true delta 0 and OM 0.90 is reported INCONCLUSIVE with probability 1.0000.
One false ceiling story: HIGH_DISCORD_EQUAL returns CEILING at look 96 with probability 0.995 — but its true OM rate is 0.50, so CEILING is correct there; the false version is OM70_EQUAL, where CEILING fires 0.746 on a model whose true OM is 0.70, i.e. only 0.10 below floor, decided on 96 pairs at 25% of the manifest under the Attack-H estimand switch.
Bypass not caught by the fourteen: the fourteen witnesses verify presence and faithfulness; not one of them can fail when a faithfully implemented formula is the wrong estimator. F-1 passes all fourteen.
One no-paid test without which I refuse implementation: the OC branch-probability table — nine cells × three looks × 10,000 replicates, published with PROMOTE probability per cell, before Gate 1.
One mechanism to borrow: the betting/empirical-Bernstein confidence sequence, from the repository the contract already pins.
One artifact or step to delete: the interim looks at 96 and 192 (F-10). Everything else is load-bearing.
Boundary to the coordination experiment: MBCX-01 ends at one logical conductor, one scope, one A0→B→writer→A1 episode, with scope_rule immutable and handoffs same-scope. The coordination experiment begins at the first multi-scope or concurrent-writer trace. That boundary is cleanly drawn in the pinned bytes and I found no leak across it.
12. Sweep log
Query	Opened at origin	Deciding content	Effect	Label
Waudby-Smith Ramdas estimating means bounded random variables betting empirical Bernstein tighter than Hoeffding	arXiv 2010.09686 abstract + JRSS-B 86(1) article page	"adaptive to the unknown variance, and empirically vastly outperform existing approaches based on Hoeffding or empirical Bernstein inequalities"; empirical-Bernstein "outperform[s] Hoeffding's method for low-variance distributions"	Converts F-1's repair from a hunch into a named, published, already-pinned method	SEARCHED

Stop reason: the verdict is NO-GO on arithmetic derived from the pinned bytes alone; only the repair rested on prior art, and one controlling primary settles it.

Declared incompleteness: six of the packet's seven §5 lanes are UNSEARCHED (DID-NOT) — selection/eligibility effects, physical-cost counters and factorial interaction tests, JCS/tokenizer render confounds, durable response journaling and crash ambiguity, memory-system baselines, and current provider route/cache behaviour. Per the standing rule, no prior-art-bearing finding of mine can be a deciding GO, and F-6, F-7 and the C4 ruling should be treated as unswept. This round is therefore incomplete on §5 and another seat must carry those lanes.

13. Residual risks and non-claims
R-1 — action_universe.available counts every obligation with any visible lifecycle event, so the action set grows with obligation history; at high H, FRONTIER_LIMIT fires before dispatch. Consequence: the paid model arm only ever sees small worlds, so arm 1 (bounded continuity at H=10⁵) and arm 3 (model usability) are measured on disjoint regimes. Not a defect; a scope limit that should be stated.
R-2 — HANDOFF-COMMIT: idempotency includes proposal_event_id, so a re-proposal of the same action yields a different key. It is guarded by complete_obligation's OPEN transition rather than by idempotency. Correct today, fragile under F-5.
R-3 — Attack H's estimand switch is confined to interim looks and disappears if F-10 is taken.
R-4 — I did not execute Attacks F or G; C7 is UNDERDETERMINED for want of an implementation, and I name the exact missing surface: candidate implementation + governed dependency API.
Non-claims: I make no claim about FD/FC/TN completeness beyond "no omission proved"; none about reconstruction isolation; none about provider behaviour; none about whether the repaired instrument would return PROMOTE on the real model.
14. Seat capability, lateral seal, side effects, cleanup
Lateral seal: intact. I did not open any r7 verdict, output log, completion marker, browser output, or the CLAUDE-OPUS5-SEAT-VERDICT-r1.md and r2–r6 synthesis files present in the directory. I noticed HEAD advance twice during the session (52592a2a → aa00f7ba) and deliberately did not inspect the new commits.
Paid inference: NONE. Zero provider calls.
Side effects: none to the repository. All reads were git cat-file extractions of pinned blobs into $env:TEMP\mbcx-pin; three Python probes written there; directory deleted, verified absent. Repo working tree untouched (the 16 dirty entries pre-date and post-date me and are not mine).
Capability: full shell, Python 3.13, and web access available; the limit on this round was attack breadth, not tooling, and I have declared exactly where.

The one-line version, <user>: the pins are perfect, the formula is implemented perfectly, and the experiment cannot answer its own question — a range-2 Hoeffding interval of 0.169 against a noninferiority margin of 0.10 means BC has to beat OM by 7 points to be called "not worse by 10." The fix is in the repo already; r7 demoted it to a footnote.
