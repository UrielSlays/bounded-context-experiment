# MBCX-01 BUILD acceptance r2 — SEAT2 (ChatGPT / GPT-5.6 Sol, <council-browser-port>) verdict — banked from thread

Banked by the driver 2026-08-14 from conversation `<id>`.
Packet `MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r2.md@12b1c992`; code pin `6622bcd9`.

## VERDICT: GO — EXECUTED

Key claims (full text of the seat's structured verdict follows the driver note):
- Constructed a NEW fully self-authored trust universe with FRESH in-memory Ed25519 keys
  (measurement signing, state signing, state readback, attacker activation authority), attacker
  manifests, all four attacker custody documents, an attacker-signed 100-cell grid, and a fifth
  `OwnerCeremonyActivationV1` correctly bound to that attacker universe — even naming the REAL
  configured anchor id. Refused at all three doors:
  `FRESH_MEAS_SELF_AUTH -> [PHYSICAL_HARNESS_UNAVAILABLE, PRODUCTION_ACTIVATION_UNAUTHENTICATED]`,
  `FRESH_EXACTNESS_SELF_AUTH -> MeasurementAuthorityError PRODUCTION_ACTIVATION_UNAUTHENTICATED`,
  `FRESH_STATE_SELF_AUTH_VERIFY/ADMIT -> [... STATE_AUTHORITY_V2_ACTIVATION_UNAUTHENTICATED]`.
- **Its own stated scope limit, verbatim: "The only thing I could not supply was its private key."**
- Independently reconstructed the PRE-FIX tree at `4e58f9b5` in a temp dir and reproduced all four
  original defects (`-> []` admissions; `STATE_AUTHORITY_V2_ROOT_NOT_TRUSTED` false-reject;
  whitespace carrier accepted), then deleted it (`PRE_FIX_TEMP_CLEAN=True`) — so the green is
  discriminating against the actual prior defect.
- C-R2-3: seven authority-bearing splices of a legitimately owner-signed activation all
  `ACTIVATION_UNAUTHENTICATED`, including a genuine generation-0 statement against an anchor floor of 1.
- C-R2-5: whitespace / unpadded / base64url refused at every door; BUILD-side `.mjs` returns
  `{"ok":true,"valid":[true,false,false,false]}`.
- SWEEP (all SEARCHED at origin this round): SLSA v1.2 Verifying-artifacts Step 1 · TUF v1.0.36
  root role + client workflow · Node Buffer API (base64 accepts whitespace + URL-safe alphabet —
  which is WHY the strict carrier check is load-bearing) · Node Crypto Ed25519 calling convention ·
  RFC 8032 (64-octet signature) · RFC 8785 (JSON canonicalization).
- WHY-THIS-EXISTS: ALREADY-BUILT ⇒ adopt the trust pattern, not a framework; PRODUCT-FIT ⇒ *"MBCX
  must distinguish 'these supplied documents agree with each other' from 'these documents were
  authorized by the owner root this verifier was already configured to trust'"*;
  BIGGER-THAN-THE-BUG ⇒ NO.
- Execution caveat, self-disclosed: the full clean-room launcher exceeded Moonwalker's 120 s
  one-shot wrapper and was terminated by the harness; the seat explicitly does NOT claim an observed
  exit code from it, and compensated with per-blob pin checks + the 86-test BUILD run + a fresh
  `verify-build-bundle.py` (`BUNDLE_EXIT=0`, all sections PASS).
- Side effects: none. No file modified/staged/committed; no experiment, provider call, paid call,
  physical collection or ceremony; pre-fix reconstruction transient and cleaned; its one persistent
  Moonwalker shell session explicitly stopped.

### P2 residual it recorded (the crux of the round's split), verbatim:

> `OwnerTrustAnchor` includes a `fixture_only` provenance bit, while the same production
> authentication function is intentionally exercised under the committed fixture owner anchor in
> no-paid tests. Therefore a trusted operator must not configure that fixture anchor as a real
> deployment's owner root. This is not reachable through the packet's contractually-untrusted data
> adversary; request callers cannot select or replace the configured anchor, and an unconfigured
> process fails closed. It belongs in activation/runbook discipline, not another trust-bootstrap
> council loop.

---

## DRIVER NOTE (added at banking; not part of the seat's verdict)

SEAT2 SAW the fixture-anchor fact that the codex seat executed into a full admission, and
adjudicated it as operator discipline rather than a bypass. The driver settled that reachability
dispute at the byte: every importer of `mbcx01_build_ceremony_fixture` is fixture/demo/test/verifier
code and no production runtime exists yet, so SEAT2 is right about reachability TODAY — and codex is
right that a verifier accepting a publicly-committed test root is unsound the moment a real ceremony
happens. Both are folded, neither is averaged. Full reasoning:
`MBCX-01-BUILD-ACCEPTANCE-ROUND-r2-SYNTHESIS.md`.
