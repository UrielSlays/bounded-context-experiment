MBCX-01 r6 — GPT-5.6 Sol / ChatGPT + Moonwalker MCP Contaminated Second-Round Design Verdict
1. Top-level verdict

NO-GO(NORMATIVE HARNESS IS STILL NON-TOTAL AND THE BOUNDEDNESS/INFERENCE GATES CAN CHANGE THE PRIMARY ANSWER)

The experiment architecture is substantially right. I do not recommend replacing the three-stage design, adding a fourth semantic memory arm, merging the three causal questions, or abandoning the paired sequential screen.

The r6 bundle nevertheless fails its own closure law: if implemented literally, it still requires unstated choices that can change the answer. I found four P1 classes:

the paid B → writer action transition is not uniquely executable;

the H/D boundedness design admits an exact but jointly archive-linear candidate that passes both stated gates;

156 of the 375 required operating-characteristic cells are mathematically impossible;

missing whole pairs have a delta sensitivity rule but no corresponding OM sensitivity rule, and one missing pair can flip PROMOTE versus INCONCLUSIVE.

These are instrument defects, not evidence that the MBCX-01 hypothesis or FD/FC/TN decomposition is wrong.

2. Seat identity

Contamination disclosure first: this conversation retains prior MBCX-01 rounds. Under MBCX-01-EXPERIMENT-COUNCIL-PACKET-r6.md:25-29, this is not a sealed independent seat. I continued only as a contaminated second-round reviewer.

Model/checkpoint: GPT-5.6 Sol
Harness: ChatGPT + Moonwalker MCP + native web + GitHub connector
Report title: MBCX-01 r6 — GPT-5.6 Sol / ChatGPT + Moonwalker MCP Contaminated Second-Round Design Verdict

I did not inspect prior verdicts, council outputs, synthesis files, receipts, execution logs, restart manifests, or other prohibited review material.

Because I cannot reliably distinguish which repair ideas may resemble recommendations from earlier rounds retained in conversational residue, all recommendations below are SECOND-ROUND / NON-INDEPENDENT as to novelty. The executable witnesses reported below were produced fresh against r6.

3. Pin / byte verification

The adjudicated Git commit is exactly:

08421f49c39c8c79c14f1ad9ba1789a2a96bcf4a

Artifact	Pinned Git blob	Bytes	Lines	SHA-384	Working copy
MBCX-01-EXPERIMENT-DESIGN-r5.md	d37dad7281310974dd9b15a1ae880a6ad84e4108	29,274	484	59AB950656AF4F48A64BC0765EE913182340410A596721CC82379B6986CA56D5BB081F11B5926B07D6237D1D449EFFF1	IDENTICAL
MBCX-01-STATE-ACTION-CONTRACT-v1.json	27abf1a85f80ac942dfc98dc965b2cb3a0226cc9	14,451	214	74695406ECFCAC230AC43633DFBE71EC21FF3357ACE293D26063A2280D6B3FBD313D856A56C9BCB33EE93A5779D849B7	IDENTICAL
MBCX-01-INFERENCE-CONTRACT-v1.json	906a36438460c498c459a2fdb59704698fda4e53	6,619	112	82FC6F0A523DD7DD5E871D0800CD40EAC44B237561A8EEFB49A0D3E11A7B8DB7F693CD996F1B3F06B6ED03F15D1D6EEF	IDENTICAL

I independently ran Git object resolution, git hash-object on each working copy, byte counts, line counts, and SHA-384 over the working-copy bytes. All three working copies equal the pinned blobs.

There is a second pin layer inside the inference contract that is defective, discussed under F5: its two upstream confseq Git blob IDs do not match the actual files at the declared upstream commit even though its byte counts and SHA-384 hashes do.

4. Evidence and probes
EXECUTED

Complete byte reads of r6, r5, both normative JSON contracts, role card, and authorized Muninn ground truth.

Exact Git/working-copy/blob/SHA-384 verification.

Structural parse of all 17 event types; all have payload/guard/effect entries.

Counted required ordered event-type pairs: 289.

Independent reducer subset:

correction/restoration;

correction-cycle rejection;

dependency-cycle rejection;

immutable scope under delegation;

four simultaneous mounted due-critical obligations → four gold actions;

wrong-scope same-name obligation remains an available distractor but not gold;

raw accepted response replay uses identical recorded bytes without provider resampling.

Executed the paid-action counterexample showing ACT:S1:o1 need not equal the obligation's required completion_action_id.

