# MBCX-01 CLOSURE COUNCIL PACKET r13

## 0. Seat command and immutable bundle

You are one Moonwalker design-council seat reviewing the final no-paid closure fold for an internal scientific instrument. You are not running the experiment and you are not reviewing a finished production harness. Read the complete role card at `<vault>` and adjudicate repository `<repo>`.

The governing subjects are frozen at Git commit `ec583834e08df77b65ca773ef6fdf525b0ee51b2`. The pin manifest is Git blob `d71e653d95df662097d2507299fd85ff265ed856`. The reconstruction launcher is Git blob `ba046408a0a210176d6d53616a8535eb26542be4`.

Do not trust or execute the working-tree launcher first. Extract the launcher from its pinned blob, verify its blob ID, and execute that copy:

```powershell
$repo = (git rev-parse --show-toplevel).Trim()
$launcher = Join-Path ([IO.Path]::GetTempPath()) 'verify-r13-pinned.ps1'
$p = Start-Process -FilePath 'git' -ArgumentList @('-C',$repo,'cat-file','blob','ba046408a0a210176d6d53616a8535eb26542be4') -RedirectStandardOutput $launcher -PassThru -Wait -WindowStyle Hidden
if ($p.ExitCode -ne 0) { throw 'launcher extraction failed' }
if ((git hash-object -- $launcher).Trim() -ne 'ba046408a0a210176d6d53616a8535eb26542be4') { throw 'launcher blob mismatch' }
powershell -NoProfile -ExecutionPolicy Bypass -File $launcher -Commit ec583834e08df77b65ca773ef6fdf525b0ee51b2 -ManifestBlob d71e653d95df662097d2507299fd85ff265ed856
```

The manifest lists 31 exact normative subjects. A clean pinned reconstruction passed before packet assembly: 132 unit tests, strict Draft 2020-12 Ajv compilation/adversarial admission, 50 named repair witnesses with two-way ledger coverage, seven joined pipeline stages, and the frozen 10,000-replicate pointwise planning diagnostic. The diagnostic is deterministic planning evidence, not experiment evidence.

Read at minimum:

- `MBCX-01-COUNCIL-R12-SYNTHESIS-AND-CLOSURE-COMMISSION.md`
- `MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md`
- `MBCX-01-R13-CLOSURE-ARCHITECTURE.md`
- `MBCX-01-R13-PRIOR-ART-AND-ENVIRONMENT-ADDENDUM.md`
- `MBCX-01-R13-PHYSICAL-HARNESS-REQUIREMENTS.md`
- the four current contracts, generator artifact, trust-root manifest and repair ledger
- all seven `mbcx01_r13_*.py` modules and five r13 test modules
- both JavaScript verifiers, the vendored Ajv runtime, normative verifier and pinned launcher

Maintain a lateral seal. Do not inspect another seat's r13 browser output, Codex log, completion marker or verdict before producing yours. Claude, ChatGPT and Codex EXEC are longitudinal seats; your own retained lane context is permitted and must be labeled. The owner/ChatGPT follow-up summarized in the pinned synthesis is governing process context: this is one bounded closure review, not an invitation to restart unconstrained conceptual design.

**Do not edit files. Do not run the scientific experiment. Do not build or run either production adapter or the physical harness. Do not execute FD/FC/TN candidates. Do not qualify routes. Do not call any provider/model or make paid calls.** Execute only deterministic, read-only, no-paid attacks on the pinned bytes.

## 1. The decision in plain language

The original question remains whether exact due-obligation continuity can be physically bounded, which implementation mechanisms survive fairly, and whether bounded-context continuity performs acceptably against an independently built oracle-minimal baseline.

Round 13 does not claim those questions have been answered. It claims the paper design and no-paid conformance implementation now define one mechanically joined world, while refusing to produce scientific eligibility until two external production artifacts exist and pass separate BUILD review:

1. an independent production state-authority adapter/store/readback receipt; and
2. a production Windows Job Object/ETW PMC physical harness and signer custody path.

The current top-level readiness is deliberately `DESIGN_OR_IMPLEMENTATION_FAIL` with `STATE_AUTHORITY_UNAVAILABLE` and `PHYSICAL_HARNESS_UNAVAILABLE`. Fixture conformance can score 1; scientific admission must score 0. A council GO authorizes only the next, separately reviewed BUILD gates. It does not authorize the experiment, model/provider calls, route qualification, physical trials or spending.

## 2. Verdict meanings — owner-locked for this closure review

- `GO`: all closure invariants hold and the bounded design is ready to advance to separately reviewed production-adapter and physical-harness BUILD gates.
- `GO-WITH-FIXES(reason)`: a bounded local no-paid repair remains. It does not change the estimand, architecture, sample size, inference rule, authority model or experiment stages; name the exact witness and fix class.
- `NO-GO(reason)`: a core redesign is required, or a reachable false result, invalid inference, unbounded authority gap, unreconstructable evidence path or practical inability to answer remains after the proposed BUILD artifacts exist.

