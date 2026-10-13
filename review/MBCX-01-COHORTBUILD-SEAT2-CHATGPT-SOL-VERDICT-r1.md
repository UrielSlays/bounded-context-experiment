# SEAT 2 (chatgpt.com sol, conversation <id>) — cohort-BUILD acceptance r1 verdict

> Banked VERBATIM by the driver from the seat thread via `browser_wait_quiesced`
> (textLen 21,827, truncated:false), 2026-08-16 ~17:55Z.

NO-GO

EXECUTED verdict. I read MBCX-01-COHORT-BUILD-ACCEPTANCE-COUNCIL-PACKET-r1.md at commit 8432132ed8db3feb3b854ac4d9efddacb840ce4f and reviewed the content pinned at f35851e94b73731dc9cb5db8cb7085471d4c1bac. The five reviewed working-tree artifacts byte-match that content pin, and git diff --stat f35851e HEAD -- '*.py' is empty.

The mandatory execution bank is fully discharged:

python -m unittest -q test_mbcx01_build_cohort → 32/32 OK, 97.433s.

Literal python -m unittest discover -q in one process → 541/541 OK, 171.900s.

python verify-build-bundle.py → BUNDLE_EXIT=0. Frozen 156, BUILD 229, ledger 98 invariants / 229 witnesses, registration totality PASS, schemas PASS, canonical parity PASS, no-production-activation PASS, execution-posture PASS.

No ETW session, Job Object, MBCX01_BUILD_ALLOW_PHYSICAL, provider call, route trial, or spend.

The suites are green, but fresh adversarial execution found a load-bearing gap: semantic re-derivation exists as a validator/witness, but it is not on the actual serve/scoring boundary. I pushed both a journal-less FACT and a non-derived gold-bearing observation through self-consistent BUILD provenance/authority contexts. The served/scorer path admitted them.

That is wrong evidence reaching the experiment.

Evidence read

Load-bearing pinned bytes included:

mbcx01_build_cohort_generator.py:149-176 — observation allowed/forbidden input sets.

mbcx01_build_cohort_generator.py:232-296 — dual-reducer program replay/code/legality gate.

mbcx01_build_cohort_generator.py:556-609 — observation projection and deterministic authority derivation.

mbcx01_build_cohort_generator.py:616-666 — deterministic variation/joint strata.

mbcx01_build_cohort_generator.py:1020-1132 — sequence coverage and census.

mbcx01_build_cohort_generator.py:1166-1310 — total-admission plan and _plan_placements.

mbcx01_build_cohort_authority.py:181-220 — canonical spec-artifact serialization.

mbcx01_build_cohort_authority.py:260-308 — committed identity and journal/state provenance binding.

mbcx01_build_cohort_authority.py:369-504 — eligibility popping, provenance validation and cohort selection.

mbcx01_build_cohort_authority.py:509-653 — retained context and scenario/cohort authority.

mbcx01_build_cohort_packet.py:157-240 — observation-record validation and replay.

mbcx01_build_cohort_packet.py:253-331 — FACT ancestry/canonical-world derivation.

mbcx01_build_cohort_packet.py:383-535 — manifest construction and validate_build_manifest.

mbcx01_build_cohort_packet.py:639-728 — actual scoring/render path.

mbcx01_build_cohort_packet.py:731-852 — exact-subtractive scorer wrapper.

mbcx01_build_cohort_packet.py:879-1067 — outcome seam and BUILD inference ingress.

test_mbcx01_build_cohort.py:582-660 — W21 ghost-FACT witness.

test_mbcx01_build_cohort.py:1329-1595 — W15 observation non-leakage witnesses.

verify-build-bundle.py:720-930 — W14 registration totality.

Findings
F1 — semantic FACT discriminator is not load-bearing on the served path

EXECUTED · UNSEARCHED — SETTLED-BY-PINNED-BYTES
Data consequence: WRONG EVIDENCE ADMITTED.

The implementation has the correct discriminator. validate_build_manifest() replays state, derives legitimate FACT rows from journal ancestry and refuses a ghost with:

BUILD_FACT_ROW_WITHOUT_JOURNAL_ANCESTRY.

