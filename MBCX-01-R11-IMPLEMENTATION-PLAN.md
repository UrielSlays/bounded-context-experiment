# MBCX-01 r11 Seam-Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a no-paid r11 governing bundle that closes every executed r10 false-green, reconstructs from pinned Git objects without r9 runtime or host-bound dependencies, and produces an undispatched council packet.

**Architecture:** r11 is split into owned state, packet/DAG, cohort, measurement/ledger and inference modules behind JSON contracts. A single normative verifier runs every retained invariant and every r10 regression witness, while a repair ledger makes dropped fixes machine-visible. The council launcher and vendored Ajv runtime are reconstructed before execution.

**Tech Stack:** Python 3.13 standard library, JSON Schema 2020-12, Node.js with a vendored Ajv 8.20.0 bundle, PowerShell, Git object plumbing.

**Spec:** `MBCX-01-R11-ARCHITECTURE-SPEC.md`

**Execution status at governing freeze:** Tasks 1–7 are complete and verified. Task 8 is the post-freeze pin/reconstruction/packet assembly sequence; its packet is intentionally not a governing subject and is not dispatched in this work session.

## Global Constraints

- Paid/provider/model calls: exactly zero.
- Runtime imports of `mbcx01_r8_*`, `mbcx01_r9_*` or `mbcx01_r10_*`: forbidden.
- Scientific sample: 768 pairs / 4,608 scheduled logical positions.
- Route qualification: 456 full six-call trials / accept at most 4 / 2,736 scheduled positions, under the r11 conditional-hazard hypotheses.
- Council packet: prepare and test, but do not dispatch.
- File changes: preserve unrelated untracked logs and historical artifacts.

---

### Task 1: Bank and synthesize r10

**Files:**
- Create: `MBCX-01-SEAT1-OUTSIDE-OPUS5-VERDICT-r10.md`
- Create: `MBCX-01-SEAT2-CHATGPT-SOL-VERDICT-r10.md`
- Retain: `MBCX-01-SEAT3-CODEX-VERDICT-r10.md`
- Create: `MBCX-01-COUNCIL-R10-SYNTHESIS-AND-DISPOSITION.md`

**Interfaces:**
- Consumes: three verbatim seat reports.
- Produces: repair IDs used by the architecture, contracts, verifier and repair ledger.

- [x] **Step 1: Bank both browser-seat replies verbatim.**
- [x] **Step 2: Classify convergence by executed counterexample, not vote count.**
- [x] **Step 3: Record the controlling NO-GO, retained repairs, cost decision and r11 closure condition.**

### Task 2: Write r11 red regression tests

**Files:**
- Create: `test_mbcx01_r11.py`
- Create: `MBCX-01-R11-REPAIR-LEDGER.json`

**Interfaces:**
- Consumes: repair IDs from the r10 synthesis.
- Produces: named `unittest` cases and witness IDs consumed by `verify-r11-normative-bundle.py`.

- [ ] **Step 1: Add state tests that initially fail because `mbcx01_r11_state_reference` and `mbcx01_r11_state_oracle` do not exist.**

```python
def test_future_fact_does_not_block_current_interval(self): ...
def test_finite_visible_head_can_be_corrected_without_inversion(self): ...
def test_noncanonical_event_id_is_rejected(self): ...
def test_proposal_requires_exact_durable_b_response_foreign_key(self): ...
```

- [ ] **Step 2: Run `python -m unittest -v test_mbcx01_r11.R11StateTests` and verify import/test failure.**
- [ ] **Step 3: Add packet/DAG tests for bound BC selection, unavailable gold, structural scorer admission, distinct A0/B/A1 packets, exact served SHA-256, response provenance and actual child bytes.**
- [ ] **Step 4: Run the packet test class and verify it fails because the r11 packet module is absent.**
- [ ] **Step 5: Add cohort, measurement, ledger, precedence, route-coupling and explicit-cell assurance tests.**
- [ ] **Step 6: Run the full test file and retain the expected red output in the development log.**

### Task 3: Implement r11-owned state and independent oracle

**Files:**
- Create: `mbcx01_r11_common.py`
- Create: `mbcx01_r11_state_reference.py`
- Create: `mbcx01_r11_state_oracle.py`
- Create: `MBCX-01-STATE-ACTION-CONTRACT-v6.json`
- Modify: `test_mbcx01_r11.py`

