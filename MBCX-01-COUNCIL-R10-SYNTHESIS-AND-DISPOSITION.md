# MBCX-01 Council Round 10 synthesis and disposition

Date: 2026-08-13  
Round: r10  
Governing commit reviewed: `efaa1bbff91b887597b711ff4936109e79ccfddd`  
Paid/model/provider calls performed by the conductor: **NONE**

## Controlling disposition

**NO-GO.** Opus returned `GO-WITH-FIXES`, but ChatGPT/Sol and Codex independently executed multiple false-green traces at the joins between otherwise-improved components. Council rulings are evidence-weighted, not majority-averaged and not softened by the gentlest seat. A reachable false scientific result controls the gate.

r10 did close important prior defects: strict event ingress, the bitemporal visibility predicate for the tested expired/future cases, action/catalog hash guards, fixed-envelope rendering, the 100-cell H-D-F grid, root-plus-child instruction aggregation, the five-by-five call-state matrix, exact missing-completion DP, the mathematical `(456,4)` binomial tails, honest scheduled-position terminology, and exact Git-object reconstruction of the listed subjects. Those repairs are retained.

## Converged failures

| Repair ID | Severity | Consolidated finding | Evidence convergence | r11 disposition |
|---|---:|---|---|---|
| R11-STATE-NATIVE | P0 | Both reducers inherit r9 semantics. A future-effective row can block a current fact, a finite visible head cannot be corrected, retro-correction can invert an interval, and arbitrary event IDs pass. | Codex executed; Chat confirmed the shared-provenance seam class. | Replace runtime inheritance with r11-owned reference and independently structured oracle reducers. Define canonical event IDs and nonempty/nonoverlapping fact intervals. |
| R11-RESPONSE-FK | P0 | A proposal can succeed with no matching B response or with an unrelated scenario's globally recorded response hash. | Codex and Chat executed independently. | Add `handoff_id`, task/request/route identities and durable-response foreign keys; require one exact `(handoff, scenario, condition, B)` record before proposal. |
| R11-SCORER-ADMISSION | P0 | `score_exact` accepts schema-invalid objects, fake packet hashes, unbound request hashes and invented child IDs. | Codex and Chat executed independently. | Add composite scorer admission and validate every object, byte hash and causal edge inside the scoring boundary. |
| R11-TYPED-DAG | P0 | There is no TaskPacket; A0/B/A1 are collapsed onto one precommit packet; the 96-hex request field cannot equal the 64-hex served SHA-256. | Codex and Chat executed independently. | Define distinct precommit A0 packet, B TaskPacket/request, durable B response, writer receipt, postcommit A1 packet and result. |
| R11-BC-BINDING | P0 | The manifest does not bind the candidate BC selection, so BC can be built from OM's gold read set. Gold/action semantics can also be forged. | Chat executed; Codex's admission/causal findings cover the same boundary. | Bind candidate selector ID, selected object IDs and selection hash; recompute unique gold/A1 truth from the canonical state and action universe. |
| R11-COHORT-PROVENANCE | P0 | Contract says `stage2-cut-r10`, implementation calls a helper hard-coded to `stage2-cut-r9`; 636/960 cuts differed. Motif and action-universe substitution also passed. | Codex and Chat executed independently. | Use the contract domain directly and require a provenance manifest binding generator, scenario→motif, cut set and action universe. |
| R11-PHYSICAL-RECEIPT | P0 | Mixed candidate IDs and Boolean axes pass; wall time and I/O are absent; no OS-produced containment/completion receipt exists. | Codex and Chat executed independently; Microsoft primary documentation confirms Job Object aggregate CPU/I/O accounting and breakaway conditions. | Require one candidate/generator identity, strict integers excluding Booleans, elapsed time, Job CPU/I/O/memory, instruction-backend evidence, no-breakaway and active-zero completion evidence. |
| R11-DURABLE-LEDGER | P0 | Empty request/token values can reach `RESPONSE_DURABLY_RECORDED`; the state contains no response bytes/hash/ref/fsync receipt/recovery record; ambiguous retry uses a bare Boolean. | Codex executed; Chat independently demonstrated cross-scenario replay and cited mature idempotency practice. | Replace the label-only dataclass with a digest-bound, serializable transactional record and structured route attestation. |
| R11-POWER-CLAIM | P1 | The region-wide interface-fail promise is false under allowed within-pair dependence. At `(p00,p01,p10,p11)=(0,.3,.1,.6)`, n=768 achieved about 71%, not 90%. | Codex and Chat executed independently. | Keep n=768 and restore assurance to explicit, fully specified joint cells. Do not buy a 50% larger run merely to defend an unnecessary region-wide sentence. |
| R11-ROUTE-MODEL | P1 | `(456,4)` is exact/minimal under iid, but r10 did not make iid true; perfect correlation gives a `.98` bad-route pass probability. | Codex and Chat executed independently; NIST expressly conditions the OC curve on a valid binomial model. | Replace the marginal-iid claim with a conditional-failure-hazard contract and a frozen time-stratified schedule. Prove the same binomial tails by sequential coupling under the stronger conditional hypotheses. |
| R11-DESIGN-PRECEDENCE | P1 | The r9-adopted `DESIGN_OR_IMPLEMENTATION_FAIL` before `TRANSPORT_INCONCLUSIVE` rule disappeared from v5 and the executable decision. | Opus executed by regression search. | Restore an explicit precedence array and make the design gate an input to every missingness decision. |
| R11-PORTABLE-AJV | P2 | The Ajv bytes are cryptographically tree-hashed, so “unhashed” is incorrect; however, execution is host-hard-coded to a different repository and the runtime bytes are outside the reconstructed subject set. | Opus executed; conductor checked the v4 runtime closure. | Vendor one deterministic Ajv bundle as a governed subject and remove the absolute path. |
| R11-BOOTSTRAP | P2 | The prescribed worktree launcher runs before its own bytes are authenticated. | Chat executed/read; SLSA verification guidance supports a pre-execution trust root. | Packet instructions extract the launcher by its council-pinned Git blob before execution. |
| R11-REPAIR-LEDGER | P2 | A previously adopted repair silently vanished in a rewrite. | Opus. | Add a machine-consumed repair ledger mapping every adopted repair to an executable witness ID. |

