# MBCX-01 r8 Reconstruction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, verify, pin, and dispatch an executable r8 MBCX-01 preregistration without paid inference.

**Architecture:** A dependency-free Python reference module owns canonical hashing, state transitions, cohort selection, mixture confidence sequences, and deterministic OC sampling. Five closed normative artifacts configure those behaviors; one behavioral verifier loads the real artifacts and executes literal adversarial witnesses before the delivery layer may pin them.

**Tech Stack:** Markdown, JSON Schema 2020-12, Python 3.13 standard library, PowerShell 7 for dispatch wrappers, Git, Moonwalker CDP, Codex EXEC.

**Spec:** `docs/superpowers/specs/2026-08-12-mbcx01-r8-reconstruction-design.md`

## Global Constraints

- Work in the canonical Downloads checkout on `codex/mbcx01-design-council` because maintained council seats adjudicate that exact path.
- Preserve every unrelated untracked file and operational log.
- Use no external Python dependency, no FD/FC/TN implementation, and no paid inference.
- Treat browser seats as maintained longitudinal lanes and Codex EXEC as fresh, read-only, and ephemeral.
- Do not dispatch until the committed five-artifact pin re-verifies from Git objects.

---

### Task 1: Behavioral Red Witness

**Files:**
- Create: `verify-r8-normative-bundle.py`
- Create: `mbcx01_r8_reference.py`

**Interfaces:**
- Consumes: the five r8 artifact paths and literal adversarial fixtures.
- Produces: `main() -> int`, plus `canonical_json`, `action_id`, `apply_event`, `mixture_interval`, `select_cohort`, and `simulate_oc` for later tasks.

- [ ] **Step 1: Write the failing verifier shell**

```python
REQUIRED = [
    "MBCX-01-EXPERIMENT-DESIGN-r7.md",
    "MBCX-01-STATE-ACTION-CONTRACT-v3.json",
    "MBCX-01-PACKET-SCHEMAS-v2.json",
    "MBCX-01-MEASUREMENT-CONTRACT-v2.json",
    "MBCX-01-INFERENCE-CONTRACT-v3.json",
]
missing = [path for path in REQUIRED if not Path(path).is_file()]
assert not missing, f"missing r8 artifacts: {missing}"
```

- [ ] **Step 2: Run the verifier and observe RED**

Run: `python .\verify-r8-normative-bundle.py`  
Expected: nonzero with all five missing r8 artifacts named.

- [ ] **Step 3: Add real behavioral tests**

Use hand-derived literals: the two ambiguous delimiter identities must produce distinct hashes; a prefix with 96 failures followed by 288 successes must not bind the terminal branch; a maximal schema-valid packet must serialize below 65,536 bytes; `(10000,64)` must be in the H-by-D grid; ambiguous acceptance must reject retry.

```python
def test_literal_breaks() -> None:
    assert action_id("S:A", "B") != action_id("S", "A:B")
    assert scientific_look(96) == "DIAGNOSTIC_ONLY"
    assert scientific_look(192) == "DIAGNOSTIC_ONLY"
    assert len(canonical_json(maximal_packet())) < 65536
```

- [ ] **Step 4: Commit the RED verifier**

Run: `git add verify-r8-normative-bundle.py mbcx01_r8_reference.py && git commit -m "test: add r8 executable red witnesses"`

### Task 2: Closed State and Packet Contracts

**Files:**
- Create: `MBCX-01-STATE-ACTION-CONTRACT-v3.json`
- Create: `MBCX-01-PACKET-SCHEMAS-v2.json`
- Modify: `mbcx01_r8_reference.py`
- Modify: `verify-r8-normative-bundle.py`

**Interfaces:**
- Consumes: JCS-compatible canonical JSON objects and closed contract tables.
- Produces: `action_id(scope_id: str, obligation_id: str) -> str`, `apply_event(state: dict, event_type: str, payload: dict) -> tuple[dict,str]`, and exact packet validators.

- [ ] **Step 1: Add failing action and transition witnesses**

```python
assert action_id("S:A", "B") != action_id("S", "A:B")
assert enumerate_ordered_pairs(event_types) == 289
assert apply_proposal(blocked_then_unblocked_children).result == "REJECTED"
```

- [ ] **Step 2: Observe RED against missing contracts**

Run: `python .\verify-r8-normative-bundle.py`  
Expected: nonzero at the first state/packet contract assertion.

- [ ] **Step 3: Implement closed contracts and reference behavior**

Define all seventeen payload/guard/effect/illegal-result records, the call-ledger state graph, opaque action catalog, five closed packet/output schemas, exact TaskPacket derivation, conditional WorkerHandoff rules, and exact scorer.

