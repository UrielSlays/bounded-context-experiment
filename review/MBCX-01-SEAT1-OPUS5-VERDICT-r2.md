Used Moonwalker integration, searched the web, ran 3 commands

Used Moonwalker integration, searched the web, ran 3 commands
MBCX-01 EXPERIMENT COUNCIL — ROUND 2 VERDICT
1. Verdict

GO-WITH-FIXES(P0 — primary-contrast identification: representation is bundled with packet-selection policy, and no primary arm is required to operate under binding budget pressure)

Answering the packet's own question (§2 l.81): if Stage A says the typed kernel wins, you should not yet believe the representation caused it — the same win is produced by a selection policy that prior art has already measured separately, and that is implementable on top of Arm L. If it loses, the test is currently unfair in one specific way — the update taxonomy omits the only mechanism class where typed versioning is strictly necessary.

Both defects are repairable inside the existing architecture: one added deterministic arm, one generator invariant, one added update kind. Neither requires new machinery. r1 is a large, real improvement over r0 — eight of twelve inherited findings are genuinely closed, and two of the closures are byte- and probe-confirmed rather than asserted.

2. Pin / byte verification
Check	Result
Pinned commit 7fa45e09… — artifact blob	2c3c12b839b8fc356feb63cd05f050884c46482f
Same blob at HEAD 84cca38…	2c3c12b8… — identical; the pin did not move under me
Diff pin→HEAD	additive only: packet-r2, seat-3 prompt, generator script (522 insertions). Artifact untouched
SHA-384 (computed from git cat-file blob)	8D8F7B083B32C5CC4B9F682C29D759967D3A71CD4B452DEE96EEC06785189A89A42B1FC95BB864B1D574117BE4729E32 — matches packet §0 exactly
Size / lines	27,182 bytes / 542 lines — matches packet §0 exactly
Working-tree file	byte-identical to the pinned blob (same SHA-384). I read from the Git object anyway
Packet r2 SHA-256	33D0E06105E898EAD48151147BA94B3DA652CC748D4972A9B391917629B69359, 364 lines
LOCAL-SOURCE-MANIFEST-r1.md items B/C	all 7 SHA-384 pins verified MATCH on disk this session

Seal observed. The working directory contains CLAUDE-OPUS5-SEAT-VERDICT-r1.md, MBCX-01-SEAT3-CODEX-VERDICT-r1.md, and a ChatGPT-<council-browser-port> restart manifest. Per packet l.18 I did not open, read, grep, or hash any of them. All three are untracked (?? in git status), so they are also outside the pin.

Bytes I created: %TEMP%\mbcx-r1-pinned.md (blob extract), and /home/claude/{p1,p5}.mjs + inline Python in my probe container. Probe-transient only. No repo, vault, or artifact writes. Nothing banked to disk.

3. Evidence read and probes run

Pinned artifact: MBCX-01-EXPERIMENT-DESIGN-r1.md @7fa45e09, all 542 lines. Packet: r2, all 364 lines. Manifest: hash-verified, not re-read (settled by the r1 artifact, which is self-contained on every claim I adjudicate).

Probes (all EXECUTED, no paid inference, no model calls):

#	Probe	Instrument
1	Max-load Arm L / Arm T payload + output fixtures at r1's stated minimums	gpt-tokenizer o200k_base BPE, offline via npm
2	Per-record verbosity ratio L vs T	same
3	Set-F1 granularity across three due/lure splits of "30 opportunities"	Python
4	12-pair pilot → SD uncertainty → n → realized power; 20,000-draw Monte Carlo of the full sizing procedure	Python + scipy
5	Adversarial scenario shape (retracted correction) vs r1's update taxonomy and invariant list	constructed and traced by hand against l.107 / l.115 / l.213 / l.226–236
6	Manifest + pin verification	PowerShell / git

Tokenizer limitation, stated up front (packet §8.2): tiktoken's BPE download is blocked from my container, so I used the npm-bundled o200k_base encoding. If the frozen endpoint serves a non-OpenAI model, absolute counts shift. Every conclusion below rests on a margin of ≥2×, so none is knife-edge — but they are estimates, not the served tokenizer.

4. Experiment-specific applicability ruling

Per packet §1.2 I excluded, and did not convert into findings:

Licensing/redistribution. NOT APPLICABLE — NON-LOAD-BEARING. I did open LongHorizon-Harness's license (MIT) as a borrowability datum for §7.2, not as a compliance question. For an internal experiment that ships nothing, exposure is near zero.
Clean-room implementation. NOT APPLICABLE. r1 l.31/l.284 already adopts "borrow the mechanism," which is correct.
Production security, hostile actors, prompt injection, FIPS, seal chains. NOT APPLICABLE — NON-LOAD-BEARING. No path from any of these to a wrong experimental answer in a single-operator lab run.
PID ownership / lifecycle / cleanup frameworks. NOT APPLICABLE. r1 l.268 and l.498 already delete the r0 leakage; I checked and found no residue.
Hash-algorithm posture. NOT APPLICABLE — NON-LOAD-BEARING. Local run identity only.
Provider-family generality. NOT APPLICABLE. l.302 declares it out of scope, correctly — Stage A pins one condition on purpose.

