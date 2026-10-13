# SEAT1 (claude.ai, NEW-ACCOUNT seat) — cohort-content design r1 verdict
Banked by the driver 2026-08-16 from conversation <id>
(CDP <council-browser-port>, relaunched council Chrome). PROVENANCE DEVIATIONS, recorded not hidden: the prior
seat's account ran out of credits mid-round and its in-flight verdict was lost; the OWNER
minted this conversation and pasted the round-1 dispatch text himself (driver's card/read-probe
/model-at-mint ritual NOT performed by the driver; the seat self-declared sealed/read-only and
its file access is proven by execution — pinned blob hashes + executed probes below; the model
label was not captured before message one). The dispatch text carried the driver's fabricated
40-hex SHA; the seat caught it as F0 and resolved via the packet's committed pin. Verdict
below is a faithful driver transcription (tables reflowed to prose, no content dropped); the
byte-exact original remains in the seat thread at the conversation id above.

---

COUNCIL VERDICT — MBCX-01 cohort-content generator DESIGN r1 (issue #17)

Seat: independent, sealed, read-only. No repo file written; all probes executed in-process from C:\ with the lane on sys.path. No other seat's view sought or seen.

0. PIN CONFIRMATION — and one pin defect at the dispatch layer

Read: packet MBCX-01-COHORT-CONTENT-DESIGN-COUNCIL-PACKET-r1.md @ 5ec09d6503084dcac86eb1395bae71ceb0a4c3ae (blob 68b8cec3307d5444…, 17,482 B, 246 L); design MBCX-01-BUILD-COHORT-CONTENT-DESIGN.md @ b18d7ab58f6ae45c2e5d309f071db79ead9d4886 (blob 8199a6fcfec99faa…, 15,221 B, 200 L). Worktree HEAD 98e7f7d; git diff --stat <pin> -- <design> empty — pinned reads. Frozen-byte pins: mbcx01_r13_measurement.py A348A453… · mbcx01_r13_packets.py 57FBA7E8… · verify-build-bundle.py 345AE87D… · MEASUREMENT-CONTRACT-v7.json F1F29E2E….

FINDING F0 — dispatch carried a fabricated 40-hex (EXECUTED). b18d7ab196325715466246a67e9d686e8163de4c does not exist (git cat-file -e exit 1); the real commit abbreviated b18d7ab is b18d7ab58f6a…. Note git rev-parse --verify echoes the bad 40-hex back without erroring — the check most seats would reach for fails to catch this. The packet is not at fault (7-char pin resolves). Consequence: wrong evidence admitted — a seat trusting the 40-hex and falling back to the tree would review unpinned bytes as pinned. Fix: pins only as emitted by git rev-parse; cheap gate: git cat-file -e on every pin before send.

Packet premise re-verified: cohort and grid are disjoint objects in contract v7 (key sets enumerated; no H/D/F under cohort). §2.4's H/D/F deferral rests on real bytes. CONFIRMED.

1. VERDICT: NO-GO — Label: EXECUTED.

Narrow, not a redesign. The diagnosis (C1) is correct — confirmed more strongly than the design states. The central mechanism (journal-as-canonical-state, replay-derived eligibility, seedless framed-hash determinism, versioned-sibling pattern) is sound in kind and should be adopted. What fails: completeness of the build surface and three invariants. Six defect classes; two are architecture/interface-level and trip the packet's own re-review trigger.

F1 manifest builder is a second, independent stamp → wrong number produced
F2 BUILD population cannot reach the frozen consumer; one module named where ≥3 needed → right evidence refused
F3 _source_authority does not bind the journal (resolves Item 7c AGAINST the design) → wrong evidence admitted
C3 ≥128 floor vs meaningful filtering in quantitative tension (97.3% fault at meaningful rates) → right evidence refused
C5 coverage invariant vacuous for omissions; record_call_response in NO motif family → wrong number produced
F4 the design's own falsification sentinel is unwitnessed → wrong number produced

No finding proposes a person-blocking control; every refusal stops a wrong number.

2. C-RULINGS

C1 SOUND (EXECUTED) — 960 generated; distinct worlds across ALL 960 = 1 (identity is GLOBAL, not merely per-motif — the design understates); declared eligible {True: 2880}; catalog histogram {1: 2880}; one action id population-wide; predicate rejected 0; predicted lowest-128-per-motif == actual retained (symmetric diff 0). Line cites :253/:317/:321/:329 byte-verified; six-code vocabulary at :277-301 confirmed. Two immaterial prose corrections (_candidate_world spans :203-240; global-not-per-motif identity).

C2 DEFECTIVE (EXECUTED+SEARCHED) — (a) the exogenous observation axis is load-bearing and unvaried: _expected_gold_read_set (:63-64) adds every OBSERVATION unconditionally to the gold read set; :78's mismatch check covers obligations/dependencies only; §2.1's variation axes contain no observation axis ⇒ read-set discrimination partly rides on an unvalidated, unvaried quantity. (b) I15 leverage is a pseudo-oracle stated as a proof — agreement establishes consistency, not correctness; a shared legality bug becomes an unfalsifiable property of all 768 and W5 goes green on it. Fix: observation axis + generation-time validated shape (or remove from gold read set with reasons); restate I15 as consistency-not-correctness with a third check at the legality frontier.

C3 DEFECTIVE (EXECUTED) — exact binomial, n=160, floor breaks at k>32: p=0.15 ⇒ P(any motif faults)=0.187; p=0.20 ⇒ 0.973; p=0.25 ⇒ 1.0. The stated intent (selection does real work) requires the fraction that breaks the floor — or the builder quietly tunes to 5-10% and filtering is token. AND bias: ambiguous-gold ineligibles correlate with richer worlds, truncating the retained set on the complexity axis BC/OM exists to exercise. Fix: QUOTA placement (rank by framed_hash within motif, take exactly k ≤ 32, declared constant), stratified across the three ineligible shapes, with a retained-vs-rejected world-size distribution witness.

C4 SOUND (READ-ONLY) with caveat — constraint enforceable pre-replay, W9 witnesses it, edits no frozen semantics; honest close (amending A1-gold reopens r13.2's 3/3). Caveat: makes target-reopen unreachable in the scored window ⇒ record in §5 as a POPULATION EXCLUSION, not merely a #23 wording note.

C5 DEFECTIVE (EXECUTED+SEARCHED) — (a) record_call_response appears in no family (16/17 named; it has payload contract common.py:55, handlers in both reducers, its own conflict code, live packet-layer use at packets.py:442). (b) The invariant is scoped to each family's self-declared legal set, so an event omitted from every family is vacuously covered — W4 green over a population that never exercises a live mechanism. Prior art: each-choice/1-way is the weakest combinatorial criterion (NIST). Sub-finding: the cross-scope collider is structurally invisible — project_state_world:70 reads only the manifest scope; the motif's phrase implies a mechanism the projection refuses to carry. Fixes: invert the invariant against the alphabet with named exclusions; raise above each-choice (≥ pairwise over mechanism × lifecycle-position) or justify 1-way; say where the collider becomes visible or drop the motif's semantic claim.

C6 SOUND (EXECUTED) — measured against the real shape + canonical JSON + ENVELOPE_BYTES=65536 (packets.py:18): 5-obj fixture 3,479 B; 58-obj 24,733 B; 98-obj 31,533 B; 196-obj 61,315 B FITS; 392-obj 120,879 B OVERFLOW. Real ceiling ≈190-200 world objects / ~61 KB ⇒ safe deferral at design scale. Minor fix: record the measured bound as a declared constant + add a served-size witness (no W asserts size < ENVELOPE_BYTES).

C7 DEFECTIVE (EXECUTED), narrow — within the declared namespace the two-way totality is tight (:559-576, :598-605, :608-652 traced), but everything is scoped to the hand-maintained BUILD_TEST_MODULES tuple; nothing cross-checks the filesystem globs against the tuples (both directions), so an unregistered test module leaves a green bundle that never covered it. Also unnamed in §3: BUILD_WORK_PRODUCTS (:155). Fix: glob-vs-tuple two-way totality for modules and test modules + a W for it.

3. OWN FINDINGS (each EXECUTED unless noted)

F1 (primary) — manifest_for_retained_candidate (packets.py:158-196) hard-codes scope "SCOPE.SHARED" (:163), target from literal "OBL.SHARED" (:164), decoy "OBL.DECOY" (:165), a fixed three-entry catalog NOT read from action_ids_by_cut (:167-173), bc_selected_object_ids = ["OBL.SHARED","OBS.SHARED"] (:184). Executed over 40 retained: distinct catalog/world/gold_read_set/bc_selection/manifest-minus-ids = 1 each. §2.1's catalog axis cannot reach the served packet; generator-only fix leaves the packet a stamp with all nine witnesses green. The packet's consumer enumeration names this function; the design never diagnoses it. Fix: a BUILD manifest sibling deriving scope/target/catalog/BC-selection from the candidate + a W that different catalogs yield different served manifests.

F2 — retained_scenario_authority (:370-395) issues authority only for byte-exact members of the frozen synthetic cache (:337-345); renaming scenario_id or target ⇒ RETAINED_SCENARIO_AUTHORITY_INVALID. W7's "I01-equivalent BUILD authority path" needs ≥3 modules (generator · selector/authority sibling · manifest sibling); §2/§3 name one. Fix: enumerate the full module set and map each W to its carrier.

F3 — _source_authority (:191-200) = fixed nine-key digest, no journal term. Executed: add event_program to every candidate ⇒ digest UNCHANGED, validate_source_provenance []; SWAP one candidate's program (open_obligation→cancel_obligation) ⇒ provenance identical, []. Resolves the design's open Item 7c AGAINST it. Fix: event_program_hash (+ observation_authority_hash if observations stay exogenous) in the BUILD sibling + a journal-only-mutation red witness (W6 covers a different, later gate).

F4 (READ-ONLY) — §6 Item 0's sentinel ("if the retained 768 still cannot produce differing BC/OM read-sets, this design failed") has no witness; given F1 (measured distinct gold_read_set = 1) it is the single most important thing to witness. Fix: W10 — read-set variance across the retained 768, non-degenerate BC/OM difference. Red today by construction.

4. RED-WITNESS NON-DISCRIMINATION ATTACK — seven defect classes no declared W catches: F1 (no cross-candidate served-manifest comparison) · F3 (no journal-only mutation) · C5a (vacuous for omitted events) · C5b (presence, never interaction) · C6 (no size witness) · C7 (no registration totality witness) · F4 (no sentinel witness). The witness set is under-discriminating against the design's own failure modes.

5. WHY-THIS-EXISTS — ALREADY-BUILT verified (14 mbcx01_build_*.py listed, no cohort generator; pipeline executed end-to-end; shelf-log queries spot-run). PRODUCT-FIT clean (every refusal examined stops a wrong number; none stops a person). BIGGER-THAN-THE-BUG: yes and more than claimed — TWO stamps in TWO layers, the second never named in any council round. PRIMARY-CONSUMER: the design's weakest point — the named primary consumer cannot consume the proposed population (F2) and would flatten it if it could (F1).

6. OMISSION ATTACK — the manifest builder's own hard-coded literals (enumerated as consumer, never diagnosed) · the observation axis · record_call_response + an invariant shaped never to surface the omission · BUILD_WORK_PRODUCTS in §3 · the reopen constraint as population exclusion. Determinism candidate largely clean (UTF-8-byte sorts throughout; no floats/locale; one unstated dependency: sha384(row) order-independence rides the canonical encoder — low severity).

7. SWEEP LOG — SEARCHED at origin: Groce/Zhang/Eide/Chen/Regehr "Swarm testing" ISSTA 2012 (feature-omission mechanism; 104 vs 73 distinct crash bugs) · NIST ACTS/Kuhn-Kacker-Lei (each-choice weakest; interaction rule 4-6-way) · differential-testing-as-pseudo-oracle. RECALLED (argument only): QuickCheck lineage; Hypothesis stateful swarm. All lane-byte claims UNSEARCHED(SETTLED-BY-PINNED-BYTES). Stopped when all three prior-art-bearing claims had an origin-opened source.

8. PROPOSE — Build the journal-replay generator as designed PLUS: (a) a swarm layer — per-candidate hash-derived omission configurations over the 17-event alphabet with the six r4 motifs as named anchor configurations rather than a partition (fixes C5a for free: omission becomes an explicit declaration); (b) alphabet-scoped coverage MEASUREMENT (1-way + 2-way over event × lifecycle-position) reported in provenance; (c) restate I15 honestly. Differently: land generator AND manifest builder in ONE slice (a generator-only slice = a green bundle over an unfixed instrument — the worst outcome, because green stops the next person looking); make the floor constructive via quota; invert the coverage invariant. Keep: journal-as-state, seedless determinism, Boolean-pop, sibling pattern, reopen ruling, no Merkle tree.

9. OMISSION SET (what this seat did NOT do) — did not execute the reducers (C2's byte-identical-agreement assessed on structure; a seat should execute a replay pair before r2 closes C2) · did not run the frozen suites or the bundle end-to-end (C7 traced, not demonstrated) · did not read the governing DoR set this session (accepted the packet's no-threat-model premise as frozen; re-run the grep) · did not verify the r2/r7/r11 seat cites or design-history line ranges · did not test _unique_gold_action against a multi-action catalog (C3 bias analytic, not executed) · did not quantify F1's downstream blast radius · did not sweep preregistered-cohort/metamorphic (NOT-LOAD-BEARING).

Verdict: NO-GO. Label: EXECUTED. Re-round narrow — the diagnosis and the journal-replay core survive intact; what must land before build: the second consumer (F1/F2), the journal binding (F3), the quota discipline (C3), the alphabet-scoped invariant (C5), and a sentinel witness (F4).
