# MBCX-01 BUILD — trust-root and key-custody ceremony specification

Status: BUILD work-product 5 (handoff). Normative for any FUTURE production activation of
either authority. Nothing in this document activates anything: r13.2/BUILD repositories carry
only `production_ready:false` manifests and fixture-only keys, and the verification code
refuses production admission without the external evidence this ceremony defines. Executing
the ceremony is a separately authorized owner act, after BUILD review.

## 0. The owner trust anchor (added by the BUILD acceptance r1 fold)

Everything below was already the intent; BUILD acceptance council r1 found that the
implementation stopped one layer short of it, so the manifest and the custody documents
were only ever checked for internal consistency against each other. Verification now
begins where SLSA v1.2 ("Verifying artifacts", step 1) and TUF (§§2.1, 5.3) begin: at a
root of trust the VERIFIER holds and the claimant cannot supply.

- The `OwnerTrustAnchorV1` document carries the OWNER's Ed25519 root **public** key
  (SPKI PEM), the authorities it may activate, and the operator's current minimum
  `activation_generation`. It is loaded by `mbcx01_build_trust_anchor` from operator
  wiring (`configure_owner_trust_anchor(...)`, at process/verifier construction) or from
  the OS-controlled path `MBCX01_BUILD_OWNER_TRUST_ANCHOR`. ⛔ It is never a parameter of
  any admission call, so a bounded API caller cannot supply or substitute one.
- The `OwnerCeremonyActivationV1` statement is the owner's signature over THIS
  activation: the exact SHA-384 canonical digest of the manifest, its validity window,
  the authorized signing-key identity, the trust-root editor key set, the build
  provenance digest, the four custody-evidence digests, and the activation generation.
  It is delivered with the manifest and the four documents, and it is the only thing
  that turns them from "data the caller sent" into authority.
- An anchor that was never configured is a REFUSAL
  (`PRODUCTION_TRUST_ANCHOR_UNAVAILABLE` / `STATE_AUTHORITY_V2_TRUST_ANCHOR_UNAVAILABLE`),
  never a bypass.
- The anchor DOCUMENT is parsed strictly at the operator boundary: a duplicate member is
  `OWNER_TRUST_ANCHOR_AMBIGUOUS`, not a last-member-wins resolution. An operator whose
  configuration has two readings must be told so, because one of the two readings is
  `fixture_only` (BUILD acceptance r2, codex F6).
- WHY THE OWNER SIGNATURE IS DETACHED rather than a field of evidence document 4: the
  manifest binds `signing_ceremony_receipt_digest` = SHA-384 of that document, so a
  document that also contained the manifest digest would be a preimage cycle with no
  solution. The detached statement binds both directions from outside.
- The instance committed to this repository (`MBCX-01-BUILD-OWNER-TRUST-ANCHOR.fixture.json`)
  is FIXTURE-ONLY (`fixture_only: true`) and carries no private key. The PRODUCTION anchor
  is generated in §3 and delivered by operator configuration, never committed.

## 0a. The verifier context (BUILD acceptance r2 fold — FIXTURE ISOLATION)

§0 said the committed fixture anchor "activates nothing". BUILD acceptance council r2
found that this was PROSE, not code: `fixture_only` was parsed and never consulted, so
the committed fixture anchor — whose private half is committed in
`mbcx01_build_ceremony_fixture.py`, and is therefore public to anyone holding this
repository — authorized production admission at all three doors (codex F1, EXECUTED).
Two siblings came with it: the anchor was a mutable process global re-read DURING an
evaluation (F2), and the integration fixture installed it process-wide and never
restored what the operator had (F3). What follows is now enforced, not described:

- **Production verification accepts exactly one thing** — a guarded, INSTANCE-SCOPED
  `ProductionVerifierContext` whose anchor is operator-supplied and NOT fixture-marked,
  carrying its own current time — **and refuses everything else.** The shape is adopted,
  not invented: Go `crypto/x509`'s `VerifyOptions` carries both the roots and
  `CurrentTime` per verification, and TUF's trusted root arrives out of band
  (`MBCX-01-BUILD-R2-TRUSTCONTEXT-SWEEP-LOG.md`).
- A `fixture_only` anchor **cannot be built into a production context through any public
  constructor or wiring call**. Wiring one is still legal — a fixture lane must be able to
  name the root it reads — and it grants nothing: every production door answers
  `PRODUCTION_TRUST_ANCHOR_FIXTURE_ONLY` /
  `STATE_AUTHORITY_V2_TRUST_ANCHOR_FIXTURE_ONLY`. **A ceremony that produced a
  `fixture_only: true` anchor document has produced no production authority**, whatever
  key it holds.
- Each door resolves its context ONCE, before it reads any caller-supplied object, so
  re-wiring the process while the caller's data is being walked cannot change the
  decision IN FLIGHT.
