# MBCX-01 BUILD acceptance council packet — r4 (whole-instrument validity round on current bytes)

Packet prose is a pointer map, not evidence — byte-check it.

ROUND LEDGER: council round 4 (r1: NO-GO, NO-GO, GO-WITH-FIXES · r2: GO-WITH-FIXES, GO-WITH-FIXES, GO-WITH-FIXES · r3: INCOMPLETE at 2/3 — one NO-GO later ruled to rest on an out-of-model premise, one seat capability report; record: `MBCX-01-BUILD-ADVERSARY-PREMISE-CORRECTION-2026-08-14.md`) · codex rounds 0 of 2

## 0. Seat priming and what this round is

You are one Moonwalker council seat reviewing the MBCX-01 production BUILD (CODE-class,
executable). Operate under the role-prime card you have already received: read-only reviewer;
probes yes, fixes no; sealed from the other seats.

**This is a scientific-validity review, not a security review.** The MBCX-01 design of record
carries no threat model. Verify that yourself — it is one command from the repository root:

```
grep -niE "threat model|adversary|attacker|untrusted|api-caller|hostile" \
  MBCX-01-EXPERIMENT-DESIGN-r9.md MBCX-01-R13-CLOSURE-ARCHITECTURE.md \
  MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md
```

Zero hits (driver re-ran 2026-08-15). The seventeen invariants I01–I17 are a validity device:
each row's falsification column describes **the experiment producing a wrong result about
itself** — a non-member candidate rehashed into the retained set, a scorer graph substituted
across episodes, fixture material counted as real evidence, a stale trust root silently
accepted, a result labelled PASS that no suite execution produced. The question this round
answers: **can this instrument, as built at the pinned commit, produce a false scientific
result that its own verifier would accept?** MBCX-01 has no network service, no production
runtime, and no external submitter; every caller of these modules is the harness and its own
test suites. Findings that require an actor already running code inside the verifier's process
are recorded residuals under the standing tamper-evidence ceiling (`DESIGN-SHELF-MAP.md` §1)
and are not this round's subject — the premise-correction file above is the full record.

Repository: `<repo>-build`
(branch `codex/mbcx01-production-build`). There is no git remote; the committed
`MBCX-01-OPEN-ISSUES.json` is the tracker.

## 1. Verdict contract

First line of your verdict: **GO / GO-WITH-FIXES(class) / NO-GO** (code artifact — no round
call token). Then: evidence read (`path:line`), your SWEEP LOG, findings each labelled
EXECUTED or READ-ONLY, residual risks, and the fix class if any. Deliver the entire verdict
in-thread. A finding names the invariant row (I01–I17) or the module surface it lands on.

## 2. Canonical bytes (path@sha pins)

Everything is reviewed at commit **`4c7056e524b16a8b0395d8853f71e4a9ac6982fc`** (branch head,
2026-08-15). Read at the pin; if you read the working tree, say so and confirm it matches.

Governing design (frozen, r13.2 CONFIRMED 3/3 — not under review, not editable):
- `MBCX-01-EXPERIMENT-DESIGN-r9.md` · `MBCX-01-R13-CLOSURE-ARCHITECTURE.md` ·
  `MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md` (§1 rule, §3 authority modes, §6 completion)

BUILD under review (the instrument):
- `mbcx01_build_trust_anchor.py` — `OwnerTrustAnchor`, `ProductionVerifierContext`,
  `configure_production_verifier_context`, `resolve_production_verifier_context`,
  `committed_fixture_key_material`, `strict_json_document`, `strict_signature_carrier_ok`
- `mbcx01_build_measurement_authority.py` — `evaluate_production_measurement`
- `mbcx01_build_state_authority.py` — `verify_production_scorer_input`
- `mbcx01_build_exactness_authority.py` — binding-only discipline,
  `AUTHORITY_BINDING_ONLY_SUITE_NOT_EXECUTED`
