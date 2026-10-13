1. Top-level verdict

GO-WITH-FIXES(COMPARATOR-PARITY)

READ-ONLY verdict. No paid inference was run. No MBCX file was edited.

Revision 1 is a substantial scientific improvement. The r0 writer-quality confound is genuinely removed: L and T are now deterministically maintained, both use the same decision model, both have action-side output instead of a model-rewritten memory artifact, run order is counterbalanced, reconstruction is genuinely process-cold, and provider variance is correctly removed rather than studied.

I would not send r1 to paid pilot exactly as written, though. The remaining defects are experiment-validity defects, not production ceremony. The most important is that r1 has created a strong flat store, but it has not yet specified a correspondingly strong flat materializer. T gets current-scope, due/near-due and relevant-closure selection; L merely says it serializes its current facts and open obligations. My executed fixture produces a perfectly plausible case in which L crosses the 6,000-token budget while a simple scope/due-filtered L using fields it already stores stays around 1,000 tokens and T also stays under 1,000. That could manufacture a persuasive T win.

There are three additional pre-pilot fixes: define the exact high_stress_set_f1 computation and empty-set convention; define actual workload maxima so “maximum-load” is a real test rather than an implementer choice; and preregister the exact conservative pilot-variance/sample-size procedure. Those are bounded fixes. They do not require rethinking Stage A.

2. Pin / byte verification

EXECUTED — PASS.

Reviewed artifact:

MBCX-01-EXPERIMENT-DESIGN-r1.md@7fa45e092bb7db14d85761f65a63b97a3740c65e

I independently verified:

Item	Verified value
Commit	7fa45e092bb7db14d85761f65a63b97a3740c65e
r1 design Git blob	2c3c12b839b8fc356feb63cd05f050884c46482f
source-manifest Git blob	b71f8b64a2000acd554bd09c7a88320172025db3
r1 SHA-384	8D8F7B083B32C5CC4B9F682C29D759967D3A71CD4B452DEE96EEC06785189A89A42B1FC95BB864B1D574117BE4729E32
r1 byte size	27,182
r1 line count	542

The working copies of both r1 and LOCAL-SOURCE-MANIFEST-r1.md hash to the same Git blobs as the pinned commit, so the working bytes and committed bytes are identical.

I also independently re-hashed all seven scientific sources named by the manifest. Every SHA-384 matched exactly.

I did not open, search, or use any prior-seat verdict file or operational receipt.

3. Evidence actually read and probes actually run
Pinned/local evidence read

I read all 542 lines of the pinned r1 design, the full r2 packet, the pinned local source manifest, and the load-bearing local research sections required by that manifest. Particularly important were:

DECISIVE-EXPERIMENT-PORTFOLIO...md:24-36,128-198,536-548 — strongest-simple baselines, bounded-sufficiency kill shot, pairing/counterbalancing.

CAPABILITY-NORMALIZED...R04.md:119-145,247-275,308-351 — matched budgets, strong baselines, mechanical validators, paired/clustered inference.

CANTOR...EXPERIMENTS...md:25-54,75-84,140-168,178-220 — missing-instrument problem, obligations/non-recall, oracle boundary, retrieval-policy confounds.

External evidence opened independently

No opened work answered the exact Stage-A contrast.

PM-Bench confirms prospective memory is already a real controlled evaluation target and provides a strong experimental precedent, but it compares agent configurations rather than r1's deterministic-flat versus deterministic-typed representation contrast. 
arXiv

AgenticSTS is very close architecturally: bounded named memory layers and fresh decision prompts. Its own repository explicitly treats a matched accumulating-context comparison as an open controlled follow-up, so it does not make MBCX obsolete. 
GitHub
+1

StateFuse is the most useful new comparator precedent I found. It explicitly compares conflict-preserving, flat, raw-log, provenance-style, and collapsed memories under matched resolver and verification policies. Its conflict-bearing benchmark tied on top-line answer accuracy while conflict-preserving representation improved contradiction visibility, abstention, and correction behavior. That is exactly the scientific discipline MBCX needs: don't let the fancy representation also receive a better resolver. 
arXiv

LongHorizon-Harness externalizes task state and uses interchangeable harness/model adapters, but its state manager changes more than r1 intends Stage A to change. It supplies implementation patterns, not the answer. 
arXiv

CAME-Bench/STITCH shows that structured intent-based selection can itself produce large gains by suppressing context-incompatible history. That makes selection policy a particularly dangerous hidden treatment in L-vs-T. 
ACL Anthology

Mem2ActBench moves beyond passive memory QA into memory-grounded action/tool use, making it useful downstream external-validity evidence, but it does not isolate r1's representation question. 
ACL Anthology
 LongMemEval-V2 similarly tests much broader accumulated experience over up to 500 trajectories/115M-token histories and is not the same causal contrast. 
GitHub

