# MBCX-01 production BUILD — design notes (working artifact, BUILD lane)

Status: driver working notes for the two BUILD artifacts; governed by the r13.2 handoff +
closure architecture + invariant matrix. Frozen r13.2 subjects are never edited; every new
module/schema/manifest below is a versioned sibling.

## 0. Ground truths from the seam maps (byte-verified 2026-08-14)

- `mbcx01_r13_measurement.py:1140` adds `PHYSICAL_HARNESS_UNAVAILABLE` **unconditionally** —
  no input clears the frozen evaluator. Production admission therefore lives in a NEW
  versioned adapter module (the handoff's "explicitly versioned compatible adapter" arm).
- `mbcx01_r13_measurement.py:109-117` — a trust-root manifest with `production_ready:true`
  RAISES; every root must be `fixture_only:true` with `NO_PAID_TEST_FIXTURE` /
  `NO_PAID_TEST_HARNESS` labels (`:143-145`), and envelopes are matched against the root's
  labels (`:721-722`). A `PHYSICAL_HARNESS_RECEIPT` envelope is structurally expressible
  (contract v7 enum) but unadmittable by the frozen path — exactly the fail-loud boundary.
- All r13 schemas are CLOSED key sets — any field addition is a re-version, never an edit.
- The frozen file's pure helpers are import-reusable for byte-identical preimages:
  `canonical_json`, `sha384`, `_receipt_preimage`, `refresh_receipt_hash`, `_query_evidence`
  (96/144-byte ABI packer), `_physical_evidence`, `measurement_grid_identity_hash`, `_cell_id`.
- Soft spot inherited from r13 (tighten, never loosen): `elapsed_monotonic_ns` is only
  checked > 0 (`:1099`) — the production adapter cross-checks it against the signed QPC
  lifetimes' span converted at a signed QPC frequency (new evidence field in the V2 envelope).

## 1. BUILD B — production Windows Job/ETW evidence producer + admission adapter

New files (all additive):

| File | Role |
|---|---|
| `mbcx01_build_windows_producer.py` | Producer core: evidence assembly, canonical preimage, custody-injected signing seam. OS collection sits behind a `WindowsCollectionInterface` so fixture tests inject simulated collection results; the real collector implementation is reviewable code that this task never executes. |
| `mbcx01_build_win32.py` | The real collector: ctypes bindings for CreateProcess(CREATE_SUSPENDED), Job creation/config, completion port, breakaway disable, assign-before-resume, final queries (raw bytes), process start-key acquisition, ETW PMC session config. NOT executed by any test in this task beyond struct-layout constants. |
| `MBCX-01-BUILD-MEASUREMENT-TRUST-ROOTS-V3.schema.json` + fixture instance | `MeasurementTrustRootManifestV3`: adds custody attestation digests (key-custodian attestation, root-editor approval, harness build provenance, signing-ceremony receipt), producer authorization rows keyed by role `PHYSICAL_MEASUREMENT_PRODUCER`, validity window + revocation list. Committed instances are fixture-only/`production_ready:false`; a production instance can only exist via the ceremony (never committed). |
| `mbcx01_build_measurement_authority.py` | Production admission adapter: re-validates the full evidence tree (importing frozen validators/helpers where pure), then applies V3 root logic — signature, role authorization, custody disjointness, validity/revocation, ceremony receipts, grid identity, exactness authority — and only a fully valid production envelope set clears `PHYSICAL_HARNESS_UNAVAILABLE`. Absence/ambiguity/fixture stays red. |
| `mbcx01_build_exactness_authority.py` | Production carrier-exactness verifier: `CarrierExactnessReceiptV3` bound to pinned suite/witness set + exact carrier artifact + exact harness build + exact grid identity + production root; fixture V2 receipts remain conformance-only. |

Producer envelope: `SignedMeasurementReceiptV2` — same 12-field signed-preimage discipline
(sorted-key canonical JSON, Ed25519, SHA-384 digest), same `MeasurementReceiptV3` evidence
tree REUSED VERBATIM (closed sets already fit a real producer; the four constants a real run
must satisfy — terminated==0, ns%100==0, per-period zeros, membership==TotalProcesses — are
exactly what the contract demands of a clean cell), plus a V2-only extension block for the
QPC-frequency cross-check evidence. Compatibility boundary documented in the BUILD contract.

Custody separation (I13, hardened): the V3 manifest's `trust_policy` binds
`signer_custodian_role != trust_root_editor_role` AND carries the four external-evidence
digests; the admission adapter refuses any manifest where the signing key id appears in the
editor-approval chain (signer-cannot-edit-root, checked mechanically, not just declared).

## 2. BUILD A — production state-owner adapter (finalized 2026-08-14 after the state seam map)

Ground truths (byte-verified by the seam map):

- `StateAuthorityReceiptV1` cannot express production: `mbcx01_r13_common.py:303-305` pins
  `authority_mode="FIXTURE_ONLY_UNAVAILABLE"`; `:366-370` forces all four signature slots to
  `None` (closed key set); `state_reference.py:486-487` / `state_oracle.py:724-725` append
  `STATE_AUTHORITY_UNAVAILABLE` unconditionally under `require_production=True`; frozen test
  `test_mbcx01_r13_state.py:212-213` pins a signature-bearing V1 as invalid. ⇒ the handoff's
  "explicitly versioned successor" arm is the ONLY reachable one: **StateAuthorityReceiptV2**.
- `packets.build_scoring_fixture:602` hard-calls the fixture receipt constructor — no
  injection seam. Production admission therefore lives in a NEW entry point, never an edit.
- Crash windows are UNMODELED in frozen code (handoff requirement 8 is net-new); the
  in-repo precedent to mirror is the CallLedger distinguished-terminal pattern
  (`ACCEPTANCE_AMBIGUOUS` ⇒ no admissible receipt, never a partial one).
- Mandatory reused primitives (never re-derived): `common.canonical_json` / `sha384` /
  `sha256` / `current_cut` / `canonical_event_id` / `structural_error` /
  `state_authority_receipt_shape_errors`; reducers `reference_apply` / `oracle_apply`.

### The non-weakening production admission shape (the load-bearing design decision)

`mbcx01_build_state_authority.verify_production_scorer_input(scorer_input, production_receipt, *, trust_root_manifest, custody_evidence)`:

1. Run the FROZEN `packets.validate_scorer_input(scorer_input, require_production_authority=True)`
   — every frozen check runs, nothing is bypassed. Collect its error set E.
2. Verify the `StateAuthorityReceiptV2` production receipt fully (schema, store identity from
   the injected config, signature against the injected `StateTrustRootManifestV1`, custody
   disjointness, validity/revocation, anti-replay identity, reader≠writer identity,
   dual-reducer replay of ITS bytes via frozen `reference_apply`/`oracle_apply`).
3. BYTE-BIND V2 to the graph the frozen path validated: V2 prestate/proposal/child/readback
   `state_utf8`/`event_utf8` bytes, hashes and cuts must equal the scorer input's
   `transition_authority` + embedded fixture-projection receipt fields exactly.
4. Discharge is subtractive and exact: the result is
   `sorted((E - {"STATE_AUTHORITY_UNAVAILABLE"}) ∪ V2_errors)` — and the sentinel is removed
   ONLY when steps 2 AND 3 are fully clean. Any V2 defect ⇒ sentinel stays AND the V2 error
   is added. A fixture receipt with no V2 alongside is completely unchanged behavior.

This never weakens the frozen path: every frozen check still executes with production
semantics; the ONLY thing the new code may do is discharge the one named sentinel with
strictly stronger evidence bound to the same bytes. (The mapper's uncertainty about
re-implementing `validate_scorer_input` is answered by not re-implementing it at all.)

### New files

| File | Role |
|---|---|
| `mbcx01_build_state_store.py` | SQLite single-writer durable store: one-door verified open (`journal_mode=WAL`, `synchronous=FULL`, schema-version check), events journal + snapshot tables, single-writer gate, one-transaction commit of proposal+child+state (record-before-effect), crash-window law: a transaction is `COMMITTED` or it yields NO receipt — `PENDING`/`BROKEN` journal rows are distinguished terminals that cannot mint. Independent reader connection class with its own attested identity. |
| `mbcx01_build_state_adapter.py` | The production state-owner adapter (operator 1): drives store commit → independent readback → mints `StateAuthorityReceiptV2` via a custody-injected signer. |
| `mbcx01_build_state_operator_b.py` | Operator-independence twin (r13.1 shelf-log BUILD prerequisite): independently derives the receipt content from the same frozen store bytes; shares ONLY schemas/hashing with operator 1; byte-identical receipt comparison gate; a contaminated finalizer must produce detected disagreement. |
| `mbcx01_build_state_authority.py` | `StateAuthorityReceiptV2` schema/verify + `verify_production_scorer_input` per the shape above; `STATE_AUTHORITY_UNAVAILABLE` preserved for every non-production path. |
| `MBCX-01-BUILD-STATE-TRUST-ROOTS-V1.schema.json` + fixture instance | `StateTrustRootManifestV1` mirroring the measurement manifest discipline: production_ready:false fixture; custody roles (signer custodian ≠ trust-root editor ≠ reader identity), validity/revocation, roots with role authorization (`STATE_OWNER_WRITER`, `STATE_READBACK_READER`). |

### StateAuthorityReceiptV2 field plan (handoff lines 151-172, superset of V1)

V1 carry-over (same canonical/hash discipline, `common.py` recomputation rules) plus:
`authority_mode` ∈ {`FIXTURE_CONFORMANCE`, `PRODUCTION`} · closed `domain`/`version` ·
`proposal_persistence.persistence_identity` (journal row identity) · `applied_child.next_sequence` ·
`postcommit_readback.reader_identity` (≠ writer producer_id, role-bound) · signer identity block
(producer_id, role, key id, algorithm, trust_root_id, policy digest, validity/revocation state,
subject identity) · full Ed25519 signature over a 12-field-style canonical preimage
(measurement-envelope discipline) · `anti_replay` {receipt_nonce, scope_id, scenario_id, run_id,
transaction_commit_id} · `receipt_digest`.

## 3. Test/witness staging (both BUILDs)

Red witnesses are written and RUN before each authority path exists; each must fail on the
baseline for its intended reason (e.g. production admission returns
`STATE_AUTHORITY_UNAVAILABLE` / `PHYSICAL_HARNESS_UNAVAILABLE` where the witness demands a
production-admitted result; falsification-oriented witnesses assert the named rejection). New witnesses
land in `MBCX-01-BUILD-REPAIR-LEDGER.json` with two-way coverage, and a deterministic
`verify-build-bundle.py` + pinned reconstruction launcher mirror the r13 discipline.

## 4. Post-green folds (2026-08-14, after the BUILD A/B green banks)

### FOLD 1 — durable anti-replay anchors (witnesses ba26, ba27)

The green-stage verifier derived `receipt_nonce` / `scenario_id` / `run_id` from the
receipt's own labels (`TXN.x -> NONCE.x`, `SCOPE.x -> SCENARIO.x`, `SUBJECT.x -> RUN.x`).
That was flagged at green as a hack, and it was a hack twice over: a value the holder of a
receipt can recompute from a label it already controls anchors nothing, and the transform
cannot express a production run whose scenario, run and nonce are independent identifiers.

The anchor set `{receipt_nonce, scope_id, scenario_id, run_id, subject_identity}`
(`mbcx01_build_state_store.ANTI_REPLAY_KEYS`) is now a DURABLE FACT:

- `SingleWriterStateStore.commit_transition(request, *, anti_replay=...)` — REQUIRED, no
  default — writes the canonical anchor bytes plus their SHA-384 into the journal INTENT
  row, before any effect row exists (record-before-effect);
- the terminal classifier covers them: anchors that do not recompute make the transaction
  `BROKEN`, never `COMMITTED`, so a tampered anchor row can never read back as evidence;
- `mbcx01_build_state_adapter` mints the receipt's anchors from that row
  (`durable_anti_replay_block`) and refuses to mint if the injected identity config
  disagrees with the durable fact;
- `mbcx01_build_state_operator_b` re-decodes and re-digests the anchors from the row with
  its own SQL and its own frozen-primitive calls, ignoring `identity_config` entirely on
  those axes (ba27 contaminates the config on every axis and the answer does not move);
- `verify_state_authority_receipt_v2` compares the receipt's five-value anchor set to the
  durable row as canonical BYTES. Retained unweakened on top: the anti-replay transaction
  id equals the receipt's, the claimed scope is carried by both of the receipt's own state
  byte sets, and the subject is the manifest root's authorized subject. No durable anchors
  (unresolvable store, unknown or corrupt row) is a rejection, never a pass.

Store schema version 1 -> 2. An older store file is refused loudly at open.

### FOLD 2 — fresh-process file-backed verification (witness ba28)

Verification previously required the verifying process to be the process that had opened
the store (the live `_STORES_BY_IDENTITY` registry). That made "no store in my registry"
indistinguishable from "this transaction never happened", and made an independent auditor
structurally unable to check anything. `ReadOnlyStateStoreView.open_verified_readonly`
opens a FILE-backed store `mode=ro` + `PRAGMA query_only=ON`, verifies the persisted store
header and `application_id`/`user_version` against the identity the caller asked for, and
never touches the write door or the registries. `verify_state_authority_receipt_v2` and
`verify_production_scorer_input` take an optional `store_path`, resolved
registry-first-then-path (`_resolve_store`). The path is INJECTED by the verifying
operator, exactly like the trust-root manifest — never read from the receipt, because a
receipt that names its own store is resolving itself. `:memory:` stores keep the registry
arm. ba28 proves it in a cold interpreter: `[]` for the honest receipt,
`TRANSACTION_NOT_COMMITTED` for a PENDING terminal, and — with no locator injected —
`TRANSACTION_IDENTITY_MISMATCH`, which is the control proving the cold registry is empty.

### Integration + verifier (witnesses bi01-bi04)

`mbcx01_build_integration.build_connected_authority_fixture()` assembles ONE connected
graph: frozen packet graph -> real file-backed store -> `StateAuthorityReceiptV2` ->
`verify_production_scorer_input() == []` (verified with the store CLOSED, from the durable
path), plus a simulated 100-cell grid -> `evaluate_production_measurement() == []` ->
`verify_production_carrier_exactness` bound to that exact envelope set. bi01/bi02 were
green at birth — both halves already had their own red-then-green witness sets — and that
is declared in the suite docstring rather than dressed up. bi03 (no network/provider/
physical call, enforced under live guards) and bi04 (Python/Node canonicalization parity,
with a mutation control) are discriminating.

`verify-build-bundle.py` runs the five frozen suites (must total 145), the three BUILD
suites, exact two-way ledger totality by unittest introspection, strict AJV compilation +
fixture/mutant validation of the two BUILD schemas, canonicalization parity (with an
out-of-domain refusal control), and a mechanically checked `production_activation:false`.
It emits `MBCX-01-BUILD-VERIFICATION-REPORT.json` at RUNTIME and refuses to run if a copy
of that report is already sitting in the tree.

## FOLD 3 — AUTHENTICATED_PRODUCTION_TRUST_BOOTSTRAP (BUILD acceptance council r1 = NO-GO)

r1 closed NO-GO on one finding, converged on independently by SEAT2 (ChatGPT Sol) and
SEAT3 (codex-exec), both EXECUTED and reproduced by the driver at the byte: **the
production trust root, its custody evidence and the signing key were all caller-supplied
and self-referential.** `evaluate_production_measurement` and
`verify_state_authority_receipt_v2` took `trust_root_manifest` and `custody_evidence` as
per-request parameters, and everything the modules did with them was internal
consistency: hash-match of caller documents against caller digests, distinct role
STRINGS, disjoint key-ID lists, SHA-384 grammar. A fresh untrusted caller Ed25519 key plus an
invented manifest, invented custody documents and 100 self-signed envelopes therefore
cleared production admission with `[]` on both planes. BUILD A had the inverse defect at
the same time: it DEMANDED `production_ready:false` + `NOT_ACTIVATED` + `fixture_only`
roots, so it accepted an untrusted caller's fixture-shaped root and refused the ceremony spec's
own published production manifest (`STATE_AUTHORITY_V2_ROOT_NOT_TRUSTED`).

The model adopted is the established one, not a new machine: SLSA v1.2 "Verifying
artifacts" step 1 and TUF §§2.1/5.3 both begin verification from a verifier-controlled,
PRECONFIGURED root of trust and never accept the claimant's own root as bootstrap.

**The one invariant that closes the class** (`mbcx01_build_trust_anchor`): *no
unauthenticated trust graph reaches production admission.* Production activation of
either authority requires an `OwnerCeremonyActivationV1` statement, signed by an owner
anchor the VERIFIER loads from operator wiring (`configure_owner_trust_anchor`) or OS
configuration (`MBCX01_BUILD_OWNER_TRUST_ANCHOR`), binding the EXACT SHA-384 canonical
digest of the manifest under evaluation plus its validity window, the authorized
signing-key identity, the trust-root editor key set, the build-provenance digest, the
four custody-evidence digests and the activation generation. There is deliberately ONE
failure code for the whole authentication class per authority: an untrusted caller learns "this
did not authenticate", not which of fourteen bindings to grind next (the round's TAR-PIT
ruling — no fake-role permutations).

