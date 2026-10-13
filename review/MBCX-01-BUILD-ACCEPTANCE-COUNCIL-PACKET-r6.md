# MBCX-01 BUILD acceptance council packet — r6 (first complete round on the folded tree)

Packet prose is a pointer map, not evidence — byte-check it.

ROUND LEDGER: council round 6 (r1: NO-GO/NO-GO/GO-WITH-FIXES · r2: 3× GO-WITH-FIXES · r3: INCOMPLETE 2/3 · r4: NO-GO/NO-GO/GO-WITH-FIXES, all EXECUTED, folded · r5: GO-WITH-FIXES/NO-GO/NO-GO, all EXECUTED, folded) · codex rounds 3 of 2 — a code lane, where the 2-round cap governs docs-only diffs; the three codex-CLI gate rounds folded 25 findings + 2 riders red-first, full logs committed (`MBCX-01-CODEXCLI-r{1,2,3}-FULL-LOG-2026-08-15.log`), and their finding count ROSE across rounds (5 → 7 → 10), which is the edge tool re-deriving classes on ground this council has never ruled. That rising count is why this round exists before codex r4.

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

(Zero hits — driver re-verified 2026-08-15 at the §2 pin.)

⛔⛔ **THE FILTER, AND THE DRIVER WILL APPLY IT TO YOUR FINDINGS.** A finding counts in this round
if, and only if, you can name how it makes the experiment **produce a wrong number, admit wrong
evidence, or refuse right evidence**. State that consequence explicitly on every finding.
Findings that harden against an actor deliberately evading a check are out of model, and the
driver will rule them out rather than fold them. ⛔ Do not propose a new machine, engine,
subsystem or general mechanism. If your fix is bigger than the defect, say so and stop — that
re-enters the design gate and is the owner's call, not a fold.

⚠ **THE SPECIFIC RISK THIS ROUND MUST WEIGH:** the three codex rounds closed a run of
refuse-right-evidence defects on the live measurement path by CHANGING SEMANTICS, twice in
signed fields. Those two changes are correct in the driver's judgment and are **not the
driver's to bless alone** — they are agenda items 1 and 2, and ruling them is this round's
first job. A FALSE REFUSAL remains as dangerous as a false admission: probe both directions.

## 1. Verdict contract

First line: **GO / GO-WITH-FIXES(class) / NO-GO**. Code artifact — no round-call token, and skip
the two design questions. Then: evidence read (`path:line`), your SWEEP LOG, findings each
labelled EXECUTED or READ-ONLY **and each carrying its wrong-number / wrong-admission /
wrong-refusal consequence**, residual risks, fix class. Items 1–7 below each end in a RULING
ask — answer each explicitly (ACCEPT / CHANGE, one line of why). Deliver the whole verdict
in-thread.

## 2. Canonical bytes (path@sha pins)

Governing content commit under review: **`396752a680d5f057daef51704a2945ccd2735b41`**. Commits
after it are records only — the regenerated pin manifests (each naming its `governing_commit`
field) and this packet itself. Read the CODE at the pin; if you read the working tree, say so
and confirm it matches (`git status --short` clean, and no `*.py` differs from
`396752a…` — `git diff --stat 396752a HEAD -- '*.py'` is empty).

The arc no seat has seen — r5 reviewed `fce7b355`; since then:
- `5269375` — AMENDMENT-2 + the r5 council folds (thread identity = TID **and** interval; RFC
  7468 transport spelling is not key identity; committed-key harvest keyed on content, not
  filename). Record: `MBCX-01-R13-AMENDMENT-2-THREAD-IDENTITY-AND-PEM-TRANSPORT-2026-08-15.md`.
- `0639fcf` — codex-CLI r1 fold (5 findings).
- `f02211b` — the pin-manifest arm now BYTE-reconciles the pinned reconstruction against the
  manifest instead of waving it through; the bundle verifier refuses a no-manifest-no-git
  directory by name.