The worldwide sweep also included AgeMem from Wuhan University and Alibaba Group. It learns memory operations as part of the agent policy, making it useful evidence for a later controller/writer stage rather than Stage A, where such extra control computation is intentionally removed. 
arXiv

Executed no-cost probes

EXECUTED — tokenizer/payload attack. I found an already-cached Llama-3 8B Instruct Hugging Face tokenizer and used it locally with the installed tokenizers runtime. This is a proxy tokenizer, not the eventual Stage-A tokenizer; Gate 0 must repeat against the exact frozen model tokenizer.

For generic rich fixtures:

24 rows:   L = 1,525 tokens   T = 4,155
60 rows:   L = 3,778 tokens   T = 10,419
120 rows:  L = 7,543 tokens   T = 20,859
common output fixture = 396 tokens

More importantly, I constructed a three-scope current-decision fixture. L-as-written serialized all flat current/open rows; a stronger flat L applied only cheap scope/due filters using information L already stores; T emitted its scoped working packet:

rows/scope   L as written   strong flat L   scoped T
24              3,819            721           858
30              4,773            829           858
36              5,727            937           858
40              6,363          1,009           858

At 40 rows/scope, L-as-written exceeds the 6,000-token budget while strong-flat L and T both fit easily. That is my executed bypass of C2/C3.

EXECUTED — metric granularity attack. For ordinary pooled set-F1, one single FN from a perfect result changes score by:

6 due positives   -> 0.0909
8                 -> 0.0667
10                -> 0.0526
15                -> 0.0345
24                -> 0.0213

One FP at six positives costs 0.0769.

Alternatively, if the intended metric is macro over 30 binary decision opportunities, one full decision flip is 1/30 = 0.0333, two are 0.0667, three are 0.1000.

And a correct no-action opportunity yields TP=FP=FN=0, so ordinary F1 has a zero denominator unless the scorer defines whether that case is 1, 0, or excluded.

Thus r1's statement that +0.08 necessarily means multiple changed decisions is not mechanically established until the aggregation and opportunity composition are pinned.

EXECUTED — pilot/sample-size attack. I simulated three bounded paired-delta distributions with true mean approximately +0.08, then estimated power for a paired bootstrap CI excluding zero:

                 SD       n=48   n=72   n=96   n=128
smooth           .120      .998   1.000   1.000   1.000
lumpy /30        .071     1.000   1.000   1.000   1.000
rare-tail        .291      .581    .699    .786    .884

The bounded rare-tail witness was 90% +0.08, 5% +1.00, 5% -0.84. A 12-pair pilot has about a 28.2% probability of seeing none of the rare tails at all. In that event an empirical resampling procedure sees zero pilot variance and falls to r1's 48-scenario minimum even though 48 has only about 58% power in the simulated underlying distribution.

That doesn't prove r1 needs hundreds of scenarios. It proves that the words “conservative upper uncertainty bound” need an exact preregistered method. Recent methodological work makes the same general point: small pilot/blinded samples can still lead to underpowered studies, and one response is an upper confidence limit that explicitly incorporates variance-estimation error. 
arXiv

Paired bootstrap and paired permutation are technically appropriate tools once the statistic is fixed; SciPy explicitly supports paired-index bootstrap resampling and paired sample permutations. 
SciPy Documentation
+1

4. Experiment-specific applicability ruling

The r2 override is correct and I applied it.

NOT APPLICABLE — NON-LOAD-BEARING: licensing, redistribution rights, clean-room implementation, future commercialization, FIPS/CNSA, Moonwalker seal-chain doctrine, malicious prompt injection, production authorization topology, PR workflow, generalized PID/process ownership, production sandboxing, and multi-provider generalization.

None can change the scientific answer to Stage A as presently scoped, so none appears as a finding.

Provider controls remain load-bearing only in the narrow scientific sense: the one chosen model/provider/request path must remain the same between L and T. OpenRouter's documentation confirms why r1 correctly specifies an exact endpoint slug rather than a provider family: a base slug can cover multiple endpoint variants and regions. 
OpenRouter

Likewise, this round does not estimate provider variance. One exact capable condition is sufficient. Any observable violation invalidates the cell.