The standing role card's ALREADY-BUILT / PRODUCT-FIT / BIGGER-THAN-THE-BUG triad is partly superseded here by §1.1–1.3. I answer ALREADY-BUILT in full (it is load-bearing: prior art could make Stage A obsolete). PRODUCT-FIT I answer in one line — does Moonwalker need to know whether typed continuity beats a flat ledger before building Munin? yes, and no shipped artifact turns on it — and mark further product-posture analysis NOT APPLICABLE — NON-LOAD-BEARING. BIGGER-THAN-THE-BUG is now NOT APPLICABLE: r1 §10/§18 already shrank the instrument, and I found nothing left to cut except one thing, named at §10 below.

5. Claim scoreboard C1–C12
	Verdict	Basis
C1 Stage A causally identified	FALSE as worded	The claim enumerates writer quality, parsing labor, call count, output burden — all genuinely closed. It omits the one that is open: packet-selection policy. l.73 declares the bundle honestly ("the representation and the deterministic packet derived from it"), so this is a scope defect, not concealment — but C1's literal claim does not hold. EXECUTED + SEARCHED
C2 Arm L strong enough to kill	UNDERDETERMINED	Arm L is a genuinely strong ledger on lifecycle (status, cancel/complete/reschedule, closed-ID dedup). It omits evidence references (l.107) while the shared output schema demands provenance_ids (l.159) and provenance is a scored secondary (l.352). Two published simple state records — LongHorizon-Harness and Meta's memory bank — both carry evidence links. SEARCHED
C3 Budget symmetry real	HOLDS	EXECUTED: max-load action-only output = 396 tok against the 512 cap (headroom 116). No arm-specific maintenance output exists (l.161). The r0 starvation is gone
C4 World does not privilege T	UNDERDETERMINED	l.193–202 checks are the strongest part of r1. But l.202's "review showing public transition fields do not precompute T's packet" is a human judgment, not a machine check, and no invariant tests whether the update taxonomy spans the mechanisms under test
C5 Outcome has useful resolution	UNDERDETERMINED	EXECUTED: holds only if most of the 30 opportunities are due items. l.219 says "due or non-due" and l.216–217 require ≥8 lures. At |D|=30, +0.08 ≈ 3.4 obligations ✓. At |D|=15, ≈1.7. At |D|=10, ≈1.2
C6 Reconstruction measures the construct	HOLDS	l.255–266: fresh interpreter process via supervisor, only the designated artifact + public cursor reopened, same adapter entry point, and l.266 states the narrower claim explicitly. This is a clean fix
C7 Runner experimentally neutral	UNDERDETERMINED	The l.288–297 acceptance gate is right in structure and incomplete in two named ways. SEARCHED — see P1-4
C8 One exact condition frozen	HOLDS	l.307 requires "exact routable provider endpoint, not only a base provider family"; l.317 falls back to a direct transport if the gateway cannot bind it; l.315 disables fallbacks and compression plugins and records returned metadata. This directly answers the r0 base-slug defect
C9 Order/retry cannot mimic an effect	HOLDS	l.151, l.321–328: pairing, within-scenario counterbalancing, interleaving, frozen schedule, one in-flight request, retry only on no-output transport failure from a clean snapshot, no selective reroll
C10 Statistical plan supports win and kill	UNDERDETERMINED	EXECUTED: power is fixed (12 pairs, conservative UB, no clamp). The failure has moved to affordability, and the bound level is unnamed so the run cannot be costed
C11 Oracle diagnostics scoped honestly	HOLDS	l.131–134: explicit exemption, explicit non-deployability, excluded from the primary estimate, plus the oracle-all-relevant variant which specifically addresses the "oracle packet is paradoxically harder" adversary
C12 Instrument proportionate	HOLDS	l.274–284 thin runner, l.298 framework adoption demoted to convenience, l.268/l.498 lifecycle machinery deleted. One remaining cut named at §10
6. r0 closure table
#	Inherited finding	Status	Exact r1 mechanism
1	Writer confound	CLOSED	l.75 both artifacts maintained by deterministic code; l.161 "Neither primary arm asks the decision model to rewrite memory"
2	Output-cap confound	CLOSED	l.153–161 action-only schema, no ledger in output. EXECUTED: 396/512 at max load
3	Weak comparator	PARTIALLY CLOSED	l.96–109 builds a real deterministic ledger. Still omits evidence refs (P1-1) and the selection-policy variant (P0-1)
4	History budget not binding	MOVED	l.235 adds a budget-pressure invariant — but only for the chronological diagnostic, on a slice. EXECUTED: neither primary arm approaches 6,000 tok at r1's scenario scale (P0-2)
5	Hidden runner state	PARTIALLY CLOSED	l.288–297 conformance gate is genuine and no-paid. SEARCHED: two gaps (P1-4)
6	Provider ambiguity	CLOSED	l.307 exact routable endpoint; l.317 transport fallback; l.315 metadata recorded
7	Missing order control	CLOSED	l.151, l.321–325
8	Fragile sizing	MOVED	l.362 12 pairs, l.375 conservative UB, l.377 no clamp + explicit "do not run underpowered." EXECUTED: power fixed, affordability now the open end (P1-3)
9	False cold-restart label	CLOSED	l.255–266 fresh interpreter + narrowed claim
10	Oracle/gold contradiction	CLOSED	l.134 explicit exemption and non-participation
11	Generator privilege	PARTIALLY CLOSED	l.181 "Arm T may not receive a more semantically resolved event than Arm L"; l.193–202 canaries, differential tests, hand-authored challenges. Taxonomy coverage unchecked (P2-2)
12	Production-doctrine leakage	CLOSED	l.268 supervisor owns one explicit child, no registry; l.498 ordinary hygiene, explicitly not a lifecycle subsystem
7. Findings
P0-1 — The treatment bundles representation with packet-selection policy. Prior art has already measured the selection effect separately. [EXECUTED + SEARCHED]

