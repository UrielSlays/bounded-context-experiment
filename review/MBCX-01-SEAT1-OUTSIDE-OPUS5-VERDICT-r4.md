Pin verified. Now running the executable attacks in my sandbox.# MBCX-01 EXPERIMENT COUNCIL VERDICT — SEXTANT-OPUS5-CLAUDEAIMCP-MBCX01-20260812T

## 1. Top-level verdict

**NO-GO(primary contrast is degenerate as specified, and the decision-rule gate is unsatisfiable at any affordable n).**

Two independent blockers, both executed rather than reasoned:

- **P0-1.** §17.3's own mandated distribution envelope makes §17.2's Student-t interval uncertifiable. No candidate `n` I could simulate up to 3,072 satisfies all five conditions across the families §17.3.3 and §17.3.4 explicitly require. The max-feasible-SD point that §17.3.4 forbids skipping needs n ≈ 8,700, which is ≈1.45M paid calls and ≈50 days of wall clock under §12's single-in-flight rule. Gate 4 therefore returns `UNDERFUNDED` deterministically, and the only lever that changes that (the "retention rule" of §17.3.2) is named but never defined.
- **P0-2.** §5.2 gives TN no public event F+ lacks, so TN's store is a deterministic function of F+'s. §7 then mandates that both arms select identical semantic IDs. I built both reducers and the §7 selector and confirmed identical selections on all nine mandated trace families. `TN - FM` therefore cannot measure a store or mechanism difference. It measures the effect of *displaying* typed annotations over an identical selected record set, which is the quantity `Presentation, Not Mechanism` (arXiv 2607.16019) already measured as indistinguishable from zero.

r3 is close to a good instrument. It is not the instrument its own §1 question asks for. §11 (reconstruction), §14 (missingness), §6 (public grammar) and the deletion of the 512-token cap and the chi-square SD bound are all real improvements and should survive into r4.

---

## 2. Seat identity

| Field | Value |
|---|---|
| Model as actually exposed | Claude Opus 5 (`claude-opus-5`), selected model in this session |
| Harness | claude.ai chat surface, Moonwalker MCP bridge (file/shell/read tools), plus an isolated Linux code container (Python 3, numpy 2.4.4, scipy 1.17.1, no network egress) |
| Native web tools | `web_search` and `web_fetch` present and live this session (checked in the tool list before planning any route) |
| Paid inference run | **NONE** |
| Report title | MBCX-01 EXPERIMENT COUNCIL VERDICT — SEXTANT-OPUS5-CLAUDEAIMCP-MBCX01-20260812T |

---

## 3. Pin and byte verification

Verified by `git` at the repository, with a unique sentinel token echoed on every shell call and the echoed `command` field checked against what I sent (bridge cross-talk mitigation, two calls, zero crossings).

| Claim in packet §0 | Measured | Result |
|---|---|---|
| Commit `f3f9273678867ace9747413d808a5f47243548c0` | `git cat-file -t` returns `commit` | MATCH |
| Blob `4d7fd5035d746935778020dcd7fab1df573ec3d8` | `git rev-parse f3f9273:MBCX-01-EXPERIMENT-DESIGN-r3.md` = `4d7fd50...` | MATCH |
| Bytes `32,319` | `git cat-file -s` = 32319; piped blob stream = 32,319 bytes | MATCH |
| Lines `569` | 569 LF bytes, 0 CR bytes in the blob | MATCH |
| SHA-384 `C1D80168...C228BDC` | Computed over the piped blob bytes: `C1D80168F0CBE0683E94CC4564238622C5EF87AEA6D51101EB89CADBD7EBF3A0A30856A05CCDC1967E262F3A3C228BDC` | MATCH |

**Working-copy difference: NONE.** `git status --porcelain` on the path is empty; `HEAD:MBCX-01-EXPERIMENT-DESIGN-r3.md` resolves to the same blob; the on-disk file is 32,319 bytes with SHA-384 identical to the blob and 0 CR bytes despite `core.autocrlf=true`. HEAD is `72f621781e127e5444bd8741ccdf8fb5d3e9f5a4`, a descendant of the pin (`git merge-base --is-ancestor` exit 0), but the artifact blob is unchanged between the pin and HEAD. I adjudicated blob `4d7fd50`, read through the working copy after proving byte identity.

Also opened at explicit path: `<vault>` (seat role, read first) and `LOCAL-SOURCE-MANIFEST-r1.md` (pinned in the packet; blob at the pin `b71f8b64a2000acd554bd09c7a88320172025db3`). No other repository file was opened, listed, grepped, or indexed.

---

## 4. Evidence and probes

**EXECUTED** (my own code, in the container, no paid inference, no local writes)

| Probe | What it produced |
|---|---|
| `lattice.py` | Exact per-arm F1 lattice from 36 positives and 24 lures: 767 distinct values; smallest adjacent gap 2/7905 = 0.000253; largest adjacent gap 2/61 = 0.03279. Attainable delta support: 470,395 distinct points on [-1, 1]. `+0.03` is exactly attainable (5/172, 3/100 and 22,000+ neighbours within the band). |
| `arms.py` | Independent reference transition table, F+ append-only replay reducer, TN typed reducer, and the §7 "ordinary cheap operations" selector. Ran all eight mandated Attack-A families plus one nested compound. |
| `packets.py` | Flat-journal conflict/supersession detector; F0 current-only ablation; exact logical F+/TF/FM/TN packets for one update-plus-conflict world with proxy token counts. |
| `budget.py` | Independent derivation of the maximum legal output serialization and of joint-maximum memory fixtures under §8's field caps. |
| `oc.py`, `oc2.py`, `oc3.py` | Monte Carlo operating characteristics of the §17.2 interval under the §17.3 family list, R = 8,000 to 40,000 per cell, n from 48 to 3,072. |
| `cost.py` | Calls, tokens, dollars and serial wall clock for n = 48 to 8,724. |

**READ-ONLY**: §11 reconstruction witnesses (no harness exists to run them against; I attacked them by constructing a passing-but-hollow implementation on paper). §13 transport assertions (no endpoint is frozen, so nothing to mock against).

**SEARCHED** (opened at origin this session): StateFuse arXiv 2607.05844; Presentation Not Mechanism arXiv 2607.16019 (abstract, HTML render, and PDF table extract); PM-Bench arXiv 2607.12385; Mem2ActBench arXiv 2601.19935 plus its ACL 2026 camera copy; TriggerBench arXiv 2606.23459; MemoryAgentBench summary; Waudby-Smith and Ramdas, JRSS-B 86(1) 1-27 (2024); OpenRouter `docs/guides/routing/provider-selection`, `docs/guides/best-practices/prompt-caching`, and the response-caching and model-routing announcements; one Chinese-language secondary surface on filesystem-based agent memory.

**UNSEARCHED, with reasons**: AgenticSTS and LongHorizon-Harness (**DID-NOT**, budget spent on the two lanes that actually move the ruling; they bear on fresh-executor discipline, which I am not disputing). LongMemEval-V2 and MemoryArena (**NOT-LOAD-BEARING**, external-validity positioning only, and §3 already excludes generalization). Exact finite-support paired methods and indifference-zone/equivalence rules (**DID-NOT**; named as the repair direction in §9 but not opened, so my recommendation there is labelled RECALLED where it is not the WSR paper). Inspect documentation (**NOT-LOAD-BEARING**, §12 forbids Inspect). NIST SD guidance (**SETTLED-BY-PINNED-BYTES**, r3 already deleted the chi-square bound the guidance would have condemned).

---

## 5. Applicability ruling

Excluded from this verdict as non-load-bearing per packet §1, and I found no direct path from any of them to a false win, false kill, biased comparison, irreproducible result, hidden reroll, unexecutable gate, or late cost: licensing and clean-room doctrine; production security, hostile actors, prompt injection, FIPS/CNSA, authorization topology; daemon/PID/fleet lifecycle, crash durability, deployment, packaging; model-family or provider generalization.

