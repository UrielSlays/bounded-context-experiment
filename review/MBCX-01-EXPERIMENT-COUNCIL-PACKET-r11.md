# MBCX-01 EXPERIMENT COUNCIL PACKET r11

## 0. Seat command and immutable bundle

You are one Moonwalker design-council seat reviewing an internal scientific instrument, not a production system. Read the complete role card at `<vault>` and adjudicate the repository `<repo>`.

The governing subjects are frozen at Git commit `b56e450f8553b96f6121cb045b62eb604e4a0655`. The owner-pinned manifest is Git blob `269dbb3fd905c3875616ac70434e333bcede0a1b`. The reconstruction launcher is Git blob `dca3d7951aeba3947af18978b88cc48028c1b572`.

Do not trust or execute the working-tree launcher first. Extract the launcher from its pinned blob, verify the extracted blob ID, and execute that copy:

```powershell
$repo = (git rev-parse --show-toplevel).Trim()
$launcher = Join-Path ([IO.Path]::GetTempPath()) 'verify-r11-pinned.ps1'
$p = Start-Process -FilePath 'git' -ArgumentList @('-C',$repo,'cat-file','blob','dca3d7951aeba3947af18978b88cc48028c1b572') -RedirectStandardOutput $launcher -PassThru -Wait -WindowStyle Hidden
if ($p.ExitCode -ne 0) { throw 'launcher extraction failed' }
if ((git hash-object -- $launcher).Trim() -ne 'dca3d7951aeba3947af18978b88cc48028c1b572') { throw 'launcher blob mismatch' }
powershell -NoProfile -ExecutionPolicy Bypass -File $launcher -Commit b56e450f8553b96f6121cb045b62eb604e4a0655 -ManifestBlob 269dbb3fd905c3875616ac70434e333bcede0a1b
```

The manifest lists 31 exact subjects with Git blob, bytes, lines, LF count and SHA-384. The pinned reconstruction was executed before packet assembly and reported state, packets, cohort, measurement verification, inference, pipeline and repair-ledger integration PASS. Its top-level readiness remains deliberately `DESIGN_OR_IMPLEMENTATION_FAIL` because `PHYSICAL_HARNESS_UNAVAILABLE`; a synthetic measurement fixture cannot turn that prerequisite green.

Read at minimum:

- `MBCX-01-COUNCIL-R10-SYNTHESIS-AND-DISPOSITION.md`
- `MBCX-01-R11-ARCHITECTURE-SPEC.md`
- `MBCX-01-R11-PRIOR-ART-MEMO.md`
- `MBCX-01-R11-PHYSICAL-HARNESS-REQUIREMENTS.md`
- all four r11 contracts
- all seven `mbcx01_r11_*.py` modules
- all five r11 test modules
- `verify-r11-normative-bundle.py`
- `verify-r11-schema-ajv.mjs`
- `verify-r11-pinned.ps1`
- `MBCX-01-R11-REPAIR-LEDGER.json`
- `MBCX-01-R11-NO-PAID-VERIFICATION.json`

The r10 verdicts are historical evidence only. Maintain the current-round lateral seal: do not inspect another seat's r11 answer, current browser output, logs, marker or verdict before producing yours. Claude and ChatGPT are retained longitudinal seats; Codex EXEC is the fresh read-only seat. Do not edit files, implement FD/FC/TN, build the physical harness, run a provider/model/route soak, or make paid calls.

## 1. Question that must be answered

If the governing design is implemented literally—including the named physical-harness prerequisite—does it now have a fair and affordable chance to answer:

1. whether exact due-obligation continuity remains physically bounded over every frozen `H,D,F` cell;
2. which of FD, FC or TN survives exactness and forms the defensible engineering Pareto set, with carrier preference separately labeled; and
3. whether one frozen model can use bounded-context BC without materially underperforming independently built oracle-minimal OM in a cold serial `A0 → B → writer → A1` episode?

A future falsification is an answer. A design that predictably returns practical indecision is not. Exact thresholds and the explicitly frozen transition region may remain inconclusive.

This round adjudicates the instrument and the next no-model engineering gate. It does **not** claim the current repository is ready for paid scientific calls. Verdict meanings:

- `GO`: the design and current no-paid implementation close the false-result paths, and the named physical harness may be built and validated next; paid/model/provider calls remain forbidden.
- `GO-WITH-FIXES(reason)`: a bounded no-paid repair is required before that harness work.
- `NO-GO(reason)`: a reachable false result, invalid inference, unreconstructable evidence, or avoidable practical indecision remains in the core design.

Do not return NO-GO merely because the packet loudly reports its unimplemented physical harness. Do return NO-GO if the proposed harness contract cannot, even when implemented, support the claim or if any synthetic/self-authored evidence can bypass the closed gate.

## 2. Round-10 blockers and r11 repairs under attack

