GO-WITH-FIXES(TRUST-ROOT-KEY-IDENTITY · PIN-MANIFEST-FRESHNESS · CITATION-ACCURACY)

Label: EXECUTED. Two blocking fixes; neither requires a new subsystem. F1 must close before the key-custody ceremony, not before the smoke run.

Read-at-the-pin. I read the packet at de49049 and the BUILD at the §2 pin 4c7056e. I then ran suites and probes against the working tree, having first confirmed it is byte-identical to the pin: git diff --stat 4c7056e -- . returns exactly one differing file, MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r4.md (the r4 packet itself, added by de49049, not BUILD source). core.autocrlf=true but the .py subjects check out LF-only (mbcx01_build_win32.py = 44768 bytes on disk, 0 CRLF, = the blob at the pin). Two untracked files sit in the tree — the seat-3 prompt and log. I did not open either; the log is another seat's output and the round is sealed. I scoped every grep to named files to avoid reading them incidentally.

Read-only compliance: no repository byte was created, edited, or deleted. Q8's deliberate break was performed by in-memory monkeypatch inside my own probe process, and probe anchor documents were written to %TEMP%, never into the repo. I did not follow Q8's literal "break the implementation locally, revert after" instruction, because editing the artifact is a write and my authority is read-only; the in-memory equivalent gives the same discrimination signal with a guaranteed revert (process exit).

## 1. Evidence read
- MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r4.md:1-323 @de49049 — the packet, whole
- mbcx01_build_trust_anchor.py:319-341 — ProductionVerifierContext.__init__, the three admission gates
- mbcx01_build_trust_anchor.py:418-433 — public_key_identity, identity computed over base64 text
- mbcx01_build_trust_anchor.py:436-495 — committed_fixture_key_material, derivation + stated scope
- mbcx01_build_trust_anchor.py:190-194, 654-673 — STRICT_BASE64_RE / strict_signature_carrier_ok, decode/re-encode equality, applied to signature_b64 only
- mbcx01_build_trust_anchor.py:236-248 — OwnerTrustAnchor.__init__, PEM validated by prefix/suffix markers only
- mbcx01_build_trust_anchor.py:626-651 — resolve_production_verifier_context, the OS-config door
- mbcx01_build_trust_anchor.py:448-455 — the CWE-1291 citation in source
- test_mbcx01_build_measurement.py:1362-1432 — witness bw28, incl. the "re-wrapped key" sub-case at 1400-1406
- verify-build-pinned.ps1:44-61 — pin authentication; line 55 binds governing_commit to -Commit
- MBCX-01-BUILD-PIN-MANIFEST.json @4c7056e (governing_commit: 3527f510…) — manifest subject list, 38 entries
- mbcx01_build_etw_consumer.py:268-310, 642-662 — ETW ABI block + verify_etw_struct_layout()
- mbcx01_build_win32.py @0521752 diff — BUILD source changed after the manifest pin
- mbcx01_build_measurement_authority.py:72, test_mbcx01_build_measurement.py:1226 — the only two surviving *_REWIRED_DURING_VERIFICATION mentions, both comments

Reproduced (EXECUTED, all at the pin): BUILD suites 114 OK; frozen 145 OK; verify-build-bundle.py exit 0, seven sections PASS, ledger 44 invariants / 114 witnesses / two_way_total true, no_production_activation all-false, readiness BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED. verify_struct_layout() → 96/144 Job ABI. §0's threat-model grep and §8's "5 stale marker lines in the FIXTUREISO green bank" both reproduce exactly.

## 2. SWEEP LOG
Web (SEARCHED):
- RFC 4648 §3.5 + §12 — opened rfc-editor.org/info/rfc4648/. Pad bits MUST be zero by conforming encoders; if not, no canonical representation and multiple strings decode to the same binary; §12 states non-significant bits may bypass string equality. Status: Proposed Standard / Standards Track, obsoletes 3548, not obsoleted. 6 errata not opened; relied text is core §3.5/§12. Controlling primary for F1.
- CWE-1291 — opened cwe.mitre.org/data/definitions/1291.html (CWE 4.20, updated 2026-04-30). Base abstraction, mapping ALLOWED, PeerOf CWE-321 confirmed. Refutes the mitigation-phase claim (F3).
- ETW/PMC ordinals: UNSEARCHED / SETTLED-BY-PINNED-BYTES-AND-PACKET-SWEEP — not resting a GO on it.