The problem is that build_scoring_fixture_for_candidate() at mbcx01_build_cohort_packet.py:639-673 does not call that validator. It checks only the frozen project_state_world() equality. The frozen projector copies FACT/OBSERVATION rows rather than re-deriving them—the exact weakness W21 documents.

Fresh attack:

Generate the real 960-candidate cohort.

Take one retained source candidate.

Add FACT.GHOST.NO.JOURNAL to its chosen-cut canonical world.

Add that ghost to the candidate's BC selected-object IDs so it will actually be model-visible.

Rebuild source provenance and a fresh BuildRetainedAuthorityContext from those candidate bytes.

Build the served manifest and execute the real scoring/render paths.

Results:

manifest_validator =
    ['BUILD_FACT_ROW_WITHOUT_JOURNAL_ANCESTRY']


ghost_in_BC_A0 = True


verify_build_scorer_input = []


render_all_six_nodes admitted = True

So the implementation possesses a correct red witness but the actual route to the model goes around it.

The existing W21 test exposes why this happened. At test_mbcx01_build_cohort.py:615-637 it mutates a manifest, invokes validate_build_manifest() directly and correctly sees RED. It does not reconstruct a self-consistent candidate/provenance/context and then exercise the serving constructor.

I separately confirmed that explicit validate_committed_identity() would reject the modified context:

baseline identity = []
modified identity =
    ['BUILD_RETAINED_COHORT_AUTHORITY_INVALID']

That is useful defense, but it does not close this path: the scoring/render functions do not invoke committed-identity validation or the semantic manifest validator. The current bundle proves the deterministic baseline generator's committed identity; it does not make arbitrary subsequently supplied BUILD contexts semantically self-authenticating.

A journal-less FACT can therefore become BC model-visible evidence. That can change the BC response and hence the recorded BC/OM pair.

Fix class: COHORT_SERVE_BOUNDARY_SEMANTIC_REDERIVATION.

F2 — ObservationAuthority admission verifies self-consistency, not derivation

EXECUTED · UNSEARCHED — SETTLED-BY-PINNED-BYTES
Data consequence: WRONG EVIDENCE ADMITTED.

The current generator is clean: the mandatory W15 tests all pass, and in my generated retained population I found no literal gold/action ID in the observation records.

But admission verifies an ObservationAuthorityV1 principally by shape, projection hash and its own record hash. It never proves that the record is the output of derive_observation_authority() for its declared allowed projection.

I constructed exactly that missing differential:

Start with one real retained candidate.

Change its observation authority's code to the candidate's literal gold action ID.

Change its observation rows consistently.

Recompute the authority record_hash.

Rebuild the two observation representations and canonical-world rows from that forged—but internally consistent—record.

Rebuild source provenance and retained context.

Execute manifest/scoring/render admission.

Results:

validate_observation_authority_record = True


validate_build_manifest = []


served_top_observation_is_gold = True


verify_build_scorer_input = []


render_all_six_nodes admitted = True

Then I independently invoked the generator's actual derivation law using the very projection stored in that authority:

fresh_derivation_matches_forged = False
expected_code = FACT.DEPTH.1

So this is not a subtle alternate encoding produced by the approved derivation. It is a non-derived authority record which every downstream gate accepts because the record is self-consistent.

The gold action therefore reaches the model as explicit observation evidence. That can directly inflate model success and contaminate the scientific number.

Again, explicit committed-root validation would reject the modified population. But the served boundary does not perform that check or observation re-derivation.

Fix class: OBSERVATION_AUTHORITY_DERIVATION_BINDING.

Together F1/F2 form one conceptual class: generator-owned semantic facts must be independently re-derived before serving, not merely hashed after construction. No new subsystem is needed.

Ten agenda rulings
1. Replay gate — SOUND

EXECUTED.

Fresh candidate mutations:

event_result_codes[0] = "LIE"
→ BUILD_EVENT_PROGRAM_REPLAY_MISMATCH


authoritative_state_hash_by_cut[chosen] = 000...000
→ BUILD_EVENT_PROGRAM_REPLAY_MISMATCH

The downstream reference replay reproduces the event codes and state digest rather than trusting recorded values. Generation's stronger dual-reducer gate is separately exercised by the 32-test cohort suite.

