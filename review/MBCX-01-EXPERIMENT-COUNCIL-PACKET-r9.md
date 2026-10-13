# MBCX-01 EXPERIMENT COUNCIL PACKET r9

## 0. Seat command and immutable bundle

You are one Moonwalker design-council seat reviewing an internal scientific instrument, not a production system.

Read the complete role card at `<vault>` and adjudicate the repository `<repo>` at commit `f8fa75647f702dcc14f91b2d974ed1497aeef400`.

The five normative artifacts are:

| Artifact | Git blob | LF bytes | Lines | SHA-384 |
|---|---|---:|---:|---|
| `MBCX-01-EXPERIMENT-DESIGN-r8.md` | `24e2b230cc2e293cbe6bd7e6dd37100c680b9ff1` | 19,867 | 180 | `5A690CFB6071D67831551C38066600E62C5A5E08A45A8B8A8AD599A4C72602FBFB5D326BF7BBD70A70806510A33E7DA3` |
| `MBCX-01-STATE-ACTION-CONTRACT-v4.json` | `9efb8dbca72542db522ded09269cae332e396def` | 16,328 | 173 | `16B89FDFD08992D9E65143E8AED4D84402A096919A3B522AFD48B78070C5778024C80D1C2070A1ABB7CCB90155D199CD` |
| `MBCX-01-PACKET-SCHEMAS-v3.json` | `a42be28546bf213d237adf306d2e0a8758ad2d52` | 14,674 | 161 | `E48B690F2FFF3BDF605A1CC6D98A0CD2BF7FD7D8F78CA9B70B7A875CD2D6326C20EA15571EB9C2217F0DD59A13C0398C` |
| `MBCX-01-MEASUREMENT-CONTRACT-v3.json` | `bf9dab5500beb49b6ed3a51e90661e76dc530dec` | 9,551 | 115 | `A96ED13DF6C7F0F4DD63C1B1CBC6703615F922D2AC30D9ACEC6F25C9FCDD3F50B870C88920359DE339BB5EDD6A090A0D` |
| `MBCX-01-INFERENCE-CONTRACT-v4.json` | `6d649433d5e36db3a81c3ecc7ec86e43f8d5ce8f` | 11,390 | 147 | `F53748B8C4AB1515A81C4E63965BB2AF37AA665A4290B6FE0CCCAEC353CB12ADB56DC99E431047F46585C57D69CBB7DB` |

Review these pinned supporting artifacts too:

| Artifact | Git blob | LF bytes | Lines | SHA-384 |
|---|---|---:|---:|---|
| `mbcx01_r9_oracle.py` | `76560dd49cbc225d36ca9090aae26efd8b7493ce` | 16,681 | 368 | `34A795648A3A2236CA43367077AF70E281E8D87CBF0D4CEDB586C25E371F012F909A8BDCB9F5F538C9C55F2C2DE4706A` |
| `mbcx01_r9_reference.py` | `170f7d2c2815c4f2d78f2c75ea5c58b4442d0fa9` | 66,936 | 1,394 | `6DA11124D3B90E2D649A99E54338E2395BC3D3BD6686BBE3F17D632394ABA6F49245D8D416340EEC60B9CA212C448A37` |
| `verify-r9-normative-bundle.py` | `ecac64be665a05f6c47d2b4ed828dd9d4118004d` | 22,271 | 507 | `88E157644F199D46035DA41B504851A741A210830604999206483E4FB9B4F8A593DF5DC266456E773168708514EF09D8` |
| `verify-r9-schema-ajv.mjs` | `4ffd38bd67147ad475309e1eefd0de3795d714ed` | 3,659 | 78 | `37FB06B5761D208D650EB29A563A3A4D63A47A9633FA0638FB1D27F0258AA1CB25B8084AB5E9DA11C63269DFD314372C` |
| `MBCX-01-R9-NO-PAID-VERIFICATION.json` | `6c0f66a0d96501e6d687a3bad72e5a00e140e40c` | 15,537 | 429 | `3294001EE104D0C14B0FD4B2C2E8D3FFD317FDE3F6CEF9165FE314196082C98657B9B211FD4157FBFBA72E934A0EDC25` |

