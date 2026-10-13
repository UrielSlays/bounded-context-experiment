# MBCX-01 SEAT1 (Opus 5, claude.ai) verdict — r13.2 — banked verbatim from the live seat thread

> Banked 2026-08-14 by the BUILD-lane driver from conversation `<id>`
> (CDP <council-browser-port>, the conversation named in `MBCX-01-COUNCIL-R13.2-DISPATCH-RECEIPT.json`), read-only
> attachment, `wait_quiesced` capture (state `indeterminate/lineage-unavailable` — expected: the
> banking session did not send the dispatch; text was settled and terminal). Reply text below is
> verbatim, including the tab's "Used Moonwalker integration" UI lines.

---

Used Moonwalker integration

Used Moonwalker integration

All 34 subjects verify, 145 tests, reconstruction PASS. Now the three required fresh attacks — C1 first.

Used Moonwalker integration, searched the web · 5 notes

Used Moonwalker integration, searched the web · 5 notes
MBCX-01 r13.2 — TARGETED CLOSURE CONFIRMATION
1. Verdict

CONFIRMED.

All three folded repairs are closed in the pinned bytes. Every required fresh attack was constructed by me, verified to be well-formed before I drew any conclusion from it, and rejected with a named error.

2. Seat, model, harness, longitudinal posture

Claude Opus 5, Moonwalker MCP harness (pwsh + CPython 3.11, read-only). Longitudinal: I carry my own r7–r13.1 lane and use it, labelled — in particular my own r13.1 P3-A (the paired_intervals naming precision item), which C1 now moots. Seal: I opened no r13.2 chat, output, log, marker or verdict from any seat. I did not open the two OpenAI seats' r13.1 verdicts either; I attacked the three named mechanisms directly so this pass stays independent of their framing. Paid inference: NONE. No experiment, provider, model, route, physical-harness, grid, or production-adapter call was made.

3. Pin, reconstruction, side effects
governing commit d97d654e : exists, ancestor of HEAD (which advanced 4x mid-session)
launcher blob    1bb8c15d : extracted via Start-Process; git hash-object == pin -> TRUE (4,455 bytes)
manifest blob    407a1cd7 : governing_commit field matches the packet commit
34 subjects at $Commit:$path -> git_blob + bytes + LF count + SHA-384 : MISMATCHES = 0
pinned launcher : exit 0; state/packets/cohort/measurement/inference/pipeline/integration ALL PASS
unit tests observed: 34 + 46 + 4 + 43 + 15 + 3 = 145   (packet claims 145 — exact)
no-paid report  : experiment_executed=false, provider_calls=0, paid_calls=0,
                  physical_harness_executed=false, top_level_readiness=DESIGN_OR_IMPLEMENTATION_FAIL

Delta vs r13.1: 34 subjects rather than 33 — the additions are MBCX-01-R13.2-NO-PAID-VERIFICATION-REPORT.json and MBCX-01-R13-CARRIER-EXACTNESS-SUITE.json. Both verify exactly.

Side effects: none to the repository. All mutation was on in-memory copies in %TEMP%; I re-verified afterward that the worktree trust root still hashes to the pinned blob (TRUE). The 46 dirty entries are not mine.

4. C1 / C2 / C3 scoreboard
C1 — exact EpisodeReceipt-to-outcome authority join → HOLDS

Required attack: two independently valid complete episodes for the same retained scenario, different outcomes, every local descendant hash repaired.

Probe validity first (I report this because two of my last three rounds produced a false reading from a malformed probe): my first two constructions did not produce distinct episodes — an OM-side a1_result mutation left episode_hash unchanged, so "B validates against A" was meaningless. I added an explicit assertion and rebuilt with a BC-side divergence plus full call-record repair (result_hash → raw_response_utf8 → raw_response_hash → parsed_response_hash → durability_receipt → call_record_hash). Only then:

PROBE CHECK -> episodes distinct: True | outcomes distinct: True
  A ep=8251CED23CD4 bits=(1,1)    B ep=D583944FC552 bits=(0,1)