- ⚠ **What an operator must NOT read into the two bullets above (corrected 2026-08-14,
  `MBCX-01-BUILD-ADVERSARY-PREMISE-CORRECTION-2026-08-14.md`).** These are
  SCIENTIFIC-VALIDITY invariants — they stop the experiment counting fixture material,
  or a stale root, as real. They are **not** an access-control boundary. Anything running
  arbitrary Python inside the verifying interpreter reaches past them: `object.__new__` +
  `object.__setattr__` builds a context around a fixture anchor and the public
  `configure_production_verifier_context` accepts it (isinstance-only), `object.__setattr__`
  edits a live context, and re-wiring the process between calls is simply allowed. That
  actor is the **box owner** — MBCX-01 has no API, no production runtime and no external
  submitter — and on-box walls against the box owner are theatre under the permanent T2
  ceiling (`DESIGN-SHELF-MAP.md` §1). The design of record carries **no threat model at
  all** (`grep -niE "threat model|adversary|attacker|untrusted|api-caller|hostile"` over
  `MBCX-01-EXPERIMENT-DESIGN-r9.md`, `MBCX-01-R13-CLOSURE-ARCHITECTURE.md`,
  `MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md` → zero hits). **In-process mutation is a
  NAMED, ACCEPTED residual: tamper-EVIDENT, not tamper-proof, zero grind.** The r2 wiring
  FREEZE built against it (`*_REWIRED_DURING_VERIFICATION`) was **reverted on 2026-08-14**;
  it defended a caller that does not exist and, being a plain module int with no
  `threading` import, could only ever false-fire in a long unattended run. The operator's
  real protection is unchanged and is procedural: **hold the anchor, and read the named
  refusal in the log.**
- The evaluation instant belongs to the verifier: `current_time` on the context when the
  operator supplies one, the REAL clock when it does not — never the manifest's own
  `revocation.published_at` and never the receipt's attested `knowledge_time`. An
  operator running a verifier in a long-lived process therefore gets freshness for free;
  an operator reproducing a historical decision passes the instant explicitly.
- A fixture ASSEMBLER (`mbcx01_build_integration`) wires its context inside
  `installed_production_verifier(...)` and gets the operator's own wiring restored on
  exit. It is packaging-classified as fixture support, not as a production module.

## 1. Roles (all MUST be distinct principals; mechanically checked)

| Role | Holds | Must NOT hold |
|---|---|---|
| `MEASUREMENT_KEY_CUSTODIAN` | the production measurement signing key (BUILD B) | any write/approve authority over either trust-root manifest |
| `STATE_KEY_CUSTODIAN` | the production state-owner signing key (BUILD A writer identity) | trust-root edit/approval authority |
| `STATE_READBACK_READER` | the independent readback identity/key (BUILD A reader) | the writer key; trust-root authority |
| `DESIGN_CONFIGURATION_EDITOR` (trust-root editor) | authority to author/approve trust-root manifests | any production private key |
| `OWNER` | final activation authority; approves the ceremony receipt | — |

The verifiers enforce role distinctness two ways: the manifest's `roles_must_be_distinct`
declaration, and a mechanical check that no signing `key_id` appears anywhere in the
trust-root editor approval chain (`CUSTODY_SEPARATION_INVALID`). Candidate and evaluator
processes never receive any private key; the signer is an injected interface, and the
recommended production custody is an OS-backed non-exportable store (Windows CNG/TPM) or an
external signing service — the receipt formats carry only key IDs and signatures, never key
material, so the custody backend is swappable without a format change.

## 2. Required external evidence (the four digests the manifests bind)

A production `MeasurementTrustRootManifestV3` / `StateTrustRootManifestV1` is admissible only
when its four custody-evidence digests match SHA-384 over the canonical bytes of documents
the verifier is HANDED (injected, not read from the repo):

1. `SEPARATE_KEY_CUSTODY_ATTESTATION` — the custodian's signed statement naming the key id,
   the custody backend, generation date, and that the private key never left that backend.
2. `SEPARATE_TRUST_ROOT_EDITOR_APPROVAL` — the editor's signed approval of the exact manifest
   bytes (by digest), from a principal distinct from every key custodian.
3. `HARNESS_BUILD_PROVENANCE` — the exact harness artifact/build/configuration digests the
   roots authorize (BUILD B), or the exact adapter/store identity (BUILD A), with how they
   were produced.
4. `PRODUCTION_SIGNING_CEREMONY_RECEIPT` — the owner-approved record of the ceremony run
   (§3), including date, principals, and the manifest digest activated.

## 3. Ceremony procedure (future, owner-authorized)

