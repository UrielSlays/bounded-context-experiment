# MBCX-01 r5 BUNDLE COUNCIL VERDICT — SEXTANT-OPUS5-CLAUDEAIMCP-MBCX01-R6-20260812T

> **NON-INDEPENDENCE DISCLOSURE, PER PACKET §0.** This conversation retains two prior MBCX-01 rounds: I adjudicated r3 (NO-GO) and r4 (GO-WITH-FIXES) earlier today. **This is not an independent seat.** I am continuing as a second-round reviewer and I do not claim the seal holds against my own prior rounds.
>
> r5 adopts, in substance, a large fraction of what I recommended on r4: the disjoint 240/384 cohorts, the named bitemporal clock, the active-depth `D` axis, the 2% missing ceiling, the pinned `confseq` code and parameters, `k=3`, scope-immutable delegation, the journal-rebuild witness, `(scope_id, subject_id)` index keys, the write-ahead response event, gold cardinality up to four, the deletion of LR/EF/XT/CO from the primary run, the separation of carrier selection from engineering authority, and the 10% performance subset with a storage ceiling. **Every one of those is a non-independent recommendation and their presence in r5 is convergence, not confirmation.** Sections 6, 9, 10 and the parts of 7 that repeat r4 findings should be discounted accordingly.
>
> What is genuinely new attack surface, and therefore not contaminated: the two normative JSON contracts, which I had never seen. Every P0 below comes from those files.

---

## 1. Top-level verdict

