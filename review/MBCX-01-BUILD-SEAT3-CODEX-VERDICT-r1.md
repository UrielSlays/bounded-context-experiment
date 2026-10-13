# MBCX-01 BUILD acceptance SEAT3 (codex-exec, gpt-5.6-sol xhigh) verdict — r1 — banked from stdout log

> Banked 2026-08-14 by the driver from MBCX-01-BUILD-SEAT3-CODEX-EXEC-r1.log (marker exit 0).
> Verdict: NO-GO. Its deciding finding (F1/F2, caller-supplied trust root) was REPRODUCED at the byte by the driver before banking.

# NO-GO

Fix class: **architecture/security — trust-root bootstrap and custody authentication**. Secondary fix class: **canonical encoding validation**.

The BUILD’s central C2/C5 boundary is false: an API caller can supply a self-authored manifest, self-authored custody documents, and its own signing root, then obtain empty production-admission errors. This contradicts the packet’s explicit API-caller adversary model and requires council re-review, not a leaf patch.

## Pin and execution record

- Packet pin resolved to `8516ea48b61da0affc70b06733d4f902f05b3e7a`; HEAD and branch matched.
- Content pin resolved to `2fd38972ca40820e5e4ac049b18ca480f29392c8` and is an ancestor of the packet pin.
- Reviewed working-tree code matched the content pin; the packet matched the review-head pin. Tracked worktree remained clean. I did not open or touch untracked council/driver files.
- Manifest object `5f5cd20b0fc526edca81bd285920ee52bf374b36` is a Git blob.
- `MBCX01_BUILD_ALLOW_PHYSICAL` remained unset. No experiment, provider/model call, real Job/ETW collection, signing ceremony, or spend occurred.
- The pinned clean-room command exited 0 in 107 seconds:
  - 145 frozen tests passed.
  - 76 BUILD tests passed.
  - 34 repair-ledger invariants / 76 witnesses passed.
  - Strict schemas, 12 mutants, canonical parity, no-production-activation and execution-posture checks passed.
  - Reported readiness remained `BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`.
- Red witnesses were reconstructed at `6c3bc2a9f240e9dc7d22dabda15e0b11b980c155`:
  - State: 25 tests, `failures=26, errors=5`, exit 1.
  - Measurement: 44 tests, `failures=16, errors=46`, exit 1.
  - The corresponding 81 frozen tests passed.
  - The packet says “24 red”; the executable committed suite ran 25. For “what happened when it ran,” my execution governs.
- All probe directories were confined to the system temp directory and deleted after execution.

## Why this exists

1. **ALREADY-BUILT? — EXECUTED / SEARCHED**

   The packet contains a non-vacuous internal-shelf log: revisions, exact queries, files opened, and adopt-or-why-not decisions at `MBCX-01-BUILD-SHELF-LOG.md:7-38@2fd38972…`.

   I spot-ran:

   `rg -l -i 'single.?writer|writer_gate|readback|append.?first|evidence.?before.?effect' <home>\source\Photon\crates`

   It returned the same six Aruna files recorded by the log. I also spot-ran the Gravity Job-object query and obtained the recorded slice0c/r2 family.

   I found no exact internal implementation of the MBCX state-owner receipt, six-call evidence join, or signed Job/ETW producer. The BUILD appropriately adopts SQLite, Photon’s one-door writer-gate pattern, Gravity’s Job/EvidenceSigner patterns, and platform Ed25519. However, its trust-bootstrap subsystem should adopt established preconfigured-root and authenticated-role mechanisms from SLSA/TUF instead of building a self-referential custody scheme.

2. **PRODUCT-FIT? — EXECUTED / UNSEARCHED (SETTLED-BY-PINNED-BYTES)**

   Customer need, in one sentence: **Let an operator turn a deterministic six-call run into scientifically admissible state and measurement evidence while failing loudly and leaving activation authority with the operator.**

   That need fits GOVERNED POWER / FAIL-LOUD / MIRROR-NOT-COP. The implemented trust bootstrap does not: it silently clears the sentinels for caller-authored authority material. The product posture is right; the implemented admission boundary is not.