2. Eligibility derivation — SOUND

EXECUTED.

pop_declared_eligibility() on an enriched retained row returned DECLARED_ELIGIBILITY_BOOLEAN. After the declared keys were removed, chosen_cut_id still made the enriched row differ from the exact raw BUILD_CANDIDATE_KEYS source shape, so a retained result is not silently re-admitted as a source candidate.

I also toggled generation.envelope_admitted on a raw candidate. candidate_is_eligible() remained unchanged. The admission flag is not being laundered back into eligibility authority.

3. Envelope admission — SOUND

EXECUTED.

I compared admission-binding versus final-binding unpadded lengths for retained positions 0 and 767. For every A0/B/A1 × BC/OM node:

true_served_length - admission_length <= 0

with maximum difference 0.

The binding widths justify that shape: retained position 767 is already the maximum three-digit position and all substituted digest fields remain fixed-width 96-hex values.

Fresh exact-edge probe also found a packet with canonical UTF-8 length exactly 65,536, and the adopted frozen renderer accepted it with a final served size of exactly 65,536.

W13 then exercised all six real final renders across the entire retained set inside the 32/32 green suite.

4. Ghost evidence — DEFECTIVE

EXECUTED.

The discriminator itself is correct but is bypassed by the real serving route. F1 demonstrates a ghost FACT that:

is correctly refused by validate_build_manifest,

is actually present in BC A0,

gets verify_build_scorer_input == [],

passes all six render admission.

Consequence: WRONG EVIDENCE ADMITTED.

This is a deciding finding.

5. Observation non-leakage — DEFECTIVE at the authority/admission boundary

EXECUTED.

The pinned generator's derivation function and current retained output pass the W15 leakage suite. My attack is not a claim that derive_observation_authority() itself currently emits gold.

The failure is that a self-consistent observation record need not be derived by that function at all. F2 replaced its semantic value with the literal gold action, rehashed it, and successfully served it.

Consequence: WRONG EVIDENCE ADMITTED.

This is the second deciding finding.

6. Exact-subtractive wrapper — SOUND

EXECUTED.

Baseline BUILD scorer validation returned [].

Changing the separately supplied expected manifest's route contract and recomputing that manifest's own hash did not get swallowed by the I01 subtraction. The result retained independent failures including:

EXPECTED_MANIFEST_MISMATCH, packet/call/result mismatches, transition mismatch and I01_INVARIANT_INVALID.

Forging the BUILD cohort authority's candidate hash while repairing its own authority hash likewise returned:

BUILD_SCORER_INPUT_INVALID plus I01_INVARIANT_INVALID.

I found no route by which population-cascade subtraction erased an unrelated frozen defect.

7. BUILD inference ingress — SOUND

EXECUTED.

Fresh full 768-membership shape with one complete pair and 767 missing pairs reached the frozen numerical core and returned:

TRANSPORT_INCONCLUSIVE.

Then:

duplicate outcome receipt
→ BUILD_EPISODE_PARTITION_MISMATCH


outcome for a scenario partitioned as missing
→ BUILD_EPISODE_PARTITION_MISMATCH


duplicate episode/scenario identity
→ EPISODE_PARTITION_MISMATCH

The potentially lossy episode_by_scenario dictionary therefore did not create a last-wins acceptance: the frozen partition and final ordered equality kill those contradictory shapes first.

8. Plan arithmetic — SOUND AT THE PIN; residual hardening gap

EXECUTED.

On the committed population, every motif has:

16 family×omission joint strata,

exactly 10 draft rows per stratum,

zero unplanned refusals,

exactly 12 planned ineligibles.

I brute-forced the worst whole-stratum deletion capacity for every e ∈ [0,32]. Even if the refusal budget deletes the smallest possible complete strata first, every motif retains at least two strata of slack over the required placement count.

So _plan_placements() cannot short-place on the pinned domain and constants.

I also executed the driver's latent question against pathological off-domain input: twelve drafts all in one joint stratum with placed_total=12 makes _plan_placements() return only 1 placement. Thus the helper is not total in isolation, and recording placed_total instead of len(placements) would lie on that shape.

