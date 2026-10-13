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

# MBCX-01 BUILD acceptance council packet — r1

Packet prose is a pointer map, not evidence — byte-check it.

## 0. Seat priming, seal, and pins

You are one Moonwalker council seat reviewing the MBCX-01 production BUILD (CODE-class,
executable). Read `<vault>` first and
operate under it: read-only adversarial reviewer; probes yes, fixes no. Maintain the
lateral seal — do not inspect any other seat's r1 output. Your own longitudinal MBCX lane
context is allowed and must be labeled.

Repository: `<repo>-build`
(branch `codex/mbcx01-production-build`).

- Review head: the dispatch message names this packet's own commit; code pins below are explicit.
- Content-final BUILD commit: `2fd38972ca40820e5e4ac049b18ca480f29392c8`
- BUILD pin manifest blob: `5f5cd20b0fc526edca81bd285920ee52bf374b36` (committed `df5bbee1`)
- Governing r13.2 commit (frozen, unchanged): `d97d654e21918450994cfddb5a53dc5da2e962bb`
- Commission: `MBCX-01-PRODUCTION-BUILD-SENIOR-HANDOFF-r13.2.md` (in-repo) — authorized by
  the 3/3 CONFIRMED r13.2 council (verdicts banked at `91329b2`).
- Read: `MBCX-01-BUILD-COMPLETION-HANDOFF.md` (what is claimed) ·
  `MBCX-01-BUILD-DESIGN-NOTES.md` (architecture + folds §4) · the six `mbcx01_build_*.py`
  modules + three `test_mbcx01_build_*.py` suites · `MBCX-01-BUILD-REPAIR-LEDGER.json` ·
  `verify-build-bundle.py` · the two trust-root schema/fixture pairs · the three banked
  witness-run transcripts.

Authorized execution: deterministic read-only reconstruction, the committed suites, and
fresh no-paid adversarial probes. ⛔ Do NOT run the experiment, provider/model calls, real
Job/ETW collection (`mbcx01_build_win32.collect` is double-gated — leave the gates unset),
a signing ceremony, or any spend.

