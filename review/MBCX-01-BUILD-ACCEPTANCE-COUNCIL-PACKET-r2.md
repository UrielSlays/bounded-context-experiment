> ⛔⛔ **CLOSED ROUND — DO NOT COPY THIS FRAMING INTO A NEW PACKET.** Banner added 2026-08-15;
> the body below is preserved byte-for-byte because the banked seat verdicts quote it by claim ID and
> by phrase, and rewriting it would desync the record from the answers it received.
>
> **Two things this packet got wrong, both settled since:** (1) it declared an outside-caller threat
> class that this lane's design of record does not have — the design carries no threat model at all,
> and every caller of the guarded functions is the harness and its own tests, so the party it names
> cannot exist (full record: `MBCX-01-BUILD-ADVERSARY-PREMISE-CORRECTION-2026-08-14.md`); and (2) it
> is written in the sharp register, which is what ends a reader at cold start on a lane that is a
> measurement harness.
>
> **The next packet asks whether the INSTRUMENT CAN PRODUCE A FALSE SCIENTIFIC RESULT** — falsify the
> I01–I17 validity invariants and the ETW surface — **and is written in the neutral CS register**
> (method: Gravity memory `fable-neutral-framing`; tool `<vault>`,
> dry-run first). Keep only the packet field names the checker enforces.

# MBCX-01 BUILD acceptance council packet — r2 (focused re-round: the trust-bootstrap fold)

Packet prose is a pointer map, not evidence — byte-check it.

## 0. Seat priming, seal, and pins

You are one Moonwalker council seat reviewing the MBCX-01 production BUILD (CODE-class,
executable). Read `<vault>` first and
operate under it: read-only adversarial reviewer; probes yes, fixes no. Maintain the
lateral seal — do not inspect any other seat's r2 output. Your own longitudinal MBCX lane
context (including your own r1 verdict) is allowed and must be labeled.

Repository: `<repo>-build`
(branch `codex/mbcx01-production-build`).