What did NOT change: every pre-existing check is retained, unweakened, as a structural
check on top of the authentication — the four hash-matches, role distinctness, key-set
disjointness, validity/revocation, the anti-replay anchors, the durable terminal, the
byte binding and the subtractive discharge formula. The per-request signatures of
`evaluate_production_measurement`, `verify_state_authority_receipt_v2` and
`verify_production_scorer_input` are unchanged; there is no anchor parameter to pass,
which is exactly what makes the bounded api-caller unable to supply one (ba31/bw18 assert
that by `inspect.signature`). T2 is untouched: this separates the api-caller from the
OPERATOR, not the operator from the box owner.

Three consequential edges, recorded rather than glossed:

* **BUILD A structural/production split** (`manifest_shape`). Structural parsing now
  accepts BOTH coherent shapes — FIXTURE (`production_ready:false` + `NOT_ACTIVATED` +
  all roots `fixture_only`) and PRODUCTION (`production_ready:true` + `ACTIVATED` + no
  root `fixture_only`) — so the committed fixture stays readable/testable and the
  ceremony manifest is expressible. A MIXED manifest (a fixture relabelled
  `production_ready:true`) is neither shape and is refused, which is what ba07 pins.
* **Injected manifest of record.** `mbcx01_build_state_adapter` and
  `mbcx01_build_state_operator_b` gained an optional `trust_root_manifest`: the ceremony
  spec is explicit (§3.6) that a production manifest is never committed to this
  repository and reaches the verifier as an injected input, so the producer side must be
  able to attest under it. The committed-fixture glob remains the fallback. Injection is
  not authority either way — operator B's content is still compared byte-for-byte with
  operator 1's, and the verifier authenticates the manifest against the anchor itself.
