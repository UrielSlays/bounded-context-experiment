# MBCX-01 cohort-content generator — DESIGN council packet r1 (issue #17)

Packet prose is a pointer map, not evidence — byte-check it.

ROUND LEDGER: council round 1 (no prior rounds on this artifact) · codex rounds 0 of 2

## Verdict shape

GO / GO-WITH-FIXES(class) / NO-GO. This is a DESIGN-class artifact: after the verdict, answer the
PROPOSE lane's two questions. Round 1 — no ROUND CALL token required yet.

## Canonical bytes (read AT THE PIN)

- Artifact under review: `MBCX-01-BUILD-COHORT-CONTENT-DESIGN.md` at commit `b18d7ab`
  (repo `<private-repo>`, branch `codex/mbcx01-production-build`; local worktree
  `<repo>-build`).
  A working-tree read must say so and confirm it matches the pin.
- Governing design of record (frozen, read-only): `MBCX-01-EXPERIMENT-DESIGN-r9.md` ·
  `MBCX-01-R10-ARCHITECTURE-SPEC.md` · `MBCX-01-R13-CLOSURE-ARCHITECTURE.md` ·
  `MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md` · amendments 1–3 — same commit.
- Frozen bytes the design diagnoses: `mbcx01_r13_measurement.py:203-334` (world stamp, declared
  eligibility, selection) · `mbcx01_r13_packets.py:34-116` (gold/legality predicates,
  `project_state_world`) · `mbcx01_r9_reference.py:777-796,820-821` (the eligibility
  high-water mark) · `mbcx01_r13_common.py:16-65` + `mbcx01_r13_state_reference.py:126-416` +
  `mbcx01_r13_state_oracle.py:128-148` (the 17-event legal alphabet).
- Design-history basis: `MBCX-01-EXPERIMENT-DESIGN-r4.md:243-287` (the only motif prose) ·
  `MBCX-01-EXPERIMENT-DESIGN-r3.md:168-215` (the lost envelope + class counts) ·
  `MBCX-01-EXPERIMENT-DESIGN-r5.md:205-240` (H/D/F content semantics, currently non-normative).

## Immutable truths / invariants

- **This lane's DoR carries NO THREAT MODEL.** The trigger-family grep over design-r9 +
  closure architecture + invariant matrix returns zero hits
  (`MBCX-01-BUILD-ADVERSARY-PREMISE-CORRECTION-2026-08-14.md`). This round is a VALIDITY
  review, not a security review: the only "adversary" is the experiment fooling itself. A
  finding proposing a person-blocking control will be adjudicated under the owner's standing
  discriminator (does it stop a WRONG NUMBER, or a PERSON?) and dies if the latter.
- The frozen r13.2 layer is untouchable: zero `*_r13_*` edits; `FROZEN_TEST_TOTAL` stays 156.
- The frozen selection pipeline (`choose_one_cut` · retention hash · 128/motif · 768 ·
  retained-set root) is ADOPTED, not redesigned.
