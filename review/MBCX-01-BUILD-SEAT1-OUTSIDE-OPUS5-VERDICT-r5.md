GO-WITH-FIXES(COMMITTED-KEY-HARVEST-SCOPE · CEREMONY-CARRIER-DISCLOSURE)

Label: EXECUTED. One blocking fix, one disclosure fix. Both are edits inside existing functions/documents — no new machine, engine or subsystem, and neither fix is bigger than its defect. I did not complete items 2 and 3; that is stated plainly below rather than hidden.

Read-at-the-pin. I read the r5 packet at d122ee1 and ran everything against the working tree, having first confirmed it matches the content pin: `git diff --stat fce7b355 -- .` returns exactly two files — the r5 packet itself and MBCX-01-BUILD-PIN-MANIFEST.json (regenerated at tree head 7af1775). Every executable BUILD and frozen source file in the tree is byte-identical to fce7b355. Two untracked seat-3 r5 files sit in the tree; I did not open either — the round is sealed.

Read-only compliance: no repository byte created, edited or deleted. The pre-amendment tree was reconstructed from `git cat-file --batch` into %TEMP%; all probe scripts live in %TEMP%. No ETW session, no Job Object, no MBCX01_BUILD_ALLOW_PHYSICAL, no run-smoke-cell.ps1.

Green baseline reproduced: BUILD `Ran 125 tests … OK` (exit 0); frozen `Ran 147 tests … OK` (exit 0); verify-build-bundle.py real exit 0 (captured directly, not through a pipe) — seven sections PASS, frozen_suites expected 147 / tests 147, ledger invariants 46 / witnesses 125 / two_way_total true, trust_root_activated false, readiness BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED.