Internal shelf (spot-run): §11's ETW query → 0 matches all three repos ("first-of-kind" verified). trust-anchor query → 43+ bridge matches (verified). Unprompted hit the log missed (F4): agentvault-mcp-bridge/src/crl/crl-authenticate.ts:15-18,109-120 loads pubkey from raw SPKI octets via node:crypto + crl/der-reader.ts:227 parses SPKI at the byte level — the discipline F1 needs, on the shelf, not adopted.

## 3. Why this exists
ALREADY-BUILT — mostly answered; ETW consumer genuinely first-of-kind (verified). Trust-admission half is not first-of-kind; shelf log stopped at shapes it had already adopted (F4).
PRODUCT-FIT — clean. Every fact the instrument could not verify says so out loud instead of becoming a number; F1 probe refused by name in the control arm; verify-build-pinned threw rather than degraded. Mirror-not-cop behaving correctly.
BIGGER-THAN-THE-BUG — no new offender. The r2 wiring-freeze rider was reverted; only two comment refs survive. F1's fix is ~10 lines inside an existing function; it trips §13's re-review trigger (admission semantics).

## 4. Findings

### F1 — BLOCKING · EXECUTED · Q3 / I13 / I14 / §3
The committed fixture key can become a PRODUCTION root of trust through the ordinary OS-config path. The "KEY, not the LABEL" fold is defeated by a byte-level re-encoding that preserves the key. public_key_identity (:418-433) returns the base64 body as text, whitespace-stripped — it compares an encoding, not a key; RFC 4648 §3.5 guarantees that is not one-to-one.

Executed at the pin via MBCX01_BUILD_OWNER_TRUST_ANCHOR — no object surgery:
  canonical b64:     MCowBQYDK2VwAyEAHt3A1PbOnMO1yjjssQWKpzaBOgzgAp0eIeVd9DvZ8zY=
  non-canonical:     MCowBQYDK2VwAyEAHt3A1PbOnMO1yjjssQWKpzaBOgzgAp0eIeVd9DvZ8zZ=
  variant decodes to identical 44-byte SPKI: True
  variant in derived committed set: None
  CONTROL (verbatim committed key) -> REFUSED PRODUCTION_VERIFIER_CONTEXT_FIXTURE_KEY_MATERIAL
  PROBE   (re-encoded same key)    -> ctx=True code=None  ← ADMITTED
A payload signed with the committed FIXTURE_OWNER_PRIVATE_KEY_PEM verifies True under both the canonical PEM and the admitted variant. The admitted "production" root is functionally the key whose private half ships in this repo — CWE-1291, at the seam the fold was built to close. The module owns the cure one field away (strict_signature_carrier_ok on signature_b64); public_key_pem gets only prefix/suffix marker checks.
The claim the bytes falsify is the fold's own (:443-446, :327-328): "a fact about the key it carries" / "cannot drift from the repository's bytes." It is a fact about one text encoding of that key.

### F2 — BLOCKING · EXECUTED · §7 omission (pin-manifest coverage)
The commit under review cannot be pin-authenticated, and §14's claim that no BUILD source changed after the manifest pin is false. Manifest still carries governing_commit 3527f510…. Reconciling 38 subjects: 33 clean, 0 missing, 5 drifted —
  MBCX-01-PRODUCTION-BUILD-SENIOR-HANDOFF-r13.2.md  20263 -> 20608
  MBCX-01-BUILD-DESIGN-NOTES.md                     28337 -> 28388
  MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md             15204 -> 15212
  MBCX-01-BUILD-SMOKE-RUNBOOK.md                     7311 ->  7316
  mbcx01_build_win32.py                             44581 -> 44768  ← executable BUILD source
0521752 edited mbcx01_build_win32.py (comment-only, diff read). verify-build-pinned.ps1:55 requires manifest.governing_commit == -Commit, so the pinned run only executes at 3527f510 — four commits and one source edit behind the reviewed bytes. `verify-build-pinned.ps1 -Commit 4c7056e… -ManifestBlob 23009028…` THREW (mismatch). Nothing in verify-build-bundle.py reconciles the manifest against current bytes, so green bundle + green pinned-at-old-commit is compatible with drift in those five. Frozen suites unaffected (separate manifest).

