# MBCX-01 r10 implementation plan

Date: 2026-08-12

## Task 1: Freeze design and prior art

- Add the r10 architecture and cited prior-art memo.
- Preserve every r9 artifact unchanged.
- Verify the transport acceptance-plan arithmetic independently in Python.

## Task 2: Red tests for council defects

- Create r10 state, packet, cohort, measurement, inference, integration, and reconstruction checks.
- First run must fail because the v5/v4/r10 artifacts do not yet exist.
- Each test names the defect it prevents.

## Task 3: State and schema repair

- Add state/action contract v5 with composed event schemas.
- Implement real ingress validation plus calendar-valid UTC parsing.
- Implement two structurally independent post-ingress reducers.
- Add fact visibility/effectivity and handoff/action/hash adversarial cases.
- Compile and exercise all packet and event schemas with pinned Ajv strict mode.

## Task 4: Packet and cohort repair

- Add packet schemas v4, including writer receipt and expected manifest.
- Implement canonical-world semantic validation, exact 65,536-byte rendering, and five-object exact scoring.
- Enforce global scenario uniqueness, known motifs, exact totals, deterministic pre-eligibility cut, and 768 selected pairs.

## Task 5: Measurement and call-ledger repair

- Add measurement contract v4 with complete process-tree counters and separate boundedness/affordability decisions.
- Add executable provider-call transition matrix and exhaustively test state/event pairs.
- Exercise root `10H`, child `10H`, `5H`, and constant-over-budget diagnostics over the complete grid.

## Task 6: Inference and transport repair

- Add inference contract v5.
- Implement exact missing-completion DP and compare it with exhaustive enumeration on small cases.
- Freeze the numerical assurance region and diagnostic-only transition cells.
- Prove the 456/4 reliability plan from exact binomial tails.

## Task 7: Reconstruction and verification

- Generate the no-paid verification report.
- Add an owner-pinned SHA-384 manifest.
- Add a PowerShell-compatible Git-object extractor that verifies before importing.
- Commit the governing bundle, then execute both the working-tree and reconstructed-blob verifiers.

## Task 8: Council packet and dispatch

- Bank all r9 verdicts as evidence for the repair.
- Create an r10 packet that asks each seat to attack the exact repaired boundaries and return one verdict.
- Pin the governing commit and manifest blob.
- Send to the maintained Opus and ChatGPT seats and one fresh Codex EXEC seat through Moonwalker.
- Confirm dispatch, close only temporary automation attachments, record a receipt, and stop polling until the owner wakes this task.