**Interfaces:**
- Produces: `canonical_json`, `sha256`, `sha384`, `action_id`, `cut_hash`, `canonical_event_id`, `initial_state`, `make_event`, `reference_apply`, `oracle_apply`.
- Both reducers consume a schema-valid event and return `(new_state, result_code)` without sharing post-ingress transition functions.

- [ ] **Step 1: Implement canonical primitives and closed event schemas sufficient for the red state traces.**
- [ ] **Step 2: Implement the reference fact/obligation/dependency/handoff/response algebra with interval and foreign-key invariants.**
- [ ] **Step 3: Run the state tests and keep the oracle tests red.**
- [ ] **Step 4: Implement the oracle with separate guard/effect organization and no reference-reducer calls.**
- [ ] **Step 5: Run state tests; require both engines to agree on legal and illegal traces and every r10 counterexample to be red.**
- [ ] **Step 6: Refactor only after green; run the state class again.**

### Task 4: Implement typed packets and causal scoring

**Files:**
- Create: `MBCX-01-PACKET-SCHEMAS-v5.json`
- Create: `mbcx01_r11_packets.py`
- Modify: `test_mbcx01_r11.py`

**Interfaces:**
- Produces: `packet_fixture_manifest`, `build_decision_packet`, `build_task_packet`, `render_served_input`, `build_scoring_fixture`, `validate_scorer_input`, `score_exact`.
- `score_exact(scorer_input: dict) -> int` performs admission internally and returns zero on any structural, semantic, hash or causal mismatch.

- [ ] **Step 1: Define schemas for manifest, A0/A1 DecisionPacket, A0 result, TaskPacket, WorkerHandoff, durable call record, writer receipt, A1 result and composite scorer input.**
- [ ] **Step 2: Implement manifest validation that recomputes candidate selection, gold action and postcommit truth.**
- [ ] **Step 3: Implement deterministic builders with distinct stage identities and exact 65,536-byte served SHA-256.**
- [ ] **Step 4: Implement scorer admission and causal-link verification, including complete child event bytes and postcommit state hash.**
- [ ] **Step 5: Run packet tests and verify every r10 mutation returns zero while the valid fixture returns one.**

### Task 5: Implement cohort, measurement and durable ledger

**Files:**
- Create: `MBCX-01-MEASUREMENT-CONTRACT-v5.json`
- Create: `mbcx01_r11_measurement.py`
- Modify: `test_mbcx01_r11.py`

**Interfaces:**
- Produces: `choose_one_cut`, `validate_source_provenance`, `select_cohort`, `baseline_receipt_rows`, `evaluate_measurement_receipts`, `CallLedger.prepare`, `CallLedger.transition`, `CallLedger.serialize`, `CallLedger.recover`.

- [ ] **Step 1: Implement domain-parameterized framed hashes and source-provenance validation.**
- [ ] **Step 2: Make the frozen r10-vs-r11 cut vector test green and reject motif/action-universe substitution.**
- [ ] **Step 3: Implement strict measurement receipt admission: one candidate/generator, exact integer axes, Job containment/completion, CPU/I/O/memory/elapsed/instruction evidence and external-work policy.**
- [ ] **Step 4: Make mixed-candidate, Boolean-axis, missing-I/O and missing-job-receipt tests red at the evaluator boundary.**
- [ ] **Step 5: Implement a digest-bound serializable call ledger whose durable transition requires response bytes/hash/ref/transaction receipt and whose ambiguous retry requires structured route attestation.**
- [ ] **Step 6: Run cohort/measurement/ledger tests, including corrupt-restart and empty-identity mutants.**

### Task 6: Port inference, restore precedence and repair claims

**Files:**
- Create: `MBCX-01-INFERENCE-CONTRACT-v6.json`
- Create: `mbcx01_r11_inference.py`
- Modify: `test_mbcx01_r11.py`

**Interfaces:**
- Produces: `paired_intervals`, `scientific_decision`, `missing_completion_bounds`, `decision_with_missingness`, `binomial_cdf`, `smallest_reliability_plan`, `route_coupling_bound`, `simulate_registered_cells`.