| r10 blocker | r11 mechanism to attack |
|---|---|
| Historical reducers shared broken semantics | r11-owned reference and independently structured oracle, sharing only structural ingress; canonical event IDs; exact current journal/knowledge cuts; append-only bitemporal closure/retraction. |
| Facts could overlap, invert or rewrite history | Half-open nonempty intervals; explicit upper bounds are never silently truncated; future/retracted versions receive dedicated witnesses. |
| Global/unbound responses authorized commits | Exact open-handoff B foreign key; raw WorkerHandoff bytes; scope, manifest, action, time, request and route binding; globally unique response/provider/transaction identities. |
| Reject/commit paths lacked causal proof | Proposal hash is stored from the exact proposal event; commit and rejection require the corresponding persisted proposal and recheck current state. |
| Packet scorer accepted forged or collapsed A0/B/A1 worlds | Typed DAG with exact served bytes, node-unique identities, one canonical durability receipt, exact applied state commit event and A1 postcommit cut. |
| State adapter silently reduced the action catalog | `open_handoff` carries canonical TaskPacket and manifest preimages and independently recomputes both hashes; TaskPacket, manifest and state must bind the same full catalog bytes. |
| Cohort domains/authority drifted | Selector has no domain override; contract owns both domains; a pinned generator artifact digest plus complete cut/state/gold/action authority controls selection and final SHA-256 scenario order. |
| Physical measurement could be self-authored | Synthetic rows now always report `PHYSICAL_HARNESS_UNAVAILABLE`; a separately governed Windows Job Object/ETW harness plus external signing trust root is mandatory. |
| Call durability differed across components | Packet, state and restart ledger consume the same `DurabilityReceiptV1` bytes and complete identity preimage. Ambiguous retry requires exact route attestation; label-only preaccept proof never authorizes retry. |
| Missingness could substitute/order-poison data | Complete and missing paths consume the exact frozen scenario order; Boolean outcomes and truthy non-Boolean design gates are rejected. |
| Region-wide 90% power promise was false | n remains 768; outputs are deterministic pointwise planning frequencies for complete registered joint cells only. The r10 counterexample remains published at about 70.68% interface-fail frequency. |
| 456/4 relied on an unstated iid premise | Full-past conditional-hazard hypotheses plus finite-horizon conditional-expectation recursion; no iid or marginal-only claim. |
| Validator/bootstrap/repair tracking were incomplete | Vendored Ajv with calendar-valid UTC, authenticated launcher-before-execution, exact subject set, and two-way executed-witness ↔ repair-ledger coverage. |

Do not accept the table as evidence. Attack the reconstructed bytes.

## 3. Known boundary and cost decision

The current bundle truthfully stops before physical measurement. `baseline_receipt_rows()` is an evaluator fixture, not OS evidence. The required future harness must create the root suspended, assign it to a no-breakaway Job Object before resume, use a completion port, wait for active-process-zero, drain completion, query final job accounting, collect root-plus-descendant CPU/I/O/memory/elapsed and pinned retired-instruction evidence, deny external compute, and produce receipts signed by a key unavailable to the candidate/evaluator.

The scientific run remains 768 paired scenarios / 4,608 scheduled logical model-call positions. Paying for 1,152 pairs would not repair identity, measurement, missingness or the false region-wide promise; it would only change precision and pointwise planning behavior.

Route qualification remains 456 complete six-call trials / 2,736 scheduled positions, accept at most four failures. Under the bad-route hypothesis `P(F_i=1 | entire observed past) ≥ .02` at every history, bad-route acceptance is at most `0.049433329807588314`. Under the good-route hypothesis `P(F_i=1 | entire observed past) ≤ .005`, good-route acceptance is at least `0.9190668746549462`, hence rejection at most `0.08093312534505381`. An abort, incomplete or unclassified launched trial is a failure; no replacement or early acceptance; fifth failure may reject. No guarantee applies when conditional hazards cross or lie between those bounds.

## 4. Claims C1–C12

Return `HOLDS`, `FALSE` or `UNDERDETERMINED` for each.

1. **C1 — decomposition:** continuity, FD/FC/TN engineering, carrier preference and conditional model usability remain separate decisions; controls may win.
2. **C2 — state totality:** exact cuts, canonical IDs, append-only temporal evidence, lifecycle guards and independent reducers yield one answer without exceptions for every admitted event.
3. **C3 — response/proposal integrity:** no cross-scope, pre-open, duplicate, aliased, stale, replayed or worker-substituted response can authorize commit/rejection.
4. **C4 — packet/DAG validity:** manifest → A0 → TaskPacket/B → exact state commit → postcommit A1 is one causal byte graph, including one durability schema and full catalog.
5. **C5 — cohort authority:** pinned generator content, contract-owned domains, complete cut/state/gold/action authority and frozen order define exactly 768 retained scenarios.
6. **C6 — physical claim honesty:** no synthetic receipt can create a physical pass, and the external harness contract is sufficient in principle for the finite 100-cell claim.
7. **C7 — recovery totality:** restart validation and route-attested ambiguous retry cannot silently duplicate or substitute a logical call.
8. **C8 — serial outcome totality:** a complete episode yields one exact pair; absent outcomes remain explicit missing IDs without population substitution.
9. **C9 — engineering fairness:** exactness filtering/Pareto analysis cannot turn carrier preference into a mechanism result.
10. **C10 — inference:** the exact-mixture implementation, missing-completion DP, alpha allocation, strict thresholds and fixed kappa support the registered average-conditional-mean estimands.
11. **C11 — planning/reliability/cost:** pointwise 10,000-replicate diagnostics and the conditional-hazard 456/4 route gate are stated no more broadly than proved, and cost units are knowable before authorization.
12. **C12 — smallest decisive instrument:** every retained stage can change a primary result; the physical harness is the only declared blocking implementation prerequisite.