Built nine independent semantic trace-family packet substitutes and canonically encoded them:
fact_current, fact_restored, conflict_visible, due_four, dependency_blocked, delegated_owner, wrong_scope_collision, handoff_replay, reopened_obligation.

Exact H/D integer-boundary arithmetic: H permits 9 additional integer charged units; D permits 0.

Executed adversarial H×D interaction candidate producing a false boundedness pass.

Independently transcribed the pinned confidence-sequence equations in pure Python.

Reproduced all five frozen reference-vector outputs.

Enumerated all 3^8 = 6,561 paired-delta support sequences through n=8; zero invalid intervals and zero running-intersection monotonicity violations.

Enumerated the complete OC parameter cross-product for joint feasibility.

Executed an explicit one-missing-pair OM threshold flip.

Exercised all scientific branch-precedence outcomes synthetically.

Derived exact primary accepted-call counts: 576 / 1,152 / 2,304 at looks 96 / 192 / 384; 768 child reconstructions at n=384.

Derived maximum 4,608 request attempts if every eventual accepted call experiences its one allowed pre-acceptance retry.

Fetched the two upstream confseq files at the exact pinned commit and independently hashed them.

READ-ONLY

The authorized Muninn ground truth was inspected. It independently contains the exact class r5 is trying to police in FC: bounded checkpoint/tail reconstruction can regress to a full walk when outstanding state exceeds checkpoint capacity. I used that as prior-art/footgun evidence, not as authority over r5.

The original commission path was attempted exactly as authorized but Moonwalker returned path denied by security policy. I did not bypass that deny through shell access.

No FD/FC/TN implementations, Stage-1 manifest, scenario generator, exact PacketV2 object schemas, or reconstruction artifacts exist in this review bundle, so actual candidate performance and the seven process-cold witnesses could not honestly be executed.

SEARCHED

All seven required prior-art lanes were searched. Deciding sources were opened rather than relying on snippets. The non-US/non-UK institutional-language requirement was covered using Chinese- and English-language Tsinghua AIR material.

UNSEARCHED

Intentionally excluded as non-load-bearing for this round:

production security hardening;

hostile actors;

licensing/IP;

FIPS/CNSA;

deployment/fleet/PR process;

cross-model generalization;

concurrent writers;

personality/affect/procedural memory;

the next multi-worker coordination experiment.

No recursive review-repository search was performed.

5. Applicability ruling

The r6 scope override is appropriate. The deciding experiment is only about:

bounded due-obligation continuity + FD/FC/TN mechanism cost/engineering behavior + one frozen model in one serial cold A0→B→writer→A1 episode.

I expressly exclude production-security doctrine, concurrent-agent correctness, cross-model transfer, commercial considerations, cryptographic compliance, deployment architecture, and broader memory psychology.

StateFuse is relevant prior art for immutable/conflict-preserving state, but its replicated CRDT/multi-writer machinery is outside this experiment's single-writer scope and does not justify a fourth primary comparator. 
arXiv

6. Claim scoreboard C1–C12
Claim	Ruling	Reason
C1 — original North Star preserved	FALSE	TN may correctly earn nothing while FD/FC survives, but the stated “passes H and D” continuity rule can false-pass a jointly H×D-unbounded candidate.
C2 — state/action total and executable	FALSE	ACT_ON_OBLIGATION is not normatively mapped onto complete_obligation; commit atomicity/event construction is unspecified; worker_handoff_v1 conflicts with prose WorkerHandoffV2.
C3 — hard obligation gates appropriate and executable	FALSE	The gates themselves are appropriate, but duplicate-effect/legal-transition execution cannot be total while the commit action semantics are undefined.
C4 — FD/FC/TN complete mechanism comparison	HOLDS	No semantically distinct fourth arm found in the single-writer scope. Hierarchical/checkpoint designs are FC strategies; typed conflict state is TN or derivable; raw replay is an FD implementation/control, not another semantics.
C5 — parity/dedup prevents fake mechanism effect	HOLDS	If the candidate outputs are truly byte-identical, sharing one stochastic call prevents storage choice from masquerading as model behavior. The render-confound literature strongly supports this control. 
arXiv