**What this round is:** r1 closed NO-GO on one P0 —
`MBCX01-BUILD-R1-TRUST-BOOTSTRAP` (production trust root, custody documents, and signing
key all caller-supplied and self-referential; BUILD A additionally false-REJECTED the
ceremony spec's own production-shaped manifest). The fold
`AUTHENTICATED_PRODUCTION_TRUST_BOOTSTRAP` landed red-first at the pins below, plus the
leaf `MBCX01-BUILD-R1-SIGNATURE-CARRIER` (strict base64 carrier). **The deciding question:
does the fold close the class, on the real adversary surface, without weakening anything
that held at r1?**

- Fold content commit: `4b84d7b9ef7713bfb94c32b32b119e4d4f732580`
- Canonical-bytes pin (all subjects; identical content to the fold commit):
  `6622bcd933454f8fdf9e029ed60664f56ac4ab45`
- BUILD pin manifest blob: `7a2b2bad87576d449dd4c7f40582dadaf8761c8a` (committed `e0378df`,
  33 subjects + 32 frozen dependencies)
- Pre-fix bytes (the red bank's pin): `4e58f9b545c0546fd53132da71500cc5be04280c`
- r1 verdicts + synthesis + `MBCX-01-OPEN-ISSUES.json` (the discharge conditions under
  review): banked in-repo at `966d922`-era commits; read
  `MBCX-01-BUILD-ACCEPTANCE-ROUND-r1-SYNTHESIS.md` for what the round must discharge.
- Governing r13.2 commit (frozen, unchanged): `d97d654e21918450994cfddb5a53dc5da2e962bb`

### Canonical bytes (read at these pins)
- `mbcx01_build_trust_anchor.py@6622bcd933454f8fdf9e029ed60664f56ac4ab45`
- `mbcx01_build_ceremony_fixture.py@6622bcd933454f8fdf9e029ed60664f56ac4ab45`
- `mbcx01_build_measurement_authority.py@6622bcd933454f8fdf9e029ed60664f56ac4ab45`
- `mbcx01_build_state_authority.py@6622bcd933454f8fdf9e029ed60664f56ac4ab45`
- `mbcx01_build_state_adapter.py@6622bcd933454f8fdf9e029ed60664f56ac4ab45` (+ `_operator_b` same pin)
- `mbcx01_build_exactness_authority.py@6622bcd933454f8fdf9e029ed60664f56ac4ab45`
- `mbcx01_build_integration.py@6622bcd933454f8fdf9e029ed60664f56ac4ab45`
- `verify-build-receipt-signature.mjs@6622bcd933454f8fdf9e029ed60664f56ac4ab45`
- `MBCX-01-BUILD-OWNER-TRUST-ANCHOR.fixture.json@6622bcd933454f8fdf9e029ed60664f56ac4ab45`
- `MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md@6622bcd933454f8fdf9e029ed60664f56ac4ab45` (§0/§3 updated)
- `test_mbcx01_build_state.py@6622bcd933454f8fdf9e029ed60664f56ac4ab45` (+ `_measurement`, `_integration` same pin)
- `MBCX-01-BUILD-REPAIR-LEDGER.json@6622bcd933454f8fdf9e029ed60664f56ac4ab45` (37 invariants / 86 witnesses)
- `verify-build-bundle.py@6622bcd933454f8fdf9e029ed60664f56ac4ab45`
- `mbcx01_build_trustboot_probe.py@6622bcd933454f8fdf9e029ed60664f56ac4ab45`
- `MBCX-01-BUILD-TRUSTBOOT-RED-WITNESS-RUN-2026-08-14.txt@6622bcd933454f8fdf9e029ed60664f56ac4ab45` (+ `…-GREEN-…` same pin)
A working-tree file at the same path may have moved off the pin — a seat reading the tree
must say so and confirm it matches the pin.

Authorized execution: deterministic read-only reconstruction, the committed suites, and
fresh no-paid adversarial probes. ⛔ Do NOT run the experiment, provider/model calls, real
Job/ETW collection (`mbcx01_build_win32.collect` stays double-gated), a signing ceremony,
or any spend. Verify the clean-room reconstruction yourself:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\verify-build-pinned.ps1 -Commit 6622bcd933454f8fdf9e029ed60664f56ac4ab45 -ManifestBlob 7a2b2bad87576d449dd4c7f40582dadaf8761c8a
```

## 1. Verdict contract

Return, in-thread, one report: **GO / GO-WITH-FIXES(class) / NO-GO** · evidence read
(path:line@sha) · SWEEP LOG (queries · opened · why stopped; labels
SEARCHED/RECALLED/UNSEARCHED with reasons) · findings labeled **EXECUTED / READ-ONLY** ·
residual risks · fix CLASS if any. Executable artifact: a READ-ONLY verdict cannot be the
deciding GO; run the banked red witnesses AND construct fresh self-authored trust
universes of your own — the r1 lesson is that the seat that never supplied its own root
missed the class entirely.

### Re-review trigger
Any finding that ripples architecture / interface / security reconvenes the council; leaf
edges go to the codex gate.

## 2. Immutable truths

- **T2 ceiling (settled — not a question):** a same-host admin / SYSTEM / box-controlling
  actor is the box owner; on-box walls against them are theater (`DESIGN-SHELF-MAP.md` §1).
  The anchor separates the bounded api-caller from the OPERATOR, not the box owner: an
  actor who can rewrite operator configuration or environment is the box owner and out of
  scope. Do not propose closing box-owner families.
- The frozen r13.2 subjects are byte-frozen; 145/145 frozen tests must remain green and
  unweakened; `verify-r13-receipt-signature.mjs` is frozen and untouched (the carrier fix
  lives in the BUILD-side `verify-build-receipt-signature.mjs` + Python doors).
- Fixture evidence must never create production or scientific authority; the committed
  anchor fixture is `fixture_only:true` and key-free, enforced by `verify-build-bundle.py`.
- Everything that HELD at r1 is not re-litigated as a question (see §4) — but any
  INTERACTION of the new activation surface with those held properties is in scope.

## 3. Claims to attack (construct the bypass; RUN it; name the residual)

1. **C-R2-1 — a self-authored trust universe cannot clear any production door.**
ADVERSARY: api-caller — supplies a fully self-authored manifest + four custody documents +
fresh Ed25519 keys + signed receipts/grid (the r1 winning attack, re-run against the fold).
REACHES IT VIA: data
ADMITTED AT: mbcx01_build_measurement_authority.py:evaluate_production_measurement
Attack: rebuild the r1 attack from scratch on all three doors (measurement, state
`verify_production_scorer_input`, exactness `verify_production_carrier_exactness`);
also self-author the ACTIVATION statement itself under your own key. Nothing may admit
without an activation signed under the verifier-configured anchor.

2. **C-R2-2 — the anchor is operator-wired, not caller-reachable.**
ADVERSARY: api-caller — tries to deliver or substitute the anchor through any per-request
parameter, evidence document, manifest field, or injected object graph (including the new
optional `trust_root_manifest` producer-side parameters).
REACHES IT VIA: data
ADMITTED AT: mbcx01_build_trust_anchor.py:configure_owner_trust_anchor
Attack: trace every path from request data to anchor resolution; a caller-supplied anchor
that is honored anywhere is the round's NO-GO. Distinguish operator wiring
(`configure_owner_trust_anchor` / `MBCX01_BUILD_OWNER_TRUST_ANCHOR`) from request surface.

3. **C-R2-3 — activation binding is exact and rollback-proof.**
ADVERSARY: api-caller — replays or splices a LEGITIMATE owner-signed activation: onto a
different manifest, a mutated manifest with the same `manifest_id`, a different signing
key, a different provenance digest, outside the validity window, or a rolled-back
activation generation.
REACHES IT VIA: data
ADMITTED AT: mbcx01_build_trust_anchor.py:activation_errors
Attack: per-axis splice/replay of a genuinely-signed activation; every axis must refuse
with a named error. Digest binding must be over canonical bytes, not `manifest_id`.

4. **C-R2-4 — the BUILD A shape split fixes BOTH r1 defects.**
ADVERSARY: api-caller — presents (a) a fixture-shaped self-authored root (the r1
false-ACCEPT) and (b) claims the ceremony's own production-shaped manifest still cannot
be used (the r1 false-REJECT).
REACHES IT VIA: data
ADMITTED AT: mbcx01_build_state_authority.py:verify_state_authority_receipt_v2
Attack: (a) must refuse; (b) the production-shaped manifest under a properly-anchored
activation must ADMIT (witness ba31) and must refuse only when unanchored. Also probe the
FIXTURE lane: fixture manifests must stay readable/testable without granting production.

5. **C-R2-5 — one signature, one carrier.**
ADVERSARY: api-caller — submits the same valid Ed25519 signature under multiple carrier
spellings (whitespace-injected, base64url alphabet, non-canonical padding) to split
receipt identity / dedup / audit trails.
REACHES IT VIA: data
ADMITTED AT: mbcx01_build_trust_anchor.py:strict_signature_carrier_ok
Attack: mutate carriers on every signature door (Python authorities + the BUILD-side
`.mjs`); decode/re-encode equality must refuse every non-canonical carrier BEFORE
cryptographic verification.

## 4. What HELD at r1 (do not re-grind; interactions ARE in scope)

C1 subtractive-sentinel non-weakening · C3 crash windows cannot mint (BEFORE_READBACK
adjudicated not-a-bypass) · C4 durable anti-replay + operator-B independence · C5 local
custody-separation mechanics. All three seats executed these at r1; the fold's own suites
keep them green (86/86 BUILD + 145/145 frozen at the pin). If the new activation surface
WEAKENS any of them, that is a fresh finding, not a re-grind.

## 5. Red witnesses per closed class (banked; re-run them)

`MBCX-01-BUILD-TRUSTBOOT-RED-WITNESS-RUN-2026-08-14.txt` — Stage 1: the four r1 attacks
reproduced on pre-fix bytes (`4e58f9b`, reconstruction byte-verified against git) via
`mbcx01_build_trustboot_probe.py`; Stage 2: 9/10 new witnesses red (the shim it needed is
printed in the bank's appendix; Stage 1 is the load-bearing red).
`MBCX-01-BUILD-TRUSTBOOT-GREEN-WITNESS-RUN-2026-08-14.txt` — 10/10 new witnesses
(ba29–ba33, bw17–bw21), BUILD 86/86, frozen 145/145, `verify-build-bundle.py` PASS with
the new `committed_owner_trust_anchor_fixture_only` check. The DRIVER re-ran, pre-dispatch,
at the pin: all four probes (refusals named), all suites, the clean-room reconstruction,
and a tamper red on the committed anchor fixture (`fixture_only` flip → bundle verifier
exit 1; restored → exit 0).

## 6. WHY THIS EXISTS (build-decision challenge — answer all three)

(1) ALREADY-BUILT? The fix ADOPTS the SLSA/TUF verifier-controlled pre-configured
root-of-trust model rather than inventing one (r1 synthesis §External anchor; driver
re-opened SLSA v1.2 Verifying-artifacts §Step-1 this session). Internally, the bridge repo
has no operator-config anchor loader to lift (its pins are compile-time constants —
RFC-7469 SPKI pin at `run-ca.ts:81` per `docs/fips-crypto-inventory.md`); the module
follows the lane's existing injected-signer style. (2) PRODUCT-FIT? Fail-loud governed
admission: absent/wrong anchor stays red with named errors; nothing prevents a box owner
from anything (mirror-not-cop). (3) BIGGER-THAN-THE-BUG? Both r1 NO-GO seats ruled this
fold "review-authority-completing, not a Shelf-Zero new subsystem" — it completes the
committed ceremony spec's own §2/§3 intent. Attack that ruling if you disagree.

## 7. Non-claims and OPEN residuals (each named; attack the choices, not just the code)

- **Detached activation:** the owner signature lives in a fifth injected item
  (`OwnerCeremonyActivationV1`), NOT inside ceremony evidence document 4 — a receipt that
  contained the manifest digest while the manifest binds the receipt's digest is a preimage
  cycle with no solution. The ceremony spec §0/§3 was updated to match. Attack: does the
  detached statement leave any evidence document unauthenticated in a way that matters?
- **BUILD A binds custody DIGESTS, not documents** (its interface never receives the four
  documents; BUILD B recomputes each digest from the injected document). Named residual in
  `production_activation_binding`'s docstring — not claimed closed.
- **BUILD A refusal is accumulate-then-refuse:** the state verifier still resolves the
  durable store read-only before returning its refusal; admission never happens and the
  frozen production verdict is preserved (ba29). BUILD B refuses before any grid analysis.
  If you judge the state-side ordering a defect, say why concretely.
- **`minimum_activation_generation` lives in the ANCHOR** (operator-controlled), not the
  manifest — an owner anti-rollback floor. Schema-placement challenge welcome.
- Producer-side optional `trust_root_manifest` parameters (adapter, operator-B,
  `derive_receipt_content_independent`) are a fold RIDER enabling ceremony §3.6 injection;
  witnessed by ba31/ba26/ba27/bi01. Attack the rider on its own terms.
- No protection against the box owner (T2, §2). Trust-root validity still uses the
  deterministic default instant; the exactness SUITE execution stays deferred (spec §3);
  `mbcx01_build_win32.py` stays unexecuted with its flagged ordinal — all unchanged from
  r1, still open, still not claimed closed.

## 8. Sweep lane (every seat)

SWEEP APPLIES TO: the verifier-root bootstrap model (SLSA/TUF/Sigstore trust-root
distribution), Ed25519 verification + signature-carrier malleability, canonical-JSON
digest binding, and any standards claim in your own findings. Run your OWN web sweep — it
is not automatic.
DELIVERABLE: a SWEEP LOG in your verdict — exact queries · what you OPENED with URL +
deciding section · what changed/confirmed · why you stopped.
LABELS: SEARCHED / RECALLED / UNSEARCHED(+reason: NOT-LOAD-BEARING /
SETTLED-BY-PINNED-BYTES / COULD-NOT / DID-NOT) — every prior-art / standards-bearing
finding carries exactly one.
CONSEQUENCE: an UNSEARCHED or RECALLED finding cannot be the deciding GO on a
prior-art/standards claim; a round where no seat swept such a claim is INCOMPLETE.
HONEST OUT: if you cannot reach the web this session, say so in one line — a
seat-capability report, not a discharge.

## 9. Driver's own search log (ANTI-DRIFT §7 required field)

- 2026-08-14, moonwalker_http_fetch: `https://slsa.dev/spec/v1.2/verifying-artifacts`
  OPENED (ranged read of §Step 1) — verification begins by verifying the envelope
  signature "using the roots of trust, resulting in a list of recognized public keys";
  the roots are the VERIFIER's own configured roster (the spec's example is the
  verifier's key/builderId list with per-entry trust ceilings). PRIMARY; confirms the
  fold's anchor model. Stopped: the deciding sentence was found and the model matches.
- TUF (pre-distributed root of trust; claimant's own root never bootstraps): carried from
  the r1 synthesis §External anchor where BOTH NO-GO seats opened it. RECALLED-with-banked-source.
- Internal-shelf log: grep across bridge `src/` for `trust anchor|pinned owner|SPKI|
  preconfigured root` (2026-08-14) → hits are compile-time pins (RFC-7469 SPKI
  `run-ca.ts:81`, per `docs/fips-crypto-inventory.md` read in full this session) and CRL
  chain verification — no operator-config anchor loader exists to adopt; adopted instead:
  the lane's own injected-signer pattern + the frozen r13 `.mjs` verifier's closed
  contract (BUILD-side sibling, frozen file untouched). `MBCX-01-BUILD-SHELF-LOG.md`
  carries the original three-repo BUILD sweep.
- Driver executed the packet's own attacks pre-dispatch: probes A–D post-fix at the pin
  (named refusals), plus the anchor-fixture tamper red (§5).

## 10. Omission attack (≥1 seat, all seats welcome)

What did the fold not name? Attack the un-named set: the anchor file's own parse surface
(`MBCX01_BUILD_OWNER_TRUST_ANCHOR` pointing at attacker-influenced paths is operator/box
ground — but is the LOADER fail-closed on malformed anchors?), canonicalization edges in
the activation preimage, the ceremony-fixture module's importability from production code,
process-global `_CONFIGURED_ANCHOR` lifecycle (test pollution / reconfiguration races),
key-id collision between anchor and manifest rosters. Also ask: is any finding-class here
a TAR-PIT (theater / unbounded / wholesale-closeable) — if so name the disposition, don't
grind.

## 11. Blind round

Sealed, independent first pass. This packet carries no driver recommendation and no other
seat's r2 findings.