- `eb04365` — codex-CLI r2 fold (7 findings).
- `e1dc539` — codex-CLI r3 fold (10 findings + 2 driver-accepted riders, each rider with its
  own red). Highlights on the LIVE MEASUREMENT PATH: retired instructions were signed as ZERO
  into an admission gate requiring nonzero; the root identity queried a boot-tagged
  ProcessStartKey that appears in NO ETW payload; the telemetry query used a 48-byte buffer
  ntdll rejects outright (real-ntdll witnessed); an elapsed-time cross-check no live run could
  pass; machine-wide provider events aborted on any busy host. Kernel-Process payloads are now
  decoded per the provider's own versioned manifest, verified via TDH (the dump is in the r3
  fold's committed log); unknown/old versions fault by name.
- `7172c2a` — repair-ledger cover fix (BA-18 `positive_covered_by` → BA-15; the bundle gate
  itself refused the dangling cover).

Governing design (frozen, not under review): `MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md` (§1
rule, §2 canonical world, §3 authority modes) · `MBCX-01-EXPERIMENT-DESIGN-r9.md` ·
`MBCX-01-R13-CLOSURE-ARCHITECTURE.md` · both frozen amendments.

Ledger: `MBCX-01-BUILD-REPAIR-LEDGER.json` — 65 invariants / 170 witnesses, `two_way_total`.

## 3. Immutable truths / invariants

1. The r13.2 design is frozen **except** where AMENDMENT-1 and AMENDMENT-2 moved it, both by
   owner ruling, on the record. No further frozen change is in scope without the same
   amendment treatment. The frozen suite must stay green (now 150, reason recorded at
   `FROZEN_TEST_TOTAL`).
2. The matrix rule (§1): every row is one fact in two places; the join is valid only when the
   listed equality is mechanically reproduced from independently admitted inputs. Every
   consumer of an invariant must honour it — a row honoured in one consumer and not another is
   a finding.
3. §3 authority modes: `FIXTURE_ONLY` may exercise parsers, signatures, reducers and join logic
   and cannot create an experiment-eligible score or a physical pass.
4. Readiness is `BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`. No ceremony, no
   production root, no experiment, no provider call, no spend. The measurement half has still
   never executed against a live ETW session.
5. Unverifiable platform constants fault loudly rather than degrading to a number.
6. Closure-architecture §7 makes the physical claim a DIFFERENCE — max-minus-min retired
   instructions across the four H values per fixed (D,F), against 500,000. An attribution
   error does not merely perturb a figure; it can flip a carrier's boundedness verdict, which
   is the experiment's actual answer. Judge every finding against that.

## 4. Claims to attack (construct-the-bypass) — each ends in a RULING ask

1. **`counter_value` is now a member-attributed accumulator — the first signed-field semantic
   change.**
   ADVERSARY: internal-consistency — a scoped counter stream whose arithmetic no longer means
   what the signed attribution string says.
   REACHES IT VIA: the machine-wide CSwitch stream the harness itself captures.
   Bytes: `mbcx01_build_etw_consumer.py:1755-1808` (`scope_cswitch_records_to_members` — kept
   records carry RAW minus accumulated foreign work per processor; `excluded` retains the
   foreign rows; `baseline_records` counts the per-processor discarded first intervals),
   recomputed downstream at `mbcx01_build_win32.py:646-660` (`consume_cswitch`) and
   independently at `mbcx01_r13_measurement._validate_physical_evidence` (:1031-1039). The
   docstring's own argument: the frozen observation schema has ONE counter field, and of the
   two readings only the accumulator makes `delta_from_previous` mean
   `raw(this switch) − raw(the previous switch on that processor)` for a member thread.
   Attack both directions: (a) construct an ordering (multiplexed counters, backwards raw
   values after exclusion, member-fault rows kept despite foreign-looking QPC) where the
   subtraction produces a WRONG member delta that still signs; (b) show a legal capture the
   scoping now REFUSES or silently undercounts beyond the declared first-record interval.
   **RULING ASK: is the member-attributed accumulator the correct reading of the one signed
   field — ACCEPT or name the change (e.g. a schema slot for the raw value, which is an
   amendment, not a fold)?**
