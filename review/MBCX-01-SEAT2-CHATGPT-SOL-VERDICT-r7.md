1. Top-level verdict

NO-GO(NORMATIVE CONTRACT REMAINS NON-TOTAL; BOUNDEDNESS, COHORT SELECTION, AND EARLY INFERENCE CAN STILL CHANGE THE SCIENTIFIC ANSWER)

r7 is a substantial improvement over r6. Several prior blockers are genuinely repaired: the ACT→completion mapping is explicit, the impossible Cartesian OC grid is gone, missing BC/OM pairs are jointly completed, the historical confseq blobs are corrected, and the periodic-vector indexing convention is explicit.

I would not redesign the three-stage experiment or replace FD/FC/TN. The remaining blockers are instrumentation defects. But they are P1 scientific defects: implemented literally, r7 can still false-pass bounded continuity, select different Stage-2 cohorts, stop on the wrong model-usability branch, admit reasoning through supposedly closed packets, or score A0/B/A1 differently depending on implementation.

2. Seat identity and review posture
MBCX-01 r7 — GPT-5.6 Sol / ChatGPT + Moonwalker MCP Longitudinal Browser Council Verdict

Model: GPT-5.6 Sol
Harness: ChatGPT web browser + Moonwalker MCP
Seat posture: LONGITUDINAL-BROWSER / LATERALLY SEALED

r7 explicitly makes retained same-lane context intentional. I therefore disclose that this browser lane retains the prior MBCX-01 r6 review and do not claim per-round freshness. Recommendations that substantially repeat prior same-lane repairs are labelled inherited where relevant.

The lateral seal held: I did not inspect another current r7 seat, r7 verdict, council output, synthesis, execution receipt/log, marker, watcher, or browser output.

3. Pin / byte verification

Adjudicated repository commit:

6cf58b4ad123cb7487faae5499e623d316a06d47

Artifact	Git blob	Bytes	Lines	SHA-384	Working copy
MBCX-01-EXPERIMENT-DESIGN-r6.md	124e4be74c795f0ab5e686a2ed9d664d45639d1b	10,660	134	3496481950FE9E07E1FFE655BAFD90F233301853CB0A32C279AE530FA36743787DEADF672EA403C17FD19451D7103FA2	EXACT
MBCX-01-STATE-ACTION-CONTRACT-v2.json	e1d8f598dbc00e18fdaa501953f4e68bc3b27d13	8,481	142	2A129568426287497FEA3404462591106AEBCD1B099963F916A9A463E707778DD484CAD43AA629DF489E83BD85EE8DAE	EXACT
MBCX-01-PACKET-SCHEMAS-v1.json	d31a9aae27e53c6a4e3d8be150db2652a43ff0aa	6,356	95	D9315572FD816BF748C528580C7F1AD75E4C70534C0ABB8494D1B162EC48908E6DD906EDE90E35A5791E69FC27195714	EXACT
MBCX-01-MEASUREMENT-CONTRACT-v1.json	095f24be2faecb19f6a6e772c58f5c7468174f54	4,630	85	C0ED0F0AE92DC5B221130CA731EF1DE16D75634FE48F0DB7987A87679B0E973A8367629B6BEA518D1F5631B84E857925	EXACT
MBCX-01-INFERENCE-CONTRACT-v2.json	907d3f65af540bc1efb5674b711f9f0aa593b75e	7,869	116	2883EC875757E91DF903960A9632F2C21032D55A96C0CF4E33D57A731E898DD941059C2BA7E88530CB17EE6763989F15	EXACT

I independently computed Git path blobs, working-copy blobs, byte counts, line counts, and SHA-384s.

Current repository HEAD was later than the adjudicated commit (52592a2a7a1c91e8501d3105a3be36cc6ecedb8d), but all five named working-copy artifacts remained byte-identical to the r7 pin, so no working-tree drift affected this review.

The packet's named test-r7-normative-bundle.ps1 also matched its pinned blob f8680103e95ea3a6b04b521d4e491a748fdbb0bc. I executed it and obtained:

PASS: r7 five-artifact normative bundle and fourteen red-witness closures hold.

I then read the test itself. It proves the repair declarations are present, which is exactly the limited evidentiary role r7 assigns it; it does not dynamically execute most of the fourteen bypasses.

4. Evidence and probes
EXECUTED

I independently executed:

five-artifact Git/byte/hash verification;

the r7 fourteen-witness bundle script;

structural enumeration of all 17 event types;

event guard/payload coverage analysis;

scoped-idempotency alternative-bypass construction;

atomic multi-action pre-state-vs-sequential validation counterexample;

strict Draft-2020-12 packet-schema validation with adversarial objects;

free-text smuggling inside DecisionPacketV2.fields;

ABSTAIN-with-action and PROPOSE-without-action WorkerHandoffV2 cases;

packet-hash-domain ambiguity using two plausible hash constructions;

multiple-eligible-cut cohort-selection counterexample;

registered-counter and unit-total arithmetic;

hidden archive-linear CPU-work false-pass;

interior H×D interaction false-pass;

page-count versus byte-bound false-kill arithmetic;

all nine explicit OC cell probability checks;

exact r7 Hoeffding radii at 96/192/384;