C6 — H/D/F physical counters make boundedness falsifiable	FALSE	Marginal H and D slices miss H×D interaction growth. Executed false-pass witness below.
C7 — cold serial handoff isolates selective continuity	FALSE	Transcript isolation is strong, but B→writer effect semantics are not uniquely executable.
C8 — paid action/scoring unit exact	FALSE	A0/B targets are enumerable, but the writer cannot deterministically translate the committed ACT into the required ordinary completion transition.
C9 — mechanism recommendation/carrier selection fair	HOLDS	Worst-cell p95 + Pareto result + separately labelled carrier rule correctly separates engineering conclusions from carrier choice, conditional on repairing candidate eligibility/boundedness.
C10 — inference coherent and executable	FALSE	Impossible OC cells, undefined OM missingness, wrong blob pins, and underdefined vector inputs.
C11 — isolation/reconstruction/transport/cost cannot choose answer	FALSE	Transport missingness can currently choose the OM-floor result because OM completion is undefined. Provider freeze is also necessarily a later Gate-5 condition.
C12 — r5 smallest decisive instrument	UNDERDETERMINED	I found no removable stage or missing semantic arm, but “smallest” is not established while the OC grid contains impossible cells and actual candidate/reconstruction machinery does not yet exist.
7. Finding table
Sev	Finding	Exact location	False-result mechanism	Smallest repair	Evidence
P1	F1 — B→writer action algebra is non-total	State contract :94-98, :129-138, :154-179; design :191-196, :344-349	ACT:{scope}:{obligation} does not define the completion_action_id required by complete_obligation; implementers can construct different effects/A1 states. Normative payload also says worker_handoff_v1 while design requires V2.	SECOND-ROUND / NON-INDEPENDENT: freeze WorkerHandoffV2; define typed action-executor mapping and exact child-event/journal semantics.	EXECUTED
P1	F2 — H×D interaction can false-pass bounded continuity	Design :213-242, :291-308	Candidate can be constant on H at D=16 and constant on D at H=1024 yet grow linearly only when H and D are both high.	Cross H at D=256 and D at H=100000, applying the same deterministic counter gate; preferably cross the full H×D grid at F=16.	EXECUTED
P1	F3 — OC grid contains impossible probability cells	Inference :70-86, Gate5 :104-110	52/125 structural cells imply negative joint BC/OM probabilities; with missingness levels, 156/375 mandated cells cannot be generated.	Replace Cartesian declaration with pre-enumerated feasible joint cells or normative feasibility filter + frozen resultant manifest.	EXECUTED
P1	F4 — whole-pair missingness leaves OM floor undefined	Inference :53-68	Missing pair removes both delta and OM, but only delta gets ±1 sensitivity. One missing OM can move its CS lower bound across 0.80 while delta remains invariant, flipping PROMOTE/INCONCLUSIVE.	Perform joint feasible completion sensitivity over BC/OM and require branch invariance; otherwise TRANSPORT_INCONCLUSIVE.	EXECUTED
P2	F5 — upstream Git blob pins are wrong	Inference :14-31	The bundle cannot satisfy all normative source pins simultaneously; implementer must decide which pin wins.	Correct both blob IDs and automate commit→path→blob→bytes→SHA384 verification.	EXECUTED + SEARCHED
P2	F6 — reference-vector inputs are not actually frozen	Inference :94-100	“Every tenth” outputs only reproduce under zero-based placement; ordinary one-based placement produces different values. Expected outputs are pinned, source arrays are not.	Freeze exact arrays, generator pseudocode with indexing convention, or array SHA-384s.	EXECUTED

For F5, the actual upstream blobs at the pinned commit are:

predmix.py → f7c3b4bf17411596d1434e3330796f3e8c8ff884, not da800273….

betting_strategies.py → 89f433fd24274e7c74d7d93fe054399fb87cfaca, not 7596cfc6….

The contract's byte counts and SHA-384s do match the actual files; this is a Git-object identity defect, not evidence that the mathematical source content is wrong.

No P0 found.

8. Attacks A–H
Attack A — estimand and program-decision trace

Input: four requested worlds.

Method: independently walked the Stage-1/Stage-2 decision rules.

Output:

World	Result
TN useless, FD succeeds and is bounded	Continuity survives; FD may be recommended; TN need not win
Every candidate H-linear	Bounded continuity falsified
FD H-bounded but D-linear, alternatives also fail D	Bounded continuity falsified
Deterministic stage passes, OM upper < .80	Continuity survives mechanically; Stage 2 returns MODEL_OR_INTERFACE_CEILING

Interpretation: the design correctly separates continuity, mechanism choice, and conditional model usability.

Limitation: the original commission could not be byte-read because its authorized path was denied by Moonwalker policy.

Attack B — normative state/action contract

Input: normative state/action JSON.

Method: parsed all 17 event classes, enumerated 289 ordered type-pairs structurally, and independently implemented the unambiguous reducer subset.