## 5. Required executable attacks

Execute everything your environment permits without model/provider calls or fabricated carrier results.

- **A — pin/reconstruction:** authenticate and extract the launcher blob before execution; verify governing commit, manifest blob, exact subject set, every blob/byte/LF/line/SHA-384 pin, vendored Ajv closure and reconstructed verifier. Attack working-tree, line-ending, manifest-omission and launcher-substitution paths.
- **B — state/time:** mutate explicit intervals, old cuts after late observations, future/retracted versions, response logical IDs with same and different bytes, worker scope/action/manifest/times, target/catalog binding, arbitrary rejection hashes and stale commit state. Differentially exercise both reducers.
- **C — causal graph:** attempt a self-consistent reduced catalog, TaskPacket/manifest substitution, cross-scenario response, duplicate transaction, packet durability receipt through restart ledger, invented WriterReceipt child, precommit A1 cut and A1-before-commit time.
- **D — cohort/population:** alter contract domains, generator bytes/digest, motif, cuts, canonical state, gold/action authority, eligibility and retained order. Verify exactly six motifs × 128 and identity-preserving missingness.
- **E — physical/ledger:** prove synthetic receipts cannot pass; attack Boolean axes, candidate mixing, missing I/O/completion/descendants/external-work accounting, corrupt recovery and label-only retry evidence. Then judge whether the specified future Job/ETW/signature harness is sufficient or overbuilt.
- **F — inference:** independently compare missing DP with enumeration on small arbitrary positions; poison outcomes with Booleans; reproduce at least one interval and all route-tail numbers. Audit the conditional-expectation recursion rather than assuming iid.
- **G — planning/cost:** reproduce the five pointwise deterministic frequencies, especially `(0,.3,.1,.6)`; verify no true-probability or rectangular-region guarantee is implied. Explain what 768 pairs, 456 route trials and paying more each buy.
- **H — deletion/boundary:** name one artifact/stage to remove or `NONE — ALL LOAD-BEARING`; name one no-paid test still missing; name the exact next physical-harness gate and the boundary to the later coordination experiment.

## 6. Open questions

Answer each `HELPFUL`, `NOT HELPFUL` or `HELPFUL WITH A NAMED FIX`.

1. Is independent post-ingress state logic with shared structural validation the right independence boundary?
2. Do exact current cuts and append-only closure/retraction fully support this single-writer experiment?
3. Does carrying canonical manifest/TaskPacket preimages close the full-catalog and response-identity seam without unnecessary duplication?
4. Is one shared durability receipt across packet/state/restart ledger sufficient for the serial crash model?
5. Is the proposed Windows Job Object + completion port + ETW instruction + external signature harness sufficient and proportionate?
6. Is n=768 defensible after narrowing assurance to explicit joint cells and publishing the failed counterexample?
7. Is the 456/4 conditional-hazard route contract mathematically valid and operationally testable as worded?
8. Is `DESIGN_OR_IMPLEMENTATION_FAIL` the correct current top-level status while the physical harness is absent, even if the design itself merits GO to the next engineering gate?

## 7. Required verdict

Return one self-contained report containing:

1. `GO`, `GO-WITH-FIXES(reason)` or `NO-GO(reason)` under the meanings in §1.
2. Seat identity, model/checkpoint, harness and longitudinal/fresh posture.
3. Governing commit, manifest blob, launcher blob and reconstruction verification.
4. Evidence separated as EXECUTED, READ-ONLY, SEARCHED and UNSEARCHED.
5. Applicability and explicit exclusions.
6. C1–C12 scoreboard.
7. Findings P0–P3 with exact location, false-result/avoidable-indecision path, smallest repair and evidence.
8. Attacks A–H with input, method, output, interpretation and limitation.
9. Eight open-question labels/answers.
10. `WHAT WOULD YOU BUILD?`
11. `WOULD YOU DESIGN IT DIFFERENTLY?`
12. Plain-language paragraphs for the owner: can the experiment answer its question if the harness is built; what 768 pairs/4,608 positions buy; what 456 trials/2,736 positions buy; what paying more would and would not buy; why the present red top-level status is honest rather than failure of the research question.
13. Prior-art sweep log with exact queries and opened primary sources/sections, omission/bypass attack, residual risks, non-claims, capability/lateral-seal report, paid inference NONE, side effects and cleanup.

No vague “more research” blocker. Name the missing byte, formula, trace, receipt, premise, alternative, plan or cost. A preferred method is not a blocker without a reachable false-result or avoidable practical-indecision path.