Do not return NO-GO merely because the two production BUILD artifacts honestly do not yet exist. Do return NO-GO if their published interfaces cannot, even in principle, provide the authority/evidence the experiment would require. Do not invent a fourth verdict.

## 3. What changed after the r12 council and owner/ChatGPT follow-up

The repair method changed from finding-by-finding patching to an authority-invariant matrix. For every place the same claimed fact appears in two representations, r13 names the authoritative producer, the exact bytes/digest/foreign key that must cross the boundary, a positive witness, and an adversarial witness where two individually valid objects disagree. Any disagreement that is accepted is a defect.

The most important changes are:

- Cohort authority is independently derived from the retained candidate and must match the manifest's scenario, scope, cut, gold action and complete legal action universe.
- The manifest binds exact authoritative prestate. A0, TaskPacket, B, the durable call ledger, persisted proposal, committed event, poststate, WriterReceipt and A1 are one causal graph.
- A1 is projected from the authoritative poststate and exact postcommit cut, not from a manifest-authored parallel world.
- The same canonical durability receipt and handoff-bound identity is used by state, packets and `CallLedgerV3`.
- `EpisodeReceiptV1` contains exactly six terminal call ledgers. Terminal ambiguous acceptance makes the whole BC/OM pair missing; inference derives the partition and offers no caller-supplied missing-ID input.
- Physical evidence has a closed signed nested envelope. The evaluator decodes and checks raw Job Basic/I/O/Extended query evidence, PID/start-key membership, completion/loss, external enforcement, ETW attribution, environment and harness identity. Aggregate user+kernel CPU H-shape and absolute gates are restored alongside I/O gates.
- The fixture trust root is bound to role, policy, subject and environment, remains `production_ready:false`, and has no authority-retirement shortcut. Its key cannot authenticate a physical receipt.
- A `StateAuthorityReceiptV1` proves exact dual-reducer fixture conformance but is explicitly fixture-only. Production verification fails loud because no independent state root/adapter exists yet.
- Reference and oracle now independently own replay, event persistence, next sequence, observation watermark and finalization semantics; poison tests make each implementation load-bearing.
- Hard engineering gates precede a complete nondominated Pareto set. Carrier preference is a separate owner choice and cannot silently become a mechanism result.
- Static r12 verification output is nonnormative. R13 status is produced live from authenticated subjects.

The scientific n=768 rule, six calls per episode, 456/4 conditional-hazard route qualification, published r10 counterexample, pointwise planning interpretation, exact missing-data analysis and owner-locked estimands are unchanged.

## 4. Authority and non-claims

A digest proves byte integrity, not external truth. A fixture key proves test plumbing, not an OS observation. Two software reducers agreeing proves conformance to their pinned transition contract, not that an external store committed anything. A self-consistent manifest is not allowed to define the state, population or result that it claims to measure.

`FIXTURE_ONLY` artifacts may exercise the full graph and prove that disagreements are rejected. They can never create experiment eligibility. `PRODUCTION` admission requires an independently operated state store/adapter and production physical harness whose receipts satisfy the published contracts and later BUILD review.

The packet does not claim that signatures make evidence true, that PMU counters are universally comparable, that nested virtualization is supported, that 10,000 diagnostic replicates prove power over a region, that route trials are iid, or that paying for more calls repairs a design/authority failure.

Supported retired-instruction environments are bare metal or the Hyper-V root partition with the required host controls, plus an explicitly enabled nonnested guest PMU path. Nested virtualization is unsupported. Cross-hardware migration/save-restore is outside the claim.

## 5. Invariant scoreboard under review

Return `HOLDS`, `FALSE` or `UNDERDETERMINED` for every row and cite the exact executed/read evidence.

1. **I01 cohort → manifest:** exact scenario/scope/cut/gold/full action universe and retained SHA-256 order.
2. **I02 manifest → authoritative prestate:** exact cut, canonical state bytes/hash and resolved world truth.
3. **I03 A0 → manifest:** exact route, model, context, input and declared prestate world.
4. **I04 TaskPacket → A0:** exact rendered request bytes/hash, scope, cut, context and full catalog.
5. **I05 B → durable ledger:** exact handoff/call identity, raw response, response/provider/transaction IDs and canonical durability receipt.
6. **I06 proposal → persisted prestate journal:** exact full proposal event bytes/hash/event ID and next journal sequence.
7. **I07 commit → proposal/prestate:** exact target/action legality plus unchanged prerequisite/target state at commit.
8. **I08 poststate → WriterReceipt:** exact applied child, canonical poststate bytes/hash, postcommit cut and durable authority receipt readback.
9. **I09 poststate → A1:** A1 is recomputed from authoritative poststate and exact postcommit cut.
10. **I10 six ledgers → inference partition:** exactly A0/B/A1 × BC/OM; terminal ambiguity means whole-pair missing; no substitution or caller partition.
11. **I11 physical requirements → schema:** every load-bearing Job/ETW/environment/containment/signing claim is machine-representable.
12. **I12 schema → evaluator:** every promised field and CPU/I/O/PMC/containment gate changes admission when mutated.
13. **I13 signed receipt → trust root:** key role, policy, subject, environment, algorithm and run/cell identity are external to and exact with the signed envelope.
14. **I14 state receipt → authority:** fixture conformance is exact; production authority remains unavailable until an external adapter/store/root exists.
15. **I15 reducer independence:** shared code ends at structural/hash admission; both engines independently own result-producing semantics.
16. **I16 physical survivors → engineering result:** hard gates first, complete Pareto set second, owner preference third.
17. **I17 authenticated run → report:** live result derives from the pinned reconstruction; stale static reports cannot govern.

