MBCX-01 DESIGN COUNCIL — ROUND 1 VERDICT
1. Verdict

GO-WITH-FIXES(P0 — treatment isolation: the shared 512-token output cap structurally starves Arm B, the primary baseline)

The experiment is worth running and the falsification architecture is unusually honest — preregistered kill condition, oracle ceiling, deterministic scorers, explicit non-claims. But as pinned it cannot answer its own primary question, because the arm it is designed to beat is handicapped by a numeric parameter nobody appears to have costed. Three of the fixes below must land before Gate 1, not before Gate 3.

Basis: EXECUTED (probes run against the pinned bytes and against primary docs I opened this session).

2. Pin / byte verification
Check	Result
Packet repo HEAD	95c2b359afb59b1f4e1b096d402a3106c44da339 ✓ matches commission
git status --porcelain	empty — clean tree, so working-tree reads == committed bytes
Artifact blob at 5c7ccfe…	ea858233aa73b3a8c600972a74d232b3979eae7e
Same blob at packet commit 95c2b35…	ea858233… — identical; the pin did not move under the packet
Artifact SHA-384 (computed)	B1D907E2C7D6B247D109B5E192541442ED07B51EAFA18A28ADCFC418B72494FBCD588B55C0504D4F44ACB2F3333007CE — matches packet §0 exactly
Size / lines	36,869 bytes / 793 lines
Diff 5c7ccfe → 95c2b35	additive only: packet + manifest, 277 insertions, spec untouched
Manifest §B–C local sources	all 7 SHA-384 pins verified MATCH=True on disk

I read the artifact from git cat-file blob 5c7ccfe…:MBCX-01-DESIGN-SPEC-r0.md piped to a temp file, not from the working tree. Line numbers below are 1-indexed against that pinned blob.

Bytes I created (probe-transient only, disclosed): %TEMP%\mbcx01-pinned.md, %TEMP%\mbcx01-manifest.md on the Windows host; /home/claude/probe.mjs, /home/claude/probe2.mjs in my container. No repo, vault, or artifact writes. No verdict banked to disk.

3. Sources actually read

Pinned local (byte-verified): MBCX-01-DESIGN-SPEC-r0.md @5c7ccfe (full, 793 lines) · MBCX-01-DESIGN-COUNCIL-PACKET-r1.md @95c2b35 (full) · LOCAL-SOURCE-MANIFEST-r1.md @95c2b35 (full) · SHA-384 verification of manifest items 2–8 (hashes only; I did not read their contents — the artifact is self-contained enough to adjudicate and the manifest itself says their numbers are proposals, not inherited truths).

External primary (opened at origin this session): arxiv.org/html/2607.12385v1 (PM-Bench, full incl. Tables 1–3, 6, 7 and Appendix A.5 prompts) · arxiv.org/abs/2607.02255 + alayalab.github.io/AgenticSTS + github.com/AlayaLab/AgenticSTS (AgenticSTS) · inspect.aisi.org.uk/solvers.html · inspect.aisi.org.uk/caching.html · openrouter.ai/docs/guides/routing/provider-selection · openrouter.ai/docs/guides/features/message-transforms (via search-result body) · api.github.com/repos/{genglinliu/PMBench, AlayaLab/AgenticSTS} + /license.

4. Claim scoreboard
	Claim	Verdict
C1	Smallest decisive next test	UNDERDETERMINED — the question is right, the five-arm custom harness is not justified against an Apache-2.0 shelf item nobody evaluated (see §6, ALREADY-BUILT)
C2	Treatment isolation is real	FALSE — P0-1. Arm B pays a mandatory output tax no other arm pays
C3	Baseline set strong enough to kill the idea	FALSE as specified — Arm A never actually operates under budget pressure at the specified scale (P1-1), so the "strong ceiling" baseline is a full-context arm by accident, and Arm B is weakened by P0-1. Both distortions point the same way: toward a spurious Arm D win
C4	Inspect is neutral and workable	UNDERDETERMINED, one sub-claim CONFIRMED-HOSTILE — messages is auto-appended by generate() (confirmed at origin); local disk cache is an undocumented-in-spec cross-restart continuity surface (P1-2)
C5	OpenRouter can be frozen tightly enough	FALSE as specified — "one named provider" does not pin an endpoint; account-wide lists merge with per-request; OpenRouter auto-manages Anthropic prompt caching and extended context (P1-3)
C6	Statistical plan supports the verdict	UNDERDETERMINED, leaning FALSE — pilot n=4 estimates the paired SD to within a factor of 3.7, i.e. required n to within a factor of 13.9; the clamp silently converts a power calculation into a budget (P1-6)
C7	Restart is represented honestly	FALSE (labelling) — "cold restart" appears at l.18, 52, 80, 116, 736 and titles §8; l.277 says it "must occur inside the same foreground harness process"
C8	Generated world valid and non-privileging	UNDERDETERMINED — invariants (l.241–252) are good but contain no budget-pressure invariant and no numeric memory-necessity bar; Arm E is defined in contradiction with invariant 1 (P1-5)
C9	Implementation burden proportionate	FALSE in one module — §12.2 safety + §14.3–14.4 build child-process ownership machinery for children §14.2 forbids (P1-7)
C10	Reproducibility fields complete	UNDERDETERMINED — no hash algorithm named anywhere (l.294, 344, 509, 633–634, 643, 758); no arm order, no cache state, no account-level routing policy, no temperature value
5. Findings
P0-1 — Arm B is starved by the shared output cap. The primary comparison measures the cap, not the memory. [EXECUTED]

