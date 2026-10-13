Used Moonwalker integration · 9 notes

Used Moonwalker integration · 9 notes

Numerics stack is absent on the host. Rather than install packages on your machine (that's a write I'm not authorized to make), I'll run the heavy statistics in my own sandbox and keep the host read-only.

Ran 10 commands, searched the web, used Moonwalker integration · 21 notes

Ran 10 commands, searched the web, used Moonwalker integration · 21 notes

Connector's still down, so the verdict comes from what I banked before it dropped plus sandbox work. Here it is, in-thread.

MBCX-01 EXPERIMENT COUNCIL VERDICT — Seat: Claude Opus 4.6
1. Top-level verdict

GO-WITH-FIXES(comparator-parity + render-control + budget-feasibility)

Three fixes are blocking for the implementation plan, not advisory. Implemented exactly as pinned, r2 would return a biased and uninterpretable answer on its own primary contrast. All three are cheap, pre-inference, and do not require redesigning the instrument. No paid inference is at risk yet, which is why this is GO-WITH-FIXES and not NO-GO.

2. Pin and byte verification
Item	Declared	Verified
Commit	b5874994f89d73efde6da90a445dd5f807808375	matches, type commit
Blob	1e7161e455d6f82707018db454e86985ae85e07f	matches b587499:MBCX-01-EXPERIMENT-DESIGN-r2.md
Bytes	34,108	34,108
Lines	596	596 LF
SHA-384	09EF...FA7A	09EF07882AD086F0CA0DD079906894C574F6B81BBA9B7D7F7BD3D8DBBC9A0C2B7FCB0E454698177C3CEF1C53981DFA7A exact
SHA-256 (mine)	n/a	F300EFC4C17A097D1AAE420CD4167295203C7AD4FD2747C6DFC33F7AF8022DD3

Working copy differed: NO. The tree file is byte-identical to the pin (same SHA-384). HEAD is 7ba9a88, two commits ahead of the pin, but HEAD:MBCX-01-EXPERIMENT-DESIGN-r2.md resolves to the same blob, so no stale-byte trap. I adjudicated all 34,108 bytes / 596 lines.

Sealed independence honoured. I did not open, grep, hash, or use any VERDICT, SYNTHESIS, EXEC-r2, or RESTART-MANIFEST file. Their names appeared unavoidably in git ls-tree and git status output; nothing was read. No other seat's conversation or output was consulted.

3. Evidence read and probes run

READ-ONLY (pinned bytes): MBCX-01-EXPERIMENT-DESIGN-r2.md (full, 596 lines) · LOCAL-SOURCE-MANIFEST-r1.md (full) · MBCX-01-EXPERIMENT-DESIGN-r1.md (decision-rule section only, for Attack E) · council-seat-role-prime-card.md (full).

EXECUTED: Llama-3 128k byte-level BPE built from the host's local tokenizer.json (roundtrip-validated on 3 probes) and used to token-count real F/TF/TN max-load packets · algebraic feasibility proof of §8.1 · exhaustive scorer-quantum search over all reachable (TP,FP) states · 40,000-rep operating-characteristic simulations across 6 distribution families × 8 candidate n · analytic n-requirement per gate · Kieser-Wassmer inflation-factor verification incl. s=0 · BCa timing and disagreement probe · pilot-size total-cost optimisation · cost model at n = 48/96/192/384 plus the n the rule actually demands.

SEARCHED (opened at origin with web_fetch, full text): PM-Bench (arXiv 2607.12385v1) · "Presentation, Not Mechanism: A Render Confound in Deprecation-Aware Memory Evaluation" (arXiv 2607.16019v1).

SEARCHED-PARTIAL (retrieval layer returned paper body text; my own fetch failed or was not performed): StateFuse (arXiv 2607.05844, PDF fetch returned empty) · MEME (2605.12477) · LatticeMind (2608.08236) · Selective QA over Conflicting Multi-Source Personal Memory (2605.30087) · Whitehead et al. 2016 (SMMR) · OpenRouter provider-routing docs. Flagged honestly rather than claimed as opened.

RECALLED: τ²-bench, LongMemEval (named in r2 §19 / manifest; not opened this session).

