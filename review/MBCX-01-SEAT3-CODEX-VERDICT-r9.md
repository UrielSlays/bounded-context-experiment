# NO-GO — the instrument has reachable false-green paths in packet validation, scoring, state semantics, and physical-work accounting

**Verdict basis:** EXECUTED. These are implementation blockers, not requests for methodological polish. A legal worker output cannot be validated by the pinned Ajv runtime; the scorer can declare success without seeing A0 and even on schema-invalid B; both state engines accept semantically forged identities and invalid-time corrections; and archive-linear work hidden in a child process passes the physical gate.

## Seat identity and posture

- Seat: independent Moonwalker Codex EXEC reviewer.
- Role: adversarial, byte-first, read-only.
- Model/checkpoint: OpenAI Codex, GPT-5 family; exact serving checkpoint is not exposed to this seat.
- Harness: Windows PowerShell, Git object database, Python 3.11, Node.js 24.17.0, pinned Ajv 8.20.0 closure, local numerical probes, and primary-source web access.
- Posture: fresh first pass; no earlier-seat reports used.
- Lateral seal: maintained. A Git tree metadata listing exposed that historical seat-named files exist, but I did not open, read, cite, or inspect any other seat’s verdict, browser output, stdout, stderr, or completion marker.
- Paid inference: **NONE**. No provider/model calls and no FD/FC/TN implementation.

## Build-decision challenge

### 1. ALREADY-BUILT?

**READ-ONLY; SEARCHED.**

The complete Moonwalker experiment is not a single off-the-shelf product, but several major mechanisms already exist and should be adopted:

| Bundle surface | Existing mechanism to adopt |
|---|---|
| Durable/atomic state | SQLite transactions and rollback/WAL semantics |
| Retry/unknown acceptance | Stripe/AWS-style idempotency tokens bound to request parameters |
| Packet syntax/canonical bytes | JSON Schema 2020-12, strict Ajv, RFC 8785/JCS |
| Frozen benchmark execution | MLPerf/LoadGen-style deterministic trace, checksums, auditability, and test-data separation |
| Windows descendant accounting | Job Objects with child-process aggregation and breakaway control |
| Long-running orchestration, if actually needed | Temporal durable execution—but this experiment does not yet justify adopting the whole platform |

I searched the pinned repository for a production counterpart and found only the reference engine, direct oracle, contracts, and verifier. No actual production FD/FC/TN implementation exists at the pin.

Conclusion: build the domain-specific scientific comparison, but adopt the durability, idempotency, schema, canonicalization, benchmark, and process-accounting primitives. Do not build bespoke substitutes for them.

### 2. PRODUCT-FIT?

**READ-ONLY; UNSEARCHED — SETTLED-BY-PINNED-BYTES.**

Customer need, in one sentence:

> Let an owner learn whether exact due-obligation continuity fits within a finite physical budget and whether bounded continuity preserves useful model behavior, while reporting unverifiable cases loudly and leaving spend and promotion decisions to the owner.

That need fits GOVERNED POWER / FAIL-LOUD / MIRROR-NOT-COP. The current bytes do not: they contain silent false-green paths, and several “prevent/leaves no choice/yield one answer” claims exceed what the executable gates establish.

### 3. BIGGER-THAN-THE-BUG?

**READ-ONLY; UNSEARCHED — SETTLED-BY-PINNED-BYTES.**

Yes. Five contracts/design artifacts, two state engines, an Ajv closure, a verifier, an inference engine, a cohort generator, a physical counter framework, and a route-reliability gate constitute a new scientific subsystem. This is bigger than a leaf repair.

The present council review is the correct design-gate re-entry, so the procedural problem is now being addressed. Owner authorization is still required before implementation or paid execution.

## Pin and byte verification

The governing commit is `f8fa75647f702dcc14f91b2d974ed1497aeef400`. Current HEAD at final check was newer, `a227948d7e86b39ff9b4c9a57068b7fae7dc72b2`, but the ten reviewed working-tree files all matched the pinned Git objects byte-for-byte. Therefore there was no byte conflict among the reviewed artifacts; the owner-pinned commit governs.

**EXECUTED:** raw `git cat-file blob` reconstruction, independent SHA-384, byte count, LF count, JSON parse, and working-tree comparison.

| Artifact | Blob | Bytes / LF lines | Result |
|---|---|---:|---|
| `MBCX-01-EXPERIMENT-DESIGN-r8.md` | `24e2b230cc2e293cbe6bd7e6dd37100c680b9ff1` | 19,867 / 180 | exact; SHA-384 `5A690C…E7DA3` |
| `MBCX-01-STATE-ACTION-CONTRACT-v4.json` | `9efb8dbca72542db522ded09269cae332e396def` | 16,328 / 173 | exact; `16B89F…199CD` |
| `MBCX-01-PACKET-SCHEMAS-v3.json` | `a42be28546bf213d237adf306d2e0a8758ad2d52` | 14,674 / 161 | exact; `E48B69…0398C` |
| `MBCX-01-MEASUREMENT-CONTRACT-v3.json` | `bf9dab5500beb49b6ed3a51e90661e76dc530dec` | 9,551 / 115 | exact; `A96ED1…090A0D` |
| `MBCX-01-INFERENCE-CONTRACT-v4.json` | `6d649433d5e36db3a81c3ecc7ec86e43f8d5ce8f` | 11,390 / 147 | exact; `F53748…BB7DB` |
| `mbcx01_r9_oracle.py` | `76560dd49cbc225d36ca9090aae26efd8b7493ce` | 16,681 / 368 | exact; `34A795…4706A` |
| `mbcx01_r9_reference.py` | `170f7d2c2815c4f2d78f2c75ea5c58b4442d0fa9` | 66,936 / 1,394 | exact; `6DA111…448A37` |
| `verify-r9-normative-bundle.py` | `ecac64be665a05f6c47d2b4ed828dd9d4118004d` | 22,271 / 507 | exact; `88E157…09D8` |
| `verify-r9-schema-ajv.mjs` | `4ffd38bd67147ad475309e1eefd0de3795d714ed` | 3,659 / 78 | exact; `37FB06…4372C` |
| `MBCX-01-R9-NO-PAID-VERIFICATION.json` | `6c0f66a0d96501e6d687a3bad72e5a00e140e40c` | 15,537 / 429 | exact; `329400…EDC25` |