Bytes. l.182: "Output is limited to 512 tokens and must follow a strict JSON schema." l.538: "Output limit: 512 tokens per decision." l.354–361: one JSON object containing ongoing_choice, action_ids, channel_queries, state_claims, provenance_ids, and "ledger only for the ledger arm." l.116: the ledger carries obligation ID, action, trigger, scope, dependencies, status. l.218: ≥12 prospective obligations per confirmatory scenario. No exemption for Arm B exists anywhere in the file.

Probe (o200k_base BPE, run offline via gpt-tokenizer):

Output	Tokens
Decision object alone (Arms A/C/D/E)	54
Decision + spec-faithful 12-obligation ledger	790 — exceeds the 512 cap
Decision + maximally abbreviated 12-obligation ledger (single-letter keys, truncated action/trigger text)	436 — fits
Same abbreviated ledger at 16 obligations	568 — exceeds

Mechanism. Arm B must fit 12+ obligations into ~38 tokens each while Arms A/C/D/E spend 54 tokens total on the whole response. Abbreviation is therefore mandatory for Arm B and impossible for it above ~14–15 obligations — and l.228 explicitly permits counts to vary upward from the 12 minimum. Every token Arm B spends maintaining memory is a token it cannot spend deciding. Under l.363, a ledger that overruns becomes malformed output → one repair call → "execution failure."

Independent corroboration. PM-Bench's own todo-ledger prompt hard-caps the ledger at 5 items with notes ≤8 words (Appendix A.5, "Todo-ledger addendum" — SEARCHED). The authors hit this constraint and solved it by capping. MBCX-01 cites PM-Bench's ledger result (l.118) without inheriting the cap that made it work.

Experimental consequence. The primary estimand (l.90) becomes typed projection vs. a ledger under a compression constraint no other arm faces. A win is uninterpretable; a loss would be remarkable. This is the "persuasive but false positive" pathway.

Fix class: treatment-budget symmetry. Give memory-maintenance output its own budget outside the decision cap (separate tool call or separate output channel), log ledger tokens as a covariate, and preregister the ledger item cap as a declared arm parameter rather than an emergent artifact.

P1-1 — The budget never binds on Arm A, so the word "bounded" is untested. [EXECUTED]

Bytes. l.182: 6,000-token memory payload. l.215: 36–48 decision steps. l.110–112: Arm A preserves original text, drops oldest first, and is labelled full_history_fits "on short calibration scenarios" — implying confirmatory scenarios should not fit. §7.4 (l.241–252) contains no invariant requiring that.

Probe. A realistic admitted public observation carrying the l.161–168 fields plus one sentence of narrative = 64 o200k tokens. Full history: 36 steps → 2,304 tokens; 48 steps → 3,072 tokens. Both fit inside 6,000 with roughly 2× headroom. The budget binds only if the mean observation exceeds ~125 tokens at 48 steps / ~167 at 36.

Consequence. Secondary hypothesis 6 (l.84, "will degrade or become infeasible under an equal bounded budget") is not merely unsupported — it is unreachable at the specified scale. Arm A silently becomes a full-context arm, which is the strongest baseline, and win condition 3 (l.416, "not more than 0.02 below the strongest non-oracle baseline") then gates on a comparison the design claims it is stressing.

Fix class: generator invariant. Add a machine-checked invariant that full chronological history exceeds the payload budget by a preregistered factor k in every confirmatory scenario, and report the realized ratio per scenario.

P1-2 — Two caching surfaces the spec never mentions; one can fake the stability audit. [EXECUTED · SEARCHED]

Bytes. "cache" appears at exactly two places: l.505 (freeze cache prices) and l.621 (delete run-owned caches). Nothing else.

Source (inspect.aisi.org.uk/caching.html, opened). Inspect maintains a local disk cache keyed on model name + message history + epoch + generate config + tools, default expiry one week, directory overridable via INSPECT_CACHE_DIR. Separately: "The Inspect cache-prompt option will by default attempt to make maximum use of provider caches" for Anthropic.

