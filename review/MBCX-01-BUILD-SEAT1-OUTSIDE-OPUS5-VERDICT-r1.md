# MBCX-01 BUILD acceptance SEAT1 (Opus 5) verdict — r1 — banked verbatim from the live seat thread

> Banked 2026-08-14 by the BUILD-lane driver from conversation `<id>`
> (CDP <council-browser-port>), read-only `wait_quiesced` capture (state `indeterminate/lineage-unavailable`; text
> settled and terminal). Verbatim, including the tab's UI lines.

---

Used Moonwalker integration

Used Moonwalker integration

Reconstruction PASS (145 frozen + 76 BUILD). Now C1 — the subtractive discharge is the novel mechanism and the likeliest laundering surface.

Used Moonwalker integration, searched the web · 4 notes

Used Moonwalker integration, searched the web · 4 notes
MBCX-01 BUILD ACCEPTANCE — SEAT VERDICT r1
1. Verdict

GO-WITH-FIXES(documentation/leaf-edge) — the BUILD is sound. Every claim C1–C5 held under fresh adversarial inputs I constructed and ran. One finding is a P3 documentation-scope correction (the store_path binding is content-scoped, not instance-scoped, and the packet does not say so), plus one P3 against my own method. Neither ripples architecture, interface, or security; both go to the codex gate, not back to council.

Label: EXECUTED. I ran the pinned reconstruction, all banked suites, and eleven fresh probes of my own.

2. Seat, harness, posture

Claude Opus 5, Moonwalker MCP harness (pwsh + CPython 3.11, read-only). Longitudinal: I carry my own r7–r13.2 MBCX lane and use it, labelled — this BUILD is the artifact my own r13.2 CONFIRMED authorized, and I re-test my own carried residual (operator-independence) below. Seal: I opened no other seat's r1 output, log, marker or verdict. No experiment, provider/model call, real Job/ETW collection, signing ceremony, or spend. Paid inference: NONE. Modified nothing.

3. Pin and reconstruction — EXECUTED
HEAD == 8516ea4                                      TRUE (branch codex/mbcx01-production-build)
2fd38972 ancestor of HEAD                            exit 0
manifest blob 5f5cd20b                               blob, 31,352 bytes
working tree vs code pin, 14 canonical artifacts     DRIFT = 0  (tree matches pin; reads are on-pin)
verify-build-pinned.ps1 -Commit 2fd38972 -ManifestBlob 5f5cd20b   -> exit 0
  frozen_suites  PASS   Ran 145 tests
  build_suites   PASS   Ran 76 tests  (34+46+4+43+15+3 across sections = 145 frozen; 76 BUILD)
  ledger PASS (34 invariants, 76 witnesses, two_way_total: true)
  schemas PASS (strict_compile, 12 mutants rejected, 2 subjects)
  canonical_parity PASS · execution_posture PASS
  no_production_activation PASS:
      committed_manifests_production_ready=false · trust_root_activated=false
      signing_ceremony_performed=false · physical_collection_env_flag_present=false
  top_level_readiness: BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED

Side effects: none. Repo dirty count 3, pre-existing and not mine. All probe work in %TEMP%\mbcxb from a git archive of the pin; directory removed and verified absent.

4. Claims C1–C5
C1 — subtractive sentinel discharge is non-weakening → HOLDS. EXECUTED.

mbcx01_build_state_authority.py:739-774@2fd38972. Probe validity established first: clean production graph admits [], and the frozen production path on the same input returns exactly ['A0_PACKET_INVALID','I02_INVARIANT_INVALID','STATE_AUTHORITY_UNAVAILABLE'] — cascade is byte-identical to SENTINEL_CASCADE_CLOSURE. The closure is the mechanical cascade, not a hand-picked set.

The structural reason it cannot weaken is line 773: on discharge it returns sorted(set(fixture_errors)) — the frozen fixture verdict verbatim, never a filtered production verdict. So no defect the fixture path catches can be dropped, by construction. The only reachable weakening surface is a defect visible only in production mode whose name lies inside the closure. I attacked exactly that:

M1 embedded V1 receipt replaced with garbage   cascade adds STATE_AUTHORITY_SCHEMA_INVALID -> discharge disabled, REJECTED
M2 embedded V1 authority_mode -> PRODUCTION    cascade adds SCHEMA_INVALID + HASH_INVALID  -> REJECTED
M3 embedded V1 receipt_hash zeroed             cascade adds STATE_AUTHORITY_HASH_INVALID   -> REJECTED
M4 genuine A0 defect                           fixture catches it (A0_CALL_INVALID, A0_RESULT_INVALID) -> survives, REJECTED
control: no V2 supplied  -> ['A0_PACKET_INVALID','I02_INVARIANT_INVALID','STATE_AUTHORITY_UNAVAILABLE']
         i.e. byte-for-byte the frozen production verdict

Any production-only name outside the closure disables the discharge wholesale (cascade <= SENTINEL_CASCADE_CLOSURE). And the sentinel is unconditional under require_production (mbcx01_r13_packets.py:543-544), so it is always a member of the cascade — a cascade consisting of {A0_PACKET_INVALID} alone is unreachable. No residual weakening found.

C2 — fixture/self-authored evidence cannot clear production admission → HOLDS. EXECUTED.

mbcx01_build_measurement_authority.py:evaluate_production_measurement. All four escalations rejected:

C2-0 committed fixture manifest, no custody   -> MEASUREMENT_CUSTODY_EVIDENCE_INVALID, MEASUREMENT_TRUST_ROOT_INVALID, PHYSICAL_…
C2-1 production_ready flipped TRUE            -> same
C2-2 + every root fixture_only=false          -> same
C2-3 + self-authored extra root appended      -> same

All six committed trust-root manifests on disk read production_ready=False; flipping copies changes nothing at the admission point. ⚠ Probe correction on the record: my first C2 attempt called validate_production_trust_root_manifest and tested == [], but that function returns a dict of roots, so every "REJECTED" label in that run was meaningless. I discarded it and re-ran at the packet's named admission point. The results above are from the corrected run.

C3 — crash windows cannot mint → HOLDS, with one adjudication. EXECUTED.

mbcx01_build_state_store.py:commit_transition, all three CRASH_POINTS driven:

BEFORE_COMMIT       durable read REFUSED  STATE_STORE_TRANSACTION_PENDING
AFTER_PROPOSAL_ROW  durable read REFUSED  STATE_STORE_TRANSACTION_BROKEN
valid receipt re-pointed at a BEFORE_COMMIT store       -> STATE_AUTHORITY_V2_TRANSACTION_NOT_COMMITTED  (+ sentinel)
valid receipt re-pointed at an AFTER_PROPOSAL_ROW store -> STATE_AUTHORITY_V2_TRANSACTION_NOT_COMMITTED  (+ sentinel)
valid receipt re-pointed at a BEFORE_READBACK store     -> verifies clean

Adjudication of the last line, because it looks like a bypass and is not. BEFORE_READBACK means the transaction committed durably and the process died before performing the readback; on restart the durable terminal is COMMITTED with the same transaction id, prestate, proposal, child and anchors. Verifying against it is verifying the same fact, not a minted one — and C4 shows a receipt cannot be re-pointed at a store with a different store_id. So nothing is minted. What it does establish is a scope fact the packet never states: store_path verification binds to durable content, not to store-instance identity. See P3-1.

C4 — anti-replay anchors are durable, not derived → HOLDS. EXECUTED.

mbcx01_build_state_authority.py:_anti_replay_errors. Per-axis replay with probe-fire counts, all rejected against the durable journal anchors:

transaction_commit_id (n=2) · receipt_nonce (n=1) · scenario_id (n=1) · run_id (n=1)
subject_identity (n=1) · store_id (n=1) · namespace (n=1)
   all -> STATE_AUTHORITY_V2_CANONICAL_BYTE… (+ STATE_AUTHORITY_UNAVAILABLE)

The docstring's own account of the fold is honest and matches behaviour: the pre-fold verifier re-derived nonce/scenario/run from labels the attacker controls (a self-check, not an anchor); the anchors are now a durable pre-effect commitment compared as canonical bytes. Confirmed by execution, not by reading.

C5 — custody separation is mechanical → HOLDS. EXECUTED.

validate_production_trust_root_manifest, each axis independently, all firing before any grid analysis:

revoked root                 -> TRUST_ROOT_REVOKED
expired validity window      -> TRUST_ROOT_VALIDITY_EXPIRED
signer/editor role collision -> MEASUREMENT_TRUST_ROOT_INVALID
forged trust_policy_digest   -> MEASUREMENT_TRUST_ROOT_INVALID