early MODEL_INTERFACE_FAIL counterexample versus terminal result;

early MODEL_OR_INTERFACE_CEILING counterexample versus terminal result;

early-PROMOTE reachability algebra;

four-missing and seven-missing joint-completion enumeration;

call/reconstruction counts at all three looks;

transport per-call/pair reliability arithmetic;

1,000-attempt zero-failure confidence-bound ambiguity.

READ-ONLY

I could not honestly execute:

all 289 semantic ordered event-pair transitions, because v2 itself does not specify enough payload/guard semantics;

FD/FC/TN candidate implementations;

the seven reconstruction witnesses against actual candidate artifacts;

candidate-process environment/module-cache/network isolation;

actual Stage-1/Stage-2 manifest generation;

actual render-discriminator/tokenizer experiments;

actual route soak against the future endpoint.

For each, I attacked the normative contract rather than fabricating an implementation.

SEARCHED

I opened current primary sources for finite-population sequential inference, DOE interactions/randomization, JSON Schema/JCS, SQLite page accounting, Bazel dependency accounting, Temporal/Orleans durability, current memory-system baselines, and current provider/router behavior.

UNSEARCHED

Explicitly outside r7's load-bearing scope: production security, hostile actors, fleet/deployment, FIPS/CNSA, commercialization, concurrent writers, cross-model transfer, procedural/personality memory, and the subsequent coordination experiment.

5. Applicability ruling + WHY THIS EXISTS

The scope override is correct. This review concerns the scientific instrument—not Moonwalker's production security or commercialization.

ALREADY-BUILT? — SEARCHED / READ-ONLY

Pieces are already built; the conjunction is not. Durable workflow replay exists in systems such as Temporal, which explicitly guarantees workflow resumption after crash/outage; Orleans provides durable actor identities and single-threaded activation semantics. 
Temporal Docs
+2
Microsoft Learn
+2

Likewise, Text2Mem already demonstrates typed memory-operation schemas separated from backend execution, while current memory research shows substantial tradeoffs among file, indexed, RAG, and more elaborate representations rather than a universal winner. 
ACL Anthology
+2
arXiv
+2

Ruling: adopt these patterns; do not replace MBCX-01 with an off-the-shelf product.

PRODUCT-FIT? — READ-ONLY

Yes. Strong fit.

The customer/product question in plain language is:

Can Moonwalker preserve the obligations that matter without paying work proportional to everything that ever happened?

That is governed power, fail-loud, and anti-overbuilding. The presence of ordinary-file, RAG, namespace/blackboard, rolling-context, raw-replay, OM, and OAR controls is particularly healthy: a special mechanism must earn its complexity.

BIGGER-THAN-THE-BUG? — READ-ONLY

No. This is deliberately an experiment/design lane, not an accidental subsystem smuggled in through a bug fix. It has the right design-gate shape.

6. Claim scoreboard C1–C12
Claim	Ruling	Reason
C1 — North Star and decomposition	HOLDS	The experiment still lets FD/FC preserve continuity when TN loses, and deterministic failure cannot be rescued by model performance. Simple files/RAG remain legitimate controls.
C2 — total state/action/writer semantics	FALSE	17 event names exist, but only two carry an explicit guard and two an explicit payload contract; handoff state is absent; semantic_operation is unconstrained; atomic multi-action validation has two possible results.
C3 — packet schemas and presentation parity	FALSE	Nested fields is open; WorkerHandoff status/action combinations are unconstrained; A0/A1 output schemas are absent; packet_hash has no hash-domain rule.
C4 — FD/FC/TN completeness	HOLDS	No semantically distinct fourth public mechanism emerged. Graph/trie/index/checkpoint/namespace/raw replay fit as representations, implementations, or controls. StateFuse's multi-replica conflict preservation is outside this single-writer lane. 
arXiv

