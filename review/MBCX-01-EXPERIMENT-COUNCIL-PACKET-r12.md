# MBCX-01 EXPERIMENT COUNCIL PACKET r12

## 0. Seat command and immutable bundle

You are one Moonwalker design-council seat reviewing an internal scientific instrument, not running the experiment. Read the complete role card at `<vault>` and adjudicate repository `<repo>`.

The governing subjects are frozen at Git commit `235f37bcbf213e6700c30333d6fee6a68f0886b6`. The owner-pinned manifest is Git blob `bd84a65b7b85530345a82a552d7c47f9e148f1a7`. The reconstruction launcher is Git blob `2b575b10f3c00c7a3ac79a39e54693104443f330`.

Do not trust or execute the working-tree launcher first. Extract the launcher from its pinned blob, verify its blob ID, and execute that copy:

```powershell
$repo = (git rev-parse --show-toplevel).Trim()
$launcher = Join-Path ([IO.Path]::GetTempPath()) 'verify-r12-pinned.ps1'
$p = Start-Process -FilePath 'git' -ArgumentList @('-C',$repo,'cat-file','blob','2b575b10f3c00c7a3ac79a39e54693104443f330') -RedirectStandardOutput $launcher -PassThru -Wait -WindowStyle Hidden
if ($p.ExitCode -ne 0) { throw 'launcher extraction failed' }
if ((git hash-object -- $launcher).Trim() -ne '2b575b10f3c00c7a3ac79a39e54693104443f330') { throw 'launcher blob mismatch' }
powershell -NoProfile -ExecutionPolicy Bypass -File $launcher -Commit 235f37bcbf213e6700c30333d6fee6a68f0886b6 -ManifestBlob bd84a65b7b85530345a82a552d7c47f9e148f1a7
```

The manifest lists 31 exact normative subjects. The implementation plan and prior council verdicts remain Git history, not experiment law. The pinned reconstruction was executed before packet assembly and reported state, packets, cohort, measurement verification, inference, pipeline and repair-ledger integration PASS. It ran 87 named unit witnesses plus strict Ajv fixture/mutant admission and the frozen 10,000-stream pointwise planning diagnostics. Its top-level readiness deliberately remains `DESIGN_OR_IMPLEMENTATION_FAIL` because `PHYSICAL_HARNESS_UNAVAILABLE`.

Read at minimum:

- `MBCX-01-COUNCIL-R11-SYNTHESIS-AND-DISPOSITION.md`
- `MBCX-01-R12-ARCHITECTURE-SPEC.md`
- `MBCX-01-R12-PRIOR-ART-AND-SHELF-MEMO.md`
- `MBCX-01-R12-PHYSICAL-HARNESS-REQUIREMENTS.md`
- all four current contracts and both r12 generator/trust-root manifests
- all seven `mbcx01_r12_*.py` modules
- all five r12 test modules
- both JavaScript verifiers and the vendored Ajv runtime
- `verify-r12-normative-bundle.py`, `verify-r12-pinned.ps1`
- `MBCX-01-R12-REPAIR-LEDGER.json`
- `MBCX-01-R12-NO-PAID-VERIFICATION.json`

Maintain the current-round lateral seal: do not inspect another seat's r12 browser output, Codex log/marker or verdict before producing yours. The r11 ChatGPT seat disclosed a procedural prior-round breach: one broad shelf grep incidentally returned non-substantive fragments of the r11 Codex role-card text, but no technical finding or verdict. Treat that disclosure as historical process evidence, not as a current-round output. Claude, ChatGPT and Codex EXEC are the same longitudinal seats; retained own-lane context is permitted and must be labeled.

**Do not edit files. Do not run the scientific experiment. Do not build or run the physical harness. Do not execute FD/FC/TN candidates. Do not run route qualification. Do not call any provider/model or make paid calls.** Execute only deterministic/no-paid attacks on the pinned bytes.

## 1. Question and verdict meanings

If implemented literally, including the named future physical-harness prerequisite, does this design have a fair and affordable chance to answer:

1. whether exact due-obligation continuity remains physically bounded over every frozen H-D-F cell;
2. which of FD, FC or TN survives exactness and forms the defensible engineering Pareto set, with carrier preference separately labeled; and
3. whether one frozen model can use bounded-context BC without materially underperforming independently built oracle-minimal OM in a cold serial A0 → B → writer → A1 episode?

A future falsification is an answer. A design that predictably returns practical indecision is not. Exact thresholds and the explicitly frozen transition region may remain inconclusive.

