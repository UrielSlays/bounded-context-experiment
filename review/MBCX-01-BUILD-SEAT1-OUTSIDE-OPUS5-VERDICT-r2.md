# MBCX-01 BUILD acceptance r2 — SEAT1 (Opus 5 Extra, <council-browser-port>) verdict — banked from thread

Banked by the driver 2026-08-14 from conversation `<id>`
(model label read back as "Opus 5 Extra" BEFORE the card was sent). Packet
`MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r2.md@12b1c992`; code pin `6622bcd9`.
The seat's own streaming trace ("Used Moonwalker integration" markers) is omitted; the
verdict body is verbatim.

---

## 1. Verdict

**GO. — EXECUTED.**

The AUTHENTICATED_PRODUCTION_TRUST_BOOTSTRAP fold closes the r1 P0 class on the real adversary surface. I built my own trust universe with my own Ed25519 keys and drove it at all three production doors; every path refused with a named error, and the legitimate anchored path stayed green at all three. Nothing that held at r1 was weakened. No P0/P1/P2. Two P3 residuals below, neither ripples architecture/interface/security.

Longitudinal disclosure (labelled, my own lane only): at r1 I returned GO-WITH-FIXES and missed this class — my C2/C5 probes flipped the committed manifest and never supplied a self-authored root. That miss is the reason this round exists, and it is the reason I made the self-authored universe the first thing I built rather than the last. I did not inspect any other seat's r1 or r2 output.

## 2. Evidence read (path:line@sha)

Packet blob `1057ab74` @ `12b1c992` — tree copy hashes identically, so my reads are on-pin. Code pin `6622bcd9` is an ancestor of the packet commit. Tree-vs-pin drift across all 17 canonical subjects = 0; I additionally worked from a `git archive` of `6622bcd9` and spot-verified the extraction against the pin.

- `mbcx01_build_trust_anchor.py:196-240` (load/configure/resolve), `:243-250` (carrier), `:293-345` (`authenticate_production_activation`) @ `6622bcd9`
- `mbcx01_build_measurement_authority.py:136-138, 373, 425-429` @ `6622bcd9`
- `mbcx01_build_state_authority.py:180-185, 409, 460-464` @ `6622bcd9`
- `mbcx01_build_ceremony_fixture.py:30-117` @ `6622bcd9`
- `test_mbcx01_build_state.py` ba29/ba31/ba32; `test_mbcx01_build_measurement.py` bw17–bw21 @ `6622bcd9`
- `mbcx01_r13_packets.py:543-544` (frozen sentinel site, unchanged)

Reconstruction: `verify-build-pinned.ps1 -Commit 6622bcd9 -ManifestBlob 7a2b2bad` — frozen_suites PASS, Ran 145 tests. The full pinned run exceeded my connector window twice mid-BUILD-suite; I therefore ran the three BUILD suites directly against the byte-verified `6622bcd9` extraction: Ran 86 tests … OK. So 86/86 BUILD + 145/145 frozen at the pin, EXECUTED — but I flag honestly that I did not see the launcher's own terminal summary block (ledger/schemas/no_production_activation) print to completion in one uninterrupted run.

## 3. Findings — C-R2-1 … C-R2-5

Control first (probe validity): the legitimate operator-anchored ceremony path ADMITS at all three doors — measurement `[]`, state `[]`, exactness `mode=PRODUCTION_MEASUREMENT_AUTHORITY`. Without a green control, every refusal below would be worthless.

**C-R2-1 — self-authored universe cannot clear any door → HOLDS. EXECUTED.**

⚠ My first attempt proved nothing and I discarded it. I re-keyed a manifest and attached my own activation, and got `MEASUREMENT_CUSTODY_EVIDENCE_INVALID` — the universe was malformed and died before the anchor gate, so it tested nothing about C-R2-1. I rebuilt it so the gate is actually exercised: take the fully well-formed legitimate universe, keep every binding byte-identical, and change only who signed the activation.

```
probe fires? signature differs from legit: True | all other signed fields identical: True

D1  measurement, MY signature, every binding correct
      -> ["PHYSICAL_HARNESS_UNAVAILABLE","PRODUCTION_ACTIVATION_UNAUTHENTICATED"]      REJECTED
F2  state,       MY signature, every binding correct
      -> ["STATE_AUTHORITY_UNAVAILABLE","STATE_AUTHORITY_V2_ACTIVATION_UNAUTHENTICATED"] REJECTED
E1  exactness,   MY signature, every binding correct
      -> MeasurementAuthorityError: PRODUCTION_ACTIVATION_UNAUTHENTICATED                REJECTED
E2  exactness,   activation removed entirely  -> PRODUCTION_ACTIVATION_UNAUTHENTICATED   REJECTED
F3  state,       r1's fixture-shaped self-authored universe
      -> ["STATE_AUTHORITY_UNAVAILABLE","STATE_AUTHORITY_V2_CUSTODY_SEPARATION_INVALID"] REJECTED
```

