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

# MBCX-01 BUILD acceptance council packet — r3 (focused re-round: the fixture-isolation fold)

Packet prose is a pointer map, not evidence — byte-check it.

## 0. Seat priming, seal, and pins

You are one Moonwalker council seat reviewing the MBCX-01 production BUILD (CODE-class,
executable). Read `<vault>` first and
operate under it: read-only adversarial reviewer; probes yes, fixes no. Maintain the
lateral seal — do not inspect any other seat's r3 output. Your own longitudinal MBCX lane
context (including your own r1/r2 verdicts) is allowed and must be labeled.

Repository: `<repo>-build`
(branch `codex/mbcx01-production-build`).

**What this round is.** r2 closed **GO-WITH-FIXES**. The r1 class (a caller supplying its
own trust root) was confirmed CLOSED by all three seats — two of them built independent
fresh-key universes and were refused at every door. What r2 opened was the adjacent class:
**our own non-production material and the anchor's process-global lifecycle**. The fold
`MBCX01-BUILD-R2-FIXTURE-ISOLATION` landed red-first. **The deciding question: does the
instance-scoped verifier context close that class without weakening anything r2 confirmed,
and is the rider it introduced sound?**

- Fold content commit: `e89168b5463e2dddddda7af3f7bca8071c1c53b9`
- Canonical-bytes pin (all subjects): `aa3d0b1a4fbd843beb23af9cbd8e94e99de20f5a`
- BUILD pin manifest blob: `3e2a67536797faa6afa17ddf4d1363950131cbc6` (committed `994540bd`)
- Pre-fix bytes for this fold's reds: `491b0ab` (r2 synthesis commit)
- r2 round record (read it — its §3 disposition table is what this fold implements):
  `MBCX-01-BUILD-ACCEPTANCE-ROUND-r2-SYNTHESIS.md` + the three banked r2 verdicts +
  `MBCX-01-BUILD-R2-TRUSTCONTEXT-SWEEP-LOG.md` + `MBCX-01-OPEN-ISSUES.json`
- Governing r13.2 commit (frozen, unchanged): `d97d654e21918450994cfddb5a53dc5da2e962bb`

### Canonical bytes (read at these pins)
- `mbcx01_build_trust_anchor.py@aa3d0b1a4fbd843beb23af9cbd8e94e99de20f5a`
- `mbcx01_build_ceremony_fixture.py@aa3d0b1a4fbd843beb23af9cbd8e94e99de20f5a`
- `mbcx01_build_measurement_authority.py@aa3d0b1a4fbd843beb23af9cbd8e94e99de20f5a`
- `mbcx01_build_state_authority.py@aa3d0b1a4fbd843beb23af9cbd8e94e99de20f5a`
- `mbcx01_build_exactness_authority.py@aa3d0b1a4fbd843beb23af9cbd8e94e99de20f5a`
- `mbcx01_build_integration.py@aa3d0b1a4fbd843beb23af9cbd8e94e99de20f5a`
- `mbcx01_build_fixtureiso_probe.py@aa3d0b1a4fbd843beb23af9cbd8e94e99de20f5a`
- `test_mbcx01_build_state.py@aa3d0b1a4fbd843beb23af9cbd8e94e99de20f5a` (+ `_measurement`, `_integration` same pin)
- `MBCX-01-BUILD-REPAIR-LEDGER.json@aa3d0b1a4fbd843beb23af9cbd8e94e99de20f5a` (42 invariants / 95 witnesses)
- `verify-build-bundle.py@aa3d0b1a4fbd843beb23af9cbd8e94e99de20f5a`
- `MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md@aa3d0b1a4fbd843beb23af9cbd8e94e99de20f5a` (updated by this fold)
- `MBCX-01-BUILD-EXACTNESS-PRODUCTION-VERIFIER-SPEC.md@aa3d0b1a4fbd843beb23af9cbd8e94e99de20f5a` (updated)
- `MBCX-01-BUILD-FIXTUREISO-RED-WITNESS-RUN-2026-08-14.txt@aa3d0b1a4fbd843beb23af9cbd8e94e99de20f5a` (+ `…-GREEN-…` same pin)
A working-tree file at the same path may have moved off the pin — a seat reading the tree
must say so and confirm it matches the pin.