Source (openrouter.ai provider-selection, opened). "OpenRouter manages some Anthropic features automatically: Prompt caching and extended context are enabled based on model capabilities."

Two distinct mechanisms:

(a) Stability audit forgery. §11.7 (l.440) randomly selects 20% of cells and runs two extra replicates. Arm D's bounded packet is deterministic by construction (l.346). If --cache is on — or an INSPECT_CACHE_DIR is inherited — identical prompts are served from disk and the replicates return byte-identical outputs with zero within-cell variance. The one instrument designed to detect nondeterminism would report perfect stability for the arm most able to trigger the cache, and the report would be sincere.
(b) Cost/latency estimand contamination. Secondary estimand l.99 measures "prompt tokens, latency, and cost per correct prospective action." Arm A appends to a stable prefix and caches beautifully; Arm D recomputes a changing packet and caches ~not at all. Anthropic cache reads cost ~90% less. Arm A's cost-per-correct-action is systematically flattered by a mechanism that is default-on at two layers and disabled by neither §6.3 nor §13.2. l.520 disables context-compression plugins; nothing disables prompt caching.

Fix class: state-surface enumeration. Prohibit the Inspect local cache explicitly in the frozen config, set cache_prompt=false, and record the four-way token split (I / CW / CR / O) per call as a first-class validity field.

P1-3 — "One named provider" does not pin an endpoint, and account settings silently merge. [SEARCHED]

Bytes. l.517: "Restrict routing to one named provider." l.525 invalidates a cell only if "a different model or provider served the request."

Source (openrouter.ai/docs/guides/routing/provider-selection, opened at origin):

"When you use a base provider slug (e.g. "google-vertex") in any provider routing field (order, only, or ignore), it matches all endpoints for that provider, including any variants or regions." A base slug spans google-vertex/us-east5, google-vertex/us-central1, deepinfra vs deepinfra/turbo, etc. — different hardware, different regions, potentially different quantization, all satisfying "one named provider."
"when you allow providers for a specific request, the list of allowed providers is merged with your account-wide allowed providers" — same for ignore, and request-level zdr ORs with account-wide. The frozen manifest (§13.1) records per-request config only; the effective routing policy lives partly in account state the manifest never captures.
allow_fallbacks defaults true, require_parameters defaults false — the spec sets both correctly. That part of C5 holds.

Consequence. A confirmatory block could straddle two regional endpoints without ever tripping l.525, and a later account-settings change makes the run unreproducible without any diff to the frozen config.

Fix class: routing identity. Require the full endpoint slug (with suffix) in only, snapshot the account-wide privacy/provider settings into the manifest, and treat a change in the returned endpoint slug — not just the provider name — as cell-invalidating.

P1-4 — No arm-order randomization, and §14.2 makes sequential execution mandatory. [EXECUTED — grep of pinned bytes]

The only occurrence of "random" in 793 lines is l.440 (random 20% cell selection). There is no interleaving, counterbalancing, or blocking scheme. Meanwhile §14.2 (l.571–573) mandates max_tasks = 1, max_connections = 1–2, adaptive concurrency disabled. The process-safety posture forces the arms into a long serial sequence and the design then omits the one control that makes a serial sequence interpretable. Provider drift, rate-limit behavior, and time-of-day effects are perfectly confounded with arm if arms run blocked. This is the driver's attack #5, and the interaction with §14.2 makes it worse than it looks.

Fix class: run-order design. Randomize arm order within scenario, record arm order and provider timestamp per cell as a §15 field, and preregister a sensitivity analysis on run-time position.

P1-5 — Arm E is defined in direct contradiction with the packet's first invariant. [EXECUTED]

l.145: Arm E assembles "the smallest gold-derived packet sufficient to make the correct current decision." That packet is a model prompt. Against: packet §3 invariant 1 — "Private gold never reaches any memory adapter, model prompt, provider request, retrieval index, or arm artifact"; spec l.486 — "The solver never receives private gold"; win condition 7 (l.420) — no "gold leakage" occurred.

Either Arm E bypasses the solver through an undefined path, or three invariant statements are false as written. Worse, invariant l.252 requires that "Oracle-minimal packets reproduce the exact gold action set" — checked mechanically before any model call. A packet whose sufficiency is deterministically verifiable without a model is a packet that encodes the answer; the "remaining reasoning error when retrieval and state selection are perfect" (l.145) then measures the model's ability to transcribe, not to reason. That degrades the §17 (l.730) claim that the oracle arm distinguishes reasoning failure from memory-selection failure.

Fix class: invariant scoping. Carve Arm E out of the gold-isolation invariants explicitly, state which surface it is exempt from and why, and redefine l.252 as "an oracle policy over the packet reproduces the gold set" rather than "the packet reproduces the gold set."

P1-6 — The pilot cannot size the confirmatory run, and the clamp hides that. [EXECUTED]