- `GO`: the design and no-paid implementation close reachable false-result paths; the separately reviewed physical-harness BUILD gate may begin, but the experiment and all paid/model/provider/route calls remain forbidden.
- `GO-WITH-FIXES(reason)`: one bounded no-paid repair is required before that BUILD gate.
- `NO-GO(reason)`: a reachable false result, invalid inference, unreconstructable authority/evidence or avoidable practical indecision remains in the core design.

Do not return NO-GO merely because the bundle honestly reports an unimplemented physical harness. Do return NO-GO if the proposed machine contract could accept invented authority/evidence after the sentinel is retired.

## 2. Round-11 failures and r12 repairs under attack

| r11 controlling finding | r12 mechanism to attack |
|---|---|
| WriterReceipt proved canonical bytes, not actual application | `TransitionAuthorityV1` carries exact authoritative precommit state/cut/digest and exact persisted proposal bytes/hash. Scoring applies the exact child independently through both state engines, requires both `APPLIED`, canonical identical poststate, exact next sequence/effective time and exact receipt/A1 postcommit state/cut. |
| Ambiguous acceptance could self-authorize retry | `ACCEPTANCE_AMBIGUOUS` is terminal whole-pair missing. There is no retry edge and runtime `RouteAttestationV1` has no authority. |
| Physical signature was prose-only and schema-invalid | Closed `SignedMeasurementReceiptV1` schema; domain/version/Ed25519/key/run/cell/fixture/payload signed preimage; separate closed trust-root manifest; verify-only Node boundary; test key is fixture-only and cannot authenticate `PHYSICAL_HARNESS_RECEIPT`. |
| Physical isolation/PMC/I/O contract was incomplete | Exact event-attached InstructionRetired/CSwitch mode, start-key/job-member attribution, zero loss/multiplexing/conflict, separate final Job Basic+I/O and Extended-Limit evidence, enforced external-work boundary, and H-shape gates for total I/O bytes/operations. Unsupported evidence fails loud. |
| “Independent” state oracle shared semantic helpers | Shared module retains structural/hash admission only. Reference and oracle separately own temporal visibility/closure, dependency reachability, action legality and effects. A poison witness attacks the boundary plus a complete 17-event legal matrix. |
| Internal shelf log missing | Exact queries, files and adopt/why-not dispositions are published. Photon supplies terminal ambiguity; Gravity supplies an Ed25519 verification/test shape; existing Job Object code is scaffolding only, not claimed evidence. |
| DP certification lived only at small missing counts | Small-m exhaustive oracle retained; deterministic 128-completion property check added at m=20 and explicitly labeled non-exhaustive. |

The scientific n=768 rule, published r10 counterexample, pointwise planning language and 456/4 conditional-hazard route theorem are unchanged.

## 3. Authority rule and known boundary

The round's governing distinction is: **a hash proves internal integrity, not external authority**. Attack every place where self-consistent bytes might still substitute for the state machine, provider, OS/supervisor, signer or frozen population.

The repository does not contain a production signing key or the Windows physical harness. The trust-root manifest is `production_ready:false`; its only key is fixture-only. Even a correctly signed test envelope must report `PHYSICAL_HARNESS_UNAVAILABLE`. The next gate after a council GO is a separate BUILD-class review of the actual harness, containment/egress enforcement and signer custody.

## 4. Claims C1–C12

Return `HOLDS`, `FALSE` or `UNDERDETERMINED` for each.

1. **C1 decomposition:** continuity, FD/FC/TN engineering, carrier preference and model usability remain separate decisions; controls may win.
2. **C2 state totality:** exact cuts, append-only temporal evidence, lifecycle guards and genuinely independent post-ingress reducers give one result for every admitted event.
3. **C3 response/proposal integrity:** no scope/action/manifest/time/reference/transaction replay or substitution can authorize proposal/commit/reject.
4. **C4 packet/application validity:** manifest → A0 → TaskPacket/B → exact persisted proposal → dual-reducer applied commit → exact postcommit A1 is one causal byte graph.
5. **C5 cohort authority:** current generator content, contract domains, full cut/state/gold/action authority and SHA-256 order define exactly 768 scenarios.
6. **C6 physical claim honesty:** signed envelope/trust-root/containment/PMC/I/O contracts cannot be bypassed by synthetic or self-authored receipts and are sufficient in principle for the finite claim.
7. **C7 recovery totality:** durable recovery cannot duplicate/substitute a call, and ambiguous acceptance remains explicit missing with no retry.
8. **C8 serial outcome totality:** a completed episode yields one exact pair; missing outcomes retain frozen IDs without replacement.
9. **C9 engineering fairness:** exactness/Pareto analysis cannot turn carrier preference into a mechanism result.
10. **C10 inference:** exact-mixture intervals, exact arbitrary-position missing DP, type guards, alpha allocation and kappa support the registered estimands.
11. **C11 planning/reliability/cost:** pointwise diagnostic frequencies and conditional-hazard route bounds are stated no more broadly than proved; cost units are knowable before later authorization.
12. **C12 smallest decisive instrument:** every retained stage can change a primary result; the physical harness is the sole declared blocking implementation prerequisite.