0. OWNER generates the ROOT ANCHOR keypair inside the owner's custody backend, exports
   only the public half into an `OwnerTrustAnchorV1` document **with
   `fixture_only: false`**, and delivers that document to every verifying host through
   operator configuration (§0, §0a). This step happens once, before any authority is
   activated, and is what every later step is checked against. ⛔ An anchor document
   marked `fixture_only: true` — including the one committed here — is refused by every
   production door, so a ceremony that ships one has activated nothing (§0a); and the
   document must parse unambiguously, so a hand-edited file with a duplicated member is
   refused rather than resolved.
   ⛔ **Do not produce this document by copying the committed example and editing the
   labels.** This is the step where that is the tempting shortcut, and the labels are not
   what makes a root of trust — the KEY is. An anchor whose `public_key_pem` is a key
   COMMITTED TO THIS REPOSITORY is refused at context construction by name,
   `PRODUCTION_VERIFIER_CONTEXT_FIXTURE_KEY_MATERIAL:<anchor_id>:<committed document>`,
   whatever `fixture_only` says, whether it is wired in code or delivered through
   `MBCX01_BUILD_OWNER_TRUST_ANCHOR`, and regardless of how the PEM is line-wrapped. The
   known-key set is derived from the committed `*.fixture.json` anchor documents
   themselves (`mbcx01_build_trust_anchor.committed_fixture_key_material`), so it never
   drifts from what this repository actually ships. The reason is not an untrusted caller: the
   private half of that committed key is in `mbcx01_build_ceremony_fixture.py` and is
   held by everyone holding this repository, so an operator who shipped it would believe
   they held the only copy of the root key and nothing would say otherwise (MITRE
   CWE-1291, PeerOf CWE-321, whose mitigation phase is Implementation). The
   correct document is written from the public half exported in this step, and its only
   copy of anything secret stays in the owner's custody backend.
   ▸ SCOPE of that refusal, stated so an operator is not misled: it covers key material
   carried by committed anchor DOCUMENTS. A committed test private key whose public half
   appears in no committed document is not in the derived set (named gap, not a silent
   one), and — like everything in §0a — this is a self-deception guard, not a wall
   against anyone running code on the verifying host.
1. OWNER authorizes a named ceremony in writing (scope: which authority, which subjects,
   which hosts, validity window).
2. Each KEY CUSTODIAN generates their keypair inside the custody backend; exports ONLY the
   public key (SPKI PEM); writes evidence document 1.
3. DESIGN_CONFIGURATION_EDITOR authors the production manifest (roots = the new public keys,
   roles, validity window, empty revocation list, `production_ready:true`), computes its
   digest, writes evidence document 2. The editor never sees a private key; custodians never
   edit the manifest. The same rule as step 0 applies to every key that lands in this
   manifest: it must be a key generated in step 2, never one copied out of a committed
   fixture document — for the OWNER ANCHOR that is now mechanically refused by name
   (step 0), and the frozen `manifest_edit_cannot_activate_production` rule already means
   a repo edit is not authority.
4. Evidence document 3 is produced from the pinned build (exact digests).
5. OWNER reviews all three, runs the BUILD verifier against the manifest + evidence
   (fixture-mode dry run), and signs evidence document 4 — and, with the ROOT ANCHOR
   key, signs the `OwnerCeremonyActivationV1` statement binding the exact manifest
   digest, the four evidence digests, the signing-key identity, the editor key set, the
   provenance digest, the validity window and the activation generation (§0). Rotation
   or re-activation increments the generation, and the operator raises
   `minimum_activation_generation` in the anchor document, which retires every earlier
   activation without touching a custodian.
6. The manifest + four documents + the activation statement are delivered to the operator
   configuration OUTSIDE the repository (injected path/parameter). ⛔ A production manifest is never committed to this
   repository; committing one changes nothing anyway (verifiers take the manifest as an
   injected input and recompute custody digests — a repo edit is not authority, per the
   frozen `manifest_edit_cannot_activate_production` rule carried into both BUILD verifiers).

## 4. Validity and revocation

- Manifests carry a validity window (`valid_from`/`valid_until`, UTC-6-microsecond grammar);
  admission outside the window fails `TRUST_ROOT_VALIDITY_EXPIRED`.
- Revocation: a root listed in `revoked_key_ids` (or a root row with revoked state) fails
  `TRUST_ROOT_REVOKED`. Revocation is an edit by the DESIGN_CONFIGURATION_EDITOR with a fresh
  editor-approval digest; it requires no custodian cooperation (the point).
- Rotation = revoke + new root row + fresh ceremony evidence for the new key.

## 5. Audit

Every ceremony document is retained with the activated manifest digest; the verification
adapters bind `trust_policy_digest` into every signed receipt preimage, so every admitted
receipt names the exact policy generation it was admitted under. Re-running the BUILD
verifier over banked receipts + the manifest of record reproduces the admission decision.