3. **BIGGER-THAN-THE-BUG? — READ-ONLY / UNSEARCHED (SETTLED-BY-PINNED-BYTES)**

   This is a new subsystem—SQLite authority journal, independent operators, state and measurement admission, trust manifests, custody documents, and Windows evidence collection—not a leaf fix. It was expressly commissioned through the r13.2 design gate rather than smuggled through a review finding, so its original size was procedurally justified.

   The discovered trust-bootstrap defect is itself architectural/security-significant. Correcting it must re-enter the DESIGN/council gate.

## Findings

### F1 — C2/C5 fail: state “production” accepts fixture-only, syntactic custody

**EXECUTED / UNSEARCHED (SETTLED-BY-PINNED-BYTES) — deciding NO-GO**

The state verifier requires the supposed production manifest to say:

- `production_ready is False`
- policy status `NOT_ACTIVATED`
- every root `fixture_only is True`

See `mbcx01_build_state_authority.py:306-330@2fd38972…`.

Its custody check receives no custody documents to authenticate. It checks only distinct role strings, disjoint key-ID lists, and that four supplied values look like 96-character SHA-384 hex strings: `:334-357@2fd38972…`.

The positive production test then signs with the committed fixture private key and expects both V2 verification and production scorer admission to return `[]`: `test_mbcx01_build_state.py:45-84,358-395@2fd38972…`.

Fresh probe:

- Replaced all four alleged custody-document digests with the same arbitrary `"A" * 96`.
- Kept the fixture-only, `NOT_ACTIVATED`, `production_ready:false` manifest.
- Result:
  - `verify_state_authority_receipt_v2` → `[]`
  - `verify_production_scorer_input` → `[]`

Thus fixture/self-authored evidence does clear state production admission.

### F2 — C2/C5 fail: measurement authority is entirely caller-bootstrapable

**EXECUTED / UNSEARCHED (SETTLED-BY-PINNED-BYTES) — deciding NO-GO**

The measurement API receives the trust manifest and all custody evidence from the caller. The manifest is not signed or anchored to owner configuration. Custody documents are also unsigned; the verifier merely recomputes their hashes against digest fields in the same caller-supplied manifest: `mbcx01_build_measurement_authority.py:173-341,653-684@2fd38972…`.

The tests demonstrate the construction:

- Committed fixture private key: `test_mbcx01_build_measurement.py:59-69@2fd38972…`
- Four self-created custody documents: `:90-117`
- In-memory manifest flipped to `ACTIVATED`, `production_ready:true`, `fixture_only:false`: `:126-187`
- Same helper produces the signer and custody evidence: `:190-196`

Fresh probe created a completely self-described authority stack:

- Attacker manifest ID and activation authority.
- Attacker-named signer/editor roles and editor key ID.
- Attacker attestation, approval and ceremony identifiers.
- Recomputed all custody, policy and root digests.
- Signed all 100 measurement envelopes with the committed test key.

`evaluate_production_measurement` returned `[]`.

The named tests catch equal role strings, signer/editor key collision, revocation, expiry and stale digests. They do not establish that distinct strings or IDs represent independent principals. C5’s custody separation is syntactic, not mechanical.