Retained in scope because they *do* have that path, per §1's second paragraph: OpenRouter sticky routing and preset state (alters experimental inputs), response and prompt caching (alters inputs and cost), the reconstruction child's filesystem reach (alters reconstruction), and whole-scenario invalidation (alters the retained target cohort and the delta distribution).

---

## 6. Claim scoreboard C1 to C12

| Claim | Ruling | One-line basis |
|---|---|---|
| **C1** F+ is the strongest cheap flat mechanism | **HOLDS** | EXECUTED: F+ replay recovers every mandated trace including retraction-of-cancellation and retraction-of-correction, where F0 current-only fails. Nothing typed was needed. |
| **C2** FM is an honest render-matched primary comparator | **FALSE** | §5.3 forbids FM from *inferring* facts F+ can compute, so FM is stripped of F+-derivable content by rule. EXECUTED: FM renders `"conflict": []` in a world where the conflict is recoverable from the journal in one linear pass. |
| **C3** TN minus FM identifies the intended treatment | **FALSE** | §5.2 plus §7 make TN's store a deterministic function of F+'s and force identical selected IDs. EXECUTED: identical selections on 9/9 families. The contrast identifies annotation display, not mechanism. |
| **C4** the 25% F+/TF subset is sufficient decomposition | **FALSE** | The difference-in-differences contrast on a quarter-size subset carries roughly 16x the variance of the primary, so ~4x the standard error. No precision target is stated anywhere and the OC gate covers only the primary. |
| **C5** public grammar and workload composition are architecture-neutral | **UNDERDETERMINED** | The per-scenario mixture is exactly frozen and that part holds. But no positive class in §8.1 requires a typed-exclusive fact, so composition is neutral in the sense of not favouring TN and non-neutral in the sense of excluding TN's mechanism from the scored surface. |
| **C6** packet budget selection is executable and fair | **UNDERDETERMINED** | §9.1.4's "per-decision mandatory-object bounds" are named but never fixed, and they are the quantity that decides feasibility. Under §8's stated field maxima my proxy puts the joint maximum an order of magnitude above the 4,096 ceiling. Not unfair, but not decidable from r3. |
| **C7** output and scorer contracts are bounded and invariant | **FALSE** | No schema cardinality limit for `action_ids` or `channel_queries` appears anywhere in r3, yet §9.3 derives the cap from "six" and "twelve". §8 permits up to 12 available actions per decision. The cap changes by 30% depending on which reading you take. |
| **C8** reconstruction is information-causal on the artifact | **UNDERDETERMINED** | The six witnesses do force artifact dependence. They do not close absolute-path continuity, and nothing forbids the artifact carrying a materialized packet cache, which would let the child pass every witness while proving nothing about reconstruction of mechanism. |
| **C9** retry and missingness cannot choose the winner | **HOLDS** | Pre-dispatch-only retry, whole-pair censoring, frozen cohort, no substitution, `[-1,1]` tipping and the 5% stop are jointly sufficient for the transport channel r3 models. This is the strongest section of the design. |
| **C10** statistical rule is coherent and executable | **FALSE** | EXECUTED: coverage 0.382 at n=48 and 0.894 at n=384 on the `eps=0.01` rare-tail family that §17.3.3 mandates including, against a 0.94 requirement. No n up to 3,072 clears all mandated families. |
| **C11** pilot and cost gates are rational | **UNDERDETERMINED** | The pilot is correctly demoted, and the cost table can indeed return `UNDERFUNDED`. But r3 removes the only cheap route from "SD unknown" to "n chosen" and replaces it with a worst-case envelope that no budget can serve, so the gate is rational and inert at the same time. |
| **C12** this is the smallest decisive Stage-A instrument | **FALSE** | Not because machinery is excess, but because the instrument is not decisive on the question in §1. Separately, the 25% diagnostic subset (18.4% of calls) buys a DiD that cannot resolve the effect it is meant to attribute. |

---

## 7. Finding table

| ID | Sev | Exact location | False-result mechanism | Smallest fix | Evidence |
|---|---|---|---|---|---|
| F1 | **P0** | §17.2 + §17.3.3 + §17.3.4 + §17.3 condition 5 | Unexecutable gate. Coverage and power requirements are quantified over a family and SD envelope whose worst member (two-point at ±1) needs n ≈ 8,700. The gate never certifies the interval, so the design cannot reach a pilot; if the envelope is quietly narrowed later, the narrowing is the unstated choice that decides the experiment. | Replace the family-envelope certification with a distribution-free bounded-mean interval that has finite-sample coverage by construction (WSR betting or predictable-plug-in empirical Bernstein on the [-1,1] delta), and define `n` by a preregistered width target rather than by family sweep. Keep Student-t as a reported sensitivity only. | EXECUTED |
| F2 | **P0** | §5.2 + §7 + §5.3 | Biased arm comparison and false kill. TN carries no information F+ lacks, and §7 forces identical selected IDs, so the treatment reduces to annotation display. §5.3's "rather than inferred" then withholds from FM facts F+ can compute, which pushes the residual up for a reason that is not mechanism value. | Name the treatment explicitly as *precomputed typed exposure versus on-demand replay under an equal render-time compute budget*, and either (a) let FM populate every field it can derive and accept that `TN - FM` is then an exposure test, or (b) add a class of scored positives whose gold requires a fact the flat transition table leaves genuinely undetermined. | EXECUTED |
| F3 | **P1** | §8.1 positive-class table | False kill. Every one of the six positive classes is resolvable by deterministic replay of the §6 grammar. There is no conflict, validity-interval or provenance-explanation positive class, so the scored surface and the treatment surface barely intersect. | Add a seventh exclusive positive class whose gold action depends on an unresolved-conflict or validity-window fact, and rebalance the 36 to keep the total fixed. | EXECUTED |
| F4 | **P1** | §5.3 FM render contract | False win. A present-but-empty field is a positive assertion of absence in a strict schema. FM shows `"conflict": []` where a conflict exists, so FM is misinformed rather than merely uninformed. | Use a distinct `not_computed` sentinel for every field an arm does not populate, identical in both arms' schemas, and add a Gate-1 fixture asserting no arm ever emits `[]`/`null` for a field it did not evaluate. | EXECUTED |
| F5 | **P1** | §9.1.6 overflow classification | False kill via cohort selection. Overflow is classified on realized per-arm serialization size. TN is the larger arm at every checkpoint (proxy ratio 1.93 at ID length 8), and TN's size is driven by typed density, so every excluded-overflow fixture is excluded because of the treatment's own intensity. | Classify overflow on an arm-neutral size proxy (F+ raw journal tokens), and publish the typed-density distribution of excluded versus retained fixtures. | EXECUTED |
| F6 | **P1** | §15.1 invalid-output rule | Hidden confound favouring FM, and it is the same tail that breaks F1. One over-limit or unknown ID anywhere in a trajectory zeroes the whole scenario, producing exactly the rare-tail two-point deltas at ±1 whose coverage I measured at 0.38. If denser packets raise invalid-output rates, the zeroes are arm-correlated. | Score the invalid *decision* as zero-credit rather than zeroing the scenario, and preregister an arm-wise invalid-rate comparison with a stop rule mirroring §14.4. | EXECUTED |
| F7 | **P1** | §9.2 candidate ladder + §9.1.4 | Cost discovered too late. The ladder tops out at 4,096 while §8's field maxima (32-token identifiers, 40 rows, 28 open obligations) imply joint maxima of 35,936 proxy tokens for TN. Only single-token identifiers fit. The bound that closes the gap is named in the freeze list and never given. | State the per-decision mandatory-object bound and the identifier length policy in the design, then re-derive the ladder. If nothing fits, that is a Gate-1 answer, not an implementation surprise. | EXECUTED (proxy) |
| F8 | **P1** | §9.3 + §10 | Unexecutable gate and biased scoring. `output_cap` is derived from "six action IDs and twelve channel IDs" but no cardinality limit for either array exists in r3. Proxy maxima: 826 tokens under r3's reading, 1,078 if `action_ids` may carry the 12 available actions. If the schema caps at 6 and a model would emit 8, truncation changes FP counts. | Put explicit `maxItems` on both arrays in the frozen output schema, state them in §10, and re-derive §9.3 from the schema rather than from prose. | EXECUTED (proxy) |
| F9 | **P1** | §13 transport freeze | Hidden reroll. A byte-exact request wrapper does not determine the served condition. Current OpenRouter docs describe sticky routing keyed at the account level per model per conversation and derived by hashing the first system message and first non-system message, with a 5-minute inactivity expiry; server-side presets that shallow-merge into the request; a top-level `models` array that is a second, independent fallback channel; and account-level ZDR that is OR'd with the request. | Extend the frozen condition to *account and key state*: assert no preset reference, `models` absent, an explicit `session_id` held constant across arms, `transforms: []`, and record `usage.prompt_tokens_details.cached_tokens` and `cache_discount` per call. Add a Gate-3 assertion that the sticky key is arm-invariant. | SEARCHED |
| F10 | **P1** | §11 reconstruction | False pass on the causal witnesses. §11 sanitizes cwd, environment and import path, and none of that restricts absolute-path reads. A helper resolving a fixed absolute config or log path, or a materialized packet cache inside the artifact, passes withhold, corrupt, swap, mutation and sufficiency while carrying continuity outside the artifact. | Add one cheap witness: rename the run-owned directory between artifact close and child launch, and require the child to still succeed. Separately, forbid materialized packet caches in the artifact and add a recompute-and-compare index witness. | READ-ONLY |
| F11 | **P2** | §4.2 diagnostic subset | Interpretability, not validity. The DiD contrast on 25% carries about 4x the primary standard error, so if the primary is powered to resolve 0.03 the DiD resolves about 0.12. C4's "adequate precision" is asserted and never computed. | State a half-width target for the DiD and size the subset to it, or drop the DiD claim and keep the cells as descriptive. | EXECUTED |
| F12 | **P2** | §17.3.2 manifest | Specification incoherence. For finite-support families, mean and mixture weight jointly determine SD, so a free SD grid and a free mixture-weight grid cannot both be honoured. The manifest requires both. | Parameterize the family list by (support, mixture weight) and derive SD, or by (mean, SD) and derive support. Not both. | EXECUTED |
| F13 | **P2** | §20 prior-art list | Stale pointer. The OpenRouter routing documentation has moved from the features path to `docs/guides/routing/provider-selection`, and now carries fields r3 does not name (`zdr`, `enforce_distillable_text`, `max_price`, `sort.partition`, `preferred_*`). | Re-pin the doc URL and re-derive the §13 assertion list from it at freeze time. | SEARCHED |