This is the r1 winning attack, isolated to the one variable that matters, on all three doors. It fails.

**C-R2-2 — the anchor is operator-wired, not caller-reachable → HOLDS. EXECUTED.**

Full trace across all BUILD modules: `configure_owner_trust_anchor` has exactly one caller — `mbcx01_build_ceremony_fixture.py:61`, a fixture helper installing the committed fixture path. `resolve_owner_trust_anchor` has exactly one caller — `trust_anchor.py:315`, inside `authenticate_production_activation`. Resolution reads only `_CONFIGURED_ANCHOR` (process wiring) then `MBCX01_BUILD_OWNER_TRUST_ANCHOR` (OS config). Neither is request data.

Parameter sets, enumerated by reflection — no anchor-ish parameter on any door:

```
evaluate_production_measurement    {envelopes, trust_root_manifest, custody_evidence, expected_run_id}
verify_state_authority_receipt_v2  {receipt, trust_root_manifest, custody_evidence, require_production, store_path}
verify_production_scorer_input     {scorer_input, production_receipt, expected_manifest, trust_root_manifest, custody_evidence, store_path}
verify_production_carrier_exactness{receipt, envelopes, suite_document, trust_root_manifest, custody_evidence}
```

Smuggling a well-formed `OwnerTrustAnchorV1` into both the manifest and the custody dict → `MEASUREMENT_TRUST_ROOT_INVALID`. Fails closed, never open: with the anchor unconfigured and otherwise legitimate evidence, measurement returns `PRODUCTION_TRUST_ANCHOR_UNAVAILABLE`, state returns `STATE_AUTHORITY_V2_TRUST_ANCHOR_UNAVAILABLE`, exactness raises `PRODUCTION_TRUST_ANCHOR_UNAVAILABLE`. "Nobody configured a root" never reads as "no root needed."

**C-R2-3 — activation binding is exact and rollback-proof → HOLDS. EXECUTED.**

Six per-axis splices of a genuinely owner-signed activation (re-signed by the real fixture owner key so authentication succeeds and only authorization is wrong):

```
S1 activation_generation rolled back to 0     -> PRODUCTION_ACTIVATION_UNAUTHENTICATED
S2 manifest_digest re-pointed                 -> PRODUCTION_ACTIVATION_UNAUTHENTICATED
S3 authority swapped to STATE                 -> PRODUCTION_ACTIVATION_UNAUTHENTICATED
S4 authorized_signing_key_id changed          -> PRODUCTION_ACTIVATION_UNAUTHENTICATED
S5 provenance_digest changed                  -> PRODUCTION_ACTIVATION_UNAUTHENTICATED
S6 custody_evidence_digests emptied           -> PRODUCTION_ACTIVATION_UNAUTHENTICATED
S7 UNCHANGED genuine activation vs a mutated manifest keeping the SAME manifest_id
   (probe fires? mutated: True | same manifest_id: True)
                                              -> MEASUREMENT_TRUST_ROOT_INVALID
```

S7 is the packet's explicit requirement — digest binding is over canonical bytes, not `manifest_id` — confirmed by execution. `manifest_activation_digest` = sha384 over the entire canonical manifest (`trust_anchor.py:293-295`).

**C-R2-4 — the BUILD A shape split fixes both r1 defects → HOLDS. EXECUTED.**
(a) r1 false-ACCEPT — fixture-shaped self-authored root: F3 refused (`STATE_AUTHORITY_V2_CUSTODY_SEPARATION_INVALID`).
(b) r1 false-REJECT — the ceremony spec's own production-shaped manifest (`production_ready: True`, `trust_policy.status: ACTIVATED`, all three roots `fixture_only: False`) now ADMITS `[]` under the operator-preconfigured anchor (F1), and returns `STATE_AUTHORITY_V2_TRUST_ANCHOR_UNAVAILABLE` when unanchored (F4). Both r1 defects are fixed, and fixing one did not re-open the other.
Fixture lane stays readable/testable without granting production: the r1-held `require_production=False` behaviour is untouched and the frozen 145 remain green.

**C-R2-5 — one signature, one carrier → HOLDS. EXECUTED.**