Bytes. l.396–400: four pilot scenarios; n = ceil(((z_0.975 + z_0.80) * paired_sd / 0.08)^2); clamp to [24, 48].

Arithmetic probe:

(z₀.₉₇₅+z₀.₈₀)² = 7.8489. The clamp honours the formula only for paired SD ∈ [0.1399, 0.1978]. Outside that window the formula is decorative.
SD 0.20 → n=50 → clamped to 48 (power 0.79). SD 0.25 → n=77 → clamped to 48 (power 0.60). SD 0.30 → n=111 → clamped to 48 (power 0.46).
Pilot n=4 gives 3 df. The 95% CI for the true SD is [0.566, 3.729] × ŝd → required n is uncertain by a factor of [0.32, 13.9].

Is a large SD plausible? I checked against the only published paired data on this exact metric. PM-Bench Table 3 (8 backbones × scaffolds, opened) gives paired SDs of 0.069–0.105 for scaffold-vs-ledger differences — comfortably inside the clamp. That evidence cuts against my initial worry and I report it as such. But it is not the right quantity: PM-Bench pairs across models on one 81-task week; MBCX-01 pairs across scenarios on ~13 high-stress items each. Which brings the sharper problem —

The target effect is roughly one obligation. From §7.2 minimums (l.219–222): 4 cross-boundary + 4 updates + 2 dependency + 3 hidden-channel = 13 gold due items in the high-stress slice. At a realistic operating point (TP=8, FP=3, FN=5), one additional correct obligation moves set-F1 by +0.053. The preregistered +0.08 threshold is ~1.5 obligations per scenario. A per-scenario outcome built on 13 items is far lumpier than PM-Bench's 81-task macro, so the between-scenario SD is plausibly 0.15–0.25, not 0.09 — squarely in the region where the clamp ceiling binds and power falls below 0.8.

The +0.08 threshold also has, as the driver noted, no cost/value derivation anywhere in the file. It now additionally lacks a measurement-granularity justification.

Fix class: estimand and sizing. Derive +0.08 from something (obligations-missed-per-week that a customer would notice); enlarge the high-stress slice so the target effect is ≥3 quanta; replace normal-theory CI on a bounded discrete outcome with a scenario-clustered paired bootstrap; and either remove the clamp or preregister the action when required n exceeds it (run fewer arms, not fewer scenarios).

P1-7 — The safety module builds child-process machinery the design forbids. [EXECUTED]

§14.2 (l.571–580): max_subprocesses = 1, no sandbox provider, no Docker, no local model server, no GPU, no background control server, no auto-launched viewer. §14.3 (l.586) then builds a run lock plus "a registry of child PIDs it creates" with parentage-and-creation-time matching. §14.4 (l.590–602) specifies a nine-step shutdown including "ask registered child processes to exit" and "terminate only surviving registered children." §16 Gate 0 (l.663) requires "Cleanup tests using harmless short-lived child processes created by the test itself" — the test must manufacture children in order to exercise machinery for children the architecture prohibits.

This is Moonwalker production process-ownership doctrine imported wholesale into a lab instrument. It is exactly the pattern the packet's own "bigger than the bug" clause and the manifest's proportional-transfer ruling (l.71: "Not inherited into MBCX-01: … the full code-delivery/PR workflow") tell the seats to reject.

Fix class: scope deletion. Keep the run lock, the unique run directory, and flush-on-exit. Delete the child-PID registry, the parentage matching, the nine-step shutdown, the stale-lock audit, and Gate 0's child-process cleanup test.