### F3 — NON-BLOCKING · READ-ONLY · SEARCHED · citation accuracy
CWE-1291 mitigation phase is wrong at the source in three places (:453-455, test :1372-1374, packet §4/Q3): they say Architecture-and-Design; the page says Potential Mitigations Phase: Implementation. "Architecture or Design Review" is under Detection Methods. PeerOf CWE-321 correct. Record is headed for external readers.

### F4 — NON-BLOCKING · EXECUTED+SEARCHED · §9 ALREADY-BUILT completeness
The internal shelf carries the byte-level key-handling pattern F1 needs and the shelf log missed it: crl-authenticate.ts:15-18 loads pubkey from raw SPKI octets; :109-120 + der-reader.ts parse SPKI structurally. §11's queries never asked "how do we already establish key identity."

### F5 — NON-BLOCKING · EXECUTED · Q8 (witness discrimination)
bw28 discriminates on breaks it anticipates and cannot discriminate the class it names. BASELINE GREEN; committed_fixture_key_material→{} RED; public_key_identity=raw PEM RED; RESTORED GREEN. But the sub-case at :1400-1406 builds its variant from identity() — the normalizer under test — so it can only confirm fixed points; it tests re-wrapping (handled) and never reaches re-encoding (F1). Author-blind-spot Q8 exists to catch.

### F6 — DISCLOSURE, NOT A DEFECT · EXECUTED · Q6 (ABI half)
The unpublished ETW struct sizes/offsets (:275-310) carry no FLAGGED marker but :268-273 + verify_etw_struct_layout() re-derive them from ctypes and say Microsoft publishes no sizeof — derivations, honestly labelled. No finding. [DRIVER NOTE ON SYNTHESIS: seat 3 disputes the CONSTANT VALUES, a different claim from the struct-size derivation — reconcile.]

## 5. What I ruled
Ruled: Q3 (F1 falsified), Q8 (F5 partial), §7 omission (F2), §9 (F4).
Confirmed not independently falsified: Q1, Q2, Q7 — reproduced witnesses + read logic, no fresh input; NOT ruling on them, verdict must not be read as clearing them.
Not ruled: Q4 (clock) read-only; Q5 (ETW honesty) read-only — deserves a seat that probes it; Q6 enum/GUID half UNSEARCHED; Q9 — did not open ceremony doc; F1 reshapes gap (2), re-rule after fix.

## 6. Residual risks
- Q4/Q5 carry no fresh probe from me; if no seat probed Q5, the ETW honesty posture (headline new surface) is council-unreviewed on execution and the round is incomplete on it.
- F1's fix is one of a class: comparing decoded SPKI closes the base64 variant, not a differently-encoded SPKI DER carrying the same 32-byte point. Durable fix compares the raw key point, not any envelope. DER variant is a hypothesis, labelled.
- T2 ceiling stands; F1 is NOT in that class (documented OS-config door, operator-authored document).
- RFC 4648 errata unopened (6). Small.

## 7. Fix class
- F1 TRUST-ROOT-KEY-IDENTITY: identity over the decoded key + canonical-carrier refusal on public_key_pem mirroring strict_signature_carrier_ok; adopt bridge raw-SPKI (F4); new witness built independently of public_key_identity. §13 re-review fires. Must close before the key-custody ceremony (§3 step 0); NOT before the smoke run.
- F2 PIN-MANIFEST-FRESHNESS: regenerate at the review commit + a bundle arm reconciling manifest vs current bytes. Close before this commit is cited as pin-authenticated anywhere.
- F3 CITATION-ACCURACY: correct CWE-1291 phase in all three places. Leaf; codex-CLI gate.
- F5 folded into F1's witness requirement. F4 shelf-log note for next round's §11.

On the GO: EXECUTED, can serve as a deciding vote. GO-WITH-FIXES rather than NO-GO because readiness is BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED — F1 corrupts no result that exists today; it corrupts the ceremony that has not happened yet, which is still ahead of it. If any part of this round is read as authorising that ceremony, my vote is NO-GO until F1 closes.