C5 — cohort and unique paid target	FALSE	Exactly-one-gold is a real repair, but the 80→64 selector does not specify how multiple eligible cuts within one scenario collapse to one scenario/cut. Different literal interpretations yield different manifests and can duplicate a scenario.
C6 — physical boundedness	FALSE	The counter surface can miss archive-linear CPU work; the H×D cross is sparse enough to miss an interior interaction; independent byte/page bounds can reject one bounded extra page.
C7 — process-cold isolation/reconstruction	FALSE	Runtime config is closed, but the explicitly allowed candidate implementation itself can carry a precomputed lookup keyed by journal/scenario identity. No source-freeze-before-gold rule closes that producer-taint path.
C8 — serial handoff and replay	FALSE	The scorer/conjunction is not normative; A0/A1 response schemas are absent; crash-after-provider-acceptance-before-response-journal has no deterministic disposition and can cause resampling.
C9 — engineering and carrier fairness	HOLDS	The Pareto result and separately labelled carrier are conceptually separated correctly. This ruling assumes repaired candidate eligibility/measurement.
C10 — inference validity	FALSE	The terminal n=384 Hoeffding calculation is coherent, but binding 96/192 decisions estimate prefix conditional means, not the declared average over the full 384-scenario frozen manifest.
C11 — OC, missingness, transport, and cost	FALSE	Paired cells and joint missing completion are repaired, but OC RNG/association algorithms and transport CI/per-call budget mapping remain undefined; route-soak cost can remain endpoint-dependent.
C12 — smallest decisive instrument	UNDERDETERMINED	The three stages remain justified, but early binding looks and the historical confseq comparator may be removable once the primary inference is repaired.
7. Finding table
Sev	Finding / exact location	False-result mechanism	Smallest repair	Evidence
P1	F1 State algebra still non-total — state v2 29–81, 128–132	Only 2/17 events have explicit guards and 2/17 explicit payload contracts; no handoff-state machine; caller-controlled semantic_operation can alter idempotency identity.	Freeze typed payload, precondition, state transition, illegal result, and semantic-operation value for all 17 types; derive semantic operation from event type.	EXECUTED
P1	F2 Atomic multi-action semantics ambiguous — state 97–112	For O1→O2 dependency, validating all children against pre-state rejects O2; validating in ordered provisional state commits both. Both satisfy current prose.	State whether child legality is evaluated against one immutable pre-state or a sequential provisional state, and red-witness it.	EXECUTED
P1	F3 Packet/scoring contract open — packet 12–67; design 42–52, 88–94	Free-text reasoning validates inside fields; ABSTAIN+action and PROPOSE+zero-action validate; no A0/A1 schemas; no contract_success definition.	Use discriminated object-field schemas; conditional Worker status constraints; add exact A0/A1 schemas and exact three-decision scorer.	EXECUTED
P1	F4 packet_hash hash domain undefined — packet 15,33,45,59,71,76,92	Hash-excluding-field and hash-placeholder rules produce different hashes; Task/Worker binding can disagree. Literal full-object hashing becomes self-referential.	Define exact hash preimage, e.g. RFC8785 of packet with packet_hash field absent.	EXECUTED
P1	F5 Stage-2 selector non-total — design 57–61	Treating eligible (scenario,cut) pairs as candidates can select the same scenario twice; choosing one cut per scenario gives another manifest.	Freeze 80 unique scenario IDs first; select exactly one cut per scenario by one exact hash rule; then test eligibility; assert final scenario uniqueness.	EXECUTED
P1	F6 Closed counters miss archive-linear compute — measurement 5–24, 44–66	Candidate performs H CPU iterations after constant registered I/O; every registered counter remains flat, latency cannot substitute, continuity passes.	Either narrow the claim to registered I/O work or add an enforceable compute-work counter/primitive.	EXECUTED
P1	F7 Sparse H×D cross misses interior interaction — measurement 34–42	cost=10000 only at (H=10000,D=64) passes H@D16/256, D@H1024/100000, and the combined corner.	Run the full 4×5 H×D deterministic grid at fixed F=16. Only 20 cells.	EXECUTED + SEARCHED
P2	F8 Absolute byte/page bounds can false-kill bounded indexing — measurement 7–24	One extra 65,536-byte storage page passes the ≤4-page allowance but violates 4,096/8,192-byte allowances. SQLite formally permits 512–65,536-byte pages. 
SQLite
	Freeze page size/backend or make byte bounds consistent with maximum allowed page growth.	EXECUTED + SEARCHED
P1	F9 Candidate implementation is an unclosed taint carrier — design 82–86; measurement config 49–56	Runtime cannot read reference/gold, but allowed implementation code can embed precomputed journal-hash→artifact mappings and pass reconstruction.	Freeze candidate source before manifest/gold generation, or generate confirmatory scenarios after candidate-source freeze; add embedded-reference red candidate.	READ-ONLY construction
P1	F10 Early binding inference targets the wrong population — inference 4–20, 34–41	Prefix 96 can bind FAIL/CEILING although the same complete 384 manifest is terminally inconclusive.	Make 96/192 informational only, or randomize scenario sampling and use finite-population inference appropriate to the terminal manifest.	EXECUTED + SEARCHED
P1	F11 OC simulation remains non-total — inference 43–80	432 requested cell/missing/placement/association combinations, but no RNG seed and no algorithm/strength defining BC_FAILURE_ENRICHED, etc.; two harnesses can publish different power/call estimates.	Freeze RNG, master/cell seeds, missing-position algorithms, and exact enrichment distributions.	EXECUTED
P1	F12 Route-soak pass rule is ambiguous — inference 109–114	With zero failures/1000, one-sided exact 95% upper ≈0.002991 passes a ≈0.00304 per-call budget while a conventional two-sided CP upper ≈0.003682 fails.	Freeze CI method, sidedness, dependence-safe mapping from six calls to pair budget, and acceptance criterion.	EXECUTED
P1	F13 Crash-before-journal ambiguity regressed into r7 — design 50,94; state 69–74	Provider may accept a request, process dies before bytes are journaled, restart cannot know whether retry resamples an accepted stochastic call.	Durable request state; retry only with proof request was never accepted. Ambiguous post-send failures become missing/no-resample unless provider offers true request idempotency.	READ-ONLY + SEARCHED
P2	F14 Current bundle test is declaration-only — named test	It asserts closure strings/fields but does not make most old bypasses go red.	Keep it as static bundle sanity, but never count it as the Gate-1 red-witness suite.	EXECUTED