r4-F2 is CLOSED, verified independently. The regenerated manifest carries governing_commit: fce7b355… — the actual reviewed bytes — and reconciles 70/70 (38 subjects + 32 frozen dependencies) against the pin blobs on git_blob, bytes and sha384. (Aside, not a finding: those 32 frozen deps appear to drift when read from the WORKING TREE because core.autocrlf=true checks them out CRLF while the manifest records the LF blob. A future manifest-freshness arm written against the working tree rather than the object store would false-fire on all 32. Worth one line in the arm's comment when it lands.)

## Evidence read

MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r5.md:1-251@d122ee1 · mbcx01_build_trust_anchor.py:355-396 (the three production gates), :473-483 (_pem_base64_body), :486-516 (_read_der_tlv), :519-544 (ed25519_public_key_bytes), :547-589 (public_key_identity), :592-626 (strict_public_key_carrier_ok), :629-643 (_public_keys_in), :646-719 (harvest), :722-732 · mbcx01_build_measurement_authority.py:345-375 (production_activation_errors) · mbcx01_build_state_authority.py:492-504 · mbcx01_build_etw_consumer.py:880-892 (_start_key_text), :979-1038 (bind_thread_start_keys), :1041-1056 · mbcx01_r13_packets.py:34-52 (_unique_gold_action), :68-97 (project_state_world, the amendment) · mbcx01_r13_measurement.py:212-235 (amended candidate world), :363, :388 · verify-build-bundle.py:53-60, :261-267 · MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md:141-174 · MBCX-01-PACKET-SCHEMAS-v7.json:24,74,79,119 · MBCX-01-R13-MEASUREMENT-TRUST-ROOTS.json.

## SWEEP LOG

Honest capability note: I can reach the web this session. I spent my sweep budget in r4 on the two primaries that govern this fold's design — and this round's findings did not turn on a new external claim, so I did not open new sources. Labels below are exact.

- RFC 4648 §3.5 / §12 — **RECALLED** from r4, where I opened it at rfc-editor.org/info/rfc4648/ (Proposed Standard, not obsoleted). It is now quoted in the fold's own docstring at mbcx01_build_trust_anchor.py:557-560, and my r5 probe confirms the fold acts on it correctly. Not the deciding evidence for any r5 finding.
- CWE-1291 — **SEARCHED** in r4 at cwe.mitre.org/data/definitions/1291.html. I verified the correction landed: mbcx01_build_trust_anchor.py:676-677 and MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md:158 now read "mitigation phase is Implementation". r4-F3 CLOSED.
- RFC 8410 §3/§4 (Ed25519 SPKI, parameters absent) — **UNSEARCHED / NOT-LOAD-BEARING**. The fold cites it at :523 and :599. My false-refusal probe tests the property empirically against a real node:crypto SPKI export, which is the question that matters for the ceremony; I am not resting a finding on the RFC's text.
- ETW ThreadStart-vs-ProcessStart emission ordering — **UNSEARCHED / DID-NOT**, and this is the honest gap that caps my item-3 ruling (see below). I built the mechanical probe but ran out of tool budget before I could either fix my probe's start-key format or open a Microsoft primary on the ordering. I am not ruling item 3.
- Internal shelf, spot-run (EXECUTED, r4): `EVENT_TRACE|TracePmc|CSwitch|ProcessTrace` → 0 files across bridge src/, Photon crates/, Gravity src/. §9's "first-of-kind" claim verified. §9's ADOPTED claim also verified in the bytes: :525-527 cites crl-authenticate.ts:109-120 / der-reader.ts and the code is that pattern. The shelf gap I raised in r4 was closed by adoption, not by argument.

## Findings

### F1 — BLOCKING · EXECUTED · item 5 ("refuses only what it should" — the MISS half) · I13/I14

A committed key whose private half ships in this repository is still admissible as a production signing root, because the harvest keys on a FILENAME SUFFIX and the one document most likely to be copied does not carry it.

The harvest (:704-706) selects on `name.endswith(".fixture.json")`. `MBCX-01-R13-MEASUREMENT-TRUST-ROOTS.json` is committed, is not `*.fixture.json`, and carries a `public_key_pem`. Executed:

```
harvest = 5 keys, all from *.fixture.json documents
MBCX-01-R13-MEASUREMENT-TRUST-ROOTS.json -> ED25519:D75A9801…511A | in harvest: None | carrier_ok: True
```

Its private half is committed. Derived via node:crypto from the PKCS#8 keys pasted in the test modules:

```
test_mbcx01_r13_measurement.py -> ED25519:D75A980182B10AB7D54BFED3C9 | harvested:None | == r13 root: True
test_mbcx01_r12_measurement.py -> ED25519:D75A980182B10AB7D54BFED3C9 | harvested:None | == r13 root: True
```

Driven through the folded door, differentially against the fold's own control:

```
CONTROL  key from a *.fixture.json                 -> errors=['PRODUCTION_SIGNING_KEY_FIXTURE_MATERIAL']
PROBE    key from R13-MEASUREMENT-TRUST-ROOTS.json -> errors=[]   <== ADMITTED
```

**Data consequence — ADMITS WRONG EVIDENCE.** Measurement receipts signed with a private key committed in this repository clear `production_activation_errors` and become experiment-eligible. A number in the result could be produced by test material. This is the identical class the fold closed, one document over — and the document in question is named MEASUREMENT-TRUST-ROOTS, i.e. it is the most natural template for a DESIGN_CONFIGURATION_EDITOR authoring the production manifest at ceremony §3 step 3, more so than any `*.fixture.json`. The state plane reads the same harvest (mbcx01_build_state_authority.py:501-503) and therefore has the same hole; I executed the measurement plane only.

In-model check: this is an honest-operator copy of a committed template, not an actor evading a check. It is the exact scenario §3 step 3 warns about in prose.

False-refusal check on the fix (the direction that matters): widening the harvest cannot refuse a legitimate ceremony key, because a key generated inside the custody backend at §3 step 2 does not appear in this repository at all. The only keys added to the refused set are keys that are, by definition, already public here. I did not run the suites under a widened harvest — that is the builder's step, and it is the one thing to check before landing.

### F2 — NON-BLOCKING · EXECUTED · item 4-inverse (the false-refusal direction)

A correctly generated custodian key is admitted; three realistic transport accidents refuse it, and one of them refuses with a code that tells the operator nothing.

Generated a real Ed25519 keypair the way the ceremony will (node:crypto, `export({type:'spki',format:'pem'})`) and drove the whole `MBCX01_BUILD_OWNER_TRUST_ANCHOR` door:

```
A real custodian key, node/openssl PEM  -> ADMITTED ctx=True code=None
Same key, CRLF line endings             -> REFUSED OWNER_TRUST_ANCHOR_INVALID
Same key, trailing newline stripped     -> REFUSED OWNER_TRUST_ANCHOR_INVALID
Same key, body wrapped at 32 chars      -> REFUSED PRODUCTION_VERIFIER_CONTEXT_KEY_CARRIER_INVALID:…
```

The headline is good news and I want it on the record: the fold does not refuse the emitter the ceremony actually uses. `strict_public_key_carrier_ok` accepts the canonical node/openssl SPKI PEM verbatim.

The residual is diagnostic, not gating. CRLF and a stripped trailing newline are refused by `OwnerTrustAnchor.__init__:242-243` — checks that PRE-DATE this fold, so the fold did not introduce them — but they surface as the generic `OWNER_TRUST_ANCHOR_INVALID`, the same code a typo'd anchor_id or a wrong algorithm produces. A custodian on Windows who pastes a PEM through a tool that writes CRLF gets a refusal that does not point at line endings.

Meanwhile the ceremony document is now stale in the safe direction and silent in the risky one:
- :152-153 and :161-162 still say the known-key set derives from committed ANCHOR documents. The fold widened it to every `public_key_pem` in every `*.fixture.json`. The doc UNDERSTATES what the code does.
- The doc has no line anywhere naming the carrier requirement. Grepping it for CRLF, line ending, newline returns nothing. Step 2 says only "exports ONLY the public key (SPKI PEM)".

**Data consequence — REFUSES RIGHT EVIDENCE.** A legitimate custodian key can halt the ceremony, loudly but uninformatively, with the runbook offering no pointer. It cannot corrupt a number and it cannot pass silently.

Explicitly not proposed: do not normalise line endings on input. That would loosen a check to fix a documentation gap. The fix is a ceremony line plus, optionally, splitting the PEM-shape refusal out of `OWNER_TRUST_ANCHOR_INVALID` so the message names the field — a message-text edit.

> ⚖ DRIVER ADJUDICATION (recorded here beside the verdict, 2026-08-15): seats 2 and 3 both ruled the OPPOSITE — normalize the RFC 7468-permitted spellings. The driver ruled WITH seats 2/3 and AGAINST this paragraph, on the merits: key identity is computed from the DECODED key, so EOL normalization cannot admit a wrong key, while refusing CRLF can block the ceremony on Windows where CRLF is native. Seat 1's other half was ADOPTED — the ceremony doc gap and the uninformative refusal code are real and are tracked. See MBCX-01-R13-AMENDMENT-2 and the r5 synthesis.

### F3 — RESIDUAL, worth one manifest row · EXECUTED · item 1 + §7 (the amendment's hash ripple)

AMENDMENT-1 changed the retained-cohort root, every internal equality stayed green, and nothing anywhere records what the root was.

I reconstructed the pre-amendment tree at 5d05755 and ran the same digest probe under both. The science is unmoved — and this is the answer to item 1's wrong-number question:

| | pre | post |
|---|---|---|
| candidates | 960 | 960 |
| scenario_ids digest | e02fd62a… | same |
| gold_action_id_by_cut over all 960 | 5251372d… | same |
| action_ids_by_cut over all 960 | abacccf9… | same |
| canonical world stripped of the two new fields | 98452636… | same |
| canonical state stripped | 5356444e… | same |
| fixture manifest gold_action_id | ACT.B13770AB… | same |
| gold_read_set, expected_a1_action_ids, action_catalog_hash, bc_selection_hash, route_contract_hash | — | all same |
| retained_total | 768 | 768 |

So: the amendment adds exactly two fields and moves nothing else. No gold answer, no action legality, no membership. `_unique_gold_action:42-49` reads only lifecycle/critical/due_at/prereqs and never touches subject_id/owner_role, which is why. Item 1's claim holds.

What DID move, as expected, is the hash ripple: canonical_world_hash, source_candidate_hash, source_provenance_hash, manifest_hash, authority_hash, and:

```
retained_set_root  PRE  B51F85FF8958EAEF…C264D663
                   POST 38A62E8C26224FC7…3012AE6F
```

I searched every committed *.json/*.md/*.py/*.txt/*.ps1 for both values: neither appears anywhere. `retained_set_root` is used at mbcx01_r13_packets.py:152, 189, 530, 1353 purely as a MUTUAL binding — manifest ↔ authority ↔ receipt, all recomputed from the same code and compared to each other — and verify-r13-normative-bundle.py:127 asserts only `len(selected) == 768`. The join is self-consistent by construction: a generator change re-roots every party at once and every equality still holds.

**Data consequence — WRONG NUMBER, latent.** A future generator edit that changes cohort MEMBERSHIP rather than just adding fields would produce a different 768 with every internal check green and nothing to compare against. AMENDMENT-1 is the live demonstration: the root moved and no verifier noticed.

Honest weight. This is narrower than it first looks. The pin manifest hashes mbcx01_r13_measurement.py and the generator JSON by sha384, so a CODE change is caught by the pinned run — the missing piece is only "and did that change the cohort". So: a residual, worth one owner-ratified row (retained_set_root + retained_total + the scenario-id digest) in the pin manifest or repair ledger plus one bundle assertion. The value to pin is the post-amendment root. Not a NO-GO, and I would not fold it without the owner ratifying the number.

### F4 — CLEAN · EXECUTED · item 7 (FROZEN_TEST_TOTAL 145 → 147)

The guard is a real gate in both directions, not a loosened one:

```
guard at 147 (declared)             -> PASS tests=147 expected=147
guard at 145 (pre-amendment number) -> RAISED VerificationFailure: 147 != 145
guard at 148 (a frozen test added)  -> RAISED VerificationFailure: 147 != 148
```

Its one structural limit — a COUNT-PRESERVING frozen edit — is covered by the pin manifest's sha384 over all 32 frozen dependencies, which I verified reconciles at the pin. No finding. The declaration at :56-60 names the amendment and its record file, which is the right way to move a number like this.

> ⚖ DRIVER ADJUDICATION: seat 3 ruled this a DEFECT (a wholly replaced 147-test suite passes). Both are right about different things — the driver confirmed at the byte that verify-build-bundle.py does NO byte-checking of frozen modules (its only digest work is JSON parity), so the BUNDLE alone is blind, while the separate pinned run does bind bytes. Resolved to the already-tracked owed bundle arm, not a new class. The r5 packet's own item-7 claim ("the guard still fails on any frozen-suite change") was FALSE as written — driver defect, recorded.

### F5 — CORRECTION TO MY OWN PROBE · disclosed rather than reported as a finding

My first differential run showed `fixture_minus_amendment` differing pre/post, which looked like an unexplained ripple. It was my error twice over: candidates key their world under `canonical_world_by_cut`, not `canonical_world`, so my candidate strip was a silent no-op; and the fixture manifest carries canonical_world_hash/manifest_hash/source_candidate_hash computed over the amended world, which stripping two fields cannot undo. Re-run with a recursive strip, the world and state digests match exactly. There is no unexplained ripple. I am recording this because a seat that reported the first run as a finding would have cost the lane a round.

## What I did NOT rule

Stated plainly, because a verdict that quietly covers everything is worth less than one that says where it stopped.

- **Item 2 (ETW fault posture)** — READ the fold's new refusals (ETW_TRACE_DRAIN_INCOMPLETE, ETW_LOSS_QUERY_AFTER_SESSION_STOP, ETW_TRACE_NOT_STOPPED, the _drain_faults/_loss discipline at teardown) and the posture reads correct: loss counters are read while the session is alive, an unproven drain does not block teardown but capture() still refuses on the record. No fresh probe run. **Not ruled.**
- **Item 3 (thread start-key binding)** — this is the one the packet flags as highest-value and not driver-executed, and I got closest to it without landing it. I read bind_thread_start_keys:1031-1036: the bind takes the last ProcessStart with `started <= qpc` and NEVER CONSULTS ProcessStop. Two orderings look mechanically mis-binding on that logic — a thread event falling in the dead gap between a ProcessStop and the next ProcessStart for a reused PID, and an initial thread of the new incarnation timestamped a tick before its own ProcessStart. My probe faulted on _start_key_text's 16-hex-digit format (my inputs carried a 0x prefix), and I hit the tool limit before re-running with valid keys. This is an UNRUN HYPOTHESIS and I am labelling it as one. It also has a genuine SWEEP dependency I did not discharge: whether Windows actually emits ThreadStart before ProcessStart for an initial thread is a platform fact needing a Microsoft primary. A seat should finish this: the consequence if it lands is exactly the packet's — another incarnation's retired instructions inside our count.
- **Item 6 (positive-lane key swap)** — the 125 green and the driver's banked 120/5/zero-collateral control are reproduced, but I picked no witness and broke nothing. **Not ruled.**
- **§8.5 (machine-wide Kernel-Process, no member filter)** — I cannot show it corrupts a number, so per §0 I leave it as the packet has it: a smoke-run blocker, tracked, not this round's subject.

> ⚖ DRIVER NOTE: seat 1's unrun item-3 hypothesis was INDEPENDENTLY CONFIRMED by seats 2 and 3 and then reproduced at the byte by the driver — the thread in the dead gap was ADMITTED against the stale incarnation. Seat 1 called the mechanism correctly from reading alone and said so honestly rather than claiming it.

## Residual risks

- **The unruled half.** Items 2, 3 and 6 carry no fresh probe from me. If no other seat probed item 3, the round is incomplete on the packet's own highest-value ground.
- **F1's fix is one of a class, and the class is "which committed documents count".** Widening to every committed `*.json` closes the document I found. It does NOT close a key whose public half is committed only in a `.md`, a `.txt`, or a witness-run bank. The durable framing is "published anywhere in this repository", and the durable check may simply be that the ceremony's step-2 export is compared against the repo once, at ceremony time.
- **F3's pin must be owner-ratified, not folded.** Pinning retained_set_root writes a scientific constant into the record; the value to pin is the one AMENDMENT-1 just produced. That is the owner's number to bless.
- The named gap survives unchanged: `FIXTURE_NON_ANCHOR_PRIVATE_KEY_PEM`, whose public half appears in no committed document, remains outside the derived set (:685-693). Accurately disclosed in both code and ceremony doc.
- No claim the consumer works. Unchanged and correct — it has still never run against a live session.

## Fix class

| # | Class | Scope | Gate |
|---|---|---|---|
| F1 | COMMITTED-KEY-HARVEST-SCOPE — widen the harvest selector at mbcx01_build_trust_anchor.py:704-706 beyond the `.fixture.json` suffix to the committed documents that publish key material, MBCX-01-R13/R12-MEASUREMENT-TRUST-ROOTS.json included. One selector, existing function. Add a red witness using the r13 root key on both planes. | committed_fixture_key_material; two witnesses | Admission semantics ⇒ §13 re-review trigger fires. Must close before the key-custody ceremony. Confirm the 125 stay green under the widened harvest — that is the whole risk of the fix. |
| F2 | CEREMONY-CARRIER-DISCLOSURE — one line in MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md §3 step 2 naming the accepted carrier with a one-line normalisation command; correct :152-153 and :161-162 to say the harvest covers every `public_key_pem` in every committed fixture document. Optionally split the PEM-shape refusal out of OWNER_TRUST_ANCHOR_INVALID. | ceremony doc + one message string | Doc + leaf; codex-CLI gate. Before the ceremony. |
| F3 | COHORT-ROOT-PIN — record retained_set_root / retained_total / scenario-id digest as a pinned constant and assert it in the bundle. | pin manifest or repair ledger + one bundle assertion | Owner's number to ratify, then a bounded edit. Not a blocker for this commit. |

On the GO. My verdict is EXECUTED and can serve as a deciding vote — with the caveat that it rules items 1, 4-inverse, 5 and 7 and does NOT rule 2, 3 or 6. GO-WITH-FIXES rather than NO-GO because readiness is BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED: no ceremony has run, no production root exists, and F1 corrupts no number that exists today. It corrupts the ceremony that has not happened yet. **If any part of this round is read as authorising that ceremony, my vote is NO-GO until F1 and F2 close.**