---

## 8. Attacks A to H

### Attack A — strongest-flat challenge (EXECUTED)

**Inputs.** Nine trace families built on the §6 grammar: correction then retraction of the correction; cancellation then retraction of the cancellation; link then unlink; a depth-3 dependency chain; reverse prerequisite activation; a cross-scope obligation against an in-scope sibling; terminal suppression; near-due window selection; and a nested reschedule plus channel cue plus retraction compound.

**Method.** Three independent implementations: a reference transition table (total, deterministic fold defining gold), an F+ store that persists only the append-only journal plus a flat current index plus tombstones plus untyped adjacency, and a TN store that persists version chains, validity fields, lifecycle states, supersession and retraction relations and provenance pointers. One shared §7 selector implementing operations 1 to 7 (scope restriction, terminal suppression, due and near-due, prerequisite readiness including the reverse scan, bounded BFS at depth 3 / width 3 / closure 12, referenced state rows, stable sort).

**Output.**

```
A1 correction then retraction     F+==TN==REF  obl=['O1']            acts=['ACT1']
A2 cancel then retract cancel     F+==TN==REF  obl=['O1']            acts=['ACT1']
A3 link then unlink dependency    F+==TN==REF  obl=['O1','O2']       acts=['ACT1','ACT2']
A4 depth-3 dependency chain       F+==TN==REF  obl=['O4']            acts=['ACT4']
A5 reverse prereq activation      F+==TN==REF  obl=['O1']            acts=['ACT1']
A6 cross-scope obligation         F+==TN==REF  obl=['O9']            acts=['ACT9']
A7 terminal suppression           F+==TN==REF  obl=[]                acts=[]
A8 near-due window                F+==TN==REF  obl=['O1']            acts=['ACT1']
A9 nested reschedule+cue+retract  F+==TN==REF  obl=['O1','O2']       acts=['ACT1','ACT2','ACT7']
ALL: F+ selection == TN selection == reference selection: True
```

Then the sharper question, which is whether anything r3 reserves to TN is obtainable by cheap untyped replay. I wrote a supersession-and-conflict detector that runs over the F+ journal alone and persists no typed object. On a world with two concurrent conflicting asserts by different actors plus an update chain, it recovered the conflicting pair, and **every** supersession pair TN persists was recomputable from the journal (`True`).

**Interpretation.** §5.2 gives TN no additional public events. §6 caps the world at 128 primitive events. F+ retains all of them. TN's typed store is therefore a deterministic function of F+'s store, and no typed field carries information F+ lacks. §7 then requires both arms to select the same semantic IDs and makes any divergence a gate failure. The result is that r3 forbids, before inference, the only channel through which a store difference could show up in an action score. What remains is annotation display. That is a real and interesting question, but it is not the question §1 asks.

The one place where retention genuinely matters is the F0 ablation, and r3 gets that right: on cancel-then-retract-cancel, F0 selects nothing while F+ and the reference both select `O1`. F0 is correctly unpaid and correctly not the opponent.

**Limitations.** My reducers are a faithful implementation of the §6 grammar as written, not of an unwritten one. If the intended transition table is *partial* (some legal sequences have no defined effective result and must surface as unresolved), the equivalence breaks and C3 recovers. r3 §5.3 says the opposite: the table "defines the effective result of every legal primitive sequence." Totality is the property that collapses the contrast.

### Attack B — render-matched control (EXECUTED)

**Inputs.** One update-plus-conflict world: two concurrent asserts on `S1/room_status` by different actors, an obligation triggered on that key, and a correction chain on `S1/load_cap`.

**Output** (proxy tokenizer, disclosed below):

| Arm | proxy tokens | chars |
|---|---:|---:|
| F+ flat store, flat render | 318 | 631 |
| TF typed store, flat render | 318 | 631 |
| FM flat store, native render, neutralized | 451 | 918 |
| TN typed store, native render | 488 | 955 |

The FM and TN rows for the conflicted key:

```
FM: {"k":"S1/room_status","v":"RED","is_current":null,"version":null,
     "valid_from":null,"valid_to":null,"superseded_by":[],"conflict":[],"evidence":[]}
TN: {"k":"S1/room_status","v":"RED","is_current":true,"version":2,
     "valid_from":2,"valid_to":null,"superseded_by":["E002"],
     "conflict":[{"a":"E001","b":"E002"}],"evidence":["E002"]}
```

**False-TN-win routes found.** (i) `"conflict": []` is not neutral. In a strict schema an empty array reads as "evaluated, none found." FM is therefore not merely denied the mechanism, it is made to assert its negation, and my Attack-A detector shows the assertion is false and cheaply falsifiable from FM's own store. (ii) §5.3's `rather than inferred` clause is the operative bias: it is a rule about what FM may *compute*, not about what F+ *knows*. (iii) FM and TN differ by only 8% in serialized size here, so token ballast is not the problem; content withholding is.