Verify the clean-room reconstruction yourself (from the repo root):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\verify-build-pinned.ps1 -Commit 2fd38972ca40820e5e4ac049b18ca480f29392c8 -ManifestBlob 5f5cd20b0fc526edca81bd285920ee52bf374b36
```

## 1. Verdict contract

Return, in-thread, one report: **GO / GO-WITH-FIXES(class) / NO-GO** · evidence read
(path:line@sha) · SWEEP LOG (queries · opened · why stopped; labels
SEARCHED/RECALLED/UNSEARCHED with reasons) · findings labeled **EXECUTED / READ-ONLY** ·
residual risks · fix CLASS if any. Executable artifact: a READ-ONLY verdict cannot be the
deciding GO; run the banked red witnesses and construct fresh adversarial inputs of your
own.

### Re-review trigger

Any finding that ripples architecture / interface / security reconvenes the council; leaf
edges go to the codex gate.

### Canonical bytes (read at these pins)
- `mbcx01_build_state_store.py@2fd38972ca40820e5e4ac049b18ca480f29392c8`
- `mbcx01_build_state_adapter.py@2fd38972ca40820e5e4ac049b18ca480f29392c8`
- `mbcx01_build_state_operator_b.py@2fd38972ca40820e5e4ac049b18ca480f29392c8`
- `mbcx01_build_state_authority.py@2fd38972ca40820e5e4ac049b18ca480f29392c8`
- `mbcx01_build_windows_producer.py@2fd38972ca40820e5e4ac049b18ca480f29392c8`
- `mbcx01_build_measurement_authority.py@2fd38972ca40820e5e4ac049b18ca480f29392c8`
- `mbcx01_build_exactness_authority.py@2fd38972ca40820e5e4ac049b18ca480f29392c8`
- `mbcx01_build_win32.py@2fd38972ca40820e5e4ac049b18ca480f29392c8`
- `mbcx01_build_integration.py@2fd38972ca40820e5e4ac049b18ca480f29392c8`
- `test_mbcx01_build_state.py@2fd38972ca40820e5e4ac049b18ca480f29392c8` (+ `_measurement`, `_integration` same pin)
- `MBCX-01-BUILD-REPAIR-LEDGER.json@2fd38972ca40820e5e4ac049b18ca480f29392c8`
- `verify-build-bundle.py@2fd38972ca40820e5e4ac049b18ca480f29392c8`
- `MBCX-01-BUILD-COMPLETION-HANDOFF.md@e6f7bdb` (claims under review)
A working-tree file at the same path may have moved off the pin — a seat reading the tree
must say so and confirm it matches the pin.

## 2. Immutable truths

- **T2 ceiling (settled — not a question):** a same-host admin / SYSTEM / box-controlling
  actor is the box owner; on-box walls against them are theater. This BUILD is
  tamper-EVIDENT machinery (`DESIGN-SHELF-MAP.md` §1 owns the ceiling). Do not propose
  closing box-owner families.
- The frozen r13.2 subjects are byte-frozen; every BUILD artifact is a versioned sibling.
  145/145 frozen tests + 61 governed witnesses must remain green and unweakened.
- Fixture evidence must never create production or scientific authority; absent production
  roots/hardware, admission stays red with the honest sentinels.
- The r13.2 handoff's fixed design decisions (single writer, six-call episode, 768 cohort,
  suspended-create discipline, separate state/measurement roots) are inputs, not open
  questions.

## 3. Claims to attack (construct the bypass; run it; name the residual)

1. **C1 — the subtractive sentinel discharge is non-weakening.**
`verify_production_scorer_input` runs the FROZEN `validate_scorer_input` both modes and may
remove ONLY `{STATE_AUTHORITY_UNAVAILABLE}` ∪ its byte-reproduced cascade set
`{A0_PACKET_INVALID, I02_INVARIANT_INVALID}`, and only on fully-clean, byte-bound V2
authority; any error the fixture-mode frozen run reports survives.
ADVERSARY: api-caller — a contractually-untrusted caller supplying scorer inputs and V2
receipts crafted to launder a defect through the discharge set.
REACHES IT VIA: data
ADMITTED AT: mbcx01_build_state_authority.py:verify_production_scorer_input
Attack: construct a scorer input the frozen fixture-mode path would REJECT whose defect
hides inside the discharged cascade names, paired with a clean V2 receipt. It must not
admit.

2. **C2 — fixture/self-authored evidence cannot clear production admission.**
ADVERSARY: api-caller — supplies relabeled fixture envelopes/receipts, self-authored
roots, or `production_ready`-flipped committed manifests.
REACHES IT VIA: data
ADMITTED AT: mbcx01_build_measurement_authority.py:evaluate_production_measurement
Attack: relabel/rehash/re-sign fixture evidence any way you like (state and measurement
sides both); flip the committed manifests on disk; nothing may admit without injected
ceremony-bound custody evidence and matching roots.

3. **C3 — crash windows cannot mint.**
ADVERSARY: our-own-automation — our own writer process dying before/mid/after commit and a
later process reading the partial state.
REACHES IT VIA: data
ADMITTED AT: mbcx01_build_state_store.py:commit_transition
Attack: drive the crash points; hand-build receipts over PENDING/BROKEN terminals with all
local hashes repaired; verify (including from a FRESH process via `store_path`) — nothing
may verify clean.

4. **C4 — anti-replay anchors are durable, not derived.**
ADVERSARY: api-caller — replays a valid receipt across scope/scenario/run/subject/txn with
outer hashes and signature re-made.
REACHES IT VIA: data
ADMITTED AT: mbcx01_build_state_authority.py:_anti_replay_errors
Attack: per-axis replay against the durable journal anchors; also attack operator-B
independence (poison a finalizer; byte-compare gate must catch it).

5. **C5 — custody separation is mechanical.**
ADVERSARY: api-caller — a key custodian (bounded, contractually-untrusted role, NOT the box
owner) submitting manifests/custody documents that self-authorize: signer key in the
editor-approval chain, colliding roles, revoked/expired roots, forged custody digests.
REACHES IT VIA: data
ADMITTED AT: mbcx01_build_measurement_authority.py:validate_production_trust_root_manifest
Attack: each custody axis independently; `CUSTODY_SEPARATION_INVALID` /
`TRUST_ROOT_REVOKED` / `TRUST_ROOT_VALIDITY_EXPIRED` / digest mismatch must fire before any
grid analysis.

## 4. Red witnesses per closed class (banked; re-run them)

`MBCX-01-BUILD-A-RED-WITNESS-RUN-2026-08-14.txt` (24 red @ `6c3bc2a` skeletons) ·
`MBCX-01-BUILD-B-RED-WITNESS-RUN-2026-08-14.txt` (44/44 red) · green banks with
DISCRIMINATION-PROBE transcripts (`…-A-GREEN…`, `…-B-GREEN…`) ·
`MBCX-01-BUILD-INTEGRATION-RUN-2026-08-14.txt` §1a–1c (fold reds ba26–ba28, including the
two-stage discriminating red for the anti-replay fold). Suites: 76/76 BUILD + 145/145
frozen at `2fd38972`.

## 5. WHY THIS EXISTS (build-decision challenge — answer all three)

(1) ALREADY-BUILT? `MBCX-01-BUILD-SHELF-LOG.md` records the three-repo sweep: patterns
adopted (Gravity slice0c containment discipline, Photon writer-gate/one-door, bridge
record-before-effect, EvidenceSigner shape) and the finding that no shelf artifact supplies
the exact state-owner receipt, six-call join, or signed Windows evidence producer —
spot-run its queries. (2) PRODUCT-FIT? fail-loud governed measurement: absent authority
stays red; nothing here prevents a box owner from anything (mirror-not-cop). (3)
BIGGER-THAN-THE-BUG? this is the commissioned BUILD of two prerequisites the r13.2 council
converged on 3/3 — not a review-authority invention; the versioned-sibling architecture
was forced by the frozen code (design notes §0/§2 cite the exact lines).

## 6. Non-claims (each swept; exclusions verified or held open)

- No protection against the box owner (T2; see §2). Hygiene present is labeled hygiene.
- A valid signature does NOT assert the OS facts are true (SLSA separation): fixture-signed
  simulated evidence proves verifier conformance only; truth of physical facts arrives at
  the smoke stage under custody-separated production roots. Grep-verified: no BUILD module
  claims otherwise; admission never trusts self-reported success fields it can recompute.
- The per-witness exactness SUITE execution is deferred (spec §3) —
  `verify_production_carrier_exactness` binds identities and refuses relabels; it does not
  bless carrier behavior. OPEN residual, tracked in the spec.
- Trust-root validity uses a deterministic default instant (manifest `published_at`), not
  wall clock — a production runbook must pass the real instant (runbook §3). OPEN residual,
  documented; not claimed closed.
- `mbcx01_build_win32.py` is UNEXECUTED reviewable code; its `ProcessTelemetryIdInformation`
  ordinal is a flagged smoke-stage check (disagreement faults loudly).

## 7. Sweep lane (every seat)

SWEEP APPLIES TO: every prior-art / standards / platform-semantics claim in this packet and in your own findings (SQLite durability, Windows Job/ETW semantics, Ed25519, SLSA authority separation, canonicalization).

Run your OWN web sweep — it is not automatic. Deliverable: a SWEEP LOG in your verdict
(exact queries · what you OPENED with URL + deciding section · what changed/confirmed ·
why you stopped). Labels: SEARCHED / RECALLED / UNSEARCHED(+reason:
NOT-LOAD-BEARING / SETTLED-BY-PINNED-BYTES / COULD-NOT / DID-NOT). Consequence: an
UNSEARCHED/RECALLED finding cannot be the deciding GO on a prior-art/standards claim; a
round where no seat swept such a claim is INCOMPLETE. Honest out: if you cannot reach the
web this session, say so in one line (capability report, not a discharge). Suggested
surfaces: SQLite WAL durability (synchronous=FULL), Windows Job accounting ABI +
TotalTerminatedProcesses, TRACE_QUERY_INFO_CLASS ordinals, ProcessStartKey acquisition,
Ed25519 verification pitfalls, SLSA verification model.

## 8. Driver's own search log (ANTI-DRIFT §7 required field)

- 2026-08-14, moonwalker_http_fetch: `https://sqlite.org/wal.html` §2.3 OPENED — WAL syncs
  per-commit only under `PRAGMA synchronous=FULL`; NORMAL loses power-loss durability ⇒
  store pins WAL+FULL. PRIMARY.