- `mbcx01_build_etw_consumer.py` — the measurement stream half: session create/configure/
  consume/teardown, the constants table (every `FLAGGED` value), loss/unavailability posture
- `mbcx01_build_win32.py` — `collect()`, the consumer seam, the frozen 96/144-byte Job ABI
- `mbcx01_smoke_cell.py` · `run-smoke-cell.ps1` · `MBCX-01-BUILD-SMOKE-RUNBOOK.md`
- Suites: `test_mbcx01_build_measurement.py` · `test_mbcx01_build_state.py` ·
  `test_mbcx01_build_integration.py` (114 tests) · frozen `test_mbcx01_r13_*.py` (145 tests)
- Verifiers: `verify-build-bundle.py` (seven sections; two-way witness↔invariant ledger) ·
  `verify-build-pinned.ps1` · `MBCX-01-BUILD-REPAIR-LEDGER.json` · `MBCX-01-BUILD-PIN-MANIFEST.json`

Banked witness runs (committed evidence; two are stale, named in §8):
`MBCX-01-BUILD-TRUSTBOOT-{RED,GREEN}-WITNESS-RUN-2026-08-14.txt` ·
`MBCX-01-BUILD-FIXTUREISO-{RED,GREEN}-WITNESS-RUN-2026-08-14.txt` ·
`MBCX-01-BUILD-FIXTUREKEY-{RED,GREEN}-WITNESS-RUN-2026-08-14.txt` ·
`MBCX-01-BUILD-ETW-CONSUMER-{RED,GREEN}-WITNESS-RUN-2026-08-14.txt` ·
`MBCX-01-BUILD-FREEZE-REVERT-WITNESS-RUN-2026-08-14.txt`

## 3. Immutable truths / invariants

1. The r13.2 experiment design is frozen and CONFIRMED. Zero frozen files may change; the
   frozen suite (145 tests) must stay green. Estimand, n=768, route policy and inference are
   settled — proposals to reopen them are out of scope for this round.
2. The matrix rule (`MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md` §1): every row is one fact in
   two places; the join is valid only when the listed equality is mechanically reproduced from
   independently admitted inputs; every row carries a positive and a falsification witness.
   Consumers of each invariant: the two authorities, the exactness authority, the integration
   layer, and `verify-build-bundle.py`'s ledger section — a row honoured in one consumer and
   not another is a finding.
3. Authority modes (§3): `FIXTURE_ONLY` may exercise parsers, signatures, reducers and join
   logic and cannot create an experiment-eligible score or a physical pass. `PRODUCTION`
   requires an independently configured trust root the signer cannot edit. No committed
   fixture implements production mode.
4. Readiness is `BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`: no ceremony has
   happened, no production root exists, nothing scientific has run, zero spend, zero provider
   calls. The measurement half has never executed an instruction against a live ETW session.
5. Unverifiable platform constants are FLAGGED in source and fault loudly rather than degrade
   to a number. The elevated smoke run (owner action, separately authorized) is the only thing
   that can settle them; this round does not run it.

## 4. Claims to attack (construct-the-bypass)

For every claim: name the byte or the executed sequence that makes it false, or name the
residual. Anchors are symbols at the §2 pin.

1. **Q1 — retained-set integrity (I01/I02).**
ADVERSARY: internal-consistency — two of our own units disagreeing about which candidates are real.
REACHES IT VIA: the harness's own admission and join paths, exercised by probe input.
Claim: a self-consistent candidate outside the 768 retained set cannot be rehashed into
admission; a legal same-cut state with one obligation changed cannot join. Probe the
join logic in the state/measurement authorities and the frozen reducers.

2. **Q2 — episode/scorer binding (I05/I10).**
ADVERSARY: internal-consistency — a scorer graph or ledger from one episode counted under another.
REACHES IT VIA: receipt and ledger structures supplied to the authorities by the harness.
Claim: `ScenarioOutcomeReceiptV2`'s episode hash and six ordered bindings make a same-scenario
substitution from another episode non-admissible, and naked bits cannot stand in for a
derived partition. Construct a substitution the equality checks would admit.