## 5. Required executable attacks

Execute everything permitted without experiment/provider/model/route/physical calls.

- **A — pin/reconstruction:** authenticate launcher before execution; verify commit, manifest, exact subject set, all object/byte/LF/line/SHA-384 pins, vendored Ajv closure and worktree/line-ending/omission/substitution resistance.
- **B — state/independence:** poison shared/reference semantic names and confirm oracle behavior; mutate temporal intervals, cuts, worker scope/actions/manifest/times, response identities, targets/catalogs, rejection hashes and stale commit state across both reducers.
- **C — authoritative causal graph:** forge proposal ID/bytes/hash, prestate/cut/digest, journal jump, pre-effective valid time, child bytes, poststate/digest/cut and A1 cut. Attempt to make a packet-local commit differ from the actually applied event while preserving descendant hashes.
- **D — cohort/population:** alter generator bytes/ID/digest, domains, motif, cuts, state/gold/action authority, selection/order and missing IDs; require six × 128 and identity preservation.
- **E — signed physical/ledger:** attack extra fields, unsigned/tampered/wrong-key/alg-confused/replayed/test-key-as-production envelopes, schema/receipt splice, candidate/generator/run mixing, missing containment/completion/external-work evidence, PMC mode/loss/attribution and total-I/O gates. Attempt any outgoing transition from ambiguity.
- **F — inference:** compare DP with small exhaustive enumeration, attack arbitrary missing positions and Boolean/type poison, run the m=20 property check, reproduce one interval and both route tails, and audit the finite-horizon recursion without assuming iid.
- **G — planning/cost:** reproduce the five frozen pointwise frequencies, especially `(0,.3,.1,.6)`; verify no region/true-probability guarantee; explain exactly what 768 pairs, 456 route trials and paying more buy.
- **H — omission/build decision:** run your own quick online primary-source sweep and the required internal-shelf challenge. Name one artifact/stage to remove or `NONE — ALL LOAD-BEARING`; one missing no-paid red witness; the smallest next BUILD artifact; and whether any repair is bigger than the bug.

## 6. Open questions

Answer `HELPFUL`, `NOT HELPFUL` or `HELPFUL WITH A NAMED FIX`.

1. Is dual-reducer replay of the exact state transition the right final scoring authority, or does it create a correlated-oracle problem?
2. Is ambiguity-as-terminal-missing the right rule while no provider-specific authenticated replay capability exists?
3. Does the closed signed envelope plus separate fixture-only trust root correctly define, without pretending to implement, the production receipt boundary?
4. Are the exact ETW PMC, loss, attribution, Job query and external-work requirements sufficient and proportionate on Windows?
5. Should retired instructions remain fail-loud primary evidence, or can it be diagnostic without weakening the physical research question?
6. Are total I/O bytes and operation counts the right additional H-shape coordinates?
7. Does the state oracle now cross a meaningful independence boundary after shared structural admission?
8. Is n=768 plus the unchanged 456/4 route plan still the smallest defensible instrument after these authority-only repairs?

## 7. Required verdict

Return one self-contained report containing:

1. top-level verdict under §1;
2. seat identity/model/checkpoint/harness and longitudinal posture;
3. pin/reconstruction verification;
4. evidence separated as EXECUTED, READ-ONLY, SEARCHED and UNSEARCHED;
5. applicability/exclusions;
6. C1–C12 scoreboard;
7. P0–P3 findings with exact location, bypass/indecision path, smallest repair and evidence;
8. attacks A–H with input/method/output/interpretation/limitation;
9. eight open-question answers;
10. `WHAT WOULD YOU BUILD?` and `WOULD YOU DESIGN IT DIFFERENTLY?`;
11. plain-language owner paragraphs answering whether the experiment can answer its question, what 768/4,608 and 456/2,736 buy, what more money would/would not buy, and why current red readiness is honest;
12. external primary-source and internal-shelf sweep logs, omission/bypass attack, residual risks, non-claims, seal/capability/side-effect/cleanup report and paid inference `NONE`.

No vague “more research” blocker. Name the missing byte, formula, trace, receipt, premise, alternative, plan or cost. A preferred method is not a blocker without a reachable false result or avoidable practical indecision.
