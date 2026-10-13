Pin verified byte-exact. Before I run the round, one disclosure that materially affects how you should weight this verdict.# MBCX-01 r4 COUNCIL VERDICT — SEXTANT-OPUS5-CLAUDEAIMCP-MBCX01-R5-20260812T

> **SEAL DISCLOSURE, READ FIRST.** This seat is **not fresh and not independent of the prior round**. I am the same conversation that adjudicated `MBCX-01-EXPERIMENT-DESIGN-r3.md` earlier today and returned NO-GO. r4 adopts several things that verdict recommended: the FC coarse-invalidation arm, Waudby-Smith and Ramdas bounded-mean inference in place of Student-t, the source-directory rename reconstruction witness, the "empty fields never mean a candidate failed" rule, the complete action universe, and retirement of the degenerate `TN - FM` contrast. **I cannot give you an independent read on whether those specific changes were the right ones, because I proposed them.** Weight sections 6, 9 and 10 accordingly, and get a genuinely fresh seat on the statistics and the FC arm before you treat convergence as confirmation. Everything below that is *new* attack surface (the algebra, the archive axis, the cohort arithmetic, the handoff, the scale accounting) is not contaminated in that way. Packet r5 §0 asks for sealed independence from other seats' reports; it does not address a seat carrying its own prior round, so I am disclosing rather than assuming.

---

## 1. Top-level verdict

**GO-WITH-FIXES(three P0 specification repairs before Stage 0 implementation: the 240-versus-384 cohort arithmetic, the unnamed bitemporal currentness clock, and a missing active-subject depth axis that lets the bounded-continuity gate pass without testing what it claims).**

