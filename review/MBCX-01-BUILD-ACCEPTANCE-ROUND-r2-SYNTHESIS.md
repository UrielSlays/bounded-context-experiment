# MBCX-01 BUILD acceptance — round r2 synthesis (driver)

Status: round CLOSED **GO-WITH-FIXES(FIXTURE-ISOLATION + VERIFIER-CONTEXT LIFECYCLE)**.
Recorded 2026-08-14. **BUILD acceptance is WITHHELD** until the named fixes land red-first and
`verify-build-bundle.py` is re-run; nothing here advances to a PR, a ceremony, or any spend.
The r13.2 experiment design remains CONFIRMED and untouched (145/145 frozen, zero frozen files
modified across the whole fold).

Pins: packet `12b1c992` (blob `1057ab74`) · code `6622bcd9` · manifest blob `7a2b2bad` ·
pre-fix bytes `4e58f9b5` · fold commit `4b84d7b` · banked verdicts beside this file.

## 1. Verdicts (all three READ, all three EXECUTED)

| Seat | Verdict | Probed WITHOUT the anchor key? | Probed WITH the committed FIXTURE key? |
|---|---|---|---|
| SEAT1 Opus 5 Extra (<council-browser-port>) | **GO** | YES — fresh keys, all 3 doors, 7 splice axes | **NO** |
| SEAT2 ChatGPT Sol (<council-browser-port>) | **GO** | YES — fresh keys, independent 2nd universe, all 3 doors | **NO** (saw the fact; ruled it operator-discipline, P2) |
| SEAT3 codex-exec sol/xhigh | **NO-GO** | (not the axis it chose) | **YES — admitted at all three doors** |

**This is not a 2-vs-1 vote and was not resolved as one.** The seats probed different instances
of one class (ANTI-DRIFT §1, 2026-08-13). Both GO seats state their own scope limit in their own
words — SEAT2: *"The only thing I could not supply was its private key."* Their GO is therefore a
demonstrated closure of **the r1 adversary** (a caller who does NOT hold the anchor key), and it is
real: two independently constructed fresh-key universes were refused at measurement, state and
exactness, with named errors, against a green control. The driver re-ran the four banked probes and
reproduces those refusals.

## 2. What the driver reproduced at the byte (LAW ZERO; done BEFORE writing any of this)

- **Codex F1 is factually correct.** `configure_fixture_owner_anchor()` →
  `resolve_owner_trust_anchor()` returns an anchor with `fixture_only=True` for BOTH production
  authorities, and `inspect.getsource(authenticate_production_activation)` contains **no**
  `fixture_only` check. The flag is parsed (`mbcx01_build_trust_anchor.py:154,162,192`) and never
  enforced. The matching private key is committed (`mbcx01_build_ceremony_fixture.py:39`), so the
  fixture owner key is public to anyone with the repository.
- **Codex F3 is factually correct**: `mbcx01_build_integration.py:141` installs the fixture anchor
  process-wide and never restores it.