Executed greens:

CORRECTION_RESTORE_CURRENT = f2
CORRECTION_CYCLE = REJECT
DEPENDENCY_CYCLE = REJECT
DELEGATION_SCOPE_UNCHANGED = true
GOLD_COUNT = 4
WRONG_SCOPE_DISTRACTOR_AVAILABLE = true
WRONG_SCOPE_DISTRACTOR_GOLD = false
RAW_RESPONSE_REPLAY_BYTE_EQUAL = true

The red witness:

COMMIT_ACTION_ID                 ACT:S1:o1
ORDINARY_COMPLETE_REQUIRES      COMPLETE:S1:o1
EQUAL                            false
ACTION_EXECUTOR_MAPPING_PRESENT false

There is no normative instruction saying whether the writer passes the ACT ID as the completion ID, synthesizes the stored completion ID, appends a distinct complete_obligation event, or mutates the obligation inside the commit event.

Also, propose_handoff_result literally requires worker_handoff_v1 at state-contract lines 129–131 while the governing prose says WorkerHandoffV2.

Interpretation: the algebra is mostly well-shaped but not total.

Limitation: I refused to “complete” all 289 dynamic pair fixtures by silently choosing the missing writer semantics. That would manufacture the answer the attack is supposed to test.

Attack C — FD / FC / TN comparison

Input: nine trace families.

Method: because candidate implementations and exact per-object schemas are not in the bundle, I built the smallest honest substitute: nine semantic DecisionPacketV2-shaped records using only the declared neutral outer contract and canonically serialized each.

All nine produced a single semantic byte representation that FD, FC, and TN can in principle emit:

fact_current
fact_restored
conflict_visible
due_four
dependency_blocked
delegated_owner
wrong_scope_collision
handoff_replay
reopened_obligation

No public semantic object was found that requires TN. StateFuse's explicit conflict machinery is valuable in replicated/multi-writer systems, but conflict can be represented as a derived packet object under FD/FC in the frozen single-writer experiment. 
arXiv

MemoryData and current system-characterization work likewise find that memory designs trade work between representation, maintenance, retrieval, and construction rather than one architecture universally dominating. 
arXiv
+1

Strong fourth comparator: NONE as a semantic arm.

A raw-full-replay implementation would be a useful negative-control FD, not a fourth mechanism.

FC's snapshot/tail class is legitimate. PostgreSQL's mature WAL/checkpoint model independently shows why snapshot/checkpoint + replay-tail is standard practice and why ceilings need explicit overflow behavior: WAL/recovery work starts from checkpoints, and even nominal WAL size limits can be exceeded under stated conditions. 
PostgreSQL
+1

Limitation: no FD/FC/TN code exists in the authorized bundle, so actual snapshot overflow, PAGE_FAULT, false-empty-array, and packet parity cannot yet be executed.

Attack D — boundedness and physical-work accounting

Integer edges executed:

H range = 100000 - 128 = 99872
floor(99872 × 0.0001) = 9 charged units

D range = 256 - 1 = 255
floor(255 × 0.0001) = 0 charged units

Those stated bounds are correct.

Then I attacked the factorization. Synthetic exact candidate:

reads(H,D) =
    10,                         normally
    H,  if D == 256 and H > 1024

Results:

H slice at D=16:
10, 10, 10, 10
normalized_range = 0.0       PASS

D slice at H=1024:
10, 10, 10, 10, 10
normalized_range = 0.0       PASS

combined H=100000,D=256:
100000 reads                  exactness may still PASS

H slice at D=256:
10, 10, 10000, 100000
normalized_range ≈ 1.00118   catastrophic FAIL if tested

Interpretation: separate marginal slices do not establish joint boundedness. The one combined corner measures an expensive point but has no hard comparison that declares the interaction itself a boundedness failure.

Bazel's Skyframe independently supports the lower-level accounting rule: a read that enters computation without registration is an undeclared dependency capable of making incremental results incorrect. 
Bazel Documentation

Limitation: synthetic candidate, deliberately. That is appropriate here: its purpose is to prove the test admits a false pass by construction.

Attack E — presentation and A→B→A

Input: declared BC/OM render requirements and paid handoff path.

Method: byte-read packet/render rules, action ordering, handoff contracts, and replay path.

The architecture correctly requires matching outer keys, descriptions, instructions, action order, output schema, token envelope, padding, serialization, and transport. Render matching is not cosmetic: recent controlled work found that apparent structured-memory benefits can largely disappear once mechanism and presentation are separated. 
arXiv

