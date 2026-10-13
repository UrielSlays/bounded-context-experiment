# MBCX-01 Council Round 11 synthesis and disposition

Date: 2026-08-13
Round: r11
Governing commit reviewed: `b56e450f8553b96f6121cb045b62eb604e4a0655`
Paid/model/provider calls performed by the conductor: **NONE**

## Controlling disposition

**NO-GO, repairable without changing the experiment.** Opus returned `GO`; ChatGPT/Sol and Codex returned `NO-GO` after independently executing the same two false-green classes. Council rulings are evidence-weighted: either reachable false scientific success controls the gate.

r11 successfully closed the state, response-FK, catalog, cohort, missingness, power-language, route-mathematics, Ajv, bootstrap and repair-ledger defects from r10. The scientific run remains 768 pairs and the route qualification remains 456 full-route trials. No additional sample size, provider call or physical run is authorized by this disposition.

## Converged failures and r12 disposition

| Repair ID | Severity | Consolidated finding | Evidence | r12 disposition |
|---|---:|---|---|---|
| R12-AUTHORITATIVE-WRITER | P0 | `WriterReceiptV2` proves a canonical child, not that the exact persisted proposal was applied to the exact authoritative precommit state. Forged proposal IDs, impossible journal jumps and a packet-local child different from the production commit can score 1 after descendant hashes are recomputed. | ChatGPT and Codex executed independently. | Scorer admission receives the exact precommit state/current cut and persisted proposal event. It replays the exact child through both r12 reducers, requires both `APPLIED`, identical poststate, exact next sequence/effective time, exact proposal identity/hash and exact postcommit state/cut. The default fixture may not invent a disconnected proposal/commit. |
| R12-AMBIGUITY-TERMINAL | P0 | After `ACCEPTANCE_AMBIGUOUS`, a caller can locally author the route-attestation fields and public digest and return the ledger to `PREPARED`, risking a duplicate stochastic call. | ChatGPT and Codex executed independently. | Remove ambiguity-to-retry authority. Ambiguous acceptance is terminal missing for MBCX-01. A future provider-specific replay profile requires a separately pinned, independently authenticated service capability and a new council review. |
| R12-SIGNED-PHYSICAL-RECEIPT | P0/P1 | The physical contract requires an external signature but the closed schema cannot represent or verify one; external-work denial is only a candidate-readable constant. | ChatGPT and Codex; Opus did not reach the bypass because the harness remains unavailable. | Define a signed receipt envelope and a separately pinned verification key. Bind the complete canonical receipt, run/cell anti-replay identity, algorithm/domain/version, containment/egress evidence and digest. Unsigned, unknown-key, tampered, replayed or synthetic receipts remain unavailable. |
| R12-PHYSICAL-BACKEND-TOTAL | P1/P2 | Retired-instruction collection, process attribution, completion evidence, external-work denial and several I/O shape axes are not yet machine-total. | ChatGPT and Codex; Microsoft primary documentation supports the platform caveats. | Pin exact ETW PMC mode/event/counter/process-start-key attribution and loss rules; fail loud when unsupported. Require separate Basic+I/O and Extended-Limit final queries, containment/egress evidence, and H-range gates for total I/O bytes and operations. Do not weaken a primary boundedness axis into a diagnostic. |
| R12-ORACLE-INDEPENDENCE | P1 | Reference and oracle share load-bearing semantic helpers after structural admission, so agreement is not independent evidence for those decisions. | Codex read/executed dependency probes. | Retain shared canonicalization, schema and hash primitives only. Implement temporal visibility/closure, dependency reachability, action legality and transition effects independently in the oracle; add perturbation witnesses. |
| R12-INTERNAL-SHELF-LOG | P2 | The mandatory internal-shelf sweep was not supplied in the governing bundle. | ChatGPT and Codex. | Publish exact queries, repositories, opened files and adopt/why-not dispositions. Reuse Photon's fail-closed ambiguous-outcome rule, Gravity's Ed25519/JWS verification shape and existing Job Object containment patterns. |
| R12-DP-SPOTCHECK | P3 | The exact exhaustive missingness oracle is intentionally bounded to small `m`; the DP runs beyond it. | Opus. | Retain exhaustive certification at small `m` and add deterministic randomized-completion property checks near `m=20`; do not mislabel these spot checks as exhaustive proof. |

## Disagreements resolved

Opus recommended making retired instructions diagnostic-only when PMU access is unavailable. ChatGPT and Codex instead required an exact pinned backend that fails loud if unsupported. r12 adopts the latter because retired instructions remain a primary physical boundedness coordinate. A host unable to produce exact, attributable, loss-audited evidence is honestly `PHYSICAL_HARNESS_UNAVAILABLE`; silently dropping the axis would change the research claim.

Codex suggested removing the r11 implementation plan from the normative subject set. Adopted: implementation plans remain Git history, not experiment law. The r12 manifest governs contracts, implementations, tests, verification, architecture, prior-art/shelf record, harness requirements and repair ledger.

## Retained findings

The following r11 mechanisms are retained and must remain green:

- r11-owned append-only bitemporal state, exact cuts, canonical IDs and strict event admission;
- durable B-response foreign keys, globally unique response identities and exact proposal/commit/reject binding;
- full TaskPacket/manifest/action-catalog identity and typed A0 → B → writer → cold-A1 graph;
- pinned cohort generator, contract-owned selection domains, six motifs × 128 retained scenarios and SHA-256 order;
- one canonical durability receipt across packet, state and restart ledger;
- exact missing-completion DP, Boolean/type guards and decision precedence;
- n=768 pointwise planning diagnostics, including the published `(0,.3,.1,.6)` counterexample;
- the finite-horizon conditional-expectation proof for the 456/4 route contract, without iid;
- vendored strict Ajv, calendar-valid UTC, authenticated Git-object bootstrap and two-way repair-ledger coverage.

## Cost decision in plain language

The experiment's question is still answerable. The remaining failures are proof-of-authority mistakes in the ruler: a hash can show that bytes are internally consistent, but it cannot prove that the state machine actually applied them, that a provider promises safe replay, or that an OS harness produced the counters. r12 makes those claims come from the authority that owns them.

Paying for more model calls buys none of these repairs. The scientific design therefore stays at 768 pairs / 4,608 scheduled positions. The route gate stays at 456 six-call trials / 2,736 scheduled positions. r12 performs only no-paid contract, implementation and adversarial verification work; the physical harness and all scientific/provider/route executions remain stopped.

## r12 acceptance condition

r12 is ready for council only when every r11 retained witness and every new r12 red trace is green under a frozen Git reconstruction; the scorer cannot accept a child without authoritative dual-reducer replay; ambiguous acceptance has no retry edge; signed physical receipts are machine-representable but synthetic fixtures still cannot pass; oracle semantic independence is mechanically attacked; the internal-shelf log is present; and the council packet itself authorizes no experiment, physical run, route soak or paid/model/provider call.