```python
def action_id(scope_id: str, obligation_id: str) -> str:
    preimage = {"schema_id": "ActionIdentityV1", "scope_id": scope_id,
                "obligation_id": obligation_id}
    return "ACT." + hashlib.sha256(canonical_json(preimage)).hexdigest().upper()

def apply_event(state: dict, event_type: str, payload: dict) -> tuple[dict, str]:
    rule = STATE_CONTRACT["event_types"][event_type]
    validate_closed_payload(payload, rule["payload_schema"])
    return execute_rule(copy.deepcopy(state), rule, payload)
```

- [ ] **Step 4: Run focused state/packet tests GREEN**

Run: `python .\verify-r8-normative-bundle.py --section state --section packets`  
Expected: `state: PASS`, `packets: PASS`.

- [ ] **Step 5: Commit the contracts**

Run: `git add MBCX-01-STATE-ACTION-CONTRACT-v3.json MBCX-01-PACKET-SCHEMAS-v2.json mbcx01_r8_reference.py verify-r8-normative-bundle.py && git commit -m "design: close r8 state and packet machines"`

### Task 3: Cohort and Measurement Contracts

**Files:**
- Create: `MBCX-01-MEASUREMENT-CONTRACT-v2.json`
- Modify: `mbcx01_r8_reference.py`
- Modify: `verify-r8-normative-bundle.py`

**Interfaces:**
- Consumes: frozen source hash record, 80 unique candidates per motif, and registered H/D/F values.
- Produces: `select_cohort(candidates: list[dict]) -> list[dict]` and `measurement_grid(contract: dict) -> set[tuple[int,int,int]]`.

- [ ] **Step 1: Add failing cohort and interaction witnesses**

```python
assert len({row["scenario_id"] for row in selected}) == 384
assert all(one_selected_cut_per_scenario(row) for row in selected)
assert len({(h,d) for h,d,f in grid if f == 16}) == 20
assert (10000, 64, 16) in grid
```

- [ ] **Step 2: Observe RED**

Run: `python .\verify-r8-normative-bundle.py --section cohort --section measurement`  
Expected: missing measurement contract and selection implementation failures.

- [ ] **Step 3: Implement deterministic selection and physical-work gates**

Use length-framed SHA-256 tuples for one-cut and retained-scenario ordering. Add full 20-cell grid, frozen 4096-byte pages, descendant accounting, CPU/memory/filesystem counters, strict unit-total inequalities, and six red candidates.

```python
def framed_hash(parts: list[str]) -> bytes:
    framed = b"".join(len(p.encode()).to_bytes(8, "big") + p.encode() for p in parts)
    return hashlib.sha256(framed).digest()

def measurement_grid(contract: dict) -> set[tuple[int, int, int]]:
    return {(h, d, 16) for h in contract["axis_values"]["H"]
                       for d in contract["axis_values"]["D"]}
```

- [ ] **Step 4: Run focused tests GREEN**

Run: `python .\verify-r8-normative-bundle.py --section cohort --section measurement`  
Expected: `cohort: PASS`, `measurement: PASS`.

- [ ] **Step 5: Commit**

Run: `git add MBCX-01-MEASUREMENT-CONTRACT-v2.json mbcx01_r8_reference.py verify-r8-normative-bundle.py && git commit -m "design: freeze r8 cohort and measurement gates"`

### Task 4: Exact Mixture Inference and Synthetic OC

**Files:**
- Create: `MBCX-01-INFERENCE-CONTRACT-v3.json`
- Modify: `mbcx01_r8_reference.py`
- Modify: `verify-r8-normative-bundle.py`

**Interfaces:**
- Consumes: bounded observations, alpha 0.025, kappa 0.25, SHA-256 counter stream, nine paired-probability cells.
- Produces: `mixture_interval(xs: list[float], alpha: float) -> tuple[float,float]`, `decision(delta_ci, om_ci) -> str`, and deterministic OC JSON.

- [ ] **Step 1: Add failing analytic/quadrature and branch witnesses**

```python
assert max(abs(a-b) for a,b in zip(analytic_ci, quadrature_ci)) <= 1e-9
assert decision_at_look(96) == "DIAGNOSTIC_ONLY"
assert decision_at_look(192) == "DIAGNOSTIC_ONLY"
assert simulate_oc(seed="R8-OC", reps=100) == simulate_oc(seed="R8-OC", reps=100)
```

- [ ] **Step 2: Observe RED**

Run: `python .\verify-r8-normative-bundle.py --section inference`  
Expected: nonzero because v3 and exact mixture functions are absent.

- [ ] **Step 3: Implement the exact registered method**

Implement predictable estimates, `psi_E`, stable exact integral, independent Simpson integration, bisection inversion, delta transform, terminal precedence, deterministic inverse-CDF pairs, and exact missingness enumeration through seven pairs.