NIST's DOE guidance independently supports F7: when multiple factors can interact, interaction terms are distinct experimental effects; full factorial designs are what expose the full interaction surface rather than only selected slices. 
NIST
+1

8. Attacks A–J
Attack A — program decisions

The intended decision decomposition is coherent:

World	Correctly scoped result
TN useless, FD succeeds/bounded	BOUNDED_CONTINUITY_SURVIVES; TN need not win
Every candidate unbounded	BOUNDED_CONTINUITY_FALSIFIED
Only H×D interaction is unbounded	That candidate should fail boundedness; if none remains, FALSIFIED
OM upper bound < .80	MODEL_OR_INTERFACE_CEILING
BC clearly inferior and OM floor clears	MODEL_INTERFACE_FAIL
Neither directional branch clears	INCONCLUSIVE_OR_UNDERFUNDED

Interpretation: C1's causal decomposition survives.

Fresh bypass: r7's sparse H×D test can misclassify the third world as bounded.

Attack B — state/action totality

Parsed event set: 17.

Executed structural counts:

WITH_EXPLICIT_GUARD = 2
  complete_obligation
  record_call_response

WITH_EXPLICIT_PAYLOAD_CONTRACT = 2
  record_call_response
  propose_handoff_result

NO_HANDOFF_STATE = true
SEMANTIC_OPERATION_CATALOG = false

The ACT repair itself is good: ACT:{scope}:{obligation} now resolves the obligation and sources completion_action_id from canonical state.

The atomicity attack remains red. Initial state:

O1 = due OPEN
O2 = OPEN, depends on O1
proposal = [ACT:O1, ACT:O2]

Executed interpretations:

validate all against original pre-state → REJECT_ALL
validate ordered provisional state:
    complete O1
    O2 becomes due
    complete O2                     → COMMIT_BOTH

The contract says both “validate every child first” and execute ordered actions, but does not decide which state the later validation sees.

The scoped-idempotency repair also has an alternative bypass:

(scope=S1, semantic_operation=COMPLETE, key=K)
(scope=S1, semantic_operation=COMPLETE_ALIAS, key=K)

are different identities, and no contract derives/fixes semantic_operation from event_type.

Result: C2 FALSE.

Attack C — schemas and rendering

Using a Draft-2020-12 validator, I executed three adversarial packets.

Free-text smuggling:

DecisionPacketV2.objects[0].fields.reasoning
  = "THE GOLD ACTION IS ACT:SCOPE:OBL"

Result:

VALID = true

The reason is mechanical: the nested fields schema is merely { "type": "object" }; JSON Schema permits additional properties unless the particular subschema closes them. 
Tour of JSON Schema
+1

Status/action contradictions:

status_code = ABSTAIN
proposed_action_ids = [ACT:SCOPE:OBL]

→ VALID

status_code = PROPOSE
proposed_action_ids = []

→ VALID

There is no if/then, oneOf, or minimum-action rule tied to status_code.

Hash ambiguity: two plausible rules for the same representative packet yielded different SHA-384s:

exclude packet_hash field
74FEAADCA8FD...C35CB16

include empty packet_hash placeholder
5CD33E1D9462...3A6F828

No contract chooses.

Other results:

outer schemas themselves do reject unspecified top-level fields;

Semantic IDs have useful length/grammar caps;

state IDs have no corresponding declared grammar, so state→packet interoperability is not total;

ID permutation exists, but no exact bijection-generation/inverse algorithm is frozen;

tokenizer/padding leakage cannot be executed before the tokenizer and real rendered fixtures exist.

RFC 8785 requires the canonical JSON representation itself to omit token whitespace; r7's design can remain compatible if the packet hash covers the unpadded canonical representation and the served envelope is separately hashed—as it intends—but the missing packet_hash preimage rule must be fixed first. 
RFC Editor

Attack D — cohort and gold

Multi-gold: excluded from paid eligibility. GOOD.

No eligible / fewer than 64 per motif: explicit DESIGN_OR_IMPLEMENTATION_FAIL. GOOD.

F=16/64/256 resource cells: explicitly outside paid action scoring. GOOD.

Motif balance: retaining exactly 64 per motif preserves count balance.

The selector itself is ambiguous. I constructed three scenarios, each with two eligible cuts. Sorting all eligible scenario-cut pairs by the declared hash produced:

S2/C1
S1/C2
S2/C2
...

Taking the first three gives scenario IDs:

S2, S1, S2

Only two independent scenarios.

Selecting the minimum-hash cut within each scenario first yields:

S2/C1, S1/C2, S3/C2

—three independent scenarios.

Both are reasonable readings of:

sort eligible candidates by hash of scenario_id, cut_id...

NIST's sampling guidance is also relevant to r7's word “unbiased”: representative sampling claims require an actual randomization/sampling mechanism; deterministic hash ranking is not self-proving statistical randomization simply because hashes look irregular. 
NIST
+1

The easiest repair is not fancy statistics: freeze 80 unique scenario IDs/motif, select one exact cut per scenario, then apply eligibility, then select 64 unique eligible scenarios. If “unbiased” is not needed, delete that adjective.

Attack E — boundedness

The closed counter mechanics themselves work as specified: per-counter and same-unit totals prevent merely renaming/splitting counted work.