The committed fixture manifest and production_ready-flipped copies return roots without raising here — correct, because this function resolves roots and the fixture-vs-production gate lives at evaluate_production_measurement (C2), where all four flips were refused. The eight banked bw01–bw03 custody witnesses ran green in my reconstruction.

5. Findings

P3-1 — store_path binding is content-scoped, not instance-scoped, and no non-claim says so. READ-ONLY (established by the C3 execution above). A V2 receipt verifies clean against any store that durably committed the same transaction under the same store_id/namespace — I demonstrated this with a BEFORE_READBACK replica. This is not a minting path (C4 closes cross-store-id replay) and it is arguably the correct semantics for a content-addressed receipt. But §6's non-claims enumerate what is not asserted, and this is exactly the sort of scope fact that a later reader will assume the other way. Smallest fix: one line in §6 — "verification binds durable content, not store instance; two stores holding the same committed transaction under the same store identity are interchangeable to the verifier." Leaf edge; codex gate.

P3-2 — against my own method, not the artifact. My first C2 probe tested a dict return against == [], producing four meaningless "REJECTED" labels; my C3/C4 probes needed two corrections before they fired. This is the fourth consecutive MBCX round in which a probe of mine, not the artifact, was the broken thing. I now assert probe-fire before drawing conclusions (the n= counts in C4, the "PROBE VALIDITY" line in C1); that practice is what caught it. Recorded so no seat inherits my bad first run.

No P0, P1 or P2. No architecture/interface/security ripple. No re-review trigger.

6. WHY THIS EXISTS — all three answered

(1) ALREADY-BUILT? — spot-run, SEARCHED-internal. I verified the shelf log's premise the way I did in r13: the claim that no shelf artifact supplies the exact state-owner receipt matches what I found independently in my own r13 event-sourcing sweep — durable append and replay are everywhere, an externally attested readback receipt binding prestate/applied-child/poststate for a third-party verifier is nowhere. Adopting containment discipline, writer-gate, record-before-effect and the signer shape while building the receipt is the right adopt/build split.

(2) PRODUCT-FIT? — yes, stated in one sentence. An operator needs to know whether a commit actually landed and what a run physically cost, from evidence a third party can check, and to get a loud red when that evidence is absent. Absent authority stays red — verified: top_level_readiness is BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED and every production admission I attempted refused. Mirror-not-cop holds: nothing here prevents a box owner from anything.

(3) BIGGER-THAN-THE-BUG? — NO. This is the commissioned BUILD of the two prerequisites the r13.2 council converged on 3/3, and I was one of those three seats. The versioned-sibling architecture is forced by the frozen code, not chosen. Nothing here is a review-authority invention.

7. SWEEP LOG
Query	Opened	Deciding content	Effect	Label
sqlite WAL "synchronous=FULL" durability commit power loss NORMAL may lose transaction	sqlite.org/forum/forumpost/fa8270b554; sqlite.org/forum/info/d1a6bc7c4cd2baca	"With PRAGMA synchronous=NORMAL in WAL mode, recent changes to the database might be rolled back by a power loss, but the database will not be corrupted"; "a single transaction with PRAGMA synchronous=FULL causes an fsync() to occur on the WAL file, which makes all prior transactions durable across power failures or OS crashes"	Confirms the driver's §8 row and, more importantly, that the pin is load-bearing rather than decorative. I then verified it is actually in force rather than documented — see below	SEARCHED
Store durability pin, executed	live PRAGMA on a store opened by open_verified	STORE_JOURNAL_MODE = WAL; store.journal_mode = WAL; live journal_mode = wal; live synchronous = 2 (FULL)	The C3 durability claim rests on a pragma the store genuinely sets, not on prose	EXECUTED
Job accounting ABI / TotalTerminatedProcesses	—	I opened learn.microsoft.com/.../ns-winnt-jobobject_basic_accounting_information at origin myself in r12 and again in r13.2, and verified there that the pinned pack string <qqqqIIIIQQQQQQ measures 96 bytes with the member defined as "processes terminated because of a limit violation"	Carried; nothing in this BUILD changes it	RECALLED-with-own-prior-open
TRACE_QUERY_INFO_CLASS ordinals (8/9)	not opened	—	UNSEARCHED — NOT-LOAD-BEARING to this verdict: mbcx01_build_win32.py is declared UNEXECUTED reviewable code, the collector is double-gated and I left the gates unset, and §6 already flags the ordinal as a smoke-stage check that faults loudly on disagreement. It cannot be the deciding GO here because nothing I admit depends on it	UNSEARCHED(NOT-LOAD-BEARING)
Ed25519 pitfalls; SLSA verification model	not opened	—	UNSEARCHED — DID-NOT (budget). Another seat should carry these; my GO does not rest on either, since C2/C5 were settled by execution against the admission points rather than by cryptographic-property argument	UNSEARCHED(DID-NOT)