```python
def psi_e(x: float) -> float:
    return -math.log1p(-x) - x

def predictable_variance(xs: list[float], kappa: float = 0.25) -> float:
    total, prefix = 1.0 / (2.0 * kappa * kappa), 0.0
    for i, x in enumerate(xs, 1):
        xhat = (0.5 + prefix) / i
        total += psi_e(abs(x - xhat))
        prefix += x
    return total

def scientific_look(n: int) -> str:
    return "TERMINAL" if n == 384 else "DIAGNOSTIC_ONLY"
```

- [ ] **Step 4: Run inference and compact OC GREEN**

Run: `python .\verify-r8-normative-bundle.py --section inference --oc-reps 1000`  
Expected: parity, reachability, repeatability, and branch-coverage PASS.

- [ ] **Step 5: Commit**

Run: `git add MBCX-01-INFERENCE-CONTRACT-v3.json mbcx01_r8_reference.py verify-r8-normative-bundle.py && git commit -m "design: add r8 exact mixture inference"`

### Task 5: Integrating Design and Full No-Paid Verification

**Files:**
- Create: `MBCX-01-EXPERIMENT-DESIGN-r7.md`
- Create: `MBCX-01-R8-NO-PAID-VERIFICATION.json`
- Modify: `verify-r8-normative-bundle.py`

**Interfaces:**
- Consumes: four machine-readable contracts and compact/full OC results.
- Produces: the fifth normative artifact and one retained, explicitly synthetic verification report.

- [ ] **Step 1: Write the integrated design**

State the finite-range claim, source freeze, full cohort procedure, six-call DAG, terminal-only inference, transport ambiguity, deterministic gates, branch precedence, cost maximum, and non-claims without contradicting the JSON contracts.

- [ ] **Step 2: Run the complete verifier**

Run: `python .\verify-r8-normative-bundle.py --oc-reps 10000 --report MBCX-01-R8-NO-PAID-VERIFICATION.json`  
Expected: every section PASS and report field `experiment_evidence=false`.

- [ ] **Step 3: Validate files and whitespace**

Run: `Get-Content MBCX-01-*-v*.json -Raw | ConvertFrom-Json | Out-Null; git diff --check`  
Expected: exit zero.

- [ ] **Step 4: Commit and pin the five-artifact bundle**

Run: `git add MBCX-01-EXPERIMENT-DESIGN-r7.md MBCX-01-R8-NO-PAID-VERIFICATION.json verify-r8-normative-bundle.py mbcx01_r8_reference.py && git commit -m "design: integrate executable r8 preregistration"`

### Task 6: Council Packet, Dispatch, and Yield

**Files:**
- Create: `MBCX-01-EXPERIMENT-COUNCIL-PACKET-r8.md`
- Create: `MBCX-01-BROWSER-SEAT-PROMPT-r8.txt`
- Create: `generate-seat3-experiment-r8-prompt.ps1`
- Create: `watch-seat3-codex-r8.ps1`
- Create: `test-r8-council-dispatch.ps1`
- Create: `MBCX-01-COUNCIL-R8-DISPATCH-RECEIPT.md`

**Interfaces:**
- Consumes: committed bundle Git blobs and the research-disposition note.
- Produces: two maintained browser turns and one fresh read-only Codex EXEC turn.

- [ ] **Step 1: Write and observe a failing dispatch test**

Run: `.\test-r8-council-dispatch.ps1`  
Expected: nonzero before the r8 packet and prompt machinery exist.

- [ ] **Step 2: Generate exact pins and council packet**

Include commit, blob, byte, line, and SHA-384 for all five normative artifacts; ask the four open research questions; forbid current-round lateral verdict inspection.

- [ ] **Step 3: Run all dispatch and normative tests GREEN**

Run: `python .\verify-r8-normative-bundle.py --oc-reps 1000; .\test-r8-council-dispatch.ps1; git diff --check`  
Expected: exit zero.

- [ ] **Step 4: Commit packet machinery and reverify pins**

Run: `git add MBCX-01-EXPERIMENT-COUNCIL-PACKET-r8.md MBCX-01-BROWSER-SEAT-PROMPT-r8.txt generate-seat3-experiment-r8-prompt.ps1 watch-seat3-codex-r8.ps1 test-r8-council-dispatch.ps1 && git commit -m "council: prepare executable r8 review"`

- [ ] **Step 5: Dispatch and yield**

Use Moonwalker CDP for the exact maintained Claude and ChatGPT conversations, verify active generation, launch a fresh read-only Codex EXEC with bounded watcher, write and commit the receipt, close only temporary attachments, and stop polling.