P2 findings
P2-1 — Restart label. "cold restart" at l.18, 52, 80, 116, 736 and §8's title, against l.277 "inside the same foreground harness process." Fix class: vocabulary — call it in_process_reconstruction everywhere, reserve "cold" for a subprocess panel that does not yet exist.
P2-2 — No temperature value. l.193 lists "Temperature and supported seed" as things to hold equal; no value appears in the file. l.508 records "seed support" as a discovered property, i.e. seed may be unavailable. With one run per main cell (l.440) and unstated temperature, the primary result may be a single draw from a stochastic process. Fix class: frozen parameter — pin temperature (0 if supported) in §13.1 and state the fallback when seed is unsupported.
P2-3 — Hash algorithm unnamed. l.294, 344, 509, 633, 634, 643, 758 all say "hash." Per manifest l.70 this is "narrowly live." Fix class: declaration — either bind SHA-384 or state in one line that lab hashes are identity-only and non-normative. Do not open seal-chain design here.
P2-4 — No numeric bar for memory necessity. l.149: the no-memory arm exists "to confirm that generated scenarios genuinely require memory" with no threshold. Fix class: preregistered criterion — e.g. no-memory high-stress set-F1 below a stated ceiling, checked before Gate 3.
P2-5 — Status contradiction. l.5 "Approved architecture; specification awaiting owner review" vs l.10 "not authorized to run" vs l.793 "Approval of this document authorizes implementation planning only." Fix class: status vocabulary — one state word.
P3 findings
P3-1 — PM-Bench characterization is directionally right but drops the constraint that matters. l.30's numbers check out at origin: 80 total steps (Table 1), 7-day week, 8 backbones × 8 configurations, deterministic seeded generation with rejection sampling, best aggregate macro set-F1 65.1% (optional-heartbeat), no scaffold dominating (Table 3). l.118's "strong low-noise scaffold" is verbatim-faithful — todo ledger ranks second at 62.8% with the lowest aggregate FP. What is dropped: that ledger was capped at 5 items. See P0-1.
P3-2 — Licensing is worse and better than the driver's note. [EXECUTED via api.github.com] genglinliu/PMBench returns license: None — not "not exposed," but absent, i.e. all rights reserved; treat definitions and paper as prior art and copy nothing. AlayaLab/AgenticSTS returns NOASSERTION because it is a monorepo with split licensing, and its root LICENSE map reads: AgenticSTS/ (Python agent: decision engine, memory, skills, tooling) Apache-2.0; AgenticSTS-Mod/ (C# game mod) AGPL-3.0; AgenticSTS-Data/ CC BY 4.0. The component MBCX-01 would actually want is permissively licensed. l.22 lumps the two repos together and gets both wrong.
6. Build-decision challenge (required of every seat)

1. ALREADY-BUILT? — Partially, and the closest match was never evaluated as an adopt target. [SEARCHED]

I searched and opened: PM-Bench (paper + repo + license API), AgenticSTS (paper + project page + repo + LICENSE text), and scanned the surrounding 2026 benchmark cluster surfaced in PM-Bench's own related-work and in the EvoMemBench/AMA-bench/AMemGym reference lists (MemoryBench, RealMem, Mem2ActBench, LongMemEval, MemBench, AMA-bench, AMemGym, Evo-Memory).

Nothing on the shelf answers MBCX-01's causal question. PM-Bench evaluates prospective memory but supplies scaffolds, not a matched memory-representation contrast under equal budget, and releases exactly one fixed week — no scenario-level replication, which is MBCX-01's clustering unit. AgenticSTS instantiates a bounded typed contract but its own headline result is 3/10 → 6/10 with Fisher exact p≈0.37, and the paper states plainly that accumulating-context baselines are "operational comparisons rather than controlled tests of the contract variable itself." So l.32's characterization is correct and the gap is real.

But: AgenticSTS's repo lists, under Good first contributions, "Add the accumulating-context comparison cell (see Future Work)" — the authors are inviting exactly the experiment MBCX-01 proposes to build from scratch, on an Apache-2.0 codebase that already implements typed layers, per-decision fresh-message assembly, ablation, frozen store snapshots, and 298 released trajectories. The spec's only engagement with this (l.22) is a code-copy hazard warning. A shelf-check that never asked "can we extend theirs?" is not a shelf-check. That is the deciding gap in C1.

The honest counterweight, which I hold: AgenticSTS's domain is Slay the Spire 2, its long-horizon pressure is tactical rather than obligation-shaped, and its ablation harness may not carry cancellations/supersessions/scope isolation at all. Adopting it may cost more than it saves. But that comparison has to be made and written down, not skipped.

2. PRODUCT-FIT? — Yes, and I can state the customer need in one sentence. An operator running Moonwalker over days needs the conductor to still know what is currently true and what is still owed after the conversation is gone — and needs to know whether paying for typed structure buys that, or whether a durable ledger already does. That is GOVERNED POWER / FAIL-LOUD: l.184 (budget failure is structured, silent truncation invalidates the cell), l.139 (packet builder fails closed rather than dropping a dependency), l.363 (no LLM judge silently repairs malformed output), §11.5 kill condition. It is MIRROR-NOT-COP: the scorer measures, the preregistered rule decides, the owner holds the gate (l.750–763).

One drift risk: §12.2's nine-module layout with a providers manifest layer, a safety module, and per-arm adapter interfaces is production-platform shaped. The spec names this risk itself (packet §2, "must not accidentally become a shadow production architecture") and P1-7 is where it already happened.

3. BIGGER-THAN-THE-BUG? — In one module, yes. §12.2 safety + §14.3 + §14.4 + Gate 0's child-process cleanup test is a process-ownership subsystem answering a risk the design forbids by construction (§14.2). It should not ride this experiment's approval. Everything else is proportionate.

Labels: ALREADY-BUILT = SEARCHED. PRODUCT-FIT = READ-ONLY (byte-derived). BIGGER-THAN-THE-BUG = EXECUTED (grep of pinned bytes).

