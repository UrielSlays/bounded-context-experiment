# MBCX-01 BUILD acceptance council packet — r5 (the r4 folds, on the folded bytes)

Packet prose is a pointer map, not evidence — byte-check it.

ROUND LEDGER: council round 5 (r1: NO-GO, NO-GO, GO-WITH-FIXES · r2: 3x GO-WITH-FIXES · r3: INCOMPLETE 2/3, its NO-GO later ruled to rest on an out-of-model premise · r4: NO-GO, NO-GO, GO-WITH-FIXES — all EXECUTED, four classes folded since) · codex rounds 0 of 2

## 0. The one thing this round is for

**NORTH STAR: the numbers this instrument produces must be true.** MBCX-01 is a measurement
harness for a scientific experiment. It has no network service, no production runtime and no
external submitter; every caller is the harness and its own tests. The design of record carries
**no threat model** — verify in one command from the repository root:

```
grep -niE "threat model|adversary|attacker|untrusted|api-caller|hostile" \
  MBCX-01-EXPERIMENT-DESIGN-r9.md MBCX-01-R13-CLOSURE-ARCHITECTURE.md \
  MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md
```

⛔⛔ **THE FILTER, AND THE DRIVER WILL APPLY IT TO YOUR FINDINGS.** A finding counts in this round
if, and only if, you can name how it makes the experiment **produce a wrong number, admit wrong
evidence, or refuse right evidence**. State that consequence explicitly on every finding.

Findings that harden against an actor deliberately evading a check — rather than the experiment
fooling itself or an operator's honest mistake — are **out of model** here, and the driver will
rule them out rather than fold them. This is not a hypothetical caution: r1/r2/r3 of this lane
burned three rounds and nine seat-verdicts on a declared untrusted caller that does not exist, and
r4's own fold went one step past the need by closing a re-encoding variant no honest tool produces.
⛔ Do not propose a new machine, engine, subsystem or general mechanism. If your fix is bigger than
the defect, say so and stop — that re-enters the design gate and is the owner's call, not a fold.

⚠ **A NEW RISK THIS ROUND MUST WEIGH, because the folds only ADDED refusals:** a FALSE REFUSAL is
now as dangerous as a false admission. If any fold refuses evidence the real ceremony or the real
smoke run would legitimately present, the experiment cannot run at all. Probe that direction too.

## 1. Verdict contract

First line: **GO / GO-WITH-FIXES(class) / NO-GO**. Code artifact — no round-call token, and skip the
two design questions. Then: evidence read (`path:line`), your SWEEP LOG, findings each labelled
EXECUTED or READ-ONLY **and each carrying its wrong-number / wrong-admission / wrong-refusal
consequence**, residual risks, fix class. Deliver the whole verdict in-thread.

## 2. Canonical bytes (path@sha pins)

Content commit under review: **`fce7b3551d228e91b77814fdb3d3296c3d7ee08b`** (tree head
`7af17752e3a8411cf91088ec404eacc4f12c0270` adds only the regenerated pin manifest). Read at the
pin; if you read the working tree, say so and confirm it matches.

The r4 fold arc is `4c7056e5..fce7b355`. What changed:
- `mbcx01_r13_packets.py` + `mbcx01_r13_measurement.py` — **AMENDMENT-1 to the FROZEN r13.2 layer**
  (owner-ruled 2026-08-15): the canonical world now binds `subject_id` and `owner_role`.
  Record: `MBCX-01-R13-AMENDMENT-1-CANONICAL-WORLD-BINDING-2026-08-15.md`.
- `mbcx01_build_etw_consumer.py` — three classes: SDK constant correction on the live CSwitch path,
  thread start-key binding, drain/loss ordering.
- `mbcx01_build_trust_anchor.py` — key identity from the decoded key; canonical carrier refusal;
  committed-key harvest widened from anchor documents to every committed fixture document.
- `mbcx01_build_measurement_authority.py` · `mbcx01_build_state_authority.py` ·
  `mbcx01_build_exactness_authority.py` — production signing-key refusals by name.
- `mbcx01_build_ceremony_fixture.py` + both BUILD suites — positive lanes moved to in-memory
  generated signing keys (forced: the old positive lanes used the material now refused).
- `verify-build-bundle.py` — `FROZEN_TEST_TOTAL` 145 → 147, declared with its reason.

Governing design (frozen, not under review): `MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md` (§1 rule,
§2 canonical world, §3 authority modes) · `MBCX-01-EXPERIMENT-DESIGN-r9.md` ·
`MBCX-01-R13-CLOSURE-ARCHITECTURE.md`.