The JSON contracts govern their named domains. Verify pins from Git objects. If checkout bytes differ, the pinned objects govern. `test-r9-normative-bundle.ps1` reconstructs the bundle into a temporary directory exclusively from `git cat-file blob` output and executes it there.

### Longitudinal seats and lateral seal

Claude and ChatGPT are a longitudinal council lane across rounds; their retained own-lane history is intentional. Codex EXEC is one fresh read-only seat. This is not a per-round freshness claim.

Maintain a lateral seal. Do not inspect another seat's r9 answer, browser output, verdict, stdout, stderr, or completion marker before producing yours. Earlier reports may be used only to test whether a named repair closes that seat's inherited defect, and must be labeled inherited. Do not edit files, implement candidates, or make paid calls.

## 1. The question that must be answered

If implemented literally, will the bundle fairly and affordably answer the original question:

1. can exact due-obligation continuity remain physically bounded over the complete frozen H, D, and F ranges;
2. which of FD, FC, or TN survives exactness and forms the defensible engineering Pareto set, with carrier preference separately labeled; and
3. can one frozen model use bounded-context BC without materially underperforming independently built oracle-minimal OM in one cold serial `A0 -> B -> writer -> A1` episode?

A future falsification is an answer. A design that merely returns `INCONCLUSIVE_OR_UNDERFUNDED` for practically separated alternatives is not. Exact-cutoff truths may remain an explicit indifference region; no finite experiment must promise a strict branch when truth lies on a strict cutoff.

Load-bearing findings are limited to paths that can cause a false continuity result, false engineering result, false scientific branch, avoidable practical indecision, non-total semantics, presentation taint, hidden work, invalid inference, or material cost learned only after authorization. Exclude licensing, deployment ceremony, FIPS/CNSA, hostile actors, concurrent writers, personality, persistent-mind claims, and the later coordination experiment unless you show a direct false-result path.

## 2. r8 council convergence and r9 dispositions to attack

The preceding round returned one GO-WITH-FIXES and two NO-GOs. r9 adopts mechanisms, not votes:

| Convergent blocker | r9 repair under attack |
|---|---|
| Friendly state reference could false-green itself; effects, longer cycles, idempotency, and originating cut were incomplete | Closed event envelope; independent journal-projection reference and direct-transform oracle; 289 ordered pairs; targeted reschedule/delegation/duplicate/conflict/three-cycle traces; six named mutants killed |
| Packet declarations did not prove real schema or cross-record meaning | Authenticated Ajv Draft 2020-12 runtime closure plus independent semantic validator; forged hash, alias, missing catalog, kind, target, prerequisite, canonical-object, and overflow attacks |
| BC and OM were described but not actually built from separate information sources | BC builder consumes candidate-selected public IDs; OM builder consumes independent gold causal read-set; shared cut, action universe, renderer, instructions, and transport |
| B scoring permitted extra semantic work | B requires exactly the singleton target proposal and exactly that singleton commit |
| A schema-valid maximum could exceed 65,536 bytes | Syntactic validity and transport fit are separate; any retained oversize packet is `PACKET_ENVELOPE_EXCEEDED` before dispatch |
| Cohort freeze could leak generator/gold information or trust supplied eligibility | Generator specification, parameters, gold enumerator, and evaluator freeze before candidate inspection; candidate freezes before a fresh hidden seed; eligibility is recomputed after one-cut selection and supplied booleans are discarded |
| The H-D plane plus F curve did not support the original full-range claim | Full `4 x 5 x 5` Cartesian product: 100 unique cells |
| Red candidates were expected-label declarations; low-slope `10*H` work could pass | Every named candidate emits real 100-cell counter rows and is evaluated; page/byte equations, shape gates, same-unit totals, descendants, page size, and counter closure execute |
| `kappa=0.25` looked tuned or theorem-incompatible | Proposition 3.1 permits positive kappa; 0.25 is frozen as source default under `SOURCE_DEFAULT_NOT_OC_TUNED`; terminal sensitivity at 0.10, 0.15, 0.25, 0.50, and uniform is published |
| OC hid poor power behind OM=0.95; 384 pairs could not reliably answer practical cases | Full negative-delta by OM=.80/.85/.95 curve exposed the weakness. Frozen sizing among 384/512/768/1024 selected n=768. Four practical targets must each clear 90% in the retained 10,000-replicate confirmation |
| Reliability was pointwise rather than simultaneous and its cost was unclear | Eight frozen modes by six positions; alpha `0.05/(6M)` and budget `0.02/(6M)`; every exact upper bound must pass. Zero failures need 16,478 observations per position, 98,868 total route-soak calls |
| Transport could hide a known broken design | `DESIGN_OR_IMPLEMENTATION_FAIL` precedes `TRANSPORT_INCONCLUSIVE` |