5. Claim scoreboard C1–C12
Claim	Verdict	Ruling
C1 — Stage A causally identified	UNDERDETERMINED	Writer quality, model calls and old ledger-output tax are closed. But L/T packet-selection parity and the common provenance_ids demand are not yet fully neutral.
C2 — Arm L strong enough to kill T	FALSE	L stores enough metadata for a much stronger simple selector than :109 actually specifies. Executed fixture shows material consequence.
C3 — treatment-budget symmetry	FALSE	Nominal caps are equal, but “maximum load” is undefined, L can incur an avoidable serialization penalty, and the output schema asks for provenance that only T explicitly carries.
C4 — world does not privilege T	UNDERDETERMINED	r1 has the correct anti-privilege tests, but exact generator/public transition schemas and hand-authored challenges do not exist yet.
C5 — outcome useful resolution	FALSE	Exact F1 aggregation and empty-set semantics are unstated; executed arithmetic falsifies the blanket “+0.08 = multiple decisions” claim.
C6 — reconstruction measures process-cold	UNDERDETERMINED	The design names the right construct, but implementation must prove a child cannot reconstruct when the required artifact is withheld/corrupted and that the public cursor carries no hidden state.
C7 — runner experimentally neutral	HOLDS	Thin direct runner by default, Inspect only after explicit conformance, is the correct design.
C8 — exact provider condition frozen	HOLDS	r1 exact-endpoint + no-fallback/transform + direct-provider escape hatch is sufficient at design level; conformance must execute it.
C9 — order/retry identity	HOLDS	Pairing, counterbalancing, interleaving and schedule freeze appropriately address time/order. Retry ambiguity needs one tightening noted below.
C10 — statistical plan supports win/kill	UNDERDETERMINED	No max clamp is a real closure; exact conservative pilot-variance rule remains unspecified and my executed tail witness demonstrates why it matters.
C11 — oracle diagnostics honest	UNDERDETERMINED	Scope is correct, but exact oracle-minimal/all-relevant construction policy still needs executable fixtures.
C12 — instrument proportionate	HOLDS	Direct thin runner, optional SQLite, deferred Stage B, and no generalized lifecycle machine are proportionate.
6. r0 inherited-finding closure
#	r0 finding	r1 status	Exact r1 mechanism
1	Writer confound	CLOSED	:71-90,140-163: L and T deterministic; model never writes either primary memory.
2	Model-ledger output-cap tax	CLOSED	:150-161: same action-side schema and cap; no rewritten ledger. A new provenance-interface issue remains, but the r0 ledger-rewrite defect itself is gone.
3	Weak comparator	PARTIALLY CLOSED	:96-109 creates a strong deterministic store, but its materializer remains weaker/less specified than T's :121-123.
4	History budget not binding	CLOSED	:125-138,226-236: history is diagnostic and budget-pressure scenarios must exceed the common budget.
5	Hidden Inspect state	MOVED	:270-298,469-476: direct runner becomes default and Inspect must earn admission via no-paid conformance. Cannot be called runtime-closed before implementation.
6	Provider ambiguity	MOVED	:300-317: exact endpoint is required and direct provider is fallback if router cannot bind it. Execution proof belongs to Gate 2.
7	Missing order control	CLOSED	:319-325: paired, randomized, counterbalanced, interleaved, frozen schedule.
8	Fragile 4-pilot/clamp sizing	PARTIALLY CLOSED	:361-384: 12 pairs, uncertainty-aware simulation, minimum 48, no maximum clamp. Exact conservative variance method still missing.
9	False cold-restart label	CLOSED	:253-268: genuinely fresh interpreter process; correctly named process-cold, with narrower non-claims.
10	Oracle/gold contradiction	CLOSED	:125-134,183-191: oracle diagnostics explicitly exempted from primary model-path gold isolation.
11	Generator privilege	PARTIALLY CLOSED	:193-202 adds byte canaries, differential admission and hand-authored challenges; materializer asymmetry and exact generator bounds remain open.
12	Production-doctrine leakage	CLOSED	:27-42,270-298,486-498: temporary instrument, thin runner, single explicit reconstruction child.
7. Findings
P0

None.

I found no defect requiring rejection of the Stage-A idea.

P1 — Comparator materialization parity is not closed

Artifact: MBCX-01-EXPERIMENT-DESIGN-r1.md:96-123,140-163@7fa45e09

EXECUTED. SEARCHED.

Arm L already stores scope, trigger, dependencies and status. Yet :109 only says it serializes current flat facts and open obligations.

T at :121 explicitly gets:

current scoped state;

due and near-due obligations;

relevant dependency closure;

active correction/conflict information.

The scientific distinction should be what T can represent that a flat ledger cannot, not “T has a competent selector and L dumps everything.”

The executed 3-scope fixture showed:

L-as-written 6,363 tokens versus strong-flat L 1,009 versus T 858.

CAME-Bench/STITCH independently shows how powerful structured context selection can be: intent-based filtering suppresses context-incompatible history and materially changes performance. That is evidence that selector policy cannot be treated as innocuous scaffolding. 
ACL Anthology
 StateFuse's matched-resolver design supplies the cleaner precedent: compare representation under matched resolver/verification policy. 
arXiv

False-positive consequence: T wins because it received a better working-set selector, then Moonwalker attributes the win to versioning/conflicts/provenance/typed closure.

Fix class: COMPARATOR-MATERIALIZATION-PARITY.

Give L the strongest cheap deterministic materialization that its existing flat fields support:

current scope → current flat state → due/near-due obligations → explicit direct prerequisite IDs → terminal-ID suppression

under the same packet budget.

T may then earn value only from mechanisms L genuinely lacks: version/currentness relationships, conflict preservation, richer supersession semantics, provenance closure, typed/multi-hop dependency closure.