* **Exactness is the third production door.** `verify_production_carrier_exactness` takes
  the same custody evidence and the same authentication (bw21); otherwise a self-authored
  root could still buy an exactness AUTHORITY BINDING.

Leaf, folded alongside (MBCX01-BUILD-R1-SIGNATURE-CARRIER, codex F6): the signature
CARRIER is now canonical — standard alphabet, correct padding, length a multiple of four,
64 decoded bytes, decode/re-encode equality — checked BEFORE any cryptographic
verification, on receipts, on envelopes and on activation statements
(`strict_signature_carrier_ok`). The FROZEN `verify-r13-receipt-signature.mjs` is NOT
edited; the BUILD-side verifier `verify-build-receipt-signature.mjs` is its strict-carrier
sibling with an identical closed request/response contract, and the BUILD state authority
invokes that one. ba33/bw20 are the witnesses.

RED-then-GREEN evidence: `MBCX-01-BUILD-TRUSTBOOT-RED-WITNESS-RUN-2026-08-14.txt` (the
four r1 probes reproduced on HEAD bytes, then the ten new witnesses ba29-ba33/bw17-bw21
failing against those same bytes) and
`MBCX-01-BUILD-TRUSTBOOT-GREEN-WITNESS-RUN-2026-08-14.txt`.

