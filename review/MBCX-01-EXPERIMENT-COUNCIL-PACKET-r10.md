# MBCX-01 EXPERIMENT COUNCIL PACKET r10

## 0. Seat command and immutable bundle

You are one Moonwalker design-council seat reviewing an internal scientific instrument, not a production system. Read the complete role card at `<vault>` and adjudicate the repository `<repo>` at governing commit `efaa1bbff91b887597b711ff4936109e79ccfddd`.

The owner-pinned manifest is `MBCX-01-R10-PIN-MANIFEST.json`, Git blob `12589dbf0cc48704ae758d00fff1d9b0d16e2c01`. It lists 21 normative subjects with exact Git blob, LF byte count, line count, and SHA-384. Do not trust the working tree. Reconstruct and execute with:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\test-r10-normative-bundle.ps1 -Commit efaa1bbff91b887597b711ff4936109e79ccfddd -ManifestBlob 12589dbf0cc48704ae758d00fff1d9b0d16e2c01
```

The reconstruction wrapper itself is a pinned subject and uses `git cat-file blob` before import. It must report all six sections PASS. The manifest is bound by the packet's Git-blob pin rather than a circular self-hash.

Read at minimum these governing subjects from the pinned commit:

- `MBCX-01-EXPERIMENT-DESIGN-r9.md`
- `MBCX-01-R10-ARCHITECTURE-SPEC.md`
- `MBCX-01-R10-PRIOR-ART-MEMO.md`
- `MBCX-01-STATE-ACTION-CONTRACT-v5.json`
- `MBCX-01-PACKET-SCHEMAS-v4.json`
- `MBCX-01-MEASUREMENT-CONTRACT-v4.json`
- `MBCX-01-INFERENCE-CONTRACT-v5.json`
- `mbcx01_r10_reference.py`
- `mbcx01_r10_oracle.py`
- `verify-r10-normative-bundle.py`
- `verify-r10-schema-ajv.mjs`
- `verify-r10-pinned.ps1`
- `MBCX-01-R10-NO-PAID-VERIFICATION.json`

The r9 verdicts that caused this repair are pinned at the same commit:

- `MBCX-01-SEAT1-OUTSIDE-OPUS5-VERDICT-r9.md`
- `MBCX-01-SEAT2-CHATGPT-SOL-VERDICT-r9.md`
- `MBCX-01-SEAT3-CODEX-VERDICT-r9.md`

Use them only to identify inherited defects and whether the named repair actually closes each one. Maintain the current-round lateral seal: do not inspect another seat's current r10 answer, browser output, logs, marker, or verdict before producing yours.

Claude and ChatGPT are longitudinal seats whose own-lane context is intentionally retained. Codex EXEC is one fresh read-only seat. Do not edit files, implement FD/FC/TN candidates, run a provider/model/route soak, or make paid calls.

## 1. Question that must be answered

If implemented literally, does this bundle now have a fair and affordable chance to answer:

1. whether exact due-obligation continuity can remain physically bounded over every frozen `H,D,F` cell;
2. which of FD, FC, or TN survives exactness and forms the defensible engineering Pareto set, with carrier preference separately labeled; and
3. whether one frozen model can use bounded-context BC without materially underperforming independently built oracle-minimal OM in a cold serial `A0 -> B -> writer -> A1` episode?

A future falsification is an answer. A design that predictably returns practical indecision is not. Exact thresholds and the explicitly frozen transition region may remain inconclusive.

Load-bearing findings are only paths to a false continuity result, false engineering result, false scientific branch, avoidable practical indecision, non-total semantics, presentation taint, hidden work, invalid inference, unreconstructable evidence, or material cost discovered only after authorization. Exclude licensing, deployment ceremony, FIPS/CNSA, hostile actors, concurrent writers, personality, persistent-mind claims, and the later coordination experiment unless you show a direct false-result path.

## 2. r9 blockers and r10 repairs under attack

The preceding round returned one GO-WITH-FIXES and two NO-GOs. r10 adopts mechanisms, not votes.

| r9 blocker | r10 repair you must attack |
|---|---|
| State engines checked key sets instead of actual schema values | One contract-driven schema ingress validates types, enums, patterns, closed objects, one-of branches, numeric limits, and calendar-real microsecond UTC. Pinned Ajv independently compiles all 17 composed event schemas under `strict:true`. Reducer independence begins after that shared boundary. |
| Expired, future-effective, or future-known facts could participate | Both post-ingress reducers separately require journal/knowledge visibility and half-open valid-time effectivity, plus non-retraction. |
| Action IDs and handoff links could be forged | Opening obligations enforces deterministic `action_id(scope,obligation)`. Handoffs bind cut, action catalog, and canonical snapshot hashes; proposals bind durable worker-response hashes when present. |
| Worker conditional schema did not compile; scorer omitted A0 | Six closed schemas compile. Conditional array subschemas declare `type: array`. Exact scoring consumes expected manifest, A0, worker, writer receipt, and A1 and requires `A0 AND B AND A1` after hash-link checks. |
| Schema-valid invented scenarios/objects/cuts/actions could score | One expected experiment manifest binds scenario, scope, cut, observation, canonical world, action catalog, gold action, and A1 target. BC and OM receive the same manifest action universe. |
| Served 65,536-byte renderer was declarative | Exact canonical UTF-8 bytes are padded with ASCII space to 65,536; SHA-256 covers the served bytes; overflow is pre-dispatch design failure. |
| Cohort prose and code disagreed; duplicates and unknown motifs could slip | Preselection rejects global duplicate IDs, unknown motifs, and wrong totals. One cut is chosen before recomputed eligibility. Exactly six motifs by 128 = 768. |
| Physical gate measured the root and mislabeled `5H`/constant work | It aggregates root plus descendants over all four H values at every D,F, rejects escape/missing accounting, admits `5H` under the explicit 500,000 tolerance, rejects root or hidden-child `10H`, and labels constant 4M instructions unaffordable but bounded. |
| Call ledger was prose | A complete 5-state by 5-event transition matrix executes. Retry identity is fixed; ambiguous acceptance is terminal unless the route attests exact idempotency; bytes/hash are durable before parse. |
| Missingness stopped at seven pairs | An exact conservative DP hull has no missing-count ceiling. It is checked against explicit `4^m` enumeration for small cases and a branch-flip witness. A substantive branch requires certification under every legal completion. |
| Indifference region was verbal | `n=768` promises 90% assurance only for delta>=0/OM>=.90 promote, delta<=-.20/OM>=.90 interface-fail, and OM<=.70 ceiling. OM .70-.90 and delta-transition cells are diagnostic only. |
| 98,868-call route soak overbudgeted diagnostic cells | One trial is the actual six-call pair route. Exact binomial planning chooses 456 trials, accept <=4 failed pairs: bad-route false acceptance 0.0494333 at p=.02; good-route pass 0.919067 at p=.005; 2,736 scheduled positions before retries. |
| Git reconstruction was absent/broken on this PowerShell host | The wrapper avoids the unavailable `ProcessStartInfo.ArgumentList`, verifies the council-pinned manifest blob, extracts exact blobs, checks all subject pins, and executes only reconstructed bytes. |

Do not accept this table as evidence. Attack the exact bytes and reachable behavior.

## 3. Prior art and orthogonal direction

The cited memo maps each repair to primary prior art: bitemporal valid/record time; JSON Schema format assertion and Ajv strict typing; AWS/Stripe idempotent request binding; Windows Job Object process-tree accounting; NIST/NASA binomial reliability-demonstration plans; Manski-style worst-case missing-data partial identification; and SLSA/Git digest reconstruction.

Open the cited primary sources when they decide a ruling. Search orthogonally for a smaller correct mechanism. In particular, attack whether a direct full-route acceptance plan is legitimate, whether its iid/representativeness assumption is adequately frozen, and whether the DP state compression really preserves the worst confidence-sequence endpoint. Record exact queries, opened primary sources/sections, effect on ruling, evidence class, and stop reason. Search snippets are locators, not evidence.

## 4. Claims C1-C12

Return `HOLDS`, `FALSE`, or `UNDERDETERMINED` for each.

1. **C1 — decomposition:** continuity, FD/FC/TN engineering, carrier preference, and conditional model usability are separate decisions; controls may win.
2. **C2 — state totality:** actual ingress schema, bitemporal cuts, identity/hash guards, idempotency, cycles, and writer transitions yield one answer for every legal input.
3. **C3 — executable independence:** sharing schema ingress is explicit and appropriate; independent post-ingress reducers plus adversarial/mutation witnesses do not share a reachable semantic false premise.
4. **C4 — packet validity:** six compiled schemas, manifest authority, canonical-object identity, shared action universe, exact served bytes, and five-object scoring prevent answer-changing presentation or forged-link paths.
5. **C5 — cohort provenance:** global validation, one cut before recomputation, supplied-Boolean deletion, exact motif totals, and retention yield the frozen 768-pair estimand population.
6. **C6 — physical boundedness:** complete 100-cell coverage and process-tree accounting support the registered finite-range practical-boundedness claim without false asymptotic language or conflated affordability.
7. **C7 — recovery totality:** the executable ledger handles every state/event and crash window; retry cannot duplicate semantic work under the frozen route contract.
8. **C8 — serial DAG:** durable response, exact writer receipt, cold A1, and missing-pair policy yield one paired outcome or an explicit missing pair.
9. **C9 — engineering fairness:** exactness filtering and Pareto output cannot turn a carrier preference into a mechanism result.
10. **C10 — inference:** Proposition 3.1 implementation, alpha allocation, strict endpoints, fixed kappa, and numerical parity support the registered heterogeneous average-conditional-mean estimands.
11. **C11 — missingness, power, reliability, cost:** DP completion bounds, numerical assurance region, 456/4 route qualification, 4,608 scheduled scientific positions, and separate raw-attempt/dollar ceilings make usefulness and cost knowable before authorization.
12. **C12 — smallest decisive instrument:** each retained stage can change a primary result; borrowed machinery strengthens the ruler without widening the claim.

## 5. Required executable attacks

Execute everything your environment permits without model/provider calls or fabricated carrier results.

- **A — pin and reconstruction:** independently verify the governing commit, manifest blob, every listed subject, exact extraction, Ajv closure, and reconstructed verifier. Attack stale checkout substitution, line-ending substitution, manifest omission, wrapper self-omission, and import-before-verify.
- **B — state schema and time:** generate legal/malformed events outside fixtures. Attack booleans-as-integers, enum/type/pattern mismatch, extra fields, impossible leap/day/time values, event/operation mismatch, future knowledge, future effectivity, expired validity, and retraction.
- **C — identities and transitions:** forge completion action, cut, catalog, snapshot, request, response, receipt, and proposal identities. Exercise idempotency collision, event reuse, cycles longer than two, handoff lifecycle, and every effect. Name any shared reducer defect.
- **D — packets and score:** compile and attack every schema, especially conditional array types. Attack invented/changed canonical objects, scenario/cut/observation substitution, unequal BC/OM action universes, duplicate semantics, overflow, non-space padding, served hash, A0 omission, extra B children, and A1/receipt link changes.
- **E — cohort:** attack unknown motifs, global and within-motif duplicates, wrong totals, duplicate cut IDs, ineligible selected cut, supplied Boolean poisoning, motif crossover, retention ties, shortfall, and action-universe substitution. Recompute 6x128=768.
- **F — physical and ledger:** recompute all 100 cells. Attack root/child `10H`, `5H`, constant-over-budget, child escape, missing descendants, preprocess/cache/filesystem/database work, counter splitting, and every ledger state/event/crash window. Separate boundedness, affordability, and implementation failure.
- **G — theorem and missing DP:** open Chugg/Ramdas Proposition 3.1 and verify every premise/constant used. Independently compare the DP hull to full enumeration, including non-suffix missing positions and enough cases to test whether retaining maximum U per prefix sum is sufficient for both endpoint extrema. Seek a counterexample.
- **H — power and decision:** reproduce at least one interval vector and the assurance-region interpretation. Test threshold, transition, clear promote, clear interface-fail, and clear ceiling truths. Decide whether `n=768` answers the original practical question without a dishonest near-threshold promise.
- **I — transport and cost:** independently search integer `(n,c)` plans and reproduce both binomial tails. Attack the composite-pair endpoint, iid/representativeness, route drift, retry contribution, denominator, `OTHER_UNCLASSIFIED`, producer/consumer risks, scheduled-versus-accepted-versus-raw attempts, and 2,736 versus 4,608 arithmetic. Propose a smaller valid plan only with declared risks and cost.
- **J — deletion and boundary:** name one stage/artifact to remove or `NONE — ALL LOAD-BEARING`; one no-paid test still missing; one strong omitted comparator; and the exact boundary to the later coordination experiment.

## 6. Specific open questions for this round

Answer each `HELPFUL`, `NOT HELPFUL`, or `HELPFUL WITH A NAMED FIX` and justify from bytes/math.

1. Is shared schema ingress with independence claimed only after it the correct architecture, or does it leave a reachable shared semantic false-green?
2. Is the bitemporal predicate complete for the experiment's single-writer journal semantics?
3. Does manifest binding plus exact served-byte hashing close the packet/scoring identity problem?
4. Does Job Object aggregate accounting plus the explicit finite-range tolerance support the claim without false pass/false kill? What exact counter still lacks a future harness binding?
5. Is the missing-completion DP exact/conservative for arbitrary missing positions and both decision endpoints? If not, provide the smallest counterexample and replacement.
6. Is the numerical assurance region at `n=768` a defensible answer to the original question, or is a different alternative/indifference design required? Give its calls if different.
7. Is the 456/4 full-route reliability-demonstration plan a valid, smaller answer to the 2% pair-missing gate? If not, give the exact violated premise and a corrected `(n,c)` plan.
8. Is any retained r9 runtime dependency an unnecessary attack surface, or is it properly pinned transitional substrate?

## 7. No-paid evidence classification

The retained report is deterministic design verification only: `experiment_evidence=false`, `paid_calls=0`. It records:

- 17 event schemas and 11 killed mutants;
- six compiled packet/output schemas and exact 65,536 served bytes;
- 768 selected scenarios, 128 per motif;
- all 100 H-D-F cells and 25 ledger state/event pairs;
- DP/exhaustive missingness parity through the small witnesses;
- independently rediscovered `(456,4)` transport plan; and
- 17-event cross-engine integration parity.

These are not FD/FC/TN results, provider reliability observations, model outcomes, or scientific evidence. The future physical harness and route soak have not run. A GO means the instrument is ready for the next no-model gate, not that the experiment or hypothesis passed.

## 8. Required verdict

Return one self-contained report:

1. `GO`, `GO-WITH-FIXES(reason)`, or `NO-GO(reason)`.
2. Seat identity, model/checkpoint, harness, title, and longitudinal/fresh posture.
3. Governing-commit, manifest-blob, subject-pin, and exact-reconstruction verification.
4. Evidence separated as EXECUTED, READ-ONLY, SEARCHED, and UNSEARCHED.
5. Applicability and explicit exclusions.
6. C1-C12 scoreboard.
7. Findings with P0-P3, exact location, false-result/avoidable-indecision path, smallest repair, and evidence.
8. Attacks A-J with input, method, output, interpretation, and limitation.
9. Eight open-question labels and answers.
10. `WHAT WOULD YOU BUILD?`
11. `WOULD YOU DESIGN IT DIFFERENTLY?`
12. Plain-language paragraphs for the owner: can this experiment now answer its question; what 768 pairs/4,608 scheduled positions buy; what the 456-trial/2,736-position route gate buys; what paying more would and would not buy; and what uncertainty remains unavoidable.
13. Omission/bypass attack, prior-art sweep log, residual risks, non-claims, capability/lateral-seal report, paid inference NONE, side effects, and cleanup.

No vague “more research” blocker. Name the missing byte, formula, trace, counter, schema, premise, alternative, plan, or cost. A preferred method is not a blocker without a reachable false-result or avoidable practical-indecision path.