That is the deciding fix behind my verdict.

P1 — The supposedly common action-only interface still contains a T-favored output demand

Artifact: :96-123,142-163

READ-ONLY.

r1 repeatedly calls the primary decision output “action-only,” but :153-159 requires:

state_claims

provenance_ids

Arm T explicitly carries evidence references/provenance (:113-121). Arm L explicitly does not maintain provenance closure (:107).

So both schemas have the same byte shape, but not the same information burden.

My output-size fixture fits below 512 tokens, so this is not the old output-cap starvation. It is a task-difficulty/cognitive-burden asymmetry.

False-positive consequence: L spends decision capacity guessing or reconstructing provenance that T receives explicitly; malformed/low-quality L output increases even if its action memory is equally good.

Fix class: PRIMARY-OUTPUT-PARITY.

For the primary call, I would require only what the primary action outcome needs—e.g. ongoing_choice, action_ids, channel_queries. If state_claims are required for action semantics, keep them. provenance_ids should either be removed from the primary model response or L must receive the corresponding flat source IDs.

Provenance quality can remain a secondary T-vs-L mechanism diagnostic without making it a mandatory inference tax.

P1 — high_stress_set_f1 is not sufficiently defined to carry the +0.08 rule

Artifact: :208-223,332-356,398-424

EXECUTED. UNSEARCHED — SETTLED-BY-PINNED-BYTES + arithmetic.

The bytes identify the metric by name but do not say whether high-stress set-F1 is:

pooled across all opportunities;

per-decision macro F1;

per-scenario set union;

averaged by stress subtype;

or something else.

They also do not define the correct score when both prediction and due-action gold are empty.

My executed arithmetic demonstrates the consequence. With only six due positives, one FN alone changes pooled F1 by 0.0909. Thus a +0.08 difference can literally be one changed action, contrary to :222 and :410.

With macro scoring over 30 decisions, three full decision flips approximate +0.10—but that is a different estimand.

False-positive/negative consequence: the same raw actions can cross or miss the win threshold depending on an unstated scoring convention.

Fix class: ESTIMAND-FREEZE.

Before implementation, specify mechanically:

opportunity inclusion → TP/FP/FN construction → empty-set rule → aggregation within stress subtype → scenario statistic → paired delta.

Then rerun the granularity arithmetic and decide whether +0.08 still represents the engineering effect the owner intends.

P1 — “Maximum-load Gate 0” has no maximum workload

Artifact: :204-251,447-468

EXECUTED.

The generator specifies minimums:

≥24 obligations;

≥30 high-stress opportunities;

≥3 scopes;

etc.

It does not specify maxima for:

simultaneously open obligations;

current-state rows;

dependency width/depth;

event fan-out;

natural-language field length.

Yet :244 and :463 require “maximum-load” payload tests.

There is no maximum to construct from the current contract.

My token fixtures show why this can matter: sufficiently large legal-looking L/T structures cross the 6,000-token budget at materially different points.

False-negative consequence: T can be killed because a generator implementation chooses a much wider active frontier than the intended operating condition.

False-positive consequence: L can be made to overflow first by filling unrelated scopes while T's selector emits only its current scope.

Fix class: WORKLOAD-ENVELOPE FREEZE.

Preregister maxima or explicit distributions for active rows, simultaneous obligations, dependency width/depth, text length and event fan-out. Then Gate 0 has an actual adversarial maximum rather than an implementer's interpretation.

P1 — Pilot variance conservatism is named but not specified

Artifact: :361-396

EXECUTED. SEARCHED.

r1 correctly removed the [24,48] clamp and correctly says an underfunded experiment must be reported as underfunded.

But:

“Use a conservative upper uncertainty bound for pilot paired variance”

doesn't define:

the estimator;

confidence level;

parametric/non-parametric assumptions;

stratification;

or the simulation family.

That leaves a result-changing analyst choice after pilot data are visible.

My rare-tail witness showed a 12-pair pilot missing both tails about 28% of the time, in which case empirical variance can collapse despite high true variance.

The broader statistical literature independently supports the underlying concern: small variance-estimation samples can still underpower subsequent work, and upper confidence limits are one explicit method of accounting for estimation uncertainty. 
arXiv

Consequence: a negative confirmation can look dispositive while never having attained the declared 80% power.

Fix class: POWER-PROCEDURE PREREGISTRATION.

Before pilot data exist, freeze the variance-UCB rule, confidence level, simulation generator, and exact power event. If the resulting n is unaffordable, r1 already has the correct answer: underfunded, not negative.

P2 — Process-cold design is good, but it needs a negative reconstruction witness

Artifact: :253-268,447-484

READ-ONLY.

Fresh interpreter process is the correct construct.

The missing adversarial test is simple: deliberately withhold or corrupt one required arm artifact while leaving the public cursor and ordinary environment intact. Reconstruction must fail or mechanically disagree.