## FIX CLASS — FIXTURE_ISOLATION / INSTANCE-SCOPED VERIFIER CONTEXT (BUILD acceptance r2)

BUILD acceptance council r2 closed GO-WITH-FIXES. The r1 fold above was right about WHERE
authority comes from and wrong about WHAT HOLDS IT. Codex-exec (SEAT3) executed three
defects of the holder (`MBCX-01-BUILD-SEAT3-CODEX-VERDICT-r2.md`), and the driver
reproduced each at the byte before ruling:

* **F1 (deciding).** `fixture_only` was PARSED (`mbcx01_build_trust_anchor.py:154,162,192`
  at `6622bcd9`) and never consulted, and the matching private key is committed
  (`mbcx01_build_ceremony_fixture.py:39`) — so the committed FIXTURE anchor, public to
  anyone with the repository, authorized production admission at all three doors.
* **F2.** The anchor was a mutable process global, re-read during an evaluation, so a
  caller `dict` subclass whose `.get`/`__getitem__` reconfigured it substituted the root
  of trust mid-verification.
* **F3.** `mbcx01_build_integration.py:141` installed the fixture anchor process-wide and
  never restored the operator's own.

**The one invariant that closes all three** — COMPLEMENT-shaped, and ADOPTED rather than
invented (Go `crypto/x509` `VerifyOptions`: roots AND `CurrentTime` are fields of a
per-verification value the verifier constructs, with the real clock as the no-time
fallback; TUF's out-of-band trusted root and monotonic anti-rollback — sweep banked in
`MBCX-01-BUILD-R2-TRUSTCONTEXT-SWEEP-LOG.md`):