**False-TN-loss routes found.** TN carries the typed scaffolding at every row whether or not it is informative, so on rows with no version history TN pays tokens for `version: 1, superseded_by: [], conflict: []` while FM pays for nulls. Under §9.2's shared budget this is a small tax on TN, in the opposite direction. I judge it second-order relative to (i).

**Ruling.** FM is *layout*-matched and is not *content*-matched. `TN - FM` is the right primary contrast for the question "does exposing typed structure help a model act," and the wrong one for the question "do typed continuity mechanisms earn their complexity," because the mechanisms are held informationally equal by §5.2 and operationally equal by §7.

**Limitations.** Single world, proxy tokenizer, no model in the loop. The empty-field salience claim is a claim about how a model reads a schema and cannot be settled without paid inference. It can, however, be *removed* by the F4 fix at zero cost.

### Attack C — workload and scorer mixture (EXECUTED)

**Support enumeration.** `scenario_f1 = 2TP/(TP + FP + 36)` with `TP` in 0..36 and `FP` in 0..24. 767 distinct attainable per-arm values. 470,395 distinct attainable deltas.

**One-action quantum.** From a perfect arm, one extra false positive costs 0.01370; one missed gold costs 0.01408. The `+0.03` decision boundary is therefore worth **about two actions out of sixty per scenario**. That is a legitimate target but it should be stated plainly in the design: the entire architecture decision turns on roughly a 2-in-60 action difference.

**Lattice pathology.** The largest adjacent gap in the attainable F1 lattice is 2/61 = 0.0328, which is wider than the decision threshold. It sits in the sparse low-TP region, so it does not bite the mean estimand, but it does mean per-scenario deltas are not dense near the boundary everywhere, and §17.3.1's "derive the attainable delta support" must be done on the *delta* lattice, not the F1 lattice, or the enumeration will look tidier than it is.

**Composition perturbation.** I could not move the idealized result across `+0.03` by composition alone without violating the written contract. §8.1 freezes both class tables exactly, the 24 lures are declared to be the complete non-gold affordance set, and the precedence table is frozen before reducer implementation. This is the best-specified part of r3 and C5's mechanical half holds.

What composition *does* do is bound the achievable effect. All 36 positives are replay-derivable (Attack A), so under the r3 grammar the idealized `TN - FM` on the scored surface is zero and the entire observed effect must come from model reading behaviour. That is finding F3, and it is a composition finding even though it is not a discretion finding.

### Attack D — exact budget and output feasibility (EXECUTED, proxy)

**Disclosed proxy.** No target tokenizer exists in r3 (§9.1.1 defers it to freeze time), so I used a regex proxy splitting on letter runs, digit runs and single punctuation characters. It is close to BPE behaviour on JSON with short identifiers and understates on long natural-language spans. **Every number in this attack is proxy, not certification**, and the certification cannot happen until §9.1.1 is executed.

**Independent output-cap derivation.**