Also run the inverse: leave the arm artifact intact while removing non-required ambient files/environment variables. Reconstruction should still succeed.

False-positive consequence: a child process appears to reconstruct memory because the supervisor/cursor/environment carried state that should have come from the arm artifact.

Fix class: RECONSTRUCTION-DEPENDENCY NEGATIVE TEST.

P2 — Retry eligibility needs to distinguish pre-dispatch failure from ambiguous post-send failure

Artifact: :319-330

READ-ONLY.

Retry only transport failures that produced no model output is almost right, but after a connection drop the client may know that it received no output without knowing whether the provider generated one.

Retrying an ambiguous accepted request gives that cell another stochastic draw. If larger T requests experience more such failures, retry behavior can correlate with arm.

False-positive/negative consequence: one arm receives more hidden rerolls.

Fix class: AMBIGUOUS-ATTEMPT INVALIDATION.

Confirmatory retries should be permitted only when the client can establish that the request was never accepted/processed. A post-send ambiguous failure invalidates that cell and follows a preregistered whole-pair handling rule.

The same logic argues against using schema repair as a rescue for primary scoring. If retained, the unrepaired first result should determine primary schema failure; the repair can be diagnostic.

P2 — OpenRouter is usable, but exact-routing evidence requires one extra cache/account check

Artifact: :300-330,469-476

READ-ONLY. SEARCHED.

r1 already contains the architectural escape hatch: if OpenRouter cannot establish the exact condition, use direct provider transport.

That is important because OpenRouter documents:

base provider names span endpoint variants/regions; exact full endpoint slugs are required for exact targeting; 
OpenRouter

require_parameters defaults false unless explicitly enabled; 
OpenRouter

request-level provider.only is merged with account-wide allowed-provider settings; 
OpenRouter

context compression can remove/truncate middle messages; 
OpenRouter

router metadata exposes the routing pipeline, but response-cache hits strip that metadata; 
OpenRouter
+1

response caching itself can be disabled per request. 
OpenRouter

Fix class: TRANSPORT-CONFORMANCE DETAIL.

If OpenRouter is chosen, Gate 2 should prove response caching off, exact account/request provider intersection, exact endpoint, transforms off, fallbacks off, parameters required, and routing metadata present when expected.

No need to study provider variance.

P2 — Oracle policy still needs exact construction fixtures

Artifact: :125-134,183-191,226-236

READ-ONLY.

The conceptual boundary is now correct. The exact oracle algorithm isn't yet specified.

Oracle-minimal should provide the minimal public evidence/state necessary to decide, not the target action itself in disguised form. Oracle-all-relevant should include all relevant public redundancy/conflict even if that can make reasoning harder.

τ-bench supplies a useful scoring principle here: score the required outcome/state rather than require the agent to reproduce one privileged reference action path. 
GitHub

Fix class: ORACLE-POLICY FIXTURE.

P3

No additional P3 issue is necessary to decide the round.

8. WHAT WOULD YOU BUILD?

READ-ONLY proposal.

I would build almost exactly r1, with one important recut.

The smallest Stage-A instrument is:

Deterministic prospective world → common reducer admission → two stores → two strongest-native deterministic materializers → one stateless decision caller → one mechanical scorer.

For the world/scorer, I would borrow the PM-Bench experimental shape rather than invent prospective-memory testing from scratch: deferred actions, a controlled long trajectory, and a dedicated prospective-memory scoring instrument. 
arXiv

For the fresh-context idea, I would borrow AgenticSTS's explicit bounded/fresh decision-prompt discipline. 
GitHub

For comparator discipline, I would borrow StateFuse's matched resolver/verification policy idea. 
arXiv

Then:

Arm L store: latest scoped state map + active obligation table + explicit trigger/status/scope/direct-dependency fields + terminal/tombstone IDs.

Arm L materializer: simple deterministic scope/due/near-due/direct-prerequisite filtering. No version chain, conflict object, provenance graph, validity interval, supersession graph, or multi-hop typed traversal.

Arm T: current r1 typed/versioned/conflict/provenance representation and closure.

That gives L everything a competent simple ledger ought to do without quietly turning it into T.

I would keep the direct stateless HTTP runner. Inspect is a capable evaluation substrate, but its normal TaskState is explicitly a growing chat history, and model generation appends messages to it. 
Inspect
 Its checkpoint recovery can also restore agent message/compaction history and internal sample state. 
Inspect
 Those are features for general evals and unnecessary hidden-state surfaces for this extremely narrow experiment.

Harbor is also broader than necessary; it is designed for arbitrary agents and large-scale container/environment execution. 
GitHub
 τ-bench is more interesting as a source of deterministic world/outcome-scoring patterns than as the MBCX runner itself. 
GitHub
+1

I would not add vector retrieval, a memory agent, model-written memory, provider-native compaction, or any Stage-B mechanism yet.

