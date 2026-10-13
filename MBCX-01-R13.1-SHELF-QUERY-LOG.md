# MBCX-01 r13.1 Shelf-Zero and Prior-Art Query Log

Status: recorded 2026-08-13; design evidence only; no BUILD or experiment authorization

## Frozen revisions

- MBCX design repository before the r13.1 fold: `5bc561aeb27d5b68d7047213bbccd493f0b7ccf3`.
- AgentVault MCP bridge shelf: `ba702fd6c7cc03a697862ed98b9f4d08cdf8d2bb`.
- Canonical shelf root queried: `C:/AgentVault/Moonwalker` (non-Git corpus).

## Exact internal queries

```text
rg -l -i "JobObject|completion port|ETW|TracePmc|state owner|state-owner|receipt|Ed25519" C:/Users/Kingo/source/agentvault-mcp-bridge -g "*.md" -g "*.py" -g "*.ps1" -g "*.js" -g "*.ts"
rg -l -i "council|operator independence|state owner|JobObject|ETW|receipt" C:/AgentVault/Moonwalker -g "*.md"
rg -n -i "JobObject|completion port|ETW|Ed25519|receipt|operator" docs/167-3b-live-wiring-DESIGN-v14-2026-08-05.md docs/_archive/m3-live-proof/m3.2-live-proof-harness-design.md tests/capture-evidence-record.test.ts tests/capture-conformance-evaluator.test.ts C:/AgentVault/Moonwalker/BUILD-FROM-THE-SHELF-CANON.md C:/AgentVault/Moonwalker/DESIGN-SHELF-MAP.md
```

## Shelf disposition

| Shelf item | Reusable fact | Disposition |
|---|---|---|
| `docs/167-3b-live-wiring-DESIGN-v14-2026-08-05.md` | independent durable receipt, supervisor-owned Job, operator/signer separation, crash/readback discipline | Adopt the authority and operator-independence pattern; do not import its unrelated security lifecycle. |
| `docs/_archive/m3-live-proof/m3.2-live-proof-harness-design.md` | live-proof harness ordering, rollback and network-isolation discipline | Reuse only as a BUILD test-shape; it is not Windows Job/PMC evidence. |
| `tests/capture-evidence-record.test.ts` and `tests/capture-conformance-evaluator.test.ts` | closed evidence records and evaluator mutation witnesses | Reuse test style, not CDP-specific evidence semantics. |
| `C:/AgentVault/Moonwalker/BUILD-FROM-THE-SHELF-CANON.md` | Shelf-Zero and prior-art-first gate | Applied here. |
| `C:/AgentVault/Moonwalker/DESIGN-SHELF-MAP.md` | ownership/shelf routing | No exact MBCX state adapter or PMC harness owner found. |

Shelf-Zero answer: the experiment design should exist, but neither missing production adapter should be invented inside the no-paid research bundle. The exact state-owner adapter and Windows evidence producer remain two bounded BUILD artifacts.

## External primary sources queried

- Microsoft `JOBOBJECT_BASIC_ACCOUNTING_INFORMATION`: https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_accounting_information
- Microsoft `JOBOBJECT_ASSOCIATE_COMPLETION_PORT`: https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_associate_completion_port
- Microsoft `TRACE_QUERY_INFO_CLASS`: https://learn.microsoft.com/en-us/windows/win32/api/evntrace/ne-evntrace-trace_query_info_class

These fix the four-DWORD Job ABI, the diagnostic-only status of ordinary completion messages, and the PMC counter/event attachment configuration.

## Future BUILD operator-independence witness

The production state adapter and Windows harness must each be exercised by two independently implemented operators over one frozen input set. Each operator must emit canonical receipt bytes without reading the other implementation or output. The BUILD gate compares byte-identical subject hashes, authority identities, ordered evidence sets and verdicts. A shared library may provide structural schemas and hashing only; it may not provide state transition effects, evidence collection, finalization or verdict derivation. Poisoning one operator's finalizer must produce a detected disagreement. This witness is a future BUILD prerequisite, not evidence supplied by r13.1.