- 2026-08-14, moonwalker_http_fetch:
  `learn.microsoft.com/en-us/windows/win32/api/evntrace/ne-evntrace-trace_query_info_class`
  OPENED — enum extracted: TracePmcEventListInfo=8, TracePmcCounterListInfo=9 (collector
  ordinals CORRECT). PRIMARY.
- Job accounting ABI + TotalTerminatedProcesses semantics: the controlling Microsoft page
  was OPENED independently by both r13.2 browser seats on 2026-08-14 (banked verdicts at
  `91329b2`) and is pinned in MEASUREMENT-CONTRACT-v7; carried as SEARCHED-by-council.
- SLSA v1.2 verifying-artifacts (signature ≠ producer authority): carried from the r13
  prior-art addendum (in-repo, pinned). RECALLED-with-pinned-source.
- Internal-shelf log: `MBCX-01-BUILD-SHELF-LOG.md` — exact grep queries across bridge /
  Photon / Gravity, files OPENED, adopt-or-why-not per row.

## 9. Omission attack (≥1 seat, all seats welcome)

What did the BUILD not name? Attack the un-named set: a footgun class, a standards clause,
an evidence field, an attack surface (e.g. the store file itself as untrusted input to
`ReadOnlyStateStoreView`; unicode/canonicalization edges in canonical_json parity; signer
subprocess boundary) that neither the witnesses nor the non-claims cover. Also ask: is any
finding-class here a TAR-PIT (theater / unbounded / wholesale-closeable) — if so say which
disposition, don't grind.

## 10. Blind round

Sealed, independent first pass. This packet carries no driver recommendation and no other
seat's findings.