- Estimand, n=768, route, inference are frozen and out of scope (r13.2 3/3 CONFIRMED).
- Consumers of the governed thing (the candidate population), enumerated: the manifest builder
  (`mbcx01_r13_packets.py:157` `manifest_for_retained_candidate`) · the retained-authority join
  (I01, `mbcx01_r13_packets.py:900-902`) · the provenance validator
  (`mbcx01_r13_measurement.py:277-301`) · the scorers/inference downstream of the manifest ·
  the future carriers FD/FC/TN (#18-#20) whose selectors run against these worlds. Each must
  honor the new population's shape or the design must say why it cannot.

## Claims to attack (construct the bypass; label EXECUTED or READ-ONLY)

Each ruling proposing a mechanism carries its declaration. No REAL adversary class is declared
anywhere in this packet — the governing design has no threat model to cite, so a REAL class
would be a phantom by this council's own precedent.

1. **C1 — the stamp diagnosis is true at the frozen bytes.**
   ADVERSARY: internal-consistency — the instrument misdescribing its own population.
   REACHES IT VIA: in-process code — our own generator and validators; no boundary is crossed and no external party exists (validity question, never a control)
   Claim: every r13 candidate in a motif carries an identical world and a declared
   `"eligible": True` read back at `mbcx01_r13_measurement.py:321` under a `RECOMPUTED` label
   (`:317`); the motif does no semantic work. Attack: execute the frozen generator and refute
   any part of this at the byte.
2. **C2 — journal-replay as state authority.**
   ADVERSARY: internal-consistency — hand-written state drifting from the journal it claims to summarize.
   REACHES IT VIA: in-process code — our own generator and validators; no boundary is crossed and no external party exists (validity question, never a control)
   Claim: deriving `canonical_state_by_cut` by replaying each candidate's event program through
   BOTH frozen reducers (I15 leveraged at generation) makes illegal or drifted states
   unrepresentable by construction. Attack: name a candidate shape the manifest needs that
   replay-derived state CANNOT express. Known seam, attack it first: OBSERVATION world rows are
   exogenous (no observe-event exists in the 17-event alphabet; `project_state_world` passes
   them through from the manifest) — is the design's obligation/dependency-from-replay,
   observations-generator-authored split sound, or does it reintroduce the drift channel?
3. **C3 — derived eligibility that filters.**
   ADVERSARY: internal-consistency — a selection stage that selects nothing (the current degeneracy).
   REACHES IT VIA: in-process code — our own generator and validators; no boundary is crossed and no external party exists (validity question, never a control)
   Claim: routing eligibility through the packet layer's own gold predicate
   (`mbcx01_r13_packets.py:34-52` equivalent) + deliberate hash-placed ineligible shapes makes
   selection do real work while staying deterministic and guaranteeing ≥128 eligible per motif.
   Attack: construct a distribution where the guarantee and the filtering are in tension, or
   where the ineligible-shape placement biases the retained set on a scientifically relevant
   axis.
4. **C4 — the reopen ruling.**
   ADVERSARY: internal-consistency — two frozen expectations contradicting on a legal event.
   REACHES IT VIA: in-process code — our own generator and validators; no boundary is crossed and no external party exists (validity question, never a control)
   Claim: constraining the GENERATOR (scored target never reopened post-commit in-window)
   closes the r7 seat-1 conflict (`MBCX-01-SEAT1-OUTSIDE-OPUS5-VERDICT-r7.md:113`) without
   editing frozen semantics. Attack: is the constraint enforceable at generation and witnessable
   (W9), and is the alternative (amending the A1-gold clause via #23) actually the honest close?
5. **C5 — the motif expansion.**
   ADVERSARY: author-blind-spot — the driver chose the program families.
   REACHES IT VIA: in-process code — the driver's own design choices; no boundary is crossed (validity question, never a control)
   Claim: the six program families in design §2.1 faithfully expand r4:249-254 under the current
   reducer semantics (incl. CROSS_SCOPE_COLLISION as name-collision because cross-scope
   delegation/dependency are illegal at the reducers). Attack: name a mechanism a motif's phrase
   implies that the program family omits, or a program element the reducers refuse.
6. **C6 — the 64 KiB ceiling.**
   ADVERSARY: internal-consistency — a population the instrument cannot serve.
   REACHES IT VIA: in-process code — our own generator and validators; no boundary is crossed and no external party exists (validity question, never a control)
   Claim: r3-envelope-informed variation bounds can produce non-trivial worlds whose served
   packets stay under the exact 65,536-byte pad (`MBCX-01-R10-ARCHITECTURE-SPEC.md` §4;
   overflow = pre-dispatch design failure). Attack: estimate at the byte — does a
   30-obligation world with catalogs and padding fit? If not, the design's "bounds are
   build-time constants" defers a constraint that shapes the whole population; say so.
7. **C7 — registration without weakening the bundle.**
   ADVERSARY: internal-consistency — a new module invisible to the two-way ledger.
   REACHES IT VIA: in-process code — our own generator and validators; no boundary is crossed and no external party exists (validity question, never a control)
   Claim: the design §3 registration list (BUILD_MODULES · BUILD_TEST_MODULES · one-letter
   WITNESS_ID widening · ledger rows/namespace/totals · `$buildSubjects` · parity docs) keeps
   every new witness inside the governed namespace with two-way totality intact. Attack: name a
   path by which the new module's tests run green while invisible to
   `verify-build-bundle.py`'s ledger check.

## Red witnesses per closed class

This design CLOSES nothing yet — it declares the witness set (design §4, W1–W9) the build must
produce red-first. The packet claims no closure; every W is `pending` until the build lands its
red. Attack the witness SET for non-discrimination: name a defect in the design that no W would
catch.

## Executable-attack lane (ALL seats)

The artifact is a design note, but its load-bearing DIAGNOSIS is executable: the frozen
generator and selector are pinned Python. Every seat: (a) execute the frozen generator
(`synthetic_candidates_r13` + `select_cohort`) and verify or refute C1 at the byte; (b) run any
fresh probe of your own against the frozen predicates the design adopts
(`_unique_gold_action`, `legal_action_ids_from_world`, `project_state_world`); (c) label every
finding and the verdict EXECUTED or READ-ONLY. A round with zero EXECUTED verdicts on this
diagnosis is incomplete.

## Omission attack (≥1 seat, all seats welcome)

What did the author NOT name? Candidates: a content axis the BC/OM discrimination question
needs that neither the motif programs nor the variation axes provide; a frozen consumer of the
candidate shape not in the enumeration above; a determinism channel (dict ordering, float,
locale) the seedless design misses; a reason the frozen `_source_authority` sub-digest shape
cannot carry journal-bearing candidates (design Item 7c); the deferred H/D/F decision hiding a
constraint that must be decided NOW rather than at #23.

## WHY-THIS-EXISTS (build-decision gate — answer all four, every seat)

- ALREADY-BUILT: The selection/authority pipeline IS already built and this design adopts it
  (`mbcx01_r13_measurement.py:304-412`); the content half is refuted-at-the-byte absent — the
  existing "generator" stamps one world 960 times (`:203-274`). Verify the Internal-shelf log
  below; spot-run at least one of its queries.
- PRODUCT-FIT: This is the research harness's own subject — the population that lets the
  instrument output accurate, discriminating numbers. Every refusal in the design stops a wrong
  number (fake population, laundered predicate), none stops a person. If you find one that
  stops a person, that is a finding under the owner's standing discriminator.
- BIGGER-THAN-THE-BUG: The engine is the DoR's missing half, not a review-finding's costume —
  r13 closure §10 scoped the verification half; issues #17–#22 name the producing half; this
  packet IS the design gate that work re-enters.
- PRIMARY-CONSUMER: The manifest builder and scorers consume the candidates; the scientific
  inference consumes the population; the carriers (#18–#20) consume the worlds as their
  selection problem. A bounded read of the generator's output buys the packet layer real worlds
  with derivable gold — the thing the current stamp cannot give it.

## Non-claims

No scientific run, no route, no spend, no physical execution, no frozen-file edit, no owner
ratification of the new cohort root (that is #4), no H/D/F content twins (a #23 decision row),
no Merkle tree, no security posture of any kind. The excluded surfaces were swept: the frozen
suites keep the synthetic fixture population (grep: no frozen test imports the BUILD module —
it does not exist yet); the exclusion of H/D/F rests on `MEASUREMENT-CONTRACT-v7.json`'s
disjoint `cohort`/`grid` objects, byte-read this session.

## Search lens

Run your own online search where a claim rests on prior art or practice (property-based /
metamorphic test-population generation, deterministic scenario synthesis, preregistered cohort
design). Sweep to sufficiency; label SEARCHED / RECALLED / UNSEARCHED(reason); return your
SWEEP LOG (queries · what you OPENED · what it changed · why you stopped). A finding labelled
UNSEARCHED or RECALLED cannot be the deciding GO on a prior-art claim; if no seat sweeps such a
claim the round is incomplete on it. If you cannot reach the web, say so in one line (a
capability report, not a discharge).

## PROPOSE lane (design-class; after the verdict)

1. What would you build? Name the mechanism and the prior art you'd take it from (labelled).
2. Would you do it differently than this design proposes — and if yes, why?

## Seat SWEEP lane (every seat, both sides)

- SWEEP APPLIES TO: every claim in this packet resting on prior art, a standard, or named practice — in this round chiefly C5 (the motif expansion vs any published scenario/population-generation practice), the PROPOSE lane, and any external mechanism a seat brings; claims resting only on this lane's own pinned bytes may be labelled UNSEARCHED(SETTLED-BY-PINNED-BYTES).
- DELIVERABLE: a SWEEP LOG in your verdict — exact queries · what you OPENED (URL/file + the
  deciding section) · what it changed or confirmed · why you stopped. Sweep to SUFFICIENCY,
  never to a source count.
- LABELS: every prior-art / standards-bearing finding carries exactly one — SEARCHED (opened at
  origin this session) · RECALLED (carried from memory, not opened — admissible as argument,
  never deciding evidence) · UNSEARCHED (with its reason: NOT-LOAD-BEARING /
  SETTLED-BY-PINNED-BYTES / COULD-NOT / DID-NOT).
- CONSEQUENCE: an UNSEARCHED or RECALLED finding cannot be the deciding GO on a claim resting
  on prior art or a standard; a round in which NO seat swept such a claim is INCOMPLETE on it.
- HONEST OUT: if you genuinely cannot reach the web this session, say so plainly in one line —
  a seat-CAPABILITY report, never a discharge.

## Internal-shelf log (the driver's own internal sweep)

- QUERIES: `synthetic_candidates` · `select_cohort` · `evaluate_eligibility` · `MOTIFS` ·
  `retained_set_root` · `motif` · `eligib` · `generator` — run by the driver 2026-08-16 across
  both lane directories (design council root + build worktree), plus two banked Explore sweeps
  whose every load-bearing cite the driver re-opened at the byte.
- REPOS: the Selene lane (both directories) in full. agentvault-mcp-bridge / Photon / Gravity
  EXCLUDED, with reason: the artifact is a scenario population defined over THIS lane's frozen
  reducer semantics (17-event alphabet, frozen predicates); the sibling repos carry no MBCX
  reducer or cohort consumer, and the adopt-target the sweep seeks — an existing generator for
  these exact semantics — can only live in this lane's own lineage, where it was found (r8→r13).
- OPENED: (each with adopt-or-why-not) `mbcx01_r13_measurement.py:20-27,203-334` (ADOPT selection
  pipeline; REPLACE the stamp + declared Boolean) · `mbcx01_r13_packets.py:34-116` (ADOPT gold
  predicate as the eligibility authority) · `mbcx01_r9_reference.py:777-796,820-821` (ADOPT the
  derivation + Boolean-pop pattern) · `mbcx01_r13_common.py:16-65` (ADOPT canonical
  JSON/hash helpers + event grammar) · `MBCX-01-EXPERIMENT-DESIGN-r3.md:168-215` (ADOPT as
  scaling reference; not normative) · `-r4.md:243-287` (ADOPT the six names) · `-r5.md:205-240`
  (NOT adopted: H/D/F content twins — no current normative mandate; #23 decision row) ·
  `MBCX-01-MEASUREMENT-CONTRACT-v7.json` (cohort/grid disjointness confirmed) ·
  `mbcx01_build_measurement_authority.py:1-229` (ADOPT the versioned-sibling + closed-error
  pattern).
- STOPPED: when the full r8→r13 generator lineage was mapped, every historical variation axis
  enumerated, and every candidate-consuming surface in the lane identified — further search
  could only re-find the same lineage.

## Search log (the driver own external sweep)

- External: no web search run for this packet — the population design is experiment-internal
  and rests on the lane's own DoR set (read in full this session) and its council record;
  prior-art claims in the design are all internal cites. Seats: treat any external-practice
  angle as YOUR sweep lane — that asymmetry is deliberate (driver builds the claim from the
  governing bytes; seats refute from the world).

## Premises, byted pre-send (each verified by the driver this session)

- The motif names have no prose definition beyond r4:249-254 — byte-read.
- The stamp + laundering — byte-read at `:203-334` (quoted lines verified).
- r9's derivation + Boolean-pop — spot-verified via sweep cites.
- `cohort`/`grid` disjoint in contract v7 — byte-read.
- No seat has ruled on cohort content; C5 UNDERDETERMINED r9/r11/r12 — verdict files opened by
  the archaeology sweep; the r2 and r7 seat cites re-quoted from the sweep's opened files.

## Re-review trigger

Architecture/interface changes to the design (candidate shape, eligibility authority, motif
family structure) re-round; build-time constant values (bounds, minimum counts) are BUILD test
material, not design-round fuel. The build lands red-first under the standing loop either way.

## Blind round

Sealed, independent first pass. Do not seek or reference other seats' views. This packet
carries no driver recommendation among open options — the pinned design is the proposal.
