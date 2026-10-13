# MBCX-01 BUILD acceptance r2 — SEAT3 codex-exec verdict (banked verbatim from the run log)

Source: MBCX-01-BUILD-SEAT3-CODEX-EXEC-r2.log lines 9838-10305 (the FINAL verdict block; the log emits the block twice — a streamed copy at 9368 and this final one).
Model: gpt-5.6-sol, xhigh, service_tier=default. Prompt: MBCX-01-BUILD-SEAT3-CODEX-EXEC-PROMPT-r2.txt. Code pin: 6622bcd933454f8fdf9e029ed60664f56ac4ab45. Run exit 0; log grep shows a real verdict (exit code is not the evidence).

# NO-GO — EXECUTED

The trust-bootstrap fold does not close the adversary class. I executed two independent production-authority bypasses against the pinned bytes:

1. The runtime accepts the repository’s `fixture_only:true` owner anchor as a production anchor, while its matching private test key is committed in the repository.
2. A caller-controlled Python `dict` subclass can reconfigure the process-global owner anchor during verification, admitting a completely reviewer-authored root, activation, manifests, custody documents, and signing keys through all three production doors.

These are security/architecture/interface findings and require council re-entry, not a leaf fix.

## Pin and execution record

**EXECUTED — UNSEARCHED (SETTLED-BY-PINNED-BYTES).**

- Branch: `codex/mbcx01-production-build`.
- Packet: `MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r2.md@12b1c99232a69e4a645d7a49fede90ff0eafb72b`.
- Code: `6622bcd933454f8fdf9e029ed60664f56ac4ab45`, confirmed as an ancestor.
- Manifest blob: `7a2b2bad87576d449dd4c7f40582dadaf8761c8a`.
- The working-tree packet and verification script matched their pinned blobs before use.
- `MBCX01_BUILD_ALLOW_PHYSICAL` remained unset.
- No experiment, provider/model call, physical Job/ETW collection, signing ceremony, or spend was performed.

The pinned clean-room command completed with exit 0 in approximately 124 seconds:

- AJV strict compilation: pass.
- Frozen suite: 145/145 pass.
- BUILD suite: 86/86 pass.
- Repair ledger: 37 invariants / 86 witnesses pass.
- Schema mutant suite: 12/12 pass.
- Canonical parity: pass.
- Production activation and execution-posture checks: pass.
- 695 deterministic Node/Python child invocations.
- Paid/provider/scientific calls: zero.
- Reported readiness: `BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`.

The isolated temporary reconstruction was deleted after review. Final `git diff --quiet` returned 0. I did not alter the four untracked driver-owned files; `MBCX-01-BUILD-CARD-FULL-r2.txt` appeared during the review and was also left untouched.

## Why this exists

### 1. Already built? — EXECUTED — SEARCHED

Yes, the trust-bootstrap mechanism has strong prior art that should be adopted structurally rather than reimplemented around a mutable module global:

- SLSA v1.2 begins verification with verifier-preconfigured roots and then verifies the artifact/provenance against those roots.
- TUF 1.0.36 starts from an out-of-band trusted root, establishes version-to-version continuity, persists the resulting root, and checks rollback and freeze conditions against a fixed update-start time.
- Sigstore’s policy controller represents a trust root as an explicit configured resource and supports initial TUF roots, serialized repositories, and out-of-band keys.
- The internal bridge shelf already has a closer implementation pattern: production configuration is constructed once, security fields are read once, arrays are cloned and deep-frozen, and the resulting trust bundle is injected into consumers.

The packet carries a non-vacuous general shelf log at `MBCX-01-BUILD-SHELF-LOG.md:7-38@6622bcd...`: exact queries, repositories, opened files, and adopt/why-not dispositions are present. I spot-ran its Photon query and obtained the same six Aruna files.

