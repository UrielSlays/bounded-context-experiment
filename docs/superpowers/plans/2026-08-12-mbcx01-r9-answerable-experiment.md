# MBCX-01 r9 Answerable Experiment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a locally executable, no-paid r9 preregistration capable of answering the original MBCX-01 question without narrowing its H, D, or F scope.

**Architecture:** A closed event envelope feeds two independently implemented state machines. Deterministic BC/OM builders feed a syntactic and semantic packet gate; a separate physical-work evaluator executes registered red candidates over all 100 cells. Exact mixture inference, reference vectors, operating characteristics, and familywise transport bounds are then verified before Git-object pinning and council dispatch.

**Tech Stack:** Markdown, JSON Schema 2020-12 declarations, Python 3.11+ standard library, PowerShell 7, Git, Moonwalker CDP, Codex EXEC.

**Spec:** `docs/superpowers/specs/2026-08-12-mbcx01-r9-answerable-experiment-design.md`

## Global Constraints

- Preserve r8 artifacts as immutable audit history and create versioned r9 files.
- Preserve every unrelated untracked file and operational log.
- Do not implement FD/FC/TN candidates or make paid inference calls.
- Do not narrow the original claim from the full 4×5×5 H-D-F range.
- Use only committed Git-object bytes for council pins.
- Use the maintained Claude and ChatGPT browser seats and one fresh Codex EXEC seat.

---

### Task 1: Commit the approved r9 design and executable red shell

**Files:**
- Create: `verify-r9-normative-bundle.py`
- Create: `mbcx01_r9_oracle.py`
- Create: `mbcx01_r9_reference.py`
- Commit: `docs/superpowers/specs/2026-08-12-mbcx01-r9-answerable-experiment-design.md`
- Commit: `docs/superpowers/plans/2026-08-12-mbcx01-r9-answerable-experiment.md`

**Interfaces:**
- Produces: `verify-r9-normative-bundle.py --section <name> [--report path]` and missing-artifact RED behavior.

- [ ] **Step 1: Write the verifier shell with r9 artifact names**

```python
REQUIRED = [
    "MBCX-01-EXPERIMENT-DESIGN-r8.md",
    "MBCX-01-STATE-ACTION-CONTRACT-v4.json",
    "MBCX-01-PACKET-SCHEMAS-v3.json",
    "MBCX-01-MEASUREMENT-CONTRACT-v3.json",
    "MBCX-01-INFERENCE-CONTRACT-v4.json",
]
missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
if missing:
    raise AssertionError(f"missing r9 artifacts: {missing}")
```

- [ ] **Step 2: Run and observe RED**

Run: `python .\verify-r9-normative-bundle.py`  
Expected: exit 1 naming all five missing r9 normative artifacts.

- [ ] **Step 3: Commit the approved design, plan, and RED shell**

```powershell
git add docs/superpowers/specs/2026-08-12-mbcx01-r9-answerable-experiment-design.md docs/superpowers/plans/2026-08-12-mbcx01-r9-answerable-experiment.md verify-r9-normative-bundle.py mbcx01_r9_oracle.py mbcx01_r9_reference.py
git commit -m "test: define r9 answerable experiment red gate"
```

### Task 2: Event envelope, independent state machines, and mutant killing

**Files:**
- Create: `MBCX-01-STATE-ACTION-CONTRACT-v4.json`
- Modify: `mbcx01_r9_oracle.py`
- Modify: `mbcx01_r9_reference.py`
- Modify: `verify-r9-normative-bundle.py`

**Interfaces:**
- `make_event(event_type: str, payload: dict, **overrides) -> dict`
- `oracle_apply(state: dict, event: dict) -> tuple[dict, str]`
- `reference_apply(state: dict, event: dict) -> tuple[dict, str]`
- `run_mutant(name: str, trace: list[dict]) -> tuple[dict, str]`

- [ ] **Step 1: Add failing state tests**

```python
rescheduled, code = reference_apply(initial_state(), make_event(
    "reschedule_obligation", {"obligation_id": "OBL.A", "due_at": T2}))
assert code == "APPLIED" and rescheduled["obligations"]["OBL.A"]["due_at"] == T2
assert_differential(three_node_cycle_trace)
assert duplicate_replay_state == original_post_state
assert all(run_mutation_suite().values())
```