Do not accept these summaries. Attack the exact governing bytes and reachable behavior.

## 3. No-paid evidence already generated

The retained report says `experiment_evidence=false` and `paid_calls=0`. It records all six sections PASS:

- 17 event types, 289 cross-implementation ordered pairs, targeted traces, and six killed mutants;
- real Ajv validation, independent semantic attacks, executed BC/OM builders, exact singleton scoring, and pre-dispatch overflow rejection;
- 960 generated and 768 retained unique scenarios, 128 per motif, with supplied eligibility ignored;
- 100 unique H-D-F cells and seven executable physical-work mutants rejected;
- analytic, Simpson, and high-precision Decimal endpoint parity;
- 16 operating-characteristic cells by 10,000 replicates: 160,000 synthetic trials; and
- 4,608 accepted scientific calls and 1,536 cold reconstructions at the only scientific look, n=768.

The practical power targets achieved:

| Cell | Required branch | Observed retained frequency |
|---|---|---:|
| equal BC/OM, OM=.90 | promote | 99.76% |
| low-discord equal, OM=.90 | promote | 99.84% |
| delta=-.20, OM=.90 | model/interface fail | 99.72% |
| equal BC/OM, OM=.70 | model/interface ceiling | 94.30% |

At n=384, the compact sizing witness produced only about 56%, 67%, 50%, and 39% on those same practical branch types. The extra 2,304 scientific calls therefore buy a large reduction in avoidable inconclusive results. They do not guarantee a decision at delta=-.10 or OM=.80, where strict-threshold uncertainty is expected.

The 98,868-call reliability soak is separate: it buys simultaneous evidence that transport will not materially erase the 768-pair experiment. It does not increase scientific power, improve the model, or rescue a bad mechanism. If no genuinely zero-price route exists, it remains paid and requires separate owner authorization.

## 4. Claims C1-C12

Return `HOLDS`, `FALSE`, or `UNDERDETERMINED` for each.

