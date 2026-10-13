# MBCX-01 BUILD acceptance — round r1 synthesis (driver)

Status: round CLOSED **NO-GO**. Recorded 2026-08-14. Do NOT advance to any PR/merge gate.
The r13.2 experiment design remains CONFIRMED and untouched; this is a BUILD-acceptance NO-GO.

## Verdicts (all three read, banked beside this file)

| Seat | Verdict | Attacked the caller-supplied-root surface? |
|---|---|---|
| SEAT1 Opus 5 (<council-browser-port>) | GO-WITH-FIXES(doc/leaf) | NO — its C2/C5 flipped the *committed* manifest (refused) and never supplied a self-authored root |
| SEAT2 ChatGPT Sol (<council-browser-port>) | **NO-GO** (P0, self-authorable trust bootstrap) | YES — EXECUTED |
| SEAT3 codex-exec sol/xhigh | **NO-GO** (P0, trust-root bootstrap / custody authentication) | YES — EXECUTED |

Model-diverse convergence: two independent seats, two different harnesses, constructed the SAME
attack and got the SAME result. Per ANTI-DRIFT (#509 lesson) convergence on one class is a strong
signal. §3 authority ladder: a constructed EXECUTED bypass on the real adversary surface outranks a
reasoned/EXECUTED pass that never reached that surface. **The round is NO-GO.**

## The finding, reproduced by the driver at the byte (LAW ZERO duty)

**Claim C2/C5 is false under the packet's own declared `api-caller` adversary: the production trust
root, its custody documents, and the signing key are ALL caller-supplied and self-referential;
nothing anchors them to owner-preconfigured configuration.**

Driver reproduction (not a bank of the seats' claim):
- `mbcx01_build_measurement_authority.py:evaluate_production_measurement` and
  `mbcx01_build_state_authority.py:verify_production_scorer_input` take `trust_root_manifest` and
  `custody_evidence` as **parameters** — byte-verified via `inspect.signature`.
- The module reads **no** fixed owner root file (no `open`/`_load`/`Path` — byte-verified via
  `inspect.getsource` regex) and references **no** owner-anchored trust constant.
- The suite's own `admit(simulated_production_grid())` returns `[]` on a fully caller-supplied
  production stack signed with the committed fixture key — driver-run, returned `[]`.
- Custody validation only checks: role strings differ · signer key not in editor chain ·
  the four digest fields hash-match documents **the same caller supplied** · SHA-384 grammar.
  It never authenticates a signature over those documents against a pre-existing anchor.

ChatGPT's sharper corollary (BUILD A, both sides wrong): the state validator *demands*
`production_ready:false` + `NOT_ACTIVATED` + `fixture_only:true` roots, so it ACCEPTS an
attacker's fixture-shaped self-authored root and REJECTS the ceremony spec's own published
production manifest (`STATE_AUTHORITY_V2_ROOT_NOT_TRUSTED`). Implementation contradicts
`MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md`.

This is NOT a T2/box-owner theater case: the adversary is a bounded, contractually-untrusted
API-side claimant (the packet's declared `api-caller`), reaching the authority via DATA it supplies
— not a box owner. It is REAL.

## External anchor (both NO-GO seats, SEARCHED)

SLSA v1.2 "Verifying artifacts" and TUF both begin verification from a **verifier-controlled,
preconfigured root of trust** and never accept the claimant's own root as bootstrap. Internal
consistency inside a supplied trust graph ≠ authentication of that graph. This is the exact
category error; the fix adopts an established model rather than inventing one.

## What HELD (do not re-grind at r2)

C1 sentinel-subtraction non-weakening (all three seats, EXECUTED — laundering attempts failed) ·
C3 crash windows PENDING/BROKEN cannot mint (EXECUTED; BEFORE_READBACK = recovery of a true
committed fact, adjudicated not-a-bypass by two seats) · C4 durable anti-replay on every axis +
operator-B poison detected (EXECUTED) · C5 local custody-separation mechanics (collision/revocation/
expiry/digest all fire) — narrow, does not close C2. Frozen 145/145 + BUILD 76/76 + clean-room
reconstruction all green and unweakened.

## Fix class (both NO-GO seats agree; NOT a new machine, NOT an experiment change)

`AUTHENTICATED_PRODUCTION_TRUST_BOOTSTRAP` — completing what the ceremony spec already intends
(the implementation "stopped one layer too early"). Minimum:
1. A pre-existing owner/operator trust anchor the API request cannot supply or substitute
   (a pinned owner root public key / OS-controlled config identity the verifier loads, not a param).
   T2 unchanged: this separates the bounded api-caller from the operator, not the box owner.
2. Authenticate the four custody documents by **signature** against that anchor (custodian
   attestation, editor approval, build provenance, owner ceremony receipt) — not hash-match of
   caller-supplied documents against caller-supplied digests.
3. Bind editor approval AND owner ceremony receipt to the **exact canonical manifest digest**
   (+ signing-key identity, provenance digest, validity window, activation generation) — not `manifest_id`.
4. BUILD A: split structural parsing (fixture, production_ready:false, readable/testable) from
   production activation (authenticated, production_ready:true) — fixing both the false-accept and
   the false-reject of the ceremony manifest.
5. New mandatory red witnesses: fresh attacker Ed25519 key + fully self-authored manifest/custody +
   signed 100-cell grid must FAIL before any store/grid/scientific analysis, while the legitimate
   authenticated ceremony path is GREEN.
TAR-PIT: one invariant closes the class wholesale — do not grind fake-role permutations.

## Routing

Security/interface finding ⇒ per the packet it re-enters the design/council gate. Both NO-GO seats
say this does NOT reopen r13.2, does NOT change the estimand/n=768/route/inference, and is bounded.
The fold completes the ceremony spec's own intent (shelf-grounded on SLSA/TUF), so it is
review-authority-completing, not a Shelf-Zero new subsystem. Next: implement the authenticated
bootstrap red-first, then BUILD acceptance r2 with the self-authored universes as the deciding red.

## Owner-relevant note (surfaced, not an escalation the canon can't answer)

The one genuinely owner-shaped question the fix implies: **who is the trusted injector of the
production trust root at experiment time?** If it is the owner's own operator config (the ceremony's
intended deployment), the anchor is a pinned owner key the verifier loads — pure implementation. The
standards + ceremony spec settle the mechanism, so this is being ruled in-lane and folded; recorded
here for visibility, not held for a decision.