- **REACHABILITY, settled at the byte (the split's real question, TAR-PIT Q1/Q2):** every importer
  of `mbcx01_build_ceremony_fixture` is fixture/demo/test/verifier code —
  `mbcx01_build_integration.py` (a *fixture* harness: its own docstring describes simulated
  collections, a FIXTURE signer and an in-memory simulated manifest), the two BUILD test modules,
  and `verify-build-bundle.py`. **No production runtime installs it, because no production runtime
  exists yet** — readiness is `BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`.
  ⇒ SEAT2's reachability reading is correct **today**; codex's severity is correct **the moment a
  real ceremony happens or a production evaluation shares an interpreter with the fixture graph.**
  Neither seat is wrong; they are answering "reachable now?" and "sound as a verifier?" respectively.

## 3. Disposition of codex's seven findings (each classified, none averaged)

| # | Codex label | Driver disposition |
|---|---|---|
| **F1** fixture anchor grants production authority | Critical | **REAL, FOLD NOW.** Not caller-reachable today (§2), but a verifier that accepts a publicly-known test root is unsound by the same standards this fold adopted. One check + one red witness. |
| **F2** injected mapping object swaps the global anchor mid-evaluation | Critical | **REAL but BOUNDED — fold as hardening.** Codex bounds it itself: unavailable if callers deserialize JSON into built-in containers. Under the packet's declared `api-caller`-via-DATA adversary it is not a live bypass; the inert-data boundary is still the right shape. |
| **F3** integration fixture leaves the anchor installed | High | **REAL, FOLD NOW** — closed by construction under the instance-scoped context. |
| **F4** default evaluation admits an expired manifest | High | **RE-FIND of a residual this packet DECLARED** (§7: "trust-root validity uses a deterministic default instant (manifest `published_at`), not wall clock … OPEN residual, not claimed closed"). Still fold it: Go's `crypto/x509` falls back to the real clock, never to a value carried by the artifact under verification. |
| **F5** strict carrier closes the tested encodings | (pass) | **CONFIRMED by all three seats** — the leaf fold holds. SEAT2 additionally opened the Node Buffer docs showing why it is load-bearing (Node's base64 decoder accepts whitespace and the URL-safe alphabet). |
| **F6** loader ambiguity at the operator config boundary | High→leaf | **FOLD** — strict parse, codex-gate class. |
| **F7** exactness can mint `PASS` without the suite running | High | **RE-FIND of a declared residual** (§7: the per-witness exactness SUITE execution is deferred; the authority binds identities and "does not bless carrier behavior"). Fold the *labelling* so `PASS` cannot read as "the suite ran." |

Two genuinely new defects (F1, F3), one bounded hardening (F2), two re-finds of declared
non-claims (F4, F7), one leaf (F6), one confirmation (F5). That is the honest count — **not**
"two Criticals", and **not** "no findings."

## 4. The close — ONE invariant, adopted not invented (driver sweep, banked separately)

`MBCX-01-BUILD-R2-TRUSTCONTEXT-SWEEP-LOG.md` records the primaries the driver opened at origin:
Go `crypto/x509/verify.go` (roots AND `CurrentTime` are per-call `VerifyOptions` fields; the
no-time fallback is the real clock, never the artifact's own value) and the TUF spec (trusted root
ships out-of-band; monotonic version defeats rollback). SEAT1 and SEAT2 independently opened TUF
and SLSA and reached the same model; SEAT1 additionally ruled — from TUF §5 Step 1.4 — that the
anti-rollback floor belongs with the client-side trusted root, which **settles the packet's open
schema-placement question in favour of the current placement (floor in the ANCHOR).**

**The invariant, COMPLEMENT-shaped (TAR-PIT Q4):** *production verification accepts exactly one
thing — an immutable, instance-scoped verifier context whose anchor is operator-supplied and not
fixture-marked, carrying its own current time — and refuses everything else.* This collapses F1,
F2 and F3 together: there is no process-global anchor left to swap or leak, and a fixture anchor is
structurally unable to enter a production context.

**Scope ruled FOLD, not a new machine** (Shelf-Zero Q-ZERO-B): it reshapes existing modules into a
named off-the-shelf pattern, adds no engine or lifecycle, and completes the committed ceremony
spec's own §2/§3 intent. ⚠ **Recorded disagreement:** codex ruled it "bigger than the bug" and asked
for a design gate; SEAT1 and SEAT2 each independently ruled NO on the same question. The driver
sides with 2 seats + the sweep, and surfaces the dissent here rather than burying it.

## 5. Fold spec (red-first; each item owes a discriminating witness)

1. **Instance-scoped immutable verifier context** replacing the process-global anchor; production
   verification takes it from operator wiring, never from a request parameter. Terminates F2/F3 by
   construction.
2. **Refuse `fixture_only` anchors in production authentication** — named error, and the committed
   fixture anchor must be structurally unable to authorize a production admission.
   RED: the fixture anchor + committed fixture key must FAIL every production door, while the
   fixture LANE (structural parsing, `require_production=False`) stays green.
3. **Verifier-controlled current time** on the context; the fallback is the real clock, never the
   manifest's `published_at`. RED: an expired manifest must refuse by name.
4. **Exactness result labelling** — a binding-only result must not present as `PASS` for suite
   execution. RED: a binding-only evaluation must not emit a value that reads as "the suite ran."
5. **Strict anchor-document parse** at the loader boundary (F6).

Everything the seats CLOSED stays closed and is not re-litigated: C-R2-1 under the r1 adversary,
C-R2-3's seven splice axes (incl. the same-`manifest_id` mutation), C-R2-5's four carrier
spellings, the r1 false-REJECT repair, and fail-closed-when-unanchored.

## 6. Honest execution caveats from the seats (recorded, not hidden)

Both browser seats reported that the full clean-room launcher exceeded their harness window
(SEAT2: Moonwalker's 120 s one-shot wrapper terminated it; SEAT1: its connector window twice), and
**both declined to claim an observed exit code from it** — each compensated with pin-verified byte
comparisons plus the 86-test BUILD run. The DRIVER ran the full launcher to completion separately:
`verify-build-pinned.ps1 -Commit 6622bcd9 -ManifestBlob 7a2b2bad` → `PINNED RECONSTRUCTION
COMPLETE`, readiness `BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`. SEAT1 also disclosed
that its first C-R2-1 probe died at custody validation before reaching the anchor gate and would
have been a meaningless "refused" had it not asserted the probe fired — it rebuilt and re-ran.

## 7. Not authorized by this round (unchanged)

No experiment, no provider/model calls, no route qualification or freeze, no physical grid, no
Job/ETW collection, no signing ceremony, no spend. Each needs its own explicit owner authorization.
