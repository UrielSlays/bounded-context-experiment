# NO-GO(inference-target, identity-encoding, schema/scoring non-totality) — EXECUTED

## 1. Seat identity

**Report:** *The Prefix Is Not the Population — sealed Codex r7 review*  
**Seat:** independent Codex EXEC reviewer  
**Model:** OpenAI Codex, GPT-5 family; exact checkpoint not exposed  
**Posture:** fresh one-shot; no prior-seat context retained  
**Paid inference:** NONE  
**Seal:** maintained. I saw lateral-output filenames in directory/Git listings but opened no r7 verdict, stdout/stderr log, completion marker, or browser output.

## 2. Pin and byte verification

Packet working copy matched HEAD `52592a2…`, blob `15f2406…`, 13,129 bytes, SHA-256 `0d6b9a…8183fb4f`.

All normative working copies were byte-identical to commit `6cf58b4ad123cb7487faae5499e623d316a06d47`; the pinned objects govern.

| Artifact | Blob | Bytes/lines | SHA-384 | Result |
|---|---|---:|---|---|
| `MBCX-01-EXPERIMENT-DESIGN-r6.md` | `124e4be…` | 10,660 / 134 | `3496481950FE9E07E1FFE655BAFD90F233301853CB0A32C279AE530FA36743787DEADF672EA403C17FD19451D7103FA2` | MATCH |
| `MBCX-01-STATE-ACTION-CONTRACT-v2.json` | `e1d8f598…` | 8,481 / 142 | `2A129568426287497FEA3404462591106AEBCD1B099963F916A9A463E707778DD484CAD43AA629DF489E83BD85EE8DAE` | MATCH |
| `MBCX-01-PACKET-SCHEMAS-v1.json` | `d31a9aae…` | 6,356 / 95 | `D9315572FD816BF748C528580C7F1AD75E4C70534C0ABB8494D1B162EC48908E6DD906EDE90E35A5791E69FC27195714` | MATCH |
| `MBCX-01-MEASUREMENT-CONTRACT-v1.json` | `095f24be…` | 4,630 / 85 | `C0ED0F0AE92DC5B221130CA731EF1DE16D75634FE48F0DB7987A87679B0E973A8367629B6BEA518D1F5631B84E857925` | MATCH |
| `MBCX-01-INFERENCE-CONTRACT-v2.json` | `907d3f65…` | 7,869 / 116 | `2883EC875757E91DF903960A9632F2C21032D55A96C0CF4E33D57A731E898DD941059C2BA7E88530CB17EE6763989F15` | MATCH |

## 3. Build-decision challenge