9. WOULD YOU DESIGN IT DIFFERENTLY?

Yes, slightly.

I would make the separation between representation and ordinary packet hygiene explicit.

Today r1 effectively allows:

L representation + L materializer

versus

T representation + T materializer.

That's defensible if the intended treatment is the entire architecture package, but it makes the causal story weaker than it needs to be.

I would define an arm-neutral basic materialization layer containing only operations possible from both stores without richer semantics:

scope restriction;

obviously terminal-row suppression;

due/near-due selection from explicit triggers/status;

direct prerequisites explicitly listed on an obligation;

deterministic serialization/budget accounting.

Then each arm supplies its representation-specific extension.

For L: nothing further.

For T: version/currentness resolution, conflict preservation, typed/multi-hop closure, provenance/validity relationships, richer supersession semantics.

That makes the result much easier to interpret:

“After giving a flat ledger every cheap obvious advantage, the extra typed semantics still bought X.”

If T loses then, I believe the loss. If T wins then, I believe the win.

I would also freeze the exact scorer before anyone writes the generator, because otherwise the generator can unconsciously evolve toward whatever makes the +0.08 rule convenient.

10. Omission attack

Omitted strong simple comparator: a scoped, due-filtered deterministic flat ledger with direct explicit prerequisites and terminal tombstones. r1's L has almost all of the underlying fields but does not clearly grant it this materializer.

Hidden confound capable of favoring L: T's richer metadata and structural closure consume substantially more payload space. An unconstrained generator can create an unrealistically wide active frontier that causes T budget_failure while compact L survives, unfairly killing a useful typed kernel.

Hidden confound capable of favoring T: L dumps many irrelevant flat rows while T receives current-scope/due/closure selection. My executed fixture demonstrates this path.

Framework/provider footgun: OpenRouter request routing can interact with account-wide allowed-provider settings, while response-cache hits remove the router metadata needed to prove what actually happened. 
OpenRouter
+1

Persuasive false positive: multi-scope noise fills L's prompt but T filters to the active scope. T wins +0.10, and the result gets attributed to versioning/provenance/conflict semantics when the real mechanism was basic scope filtering.

Unfair kill: generator produces an unusually huge live dependency frontier because r1 sets no maximum. T correctly refuses to omit structural closure, hits budget_failure, and is killed even though the intended Moonwalker operating regime rarely has such a frontier.

Machinery I would delete: SQLite unless implementation proves it is simpler than plain files/JSONL for Stage A. I would also keep Inspect out unless its no-paid conformance suite passes trivially.

Missing no-paid test without which I refuse pilot inference: a materialization-parity differential. Feed the exact same public state into L and T, then mechanically verify that every cheap selection operation available from L's own fields is actually exercised by the strongest L implementation. Pair that with exact-tokenizer max-load cases.

Prior-art mechanism I would directly borrow: StateFuse's matched resolver/verification-policy discipline for representation comparison, plus PM-Bench's prospective-memory experimental world/scoring patterns. 
arXiv
+1

11. Sweep log
A — Has the question already been answered?

Query: PM-Bench prospective memory LLM agents 2026 arXiv official repository
Opened: https://arxiv.org/abs/2607.12385
SEARCHED. Section deciding it: abstract/controlled-testbed description. Prospective memory is directly studied, but not deterministic-flat versus deterministic-typed under matched writers/materializers. Further PM-Bench searching was unlikely to answer the exact Stage-A contrast. 
arXiv

Query: AgenticSTS bounded memory long horizon agents 2026 arXiv official repository
Opened: https://github.com/AlayaLab/AgenticSTS
SEARCHED. Bounded named layers and fresh prompts are relevant; repository explicitly leaves matched accumulating-context testing open. Does not obsolete MBCX. 
GitHub
+1

Query: "LongHorizon-Harness" long-horizon agents 2026 arXiv GitHub
Opened: https://arxiv.org/abs/2608.01964
SEARCHED. Supplies external-state/fresh-executor patterns but bundles a richer management architecture, so it is not the r1 causal contrast. 
arXiv

Query: StateFuse deterministic conflict preserving memory flat matched resolver 2026
Opened: https://arxiv.org/abs/2607.05844
SEARCHED. Deciding mechanism: representation comparison under matched resolver/verification. This directly changed my r2 recommendation: L and T need comparator materialization parity. 
arXiv

Query: CAME-Bench STITCH 2026 ACL contextual memory agent benchmark
Opened: https://aclanthology.org/2026.findings-acl.584/
SEARCHED. Deciding mechanism: intent-aware filtering can materially suppress context interference. Confirmed selection policy is itself a possible treatment. 
ACL Anthology

Query: Mem2ActBench ACL 2026 memory grounded tool use
Opened: https://aclanthology.org/2026.acl-long.370/
SEARCHED. Memory-grounded actions are useful external validity; no flat-vs-typed representation isolation. 
ACL Anthology