Banked witness runs: `MBCX-01-BUILD-ETW-CONSUMER-{RED,GREEN}-WITNESS-RUN-2026-08-15.txt` and the
2026-08-14 set. Ledger: `MBCX-01-BUILD-REPAIR-LEDGER.json` (46 invariants / 125 witnesses).

## 3. Immutable truths / invariants

1. The r13.2 design is frozen **except** where AMENDMENT-1 moved it, by owner ruling, on the record.
   No further frozen change is in scope. The frozen suite must stay green (now 147).
2. The matrix rule (§1): every row is one fact in two places; the join is valid only when the listed
   equality is mechanically reproduced from independently admitted inputs; every row carries a
   positive and a falsification witness. Every consumer of an invariant must honour it — a row
   honoured in one consumer and not another is a finding.
3. §3 authority modes: `FIXTURE_ONLY` may exercise parsers, signatures, reducers and join logic and
   cannot create an experiment-eligible score or a physical pass.
4. Readiness is `BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`. No ceremony, no production
   root, no experiment, no provider call, no spend. The measurement half has still never executed
   against a live ETW session.
5. Unverifiable platform constants fault loudly rather than degrading to a number.

## 4. Claims to attack (construct-the-bypass)

Each item: name the byte or executed sequence that falsifies it, **and its consequence for the
data**, or name the residual.

1. **AMENDMENT-1 binds what it claims, and broke no join.**
   ADVERSARY: internal-consistency — the amended projection disagreeing with another consumer of the same fact.
   REACHES IT VIA: manifest / state / receipt structures the harness itself builds.
   Claim: `project_state_world` now carries `subject_id` + `owner_role`; a legal `delegate_obligation`
   or `reopen_obligation` at the same cut is refused by I02; and no other consumer of the canonical
   world (A0/A1 packets, gold action derivation, episode joins, the reducers) silently changed
   meaning. **Wrong-number consequence to hunt: does the amendment alter any gold answer, action
   legality, or score that the frozen design intended?** It must not.
2. **The ETW consumer's fault posture is real, not decorative.**
   ADVERSARY: internal-consistency — the measurement stream reporting a number where evidence is absent.
   REACHES IT VIA: the record stream, lifetime roster, capability record and loss counters.
   Claim: after the fold, an incomplete drain, a failed `CloseTrace`, a still-live pump, an
   unbindable thread event, and a post-stop loss query each make evidence UNAVAILABLE or fault by
   name — never a count. Find a path where degraded input still yields a signable number.
3. **The thread start-key binding is correct, not merely non-faulting.**
   ADVERSARY: internal-consistency — a thread attributed to the wrong process incarnation.
   REACHES IT VIA: the decoded ProcessStart/ThreadStart streams.
   Claim: binding by PID + QPC interval (last start not in the thread's future) attributes every
   thread to the correct incarnation. **Wrong-number consequence: a mis-bound thread puts another
   process's instructions in our count.** Construct a PID-reuse ordering that mis-binds.
4. **Key identity is the key.**
   ADVERSARY: internal-consistency — committed test material admitted as a production root.
   REACHES IT VIA: `configure_production_verifier_context` and the `MBCX01_BUILD_OWNER_TRUST_ANCHOR` OS-config path.
   Claim: identity derives from the decoded Ed25519 point, so no re-encoding of a committed key
   escapes the refusal. ⚠ **And the inverse, which is the more valuable probe: does the new
   structural SPKI walk or the canonical-carrier check REFUSE a legitimate, correctly-formed
   operator key** — one a real HSM, `openssl`, or the ceremony's own export step would produce?
   A false refusal blocks the ceremony.
5. **The widened committed-key harvest refuses only what it should.**
   ADVERSARY: internal-consistency — fixture signing material creating experiment-eligible evidence.
   REACHES IT VIA: production manifests and custody documents supplied by the harness.
   Claim: harvesting every `public_key_pem` from every committed `*.fixture.json` (1 → 5 keys)
   refuses committed material on both planes while the fixture lane stays green. ⚠ **Inverse
   probe: could this refuse a legitimate production root that merely happens to appear in some
   committed document, or miss one that should be refused?**
6. **The positive-lane key swap did not weaken the suites.**
   ADVERSARY: author-blind-spot — a witness that passes because its inputs got easier, not because the code is right.
   REACHES IT VIA: the BUILD suites' own fixtures.
   Claim: moving both suites' positive lanes to in-memory generated signing keys changed only which
   key signs, not what is proven. The driver's control run (new tests vs pre-fix authorities: 120
   ran, exactly 5 failed, zero collateral) is banked evidence, not proof for every witness —
   pick witnesses and check they still discriminate.
