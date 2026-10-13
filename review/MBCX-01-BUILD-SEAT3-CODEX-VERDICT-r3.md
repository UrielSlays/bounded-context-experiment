# MBCX-01 BUILD acceptance r3 — SEAT3 codex-exec verdict (banked verbatim from the run log)

Source: MBCX-01-BUILD-SEAT3-CODEX-EXEC-r3.log lines 9591-9883 (FINAL verdict block; the log emits it twice — a streamed copy at 9296 and this final one after the 'tokens used' marker at 9589).
Model gpt-5.6-sol, xhigh, service_tier=default. Prompt MBCX-01-BUILD-SEAT3-CODEX-EXEC-PROMPT-r3.txt. Code pin aa3d0b1a.
Exit 0 AND the log carries a real verdict — verified by log-tail read + finding headers, not by the exit code.

# NO-GO — EXECUTED

The r3 fold does not isolate production authority from fixture material. A caller-supplied behavior-bearing mapping can bypass the wiring guard by calling `object.__setattr__` on the supposedly immutable anchor/context. I executed this against the pinned production bytes: fixture-signed material was admitted by measurement, exactness, and state. Failed verification left the context poisoned, and overlapping thread scopes independently corrupted/restored the global wiring incorrectly.

These are production-authority failures, not documentation defects. C‑R3‑1, C‑R3‑2, and C‑R3‑3 are false. C‑R3‑4 and C‑R3‑5 pass.

## Pin and execution record

- Packet pin verified: `MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r3.md:1-264@e2e6c662ad885001cd705dfd64c296f03d762398`.
- Code pin verified: `aa3d0b1a4fbd843beb23af9cbd8e94e99de20f5a`.
- Governing manifest: blob `3e2a67536797faa6afa17ddf4d1363950131cbc6`, committed at `994540bd`. It wins over the older manifest embedded at the code pin because the packet explicitly pins the later regenerated manifest.
- Pinned production subjects byte-match `aa3d0b1…`.
- During review, HEAD advanced externally from `e2e6c662…` to `4969d59e…`. The packet remained byte-identical and the production subjects still matched the code pin. I did not open the newly added unrelated artifacts.
- `MBCX01_BUILD_ALLOW_PHYSICAL=UNSET`.
- No experiment, provider/model call, Job/ETW collection, physical run, paid call, or signing ceremony was performed.
- No repository file was modified by this seat. Transient reconstruction/probe material was discarded.

### Clean-room reconstruction — EXECUTED

The packet’s pinned reconstruction completed in 128.7 seconds:

- 145 frozen tests: PASS
- 95 BUILD witnesses: PASS
- ledger: 42 invariants / 95 witnesses, two-way mapping: PASS
- schemas, canonical parity, no-production-activation check, execution posture: PASS
- reported readiness: `BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`
- reconstruction report discarded as instructed

### Banked witnesses — EXECUTED

I independently reconstructed pre-fix `491b0ab…` from 356 verified tracked blobs and reran the banked probe:

- fixture owner key admitted at all production doors;
- behavior-bearing mapping rewired authority;
- integration leaked fixture wiring;
- stale-2001 trust material admitted;
- binding-only exactness appeared as `PASS`;
- duplicate-member anchor was accepted.

Against `aa3d0b1…`, the banked probe reports the expected named refusals, scoped restoration, stale rejection, explicit binding-only result, and duplicate rejection. That proves the intended fold happened; it does not close the fresh bypass below.

## Why this exists

### 1. ALREADY-BUILT? — EXECUTED — SEARCHED

Yes, the mechanism’s shape already exists and should have been adopted more faithfully.

The packet carries a formal three-repository shelf log, but its specialized trust-context search is too narrow. I spot-ran its exact bridge query:

`process\.env.*(TRUST|ANCHOR|ROOT_KEY)` over `agentvault-mcp-bridge/src` → zero matches.

I then searched all three Moonwalker repos for the mechanism rather than only environment-variable spellings. At the packet’s own bridge shelf base `ba702fd6c7…`, I found:

- `src/enrollment.ts:137-177@ba702fd6c7`: installer-pinned offline root passed explicitly into signature verification.
- `src/runtime-trust.ts:180-240@ba702fd6c7`: verified trust construction with supplied time, copied/frozen fields, and runtime provenance.
- `src/broker-proxy.ts:253-365@ba702fd6c7`: private runtime brand, read-once snapshot discipline, nested-copy freeze, and no reread of hostile input.