The A→B→writer→A1 path nevertheless stops at F1: B's output type is version-inconsistent and the writer's ACT execution is undefined.

Smuggling reasoning: zero-free-text caps are a strong control. I found no declared free-text field.

Residual false-positive story: public semantic IDs are not explicitly required to be generator-independent of critical/due/gold class. If IDs encode generator structure, both BC and OM can exploit the leak and make model usability look easier than the semantics actually are. Before paid Stage 2 I would require an ID-permutation/equivariance or ID-only-predictor red test.

Limitation: no paid model call was permitted; exact final PacketV2/HandoffV2 schema artifacts do not yet exist, so a real render classifier was not executable.

Attack F — producer taint and artifact causality

The isolation design is strong: candidate child receives public journal/payloads, normative schema, implementation, governed dependency API, output/config only; generator/reference/gold/network/ambient source are prohibited.

The seven reconstruction witnesses are also well selected.

I could not execute them because there is no candidate implementation or artifact to reconstruct. Inventing one would test my substitute rather than r5.

The authorized Muninn ground truth does reinforce why witness 7 and clean rebuild matter: its existing checkpoint machinery documents an explicit residual where checkpoint capacity can be exceeded and restart then falls back to a full walk. That is precisely the class r5 says FC must expose instead of hiding.

Interpretation: READ-ONLY pass on architecture, no executable candidate evidence.

Limitation: actual Gate 2/3 causality remains unproven until candidate bytes exist.

Attack G — exact inference

This lane produced the most reds.

Upstream source

The content itself is reproducible. The actual confseq files at the frozen commit have the contract's exact byte counts and SHA-384s; their declared Git blob IDs are wrong.

Reference vectors

Independent pure-Python transcription exactly reproduced:

delta_all_zero n384:
[-0.046149098227, +0.046149098227]

delta_every_tenth_minus_one n384:
[-0.165202165789, -0.035340633611]

delta_every_tenth_plus_one n384:
[+0.035340633611, +0.165202165789]

OM 90% n384:
[0.838513500163, 0.958131809402]

OM 80% n384:
[0.717732759517, 0.878808235770]

But the latter four match only when the periodic perturbation begins at array index 0. One-based positions 10,20,… produce different numbers. Thus the expected result is frozen but its input is not.

Small exact support

All 6,561 sequences in {-1,0,+1}^8 produced finite, ordered intervals inside support and monotonic running intersections.

That is a useful green for the independent mathematical transcription.

Time-uniform confidence sequences are an appropriate family for preregistered sequential looks: Waudby-Smith and Ramdas explicitly construct time-uniform bounds for bounded means using betting/martingale methods. 
arXiv

Full grid feasibility

For binary (BC, OM) define:

d = E[BC - OM]          = p10 - p01
r = P(BC != OM)         = p10 + p01
q = P(OM = 1)           = p01 + p11

Therefore:

p10 = (r + d)/2
p01 = (r - d)/2
p11 = q - p01
p00 = 1 - q - p10

Executed over the exact specified Cartesian grid:

structural cells:     125
feasible:              73
impossible:            52

with 3 missing levels:
specified:            375
impossible:           156

Example:

d = -0.25
r = 0.02
q = 0.70

p10 = -0.115   IMPOSSIBLE

So Gate 5 cannot “simulate every specified grid cell.”

Missingness attack

One whole pair missing. Keep the 383 observed delta values at zero so either delta completion remains comfortably above the -0.10 noninferiority margin:

missing delta = -1 → lower -0.049076347065
missing delta = +1 → lower -0.045879963529

For the corresponding OM sequence with 333 observed successes:

missing OM = failure:
OM lower = 0.798975030093

missing OM = success:
OM lower = 0.802607690682

That crosses the exact 0.80 oracle floor.

So the same observed experiment can become:

INCONCLUSIVE

or

PROMOTE_TO_COORDINATION_STAGE

depending on an OM missing-value choice the contract never defines.

This is not exotic statistical nitpicking. FDA guidance for binary missing endpoints explicitly uses sensitivity analyses that vary missing outcomes as successes and failures; the r6 delta-only worst-case treatment omits the corresponding OM dimension. 
fda.gov
+1

Branch precedence

Synthetic fixtures independently fired:

PROMOTE_TO_COORDINATION_STAGE
MODEL_INTERFACE_FAIL
MODEL_OR_INTERFACE_CEILING
INCONCLUSIVE_OR_UNDERFUNDED
DESIGN_OR_IMPLEMENTATION_FAIL
TRANSPORT_INCONCLUSIVE