both independently valid against their OWN episode:
  rA vs epA -> []      rB vs epB -> []

ATTACK 1  rB vs epA                                          -> ['SCENARIO_OUTCOME_AUTHORITY_INVALID']
ATTACK 2  rB, episode_hash swapped to A, receipt_hash repaired -> ['SCENARIO_OUTCOME_AUTHORITY_INVALID']
ATTACK 3  + all six call_bindings copied from A, rehashed    -> ['SCENARIO_OUTCOME_AUTHORITY_INVALID']
ATTACK 4  fed to inference over episode A (all three forms)  -> ValueError: EPISODE_PARTITION_MISMATCH

Attack 3 goes beyond the pinned witness: I copied episode A's own call bindings into B's receipt and rehashed, so the forgery was internally perfect at every level the caller controls. It still failed, because validation recovers each CallLedgerV3 and recomputes BC/OM from the exact ledgers rather than trusting the binding fields. Exact rejections: SCENARIO_OUTCOME_AUTHORITY_INVALID at the receipt boundary, EPISODE_PARTITION_MISMATCH at inference. This also moots my r13.1 P3-A: the scientific entry is now bound to an exact episode, not merely to a receipt shape.

C2 — correct TotalTerminatedProcesses semantics → HOLDS
pack string "<qqqqIIIIQQQQQQ" -> struct.calcsize = 96   (4 LARGE_INTEGER + 4 DWORD + 6 ULONGLONG)
clean baseline cell field: total_terminated_processes = 0

Attack 1 (must PASS): clean run, terminated == 0
  -> job-gate codes = []          all codes = ["MEASUREMENT_SIGNATURE_INVALID","PHYSICAL_HARNESS_UNAVAILABLE"]
Attack 2 (must FAIL): identical evidence, terminated == 1, every receipt hash refreshed
  -> job-gate codes = ["JOB_QUERY_EVIDENCE_INVALID"]

Attack 1 produces no job gate — the only two codes are the standing fixture sentinels, which are the honest BUILD boundary, not a failure of this gate. Attack 2 adds JOB_QUERY_EVIDENCE_INVALID and refreshing the hashes does not launder it.

Primary source re-opened as instructed, not taken from packet prose: learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_accounting_information, the Syntax block and the TotalTerminatedProcesses member. Field order confirmed exactly as the packet states, and the member definition is decisive — "The total number of processes terminated because of a limit violation." Not ordinary exits. The r13.2 semantics are correct, and requiring zero for a clean cell is the right reading. (Cross-check on the neighbouring members: ActiveProcesses is decremented when a terminated process exits and all references are released, which is exactly why final ActiveProcesses == 0 plus signed terminal lifetimes is the right proof of normal completion.)

C3 — carrier exactness authority and exact-build binding → HOLDS

CarrierExactnessReceiptV2 confirmed present: authority_mode: FIXTURE_CONFORMANCE, keys candidate_id, carrier_artifact_digest, measurement_grid_identity_hash, suite_id, suite_artifact_hash, witness_set_hash, producer_id, trust_root_id, result, receipt_hash.

C3-0  honest fixture receipt, fixture admission        -> ACCEPTED (honest)
C3-3  honest fixture receipt, PRODUCTION admission     -> CARRIER_EXACTNESS_AUTHORITY_UNAVAILABLE
C3-1a self-authored PASS + authority_mode=PRODUCTION + rehash -> ENGINEERING_SELECTION_INVALID
C3-1b suite_artifact_hash altered + rehash             -> ENGINEERING_SELECTION_INVALID
C3-1c witness_set_hash altered + rehash                -> ENGINEERING_SELECTION_INVALID
C3-2  replay across other build/grid identity + rehash -> ENGINEERING_SELECTION_INVALID
C3-2b replay across a different candidate + rehash     -> ENGINEERING_SELECTION_INVALID