- [ ] **Step 2: Run state section and observe RED**

Run: `python .\verify-r9-normative-bundle.py --section state`  
Expected: exit 1 because v4 and complete implementations do not exist.

- [ ] **Step 3: Implement v4, both reducers, exact traces, and named mutants**

The reference uses journal projection and the oracle uses direct immutable state transformations. Implement independent cycle, cut, fact-version, idempotency, obligation, handoff, and response logic.

- [ ] **Step 4: Run state section GREEN**

Run: `python .\verify-r9-normative-bundle.py --section state`  
Expected: `state: PASS`, 17 event types, 289 differential pairs, every named mutant killed.

- [ ] **Step 5: Commit**

```powershell
git add MBCX-01-STATE-ACTION-CONTRACT-v4.json mbcx01_r9_oracle.py mbcx01_r9_reference.py verify-r9-normative-bundle.py
git commit -m "design: make r9 state semantics executable"
```

### Task 3: Packet semantic gate and deterministic BC/OM builders

**Files:**
- Create: `MBCX-01-PACKET-SCHEMAS-v3.json`
- Modify: `mbcx01_r9_oracle.py`
- Modify: `mbcx01_r9_reference.py`
- Modify: `verify-r9-normative-bundle.py`

**Interfaces:**
- `validate_packet_semantics(packet: dict, canonical_cut: dict) -> list[str]`
- `build_bc_packet(cut: dict, selected_object_ids: list[str], action_ids: list[str]) -> dict`
- `build_om_packet(cut: dict, gold_read_set: list[str], action_ids: list[str]) -> dict`
- `score_condition(target_action_id: str, worker: dict, committed: list[str], a1: list[str], gold_a1: list[str]) -> int`

- [ ] **Step 1: Add failing packet witnesses**

```python
assert "DUPLICATE_ACTION_ID" in validate_packet_semantics(alias_packet, cut)
assert "ACTION_HASH_MISMATCH" in validate_packet_semantics(bogus_hash_packet, cut)
assert "PACKET_ENVELOPE_EXCEEDED" in validate_packet_semantics(cap_packet, cut)
assert bc_packet["available_action_ids"] == om_packet["available_action_ids"]
assert score_condition(target, extra_action_worker, [target, extra], [], []) == 0
```

- [ ] **Step 2: Observe RED**

Run: `python .\verify-r9-normative-bundle.py --section packets`  
Expected: exit 1 on absent v3 semantic validation/builders.

- [ ] **Step 3: Implement the schema, semantic validator, builders, and exact singleton B score**

Oversize is a deterministic design failure before dispatch. Builders differ only in the public semantic object-ID source and share rendering settings and action universe.

- [ ] **Step 4: Run packet section GREEN**

Run: `python .\verify-r9-normative-bundle.py --section packets`  
Expected: `packets: PASS` with alias, hash, missing-catalog, kind, prerequisite, and overflow mutants rejected.

- [ ] **Step 5: Commit**

```powershell
git add MBCX-01-PACKET-SCHEMAS-v3.json mbcx01_r9_oracle.py mbcx01_r9_reference.py verify-r9-normative-bundle.py
git commit -m "design: define r9 packet builders and semantic gate"
```

### Task 4: Honest cohort freeze and full physical-work evaluator

**Files:**
- Create: `MBCX-01-MEASUREMENT-CONTRACT-v3.json`
- Modify: `mbcx01_r9_reference.py`
- Modify: `verify-r9-normative-bundle.py`

**Interfaces:**
- `evaluate_eligibility(canonical_state: dict, cut: dict, action_ids: list[str], gold_action_id: str) -> tuple[bool, str]`
- `select_cohort(candidates: list[dict]) -> list[dict]`
- `measurement_grid() -> set[tuple[int, int, int]]`
- `evaluate_counter_grid(rows: list[dict]) -> list[str]`
- `execute_red_candidate(name: str) -> list[dict]`

- [ ] **Step 1: Add failing cohort and measurement tests**

```python
assert len(measurement_grid()) == 100
assert (10000, 64, 256) in measurement_grid()
assert "H_SHAPE_LIMIT" in evaluate_counter_grid(execute_red_candidate("LOW_SLOPE_ARCHIVE_LINEAR_10X"))
assert "PAGE_BYTE_INCONSISTENT" in evaluate_counter_grid(execute_red_candidate("PAGE_BYTE_MISMATCH"))
assert supplied_eligibility_is_ignored()
```