1. **C1 — decomposition:** continuity, FD/FC/TN engineering, carrier choice, and conditional model usability are separate; simpler controls can win.
2. **C2 — state totality:** the envelope, guards/effects, two independent implementations, originating cut, idempotency, cycles, and writer yield one answer for every legal input.
3. **C3 — executable independence:** differential and mutation witnesses meaningfully test the contract rather than sharing a false premise or implementation path.
4. **C4 — packet validity:** real Draft 2020-12 validation plus semantic checks, independent builders, action identity, envelope, and exact scorer leave no answer-changing presentation choice.
5. **C5 — cohort provenance:** instrument-before-candidate freeze, candidate-before-seed freeze, one cut before recomputation, and retention rules prevent leakage, duplication, and hidden population claims.
6. **C6 — physical boundedness:** complete 100-cell coverage, closed counters, same-unit totals, page/byte coherence, descendants, shape gates, and executed red candidates avoid false passes and false kills.
7. **C7 — reconstruction and isolation:** future candidate harness gates are sufficient to bind output causally to canonical artifacts without pretending they already ran.
8. **C8 — serial DAG and recovery:** response durability, ambiguous acceptance, no resample, writer atomicity, and cold A1 yield one paired outcome.
9. **C9 — engineering fairness:** exactness filtering and Pareto output cannot turn carrier preference into a mechanism result.
10. **C10 — inference:** Proposition 3.1, alpha allocation, delta transform, strict endpoints, kappa freeze/sensitivity, terminal-only n=768, and numerical witnesses support the estimands.
11. **C11 — power, missingness, reliability, and cost:** the practical power targets, threshold indifference region, joint missing completions, simultaneous route gate, 4,608 scientific calls, and separately priced soak make both usefulness and cost knowable before authorization.
12. **C12 — smallest decisive instrument:** each retained stage can change a primary result; borrowed machinery strengthens the ruler without widening the research claim.

## 5. Required executable attacks

Execute everything your environment permits without making model calls or fabricating FD/FC/TN results.

- **A — Git reconstruction:** verify every pin, reconstruct only from Git blobs, parse all JSON, authenticate the complete Ajv closure, and run a compact full verifier. Attack stale checkout substitution and report-hash self-consistency.
- **B — state differential:** generate traces outside the verifier fixtures. Attack closed payloads, sequence/time/cut validity, correction/restoration, four-plus-node cycles, scope, action substitution, idempotency collision, handoff lifecycle, and every declared effect. Add a mutant if the existing six miss a plausible shared bug.
- **C — packets and scoring:** attack every schema with extra/missing properties, wrong discriminators, unsafe integers/times, duplicate semantic IDs, forged opaque actions, unavailable catalogs, unresolved references, cap arrays, padding, hashes, non-target and multi-target B outputs, and schema-invalid provider output.
- **D — builders and cohort:** prove BC and OM share presentation and action universe but derive object IDs independently. Attack duplicate scenario/cut IDs, chosen-cut-only ineligibility, supplied Boolean poisoning, motif crossover, shortfall, retention ties, global collisions, source change after freeze, and seed visibility.
- **E — physical work:** recompute all 100 cells and unit totals. Seek a candidate hiding work in descendants, preprocessing, cache, filesystem, database, memory, page substitution, counter splitting, low-slope archive-linear work, H-D-F interaction, or logical lookup backed by scan. Seek both false pass and false kill.
- **F — theorem and numerics:** open the Chugg/Ramdas primary source. Verify every constant and premise in Proposition 3.1, predictable estimate, normalizer, inequality, inversion, clipping, strict endpoint, transform, alpha split, and uniform limit. Independently reproduce at least one vector.
- **G — sample size and OC:** recompute the n=384/512/768/1024 selection and retained practical powers. Verify every cell's derived delta/OM, SHA-256 stream framing, categorical boundaries, fixed positions, and the rule that exact/near thresholds may remain inconclusive. Determine whether the 90% target set is sufficient to call the original question answerable.
- **H — missingness and reliability:** exercise zero, one, seven, and eight missing pairs. Recompute `0.05/(6M)`, `0.02/(6M)`, Clopper-Pearson endpoints, 16,478 clean observations per position, and 98,868 total. Attack dependence, failure-mode overlap, and unregistered route failures.
- **I — decisions and cost:** trace candidate exact/bounded success, all-candidate failure, exact-but-unbounded, promote, interface fail, oracle ceiling, threshold inconclusive, transport inconclusive, and design failure. Recompute 4,608 calls and 1,536 reconstructions. State plainly what the extra scientific calls and route-soak calls each buy.
- **J — deletion and boundary:** name one stage or artifact to remove, or `NONE — ALL LOAD-BEARING`; name one no-paid test still missing; and state the exact boundary to the later coordination experiment.