Both required attacks land: self-authoring and relabelling fail, and replay across a different carrier artifact digest or full-grid identity fails even with outer hashes repaired. C3-3 is the important one — there is no production activation path: an otherwise honest fixture receipt fails production admission with CARRIER_EXACTNESS_AUTHORITY_UNAVAILABLE, exactly as §4 claims.

5. Findings

No P0, P1, P2, or P3 against the artifact.

P3 against my own method (recorded, not a defect in the bundle). My first two C1 probes were malformed — the OM-side mutation left episode_hash unchanged, and one earlier attempt used the wrong fixture class entirely. Had I reported from either, I would have filed a false pass on C1. Smallest fix, and I applied it: assert the divergence actually took (assert epA["episode_hash"] != epB["episode_hash"]) before drawing any conclusion. This is the third round in which my probe, not the artifact, was the thing that was broken; the assertion is now standing practice in my lane.

Residual carried, unchanged and correctly deferred (from my r13 §10 and r13.1 P3-B): the operator-independence witness — a StateAuthorityReceiptV1 whose postcommit_readback was produced by the same process that produced applied_child must be rejected in production mode. That belongs to BUILD artifact 1 and I do not reopen it here.

6. Direct answers

Are the three r13.1 fixes actually closed? Yes. C1, C2 and C3 all HOLD under fresh attacks I built myself, each rejected with a specific named error, and the C2 semantics are confirmed against the controlling Microsoft primary I reopened rather than against packet prose.

Can conceptual council rounds stop? Yes. The arc is unambiguous: r7 I killed it on arithmetic, r9 on two mutually inconsistent contracts, r10 on a repair lost in a rewrite, r12 on a missing sentinel-retirement rule, r13 on nothing but my own broken probe, r13.1 on nothing, and r13.2 on nothing. Six fresh attacks this round, six rejections. The conceptual surface is closed, and the only remaining risk lives in two artifacts that do not exist yet.

Is the next authorized step BUILD rather than experiment execution? Yes, and only BUILD. The top-level readiness is still DESIGN_OR_IMPLEMENTATION_FAIL solely because STATE_AUTHORITY_UNAVAILABLE and PHYSICAL_HARNESS_UNAVAILABLE are true — I verified that is the published boundary, not a hidden result, with experiment_executed:false, provider_calls:0, paid_calls:0, physical_harness_executed:false. This confirmation authorizes only separately reviewed implementation of (1) the production state-owner adapter/store/readback authority and (2) the production Windows Job/ETW evidence producer with custody-separated signing. It authorizes no provider calls, no route trials, no physical trials, no 100-cell grid, no 4,608 scientific calls, and no spending.

Cleanup and seal: probe directory, extracted launcher and run log removed and verified absent; trust root confirmed restored to pinned bytes. Two directories persist and neither is mine — the empty mbcx8 shell (r8 locked handle, disclosed since r10) and mbcx01-r12-… (r12 launcher scratch).

Short version, <user>: CONFIRMED, plainly. All three closed. The one worth telling you about is C1 — I built two genuinely different valid episodes for the same scenario, then copied episode A's own six call bindings into B's outcome receipt and rehashed everything, so the forgery was perfect at every level a caller controls. Still dead: SCENARIO_OUTCOME_AUTHORITY_INVALID, and EPISODE_PARTITION_MISMATCH at inference. It doesn't trust the bindings; it re-recovers the ledgers and recomputes the bits. C2 I checked against Microsoft's own page rather than your prose, and the member text settles it — TotalTerminatedProcesses is "processes terminated because of a limit violation," so requiring zero on a clean cell is right, and a nonzero value with refreshed hashes trips JOB_QUERY_EVIDENCE_INVALID. C3 has no production door at all: an honest fixture receipt under production admission fails CARRIER_EXACTNESS_AUTHORITY_UNAVAILABLE. One confession, third round running — my first two C1 probes were duds that left the episodes identical, and I'd have reported a false pass if I hadn't asserted the divergence actually took. That assertion is permanent in my lane now. Stop the rounds. Go build the two artifacts.
