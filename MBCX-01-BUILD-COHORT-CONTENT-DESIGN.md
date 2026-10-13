# MBCX-01 BUILD — Cohort Content design r6 FINAL (issue #17) — GO-TO-CODE

Status: DESIGN r6 FINAL — the closing council fold (r4) + both codex design-gate rounds' edges folded (r5, r6; gate logs banked; the 2-round cap is EXHAUSTED and the lane is in code). Council record: r1 3/3 NO-GO · r2 GWF/NO-GO/NO-GO ·
r3 ROUND CALLS **GO-TO-CODE / CONTINUE-DESIGN(one function) / GO-TO-CODE** — GO-TO-CODE
outranks and this fold writes the round's bounded items in (no architecture change; syntheses
`MBCX-01-COHORT-DESIGN-COUNCIL-R{1,2,3}-SYNTHESIS.md`). The design phase is CLOSED; the next
artifact is the BUILD itself (after one codex-CLI design round per the loop's cap).
BUILD-class; zero frozen files touched; zero spend; nothing here authorizes an experiment,
route, or physical run.

## 1. Problem, at the byte (r1–r3 CONFIRMED: the population authority is FIVE surfaces deep)

The frozen generator stamps one world (r1, 3/3 executed: ONE distinct world/state/action
across all 960 candidates; eligibility a declared Boolean read back under a `RECOMPUTED`
label). The frozen manifest builder is a second stamp (`mbcx01_r13_packets.py:158-196`
hard-codes scope/target/decoy/catalog/BC-selection). The frozen scorer/outcome joins are a
third (`:118-155` retained-authority join, called from `invariant_matrix:900-902` and
scenario-outcome build/validation `:1285-1304`/`:1347-1367` — a BUILD candidate dies at
`I01_INVARIANT_INVALID`; r2 seats 2+3, executed). And `_fixture_authoritative_state`
(`:352-376`) is a fourth, on the DEFAULT scoring path (`build_scoring_fixture:576`,
`build_transition_authority:422` when `authoritative_state=None`): it builds from
`initial_state()`'s hard-coded `OBL.SHARED`/`OBL.PREREQ` literals and enforces exact
obligation-set equality, so a renamed population is refused outright (r2 seat 1, executed
both branches). And the frozen INFERENCE ENTRY is a fifth — a JOIN surface, not a literal
one: `ordered_decision_from_episode_receipts` re-runs the frozen cohort joins
(`mbcx01_r13_inference.py:186-193`, `validate_scenario_outcome_receipt` +
`scenario_outcome_pair`) before the numerical core at `:198` (r3 seats 2+3 executed
end-to-end — a valid BUILD receipt dies `SCENARIO_OUTCOME_AUTHORITY_INVALID`; driver
byte-verified `:168-200`). The slice builds the producing half end-to-end through the
inference ingress or it builds an illusion.

## 2. What is built — THREE versioned BUILD siblings, landing in ONE slice

On the `mbcx01_build_measurement_authority.py` pattern (docstring cites the frozen lines
superseded; closed error vocabulary extending the six cohort codes; instance-scoped, no
module-global caches):

1. **`mbcx01_build_cohort_generator.py`** — candidates as deterministic 17-event programs
   replayed through BOTH frozen reducers at generation (gate per §2.7), states and
   obligation/dependency/FACT world rows derived from replay, observations from §2.2,
   eligibility from §2.3, envelope admission from §2.5, coverage measurement from §2.6.
2. **`mbcx01_build_cohort_authority.py`** — selection/provenance/retained-authority siblings:
   adopts `choose_one_cut`/retention-hash/128-per-motif/retained-root arithmetic unchanged
   (imported from the frozen module), owns the BUILD pinned source, binds the journal
   (`event_program_hash`) and the observation record (`observation_authority_hash`) into the
   provenance sub-digests, and pops/refuses declared-eligibility keys by name
   (`DECLARED_ELIGIBILITY_BOOLEAN`).
3. **`mbcx01_build_cohort_packet.py`** — the population-dependent PACKET/SCORER sibling
   (r2's "manifest sibling", widened by the round's convergent R3): (a) derives scope,
   target, decoy set, FULL action catalog, gold, read-set, and BC selection from the
   candidate; (b) projects FACT world rows from replayed state (ghost facts
   unrepresentable); (c) derives both observation representations from the §2.2 record;
   (d) SUPPLIES `authoritative_state` explicitly from the replayed generation state —
   witnessed against `project_state_world` equality, never defaulting into the frozen
   fixture path (`_fixture_authoritative_state`'s literals; r2 seat-1 R3); and (e) carries
   the exact-subtractive scorer/outcome wrapper on the named internal shelf pattern
   (`mbcx01_build_state_authority.verify_production_scorer_input`) so I01, scorer-input, and
   scenario-outcome validation join the BUILD population; and (f) **the BUILD inference
   ingress** — `ordered_decision_from_build_episode_receipts(...)`: the frozen
   `derive_episode_partition` unchanged for episode/missingness authority, complete pairs
   validated/extracted through the BUILD exact-subtractive outcome seam, then the frozen
   numerical core `ordered_decision_with_missingness` unchanged — estimand, missingness hull,
   n=768, and frozen formulas untouched; only the population-specific receipt admission
   differs — AND the ingress DERIVES the ordered scenario-ID list and `retained_set_root`
   from the BUILD pinned retained authority, never accepting a caller-supplied membership
   (codex gate r1, EXECUTED: 768 phantom IDs with valid missing receipts reached the frozen
   numerical core; `mbcx01_r13_inference.py:141-165` validates only the supplied list). W19
   extends with a same-length missing-ID substitution/reordering red (the fifth surface, r3
   seats 2+3 executed).

**Frozen couplings this slice lives inside (recorded, not fought):** `MANIFEST_KEYS` is a
closed set (`mbcx01_r13_packets.py:203-214`) — no new manifest key without a frozen
amendment; all BUILD-side identities ride PROVENANCE. The motif taxonomy is frozen to the six
(`:217`). `retained_position < 768` at BOTH sites — `:222` and `mbcx01_r13_measurement.py:1501`
(r3 seat 1; record both so a future n-change finds them). `mbcx01_r13_integration.py` is
hard-bound to the frozen fixture population by construction (self-builds it; breaks silently
if the synthetic cohort's fixture role is ever retired — noted, retained as-is). The frozen
layer is untouched;
`FROZEN_TEST_TOTAL` stays 156; the frozen synthetic cohort keeps the fixture role.

## 2.1 Motifs are SEMANTIC CONTRACTS — postcondition + REALIZATION CONSTRUCTION + exact codes

r2 fixed the r1 event-vocabulary confusion but stated postconditions without their
constructions; seat 1's executed duplicate matrix showed why that fails: `DUPLICATE_NOOP` is
reachable ONLY by byte-identical event replay (same `event_id` — the replay/idempotency
gates, `state_reference:23,28` / `state_oracle:36,42`), while the three other natural
"duplicate" constructions return `PROPOSAL_INVALID` / `COMMIT_INVALID` /
`IDEMPOTENCY_CONFLICT` — and ALL FOUR leave state byte-unchanged, so a state-only witness
discriminates nothing. **Each motif contract therefore binds three things: the observable
postcondition · the legal realization construction · the exact expected result-code sequence
from both reducers. W4 asserts the codes.**

| Motif | CONTRACT (postcondition) | REALIZATION (construction + expected codes) |
|---|---|---|
| CORRECTION_RESTORATION | a prior `value_code` VISIBLE AGAIN at a later cut after its correction was retracted | assert → correct chain → retract(correction) → REASSERT; codes all `APPLIED`; visible@later = the reasserted value (r2 seat-1 executed the full chain) |
| OBLIGATION_LIFECYCLE | named lifecycle transitions OBSERVED in the projected world across cuts, on NON-target obligations | open → reschedule → {complete \| cancel} → reopen; codes `APPLIED` each; §2.4 governs the scored target |
| DEPENDENCY_REVERSAL | the target OBSERVED blocked at one cut and due at another purely from prerequisite completion order | link (`APPLIED`) → target illegal; complete prereq (`APPLIED`) → target legal (r2 seat-3 executed) |
| CROSS_SCOPE_COLLISION | (a) in-scope subject/name collision pressure; (b) scored projection carries ZERO foreign-scope objects while the journal is genuinely multi-scope | foreign-scope events `APPLIED`; projection zero-foreign witnessed (r2 seat-3 executed) |
| DELEGATION_IDEMPOTENT_HANDOFF | owner-role rewrite visible; duplicate proposal AND duplicate commit each a true no-op; a rejection path; B-call recorded | duplicates constructed as BYTE-IDENTICAL EVENT REPLAY → `DUPLICATE_NOOP` exactly (never `PROPOSAL_INVALID`/`COMMIT_INVALID`/`IDEMPOTENCY_CONFLICT` — distinct facts, W4 distinguishes them); rejection realization → result code `APPLIED` with handoff status `REJECTED` and `terminal_disposition` = the payload's `rejection_code` (⚠ NOT result code "REJECTED" — r3 seat 1 executed the cell; W4 asserts the code/status/disposition TRIPLE and the deliberate commit/reject asymmetry, commit alone writing its literal); `record_call_response` carried |
| MIXED_DELAYED_CONTINUITY | the target's due-state transition OBSERVED across the scored cuts | CONSTRUCTION (completed at r4 per r3 seat 3): `open_obligation` (target, `due_at` = the chosen cut's `valid_time`, `APPLIED`) at an early cut where `due_at > valid_time` ⇒ target NOT in the legal set at the earlier cuts (witnessed); no reschedule of the target thereafter; at the chosen cut `due_at <= valid_time` ⇒ target uniquely legal (witnessed). Codes: all `APPLIED`; the postcondition is the legality flip across cuts (r2 seat-3 executed the flip) |

**Variation:** per-candidate, hash-derived (seedless `framed_hash`, domains declared in the
generator spec): obligation count, prerequisite graph shape (width/depth ≤ 3/3), decoy count
and lifecycle mix, catalog size (every eligible candidate ≥1 non-gold action), fact-chain
depth, observation family (§2.2), event ordering within legality, and a per-candidate
mechanism-OMISSION configuration within the family (bounded swarm form; Groce et al. ISSTA
2012), the six motifs kept as named anchor configurations. **[amended 2026-08-16,
cohort-BUILD r1 fold 2] The SCORED TARGET's OBLIGATION IDENTITY is a variation axis:
it is derived per scenario (`OBL.TGT.` + `scenario_id`, distinct by construction — no
hash, no collision argument), so `action_id = sha256([scope, obligation_id])` gives
every retained row its OWN gold. A constant target id made the gold a constant across
all 768 retained rows, and a positional heuristic then scored at ceiling in BOTH arms
with no population knowledge — the BC/OM contrast collapsed for a reason unrelated to
the hypothesis (council r1: seat 1 A, driver-reproduced). Decoy, blocker and BC-only
obligation identities are unchanged.**

## 2.2 Observation and FACT authority — consistency AND non-leakage

Two laws, one record:

- **Consistency (r2, kept):** `ObservationAuthorityV1` — one deterministic record per
  (scenario, chosen cut); BOTH the manifest top-level observation and the world OBSERVATION
  row derive from it; divergence unrepresentable in module 3 and witnessed (W15).
  `observation_authority_hash` rides provenance (not the manifest — `MANIFEST_KEYS` is
  closed). FACT world rows are ENDOGENOUS (projected from replayed state; ghost facts
  unrepresentable).
- **Non-leakage (r3+r4; witness = W15's FULL checklist, normatively — this section defers
  to W15's four discriminator classes, never a two-arm subset):** the observation grammar is
  CLOSED and its derivation rule's inputs pass through an EXPLICIT PROJECTION FUNCTION whose
  allowed-field set is a declared constant (the lane's own FACT-projection move: a gold-determining field cannot REACH the
  rule, unrepresentable beats detectable — r3 seat-1 PROPOSE, adopted). FORBIDDEN inputs: the
  motif label, the gold action id, any action identity, selector output, retained position,
  AND the gold-DETERMINING field set of the scored target and its prerequisites — lifecycle,
  critical, due_at, prerequisite lifecycles (r3 seat 1: these leak gold EXISTENCE, and
  relabeling invariance cannot see value-preserving leaks; addition lands via Item 7(c)'s
  governed process). The non-leakage witness: (a) no gold/action literal or derivable encoding appears
  in any observation field (executed check over the retained set); (b) relabeling invariance —
  an identifier/action relabeling that preserves the observation's declared meaning leaves the
  observation family/value unchanged (r2 seat-2's semantic-noninterference form). Observations
  are a declared variation axis (they sit inside the gold read set unconditionally,
  `mbcx01_r13_packets.py:63-64` — the measured quantity may not ride an unvaried input).
- **DECLARED RESIDUAL — POPULATION-LEVEL SIGNATURE→MOTIF LEAK [amended 2026-08-16,
  cohort-BUILD r1 fold 2].** The four discriminator classes above are per-CANDIDATE
  properties; ACROSS the retained population, **3 of the 23 observation signatures
  (family, code, cardinality, order) identify exactly ONE motif, and 15 of the 768
  retained rows carry one** — the signatures are `COUNT_SUMMARY|POPULATION.COUNT.9`
  (cardinality 1 and 2, ASCENDING → `OBLIGATION_LIFECYCLE`) and
  `STRUCTURE_DEPTH|FACT.DEPTH.4|2|ASCENDING` (→ `MIXED_DELAYED_CONTINUITY`): the
  distribution TAILS of two allowed counts. These are the measured numbers, reported
  in the census itself (§2.3) and pinned to the constant
  `DECLARED_SINGLE_MOTIF_SIGNATURE_RESIDUAL` by `test_bc19_*`, so the number cannot
  drift in silence. ONE bounded reshaping attempt was made and DISCARDED: 0–2
  hash-derived non-legal PAD obligations per candidate (opened `critical=False`,
  `due_at=T2`, never catalogued) moved the tail — `POPULATION.COUNT.9` →
  `POPULATION.COUNT.10`/`.11`, `FACT.DEPTH.4` → `FACT.DEPTH.3` — leaving **3
  single-motif signatures either way** with affected rows 15 → 8. A tail is a tail;
  eliminating it needs identical per-motif count SUPPORT, which is machinery this
  no-adversary harness does not buy. Live exploitation requires cross-scenario
  statistics a frozen cold-episode subject does not have; the honest label is carried
  here instead.

## 2.3 Eligibility: derived; the quota composes over ALL refusal classes; multivariate census

Derived through the packet layer's gold predicate (unique gold + ≥1 non-gold action);
supplied Booleans popped and refused by name. **Total-admission arithmetic (r2 seat-3; SEQUENCED at r4):** the
per-motif plan accounts every refusal class IN GENERATION ORDER — render first, measure the
envelope refusals e, THEN place exactly max(0, min(k, 32 − e)) planned ineligibles — and e > 32 for any motif is
itself a REFUSAL of the generation plan (a shape whose envelope refusals alone exceed the
floor margin cannot honestly reach 128; the e=33 red is banked BUILD material) (k ≤ 32, declared,
framed-hash ranked, stratified across target-not-due / ambiguous-gold / missing-non-gold) —
so admitted-eligible ≥ 128 per motif holds by arithmetic over the whole plan on honest input
(r3 seats 1+3: a fixed k plus discovered envelope refusals can otherwise fault); the frozen
`eligible motif shortfall` fault stays as backstop. **Census, not a scalar proxy (r2 seats 2+3):** the generated / rejected / retained
populations are censused across every declared semantic axis — observation family, omission
configuration, catalog size, dependency/frontier shape, fact-chain depth, gold-read-set size,
BC/OM set difference — and the census is a witness: an axis value present in the generated
population and absent from the retained 128 fails loud unless declared — AND the census
reports JOINT occupancy over declared tuples (at minimum motif × observation-family ×
omission-configuration; r3 seats 1+3 executed the marginal blind spot: two joint strata can
vanish while every marginal stays present), with a red witness deleting one tuple while
preserving every marginal; and each governed stratum carries a DECLARED RETAINED FLOOR with
a red where occupancy is nonzero but below the floor (RETAINED_AXIS_STRATUM_FLOOR — one
retained row must not read as represented; REGISTERED as W20). **[amended 2026-08-16,
cohort-BUILD r1 fold 2] The census also carries two POPULATION-CONTENT measurements:
(a) `distinct_gold_action_ids` over the retained set against a DECLARED floor —
`ONE_DISTINCT_GOLD_ACTION_ID_PER_RETAINED_ROW`, i.e. the floor IS `retained_total`,
because §2.1's per-scenario target identity makes the golds distinct by construction —
refused by name as `RETAINED_GOLD_VARIETY_BELOW_FLOOR` when below (witness bc18); and
(b) the SIGNATURE × MOTIF cross-tab (`observation_signature_total`,
`single_motif_observation_signatures`, `rows_carrying_a_single_motif_signature` and the
signature list), MEASURED and reported, NOT gated — the residual it reports is declared
in §2.2 and gating it would refuse a whole build over a distribution tail (witness
bc19). Also: `_plan_placements` must ACHIEVE the placement total the plan record signs,
or the generation is refused as `BUILD_GENERATION_PLAN_REFUSED` naming requested vs
achieved, and a derived census axis that cannot be recorded refuses as
`BUILD_DERIVED_AXIS_UNRECORDABLE` instead of being censused as the sentinel `-1`
(witness bc20; all four population classes were checked at the pin before the `-1` net
was removed).

## 2.4 The reopen ruling — unchanged (a declared POPULATION EXCLUSION)

The scored target is never reopened after completion inside the scored window (W9); BC/OM is
never measured over target-reopen — recorded in §5's non-claims; #23 proposes the DoR
sentence.

## 2.5 Envelope admission — delegate to the frozen renderer (the r2 comparator was wrong twice)

The frozen renderer pads every fitting packet to exactly 65,536 bytes and raises only on
`len(encoded) > ENVELOPE_BYTES` (`mbcx01_r13_packets.py:302-306`, driver byte-verified) — so
r2's "served < 65,536" was unsatisfiable and its `≥` refused the legal exact-fit. **r4:
admission = `render_served_input` SUCCEEDS for ALL SIX NODES — BC and OM × A0/B/A1 — at
generation** (equivalently: unpadded canonical length ≤ 65,536 for each; r3 seat 3 executed an
A1 render overflowing at 65,541 while its A0 fit, and the governing R10:49 requires exact
served bytes for all six nodes). Refused candidates are part of the deterministic plan
and counted in §2.3's arithmetic. The measured shape ceiling (~190–200 world objects at
default ID lengths; input-shape-sensitive per r1 seat-3's 14-byte overflow) is recorded as a
declared constant; W13 asserts ALL SIX renders succeed across the retained 768.

## 2.6 Coverage: SEQUENCE covering, not event×position (r2 convergent 3/3)

The reducers are order-sensitive (the correction's closure surviving its retraction is purely
an ordering effect). The PRIMARY provenance coverage number is **t-way SEQUENCE coverage over
the 17-event alphabet — ordered pairs minimum — constrained to reducer-legal sequences with
the frozen reducers as the labeled transition system** (NIST sequence covering arrays;
LTS-constrained variant). The alphabet-scoped presence invariant (named, reasoned exclusions)
and the (event × lifecycle-position) matrix are kept as SECONDARY diagnostics. The
mechanism-omission configurations of §2.1 are what generate the ordering diversity the SCA
scores. A witness asserts the measurement is computed, reported in provenance WITH ITS STRENGTH t
AND FLOOR BESIDE THE NUMBER (2-way detects ≈70% of sequence-sensitive fault classes in the
Kuhn/NIST lineage, 3-way ≈90% — a 2-way figure must never read as "covered"; r3 seat 1
SEARCHED), and meets its declared floor. **[amended 2026-08-16, cohort-BUILD r1 fold 4]
The record declares its NUMERATOR rule beside its denominator rule:
`covered_pair_rule = ORDERED_PAIRS_OVER_ALL_GATE_CHECKED_PROGRAM_EVENTS`. Every event
in a program passed §2.7's replay gate against its EXPECTED result code, so a
`DUPLICATE_NOOP` is a legal EXECUTED program event and its ordered pairs are covered
pairs; counting pairs over the APPLIED subset alone undercounted by one pair
(`commit_handoff_result > commit_handoff_result`, 150 vs 151 of 289 — council r1 seat 3
F2, driver-reproduced). `sequence_coverage_report_errors` now REQUIRES both rules, and
bc06's recomputation was re-derived non-mirroring (it had copied the applied-only
filter, which is why it could not see the undercount).
**[amended 2026-08-16, cohort-BUILD r2 fold]** Provenance ADMISSION recomputes the coverage
record from the candidate programs themselves — `validate_build_source_provenance` re-runs
the measurement (which moves to `mbcx01_build_cohort_authority` so the validator can run it)
over the popped candidate rows and refuses a record that does not byte-equal the recompute by
name, `BUILD_SEQUENCE_COVERAGE_MISMATCH`, because field presence plus a floor Boolean admitted
a self-consistent forged 289/289 into the retained authority's own provenance (council r2 seat
3 F1, driver-reproduced).

## 2.7 The reducer-agreement gate, stated honestly (unchanged from r2)

Dual-reducer agreement is CONSISTENCY (differential pseudo-oracle), not correctness; a shared
legality bug is invisible to it. Generation runs reference apply + oracle apply +
byte-equality + the DoR legality predicate at each step's frontier. The named residual (shared
reducer bug) is carried, not papered over.

## 3. Identity, pinning, registration — totality at every level

- BUILD cohort spec `MBCX-01-BUILD-COHORT-GENERATOR-V1.json`
  (`generator_id: GENERATOR.BUILD.COHORT.V1`); own provenance manifest; own
  `retained_set_root` in a committed identity block; #4's ratification surface extends to the
  new root.
- Registration (all three modules + `test_mbcx01_build_cohort`): `BUILD_MODULES` ·
  `BUILD_TEST_MODULES` · `WITNESS_ID` prefix widening (recorded) · repair-ledger rows +
  `witness_namespace` + totals · `$buildSubjects` · `BUILD_WORK_PRODUCTS` · parity documents.
- **Totality, four levels (r1 C7 + r2 residuals; sharpened at r4):** (a) glob-vs-tuple
  two-way for modules and test modules; (b) REQUIRED ⊆ pin-manifest-subject-set, with every
  pinned-beyond-REQUIRED subject named in the declared allowlist
  `PIN_MANIFEST_SUBJECTS_BEYOND_REQUIRED` and any other pinned subject refused by name as
  `W14_PIN_MANIFEST_SUBJECT_OUTSIDE_DECLARED_SET` — equality would refuse a RIGHT
  reconstruction, which deliberately pins the frozen r13.2 layer
  `[amended 2026-08-16, cohort-BUILD r1 adjudication 2]`;
  (c) **artifact-namespace totality** — the governed artifact namespace is DERIVED FROM THE
  UNION OF THE REGISTRATION LISTS themselves, never a filename glob (r3 seat 1: a glob leaves
  a differently-named artifact unregistered-and-unnoticed); every artifact in that union is on
  disk and conversely; (d) **module-to-witness coverage WITH NONTRIVIALITY** — every
  `BUILD_MODULES` entry maps to a NAMED owned behavior and ≥1 declared ledger witness whose
  result CHANGES when that behavior is replaced or refused (r3 seats 1+3: import-only coverage
  is inadmissible). All four witnessed (W14).
- **Pin discipline (verified working by all three r2 seats):** every pin emitted by
  `git rev-parse`, gated by `git cat-file -e` (never `rev-parse --verify`, which echoes a bad
  40-hex without erroring) before any dispatch.

## 4. Red witnesses (red-first)

W1 membership discrimination · W2 declared-Boolean refusal · W3 derivation does real work +
exact quota counts over ALL refusal classes · W4 **postcondition + EXACT RESULT-CODE
witnesses per motif** (incl. `DUPLICATE_NOOP` distinguished from
`PROPOSAL_INVALID`/`COMMIT_INVALID`/`IDEMPOTENCY_CONFLICT`; a state-only clause is
insufficient by construction) · W5 three-check replay gate + legality frontier · W6
determinism (byte-identical re-runs; post-generation mutation fails authority re-derivation) ·
W7 BUILD population joins the BUILD authority path (768, 6×128, positions, root, provenance) ·
W8 committed root equals recomputed root · W9 reopen constraint · W10 **the sentinel,
structural half** — gold read-sets take ≥ a declared number of distinct values AND the BC/OM
difference is non-degenerate AND (relevance, r2 seats 2+3) for a declared coverage class the
OM-only evidence is NECESSARY for canonical gold derivation under a registered counterfactual
(RED today by construction) · W11 different catalogs ⇒ different served manifests · W12 a
journal-only mutation fails the BUILD provenance gate · W13 all six renders succeed across the
retained 768 (delegated comparator; incl. exact-fit and A1-growth witnesses) · W14 four-level registration totality · W15 observation
consistency AND non-leakage — the FULL checklist: gold/action-encoding scan · relabeling
invariance · per-forbidden-input independent perturbation with the allowed projection held
fixed · family/order/cardinality codebook reds (LITERAL_LEAK · DERIVABLE_ENCODING ·
RELABEL_DRIFT · CARDINALITY_OR_ORDER_CODEBOOK) · **W16
scorer-join end-to-end** — one retained BUILD candidate through supplied-state
`build_scoring_fixture`, I01/scorer-input validation, and scenario-outcome validation, green
on the BUILD path and RED against the unwrapped frozen path · **W17 sequence-coverage
measurement** — the canonical reducer-legal TARGET SET (or its exact identity and count) is
REGISTERED and coverage is recomputed against that registered denominator; the number reported
in provenance with its strength t and floor beside it, meeting the declared floor · **W18
authoritative-state supply** — the supplied state satisfies `project_state_world` equality
against the BUILD manifest; the frozen fixture default is never reached by BUILD candidates ·
**W19 the inference ingress** — a full 768-position BUILD receipt set (one complete-pair
fixture) accepted through `ordered_decision_from_build_episode_receipts` reaching the frozen
numerical core, while the SAME receipts are RED at the unwrapped frozen
`ordered_decision_from_episode_receipts` (RED today by construction) — AND the
population-substitution red: a same-length missing-ID substitution or reordering of the
membership list is REFUSED (the gate-r1 768-phantom-ID discriminator, registered) ·
**W20 census stratum floors** — a governed stratum with nonzero occupancy below its declared
retained floor is RED (RETAINED_AXIS_STRATUM_FLOOR, registered in the ledger) · **W21
ghost-FACT discrimination** — a FACT row injected into the manifest without journal ancestry,
or mutated post-generation, is REFUSED by the BUILD packet sibling (the frozen projector
copies FACT rows unchanged, `mbcx01_r13_packets.py:68-95`, so generic projection equality is
NOT this discriminator; the r1 driver reproduction P2 is the banked red).

## 5. Non-claims, exclusions, and honest limits

No scientific run, route, spend, physical execution, frozen edit, or root ratification (#4);
no H/D/F twins (#23); no Merkle tree; no security posture. Population exclusions: BC/OM never
measured over target-reopen; the six motifs are a bounded frozen taxonomy (also a frozen
COUPLING — `validate_expected_manifest:217`); the UNWRAPPED frozen inference ingress remains frozen-cohort-scoped; the BUILD ingress changes only population admission (membership derived from the BUILD pinned authority); observation
truth is generator-authored under §2.2's two laws. **Honest limit (r2 seat-1): W10 discharges
the falsification sentinel's STRUCTURAL half only — statistical power is unknowable until
first inference, and no pre-run witness can close that.** Shared-reducer-bug residual carried
(§2.7).

## 6. Pre-review evidence (r3)

- Item 0 anchor: issue #17 + ENGINE-FIRST ruling; sentinel witnessed structurally (W10),
  limit recorded.
- Item 2 internal: two complete council rounds (six EXECUTED verdicts) + the driver
  reproduction record + driver byte-verifications (r2 synthesis) are the internal evidence
  set; the scorer-wrapper pattern is adopted from the lane's own shelf
  (`mbcx01_build_state_authority.verify_production_scorer_input`). External (SEARCHED at
  origin by seats, banked): NIST sequence covering arrays + LTS-constrained variant · NIST
  each-choice/interaction rule · Groce et al. swarm testing · differential-pseudo-oracle ·
  Hypothesis/QuickCheck stateful lineage · W3C PROV-DM (lineage only).
- Item 7 open unknowns: (a) declared constants (k, mechanism minimums, coverage floors,
  envelope shape constant, census floors) are BUILD-time values — the suite pins them;
  (b) whether the SCA floor gates or reports at first build is a build-time call, witnessed
  either way; (c) the exact forbidden-input list for §2.2's derivation rule is closed at
  build with its own witness — additions are design-round material, removals are not
  permitted.