- [ ] **Step 1: Port only the reviewed mixture/DP kernels; add no historical runtime import.**
- [ ] **Step 2: Make exact DP-vs-enumeration tests green through seven arbitrary missing positions and all-missing hull tests green.**
- [ ] **Step 3: Restore the design-failure precedence input and prove transport cannot mask a known broken design.**
- [ ] **Step 4: Register explicit joint assurance cells and verify frozen 10,000-replicate results meet only the claims actually written.**
- [ ] **Step 5: Implement the conditional-hazard coupling bound and verify it rejects the marginal-only perfect-correlation interpretation while reproducing the `(456,4)` tails.**

### Task 7: Build the normative verifier and portable validator closure

**Files:**
- Create: `verify-r11-schema-ajv.mjs`
- Create: `vendor/ajv-r11.bundle.cjs`
- Create: `verify-r11-normative-bundle.py`
- Create: `verify-r11-pinned.ps1`
- Create: `test-r11-normative-bundle.ps1`
- Create: `MBCX-01-R11-NO-PAID-VERIFICATION.json`
- Modify: `MBCX-01-R11-REPAIR-LEDGER.json`

**Interfaces:**
- The Python verifier returns nonzero on any unit failure, schema failure, repair-ledger mismatch, runtime import, pin mismatch or nonzero paid-call declaration.
- The PowerShell verifier reconstructs every subject before Python/Node execution.

- [ ] **Step 1: Run the verifier before creation and confirm it is absent/failing.**
- [ ] **Step 2: Bundle Ajv 8.20.0 deterministically into one governed file and make the schema verifier load only that relative file.**
- [ ] **Step 3: Implement six verifier sections: state, packets, cohort, measurement/ledger, inference/route and integration/repair-ledger.**
- [ ] **Step 4: Add a forbidden-import scan and assert every repair-ledger witness was executed.**
- [ ] **Step 5: Run `python -m unittest -v test_mbcx01_r11.py` and `python verify-r11-normative-bundle.py`; require zero failures.**
- [ ] **Step 6: Generate the no-paid report from verifier outputs and confirm `paid_calls=0`, `experiment_evidence=false`.**

### Task 8: Pin, reconstruct and prepare the undispatched r11 council packet

**Files:**
- Create: `MBCX-01-R11-PIN-MANIFEST.json`
- Create: `MBCX-01-EXPERIMENT-COUNCIL-PACKET-r11.md`
- Create: `MBCX-01-BROWSER-SEAT-PROMPT-r11.txt`
- Create: `MBCX-01-SEAT3-CODEX-EXEC-PROMPT-r11.txt`
- Create: `generate-seat3-experiment-r11-prompt.ps1`
- Create: `test-r11-council-packet.ps1`

**Interfaces:**
- Produces a governing commit + manifest blob + launcher blob and a packet that asks all three seats to attack the same reconstructed bytes.
- Does not send browser messages, create a Codex Exec run or create a dispatch receipt.

- [ ] **Step 1: Commit the r10 verdicts/synthesis and r11 governing subjects intentionally.**
- [ ] **Step 2: Generate exact Git blob, LF byte, line and SHA-384 pins for every governing subject, including the launcher and Ajv bundle.**
- [ ] **Step 3: Reconstruct from Git objects in a fresh temporary directory and run the full verifier.**
- [ ] **Step 4: Write the council packet with the governing commit, manifest blob and launcher blob; explicitly foreground the conditional-hazard route proof and cross-artifact DAG attacks.**
- [ ] **Step 5: Generate the browser and Codex Exec prompts from the packet and run packet/prompt consistency tests.**
- [ ] **Step 6: Confirm no r11 seat verdict, completion marker, dispatch receipt or sent browser turn exists. Stop and wait for the owner.**

## Self-review

- Spec coverage: every r10 repair ID maps to Tasks 2–8.
- Placeholder scan: no implementation step delegates an unspecified behavior; exact interfaces and failure cases are named.
- Type consistency: served request hashes are SHA-256/64 hex; artifact and semantic object hashes are SHA-384/96 hex; event IDs are canonical SHA-256-based `EV.` IDs.
- Cost: no task authorizes a paid or provider/model call.
