# MBCX-01 COHORT-BUILD acceptance council packet — r1 (the cohort engine CODE)

Packet prose is a pointer map, not evidence — byte-check it.

ROUND LEDGER: cohort-BUILD acceptance council round 1 (this arc is FRESH — the cohort
CONTENT DESIGN arc closed GO-TO-CODE at its r3: r1 3× NO-GO · r2 GO-WITH-FIXES/NO-GO/NO-GO ·
r3 ROUND CALLS 2-1 GO-TO-CODE; the CODE under review has had driver audits and mechanical
gates only, zero seat rounds) · codex rounds 0 of 2 — a code lane; the two design-gate codex
rounds were spent on the DESIGN and are exhausted; the CODE goes to codex-CLI literal green
AFTER this arc (issue #1), serialized after the seats.

## 0. What this round is for

**NORTH STAR: the numbers this instrument produces must be true.** This lane is a research
harness for a scientific experiment. No network service, no production runtime, no external
submitter; every caller is the harness and its own tests. The design of record carries **no
threat model** — verify in one command from the repository root:

```
grep -niE "threat model|adversary|attacker|untrusted|api-caller|hostile" \
  MBCX-01-EXPERIMENT-DESIGN-r9.md MBCX-01-R13-CLOSURE-ARCHITECTURE.md \
  MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md
```

(Zero hits — driver re-ran it at the §2 pin, 2026-08-16.) A finding counts iff it names its
wrong-number / wrong-admission / wrong-refusal consequence for the experiment's data.
⛔ No new machines: the owner's standing rule is *"don't build crazy machinery to protect an
experiment that has no adversary"* — when a finding's remedy is a wall, a census-scanner, or
a gate on a person, the honest level-up is usually DELETING a wrong restriction, and a
severity label is not authority. This round reviews the COHORT ENGINE — the three BUILD
siblings + their suite that produce the 960-candidate population, retain 768, and carry them
to the frozen inference core. It is the experiment's actual scenario population: a defect
here is a wrong number in every downstream result.

## 1. Verdict contract

First line: **GO / GO-WITH-FIXES(class) / NO-GO**. Code artifact — no round-call token, skip
the design questions. Then: evidence read (`path:line`), SWEEP LOG, findings labelled
EXECUTED/READ-ONLY each naming its data consequence, residual risks, fix class. Whole
verdict in-thread; write nothing to disk.

## 2. Canonical bytes (path@sha pins)

Governing CONTENT commit under review: **`f35851e94b73731dc9cb5db8cb7085471d4c1bac`**
(both pins `git cat-file -e` gated). HEAD at dispatch is
`dc064fbe53e8e1dfbbaa361aa629612d87d3b5fb`; every commit between them touches docs/records
only — driver verified `git diff --stat f35851e dc064fbe -- '*.py'` is EMPTY, so reading the
tree at HEAD reads the pinned code bytes. Under review:

- `mbcx01_build_cohort_generator.py` (1,326 L) — programs, motifs, observation
  projection/derivation, plan arithmetic, census, sequence coverage
- `mbcx01_build_cohort_authority.py` (671 L) — spec artifact load, provenance sub-digests,
  declared-eligibility refusal, selection, instance-scoped retained authority
- `mbcx01_build_cohort_packet.py` (1,073 L) — manifest derivation/validation, ghost-FACT
  discriminator, W10 sentinel, exact-subtractive scorer wrapper, scenario-outcome seam,
  the BUILD inference ingress
- `test_mbcx01_build_cohort.py` (2,431 L) — 32 witnesses (bw94-99 · bw23 · bw64 · bw70-79 ·
  bc01-bc14)
- `MBCX-01-BUILD-COHORT-GENERATOR-V1.json` — the committed spec artifact (constants + the
  committed identity block)

Design of record (context, already council-closed — review the CODE against it, do not
re-round the design): `MBCX-01-BUILD-COHORT-CONTENT-DESIGN.md` r6 FINAL. Frozen layer:
untouched this slice; `FROZEN_TEST_TOTAL` 156 stands.

## 3. Immutable truths / invariants

- The frozen r13.2 layer + amendments A-1/A-2/A-3 are settled; zero frozen `.py` files
  changed in this slice (the 07b11b11 commit amended frozen DOC prose only, owner-ratified
  #23). The 17-invariant matrix rule, authority modes, and readiness
  (`BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`) stand.
- Frozen couplings the code lives INSIDE (recorded, not fought): `MANIFEST_KEYS` closed ·
  motif taxonomy frozen to the six · `retained_position < 768` at `mbcx01_r13_packets.py:222`
  and `mbcx01_r13_measurement.py:1501` · `_unique_gold_action` is a frozen private name.
- ENGINE-FIRST owner ruling (2026-08-16) governs; the on-contact discriminator applies to any
  finding whose remedy gates a person.
- Nothing here authorizes an experiment, route trial, spend, physical run, or frozen edit.

## 4. Claims to attack — each carries its adversary declaration and a construct-the-bypass ask

1. **The replay gate is honest end-to-end.** Every candidate's 17-step program replays
   through BOTH frozen reducers with byte equality, an EXPECTED result code per step, and a
   legality cross-check between two independent predicates at every frontier
   (`ProgramReplay.apply`/`_legality_frontier`, generator :232-296).
   ADVERSARY: internal-consistency — a recorded journal whose replay does not reproduce it.
   REACHES IT VIA: `replay_event_program` (packet :203-230), which by default re-derives with
   the REFERENCE reducer alone, bound by the recorded state digest
   (`authoritative_state_hash_by_cut`).
   Attack: is digest-binding as strong as the dual gate at every downstream re-derivation
   site? Construct a candidate whose recorded codes or digests lie and find the path that
   swallows it.
2. **Eligibility is DERIVED and nothing reads a declared Boolean back.**
   `candidate_is_eligible` (packet :359-376) reads NO stored flag — §2.5's envelope refusal
   is enforced structurally (a non-servable draft is REBUILT as a shape the predicate itself
   refuses); `DECLARED_ELIGIBILITY_KEYS` are popped and refused by name (authority :369-397).
   ADVERSARY: author-blind-spot — a read-back path the pop list does not cover.
   REACHES IT VIA: `select_build_cohort` (authority :461-504), which itself WRITES
   `eligible` / `eligibility_source` / `retention_hash` / `chosen_cut_id` onto retained rows
   that are then sha384-hashed into the retained-set root.
   Attack: does any validator re-admit those enriched rows as candidates (key-set equality,
   `BUILD_CANDIDATE_KEYS`)? Is the enrichment a second authority surface? Is any admission
   flag (`envelope_admitted`) ever read back anywhere?
3. **Envelope admission covers the served reality.** Admission renders ALL SIX nodes
   (BC/OM × A0/B/A1) through the frozen renderer with the ADMISSION binding
   (`ADMISSION_RETAINED_POSITION = 767`, all-F digests, packet :83-91), claimed never
   SHORTER than the served render; W13/bw76 re-executes every render on the FINAL served
   manifests of the retained 768.
   ADVERSARY: internal-consistency — a candidate admitted at the admission binding that
   overflows at its true served binding.
   REACHES IT VIA: `render_all_six_nodes` (packet :676-728) and
   `build_manifest_for_candidate`'s two binding modes (:383-441).
   Attack: construct the length inversion, or show by field-width arithmetic that none can
   exist; check the exact-fit edge (65,536 exactly) both ways.
4. **Ghost evidence is unrepresentable.** FACT world rows re-derive from journal ancestry
   (`fact_world_rows_from_state`, packet :264-293 — the frozen projector COPIES non-obligation
   rows unchanged, so this is the ONLY discriminator); both observation representations derive
   from ONE `ObservationAuthorityV1` record (packet :157-196).
   ADVERSARY: internal-consistency — a FACT or OBSERVATION row with no journal ancestor
   surviving to a served packet.
   REACHES IT VIA: `validate_build_manifest` (packet :456-535).
   Attack: ancestry keys on `event_id` — construct collisions/mutations the one-way
   `fact_key` digest cannot distinguish; mutate a row post-generation and find a path that
   serves it.
5. **The observation channel does not leak gold.** Derivation inputs pass an allowlist
   projection (`OBSERVATION_ALLOWED_FIELDS`, generator :149-157; leak refusal at :575-584);
   the forbidden list is CLOSED (generator :163-176); witnesses bc01-bc04 cover literal
   leaks, per-forbidden-input perturbation, relabeling invariance, and the cardinality/order
   codebook.
   ADVERSARY: author-blind-spot — a derivable encoding THROUGH the allowed fields.
   REACHES IT VIA: `project_observation_inputs` / `derive_observation_authority`
   (generator :556-609).
   Attack: `obligation_row_count` / `fact_row_count` / family assignment all co-vary with
   motif and program shape — construct a value-preserving joint encoding bc02's
   one-at-a-time perturbation cannot see, or show why none exists at these domains.
6. **The exact-subtractive wrapper cannot launder a frozen verdict.** The frozen validator
   runs TWICE (real authority vs inert sentinel); subtraction happens only when the two runs
   agree, the observed set ⊆ `{I01_INVARIANT_INVALID}`, and the independent BUILD population
   join is clean; manifest equality survives via the out-of-closure
   `EXPECTED_MANIFEST_MISMATCH` (packet :731-852).
   ADVERSARY: internal-consistency — a defect inside the subtracted closure that the BUILD
   join does not independently re-establish.
   REACHES IT VIA: `verify_build_scorer_input` / `POPULATION_AUTHORITY_CASCADE_CLOSURE`.
   Attack: enumerate what `I01_INVARIANT_INVALID` covers in the FROZEN validator
   (`mbcx01_r13_packets.py:900-902`) and prove each half is re-established by
   `validate_build_population_join` or independently returned — or name the half that is not.
7. **The inference ingress admits exactly the derived population.** Membership DERIVES from
   the pinned retained authority; a same-length substitution or reordering is refused
   `BUILD_MEMBERSHIP_SUBSTITUTED` before numerical work; the frozen partition + numerical
   core run unmodified (packet :1016-1067).
   ADVERSARY: internal-consistency — duplicate or conflicting receipts collapsing silently.
   REACHES IT VIA: `episode_by_scenario` dict construction (:1043 — last-wins on duplicate
   scenario_id) and the `rows`-vs-`expected_complete` ordering equality (:1064).
   Attack: two episode receipts for one scenario; duplicate outcome receipts; an outcome
   receipt for a scenario the partition calls missing; confirm each dies by name, or name
   the one that does not.
8. **The plan arithmetic is total.** Unplanned refusals `e > 32` refuse the plan; exactly
   `max(0, min(k=12, 32 − e))` planned ineligibles are placed, stratified, at most one per
   joint stratum (generator :1166-1274, `_plan_placements` :1288-1310).
   ADVERSARY: internal-consistency — the plan RECORD stating a number the placement loop did
   not achieve.
   REACHES IT VIA: `_plan_placements` returns ≤ `placed_total` (one-per-stratum over 16
   joint strata can exhaust); `plan["per_motif"]` records `placed_total`, not
   `len(placements)`, and no `len(placements) == placed_total` check exists.
   Attack: DRIVER-NAMED, EXECUTE IT — construct a draft set where placements fall short and
   the plan record therefore misstates `admitted_eligible_lower_bound`; or prove the bound
   safe at these constants and say whether the record is still the right thing to sign.
9. **Census and coverage numbers say what they claim.** Joint strata (motif ×
   family × omission) with declared floors; marginal-preserving deletions caught; SCA
   coverage reported with strength t=2 and floor 0.40 BESIDE the number, denominator = the
   REGISTERED unconstrained 289-pair square — a DECLARED LOWER BOUND on the LTS-constrained
   ratio (generator :1020-1132; residual homed at #31).
   ADVERSARY: author-blind-spot — a census key or coverage count that miscounts.
   REACHES IT VIA: `"|".join` stratum keys (:1086 — axis values containing `|` merge
   strata); pair counting over APPLIED events only (:1027-1032).
   Attack: construct the collision or show current domains cannot produce it; check
   DUPLICATE_NOOP exclusion is the right call for a coverage ratio that GATES.
10. **Registration totality holds and the committed identity is non-circular.** Four levels
    (glob/tuple two-way · REQUIRED == pin-subject set · artifact namespace derived from the
    union of registration lists · module-to-witness nontriviality) live in the bundle;
    the committed identity carries only candidate-derived values (authority :260-292;
    bc11-bc14).
    ADVERSARY: maintainer — a future edit that un-registers silently.
    REACHES IT VIA: `verify-build-bundle.py` registration arms.
    Attack: falsify one level with a synthetic tree probe (bc14 shows the shape); check the
    spec-artifact canonical-serialization gate (authority :186-220) against CRLF checkouts
    both ways.

## 5. Red witnesses per closed class

All 32 cohort witnesses were red-first: 10 engine reds + 14 bc registration/channel reds
recorded verbatim in-tree (commits `4f70378` + `f35851e`, red transcripts in each message and
the banked records), plus 1 rider red (ps1 comment-parser phantom). Repair ledger 98
invariants / 229 witnesses, two-way total, in the bundle. The design-round executed probes
(duplicate matrix, leakage, family-deletion, scorer-join) are banked in the r1-r3 syntheses +
`MBCX-01-COHORT-R1-DRIVER-REPRODUCTIONS.md`.

## 6. Executable-falsification lane — all seats

- Suites at the pin: `python -m unittest test_mbcx01_build_cohort` (expect **Ran 32 — OK**) ·
  full local discover (expect **541 OK**) · `python verify-build-bundle.py` (REAL exit 0;
  frozen 156 · BUILD 229 · ledger two-way).
- Construct and RUN at least one fresh adversarial input per claim you rule on; label every
  finding EXECUTED or READ-ONLY. A READ-ONLY verdict cannot be the deciding GO. Empty probe
  output = broken harness, never a pass.
- The suite is ~97s and discover ~170s — run them to completion, do not time them out.
- ⛔ No ETW session, no Job Object, no `MBCX01_BUILD_ALLOW_PHYSICAL`, no provider calls, no
  route trials, no spend.

## 7. Omission attack

At least one seat: what did the BUILD engine NOT build that the design of record requires —
a witness in design §4 (W1-W21) with no discriminating test at these bytes, a §2.3 refusal
class not counted in the plan arithmetic, a frozen coupling not recorded in §3? And the
inverse: does any witness here test the MOCK rather than the mechanism (a probe built FROM
the code under test — the bw28 class)? Is there machinery in this slice the no-adversary
rule says should not exist?

## 8. Non-claims (each is a load-bearing assertion of safe exclusion — attack them too)

Consolidated at issue #31, restated: SCA denominator is the unconstrained 289 superset
(coverage is a LOWER bound, never "covered") · W14(d) nontriviality is half-mechanical ·
8 of 12 forbidden observation inputs are asserted structurally rather than perturbed ·
W10 relevance is selection-level (the frozen `_object_closure` pads both served packets) ·
scored cuts are T1-pinned · the frozen private-name dependency
(`packets._unique_gold_action`) is accepted and recorded. Plus: the shared-reducer
pseudo-oracle residual (§2.7 — agreement is consistency, not correctness); no scientific
run, spend, route, physical execution, or frozen edit; no security posture — this artifact
has no adversary and claims none.

## 9. Why this exists (build-decision challenge — answer all four)

ALREADY-BUILT: the frozen generator EXISTS and stamps one world on 960 candidates — the gap
was scientific CONTENT (issue #17, byte-corrected); the frozen selection arithmetic is
ADOPTED unchanged by import, not rebuilt; the exact-subtractive wrapper adopts the lane's own
`mbcx01_build_state_authority.verify_production_scorer_input` pattern; the three-repo shelf
returned zero matches for the population-strata/coverage/membership shapes (§11).
PRODUCT-FIT: the engine is the experiment's subject population — without it the instrument
referees machines that do not exist. One sentence: the owner needs 768 real, varied,
leak-free scenarios whose every property is derived and refused loud, or the experiment
measures its own fixture.
BIGGER-THAN-THE-BUG: three siblings + one suite, landing exactly the design's §2 modules
1-3; no new subsystem beyond the design of record; the design got three council rounds +
two codex gates first.
PRIMARY-CONSUMER: the frozen inference core (via the BUILD ingress) and, through it, the
owner defending one number — a bounded read of the provenance/census/coverage records buys
the reader the exact population identity, its variation axes, and what the coverage figure
does and does not claim.

## 10. Search log (driver's own sweep)

The code introduces NO new external prior-art claim beyond the design's banked set (NIST
sequence covering arrays + LTS-constrained variant · Kuhn/NIST t-way detection lineage ·
Groce et al. swarm testing · differential pseudo-oracle — all SEARCHED at origin by seats in
design r1-r3, banked in the syntheses). The 2-way≈70%/3-way≈90% figures ride the design and
are cited in provenance labels only. UNSEARCHED for this round: NOT-LOAD-BEARING — every §4
claim rests on our own pinned bytes and the frozen layer's recorded behavior.

## 11. Internal-shelf log (driver's own internal sweep, run 2026-08-16 at this pin)

QUERIES: `sequence coverage` · `covering array` · `stratif(y|ied)` · `census` ·
`retained_set_root` · `membership.substitut` · `cohort` (one alternation grep each,
driver-run 2026-08-16 at this pin).
REPOS: agentvault-mcp-bridge (`src/`) · Photon (`crates/`) · Gravity (`src/`) — all three.
OPENED: only `census` matched anywhere — bridge `pii-sidecar.ts`/`audit.ts` census sites ·
Photon `aruna` census mentions · Gravity `capture/censusRow.am-f41.test.ts` — all
LIVE-RESOURCE INVENTORY censuses, a different problem from statistical population strata
with retained floors: declined, reasons recorded in the design r2/r3 syntheses; Photon
`writer_gate.rs` / `store_open.rs` opened and declined at design r6 (different problem,
ruling recorded). Zero hits for every other term.
STOPPED: seven problem-shape terms, three repos, the near-misses already adjudicated in this
lane's own design arc — a further pass would re-read known misses.

## 12. Seat SWEEP lane (the seats' own sweep)

SWEEP APPLIES TO: any claim resting on prior art, a standard, or vendor-documented
behaviour — go look with your own queries before you bless or refute it.
DELIVERABLE: a SWEEP LOG in your verdict — exact queries · what you OPENED (URL + deciding
section) · what it changed or confirmed · why you stopped.
LABELS: every prior-art or standards-bearing finding carries exactly one of SEARCHED /
RECALLED / UNSEARCHED (UNSEARCHED carries its reason: NOT-LOAD-BEARING ·
SETTLED-BY-PINNED-BYTES · COULD-NOT · DID-NOT).
CONSEQUENCE: an UNSEARCHED or RECALLED finding cannot be the deciding GO on a claim resting
on prior art or a standard; a round where no seat swept such a claim is incomplete.
HONEST OUT: if you cannot reach the web this session, say so plainly in one line.

## 13. Re-review trigger

Any fold that touches the frozen layer ⇒ an AMENDMENT on the A-1/A-2/A-3 pattern + a fresh
round. Architecture/interface folds in the BUILD siblings ⇒ fresh round on the folded
bytes. Localized code folds ⇒ fold red-first, then the codex-CLI gate (#1) serialized after
this arc closes. A finding whose remedy gates a person ⇒ the on-contact discriminator, not
a build.

## 14. Driver pre-dispatch execution (run before sending, at the §2 pin)

- Cohort suite **Ran 32 — OK, exit 0** (96.7s) · full local discover + bundle re-run at
  dispatch time this session (results recorded in the dispatch receipt beside this packet).
- The §0 settling grep re-run: zero hits.
- §4.8's placement-shortfall question was driver-constructed as far as arithmetic: k=12
  against 16 joint strata per motif with ~10 candidates per stratum — no shortfall is
  reachable at the COMMITTED constants unless refusals wipe ≥5 whole strata; the missing
  totality CHECK (not a live wrong number) is what the seats rule on. Labelled REASONED,
  not executed to a red.
- Pins emitted by `git rev-parse`, gated by `git cat-file -e`, both verified above.