Fresh false pass 1: invisible compute

At all H values I held every registered counter constant at 10 while an implementation performs:

hidden_cpu_iterations = H

Results:

all registered per-counter gates  PASS
all unit-total gates              PASS
hidden CPU work range             99,872 iterations
CPU counter registered            false
latency allowed as boundedness substitute false

Therefore an archive-linear computation can satisfy the literal deterministic boundedness contract.

Fresh false pass 2: missed interaction

Define:

cost(H,D) =
  10,000  only when H=10,000 and D=64
  10      otherwise

Executed r7 surfaces:

H @ D=16       10,10,10,10
H @ D=256      10,10,10,10
D @ H=1024     10,10,10,10,10
D @ H=100000   10,10,10,10,10
combined corner 10

Yet:

cost(10000,64) = 10000

That exact cell is never tested.

With only four H values and five D values, the honest wholesale close is the 20-cell H×D factorial. NIST's DOE material treats interactions as their own effects and full-factorial coverage as the non-confounded way to expose them. 
NIST
+1

Fresh false kill

The contract allows an H-range of four pages but only 4,096 bytes on an artifact counter / 8,192 bytes in the byte-class total. SQLite officially permits 65,536-byte pages, and reads are normally page-granular. 
SQLite

One additional bounded page:

PAGES_READ range = 1       PASS
bytes range      = 65,536  FAIL

So the same O(1) page-height change is accepted or rejected depending on backend page size.

Bazel's Skyframe supports r7's broader dependency-accounting doctrine: direct unregistered data access is specifically identified as producing incorrect incremental builds. 
Bazel Documentation

Attack F — isolation and reconstruction

The runtime config closure is materially better: no arbitrary source path, precomputed_packet, gold, selected event IDs, or generator path.

But the candidate implementation is itself authorized input.

A contaminated implementation can contain:

journal_hash → precomputed candidate artifact

It reads only permitted journal bytes, performs no forbidden file/network read, and writes a self-sufficient artifact. That can satisfy:

source-directory rename;

artifact swap;

field mutation;

clean journal equality;

no forbidden runtime read.

Runtime taint canaries therefore cannot prove the implementation was not produced from reference/gold knowledge.

Smallest repair: candidate implementations must be frozen before confirmatory scenario/gold generation, or the confirmatory manifest must be generated blind after implementation freeze.

I could not execute the seven actual reconstruction witnesses because no FD/FC/TN artifact implementation exists yet. That is the exact missing surface.

Attack G — serial DAG

The frozen maximum arithmetic is correct:

Look	Accepted calls	Reconstructions	Max attempts if every accepted node gets one proven pre-accept retry
96	576	192	1,152
192	1,152	384	2,304
384	2,304	768	4,608

record_call_response now keys on (scenario_id, condition, node) and covers A0/B/A1. That is a real r6 repair.

But the crash seam is no longer total:

request sent
provider accepts/computes
process dies before record_call_response
restart

The runner has no durable evidence proving whether the request was accepted. Retrying may sample a second stochastic response; refusing to retry yields a missing pair.

Current OpenAI documentation exposes client request IDs for tracing/support, but a client request ID is not itself a general exactly-once inference primitive. 
OpenAI Platform
 OpenRouter's router metadata is useful but explicitly absent in some failure classes, so it also cannot universally close this crash seam. 
OpenRouter

The missing rule should be the old durable-systems one:

after a request may have crossed the acceptance boundary, ambiguity means missing/no-resample unless the provider supplies actual idempotent recovery.

Temporal is relevant prior art precisely because durable-execution systems make crash/replay state an external runtime concern rather than asking application logic to remember what happened. 
Temporal Docs

There is also still no normative contract_success scorer or A0/A1 output schema, so the exact “one scored conjunction” remains undefined.

Attack H — inference

The basic mathematics reproduce.

With:

look_alpha = 0.025 / 3

I independently obtained:

n	delta radius	OM radius
96	0.337905278990	0.168952639495
192	0.238935114173	0.119467557086
384	0.168952639495	0.084476319748

The Bonferroni accounting is internally coherent: two streams × three looks, each two-sided interval controlled at 0.05/6.

The nine OC probability cells are all feasible and sum to one. The r6 impossible-cell defect is genuinely closed.

Joint missing-pair completion is also computationally tractable; m=7 means only:

4^7 = 16,384

binary BC/OM completions.

The fatal issue is the estimand

r7 declares:

average conditional mean over the frozen 384-scenario manifest

but allows the prefix 96/192 intervals to bind.

Those intervals estimate the average conditional mean of the observed prefix, not the unobserved complete finite manifest when scenario-specific means may vary arbitrarily.

Executed false early interface failure

First 96:

OM = 1 on all 96
BC fails on 43, succeeds on 53

delta mean = -0.4479167
delta upper = -0.1100114 < -0.10
OM lower = 0.8310474 >= 0.80

r7 stops:

MODEL_INTERFACE_FAIL

Now let the remaining 288 scenarios have BC=OM=1.

Full frozen 384 manifest:

delta mean = -0.1119792
delta interval = [-0.280932, +0.056973]
OM lower = 0.915524

Terminal branch:

INCONCLUSIVE, not interface fail.

Executed false early ceiling

First 96:

OM = 58/96 = 0.604167
BC = OM
OM upper = 0.773119 < 0.80

r7 stops:

MODEL_OR_INTERFACE_CEILING

Remaining 288 all succeed.

Full manifest:

OM = 346/384 = 0.901042
OM interval = [0.816565, 0.985518]

Terminal result is not ceiling.

This is exactly the distinction handled by finite-population sequential inference. Waudby-Smith and Ramdas develop confidence sequences specifically for sequential sampling without replacement from a finite population, including decisions about when to stop. 
arXiv
+1
 Newer 2026 work likewise treats the finite-population mean under WoR as a distinct inference problem. 
arXiv

The smallest repair is even simpler: make 96 and 192 informational, with all scientific branches binding only at 384.

Side finding: PROMOTE is mathematically unreachable at both early looks anyway. The joint requirements imply impossible BC means:

n=96  required BC mean > 1.2069
n=192 required BC mean > 1.0584

so the only early savings currently come from FAIL/CEILING—the exact branches vulnerable to the estimand mismatch.

Attack I — transport and cost

The call arithmetic above is exact.

The per-call route reliability gate is not.

At the terminal missingness ceiling:

allowed missing-pair fraction = 7/384
                              ≈ 0.0182292

A dependence-safe six-node union-bound requirement would be approximately:

p_call <= (7/384)/6
       ≈ 0.00303819

The inference contract only says:

upper 95 percent confidence bound...

with no method or sidedness.

For 0 failures in 1,000:

one-sided exact 95% upper:
0.00299125   → PASS

two-sided 95% Clopper-Pearson upper:
0.00368208   → FAIL

Same observations; opposite route decision.

The route/routing controls themselves are well motivated. OpenRouter currently allows fallbacks by default, load-balances absent explicit provider ordering, and allows exact provider-endpoint targeting plus fallbacks disabled. 
OpenRouter
+1
 Its caching layer and provider-sticky prompt caching are also separate behaviors that can alter execution and cost. 
OpenRouter
+1
 Router metadata can expose provider attempts and pipeline transformations, but not every failure path produces it. 
OpenRouter

The zero-paid soak is endpoint-dependent. OpenRouter does provide zero-completion insurance for certain zero-output/error responses, but that does not turn 1,000 successful target-model calls into a universally free reliability study. 
OpenRouter

So no dollar ceiling can be finalized yet—which is acceptable—but r7 must not promise a target-route no-paid soak until the chosen endpoint demonstrates such a primitive.

Attack J — fourteen red witnesses
Witness	Old bypass	r7 closure	Fresh alternative attack	Status
CROSS_SCOPE_IDEMPOTENCY	same key collided across scopes	scope included in identity	vary unconstrained semantic_operation inside same scope	EXECUTED — bypass remains
UNSAFE_INTEGER_ALIAS	>2^53 numeric alias	SafeInteger / decimal-string rule	arbitrary nested packet fields/payloads lack numeric schema	EXECUTED — partial closure
ACT_COMPLETION_ID_SUBSTITUTION	ACT ID mistaken for completion ID	state supplies canonical completion_action_id	pre-state vs provisional multi-action legality diverges	EXECUTED — old fixed, new bypass
INVALID_PROPOSAL_PATH_DIVERGENCE	invalid proposal could follow two paths	writer says reject once	schema admits ABSTAIN+action and PROPOSE+zero-action	EXECUTED — new bypass
UNJOURNALED_A0_A1	only B response durably captured	all A0/B/A1 journaled	post-provider-acceptance/pre-journal crash remains ambiguous	READ-ONLY — new bypass
MULTI_GOLD_GUESSING	paid cut has several targets	exactly-one-gold eligibility	multiple eligible cuts/scenario make cohort selector ambiguous	EXECUTED — old fixed
RENDER_ID_LEAKAGE	IDs reveal target	permutation + discriminator	nested fields may literally carry gold/reasoning; permutation algorithm not frozen	EXECUTED
CONFIG_PRECOMPUTED_PACKET	packet injected through config	closed config forbids field	precomputed lookup can live in allowed candidate implementation	READ-ONLY — bypass
COUNTER_SPLIT	split work across counters	closed catalog + unit totals	unregistered CPU work needs no split at all	EXECUTED — bypass
HD_INTERACTION	high-H/high-D joint cost	added high-edge crosses	interior (10000,64) interaction is never sampled	EXECUTED — bypass
IMPOSSIBLE_OC_CELL	invalid Cartesian probabilities	nine explicit valid cells	cells are valid; simulation RNG/mode mechanics remain unstated	EXECUTED — old bypass closed
MISSING_OM_BRANCH_FLIP	delta-only completion ignored OM	joint {00,01,10,11}^m completion	early prefix inference still targets wrong population	EXECUTED — old fixed, new bypass
PERIODIC_INDEX_AMBIGUITY	“every tenth” indexing ambiguous	zero-based positions frozen	SHA256 fixture permutation is still not algorithmically specified	READ-ONLY — old fixed
INFERENCE_IMPLEMENTATION_MISMATCH	library/transcription could drift	dependency-free formula + vectors	correct formula can faithfully estimate the wrong prefix estimand	EXECUTED — old fixed, design bypass