All four JSON contracts and the retained report parsed. Ajv 8.20.0 and its four pinned dependencies authenticated.

Fresh full verifier result:

```text
state: PASS
packets: PASS
cohort: PASS
measurement: PASS
inference: PASS
integration: PASS
```

Exit code was zero. That PASS does not survive the attacks below.

Evidence read completely:

- `MBCX-01-EXPERIMENT-COUNCIL-PACKET-r9.md:1`
- `<vault>`
- `MBCX-01-EXPERIMENT-DESIGN-r8.md:1@f8fa756…` through line 180
- `MBCX-01-STATE-ACTION-CONTRACT-v4.json:1@f8fa756…` through line 173
- `MBCX-01-PACKET-SCHEMAS-v3.json:1@f8fa756…` through line 161
- `MBCX-01-MEASUREMENT-CONTRACT-v3.json:1@f8fa756…` through line 115
- `MBCX-01-INFERENCE-CONTRACT-v4.json:1@f8fa756…` through line 147
- `mbcx01_r9_oracle.py:1@f8fa756…` through line 368
- `mbcx01_r9_reference.py:1@f8fa756…` through line 1,394
- `verify-r9-normative-bundle.py:1@f8fa756…` through line 507
- `verify-r9-schema-ajv.mjs:1@f8fa756…` through line 78
- `MBCX-01-R9-NO-PAID-VERIFICATION.json:1@f8fa756…` through line 429

## Applicability and exclusions

- The Chugg–Ramdas result applies to bounded, adapted observations and average conditional means; it supports the registered mathematical estimands.
- FDA/EMA noninferiority guidance is analogical assurance-design evidence, not regulatory authority over this internal experiment.
- MLCommons/NIST sources are benchmark prior art, not mandatory rules.
- Microsoft Job Objects are directly applicable to the current Windows harness; another platform needs an equivalent descendant-accounting primitive.
- Current OpenAI documentation was reviewed only as provider-practice and price evidence. The packet does not freeze OpenAI—or any other named provider—so those documents do not bind the future route.
- This verdict does not adjudicate actual FD/FC/TN exactness, boundedness, performance, or model quality because those implementations/results do not exist at the pin.

## C1–C12 scoreboard

| Claim | Ruling | Basis |
|---|---|---|
| C1 decomposition | **FALSE** | EXECUTED: absolute resource caps can kill genuinely H-independent work, while child archive-linear work passes; scorer also merges interface/model conclusions after omitting A0. |
| C2 state totality | **FALSE** | EXECUTED: forged action identity, ineffective-time correction, and forged handoff hashes are accepted. |
| C3 executable independence | **FALSE** | EXECUTED: reference and oracle agree on the same false premise; existing mutants omit action-hash identity. |
| C4 packet validity | **FALSE** | EXECUTED: WorkerHandoff schema cannot compile; semantic manifest substitution and A0 omission remain. |
| C5 cohort provenance | **FALSE** | EXECUTED: unretained global duplicates and unknown motifs pass; retention size is internally contradictory. |
| C6 physical boundedness | **FALSE** | EXECUTED: child `10H` instructions pass; a constant 4,000,000-instruction candidate is killed. |
| C7 reconstruction/isolation | **UNDERDETERMINED** | READ-ONLY: future harness gates are declarations; no candidate harness executes causal source binding or isolation. |
| C8 serial DAG/recovery | **FALSE** | EXECUTED/READ-ONLY: forged handoff linkage passes, and no executable top-level recovery/decision reducer exists. |
| C9 engineering fairness | **UNDERDETERMINED** | READ-ONLY: no exactness-filter/Pareto executor or candidate results exist; current gates permit false physical preference. |
| C10 inference | **HOLDS** | EXECUTED + SEARCHED: theorem premises, transform, alpha split, strict endpoints, and numerical implementations checked. |
| C11 power/missingness/reliability/cost | **FALSE** | EXECUTED: a registered practical cell has 8.71% decision probability; missingness is not implemented; route denominator/modes are open. |
| C12 smallest decisive instrument | **FALSE** | EXECUTED/READ-ONLY: `n=768` is not decisive for a practical registered alternative, and the 48-cell route gate has a much smaller direct replacement. |

## Findings

### P0 — WorkerHandoffV3 is not executable under the pinned strict validator

**EXECUTED; SEARCHED.**