7. **`FROZEN_TEST_TOTAL` 145 → 147 is a declaration, not a loosened gate.**
   ADVERSARY: maintainer — a future frozen change riding in under a number nobody questions.
   REACHES IT VIA: `verify-build-bundle.py`'s frozen-count guard.
   Claim: the guard still fails on any frozen-suite change, and the amendment is the only reason the
   number moved.

## 5. Red witnesses per closed class

Every class folded in r4 carries a discriminating probe, RED on pre-fix bytes and GREEN after,
banked in the witness-run files in §2 and mapped two ways in the repair ledger (46/125,
`two_way_total: true`). The driver re-ran each red **independently of the builder's harness**,
forcing pre-fix modules to win the import and proving it by hash before accepting any red. Re-run
them yourself — §6.

## 6. Executable-falsification lane — all seats

- Re-run the banked witnesses: `python -m unittest test_mbcx01_build_measurement
  test_mbcx01_build_state test_mbcx01_build_integration` (expect 125 OK); the frozen
  `test_mbcx01_r13_*` set (expect 147 OK); `python verify-build-bundle.py` (expect a REAL exit 0 —
  check the code directly, not through a pipe).
- Construct and RUN at least one fresh probe of your own per item you rule on. Label every finding
  EXECUTED or READ-ONLY. A READ-ONLY verdict cannot be the deciding GO here.
- ⛔ Do not start an ETW session, create a Job Object, set `MBCX01_BUILD_ALLOW_PHYSICAL`, or run
  `run-smoke-cell.ps1`. The pure layer and the static ABI check run fine unelevated.

## 7. Omission attack

At least one seat: what, un-named above, could still make this instrument produce a wrong number?
Candidate surfaces the author may have under-weighted: the amendment's ripple through hashes that
other rows depend on; the ETW capability record's honesty about what it did and did not observe;
the interaction between the new refusals and the smoke runbook's expectations; whether any fold
made a previously-covered path unreachable and therefore untested.

## 8. Non-claims

1. **No claim the consumer works.** It has never executed against a live session. A green suite
   means the logic is right *if the platform behaves as documented*.
2. **No security boundary against in-process actors.** Tamper-evident, not tamper-proof.
3. **No exactness-execution claim.** The per-witness suite runner is still unbuilt and labelled so.
4. **No completeness claim beyond the enumerated set** — 125 + 147 tests, 46 ledger rows. The green
   means "no failure seen in the shapes this net covers".
5. **A known open risk, named not hidden:** the consumer enables Kernel-Process machine-wide with no
   member filter, so on a non-idle host the smoke run is expected to abort on foreign processes.
   Tracked; NOT folded in r4; not this round's subject unless you can show it corrupts a number.

## 9. Why this exists (build-decision challenge)