Bottom line: several old witnesses are now truly closed, but the current bundle test is not evidence that the witness inputs themselves go red. Its static green should remain a bundle-presence check only.

9. WHAT WOULD YOU BUILD?

I would keep the MBCX-01 architecture and recut Stage 0, not invent another memory subsystem.

The repaired instrument would contain:

Executable EventTransitionV2 table
Every one of the 17 event types gets exact payload schema, guard, prior state, state effect, journal effect, semantic-operation constant, illegal result, and idempotency behavior.

Closed packet family

DecisionPacketV2

A0ResultV2

TaskPacketV2

WorkerHandoffV2

A1ResultV2

exact contract_success

exact packet_hash preimage

I would directly borrow Text2Mem's schema→typed-operation→backend-execution separation rather than keeping execution semantics in prose. 
ACL Anthology

20-cell H×D deterministic factorial at F=16.
This is tiny and removes the entire interaction-tar-pit rather than inventing ever more “important crosses.” NIST's DOE treatment is the shelf pattern. 
NIST

Compute accounting decision.
Either:

explicitly define boundedness as bounded registered storage/data work, dropping any claim about all physical work; or

instrument CPU/work primitives so an H-linear in-memory computation cannot disappear.

Unique Stage-2 scenario selector

freeze 80 unique scenario IDs/motif;

one exact hash-selected cut per scenario;

eligibility after cut selection;

first 64 unique eligible scenarios;

no duplicate scenario IDs.

Terminal-only primary inference at n=384.
Keep 96/192 for spending visibility and diagnostics. If early scientific stopping is truly valuable later, borrow a finite-population sequential method rather than stretching prefix Hoeffding bounds beyond their estimand. 
arXiv

Exact transport state machine

PREPARED

DISPATCHED

ACCEPTANCE_PROVEN / ACCEPTANCE_AMBIGUOUS

RESPONSE_RECEIVED

RESPONSE_JOURNALED

PARSED

Ambiguous post-dispatch failures are missing/no-resample unless the chosen provider offers true idempotent recovery.

Candidate-source freeze before confirmatory truth generation to close producer contamination.

10. WOULD YOU DESIGN IT DIFFERENTLY?

Yes, but only at the contract layer.

I would not alter the scientific architecture:

Stage 0 — prove instrument
Stage 1 — deterministic continuity + FD/FC/TN engineering
Stage 2 — one frozen model's conditional usability

I would keep:

the North Star;

FD/FC/TN;

exactly-one paid target;

presentation-matched BC/OM;

single writer;

transcript-free B;

process-cold A1;

Pareto engineering output;

carrier choice separated from engineering authority;

hard deterministic obligation failures;

joint missingness completion;

separate paid authorization.

What I would eliminate is the repeated pattern of normative prose that names a property without providing the executable object that owns it.

r7 is now over the hump conceptually. The next revision should get more boring, not more sophisticated.

11. Omission / bypass attack

Strong omitted comparator: NONE as a fourth semantic arm. The best addition is a deliberately unbounded raw-replay negative-control FD, which r6 already names as a control.

Legal trace with two answers: FOUND. O1 due, O2 blocked on O1, proposal [O1,O2]: pre-state validation rejects; sequential provisional validation commits both.

False bounded-continuity pass: FOUND twice.

H-linear unmetered CPU loop;

interior H×D interaction.

False bounded-continuity kill: FOUND. One bounded 65,536-byte extra page passes pages but fails byte gates.

False FD/FC/TN preference: FOUND. Candidate implementation may embed precomputed reference-derived outputs despite runtime isolation; backend page-size-dependent byte gates can also asymmetrically reject candidates.

False model/interface failure: FOUND. Binding n=96 prefix can declare MODEL_INTERFACE_FAIL while the exact full frozen manifest is terminally inconclusive.

False model/interface ceiling: FOUND. Binding n=96 prefix can declare MODEL_OR_INTERFACE_CEILING while the full manifest clears the OM floor.

New bypass not caught by fourteen named witnesses: FOUND. DecisionPacketV2.objects[].fields accepts arbitrary free text, including an explicit gold-answer statement.

One no-paid test without which I refuse implementation: run the full 20-cell H×D pathological red candidate and prove every archive/depth-linear implementation fails regardless of where the interaction occurs.

Prior-art mechanism to borrow: Text2Mem's typed operation boundary for state/action execution. 
ACL Anthology

Piece of machinery to delete: move the old confseq source pins out of the normative inference contract into provenance/reference material. r7 explicitly says they are historical comparators and the primary interval no longer depends on them.

Boundary to next experiment: MBCX-01 ends with one canonical writer and one serial A0→B→writer→A1 chain. The next experiment begins with concurrent branches/workers, shared mutable state, authority attenuation across delegation, resource contention, conductor failure/recovery, multi-model transfer, or adjudication among simultaneous proposals.