3. **Q3 — fixture cannot become production (I13/I14/I16, §3).**
ADVERSARY: internal-consistency — test material counting as real evidence.
REACHES IT VIA: the ordinary public constructors and the `MBCX01_BUILD_OWNER_TRUST_ANCHOR`
OS-config path — no in-process object surgery.
Claim: the committed fixture anchor, the committed fixture private key
(`committed_fixture_key_material`), and any fixture-marked document are refused by name at
all three production doors on both wiring paths, while the fixture lane
(`require_production=False`) stays green. Probe with fresh documents through
`configure_production_verifier_context` / `resolve_production_verifier_context` and the
authorities' entry points.

4. **Q4 — validity at the verifier's clock.**
ADVERSARY: internal-consistency — a stale root or expired window silently counting.
REACHES IT VIA: manifest and anchor validity fields evaluated at admission.
Claim: trust-root validity is judged at the verifier's clock, never at a date carried inside
the artifact; an expired manifest refuses by name. (Known dated behaviour: witness `ba28`
judges at the real clock and will correctly refuse after 2027-08-13 — disclosure, not a bug.)

5. **Q5 — the ETW consumer's honesty posture (new surface, never council-reviewed).**
ADVERSARY: internal-consistency — the measurement stream reporting a number where evidence is absent.
REACHES IT VIA: the record stream, lifetime roster, capability record and loss counters the
consumer hands to `collect()`.
Claim: every unavailable source, counter loss (`EventsLost`/`LogBuffersLost`/
`RealTimeBuffersLost`), unattached seam, missing PMC extended data, absent lifetime root, or
capability contradiction is a named fault or UNAVAILABLE evidence — never a zero, never an
estimate, never a partial roster presented as complete. Probe `mbcx01_build_etw_consumer.py` and
the `collect()` seam in `mbcx01_build_win32.py`: find one path where degraded input yields
a signable count. Also probe the three repaired defect sites (capability record shape,
`configure()` key handling, the CSwitch attachment blob — now
`3d6fa8d1-fe05-11d0-9dda-00c04fd7ba7c` / Type 36) for neighbours the repair did not cover.

6. **Q6 — FLAGGED constants discipline (new surface).**
ADVERSARY: maintainer — a future edit or platform revision landing on an unverified value.
REACHES IT VIA: the constants table in `mbcx01_build_etw_consumer.py`.
Claim: every constant Microsoft does not publish is FLAGGED in source, used only where a
wrong value faults loudly, and listed in the smoke runbook's verification set. Driver's
sweep (§10) confirmed `TracePmcEventListInfo=8` / `TracePmcCounterListInfo=9` at the
Microsoft enum page and confirmed `EVENT_HEADER_EXT_TYPE_PMC_COUNTERS` is named but not
numbered on its page. Check the FLAGGED set is complete: an unflagged unpublished constant
is a finding.

7. **Q7 — exactness cannot self-author (I16).**
ADVERSARY: internal-consistency — a PASS label with no execution behind it.
REACHES IT VIA: exactness receipts and evidence records presented to the authority.
Claim: a binding-only exactness result cannot present as suite-executed PASS
(`AUTHORITY_BINDING_ONLY_SUITE_NOT_EXECUTED`); the per-witness suite runner does not exist
yet and nothing in the bytes claims otherwise (tracked: `MBCX01-EXACTNESS-SUITE-RUNNER-UNBUILT`).

8. **Q8 — the witnesses discriminate (suite honesty).**
ADVERSARY: author-blind-spot — a green that cannot fail on the class it names.
REACHES IT VIA: the committed suites and the two-way repair ledger.
Claim: the 44-invariant / 114-witness ledger in `verify-build-bundle.py` maps every closed
class to a probe that goes red on the pre-fix bytes. Pick at least one witness per authority,
break the implementation deliberately (locally, revert after), and confirm the witness goes
red. A witness that stays green under a deliberate break is a finding.