Query: LongMemEval-V2 2026 ICML memory agent official arXiv
Opened: https://github.com/xiaowu0162/LongMemEval-V2/
SEARCHED. Much broader long-term accumulated experience; useful later, not Stage-A replacement. 
GitHub

Query: MAGE MemoryArena execution state tree 2026 Microsoft
Opened: https://www.microsoft.com/en-us/research/publication/beyond-semantic-organization-memory-as-execution-state-management-for-long-horizon-agents/
SEARCHED. Execution-state-tree architecture is useful prior art but uses active maintenance/branch machinery that changes more causal factors than Stage A. 
Microsoft

Query: Remember When It Matters Meta Research 2026 agent memory
Opened: https://arxiv.org/abs/2607.08716
SEARCHED. Separate proactive memory agent is an ecological/controller intervention, not a pure representation comparison, so it belongs conceptually after Stage A. 
arXiv

Non-US/non-UK surface

Query: AgeMem Wuhan University Alibaba Agentic Memory 2026 ACL
Opened: https://arxiv.org/html/2601.01885v3
SEARCHED. Authors are from Wuhan University and Alibaba Group; AgeMem learns long- and short-term memory actions end-to-end. It expands the mechanism landscape but strengthens r1's decision to postpone learned management to Stage B. 
arXiv

I stopped the “already answered?” lane there because the mechanism classes had converged: prospective benchmarks, bounded/fresh contracts, flat/conflict-preserving matched comparisons, active state managers, learned memory controllers and action-grounded benchmarks were all represented, and none duplicated Stage A.

B — What should be borrowed?

Query: Harbor framework official GitHub agent evaluation framework Terminal-Bench
Opened: https://github.com/harbor-framework/harbor
SEARCHED. Harbor is strong general eval infrastructure but substantially broader than the needed Stage-A runner. Borrow ideas if needed; do not make it a required dependency. 
GitHub

Query: tau2-bench official GitHub simulation framework tasks agent evaluation deterministic scoring 2026
Opened: https://github.com/sierra-research/tau2-bench
Opened: https://github.com/sierra-research/tau2-bench/blob/main/docs/evaluation.md
SEARCHED. Useful borrow: state/outcome-based scoring rather than forcing one reference action trajectory. Its July 2026 grading fixes also demonstrate why scorer/task versions must be frozen before interpreting results. 
GitHub
+1

Query: synthetic benchmark generator bias LLM agent evaluation benchmark contamination primary paper 2026 generated tasks
Opened: https://www.microsoft.com/en-us/research/publication/synae-a-framework-for-measuring-the-quality-of-synthetic-data-for-tool-calling-agent-evaluations/
SEARCHED. SynAE separates synthetic benchmark quality into validity, fidelity and diversity and reports that no single metric captures it. This confirms r1's hand-authored challenge set is worthwhile rather than decorative. 
Microsoft

Stop reason: direct runner, Inspect, Harbor and τ-bench cover the meaningful runner choices. Another generic framework was unlikely to change the recommendation: r1 needs less framework, not more.

C — Framework/transport footguns

Query: site:inspect.aisi.org.uk TaskState messages generate checkpoint retry cache prompt parallelism Inspect AI
Opened: https://inspect.aisi.org.uk/solvers.html
Opened: https://inspect.aisi.org.uk/checkpointing.html
SEARCHED. TaskState includes chat history extended by model interactions, generation appends assistant messages, and checkpoint recovery restores agent state including message/compaction history. Confirms Inspect must pass r1's conformance gate before use. 
Inspect
+1

Query: site:inspect.aisi.org.uk errors eval retry sample retry completed samples bias
Opened: https://inspect.aisi.org.uk/errors-and-limits.html and current retry/reference documentation.
SEARCHED. Inspect can preserve completed samples and has explicit retry behavior; r1 is correct not to inherit this blindly for scenario-level trajectories. 
Inspect
+1

Query: site:openrouter.ai/docs/guides/routing/provider-selection exact endpoint provider slug allow_fallbacks require_parameters
Opened: https://openrouter.ai/docs/guides/routing/provider-selection
SEARCHED. Exact endpoint slugs, fallback control and require_parameters confirmed. 
OpenRouter
+1

Query: site:openrouter.ai/docs/guides/features/router-metadata account provider settings merge route metadata cache hit
Opened: https://openrouter.ai/docs/guides/routing/provider-selection
Opened: https://openrouter.ai/docs/guides/features/router-metadata
SEARCHED. Request provider allowlist merges with account-wide allowed providers; cached responses omit routing metadata. Both belong in Gate 2. 
OpenRouter
+1

Query: site:openrouter.ai/docs/guides/features/message-transforms context compression middle-out transforms
Opened: https://openrouter.ai/docs/guides/features/message-transforms
SEARCHED. Context compression can truncate/remove middle messages. r1 correctly invalidates transformed requests. 
OpenRouter