and 8 missing pairs correctly triggers the hard transport ceiling.

Interpretation: the basic sequential-test mathematics and branch taxonomy are sound. The preregistered input domain and missing-data contract are not.

Limitation: the full 10,000-replicate OC study was not run because 156 mandated cells have no probability distribution to sample from. Running a silently filtered grid would have violated the attack.

Attack H — exact DAG, cost, and transport

The call DAG arithmetic reproduces exactly:

n=96:
96 × 2 conditions × 3 calls = 576 accepted calls

n=192:
1,152 accepted calls

n=384:
2,304 accepted calls

cold child reconstructions at n=384:
384 × 2 = 768

With one allowed pre-acceptance retry per node, if every first attempt fails pre-acceptance and every second attempt succeeds:

maximum attempts = 2,304 × 2 = 4,608

Crash windows separate correctly in the design:

accepted response successfully journaled → replay bytes, no resample;

response accepted but process dies before journaling → pair missing;

pre-acceptance failure → one retry allowed.

No endpoint or price was specified, and r5 explicitly withholds that until owner authorization. I therefore did not invent dollar figures.

Generic cost sensitivity is simply:

accepted_cost =
Σ (input_tokens_i × input_price
 + output_tokens_i × output_price)

plus any endpoint-specific billable failed attempts

Current provider/router documentation demonstrates why r5's later transport freeze is necessary. OpenAI recommends pinned model versions because behavior can change between snapshots. 
OpenAI Platform
 OpenRouter load-balances by default and defaults allow_fallbacks to true, but allows a specific provider plus fallbacks disabled and can require support for all request parameters. 
OpenRouter

OpenRouter response caching is off when neither request nor preset enables it, can be explicitly disabled per request, and is separate from provider prompt caching. 
OpenRouter
 Its route-metadata facility can expose provider attempts and intervening pipeline stages, which is useful for the proposed route witness. 
OpenRouter

Interpretation: the no-paid call DAG is exact. A provider-specific execution contract cannot be adjudicated until Gate 5 names the provider/endpoint/model snapshot; that deferral is appropriate.

9. WHAT WOULD YOU BUILD?

SECOND-ROUND / NON-INDEPENDENT recommendation.

I would keep FD, FC, and TN and build only Stage 0 first, with four repaired machine-readable components:

Action executor contract. A typed operation table mapping every public action ID to one exact event invocation, payload derivation, event ordering, journal assignment, atomicity, and idempotency behavior. Freeze TaskPacketV2 and WorkerHandoffV2 at the same time.

Crossed boundedness harness. H and D marginal twins plus high-edge cross-tests. Include a deliberately pathological full-replay/red candidate and the H×D interaction witness above; both must go red.

Inference verifier. Correct upstream object pins, exact reference-vector input bytes, feasible joint-distribution OC manifest, and branch-invariant joint missingness enumeration.

Only after 1–3 are green, implement FD/FC/TN behind the same dependency-read API and run the reconstruction/taint gates.

I would not build a paid model harness yet.

Text2Mem is the strongest direct prior-art pattern to borrow for item 1: it turns instructions into schema-based contracts with explicit semantic invariants, parses them into typed operations, and separates the contract from backend execution. 
ACL Anthology

That is almost exactly the missing architectural seam in r6.

10. WOULD YOU DESIGN IT DIFFERENTLY?

SECOND-ROUND / NON-INDEPENDENT recommendation.

At the top level, barely.

I would preserve:

Stage 0 — prove the instrument
Stage 1 — test continuity/mechanism boundedness
Stage 2 — conditionally test one frozen model/interface

I would preserve FD / FC / TN.

I would preserve the semantic packet parity, cold A→B→A episode, no-transcript handoff, exact mechanical scoring, writer isolation, registered physical reads, Pareto engineering result, and separate carrier decision.

The differences would be in the contracts:

EventReducerSpec
ActionExecutorSpec
DecisionPacketV2Schema
TaskPacketV2Schema
WorkerHandoffV2Schema
InferenceSpec

All six should be executable data, not partly prose.

And I would design boundedness as a factorial adversarial test, not two marginal slopes plus one corner:

H × D at fixed F

at least on the edge strata necessary to detect interactions.

The outside literature does not make me want a fancier mechanism. It makes me want a more boring executable contract.

11. Omission attack