9. **Q9 — the three named fixture-key gaps (tracked, put to this round on purpose).**
ADVERSARY: maintainer — a ceremony or future edit stepping into a gap the fold names.
REACHES IT VIA: the ceremony path in `MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md` §3 step 0.
From `MBCX01-FIXTUREKEY-NAMED-GAPS`: (1) `FIXTURE_NON_ANCHOR_PRIVATE_KEY_PEM` is not in the
derived known-key set; (2) a committed test SIGNING key copied into a production trust-root
manifest is refused only via `MEASUREMENT_CUSTODY_EVIDENCE_INVALID`, not as committed
material; (3) the OS-config path raises on a committed-key anchor rather than returning a
named code. Rule each: is the gap reachable in the ceremony as written? If yes, it needs a
close before the ceremony; if no, confirm the disclosure is accurate and sufficient.

## 5. Red witnesses per closed class

Every closed class carries a banked discriminating probe, red on pre-fix bytes, green after —
committed in the witness-run files listed in §2 and mapped two ways in
`MBCX-01-BUILD-REPAIR-LEDGER.json` (checked every run by `verify-build-bundle.py`'s ledger
section: 44 invariants / 114 witnesses, `two_way_total: true`). Re-run them yourself — §6.
The trust-boot probes, fixture-key probe and fixture-isolation probe are committed as
`mbcx01_build_trustboot_probe.py` · `mbcx01_build_fixturekey_probe.py` ·
`mbcx01_build_fixtureiso_probe.py`.

## 6. Executable-falsification lane — all seats

The load-bearing claims are executable, so reading is the floor, not the review:
- Re-run the banked witnesses: `python -m unittest test_mbcx01_build_measurement
  test_mbcx01_build_state test_mbcx01_build_integration` (expect 114 OK) and the frozen
  `test_mbcx01_r13_*` set (expect 145 OK); `python verify-build-bundle.py` (expect exit 0,
  seven sections PASS).
- Construct and run at least one fresh probe of your own per question you rule on — your own
  input, not the author's. Label every finding and your verdict EXECUTED or READ-ONLY. A
  READ-ONLY verdict cannot be the deciding GO on this artifact.
- Do not start an ETW session, create a Job Object, set `MBCX01_BUILD_ALLOW_PHYSICAL`, or run
  `run-smoke-cell.ps1` — the physical smoke run is a separately authorized owner action. The
  pure layer and static ABI (`verify_struct_layout()`) run fine unelevated and are in scope.

## 7. Omission attack

At least one seat: probe the un-named set. What can make this instrument produce a false
result that no I01–I17 row and no question above names? Candidate surfaces the author may
have under-weighted: the frozen-suite/BUILD seam (does any BUILD path bypass a frozen
equality?), the pin manifest's coverage (does `verify-build-pinned.ps1` authenticate every
load-bearing file?), unicode/canonicalisation in `strict_json_document`, the smoke driver's
evidence-banking path, duplicate-witness identity in the repair ledger. Name what is missing,
or state that the falsification surface is covered and why.

## 8. Non-claims

1. **No claim the consumer works.** The measurement half has never executed against a live
   session; a green suite means the logic is right if the platform behaves as documented.
   Seven platform facts are settled only by the elevated smoke run (tracked:
   `MBCX01-SMOKE-RUN-OUTSTANDING`).
2. **No security boundary against in-process actors is claimed.** Tamper-evident, not
   tamper-proof; the standing ceiling governs (premise-correction file). Verified exclusion:
   the sweep in §4/§7 still covers these surfaces for *validity* (fault-vs-number), which is
   the property this round does test.
3. **No exactness-execution claim.** The suite runner is unbuilt and labelled so (Q7).
4. **No completeness claim beyond the enumerated set**: 114 + 145 tests, 44 ledger rows, the
   named witness banks — totality is not claimed; the bundle's green means "no failure seen in
   the shapes this net covers".