Authorized execution: deterministic read-only reconstruction, the committed suites, and
fresh no-paid adversarial probes. ⛔ Do NOT run the experiment, provider/model calls, real
Job/ETW collection (`mbcx01_build_win32.collect` stays double-gated), a signing ceremony,
or any spend. Verify the clean-room reconstruction yourself:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\verify-build-pinned.ps1 -Commit aa3d0b1a4fbd843beb23af9cbd8e94e99de20f5a -ManifestBlob 3e2a67536797faa6afa17ddf4d1363950131cbc6
```

⚠ Two r2 seats reported this launcher exceeding their harness window (one at a 120 s
one-shot wrapper) and honestly declined to claim its exit code. The DRIVER ran it to
completion at this pin: `PINNED RECONSTRUCTION COMPLETE`, all sections PASS, readiness
`BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`. If it exceeds your window, say so
and compensate with per-blob pin checks + the suites, exactly as they did.

## 1. Verdict contract

Return, in-thread, one report: **GO / GO-WITH-FIXES(class) / NO-GO** · evidence read
(path:line@sha) · SWEEP LOG (queries · opened · why stopped; labels
SEARCHED/RECALLED/UNSEARCHED with reasons) · findings labeled **EXECUTED / READ-ONLY** ·
residual risks · fix CLASS if any. Executable artifact: a READ-ONLY verdict cannot be the
deciding GO. **The r2 lesson is explicit and applies to you: two seats returned GO after
building attacker universes WITHOUT the anchor key, while the class was open through OUR
OWN committed material. Vary the knob nobody varied.**

### Re-review trigger
Any finding that ripples architecture / interface / security reconvenes the council; leaf
edges go to the codex gate.

## 2. Immutable truths

- **T2 ceiling (settled — not a question):** a same-host admin / SYSTEM / box-controlling
  actor is the box owner; on-box walls against them are theater (`DESIGN-SHELF-MAP.md` §1).
  The context separates the bounded api-caller from the OPERATOR. **The fold states its own
  ceiling: an adversary who can define a Python class in the verifier's process is already
  past the declared api-caller-via-DATA boundary; the fold makes the specific gadget inert,
  it does not contain arbitrary in-process code.** Do not propose closing box-owner families.
- Frozen r13.2 subjects are byte-frozen: 145/145 must stay green, zero frozen files modified
  (driver verified per-path with `git cat-file -e 91329b2:<path>`).
- The committed owner anchor document is fixture-only and key-free and must remain so.
- Everything r2 CONFIRMED is not re-litigated as an open question (§4) — but INTERACTIONS
  with the new context surface are in scope.

## 3. Claims to attack (construct the bypass; RUN it; name the residual)

1. **C-R3-1 — non-production material cannot grant production authority at any door.**
ADVERSARY: api-caller — presents the COMMITTED fixture anchor, the committed fixture owner
private key, fixture-shaped roots, or any other test material this repository ships.
REACHES IT VIA: data
ADMITTED AT: mbcx01_build_trust_anchor.py:authenticate_production_activation
Attack: sign a fully well-formed activation with the committed fixture owner key and drive
measurement, state (both doors) and exactness. Also hunt a SECOND path to a context: can any
sequence construct a `ProductionVerifierContext` around a `fixture_only` anchor at all?
The fixture LANE (`require_production=False`, structural parsing) must stay usable.

2. **C-R3-2 — no request-reachable path mutates authority state, during or between doors.**
ADVERSARY: api-caller — supplies mapping/sequence objects with behaviour (`__getitem__`,
`get`, `__iter__`, `__eq__`, properties, `__len__`) on any parameter of any door.
REACHES IT VIA: data
ADMITTED AT: mbcx01_build_trust_anchor.py (context resolution + wiring freeze)
Attack: the r2 gadget and better ones. The r2 fold's own rider exists because a snapshot
alone still let the gadget poison the process BETWEEN doors — attack the freeze itself:
re-entrancy, nesting, exceptions leaving it stuck, threads, and whether a failed
verification restores the prior wiring.

3. **C-R3-3 — the verifier's clock is the verifier's, and freshness never comes from the artifact.**
ADVERSARY: api-caller — supplies a manifest/receipt whose own timestamps would make a stale
or future-dated trust root look current.
REACHES IT VIA: data
ADMITTED AT: mbcx01_build_measurement_authority.py / mbcx01_build_state_authority.py validity paths
Attack: expired, not-yet-valid, and boundary instants; then attack the SCOPE CALL the fold
made — BUILD A judges the manifest validity window at the verifier instant while every other
instant remains the receipt's attested `knowledge_time`. Is that seam exploitable or
inconsistent?

4. **C-R3-4 — a binding-only exactness result cannot be read as proof the suite ran.**
ADVERSARY: api-caller — submits a receipt claiming `PASS`, or relies on a downstream reader
treating the binding result as suite execution.
REACHES IT VIA: data
ADMITTED AT: mbcx01_build_exactness_authority.py:verify_production_carrier_exactness
Attack: every value that can reach a consumer; is there any remaining spelling that reads as
"the carrier suite executed" when it did not?

5. **C-R3-5 — nothing r2 confirmed has regressed.**
ADVERSARY: (regression, not an actor) — the interface change made `context` a required
keyword of `authenticate_production_activation`.
REACHES IT VIA: data
ADMITTED AT: mbcx01_build_measurement_authority.py + mbcx01_build_state_authority.py callers
Attack: re-run the r2-confirmed set — self-authored universe WITHOUT the anchor key at all
three doors; the seven activation splice axes incl. the same-`manifest_id` mutation; all four
carrier spellings; the r1 false-REJECT repair; fail-closed-when-unanchored. Also: does any
caller reach the authentication path WITHOUT a context (a legacy/no-context branch would be
a hole), and is there any consumer outside this lane the signature change breaks?

## 4. What r2 CONFIRMED (do not re-grind; interactions ARE in scope)

Closure of the r1 class on all three doors, executed independently by SEAT1 and SEAT2 with
fresh keys · seven activation splice axes · four carrier spellings (SEAT2 opened the Node
Buffer docs showing why the check is load-bearing) · the r1 false-REJECT repair ·
fail-closed-when-unanchored named errors · the frozen 145 and the subtractive sentinel.

## 5. Red witnesses per closed class (banked; re-run them)

`MBCX-01-BUILD-FIXTUREISO-RED-WITNESS-RUN-2026-08-14.txt` — deciding reds on REAL committed
bytes. ⚠ Method note worth attacking: the worker found `git archive` NOT byte-identical
under this clone's `core.autocrlf=true` and switched to
`git -c core.autocrlf=false checkout-index`, verifying 356 tracked files identical to their
blobs. Verbatim pre-fix admissions: fixture anchor + committed fixture key → measurement
`[]`, state `[]`, exactness `ADMITTED result='PASS'`; gadget → `swaps_fired=15` and admitted;
integration release left `fixture_only=True` installed and a later production evaluation
returned `[]`; expired manifest → `[]`; binding-only exactness → `result='PASS'`;
duplicate-member anchor doc → ACCEPTED with the flag flipped.
⚠ **Honest limitation the worker disclosed:** the nine witness-level reds are
SYMBOL-ABSENCE (`AttributeError`), not behavioural, because the post-fix API requires the
context — it declined to add an optional-context path that would have left a hole. The
BEHAVIOURAL red is the probe. Attack that trade.
GREEN: 9/9 new witnesses, BUILD **95/95** (was 86), frozen **145/145**,
`verify-build-bundle.py` exit 0 all sections PASS (ledger 42 invariants / 95 witnesses,
`two_way_total: true`, `committed_owner_trust_anchor_fixture_only: true`). Driver re-ran all
of it plus the r2 trustboot probes (no regression) and the clean-room launcher.

## 6. WHY THIS EXISTS (build-decision challenge — answer all three)

(1) ALREADY-BUILT? The shape is ADOPTED, not invented: Go `crypto/x509` `VerifyOptions`
(roots AND `CurrentTime` are per-call fields; the no-time fallback is the real clock, never
the artifact's own value) + TUF's out-of-band trusted root. Both opened at origin by the
driver (`MBCX-01-BUILD-R2-TRUSTCONTEXT-SWEEP-LOG.md`), and independently by two r2 seats.
Internal shelf: the bridge has pinned anchors but no operator-config anchor loader to lift —
an r2 seat sharpened this with a zero-hit `process.env.*TRUST|ANCHOR|ROOT_KEY` query over
`src/`. Spot-run it. (2) PRODUCT-FIT? Fail-loud governed admission: wrong/absent/fixture
anchor stays red with named errors; nothing walls out a box owner. (3) BIGGER-THAN-THE-BUG?
The driver ruled FOLD; two r2 seats independently agreed; the codex seat dissented and asked
for a design gate. **That dissent is live — attack the ruling if you disagree.**

## 7. Non-claims and OPEN residuals (attack the choices, not just the code)

- **RIDER, flagged with its own red: the wiring FREEZE** (`*_REWIRED_DURING_VERIFICATION`).
  Added beyond the fold spec because snapshot-alone left the gadget poisoning the process
  between doors. Two NEW anchor-class error codes per authority; the single
  `ACTIVATION_UNAUTHENTICATED` code was deliberately NOT fragmented. A reviewer may contest
  that "rewired" earns its own name.
- **In-process code is out of scope** (T2 operator boundary): operator wiring remains a
  process global that in-process code may change BETWEEN verifications.
- **NEW TIME DEPENDENCE:** witness `ba28` resolves its anchor from the OS path with no
  injected instant and judges at the real clock — it WILL go red when the committed fixture
  manifest's window closes (`not_after` 2027-08-13). Correct refusal, but a previously
  time-independent suite is now time-dependent.
- **NOT DONE, deliberately:** the "inert bytes or verified immutable model" boundary
  (exact built-in container enforcement on manifests/custody). Strict parse was scoped to the
  ANCHOR DOCUMENT only (duplicate members, NaN/Infinity), because manifests and custody
  arrive as Python objects through the API, not as files.
- **Packaging:** `mbcx01_build_integration.py` reclassified `BUILD_MODULES` →
  `BUILD_FIXTURE_SUPPORT` in `verify-build-bundle.py` (classification only).
- **NOT VERIFIED by the fold:** that no consumer OUTSIDE this lane calls
  `authenticate_production_activation` (its signature now requires `context`).
- Unchanged and still open: BUILD A binds custody digests not documents; accumulate-then-refuse
  ordering; deferred exactness SUITE execution; `mbcx01_build_win32.py` unexecuted with its
  flagged `ProcessTelemetryIdInformation` ordinal; no production ceremony has occurred.

## 8. Sweep lane (every seat)

SWEEP APPLIES TO: the verifier-context model (Go `VerifyOptions` / TUF / SLSA), clock and
freshness handling in verification, fixture-vs-production key separation (e.g. CWE-321 and
the vendor literature on test keys in trust stores), and any standards claim in your own
findings. Run your OWN web sweep — it is not automatic.
DELIVERABLE: a SWEEP LOG — exact queries · what you OPENED with URL + deciding section ·
what changed/confirmed · why you stopped.
LABELS: SEARCHED / RECALLED / UNSEARCHED(+reason: NOT-LOAD-BEARING /
SETTLED-BY-PINNED-BYTES / COULD-NOT / DID-NOT) — every prior-art / standards-bearing finding
carries exactly one.
CONSEQUENCE: an UNSEARCHED or RECALLED finding cannot be the deciding GO on a
prior-art/standards claim; a round where no seat swept such a claim is INCOMPLETE.
HONEST OUT: if you cannot reach the web this session, say so in one line — a
seat-capability report, not a discharge.

## 9. Driver's own search log (ANTI-DRIFT §7 required field)

- 2026-08-14, `moonwalker_http_fetch`, `raw.githubusercontent.com/golang/go/master/src/crypto/x509/verify.go`
  OPENED (ranged) — `isValid(..., opts *VerifyOptions)` with `now := opts.CurrentTime; if
  now.IsZero() { now = time.Now() }`, and `Verify` builds chains "to a certificate in
  `opts.Roots`". PRIMARY: roots AND time are per-call verifier-supplied; the fallback is the
  real clock, never the artifact's value. This is the model the fold implements.
- 2026-08-14, `moonwalker_http_fetch`,
  `raw.githubusercontent.com/theupdateframework/specification/master/tuf-spec.md` OPENED
  (ranged, §Update the root role) — "a good, trusted copy of this file was shipped … using an
  out-of-band process"; new root must be signed by a threshold of keys in the ALREADY-TRUSTED
  root; rollback check requires exactly N+1. PRIMARY.
- 2026-08-14, `slsa.dev/spec/v1.2/verifying-artifacts` §Step 1 OPENED (ranged) — verify the
  envelope signature "using the roots of trust", the verifier's own configured roster. PRIMARY.
- Internal shelf: `git grep` over bridge `src/` for `trust anchor|pinned owner|SPKI|
  preconfigured root` → compile-time pins only (RFC-7469 SPKI `run-ca.ts:81`, per
  `docs/fips-crypto-inventory.md`), no operator-config loader to adopt. An r2 seat's sharper
  `process.env.*TRUST|ANCHOR|ROOT_KEY` query returned ZERO hits.
- CWE-321 (hard-coded cryptographic key) was cited by the codex seat as the footgun class for
  the committed fixture key; the driver did NOT open cwe.mitre.org — **RECALLED**, and
  load-bearing on nothing: the deciding evidence is the executed byte.
- Driver executed the packet's own attacks pre-dispatch: the full fixture-isolation probe at
  the pin (all six classes refuse by name, fixture lane green), the r2 trustboot probes (no
  regression), BUILD 95/95, frozen 145/145, bundle exit 0, clean-room COMPLETE.

## 10. Omission attack (≥1 seat, all seats welcome)

What did this fold not name? Attack the un-named set: context construction paths not covered
by the probe; the freeze's failure modes (exception, re-entrancy, threads, nested doors);
whether any door reads a caller object BEFORE resolving the context; the ceremony fixture's
in-memory keypair generation (it changes per run — does anything depend on stability?);
`verify-build-bundle.py`'s own new checks (are they falsifiable, or do they merely assert?);
the ledger's two-way totality claim; and whether the reclassification of the integration
module hides anything from a gate. Also ask: is any finding-class here a TAR-PIT (theater /
unbounded / wholesale-closeable) — name the disposition, don't grind.

## 11. Blind round

Sealed, independent first pass. This packet carries no driver recommendation and no other
seat's r3 findings.