Strong simple comparator omitted: NONE as a primary semantic arm. A raw/full-replay implementation should be added only as a deliberately unbounded red-control FD, not promoted to a fourth mechanism.

Legal state/action trace with two possible answers: FOUND. commit_handoff_result(committed_action_ids=["ACT:S1:o1"]) can either use that action ID as the completion payload or synthesize the obligation's distinct completion_action_id; the contract does not choose, and the resulting ordinary event/journal semantics are also unspecified.

Hidden confound capable of falsely passing bounded continuity: FOUND — H×D interaction.

Hidden confound capable of falsely favoring FD/FC/TN: no fourth-mechanism presentation confound found. Candidate eligibility can nevertheless be corrupted by the H×D gate, which can place an actually unbounded candidate on the engineering Pareto set.

Persuasive false-positive model-usability story: public semantic/action IDs encode generator regularities correlated with gold. Both BC and OM exploit IDs rather than state semantics, OM clears 0.80, delta is noninferior, and the experiment “promotes.” Require opaque generator-independent IDs or an ID permutation/equivariance test.

Persuasive false-kill story: use a provider alias/router whose underlying snapshot/provider changes across calls. A changed model/interface fails the structured BC packet while OM remains easier, creating MODEL_INTERFACE_FAIL for something that was not the frozen model. Current provider documentation confirms snapshot/routing variability is real; r5's later hard route/model freeze must therefore mean an immutable snapshot/endpoint rather than merely a friendly alias. 
OpenAI Platform
+1

Uncaught statistical/transport footgun: missing OM outcome treatment.

No-paid test without which I refuse Stage 2: the H×D interaction red witness must fail mechanically after the repair. If the exact synthetic candidate above can still pass, the experiment cannot claim bounded continuity.

Prior-art mechanism to borrow directly: Text2Mem's typed schema-contract → validated operation object → backend executor separation. 
ACL Anthology

Machinery to delete: delete the unconstrained Cartesian OC-grid generator. Keep the OC stage and same scientific coordinates, but preregister a frozen list of feasible joint distributions instead.

Exact MBCX-01 boundary: ends after one single-writer state system, one mechanism selected from FD/FC/TN, and one frozen model executing one serial cold A0→B→writer→A1 episode. The next experiment begins when multiple workers/conductors share mutable state, delegate authority across branches, contend on resources, run concurrently, recover conductor failure, or require cross-model coordination.

12. Sweep log
Lane	Exact query / origin	Deciding mechanism	Effect on r6	Stop reason
1. Module/stage diagnosis	site:arxiv.org MemoryData agent-native memory system evaluation representation storage extraction retrieval maintenance 2026; MemoryData; MemEval	Memory decomposes into storage/representation, extraction, retrieval/routing, maintenance; fair evaluation should normalize LLM/embedding/scoring and account for costs. 
arXiv
+1
	Supports separating deterministic mechanism evaluation from model use/cost.	New hits repeated same decomposition.
2. Mechanism/render	site:arxiv.org "Presentation, Not Mechanism" memory agent render matched controls; StateFuse	Render matching is essential; coarse retained state can outperform richer typing after presentation is held fixed. StateFuse's special CRDT value is conflict preservation under replication. 
arXiv
+1
	Supports C4/C5; no fourth single-writer mechanism.	New systems folded into FD/FC/TN representation strategies.
3. Obligations/durable identity	site:learn.microsoft.com Orleans virtual actors durable identity always addressable persistent state; site:docs.temporal.io "Event History" replay workflow durable execution; PM-Bench	Durable entities have stable identity and serial state operations; durable workflows resume after failure; prospective memory explicitly tests deferred intention at future state/cue. 
Microsoft Learn
+2
Temporal Docs
+2
	Supports obligation identity, writer serialization, record/replay, and deferred-action motifs.	No missing state-machine religion found.
4. Selective handoff	site:arxiv.org "Shared Selective Persistent Memory" LLM agents selective memory transcript	Selective persistence keeps reusable task/schema/tool/output constraints while discarding session reasoning; full-history persistence can be harmful. 
arXiv
	Supports capped typed transcript-free B handoff.	Additional blackboard/shared-memory results were broader than this serial lane.
5. Boundedness	site:bazel.build Skyframe dependency graph unregistered reads correctness incremental build; PostgreSQL WAL/checkpoint; LongMINT	Registered dependencies are necessary for correct incremental behavior; checkpoint/replay is standard but recovery/storage ceilings need explicit treatment; interference grows with updates. 
Bazel Documentation
+2
PostgreSQL
+2
	Strongly supports physical-read accounting, clean rebuild, D/H stress. Also motivated the H×D attack.	New hits changed implementation details, not the experimental dimensions.