## 6. Required executable attacks

Execute all attacks that remain within the no-paid/read-only boundary.

- **A — pins/reconstruction:** authenticate the launcher; reconstruct 31 subjects; check object, byte, LF, line and SHA-384 pins; run the verifier; attack omission/substitution/line-ending/worktree drift.
- **B — valid-vs-valid disagreement:** for I01–I17, attempt at least one fresh case where each side is locally valid and self-consistent but they disagree. A hash-only mutation is not enough.
- **C — world/transition graph:** substitute cohort authority, full catalog, prestate/cut, A0/TaskPacket, B ledger, proposal, commit, child, poststate/readback, WriterReceipt or A1 while repairing descendant hashes. Confirm the first wrong edge fails.
- **D — authority modes:** try to promote fixture state or measurement receipts to production by changing labels, roots, policies, subjects, environments or signatures. Confirm scientific score remains 0 and physical evidence unavailable.
- **E — reducer independence:** poison shared and opposite-engine replay/finalization names; show each engine changes when its own logic is poisoned and does not change when the other is poisoned.
- **F — measurement/episode:** remove or replace nested evidence; attack aggregate CPU H-shape, I/O, PMC mode/loss, completion, attribution, containment, mixed grid/run and trust-root identity. Attempt retry/outgoing transition after ambiguous acceptance and attempt pair substitution at inference.
- **G — math/cost:** reproduce exact route tails and one exact interval; compare missing DP to the small exhaustive oracle; run the registered m=20 spot check; reproduce all five pointwise planning cells including `(0,.3,.1,.6)`. State what 768 pairs, 4,608 calls and 456 route trials buy—and what more money cannot buy.
- **H — build/omission:** do a current primary-source web sweep and an internal-shelf spot-run. Name `NONE — ALL LOAD-BEARING` or one removable artifact/stage. Name the smallest production state-adapter BUILD artifact, smallest physical-harness BUILD artifact, and any remaining no-paid witness.

## 7. Focused questions

Answer `HELPFUL`, `NOT HELPFUL` or `HELPFUL WITH A NAMED FIX`.

1. Is the 17-row authority matrix an adequate closure method, or can two valid representations still disagree without rejection?
2. Does independently deriving cohort authority from retained candidates prevent circular manifest self-authorship?
3. Is fixture conformance 1 / scientific admission 0 the correct boundary until an external state adapter exists?
4. Is the proposed state-authority adapter/store/readback interface sufficiently specified to move into a separate BUILD gate, or is a design element still missing?
5. Is the signed nested physical envelope plus exact Windows environment contract sufficiently specified to move into a separate BUILD gate?
6. Are aggregate user+kernel CPU, total I/O bytes/operations, exact PMU attribution and hard supported-environment rules proportionate to the physical claim?
7. Is terminal acceptance ambiguity → whole-pair missing the correct conservative join into inference?
8. Do hard gates → complete Pareto set → owner selection prevent engineering preference from contaminating the scientific result?
9. Is any remaining issue truly a conceptual redesign under §2, or is it a bounded build/local-fix item?
10. If the closure holds, should numbered conceptual design rounds stop and the two separately reviewed BUILD gates begin?

## 8. Required verdict

Return one self-contained in-thread report containing:

1. the exact top-level verdict under §2;
2. seat identity/model/checkpoint/harness and longitudinal posture;
3. pin/reconstruction result;
4. evidence separated as `EXECUTED`, `READ-ONLY`, `SEARCHED`, `RECALLED` and `UNSEARCHED`;
5. applicability, exclusions and non-claims;
6. I01–I17 scoreboard;
7. P0–P3 findings with exact location, reachable false-result or indecision path, smallest repair and evidence;
8. attacks A–H with input/method/output/interpretation/limitation;
9. ten focused-question answers;
10. `WHAT WOULD YOU BUILD?` and `WOULD YOU DESIGN IT DIFFERENTLY?`;
11. a plain-language owner section explaining whether the design can answer the question after the two BUILD prerequisites, why it is red today, what paying for 4,608 calls plus route trials buys, and what extra spending would not fix;
12. external primary-source and internal-shelf sweep logs, omission/bypass attack, residual risks, seal/capability/side-effect/cleanup report, and paid inference `NONE`.

No vague “more research” blocker. Name the missing byte, field, formula, trace, receipt, premise, alternative, implementation or cost. A preferred method is not a blocker without a reachable false result, invalid authority path or avoidable practical indecision. Do not broaden this closure review into a new conceptual round unless you can show why the owner-locked NO-GO threshold is met.