2. **`root_process_start_key` now carries the ETW-published ProcessSequenceNumber — the second
   signed-field semantic change.**
   ADVERSARY: internal-consistency — the root's identity field and the membership joins
   meaning two different things.
   REACHES IT VIA: the decoded ProcessStart/ProcessStop stream and every consumer of
   `root_process_start_key` (`mbcx01_build_etw_consumer.py:1193,1239,1575-1610,1651-1692,
   2112-2143,2180-2242`; the versioned layout map at `:320-360`; rationale at `:2924`).
   The old value — the boot-tagged ProcessStartKey from
   `ProcessTelemetryIdInformation` — appears in NO Kernel-Process payload, so nothing could
   ever have matched (driver-searched, §10: the published Win10-17134 manifest carries no
   `ProcessStartKey` field in any template, and no `ProcessSequenceNumber` before V3 — which
   is also why the version-gated decode faults by name on old versions rather than guessing).
   Attack: find a consumer, receipt field, schema description, comment or issue (#12's
   `ProcessTelemetryIdInformation = 64` verification) that still assumes the OLD semantics;
   construct a PID-reuse ordering where sequence-number identity mis-roots the tree.
   **RULING ASK: ACCEPT ProcessSequenceNumber as the root identity of record (and the field
   name keeping its old spelling), or name the change?**
3. **The writer-door question: does this instrument need "exactly one producer process per
   store" AT ALL?**
   ADVERSARY: internal-consistency — two harness processes writing one journal minting
   conflicting sequence numbers.
   REACHES IT VIA: the state store's own commit path.
   Bytes: `mbcx01_build_state_store.py:37-41` (the serializer is SQLITE ITSELF), `:143`
   (`journal_seq_unique`), `:381,461-464,500,727` (`BEGIN IMMEDIATE` + in-transaction sequence
   allocation). The named harm — duplicate journal seq — is closed inside SQLite's own write
   serialization; a second producer either serializes behind the first or faults on the unique
   index. The internal shelf HOLDS a stronger door — Photon
   `crates/aruna/src/writer_gate.rs` (process-wide per-file-identity enrollment gate; opened,
   §11) — and the driver deliberately did NOT adopt it: it exists to give SEVER priority under
   a concurrency model (multi-writer service) this instrument does not have, and its own
   header names multi-process contention as a residual SQLite busy-handling already covers
   here. No adversary exists; the honest answer may be NO DOOR.
   **RULING ASK: is SQLite's serialization + unique index + in-transaction allocation
   SUFFICIENT for a single-harness scientific instrument — ACCEPT no-door, or name the door
   this lane must build (that is a design-gate answer, not a fold)?**