> **Production verification accepts exactly one thing — a guarded, INSTANCE-SCOPED
> `ProductionVerifierContext` whose anchor is operator-supplied and NOT fixture-marked,
> carrying its own current time — and refuses everything else.**

⚠ **Scope of that sentence, corrected 2026-08-14**
(`MBCX-01-BUILD-ADVERSARY-PREMISE-CORRECTION-2026-08-14.md`). It is a
SCIENTIFIC-VALIDITY invariant, not an access-control boundary. It stops the experiment
fooling ITSELF — a fixture root silently counting as real (DoR I13 "flip production
flag", I16 "flips production mode", §3 authority modes). It does not, and is not trying
to, stop an actor executing arbitrary Python inside this interpreter: `object.__new__` +
`object.__setattr__` builds a context around the committed fixture anchor and the public
`configure_production_verifier_context` accepts it (isinstance-only), and
`object.__setattr__` edits a live context. That actor is the BOX OWNER — MBCX-01 has no
API, no production runtime and no external submitter, so every caller of these
authorities is the harness and its own tests — and on-box walls against the box owner are
theatre under the permanent T2 ceiling (`DESIGN-SHELF-MAP.md` §1). **In-process mutation
is therefore a NAMED, ACCEPTED residual with zero grind: tamper-EVIDENT, not
tamper-proof.** The design of record carries no threat model at all
(`grep -niE "threat model|adversary|attacker|untrusted|api-caller|hostile"` over
`MBCX-01-EXPERIMENT-DESIGN-r9.md`, `MBCX-01-R13-CLOSURE-ARCHITECTURE.md` and
`MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md` → **zero hits**).

Mechanically, in `mbcx01_build_trust_anchor`:

* `ProductionVerifierContext` refuses ordinary attribute assignment and **cannot be
  constructed around a `fixture_only` anchor through any public constructor or wiring
  call** (F1 closed by construction, then checked again inside
  `authenticate_production_activation` because the whole finding was a flag that was
  parsed and never consulted). Wiring a fixture anchor stays legal and installs NO
  production context, so the doors answer `PRODUCTION_TRUST_ANCHOR_FIXTURE_ONLY` /
  `STATE_AUTHORITY_V2_TRUST_ANCHOR_FIXTURE_ONLY`. The FIXTURE LANE is untouched:
  structural manifest parsing and `require_production=False` verification stay green,
  because refusing fixture AUTHORITY is not refusing fixture DOCUMENTS.
* Every door calls `resolve_production_verifier_context(...)` ONCE, at entry, BEFORE it
  reads any caller-supplied object, and threads that immutable value through the whole
  evaluation — `authenticate_production_activation` now takes `context` as a REQUIRED
  keyword and reads no process state at all (F2 in flight). **The wiring FREEZE that
  rode along with this at r2 was REVERTED on 2026-08-14 and is gone**
  (`_VERIFICATION_DEPTH`, `production_verification_scope`,
  `_refuse_wiring_during_verification`, `AuthorityWiringDuringVerification` and both
  `*_REWIRED_DURING_VERIFICATION` codes, plus witness bw23). Two reasons, both bytes:
  the gadget it defended against is an in-process actor, i.e. the box owner, which the
  T2 ceiling puts out of scope; and it carried a real reliability cost in a long
  unattended run, because `_VERIFICATION_DEPTH` was a plain module int and `threading`
  was never imported, so it could only ever FALSE-fire, never true-fire. **What that
  costs, stated plainly:** such a gadget now succeeds in re-wiring the process for
  SUBSEQUENT calls. It still buys no admission in flight — the executed probe shows the
  measurement and exactness doors answering `PRODUCTION_ACTIVATION_UNAUTHENTICATED` and
  the state door `STATE_AUTHORITY_V2_ACTIVATION_UNAUTHENTICATED` under the operator's
  snapshotted context, with the process left holding the untrusted caller's anchor afterwards
  (`MBCX-01-BUILD-FREEZE-REVERT-WITNESS-RUN-2026-08-14.txt`, P2).
* `installed_production_verifier(...)` is scoped wiring that restores what the operator
  had; `mbcx01_build_integration` uses it and is re-classified in `verify-build-bundle.py`
  as fixture SUPPORT rather than a production module, which is what it always was (F3).

Folded alongside, each with its own witness:

* **Verifier-controlled clock (F4).** `context.current_instant()` is the operator's fixed
  instant or the REAL clock — never the artifact's own value. BUILD B stops defaulting the
  evaluation instant to the manifest's `revocation.published_at`; BUILD A additionally
  judges the trust-root validity WINDOW at the verifier's instant while keeping the
  receipt's attested `knowledge_time` for the deterministic replay checks, because
  "is this root fresh?" and "does this receipt replay identically?" are different
  questions. Witnesses bw24 / ba35.
* **Exactness labelling (F7).** The authority BINDS; it does not run the carrier suite
  (`MBCX-01-BUILD-EXACTNESS-PRODUCTION-VERIFIER-SPEC.md` §3 defers the runner). It now
  emits `result: AUTHORITY_BINDING_ONLY_SUITE_NOT_EXECUTED`, and a receipt CLAIMING
  `PASS` is refused `CARRIER_EXACTNESS_SUITE_NOT_EXECUTED`. Witness bw25.
* **Strict anchor parse (F6).** Duplicate members are `OWNER_TRUST_ANCHOR_AMBIGUOUS`.
  Witness bw26.

**Consequence handled rather than papered over:** after this fold a fixture anchor cannot
grant production, so the pre-existing positive witnesses (ba31, bw18, bi01 …) could no
longer be green under the committed fixture anchor. They now run under a production-SHAPED
TEST anchor whose key pair `mbcx01_build_ceremony_fixture` generates IN MEMORY at first use
(`configure_test_production_anchor()`, instant pinned to `TEST_VERIFIER_INSTANT` for
determinism). No new key material is committed; the committed anchor document stays
`fixture_only: true` and key-free, and `verify-build-bundle.py`'s check on it still passes.
The refusal was not weakened to keep an old green alive — the green was moved to a root
that is entitled to it.

RED-then-GREEN evidence: `MBCX-01-BUILD-FIXTUREISO-RED-WITNESS-RUN-2026-08-14.txt` and
`MBCX-01-BUILD-FIXTUREISO-GREEN-WITNESS-RUN-2026-08-14.txt`
(probe: `mbcx01_build_fixtureiso_probe.py`; witnesses: ba34-ba35, bw22-bw27, bi05).