However, the r2 trust-fold delta at `MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r2.md:229-235@12b1c99...` is incomplete: it provides one query and a conclusion, but no trust-specific files-opened/adopt-or-why-not record. Its conclusion that the bridge contained only compile-time pins/CRL support is contradicted by current committed bridge bytes:

- `src/broker-proxy.ts:221-223,273-350@ba702fd6...`
- `src/web-data-capture-compose.ts:63-71,160-176@ba702fd6...`

Those bytes contain an explicit pinned upstream trust-anchor bundle and snapshot-root injection. The actual bridge bytes govern what the shelf contains, so they defeat the packet’s characterization.

### 2. Product fit? — READ-ONLY — UNSEARCHED (SETTLED-BY-PINNED-BYTES)

Customer need, in one sentence:

> Let an operator admit state, measurement, and exactness evidence only under an operator-chosen trust root, while returning loud, inspectable refusals whenever that authority cannot be authenticated.

That is governed power / fail-loud / mirror-not-cop. The intended capability fits the product. The shipped implementation does not: fixture authority, object-triggered global reconfiguration, and persistent integration-fixture poisoning remove the operator’s effective knob.

### 3. Bigger than the bug? — READ-ONLY — UNSEARCHED (SETTLED-BY-PINNED-BYTES)

Yes. The r1 finding produced a new trust-anchor document, activation schema, global configuration lifecycle, custody-binding protocol, and authentication path spanning three authorities. That is a security subsystem and interface change, not a leaf repair. The packet does not evidence a separate owner-approved DESIGN gate for that subsystem. This acceptance re-round exercises it, but the architecture findings below require another explicit design/council pass.

## Claim disposition

| Claim | Disposition | Executed result |
|---|---|---|
| C-R2-1: self-authored universe cannot clear a production door | **FAIL — EXECUTED** | A fully reviewer-authored universe cleared all three doors through the mapping-object global-anchor substitution. A second universe cleared all three using the repository fixture owner key. |
| C-R2-2: bounded caller cannot replace the preconfigured anchor | **FAIL — EXECUTED** | `AnchorInjectingDict` changed the global anchor from inside `.get`/`__getitem__` calls made by each verifier. |
| C-R2-3: activation is exact-byte bound and rollback-proof | **PARTIAL — EXECUTED** | Byte, key, provenance, validity, and generation substitutions were rejected. Default wall-clock freshness is not enforced; an expired manifest admitted through the measurement production door. |
| C-R2-4: fixture/production shape distinction preserves fixture non-authority | **PARTIAL — EXECUTED** | The state shape split itself works. The larger “fixture evidence never grants production authority” invariant fails because the fixture owner anchor is accepted at runtime. |
| C-R2-5: strict carrier canonicality | **PASS — EXECUTED** | Whitespace, base64url alphabet, and nonzero unused pad-bit variants were rejected at every tested carrier door. |

## Findings

### F1 — Critical: fixture owner root grants production authority

**EXECUTED — SEARCHED.**

The parser records `fixture_only`, but `authenticate_production_activation` never rejects it:

- `mbcx01_build_trust_anchor.py:134-163,298-345@6622bcd...`
- `MBCX-01-BUILD-OWNER-TRUST-ANCHOR.fixture.json:3-12@6622bcd...`
- `mbcx01_build_ceremony_fixture.py:35-42@6622bcd...`

The bundle verifier merely checks that the committed anchor is marked fixture-only and contains no private key:

- `verify-build-bundle.py:373-394@6622bcd...`

The matching private test key is nevertheless committed as Python fixture material. I configured the committed fixture anchor, generated fresh measurement/state signing keys, fresh production manifests, four fresh custody documents per authority, fresh activations, a 100-cell measurement grid, and a newly committed in-memory state transaction.

Result:

```text
configured_fixture_only=True
measurement=[]
state_verify=[]
state_scorer=[]
exactness=ADMITTED
exactness.schema_id=CarrierExactnessReceiptV3
exactness.result=PASS
exactness.authority_mode=PRODUCTION_MEASUREMENT_AUTHORITY
```

`MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md:36-40@6622bcd...` asserts that the fixture anchor “activates nothing.” The executed runtime behavior governs what the code does and wins over that prose.

The external footgun class is consistent with [MITRE CWE-321](https://cwe.mitre.org/data/definitions/321.html), which classifies a hard-coded cryptographic key used for protection as capable of producing authentication/protection bypass. The decisive evidence here is narrower and executable: a known test key becomes dangerous because the production verifier omits the fixture policy check.

**Fix class:** security architecture / fixture isolation. A fixture-only anchor must be structurally unrepresentable or unconditionally rejected in production verification—not merely labelled and checked by a build-time bundle test.

### F2 — Critical: injected object graph substitutes the global trust anchor

**EXECUTED — UNSEARCHED (SETTLED-BY-PINNED-BYTES).**

All production APIs accept `Any`, use `isinstance(value, dict)`, and then repeatedly invoke virtual mapping methods. They do not first serialize, deep-snapshot, or require exact built-in inert data:

- `mbcx01_build_measurement_authority.py:202-305,753-791@6622bcd...`
- `mbcx01_build_state_authority.py:350-467,728-805@6622bcd...`
- `mbcx01_build_exactness_authority.py:130-194@6622bcd...`

The anchor itself is a mutable module global with a public configurator:

- `mbcx01_build_trust_anchor.py:174-240@6622bcd...`

I created an `AnchorInjectingDict(dict)` whose `.get` and `__getitem__` install my reviewer-authored anchor. Before each call, I restored the legitimate repository fixture anchor. I then passed only the armed manifest parameter plus my own owner key, activation, custody documents, authority keys, receipts, and envelopes.

Result:

```text
OBJECT_GRAPH_MEASUREMENT
  before=fixture anchor
  after=reviewer attacker anchor
  errors=[]

OBJECT_GRAPH_STATE
  before=fixture anchor
  after=reviewer attacker anchor
  verify=[]
  scorer=[]

OBJECT_GRAPH_EXACTNESS
  before=fixture anchor
  after=reviewer attacker anchor
  result=PASS
```

This is the requested fully self-authored trust universe: the owner root and private key, manifest signers, manifests, custody documents, activation statements, state transaction, measurement grid, and exactness inputs were reviewer-generated.

Applicability is bounded: if every consumer guarantees a fresh JSON deserialization into exact built-in containers before calling these APIs, this particular gadget is unavailable. No such boundary is present in the pinned API contract, and the packet explicitly puts injected Python object graphs in scope.

**Fix class:** security architecture / interface. Use instance-scoped immutable verifier context. Admit inert bytes or a verified immutable model at the trust boundary; never perform authority decisions over arbitrary behavior-bearing mapping objects. Remove public request-adjacent mutation of process-global authority.

### F3 — High: integration fixture persistently poisons process authority

**EXECUTED — UNSEARCHED (SETTLED-BY-PINNED-BYTES).**

`mbcx01_build_integration.py` is listed as a BUILD module, imports test/fixture machinery directly, calls `configure_fixture_owner_anchor`, and does not restore the previous anchor when the fixture is released:

- `verify-build-bundle.py:64-75@6622bcd...`
- `mbcx01_build_integration.py:52-76,137-142,223-227@6622bcd...`

Executed sequence:

```text
before: reviewer nonfixture operator anchor
build_connected_authority_fixture:
  measurement=[]
  state=[]
  exactness=PASS
after build: committed fixture-only anchor
after release_connected_authority_fixture: committed fixture-only anchor
```

Combined with F1, any long-lived process that invokes this integration helper is left using a publicly signable production root.

**Fix class:** packaging / lifecycle / architecture. Remove fixture assemblers and test imports from the production module graph; bind roots per verifier instance. A restore-on-release guard would reduce one leaf symptom but would not cure global mutability or concurrency.

### F4 — High: default production evaluation admits expired policy

**EXECUTED — SEARCHED.**

Activation binding itself rejected every fresh substitution I tested:

- exact manifest ID with altered canonical bytes;
- alternate manifest signing key;
- changed provenance digest;
- changed validity window;
- activation generation below the configured floor.

Each returned `ACTIVATION_UNAUTHENTICATED`.

But the measurement manifest validator defaults its evaluation instant to the manifest’s own `revocation.published_at`:

- `mbcx01_build_measurement_authority.py:202-217,265-270,753-755@6622bcd...`

I created a manifest valid only from 2000 through 2001, set `revocation.published_at` in 2000, and authenticated it correctly. On 2026-08-14:

```text
default production door=[]
explicit evaluated_at=2026-08-14T00:00:00Z
  -> TRUST_ROOT_VALIDITY_EXPIRED
```

The packet’s specific residual at `MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r2.md:198-201@12b1c99...` acknowledges this deterministic historical instant. That specific caveat and the runtime bytes govern over the broader “rollback-proof” wording.

[TUF 1.0.36 §5.2–5.3](https://theupdateframework.github.io/specification/latest/) confirms the relevant established pattern: start from an out-of-band trusted root, require version continuity, persist it, and test expiration against a fixed update-start time. It does not make TUF directly applicable to MBCX receipts, but it disproves treating a claimant-selected historical instant as sufficient freshness.

**Fix class:** trusted-time / activation-state architecture. Bind evaluation to a verifier-controlled run instant and durably maintained minimum generation or equivalent monotonic state.

### F5 — Strict signature carrier successfully closes the tested alternate encodings

**EXECUTED — SEARCHED.**

I tested valid carriers and three decoded-byte-equivalent mutations:

- inserted ASCII whitespace;
- standard/base64url alphabet substitution;
- nonzero unused padding bits.

Measurement returned `MEASUREMENT_SIGNATURE_CARRIER_INVALID` plus its refusal sentinel; state returned `STATE_AUTHORITY_V2_SIGNATURE_CARRIER_INVALID` plus its sentinel; exactness threw the same carrier-invalid refusal. Activation carriers were likewise rejected.

The standalone Node verifier returned:

```text
[true,false,false,false]
```

Relevant bytes:

- `mbcx01_build_trust_anchor.py:116-120,243-262@6622bcd...`
- `mbcx01_build_state_authority.py:786-801@6622bcd...`
- `mbcx01_build_exactness_authority.py:112-123@6622bcd...`
- `verify-build-receipt-signature.mjs:21-53@6622bcd...`

This strict layer is necessary because [Node’s Buffer documentation](https://nodejs.org/api/buffer.html) states that its base64 decoder also accepts the URL-safe alphabet and ignores whitespace. [RFC 4648 §§3.1–3.5](https://www.rfc-editor.org/rfc/rfc4648.html) supplies the canonical no-line-feed, alphabet, padding, and pad-bit rules. RFC 4648 is Standards Track. [RFC 8032 §5.1.7 and §8.4](https://www.rfc-editor.org/rfc/rfc8032.html) was also checked for Ed25519 verification/malleability context; it is Informational, so I did not treat it as a controlling application standard.

No fresh carrier bypass was found.

### F6 — Loader ambiguity remains at the operator configuration boundary

**EXECUTED — SEARCHED.**

Missing anchor path, missing environment configuration, and malformed JSON failed closed by exception. A JSON file containing a duplicate member was accepted with last-member-wins semantics:

```text
duplicate_member ACCEPTED fixture_only=True
```

The loader uses ordinary `json.load`:

- `mbcx01_build_trust_anchor.py:196-203@6622bcd...`

This did not provide a bounded-caller bypass because the path is owner/operator controlled under the packet’s T2 boundary. It remains a configuration-audit ambiguity. [RFC 8785 §3.1](https://www.rfc-editor.org/rfc/rfc8785.html) requires canonicalization inputs not to contain duplicate property names; RFC 8785 is Informational and applies only if MBCX chooses that JCS/I-JSON contract.

**Fix class:** parser/configuration hardening.

### F7 — Exactness can mint a `PASS` binding without executing the suite

**EXECUTED — UNSEARCHED (SETTLED-BY-PINNED-BYTES).**

`verify_production_carrier_exactness` accepts a minimal suite claim, defaults missing result and authority mode to `PASS` and production measurement authority, and returns a `CarrierExactnessReceiptV3`:

- `mbcx01_build_exactness_authority.py:24-30,142-194@6622bcd...`

The module and packet openly state that the suite is not run, so this does not refute a claimed runner. It is nevertheless a semantic footgun: downstream consumers can mistake the returned `result:"PASS"` for proof that the suite executed.

**Fix class:** interface/semantics. A binding-only receipt should not mint an unqualified `PASS`; execution evidence should be distinct and authenticated.

## Red-bank replay

**EXECUTED — UNSEARCHED (SETTLED-BY-PINNED-BYTES).**

I reran the committed TRUSTBOOT red probe against archived pre-fix `4e58f9b...` and post-fix `6622bcd...` bytes.

Pre-fix:

```text
measurement self-authored -> []
state verify -> []
state scorer -> []
production manifest/no activation ->
  [STATE_AUTHORITY_UNAVAILABLE, ROOT_NOT_TRUSTED]
canonical carrier -> []
whitespace carrier -> []
```

Post-fix:

```text
measurement self-authored ->
  [MEASUREMENT_CUSTODY_EVIDENCE_INVALID, refusal sentinel]

state self-authored ->
  [sentinel, custody-separation-invalid, root-not-trusted]
state scorer retained the frozen errors

production manifest/no activation ->
  [sentinel, custody-separation-invalid,
   root-self-authored, anchor-unavailable]

whitespace mutation added carrier-invalid
```

Thus the bank faithfully demonstrates the intended fold against ordinary built-in data. It did not cover the fixture-root policy omission or behavior-bearing mapping objects.

## Omission attack record

- **EXECUTED:** missing anchor, absent environment path, malformed JSON — fail closed by exception.
- **EXECUTED:** duplicate JSON member — accepted, last value wins.
- **EXECUTED:** mutable/global anchor configuration — production bypass achieved.
- **EXECUTED:** integration fixture followed by release — global fixture anchor persists.
- **EXECUTED:** legitimate anchor plus ordinary attacker-supplied plain data — all three doors refused.
- **EXECUTED:** fully reviewer-authored root introduced through a behavior-bearing mapping — all three doors admitted.
- **EXECUTED:** activation manifest-byte, key, provenance, validity, and generation splices — rejected.
- **EXECUTED:** whitespace, alternate alphabet, and pad-bit carrier mutations — rejected.
- **EXECUTED:** expired policy under default evaluation instant — admitted by measurement; rejected when given current time.
- **READ-ONLY:** anchor `anchor_id` and manifest roster `key_id` are separate fields, but identical strings are not prohibited. Cryptography still selects different public-key fields, so I found no key-substitution result; audit/log identity ambiguity remains.
- **READ-ONLY:** state verification resolves store material before returning some authority refusals. The packet already names this as a residual; I found no admission bypass from it.

## Sweep log

### Prior art / trust bootstrap — SEARCHED

Exact queries:

```text
site:slsa.dev/spec/v1.2/verifying-artifacts roots of trust verifier
site:theupdateframework.github.io/specification trusted root keys root rotation
site:docs.sigstore.dev trust root TUF trusted_root.json
site:docs.sigstore.dev "TrustedRoot" trust root distribution TUF
site:docs.sigstore.dev "root.json" "trust" Sigstore TUF
```

Opened:

- [SLSA v1.2, “Verifying artifacts,” Step 1](https://slsa.dev/spec/v1.2/verifying-artifacts): confirmed verifier-preconfigured roots and artifact/provenance binding.
- [TUF specification 1.0.36, §§2.1, 5.2, 5.3, 6.1](https://theupdateframework.github.io/specification/latest/): confirmed out-of-band bootstrap, immutable continuity rules, persisted generations, rollback and freeze checks. I checked the current index/version rather than relying on the initially found 1.0.26 page.
- [Sigstore policy-controller, “Configuring TrustRoot”](https://docs.sigstore.dev/policy-controller/overview/): confirmed explicit custom TUF root/repository and bring-your-own out-of-band keys.
- [Sigstore installation, TUF initialization](https://docs.sigstore.dev/cosign/system_config/installation/): confirmed starting from a particular root and chaining to the latest unexpired root.

Changed/confirmed: the fold’s goal is conventional, but its mutable-global implementation is not the established verifier-context pattern. Stopped because current SLSA, current TUF, Sigstore practice, and the internal shelf converged on the same narrow question.

### Carrier / parser standards — SEARCHED

Exact queries:

```text
site:nodejs.org/api/buffer.html base64 whitespace base64url alphabet
site:rfc-editor.org/rfc/rfc4648 canonical base64 pad bits reject non alphabet
site:rfc-editor.org/rfc/rfc8032 Ed25519 verify S canonical encoding
site:rfc-editor.org/rfc/rfc8785 JSON canonicalization duplicate property names I-JSON
site:rfc-editor.org/rfc/rfc8259 object names unique unpredictable duplicate
```

Opened:

- [Node Buffer documentation](https://nodejs.org/api/buffer.html), base64/base64url behavior.
- [RFC 4648 §§3.1–3.5](https://www.rfc-editor.org/rfc/rfc4648.html), canonical Base-N encoding.
- [RFC 8032 §5.1.7 and §8.4](https://www.rfc-editor.org/rfc/rfc8032.html), Ed25519 verification and malleability context.
- [RFC 8785 §3.1](https://www.rfc-editor.org/rfc/rfc8785.html), duplicate-property exclusion for canonicalization input.

RFC 8259 origin retrieval was rate-limited, so I did not admit its search excerpt as evidence. Stopped because RFC 4648 plus Node’s current primary documentation settle the executable carrier question; RFC 8785 is sufficient only as a non-controlling parser comparison.

### Footgun literature — SEARCHED

Exact queries:

```text
site:cwe.mitre.org CWE hard-coded cryptographic key production test key
site:cisa.gov hardcoded credentials product security bad practices cryptographic keys
site:owasp.org test keys production hardcoded cryptographic key
```

Opened:

- [MITRE CWE-321, “Use of Hard-coded Cryptographic Key”](https://cwe.mitre.org/data/definitions/321.html), description, consequences, examples, and current version history.

CISA’s primary guidance and alert returned HTTP 403 when opened; their search snippets were not admitted as evidence. OWASP results were mobile-specific and not needed after the executable bypass plus CWE taxonomy. Stopped because external literature only corroborates this finding; pinned bytes and execution already decide it.

### Internal shelf — EXECUTED / SEARCHED

Exact spot queries:

```text
rg -n -i "trust anchor|pinned owner|SPKI|preconfigured root" src
```

Run in `<home>\source\agentvault-mcp-bridge`; opened the matching committed `broker-proxy.ts` and `web-data-capture-compose.ts` sections described above.

```text
rg -l -i "single.?writer|writer_gate|readback|append.?first|evidence.?before.?effect" crates
```

Run in `<home>\source\Photon`; reproduced:

```text
crates\aruna\src\lib.rs
crates\aruna\src\message_store.rs
crates\aruna\src\message_header.rs
crates\aruna\src\read_coordinator.rs
crates\aruna\src\writer_gate.rs
crates\aruna\src\store_open.rs
```

Stopped after reproducing a logged shelf query and disproving the r2 trust-delta characterization with opened code bytes.

## Load-bearing evidence read

- `MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r2.md:1-248@12b1c99232a69e4a645d7a49fede90ff0eafb72b`
- `<vault>`
- `mbcx01_build_trust_anchor.py:86-345@6622bcd933454f8fdf9e029ed60664f56ac4ab45`
- `mbcx01_build_ceremony_fixture.py:32-100@6622bcd...`
- `MBCX-01-BUILD-OWNER-TRUST-ANCHOR.fixture.json:1-12@6622bcd...`
- `MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md:1-119@6622bcd...`
- `mbcx01_build_measurement_authority.py:202-432,753-791@6622bcd...`
- `mbcx01_build_state_authority.py:350-493,728-922@6622bcd...`
- `mbcx01_build_state_adapter.py:115-275@6622bcd...`
- `mbcx01_build_state_operator_b.py:51-76,102-224@6622bcd...`
- `mbcx01_build_exactness_authority.py:24-30,112-194@6622bcd...`
- `mbcx01_build_integration.py:52-76,112-142,172-194,223-227@6622bcd...`
- `verify-build-receipt-signature.mjs:21-53@6622bcd...`
- `verify-build-bundle.py:64-86,373-394@6622bcd...`
- `mbcx01_build_trustboot_probe.py:1-end@6622bcd...`
- `MBCX-01-BUILD-TRUSTBOOT-RED-WITNESS-RUN-2026-08-14.txt:1-end@6622bcd...`
- `MBCX-01-BUILD-TRUSTBOOT-GREEN-WITNESS-RUN-2026-08-14.txt:1-end@6622bcd...`
- `test_mbcx01_build_measurement.py:95-106@6622bcd...`
- `test_mbcx01_build_state.py:86-98@6622bcd...`
- `MBCX-01-BUILD-SHELF-LOG.md:7-38@6622bcd...`

`MBCX-01-BUILD-SEAT3-CODEX-VERDICT-r1.md` was opened only as **READ-ONLY — LONGITUDINAL, OWN-SEAT, NON-DECIDING** context. No r1 assertion substitutes for the probes above.

## Residual risks

- **EXECUTED:** fixture-root production admission remains open.
- **EXECUTED:** behavior-bearing object graphs can mutate authority during validation.
- **EXECUTED:** integration helpers leave persistent global authority state.
- **EXECUTED:** measurement freshness defaults to a claimant-controlled historical instant.
- **EXECUTED:** duplicate-member anchor configuration is parser-ambiguous.
- **EXECUTED:** exactness returns `PASS` without executing the named suite.
- **READ-ONLY:** concurrent verifier calls can race process-global anchor changes; I proved sequential poisoning but did not need to add nondeterministic concurrency to establish the class.
- **READ-ONLY:** the owner anchor lacks an authenticated rotation/continuity implementation comparable to TUF; operator replacement remains the governing act under the T2 boundary.
- **READ-ONLY:** state authority binds custody-document digests rather than retaining the documents in the receipt; the packet names this residual.
- **READ-ONLY:** SQLite power-loss durability was not physically exercised.
- **READ-ONLY:** real Job/ETW collection and the scientific experiment were intentionally not run.
- **READ-ONLY:** no production signing ceremony or non-exportable custody backend was exercised.
- **READ-ONLY:** a box-owning admin/SYSTEM actor remains outside scope as owner-locked T2 doctrine requires.

## Required fix class

**SECURITY / ARCHITECTURE / INTERFACE / PACKAGING-LIFECYCLE**

Required properties, not a patch:

- immutable, instance-scoped verifier trust context;
- production verifiers structurally unable to consume fixture anchors;
- no public process-global authority mutation;
- inert byte/model boundary before authority evaluation;
- fixture/test integration absent from the production import graph;
- verifier-controlled current-time and monotonic activation state;
- unambiguous strict configuration parsing;
- binding-only exactness results separated from proof that a suite actually ran.

Because these fixes change authority lifecycle and public interfaces, the packet’s own re-review trigger requires council reconvening.