1. **ALREADY-BUILT? — READ-ONLY / SEARCHED.** No single product answers the entire MBCX scientific question, but most machinery is established: event sourcing/CQRS and projections, PostgreSQL indexed materialized views, SQLite atomic journals, AWS/Stripe idempotency, Temporal durable workflows, RAG, and blackboards. Adopt these components rather than inventing persistence, replay, and transaction machinery. [Microsoft Event Sourcing](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing), [PostgreSQL materialized views](https://www.postgresql.org/docs/current/rules-materializedviews.html), [SQLite atomic commit](https://sqlite.org/atomiccommit.html).

2. **PRODUCT-FIT? — READ-ONLY / UNSEARCHED—NOT-LOAD-BEARING (owner posture plus pinned bytes).** Customer need: *give the owner a fail-loud, cost-capped answer about whether due obligations survive archive/depth growth and whether a frozen model can use the packet.* The separated conclusions and preauthorization knob fit GOVERNED POWER/MIRROR-NOT-COP. Claims that “no mechanism is omitted,” counters are “closed,” or leakage is “prevented” are completeness/prevention ambitions and do not fit.

3. **BIGGER-THAN-THE-BUG? — READ-ONLY / UNSEARCHED—SETTLED-BY-PINNED-BYTES.** Yes: five contracts, 2,304 accepted calls, 768 reconstructions, a custom writer, renderer, counter system, isolation system, and sequential inference constitute a new experimental subsystem. This council round is the necessary return to the design gate; owner approval is still required.

## 4. Claim scoreboard

| Claim | Ruling | Evidence |
|---|---|---|
| C1 decomposition | **HOLDS, READ-ONLY** | Conclusions are separated at design:9-15, 70-78. Residual: no candidate/harness exists. |
| C2 state/action totality | **FALSE, EXECUTED** | Legal composite-ID collision; absent payload schemas/reducer. |
| C3 schema/parity | **FALSE, EXECUTED / SEARCHED** | Explicit condition disclosure, open `fields`, oversize valid packet, JCS conflict. |
| C4 FD/FC/TN completeness | **UNDERDETERMINED, READ-ONLY / SEARCHED** | Taxonomy is not operationally exhaustive and candidates are unfrozen. |
| C5 cohort/gold | **FALSE, EXECUTED / SEARCHED** | Gold cardinality closes guessing, but eligibility-conditioned selection is not an unbiased sample of the generated population. |
| C6 boundedness | **FALSE, EXECUTED / SEARCHED** | Unregistered CPU work and untested H×D cells pass. |
| C7 isolation/reconstruction | **FALSE, EXECUTED** | Allowed config values can encode output; no sandbox/reconstruction implementation exists. |
| C8 serial DAG | **FALSE, EXECUTED** | A1 output/scoring algebra absent; crash-before-journal has two policies. |
| C9 engineering/carrier fairness | **UNDERDETERMINED, READ-ONLY** | Label separation exists; Pareto aggregation and carrier rule remain unspecified. |
| C10 inference | **FALSE, EXECUTED / SEARCHED** | Early intervals cover prefix means, not the declared full-manifest estimand. |
| C11 transport/cost | **FALSE, EXECUTED** | CI method and six-node mapping are absent; invalid model output is not classified. |
| C12 smallest instrument | **FALSE, READ-ONLY** | Historical `confseq` pins cannot affect the primary r7 method; subsystem is larger than the spawning defect. |

## 5. Deciding findings

| Sev | Location | False-result mechanism | Fix class | Evidence |
|---|---|---|---|---|
| **P0** | inference:4-25, 27-41 | Binding look 96 estimates the first 96 heterogeneous means, while the estimand is all 384 fixed scenarios. | **Estimand/randomization/stopping redesign** | EXECUTED / SEARCHED |
| **P0** | state:18, 86-101; schemas:6 | `:` is legal inside IDs but also the ACT delimiter. `(S:A,B)` and `(S,A:B)` both encode `ACT:S:A:B`. | **Unambiguous composite-key encoding** | EXECUTED / UNSEARCHED—SETTLED-BY-PINNED-BYTES |
| **P0** | design:88-94; schemas:36-67; inference:4-10 | No A1 output schema and no mapping from three node scores to binary `BC_i`/`OM_i`. Literal implementations can produce different datasets. | **Normative scorer/output algebra** | READ-ONLY / UNSEARCHED—SETTLED-BY-PINNED-BYTES |
| **P1** | schemas:15-33, 69-92 | `condition:"BC"` reveals the arm; `fields` admits arbitrary text/config/unbounded arrays; valid packets can exceed 65,536 bytes. | **Schema closure and arm-blind rendering** | EXECUTED / SEARCHED |
| **P1** | schemas:69-77 | Declared outer key order contradicts JCS lexicographic order; `packet_hash` coverage is undefined/self-referential. | **Single canonicalization/hash definition** | EXECUTED / SEARCHED |
| **P1** | measurement:4-29, 35-40 | H×D CPU scans are absent from the catalog; a hotspot at H=10,000/D=64 is untested and passes. | **External instrumentation plus factorial coverage** | EXECUTED / SEARCHED |
| **P1** | measurement:52-64; design:80-84 | Config field names are restricted but their values have no schemas; `candidate_id`/`cache_mode` can carry precomputed gold. | **Typed config and freeze/provenance order** | EXECUTED |
| **P1** | design:58-62 | Eligibility can remove all hard cases before hash selection; target population is not defined independently of selection. | **Cohort estimand and exclusion audit** | EXECUTED / SEARCHED |
| **P1** | state:69-79; design:88-94 | Crash after receiving bytes but before durable response append permits “retry R2” or “R1 was accepted/missing.” | **Transactional request/response journal** | EXECUTED / SEARCHED |
| **P1** | inference:78-93 | Stored 0.8/0.9 vector centers disagree with `floor(p*n)/n` inputs at every look. | **Reference-fixture consistency** | EXECUTED |
| **P2** | test:14 | Pinned witness test exits 1 under PowerShell 5.1 because `ConvertFrom-Json -Depth` is unsupported. PowerShell 7 was installed but execution was access-denied. | **Harness runtime declaration/portability** | EXECUTED |

### Decisive inference witness

A legal deterministic heterogeneous sequence:

- First 96: 48 `(BC,OM)=(0,1)`, 48 `(1,1)`.
- Remaining 288: 38 `(1,0)`, 250 `(1,1)`.

At look 96:

- \(\bar\Delta=-0.5\), \(\bar{OM}=1\)
- \(\Delta_U=-0.162095<-0.1\), \(OM_L=0.831047\)
- literal branch: `MODEL_INTERFACE_FAIL`.

For the declared full 384 manifest:

- \(\bar\Delta=-10/384=-0.026042\)
- \(\bar{OM}=346/384=0.901042\)
- terminal branch if not stopped: `INCONCLUSIVE_OR_UNDERFUNDED`.

The Hoeffding arithmetic is correct for the prefix average. It does not cover the declared full-manifest mean under arbitrary heterogeneity. Sequential finite-population inference requires random without-replacement order or a different estimand; the opened paper explicitly assumes the fixed population is observed in uniformly random order. [Waudby-Smith & Ramdas, §§1.1 and 3](https://papers.nips.cc/paper_files/paper/2020/file/e96c7de8f6390b1e6c71556e4e0a4959-Paper.pdf).

A second executed sequence produced `MODEL_OR_INTERFACE_CEILING` at look 96 with 50/96 OM successes, despite a full-manifest OM mean of 338/384 = 0.8802.

## 6. Required attacks A–I

- **A — EXECUTED.** Independent decision oracle produced distinct results for TN useless/FD succeeds, all unbounded, H×D design failure, OM ceiling, BC inferiority, and inconclusive. Limitation: the bundle contains no executable decision program.

- **B — EXECUTED/READ-ONLY.** Parsed 17 event types and enumerated 289 ordered names. Zero pair fixtures, zero payload schemas, and no reducer exist, so 289/289 pair outcomes remain unexecutable. Fresh ACT collision proves non-totality.

- **C — EXECUTED / SEARCHED.** Independent structural validator accepted:

  - free-text reasoning and arbitrary config inside `objects[].fields`;
  - a nested 10,000-item array and unsafe nested integer;
  - `ABSTAIN` with proposed actions;
  - `PROPOSE` with an empty action list;
  - `NOT-A-DATETIMEZ` because Draft 2020-12 `format` is annotation by default.

  It correctly rejected a root extra property and unsafe `cut.journal_seq`. A schema-valid packet serialized to 70,501 bytes, making the 65,536-byte padding envelope impossible. JSON whitespace padding is syntactically valid, but operational provider handling remains unspecified. [JSON Schema format vocabularies](https://json-schema.org/draft/2020-12/json-schema-validation), [RFC 8259 §2](https://www.rfc-editor.org/info/rfc8259/), [RFC 8785 §§3.2.1–3.2.3](https://www.rfc-editor.org/info/rfc8785/).

- **D — EXECUTED / SEARCHED.** Multi-gold/no-gold cases were ineligible and a 63-case cohort failed loudly. In a generated 64-easy/16-hard world where BC validity excluded the hard cases, all 64 retained cases were easy. Hash input framing is unspecified: naïve concatenation makes `(A,BC)` and `(AB,C)` identical. FDA enrichment guidance is only an analogy, but confirms selection preserves conclusions for the selected population while changing applicability/generalizability. [FDA guidance §§II and VI.E](https://www.fda.gov/media/121320/download).

- **E — EXECUTED / SEARCHED.** Named H×D-linear red candidate failed. Fresh H=10,000/D=64 hotspot passed because that pair is not crossed. All registered counters can remain zero while CPU instructions grow as H×D; no CPU, cycle, allocation, or memory-touch counter exists. Numeric counter splitting of 4,000 read + 4,000 written bytes also passed individual and unit-total gates; no semantic-equivalence detector exists. SQLite documents indexed lookup as \(O(\log N)\), while operating systems and databases expose instruction/cache/buffer counters omitted here. [SQLite query planner](https://www.sqlite.org/queryplanner.html), [PostgreSQL `EXPLAIN BUFFERS`](https://www.postgresql.org/docs/18/sql-explain.html), [Linux `perf-stat`](https://man7.org/linux/man-pages/man1/perf-stat.1.html). Sparse crosses are screening, not exhaustive interaction coverage. [NIST factorial interactions](https://itl.nist.gov/div898/handbook/prc/section4/prc437.htm).

- **F — EXECUTED/READ-ONLY.** An allowed config with a 49,553-byte `candidate_id`, string `memory_budget_bytes`, negative checkpoint interval, and object-valued `cache_mode` passed the only name-based interpretation while carrying gold. Environment/module/path/timing/child witnesses could not run because no child sandbox, candidate, taint harness, or reconstruction implementation exists.

- **G — EXECUTED/READ-ONLY / SEARCHED.** Walked pre-acceptance, accepted/no-body, body-before-journal, journal-before-parse, writer-child, terminal, retry, rejection, and close windows. The body-before-journal window has two legal policies. SQLite’s crash-safe transaction machinery and AWS/Stripe server-side idempotency demonstrate the missing atomic boundary. [SQLite atomic commit and crash tests](https://sqlite.org/atomiccommit.html), [AWS idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/), [Stripe network-error semantics](https://docs.stripe.com/error-low-level).

- **H — EXECUTED / SEARCHED.** Re-derived radii exactly:

  - n=96: Δ `0.337905278990`, OM `0.168952639495`
  - n=192: Δ `0.238935114173`, OM `0.119467557086`
  - n=384: Δ `0.168952639495`, OM `0.084476319748`

  Six-way Bonferroni allocation sums to 0.05. All nine OC cells are nonnegative and sum to one. Enumerated all \(4^7=16,384\) completions for a seven-missing-pair boundary case: 9,908 inconclusive versus 6,476 fail, correctly yielding transport-inconclusive. Eight missing is terminal. The full-manifest/prefix target defect remains.

- **I — EXECUTED.** Derived:

  | Stop | Accepted calls | Reconstructions | Max attempts with one retry/node |
  |---:|---:|---:|---:|
  | 96 | 576 | 192 | 1,152 |
  | 192 | 1,152 | 384 | 2,304 |
  | 384 | 2,304 | 768 | 4,608 |

  Seven-of-384 missing implies per-call \(q\le0.003038\) by union bound. Zero failures in 1,000 gives one-sided exact 95% upper `0.002991`—pass—but a two-sided 95% construction gives `0.003682`—fail. The contract specifies neither CI method nor six-call mapping. Provider, endpoint, route, billing, and zero-paid-soak feasibility are absent. Current OpenAI documentation, as a non-governing comparator, says prompt caching is automatic for long exact prefixes and routing can depend on `prompt_cache_key`; therefore cache/route behavior must be provider-specific and cannot be presumed away. [Official OpenAI prompt-caching documentation](https://developers.openai.com/cookbook/examples/prompt_caching_201#11-basics).

## 7. Attack J — fourteen witnesses

| Witness | Declared closure | Alternative bypass | Status |
|---|---|---|---|
| CROSS_SCOPE_IDEMPOTENCY | scoped identity tuple | unconstrained `semantic_operation`; ACT delimiter collision | EXECUTED |
| UNSAFE_INTEGER_ALIAS | safe integer bounds/string rule | unsafe numbers and arrays inside open `fields` | EXECUTED |
| ACT_COMPLETION_ID_SUBSTITUTION | completion ID read from obligation | ambiguous ACT parsing targets two obligations | EXECUTED |
| INVALID_PROPOSAL_PATH_DIVERGENCE | reject exactly once | no rejection idempotency construction or status/action cross-rule | READ-ONLY |
| UNJOURNALED_A0_A1 | A0/B/A1 journal keys | received-body-before-append crash; invalid A0 has no transition | EXECUTED |
| MULTI_GOLD_GUESSING | exactly one gold + distractor | eligibility selects easy/trivial cases | EXECUTED |
| RENDER_ID_LEAKAGE | ID permutation/discriminator | literal `condition` reveals BC/OM | EXECUTED |
| CONFIG_PRECOMPUTED_PACKET | field allowlist/prohibition | allowed values and implementation bytes carry lookup table | EXECUTED |
| COUNTER_SPLIT | closed catalog/unit totals | 4,000+4,000 split passes; CPU absent | EXECUTED |
| HD_INTERACTION | crossed H and D | untested 10,000×64 hotspot | EXECUTED |
| IMPOSSIBLE_OC_CELL | explicit nonnegative cells | cells hold; target/stopping mismatch remains | EXECUTED |
| MISSING_OM_BRANCH_FLIP | joint \(4^m\) completion | invalid model output is not classified as missing/model failure | EXECUTED |
| PERIODIC_INDEX_AMBIGUITY | zero-based 0,10,20 | stored 0.8/0.9 vectors contradict floored inputs | EXECUTED |
| INFERENCE_IMPLEMENTATION_MISMATCH | independent evaluator | evaluator may faithfully match wrong vectors and wrong estimand | EXECUTED |

The repository test checks strings/field presence, not these semantics. Fresh execution exited 1 in the available PowerShell runtime before reaching its assertions.

## 8. Omission and bypass attack

- **Strong comparator omitted:** a concrete transactional relational baseline—append-only event table, indexed/materialized due queue, ACID writer/idempotency table—using SQLite or PostgreSQL. It fits FD/FC but is not frozen as a candidate.
- **Legal trace with two answers:** `(scope=S:A, obligation=B)` and `(scope=S, obligation=A:B)` both yield `ACT:S:A:B`.
- **False continuity pass:** H×D CPU scan or the untested 10,000×64 hotspot.
- **False kill:** an otherwise constant-bounded candidate that reads one extra 8-KiB metadata page after a threshold fails the 4,096-byte per-counter range despite remaining absolutely bounded.
- **False mechanism preference:** vectorized/in-memory O(H×D) computation is absent from counters and can appear Pareto-superior.
- **False model-usability:** direct `condition` disclosure permits arm-specific behavior.
- **False ceiling story:** executed prefix-low/full-manifest-high OM sequence above.
- **Bypass outside the fourteen:** delimiter collision in composite action IDs.
- **Mandatory no-paid test:** deterministic fake-provider Stage-2 run with crash injection at every request, response-journal, child-event, commit-terminal, teardown, and reconstruction boundary; assert one binary outcome, exact replay, and no resampling.
- **Mechanism to borrow:** SQLite transactional journal plus AWS/Stripe-style idempotency-key/request-parameter binding.
- **Delete:** inference:95-103 historical `confseq` source pins. The contract says they are not the primary r7 interval, so they cannot change a result.
- **Coordination boundary:** MBCX ends after one single-writer cold A0→B→writer→A1 episode. The later experiment begins when multiple independently scheduled agents or writers exchange, compete over, or jointly resolve obligations.

## 9. What would I build? — READ-ONLY / SEARCHED

A smaller instrument:

1. SQLite/PostgreSQL append-only event store with an ACID idempotency table and materialized/indexed due-obligation projection.
2. Generated, closed JSON Schemas with opaque or length-prefixed IDs, one JCS definition, and an explicit hash preimage.
3. Condition-blinded rendered messages, exact frozen instructions, exact output schemas, and one normative scorer mapping A0/B/A1 to the binary pair outcome.
4. Full H×D measurement grid initially; external process/DB counters for bytes, pages, records, instructions, cycles, allocations/RSS, cache misses, and child/background work.
5. Deterministic fake-provider crash campaign before any model call.
6. Either terminal-only n=384 inference, or a genuinely randomized without-replacement order and finite-population confidence sequence.

Prior art: [event sourcing/CQRS](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing), [PostgreSQL indexed materialization](https://www.postgresql.org/docs/current/rules-materializedviews.html), [SQLite transactions](https://sqlite.org/atomiccommit.html), [finite-population confidence sequences](https://papers.nips.cc/paper_files/paper/2020/file/e96c7de8f6390b1e6c71556e4e0a4959-Paper.pdf), [RAG](https://papers.nips.cc/paper_files/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html), and [blackboard systems](http://mas.cs.umass.edu/pub/paper_detail.php/218). **SEARCHED.**

## 10. Would I design it differently? — READ-ONLY

Yes. I would adopt transactional persistence and standard instrumentation, remove the universal “complete/closed/prevent” claims, freeze the scorer before cohort generation, make arm identity invisible, run a full factorial mechanical stage, and defer all early inferential stopping until a valid population-level sampling design exists.

## 11. Sweep log

- **Sequential finite population.** Queries: `site:projecteuclid.org Hoeffding probability inequalities sums sampling without replacement finite population`; `confidence sequences sampling without replacement finite population arXiv Waudby-Smith Ramdas`. Opened NeurIPS paper §§1.1, 3. It changed C10 from “formula plausible” to FALSE because its governing model requires random order. Stopped after a primary paper directly settled the mechanism.

- **Eligibility/selection.** Queries: `site:fda.gov guidance enrichment strategies clinical trials eligibility selection target population generalizability`; `site:nih.gov eligibility criteria selection bias target population generalizability trial guidance`. Opened final FDA guidance §§II, VI.E, VII. Confirmed enrichment changes applicability and must be reported. Stopped because this is analogous evidence, not regulatory authority here.

- **Counters/index/interactions.** Queries: `site:sqlite.org/queryplanner.html binary search logN index official`; `site:postgresql.org/docs/current sql-explain buffers shared hit read write official`; `site:man7.org perf-stat hardware events instructions cache-misses official Linux man`; `site:itl.nist.gov factorial design interaction effects NIST handbook`. Opened SQLite query planner, PostgreSQL EXPLAIN, perf-stat, NIST two-way ANOVA/fractional factorial sections. Confirmed the catalog omits standard physical counters and sparse crosses cannot establish arbitrary interaction closure. Stopped after primary documentation covered cost and design.

- **JSON/JCS/render.** Queries: `site:json-schema.org draft 2020-12 format annotation assertion validation official`; `RFC 8785 JSON Canonicalization Scheme property sorting whitespace RFC Editor`; `RFC 8259 JSON whitespace after value RFC Editor`. Opened JSON Schema §7.2, RFC 8785 §§3.2.1–3.2.3 and status, RFC 8259 §§2,4. Confirmed format is annotation by default, JCS sorting conflicts with the declared order, and trailing space is legal JSON. RFC 8785 is Informational; RFC 8259 is Internet Standard. Stopped because the standards directly settled interoperability.

- **Durability/idempotency.** Queries: `site:aws.amazon.com/builders-library making retries safe with idempotent APIs official`; `site:docs.stripe.com/api idempotent requests same result 500 official`; `site:sqlite.org atomiccommit.html SQLite atomic commit rollback journal crash`; `site:docs.temporal.io workflow execution event history durable replay crash official Temporal`. Opened AWS atomic idempotency section, Stripe network/server errors, SQLite atomic commit/crash testing, Temporal overview. Confirmed the bundle names desired properties without supplying the transactional mechanism. Stopped after three independent primary implementations agreed on the missing boundary.

- **Memory/prior art.** Queries: `Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks NeurIPS 2020 paper`; `Hearsay-II speech understanding system blackboard architecture primary paper pdf`; `site:learn.microsoft.com architecture event sourcing pattern append-only store materialized views official`; `site:postgresql.org/docs current materialized views indexes official`. Opened NeurIPS RAG, UMass blackboard publication, Microsoft Event Sourcing, PostgreSQL 18. Confirmed components are already built; found no single existing product for the full MBCX scientific question. Stopped when every named baseline class had a primary origin/current implementation.

- **Provider behavior.** Query: `prompt caching structured outputs routing` in official OpenAI documentation. Opened Prompt Caching 201 §1.1. Confirmed caching/routing is provider-specific and automatic in at least one current provider. Applicability remains undetermined because the bundle names no provider/route. Stopped because further provider comparison cannot govern an unnamed endpoint.

## 12. Residual risks and non-claims

Residuals even after the blocking classes are repaired:

- finite H/D tests do not prove behavior outside the grid;
- provider calls may be dependent through cache, route, outages, or backend state;
- exactly-one-gold tasks may not represent multi-obligation continuity;
- FD/FC/TN is a reporting taxonomy, not a proven exhaustive ontology;
- OS/database counters are platform-specific and noisy;
- no production counterpart, candidate, reducer, renderer, scorer, sandbox, or transport implementation exists to test differentially.

I make no production, security, concurrent-writer, cross-model, personality, procedural-memory, or coordination-stage claim.

## 13. Capability, side effects, and cleanup

Web access and primary-source retrieval worked. Node-based in-memory execution worked. Windows PowerShell 5.1 ran but could not execute the pinned witness script because of its unsupported `-Depth` parameter; installed PowerShell 7 was access-denied.

Git status after review was byte-for-byte identical to initial status. No files were created, edited, committed, labeled, pushed, or merged. No paid inference occurred. No cleanup is required.