12. Sweep log
Lane	Exact search	Opened origin / decisive mechanism	Effect	Stop reason
1. Finite-population / heterogeneous sequential inference	finite population sequential confidence sequence sampling without replacement heterogeneous means Waudby-Smith Ramdas	Waudby-Smith/Ramdas finite-population CS; 2026 Shekhar/Ramdas WoR CI. 
arXiv
+1
	Decisive against using prefix mean bounds as bounds on a declared full-manifest mean.	Direct primary method found.
2. Selection / eligibility	NIST random sampling sample selection unbiased population experimental design randomization	NIST randomization/sampling guidance. 
NIST
+1
	“Unbiased” requires an actual sampling/randomization claim; hash order alone doesn't establish it.	Sufficient; r7's larger defect is byte-level selector ambiguity.
3. Physical counters / interactions	NIST design of experiments interaction effects full factorial detect interactions; SQLite page size 65536	NIST DOE interaction model; SQLite official file format. 
NIST
+1
	Supports full H×D factorial and demonstrates page-vs-byte false kill.	Fresh bypass constructed.
4. JSON/JCS/render	JSON Schema 2020-12 additionalProperties default; RFC 8785 whitespace canonical JSON	JSON Schema spec/tour; RFC 8785. 
Tour of JSON Schema
+2
JSON Schema
+2
	Confirmed nested fields is open and clarified canonical-vs-padding boundary.	Executable schema red obtained.
5. Durable journaling/replay	Temporal event history replay durable execution; Orleans at-most-once single threaded	Temporal docs; Microsoft Orleans docs. 
Temporal Docs
+2
Microsoft Learn
+2
	Confirms established durable-runtime pattern: crash/retry ambiguity must live outside agent/model semantics.	Enough to characterize r7's transport seam.
6. Memory systems / simpler controls	Filesystem-Based Memory for LLM Agents; Text2Mem; StateFuse; MemoryData	Current primary papers. 
arXiv
+3
arXiv
+3
ACL Anthology
+3
	No fourth semantic arm found; strengthens simple-file and schema-operation controls.	New hits were representational variants.
7. Provider routing/cache/structured output	OpenRouter provider routing allow_fallbacks response caching sticky routing; OpenAI pinned model versions structured outputs	Current official OpenRouter/OpenAI docs. 
OpenAI Platform
+3
OpenRouter
+3
OpenRouter
+3
	Confirms route, cache, fallback, snapshot, and schema support must be pinned later.	Endpoint itself intentionally remains unselected.
13. Residual risks and explicit non-claims

Even after the P1 repairs:

a finite H/D experiment will remain evidence over the frozen tested range, not a universal asymptotic theorem;

Stage 2 will describe one frozen model/provider/snapshot only;

a serial single-writer handoff will establish nothing about concurrent coordination;

mechanism Pareto results remain workload/backend-specific;

no result establishes a persistent mind, hidden state transfer, procedural/personality memory, or production readiness;

provider behavior can still change unless the eventual model snapshot and route are frozen—OpenAI explicitly recommends pinned model versions where prompting behavior consistency matters. 
OpenAI Platform

the render discriminator still needs the actual frozen tokenizer and actual rendered fixture bytes;

seven reconstruction witnesses remain unexecuted until candidate artifacts exist;

exact affordability remains unknown until endpoint, token envelope, route, prices, and retry semantics exist;

route metadata itself is not universally present across every error path. 
OpenRouter

14. Seat capability and lateral-seal report

Local capability: exact file reads, bounded line reads, Git-object inspection, PowerShell, bounded Python/Node, JSON parsing, native JSON Schema validation, byte/hash computation.

Web capability: current native web search/open with primary-source access.

Statistical capability: independent formula/arithmetic implementation; exhaustive small discrete enumeration; no specialist package required.

Execution caveat: one harmless Python joint-completion probe was blocked pre-dispatch by the ChatGPT/provider layer because its safety status could not be determined. I substituted a read-only PowerShell enumerator. An initial PowerShell version collided with built-in aliases; I discarded that output and reran with unambiguous function names. Only the clean rerun is reported above.

Paid inference: NONE.

Writes / repository mutation: NONE.

Persistent side effects: none to reviewed files, repository, vault, or user data. Moonwalker audit records and ordinary transient shell processes are the only operational side effects.

Cleanup: no review artifact was written, so no file cleanup was required; no persistent worker/background process was intentionally launched.

Longitudinal disclosure: prior same-browser MBCX context retained intentionally under r7.

Lateral seal: HELD. No other current r7 seat/output was consulted.

Closure condition

I would not authorize harness implementation from r7.

The minimum r8 closure set is:

make all 17 state/event transitions genuinely executable;

close the packet object's nested fields, Worker status semantics, A0/A1 output schemas, scorer, and packet-hash preimage;

define one unique Stage-2 scenario→cut selector;

close the boundedness surface with full H×D coverage and a decision on CPU work;

freeze candidate source before confirmatory truth generation;

make 96/192 non-binding or replace them with inference targeting the actual finite manifest;

freeze OC RNG/missing-association mechanics and the transport CI/budget rule;

restore a deterministic no-resample disposition for the crash-after-dispatch/before-journal window.

The key result is that the research program itself still survives. r7 is not suffering from “wrong experiment.” It is suffering from the last, annoying kind of failure before an experiment becomes trustworthy: the prose says the machine has one answer, but several of the normative seams still allow two.