Why I stopped: the one platform-semantics claim that is genuinely load-bearing for a claim I am blessing (WAL durability under C3) was settled by a primary plus an executed pragma check. The rest either don't gate my verdict or are carried from origins I opened myself in earlier rounds.

8. Omission attack

What the BUILD did not name — and I could not turn into a finding: the store file itself as untrusted input to ReadOnlyStateStoreView. I probed the adjacent surface (re-pointing receipts at PENDING/BROKEN/replica stores) and the verifier refused every non-committed terminal; a hostile store file is a box-owner artifact and therefore sits under the T2 ceiling, which §2 settles. Disposition: TAR-PIT — box-owner family, do not grind.

What it did name that I'd sharpen: the store_path scope (P3-1).

One un-named class I'd put on the smoke-stage list, not this gate: subject_identity is the fifth anchor and the only one whose production value comes from outside the store's own labels. C4 shows it is byte-compared to a durable anchor, so it cannot be replayed — but who is authorized to assert it in production is a custody question the runbook should name alongside signer/editor separation. Not a finding here (no reachable false result at this gate); a line for the runbook.

My carried r13.2 residual — operator-independence — is now largely discharged by construction: independent_readback is a distinct call with its own reader_identity, and the C3 fresh-store probes show the readback is re-performed against durable rows rather than returned from writer memory. What remains for the smoke stage is the organizational half: proving the reader is a different party, not just a different code path.

9. Residual risks and non-claims
R-1 Suite coverage of C2/C5 leans partly on the banked witnesses (bw01–bw03, BuildReplayAndRelabelTests, BuildMalformedEvidenceTests) which I ran but did not each independently re-derive; my own fresh probes covered four C2 and four C5 axes.
R-2 mbcx01_build_win32.py is UNEXECUTED by design and by my instruction; the ordinal check is smoke-stage. Correctly declared.
R-3 Per-witness exactness SUITE execution deferred (§6) — I confirm verify_production_carrier_exactness binds identities and refuses relabels; it does not bless carrier behaviour. OPEN, correctly tracked.
R-4 Trust-root validity uses published_at rather than wall clock — OPEN, documented, and my C5-4 probe shows the window logic itself fires correctly.
R-5 P3-2: my own probe hygiene.
Non-claims I endorse as honest: a valid signature does not assert OS facts (fixture-signed simulated evidence proves verifier conformance only); no protection against the box owner; nothing here is scientific or physical evidence — physical_harness_executed=false, paid_calls=0, verified in the reconstruction report.

Fix class: documentation/leaf-edge (P3-1), to the codex gate. No re-review trigger; council need not reconvene.

Short version, <user>: GO with one doc line. The subtractive discharge is the cleverest thing in this build and it's correct for a structural reason worth keeping: on discharge it returns the fixture verdict verbatim, so nothing the frozen path catches can ever be dropped — and I confirmed the discharge set is exactly the mechanical cascade by reproducing it on a clean graph. I tried to launder a defect through it three ways by corrupting the embedded V1 receipt; each one adds an error name outside the closure, which disables the discharge wholesale. Crash points behave: PENDING and BROKEN both refuse to yield a receipt, and a good receipt re-pointed at either store fails TRANSACTION_NOT_COMMITTED. Anti-replay held on all seven axes I could make fire. Custody fired on revocation, expiry, role collision and forged digest, all before any grid work. One thing to write down: a receipt verifies against any store holding the same committed transaction under the same store id — that's correct behaviour, not a hole, but it isn't in your non-claims and someone will assume otherwise. And my own confession, fourth round running: my first C2 probe compared a dict to [] and produced four meaningless "rejected" labels. Caught it, threw it out, re-ran at the real admission point. The probe-fire assertions are earning their keep.