4. **The six AMENDMENT-2 judgment calls (issue #8) — rule each, don't inherit.**
   ADVERSARY: author-blind-spot — an unchallenged judgment call becoming an unexamined
   assumption.
   REACHES IT VIA: the fault vocabulary and carrier rules the next real capture will hit.
   (1) bare-CR PEM accepted — broader than openssl, which refuses a CR-only document
   (probe-verified); we follow RFC 7468 §2 parser guidance. (2) the anchor STORES the
   normalised carrier, so `public_key_pem` is not byte-identical to a CRLF source document.
   (3) `ETW_THREAD_LIFETIME_DUPLICATE_START` narrowed to same-QPC duplicates; overlap gets
   `ETW_THREAD_LIFETIME_OVERLAPPING_REUSE`; two-starts-one-stop now yields
   `ETW_THREAD_LIFETIME_INCOMPLETE` — **no banked test asserts that name**. (4) TOUCHING
   intervals refused in both layers (containment is inclusive at both ends; the join must stay
   a function). (5) `ETW_PROCESS_INCARNATION_AMBIGUOUS` is a new name rather than folding into
   UNBINDABLE. (6) a stop-less incarnation is OPEN-ENDED for the binder; roster completeness
   stays `assemble_member_lifetimes`' fault.
   **RULING ASK: six explicit ACCEPT/CHANGE calls; on (3) additionally rule whether a witness
   pinning the INCOMPLETE name is owed (the driver believes yes — it is currently unpinned
   vocabulary).**
5. **The three fixture-key gaps (issue #14) — rule each per its own discharge condition.**
   ADVERSARY: internal-consistency — committed fixture material creating production authority.
   REACHES IT VIA: `mbcx01_build_trust_anchor.py:418` (`public_key_identity`), `:436`
   (`committed_fixture_key_material`), and the ceremony
   (`MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md` §3 step 0).
   (1) `FIXTURE_NON_ANCHOR_PRIVATE_KEY_PEM` — a committed private key whose public half
   appears in no committed document is NOT in the derived known-key set; deriving
   public-from-private would put a Node subprocess on the production construction path. Close
   only if the ceremony makes that key copyable in practice. (2) a committed test SIGNING key
   copied into a production trust-root manifest is refused today as
   `MEASUREMENT_CUSTODY_EVIDENCE_INVALID`, not as committed material — explicitly unclaimed.
   Close only if a seat shows the copy path is reachable in the ceremony. (3)
   `resolve_production_verifier_context` RAISES on a committed-key anchor via the OS-config
   path rather than returning a named code — matches the module's malformed-anchor rule; a
   seat should look at it.
   **RULING ASK: three explicit ACCEPT-as-residual / CHANGE calls, judged against the
   ceremony's actual reachability, not against an evasion story.**
6. **The smoke pass-criterion is now a CONJUNCTION — and both halves must discriminate.**
   ADVERSARY: internal-consistency — a smoke "pass" that certifies nothing.
   REACHES IT VIA: `mbcx01_smoke_cell.py:515-567` (`validate_produced_envelope` — judged on
   its OWN merits, with the production authority's own per-envelope validator and the same
   Node verifier seam admission uses) and `:571-595` (`verify_envelope` — the honest
   `PHYSICAL_HARNESS_UNAVAILABLE` red is the pass criterion ONLY for an independently valid
   envelope); a failed criterion exits nonzero.
   Attack both halves: (a) construct an envelope that is structurally/signature-valid to
   `validate_produced_envelope` yet evidentially empty enough that the conjunction certifies
   nothing about the real producer; (b) name a legitimate first-run condition the conjunction
   would falsely fail (owner runs it elevated once — a false failure burns the session that
   was supposed to settle seven platform facts).
   **RULING ASK: ACCEPT the conjunction as the smoke criterion of record, or name the change
   before the elevated run (#2/#3)?**
7. **Dropped live-path provenance: exclusion counts have no receipt slot.**
   ADVERSARY: internal-consistency — a scoped capture whose discard arithmetic is invisible to
   every downstream reader.
   REACHES IT VIA: the signed receipt's frozen observation schema.
   Bytes: the replay/consumer path records `excluded_foreign_cswitch_records`
   (`mbcx01_build_etw_consumer.py:1892`) and `excluded_foreign_process_events` /
   `excluded_foreign_thread_events` (`:3106-3108`) in its provenance dict — and the frozen
   receipt schema has NO slot, so on the physical path those counts are computed and
   discarded. A future auditor of a signed receipt cannot see how much foreign work was
   subtracted (item 1's arithmetic) or how many foreign events were excluded.
   **RULING ASK: receipt slot via a third frozen amendment, or ACCEPT as a named residual
   until the smoke run says whether the counts carry diagnostic weight? (A new slot is a
   frozen-layer change — amendment treatment, owner ratifies.)**

## 5. Red witnesses per closed class

Every class folded since r5 carries a discriminating probe, RED on pre-fix bytes and GREEN
after: the AMENDMENT-2 set (five BUILD reds + two frozen reds + one disclosed GUARD, recorded
as such in the amendment §6), and the codex r1/r2/r3 folds (25 findings + 2 riders, each with
ledger rows; full logs committed at the three `MBCX-01-CODEXCLI-r*-FULL-LOG-2026-08-15.log`
files). The driver re-ran every red against hash-proven pre-fix bytes (`git show HEAD:` into a
scratch dir at `sys.path[0]`, module `__file__` + SHA-256 printed and asserted) before any
commit. Ledger 65/170, `two_way_total: true`. Re-run them yourself — §6.

## 6. Executable-falsification lane — all seats

- Re-run the banked witnesses: `python -m unittest test_mbcx01_build_state
  test_mbcx01_build_measurement test_mbcx01_build_integration` (expect 170 OK); the frozen
  `test_mbcx01_r13_*` set (expect 150 OK); `python verify-build-bundle.py` (expect a REAL exit
  0 — check the code directly, not through a pipe; it now also byte-reconciles the pinned
  reconstruction arm).
- Construct and RUN at least one fresh probe of your own per item you rule on. Label every
  finding EXECUTED or READ-ONLY. A READ-ONLY verdict cannot be the deciding GO here.
- ⚠ A probe/grep returning EMPTY output is a broken-harness signal, not a pass — run it raw
  and read the traceback before concluding anything (this lane's own harnesses failed silently
  twice; the re-entry records both).
- ⛔ Do not start an ETW session, create a Job Object, set `MBCX01_BUILD_ALLOW_PHYSICAL`, or
  run `run-smoke-cell.ps1`. The pure layer and the static ABI checks run fine unelevated.

## 7. Omission attack

At least one seat: what, un-named above, could still make this instrument produce a wrong
number? Surfaces the author may have under-weighted: the TDH-manifest-driven decode's own
assumptions (the manifest names offsets — does anything still assume a layout the manifest
does not state?); the deliberately-NOT-built list from the codex arc (no second value in the
root-identity receipt; no version gates on thread events, both published versions verified
identical for the fields read — is either omission load-bearing?); the amendment ripple
through hashes other rows consume; `sqlite3.OperationalError` escaping `commit_transition`
raw (#25, pre-existing, red owed); whether any fold made a previously-covered path unreachable
and therefore untested.

## 8. Non-claims

1. **No claim the consumer works.** It has never executed against a live ETW session. A green
   suite means the logic is right *if the platform behaves as documented*; known constants are
   now manifest/TDH-verified where the platform publishes anything, and every remaining
   unknown faults loudly by name.
2. **No security boundary against in-process actors.** Tamper-evident, not tamper-proof; this
   round reviews scientific validity only.
3. **No exactness-execution claim.** The per-witness suite runner is still unbuilt (#7) and
   labelled so.
4. **No completeness claim beyond the enumerated set** — 170 + 150 tests, 65 ledger rows. The
   green means "no failure seen in the shapes this net covers".
5. **Known open, tracked, not this round's subject unless it corrupts a number:** the
   machine-wide Kernel-Process provider abort risk on a busy host (#3, gating the smoke run);
   the engine's producing half is ZERO lines (#17–#22); the DoR reconciliation sweep (#23) has
   not run, so DoR sentences about BUILD STATE may lag the tree.

## 9. Why this exists (build-decision challenge)

ALREADY-BUILT: the folds under review ADOPTED where the shelf held the pattern — the key/SPKI
handling stays on the bridge `crl-authenticate.ts`/`der-reader.ts` pattern adopted at r4; the
writer-door question EXPLICITLY weighs Photon `writer_gate.rs` (opened this round, §11) and
declines it with a stated reason for the seats to attack (item 3). The ETW/PMC acquisition
half has no internal counterpart — the three-repo query re-ran today and returns zero files
(§11) — so it remains first-of-kind here, now anchored to the provider's own versioned
manifest via TDH rather than to guessed layouts.
PRODUCT-FIT: this is the experiment's instrument. Fail-loud, mirror-not-cop: unverifiable
facts fault or report UNAVAILABLE; nothing built this arc is a wall, census or scanner — 23 of
25 codex findings made the instrument ACCEPT more true evidence or stop lying to itself.
BIGGER-THAN-THE-BUG: every fold was a bounded edit inside existing functions; the one
candidate machine (an interprocess writer door) was NOT built and is put to this round as
item 3 instead.
PRIMARY-CONSUMER: the signed measurement receipt's consumer is the INFERENCE layer and, behind
it, the owner defending one number; the two semantic changes (items 1–2) exist precisely so
that what that consumer reads — a member-attributed delta stream and a root identity — is
true of the bytes the platform actually emits. A bounded read of the receipt buys the
consumer the boundedness verdict of §3.6 and nothing else.

## 10. Search log (driver's own sweep, 2026-08-15)

- Query: `ETW Kernel-Process provider ProcessStart ProcessSequenceNumber payload
  ProcessStartKey` (WebSearch). OPENED at origin:
  `github.com/repnz/etw-providers-docs/blob/master/Manifests-Win10-17134/Microsoft-Windows-Kernel-Process.xml`
  — ProcessStartArgs v0/V1/V2 field lists read; **no template in the provider carries a
  `ProcessStartKey` field; no `ProcessSequenceNumber` before V3**. This independently supports
  item 2's fold (the boot-tagged start key appears in no payload) AND the version-gated
  faulting (old OS builds genuinely lack the field).
- The authoritative layout source for THIS host remains the machine-local TDH dump banked in
  the codex r3 fold log (`wevtutil` emits empty templates — the dump, not Learn, names the
  offsets), plus the installed SDK header `evntcons.h` verified line-by-line at r5.
- Standing from r5, unchanged and still load-bearing: CWE-1291 (Potential Mitigations =
  Implementation phase), RFC 7468 §2/§3 (carrier spellings), Microsoft Learn on TID reuse.
Stopped because the round's one new vendor question (which identity the payload actually
publishes) was settled at a primary source and at the banked TDH dump; the remaining platform
facts are settled only by the elevated run.

## 11. Internal-shelf log (driver's own internal sweep, 2026-08-15)

QUERIES: `InstructionRetired` · `TracePmc` · `CSwitch` · `ProcessSequenceNumber` ·
`writer_gate` · `single-writer` · `BEGIN IMMEDIATE` · `exactly one producer` (run as two
alternation greps over these eight terms)
REPOS: agentvault-mcp-bridge (`src/`) · Photon (`crates/`) · Gravity (`src/`) — all three.
OPENED: Photon `crates/aruna/src/writer_gate.rs` (header + invariants read this session) —
process-wide per-file-identity writer enrollment with sever priority; NOT adopted, reason
stated in item 3 for the seats to attack: it solves sever-priority under a multi-writer
concurrency model this single-harness instrument does not have, and its own header names
multi-process contention as a residual that SQLite busy machinery covers. Photon
`crates/aruna/src/store_open.rs` — one-door open chokepoint, already mirrored by the state
store's preflight (`mbcx01_build_state_store.py:37-41` reading confirmed). ETW/PMC query:
ZERO files in all three repos — first-of-kind confirmed again.
STOPPED: both problem shapes resolved — one to a named adopt-or-why-not, one to a verified
empty shelf.

## 12. Seat SWEEP lane (the seats' own sweep)

SWEEP APPLIES TO: any claim resting on prior art, a standard, a vendor's documented behaviour
(ETW payload versioning, PMC counter semantics, SQLite write serialization, RFC 7468, Ed25519/
SPKI encoding) or a footgun class — go look with your own queries before you bless or refute
it.
DELIVERABLE: a SWEEP LOG in your verdict — exact queries · what you OPENED (URL + deciding
section) · what it changed or confirmed · why you stopped.
LABELS: every prior-art or standards-bearing finding carries exactly one of SEARCHED /
RECALLED / UNSEARCHED (UNSEARCHED carries its reason: NOT-LOAD-BEARING · SETTLED-BY-PINNED-
BYTES · COULD-NOT · DID-NOT).
CONSEQUENCE: an UNSEARCHED or RECALLED finding cannot be the deciding GO on a claim resting on
prior art or a standard; a round where no seat swept such a claim is incomplete.
HONEST OUT: if you cannot reach the web this session, say so plainly in one line — a
capability report, not a discharge.

## 13. Re-review trigger

A ruling that CHANGES either signed-field semantic, adds a receipt slot, or orders a writer
door ⇒ the change is an amendment/design-gate matter and the amended bytes come back to a
fresh round. ACCEPT rulings + leaf fixes (names, messages, witness additions) ⇒ fold and
proceed to the codex-CLI r4 gate. Any finding needing a new subsystem stops at the owner.

## 14. Driver pre-dispatch execution (run before sending, at the §2 pin)

- BUILD **170/170 OK, exit 0** · frozen **150/150 OK, exit 0** · `verify-build-bundle.py`
  REAL exit **0** (65 invariants / 170 witnesses, `two_way_total`, pin-manifest reconciliation
  PASS, readiness unchanged) — all three re-run and witnessed THIS session, not inherited from
  the re-entry doc.
- Clean-room `verify-build-pinned.ps1 -Commit 396752a… -ManifestBlob 97a02c13…` →
  `PINNED RECONSTRUCTION COMPLETE`, real exit 0, re-run this session (pwsh 7; Windows
  PowerShell 5.1 fails on `Get-FileHash` — a harness fact, not a lane fact).
- The no-adversary grep re-run at the pin: zero hits.
- Items 1 and 2 were driver-reproduced at the byte during the codex arc (the probes are in the
  committed fold logs). Items 3–7 are RULINGS this driver deliberately did not make alone —
  they, and the fresh adversarial probes on items 1–2, are the highest-value ground in this
  round: the author checking his own semantic changes is the blind spot the council exists to
  cover.