| Reading | max legal output | `ceil(1.20x)` |
|---|---:|---:|
| r3 §9.3 as written (6 action IDs, 12 channel IDs, 32-token identifiers) | 688 | **826** |
| §8 allows 12 available actions per decision | 898 | **1,078** |
| 12 actions, 10 channels (§8's per-scenario cue range) | 828 | **994** |

The deleted 512 cap was indeed too small under every reading, so r3's fix is directionally right. But the derivation is not reproducible from r3, because **no cardinality limit for `action_ids` or `channel_queries` exists anywhere in the document**. §15.1 penalizes "over-limit cardinality" against a limit that is never stated. That is the unbounded co-occurrence Attack D asks for.

**Joint-maximum memory fixtures.**

| Fixture | TN proxy tokens | FM proxy tokens | Fits 4,096? |
|---|---:|---:|---|
| §8 joint maximum: 40 current rows + 28 open obligations, 32-token identifiers | 35,936 | 20,600 | No |
| §8 *minimum* world: 18 rows + 12 obligations, 32-token identifiers | 15,708 | 8,922 | No |

Sweeping identifier length: 16 tokens gives 19,232; 8 gives 10,880; 4 gives 6,704; 2 gives 4,616; only 1-token identifiers fit at 3,572. And that is before a single natural-language span or journal event enters the packet.

**Interpretation.** At least one candidate payload can satisfy all conditions only if identifiers are effectively one or two tokens and the per-decision object count is small. r3 names the missing bound in its own freeze list (§9.1.4, "per-decision mandatory-object bounds") and never gives it, so §9.2's selection procedure is not decidable from the pinned bytes. This is not a fairness problem, since selection is pre-outcome. It is a feasibility problem that will surface after Gate 0 and Gate 1 work is already sunk.

**Overflow asymmetry.** At 8-token identifiers, TN rows serialize to 1.93x FM rows. Since overflow is classified per arm, and TN is always the larger arm, every excluded-overflow fixture is excluded because of TN's size, which is a monotone function of typed density. The retained target cohort is therefore depleted of exactly the worlds where the treatment is most concentrated. That is finding F5, and it is a systematic downward bias on the primary estimand that no gate in r3 detects.

### Attack E — complete decision-rule calibration (EXECUTED)

**Bug verification.** Confirmed gone. §17.3 uses `+0.03` as the observed-mean gate and demotes `+0.08` to a planning alternative. §17.1 states plainly that the pilot does not set or shrink `n` through a chi-square SD bound. Both r2 defects are genuinely repaired.

**Feasible SD.** On support [-1, 1], max SD is 1.0000 at mean 0, 0.9995 at +0.03, 0.9968 at +0.08. §17.3.4 requires sweeping "through the exact maximum feasible at each target mean" and says explicitly not to stop at 0.40, so those points are in the envelope by the design's own instruction.

**Which condition binds.** Normal-approximation minimum `n`, in the design's own increments:

| SD | n for condition 1 (power at +0.08) | n for condition 3 (upper endpoint below +0.03 at mean 0) |
|---:|---:|---:|
| 0.10 | 36 | 96 |
| 0.15 | 84 | 204 |
| 0.25 | 204 | 552 |
| 0.40 | 516 | 1,404 |
| 0.80 | 2,016 | 5,592 |
| 1.00 | 3,144 | **8,724** |

Condition 3 binds throughout, by roughly a factor of 2.8 in `n`. r3 never notes that its hardest requirement is the null-side one.

**Mandated-family Monte Carlo.** Rare-tail mixtures with the six tail masses §17.3.3 names, mass at the attainable extreme `+1`:

| n | family | cov@0 | cov@.03 | cov@.08 | power@.08 | kill@0 | pass |
|---:|---|---:|---:|---:|---:|---:|---|
| 48 | eps=0.010 | 0.384 | 0.380 | 0.381 | 1.000 | 0.616 | FAIL |
| 48 | eps=0.050 | 0.915 | 0.912 | 0.912 | 0.305 | 0.292 | FAIL |
| 48 | two-point ±1 | 0.940 | 0.958 | 0.941 | 0.054 | 0.029 | FAIL |
| 192 | eps=0.010 | 0.852 | 0.853 | 0.853 | 1.000 | 0.877 | FAIL |
| 192 | eps=0.150 | 0.940 | 0.940 | 0.940 | 0.431 | 0.195 | FAIL |
| 384 | eps=0.010 | 0.894 | 0.895 | 0.892 | 1.000 | 0.995 | FAIL |
| 768 | eps=0.010 | 0.943 | 0.946 | 0.940 | 1.000 | 1.000 | **OK** |
| 768 | two-point ±1 | 0.953 | 0.948 | 0.952 | 0.290 | 0.134 | FAIL |
| 1,536 | eps=0.200 | 0.949 | 0.951 | 0.951 | 0.994 | 0.656 | FAIL |
| 3,072 | eps=0.010 through 0.200 | 0.941 to 0.953 | | | 1.000 | 0.907 to 1.000 | **all OK** |
| 3,072 | two-point ±1 | 0.955 | 0.953 | 0.948 | 0.792 | 0.373 | FAIL |

**Answers to the four sub-questions.**

1. *Is the stated support and SD sweep finite and executable?* The support is: 767 F1 values, 470,395 deltas, enumerable in under a second. The SD sweep is finite (0.05 to 1.00 in 0.05 steps is 20 points) but the `n` search on top of it is not affordable, because §17.3.6 forbids a maximum clamp and the envelope's worst point sits at n ≈ 8,700.
2. *Can the family grid still omit a worst legal distribution?* No, and that is the problem. It is *complete enough to be unsatisfiable*. The escape is §17.3.2's "retention rule," which is listed as a manifest field and never specified. Whoever writes that rule chooses whether the experiment can run, after Gate 4 has already shown that no envelope-honouring `n` is affordable. That is an unstated choice that changes the answer, which packet §7 declares disqualifying.
3. *Is Clopper-Pearson oriented correctly?* The orientation r3 specifies is right in principle: a one-sided 95% bound in the conservative direction for each threshold (lower bound on power and coverage, upper bound on false-decision rates), with at least 100,000 replicates. At 100k replicates the CP adjustment is roughly 0.002 at a 0.80 target and roughly 0.001 at a 0.05 target, which is immaterial next to the gaps above. The orientation is correct and the effect is negligible; it is not what is stopping this gate.
4. *Can a feasible n be costed before the pilot?* Only conditionally. `n` is a function of the delta SD, which is a function of the between-scenario difficulty correlation between paired arms, which no no-model gate can estimate. r3 removes the pilot's authority to inform `n` (correctly, given the r2 defect) and puts nothing in its place. That is the structural hole: the design forbids the only cheap way to learn the one parameter that decides affordability.

**Proposed alternative primary interval, with an executable algorithm.** Use a distribution-free bounded-mean interval on `delta_i / 2 + 1/2` mapped to [0, 1]:

- **Fixed-n form.** Waudby-Smith and Ramdas predictable-plug-in empirical Bernstein CI, or the hedged-capital betting CI, both closed-form or one-dimensional-root-find, both variance-adaptive, both with finite-sample coverage at least 1-alpha over *all* distributions on the bounded support. The family envelope disappears because coverage is guaranteed by construction rather than certified by simulation, which deletes §17.3.2 through §17.3.5 entirely.
- **Sequential form.** The same paper's time-uniform confidence sequence gives anytime validity, so you may stop as soon as the interval clears `+0.03` or excludes it. This converts an unaffordable fixed-`n` design into a cost-adaptive one with no alpha inflation, which is the single largest cost lever available.

**Full operating-characteristic comparison, not a slogan.** The guarantee is not free. Half-widths at alpha = 0.05 on this support:

| n | observed sd | Student-t | empirical Bernstein | Hoeffding |
|---:|---:|---:|---:|---:|
| 192 | 0.15 | 0.0214 | 0.1195 | 0.1960 |
| 384 | 0.15 | 0.0151 | 0.0657 | 0.1386 |
| 768 | 0.15 | 0.0106 | 0.0371 | 0.0980 |
| 1,536 | 0.15 | 0.0075 | 0.0216 | 0.0693 |
| 1,536 | 0.25 | 0.0125 | 0.0285 | 0.0693 |

So the honest trade is: Student-t at n=192 has a nominal width that resolves 0.03 and a real coverage of 0.85 on a mandated family, while empirical Bernstein at n=1,536 has a width of 0.022 and coverage that holds by theorem. The betting CI is tighter than closed-form empirical Bernstein (that is its headline result) and would land between the two columns, so the realistic requirement is `n` in the high hundreds to low thousands rather than n=48. That is a much smaller number than the 8,724 the current envelope demands, and it is honestly costable before the pilot.

**Limitations.** I did not implement the betting CI; the two right-hand columns are analytic closed forms and the betting interval is strictly tighter than the empirical-Bernstein column, so treat my `n` guidance as an upper bound. The WSR result is **SEARCHED** (JRSS-B 86(1) 1-27, 2024, opened at Oxford Academic and at the RSS discussion-meeting PDF). I did not open the two-stage and indifference-zone literature, so any suggestion in that direction would be RECALLED and I have not leaned on it.

### Attack F — artifact-causal reconstruction (READ-ONLY)

**The maliciously convenient implementation.** A child that reconstructs honestly from artifact bytes but where the artifact contains a *materialized packet cache* written by the parent. It passes withhold (nothing to read), corrupt (hash fails), ambient-removal (needs nothing else), prefix mutation (hash fails), A/B swap (states follow the artifact), field mutation (predicted fields change), and information sufficiency (a reference decoder reads the same cache). It proves artifact dependence and proves nothing about reconstructing *mechanism* from *evidence*. §11 does not forbid it. §5.1 and §5.2 constrain what each store may persist but say nothing about a rendered-packet cache.

**The continuity channel §11 leaves open.** §11.3 creates an empty run-owned temp working directory, §11.5 sanitizes the environment, and the import path excludes generator, registry, event log, expected-state and fixture modules. None of that restricts **absolute-path filesystem reads**. A helper that resolves a fixed absolute config, log, or default-state path (the ordinary shape of a real adapter, not a hostile one) supplies continuity through a channel every witness ignores. Scenario-ID opacity does not help, because the path need not be scenario-keyed: the parent's own run log at a fixed location is enough.

**Smallest honest substitute I ran instead of the witnesses.** No harness exists, so I could not execute them. I constructed the two implementations above against the §11 text and checked each of the six witnesses by hand. Both pass all six.

**The missing witness, and it is cheap.** Rename the run-owned directory between artifact close and child launch, and pass the artifact by its new path. Any absolute-path dependency breaks. Add a second witness that forbids a packet cache: require the child to recompute its index from the journal and to prove the recomputed index equals the persisted one.

### Attack G — transport and frozen target cohort (SEARCHED plus READ-ONLY state machine)

**What current official documentation says that r3's §13 does not cover.**

- **Sticky routing.** Routing stickiness is tracked at the account level, per model, per conversation, and by default OpenRouter derives the conversation key by hashing the first system or developer message together with the first non-system message. Sticky sessions expire after five minutes of inactivity and each successful request resets the timer. Under §12's single-in-flight rule and §14's within-block order randomization, this makes endpoint stickiness a function of arm order and of wall-clock pacing. If the memory payload sits in the first non-system message, FM and TN hash to *different* sticky keys and can be assigned different endpoints. That is arm-correlated endpoint assignment, which is precisely the confound §13 exists to prevent, and §13 does not name it.
- **Presets.** A preset stores provider rules, parameters and a system prompt server-side under a slug, referenced as `@preset/slug`, and request fields shallow-merge over it. A byte-exact request wrapper therefore does not determine the served condition.
- **Model-level fallback.** The top-level `models` array is XOR-gated with `model` and triggers on context-length errors, moderation flags, rate limits and downtime. It is a second fallback channel independent of `provider.allow_fallbacks`, and §13 only names the latter.
- **Response caching (beta).** Identical prompt plus model plus parameters returns a cached response scoped to the API key, and a cache hit never reaches the provider. §13 correctly invalidates the pair on a cache hit, but the routing metadata on such a response may be absent or synthetic, so the *detection* must key on the cache indicator, not on the absence of a provider mismatch.
- **Prompt caching.** `usage.prompt_tokens_details.cached_tokens` and `cache_write_tokens` are the only reliable hit signal, and `cache_discount` gives the cost effect. Since FM and TN share the schema declaration prefix but diverge immediately after, hit rates will differ by arm, which is a cost asymmetry rather than a validity one, but §17.4's "exact input/output/cache token assumptions" cannot be written without it.
- **Doc drift.** The routing page now lives at `docs/guides/routing/provider-selection` and carries `zdr`, `enforce_distillable_text`, `max_price`, `sort` with a `{by, partition}` form, `preferred_min_throughput` and `preferred_max_latency`, none of which appear in §13. Defaults matter: `allow_fallbacks` defaults to true and `require_parameters` defaults to false, and the default router picks among lowest-cost providers weighted by inverse square of price after deprioritizing anything with a recent outage.

**Mock state machine, traced by hand.** Pre-dispatch failure to whole-pair retry: correct. Accepted-with-no-body to missing pair: correct and this is the strongest rule in r3. Malformed response to scored failure: correct. Endpoint mismatch to pair invalidation: correct given per-call metadata. Cache hit: correct. Transform: correct if `transforms: []` is asserted rather than assumed. Fallback: covered for provider-level, **not covered** for model-level. Metadata omission: correct.

**Arm-correlated missingness.** Constructed three: (i) TN packets are larger, so context-length errors and rate-limit trips land on TN preferentially, and both are `models`-array fallback triggers; (ii) sticky-key divergence assigns arms to different endpoints with different error profiles; (iii) if pressure checkpoints are also the largest packets, missingness correlates with pressure, which is already one of §14.1's required breakdowns. §14.4's stop rule catches all three *if* the metadata is captured. The 5% cohort ceiling and the `[-1,1]` tipping interval are both sound and I found no way past them.

**Limitations.** I could not execute anything here: no endpoint is frozen, so there is nothing to mock against, and running a canary would be paid inference. All of §13 remains READ-ONLY and cannot be the deciding GO on transport.

### Attack H — cost and proportionality (EXECUTED)

Per confirmatory scenario at 56 decision steps (midpoint of §8's 48 to 64): two primary arms at 56 calls each, the 25% diagnostic subset at two more arms, one batched status probe per diagnostic arm, a 10% oracle and control fraction across three conditions, and a 5% transport loss allowance gives **165.7 calls per scenario**. Reconstruction adds no paid calls.

Token assumptions: 3,000 input tokens per call (frozen schema declarations plus a roughly 70% utilized 3,072-token payload plus current observation and available actions) and 80 output tokens typical against a derived cap near 830.

| n | calls | input (M tok) | $ at 1/5 | $ at 3/15 | $ at 15/75 | serial days at 3s |
|---:|---:|---:|---:|---:|---:|---:|
| 48 | 7,953 | 23.9 | 27 | 81 | 406 | 0.3 |
| 96 | 15,906 | 47.7 | 54 | 162 | 811 | 0.6 |
| 192 | 31,812 | 95.4 | 108 | 324 | 1,622 | 1.1 |
| 384 | 63,625 | 190.9 | 216 | 649 | 3,245 | 2.2 |
| 768 | 127,250 | 381.7 | 433 | 1,298 | 6,490 | 4.4 |
| 1,536 | 254,500 | 763.5 | 865 | 2,596 | 12,979 | 8.8 |
| 3,072 | 509,000 | 1,527.0 | 1,731 | 5,192 | 25,959 | 17.7 |
| **8,724** (Attack E's own envelope) | **1,445,480** | **4,336** | **4,915** | **14,744** | **73,719** | **50.2** |

**The proportionality finding r3 does not make.** §12 mandates one in-flight model request. Wall clock is therefore linear in calls and **cannot be bought down with money**. At n=192 the confirmation run is about a day. At the `n` a distribution-free interval would actually require (high hundreds to low thousands), it is one to two weeks of continuous serial execution with no failure. At the `n` §17.3's envelope demands, it is fifty days. r3's §17.4 cost gate publishes dollars and never publishes duration, so `UNDERFUNDED` can only fire on the axis that is not binding.

**Deletable machinery, measured.** Dropping the oracle and control fraction removes 10.6% of calls. Dropping the 25% diagnostic subset removes 18.4%. Halving decision steps from 56 to 28 removes 50% and is by far the largest lever, since `n` and steps multiply. My recommendation on each is in §11 below.

---

## 9. WHAT WOULD YOU BUILD?

**Mechanism 1: measure the cost side, because that is where the effect actually lives.** Keep FM and TN and the F1 outcome, and add a co-primary that r3 has no analogue for: **materialization cost under a fixed render-time compute budget**. The honest difference between a typed store and an append-only journal is not what they know, which Attack A shows is the same thing, but what it costs to answer a query from each: TN amortizes maintenance at write time, F+ pays at read time. Define the treatment as *precomputed typed index versus on-demand replay at equal render-time budget*, cap the render-time compute for both arms, and let the arms differ in what they can produce inside it. Then a TN win means "typed maintenance buys you a better packet for the same read-time budget," which is a claim a build decision can act on.

Prior art I would take it from: the Chinese-language secondary surface I opened on filesystem-based agent memory reports that the one benefit structured organization reliably delivers is cheaper retrieval, halving per-retrieval cost in the densest settings and shrinking to near-parity when the material volume is small, while accuracy effects were not the stable finding. **Label: SEARCHED, but a secondary blog summarizing a paper I did not open, so this is a pointer at primary-source strength, not primary evidence.**

**Mechanism 2: the coarse-invalidation arm.** `Presentation, Not Mechanism` decomposes the ledger gain into render plus mechanism and reports the fine-grained mechanism residual as indistinguishable from zero while **coarse-grained deprecation gives +0.087 with a 95% interval of [+0.046, +0.130]**. r3's TN is fine-grained (version chains, validity intervals, provenance closure, conflict objects). The only mechanism prior art measured as nonzero has no arm in r3. Add **FC**: flat store plus terminal and superseded flags only, no version chain, no validity intervals, no provenance, rendered through the same native layout. F+ already persists tombstones, so FC is nearly free to build, and `FC - FM` targets the one effect with an empirical prior big enough for the `n` you can afford. **Label: SEARCHED (arXiv 2607.16019, abstract, HTML render and Table 2 extract opened this session).**

**Mechanism 3: distribution-free bounded-mean inference.** As in Attack E. Deletes §17.3.2 through §17.3.5 outright and replaces a 4-page uncertifiable gate with a width target and a stopping rule. **Label: SEARCHED (Waudby-Smith and Ramdas, JRSS-B 86(1) 1-27, 2024).**

**Mechanism 4: the directory-rename reconstruction witness.** As in Attack F. One line of harness, closes the one continuity channel §11 leaves open. **Label: EXECUTED reasoning against the pinned §11 text, RECALLED as a general technique.**

---

## 10. WOULD YOU DESIGN IT DIFFERENTLY?

Yes, in four places, and I would keep everything else.

**(1) Change the primary outcome, not just the arms.** StateFuse ran the closest matched comparison already: conflict-preserving typed memory against flat multi-value, raw-log, provenance-style and collapsed baselines, under matched resolver and verification policies, on an official conflict-bearing benchmark slice. The compared methods **tied on answer accuracy**, and the value appeared in contradiction surfacing, safer abstention and auditable correction. Its authors state the claim narrowly and explicitly disclaim a universal accuracy gain. r3 puts all its statistical power on the channel that tied and demotes the channel that won to a secondary probe that "cannot create a primary win" (§4.3). I would swap them: make the status and abstention contrast co-primary with a preregistered threshold and its own power analysis, and keep set-F1 as the harm-check that TN must not lose on. **Label: SEARCHED (arXiv 2607.05844, University of Hong Kong; abstract and introduction opened at the arXiv PDF origin, full-text fetch returned no machine-readable text).**

**(2) Halve the decision steps and spend the savings on `n`.** Steps and `n` multiply in cost but only `n` buys statistical resolution, since §15.1 correctly says decisions within a trajectory are not independent samples. 48 to 64 steps per scenario is a *presentation* choice about how much history accumulates, and much of that accumulation can be front-loaded into the admitted event journal rather than into paid decisions. Cutting to 28 to 32 steps halves cost at constant `n`, or doubles `n` at constant cost. Given that condition 3 needs `n` in the hundreds at any plausible SD, this is the single most valuable structural change in the document.

**(3) Delete the DiD claim, keep the cells.** The 2x2 costs 18.4% of calls and returns a difference-in-differences with roughly four times the primary standard error. Keep F+ and TF as descriptive cells at the same 25% and drop the attribution claim in C4, or size the subset to a stated half-width. Do not keep the claim at the current subset size.

**(4) Set the threshold from the prior, not from taste.** `+0.03` is asserted as "the minimum worthwhile boundary" with no derivation. The only comparable published mechanism residual is `+0.087 [+0.046, +0.130]` for coarse deprecation and approximately zero for fine-grained typing, and the closest prospective-action benchmark, PM-Bench, reports the best configuration reaching only 65.1% F1, so there is both headroom and a large per-arm variance to fight. A threshold of `+0.05` costs about a third of the `n` that `+0.03` costs at the same power and sits inside the only nonzero prior interval. **Label: SEARCHED (arXiv 2607.12385 for PM-Bench, arXiv 2607.16019 for the residuals).**

---

## 11. Omission attack

| Required item | Answer |
|---|---|
| **Strong simple comparator still omitted** | **FC, a coarse-invalidation arm**: flat store plus terminal and superseded flags, no version chain, no validity intervals, no provenance closure, native render. It is the only mechanism prior art measured as nonzero (+0.087 [+0.046, +0.130]) and r3 has no arm for it. It is nearly free because F+ already persists tombstones. Evidence: SEARCHED, arXiv 2607.16019 Table 2. |
| **Hidden confound favouring FM** | **Overflow exclusion is TN-size-driven** (F5): classification uses realized per-arm serialization, TN is always larger (proxy ratio 1.93), so excluded fixtures are excluded because of typed density, depleting the cohort of the worlds where the treatment concentrates. Secondary: whole-scenario invalidation (F6) if denser packets raise invalid-output rates. |
| **Hidden confound favouring TN** | **Empty typed fields assert absence** (F4). FM renders `"conflict": []` where a conflict exists and is recoverable from FM's own store. §5.3's `rather than inferred` clause withholds F+-derivable content by rule, so the "render-matched" control is content-degraded, not merely mechanism-neutralized. |
| **Persuasive false-positive story** | Budget is sized to fit TN's joint maximum (§9.2.1), so at every ordinary checkpoint FM sits well below the ceiling with slack it may not spend, while TN uses the full budget productively. The model reads TN's populated conflict and supersession fields as decision hints and FM's empty ones as evidence of no conflict. `TN - FM` comes back at +0.05 with a lower endpoint above +0.03. The council reads it as typed mechanisms earning complexity. What actually happened is that the control was told there were no conflicts and the treatment was told there were, over an identical selected record set that §7 guaranteed was identical. |
| **Persuasive false-kill story** | Gate 1 enforces semantic-ID parity, so the store difference is invisible by construction (Attack A). All 36 positives are replay-derivable, so no scored item needs a typed-exclusive fact (F3). Overflow exclusion removes the densest typed worlds (F5). Whole-scenario zeroes land on the denser arm (F6). The result comes back at +0.004 with an upper endpoint below +0.03, and Moonwalker kills typed continuity for prospective action on the basis of an instrument that removed the treatment before the first paid call. |
| **Footgun not caught by a gate** | **Sticky routing** (F9). It is account-level state, keyed by a hash of the first system message plus the first non-system message, with a five-minute inactivity expiry. Under §12's single-in-flight rule and §14's within-block randomization it makes endpoint assignment a function of arm order and pacing. Gate 3 asserts endpoint identity per call but nothing in r3 asserts that the *sticky key* is arm-invariant, and a byte-exact request wrapper cannot detect it. |
| **One no-paid test without which I refuse pilot inference** | **The F+ / TN selected-semantic-ID equivalence test, run against the real reducers on the frozen generator output rather than on Gate-1 fixtures.** Take 200 generated scenarios, run both reducers and the §7 selector at every decision step, and report the fraction of steps at which the selected obligation and action sets differ. If that fraction is at or near zero, the paid experiment cannot measure a mechanism difference and must not be run as framed. My nine-family version says it will be zero. It costs an afternoon and it decides whether the whole design is worth funding. |
| **One mechanism to borrow directly** | **Waudby-Smith and Ramdas bounded-mean intervals** (JRSS-B 86(1) 1-27, 2024). Predictable-plug-in empirical Bernstein for the fixed-`n` interval, and the time-uniform confidence sequence for anytime-valid stopping. Deletes the entire uncertifiable family envelope, gives finite-sample coverage by theorem on the [-1, 1] delta, and turns an unaffordable fixed-`n` design into a cost-adaptive one. SEARCHED. |
| **Machinery to delete** | **The 25% F+/TF diagnostic subset as currently specified** (18.4% of calls) and **§17.3.2 through §17.3.5's family and grid manifest** (all of Gate 4's simulation work). The first buys a DiD it cannot resolve; the second is replaced wholesale by mechanism 3. Redirect both into `n` and into the FC arm. Everything else in r3 is load-bearing. |

---

## 12. Sweep log

| Lane | Exact query | Opened at origin | Decisive section | Level | Effect on ruling | Stop reason |
|---|---|---|---|---|---|---|
| 2. Render/mechanism factorial | `"Presentation, Not Mechanism" arXiv 2607.16019 render-matched memory` | `arxiv.org/abs/2607.16019`, `arxiv.org/html/2607.16019v1`, `arxiv.org/pdf/2607.16019` | Abstract plus Table 2 render-matched decomposition; Figure 3 caption "Provenance needs retention, not typing" | SEARCHED, primary | Decisive. Fine-grained mechanism residual indistinguishable from zero, coarse-d at +0.087 [+0.046, +0.130], almost all apparent gain is render. Drives F2, C3, the FC recommendation, and the threshold argument. | Found the exact decomposition table and the effect sizes. Nothing further would change the ruling. |
| 1. Already answered | `StateFuse arXiv 2607.05844` | `arxiv.org/pdf/2607.05844` (abstract and introduction returned by the index; my own full-text fetch returned no machine-readable text) | Abstract: matched-resolver comparison against flat multi-value, raw-log, provenance and collapsed baselines; methods tie on answer accuracy; value is in contradiction surfacing and abstention; explicit disclaimer of universal accuracy gain | SEARCHED, primary, partial read | Decisive for §10(1). The nearest matched comparison already ran and tied on the accuracy channel r3 makes primary. University of Hong Kong satisfies the named non-US, non-UK institution requirement. | Full-text fetch failed; abstract carries the deciding claim explicitly, so escalation was not worth the write. **Partial read, logged as partial.** |
| 3. Prospective action | `PM-Bench prospective memory benchmark agent action selection lures set-F1 Mem2ActBench` | `arxiv.org/html/2607.12385v1`, `arxiv.org/abs/2601.19935`, `aclanthology.org/2026.acl-long.370.pdf`, `arxiv.org/pdf/2606.23459` | PM-Bench: best configuration reaches 65.1% F1. Mem2ActBench: memory-driven execution gap of over 23 F1 points. TriggerBench: PM is harder than RM, passive retrieval near-saturates while proactive intervention declines. MemoryAgentBench: multi-hop conflict resolution at or below 6% for all paradigms. | SEARCHED, primary | Confirms r3's workload framing is well grounded and gives an empirical ceiling (per-arm F1 near 0.65) that makes the delta SD assumption load-bearing. The 6% conflict-resolution floor reinforces F3. | Four benchmarks opened, consistent picture, marginal return falling. AgenticSTS and LongHorizon-Harness left unopened (DID-NOT). |
| 4. Bounded paired inference | `Waudby-Smith Ramdas estimating means of bounded random variables betting confidence intervals empirical Bernstein` | `academic.oup.com/jrsssb/article/86/1/1/7043257`, `rss.org.uk` discussion-meeting PDF, `arxiv.org/abs/2010.09686` | Closed-form empirical-Bernstein CIs and CSs converging to oracle Bernstein width, plus non-closed-form betting CIs; variance-adaptive; extends to sampling without replacement | SEARCHED, primary | Supplies the executable replacement for §17.2 and §17.3. | Found the controlling primary. Exact finite-support and indifference-zone lanes left unopened (DID-NOT). |
| 6. OpenRouter | `OpenRouter provider routing docs allow_fallbacks require_parameters only endpoint selection 2026`; `OpenRouter transforms middle-out default prompt caching usage accounting response cache docs` | `openrouter.ai/docs/guides/routing/provider-selection`, `openrouter.ai/docs/guides/best-practices/prompt-caching`, `openrouter.ai/blog/announcements/response-caching/`, `openrouter.ai/blog/insights/model-routing/`, `openrouter.ai/blog/tutorials/keep-your-agent-running-when-models-disappear/` | Sticky-routing granularity and hashing rule; five-minute expiry; presets shallow-merged server-side; `models` array XOR-gated with `model`; response cache scoped to API key and bypassing the provider; `cached_tokens` and `cache_discount` as the hit signals; default `allow_fallbacks: true` and `require_parameters: false`; inverse-square-of-price default weighting | SEARCHED, primary vendor docs, checked this session | Drives F9 and F13. Establishes that account-level state, not request bytes, determines the served condition. | Both routing and caching surfaces opened at the vendor origin and current within hours to days. |
| 5. Generator bias, national-language pass | `自生成基准偏差 智能体记忆 结构化与扁平基线 对比实验 生成器偏置` | `tonybai.com/2026/08/05/filesystem-based-memory-for-llm-agents/`, `zhuanlan.zhihu.com/p/1988593383057429498` | The only stable benefit of structured organization is cheaper retrieval, halving per-retrieval cost in the densest settings and shrinking to near-parity at low material volume; the shape of the memory store is determined by the organizing model rather than by the data | SEARCHED, **secondary** (blog summarizing a paper I did not open) | Corroborates §9 mechanism 1 (measure cost, not only accuracy) and the own-generator-shape concern behind §8.2. Not load-bearing on its own because it is secondary. | Language pass produced one on-point surface; the primary paper behind it was not identified, so I stopped rather than chase it and labelled the evidence honestly. On own-generator bias specifically I found no primary source this session, so **C5's generator-bias half rests on r3's own construction and on my arithmetic, not on prior art**. |

---

## 13. Residual risks and explicit non-claims

**Residual risks I am leaving open.**

1. My equivalence result (Attack A) depends on the §5.3 transition table being **total**. If the intended table is partial, C3 recovers and F2 weakens substantially. r3's own text says it is total; if that is a drafting artifact rather than intent, say so in r4 and I would revisit.
2. Every budget and output-cap number is **proxy**, because §9.1.1 defers the tokenizer. The direction of my §9.2 finding is robust to a 30% proxy error; the exact ceiling is not.
3. The empty-field-salience mechanism (F4) is a claim about model reading behaviour and is unfalsifiable without paid inference. I did not run it and I do not claim it as measured. I claim only that the design permits it and that the F4 fix removes it for free.
4. My `n` guidance assumes a delta SD that nobody has measured. If the paired correlation between FM and TN scenario F1 is high, SD could be near 0.10 and `n` near 100 suffices. That parameter is the whole ballgame and r3 has no way to learn it.
5. All of §13 is READ-ONLY from me. No endpoint is frozen, so I could mock nothing. A READ-ONLY verdict on transport cannot be the deciding GO, and mine is not: my NO-GO rests on F1 and F2, both EXECUTED.

**Explicit non-claims.**

- I do **not** claim typed continuity memory is worthless. I claim r3 cannot detect its value on the axis it measures.
- I do **not** claim the design is unsalvageable. The five fixes named in §10 plus F1 through F10 produce a fundable r4.
- I do **not** claim any licensing, security, deployment or model-family position. Those were ruled non-load-bearing in §5 and I did not smuggle them back in.
- I do **not** claim my proxy tokenizer certifies anything.
- I did **not** open AgenticSTS, LongHorizon-Harness, LongMemEval-V2, MemoryArena, the Inspect documentation, the NIST SD guidance, or any primary source on own-generator bias, and no ruling above rests on them.

---

## 14. Seat capability and seal report

| Dimension | Status |
|---|---|
| Local file read | Full, via the Moonwalker bridge. Verified byte-exact against the git object before relying on any content. |
| Local shell | Available. Two calls, both sentinel-verified: unique token as the first output line, token confirmed in stdout, and the echoed `command` field compared against what I sent. Zero crossings, zero foreign payloads. |
| Code execution | Available in an isolated Linux container (Python 3, numpy 2.4.4, scipy 1.17.1). No network egress. Seven scripts written and run. `tiktoken` unavailable and not installable without egress, hence the disclosed proxy tokenizer. |
| Web | Native `web_search` and `web_fetch` both live. Six searches, one fetch attempt. One fetch failure (`arxiv.org/pdf/2607.05844` returned no machine-readable text) and one permissions refusal (`openrouter.ai/docs/features/provider-routing`, a URL not previously surfaced), both worked around by searching for the surfaced URL instead. **No Moonwalker crawler escalation was needed and none was performed.** |
| Tokenizer | **LIMITED.** No target tokenizer frozen in r3 and none available offline. All Attack-D numbers are proxy and separated from certification throughout. |
| Statistical | Full. Monte Carlo at R = 8,000 to 40,000 per cell, chunked for large `n`. Simulation error at R = 20,000 is roughly ±0.007 at a 0.94 coverage target, which is an order of magnitude smaller than every gap I report. |
| Paid inference | **NONE.** No model call, no canary, no API request of any kind. |
| Side effects | **NONE on the user's machine.** No file created, modified, moved or deleted anywhere under `C:\`. No git object written, no branch, no stash, no index change. Both shell calls were read-only (`git rev-parse`, `cat-file`, `status --porcelain`, `merge-base`, `config --get`, plus in-memory hashing through a piped stream, chosen specifically so that no temporary file was written). All seven of my scripts live only in the container sandbox and are discarded with it. No browser session opened, no tab spawned, no council seat contacted. |
| Verdict delivery | In-thread, as this reply. Nothing written to a file, artifact, canvas or vault. Banking is the driver's job. |

**Sealed-independence confirmation.** I read exactly four files: the packet (`MBCX-01-EXPERIMENT-COUNCIL-PACKET-r4.md`), the seat role card (`<vault>`, named by packet §0), the pinned design (`MBCX-01-EXPERIMENT-DESIGN-r3.md`, blob `4d7fd50`), and the pinned local source manifest (`LOCAL-SOURCE-MANIFEST-r1.md`, permitted by packet §0). Every one was reached by exact explicit path. I did **not** recursively list, glob, grep, index, or tokenizer-search the repository. I ran no `moonwalker_search_files`, no `moonwalker_grep`, no `moonwalker_ls`, no `moonwalker_memory_search`, and no `dir` or `Get-ChildItem`. I opened no prior council report, synthesis, exec log, receipt, watcher, restart manifest, or browser output, and no file whose name contains `VERDICT`, `SYNTHESIS`, `EXEC-`, `RECEIPT`, or `RESTART-MANIFEST`. No prohibited snippet reached my context by any route. **The seal held. No protocol failure to disclose.**