- [ ] **Step 2: Observe RED**

Run: `python .\verify-r9-normative-bundle.py --section cohort --section measurement`  
Expected: exit 1 because v3, 100-cell coverage, and executable red candidates are absent.

- [ ] **Step 3: Implement freeze ordering, eligibility recomputation, 100-cell evaluator, and red candidates**

Use literal counter rows from each candidate. The evaluator, not the candidate declaration, decides the branch.

- [ ] **Step 4: Run focused sections GREEN**

Run: `python .\verify-r9-normative-bundle.py --section cohort --section measurement`  
Expected: both sections pass, 960 generated and 768 retained, 100 cells, every mutant rejected by execution.

- [ ] **Step 5: Commit**

```powershell
git add MBCX-01-MEASUREMENT-CONTRACT-v3.json mbcx01_r9_reference.py verify-r9-normative-bundle.py
git commit -m "design: execute r9 cohort and physical-work gates"
```

### Task 5: Frozen inference sensitivity, honest OC, and simultaneous reliability

**Files:**
- Create: `MBCX-01-INFERENCE-CONTRACT-v4.json`
- Modify: `mbcx01_r9_oracle.py`
- Modify: `mbcx01_r9_reference.py`
- Modify: `verify-r9-normative-bundle.py`

**Interfaces:**
- `mixture_interval(xs: list[float], alpha: float, kappa: float, method: str) -> tuple[float, float]`
- `kappa_sensitivity(pairs: list[tuple[int, int]]) -> list[dict]`
- `reliability_cell_alpha(mode_count: int) -> float`
- `reliability_cell_budget(mode_count: int) -> float`
- `simulate_oc(replicates: int, seed: str) -> dict`

- [ ] **Step 1: Add failing inference tests with independent literal expectations**

```python
assert contract["method"]["kappa_source_rule"] == "SOURCE_DEFAULT_NOT_OC_TUNED"
assert [row["kappa"] for row in kappa_sensitivity(low_discord_pairs)] == [0.10, 0.15, 0.25, 0.50, "UNIFORM"]
assert abs(delta_zero_half_width - 0.028724411) < 1e-9
assert reliability_cell_alpha(M) * (6 * M) == 0.05
assert reliability_cell_budget(M) * (6 * M) == 0.02
```

- [ ] **Step 2: Observe RED**

Run: `python .\verify-r9-normative-bundle.py --section inference`  
Expected: exit 1 because v4 vectors, sensitivity, OC curve, and familywise allocation are absent.

- [ ] **Step 3: Implement exact vectors, sensitivity, near-floor OC curve, and reliability allocation**

Freeze exact low-discord pair indices. Delete 96/192 interval decisions. Report OM=.80, .85, and .95 separately for every negative-delta curve.

- [ ] **Step 4: Run inference GREEN**

Run: `python .\verify-r9-normative-bundle.py --section inference --oc-reps 250`  
Expected: `inference: PASS`, analytic/Simpson endpoint agreement within tolerance, deterministic OC repeat, and exact familywise arithmetic.

- [ ] **Step 5: Commit**

```powershell
git add MBCX-01-INFERENCE-CONTRACT-v4.json mbcx01_r9_oracle.py mbcx01_r9_reference.py verify-r9-normative-bundle.py
git commit -m "design: freeze honest r9 inference and reliability"
```

### Task 6: Integrate the r9 design and full no-paid report

**Files:**
- Create: `MBCX-01-EXPERIMENT-DESIGN-r8.md`
- Create: `MBCX-01-R9-NO-PAID-VERIFICATION.json`
- Modify: `verify-r9-normative-bundle.py`

**Interfaces:**
- Full verifier report `MBCX01R9NoPaidVerificationV1` with working-tree hashes, evidence classification, section results, mutation kills, packet failures, 100-cell coverage, vectors, OC, and zero paid calls.

- [ ] **Step 1: Add failing full-bundle consistency checks**

```python
assert design_names_exact_r9_artifacts()
assert decision_precedence[0] == "DESIGN_OR_IMPLEMENTATION_FAIL"
assert report["paid_calls"] == 0 and report["experiment_evidence"] is False
```