Artifact. l.109: Arm L "serializes the current flat facts and open obligations." l.121: Arm T "assembles a bounded packet containing current scoped state, due and near-due obligations, relevant dependency closure, active corrections or conflicts." l.73 declares the causal factor as "the persisted memory representation and the deterministic packet derived from it."

Mechanism. Two things vary at once, and only one is the stated hypothesis:

Data-model richness — versions, validity intervals, supersession graphs, evidence refs. Mostly invisible to the model: whatever T does internally, the model sees only the assembled packet.
Packet-assembly policy — L dumps everything open; T computes due-ness and near-due windowing, traverses dependency closure, and selects.

The second is where a model-visible difference actually lives. Due-ness computation is also task-adjacent: selecting "which obligations are due now" is a large fraction of what the decision model is being scored on. r1's l.163 invalidates "any other arm-specific capability" — but selection sits inside the declared representation contract, so it does not read as arm-specific capability and no invariant catches it.

Prior art settles the magnitude. Meta AI, Remember When It Matters (arXiv 2607.08716, opened at origin), Table 2, τ²-Bench, n=278 paired tasks, Sonnet 4.5 action agent: the same maintained memory bank exposed two ways —

full bank dumped every step ("Full-bank context"): macro 61.5 / micro 58.6
bank + selective reminder-or-silence ("Full memory agent"): macro 64.3 / micro 61.2
no memory baseline: macro 57.5 / micro 55.0

Selection alone is worth +2.8 macro / +2.6 micro on top of maintaining the bank — roughly 40% of the total memory effect, with the representation held constant. Their own conclusion: "maintaining a memory bank is useful but exposing all remembered state is not enough; the memory agent must select what is currently behaviorally relevant."

Consequence — false positive. T wins by +0.08, the report says typed structure earns engineering, and Moonwalker builds version chains, validity intervals, and supersession graphs when the recoverable effect was a due/near-due filter over the flat ledger — ~20 lines on top of Arm L.

Fix class: treatment decomposition. Add Arm L+ — the identical flat ledger, with Arm T's selection policy (due/near-due windowing + dependency closure) applied to it. Three deterministic arms, one extra cell per scenario, zero new machinery. L→L+ isolates selection; L+→T isolates structure. If L+ ≈ T, the answer is "build the filter, not the kernel," and that is the cheapest true answer this experiment can return. Blocking before Gate 1.

P0-2 — Neither primary arm operates under binding budget pressure, so the bounded contract has no room to matter. [EXECUTED]

Artifact. l.240 budget 6,000 tokens. l.208 scenarios are 40–60 steps; l.211 ≥24 obligations. l.235 requires history to exceed the budget "by a declared factor on the budget-pressure slice" — a slice, and framed around the chronological diagnostic (l.130). No invariant requires the primary arms' payloads to approach the budget at all.

Probe. Arm L serialized at r1's stated content:

Arm L load	Tokens (o200k)	vs 6,000
24 open obligations, 12 state keys, 10 closed IDs	1,570	headroom 4,430
36 obligations, 18 state, 20 closed	2,362	headroom 3,638
60 obligations, 30 state, 40 closed	3,946	headroom 2,054
120 obligations, 60 state, 80 closed	7,876	over — but 5× r1's minimum and implausible in a 40–60 step scenario

Arm T's selected packet at comparable content: 1,869–4,821 tokens. Both arms sit at a quarter to a half of the budget. L never truncates, so its "serialize under the common budget" (l.109) never engages — which is also why r1 never had to specify L's overflow policy while T has an explicit budget_failure (l.123).

Consequence — uninterpretable null. T's entire architectural pitch is bounded continuity. If nothing is ever bounded, T's selection can only remove information L retained. A null result then means "selection did not help when there was nothing to select against," which is not evidence about the kernel. Combined with P0-1, the two failure modes point opposite ways: without pressure you get a spurious null; with pressure but no L+ you get a spurious positive.

Fix class: generator invariant. Extend l.235 to the primary arms: require Arm L's full serialization to exceed the payload budget by a declared factor k in every confirmatory scenario, report the realized ratio per scenario, and specify L's truncation policy explicitly (oldest-first, with a logged budget_failure on the same terms as T). Reaching that at 6,000 tokens means roughly 90+ simultaneously-open obligations or a smaller budget — the cheaper lever is to lower the budget, not to inflate the world. Blocking before Gate 1.

P1-1 — Arm L is required to emit provenance it structurally cannot ground. [EXECUTED byte-trace + SEARCHED]