7. WHAT WOULD YOU BUILD?

Smallest architecture that can actually answer the question. Four changes, roughly 40% less code than the pinned design.

(a) Two arms at Gate 3, not five. D vs B only, powered. A, C, E become descriptive companions run on a fixed subset — they inform interpretation and cannot consume the confirmatory error budget anyway (l.408 already concedes this for E). This roughly halves inference cost, which buys back the scenarios P1-6 says you may need. Prior art: PM-Bench's own finding that no scaffold dominates across backbones (SEARCHED, Table 3) — a five-way comparison on one backbone was never going to generalize, so pay for depth on the decisive contrast instead of breadth on the others.

(b) Symmetric memory-maintenance channel. Both maintenance-writing arms emit memory state through a separate tool call with its own token budget, never inside the 512-token decision object. Log maintenance tokens per step as a covariate and report cost-per-correct-action both raw and maintenance-adjusted. This is the P0-1 fix and it is the difference between measuring representation and measuring the cap. Prior art: PM-Bench Appendix A.5's ledger cap is the workaround; making the channel separate is the correction (SEARCHED).

(c) The decision is the Inspect sample; the trajectory lives in a checkpointed store. One scenario as one sample is what creates the retry-granularity problem (driver attack #4) and the accidental-history problem simultaneously. Make each decision a sample keyed (scenario_seed, arm, step), carry trajectory state in an explicit store with a checkpoint written after every step, and build the message list fresh from the store every time. Then eval-retry resumes at the step, not the scenario, and "fresh conversation" is structural rather than disciplinary. Inspect exposes a Checkpointing doc page — SEARCHED for existence in the nav of the two pages I opened; I did not read its contents and am not claiming its semantics. The generate()-appends-to-messages behavior is SEARCHED and confirmed at solvers.html.

(d) Adopt AgenticSTS's Apache-2.0 agent package as the Arm D substrate, or write one paragraph saying why not. [SEARCHED — LICENSE text read via api.github.com] Their typed-slot assembly, ablation switches, and frozen-snapshot discipline are the parts MBCX-01 would otherwise rebuild. The AGPL exposure is confined to the C# game mod, which MBCX-01 has no use for. This is the shelf-first move the spec claims to be making.

Scenario generator: keep it. It is the genuinely novel contribution — nothing on the shelf produces replicated obligation trajectories with cancellations, supersessions, scope isolation, and dependency closure at scenario-level replication. Add the budget-pressure invariant (P1-1) and the memory-necessity bar (P2-4).

8. WOULD YOU DESIGN IT DIFFERENTLY?

Yes, in three respects, and one of them is scientific rather than engineering.

(i) Make the outcome less lumpy before touching the statistics. The +0.08 threshold is ~1.5 obligations out of 13 (EXECUTED, §5/P1-6). No amount of statistical machinery fixes an effect size that sits at the measurement quantum. I would raise the high-stress slice to 30–40 scored items per scenario — longer trajectories or denser obligation load — so the target effect is several quanta wide, then size the study. This is cheaper than the alternative (many more scenarios) because per-scenario cost scales with steps while variance scales with items.

(ii) Replace the fixed-n-with-clamp plan with an internal-pilot design and a clustered bootstrap. Preregister a rule that re-estimates n at an interim point using the accumulating paired SD (not the observed direction), with the alpha adjustment stated up front; report the primary interval as a scenario-clustered paired bootstrap rather than a normal-theory CI on a bounded discrete outcome. Prior art: internal-pilot / sample-size re-estimation designs (Wittes & Brittain; Birkett & Day) — RECALLED, not opened this session, and admissible here as argument only. The bootstrap recommendation rests on the arithmetic in P1-6 and on the outcome's own boundedness, not on recalled literature.

(iii) Run the restart panel for real, or drop the word. l.277 defers process-level recovery. Either add a genuine subprocess panel on a small scenario subset — spawn, kill, restart from artifact — or rename the metric in_process_reconstruction_rate throughout and remove "cold" from §4.2, §18, and the hypothesis at l.18. A 95% threshold (l.418) on a serialization round-trip is close to a tautology for Arms A/C/D, which persist immutable records; the interesting failure is Arm B's, whose artifact is a model-authored ledger. The restart hypothesis is really a hypothesis about Arm B, and the design does not say so.

What I would keep unchanged: the public/private envelope split (§6.1), the invariant ledger and pre-model exclusion (l.254), the deterministic-admission isolation stage with the explicit non-claim that it does not prove the write path (l.199–203) — that is the single best piece of scientific hygiene in the document — the preregistered kill condition (§11.5), the no-optional-stopping rule (l.436), and the ban on LLM judges overriding mechanical metrics (l.384).

9. Omission attack
Required	My answer
Omitted prior-art comparator	A deterministic, non-model-maintained compact obligation ledger — a rule-based projection with no typed versioning, no supersession graph, no provenance. It separates "structure helps" from "this much structure helps," and it is the arm that could show the whole typed data model (§9) is overbuilt. The spec's baseline set cannot distinguish those two hypotheses.
Unmeasured confound	Output-token budget consumed by memory maintenance (P0-1). Never measured, never reported, never equalized — and it is perfectly correlated with arm.
Implementation footgun that silently biases	Inspect's local disk cache (P1-2a). Persists across process restarts, keyed on the message history that Arm D generates deterministically, and would make the stability audit report perfect within-cell variance for the favored arm.
Harness machinery I would delete	§12.2 safety + §14.3 child-PID registry + §14.4 nine-step shutdown + Gate 0's child-process cleanup test (P1-7). Zero children exist by §14.2's own constraints.
Missing artifact/test without which I refuse paid inference	A Gate 0 output-budget conformance test: render each arm's maximum-load response with the served model's tokenizer and assert every arm fits its cap with equal headroom. This test would have caught P0-1 before a dollar was spent, and it is exactly the kind of thing §16's list does not include.
How it produces a persuasive false positive	Three independent mechanisms all pointing the same way: Arm B truncated by the output cap; Arm A's budget never binding so its "bounded degradation" never appears; prompt caching flattering Arm A's cost metric while Arm D wins on accuracy. Arm D wins the primary, clears win conditions 1–3, and the report reads clean — because every logged invariant held.
How it kills a useful kernel unfairly	The clamp at n=48 with a true paired SD near 0.25 gives ~0.60 power (EXECUTED). A real +0.08 effect fails to clear the CI, §11.5's kill condition fires on an upper bound below +0.03, and a working kernel is abandoned on an underpowered study whose sizing formula was overridden by a budget constant.
10. Sweep log
#	Query	Opened (URL)	What decided it	Effect
1	PM-Bench prospective memory Genglin Liu Saadia Gabriel arXiv	arxiv.org/html/2607.12385v1 — Table 1, Table 2, Table 3, §4.1, App. A.5	Table 1 total steps = 80; Table 2 best macro set-F1 = 65.1% (heartbeat-optional), ledger 62.8% with lowest FP; Table 3 no scaffold dominates; A.5 ledger prompt caps at 5 items	SEARCHED. Confirmed l.30 and l.118. Produced the corroboration for P0-1 and the paired-SD anchor for P1-6
2	AgenticSTS bounded-memory testbed arXiv 2607.02255	arxiv.org/abs/2607.02255, alayalab.github.io/AgenticSTS, github.com/AlayaLab/AgenticSTS	Bounded/typed/ablatable contract confirmed verbatim; paper states accumulating-context baselines are operational, not controlled; repo invites "add the accumulating-context comparison cell"	SEARCHED. Confirmed l.32. Created the ALREADY-BUILT finding
3	(API) repos/genglinliu/PMBench, repos/AlayaLab/AgenticSTS + /license	api.github.com	PMBench license: None; AgenticSTS root LICENSE = monorepo map, Apache-2.0 for the Python agent, AGPL only for the C# mod, CC BY 4.0 data	SEARCHED + EXECUTED. Sharpened driver attack #9 in both directions (P3-2)
4	Inspect AI solver TaskState messages generate appends	inspect.aisi.org.uk/solvers.html	"messages … is automatically appended to by the generate() solver"	SEARCHED. Driver attack #2 confirmed at origin
5	(nav from #4) Inspect caching	inspect.aisi.org.uk/caching.html	Local disk cache keyed on message history, INSPECT_CACHE_DIR, 1-week default; cache-prompt defaults to maximum provider-cache use, Anthropic-only off-switch; four-way I/CW/CR/O usage reporting	SEARCHED. Produced P1-2. Note: I could not confirm the driver's sub-claim that cache markers are absent from the .eval request snapshot — that specific assertion remains unverified, and I am not carrying it
6	OpenRouter provider routing allow_fallbacks require_parameters	openrouter.ai/docs/guides/routing/provider-selection	Base-slug matching spans all regions/variants; account-wide only/ignore merge with per-request; OpenRouter auto-manages Anthropic prompt caching and extended context; defaults allow_fallbacks=true, require_parameters=false	SEARCHED. Produced P1-3; independently corroborated P1-2 at the gateway layer
7	OpenRouter transforms middle-out default	openrouter.ai/docs/guides/features/message-transforms (body via search)	Mechanism is now the context-compression plugin, default-on only for endpoints ≤8k context, disabled via plugins:[{id:"context-compression",enabled:false}]; if disabled and over context, the request fails loudly	SEARCHED. l.520 uses current nomenclature and is correct. C5's compression sub-claim holds. Recorded as a confirmation, not a finding
8	Statistical design — paired bounded outcomes, pilot-based sizing	not opened	—	RECALLED (internal-pilot literature) for the §8(ii) proposal only. The P1-6 findings themselves are EXECUTED arithmetic, not literature-dependent, so this is UNSEARCHED — NOT-LOAD-BEARING for the verdict
9	LongMemEval-V2 (l.773), Mem2ActBench (l.774 ACL-anthology URL vs PM-Bench's arXiv:2601.19935)	not opened	—	UNSEARCHED — NOT-LOAD-BEARING. Both are Gate 6 external-validity adapters, gated behind Gates 3–5; neither can affect the confirmatory design under review. Flagged for a later round if Gate 6 is ever costed

Why I stopped. The four load-bearing external claims (PM-Bench numbers, AgenticSTS positioning, Inspect state/cache behavior, OpenRouter routing/caching) each resolved against a primary source I opened, and two of them flipped a packet claim. Further sweeping would have gone to Gate-6 references that cannot change this verdict.

11. Residual risks and explicit non-claims

Residual risks I am naming rather than closing:

My tokenizer probe is an approximation. I used o200k_base because tiktoken's BPE download is blocked from my container and I obtained the encoding offline via npm. If the pinned model is Anthropic/Google/Qwen-served, the true token counts differ. The P0-1 margin is 790 vs 512 — a 54% overrun — which survives any plausible tokenizer ratio. The P1-1 margin is 2× headroom, which likewise survives. Neither conclusion is knife-edge, but both are estimates.
My cross-tokenizer asymmetry hypothesis FAILED. I predicted the "tokenizer-compatible counter" escape hatch at l.182 would give the structured arm systematically different effective headroom. I ran it: o200k_base and cl100k_base returned identical token counts for both the prose transcript (768) and the typed projection (1358). I verified the two encodings are genuinely distinct (different token IDs on a control string) before accepting the null. The confound I hypothesized did not reproduce. The narrowed residual — an OpenAI-family counter standing in for a non-public non-OpenAI tokenizer — I could not test offline. UNDETERMINED, capability-limited.
My paired-SD anchor is the wrong quantity. PM-Bench Table 3 pairs across models on one fixed week (SD 0.069–0.105); MBCX-01 pairs across scenarios on one fixed model with ~13 scored items. I argued the latter is noisier from the granularity computation, not from data. The pilot remains the only real estimate, and P1-6 is about how little the pilot can tell you.
I did not execute anything against Inspect or OpenRouter. My C4 and C5 findings are documentation-derived. Doc claims are primary evidence for what the vendor says, not for what the code does — and Inspect's runtime behavior is exactly the kind of thing that drifts between doc and implementation. Gate 1 should verify the cache, retry-granularity, and routing-metadata behaviors empirically against a mocked provider before Gate 2 spends money.
Manifest items 2–8 were hash-verified, not read. If any of them contains a design constraint that contradicts the spec, I would not have seen it.
Single-seat, single-round. I am sealed and have not seen the other seats.

Explicit non-claims:

I do not claim MBCX-01 should not be built. The falsification architecture is sound and the scenario generator is a real contribution.
I do not claim AgenticSTS can substitute for it. I claim the adopt-vs-build comparison was never performed and must be, in writing, before implementation planning is approved.
I do not claim the driver's cache-marker-invisible-in-.eval sub-claim is true. I could not verify it and I am not carrying it forward.
I do not claim the +0.08 threshold is wrong — only that it is underived and sits ~1.5 measurement quanta wide.
I do not endorse expanding the hash question into seal-chain design. One declaratory line, per the packet's own instruction.
I have proposed fix classes only. No patches, no line edits, no leaf implementation. Codex owns the leaf edge.
12. Seat capability report
Model: Claude (Opus 5 currently selected), single sealed council seat.
Harness: Anthropic chat interface with Moonwalker MCP tool surface + Linux probe container + web search/fetch.
Reach exercised: Windows host via moonwalker_shell_exec (pwsh) — git object reads, SHA-256/384 verification, pattern grep of the pinned blob. Linux container — Node/Python probes, npm (gpt-tokenizer), pip (scipy/numpy), api.github.com. Web — search and full-page fetch at origin.
Web access: available and used. Nine sweep entries, seven sources opened at origin.
Limitations hit: tiktoken's BPE endpoint (openaipublic.blob.core.windows.net) is outside my container's allowlist — worked around via npm-bundled encodings. No non-OpenAI-family tokenizer obtainable offline. No model inference executed (correctly — the artifact forbids it and my authority is read-only). No Inspect or OpenRouter runtime execution; those findings are documentation-derived and labelled as such.
Authority discharged: read-only throughout. No edits, commits, pushes, labels, or merges. Bytes created are limited to probe-transient files listed in §2. This verdict is delivered in-thread only and was not written to disk.

Roll Tide 🐘