I do not count this as a §0 finding because that shape is unreachable through the pinned balanced generator with the registered refusal ceiling. A direct equality assertion is sensible BUILD hardening, but no current wrong number/evidence/refusal was demonstrated.

9. Census and sequence coverage — SOUND WITH THE DECLARED RESIDUAL

EXECUTED / SEARCHED.

At the pinned population:

joint-axis values containing "|" = 0


reported ordered-pair coverage = 150 / 289
ratio = 0.5190311418685121
declared floor = 0.40
meets floor = True

I independently recomputed:

all event-occurrence ordered pairs = 151
APPLIED-only ordered pairs         = 150

so the implementation's reported numerator exactly matches its declared APPLIED-only rule. Excluding the one NOOP-derived pair makes the figure more conservative, not inflated.

NIST's primary sequence-generation publication defines t-way sequence coverage using ordered events under a general labeled transition system and computes the valid t-way target sequences that must be covered.
NIST Computer Security Resource Center
 NIST's sequence-covering project likewise emphasizes event ordering and t-event permutations, including non-adjacent events.
NIST Computer Security Resource Center

The BUILD code does not claim it computed that LTS-reduced denominator. It explicitly registers the unconstrained 17×17 = 289 square as a superset, making its ratio a lower bound on an LTS-constrained ratio. That is conservative and accurately labeled.

10. Registration/identity — DEFECTIVE AS LITERALLY WORDED, NON-BLOCKING UNDER §0

EXECUTED.

The practical registration machinery is working:

normal check_registration_totality() → PASS;

adding a synthetic registered-but-absent module → W14_MODULE_GLOB_VS_REGISTRATION_MISMATCH;

raw working-tree spec normalizes to canonical LF bytes;

simulated CRLF bytes normalize to the same canonical artifact;

current committed identity validates [];

my modified population's identity fails BUILD_RETAINED_COHORT_AUTHORITY_INVALID.

But two literal claims in the design/agenda are stronger than the implemented verifier:

Level (b). Design says:

REQUIRED == pin-manifest-subject-set.

The verifier actually enforces:

REQUIRED ⊆ pinned.

Its own PASS report explicitly emits a nonempty level_b_pin_manifest_is_subset_not_equal containing the deliberately pinned frozen dependencies.

That implementation is sensible: literal equality would refuse RIGHT reconstruction merely because the pin manifest also carries its frozen dependencies.

Level (d). The verifier confirms that each module is named by a ledger row that states a behavior and carries a witness, but it explicitly reports that replacement sensitivity is not mechanically checked. That half rests on the red-first discipline.

So item 10 is DEFECTIVE as a statement of literal mechanics, but I do not promote it to a data finding at this pin. Registration is not silently missing anything I demonstrated, the synthetic omission probe fails loud, and current committed identity is correct.

Omission attack

The principal omission is now concrete: W21 tests the semantic discriminator, not the served mechanism.

test_bw71_red_w6_determinism_and_the_ghost_fact_discriminator deliberately proves that frozen projection accepts the ghost and that validate_build_manifest() rejects it. But it stops there. It does not ask whether build_scoring_fixture_for_candidate() and render_all_six_nodes() are forced through that same discriminator.

My fresh test did; they are not.

Likewise W15 extensively attacks the current generator's observation derivation, but no admission witness takes a self-consistent yet non-derived authority record and asks whether the served path independently proves it was actually generated by that law.

That distinction—testing the checker versus making the checker load-bearing—is the key acceptance defect in this round.

WHY THIS EXISTS
ALREADY-BUILT — EXECUTED

The engine correctly adopts rather than rebuilds substantial existing machinery: frozen cut selection/retention arithmetic, frozen reducers/renderer/numerical inference, and the lane's existing exact-subtractive state-authority pattern.

I independently spot-ran:

retained_set_root
sequence coverage
membership.substitut
cohort generator
ObservationAuthority

over:

agentvault-mcp-bridge/src

Photon/crates

Gravity/src

Result: zero files in all three.

So there is no sibling implementation of this MBCX population/retention/observation shape to adopt instead.

PRODUCT-FIT — READ-ONLY

Yes.