## Cost decision in plain language

The experiment's main question is still answerable. The current blocker is wiring, not sample size. Paying for more calls cannot repair the wrong cohort, an invented causal lineage, unmeasured I/O, or a ledger that calls a response durable without storing evidence.

The proposed r11 keeps the scientific run at 768 pairs / 4,608 scheduled positions. The broader r10 sentence promised 90% failure classification for every allowed joint distribution in a large region; that sentence was stronger than the research question requires. r11 will make the power claim only at explicit joint distributions that are actually simulated and pinned. A larger run may broaden the set of distributions receiving a 90% planning assurance, but it does not make the decision rule valid and it does not remove exact-threshold uncertainty.

The route gate remains 456 six-call trials / 2,736 scheduled positions only if its hypotheses are rewritten correctly. r11 will not claim that time spacing magically creates independence. Instead it will state two conditional hypotheses: a bad route has at least 2% failure probability at every scheduled trial given the entire past; a good route has at most 0.5% at every trial given the entire past. Sequential coupling then makes the binomial bad/good tails conservative without requiring marginal independence. A frozen randomized, time-stratified schedule defines what route and operating window the claim applies to. Council must attack this redesign before any route call is authorized.

## Retain, replace, delete

Retain: three-stage stop order, single-writer scope, strict shared schema ingress, independent post-ingress reducers, bitemporal visibility dimensions, action/catalog hashing, fixed 65,536-byte envelope, the H-D-F cell grid, separated boundedness/affordability gates, exact missing-completion DP, Proposition 3.1 ruler, explicit indifference region, full-route qualification unit, and no-paid-first workflow.

Replace: r9 runtime inheritance, component-only packet scoring, version-hard-coded selector helpers, prose-only physical accounting, label-only ledger durability, region-wide power language, marginal-iid route language, host-bound Ajv resolution and working-tree-first bootstrap.

Delete: the r10 runtime dependency on `mbcx01_r9_reference.py` and `mbcx01_r9_oracle.py`. Historical files remain in Git for audit but are not r11 runtime subjects.

## r11 acceptance condition

r11 is ready for another council round only when its pinned reconstruction executes the r10 counterexamples as red witnesses, all retained green invariants still pass, no r9 Python module is imported, the validator runtime is reconstructed from governed bytes, the repair ledger has no unexercised entry, and the packet can be generated and tested without dispatching or making a provider/model call.