**READ-ONLY / SEARCHED corroboration:** SLSA verification starts from a **preconfigured root of trust** and trusted producer identities; it does not accept the provenance subject’s own root as its bootstrap. [SLSA v1.2, “Verifying artifacts,” Step 1](https://slsa.dev/spec/v1.2/verifying-artifacts). TUF similarly ships trusted root keys and role thresholds with the client and requires signed root continuity. [TUF specification §§2.1 and 5.3](https://theupdateframework.github.io/specification/v1.0.20/).

### F3 — C1 held under fresh defect laundering attempt

**EXECUTED / UNSEARCHED (SETTLED-BY-PINNED-BYTES)**

Baseline connected graph:

- Fixture-mode frozen errors: `[]`
- Production errors: `A0_PACKET_INVALID`, `I02_INVARIANT_INVALID`, `STATE_AUTHORITY_UNAVAILABLE`
- Clean V2 admission: `[]`

I changed `a0_packet.packet_hash` to a shape-valid but false all-zero SHA-384 value while preserving a clean V2 receipt.

Fixture-mode rejection became:

`A0_CALL_INVALID, A0_PACKET_INVALID, A0_RESULT_INVALID, I03_INVARIANT_INVALID, I04_INVARIANT_INVALID, TASK_PACKET_INVALID`

Production admission preserved every one of those errors. The subtractive formula at `mbcx01_build_state_authority.py:739-774@2fd38972…` did not launder the defect.

Residual: correctness remains coupled to the hard-coded cascade closure and the frozen validator’s future error relationships. The subset gate fails closed for the fresh attack and banked cases.

### F4 — C3 held for durable PENDING/BROKEN tampering

**EXECUTED / UNSEARCHED (SETTLED-BY-PINNED-BYTES)**

I created a valid file-backed transaction and receipt, closed the writer, then independently changed the journal terminal to `PENDING` and `BROKEN` while leaving effect rows present.

Fresh-path verification returned, for both:

`STATE_AUTHORITY_UNAVAILABLE` and `STATE_AUTHORITY_V2_TRANSACTION_NOT_COMMITTED`

The record-before-effect/atomic-effect protocol is at `mbcx01_build_state_store.py:350-442@2fd38972…`; terminal classification is at `:594-623`; registry-free read-only verification is at `:635-658`.

Residual: this proves application-level classification, not physical power-loss behavior of the specific filesystem/VFS. Physical testing was outside authority.

### F5 — C4 held for coherent replay and operator poisoning

**EXECUTED / UNSEARCHED (SETTLED-BY-PINNED-BYTES)**

I coherently altered all five replay axes—nonce, scope, scenario, run and subject—repaired the outer canonical preimage/digest, and re-signed with the valid fixture key.

Verification returned:

`STATE_AUTHORITY_UNAVAILABLE` and `STATE_AUTHORITY_V2_REPLAY_IDENTITY_INVALID`

The durable journal anchors won over receipt-local labels. The banked operator-B finalizer-poison witness also passed. Relevant bytes: `mbcx01_build_state_store.py:350-388,594-623@2fd38972…` and `mbcx01_build_state_operator_b.py:97-207@2fd38972…`.

### F6 — omission attack: signature carrier is malleable

**EXECUTED / SEARCHED**

`signature_b64` is deliberately excluded from the signed/canonical receipt content: `mbcx01_build_state_authority.py:138-139,196-198@2fd38972…`. The Node verifier decodes it with permissive `Buffer.from(value, "base64")`: `verify-r13-receipt-signature.mjs:15-23@2fd38972…`.

Fresh probe inserted a newline into an otherwise valid 64-byte Ed25519 signature’s base64 representation without re-signing:

- Baseline verification: `[]`
- Newline-bearing signature verification: `[]`

Node documents that its base64 decoder ignores whitespace and also accepts the base64url alphabet. [Node Buffer encodings](https://nodejs.org/api/buffer.html#buffers-and-character-encodings).

This does not forge authority, but it permits multiple accepted carrier byte strings for the same signature, creating receipt-identity, deduplication and audit-log ambiguity.

Fix class: canonical encoding—strict base64 grammar/padding/length and decode/re-encode equality before cryptographic verification.

## Evidence read

Primary load-bearing bytes:

- `MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r1.md:1-216@8516ea48…`
- `MBCX-01-BUILD-COMPLETION-HANDOFF.md:1@e6f7bdba…`
- `verify-build-pinned.ps1:44-73@2fd38972…`
- `MBCX-01-BUILD-SHELF-LOG.md:7-38@2fd38972…`
- `MBCX-01-BUILD-STATE-TRUST-ROOTS-V1.fixture.json:2-92@2fd38972…`
- `mbcx01_build_state_store.py:29-56,350-442,594-658@2fd38972…`
- `mbcx01_build_state_authority.py:138-198,306-397,592-665,691-774@2fd38972…`
- `mbcx01_build_state_operator_b.py:97-207@2fd38972…`
- `mbcx01_build_measurement_authority.py:173-341,653-720@2fd38972…`
- `mbcx01_build_integration.py:110-175@2fd38972…`
- `test_mbcx01_build_state.py:45-84,358-395@2fd38972…`
- `test_mbcx01_build_measurement.py:59-69,90-196@2fd38972…`
- `verify-r13-receipt-signature.mjs:15-23@2fd38972…`
- `verify-build-canonical-parity.mjs:11-40@2fd38972…`
- `MBCX-01-BUILD-REPAIR-LEDGER.json:1@2fd38972…`
- Red suites at `6c3bc2a9f240e9dc7d22dabda15e0b11b980c155`; banked transcripts at the content pin.

## Sweep log

- **SEARCHED** — `site:sqlite.org wal.html synchronous FULL power failure WAL commit durability`  
  Opened [SQLite WAL §§2.3, 4 and 5](https://sqlite.org/wal.html). Confirmed that `synchronous=FULL` syncs the WAL for each commit while NORMAL has different power-loss durability, and that WAL sidecars affect read-only recovery. Stopped because the controlling SQLite source settled the configured semantics; real power-loss remained deliberately unexecuted.

- **SEARCHED** — `site:learn.microsoft.com JOBOBJECT_BASIC_ACCOUNTING_INFORMATION TotalTerminatedProcesses QueryInformationJobObject`  
  Opened [JOBOBJECT_BASIC_ACCOUNTING_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_accounting_information), especially `TotalTerminatedProcesses`. Confirmed that it counts processes terminated for limit violations, not ordinary exits.

- **SEARCHED** — `site:learn.microsoft.com TRACE_QUERY_INFO_CLASS TracePmcEventListInfo TracePmcCounterListInfo`  
  Opened [TRACE_QUERY_INFO_CLASS](https://learn.microsoft.com/en-us/windows/win32/api/evntrace/ne-evntrace-trace_query_info_class). Confirmed ordinals 8 and 9 and their platform-version descriptions.

- **SEARCHED** — `site:learn.microsoft.com ProcessTelemetryIdInformation ProcessStartKey NtQueryInformationProcess`  
  Opened [PROCESS_TELEMETRY_ID_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winternl/ns-winternl-process_telemetry_id_information), especially `ProcessStartKey` and Requirements. It confirmed the field and Windows-version floor but did not establish the private `NtQueryInformationProcess` class ordinal. The packet’s smoke-stage ordinal residual therefore remains open.

- **SEARCHED** —  
  `site:slsa.dev/spec/v1.2 verifying artifacts trusted producer identity signature verification`  
  `site:theupdateframework.github.io/specification root role threshold keys trusted root metadata`  
  Opened [SLSA Step 1](https://slsa.dev/spec/v1.2/verifying-artifacts) and [TUF §§2.1/5.3](https://theupdateframework.github.io/specification/v1.0.20/). These changed the assessment from “custody validation defect” to “missing external trust bootstrap”: both models start from verifier-controlled trust, not candidate-supplied roots.

- Query with no deciding source opened: `site:in-toto.io attestation framework statement predicate verification identities`. I reworded around the mechanism and obtained the controlling SLSA/TUF primaries above; the unopened result was not used.

- **SEARCHED** —  
  `site:rfc-editor.org RFC 8785 JSON canonicalization Unicode sorting invalid Unicode data`  
  `site:rfc-editor.org RFC 8259 surrogate interoperability JSON strings`  
  Opened [RFC 8785 §§1, 3.2.2.2 and 3.2.3](https://www.rfc-editor.org/rfc/rfc8785.html) and [RFC 8259 §8.2](https://www.rfc-editor.org/rfc/rfc8259.html). Confirmed that the BUILD’s Python/Node parity is a custom canonicalization contract, not JCS, and that lone-surrogate handling remains an interoperability residual.

- **SEARCHED** —  
  `site:rfc-editor.org/rfc/rfc8032 Ed25519 verification canonical encoding security considerations`  
  `site:csrc.nist.gov FIPS 186-5 EdDSA Ed25519 approved digital signature`  
  Opened [RFC 8032 §§5.1.7 and 8.4](https://www.rfc-editor.org/rfc/rfc8032.html) and [NIST FIPS 186-5](https://csrc.nist.gov/pubs/fips/186-5/final). Confirmed the Ed25519 signature length/malleability requirements and that EdDSA is standardized. These do not authenticate the caller-supplied trust root.

- **SEARCHED** —  
  `site:nodejs.org/api/buffer.html Buffer.from base64 whitespace ignored base64url alphabet`  
  `site:nodejs.org/api/buffer.html base64 decoder assumes valid input whitespace ignored`  
  Opened [Node Buffer encodings](https://nodejs.org/api/buffer.html#buffers-and-character-encodings). Confirmed the executed signature-carrier malleability.

- **SEARCHED** —  
  `site:learn.microsoft.com job objects completion port messages delivery not guaranteed JOB_OBJECT_MSG_ACTIVE_PROCESS_ZERO`  
  `site:learn.microsoft.com CreateProcess CREATE_SUSPENDED AssignProcessToJobObject before resume`  
  `site:learn.microsoft.com job objects breakaway silent breakaway nested jobs AssignProcessToJobObject`  
  `site:learn.microsoft.com QueryInformationJobObject JobObjectBasicAndIoAccountingInformation structure 96 bytes`  
  Opened [AssignProcessToJobObject remarks](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject), [completion-port association remarks](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_associate_completion_port), [nested jobs](https://learn.microsoft.com/en-us/windows/win32/procthread/nested-jobs), and [basic-and-I/O accounting structure](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_and_io_accounting_information). Confirmed suspended-create/assign-before-resume discipline, child inheritance/breakaway behavior, diagnostic—not guaranteed—completion messages, and accounting composition.

I stopped because controlling primary sources had settled the platform and trust-model claims relevant to this review. The remaining physical and private-ordinal questions were explicitly outside authorized execution. The NO-GO itself rests on pinned bytes and fresh executable bypasses, not source count.

## Residual risks

- Real Windows Job/ETW collection remains unexecuted.
- SQLite filesystem/VFS power-loss behavior remains unexecuted.
- `ProcessTelemetryIdInformation` information-class ordinal remains a smoke-stage check.
- Production validity depends on callers supplying a real evaluation instant; the deterministic `published_at` default remains weaker.
- Per-witness physical carrier exactness remains deferred.
- Custom JSON canonicalization has an untested lone-surrogate edge.
- T2 box-owner attacks remain intentionally outside the claim.
- Signature base64 carrier malleability remains open until the leaf encoding fix.

## Required fix classes

1. **Architecture/security:** anchor state and measurement verification in an owner/preconfigured trust root outside the candidate-controlled manifest/custody arguments.
2. **Architecture/security:** authenticate manifests and custody evidence, with signer/editor/witness separation established by independently trusted keys or threshold signatures—not distinct role strings.
3. **Interface/architecture:** keep fixture/conformance authority incapable of invoking the production sentinel-discharge API; state production validation must not require `NOT_ACTIVATED` fixture roots.
4. **Canonical encoding:** strictly validate signature base64 representation.
5. **Documentation:** reconcile the packet’s 24-state-red count with the committed executable suite’s 25 tests.

Because items 1–3 change the trust architecture, interface and security boundary, this BUILD must return to council review.