The customer need in one sentence: the owner needs 768 deterministic, varied scenarios whose model-visible evidence is genuinely derived from the registered journal and population law, or the experiment measures evidence the harness invented.

F1/F2 hit that exact product requirement: a green hash chain around semantically non-derived content is still the wrong experiment.

BIGGER-THAN-THE-BUG — READ-ONLY

No new machine is warranted.

The existing architecture already contains:

journal replay,

FACT ancestry derivation,

observation derivation,

manifest validation,

scorer admission,

retained authority.

The defect is that these existing semantic authorities are not all made load-bearing at the serving boundary.

The needed class stays inside the existing three-sibling design. If the fold requires changing the authority/interface direction between generator and packet sibling so observation derivation can be independently checked, packet §13 says that interface fold gets a fresh round. No frozen amendment is implicated by the evidence I found.

PRIMARY-CONSUMER — READ-ONLY

The immediate consumer is the BUILD packet/scorer/inference ingress; the ultimate consumer is the owner defending the experiment's one scientific number.

A bounded read of the provenance/census/coverage records buys something useful only if the actual model-visible canonical world and observation are tied to the same derivation—not merely to a fresh self-consistent hash chain.

SWEEP LOG

SEARCHED.

Exact queries:

site:csrc.nist.gov event sequence testing sequence covering arrays labeled transition system t-way sequence coverage


site:csrc.nist.gov "Efficient Algorithms for T-way Test Sequence Generation" labeled transition system

Opened at origin:

https://csrc.nist.gov/pubs/conference/2012/10/16/efficient-algorithms-for-tway-test-sequence-genera/final — deciding abstract: ordered event sequences, general labeled transition system, valid t-way target sequences.

https://csrc.nist.gov/Projects/automated-combinatorial-testing-for-software/combinatorial-methods-in-testing/event-sequence-testing — deciding sections "Need for Sequence Covering" and the SCA definition: ordering matters; t events need not be adjacent; sequence covering exercises order permutations.

https://csrc.nist.gov/pubs/ir/7878/final — deciding abstract: t-way coverage measurement can quantify partial combinatorial coverage of an existing test suite.

What changed: the sweep confirmed item 9's external vocabulary while sharpening its limitation. The NIST LTS formulation computes valid target sequences; MBCX currently uses an unconstrained registered superset and labels its result a lower bound. That label is materially important.

Why stopped: no other deciding finding rests on an external standard or prior art. F1/F2 and the other agenda rulings are pinned-byte/runtime questions.

Residual risks

The sequence-coverage figure remains the explicitly declared unconstrained-289 lower bound rather than an LTS-reduced coverage ratio. This is accurately disclosed at the pin.

_plan_placements() has a latent off-domain short-placement shape because it does not assert len(placements) == placed_total; current registered strata and refusal ceilings make it unreachable.

W14(d) remains half-mechanical: it proves module→named-behavior→witness registration, not replacement sensitivity.

The observation suite structurally excludes some forbidden inputs rather than perturbing every class at runtime, as the packet already declares.

Dual-reducer agreement remains a pseudo-oracle: a shared semantic bug can survive both reducers.

The full tests emit two existing ResourceWarnings for unclosed fixture file readers in test_mbcx01_build_integration.py; all mandatory suites nevertheless complete OK. I found no measurement consequence from those warnings.

No physical or paid claims were exercised. The bundle itself reports production authority not activated, physical harness not executed, zero provider calls, and zero paid calls.

Fix class

Primary class: COHORT_SERVE_BOUNDARY_SEMANTIC_REDERIVATION.

It has two demonstrated leaves:

FACT_ANCESTRY_MUST_GATE_SERVED_PACKET

OBSERVATION_AUTHORITY_MUST_BIND_TO_DERIVATION

The acceptance property is simple: a candidate must not become model-visible merely because its candidate/provenance/authority bytes are mutually self-consistent; model-visible FACT and OBSERVATION evidence must survive independent re-derivation from the registered event program/state/allowed observation law at the serving boundary.

Both red constructions already exist in substance. The missing piece is making them exercise the actual serving path.

Because F1/F2 admit wrong evidence into the scientific packet, green suites and a green bundle are not sufficient to accept these bytes.

FINAL VERDICT: NO-GO.