6. Paired inference	site:arxiv.org Waudby-Smith Ramdas confidence sequences bounded means predictable plug-in empirical Bernstein; FDA binary missing-data sensitivity	Time-uniform bounded-mean CS is established; binary missing outcomes should be sensitivity-tested under success/failure alternatives. 
arXiv
+2
U.S. Food and Drug Administration
+2
	CS family survives; missing OM contract does not.	Decisive statistical defect became executable.
7. Provider/runner	site:openrouter.ai/docs provider allow_fallbacks false only provider require_parameters routing; site:platform.openai.com/docs models pinned model version snapshot consistency structured outputs strict JSON schema	Routers may load-balance/fallback unless disabled; response caches/presets exist; pinned versions are needed for model behavior consistency. 
OpenRouter
+2
OpenRouter
+2
	Confirms Gate-5 exact route/model/cache freeze is load-bearing.	Endpoint remains intentionally unselected, so provider-specific attack stops here.

National-language/institutional pair: Tsinghua AIR's Chinese material explicitly discusses feedback-derived experience being validated before entering long-term memory, and its Chinese/English institutional pages describe learnable long-range memory in MemAgent. 
Tsinghua Intelligent Industry Institute
+1
 This provided a non-US/non-UK institutional check; it added no comparator that escapes FD/FC/TN.

13. Residual risks and explicit non-claims

Even after the six findings above are repaired:

Stage-1 results will remain finite-workload evidence, not a universal asymptotic proof.

One frozen provider/model episode will say nothing about other models, snapshots, or wrappers.

A serial single-writer success will not establish concurrent/multi-writer safety.

FD/FC/TN engineering results will be workload-specific.

The experiment cannot prove production security or hostile-agent containment.

Presentation parity must still be demonstrated against the actual frozen packet bytes, not inferred from the design prose.

Producer taint and all seven reconstruction witnesses remain genuinely open until candidate artifacts exist.

Actual dollar affordability remains open until an endpoint, prices, token envelopes, and owner authorization are frozen.

Public-ID leakage should be treated as a Stage-0 blinding residual and tested before paid calls.

The inaccessible original commission means I cannot independently certify lineage wording beyond the current r6/r5 instrument.

None of those residuals requires another primary mechanism or another experiment stage.

14. Seat capability and seal report

Local capability: exact read/range read, Git object inspection, PowerShell, bounded Python/code execution, file hashing, local source inspection.

Web capability: native current web search/open plus GitHub repository-content API. Primary/official sources were preferred.

Statistical capability: no specialized statistical package was required. Moonwalker's Python environment lacked NumPy on the first attempted transcription, so I reran the mathematical checks in pure Python rather than installing or modifying anything. The reference-vector, missingness, support-enumeration, grid-feasibility, and interaction witnesses are therefore independent small executables rather than calls into confseq.

Tokenizer capability: no provider tokenizer was invoked. No paid model experiment or token-cost estimate requiring a selected endpoint was authorized.

Paid inference: NONE.

Filesystem side effects: NONE to user artifacts. No bundle/repository/vault file was edited, created, deleted, committed, or moved.

Execution side effects: transient local shell/code processes, normal Moonwalker audit records, read-only network GETs, and web searches. No harness was implemented. No persistent worker/background process was left running.

Cleanup: no generated review artifact or changed repository state existed to clean up.

Repository seal discipline: exact paths/Git objects only; no recursive review-repository listing/search; no prohibited prior verdict/synthesis/receipt/execution material inspected.

Sealed independence: FAILED BY PRIOR CONVERSATION CONTAMINATION, DISCLOSED. This is a second-round review only, not an independent council seat.

Final closure condition

I would not authorize harness implementation from r6 until all four P1s are repaired and red-witnessed:

1. one exact WorkerHandoffV2 + ACT→event executor contract;
2. H×D interaction gate;
3. feasible frozen OC cell manifest;
4. joint BC/OM missingness branch-invariance rule.

Then fix the two P2 reproducibility pins, rerun the no-paid Stage-0 oracle attacks, and send the repaired bundle to a genuinely fresh sealed seat.

The important result from this round is that I do not think you need to redesign MBCX-01 from scratch. The machine's architecture is basically there. The remaining failures are exactly where a scientific instrument has to be boringly literal: what action executes, which workload cells exist, what “bounded” means jointly, and what a missing observation means.