Artifact. l.107: Arm L "does not maintain ... provenance closure." l.159: the shared output schema includes provenance_ids — l.153 says "the same JSON shape in both arms." l.352: provenance precision/recall is a scored secondary outcome.

Mechanism. T's packet carries "the minimum provenance needed to ground the decision" (l.121). L's carries none. Both models are asked for provenance_ids. Arm L can only guess, echo obligation IDs, or return empty. On any provenance-bearing metric, L loses by construction — and l.352 already hedges this ("reported as a mechanism diagnostic rather than an automatic win"), which is the design half-noticing the problem without fixing it.

Prior art says a competent simple ledger keeps evidence links. LongHorizon-Harness (arXiv 2608.01964, AMAP-ML, MIT, opened at origin) maintains "every requirement, artifact and environment fact, each marked completed, pending, blocked or untrusted, together with the audit evidence behind that status" — status enum plus evidence, and it lifts WeaveBench 51.8→80.7. Meta's bank likewise stores entries with identifiers and metadata. Two independent published simple-state designs include the field Arm L is defined without.

Consequence — false positive on a secondary that will be read as corroborating. A T win on provenance will look like independent confirmation of the typed kernel when it is a definitional artifact.

Fix class: comparator parity. Either give Arm L a single evidence_ref per record (cheap, and matches published practice), or drop provenance_ids from the shared schema and score provenance only where both arms can ground it.

P1-2 — "30 high-stress opportunities" does not pin the metric quantum; |D| does. [EXECUTED]

Artifact. l.219 "at least 30 scored high-stress due or non-due opportunities." l.222 and l.410 both claim this makes +0.08 "multiple changed decisions." l.216–217 separately require ≥4 wrong-scope lures and ≥4 completed/canceled/superseded lures.

Probe. Set-F1's granularity is driven by the gold due set, not the opportunity count:

Composition of the 30	+0.08 ≈
all 30 due (|D|=30)	3.4 obligations ✓ claim holds
15 due / 15 lures	1.7 obligations
10 due / 20 lures	1.2 obligations — the r0 problem, restored

Consequence. The stated justification for the whole +0.08 threshold silently depends on a split the artifact never specifies.

Fix class: estimand definition. State a minimum on gold due items (≥30), separately from lures, and require the generator to report realized |D| per scenario. One sentence, and it makes l.410 true.

P1-3 — Power is fixed; the failure moved to affordability, and the design cannot be costed. [EXECUTED + SEARCHED]

Artifact. l.362 twelve pilot pairs; l.375 "a conservative upper uncertainty bound for pilot paired variance"; l.377 minimum 48, no clamp, plus four named branches including "report that the decisive experiment is presently underfunded."