**GO-WITH-FIXES(three P0 numeric repairs in the normative contracts before Stage 0: the §9.2 normalized-range gate is unit-incoherent and both falsely falsifies and vacuously passes depending on which counter it is applied to; the A0 target rule requires the model to guess an unstated tie-break on multi-gold cuts; and the OM branch thresholds put the design's own nominated floor inside a dead band where no branch can fire).**

r5 is a substantial and largely successful executable preregistration. The bundle-at-one-commit discipline works, all three pins verify byte-exact, the state/action contract is a real contract rather than prose, and the inference contract pins upstream code, parameters, transforms, alpha allocation and reference vectors, which is more rigor than most published protocols carry. The three-question decomposition survives intact and the interpretation boundaries in §16 are honest.

The blockers are arithmetic, not architectural:

- **P0-1.** §9.2 applies one dimensionless threshold (`0.0001`) to counters with incommensurable units. On the `D` axis the permitted integer range is **zero units on every counter**: one extra record read gives `normalized_range = 0.00392`, which is 39x over. On the `H` axis a byte counter fails at one extra 4 KiB page by **410x**, while the identical physical event passes on a page counter at `1.0e-5`. The prose claim that the gate "admits a small bounded index-height change" is false for any counter denominated in bytes. Meanwhile the same gate is vacuous for slow growth: 1 charged unit per 11,097 archive events passes, which extrapolates to 901 units at a 10M-event archive.
- **P0-2.** `action_universe.gold_cardinality` permits one through four gold ACT IDs, `paid_handoff_gold.A0_target` is the UTF8-bytewise smallest of them, and §6.2 forbids any packet content that points at the target. On a multi-gold cut the model must guess a lexicographic convention it was never told. Under a uniform 1..4 gold mix the blind A0 factor is **0.521**, and `contract_success` is a conjunction that includes A0.
- **P0-3.** Executed against the contract's own reference vectors and my reconstruction: at `n=384`, `PROMOTE` requires observed OM contract success of roughly **0.87 or better**, and `MODEL_OR_INTERFACE_CEILING` requires roughly **0.70 or worse**. Between them, approximately **[0.71, 0.86]**, no branch fires regardless of delta. The design's nominated floor of `0.80` sits in the middle of that dead band. Translated through `k=3`, the study is informative only if per-decision reliability is above ~0.955 or below ~0.892.

P0-2 feeds P0-3: the A0 tie-break alone can move OM into the dead band, at which point the entire 2,304-call run returns `INCONCLUSIVE_OR_UNDERFUNDED` for a reason that has nothing to do with memory.

---

## 2. Seat identity

| Field | Value |
|---|---|
| Model as exposed | Claude Opus 5 (`claude-opus-5`) |
| Harness | claude.ai chat surface, Moonwalker MCP bridge, isolated Linux container (Python 3, numpy 2.4.4, scipy 1.17.1, no egress) |
| Native web | `web_search` and `web_fetch` live |
| Paid inference | **NONE** |
| Independence | **Compromised across r3 and r4.** See the disclosure above. |
| Report title | MBCX-01 r5 BUNDLE COUNCIL VERDICT — SEXTANT-OPUS5-CLAUDEAIMCP-MBCX01-R6-20260812T |

---

## 3. Pin and byte verification

One sentinel-guarded shell call (`MBCX01-R6-SEAL-V7N2` echoed in stdout, `command` field compared against what I sent). Commit `08421f49c39c8c79c14f1ad9ba1789a2a96bcf4a` resolves to type `commit`. Repository HEAD is `0f61d8aa3342e5b94376d850a1bfa703c235849f`.

| Artifact | Blob at pin | Expected blob | Bytes | Lines (LF/CR) | SHA-384 | HEAD blob | Working copy |
|---|---|---|---:|---|---|---|---|
| `MBCX-01-EXPERIMENT-DESIGN-r5.md` | `d37dad72…` | `d37dad72…` MATCH | 29,274 MATCH | 484 / 0 MATCH | `59AB9506…49EFFF1` MATCH | same blob | byte-identical, `status` clean |
| `MBCX-01-STATE-ACTION-CONTRACT-v1.json` | `27abf1a8…` | `27abf1a8…` MATCH | 14,451 MATCH | 214 / 0 MATCH | `74695406…79D849B7` MATCH | same blob | byte-identical, `status` clean |
| `MBCX-01-INFERENCE-CONTRACT-v1.json` | `906a3643…` | `906a3643…` MATCH | 6,619 MATCH | 112 / 0 MATCH | `82FC6F0A…5D1D6EEF` MATCH | same blob | byte-identical, `status` clean |

**Working-copy difference: NONE on all three.** I adjudicated the three pinned blobs, read through working copies after proving byte identity. Also opened by exact path: the role card at `<vault>`. **None of the seven packet-§1 lineage artifacts was opened**; the bundle is self-contained for every finding I make, and reading them would have added exposure without adding evidence.

**Upstream pin, partially verifiable.** The inference contract pins `github.com/gostevehoward/confseq` at commit `5ffe733c…`, with blob and SHA-384 for `src/confseq/predmix.py` and `src/confseq/betting_strategies.py`. I reached the repository origin and confirmed it exists, that `confseq.predmix` is a real module, and that `lambda_predmix_eb` is imported from `confseq.predmix` by `betting.py`. I **could not** reach either pinned file at the pinned commit (`web_fetch` refuses constructed URLs and the raw path never surfaced in a search result), so the two upstream pins are **UNVERIFIED by this seat**. See F9 and F13.

---

## 4. Evidence and probes

**EXECUTED** (container, no paid inference, no writes to your machine)

| Probe | Produces |
|---|---|
| `cs.py` | Independent reconstruction of `predmix_empbern_twosided_cs` with the contract's exact parameters; reference-vector comparison; PROMOTE feasibility per look; discordance sweep; OM dead-band mapping; missingness-to-transport-reliability translation. |
| `gate.py` | §9.2 normalized-range arithmetic at both axis boundaries; counter-splitting aggregation attack; unit-mismatch table across records, pages and bytes; exact Stage-2 DAG reproduction and a hypothetical-price cost envelope. |
| `algebra.py` | Literal implementation of the `correct_fact` guard against the retroactive-correction fixture; A0 tie-break arithmetic; `record_handoff_response` node-coverage analysis; writer-path nondeterminism; F-axis versus action-cardinality check. |

**READ-ONLY**: §10 producer isolation and the seven reconstruction witnesses (no harness exists; attacked by constructing implementations that pass while proving less than claimed). §13 transport (no endpoint frozen). §6.2 presentation matching (attacked by schema analysis).

**SEARCHED this round**: `gostevehoward/confseq` repository origin and `src/confseq/betting.py` at master (opened in full); event-sourcing snapshot-plus-tail practice (arc42 quality model, AWS Prescriptive Guidance, two practitioner deep-dives).

**SEARCHED earlier in this session and carried forward, disclosed as prior-round work**: MINTEval (arXiv 2605.18565); LongMemEval-V2 (arXiv 2605.12493); Text2Mem (arXiv 2509.11145); MemTrace (arXiv 2605.28732); StateFuse (arXiv 2607.05844, University of Hong Kong); Presentation Not Mechanism (arXiv 2607.16019); PM-Bench (arXiv 2607.12385); Mem2ActBench (arXiv 2601.19935); TriggerBench (arXiv 2606.23459); Waudby-Smith and Ramdas JRSS-B 86(1) 1-27 (2024); Temporal/Restate/LangGraph durable-execution surfaces; OpenRouter provider-selection and prompt-caching docs.

**UNSEARCHED, with reasons**: the two pinned upstream `confseq` files (**COULD-NOT**, see §3, and this is the single most consequential gap in my evidence). The seven lineage artifacts (**NOT-LOAD-BEARING**, deliberate). Exact paired-binary noninferiority alternatives and e-value optional-stopping literature (**DID-NOT**; my finding is that r5's chosen procedure has a threshold problem, not a family problem, so an alternative family would not change the ruling). Blackboard and shared-selective-memory literature as a named field (**DID-NOT**). A national repository surface this round (**DID-NOT**; the non-US institutional pass is carried, so **every negative in this report is field-level, not country-level**).

---

## 5. Applicability ruling

Excluded per packet §2, with no direct path shown to any load-bearing failure class: licensing, IP, commercialization; hostile actors and production security; FIPS and CNSA; deployment, fleet and PR ceremony; cross-model generalization; concurrent writers; procedural, personality and affect memory.

Retained because they do have that path: the `record_handoff_response` node coverage (alters retained outcomes and the missing-pair budget); the writer's invalid-proposal path (alters A1's reconstructed input and therefore the scored outcome); the per-call transport reliability implied by the 7-pair ceiling (alters whether any branch can be reached); the two upstream pin styles (alter whether the inference layer can be validated at all).

---

## 6. Claim scoreboard C1 to C12

| Claim | Ruling | Basis |
|---|---|---|
| **C1** the North Star is preserved | **HOLDS** | Traced all four Attack-A worlds. §1, §9.2's final paragraph and §16 make a TN loss non-fatal and make falsification conditional on no candidate passing `H` and `D`. The `D` axis is what makes the falsification branch reachable at all, and it is now present. |
| **C2** the state/action contract is total and executable | **FALSE** | EXECUTED: the `correct_fact` guard's "no sibling branch" clause plus the "one linear supersession chain" rule make a retroactive correction structurally impossible whenever any later correction exists, while `retroactivity` and a mandatory enumerator check both assert it is legal. Additionally the writer's path for an invalid proposal is underdetermined (F6), the normative payload names `worker_handoff_v1` while the design defines `WorkerHandoffV2` (F11), and F=16 breaches the 7-to-15 obligation cap (F12). |
| **C3** hard obligation gates are appropriate and executable | **HOLDS** | Zero due-critical loss, wrong-scope gold and admission, stale resurrection at any canonical cut, duplicate committed effect, reconstruction drift, taint canaries and unregistered reads are all deterministic, all defined against named contract predicates, and all separated from paid model error. The removal of r4's undefined "propagation barrier" is a clean fix. |
| **C4** FD/FC/TN are the complete mechanism comparison | **HOLDS** | Executed nine trace families in the r4 round with the same three candidates and found no public semantic object reachable only by TN. FC's segmented snapshot plus bounded tail is correctly classified as a storage strategy: snapshot-plus-tail is the standard event-sourcing rehydration pattern, not a distinct semantics. I could not construct a semantically distinct fourth comparator. |
| **C5** parity and dedup prevent a fake mechanism effect | **HOLDS** | One normative packet, byte-identical packets share one call and one stochastic result, empty arrays are reference-proven, residuals are a closed preregistered list, and `ALGEBRA_UNDERSPECIFIED` is explicitly not a mechanism result. This is the strongest section of the bundle. |
| **C6** `H`, `D`, `F` and physical counters make boundedness falsifiable | **FALSE** | EXECUTED: the gate permits 9 integer units on `H` and **0** on `D`. One extra record on `D` is 39x over threshold; one 4 KiB page counted in bytes is 410x over on `H` and 16,000x over on `D`. The same physical event passes or fails depending only on the unit of the counter. Separately the gate is per-counter with no total, so 13 counter families conceal up to 117 units. |
| **C7** the serial cold handoff isolates selective continuity | **UNDERDETERMINED** | The structure is right and `WorkerHandoffV2` with zero free-text fields and enumerated codes closes the r4 leak channel properly. But `record_handoff_response` guards on `handoff status == OPEN`, which covers only the B node: A0 precedes any handoff and A1 follows a CLOSED one, so 1,536 of 2,304 accepted calls have no journalable write-ahead event. |
| **C8** the paid action and scoring unit is exact | **FALSE** | EXECUTED: `k=3` removes r4's ambiguity, but `A0_target` is the lexicographically smallest of up to four equally-gold ACT IDs and no packet may point at it. Blind A0 factor 0.521 under a uniform 1..4 mix. The cut selector requires only "at least one" mounted critical `O_due`, so multi-gold cuts are eligible. |
| **C9** mechanism recommendation and carrier selection are fair | **HOLDS** | Worst-cell type-7 p95 rather than a pooled quantile, frozen indifference bands with a defined measurement resolution, Pareto reporting with `NO_UNIQUE_ENGINEERING_WINNER`, and a carrier rule explicitly stripped of engineering authority. The r4 read-side-first contradiction is properly repaired. |
| **C10** the inference contract is coherent and executable | **UNDERDETERMINED** | EXECUTED: my independent reconstruction with the contract's stated parameters returns `-0.182584443111` at `n=96` against the contract's `-0.184596392909`, a 1.10% relative difference against a stated tolerance of `1e-12`. The vectors imply an effective `log(1/alpha)` of `4.430313`, hence `alpha_eff = 0.011911`, which is neither `0.025` nor `0.0125`. Also: no stopping rule is stated, the `n=96` look cannot produce PROMOTE, and the OM thresholds create a dead band around the design's own floor. |
| **C11** producer isolation, reconstruction, transport and cost cannot choose the answer | **UNDERDETERMINED** | The seven witnesses including journal-rebuild equality close the r3 and r4 gaps. What remains: the write-ahead gap (F5), an unstated per-call transport reliability requirement of roughly 0.1% implied by the 7-pair ceiling over six call nodes (F7), and two pin styles (`git_blob` versus `bytes_via_utf8_response_body` plus SHA-384) that are not proven to cover the same bytes (F13). |
| **C12** r5 is the smallest decisive instrument | **HOLDS** | Diagnostics deferred, performance repetitions cut to a 10% stratified subset with a 20 GiB ceiling, exactness run once, 2,304 calls with no diagnostic inflation. Every retained stage can change a primary result. The only removable item is analytic, not operational (F4). |

---

## 7. Finding table

| ID | Sev | Exact location | False-result mechanism | Smallest repair | Evidence |
|---|---|---|---|---|---|
| **F1** | **P0** | design §9.2, both axes | False falsification of bounded continuity, and simultaneously a false pass. One dimensionless threshold over incommensurable counters. `D` permits **0** integer units on every counter: one extra record read is `1/255 = 0.00392`, 39x over. A byte counter fails on `H` at one 4 KiB page (`4096/99872 = 0.0410`, 410x over) and by 16,000x on `D`. The prose "admits a small bounded index-height change" is false wherever bytes are charged. In the other direction, growth of 1 unit per 11,097 archive events passes as bounded, which is 901 units at a 10M-event archive. | Set a per-unit-class threshold: an absolute integer allowance for count-class counters (records, pages, probes, ops) and a separate relative allowance for byte-class counters, each stated in the contract. Or normalize by `log2(H)` rather than by `H` for counters whose intended growth is index height. State the allowance per counter, not one number for all. | EXECUTED |
| **F2** | **P0** | design §9.2, "for every deterministic charged counter" | Hidden work through aggregation. The gate is applied per counter with no constraint on the total. §8.1 enumerates roughly 13 charged counter families, so a candidate may rise 9 units on each and conceal 117 units of archive-linear work while every individual counter passes. A single counter rising 10 fails; the same work split 5 and 5 passes. | Add a total-charge gate: the sum over all counters of the same unit class must also satisfy the threshold, and declare the counter set closed so a new counter cannot be introduced to create headroom. | EXECUTED |
| **F3** | **P0** | state/action `action_universe.gold_cardinality` + `paid_handoff_gold.A0_target` + design §6.2 | Depressed `contract_success` for a reason unrelated to continuity, which pushes OM into the F4 dead band and produces a false model-ceiling or false inconclusive. Gold may hold four equally-due critical ACT IDs; A0 must emit the lexicographically smallest; no packet field, label or instruction may indicate which. Blind A0 factor 0.521 under a uniform 1..4 mix. | Either restrict `cut_selection` to cuts with **exactly one** mounted critical `O_due` obligation, or make A0's task "emit the complete gold set" so cardinality is not a guessing game, or state the tie-break convention in the identical system instruction both conditions receive (a convention is not an answer hint). | EXECUTED |
| **F4** | **P0** | inference `decision_thresholds` + `oracle_floor` | Cost discovered after authorization. At `n=384`, `om_lower >= 0.80` needs observed OM around 0.87; `om_upper < 0.80` needs observed OM around 0.70. Between roughly 0.71 and 0.86 no branch can fire. The contract's own `om_eighty_percent_pattern` vector at 384 is `[0.7177, 0.8788]`, which is neither branch. The nominated floor 0.80 sits inside the dead band. Through `k=3`, the study is informative only if per-decision reliability exceeds ~0.955 or falls below ~0.892. | State the dead band in the contract and pick the floor from it, not from a round number. If the intent is "OM must be usable", require `om_point >= 0.80` with a separate precision requirement, or lower the floor to ~0.70 so `CEILING` and `PROMOTE` tile the space. Publish the implied per-decision reliability requirement alongside. | EXECUTED |
| **F5** | **P1** | design §6.4 vs state/action `record_handoff_response.guards` | Lost paid work and inflated missingness. §6.4 says any accepted response is journaled before parsing; the only recording event guards on `handoff status == OPEN`, which is true only for B. A0 precedes handoff creation; A1 follows a CLOSED handoff. 1,536 of 2,304 accepted calls are unprotected, and §6.4's own fallback converts each such crash into a missing pair against a 7-pair ceiling. | Add `record_call_response` keyed on `(scenario_id, condition, node)` with no handoff-status guard, or open a nominal handoff per node. One event type. | EXECUTED |
| **F6** | **P1** | state/action `illegal_transition_result` vs `reject_handoff_result` | Implementer choice that changes a scored outcome. An invalid B proposal has two legal writer paths: attempt `propose_handoff_result`, fail its guard, and per the contract append nothing to the canonical journal (handoff stuck at `RESPONSE_RECORDED`); or emit `reject_handoff_result`, which is legal from `RESPONSE_RECORDED` and does append. A1 reconstructs from the canonical journal, so the two paths give A1 different input and different `contract_success`. | State the writer algorithm: on any proposal-guard failure the writer MUST emit `reject_handoff_result` with the matching `rejection_code` and MUST NOT attempt `propose_handoff_result`. One sentence. | EXECUTED |
| **F7** | **P1** | inference `missingness` + design §11 | Unstated operational requirement that can end the run. A pair is missing if any of six call nodes fails. At a per-call accepted/no-body or route-identity failure rate of 0.2% the probability of `TRANSPORT_INCONCLUSIVE` is 0.09; at 0.3% it is 0.38; at 0.5% it is 0.88. The design nowhere states that it requires better than roughly 0.1% per call. | Publish the implied per-call reliability requirement in §13 and in the preauthorization manifest, and require a pre-paid transport soak that measures it before the confirmatory run. | EXECUTED |
| **F8** | **P1** | inference `reference_vectors` | The acceptance criterion for the whole inference layer may itself be wrong. My independent reconstruction with the contract's stated parameters gives `-0.182584443111` at `n=96` against the published `-0.184596392909`. The published vectors are exactly proportional to `1/n`, which forces constant lambda at truncation and hence `delta_lower = -4·log(1/alpha_eff)/n`, implying `alpha_eff = 0.011911`. That is neither `0.025` nor `0.0125`. If the vectors are wrong, Gate 5 will reject a correct implementation at a `1e-12` tolerance. | Regenerate the vectors from the pinned bytes with the pinned call, publish the generating script and its hash alongside them, and record the interpreter and NumPy versions. Until then Gate 5 must treat a vector mismatch as a vector defect until proven otherwise. **I could not resolve which side is wrong; see the seal report.** | EXECUTED, unresolved |
| **F9** | **P1** | inference `reference.betting_strategies_py` | Unverifiable dependency pin. At the origin I reached, `lambda_predmix_eb` is imported from `confseq.predmix`, and `betting.py` at master imports it from there. The contract pins `src/confseq/betting_strategies.py` as a second load-bearing file. Either that module exists only at the pinned commit or the dependency pin is wrong. | Gate 5 must check out the pinned commit and list `src/confseq/`, then record the actual import graph of `predmix_empbern_twosided_cs` in the contract. | READ-ONLY / COULD-NOT |
| **F10** | **P1** | inference `looks` + design §12 | Unstated stopping rule and a dead look. Nothing in either normative document says whether execution stops when a branch fires at a look. If it does not, the looks are analytic only and the cost is always 2,304 calls. If it does, the cost profile and the manifest change. Separately, from the contract's own `delta_all_zero` vector, the best possible `delta_lower` at `n=96` is `-0.1846`, so **the `n=96` look can never produce PROMOTE**; and at `n=192` PROMOTE requires near-perfect concordance (P = 0.75 at 2% discordance, 0.49 at 5% in my reconstruction). | State the stopping rule. State that look 1 is futility-only for the PROMOTE branch, and publish the per-look PROMOTE feasibility alongside the operating-characteristic grid so the owner sees that this is effectively a single-look `n=384` design with two early-failure checks. | EXECUTED |
| **F11** | **P1** | state/action `propose_handoff_result.payload_required` vs design §6.1/6.3 | Normative naming conflict, and the contract governs. The payload names `worker_handoff_v1`; the design defines `WorkerHandoffV2`, `TaskPacketV2` and `DecisionPacketV2`, none of which the contract references. The caps block is `worker_handoff_caps` with no version. An implementer following the governing document builds a schema the bundle never defines. | Rename to `worker_handoff_v2` in the contract and add `packet_schemas` naming `DecisionPacketV2` and `TaskPacketV2` so both documents reference the same identifiers. | EXECUTED |
| **F12** | **P2** | state/action `deterministic_core_constraint` and `frontier_axis_rule` vs design §7.5 | Contradiction at `F=16`. Scored scenarios are capped at 7 to 15 obligation IDs; only `F=64` and `F=256` are exempted as resource cells; but `F=16` implies at least 16 live obligations and is used as a scored and gated cell in §7.4 and in the §9.2 stress corner. | Exempt `F=16` as well, or raise the cap to 17 and restate the action envelope as 8 to 18 IDs. | EXECUTED |
| **F13** | **P2** | inference `reference.*.bytes_via_utf8_response_body` | Two pins that are not proven to cover the same bytes. A git blob is identified by SHA-1 over `blob <len>\0` plus content; the contract's byte count and SHA-384 are explicitly over an HTTP response body. If the served body ever differs from the blob (line endings, encoding, transfer transform), the two pins name different artifacts and a Gate-5 verifier can satisfy one and not the other. | Record the git blob size alongside the blob hash and compute the SHA-384 over the blob bytes, not the response body. | READ-ONLY |
| **F14** | **P2** | inference `call_parameters` | Four of the eight listed parameters (`lambda_prior_mean`, `lambda_prior_variance`, `lambda_fake_obs`, `lambda_scale`) are arguments of `lambda_predmix_eb`, not of `predmix_empbern_twosided_cs`, and are not passed by either `reference_call` string. They are documented as pinned but are unenforced defaults of an inner function. | Move them to a `documented_inner_defaults` block and add a Gate-5 assertion that the pinned source's defaults equal those values. | EXECUTED |
| **F15** | **P2** | design §6.2, "a render-only discriminator must remain at chance" | The discriminator is unspecified. If it is a statistical or deterministic classifier the fixture is no-paid; if it is a model, Gate 5 requires paid inference that §13's authorization gate does not cover. | Name the discriminator and its features (token counts, key order, position, length after padding) and state that it is deterministic and unpaid. | READ-ONLY |
| **F16** | **P2** | design §7.2 + Gate 1 | No remedy if fewer than 384 scenarios are eligible. Gate 1 requires all 384 paid cuts eligible under the cut selector, §12 forbids reserve substitution, and generation is `6 x 64` seeds fixed in advance. If some seed yields no eligible cut there is no stated path that does not break the freeze. | State a frozen over-generation rule: generate `6 x 80`, take the first 64 eligible per motif by SHA-256 order, and hash the eligibility decision into the manifest. | READ-ONLY |
| **F17** | **P3** | state/action `state.fact_current_rule` | Internal redundancy: the rule filters to "visible, effective, unretracted" and then says "if that version is retracted or out of interval, walk parent". The second clause is unreachable under the first. For a single linear chain both readings coincide, so no answer changes, but an implementer must resolve it. | Drop "effective, unretracted" from the selection clause and keep the walk, or drop the walk. | EXECUTED |

---

## 8. Attacks A to H

### Attack A — estimand and program-decision trace (READ-ONLY trace, EXECUTED arithmetic)

Four worlds, four decisions:

1. **TN useless, FD succeeds.** All candidates emit byte-identical `DecisionPacketV2`; §5 collapses them to one paid call; §9.2 passes for all three on `H` and `D`; §9.4 finds no strict dominance and returns the Pareto set with `NO_UNIQUE_ENGINEERING_WINNER`; §16 records that Moonwalker should prefer the simpler eligible mechanism. **Correct and correctly scoped.**
2. **All candidates H-linear.** §9.2's `normalized_range` exceeds threshold on every candidate; the final paragraph of §9.2 falsifies bounded continuity for the frozen workload; §16 confines the claim to the measured envelope. **Correct.**
3. **FD H-bounded but D-linear.** This is the world r4 could not see. On my r4 instrumentation FD went 24 to 2,064 reads across `D = 1..256` while FC and TN stayed flat; the `D` gate rejects FD and admits FC/TN; bounded continuity survives on FC. **Correct, and this is the single most valuable addition in r5.**
4. **Model-ceiling world.** OM below the floor triggers `MODEL_OR_INTERFACE_CEILING`, which precedes `MODEL_INTERFACE_FAIL` and `PROMOTE` in `branch_precedence`. **Correct in structure.** But F4 shows the ceiling branch requires observed OM around 0.70 or worse, so a world with OM at 0.78 produces `INCONCLUSIVE` rather than the ceiling verdict it deserves.

**Limitation.** Worlds 1 to 3 are traced against the contract text, not run end to end; only the `D` behaviour is executed, and that was executed in the prior round on my own reducers.

### Attack B — normative state and action contract (EXECUTED)

**The contradictory legal sequence.** Journal: `E1 assert_fact X=GREEN (obs 10, valid_from 10)`; `E2 correct_fact X=AMBER supersedes E1 (obs 20, valid_from 20)`; `E3 correct_fact X=RED (obs 30, valid_from 15)`, a retroactive correction that `query_clock.retroactivity` explicitly permits.

`correct_fact`'s guard evaluates the supersession target at `(journal_seq-1, observed_at, valid_from) = (2, 30, 15)`. At valid time 15, `E2` is not yet effective, so the current visible effective version is `E1`. The guard therefore requires `E3` to supersede `E1`. But `E1` already has child `E2`, and the same guard forbids an edge that creates "a cycle or sibling branch", and `fact_current_rule` speaks of "the one linear supersession chain". **The retroactive correction is rejected as `ILLEGAL_TRANSITION`.**

So `mandatory_enumerator_checks`'s "retroactive correction changes a later knowledge cut but never rewrites a prior cut" and §7.6's "retroactive correction at two knowledge cuts" are satisfiable only on a chain with no later correction. The contract never says so, and an implementer meeting `ILLEGAL_TRANSITION` on the natural fixture has to guess whether that is the intended answer. This is exactly the "legal state/action trace with two possible answers" the omission attack asks for.

**Other guard attacks that held.** Two-event pair coverage is asserted rather than enumerable by me. `delegate_obligation` correctly forbids a payload `scope_id` and `scope_rule` makes scope immutable, so cross-scope delegation is cleanly illegal. `link_dependency` requires same scope, both OPEN, distinct IDs, no existing edge, and acyclicity. `open_handoff` forbids a second in-flight handoff on one obligation. `complete_obligation` requires the obligation to be in `O_due` at the event cut, which is a real and useful restriction. `reopen_obligation` requires `supersedes_event_id == terminal_event_id`, which prevents reopening a stale terminal. Duplicate `event_id` or `idempotency_key` yields `DUPLICATE_NOOP`. These are well built.

**Four simultaneous due criticals.** `gold_cardinality` up to four now expresses it, which repairs the r4 defect. It creates F3.

**Limitation.** I did not build the full enumerator over all 17x17 ordered pairs. My substitute was a literal implementation of the guards for the fixtures §7.6 names, which is where the contradiction lives.

### Attack C — FD/FC/TN comparison (READ-ONLY this round, EXECUTED in the prior round)

Nine trace families run in the r4 round on the same three candidate families produced FD/FC/TN semantic parity in nine of nine, and every typed supersession pair TN persists was recomputable from the flat journal. Nothing in r5 changes that, and r5's §5 now handles it correctly by construction rather than treating it as a defect.

**FC snapshot-tail overflow.** r5 §5 already names the risk ("its contract must prevent a checkpoint ceiling from silently restoring full replay") and §7.6 mandates a "checkpoint/tail overflow without full replay" trace. Opened prior art confirms this is the standard failure mode: snapshot-plus-tail is the ordinary rehydration pattern, and the practitioner literature is explicit that the fitness function is a **scheduled clean rebuild from event zero that completes inside its time budget**, with the named failure being that "storage and replay time grow without bound; the first projection rebuild attempted during an incident takes days". r5 has the rebuild-equality witness (witness 7) but **does not time-budget it**. That is the borrow in §9.

**No semantically distinct fourth comparator found.** FD, FC and TN span read-time derivation, coarse materialization and typed materialization over one journal. Anything else I could name (a pure current-only overwrite, a learned retriever, a summary tier) is either dominated by FD, excluded by §2, or a storage strategy inside FC.

### Attack D — boundedness and physical-work accounting (EXECUTED)

| Axis | span | allowed range at `1e-4` | integer units permitted |
|---|---:|---:|---:|
| `H` = 128..100,000 | 99,872 | 9.9872 | **9** |
| `D` = 1..256 | 255 | 0.0255 | **0** |

**Unit incoherence, the same physical event judged three ways:**

| event | counter unit | `H` | `D` |
|---|---|---|---|
| one extra index page touched | pages | `1.0e-5` PASS | `3.9e-3` **FAIL** |
| one extra index record read | records | `1.0e-5` PASS | `3.9e-3` **FAIL** |
| the same page, charged in bytes | bytes (4,096) | `4.10e-2` **FAIL** | `16.06` **FAIL** |
| one 512 B index node | bytes | `5.13e-3` **FAIL** | `2.008` **FAIL** |
| one 64 B cache line | bytes | `6.41e-4` **FAIL** | `0.251` **FAIL** |

§9.2's prose says the gate "admits a small bounded index-height change". On a page counter it does. On a byte counter it does not, by 410x on `H`. On `D` it admits nothing at all on any counter. Since §8.1 charges "physical records/pages/**bytes** read and written" and §9.2 says "no operation is exempt as metadata", the byte counters are in scope and the `D` gate as written requires **byte-identical physical reads across a 256-fold change in active-subject history depth**. That is satisfiable only by fixed-size records with a constant-depth lookup path, a storage-family mandate the design never states, and it is unsatisfiable by FD by construction.

**Hiding work.** Two routes that survive: growth at 1 charged unit per 11,097 archive events passes as bounded (901 units at a 10M archive, 9,012 at 100M); and because the gate is per counter with no total, splitting one linear counter across two halves its slope, so the roughly 13 counter families of §8.1 can absorb up to 117 units while every counter individually passes.

**What the gate does catch, and catches well.** "Every intermediate scale must lie within the same minimum-to-maximum counter envelope" defeats a non-monotone spike at an intermediate `H`. Cold open, decode and background work are explicitly included, which closes the r4 hole. The governed physical-read API with taint on direct reads is the right enforcement primitive.

**Limitation.** My analysis is arithmetic on the stated rule; I have no candidate implementations at r5's contract to measure. The prior round's FD/FC/TN counters are indicative of shape, not of these specific counters.

### Attack E — presentation and A→B→A (EXECUTED for the DAG, READ-ONLY for rendering)

**Presentation.** §6.2's byte-identical outer keys, key order, descriptions, instructions, action list and order, output schema, token envelope, padding policy, serialization and transport, plus neutral `object_kind` and reference-proven empty arrays, is the correct repair to the r3 empty-field problem. The blinding fixture is the right test. F15 is the only gap: the discriminator is unnamed.

**The A0 leak that is not a leak but is a scoring artifact.** Because §6.2 forbids anything pointing at the target and `A0_target` is defined by a lexicographic rule the model is never told, a multi-gold cut is a coin flip. Detail in F3. Note the asymmetry risk: if OM's "minimal public semantic objects required for the selected cut" happens to carry fewer critical due obligations than BC, the two conditions face different gold cardinalities and the comparison is biased. §6.2 does not pin OM's gold cardinality to BC's.

**The walk.** A0 emits a target plus `TaskPacketV2`; B receives only `TaskPacketV2` and emits `WorkerHandoffV2` with zero free-text fields and capped enumerated codes; the writer validates scope, hash binding, transition legality, action availability and idempotency; A1 reconstructs process-cold from the committed artifact. Wrong-scope, correction, duplicate, rejection, commit and close are all covered by contract guards. **Crash after accepted response is covered only at the B node** (F5). **The invalid-proposal path is underdetermined** (F6).

**Smuggling reasoning.** I could not find a channel. `unresolved_item_codes` and `warning_codes` are closed enumerations of five and four values respectively, and the numeric caps (4, 32, 8, 4, 4, 4, 8, 8) bound the total channel to roughly a few dozen public IDs. The residual bandwidth is the **choice among enumerated codes**, which is a handful of bits per handoff. That is a real but small channel and I would not call it a defect.

### Attack F — producer taint and artifact causality (READ-ONLY)

The §10 allowlist (public journal and payload root, normative schema, candidate implementation, governed dependency API, output path, explicit config) plus taint canaries in forbidden modules and packets, plus opaque scenario IDs, plus network disabled, is the right shape. Witness 3 (source-directory rename) closes the absolute-path channel from r3. Witness 7 (journal-rebuild equality) closes the persisted-final-packet loophole from r4: a candidate that persists a materialized packet must still show that the packet is rebuildable from the canonical journal.

**What I could still construct that passes.** A candidate whose rebuild path is correct but whose **rebuild cost is unbounded**. Witness 7 asserts equality, not budget. A candidate that keeps a tiny artifact and rebuilds everything from the journal on demand passes all seven witnesses, passes packet identity, and only shows up in the §9.3 "rebuild time" Pareto dimension, which is a reported dimension rather than a gate. That is the exact failure the event-sourcing literature names. Repair in §9.

**Limitation.** No harness exists; all seven witnesses are analysed against text, not run.

### Attack G — exact inference (EXECUTED)

**Reference vectors.** My independent reconstruction of `predmix_empbern_twosided_cs` (`mu_hat_t = (1/2 + cumsum(x))/(t+1)`, `sigma2_hat_t = (1/4 + cumsum((x-mu_hat_t)^2))/(t+1)`, lagged `sigma2`, `lambda_t = min(sqrt(2 log(1/alpha) / (sigma2_{t-1} t log(1+t))), 0.5)`, `psi_E`, `v_t = 4(x_t - mu_hat_{t-1})^2`, running intersection, two-sided by `1 - lower(1-x)` with alpha split):

| vector | my reconstruction at n=96 | contract at n=96 | relative difference |
|---|---|---|---|
| `delta_all_zero` | `[-0.182584443111, +0.182584443111]` | `[-0.184596392909, +0.184596392909]` | **1.10%** |

With no alpha split the reconstruction gives `-0.153703310588`, which is further away. The contract's vectors are exactly proportional to `1/n` (`0.184596 -> 0.092298 -> 0.046149`), which forces `cumsum(lambda) = 0.5n` and hence `delta_lower = -4 log(1/alpha_eff)/n`, giving `log(1/alpha_eff) = 4.430313430` and `alpha_eff = 0.011911`. For comparison `log(1/0.0125) = 4.382027` and `log(1/0.025) = 3.688879`. **I cannot identify any documented parameter convention that yields 0.011911**, and I could not reach the pinned upstream bytes to settle it. This is F8 and it is unresolved by me.

**Branch feasibility, using the contract's own published vectors so the conclusion is robust to F8:**

| look | best possible `delta_lower` (all deltas zero) | PROMOTE possible? |
|---:|---:|---|
| 96 | `-0.184596` | **No** |
| 192 | `-0.092298` | Yes, but only near-perfect |
| 384 | `-0.046149` | Yes |

Discordance sweep on my reconstruction, `P(delta_lower > -0.10)`:

| n | 0.00 | 0.02 | 0.05 | 0.10 | 0.15 | 0.20 |
|---:|---:|---:|---:|---:|---:|---:|
| 192 | 1.00 | 0.75 | 0.49 | 0.33 | 0.29 | 0.19 |
| 384 | 1.00 | 1.00 | 1.00 | 0.98 | 0.87 | 0.72 |

`n=384` is well powered on the delta side out to roughly 15% discordance. That part of the design is sound.

**The OM dead band** (my reconstruction, anchored on the contract's two published OM vectors):

| observed OM at n=384 | CS | branch |
|---:|---|---|
| 0.65 | `[0.605, 0.769]` | CEILING |
| 0.70 | `[0.601, 0.778]` | CEILING |
| 0.75 | `[0.667, 0.836]` | **dead band** |
| 0.80 | `[0.766, 0.890]` | **dead band** |
| 0.86 | `[0.789, 0.926]` | **dead band** |
| 0.87 | `[0.806, 0.933]` | PROMOTE-eligible |
| 0.90 | `[0.849, 0.960]` | PROMOTE-eligible |

The contract's own `om_eighty_percent_pattern` at 384 is `[0.717733, 0.878808]`, which is neither branch. **The design's nominated floor sits inside the region where the design cannot conclude.**

**Parameters still left to implementer choice.** Beyond F8 and F14: no stopping rule (F10); no per-look missingness ceiling (the 2% rule is stated only "by n=384", so five missing pairs at `n=96` is 5.2% and unconstrained by the fraction rule, mitigated but not eliminated by the worst-case invariance requirement); and the interpreter and NumPy versions used to generate the vectors are unrecorded, which matters at a `1e-12` tolerance.

**Limitation.** My reconstruction is a transcription from the published construction, not the pinned source. Everything I say about the vectors is conditional on it, which is why F8 is stated as unresolved rather than as a defect in the contract.

### Attack H — DAG, cost and transport (EXECUTED)

| n | BC calls | OM calls | accepted calls | child reconstructions |
|---:|---:|---:|---:|---:|
| 96 | 288 | 288 | 576 | 192 |
| 192 | 576 | 576 | 1,152 | 384 |
| 384 | 1,152 | 1,152 | **2,304** | **768** |

Reproduces §11 and §13 exactly from the invocation graph. **The DAG is right and the arithmetic checks.**

Hypothetical envelope (**price is illustrative; no authorization is implied or requested**): BC 3,000 input tokens, OM 1,500, 300 output, gives 5.18M input and 0.69M output tokens, so roughly **$9 at $1/$5 per M, $26 at $3/$15, $130 at $15/$75**, and about **1.9 hours** of single-in-flight wall clock plus 768 cold child starts. This is a proportionate first screen and a large improvement on every prior revision.

**Transport reliability implied by the 7-pair ceiling** (F7):

| per-call failure | per-pair (6 nodes) | expected missing of 384 | P(TRANSPORT_INCONCLUSIVE) |
|---:|---:|---:|---:|
| 0.05% | 0.30% | 1.2 | 0.000 |
| 0.10% | 0.60% | 2.3 | 0.002 |
| 0.20% | 1.19% | 4.6 | 0.093 |
| 0.30% | 1.79% | 6.9 | 0.380 |
| 0.50% | 2.96% | 11.4 | 0.883 |

**Transport surface.** §13's freeze list is materially complete: one provider, fallbacks off, response cache off, no server preset, tools, transforms or hidden conversation chain, route metadata required on every uncached response, session and routing fingerprint held constant across paired arms. Against current provider and router documentation the two residual items are both account-level rather than request-level, and §13 now names both ("session/routing fingerprint held constant", "no server preset"), which closes what r4 left open. The one thing I would add explicitly is the model-level fallback array, which is a channel independent of provider fallbacks.

**Removable machinery.** Nothing operational. The only removable item is the `n=96` look's PROMOTE branch, which is provably unreachable and should be labelled futility-only rather than deleted, since it retains value for early `CEILING` and `FAIL` stopping if a stopping rule is added.

---

## 9. WHAT WOULD YOU BUILD?

**Mechanism 1: a per-unit-class boundedness gate, plus a total.** Replace the single `1e-4` with an allowance table: count-class counters get an absolute integer allowance per axis, byte-class counters get a relative allowance calibrated to one index node, and the sum within each class is gated as well as each member. This is the F1 and F2 repair and it is the difference between a gate that measures boundedness and a gate that measures which units you happened to pick. **Label: EXECUTED (my own arithmetic); no prior art claimed.**

**Mechanism 2: time-budget the rebuild, do not just assert its equality.** Witness 7 proves the projection is rebuildable. The event-sourcing fitness function that practitioners actually use is stronger: a scheduled clean rebuild from event zero that **completes inside a declared time budget**, with the named failure mode being that storage and replay time grow without bound until the first rebuild attempted during an incident takes days. Add a rebuild-time ceiling to witness 7 and charge it on the `H` and `D` axes. This is also the honest way to gate FC's snapshot-plus-tail against a checkpoint ceiling silently restoring full replay. **Label: SEARCHED (arc42 quality model event-sourcing entry and AWS Prescriptive Guidance, opened this session).**

**Mechanism 3: make the A0 unit unambiguous by construction.** Restrict `cut_selection` to cuts with exactly one mounted critical `O_due` obligation. The multi-gold case is still exercised deterministically at all 24 Stage-1 cuts and by the mandatory four-simultaneous-due trace, so nothing is lost scientifically, and the paid unit stops carrying a guessing factor. **Label: EXECUTED reasoning against the pinned contract.**

**Mechanism 4: set the OM threshold from the dead band, not from a round number.** Publish the `n=384` mapping from observed OM to branch (my table above), pick the floor so `CEILING` and `PROMOTE` tile the achievable space, and publish the implied per-decision reliability alongside so the owner authorizes against a number they can compare to prior art rather than against 0.80. **Label: EXECUTED.**

---

## 10. WOULD YOU DESIGN IT DIFFERENTLY?

Three changes. The causal program stays exactly as it is.

**(1) Gate boundedness on shape, not on a threshold.** The deeper problem behind F1 is that a two-point or four-point slope test is being asked to certify an asymptotic property. Better: fit the charged counter against `H` and against `log H`, and require that the linear coefficient's confidence bound exclude a preregistered slope while reporting the logarithmic coefficient freely. That is honest about what four points can show, it is unit-invariant if you fit per counter and report standardized coefficients, and it lets a legitimate index-height change appear as a logarithmic term instead of failing a linear gate.

**(2) Make Stage 2's unit the decision, not the scenario.** `contract_success` is a three-way conjunction and every problem in F3 and F4 flows from that: a single guessed tie-break at A0 kills the whole scenario, and OM lands in the dead band. Score the three nodes separately, report the paired delta on each, and define the scenario conjunction as a secondary. You keep the strictness where it belongs (duplicate effects, stale resurrection, wrong scope are all still zero-tolerance deterministic gates) while giving the paid screen a unit whose failure rate is interpretable.

**(3) Resolve F8 before anything else.** The reference vectors are the acceptance criterion for the entire inference layer. If they were generated with parameters other than the ones the contract states, Gate 5 will reject a correct implementation at `1e-12` and the failure will look like an implementation bug for as long as anyone is willing to keep debugging. This is a half-day of work and it gates everything downstream of it.

---

## 11. Omission attack

| Required item | Answer |
|---|---|
| **Strong simple comparator still omitted** | **NONE, with evidence.** FD spans read-time derivation with the full index set, FC spans coarse materialization plus snapshot-and-tail, TN spans typed relations. Nine trace families in the prior round showed semantic parity across all three, and the snapshot-plus-tail literature I opened confirms FC's variant is the standard rehydration strategy rather than a distinct semantics, which is exactly how r5 classifies it. Any further candidate is dominated, excluded by §2, or a storage strategy inside FC. |
| **Legal trace with two possible answers** | **FOUND, executed.** `assert(valid 10) -> correct(valid 20) -> retroactive correct(valid_from 15, observed 30)`. `correct_fact`'s guard forces the third event to supersede the first, and the same guard's no-sibling-branch clause then rejects it. `retroactivity` says it is legal; `mandatory_enumerator_checks` requires it as a fixture. Answer 1: `ILLEGAL_TRANSITION`. Answer 2: the branch is permitted and `fact_current_rule` must handle a non-linear chain. The contract supports both readings. |
| **Hidden confound falsely PASSING bounded continuity** | **Per-counter aggregation with no total** (F2). Thirteen counter families each permitted 9 units on `H` conceal up to 117 units of archive-linear work while every counter passes. Secondary: growth at 1 unit per 11,097 events is certified bounded and reaches 901 units at a 10M-event archive. |
| **Hidden confound falsely favouring FD/FC/TN** | **The unit choice in the `D` gate** (F1). `D` permits zero charged units on every counter. FD reads the correction chain, so FD fails by construction; FC and TN pass if and only if their lookup path is byte-identical across a 256-fold depth change. So the `D` gate does not merely test boundedness, it selects a storage family, and it selects against the simplest candidate. Whether that is correct science or an artifact of the threshold cannot be told apart as the gate is written. |
| **Persuasive false-positive model-usability story** | BC and OM are near-substitutes because OM must contain every mounted critical due obligation for `A0_target` to be well-defined, so the two packets differ only in distractor load. Discordance comes in at 3%, the delta CS clears `-0.10` comfortably at `n=384`, OM happens to land at 0.89, and the run returns `PROMOTE`. What was actually shown is that removing distractors from a packet does not change a three-node conjunction, which is a much weaker claim than "the model can use externally validated state". Guard: preregister the discordance rate that makes the result informative, and report `P(BC=1,OM=0)` and `P(BC=0,OM=1)` separately, which the contract already requires. |
| **Persuasive false-kill story** | Gold cardinality averages two to three across the 384 selected cuts, so the A0 factor sits near 0.5 (F3). OM's observed contract success lands at 0.78, inside the dead band (F4). The run returns `INCONCLUSIVE_OR_UNDERFUNDED` at `n=384`, the owner reads it as "the model could not use the packet", and the actual cause is an unstated lexicographic tie-break interacting with a floor chosen from a round number. Full budget spent, nothing learned about continuity. |
| **Uncaught footgun** | **The invalid-proposal writer path** (F6). Both `ILLEGAL_TRANSITION` (nothing appended, handoff stuck at `RESPONSE_RECORDED`) and `reject_handoff_result` (appended, handoff `REJECTED`) are legal responses to a bad B proposal. A1 reconstructs from the canonical journal, so the choice changes A1's input and therefore `contract_success`. No gate in §14 detects it because both paths are individually contract-conformant. |
| **No-paid test without which I refuse harness implementation** | **Regenerate and re-verify the five reference vectors from the pinned upstream bytes, with the generating script, its hash, and the interpreter and NumPy versions recorded.** Until an independent implementation and the pinned implementation agree with the published vectors to `1e-12`, Gate 5's acceptance test is unvalidated and every downstream inferential claim rests on five numbers nobody has reproduced. My reconstruction does not reproduce them (1.10% off), and I could not reach the bytes to say which side is wrong. |
| **Prior-art mechanism to borrow** | **A time-budgeted scheduled clean rebuild from event zero** as the fitness function for the snapshot-plus-tail path, from event-sourcing practice. Witness 7 already asserts rebuild equality; the practitioner literature's stated failure mode is that replay time grows without bound until the first incident-time rebuild takes days, and its stated control is that a full rebuild runs regularly and completes inside its budget. Adding a rebuild-time ceiling to witness 7 and charging it on `H` and `D` converts an equality assertion into a boundedness test. SEARCHED. |
| **Machinery to delete** | **Operationally, NONE — ALL LOAD-BEARING.** r5 has already cut the diagnostics, the exhaustive performance repetitions and the paid diagnostic cells. The only deletion available is analytic: the `n=96` look's PROMOTE branch is provably unreachable from the contract's own vectors and should be relabelled futility-only rather than removed, since it still supports early `CEILING` and `FAIL` stopping once F10's stopping rule exists. |
| **Exact boundary versus the next coordination experiment** | MBCX-01 owns everything with **one canonical journal, one single-threaded writer enforced by construction, one logical conductor identity, and one frozen model**: the bitemporal algebra, obligation lifecycle, bounded materialization across `H` and `D`, artifact-causal reconstruction, and exactly one serial `A0 -> B -> writer -> A1` episode per condition per scenario adjudicated before A1 resumes. The boundary is crossed the moment any of four things is true: a second proposal may be in flight against the same obligation; two workers hold divergent views of one scope; B is a different model or a different endpoint; or the writer must merge rather than accept-or-reject. r5 draws this correctly in §2 and §16, and `open_handoff`'s guard enforces the first of the four **in the contract rather than by convention**, which is the right place for it. The one thing I would add is the symmetric statement for the writer: the single-threaded commit boundary is a contract-level guard, not a runner convention, so that concurrency cannot leak in as an implementation accident during Stage 1. |

---

## 12. Sweep log

| Lane | Exact query | Opened origin | Decisive section | Level | Effect | Stop reason |
|---|---|---|---|---|---|---|
| 6. Pinned inference source | `gostevehoward confseq predmix.py predmix_empbern_twosided_cs github` | `github.com/gostevehoward/confseq/`, `.../blob/master/src/confseq/betting.py` (fetched in full), releases and package datasheet pages | `betting.py` line 1 imports: `from confseq.predmix import lambda_predmix_eb`; `hedged_cs` defaults `prior_mean=1/2, prior_variance=1/4, fake_obs=1`, matching the contract's `lambda_*` values; module-level imports of `matplotlib`, `scipy.optimize` and `multiprocess`, consistent with the contract's note about stubbing unused optional imports | SEARCHED, primary repository | Confirms the repo, the function family and the lambda defaults are real, and corroborates the contract's honesty about import stubbing. **Does not verify the two pinned blobs**: `web_fetch` refuses constructed URLs and neither pinned file surfaced in search. Raises F9 (`betting_strategies.py` not evidenced at master, where the lambda function lives in `predmix`). | Could not reach the pinned files by any route available to this seat; escalating further would not have produced the bytes. Logged **COULD-NOT**. |
| 2 and 5. Snapshot, delta tail, checkpoint, clean rebuild | `event sourcing snapshot plus delta tail checkpoint frequency read amplification bounded replay incremental materialized view maintenance` | `quality.arc42.org/approaches/event-sourcing`, `docs.aws.amazon.com/prescriptive-guidance/.../event-sourcing.html`, two practitioner deep-dives | arc42: "A command rehydrates its aggregate by replay (or snapshot plus tail) ... each rebuildable from event zero"; failure mode "Storage and replay time grow without bound; the first projection rebuild attempted during an incident takes days"; fitness function "A projection rebuild from event zero runs regularly and completes inside its time budget". AWS: replay complexity, idempotency, snapshot complexity, event-store growth | SEARCHED, one quality-model reference and one vendor guidance, plus practitioner secondary | Supplies the §9 mechanism-2 borrow and confirms r5's FC classification and its snapshot-ceiling warning are correctly aimed. Does not change any ruling on its own. | Found the named fitness function and the named failure mode; further practitioner sources were repeating the same content. |
| 1. Module and stage diagnosis | carried: `Text2Mem MemEval agent memory system evaluation phase-aware decomposition benchmark 2026` | `arxiv.org/pdf/2605.18565` (MINTEval), `arxiv.org/html/2605.12493v1` (LongMemEval-V2), `arxiv.org/pdf/2509.11145` (Text2Mem), `arxiv.org/pdf/2605.28732` (MemTrace) | MINTEval: evaluation overlooks "recall and aggregate information from earlier states" and targets "evolving and interference-heavy contexts" | SEARCHED, primary | This is the source r5 §17 now cites for the `D` axis, and the citation is accurate. **Non-independent: I introduced it in the r4 round.** | Already opened this session. |
| 2. Mechanism and render controls | carried: StateFuse, Presentation Not Mechanism | `arxiv.org/pdf/2607.05844`, `arxiv.org/abs/2607.16019` and its PDF Table 2 | Fine-grained typed residual indistinguishable from zero; coarse deprecation `+0.087 [+0.046, +0.130]`; StateFuse ties flat and raw-log baselines on accuracy under matched resolvers | SEARCHED, primary | Underwrites r5's retirement of `TN - FM` and its FC arm. **Non-independent.** | Already opened. |
| 3 and 4. Obligations, durable identity, handoff | carried: durable execution and record/replay | Temporal, Restate, LangGraph, Inngest surfaces plus the durable-execution section of arXiv 2606.17182 | Recorded non-deterministic results replayed as data; journaled steps giving exactly-once without application idempotency keys | SEARCHED, vendor docs plus one secondary | This is the source of r5 §6.4's write-ahead rule. My F5 is that r5 implemented it at one of three call nodes. **Non-independent.** | Already opened; the Burckhardt formalization remains unopened and is a pointer only. |
| 7. Provider and runner | carried: OpenRouter provider-selection and prompt-caching docs | `openrouter.ai/docs/guides/routing/provider-selection`, `.../best-practices/prompt-caching`, response-caching announcement | Sticky routing hashed from first system plus first non-system message, account-level, five-minute expiry; server-side presets shallow-merged; `models` array as an independent fallback channel; response cache scoped to API key | SEARCHED, primary vendor docs | r5 §13 now names session and routing fingerprint, presets, cache, transforms and tools, closing what r4 left open. The model-level `models` array is the one channel still unnamed. **Non-independent.** | Already opened and current. |

**Global-surface note.** The named non-US, non-UK institutional pass in this bundle's evidence base (StateFuse, University of Hong Kong) is carried from a prior round, and I ran **no national-repository or national-language query this round**. Every negative in this report is therefore **field-level, not country-level**, per packet §6.

---

## 13. Residual risks and explicit non-claims

**Residual risks.**

1. **Non-independence is still the largest risk in this document.** Most of what I praise in r5 is what I asked for in r4. A fresh seat should be run specifically on the two JSON contracts, and should be given the packet without this thread.
2. **F8 is unresolved and I could not resolve it.** If my transcription is wrong, the vectors are fine and F8 collapses to nothing. If the vectors are wrong, F8 is a P0 that blocks the entire inference layer. A seat with repository access settles it in ten minutes.
3. My boundedness analysis is arithmetic on the stated rule. I have no candidate implementations at r5's contract and no measured counters, so the claim that FD fails the `D` gate rests on the structure of read-time derivation, not on a measurement of r5's FD.
4. The OM dead band is computed with my reconstruction, anchored on the contract's two published OM vectors. The two anchors bracket the band, so the band's existence is robust; its exact edges (0.71 and 0.86) depend on F8.
5. The A0 blind-success arithmetic assumes a model with no prior over lexicographic conventions. A model that guesses "first listed" or "smallest ID" by habit would do better than chance. The direction of the bias is certain; the magnitude is not.
6. All of §10 and §13 are READ-ONLY from me and cannot be a deciding GO.

**Explicit non-claims.**

- I do **not** claim the contract's reference vectors are wrong. I claim an independent reconstruction does not reproduce them and that the discrepancy must be resolved before they are used as an acceptance test.
- I do **not** claim FD is unbounded in depth as r5 would implement it; I claim the `D` gate as written permits zero units on every counter and that a read-time deriver cannot meet that.
- I do **not** claim Stage 2 will return `INCONCLUSIVE`; I claim the design's own thresholds make that the outcome across a wide and plausible band of OM performance, and that the band is not stated anywhere in the bundle.
- I do **not** claim any licensing, security, deployment, concurrency, or cross-model position.
- I did **not** open the two pinned upstream files, the seven lineage artifacts, a national repository surface, or the Burckhardt durable-functions formalization, and no ruling rests on them.

---

## 14. Seat capability and seal report

| Dimension | Status |
|---|---|
| Local file read | Full via the Moonwalker bridge, byte-verified against the git objects before use. |
| Local shell | One call, sentinel-verified (`MBCX01-R6-SEAL-V7N2` in stdout, echoed `command` compared). No crossing. |
| Code execution | Isolated Linux container, no egress. Three scripts written and run. |
| Web | Native `web_search` and `web_fetch` live. Two searches, one full fetch. **One capability limit that matters: `web_fetch` refuses any URL that has not appeared in a prior search or fetch result, so I could not reach `raw.githubusercontent.com` at the pinned commit and could not verify the two upstream `confseq` pins.** No Moonwalker crawler escalation was attempted; it would have required a local write. |
| Tokenizer | **LIMITED.** No tokenizer is frozen in r5 (§13 defers it). All Attack-H token figures are disclosed hypotheticals from stated caps, and the price figures are illustrative with no authorization implied. |
| Statistical | Full within the container. Reconstruction transcribed from the published construction, not the pinned source; this is the binding limit on Attack G and is recorded as F8. |
| Paid inference | **NONE.** No model call, no canary, no API request of any kind. |
| Side effects and cleanup | **NONE on your machine.** No file created, modified, moved or deleted anywhere under `C:\`. No git object, branch, stash, index or config change. The single shell call was read-only (`rev-parse`, `cat-file`, `status --porcelain`) with hashing done in memory through a piped stream so that no temporary file was written. All three probe scripts exist only in the container sandbox and are discarded with it. No child process, watcher, daemon, browser session or tab was created. No council seat was contacted. |
| Verdict delivery | In-thread, as this reply. Nothing written to a file, artifact, canvas or vault. |

**Sealed-independence confirmation, with the disclosed exception.** I read exactly four files, each by exact explicit path: the r6 packet, the role card, and the three pinned bundle blobs (`d37dad72`, `27abf1a8`, `906a3643`). I ran no `moonwalker_search_files`, no `moonwalker_grep`, no `moonwalker_ls`, no `moonwalker_memory_search`, no `dir` and no `Get-ChildItem`. I opened no prior verdict, council report, synthesis, exec log, receipt, watcher, restart manifest or browser output, and no filename containing `VERDICT`, `COUNCIL-ROUND`, `SYNTHESIS`, `EXEC-`, `RECEIPT` or `RESTART-MANIFEST`. No prohibited snippet reached my context through any file route.

**The exception, per packet §0's own instruction:** this conversation retains my r3 and r4 rounds. I have disclosed it at the top, labelled the repeated recommendations as non-independent throughout section 6 and section 12, and continued as a second-round reviewer. **The seal does not hold against my own prior rounds, and I am not pretending otherwise.** The three P0 findings all originate in the two JSON contracts, which I had not previously seen, so they are the part of this verdict least affected by that contamination.