- Location: `MBCX-01-PACKET-SCHEMAS-v3.json:112-119`, `verify-r9-schema-ajv.mjs:73`, `mbcx01_r9_reference.py:677-688`, `verify-r9-normative-bundle.py:162-168`.
- Input: schema-valid-looking `WorkerHandoffV3` with `status_code=PROPOSE` and one proposed action.
- Output:

```text
Error: strict mode: missing type "array" for keyword "minItems"
at "#/allOf/0/then/properties/proposed_action_ids" (strictTypes)
```

Node exited 1; the Python wrapper then produced `JSONDecodeError` because stdout contained no result.

The full verifier compiles only `DecisionPacketV3`, so it reports `packets: PASS`.

Ajv’s official strict-mode documentation confirms that strict mode deliberately throws on schemas with non-applicable keyword types. [Ajv strict types](https://ajv.js.org/strict-mode.html#strict-types-stricttypes-option)

- False result: the experiment can report its packet layer ready even though no B output can pass the specified validator.
- Repair class: **ALL-SCHEMA-COMPILATION-AND-RUNTIME-CLOSURE GATE**. Compile and adversarially validate every schema, including conditional branches, before any readiness report.

### P0 — The success scorer does not receive A0 and accepts schema-invalid B

**EXECUTED; UNSEARCHED — SETTLED-BY-PINNED-BYTES.**

- Location: `MBCX-01-EXPERIMENT-DESIGN-r8.md:81`, `MBCX-01-PACKET-SCHEMAS-v3.json:154-159`, `mbcx01_r9_reference.py:751-760`, `verify-r9-normative-bundle.py:223-229`.
- The registered condition requires correct A0, singleton B, writer commitment, and exact A1.
- `score_condition` has no A0 argument.
- A WorkerHandoff with an illegal extra `TAINT` property returned `1` when B/writer/A1 named the target.
- A deliberately wrong A0 cannot affect the result because it cannot be supplied.

- False result: conditional model usability can be declared on a trace that the registered definition scores zero.
- Repair class: **END-TO-END-CONDITION-BINDING**. The scorer must consume validated A0, validated B, the writer receipt, and validated A1, all bound to expected packet/action hashes.

### P0 — Both state engines accept semantically forged events

**EXECUTED; UNSEARCHED — SETTLED-BY-PINNED-BYTES.**

Locations include:

- Action identity declaration: `MBCX-01-STATE-ACTION-CONTRACT-v4.json:62`
- Open payload: `MBCX-01-STATE-ACTION-CONTRACT-v4.json:104-106`
- Reference envelope/effects: `mbcx01_r9_reference.py:157-189`, `238-282`, `337-403`
- Oracle envelope/effects: `mbcx01_r9_oracle.py:51-78`, `135-198`, `258-329`

Executed witnesses:

- Forged `completion_action_id` for `OBL.FRESH`: both engines returned `APPLIED` and stored the forgery instead of enforcing the deterministic action hash.
- A fact effective from `2026-09-01` was “corrected” at `2026-08-13`; both engines created `valid_to < valid_from`.
- A handoff with an arbitrary `originating_cut_hash` was accepted.
- A proposal with an arbitrary `worker_handoff_hash` was accepted.
- Calendar-invalid `2026-99-99T99:99:99.999999Z` was accepted.
- Control: a fresh four-node dependency cycle was correctly rejected and left state unchanged.
- All 17 declared legal fixtures agreed across engines.

The two implementations therefore share false premises. The existing six mutants do not cover deterministic action identity.

- False result: state exactness, correction/restoration, and handoff provenance can green on different semantic histories.
- Repair class: **SEMANTIC-IDENTITY, EFFECTIVE-TIME, AND HASH-LINK GUARDS**, plus an `ACTION_ID_HASH_GUARD` mutant.

### P0 — Physical accounting permits an archive-linear false pass and a constant-work false kill

**EXECUTED; SEARCHED.**

- Location: `MBCX-01-MEASUREMENT-CONTRACT-v3.json:51-73`, `mbcx01_r9_reference.py:929-998`.
- Baseline and all 100 H-D-F cells recomputed successfully.
- All seven provided red candidates were rejected.
- Fresh evasion: set `CHILD_CPU_INSTRUCTIONS = 10H`, leaving `PROCESS_CPU_INSTRUCTIONS` unchanged. Across the registered H range, the evaluator returned `[]`.
- Fresh low-slope evasion: root `PROCESS_CPU_INSTRUCTIONS = 500000 + 4H` also returned `[]`.
- Fresh false kill: a candidate with constant `PROCESS_CPU_INSTRUCTIONS = 4,000,000`, zero H range, was rejected solely by `UNIT_TOTAL_LIMIT`.

Only the root process instruction counter receives the H-shape gate. The evaluator trusts the booleans `descendant_accounted` and `unregistered_work`; it does not establish them.

Windows Job Objects already aggregate child-process accounting, while explicitly documenting breakaway exceptions. [Microsoft Job Objects, process trees and accounting](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)

- False result: an H-linear archive walk can pass by moving into a child, while genuinely H-independent work can be labeled continuity failure.
- Repair class: **DESCENDANT-AGGREGATE SHAPE GATE** plus **CONTINUITY/AFFORDABILITY SEPARATION**. Shape-test the same-unit process-tree aggregate; report absolute budget separately.

### P1 — Semantic packet validation is not bound to the expected experiment manifest

**EXECUTED; UNSEARCHED — SETTLED-BY-PINNED-BYTES.**

- Location: `mbcx01_r9_reference.py:691-748`.
- All were rehashed into self-consistent packets and returned no semantic errors:
  - invented schema-valid `FACT.INJECTED` absent from canonical world;
  - altered cut time;
  - altered `scenario_id`;
  - altered top-level observation scope/time/code.
- The validator checks a canonical object only when one happens to exist. It receives no expected scenario, cut, observation, or manifest.
- It correctly rejected a forged catalog action and unresolved prerequisite, showing the bypass is narrower than “validator does nothing.”
- `UtcTime` also accepts calendar-invalid values because it is a shape regex, not semantic UTC validation.

- False result: BC and OM can receive different experiment identities or observations while both are reported valid.
- Repair class: **EXPECTED-MANIFEST SEMANTIC BINDING** and **CALENDAR-VALID UTC FORMAT CHECK**.

### P1 — Builder/cohort provenance permits unequal actions and hidden global duplication

**EXECUTED; SEARCHED.**

- Location: `mbcx01_r9_reference.py:642-674`, `799-832`; `MBCX-01-MEASUREMENT-CONTRACT-v3.json:81-96`.
- With the same actions, BC selected `OBL.DECOY`, `OBL.PREREQ`, `OBL.SHARED`, `OBS.SHARED`; OM additionally selected the dependency. This demonstrates distinct object-ID sources.
- Passing all three actions to BC but only target plus `NO_ACTION` to OM produced two schema- and semantic-valid packets with unequal action universes.
- An unretained cross-motif duplicate scenario ID was accepted because global uniqueness is checked only after selection.
- An extra unknown motif scenario was silently ignored.
- A supplied `eligible=False` was ignored and the row retained, which is good against Boolean poisoning.
- Duplicate cut IDs, motif crossover, and 127-per-motif shortfall were correctly rejected.
- Contract line 88 says retain 128 per motif; line 93 says retain the first 64.

MLCommons treats checksums, fixed reference preprocessing, deterministic seeds, and train/test separation as executable benchmark controls, not prose-only promises. [MLCommons training rules, §§6.1, 6.5, 6.6](https://github.com/mlcommons/training_policies/blob/master/training_rules.adoc)

- False result: a hidden duplicate or unequal action presentation can contaminate a paired comparison without triggering a gate.
- Repair class: **GLOBAL-PRESELECTION PROVENANCE INVARIANTS**, **SHARED-ACTION-MANIFEST CAPABILITY**, and **CONTRACT COHERENCE**.

### P1 — `n=768` leaves a practical registered alternative overwhelmingly inconclusive

**EXECUTED; SEARCHED.**

- Location: `MBCX-01-INFERENCE-CONTRACT-v4.json:81-108`; `MBCX-01-R9-NO-PAID-VERIFICATION.json:263-275`.
- Retained 10,000-replicate powers at the four assurance targets reproduced: `0.9430`, `0.9972`, `0.9984`, `0.9976`.
- But registered `DELTA_NEG25_OM85` produced the correct interface-fail decision only 871/10,000 times: **8.71%**, leaving 91.29% inconclusive.
- This is not an exact-threshold case: Δ is 15 percentage points beyond the −0.10 margin and OM is 5 points above the 0.80 floor.
- Reviewer-owned deterministic sizing for that cell:
  - `n=768`: 8.0%
  - `n=1,024`: 19.6%
  - `n=1,536`: 51.3%
  - `n=2,048`: 78.5%
  - `n=2,304`: 86.95%
  - `n=2,560`: 92.45%
  - `n=2,688`: 94.6%

FDA and EMA both separate the choice of a meaningful noninferiority margin from adequate power; a small study is not repaired by widening the margin. [FDA guidance, sample size section](https://www.fda.gov/media/78504/download), [EMA margin guideline, pp. 3–4](https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-choice-non-inferiority-margin_en.pdf)

- Avoidable indecision: the experiment can consume 4,608 calls and remain nearly unable to identify a plainly inferior BC condition that still clears the OM floor.
- Repair class: **ASSURANCE-TARGET COMPLETION AND SAMPLE RESIZING**. Either owner-rule this cell outside the practical target set, or expand the frozen population to at least 2,560 retained pairs and validate the resulting 15,360-call design. `2,560` is the smallest tested value clearing 90%, not a proof of the mathematical minimum.

### P1 — The claimed Git-only reconstruction gate is absent at the pin

**EXECUTED; UNSEARCHED — SETTLED-BY-PINNED-BYTES.**

- Location: `MBCX-01-EXPERIMENT-COUNCIL-PACKET-r9.md:29`; `verify-r9-normative-bundle.py:44-48`, `486-489`.
- `test-r9-normative-bundle.ps1` is not a Git object at `f8fa756…`.
- In a temporary reconstructed bundle, I inverted a load-bearing state guard. Running the verifier on that mutated directory still returned `state: PASS`.
- The verifier calculated and reported the new SHA-384 but did not compare it against the owner-pinned digest.
- Therefore report self-consistency is not pin enforcement.

- False result: a stale or substituted semantic artifact can produce a fresh green report.
- Repair class: **OWNER-PINNED MANIFEST ENFORCEMENT** performed before import/execution, with a committed Git-object-only wrapper.

### P1 — The route-soak gate conditions away failures and omits an OTHER class

**EXECUTED/READ-ONLY; SEARCHED.**

- Location: `MBCX-01-EXPERIMENT-DESIGN-r8.md:154-160`; `MBCX-01-INFERENCE-CONTRACT-v4.json:118-130`; `mbcx01_r9_reference.py:1261-1319`.
- Arithmetic reproduced:
  - `0.05/(6×8) = 0.0010416667`
  - `0.02/(6×8) = 0.0004166667`
  - minimum zero-failure trials per position: `16,478`
  - zero-failure upper: `0.000416646598`
  - at `16,477`: `0.000416671879`
  - one failure at `16,478`: `0.000557463`
  - total calls: `6 × 16,478 = 98,868`
- Bonferroni remains valid under dependence. The arithmetic is sound.
- The design describes “accepted route-soak calls”; conditioning on acceptance excludes DNS, connection, authentication, safety refusal, and some client/request failures from the denominator.
- The eight named modes have no `OTHER/UNCLASSIFIED`.
- No route collector or executable mode classifier exists.
- Current OpenAI documentation says safeguards can block or refuse legitimate requests, illustrating a real unregistered path; it does not bind the unspecified future provider. [OpenAI current model guide, safeguards](https://developers.openai.com/api/docs/guides/latest-model)

- False result: readiness can green while an omitted pre-acceptance route failure erases paired outcomes.
- Repair class: **ATTEMPT-DENOMINATOR, OTHER-MODE, AND ROUTE-RECEIPT CLOSURE**.

### P2 — Contract coherence and semantic formats remain non-total

**EXECUTED; UNSEARCHED — SETTLED-BY-PINNED-BYTES.**

- `MBCX-01-MEASUREMENT-CONTRACT-v3.json:88` says 128 retained per motif; line 93 says first 64.
- State and packet `UtcTime` patterns accept impossible calendar times.
- No executable renderer, fixed padding mechanism, or served-input hash binds what a provider would receive; `mbcx01_r9_reference.py:745-747` checks only unpadded canonical byte length.

Repair classes: **NORMATIVE-CONTRACT COHERENCE**, **SEMANTIC-DATETIME VALIDATION**, and **BYTE-EXACT RENDER/RECEIPT BINDING**.

No P3 finding changes the verdict.

## Required attacks A–J

### A — Git reconstruction

**EXECUTED.**

- Input: all ten paths at `f8fa756…`.
- Method: raw Git blobs, independent byte/LF/SHA-384 checks, JSON parse, Ajv closure validation, temporary reconstruction, and compact full verifier.
- Output: all pins exact; full verifier exit 0. Stale semantic substitution also passed.
- Interpretation: object reconstruction works when performed manually; the pinned bundle does not contain the claimed enforcing wrapper.
- Limitation: the built-in verifier’s PASS cannot establish properties it never attacks.

### B — State differential

**EXECUTED.**

- Input: all 17 declared effects, existing mutants, a fresh four-node cycle, forged action ID, future-ineffective correction, calendar-invalid time, forged originating cut, and forged worker-handoff hash.
- Output: declared fixtures agreed; cycle rejected; all four semantic forgeries accepted by both engines.
- Interpretation: differential agreement shares false premises and is not totality evidence.
- Limitation: no production state engine exists for a three-way differential.

### C — Packets and scoring

**EXECUTED.**

- DecisionPacket/A0/Task/A1: valid forms compiled; extra/missing/wrong discriminator rejected; 65 objects and 17 actions rejected; unsafe integers rejected.
- WorkerHandoff: strict compilation crashed.
- Impossible calendar times passed.
- Invented world object, altered cut/scenario/observation, and tainted B passed the relevant semantic/scoring layers.
- Non-target and multi-target B returned zero.
- Interpretation: syntax closure and experimental identity are not end-to-end.
- Limitation: no paid provider output was sampled.

### D — Builders and cohort

**EXECUTED.**

- Independent object selections were demonstrated.
- Shared action universe was not enforced.
- Chosen-cut eligibility, duplicate cut rejection, motif crossover, and shortfall worked.
- Unknown motifs and unretained global duplication passed.
- Frozen source hashes, seed secrecy, and post-freeze source immutability are not executable.
- Interpretation: partial builder independence exists, but provenance closure does not.

### E — Physical work

**EXECUTED.**

- All 100 cells and unit totals recomputed.
- Supplied red candidates rejected.
- Fresh child `10H`, root `500000+4H`, and constant-work witnesses run.
- Output: two false passes and one false kill.
- Interpretation: the closed-counter claim is false.
- Limitation: filesystem/cache/DB/page/memory accounting is synthetic data evaluated by the oracle, not measured OS activity.

### F — Theorem and numerics

**EXECUTED; SEARCHED.**

- Opened Proposition 3.1 at the primary paper.
- Checked bounded `X_t∈[0,1]`, heterogeneous/adapted average conditional means, predictable estimates, κ>0, normalizer, mixture inequality, inversion, clipping, strict endpoints, Δ transform, α=.025 per stream, union bound, and uniform limit.
- Analytic, Simpson, and Decimal implementations agreed.
- Reviewer-owned adaptive Simpson produced threshold `25.064694985704577`, boundary `11.030173853092123`, and mapped half-width `0.028724411075760736`.
- Interpretation: C10’s mathematics holds.
- Limitation: the source is a current arXiv preprint, not a product standard. [Chugg–Ramdas, Proposition 3.1](https://arxiv.org/pdf/2512.21300)

### G — Sample size and OC

**EXECUTED.**

Compact 2,000-replicate reproduction:

| n | Ceiling | Δ −.20 | Low discordance | Equal |
|---:|---:|---:|---:|---:|
| 384 | .4115 | .5160 | .6980 | .5660 |
| 512 | .6760 | .8715 | .9105 | .9060 |
| 768 | .9350 | .9975 | .9955 | .9980 |
| 1024 | .9950 | 1.0000 | 1.0000 | 1.0000 |

The retained 10,000-replicate values reproduced. Framing, categorical boundaries, fixed positions, and threshold-inconclusive behavior were checked.

Interpretation: `n=768` is the smallest of the four tested sizes meeting the selected four-target assurance set, but that target set omits a practically separated registered cell.

### H — Missingness and reliability

**EXECUTED/READ-ONLY.**

- No pinned missingness implementation exists.
- Reviewer-owned exact enumeration:
  - 0 missing: 1 completion;
  - 1 missing pair: 4 completions;
  - 7 missing pairs: 16,384 completions;
  - 8 missing pairs: immediate transport inconclusive.
- Reliability arithmetic reproduced exactly.
- Failure dependence does not invalidate Bonferroni; missing denominator/mode closure does.
- Interpretation: the missingness rule is computable but not delivered; the reliability contract measures the wrong conditional population.

### I — Decisions and cost

**EXECUTED/READ-ONLY.**

The scientific decision function returned:

- low OM upper bound → `MODEL_OR_INTERFACE_CEILING`
- Δ wholly below margin with OM floor → `MODEL_INTERFACE_FAIL`
- Δ wholly above margin with OM floor → `PROMOTE_TO_COORDINATION_STAGE`
- threshold overlap → `INCONCLUSIVE_OR_UNDERFUNDED`

Arithmetic: `6×768 = 4,608` scientific calls; `2×768 = 1,536` reconstructions.

No executable top-level reducer traces candidate exact/bounded success, all-candidate failure, transport failure, and design failure together. Those branches exist only as prose/string-presence integration checks.

Interpretation: scientific branching exists; experiment-level precedence is not executable.

### J — Deletion and boundary

**READ-ONLY.**

- Artifact to remove from the minimal instrument: `MBCX-01-R9-NO-PAID-VERIFICATION.json`. Retain it outside the instrument as a derived build receipt; do not make a self-reported PASS artifact part of the mechanism it claims to validate.
- Missing no-paid test: one end-to-end red gate that compiles all five schemas and runs wrong A0, tainted B, substituted manifest/hash, and child-`10H` work through the actual top-level decision path.
- Exact later boundary: this experiment ends after a single serial cold A0→B→writer→A1 pair. Concurrent writers, multiple agents, cross-episode persistence, negotiation, delegation, and coordination effectiveness belong to the later coordination experiment.

## Orthogonal-method answers

1. **HELPFUL — EXECUTED; SEARCHED.** Proposition 3.1 covers the registered heterogeneous average-conditional-mean estimands. The `.025/.025` split gives `.05` family error without independence.

2. **HELPFUL WITH A NAMED FIX — EXECUTED; SEARCHED.** The 100 cells cover the finite H-D-F grid, but a legal implementation evades the gates through child work. Fix class: shape-test aggregate descendant work and separate H-independence from affordability.

3. **HELPFUL WITH A NAMED FIX — EXECUTED.** Two engines are useful but share action/time/hash blind spots. The smallest stronger oracle is not a third handwritten reducer; it is a declarative guard/effect relation that independently checks identities, temporal intervals, cut hashes, and postconditions, then property-generates traces against both engines.

4. **HELPFUL WITH A NAMED FIX — EXECUTED; SEARCHED.** `n=768` answers the selected four power targets but not the practical `Δ=-.25, OM=.85` cell. The tested alternative is at least `n=2,560`, requiring 15,360 model calls and an expanded frozen cohort, unless the owner explicitly removes that cell from the practical assurance target.

5. **HELPFUL WITH A NAMED FIX — EXECUTED.** The real need is the probability that a six-call pair becomes unusable, not 48 separately powered labels. With a direct pair-level Bernoulli failure event, zero failures in 149 attempted complete pairs gives one-sided 95% upper bound `0.0199048`, preserving the 2% guarantee with at most 894 calls. Mode/position labels can remain diagnostics rather than separately multiplicity-budgeted gates. This requires an attempted-pair denominator and `OTHER`.

## WHAT WOULD I BUILD?

**READ-ONLY.**

I would build a smaller instrument:

1. A SQLite-backed append-only journal and indexed projection, using transactions for writer atomicity and constraints for deterministic identity. **SEARCHED:** SQLite already specifies crash/power-loss atomic commit. [SQLite atomic commit](https://www.sqlite.org/atomiccommit.html)

2. One production reducer plus one declarative transition oracle generated from the same normative event vocabulary—but not the same handwritten guard implementation.

3. All packet schemas compiled at startup/CI through strict Ajv, with expected scenario/cut/world/action manifests passed to semantic validation. Canonical bytes would use JCS. **SEARCHED:** [JSON Schema 2020-12](https://json-schema.org/draft/2020-12), [RFC 8785/JCS](https://www.rfc-editor.org/rfc/rfc8785.html)

4. A single end-to-end result record containing A0, B, writer receipt, A1, packet hashes, route receipt, and served-input hash.

5. A LoadGen-like deterministic, checksum-bound, sequestered generator. **SEARCHED:** [MLCommons inference rules](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc), [NIST sequestered evaluations](https://pages.nist.gov/ai-technology-evaluation/)

6. OS-backed descendant accounting—Job Objects on Windows—with shape tests on process-tree aggregates and separate absolute affordability results.

7. The verified confidence-sequence calculation, but with assurance targets covering all owner-designated practical alternatives.

8. A direct 149-pair route gate rather than the 48-cell inferential gate, while retaining per-mode diagnostics.

For unknown acceptance, borrow parameter-bound idempotency semantics: Stripe stores the first result for an idempotency key, and AWS rejects the same token with changed parameters. **SEARCHED:** [Stripe idempotent requests](https://docs.stripe.com/api/idempotent_requests), [AWS client-token idempotency](https://docs.aws.amazon.com/ec2/latest/devguide/ec2-api-idempotency.html)

## WOULD I DESIGN IT DIFFERENTLY?

**READ-ONLY: yes.**

I would:

- use owner-pinned manifest enforcement before importing any reviewed code;
- compile and execute every schema, not sample one;
- bind validation to the expected experiment manifest rather than merely self-consistent packet hashes;
- make A0 an explicit scorer input;
- separate continuity shape, engineering affordability, carrier selection, model usefulness, and route reliability into independent outputs;
- measure descendant work rather than trust an assertion that descendants were measured;
- choose sample size from the complete practical alternative set;
- replace the 48-cell readiness inference with the direct pair-missing contract;
- keep generated PASS reports as external receipts, not part of the instrument’s normative bundle.

## Plain-language answer

No: the experiment does not yet have a fair chance to answer its question. It can reject valid worker-schema execution before the experiment starts, score an incorrect/invalid trace as successful, treat semantically different histories as identical, and let archive-linear child work pass as bounded.

The 4,608 scientific calls buy much better power than the 2,304-call `n=384` design for four selected alternatives. They do not buy general answerability, and they do not reliably distinguish the registered `Δ=-.25, OM=.85` case.

The 98,868 route-soak calls would buy a conservative simultaneous bound across the registered mode/position cells if attempted calls, all failure paths, and the route were properly frozen. As written, they condition away some failures and omit an `OTHER` mode, so they do not buy the advertised pair-missing guarantee.

Unavoidable uncertainty remains near the Δ=−.10 and OM=.80 thresholds, from finite-sample randomness, future route/provider drift, model stochasticity, and the fact that this experiment covers only one serial episode—not coordination.

## Omission and bypass record

- Strong omitted comparator: **ordinary SQLite indexed projection/query over the canonical journal**, with no new FD/FC/TN carrier branding. Controls are mentioned as eligible but no executable comparator manifest requires this simplest implementation. **SEARCHED.**
- Legal two-answer trace: wrong A0 + correct singleton B/writer/A1. Registered definition says zero; pinned scorer returns one because A0 is absent. **EXECUTED.**
- False continuity pass: child `CHILD_CPU_INSTRUCTIONS=10H` returns no error. **EXECUTED.**
- False continuity kill: constant 4,000,000 root instructions are rejected despite zero H slope. **EXECUTED.**
- False mechanism preference: a constant-work control can be removed by the absolute cap while a branded candidate can hide H-linear work in a child; no Pareto executor repairs that. **EXECUTED/READ-ONLY.**
- False model usability: schema-invalid B or wrong A0 can score one. **EXECUTED.**
- False ceiling story: an altered but self-consistent OM cut/observation is accepted; a resulting low OM score can be called `MODEL_OR_INTERFACE_CEILING` even though the input interface was substituted. **READ-ONLY downstream; packet acceptance EXECUTED.**
- Inference bypass: assurance grid omits a practical registered alternative.
- Cohort bypass: global duplicate outside the retained subset.
- Render bypass: no executable renderer/padding/served-hash binding.
- Reconstruction bypass: verifier accepts changed semantic bytes and reports their new hash.
- Transport bypass: pre-acceptance/unclassified failure is outside the denominator/mode list.
- Cost bypass: future provider, route, fallback, cache behavior, and price are not frozen.
- Refusal test: the end-to-end red gate named in Attack J.
- Mechanism to borrow: MLPerf/LoadGen deterministic trace/checksum/audit structure.
- Artifact to remove: derived no-paid PASS report from the instrument bundle.
- Later boundary: concurrent/multi-agent coordination after one serial cold pair.

## Sweep log

1. **Sequential confidence sequences**

   - Exact query: `arXiv 2512.21300 Proposition 3.1 average conditional mean Chugg Ramdas`
   - Opened: [Chugg and Ramdas, Proposition 3.1 and average conditional mean definition](https://arxiv.org/pdf/2512.21300), pp. 5, 7–9.
   - Effect: confirmed heterogeneous/adapted applicability, κ premise, mixture expression, and uniform limit; C10 changed to HOLDS.
   - Stop: one primary mathematical source plus independent numerical reproduction settled the narrow theorem claim.
   - Label: **SEARCHED**.

2. **Noninferiority/assurance sizing**

   - Queries: `site:fda.gov "Non-Inferiority Clinical Trials" "Sample Size" guidance PDF`; `site:ema.europa.eu non-inferiority margin sample size guideline`
   - Opened: [FDA sample-size section](https://www.fda.gov/media/78504/download); [EMA choice-of-margin guideline](https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-choice-non-inferiority-margin_en.pdf), pp. 3–4.
   - Effect: confirmed that margin and adequate power are separate decisions; strengthened the `OM=.85, Δ=-.25` blocker.
   - Stop: two current regulator-origin guidance documents agreed; they are analogical, not jurisdictional authority here.
   - Label: **SEARCHED**.

3. **Generator freeze and leakage**

   - Queries: `site:github.com/mlcommons training policies test set fixed random seed audit rules`; `site:nist.gov AI benchmark test data contamination evaluation`; `site:nist.gov cheating AI agent evaluations`
   - Opened: [MLCommons training rules](https://github.com/mlcommons/training_policies/blob/master/training_rules.adoc), §§6.1/6.5/6.6; [MLCommons inference rules](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc), fixed trace/audit sections; [NIST AITE](https://pages.nist.gov/ai-technology-evaluation/); [NIST evaluation cheating](https://www.nist.gov/caisi/cheating-ai-agent-evaluations).
   - Effect: confirmed checksum-bound generation, fixed deterministic traces, sequestered data, and grader-gaming threats as directly borrowable controls.
   - Stop: official benchmark and government sources converged; pinned cohort attacks independently established the defect.
   - Label: **SEARCHED**.

4. **Factorial coverage and physical counters**

   - Queries: `site:nist.gov full factorial experiment design handbook`; `site:learn.microsoft.com job object accounting child processes CPU time official`
   - Opened: [NIST full factorial design](https://www.itl.nist.gov/div898/handbook/pri/section3/pri333.htm), §5.3.3.3; [Microsoft Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects), process-tree/accounting sections.
   - Effect: confirmed 4×5×5 is complete finite-grid coverage, but that real descendant aggregation and breakaway handling are separate requirements.
   - Stop: primary platform documentation plus executed child-work bypass settled the claim.
   - Label: **SEARCHED**.

5. **Schema, canonicalization, and runtime**

   - Queries: `site:json-schema.org draft 2020-12 validation specification additionalProperties official`; `site:rfc-editor.org RFC 8785 JSON Canonicalization Scheme`; `site:ajv.js.org strict mode strictTypes missing type keyword official`
   - Opened: [JSON Schema 2020-12](https://json-schema.org/draft/2020-12); [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html), §§3.1–3.2; [Ajv strict mode](https://ajv.js.org/strict-mode.html), strictTypes.
   - Effect: confirmed the selected standards/primitives are appropriate; the actual pinned Ajv exception governs the WorkerHandoff failure.
   - Stop: runtime execution answered behavior; official origins answered external requirements/status.
   - Label: **SEARCHED**.

6. **Durability, atomicity, idempotency**

   - Queries: `site:docs.stripe.com idempotent requests retry original result official`; `site:docs.aws.amazon.com idempotent API client token same parameters official`; `site:sqlite.org atomic commit rollback journal official`; `Temporal durable execution official docs crash recovery workflows`
   - Opened: [Stripe idempotency](https://docs.stripe.com/api/idempotent_requests); [AWS EC2 idempotency](https://docs.aws.amazon.com/ec2/latest/devguide/ec2-api-idempotency.html); [SQLite atomic commit](https://www.sqlite.org/atomiccommit.html); [Temporal durable execution](https://docs.temporal.io/temporal).
   - Effect: confirmed smaller adoptable mechanisms for request identity, parameter mismatch, crash-safe commit, and recovery; no need for bespoke equivalents.
   - Stop: multiple vendor/primary sources distinguished narrow primitives from the larger Temporal product.
   - Label: **SEARCHED**.

7. **Provider receipts, cache, refusal, and price**

   - Query: `site:developers.openai.com API request ID safeguards prompt caching pricing`
   - Opened: [OpenAI request IDs/debugging](https://developers.openai.com/api/reference/overview#backwards-compatibility); [current model/cache and safeguards guide](https://developers.openai.com/api/docs/guides/latest-model); [current model pricing example](https://developers.openai.com/api/docs/models/gpt-5.6-luna).
   - Effect: confirmed request IDs are troubleshooting receipts, not idempotency guarantees; safeguards add a plausible unregistered failure; current routes have nonzero and changeable prices.
   - Applicability: provider is not frozen, so this is evidence of exposure, not a claim about the eventual route.
   - Stop: the pinned bytes already decide the main defect—provider/route/price are unspecified.
   - Label: **SEARCHED**.

## Residual risks after the named repair classes

- Exact and near-threshold cases can remain inconclusive by design.
- A finite route soak cannot guarantee future provider behavior or price.
- A Windows descendant-accounting solution must explicitly prohibit or detect breakaway.
- Sequestered generator integrity remains partly organizational.
- The confidence-sequence source is a preprint; theorem status/errata should be rechecked before paid execution.
- One serial episode cannot establish multi-agent coordination or cross-episode continuity.
- A complete schema/validator cannot prove a provider followed the served bytes without a route receipt or trusted capture.
- Exactness and Pareto fairness remain untested until real candidate implementations exist.

## Non-claims

This verdict does not claim that:

- FD, FC, or TN fails;
- bounded continuity is impossible;
- every possible state/action domain is covered;
- the experiment can prevent all leakage or bypass;
- any provider offers a zero-price or stable route;
- model/interface separation is identifiable outside the registered serial design;
- the later coordination experiment is answered.

## Side effects and cleanup

- Repository authority remained read-only.
- Temporary Git-object reconstructions and reviewer probe files were removed.
- Python bytecode generated by the probes was removed; two pre-existing r8 cache files were preserved.
- No report or verdict was written to disk.
- Final `git diff --quiet` and cached-diff checks both returned zero: no tracked or index changes.