Probe. At df=11, the 95% CI for the true SD is [0.708, 1.698] × ŝd → n uncertain by [0.50×, 2.88×]. (r0's 4-pair pilot was [0.57, 3.73] → [0.32×, 13.9×]. The improvement is real.) A 20,000-draw Monte Carlo of the whole procedure — pilot → 95% UB → n → realized power — gives median power ≈ 0.996 at true SD 0.12 and 0.20. The rule is safe. What it costs:

pilot ŝd	n at ŝd	ŝd at 95% UB	n at UB	primary decision calls*
0.10	13	0.170	36 → 48	4,800
0.15	28	0.255	80	8,000
0.20	50	0.340	142	14,200
0.25	77	0.424	221	22,100

*two primary arms × 50 steps (l.208 midpoint). Excludes the four diagnostic controls (l.129–132), reconstruction re-calls, schema repairs, and the 20% stability replicates (l.394) — realistically another 40–80%.

Mechanism. l.375 names a rule without naming its level. 80% one-sided, 90%, 95% two-sided are all "conservative" and differ by ~2× in n. The design is therefore uncostable as written, and on plausible variance the literal outcome of following it is l.377's "underfunded" branch.

Consequence. Not a false result — a stalled one, discovered after the pilot money is spent.

Fix class: cost calibration. Name the bound level in the artifact; add a pre-pilot cost envelope (calls × tokens × price) for the plausible SD range so the owner approves against a range, not a number; and pre-commit which of l.377's four branches is preferred, so the decision is not made under sunk-cost pressure.

P1-4 — The Inspect acceptance gate is right in structure and incomplete in two specific, documented ways. [SEARCHED]

Artifact. l.288–297 requires: fresh message list per decision, no hidden TaskState.messages, caching disabled or non-contaminating, request equivalence to the direct path, no dirty resume or selective reroll, "checkpoint failure is fatal, not warning-and-continue," and "actual retry and resume identity is explicit in the log."

Two gaps, from Inspect's own docs opened at origin:

Adaptive concurrency is ON by default, max 100. inspect_ai.html reference for eval_set: "Adaptive concurrency for Model API connections. Defaults to enabled (resolves to AdaptiveConcurrency() defaults: min=10, start=20, max=100). Pass False to opt out." r1 l.279 and l.325 specify one in-flight request and frozen order blocks. Adopting Inspect without explicitly disabling this silently breaks the l.321–325 order controls — the exact confound C9 exists to prevent. The gate does not test for it.
The checkpoint setting is not recorded in the log. inspect_ai.html: "Must match the config used on the original eval for resume detection to find the checkpoint files (the original --checkpoint is not recorded in the log file)." And checkpointing.html: checkpointing "periodically persists the state of each sample so the evaluation can be resumed mid-sample," saving "the current state of the main agent (e.g. messages, compaction, etc.)" plus store and event history, and "when Inspect retries a failed sample, checkpointed data is automatically restored and the sample continued from where it left off."

That is precisely the hidden-continuity surface l.294 targets — and l.296's requirement that resume identity be "explicit in the log" is partly unmeetable, because the log does not carry the setting that determines whether checkpointing happened.

Consequence. A cell that resumed mid-sample from restored agent state — including messages — would be indistinguishable in the eval log from a clean cell.

Fix class: gate completion. Add to l.288–297: assert adaptive concurrency disabled and static max_connections=1; assert checkpoint=False and record it in the harness's own frozen manifest rather than relying on the eval log; and treat presence of any CheckpointEvent in the event stream as a cell invalidator. All three are no-paid checks and cheap. Given C12 and l.298, the simpler answer is: stay on the direct runner — see §9.

P2-1 — Typed records cost ~2.2× per obligation; information density is an unnamed treatment component. [EXECUTED]

Flat obligation record: 49 tokens. Typed obligation record (l.113–119 fields): 106 tokens. At 6,000 tokens the budget holds ~122 flat vs ~56 typed records. l.149's "identical memory-payload token budget" is identical in tokens, not in records. Once P0-2 is fixed and pressure binds, T is spending its budget on structure and L on volume — a second axis inside the "single" treatment. Fix class: reporting. Log realized records-per-packet alongside tokens-per-packet for both arms, and report the density ratio as a covariate of the primary delta.

P2-2 — The update taxonomy omits the one mechanism only typed versioning can pass. [EXECUTED]

l.213 requires updates spanning "cancellation, completion, reschedule, supersession, and value correction." Retraction of a correction is absent. Traced against the arms:

step 8 handoff_window = 09:00–11:30 → step 19 correction to 13:00–15:00 → step 31 the step-19 correction is retracted → step 44 obligation due on handoff_window.

Arm L (l.107, "corrections overwrite current flat state") has destroyed 09:00–11:30 at step 19 and cannot restore it at step 31 — it can only keep the wrong value or drop the key. Step 44 is wrong either way. Arm T (l.115 versioned assertions with validity, l.118 supersession relationships) invalidates v2 and v1 becomes current. Step 44 is right.

Which r1 invariant catches the omission? None. l.226–236 validate that updates are well-formed, not that the taxonomy spans the mechanisms under test. l.201's hand-authored challenge scenarios are specified as "ontology-independent" — aimed at the opposite failure.

Consequence — false negative. The experiment omits the stress only T can survive, then concludes typed structure does not earn its keep. Fix class: scenario content. Add retraction-of-correction (and retraction-of-cancellation) to l.213, at a declared minimum count, and add a generator invariant that every mechanism in the taxonomy appears at least once per confirmatory scenario.

P2-3 — Retrieval is deferred, but prior art shows a plain retrieval baseline is competitive. [SEARCHED]

l.138 defers lexical/vector retrieval from Stage A. Meta's Table 2: Mem0 (vector + BM25 top-10) scored macro 62.1 / micro 60.8 — above full-bank exposure (61.5/58.6) and within ~2 points of their full two-phase system (64.3/61.2). MemoryArena's cross-system result is consistent: "memory architecture complexity does not map monotonically" to outcome. Deferring retrieval is defensible for Stage A scope, but l.138's "cannot replace or weaken Arm L" understates the risk: a competitive retrieval arm might beat both L and T, and Stage A would never see it. Fix class: declared non-claim. If retrieval stays deferred, state explicitly in §19 that a Stage A win does not establish superiority over lexical retrieval — the current l.506 non-claims do not cover it.

P2-4 — Win condition 4 is structurally favorable to Arm L. [READ-ONLY]

l.405 requires T's upper bound on excess stale/canceled/superseded/wrong-scope actions to be below +0.02. Arm L drops canceled and superseded obligations from the active ledger entirely (l.107) — it cannot select a lure that is not in its payload. Whether T can depends on an ambiguity: l.121's packet lists "due and near-due obligations" and "active corrections or conflicts," which may or may not carry non-active lifecycle records. If they do, T inherits a false-positive surface L does not have, wired directly into a win condition. If they do not, then T's supersession machinery is invisible on this metric and contributes nothing observable — which loops back to P0-1. Fix class: packet specification. State explicitly whether non-active lifecycle records enter T's assembled packet. Either answer is defensible; the ambiguity is not.

P3-1 — The pilot is external where an internal pilot is both cheaper and more structurally honest. [SEARCHED]

l.362 excludes the 12 pilot scenarios from confirmation, and l.371 forbids by policy using pilot direction. The internal-pilot literature (Wittes & Brittain 1990 restricted design; Birkett & Day 1994 unrestricted — r1's "minimum 48, no maximum clamp" is structurally the unrestricted design, arrived at independently) keeps the pilot data in the final analysis, and blinded SSR estimates variance without unblinding arm labels, so direction cannot leak — structure instead of promise. Kieser & Friede: in the superiority case, blinded reassessment carries no relevant type-I inflation; the inflation results are for non-inferiority/equivalence. MBCX-01's primary comparison is a superiority test. Fix class: design substitution. Adopt a blinded internal pilot: recovers 12 paired scenarios (~1,200 primary decision calls) and replaces a policy prohibition with an analyst who never sees the labels.

8. WHAT WOULD YOU BUILD?

Three deterministic arms, a smaller budget, a direct runner, and a blinded internal pilot. Roughly r1 minus the Inspect branch, plus one arm.

(a) L / L+ / T, not L / T. L+ is the flat ledger with T's selection policy. One extra deterministic adapter, one extra cell per scenario, no new model capability. This is the whole P0-1 fix and it converts a bundled contrast into a two-step decomposition that can return three distinct actionable answers instead of one ambiguous one. Prior art: Meta's Full-bank-context vs Full-memory-agent ablation, which is exactly this decomposition run at n=278 — SEARCHED, opened at arXiv 2607.08716 Table 2.

(b) Lower the budget until it binds; do not inflate the world. EXECUTED: at r1's scenario minimums, Arm L lands at 1,570–2,362 tokens. A payload budget near 1,500 tokens makes the bounded contract engage at the stated scenario scale, keeps scenarios readable, and costs less per call. Pair it with the P0-2 invariant so the realized ratio is reported, not assumed.

(c) Direct async HTTP runner. Do not adopt Inspect for Stage A. r1 l.298 already makes framework adoption a convenience; the evidence says the convenience is negative here. Inspect's defaults that must each be affirmatively disabled: adaptive concurrency (on, max 100), local disk cache, provider prompt caching, checkpointing (which persists agent messages and resumes mid-sample, and whose setting is not in the log). SEARCHED. Every one of those is a hidden-state surface the experiment then has to prove absent. Liabilities the direct runner still has, named honestly: no built-in resume, so an interrupted confirmatory run must restart the affected scenario from a clean snapshot — which l.327 already requires; and no built-in retry accounting, so cell identity and attempt logging are hand-rolled and must be tested at Gate 2 (l.471–476 already specifies this).

(d) Borrow LongHorizon-Harness's audited-state record shape. MIT-licensed, pip-installable lh-harness, from AMAP-ML/DreamX. SEARCHED — opened the project page and repo metadata at origin. Its state record — requirement/artifact/fact entries with a four-value status enum (completed / pending / blocked / untrusted) plus the audit evidence behind each status — is a validated, published shape for Arm L, and the untrusted state is a mechanism r1 has no equivalent for: it distinguishes "not yet known" from "known false," which is exactly the conflict case T claims to handle (l.118). Borrow the record shape for L (fixing P1-1) and the untrusted state as a scenario stress. Do not borrow the MEA loop — it is a Stage B writer architecture.

(e) Blinded internal pilot. Per P3-1. SEARCHED — Wittes & Brittain 1990 / Birkett & Day 1994 / Kieser & Friede on the superiority case, opened via the internal-pilot bibliography and the R Journal SSR package paper.

Everything else in r1 I would keep: the two-stage program (l.69–92), the l.193–202 privilege tests, the fresh-interpreter reconstruction (l.255–266), the exact-endpoint provider posture (l.300–317), the order controls (l.321–328), and the four no-model gates (l.447–484).

9. WOULD YOU DESIGN IT DIFFERENTLY?

Yes, in one structural respect beyond the arms. r1 measures a single bundled contrast and interprets it as a claim about representation. I would run it as a staircase with a stopping rule at each rung, in ascending cost:

L → L+ (selection). If selection alone captures the effect, stop. Build the filter. This rung is cheap and, on Meta's evidence, is where ~40% of the available effect lives.
L+ → T (structure). Only this rung licenses "typed structure earns engineering."
T → T + retraction stress (versioning). The P2-2 mechanism, run as a declared sub-slice with its own preregistered threshold.

Same total cost as r1's two-arm design plus one adapter, but each rung returns a decision rather than a delta, and a null at rung 1 is informative rather than ambiguous.

Second difference: report the interpretation the design actually licenses. l.504 says a positive result "says the richer representation contributed measurable value." Under r1 as pinned, a positive result licenses only: "the typed contract — representation plus its derivation policy — beat a flat ledger dumped whole, at this budget, on this model." That is a narrower and still useful sentence. l.506's non-claims should carry it.

What I would not change. The staging discipline (l.81–92), the mechanical-scoring floor (l.356), the kill condition (l.412–420) — which correctly includes "the apparent advantage disappears when writer quality and output burden are matched" — and the authorization gates (l.532–542). r1's honesty about what Stage A cannot prove is the strongest thing in the document.

Both answers: READ-ONLY as proposals; the evidence beneath them is EXECUTED/SEARCHED as labelled.

9b. Packet §2 questions 3–5

3. Implementable without unstated gaps that change the answer? No. Four gaps change it: L's payload-overflow policy is unspecified (l.109 vs T's l.123); the due/lure split of the 30 opportunities is unspecified (l.219); the "conservative upper bound" level is unspecified (l.375); and whether T's packet carries non-active lifecycle records is unspecified (l.121). Each is one sentence to close.

4. Which r0 confounds are closed, which only moved? Closed: writer, output cap, provider endpoint, order, cold-restart label, oracle/gold, production leakage. Moved: budget-binding (from "not required anywhere" to "required only on a diagnostic slice") and sizing (from "silently underpowered" to "silently unaffordable"). Partially closed: comparator strength, hidden runner state, generator privilege.

5. What must be demonstrated before the first paid pilot call? Beyond r1's Gates 0–3: (i) L+ exists and is deterministic; (ii) realized Arm L payload exceeds the budget by the declared factor on every confirmatory seed; (iii) max-load output fixtures pass for all three arms — already demonstrated for the two-arm case by my probe, 396/512; (iv) the retraction-of-correction scenario family generates and validates; (v) a mock-provider transcript proving one in-flight request and no checkpoint/cache surface; (vi) a costed pilot envelope over the plausible SD range with the bound level named.

10. Omission attack
Required	Answer
Omitted strong simple comparator	Arm L+ — flat ledger with T's selection policy. Not in r1's arm set (l.96–138). It is the single cheapest arm that could make the whole experiment interpretable
Hidden confound favoring L	Lure immunity. L drops canceled/superseded obligations from the active set (l.107), so it cannot emit them as false positives. l.216–217 requires ≥8 lures and l.405 makes excess stale/wrong-scope action a win condition. L wins that condition by construction
Hidden confound favoring T	Due-ness computation. T's packet is "due and near-due obligations" (l.121) — the harness deterministically computing part of what the model is scored on. L gets triggers and must judge due-ness itself. This is an oracle-adjacent capability sitting inside the treatment
Framework/provider footgun	Inspect adaptive concurrency, on by default, max=100 (official reference, SEARCHED) — silently voids l.321–325's frozen order blocks. Runner-up: checkpointing resumes mid-sample with restored agent messages, and its setting is not recorded in the eval log
Persuasive false positive	P0-1 + P0-2 together: T wins because it filters, L never had to filter because nothing bound, the report attributes the win to versioning, and Moonwalker builds a supersession graph to get a due-date filter
Unfair kill of a useful kernel	P2-2: the update taxonomy (l.213) omits retraction-of-correction — the only mechanism where flat overwrite is unrecoverable and typed versioning is strictly necessary. The experiment omits the exam question T would ace
Machinery I would delete	The Inspect acceptance gate (l.286–298) in its entirety. Not because the checks are wrong — they are good — but because passing them costs more than the framework saves for a two-to-three arm, one-request-in-flight, action-only experiment, and l.298 already concedes framework adoption is "an engineering convenience, not an experimental objective." Delete the branch, keep the direct runner, and spend the saved effort on Gate 2's mock-provider transcript
Missing no-paid test without which I refuse pilot inference	A realized-budget-pressure report per confirmatory seed — Arm L's full serialization measured against the payload budget with the served tokenizer. Without it, nobody knows whether the bounded contract was ever under test, and my probe says at r1's stated scale it is not
Prior-art mechanism to borrow directly	Blinded sample-size re-estimation from the internal-pilot literature (Wittes & Brittain 1990; Birkett & Day 1994; Kieser & Friede on superiority-case inflation). Recovers 12 paired scenarios and makes l.371's direction prohibition structural rather than promissory. Runner-up: LongHorizon-Harness's status-plus-audit-evidence record shape for Arm L (MIT)
11. Sweep log
Query	Opened at origin	What decided it	Label	Effect
LongHorizon-Harness externalized state fresh executor agent benchmark	lh-harness.pages.dev (project page, full); repo/license metadata via api.github.com	§"Manager" — task state = requirement/artifact/fact records with completed/pending/blocked/untrusted status plus audit evidence; MIT; pip install lh-harness; AMAP-ML/DreamX (non-US/non-UK surface, satisfying §7)	SEARCHED	Produced P1-1 (a competent simple ledger keeps evidence refs) and the §8(d) borrow. Confirmed externalized-state gains are large but measure a different contrast than Stage A
"CAME-Bench" OR "MemoryArena" OR "Remember When It Matters" agent memory benchmark 2026	search → three real works located	All three exist: CAME-Bench arXiv 2601.10702; MemoryArena arXiv 2602.16313; Remember When It Matters arXiv 2607.08716	SEARCHED	No fabricated references in the packet's target list. MemoryArena's "complexity does not map monotonically" supports P2-3
Remember When It Matters full text	arxiv.org/pdf/2607.08716 (Meta AI, full paper)	Table 2 ablation: same bank, dumped (61.5/58.6) vs selected (64.3/61.2) vs baseline (57.5/55.0); Mem0 retrieval 62.1/60.8	SEARCHED	The decisive source. Converted P0-1 from hypothesis to measured effect; produced P2-3; anchored effect sizes (2.4–10.0 pp at n=50–278) for P1-3
Inspect AI checkpointing docs checkpoint failure resume eval-set retry semantics	inspect.aisi.org.uk/checkpointing.html; inspect.aisi.org.uk/reference/inspect_ai.html	Checkpointing resumes mid-sample, restoring agent messages and compaction; --checkpoint not recorded in the log; eval_set adaptive concurrency default enabled, max=100	SEARCHED	Produced P1-4 and the §10 deletion. Refuted the sufficiency of r1's l.288–297 gate
internal pilot blinded sample size re-estimation Wittes Brittain Birkett Day	Wiley/Stat.Med. abstracts, MCW internal-pilot annotated bibliography, R Journal RJ-2022-001	Restricted vs unrestricted designs; blinded SSR keeps the analyst from seeing arm labels; superiority case carries no relevant type-I inflation	SEARCHED	Produced P3-1. Confirmed r1's no-clamp rule is the published unrestricted design, arrived at independently
Inspect solver/caching + OpenRouter provider routing	inspect.aisi.org.uk/{solvers,caching}.html; openrouter.ai/docs/guides/routing/provider-selection — opened earlier in this same conversation, under the prior round	generate() auto-appends to messages; local disk cache; Anthropic prompt caching auto-managed by OpenRouter; base slug spans all endpoints; account-wide provider lists merge with per-request	SEARCHED (disclosed: opened earlier in-session, not re-fetched this round)	Confirmed C8 CLOSED by l.307/l.315/l.317, and supplied the caching half of P1-4
PM-Bench / AgenticSTS	not re-opened this round	—	RECALLED	Both are real and were opened at origin earlier in this session. Neither runs the deterministic-typed-vs-deterministic-flat contrast at matched writer and budget, so neither makes Stage A obsolete. Admissible here as argument only; it is not the deciding evidence for any finding above
Harbor / OpenAI Evals / tau2-bench as harness alternatives	not opened	—	UNSEARCHED — NOT-LOAD-BEARING	The harness decision turns on hidden-state surface, and I have direct primary evidence for the two paths r1 actually names (direct runner vs Inspect). A third framework cannot beat "no framework" on hidden-state count

Why I stopped. Each load-bearing external claim resolved against a primary source opened at origin, and two of them changed a finding's status (Meta's ablation created P0-1's evidentiary basis; Inspect's reference refuted the gate's sufficiency). The remaining unsearched item cannot change the design decision.

12. Residual risks and explicit non-claims

Residual risks:

Tokenizer approximation. o200k_base via npm; tiktoken's BPE endpoint is blocked from my container. All margins are ≥2×, but absolute counts will shift on a non-OpenAI endpoint. The P0-2 conclusion should be re-run at Gate 1 with the served tokenizer.
Payload realism. My Arm L/T fixtures are my constructions from l.100–121, not r1's. If real records are 3× my length, P0-2 weakens; if shorter, it strengthens. The fix I propose (measure and report realized pressure) is robust to this either way.
Meta's ablation is a different task and a model-written bank. τ²-Bench conversational tool use, Opus-4.6-written memory. It is Stage-B-shaped, not Stage A. I claim it establishes that selection is a separable, sizeable effect, not that its magnitude transfers to MBCX-01.
Inspect findings are documentation-derived. I did not run Inspect. Doc claims are primary for what the vendor states, not for what the code does.
C11 accepted largely on reading. The oracle-packet-transcribes-the-answer adversary would need a constructed oracle policy to test properly; l.132's oracle-all-relevant variant addresses it in principle and I did not probe it.
Sealed and single-pass. I did not open the three prior-round verdict files in the working directory and have not seen any other seat.

Explicit non-claims:

I do not claim Stage A is obsolete. Nothing I opened runs deterministic-typed vs deterministic-flat at matched writer and budget. The question is live.
I do not claim Arm T will lose. I claim that as pinned, a T win is not attributable to representation, and a T loss is partly pre-arranged by an incomplete update taxonomy.
I do not claim the 12-pair pilot is statistically unsound. It is sound; my finding is that it is uncosted.
I do not claim Inspect is unusable — only that its defaults impose a verification burden this experiment does not need to carry.
I did not analyze licensing as a validity question, per §1.2. The MIT/Apache facts appear only as borrowability data.
No fix in this verdict was applied. No paid inference was run. No model call of any kind was made.
13. Seat capability report
Model: Claude, Opus 5. Single sealed council seat, independent pass.
Harness: Anthropic chat interface with Moonwalker MCP tool surface, a Linux probe container, and web search/fetch.
Local reach: Windows host via moonwalker_shell_exec (pwsh) — git object reads at the pin, SHA-256/384 verification, line-addressed reads of all 542 artifact lines and all 364 packet lines, manifest hash verification. Read-only throughout.
Search reach: native web search plus full-page fetch at origin. Seven external sources opened; five decided a finding. Non-US/non-UK surface covered (AMAP-ML/DreamX, Alibaba). Native search was sufficient; I did not need Moonwalker locator/fetch fallbacks.
Execution reach: Node + Python in an isolated container with network to npm/PyPI/api.github.com. Six probes executed: pin/manifest verification, max-load payload and output fixtures, per-record verbosity, metric granularity across three due/lure splits, sizing sensitivity plus a 20,000-draw Monte Carlo of the full pilot→n→power procedure, and a hand-traced adversarial scenario shape.
Limitations: tiktoken BPE download blocked (worked around via npm-bundled encoding); no non-OpenAI-family tokenizer obtainable offline; no Inspect or OpenRouter runtime execution — those findings are documentation-derived and labelled; no paid inference, correctly, per l.13 and packet §11; and I did not open the other seats' verdicts, which were present on disk and untracked.

Roll Tide 🐘