Query: site:openrouter.ai/docs prompt caching response cache disable cache provider routing
Opened: https://openrouter.ai/docs/guides/features/response-caching
SEARCHED. Response caching is a distinct router surface and can be disabled request-by-request. Add that exact control to the frozen cache posture. 
OpenRouter

Stop reason: these official docs cover the concrete hidden-state/request-mutation paths capable of changing L-vs-T.

D — Experimental-design footguns

Query: site:itl.nist.gov paired observations bootstrap paired permutation test sample size pilot variance uncertainty
Opened: https://www.itl.nist.gov/div898/handbook/prc/section3/prc311.htm
SEARCHED. Scenario pairing is methodologically correct: corresponding measurements on the same experimental unit are paired. 
NIST

Query: site:docs.scipy.org bootstrap paired confidence interval paired data scipy.stats.bootstrap paired
Opened: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html
SEARCHED. Paired bootstrap is directly supported by resampling common indices across paired samples. 
SciPy Documentation

Query: site:docs.scipy.org permutation_test paired samples exact Monte Carlo scipy stats
Opened: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.permutation_test.html
SEARCHED. Paired sample permutation is a valid sensitivity test for this paired design. 
SciPy Documentation

Query: pilot standard deviation uncertainty sample size re-estimation internal pilot blinded variance primary source paired continuous outcome
Opened: https://arxiv.org/abs/2602.03218
SEARCHED. Small variance-estimation samples can still underpower later work; explicit variance upper-confidence methods exist. This did not supply a plug-and-play formula for bounded F1, but it confirms r1 must specify rather than merely name “conservative.” 
arXiv

Query: site:itl.nist.gov handbook randomization order effects experimental design blocking sequence effects
Opened: https://www.itl.nist.gov/div898/handbook/pri/section3/pri331.htm
Opened: https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm
SEARCHED. NIST's design guidance supports randomization plus blocking nuisance variables—the exact logic of r1's within-scenario counterbalancing/interleaving. 
NIST
+1

Stop reason: paired inference, order control, small-pilot uncertainty and synthetic-data validity were all covered by primary methodological sources. Further generic statistics searching would not alter the concrete fixes above.

12. Residual risks and explicit non-claims

After the fixes, the remaining residuals are legitimate limits rather than reasons not to run Stage A.

A positive Stage-A result would mean only that the richer typed representation/materialization package beats the strongest flat deterministic ledger under the chosen frozen model/provider condition and workload distribution.

It would not establish:

natural-language memory writing;

learned memory management;

semantic/open-world retrieval;

general memory;

production Munin;

multi-agent sharing;

personality/emotion/procedural memory;

security against hostile memory;

model-family generality;

provider generality;

host/power-failure durability;

unbounded-scale continuity.

AgeMem, MAGE and proactive-memory-agent work make clear that active/learned memory controllers are potentially valuable, but they add causal variables deliberately excluded here. 
arXiv
+2
Microsoft
+2

The remaining important scientific residual is external validity: a synthetic bounded control-room world can tell us whether the mechanism exists, not how broadly it transfers. Mem2ActBench and LongMemEval-V2 are sensible later validation surfaces precisely because they test substantially different long-term-memory demands. 
ACL Anthology
+1

13. Seat capability report

Model: GPT-5.6 Sol.

Harness: ChatGPT council seat with Moonwalker MCP local read/shell capability and independent web search/opening of primary sources.

Local reach: pinned Git objects, authorized Downloads sources, hash verification, bounded shell/Python execution.

Search reach: worldwide web discovery plus primary-source opening. The sweep included US and non-US research, including the Wuhan University/Alibaba AgeMem work. 
arXiv

Execution reach: Git/hash probes, local tokenizer execution, payload generation, F1 boundary arithmetic, stochastic power simulation, comparator-construction attack. No implemented MBCX harness exists yet, so I could not execute a real L-vs-T model run or reconstruction failure injection.

Tokenizer limitation: the exact Stage-A model is not yet frozen, so the executed token counts use a cached Llama-3 8B Instruct tokenizer as a modern BPE proxy. Every actual Gate-0 number must be recomputed with the selected model's exact tokenizer/request wrapper.

Tool-side-effect disclosure: while searching for an already-installed tokenizer, I invoked the apparently read-only command ollama list. Ollama unexpectedly started its application updater, downloaded an update, and launched its installer in the background. I immediately stopped using Ollama. I did not run local inference and the command did not touch MBCX experiment files, but strict environment-level read-only purity was therefore imperfect due to the tool's own updater behavior.

Paid inference: none.

Other seats/prior verdicts: not read, sought, or referenced.

The r1 architecture is now pointed at the right experiment. I would keep Stage A, keep the one fixed provider condition, keep the direct thin runner, and keep the deterministic L-vs-T comparison. Before money moves, make L genuinely brutal, remove the residual interface advantage, freeze the scorer and workload envelope, and make the sample-size conservatism executable rather than adjectival. Once those are fixed, I would run it.