This is a different document from r3 and a much better one. The three-question decomposition is the correct repair, the retirement of `TN - FM` is honest and correctly reasoned, the byte-identity deduplication rule closes the fake-treatment hole, `contract_success` with zero-failure hard gates is the right shape for obligation state, and Stage 2 is now genuinely affordable (my own accounting puts it at roughly $82 to $1,230 and three to seven hours of wall clock, against r3's implied $14,744 and fifty days). The statistical machinery I could execute against is sound: my reference implementation of the confidence sequence delivers coverage of 0.999 across all three looks, which is the opposite of r3's 0.38.

It does not close, for three reasons that are each a local specification repair rather than a redesign:

- **P0-1.** §7.1 freezes a cohort of 240 scenarios. §12.1 runs looks to a hard cap of `n = 384`. 144 scenarios do not exist, and §12.4 forbids reserve substitution. The inference plan cannot be executed against the frozen cohort.
- **P0-2.** §4.2 puts `observed_at`, `valid_from` and `valid_to_or_null` on every event, and never says which clock decides "current". I built a three-event legal trace on which two defensible readings return different gold. The table cannot be total, and §5 would log the resulting FD/TN divergence as a mechanism residual when it is a spec gap.
- **P0-3.** §7.2 defines archive growth as **dormant** padding with the active world held identical. I implemented FD, FC and TN and measured primitive-object reads: all three are perfectly flat across `H = 128` to `100,000`. The bounded-history gate passes every candidate, including the pure read-time deriver, without testing anything. On the axis r4 does not have, active-subject history depth, FD goes from 24 reads to 2,064 reads while FC and TN stay flat. That is a **false pass on deciding question (a)**, which packet §2 names as load-bearing.

None of these requires changing the causal program. Fix them and I expect a GO.

---

## 2. Seat identity

| Field | Value |
|---|---|
| Model as actually exposed | Claude Opus 5 (`claude-opus-5`) |
| Harness | claude.ai chat surface, Moonwalker MCP bridge, plus an isolated Linux container (Python 3, numpy 2.4.4, scipy 1.17.1, no network egress) |
| Native web tools | `web_search` and `web_fetch` live this session |
| Paid inference | **NONE** |
| Independence | **COMPROMISED with respect to the r3 round.** See the disclosure above. |
| Report title | MBCX-01 r4 COUNCIL VERDICT — SEXTANT-OPUS5-CLAUDEAIMCP-MBCX01-R5-20260812T |

---

## 3. Pin and byte verification

Verified by `git`, sentinel-guarded (unique token first in stdout, echoed `command` field compared against what I sent; one call, no crossing).

| Packet §0 claim | Measured | Result |
|---|---|---|
| Commit `4e45d16ad85f7033e13368e133f30588c47848a7` | `git cat-file -t` returns `commit` | MATCH |
| Blob `3f627032a1c54babc7c1aad5f0146a49138a5412` | `git rev-parse 4e45d16:MBCX-01-EXPERIMENT-DESIGN-r4.md` = `3f62703...` | MATCH |
| Bytes `28,155` | `cat-file -s` = 28155; piped blob stream = 28,155 | MATCH |
| Lines `614` | 614 LF, 0 CR | MATCH |
| SHA-384 `FCEB7E5E...8E3DEEB8` | `FCEB7E5E6757D649019DC69F6A6CB739420C7B4315EFFD26391E8CAD72B893F92E1542569747A6A2F19E4C088E3DEEB8` | MATCH |

**Working-copy difference: NONE.** `git status --porcelain` empty on the path; `HEAD:MBCX-01-EXPERIMENT-DESIGN-r4.md` resolves to the same blob; on-disk file byte-identical to the blob. HEAD is `072d4593cfe27f2ebedd3e2f2add6cef2fd2ae6d`. I adjudicated blob `3f62703`, read through the working copy after proving byte identity.

Also opened by exact explicit path: `<vault>` (packet §0). **I did not open any of the seven lineage artifacts authorized by packet §1.** They are permitted, not required; my findings rest on the pinned design, my own probes, and external primary sources, so opening them would have added exposure without adding evidence. That is a deliberate choice, logged as UNSEARCHED with reason below.

---

## 4. Evidence and probes

**EXECUTED** (container, no paid inference, no writes to your machine)

| Probe | Produces |
|---|---|
| `arith.py` | Cohort-versus-look arithmetic; `contract_success` conjunction against the 0.80 oracle floor; worst-case missingness against the `-0.10` margin; Stage-1 journal volume and materialization counts. |
| `cs.py` | Faithful reference implementation of the predictable-plug-in empirical-Bernstein confidence sequence on `[-1,1]` paired binary deltas; coverage and decision rates at all three looks; tuning-constant sensitivity; maximum tolerable BC/OM discordance. |
| `mech.py` | FD, FC and TN reducers over r4's 16-type event algebra with instrumented primitive-object reads; r4's dormant archive axis at `H = 128 / 1,024 / 10,000 / 100,000`; an active-subject depth axis at `D = 1 / 4 / 16 / 64 / 256`; nine-family semantic parity. |
| `bitemporal.py` | A legal three-event trace on which transaction-time and valid-time readings return different gold. |
| `cost.py` | Stage-2 calls, tokens, dollars and wall clock at `n = 96 / 192 / 384` under both readings of "scored handoff decision". |

**READ-ONLY**: §10 reconstruction witnesses (no harness to run them against; attacked by constructing a passing-but-hollow implementation). §13 transport (no endpoint frozen). §11.4 handoff discipline (attacked by channel analysis on the `WorkerHandoffV1` schema).

**SEARCHED this session**: MINTEval (arXiv 2605.18565); LongMemEval-V2 (arXiv 2605.12493); Text2Mem (arXiv 2509.11145); MemTrace (arXiv 2605.28732) and the HaluMem/MemoryArena/EMemBench/AgentLongBench pointers it carries; Temporal, Restate, LangGraph and Inngest durable-execution surfaces plus the Burckhardt-formalization pointer in arXiv 2606.17182. **SEARCHED earlier in this same session and carried forward** (opened at origin, so not RECALLED, but disclosed as prior-round work): StateFuse arXiv 2607.05844; Presentation Not Mechanism arXiv 2607.16019; PM-Bench arXiv 2607.12385; Mem2ActBench arXiv 2601.19935; TriggerBench arXiv 2606.23459; Waudby-Smith and Ramdas JRSS-B 86(1) 1-27 (2024); OpenRouter provider-selection and prompt-caching docs.

**UNSEARCHED, with reasons**: the seven packet-§1 lineage artifacts (**NOT-LOAD-BEARING** for the findings I actually make; deliberate, see §3). Exact/near-exact paired binary noninferiority alternatives and e-value optional-stopping literature beyond WSR (**DID-NOT**; the CS I implemented already delivers 0.999 coverage, so the marginal value was low, but this means my "no better procedure exists at n=384" is not a claim I make). Blackboard architectures and shared selective persistent memory as a named literature (**DID-NOT**; I reached the durable-execution surface instead, which covers the commit-boundary mechanism I recommend). Active-frontier scaling and page-fault literature (**DID-NOT**; my depth-axis finding is arithmetic and executed, not prior-art-dependent).

---

## 5. Applicability ruling

Excluded per packet §2 with no direct path to a load-bearing failure: licensing, patents, commercialization, clean-room; hostile actors, prompt injection, FIPS/CNSA, production authorization topology; daemon and fleet lifecycle, packaging, deployment, PR process, service hardening; cross-model generalization, concurrent canonical writers, procedural-memory product design.

Retained because they do have that path: the crash window between provider response and commit-event append (alters retained outcomes); free-text fields in `WorkerHandoffV1` (alters what the A→B→A claim means); EF applicability (alters which scenarios a diagnostic cell is computed on); artifact open and decode cost (hides archive-linear work outside the measured window).

**One ruling against myself:** benign cross-scope collision is in scope by r4 §2's own sentence, and my own reducer produced a cross-scope collision on trace family 8 because I keyed the subject index on `subject_id` alone. That is a shortcut in my implementation, not a defect in r4, but the fact that the natural reading of §5's "generic public-ID indexes ... by scope, subject, obligation ID" produces it is a genuine finding, logged as F11.

---

## 6. Claim scoreboard C1 to C12

| Claim | Ruling | Basis |
|---|---|---|
| **C1** r4 preserves the North Star | **HOLDS** | §1 and §16 state explicitly that a TN mechanism loss does not falsify bounded continuity, and the Stage-0/1/2 nesting enforces it structurally. I traced both worlds Attack A asks for and r4 produces the correct different program decisions in each. This is the single best repair in the document. |
| **C2** the algebra and reference boundary are complete | **FALSE** | EXECUTED: a legal three-event trace with a retroactive correction yields RED under transaction-time and AMBER under valid-time. §4.2 declares both clocks and names neither as governing. Also undefined: the index key structure (F11), scope membership after `delegate_obligation` (F7), and the term "propagation barrier" used in a zero-tolerance gate at §9.1 and defined nowhere (F8). |
| **C3** obligation hard gates are appropriate and executable | **UNDERDETERMINED** | The gate *shape* is right and I endorse it. But one of the eight universal gates is stated against an undefined term ("after the propagation barrier"), and a second ("0 wrong-scope semantic admissions") collides with undefined cross-scope delegation semantics. A zero-tolerance gate whose predicate is undefined is not executable. |
| **C4** FD and FC are the strongest cheap comparators | **HOLDS** | EXECUTED: nine trace families, FD/FC/TN semantic parity in all nine, including correct-then-retract-the-correction, cancel-then-legal-reopen, propose/reject, propose/commit, and a depth-3 correction chain. FD is genuinely given the full derivation path and is not strawmanned. |
| **C5** parity plus unique-packet deduplication prevents a degenerate claim | **HOLDS** | §5's "if byte-identical, one call, mapped to every mechanism that produced it" is the correct and honest rule, and §6.1's "empty fields mean the reference reducer proved the set empty, never that a candidate failed" closes the empty-field-asserts-absence hole. The declared-residual taxonomy is the right shape. |
| **C6** archive-padding twins test boundedness | **FALSE** | EXECUTED: FD, FC and TN read 24, 12 and 16 primitive objects respectively, **identically at every `H` from 128 to 100,000**. The gate is satisfied by any index-based mechanism because the padding never touches an active subject. On depth, FD goes 24 → 48 → 144 → 528 → 2,064 while FC and TN stay at 12 and 16. |
| **C7** A→B→A isolates continuity | **UNDERDETERMINED** | The structural discipline is right. Two open channels: `proposed_claims[]`, `unresolved_items[]` and `warnings[]` in `WorkerHandoffV1` are untyped and uncapped, so B's reasoning can reach fresh A through the committed journal; and the window between provider response receipt and commit-event append is not journaled, so a crash there either loses a paid proposal or duplicates it. |
| **C8** the action universe and scorer are executable | **UNDERDETERMINED** | Two undefined quantities that change the answer: gold is capped at 1-3 actions while §7.2 permits up to 4 due critical obligations, which forces an unstated generator constraint precisely on the hardest continuity case; and the number of scored handoff decisions per scenario is never stated, which makes both the conjunction length and the cost table undecidable. |
| **C9** the Stage-1 mechanism recommendation is fair | **FALSE** | §9.3's tie-break prefers `FD, FC, TN` and demands strict dominance. §11.1's lexicographic selection orders on **read-side metrics first** (p95 primitive objects inspected, then p95 latency) with write work only third. Read-side-first systematically selects the precomputing mechanism. The two procedures can and generally will disagree, and r4 never says which governs the engineering recommendation. |
| **C10** the paid usability screen is coherent and proportionate | **UNDERDETERMINED** | EXECUTED and largely good: coverage 0.999 at all three looks, no optional-stopping penalty, correct behaviour at true delta 0, `-0.10` and `+0.10`. But three unstated quantities decide it: the CS tuning constants (a `c` change from 0.5 to 0.75 moves the half-width from 0.0973 to 0.1143, straddling the margin), the tolerable BC/OM discordance (n=384 concludes only below 0.20), and the interaction with §12.4's 5% missing ceiling, which consumes the entire margin. |
| **C11** baselines, reconstruction, transport and cost cannot choose the answer | **UNDERDETERMINED** | EF is defined as complete evidence "where it fits the target context", so EF runs only on small worlds and its cohort is size-selected. Reconstruction still has no rebuild-equality witness, so a candidate persisting a materialized packet passes all six witnesses and trivially passes the boundedness gate. |
| **C12** r4 is the smallest decisive instrument | **FALSE** | EXECUTED: EF and XT together consume **90% of Stage-2 input tokens** while being 25% cells that §11.3 says cannot create the primary conclusion. Stage 1's 30-repetition measurement across both axes implies 4.67M materializations and 30 to 58 GB of journals, none of which appears in §12.5's cost table. |

---

## 7. Finding table

| ID | Sev | Location | False-result mechanism | Smallest fix | Evidence |
|---|---|---|---|---|---|
| **F1** | **P0** | §7.1 vs §12.1 | Unexecutable plan. Cohort is 240; the hard cap is 384; §12.4 forbids substitution. 144 scenarios (6 blocks) do not exist, and the 25% diagnostic allocation at n=384 needs 96 scenarios against a cohort that supplies 60. | Either raise the generator to `6 x 64 = 384` seeds and re-freeze, or cap looks at `96 / 168 / 240`. State which, and re-derive the diagnostic allocation from the same number. | EXECUTED |
| **F2** | **P0** | §4.2, §4.3 | Gold is underdetermined. Both `observed_at` and `valid_from`/`valid_to_or_null` are declared; nothing names the clock that decides currentness, and §4.3 uses a bare `now`. A retroactive correction returns RED under transaction time and AMBER under valid time. FD naturally implements the first, TN the second, so the divergence would be logged under §5 as a mechanism residual when it is a spec gap. | Name the governing clock in §4.2, state whether retroactive `valid_from` is legal, and if bitemporal semantics are intended, make `O_due` a function of both clocks and add the retroactive-correction trace to §7.4. | EXECUTED |
| **F3** | **P0** | §7.2, §9.2 | False pass on the primary question. Archive growth is operationalized as dormant events touching no active subject, so the boundedness gate is satisfied by any indexed mechanism without testing the growth that actually threatens a long-lived conductor: deep per-subject history. FD is flat in `H` and linear in depth. | Add a third axis `D` (superseding/correcting events per active subject, e.g. 1/4/16/64/256) at fixed `H` and fixed `F`, and apply §9.2's inspection-identity gate to it. Report all three axes separately. | EXECUTED |
| **F4** | **P1** | §12.4 vs §12.3 | The stated missing-pair ceiling nullifies the stated margin. Forcing one pair from `+1` to `-1` moves the mean by `2/n`, so 5% missing consumes exactly 0.10, the whole margin. My simulation: PROMOTE at `n=384` needs discordance ≤ 0.20 with no missingness, ≤ 0.13 at 2% missing, and is **unreachable at 5%**. | Set the missing-pair ceiling from the margin rather than from habit: at margin `-0.10` and `n=384` the operational ceiling is about 1 to 2%. State it, and state the discordance budget the design is powered for. | EXECUTED |
| **F5** | **P1** | §12.2 | Unstated choice that changes the answer. The PrPl-EB construction has free constants (the `lambda` truncation `c`, the `sigma-hat` initialization, the alpha split). At `c = 0.5` my half-width at n=384 is 0.0973; at `c = 0.75` it is 0.1143. The decision boundary is 0.10. The constant flips the verdict. | Pin the reference implementation by name, version and hash (the authors' `confseq`-family code is the obvious candidate) **and** pin `c`, the initialization, and the alpha handling in the design text, not in the code. | EXECUTED |
| **F6** | **P1** | §8, §12.3 | Cost discovered too late. `contract_success` is a conjunction over "every scored handoff decision" and r4 never says how many there are. At k=3 the 0.80 oracle floor needs 0.928 per-decision reliability; at k=24 it needs 0.991. PM-Bench's best configuration reaches 0.651 F1 on prospective action. If k is large, Stage 2 returns `MODEL_OR_INTERFACE_CEILING` by arithmetic, after the full spend. | State k. If k > 3, either score contract success over the critical-obligation cuts only, or set the floor from the conjunction arithmetic rather than from a round number. | EXECUTED |
| **F7** | **P1** | §4.3, §9.1 | Zero-tolerance gate with an undefined predicate. `delegate_obligation` transfers ownership; nothing says whether delegation may cross scope, and if it may, whether the obligation then belongs in the delegate's scope packet. A correct cross-scope delegation could be counted as a wrong-scope admission, which is an instant `DESIGN_OR_IMPLEMENTATION_FAIL`. | One sentence in §4.3: delegation does or does not change `scope_id`, and scope membership for packet purposes is defined by X. Add a cross-scope delegation trace to §7.4. | READ-ONLY |
| **F8** | **P1** | §9.1 | Same class. The gate "0 stale terminal/corrected resurrection **after the propagation barrier**" uses a term that appears exactly once in r4 and is defined nowhere. Whoever implements it chooses what the gate means. | Define the propagation barrier in §4.2 as a named point in the algebra, or delete the qualifier and make the gate unconditional. | READ-ONLY |
| **F9** | **P1** | §9.3 vs §11.1 | Biased mechanism selection. §11.1 orders lexicographically on read-side metrics first; TN and FC precompute, so they win step 1 by construction. §9.3's tie-break prefers FD and requires strict dominance. The two procedures select different mechanisms and r4 never reconciles them. | Make §11.1's order match §9.3's decision (or state explicitly that §11.1 selects only the Stage-2 packet carrier and carries no engineering recommendation, which is defensible but must be said). | READ-ONLY |
| **F10** | **P1** | §9.2, §10 | Archive-linear work can hide outside the measured window. §9.2 gates "primitive objects inspected **by the materializer**"; nothing bounds artifact open and decode. A candidate that loads the whole journal at open, or that persists a materialized `DecisionPacketV1`, passes all six §10 witnesses and the boundedness gate while doing archive-proportional work. | Add cold-open cost to the §9.2 twin-identity gate, and add a seventh reconstruction witness: rebuild the projection from the journal and prove equality with the persisted projection (§4.1 asserts rebuildability; no gate checks it). | READ-ONLY |
| **F11** | **P1** | §5 "generic public-ID indexes" | Wrong-scope admission by index design. The index list reads "by scope, subject, obligation ID, dependency endpoint, and time" and does not say whether the subject index is scope-partitioned. My independently written reducer took the natural reading and collapsed `S1/NAME` and `S2/NAME`, which is exactly the motif-4 failure the zero-tolerance gate targets. | Specify the index key tuples explicitly, e.g. subject index keyed on `(scope_id, subject_id)`. One line. | EXECUTED (my implementation reproduced the failure) |
| **F12** | **P1** | §11.4, §4.1 | Lost or duplicated paid work. The window between the provider response arriving and the commit or rejection event being appended is not journaled. §12.4 covers accepted/no-body ambiguity at the transport layer, not crash-after-receipt at the runner layer, and §7.4's trace list has no process-death-mid-commit case. | Write-ahead the raw provider response to the journal before validation, then commit or reject from the recorded bytes (the Temporal/Restate record-and-replay discipline). Add the crash-mid-commit trace to §7.4 and to Gate 4. | READ-ONLY |
| **F13** | **P1** | §8 vs §7.2 | Unstated generator constraint on the hardest case. Gold is 1-3 actions per cut; up to 4 due critical obligations are permitted. Four simultaneously actionable critical obligations cannot be expressed, so the generator must silently avoid them, and that is precisely the continuity case the North Star cares most about. | Raise the gold cap to match the due-critical cap, or state the constraint explicitly and add a separate maximum-frontier trace family outside the scored cohort. | EXECUTED |
| **F14** | **P1** | §12.5, §9.3, §7.2, §7.3 | Cost discovered too late, on the unpaid side. §12.5's table covers paid calls only. Stage 1's naive reading is 26.7M archive-twin events plus 120M frontier events (5.3 to 10.7 GB and 24 to 48 GB respectively, times three candidate artifacts) and 4.67M measured materializations. At 100 ms each that is 130 core-hours; at 1 s, 1,296. | Extend §12.5 to Stage 1: state the cell allocation for both scaling axes (r4 never says whether the frontier axis runs on all 240 seeds), the repetition count's subsampling rule, and the storage ceiling. | EXECUTED |
| **F15** | **P2** | §11.3 | Content-correlated cohort for a diagnostic. EF is "complete public evidence ... where it fits the target context", so EF exists only for small worlds and never at `H = 100,000`. XT inherits EF's envelope. Comparing BC to EF across different effective subcohorts is biased. | State EF's applicability rule as an explicit scenario filter and report EF/XT only within it. | READ-ONLY |
| **F16** | **P2** | §6.3 | The declarative-handoff claim is weaker than it reads. `proposed_claims[]`, `unresolved_items[]` and `warnings[]` are untyped and uncapped, so B's natural-language reasoning reaches fresh A through the committed journal. | Type and cap them: public IDs plus enumerated codes only, or measure their token volume as a reported outcome so the channel is visible. | READ-ONLY |
| **F17** | **P2** | §12.3 | Untested branch. The packet's own Attack G list specifies deltas `0`, `-0.10`, `+0.10`. At all three, `P(MODEL_INTERFACE_FAIL)` is 0.000 to 0.001 in my simulation, because the FAIL branch needs the upper bound below the margin. The three-way rule is effectively two-way at n=384 unless the true delta sits well below `-0.10`. | Add a calibration point at, say, `-0.25` to the Gate-5 fixture list so the FAIL branch is exercised at least once before dispatch. | EXECUTED |

---

## 8. Attacks A to H

### Attack A — original-question and estimand drift (READ-ONLY trace, EXECUTED arithmetic)

I traced the three conclusions r4 §1 defines against the two worlds the packet demands.

**World 1: TN useless, bounded FD succeeds.** Corrections are shallow (depth 1), obligations are few and flat, no conflicts arise. FD, FC and TN emit byte-identical packets (confirmed in Attack C, nine of nine families). §9.2 passes for all three. §9.3 finds cost equivalence within measurement resolution and its tie-break records `FD`, with "typing did not earn its complexity" on the record. §16 states that this is not a memory-program failure. **r4 produces the correct decision.** This is the world r3 could not distinguish from a kill, and fixing that is r4's central achievement.

**World 2: no candidate is archive-bounded.** §9.2's first bullet fails for every candidate, §9.2's last sentence declares bounded continuity falsified for this workload, and §16 confines that to "the frozen workload and active-frontier envelope". **r4 produces the correct decision** and correctly refuses to generalize it.

**The drift I did find is in the opposite direction from r3's.** World 2 is unreachable as r4 defines the axis. My Attack D shows all three candidates pass §9.2 trivially at every `H`, so the falsification branch is dead on the archive axis and alive only on the frontier axis, which §7.3 explicitly excludes from the boundedness claim. **The primary question therefore has no failing branch under r4's own workload.** That is F3, and it is why I rate it P0 rather than P1: a gate that cannot fail is not evidence.

### Attack B — state algebra, SAT and scored universe (EXECUTED)

**Method.** Independent reducers for FD, FC and TN over the 16 event types, plus a hand enumeration of the two-event interactions r4 §7.4 names. I did not build a full SAT enumerator; the smallest honest substitute was nine hand-authored families driven through three independent implementations with set equality on the decoded state.

**Result on the families:** all nine agree across FD, FC and TN.

```
1 correct then retract the correction   parity=YES  state={'X':'P1'}
2 open then cancel then legal reopen    parity=YES  obl={'O1':'open'}
3 complete then stale duplicate         parity=YES  obl={'O1':'terminal'}
4 link unlink reverse activation        parity=YES  obl={'O1':'open','O2':'open'}
5 delegate then complete                parity=YES  obl={'O1':'terminal'}
6 handoff propose reject                parity=YES  obl={'O1':'open'}
7 handoff propose commit                parity=YES  obl={'O1':'terminal'}
8 cross-scope same-name subject          parity=YES  (and WRONG, see F11)
9 correction chain depth 3               parity=YES  state={'X':'P4'}
```

**Result on totality.** The table is **not** total as specified. Trace: `assert GREEN (observed 10, valid_from 10)`, `assert AMBER (observed 20, valid_from 20)`, `correct RED superseding E1 (observed 30, valid_from 15)`. Querying current state for the subject at decision time 25:

```
reading 1  transaction-time last write wins ......... RED
reading 2  valid-time interval containing now ....... AMBER
reading 3  bitemporal, as-of knowledge at now ....... AMBER
```

Two different gold values from one legal sequence. §4.2 asserts the table specifies "exact next state" for every legal pair and forbids candidate-specific interpretation; the clock is never named. This is F2.

**Result on the scored universe.** `available_action_ids[]` is 8-16 with 1-3 gold or `NO_ACTION`, which is clean and resolves r3's exposure-count contradiction. But 1-3 gold cannot express a cut with 4 due critical obligations, which §7.2 permits (F13). And "every legal generated cut has a complete action set and unique gold" cannot be proven while F2 stands, because gold itself is not unique.

**Limitations.** Nine families and a hand enumeration are not the SAT proof §14 Gate 1 requires. I did not enumerate all 16×16 two-event interactions; I attacked the ones §7.4 names plus the bitemporal case §7.4 omits.

### Attack C — FD/FC/TN bakeoff (EXECUTED)

Covered above for parity. On the three specific questions the packet asks:

- **Any public semantic object available to TN but cheaply derivable by FD/FC?** Yes, all of them, at depth 1. That is not a defect in r4; §5's byte-identity rule anticipates it and handles it honestly by collapsing to one paid call. r4 has correctly converted r3's fatal problem into a stated property.
- **Any false empty field?** No. §6.1's rule that empty means reference-proven-empty closes it, and Gate 2's "no empty field asserts absence unless reference-proven" enforces it. This is the cleanest fix in the document.
- **Any legitimate typed residual not covered by r4's five declared failure categories?** Yes, one: **a semantic divergence caused by an ambiguity in the algebra rather than by a mechanism limit**. The bitemporal case produces exactly this, and none of the five categories (object omitted, field unavailable, PAGE_FAULT/FRONTIER_LIMIT, overflow, work-budget exhaustion) names it. Add a sixth: `ALGEBRA_UNDERSPECIFIED`, which halts Stage 1 rather than being scored as a mechanism residual.

### Attack D — archive, frontier and hidden work (EXECUTED)

**Instrumented result on r4's own axis (§7.2), depth held at 1:**

| H (dormant) | FD reads | FC reads | TN reads |
|---:|---:|---:|---:|
| 128 | 24 | 12 | 16 |
| 1,024 | 24 | 12 | 16 |
| 10,000 | 24 | 12 | 16 |
| 100,000 | 24 | 12 | 16 |

**On the axis r4 does not have, archive fixed at 1,024 and frontier fixed:**

| D (active-subject depth) | FD reads | FC reads | TN reads | FD/FC |
|---:|---:|---:|---:|---:|
| 1 | 24 | 12 | 16 | 2.0 |
| 4 | 48 | 12 | 16 | 4.0 |
| 16 | 144 | 12 | 16 | 12.0 |
| 64 | 528 | 12 | 16 | 44.0 |
| 256 | 2,064 | 12 | 16 | 172.0 |

**Interpretation.** r4's boundedness gate certifies FD as bounded, and §9.3's tie-break and §11.1's step 5 both prefer FD, so the design is on a path to recommend FD on the strength of a gate that never exercised the growth FD is vulnerable to. A conductor that has been running for a year has not accumulated a million unrelated events; it has accumulated a hundred corrections to the same twenty obligations. That is the depth axis.

**Hiding a journal scan while keeping packet bytes constant.** Two routes I found that §9.2 does not close: load the full journal at artifact open (measured under §9.3's "reconstruction time", not under §9.2's twin-identity gate), and persist a materialized `DecisionPacketV1` so materialization is a no-op read. Both are F10.

**Limitations.** My reducers are minimal and my "primitive objects inspected" counter is a proxy for whatever the real harness would instrument. The *shape* of the result (flat in H, linear in D for a read-time deriver) is a property of the access pattern and does not depend on my constants.

### Attack E — A→B→A and baselines (READ-ONLY)

**The leak channels I found.** Not the ones r4 blocks. §11.4 correctly forbids transcript, scratch, hidden reasoning and provider conversation chains, and `TaskPacketV1` is genuinely minimal. But `WorkerHandoffV1` carries `proposed_claims[]`, `unresolved_items[]` and `warnings[]` with no type or cap, and those are committed to the journal, and fresh A reconstructs from the committed artifact. So A can receive B's prose. That is a legitimate design choice for a real system and a confound for the claim "selective declarative handoff, not transcript inheritance" (F16).

**The crash window.** Walk the trace the packet asks for: A opens the obligation, B proposes, the process dies **after the provider response is received and before the commit event is appended**. r4 has no rule for this. §12.4 covers accepted-with-no-body, which is the transport-layer twin, and §7.4's trace list stops at "duplicate B proposal → A resumes". The paid call is either lost or replayed, and if replayed, `idempotency_key` protects the *effect* but not the *spend* or the *sampling*. That is F12, and the durable-execution literature has the standard answer: journal the raw response before validation.

**Baseline fairness.** LR gets an exact due-obligation enumerator, which is generous and correct. CO is a floor and correctly labelled. EF's "where it fits" makes it a small-world-only baseline (F15). XT is well-conceived and is the one baseline I would defend hardest: process exhaust is the realistic failure mode and separating it from complete evidence is a real contribution. But EF and XT share the maximum input-token envelope, which is where 90% of the paid tokens go (Attack H).

### Attack F — artifact-causal reconstruction (READ-ONLY)

Five of the six witnesses are unchanged from what I would ask for, and witness 3 (source-directory rename) closes the absolute-path continuity channel that r3 left open. Witness 6 (nonce-only fails sufficiency) closes another.

**What still passes while proving nothing:** a candidate whose artifact contains a materialized `DecisionPacketV1`. Withheld fails, corrupted fails loudly, rename survives, swap swaps, field mutation propagates, nonce-only fails sufficiency. All six pass. Reconstruction is a decode of a cached answer and the boundedness gate is satisfied by construction. §4.1's "every candidate projection is rebuildable from it" is the property that would exclude this, and no gate verifies it. Add witness 7: **rebuild from journal, assert equality with the persisted projection** (F10).

I could not execute these; there is no harness. The smallest honest substitute was constructing the hollow implementation against the §10 text and checking each witness by hand.

### Attack G — bounded inference and decision rule (EXECUTED)

I implemented the predictable-plug-in empirical-Bernstein confidence sequence directly: `mu_hat_t = (1/2 + sum X)/(t+1)`, `sigma_hat_t^2 = (1/4 + sum (X_i - mu_hat_i)^2)/(t+1)`, `lambda_t = min(sqrt(2 log(2/alpha) / (sigma_hat_{t-1}^2 t log(1+t))), c)`, `v_i = 4(X_i - mu_hat_{i-1})^2`, `psi_E(lambda) = (-log(1-lambda) - lambda)/4`, with `delta` in `[-1,1]` mapped to `[0,1]` and the bounds mapped back. R = 4,000 replicates.

**Coverage and decisions:**

| true delta | discordance | n | P(PROMOTE) | P(FAIL) | coverage at look | coverage across all 3 |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.10 | 96 | 0.011 | 0.000 | 1.000 | 0.999 |
| 0 | 0.10 | 192 | 0.575 | 0.000 | 1.000 | 0.999 |
| 0 | 0.10 | 384 | 0.991 | 0.000 | 0.999 | 0.999 |
| 0 | 0.30 | 384 | 0.540 | 0.000 | 0.999 | 0.999 |
| -0.10 | 0.10 | 384 | 0.000 | 0.000 | 1.000 | 1.000 |
| -0.10 | 0.30 | 384 | 0.001 | 0.000 | 0.999 | 0.999 |
| +0.10 | 0.10 | 96 | 0.856 | 0.000 | 1.000 | 1.000 |
| +0.10 | 0.30 | 384 | 1.000 | 0.000 | 0.999 | 0.999 |

**Verdict on the procedure: sound.** Coverage holds at 0.999 across all three looks simultaneously, optional stopping costs nothing, and the rule behaves correctly at the margin. r4's statistical choice is right and I have no better one to offer at this `n`.

**Verdict on the parameters: three unstated quantities decide the outcome.**

1. **Discordance.** Half-width at n=384 runs 0.042 at 2% discordance to 0.127 at 50%. PROMOTE with probability at least 0.80 requires discordance at or below **0.20**. r4 never states the discordance the design is powered for, and discordance is the one quantity nobody can estimate before Stage 2.
2. **Missingness.** Adding worst-case missing pairs: the tolerable discordance falls to 0.17 at 1% missing, 0.13 at 2%, and **0.00 at the 5% ceiling §12.4 itself sets**. The ceiling and the margin are numerically incompatible (F4).
3. **Tuning constants.** `c = 0.25` gives half-width 0.1015; `c = 0.5` gives 0.0973; `c = 0.75` gives 0.1143. The margin is 0.10. An unpinned constant flips the decision (F5).

**Pinned reference the design must freeze:** the WSR reference implementation by name, version and content hash, plus `c`, the `sigma-hat` initialization, and the alpha handling written into the design text. Verification against "published examples" is not enough, because the published examples do not fix `c`.

**Limitation.** My implementation is a faithful reconstruction from the published construction, not the authors' code. It should be diffed against the pinned reference at Gate 5, which is exactly what §12.2 asks for. I did not test deltas below `-0.10`, so I cannot tell you when the FAIL branch becomes reachable (F17).

### Attack H — calls, transport and proportionality (EXECUTED)

`k` = scored handoff decisions per scenario; calls per arm per scenario = `2k + 1`.

| n | k | loss | total calls | BC/OM | diagnostics | wall clock at 3 s |
|---:|---:|---:|---:|---:|---:|---:|
| 96 | 1 | 0% | 864 | 576 | 288 | 0.7 h |
| 192 | 1 | 5% | 1,814 | 1,210 | 605 | 1.4 h |
| 384 | 1 | 0% | 3,456 | 2,304 | 1,152 | 2.9 h |
| 384 | 3 | 5% | 8,467 | 5,645 | 2,822 | 6.7 h |

Token envelope at n=384, k=1:

| cell | input tokens per call | calls | input tokens | $ at 3/M |
|---|---:|---:|---:|---:|
| BC | 3,000 | 1,152 | 3.46M | 10 |
| OM | 1,500 | 1,152 | 1.73M | 5 |
| LR | 8,000 | 288 | 2.30M | 7 |
| **EF** | 120,000 | 288 | **34.56M** | **104** |
| **XT** | 120,000 | 288 | **34.56M** | **104** |
| CO | 800 | 288 | 0.23M | 1 |

Totals: 76.8M input, 1.04M output. **$82 at $1/$5, $246 at $3/$15, $1,230 at $15/$75.** Stage 2 is affordable, and that is a genuine achievement relative to r3.

**EF and XT consume 90% of the input tokens** and are 25% cells that §11.3 says cannot create the primary conclusion. That is the machinery to delete or cap.

**Transport.** r4 §13's freeze list is materially better than r3's: it names cache and session identifiers, transform, fallback and the metadata needed for cell identity, and it makes a mismatch a missing pair rather than another draw. Two things it still does not name, and both are account-level rather than request-level, so a byte-exact wrapper cannot detect them: **sticky routing** (keyed on a hash of the first system message plus the first non-system message, account-level per model per conversation, five-minute inactivity expiry) means BC and OM packets hash to different sticky keys and can land on different endpoints; and **server-side presets** shallow-merge into the request. Pin an explicit session identifier held constant across arms, and assert preset absence. r4 leans toward direct-provider transport, which reduces but does not eliminate this.

**Machinery deletable without weakening the three decisions**: cap EF and XT at a stated token ceiling or drop XT to a 10% cell (removes roughly 45% of paid input tokens); subsample §9.3's 30 repetitions to a stratified subset of seed/scale cells (Stage-1 measurement scales as 4.67M materializations otherwise); and run the frontier axis on one motif family rather than all six unless r4 states otherwise.

---

## 9. WHAT WOULD YOU BUILD?

**Mechanism 1: the depth axis, built the way build systems already do it.** Add `D` as a third scaling axis and gate inspection-identity on it. The prior art to take it from is incremental computation and build systems, which r4 §17 already cites for "dependency registration and clean-rebuild oracles" but does not apply here: the property those systems guarantee is that rebuild cost is proportional to the *changed* frontier, not to the *history depth* of any node, and they achieve it by storing a current-value pointer per node rather than replaying the node's edit history. That is exactly what separates FC from FD in my measurement (12 reads versus 2,064 at `D = 256`). **Label: RECALLED for build systems as a class; the specific mechanism is demonstrated EXECUTED in my own probe.**

**Mechanism 2: write-ahead the provider response before validation.** Temporal records non-deterministic side effects into workflow history so replay reuses the recorded result instead of re-running the operation, and Restate journals each `ctx.run()` before execution so a crashed handler replays the journal and skips completed runs, giving exactly-once without application-level idempotency keys. Applied to r4: B's raw response becomes a journal event the instant it is received, and validation, commit or rejection all read from that recorded event. This closes F12, makes A→B→A deterministically replayable (which §14 Gate 4 already demands as "A→B→A deterministic replay equality"), and guarantees no paid call is ever re-sampled. **Label: SEARCHED (Temporal, Restate and LangGraph durable-execution surfaces opened this session; the formal semantics pointer is Burckhardt et al. as cited in arXiv 2606.17182, which I did **not** open).**

**Mechanism 3: interference-heavy evaluation rather than dormant padding.** MINTEval's stated gap is precisely r4's: across memory systems, "a common assumption is that the goal of memory is to surface the most current and relevant state in response to a query", and evaluation follows, "largely overlooking their ability to recall or aggregate information from earlier states". MINTEval evaluates recall and aggregation "in evolving and interference-heavy contexts". r4's dormant twins are the opposite of interference-heavy. Take the interference construction and use it to build the `D` axis. **Label: SEARCHED (arXiv 2605.18565).**

**Mechanism 4: a sixth declared-residual category.** `ALGEBRA_UNDERSPECIFIED`, which halts Stage 1 rather than being scored as a mechanism residual, so that a spec gap can never be credited or debited to a mechanism. This is my own construction, no prior art claimed. **Label: EXECUTED reasoning against the pinned §5 text.**

---

## 10. WOULD YOU DESIGN IT DIFFERENTLY?

Four changes, all local. I am keeping the causal program intact, which is a change from my position on r3.

**(1) Make the boundedness gate falsifiable.** As written it cannot fail on the axis that carries the primary claim. Three axes, not two: dormant archive `H`, active-subject depth `D`, live frontier `F`. Gate inspection-identity on `H` and `D`; report `F` as a curve. This is the difference between "we proved our indexes work" and "we proved conductor continuity is bounded".

**(2) Reconcile the two mechanism selectors, and say which is the recommendation.** §9.3 and §11.1 currently disagree by construction. My preference: §11.1 selects only the Stage-2 packet carrier and explicitly carries no engineering weight; §9.3's Pareto plus strict-dominance rule is the recommendation. Say that in the text.

**(3) Set `n`, the margin and the missing ceiling from one arithmetic, not three habits.** Right now `n = 384` comes from a doubling ladder, `-0.10` from operator tolerance, `5%` from convention, and `240` from `6 x 40`. My simulation ties them together: at margin `-0.10` and `n = 384`, the design tolerates discordance up to 0.20 and missingness up to about 1 to 2%. Pick two of `{n, margin, discordance budget}` and derive the third, then set the missing ceiling from the margin. Also fix `240 < 384` (F1), which is the arithmetic that makes the rest moot.

**(4) Buy the depth axis with the EF and XT budget.** EF and XT are 90% of paid input tokens for cells that cannot create the primary conclusion. Cap them, and spend the saving on the deterministic axis that actually decides the North Star, which costs compute rather than tokens. This is a straight reallocation from a diagnostic that cannot conclude to a gate that currently cannot fail.

---

## 11. Omission attack

| Required item | Answer |
|---|---|
| **Strong simple comparator still omitted** | **NONE, with evidence.** FD is genuinely the strongest cheap deriver (nine-family parity, EXECUTED), FC is the coarse-invalidation arm that prior art measured as the only nonzero mechanism effect, and F0-style current-only overwrite is correctly absent because FD subsumes it. The comparator space is now complete. What is missing is not an arm, it is an **axis** (F3). |
| **Hidden confound capable of falsely PASSING bounded continuity** | **Dormant-only archive padding** (F3). All three candidates read an identical number of primitive objects at every `H` from 128 to 100,000, so §9.2 certifies boundedness without exercising it. Secondary: archive-linear work relocated into artifact open and decode, which §9.2 does not measure (F10). |
| **Hidden confound capable of falsely favouring a mechanism** | **§11.1's read-side-first lexicographic order** (F9) favours FC and TN by construction, because precomputation is what read-side metrics reward. In the opposite direction, **§7.2's shallow active worlds** favour FD, because depth is where FD's cost lives and depth is held at whatever the motif generator happens to produce. The two biases point in opposite directions and neither is measured. |
| **Persuasive false-positive model-usability story** | Discordance between BC and OM turns out to be low (say 0.05) because both packets are competent and the model answers identically on almost every scenario. The confidence sequence tightens fast, the lower bound clears `-0.10` at n=192, and the council reads PROMOTE as "the model can use the bounded packet". What actually happened is that the screen had almost no variance to work with because BC and OM are near-substitutes on this workload, and the same PROMOTE would have been returned by a packet with far less content. Guard: preregister the discordance rate that would make the result informative, and report `P(BC=1, OM=0)` and `P(BC=0, OM=1)` separately, not just their difference. |
| **Persuasive false-kill story** | `contract_success` is a conjunction over `k` scored handoff decisions and `k` turns out to be large. At `k = 12` and per-decision reliability 0.95, scenario success is 0.54; at `k = 24` it is 0.29. OM falls below the 0.80 floor, Stage 2 returns `MODEL_OR_INTERFACE_CEILING`, and the program concludes the model cannot use validated state when the actual finding is that a 24-way conjunction is an unreasonable success criterion. Full budget spent, nothing learned (F6). |
| **Footgun not caught by a gate** | **The crash window between provider response receipt and commit-event append** (F12). §12.4 catches the transport-layer twin (accepted, no body). Gate 4 tests duplicate, stale, rejected and committed proposals. Nothing tests death *after* a valid response arrives and *before* the journal records it, and that is the one window where a paid call can be silently lost or re-sampled. |
| **One no-paid test without which I refuse Stage 2** | **The depth sweep.** Build FD, FC and TN, hold archive size and active frontier fixed, sweep active-subject correction depth over 1/4/16/64/256, and report primitive objects inspected. My minimal version took under an hour and returned 24 → 2,064 for FD against a flat 12 for FC. Until that number exists, a Stage-1 pass on §9.2 is not evidence that bounded continuity holds, and Stage 2 would be testing model usability of a packet whose boundedness was never established. |
| **One mechanism to borrow directly** | **Record-and-replay of non-deterministic step results into the journal**, from the durable-execution lineage (Temporal's event history reusing recorded results rather than re-running the operation; Restate journaling each step before execution to get exactly-once without application-level idempotency keys). It closes F12, satisfies Gate 4's own A→B→A replay-equality requirement, and guarantees no paid call is ever re-sampled on recovery. SEARCHED. |
| **Machinery to delete** | **XT as a full-envelope 25% cell.** With EF it consumes 90% of Stage-2 input tokens for a diagnostic that §11.3 forbids from creating the primary conclusion. Cap both at a stated token ceiling or run XT at 10%. Second candidate: §9.3's flat 30 repetitions across every seed and scale cell, which implies 4.67M measured materializations; a stratified subsample gives the same p95 estimate. Neither deletion touches any of the three decisions. |
| **Exact boundary between MBCX-01 and the next coordination experiment** | MBCX-01 owns everything with **one canonical writer, one logical conductor identity, and one frozen model**: the event algebra, obligation lifecycle, bounded materialization, artifact-causal reconstruction, and a *sequential* A→B→A where B's proposal is adjudicated by the deterministic writer before A resumes. The moment two proposals can be in flight against the same obligation, or two workers hold different views of the same scope, or B is a different model, you are in the next experiment. r4 §16 draws this line correctly. One sentence I would add to make it operational: **MBCX-01's commit boundary must be single-threaded by construction, not by convention**, so that "concurrent" cannot leak in as an implementation accident during Stage 1. |

---

## 12. Sweep log

| Lane | Exact query | Opened at origin | Decisive section | Level | Effect on ruling | Stop reason |
|---|---|---|---|---|---|---|
| 1. Module and stage diagnosis | `Text2Mem MemEval agent memory system evaluation phase-aware decomposition benchmark 2026` | `arxiv.org/pdf/2605.18565` (MINTEval), `arxiv.org/html/2605.12493v1` (LongMemEval-V2), `arxiv.org/pdf/2509.11145` (Text2Mem), `arxiv.org/pdf/2605.28732` (MemTrace) | MINTEval §5: memory work assumes the goal is surfacing the most current state and evaluation follows, overlooking recall and aggregation from earlier states; MINTEval targets evolving, interference-heavy contexts. LongMemEval-V2 related-work: MemoryArena measures memory indirectly through task success; AgentLongBench and EMemBench use synthetic histories. Text2Mem: typed operation objects, deterministic parsing, planning separated from execution. | SEARCHED, primary | Decisive for F3. Named prior art states the exact gap r4's dormant-padding axis reproduces. Also confirms r4 §17's Text2Mem citation is accurate. | Four primaries opened, consistent picture, the MINTEval framing settled the depth question. |
| 2. Mechanism and render controls | (carried from earlier this session) `StateFuse arXiv 2607.05844`; `"Presentation, Not Mechanism" arXiv 2607.16019` | `arxiv.org/pdf/2607.05844`, `arxiv.org/abs/2607.16019`, `arxiv.org/html/2607.16019v1`, `arxiv.org/pdf/2607.16019` | StateFuse: conflict-preserving memory ties flat and raw-log baselines on answer accuracy under matched resolvers; value is in surfacing and abstention. Presentation Not Mechanism Table 2: fine-grained typed residual indistinguishable from zero, coarse deprecation +0.087 [+0.046, +0.130]. | SEARCHED, primary | Confirms FC was the right arm to add and that r4's retirement of `TN - FM` matches the empirical record. **Contaminated: I brought these to the r3 round, so this lane is convergence, not confirmation.** | Already opened this session; no new query would change the ruling. |
| 3 and 4. Obligations, durable identity, selective handoff | `durable execution workflows virtual actors exactly-once obligation deterministic replay agent handoff context transfer instead of transcript 2026` | `temporal.io/blog/of-course-you-can-build-dynamic-ai-agents-with-temporal`, `zylos.ai/research/2026-04-24-durable-execution-agent-runtimes/`, `zylos.ai/research/2026-04-24-replayable-agent-runtimes-event-sourced-execution/`, `spheron.network` (Restate/Temporal/Inngest comparison), `arxiv.org/pdf/2606.17182` (concurrency-anomaly paper's §7.9 durable-execution section) | Temporal records non-deterministic side effects into workflow history so replay reuses the recorded result; Restate journals each `ctx.run()` before execution, replaying and skipping completed runs for exactly-once without application idempotency keys; durable-execution engines guarantee exactly-once activity completion and saga compensation through deterministic replay, semantics formalized by Burckhardt et al. | SEARCHED; vendor documentation and one secondary research surface, plus a **pointer** to the Burckhardt formalization I did not open | Drives F12 and the borrow in §9. Also validates r4 §17's "durable logical identity and prospective obligations from virtual actors and durable workflows" as an accurate citation. | Mechanism found and specific enough to name a repair. I did **not** open the Burckhardt formalization, so the formal-semantics claim is a pointer, not evidence. |
| 5. Boundedness and hidden work | Folded into lanes 1 and 3 | as above | MINTEval's interference framing; durable-execution replay cost discussion | SEARCHED, indirect | My boundedness finding is EXECUTED arithmetic and does not rest on prior art. | **DID-NOT** run a dedicated query; the finding is self-supporting and I judged the marginal value low. Flagging so the next seat can close it. |
| 6. Bounded paired inference | (carried) `Waudby-Smith Ramdas estimating means of bounded random variables betting` | `academic.oup.com/jrsssb/article/86/1/1/7043257`, RSS discussion-meeting PDF, `arxiv.org/abs/2010.09686` | Closed-form empirical-Bernstein CIs and CSs plus betting CIs; variance-adaptive; finite-sample validity on bounded support | SEARCHED, primary | Confirms r4 §12.2's choice is the right family and supplies the construction I implemented. **Contaminated: I recommended this in the r3 round.** | Controlling primary already open. I did **not** search exact paired-binary alternatives or e-value stopping, so "nothing better exists at n=384" is not a claim I make. |
| 7. Provider and runner footguns | (carried) `OpenRouter provider routing`; `OpenRouter transforms middle-out prompt caching response cache docs` | `openrouter.ai/docs/guides/routing/provider-selection`, `openrouter.ai/docs/guides/best-practices/prompt-caching`, `openrouter.ai/blog/announcements/response-caching/` | Sticky routing at account level per model per conversation, keyed by hashing the first system and first non-system message, five-minute inactivity expiry; server-side presets shallow-merged; `models` array as a second fallback channel; response cache scoped to API key and bypassing the provider | SEARCHED, primary vendor docs | r4 §13 closes most of what r3 left open. Sticky routing and presets remain unnamed and are account-level, so a byte-exact wrapper cannot detect them. | Vendor origins opened and current; r4 leans direct-provider, which reduces the exposure. |

**Global-surface requirement**: satisfied by named non-US, non-UK institutional primaries opened this session, including StateFuse (University of Hong Kong) from the carried lane and the Chinese-language filesystem-memory surface from the earlier round, paired with the named-institution English pass above (MINTEval, LongMemEval-V2, Text2Mem, PM-Bench). I did **not** open a national repository surface this round, so a negative in any lane above is field-level only.

---

## 13. Residual risks and explicit non-claims

**Residual risks.**

1. **My non-independence is the largest one.** Sections 6, 9 and 10 evaluate changes I proposed. Convergence between my r3 recommendations and r4's content is not evidence that either is correct.
2. My depth-axis result depends on FD being implemented as a read-time fold over a subject's event list. A cleverer FD (a per-subject current pointer maintained lazily on read, memoized) would be flat in depth, at which point it is FC by another name. That is itself an interesting result and worth stating in r5 of the design, but it means my numbers show the *shape* of the risk, not a proof that FD must be linear.
3. My confidence-sequence implementation is a faithful reconstruction, not the pinned reference. All of Attack G's conclusions are conditional on it matching whatever gets pinned at Gate 5. Diff them.
4. All of §13 transport and §10 reconstruction remain READ-ONLY. I could mock nothing, and a READ-ONLY verdict on an executable artifact cannot be a deciding GO. My verdict rests on F1, F2 and F3, all EXECUTED.
5. I did not open the seven lineage artifacts, so any claim about whether r4 faithfully transfers its own research inputs is one I have not made and cannot make. If the round needs that adjudicated, it needs a seat that opens them.
6. The `contract_success` conjunction analysis assumes independence across scored decisions within a scenario, which is false in a correlated way I cannot sign. Positive correlation makes the arithmetic less bad, not good.

**Explicit non-claims.**

- I do **not** claim r4's causal program is wrong. I claim three specifications inside it are missing and one gate cannot fail.
- I do **not** claim FD is a bad mechanism. I claim the design as written cannot tell you whether it is.
- I do **not** claim Stage 2 will fail. I claim its outcome is currently determined by three quantities nobody has written down.
- I do **not** claim any licensing, security, deployment, concurrency or cross-model position; all were excluded in §5 and none is smuggled back.
- I did **not** open the Burckhardt durable-functions formalization, exact paired-binary noninferiority literature, blackboard or shared-selective-memory literature, or a national repository surface, and no ruling above rests on them.

---

## 14. Seat capability and seal report

| Dimension | Status |
|---|---|
| Local file read | Full via the Moonwalker bridge, byte-verified against the git object before use. |
| Local shell | One call, sentinel-verified: unique token first in stdout, echoed `command` field compared against what I sent. No crossing. |
| Code execution | Isolated Linux container (Python 3, numpy 2.4.4, scipy 1.17.1), no network egress. Five scripts written and run. |
| Web | Native `web_search` live; two searches this round plus seven carried origins from earlier in the session. No `web_fetch` needed. **No Moonwalker crawler escalation performed.** |
| Tokenizer | **LIMITED.** No tokenizer frozen in r4 (§13 defers it). Attack H token counts are disclosed estimates from stated packet caps, not certification. |
| Statistical | Full. R = 1,500 to 4,000 per cell; simulation error roughly ±0.008 at a 0.80 target, an order of magnitude below every gap reported. |
| Paid inference | **NONE.** No model call, no canary, no API request. |
| Side effects | **NONE on your machine.** No file created, modified, moved or deleted anywhere under `C:\`. No git object, branch, stash or index change. The single shell call was read-only (`rev-parse`, `cat-file`, `status --porcelain`) with in-memory hashing through a piped stream so no temporary file was written. All five scripts live only in the container sandbox. No browser session, no tab, no seat contacted. |
| Verdict delivery | In-thread, as this reply. Nothing written to a file, artifact, canvas or vault. |

**Sealed-independence confirmation, with one disclosed exception.** I read exactly three files, each by exact explicit path: the r5 packet, the seat role card at `<vault>`, and the pinned design blob `3f62703`. I ran no `moonwalker_search_files`, no `moonwalker_grep`, no `moonwalker_ls`, no `moonwalker_memory_search`, no `dir` and no `Get-ChildItem`. I opened no prior council report, synthesis, exec log, receipt, watcher, restart manifest or browser output, and no file whose name contains `VERDICT`, `COUNCIL-ROUND`, `EXEC-`, `RECEIPT` or `RESTART-MANIFEST`. No prohibited snippet reached my context through any file route.

**The exception, disclosed as a protocol deviation rather than concealed:** this seat carries its own prior-round verdict on r3 in working context, because it is the same conversation. That is a prior council report by any reasonable reading of §0, even though it is mine and was never written to disk. I could not unsee it, and pretending otherwise would have been the worse failure. Treat this as a **second-round seat**, not a fresh one, and get a genuinely sealed seat on the FC arm and the statistics before you close the round.