- [ ] **Step 2: Observe RED, then write the integrated r8 design**

Run: `python .\verify-r9-normative-bundle.py --oc-reps 250 --report .\MBCX-01-R9-NO-PAID-VERIFICATION.json`  
Expected before integration: exit 1. Expected after integration: all sections pass.

- [ ] **Step 3: Run the complete deterministic verification**

Run: `python .\verify-r9-normative-bundle.py --oc-reps 10000 --report .\MBCX-01-R9-NO-PAID-VERIFICATION.json`  
Expected: exit 0 and `paid_calls: 0`.

- [ ] **Step 4: Commit**

```powershell
git add MBCX-01-EXPERIMENT-DESIGN-r8.md MBCX-01-R9-NO-PAID-VERIFICATION.json verify-r9-normative-bundle.py
git commit -m "design: integrate executable r9 preregistration"
```

### Task 7: Git-object reconstruction and r9 council packet

**Files:**
- Create: `test-r9-normative-bundle.ps1`
- Create: `MBCX-01-EXPERIMENT-COUNCIL-PACKET-r9.md`
- Create: `MBCX-01-BROWSER-SEAT-PROMPT-r9.txt`
- Create: `generate-seat3-experiment-r9-prompt.ps1`
- Create: `test-r9-council-dispatch.ps1`
- Create: `watch-seat3-codex-r9.ps1`

**Interfaces:**
- Git-object-only verifier extraction.
- Two-line maintained browser pointer.
- Fresh read-only Codex EXEC prompt and watcher.

- [ ] **Step 1: Write dispatch tests before generators**

Test the exact r9 artifact set, named commit, LF Git-blob byte counts, SHA-384 values, lateral seal, no-paid status, and same-seat/fresh-seat rules.

- [ ] **Step 2: Observe RED**

Run: `pwsh -NoProfile -File .\test-r9-council-dispatch.ps1`  
Expected: exit 1 because packet and prompt generators are missing.

- [ ] **Step 3: Implement Git-object verification and delivery artifacts**

Every byte count and SHA-384 must be computed from `git cat-file blob <commit>:<path>` output. Never hash the checkout for a field labeled as a Git-object pin.

- [ ] **Step 4: Verify from extracted pinned blobs and run dispatch test GREEN**

Run: `pwsh -NoProfile -File .\test-r9-normative-bundle.ps1`  
Run: `pwsh -NoProfile -File .\test-r9-council-dispatch.ps1`  
Expected: both exit 0.

- [ ] **Step 5: Commit packet and delivery layer**

```powershell
git add test-r9-normative-bundle.ps1 MBCX-01-EXPERIMENT-COUNCIL-PACKET-r9.md MBCX-01-BROWSER-SEAT-PROMPT-r9.txt generate-seat3-experiment-r9-prompt.ps1 test-r9-council-dispatch.ps1 watch-seat3-codex-r9.ps1
git commit -m "council: prepare executable r9 review"
```

### Task 8: Dispatch and acceptance confirmation

**Files:**
- Create: `MBCX-01-COUNCIL-R9-DISPATCH-RECEIPT.md`
- Runtime only: Codex r9 prompt, logs, verdict, and completion marker.

**Interfaces:**
- Same maintained Claude and ChatGPT conversations through Moonwalker.
- One fresh read-only Codex EXEC process.

- [ ] **Step 1: Re-run all no-paid and dispatch gates from the final pin**

Run the full Python verifier, Git-object reconstruction test, dispatch test, and `git status --short` scope check.

- [ ] **Step 2: Deliver the exact browser pointer to both maintained seats through Moonwalker**

Confirm the r9 marker appears in each seat and generation begins. Close Moonwalker attachments without closing the operator's browser tabs.

- [ ] **Step 3: Start fresh Codex EXEC and verify process plus artifact paths**

Use the generated r9 prompt and watcher. Confirm the process is live and the verdict path is unique to r9.

- [ ] **Step 4: Record and commit the receipt**

```powershell
git add MBCX-01-COUNCIL-R9-DISPATCH-RECEIPT.md
git commit -m "council: record r9 dispatch"
```

- [ ] **Step 5: Yield without polling**

Tell the owner all three seats are visibly running, state that no paid experiment calls were made, and wait for the owner to wake the driver.