Those three blobs are identical at the bridge repository’s current committed HEAD. This is not a directly importable TypeScript library for Python, but it is exact internal prior art for the security pattern. The packet’s “no loader/context precedent” conclusion is false.

External named prior art independently agrees: Go’s verifier takes roots and current time in `VerifyOptions`; TUF begins an update with a fixed verifier time and out-of-band trusted root; SLSA describes verifier-preconfigured roots. Those are patterns, not authorities over MBCX.

### 2. PRODUCT-FIT? — READ-ONLY — SEARCHED

Customer need, in one sentence:

> Let the operator choose the production root and verification instant while every absent, fixture-only, stale, or unverifiable authority condition remains a named refusal.

That need fits GOVERNED POWER, FAIL-LOUD, and MIRROR-NOT-COP.

The implementation’s stronger claims—“not representable,” “immutable,” and “cannot become production authority by any sequence”—are completeness/prevention claims that the Python object boundary does not support. When behavior-bearing request objects remain in scope, pretending manual `__setattr__` overrides provide true immutability is contrary to the product posture. The honest choices are an inert-byte boundary, a stronger isolation boundary, or an explicit `UNDETERMINED`/out-of-scope result.

### 3. BIGGER-THAN-THE-BUG? — EXECUTED

Yes. I press my r2 dissent.

The originating fixture-flag defect grew into a new context type, global wiring manager, global verification-depth state machine, scoped installation lifecycle, injected-clock policy, and cross-door interface changes. The fresh lifecycle, concurrency, and mutability failures demonstrate that this was a subsystem/design change and should have re-entered the DESIGN gate with shelf-check, product-fit, concurrency semantics, and owner approval.

My r2 verdict is `READ-ONLY — OWN-SEAT LONGITUDINAL CONTEXT, NON-DECIDING`; the r3 conclusion rests independently on the pinned bytes and executions reported here.

## Claim disposition

| Claim | Result | Byte/scenario that defeats it or residual |
|---|---|---|
| C‑R3‑1 fixture material cannot grant production authority | **FALSE — EXECUTED** | A fixture context can be constructed with `object.__new__`; request callbacks can change `fixture_only` to `False` and replace `context.anchor`. Fixture-signed measurement and state returned `[]`; exactness admitted the explicit binding-only result. |
| C‑R3‑2 no request-reachable authority mutation | **FALSE — EXECUTED** | `.get`/`__getitem__` callbacks bypass the public wiring guard through `object.__setattr__`. Poison survives a failed verification. Threaded scoped installations restore global state out of order. |
| C‑R3‑3 verifier owns freshness time | **FALSE — EXECUTED** | Exactness reads the caller receipt before resolving its context. A receipt callback changed `context.current_time` from 2026 to 2000; a manifest expired in 2001 was admitted. |
| C‑R3‑4 binding-only result cannot claim suite execution | **PASS — EXECUTED** | Output is `AUTHORITY_BINDING_ONLY_SUITE_NOT_EXECUTED`; submitted `PASS` is rejected. Repo consumer search found only integration packaging, tests, and documentation. Residual: this still proves binding only, never suite execution. |
| C‑R3‑5 r2-confirmed behavior did not regress | **PASS — EXECUTED** | Full suites, trustboot, seven splice axes, carrier spellings, false-reject repair, and unanchored refusals passed. Authentication callers at the pin are the measurement/state production paths; no legacy context-free caller was found. |

## Findings

### F1 — Critical: request-reachable fixture-authority admission — EXECUTED — SEARCHED

Relevant bytes:

- `mbcx01_build_trust_anchor.py:193-277@aa3d0b1…`
- `mbcx01_build_trust_anchor.py:408-444@aa3d0b1…`
- `mbcx01_build_trust_anchor.py:581-646@aa3d0b1…`

The ordinary constructor correctly refuses a fixture anchor. A second path succeeds:

1. `object.__new__(ProductionVerifierContext)`
2. `object.__setattr__` populates `anchor`, `current_time`, and `source`
3. `configure_production_verifier_context` accepts it because it only checks `isinstance`
4. the resolver returns that context without a fixture refusal.