ALREADY-BUILT: the key-handling half WAS already built on our own shelf and r4 ADOPTED it rather
than inventing — bridge `src/crl/crl-authenticate.ts:15-18,109-120` loads a public key from raw
SPKI octets and `src/crl/der-reader.ts:227` walks SPKI structurally, which is exactly the pattern
the key-identity fold now uses (the lane's earlier shelf log had missed it; a seat found it). The
ETW/PMC acquisition half has no internal counterpart: the driver spot-ran that query across all
three Moonwalker repos again this round and it returns zero files, so that code is first-of-kind
here and stays hand-written. Externally, WPR/Xperf can attach InstructionRetired to CSwitch and a
prior seat argued we should say so out loud — we do: we are not replacing our signed-evidence join
with it, because the experiment needs the attestation semantics WPR does not provide. Spot-run one
of these queries yourself.
PRODUCT-FIT: this is the experiment's instrument. Fail-loud, mirror-not-cop: unverifiable facts
fault or report UNAVAILABLE. It serves one need — a result the owner can defend.
BIGGER-THAN-THE-BUG: r4's folds were bounded edits inside existing functions; no new subsystem was
introduced. The one place r4 went past the need is recorded in §0 and is the standard this round
is held to.

## 10. Search log (driver's own sweep)

- `cwe.mitre.org/data/definitions/1291.html` (CWE 4.20), opened at origin 2026-08-15: Potential
  Mitigations carries exactly one row — **Phase: Implementation**, "Use different keys for
  Production and Debug"; "Architecture or Design Review" is under Detection Methods; PeerOf CWE-321
  confirmed. This CORRECTED our own prior citation at six live sites.
- `learn.microsoft.com/.../ns-evntcons-event_header_extended_data_item` and the sdk-api source of
  `ne-evntrace-trace_query_info_class`, opened 2026-08-15: the ExtType/Flags numbers are NOT
  published on Learn, which is why the pins were flagged; `TracePmcEventListInfo:8` /
  `TracePmcCounterListInfo:9` are published and match.
- The authoritative ABI source used for the fold was the **installed SDK header**
  `C:/Program Files (x86)/Windows Kits/10/Include/10.0.26100.0/um/evntcons.h` (`:58,:60,:63,:154,:156`)
  — driver-verified line by line, not taken from the builder.
Stopped because each load-bearing vendor question was settled at a primary source or at the
installed header; the remaining platform facts are settled only by the elevated run.

## 11. Internal-shelf log (driver's own internal sweep)

QUERIES: `grep -rilE "EVENT_TRACE|TracePmc|CSwitch|ProcessTrace"` · `grep -rilE "trust[_ -]?(anchor|root)"` · `grep -rilE "spki|subjectPublicKeyInfo|der[_ -]?reader"` · `grep -rilE "fixture[_ -]?only|fixture[_ -]?mode"`
REPOS: agentvault-mcp-bridge (`src/`) · Photon (`crates/`) · Gravity (`src/`) — all three.
OPENED: bridge `src/crl/crl-authenticate.ts:15-18,109-120` and `src/crl/der-reader.ts:227` — ADOPTED for the key-identity fold (load the key from raw SPKI octets rather than a text carrier); bridge `runtime-trust.ts`, `enrollment-fingerprint.ts` — trust-root shapes, already adopted at r1/r2; Photon `crates/aruna-jmap/src/transport.rs` — only sibling fixture-mode hit, a transport test fixture, not adopted (different problem); ETW query returns zero files in all three repos.
STOPPED: the four problem shapes of this round each resolved to an adopted bridge pattern or returned empty across all three repos.

## 12. Seat SWEEP lane (the seats' own sweep)

SWEEP APPLIES TO: any claim resting on prior art, a standard, a vendor's documented behaviour (ETW
semantics, Ed25519/SPKI encoding rules, base64 canonicality, Windows Job accounting) or a footgun
class — go look with your own queries before you bless or refute it.
DELIVERABLE: a SWEEP LOG in your verdict — exact queries · what you OPENED (URL + deciding section)
· what it changed or confirmed · why you stopped.
LABELS: every prior-art or standards-bearing finding carries exactly one of SEARCHED / RECALLED /
UNSEARCHED (UNSEARCHED carries its reason: NOT-LOAD-BEARING · SETTLED-BY-PINNED-BYTES · COULD-NOT ·
DID-NOT).
CONSEQUENCE: an UNSEARCHED or RECALLED finding cannot be the deciding GO on a claim resting on
prior art or a standard; a round where no seat swept such a claim is incomplete.
HONEST OUT: if you cannot reach the web this session, say so plainly in one line — a capability
report, not a discharge.

## 13. Re-review trigger

A fold that changes admission semantics, an invariant consumer, or the consumer's fault posture
⇒ fresh round. Leaf fixes (names, messages, test bodies) ⇒ the codex-CLI gate covers them. Any
finding needing a new subsystem stops at the owner instead of being folded.

## 14. Driver pre-dispatch execution (run before sending, at the §2 pin)

- BUILD 125/125 · frozen 147/147 · `verify-build-bundle.py` REAL exit 0 (46 invariants / 125
  witnesses, `two_way_total`, readiness unchanged) · clean-room
  `verify-build-pinned.ps1 -Commit fce7b355… -ManifestBlob 60d75d62…` → `PINNED RECONSTRUCTION
  COMPLETE`, real exit 0 — this time authenticating the ACTUAL reviewed bytes, which r4's did not.
- Every r4 red re-run by the driver against pre-fix bytes through an independently built harness,
  with the pre-fix module proven in play by hash before any red was accepted.
- Collateral control for item 6 executed: new tests vs pre-fix authorities → 120 ran, exactly 5
  failed (the 4 new witnesses + the rebuilt `bw28`), zero collateral.
- Items 3, 4-inverse, 5-inverse and 7 are NOT driver-executed and are the highest-value ground in
  this round — the author checking his own false-refusal risk is the blind spot the council exists
  to cover.