5. **Two committed evidence files are stale, named here so nobody reads them as current:**
   `MBCX-01-BUILD-FIXTUREISO-GREEN-WITNESS-RUN-2026-08-14.txt` (its P2 block names
   `*_REWIRED_DURING_VERIFICATION`, deleted by the freeze revert — 5 marker lines still in the
   bank, counted 2026-08-15) and `MBCX-01-BUILD-COMPLETION-HANDOFF.md` (predates the last five content commits;
   carries a superseded banner). Compare against current bytes, not those banks.

## 9. Why this exists (build-decision challenge — answer before the mechanism review)

ALREADY-BUILT: The instrument is bespoke by necessity — no shelf module measures retired
instructions per Job-scoped process tree over ETW kernel PMC with signed evidence semantics.
Driver's internal sweep (§11, run 2026-08-15): no ETW/PMC consumer exists anywhere in the
three Moonwalker repos; trust-anchor and fixture-gating shapes exist in the bridge repo
(`runtime-trust.ts`, `enrollment-fingerprint.ts`, seal-chain custody) and the fold's own-key
walk adopted the bridge's strict-parse pattern; prior art is cited per fold (Go
`crypto/x509 VerifyOptions`, TUF out-of-band root, MITRE CWE-1291). Seats: spot-run at least
one §11 query yourself.
PRODUCT-FIT: This is the experiment's measurement instrument. The posture is fail-loud
mirror-not-cop: every unverifiable fact faults or reports UNAVAILABLE; nothing prevents,
everything evidences. It serves the scientific-validity need (a result the owner can trust),
not a completeness or prevention ambition.
BIGGER-THAN-THE-BUG: The r2 wiring-freeze rider was exactly this defect — machinery bigger
than any defect it addressed, built against an out-of-model actor — and it was reverted
(`MBCX-01-BUILD-FREEZE-REVERT-WITNESS-RUN-2026-08-14.txt`, byte-identical trustboot probe
before/after). Rule whether anything else in the current bytes is machinery without a DoR row
behind it.

## 10. Search log (the driver's own sweep, run 2026-08-15)

Tool: Moonwalker web_search (duckduckgo) + web_fetch, primary pages opened:
1. Query: `EVENT_HEADER_EXTENDED_DATA_ITEM ExtType PMC_COUNTERS site:learn.microsoft.com` →
   opened `learn.microsoft.com/.../ns-evntcons-event_header_extended_data_item` (SEARCHED):
   the page names `EVENT_HEADER_EXT_TYPE_PMC_COUNTERS` and publishes no numeric value for any
   ext type — confirms the in-source FLAGGED posture for `0x0008`.
2. Query: `TRACE_QUERY_INFO_CLASS TracePmcEventListInfo TracePmcCounterListInfo` → opened the
   MicrosoftDocs sdk-api source of `ne-evntrace-trace_query_info_class` (SEARCHED):
   `TracePmcEventListInfo:8`, `TracePmcCounterListInfo:9` — the two configure ordinals the
   consumer uses are published and match. Also present: `TraceMaxPmcCounterQuery:22`,
   `TracePmcCounterOwners:25` (Win10 21H2+) — relevant to the counter-ownership smoke check.
3. Query: `"Microsoft-Windows-Kernel-Process" provider "22FB2CD6" site:learn.microsoft.com` →
   zero results (recorded as a pointer, not proof of absence) — consistent with the in-source
   claim that the provider has no Microsoft page and stays FLAGGED until the smoke run.
Stopped because: the three load-bearing platform-fact classes this round can act on were each
opened at their origin; the remaining platform facts are execution-settled only (smoke run),
where no further reading changes anything.

## 11. Internal-shelf log (the driver's own internal sweep, run 2026-08-15)