More seriously, a caller-supplied `dict` subclass changed the existing fixture anchor’s `fixture_only` slot to `False` and replaced the snapshotted context’s anchor while verification read the request.

Executed results:

- measurement: `[]`
- exactness: admitted `AUTHORITY_BINDING_ONLY_SUITE_NOT_EXECUTED`
- state: `[]`
- callback counts: measurement 15, exactness 14, state 27

The activation was signed by the committed fixture private key named by the packet.

Python 3.11’s own documentation says true immutable Python objects cannot generally be created; frozen setters only emulate immutability. That directly confirms what the executed bypass demonstrates. [Python 3.11 dataclasses, “Frozen instances”](https://docs.python.org/3.11/library/dataclasses.html#frozen-instances).

The packet’s generic exclusion of arbitrary in-process classes conflicts with C‑R3‑2’s specific inclusion of caller-supplied mappings with `.get`, `__getitem__`, and other behavior. The banked r2 gadget itself is such a class. The same callback capability cannot be in scope when it invokes the public rewire function but out of scope when it invokes `object.__setattr__`.

### F2 — Critical: failed verification leaves authority poisoned — EXECUTED — UNSEARCHED — SETTLED-BY-PINNED-BYTES

A malicious mapping mutated the installed context, then deliberately failed verification with the wrong run ID.

First result:

`['MEASUREMENT_ENVELOPE_INVALID', 'MEASUREMENT_REPLAY_IDENTITY_MISMATCH', 'PHYSICAL_HARNESS_UNAVAILABLE']`

After the failure:

- the context still referenced the fixture anchor;
- `fixture_only` remained `False`;
- a subsequent ordinary fixture-signed request returned `[]`.

The scope’s `finally` restores only `_VERIFICATION_DEPTH`; it does not restore the semantic contents of the already-mutated wiring/context.

### F3 — High: process-global scoped wiring is not thread-safe — EXECUTED — SEARCHED

Relevant bytes:

- `mbcx01_build_trust_anchor.py:294-336@aa3d0b1…`
- `mbcx01_build_trust_anchor.py:447-466@aa3d0b1…`

Positive results:

- nested verification depths were `0 → 1 → 2 → 1 → 0`;
- public reconfiguration during nested verification raised `AuthorityWiringDuringVerification`;
- a forced verifier exception restored depth to zero;
- later configuration was possible.

Failures:

- While a worker was actively verifying under context B, the main thread exited `installed_production_verifier`; its unguarded `finally` restored global context A during verification.
- With overlapping thread scopes A then B, A exited first, B exited second. The final global context became A instead of the original context.

Observed sequence:

`B active → ORIGINAL after A exits → A after B exits`

Thus the “freeze” is a process-global counter plus uncoordinated global assignment, not a concurrency-safe authority scope. Python’s documentation explicitly distinguishes reentrancy from thread safety and notes that global-state context managers are not thread-safe; `ContextVar` provides token-based restoration and separate top-level contexts per thread. [Python contextlib](https://docs.python.org/3.11/library/contextlib.html#single-use-reusable-and-reentrant-context-managers), [Python contextvars](https://docs.python.org/3.11/library/contextvars.html).

### F4 — Critical: exactness lets request data steer the verifier clock — EXECUTED — SEARCHED

Relevant bytes:

- `mbcx01_build_exactness_authority.py:149-202@aa3d0b1…`
- `mbcx01_build_measurement_authority.py:226-330,826-849@aa3d0b1…`

Exactness reads caller-controlled receipt fields before resolving the production context. I installed a non-fixture operator context with:

`current_time=2026-08-14T00:00:00Z`

A malicious receipt’s `.get` callback changed the same context to:

`current_time=2000-06-01T00:00:00Z`

It then submitted a correctly signed trust manifest with validity:

`2000-01-01T00:00:00Z ≤ t ≤ 2001-01-01T00:00:00Z`

Executed output:

- receipt callbacks: 3
- mutated context time: `2000-06-01T00:00:00Z`
- exactness admitted: `AUTHORITY_BINDING_ONLY_SUITE_NOT_EXECUTED`

The artifact therefore supplied behavior that selected the “verifier” time and made stale trust material current.

### F5 — Medium: validity endpoints disagree across doors — EXECUTED — SEARCHED

Relevant bytes:

- measurement: `mbcx01_build_measurement_authority.py:293-328@aa3d0b1…`
- state: `mbcx01_build_state_authority.py:486-503,532-569@aa3d0b1…`

Fresh boundary probe:

- measurement accepted at `not_before`, one second before `not_after`, and exactly at `not_after`;
- state accepted one second before `not_after` but rejected exactly at `not_after` with `KEY_REVOKED_OR_EXPIRED`.

Go X.509 uses an inclusive upper endpoint, while the current TUF specification requires expiry to be strictly greater than the fixed update time. Neither standard governs MBCX; they show that either convention is possible. The pinned MBCX bytes must choose one convention consistently. [Go `crypto/x509` validity check](https://go.dev/src/crypto/x509/verify.go), [TUF §§5.1–5.6](https://theupdateframework.github.io/specification/latest/).

### F6 — Governance: internal prior art was missed — EXECUTED — SEARCHED

The three-repo shelf log exists, so this is not a missing-log finding. It is an insufficient-query/adoption finding.

The specialized sweep looked principally for environment-wired roots and opened a crypto inventory. It missed existing committed code implementing installer-pinned roots, verifier-supplied time, runtime-minted trust, hostile-input snapshots, and frozen copies. That omission matters because the fold repeated a known mistake: it retained a caller-reachable object reference and tried to turn Python setter overrides into a security boundary.

### F7 — Verification “totality” is syntactic, not semantic — READ-ONLY — UNSEARCHED — SETTLED-BY-PINNED-BYTES

`mbcx01_build_verify_bundle.py:280-319@aa3d0b1…` proves that ledger witness names exist, are unique, run, and total correctly. It does not prove that the witness set closes an invariant.

No ledger witness covers:

- `object.__new__` context construction;
- `object.__setattr__` anchor/context mutation;
- poison persistence after refusal;
- overlapping thread scopes;
- caller-driven clock mutation before exactness context resolution;
- cross-door `not_after` disagreement.

Therefore “42 invariants / 95 witnesses / two-way totality” is true only as a ledger-mapping claim.

## Omission attack

- **TAR-PIT:** Trying to enumerate every Python callback or dunder is a trap. The governing boundary must be inert bytes/exact primitive values, or behavior-bearing objects must be explicitly rejected before authority evaluation.
- **Literal ordering defect:** C‑R3‑2 says context resolution precedes caller-object processing. Exactness reads receipt fields at `mbcx01_build_exactness_authority.py:177-196@aa3d0b1…` and resolves at lines 197-202.
- **Integration:** I found no hidden integration-gate omission. Integration ran in the pinned reconstruction, but its scoped global wiring is subject to F3.
- **Ceremony fixture:** The in-memory ceremony keypair is stable only within its process lifetime. That is acceptable for the fixture lane, but it must never be evidence that production identity persists.
- **External applicability:** No law, regulator, or jurisdictional rule controls this internal verifier-context design. External sources are prior-art evidence only; execution against the pinned bytes decides the verdict.

## Sweep log

### Exact internal queries

- Packet query spot-run: `process\.env.*(TRUST|ANCHOR|ROOT_KEY)` over `agentvault-mcp-bridge/src`.
- Three-repo mechanism search: `verifier context|trust anchor|preconfigured root|fixture[_ -]?only|trusted root|root[_ -]?key`.
- Pinned caller search: `authenticate_production_activation`, public verifier doors, and production-context configuration across the code pin.

Changed/confirmed: the zero-hit packet query was reproducible but too narrow; the broader mechanism search found directly relevant bridge prior art. I stopped after opening the exact committed implementation bytes and verifying the same blobs existed at the packet’s shelf base.

### Exact external queries

- `site:go.dev/src/crypto/x509 VerifyOptions CurrentTime Roots Verify`
- `site:theupdateframework.github.io/specification latest trusted root out-of-band expires current time`
- `site:slsa.dev/spec/v1.2/verifying-artifacts roots of trust verifier`
- `site:cwe.mitre.org/data/definitions/321 hard-coded cryptographic key`
- `site:docs.python.org/3/reference/datamodel.html object.__setattr__ __slots__`
- `site:docs.python.org/3/library/dataclasses.html frozenInstanceError object.__setattr__ frozen`
- `site:docs.python.org/3/library/contextvars.html thread contexts context local state`
- `site:docs.python.org/3/library/contextlib.html reentrant reusable thread safe context manager`
- `site:developer.android.com "debug-overrides" certificate authorities trust production`
- `site:learn.microsoft.com test certificate do not use in production trust store`
- `site:docs.aws.amazon.com test certificates production trust store`
- `site:cloud.google.com test keys production cryptographic keys warning`

### Opened at origin

- **SEARCHED:** [Go `crypto/x509/verify.go`](https://go.dev/src/crypto/x509/verify.go), `VerifyOptions` and certificate-validity checks. Confirmed verifier-owned roots/time and documented inclusive endpoint behavior.
- **SEARCHED:** [TUF current specification](https://theupdateframework.github.io/specification/latest/), §§5.1–5.3 and expiry steps. Confirmed fixed workflow time, out-of-band trusted root, continuity, and strict expiry.
- **SEARCHED:** [SLSA v1.2, “Verifying artifacts”](https://slsa.dev/spec/v1.2/verifying-artifacts), Step 1. Confirmed verifier-preconfigured roots of trust.
- **SEARCHED:** [Python 3.11 dataclasses](https://docs.python.org/3.11/library/dataclasses.html#frozen-instances), “Frozen instances.” Confirmed Python-level immutability is emulated, not absolute.
- **SEARCHED:** [Python 3.11 contextvars](https://docs.python.org/3.11/library/contextvars.html), token reset and per-thread contexts; [contextlib](https://docs.python.org/3.11/library/contextlib.html#single-use-reusable-and-reentrant-context-managers), reentrancy versus thread safety. Confirmed the global-scope concurrency risk and available standard-library lifecycle primitive.
- **SEARCHED:** [Android Network Security Configuration](https://developer.android.com/privacy-and-security/security-config), “Configure CAs for debugging” and `debug-overrides`. Confirmed declarative separation where debug anchors are ignored outside debuggable builds.
- **SEARCHED:** [AWS ACM best practices](https://docs.aws.amazon.com/acm/latest/userguide/acm-bestpractices.html), account-level separation. Confirmed vendor practice of separating production certificates from test/development certificates.
- **SEARCHED:** [CWE‑321](https://cwe.mitre.org/data/definitions/321.html), description and consequence. Corroborated the general shipped-key footgun class; it is taxonomy, not the deciding evidence.

I did not rely on unopened Microsoft or Google search results. I stopped because current primary language documentation, two current verification standards, two vendor practices, the internal committed precedent, and direct execution converged on the relevant questions. No regulatory applicability was asserted.

## Fix class

**SECURITY-BOUNDARY + AUTHORITY-CONTEXT + CONCURRENCY/LIFECYCLE + VALIDITY-SEMANTICS + WITNESS-COVERAGE + DESIGN-GATE**

Required class of correction—not a patch:

- Remove caller-reachable mutable Python objects from the production authority boundary.
- Accept strict serialized bytes or exact inert primitive containers, normalize once, and retain only trusted local primitive values.
- Pass verifier authority per call; do not make a mutable process-global context the security boundary.
- If scoped wiring remains, define concurrency semantics and use context-local/token restoration or an equivalent atomic lifecycle.
- Separate fixture trust material structurally from production configurations/builds, not through a mutable boolean.
- Harmonize validity endpoint semantics across measurement, state, and exactness.
- Add permanent red witnesses for forged context construction, slot mutation, failed-poison persistence, exactness clock mutation, overlapping thread scopes, and endpoint equality.

## Residual risks

- If arbitrary code executing in the verifier interpreter is truly in scope, Python object-level isolation cannot establish a hard authority boundary; process isolation or a narrower byte-only threat model is required.
- Binding-only exactness still does not run the carrier suite. Its current explicit result makes that residual honest.
- Environment/file custody and real operator provisioning were not exercised.
- Physical collection, paid/provider behavior, and production activation remain unverified by explicit authorization.
- The build’s clean-room suite is green, but it currently omits the deciding adversarial mechanisms above.

The post-verdict design questions are not separately applicable: this is an executable BUILD/code acceptance artifact. The mechanism-level alternative is captured in the fix class rather than proposed as a patch.