## 6. Orthogonal-method questions

For each, answer `HELPFUL`, `NOT HELPFUL`, or `HELPFUL WITH A NAMED FIX`.

1. Does Proposition 3.1 cover the registered heterogeneous average-conditional-mean estimands and alpha allocation? If not, name the exact premise and replacement.
2. Is complete 100-cell H-D-F evaluation sufficient for the frozen finite-range claim, or can a legal implementation evade the counter/shape gates inside those cells?
3. Are the journal-projection and direct-transform engines independent enough? Name the smallest stronger differential oracle or model checker only if it closes a reachable shared-error path.
4. Is n=768 the smallest defensible answerable design given the practical alternatives and strict threshold indifference region? If not, provide an executable alternative and its call cost.
5. Does the simultaneous 48-cell reliability gate measure a real need, or is there a less expensive dependence-safe route contract that preserves the two-percent pair-missing guarantee?

## 7. Current primary-source and prior-art sweep

Use current primary sources where a fact decides a ruling. Search at least these lanes unless pinned bytes already settle them:

1. sequential empirical-Bernstein confidence sequences for heterogeneous conditional means;
2. indifference-zone and assurance-based sample sizing for composite noninferiority plus performance-floor decisions;
3. confirmatory generator freeze, eligibility-conditioned target populations, and benchmark leakage;
4. full factorial finite-range coverage and physical-cost counter coherence;
5. JSON Schema 2020-12, RFC 8785/JCS, and content-pinning validation runtimes;
6. workflow durability, atomic commit, idempotency tokens, and unknown acceptance; and
7. current provider acceptance receipts, route fallback/cache behavior, zero-price primitives, and price exposure.

Log exact queries, opened origins/sections, effect on the ruling, evidence class, and stop reason. Search snippets are locators, not evidence. If another field offers a smaller correct instrument, say exactly what to borrow and which artifact it replaces.

## 8. Omission and bypass attack

Identify a strong omitted comparator or `NONE`; a legal two-answer trace or `NONE`; one false continuity pass and false kill; one false mechanism preference; one false model-usability and false ceiling story; one inference/cohort/render/reconstruction/transport/cost bypass; one no-paid test without which you refuse implementation; one mechanism to borrow; one artifact to delete or `NONE — ALL LOAD-BEARING`; and the exact later-experiment boundary.

## 9. Required verdict

Return one self-contained report:

1. `GO`, `GO-WITH-FIXES(reason)`, or `NO-GO(reason)`.
2. Seat identity, model/checkpoint, harness, title, and longitudinal/fresh posture.
3. Pin/byte verification for all artifacts.
4. Evidence separated as EXECUTED, READ-ONLY, SEARCHED, and UNSEARCHED.
5. Applicability and explicit exclusions.
6. C1-C12 scoreboard.
7. Findings with P0-P3, exact location, false-result or avoidable-indecision path, smallest repair, and evidence.
8. Attacks A-J with input, method, output, interpretation, and limitation.
9. Orthogonal-method answers using the required labels, including any `HELPFUL WITH A NAMED FIX` ruling.
10. WHAT WOULD YOU BUILD?
11. WOULD YOU DESIGN IT DIFFERENTLY?
12. Plain-language answer: does the experiment now have a fair chance to answer its question, what do 4,608 scientific calls buy, what would 98,868 route-soak calls buy, and what uncertainty remains unavoidable?
13. Omission/bypass attack, sweep log, residual risks, non-claims, capability/lateral-seal report, paid inference NONE, side effects, and cleanup.

No vague “more research” blocker. Name the missing byte, formula, trace, counter, schema, premise, alternative, power target, or cost. A preferred method is not a blocker without a reachable false-result or avoidable practical-indecision path.