QUERIES: `grep -rilE "trust[_ -]?(anchor|root)"` · `grep -rilE "fixture[_ -]?only|fixture[_ -]?mode"` · `grep -rilE "EVENT_TRACE|TracePmc|CSwitch|ProcessTrace"` · `grep -rilE "adversarial[_ -]?witness|two[_ -]?way.*(witness|ledger)|invariant[_ -]?matrix"`
REPOS: agentvault-mcp-bridge (`src/`) · Photon (`crates/`) · Gravity (`src/`) — all three, no exclusions.
OPENED: bridge `runtime-trust.ts` / `enrollment-fingerprint.ts` / `muninn-commitment.ts` (trust-root and identity shapes — adopted at the r1/r2 folds, cited in their sweep logs); Photon `crates/aruna-jmap/src/transport.rs` (the only sibling fixture-mode hit — a transport test fixture, not an authority gate; not adopted, different problem); ETW/PMC query and witness-matrix query returned zero files in all three repos — nothing to adopt, the consumer is genuinely first-of-kind here.
STOPPED: the four problem shapes of this round (trust admission, fixture gating, ETW consumption, two-way witness ledger) each either resolved to an already-adopted bridge pattern or returned empty across all three repos; further queries would re-cover the same mechanism space. The BUILD's own fuller log: `MBCX-01-BUILD-SHELF-LOG.md`.

## 12. Seat SWEEP lane (the seats' own sweep)

SWEEP APPLIES TO: any claim resting on prior art, a standard, a vendor's documented behaviour
(ETW/PMC semantics, Ed25519 carrier rules, JSON strictness, Go/TUF trust-root patterns), or a
footgun class — before you bless or refute it, go look with your own queries and sources.
DELIVERABLE: a SWEEP LOG in your verdict — exact queries · what you OPENED (URL + the section
that decided it) · what it changed or confirmed · why you stopped.
LABELS: every prior-art or standards-bearing finding carries exactly one of SEARCHED /
RECALLED / UNSEARCHED (UNSEARCHED carries its reason: NOT-LOAD-BEARING · SETTLED-BY-PINNED-BYTES ·
COULD-NOT · DID-NOT).
CONSEQUENCE: an UNSEARCHED or RECALLED finding cannot be the deciding GO on a claim resting
on prior art or a standard; a round in which no seat swept such a claim is incomplete.
HONEST OUT: if you genuinely cannot reach the web this session, say so plainly in one line —
a capability report, not a discharge.

## 13. Re-review trigger

A fold that changes an authority's admission semantics, a door contract, an invariant
consumer, or the consumer's fault/unavailability posture ⇒ a fresh council round on the new
bytes. Localized leaf fixes (naming, message text, test-body edits) ⇒ the codex-CLI gate
covers them, no re-round. Any finding that requires a new subsystem to close re-enters the
design gate and stops at the owner.

## 14. Driver pre-dispatch execution (the packet's own probes, run before sending — 2026-08-15, at the §2 pin)

- Premise: threat-model grep over the three governing docs → 0 hits (run today, §0).
- BUILD suites 114/114 OK · frozen suites 145/145 OK (run today).
- `verify-build-bundle.py` exit 0 — all seven sections PASS, ledger 44/114 `two_way_total`,
  `no_production_activation` all-false, readiness `BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED` (run today).
- Clean-room `verify-build-pinned.ps1 -Commit 3527f510… -ManifestBlob 23009028…` →
  `PINNED RECONSTRUCTION COMPLETE` (run today; the four commits after the manifest pin are
  records/ledger files, not BUILD source — confirm with `git log --stat 331f25b..HEAD`).
- Committed probes re-run today on current bytes: trustboot, fixture-key, fixture-isolation —
  refusals fire by name (transcripts in the driver's session log; the committed banks remain
  the durable record, with the two stale files named in §8).
- Q1/Q2/Q3/Q4/Q7 are exercised by the suites' falsification-oriented witnesses re-run above; Q5/Q6 are
  exercised by the ETW witness set (bw29–bw47) re-run above; Q8's deliberate-break step and
  Q9's ceremony-reachability ruling are left to seats by design — the author breaking his own
  suite and grading it is the blind spot this council exists to remove.