All four carrier spellings of the same valid signature, refused before cryptographic verification (`strict_signature_carrier_ok` at `trust_anchor.py:320`, ahead of the binding checks at `:323` and the verifier call at `:337`):

```
whitespace injected · newline injected · base64url alphabet · padding stripped
   -> ["MEASUREMENT_SIGNATURE_CARRIER_INVALID","PHYSICAL_HARNESS_UNAVAILABLE"]  (all four)
```

**§4 interaction check — nothing that held at r1 is weakened.** The frozen sentinel site `mbcx01_r13_packets.py:543-544` is untouched; the subtractive discharge (my r1 C1) still returns the fixture verdict verbatim; 145/145 frozen and 86/86 BUILD green at the pin. I found no interaction where the new activation surface weakens C1/C3/C4/C5.

## 4. Residual risks / P3 findings

**P3-1 — the single failure code is a deliberate trade, and I endorse it, but name its cost. READ-ONLY.** `authenticate_production_activation` collapses fourteen distinct binding failures into one `ACTIVATION_UNAUTHENTICATED` (docstring `:309-311`). Security-wise correct — an attacker learns "no", not which binding to grind. Cost: a legitimate operator who mis-enters one field during a real ceremony gets one undifferentiated code across fourteen possibilities, which is a fail-loud-but-not-fail-informative corner. That is a runbook problem, not a code one: the ceremony runbook should carry a local, non-admitting self-check that tells the operator which binding is wrong before they take the statement to the verifier. Fix class: documentation/runbook. Codex gate.

**P3-2 — my own probe hygiene. EXECUTED.** My first C-R2-1 probe died at custody validation before reaching the anchor and would have been reported as a meaningless "refused." This is the fifth consecutive MBCX round where a probe of mine, not the artifact, was the broken thing; the probe-fire assertions (`probe fires? …`, `bindings identical: …`) are what caught it and are now standing practice in my lane.

Carried, unchanged, correctly not-claimed-closed (I re-read and do not reopen): BUILD A binds custody digests not documents; BUILD A's accumulate-then-refuse ordering (I judge it not a defect — admission never happens and the frozen verdict is preserved; the store read is read-only); deterministic default validity instant; deferred exactness SUITE execution; `mbcx01_build_win32.py` unexecuted with its flagged ordinal; T2 box-owner ceiling.

Ruling on the packet's invited schema-placement challenge (§7): `minimum_activation_generation` belongs in the anchor, and TUF settles it — the anti-rollback floor lives with the trusted (client-side) root, not with the metadata being offered.

## 5. SWEEP LOG

| Query | Opened (URL + deciding section) | Effect | Label |
|---|---|---|---|
| TUF specification root metadata "root of trust" client must be pre-installed trusted root keys bootstrap | `github.com/theupdateframework/specification/blob/2b4e184…/tuf-spec.md` — §5 Step 0: *"Load the trusted root metadata file. We assume that a good, trusted copy of this file was shipped with the package manager or software updater using an out-of-band process."* · §2.1.1: *"The client-side of the framework must ship with trusted root keys."* · §1.5.3: *"The root of trust must not rely on external PKI."* · §5 Step 1.4 rollback rule | Confirms the fold's model at its origin: the verifier's root arrives out-of-band and the claimant's own root never bootstraps. Step 1.4 additionally settles the packet's open schema-placement question: the anti-rollback floor belongs with the trusted client-side root, so `minimum_activation_generation` in the ANCHOR is standard-consistent | SEARCHED |
| SLSA v1.2 verifying-artifacts §Step 1 | not opened by me this round | Driver's §9 row cites it; I opened it in an earlier MBCX round. Carried as argument only — my GO does not rest on it | RECALLED |
| Ed25519 malleability / carrier canonicalization | not opened | The claim is about whether this code maps one signature to one carrier string; settled by executing four carrier mutations against the pinned check | UNSEARCHED (SETTLED-BY-PINNED-BYTES) |
| Canonical-JSON digest binding | not opened | S7 executed the only question that matters (bytes vs `manifest_id`) | UNSEARCHED (SETTLED-BY-PINNED-BYTES) |

Why I stopped: the one claim in this round that genuinely rests on prior art is the bootstrap model, and one controlling primary opened at origin settles it. Everything else was answerable by execution against pinned bytes.

## 6. WHY THIS EXISTS

**(1) ALREADY-BUILT? — ADOPT is the right call, and the internal-shelf log is real. SPOT-RUN, EXECUTED.**
The role card requires me to spot-run the internal log rather than read it. I ran the packet's own query against the bridge repo at HEAD:

```
git grep -i -E "trust anchor|pinned owner|preconfigured root|OWNER_TRUST_ANCHOR" HEAD -- src
  -> 12 hits, ALL compile-time or per-run pins:
     broker-proxy.ts:221,327 "PINNED upstream trust anchor bundle … no ambient trust"
     revocation-verifier.ts:180 "The pinned trust anchor (root)"
     web-data-capture-compose.ts:64,175 pinned root snapshot
     run-ca.ts:4,33 per-run SPKI (the packet's cited RFC-7469 pin)
git grep -i -E "process\.env\.[A-Z_]*(TRUST|ANCHOR|ROOT_KEY)" HEAD -- src   ->  ZERO HITS
```

The log's claim is true and its conclusion is right: the bridge has plenty of pinned anchors but no operator-configurable anchor loader to lift — confirmed by the zero-hit env query, which is the sharper form of the question and which the log did not run. Not a vacuous log; not a curated-list read.

**(2) PRODUCT-FIT? — one plain sentence, and it is fail-loud, not prevention.** An operator needs the system to refuse production admission unless the root of trust they themselves configured has signed off on exactly this manifest and custody set — and to say so by name when it hasn't. Mirror-not-cop holds: the T2 ceiling is intact, nothing here walls out a box owner, and the fold is tamper-evident, not tamper-proof. `PRODUCTION_TRUST_ANCHOR_UNAVAILABLE` is a named, loud red.

**(3) BIGGER-THAN-THE-BUG? — NO, on my own reading.** The bug was "the claimant supplies its own root." The minimum mechanism that fixes it is a verifier-side root plus a statement binding this manifest — which is what landed: one module (345 lines), one fixture, five witnesses, one detached statement. It builds no engine, no policy language, no key-management subsystem, and completes the already-committed ceremony spec's §2/§3 intent. A repair sized to the defect.

## 7. Fix class and re-review

No re-review trigger. No finding ripples architecture, interface or security. The one actionable item (P3-1) is documentation/runbook class → codex gate. P3-2 is against my own method, not the artifact.

Side effects: none. Review repo `git status --porcelain` = 0 entries. All probes ran on a `git archive` extraction and in-memory copies under `%TEMP%`; probe directory and all transcripts removed and verified absent. No file modified, staged, or committed. No experiment, provider call, Job/ETW collection (`MBCX01_BUILD_ALLOW_PHYSICAL` left unset), signing ceremony, or spend. Nothing written to disk as a verdict.

---

## DRIVER ADJUDICATION NOTE (added at banking time — not part of the seat's verdict)

⚠ **This GO does not survive contact with the codex seat's executed findings, and the reason is
instructive rather than a seat error.** The two seats attacked DIFFERENT instances of one class
(ANTI-DRIFT §1, 2026-08-13: "two seats can also be right about different things"):

- SEAT1's decisive construction holds the legitimate universe fixed and changes **who signed the
  activation** — i.e. it tests an attacker who does NOT hold the anchor's private key. Correctly refused.
- The codex seat instead **configured the committed FIXTURE anchor and signed with the committed
  FIXTURE private key** (`mbcx01_build_ceremony_fixture.py:39`). That key ships in the repository, and
  production admission accepts it. SEAT1 never probed this, because its threat model assumed the
  configured anchor is legitimate.
- Likewise SEAT1's C-R2-2 check enumerated PARAMETER NAMES and callers and smuggled an anchor
  through the manifest/custody fields (refused); the codex seat instead passed a **mapping object whose
  `.get`/`__getitem__` reconfigure the process-global anchor mid-evaluation**. A parameter-name
  enumeration cannot see that gadget.

**Driver reproduction (LAW ZERO, run before this note was written):** with
`configure_fixture_owner_anchor()` installed, `resolve_owner_trust_anchor()` returns an anchor with
`fixture_only=True` for BOTH production authorities, and `inspect.getsource(authenticate_production_activation)`
contains no `fixture_only` check at all. The flag is parsed and stored, never enforced.

Both seats are therefore correct about what they tested; the CLASS is open. Per §3's authority ladder a
constructed EXECUTED bypass outranks a pass over ground that bypass was never run against, so the round
adjudicates NO-GO — see `MBCX-01-BUILD-ACCEPTANCE-ROUND-r2-SYNTHESIS.md`. SEAT1's positive
contributions stand and are NOT re-litigated: C-R2-3 (seven splice axes incl. the same-`manifest_id`
mutation), C-R2-5 (four carrier spellings), the r1 false-REJECT repair, the fail-closed-when-unanchored
behaviour, and the sharper zero-hit `process.env.*TRUST|ANCHOR|ROOT_KEY` shelf query.