UNSEARCHED — NOT-LOAD-BEARING: AgenticSTS, LongHorizon-Harness, CAME/STITCH, MAGE/MemoryArena, AgeMem. I could not verify these exist. Mem2ActBench is real (Shen et al. 2026, arXiv 2601.19935, seen in PM-Bench's reference list). See P1-9.

Tool side effects: one transient probe script and one extracted blob under %TEMP%\mbcx_probe\. Nothing written to the repo, the vault, or any seat file. Nothing installed on the host. Heavy numerics ran in my own sandbox specifically to avoid installing packages on your machine.

4. Applicability ruling: doctrine I excluded

Excluded as NOT APPLICABLE — NON-LOAD-BEARING, no path shown to a wrong experimental answer:

Licensing/clean-room posture of PM-Bench, StateFuse, ESR-Bench code (tempting: §19 says "borrow mechanisms"; irrelevant to validity).
FIPS/CNSA, seal chains, hash-chained audit for run artifacts (tempting: §17 lists run artifacts; the experiment is disposable).
Prompt-injection hardening of natural_language_text (tempting: §6.1 admits free text into both stores; both arms receive byte-identical bytes, so it cannot bias the contrast).
Process registry / stale-PID / daemon lifecycle around the §9 reconstruction child (tempting: §10 discusses child waits; scoped to one child, run-owned).
PR ceremony, provider-family generality, cross-model variance.
SDVOSB / GovCon citability of the result.

Kept in scope per §3: response caching, prompt caching, endpoint routing, transforms, retries, hidden message state, because each can change an arm's input or draw.

5. Claim scoreboard
Claim	Verdict	One-sentence reason
C1 primary treatment honestly identified	FALSE	F does not receive every cheap flat-compatible selection available from its own fields: §5.4's enumerated rules select only on time triggers, so dependency-triggered obligations (≥6 mandatory per scenario) are structurally unreachable for F.
C2 TF is the right smallest decomposition	FALSE	TF isolates typed persistence from typed exposure but cannot isolate typed exposure from typed presentation; the missing cell is flat-store-under-typed-render, which opened prior art quantifies as carrying ~87% of the apparent gain.
C3 F strong enough to kill TN fairly	FALSE	F is specified as a discarding store (retraction to unknown); prior art shows the discard choice, not flatness, drives the apparent typed win, and a 1-deep prev-value column costs ~10 tokens/row.
C4 public events do not privilege TN	HOLDS	The §6.1 primitive grammar withholds is_current/is_due/closure/answers, retraction carries only target_event_id, and my traces confirm both reducers get identical deterministic evidence; the asymmetry lives in §5.1's store spec, not in the event grammar.
C5 budget contract binding and fair	UNDERDETERMINED	Verified TN/F density ratio 1.65×–2.19× (measured, Llama-3), but §8.1 never states whether the arm's schema declaration counts inside the memory budget, and "maximum-load fixture" is undefined as selected-set vs live-set.
C6 workload envelope makes gates executable	FALSE	Envelope bounds width but places no cap on the share of gold-positive pairs whose correctness depends on any single update mechanism, so an implementer can predetermine the winner without violating one declared bound.
C7 primary metric has invariant resolution	HOLDS	Exhaustive search confirms the one-action quantum at G=30 is 0.064516 < 0.08, exactly as r2 claims; §13.1's empty-case branch is unreachable but harmless.
C8 decision rule statistically coherent	HOLDS (with one gap)	Simulated OCs meet all five criteria across all six declared families; the r1 bug is gone; but §15.5.7's BCa-agreement gate is binding and is not in §15.4's calibrated rule.
C9 external pilot and cost gate rational	UNDERDETERMINED	Excluding the pilot is defensible for a new instrument, and the four-point envelope does surface affordability pre-pilot, but m=12 is total-cost-suboptimal by a 36:1 margin against m=24–30.
C10 reconstruction measures the named construct	HOLDS (with one gap)	The three mandatory witnesses are the right ones, but nothing forbids the child importing the deterministic generator, which scenario_id alone would make sufficient to replay history.
C11 runner/transport/retry cannot mimic an arm effect	UNDERDETERMINED	Controls are proportionate and match real OpenRouter fields, but whole-pair invalidation correlates with TN payload size, and OpenRouter silently strips strict absent a specific header.
C12 smallest decisive experiment	HOLDS	No framework, DB platform, third primary arm, retrieval family, learned writer, or production doctrine has been added; the machinery that remains is load-bearing (one deletion candidate named in §10).
6. Findings
#	Sev	Location	Mechanism	False-result consequence	Smallest fix	Label
P0-1	P0	§5.4 rules 3–4 vs §7 "at least six dependency-triggered obligations"	Rule 3 selects due/near-due "from public trigger fields and the current public time"; rule 4 walks selected→prereq. Nothing walks prereq→dependent. An obligation whose prerequisite just completed is unreachable for F. TN surfaces it via typed closure.	False TN win on a mandatory, every-scenario stratum, caused by a selector omission rather than persistence. Or, if the implementer silently adds the reverse scan, an unstated choice sets the effect size.	Add rule 3b to the shared materializer: "select any open obligation all of whose direct_prereq_ids are terminal." One pass over ≤28 rows.	EXECUTED
P0-2	P0	§4.2, §5.3, §13.2 (TF diagnostic)	TN differs from TF in both typed semantics and packet layout. r2 has no cell that holds layout fixed while disabling typed semantics.	Persuasive false positive. Opened prior art measures this exact confound on this exact stratum: apparent gain +0.182, of which render is +0.159 and typed mechanism is +0.025, CI crossing zero.	Add a fourth cell on the same 25% subset: flat store rendered in TN's exact layout with typed semantics forced off. Report TN − render-matched as the mechanism residual.	EXECUTED + SEARCHED
P0-3	P0	§8.1 conditions 1 and 2 vs §7 maxima	cond1 needs TN ≤ c; cond2 needs unfiltered-flat ≥ 1.25c. Feasible for some c iff flat/TN ≥ 1.25. Verbosity cancels algebraically. Measured: verbose 0.765, compact 0.457. Both fail.	Gate 1 unsatisfiable under reading 1 (instrument never launches); under reading 2 the implementer's selection ratio silently sets how often TN hits budget_failure, i.e. picks the loser.	Define "maximum-load fixture" as the selected set, and add the explicit invariant unfiltered_flat_tokens ≥ 1.25 × TN_max_selected_tokens with the realised selection ratio published (must be ≤ ~0.61).	EXECUTED
P1-1	P1	§5.1 bullet 7 ("deterministic unknown")	F is specified as a discarding store. Retraction-of-correction and retraction-of-cancellation are mandatory every scenario.	Hidden confound favouring TN on a mandatory stratum. Prior art: retention-coarse recovers +0.361 of a +0.472 apparent typed win; "most of the apparent provenance win was a discard modeling choice, not a property of the coarse class."	Grant F a 1-deep prev_value/prev_source_event_id column and status-on-row tombstones (not deletion). Measured cost ~10 tokens/row. TN still earns depth-≥2 chained restores, which §7 already mandates.	EXECUTED + SEARCHED
P1-2	P1	§13.1 vs §5.4 rule 8	budget_failure scoring is undefined. Dropped step → TN gets a free pass on its hardest steps. All-FN → TN heavily punished.	Unstated choice, opposite-signed bias depending on reading.	Preregister: a budget_failure step scores all its gold-due actions as FN for that arm, and the count is reported separately.	EXECUTED
P1-3	P1	§7 realised-cardinality report	Width bounded; per-mechanism gold mass unbounded. 20 of 30 gold positives could be retraction-dependent inside every declared bound.	Generator composition predetermines the winner. LatticeMind reports exactly this: an earlier benchmark "often favored free-form summarization baselines and did not consistently show an advantage for the structured belief pipeline."	Cap any single update mechanism at a preregistered share of gold-positive pairs; publish the per-mechanism gold histogram in the realised-cardinality report.	EXECUTED + SEARCHED
P1-4	P1	§15.4 vs §15.5 crit 7	§15.4 says simulate "the complete frozen decision rule" ≥100k per family/n; §15.5.7 makes BCa/t agreement binding; §15.3 sets BCa at 50,000 resamples.	Either Gate 4 never passes, or BCa agreement is silently dropped and published OCs overstate decisiveness. Measured disagreement 0.7% at the boundary, 2.4% between.	Simulate the agreement gate at reduced fidelity (2,000 resamples × 2,000 experiments) to bound the rate and publish it, or demote BCa to reported sensitivity. One BCa at n=360 took 0.15 s; the literal grid is ~25 CPU-hours per cell.	EXECUTED
P1-5	P1	§15.4 criteria 1–3, §15.4 "never below 48"	The kill gate (0 → +0.03, distance 0.03) dominates n, not the win gate (0.08 → 0.03, distance 0.05).	Cost shock. Simulation: kill power 0.174 at n=48, 0.406 at n=132, 0.806 at n=360. Analytic binding n: 96 / 360 / 792 / 1404 at SD 0.10/0.20/0.30/0.40. "Never below 48" understates by 7.5×–29×.	State in §15.4 that the kill gate is binding, and publish the n table alongside the four-point cost envelope so the owner sees 360 before the pilot, not after.	EXECUTED
P1-6	P1	§15.2 SD floor max(0.20, s_upper)	The floor is mandatory, so a genuinely low-variance pilot cannot reduce n below 360.	If true SD is 0.10, honest n is 96; the floor forces 360, a 3.8× overspend (MID $135 → $508).	Keep the floor as a default, but allow it to be lowered to the observed s_upper if a preregistered rare-tail probe on the pilot returns empty. Floor still saves the s=0 case (verified).	EXECUTED
P1-7	P1	§15.1 m = 12	m=12 gives Kieser-Wassmer inflation ×1.5506; m=24 gives ×1.3255; m=30 gives ×1.2797.	Total (pilot + confirmatory) cost is not minimised. At true SD 0.25: m=12 → n=1320; m=30 → n=900. 32% fewer confirmatory scenarios for 2,116 extra pilot calls, net saving 75,851 calls. Total-cost-minimising m is 24 at SD 0.15 and 70 at SD 0.20–0.25.	Raise the pilot to m=24–30 and cite Whitehead et al. 2016 for the optimisation. Julious's "12 per group" is a floor for feasibility, not a cost optimum; Teare et al. recommend 70 for SD precision.	EXECUTED + SEARCHED
P1-8	P1	§5.5 "short arm-neutral declaration of the supplied packet schema"	The typed schema declaration is necessarily longer than the flat one. Unstated whether it counts inside the memory-payload budget.	If outside, TN receives free tokens to explain its richer schema; if inside, TN pays twice. Either way the budget is not matched.	State that the schema declaration sits outside the memory budget and is capped at an identical token count for both arms, with the realised counts logged.	EXECUTED
P1-9	P1	§19 borrow list	PM-Bench, StateFuse, Mem2ActBench, τ²-bench verified real. AgenticSTS, LongHorizon-Harness could not be verified to exist this session.	An implementation plan told to "borrow fresh-message assembly from AgenticSTS" may be borrowing from nothing.	Before the implementation plan, require each §19 entry to carry an opened origin URL, or drop it.	SEARCHED (negative)
P1-10	P1	§13.1 primary estimand	Set-F1 conflates information quality with action-aggressiveness calibration. PM-Bench's headline finding is precisely that scaffolds mostly move agents along the precision/recall tradeoff: heartbeat 65.1% F1 with 178 FP vs auto-heartbeat-30 at 57.8% with 489 FP.	A typed packet that merely makes the model more or less trigger-happy registers as an F1 delta.	Report precision and recall separately as preregistered co-primaries, and add mean actions-selected-per-step as a covariate. §15.5 crit 3 partially guards this; it is not sufficient.	SEARCHED
P2-1	P2	§12 whole-pair invalidation	TN payloads are 1.65×–2.19× larger, so TN requests have higher timeout exposure. Pairs invalidate when either arm fails.	Retained sample biased toward scenarios where TN's payload was small, i.e. the easy ones. Bounded by the 5% cap.	Log per-arm payload tokens for invalidated pairs; preregister a check that the invalidated-pair TN payload distribution matches retained.	EXECUTED
P2-2	P2	§9 cursor	Cursor carries scenario_id. The generator is deterministic and seeded. If importable in the child, scenario_id alone reconstructs full history.	Reconstruction success would not depend on the arm artifact. The artifact-withheld witness catches it only if the code does not do it.	Add a mandatory negative witness: the child cannot import or invoke the generator or event-log reader (module denylist or separate package).	EXECUTED
P2-3	P2	§11 transport assertions	OpenRouter strips strict on tools unless the structured-outputs-2025-11-13 header is passed, and routes normally. r2 asserts route/cache/transform metadata but not schema-field survival.	Elevated malformed-JSON rate, scored as primary failure. Arm-neutral in expectation but inflates SD, which raises n.	Add to Gate 3: assert the structured-output/strict field survived the round trip, not only that route metadata matched.	SEARCHED
P2-4	P2	§15.4 criterion 5	Coverage at n=48: 2pt-asym 0.9293, below the 0.94 gate.	None. This is the criterion working: it correctly excludes small n. Noted so it is not mistaken for a defect later.	None. Keep criterion 5.	EXECUTED
P3-1	P3	§13.1 "If TP = FP = FN = 0, the scenario is invalid"	§7 guarantees TP+FN = G ≥ 30, so the denominator is always ≥30.	None. Dead branch.	Delete or annotate as unreachable-by-construction.	EXECUTED
7. Required attacks

Attack A — treatment/materializer parity. EXECUTED.
Built a max-load world at the §7 ceiling (28 open obligations, 40 state rows, 4 scopes, dependency width/depth 3, closure 12, 12 tombstones) and rendered exact F/TF/TN packets, token-counted with a locally-built Llama-3 128k byte-level BPE (roundtrip-validated).

False TN win, found: a two-obligation world, OBL-A terminal, OBL-B open with pre=[OBL-A] and no time trigger. Literal §5.4 selects []. Repaired materializer selects ['OBL-B']. TN selects it via typed closure. Gold is OBL-B. §7 mandates ≥6 such obligations per scenario. r2's shared materializer and density logs do not catch this, because the parity differential in §6.3 only proves F exercises operations available from its own fields, and rule 3 never names this one.

False TN loss, found: measured TN/F density 1.65× (verbose) and 2.19× (compact) at identical selected content. At a binding budget TN either drops records or budget_failures while F sits comfortably. Confirmed against prior art: with deployed renders the sign reverses, fine-d 0.311 vs coarse-d 0.546, fine − coarse = −0.236, "because the heavier ledger render now hurts the reader." r2's density logs do catch and report this, but §13.1 does not say how to score it (P1-2).

Attack B — retraction and public-schema neutrality. EXECUTED.
Traced correction→retraction and cancellation→retraction from §6.1 primitives only.

Reducer	after retraction-of-correction	after retraction-of-cancellation
F (as specified)	'unknown'	not active
F + 1-deep prev column	'VALUE-A' ✓	active ✓
TN	'VALUE-A' ✓	active ✓
gold	'VALUE-A'	active

TN succeeds because it retained legitimate public history, not because the grammar pre-resolved its ontology. C4 holds. But the F-vs-TN gap here is produced by §5.1's discard specification, not by flatness: a 1-deep column (~10 tokens/row) closes it entirely. The grammar is neutral; the store spec is not.

Attack C — exact scorer quantum. EXECUTED.
Exhaustive search over all reachable (TP, FP) at G=30, FP∈[0,40]:

one recovered FN: max Δ = 0.064516 at TP=0, FP=0, FN=30
one suppressed FP: max Δ = 0.016393 at TP=30, FP=1, FN=0
one-action quantum = 0.064516 < 0.08 → r2's claim VERIFIED
quantum by G: 30→0.0645, 40→0.0488, 60→0.0328, 100→0.0198 (G=30 is the binding floor, correctly identified)
boundary cases: zero prediction 0.0; all-gold 1.0; TP=29/FN=1 → 0.983051; TP=30/FP=1 → 0.983607; TP=15/FP=5/FN=15 → 0.600000; lure-heavy TP=15/FP=20/FN=15 → 0.461538

Caveat r2 does not state: one action can move a single scenario delta by 2.2× the +0.03 boundary. Harmless at n≥48 (contributes 0.0013 to the mean), and it is exactly why §15.4's lattice family is load-bearing. C7 holds.

Attack D — budget selection and maximum load. EXECUTED.
Tokenizer: locally-available Llama-3 128k byte-level BPE, disclosed as sensitivity proxy for the eventual exact counter.

Fixture	F	TN	TN/F
verbose JSON, time-only selection (10 obl)	937	1,548	1.65×
verbose JSON, all 28 obligations	2,704	4,491	1.66×
compact positional, 28 obl / 40 state	~941	~2,060	2.19×
unfiltered flat-current (verbose)	3,436		
chronological history, 60 events (verbose)	6,888		

At the verbose max-load fixture no candidate satisfies cond1 (TN=4,491 > 4,096). At the compact fixture no candidate satisfies cond2 (flat/budget 0.61× at 1,536). The loophole is not verbosity. Writing A·v for unfiltered-flat and B·v for TN-max-load, cond1 ∧ cond2 is feasible for some c iff A/B ≥ 1.25; v cancels. Measured A/B: 0.765 verbose, 0.457 compact. Both fail, and structurally must, because on a whole-live-set fixture TN is a superset of the flat dump.

Rescue exists only through aggressive selection: required selection ratio ρ ≤ 0.612 (TN may expose at most ~42 of 68 live records). §7 permits this (≤6 gold due actions, ≤12 closure nodes). But §8.1 never states the constraint, and "maximum-load fixture" is never defined as selected-set vs live-set. That is the loophole that lets the implementer choose the winner (P0-3).

Attack E — full decision-rule calibration. EXECUTED.

r1 bug, independently verified gone. r1's win rule was observed-mean ≥ +0.08 and CI excludes 0. At true mean +0.08, P(observed ≥ 0.08) ≈ 0.5 for any n:

n	r1 win prob	r2 win prob
48	0.498	0.396
96	0.497	0.677
192	0.501	0.932
384	0.497	0.998

r1 was capped near 0.50 structurally. r2 removed the observed-mean cutoff. Bug gone.

r2 OCs, smooth family at the SD floor 0.20 (40k reps):

n	falseWIN@+0.03	WINpow@+0.08	KILLpow@0	falseKILL@+0.08	coverage
48	0.0242	0.395	0.174	0.0003	0.9519
132	0.0261	0.813	0.406	0.0000	0.9490
360	0.0238	0.997	0.806	0.0000	0.9489
504	0.0256	1.000	0.919	0.0000	0.9494

All six families at n=360 meet all five criteria (kill power 0.806–0.839; coverage 0.9481–0.9512). False-win is ~0.025 because a two-sided 95% interval gives a one-sided 2.5% test: conservative, not broken.

Honest correction: my first rare-tail run showed kill power collapsing to 0.429. That was my artifact, an un-normalised mixture whose realised SD exceeded 0.20. With SD held to target, raretail5 and raretail10 both give kill power 0.811 at n=360. Tail shape costs little; tail scale is what matters, and the SD floor already handles scale.

s_upper formula: chi2.ppf(0.05, 11) = 4.574813, inflation ×1.550635. Correct Kieser-Wassmer one-sided upper limit. s=0 → s_upper=0 → floor 0.20 binds, verified. Floor binds for any s < 0.129. Missed-rare-tail probe: pilot drawn from a tail-free core (sd 0.12) against true sd 0.20 understates in 0.0% of pilots because the floor rescues it; without the floor it would be ~100%.

Attack on Student-t and the fixed floor: the t interval is fine. Coverage ≥0.94 everywhere except 2pt-asym at n=48 (0.9293), and the design's own criterion 5 correctly excludes that n. I do not recommend replacing it: BCa would cost 25 CPU-hours per calibration cell and buys nothing measurable at these n. The floor is right in kind and wrong in rigidity (P1-6). My recommended change is not the interval, it is the pilot size (P1-7), which is executable, cited, and quantified.

Attack F — reconstruction dependency. Modelled, READ-ONLY on the eventual harness.
The cursor holds scenario_id, next_step_index, prefix hash. The three mandatory witnesses are the right three. The unstated capability: the child runs "through the same adapter entry point used at ordinary start," i.e. inside the same codebase. The generator is deterministic and seeded (§7). scenario_id plus an importable generator is sufficient to replay the entire public history without the arm artifact. The artifact-withheld witness catches this only if the code does not do it; nothing in §9 forbids the capability. Fix in P2-2. working directory, module globals, and environment are covered by the ambient-removal witness; prefix hash is covered by the fail-closed witness.

Attack G — transport and pair replacement. SEARCHED + modelled.
r2's named controls map onto real OpenRouter fields: only/ignore/order, allow_fallbacks, require_parameters ("only route to providers that support all parameters in your request... avoids silent parameter drops"), and the middle-out transform ("automatically compresses the middle portion of long contexts while preserving the beginning and end"), which is precisely the footgun that would silently void the budget contract. r2 disables it. Correct.

Gap found: OpenRouter applies the structured-outputs header automatically for response_format, but for strict: true on tools, "without this header, OpenRouter will strip the strict field and route normally." Silent field stripping, arm-neutral but SD-inflating (P2-3).

Selection bias: whole-pair invalidation is content-correlated through payload size (P2-1), bounded by the 5% stop. Frozen reserves are the right mechanism; the cost is proportionate. I do not think whole-pair invalidation should be relaxed: partial retention would be worse.

Attack H — cost and proportionality. EXECUTED.
Model: 56 steps (midpoint), 2 primary calls/step, TF on 25%, controls on 25%, oracles on 15%, 3 reconstruction boundaries × 2 arms, 5% reserve. Input ~2,800 tok (2,048 budget + wrapper), output ~60. MID = $2.50/$10 per Mtok; FRONTIER = $15/$75.

n	calls	MID	FRONTIER
48	8,887	$68	$413
96	17,774	$135	$826
192	35,548	$270	$1,653
384	71,215	$541	$3,311

At the n the rule actually demands: SD 0.10 → n=96 ($135 / $826); SD 0.20 (mandatory floor) → n=360, 66,830 calls, $508 / $3,108; SD 0.30 → n=792 ($1,117 / $6,832); SD 0.40 → n=1,404, 260,568 calls ($1,980 / $12,116).

Verdict on affordability: the experiment is affordable at MID pricing across the whole envelope, and affordable at FRONTIER pricing up to SD 0.30. The four-point envelope does its job. The surprise is not the money, it is that "minimum 48" reads as a 48-scenario study when the rule demands 360.

Machinery that can be deleted: §10's SQLite allowance ("allowed only if it is demonstrably simpler for transactional test fixtures"). Plain JSONL is already preferred, the runner is single-in-flight, and a conditional storage branch is a second code path that Gate 2 goldens must cover twice. Delete the allowance; mandate JSONL. Nothing else is idle.

8. WHAT WOULD YOU BUILD

The same instrument, with the arm ladder replaced by a 2×2 store × render factorial on the frozen 25% diagnostic subset. Cost barely moves because the fourth cell reuses the subset budget.

	flat render	typed render
flat store (with 1-deep retention)	F (primary)	R ← the missing render-matched control
typed store	TF	TN (primary)

Contrasts: TN − F primary as now; TF − F typed persistence; TN − TF typed exposure; R − F render; TN − R typed mechanism residual, render held fixed. That last one is the number that actually answers the owner's question, and r2 currently cannot compute it.

Mechanism borrowed, SEARCHED: the render-matched control from Presentation, Not Mechanism (arXiv 2607.16019v1), which specifies it as a reusable protocol precisely so future comparisons can separate layout from mechanism. Their construction: the ledger's exact structured layout with the deprecation mechanism switched off, forcing every co-keyed relation to same-state, no supersedes, no contradicts, no unresolved status.

Also build, on a costed subset only: a status/abstention probe as a preregistered secondary. Mechanically scored, three-way ("in force / superseded / unresolved"), asked about a named (scope_id, state_key). This is where the opened prior art says typed structure actually pays: fine typing is idle on snapshot queries but recovers +0.147 (refines) and +0.152 (cross-source conflict) once the queried coordinate is read and recovered.

Plus: F gains the 1-deep prev column and status-on-row tombstones; §5.4 gains rule 3b; the pilot goes to m=24–30; the n table publishes before the pilot.

9. WOULD YOU DESIGN IT DIFFERENTLY

Yes, on one structural point, and it is the most important thing in this verdict.

r2's primary estimand is "which actions are due now." That is a pure current-state / snapshot query. Two independently opened sources say the answer for that query class is already known and it is approximately zero:

StateFuse evaluated conflict-preserving typed memory against flat multi-value, raw-log, provenance-style and collapsed baselines under matched resolvers and verification policies, on a 282-question conflict-bearing MemoryAgentBench slice, and reports the compared methods tie on answer accuracy, with the authors explicitly declining to argue that explicit conflict objects universally beat strong flat multi-value surfaces. Their retained claim is about the public contract: contradiction surfacing, safe abstention, auditable correction.
ESR-Bench proves (P2b) that for snapshot queries the binary live/dead partition is a minimal sufficient statistic, so finer relation typing carries no additional value-relevant information, b_type = 0. Empirically the typed mechanism residual is statistically zero on all four strata, and coarse invalidation beats the fine ledger by 0.084 on clean supersession.

So r2 is powered to detect an effect that the closest matched-comparator work says is ~0, on the exact query class where it is provably 0, while its action-only output schema (§5.6, no provenance, no state explanation, no abstention channel) structurally excludes every coordinate where typed structure was measured to pay.

That does not make r2 wrong. A kill is a legitimate and valuable answer, and §15.6 plus §18's non-claims are honest. But it means r2 is very likely buying the expensive branch (kill gate binding, n≈360 at the floor, ~$500–$3,100) to re-derive a published null, while remaining blind to the contrast that would tell Moonwalker something new.

The cheaper, truer design: keep TN − F as primary, add the render-matched cell so a win is interpretable, and add the status/abstention probe so a null on actions is not the whole story. If actions tie and abstention/provenance separates, that is a genuinely new and Moonwalker-relevant result: the typed kernel earns its keep as an audit and abstention surface, not as an action-accuracy improver. That is also, not coincidentally, closer to what Moonwalker actually sells.

Second, smaller: PM-Bench's headline lesson is that scaffold changes mostly move agents along the precision/recall tradeoff (65.1% F1 with 178 FP vs 57.8% with 489 FP). Set-F1 alone cannot distinguish "better information" from "differently calibrated aggressiveness." Report precision and recall as co-primaries.

10. Omission attack
Strong simple comparator still omitted: not NONE. Two. (a) The render-matched flat-store-under-typed-layout cell (P0-2). (b) F with 1-deep retention (P1-1). Both are cheaper than TN and both are what a competent engineer would actually build before reaching for a typed kernel.
Hidden confound favouring F: TN's typed metadata costs 1.65×–2.19× tokens for identical selected content (measured). At a binding budget TN carries fewer records or budget_failures. Amplified because §13.1 does not say how budget_failure scores. Prior art confirms heavier renders can reverse the sign (fine − coarse = −0.236 under deployed renders).
Hidden confound favouring TN: three, all on mandatory-every-scenario strata. (1) F cannot surface dependency-triggered obligations under the literal §5.4 rules. (2) F is a discarding store on retraction. (3) TN's packet layout is more readable, and nothing holds render fixed.
Persuasive false-positive story: TN wins by +0.09 on the retraction and dependency strata. The team reports a typed-package win, TN − TF is positive so it looks like typed exposure earns it, and the kernel gets built. In fact ~87% of the gap was layout readability (render term +0.159 vs mechanism +0.025 in the opened analog on this exact stratum), and most of the remainder was F's discard specification plus the missing reverse-edge scan. Every one of r2's current gates passes.
Way the design could unfairly kill a useful typed kernel: the workload is action-selection only. ESR-Bench proves typed structure is information-theoretically idle for snapshot queries. r2 would return a correct null on actions, Moonwalker would conclude "typed continuity does not earn its complexity," and would discard a kernel whose measured value (abstention, contradiction surfacing, provenance-from-retained-state) was never on the instrument. Compounded by the SD floor forcing n=360 even when the true SD is small, making the null look better-powered than it was cheap to get.
Framework/provider/statistical footgun not caught: OpenRouter strips strict on tools without the structured-outputs-2025-11-13 header and routes normally. §11 asserts endpoint, cache, fallback, transform, and parameter metadata; it does not assert that the structured-output schema field survived the round trip. Raises malformed-primary-output rate, which §12 scores as failure, which inflates SD, which raises n.
One no-paid test without which I refuse pilot inference: the Gate-1 budget feasibility check restated as unfiltered_flat_tokens ≥ 1.25 × TN_max_selected_tokens on the exact tokenizer, with the realised selection ratio published. It is free, it takes an afternoon, and my measurements say the contract as currently worded has no solution. Everything downstream of a budget that cannot exist is wasted money.
One mechanism to borrow directly from prior art: the render-matched control from Presentation, Not Mechanism (arXiv 2607.16019v1, §F, released as a reusable protocol). SEARCHED, opened at origin.
One piece of machinery to delete: §10's conditional SQLite allowance. Mandate plain JSONL. Everything else is load-bearing.
11. Sweep log
Lane	Query	Opened	Decisive section	Effect	Label	Stop
1 Already answered	PM-Bench prospective memory benchmark LLM agents	arxiv.org/html/2607.12385v1 (full)	§4.1 primary metric; Table 2	Set-F1 identical to r2's; todo-ledger 62.8 vs single 60.0 vs best 65.1 → r2's +0.08 alternative exceeds the whole no-scaffold-to-best-scaffold gap in the closest analog	SEARCHED	Confirmed r2's contrast is not run there
1 Already answered	StateFuse matched resolver materializer representation comparison + StateFuse conflict-preserving flat multi-value baseline abstention results	arxiv 2607.05844 (body via retrieval; PDF fetch returned empty)	§5.2 "What the Strong Flat Baselines Mean"	Typed vs strong flat tie on answer accuracy under matched resolvers; authors retreat to contract claims	SEARCHED-PARTIAL	Two independent retrievals agreed; direct fetch failed
2 Comparator/decomposition	same as above	arxiv.org/html/2607.16019v1 (full)	§4.1 render-matched decomposition, Table 2; §4.3	The decisive hit. Render +0.159, fine-d mechanism +0.025 (CI crosses 0), coarse-d +0.087. Provenance needs retention not typing; discard was a modeling choice worth +0.361	SEARCHED	Deciding source found; stopped
3 Prospective/action eval	via PM-Bench + render-confound reference lists	reference lists only	Mem2ActBench = Shen et al. 2026 arXiv 2601.19935 (real); AgenticSTS, LongHorizon-Harness, CAME/STITCH, MAGE/MemoryArena, AgeMem not located	§19 borrow list is partly unverifiable	SEARCHED (negative)	Field-level negative recorded, not concluded absent
4 Bounded paired inference	internal pilot sample size re-estimation variance uncertainty Browne rule of thumb	journals.sagepub.com (Whitehead et al. 2016, body via retrieval); NCSS PASS PDF; arXiv 1703.06957, 2603.17031	Kieser & Wassmer 1996 = r2's exact s_upper method; Julious 2005 = the "12" rule; Teare recommends 70	r2's formula is correct and named; m=12 is a feasibility floor, not a cost optimum	SEARCHED-PARTIAL	Method provenance established
5 Generator bias	surfaced in lane 2	arxiv 2608.08236 (LatticeMind, body via retrieval); 2605.12477 (MEME)	LatticeMind negative result; MEME dependency reasoning	Benchmark composition determines whether structured memory wins; none of six systems solves dependency reasoning	SEARCHED-PARTIAL	Confirmed P1-3 and P0-1 independently
6 OpenRouter footguns	OpenRouter provider routing allowlist require_parameters transforms middle-out fallback prompt caching docs	openrouter.ai/docs/guides/routing/provider-selection, openrouter.ai/blog (body via retrieval); pydantic, hexdocs, openclaw	provider-selection: strict-field stripping; middle-out transform semantics	r2's controls are real and correctly named; found one uncovered stripping footgun	SEARCHED-PARTIAL	Sufficient for a validity question

Non-US/non-UK named institutions and national-language surfaces reached: Shanghai Jiao Tong University School of Medicine (Shanghai) and University of Electronic Science and Technology of China (Chengdu), co-authors of the render-confound paper, which also runs a bilingual phenomenon classifier and uses DeepSeek-V3/V4-flash and MiniMax-M2.5 as judges; Xiamen University and Jilin University (MemSyco-Bench). Paired with English-language named-institution passes (UCLA for PM-Bench, Glasgow/UCL for the render confound).

12. Residual risks and explicit non-claims

A positive r2 result (post-fixes) still cannot establish: that typed continuity beats retrieval, learned writers, or provider compaction; that it generalises across models or providers; that the effect is mechanism rather than presentation unless the render-matched cell is added; that it holds outside the frozen budget and workload; that production Munin works.

A negative r2 result still cannot establish: that typed continuity is worthless. It would establish only that typed structure does not improve prospective action selection under a bounded packet, which ESR-Bench's P2b predicts analytically for snapshot queries. It says nothing about abstention, contradiction surfacing, provenance recovery, or auditability, which is where the opened prior art locates the value and where Moonwalker's actual product claim lives.

Residual risks I could not close: whether the eventual exact tokenizer preserves my measured density ratios (my Llama-3 counts are a disclosed proxy); whether the realised scenario-level SD lands near 0.20 (PM-Bench's per-model spread of 42.0–78.9 suggests it could be higher, which would push n toward 792); whether budget_failure is rare enough for its scoring rule to be immaterial; whether the BCa agreement gate's 0.7–2.4% disagreement rate is stable at the final n.

13. Seat capability report
Model: Claude Opus 4.6. Harness: claude.ai chat with a governed MCP bridge to the host plus an isolated Linux sandbox.
Local reach: full read of the pinned repo and vault via the Moonwalker bridge, verified by independent SHA-384/SHA-256 computation. The bridge went down partway through Attack D and did not recover; the compact-schema sensitivity was therefore completed in my sandbox using a chars-per-token constant (2.3378) calibrated against five real Llama-3 measurements taken on the host before the outage. Disclosed as a proxy, and the algebraic result (Attack D) is verbosity-invariant, so it does not depend on the proxy.
Web reach: yes. Two sources opened at origin with full text; six read as retrieval-layer body text where my own fetch failed or was not attempted, labelled SEARCHED-PARTIAL throughout rather than claimed as opened.
Execution reach: yes, both host (until the outage) and sandbox. All statistics, the tokenizer, and every attack computation were executed, not reasoned.
Tokenizer limitation: no exact provider tokenizer available; tiktoken installed but its BPE files are network-blocked in my sandbox. I built a byte-level BPE from the host's local Llama-3 128k tokenizer.json and validated it by roundtrip decode on three probes, including a JSON fragment. The ASCII-restricted split regex is exact for the pure-ASCII fixtures used.
Statistical limitation: OC simulations ran at 40,000 reps, not §15.4's 100,000, for time. Monte Carlo error at these rates is ≈±0.002–0.004, well inside every margin I relied on. One first-pass rare-tail result was wrong and I corrected it in-thread rather than shipping it.
Paid inference performed: NONE.
Tool side effects: one probe directory under %TEMP%\mbcx_probe\ (one extracted blob, one script). No writes to the repo, vault, design, or any seat file. Nothing installed on the host; sandbox package installs only.
Confirmation: I did not read another seat's verdict, synthesis, exec output, or restart manifest, and did not consult any other conversation. Filenames were visible in git ls-tree/git status; no contents were accessed.

Bottom line, crayon level: the statistics are sound and the r1 bug is genuinely dead, but the experiment as pinned is rigged three ways toward TN without anyone meaning to rig it, the budget gate as written has no solution, and the thing you are powering to detect has already been measured at roughly zero twice by people who held their comparators fixed. Add the fourth cell, give F its one-deep undo, fix rule 3b, restate the budget invariant, and you have an instrument worth paying for. 🐘
