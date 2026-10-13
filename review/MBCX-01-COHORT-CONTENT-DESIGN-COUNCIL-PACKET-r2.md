# MBCX-01 cohort-content generator — DESIGN council packet r2 (issue #17)

Packet prose is a pointer map, not evidence — byte-check it.

ROUND LEDGER: council round 2 (r1: NO-GO / NO-GO / NO-GO, all EXECUTED — synthesis
`MBCX-01-COHORT-DESIGN-COUNCIL-R1-SYNTHESIS.md`, banked verdicts beside it) · codex rounds 0 of 2

## Verdict shape

GO / GO-WITH-FIXES(class) / NO-GO. DESIGN-class, round 2: no ROUND CALL token yet (it binds
from round 3); the PROPOSE lane's two questions apply after the verdict.

## Canonical bytes (read AT THE PIN — every 40-hex below emitted by `git rev-parse` and
gated by `git cat-file -e` before this packet shipped; the r1 fabricated-pin defect is closed)

- Artifact under review: `MBCX-01-BUILD-COHORT-CONTENT-DESIGN.md` (now r2) at commit
  `3614ae4790a2068a798731c29501ae91c3d177e7` — worktree
  `<repo>-build`,
  branch `codex/mbcx01-production-build`. A working-tree read must say so and confirm the pin.
- Round-1 record (context, not contamination — banked history of a completed round):
  `MBCX-01-COHORT-DESIGN-COUNCIL-R1-SYNTHESIS.md` ·
  `MBCX-01-COHORT-R1-DRIVER-REPRODUCTIONS.md` · the three banked r1 verdicts — same commit.
- Frozen bytes (read-only, unchanged): `mbcx01_r13_measurement.py` · `mbcx01_r13_packets.py`
  (esp. `:18` ENVELOPE_BYTES, `:34-116`, `:158-196`) · `mbcx01_r13_common.py` ·
  `mbcx01_r13_state_reference.py` / `mbcx01_r13_state_oracle.py` · `verify-build-bundle.py`.
- Governing DoR set: design r9 + R10 spec + closure architecture + invariant matrix +
  amendments 1–3 — same commit.

## Immutable truths / invariants

- **NO THREAT MODEL in this lane's DoR** — VALIDITY review; a finding counts only with a named
  wrong-number / wrong-evidence-admitted / right-evidence-refused consequence; person-blocking
  proposals are ruled out under the owner's standing discriminator.
- Zero `*_r13_*` edits; `FROZEN_TEST_TOTAL` stays 156; frozen selection arithmetic adopted.
- Estimand, n=768, route, inference frozen and out of scope.
- Consumers of the population, enumerated: the BUILD manifest sibling (new, §2 module 3) ·
  the BUILD authority path (new, module 2) · the frozen scorers/inference downstream · the
  carriers FD/FC/TN (#18-#20). r1 established the frozen
  `manifest_for_retained_candidate`/`retained_scenario_authority` CANNOT consume this
  population (seat-1 F1/F2, executed) — that is now the design's own premise; attack it.

## Claims to attack (the r2 surface; label EXECUTED or READ-ONLY)

No REAL adversary class exists in this packet; every declaration is a validity question.

1. **R1 — one observation record, two representations.**
   ADVERSARY: internal-consistency — the served packet contradicting itself or its journal.
   REACHES IT VIA: in-process code — our own generator; no boundary crossed (validity question, never a control)
   Claim: §2.2's ObservationAuthorityV1 (one deterministic record per scenario/cut from which
   BOTH the top-level observation and the world OBSERVATION row derive; endogenous FACT rows;
   `observation_authority_hash` in provenance) closes the r1 drift channel wholesale. Attack:
   construct a divergence W15 would miss, or show the derivation rule cannot be both
   deterministic and scientifically meaningful as a variation axis.
2. **R2 — quota eligibility.**
   ADVERSARY: internal-consistency — a floor that faults on honest input or a filter that biases the science.
   REACHES IT VIA: in-process code — our own selector; no boundary crossed (validity question, never a control)
   Claim: exactly-k-per-motif (k ≤ 32, declared, framed-hash ranked, stratified across the
   three ineligible shapes, world-size distribution witness) makes the ≥128 floor arithmetic
   and bounds the bias channel. Attack: a distribution the stratification + witness still
   admits that biases the retained set on a BC/OM-relevant axis.
3. **R3 — the three-sibling scope is complete.**
   ADVERSARY: author-blind-spot — a fourth consumer or module the driver did not name.
   REACHES IT VIA: in-process code — the driver's own scoping; no boundary crossed (validity question, never a control)
   Claim: generator + authority + manifest siblings, landing together, reach W7 end-to-end
   with no further frozen consumer needing a sibling. Attack: name the missing module or the
   frozen consumer that still flattens or refuses the population downstream of the manifest.
4. **R4 — each motif contract is realizable and its postcondition witnessable.**
   ADVERSARY: internal-consistency — a contract the frozen reducers cannot produce (the r1 restoration class).
   REACHES IT VIA: in-process code — our own event programs against frozen reducers (validity question, never a control)
   Claim: the six contracts in §2.1 (restoration-by-reassertion · lifecycle transitions ·
   blocked→due flip · in-scope collision + zero-foreign-rows · duplicate proposal AND commit
   NOOPs + role rewrite + B-call record · delayed due transition) are each producible by legal
   programs and discriminated by their postcondition witnesses. Attack BY EXECUTION where you
   can: run a candidate program against the frozen reducers and refute a postcondition.
5. **R5 — the inverted coverage invariant.**
   ADVERSARY: internal-consistency — an invariant that cannot fail for the failure it exists to catch.
   REACHES IT VIA: in-process code — our own census; no boundary crossed (validity question, never a control)
   Claim: alphabet-scoped statement + named exclusions + measured 1-way/2-way over
   (event × lifecycle-position) reported in provenance is falsifiable for omissions. Attack:
   an omission or interaction blind spot the measurement still hides; whether 2-way over that
   pair is the right matrix.
6. **R6 — envelope-at-admission.**
   ADVERSARY: internal-consistency — an unservable or identity-unstable population.
   REACHES IT VIA: in-process code — our own renderer; no boundary crossed (validity question, never a control)
   Claim: rendering BC+OM at generation and refusing oversize candidates PRE-selection keeps
   the cohort deterministic and servable (refused candidates are part of the deterministic
   plan, not a data-dependent surprise). Attack: an interaction between admission-refusal and
   the quota arithmetic or the retention ordering that makes cohort identity input-sensitive.
7. **R7 — W10 operationalizes the sentinel.**
   ADVERSARY: internal-consistency — a green suite over a scientifically dead population.
   REACHES IT VIA: in-process code — our own witnesses; no boundary crossed (validity question, never a control)
   Claim: "gold read-sets take ≥ N distinct values and the BC/OM read-set difference is
   non-degenerate" is the right executable form of "the 768 can discriminate BC from OM".
   Attack: a population passing W10 that still cannot answer the research question.
8. **R8 — totality and pin discipline.**
   ADVERSARY: internal-consistency — a green bundle that never covered the new modules.
   REACHES IT VIA: in-process code — our own registration; no boundary crossed (validity question, never a control)
   Claim: glob-vs-tuple two-way + REQUIRED==manifest-subjects + BUILD_WORK_PRODUCTS
   registration + rev-parse/cat-file pin gates close r1's C7/F0 classes. Attack: the
   registration or pin route that still slips through.

## Red witnesses per closed class

The design closes r1's classes ON PAPER; every closure is `pending` until the build lands
red-first. W1–W15 are declared in design §4; W10/W11/W12 are RED TODAY BY CONSTRUCTION against
the frozen layer. Attack the witness set again: name an r2 defect no W would catch.

## Executable-attack lane (ALL seats)

The frozen generator/selector/reducers/packet-builder are pinned Python; the r1 probes are in
`driver-repro-cohort-r1.py` and the banked verdicts. Execute at least one fresh probe of your
own against the r2 surface (R4 especially). Label every finding and the verdict EXECUTED or
READ-ONLY; a round with zero EXECUTED verdicts is incomplete.

## Omission attack (≥1 seat)

What does r2 still not name? Candidates: a consumer of the SERVED packet beyond the manifest
(scorers' assumptions about the stamp?); observation-family semantics leaking gold; the
mechanism-omission configuration interacting with motif contracts; anything the three-sibling
cut leaves orphaned in the repair ledger.

## WHY-THIS-EXISTS (all four, every seat)

- ALREADY-BUILT: selection/authority pipeline adopted from the frozen layer (executed r1,
  3/3); content half absent (executed, 3/3: ONE world across 960); no sibling-repo generator
  (seat-1 three-repo spot-run, zero hits). Verify the internal-shelf log below; spot-run a query.
- PRODUCT-FIT: the research harness's own subject — a population able to discriminate BC from
  OM. Every refusal stops a wrong number; none stops a person; flag any that does.
- BIGGER-THAN-THE-BUG: the producing half the DoR names as missing (#17-#22); r1 confirmed it
  is TWO stamps in TWO layers — the three-sibling scope is proportionate to that finding, not
  an expansion; attack that proportionality if you disagree.
- PRIMARY-CONSUMER: the manifest sibling and scorers consume candidates; inference consumes
  the 768; carriers consume the worlds. r1's lesson is folded: the consumer that could not
  consume the population is now inside the slice.

## Non-claims

No scientific run, route, spend, physical execution, frozen edit, or root ratification (#4);
no H/D/F twins (#23); no Merkle tree; no security posture. Population exclusions declared in
design §5 (target-reopen excluded; bounded taxonomy; frozen-cohort-scoped inference;
generator-authored observation truth under §2.2's law).

## Search lens

Run your own search where a claim rests on prior art (swarm/omission testing, combinatorial
coverage, differential-oracle discipline, deterministic population design). Sweep to
sufficiency; label SEARCHED / RECALLED / UNSEARCHED(reason); return your SWEEP LOG. An
UNSEARCHED/RECALLED finding cannot decide a prior-art claim; if no seat sweeps such a claim
the round is incomplete on it. If you cannot reach the web, say so — a capability report.

## Seat SWEEP lane (every seat, both sides)

- SWEEP APPLIES TO: claims resting on prior art or named practice — chiefly R5 (coverage
  matrices), R1 (derived-observation design), the PROPOSE lane, and any external mechanism a
  seat brings; lane-byte claims may be labelled UNSEARCHED(SETTLED-BY-PINNED-BYTES).
- DELIVERABLE: a SWEEP LOG in your verdict — exact queries · what you OPENED (origin + the
  deciding section) · what it changed or confirmed · why you stopped.
- LABELS: SEARCHED · RECALLED (argument, never deciding evidence) · UNSEARCHED (with reason:
  NOT-LOAD-BEARING / SETTLED-BY-PINNED-BYTES / COULD-NOT / DID-NOT).
- CONSEQUENCE: an UNSEARCHED or RECALLED finding cannot be the deciding GO on a prior-art
  claim; a round where no seat swept such a claim is INCOMPLETE on it.
- HONEST OUT: if you cannot reach the web this session, one plain line — capability report,
  not a discharge.

## PROPOSE lane (design-class; after the verdict)

1. What would you build? Name mechanism + prior art (labelled).
2. Would you do it differently than r2 proposes — and why?

## Internal-shelf log (the driver's own internal sweep)

- QUERIES: r1's query set (`synthetic_candidates` · `select_cohort` · `evaluate_eligibility` ·
  `MOTIFS` · `retained_set_root` · `motif` · `eligib` · `generator`) plus this round's
  `manifest_for_retained_candidate` · `retained_scenario_authority` · `_source_authority` ·
  `ENVELOPE_BYTES` · `BUILD_WORK_PRODUCTS` — driver-run 2026-08-16 across both lane dirs.
- REPOS: the Selene lane in full. agentvault-mcp-bridge / Photon / Gravity EXCLUDED with
  reason (population defined over THIS lane's frozen reducer semantics; no sibling carries an
  MBCX reducer consumer) — and independently CONFIRMED by seat 1's r1 spot-run across all
  three sibling repos: zero hits.
- OPENED: (each with adopt-or-why-not) the r1 set plus, this round at the byte:
  `mbcx01_r13_packets.py:158-196` (REPLACE via manifest sibling — the second stamp),
  `:370-395` + `:337-345` (REPLACE via authority sibling), `:18` (ADOPT ENVELOPE_BYTES as the
  admission constant), `verify-build-bundle.py:408-481` + `:321` (EXTEND: totality
  assertions), `mbcx01_r13_common.py:16-65,97-167` (ADOPT event grammar + make_event),
  driver replay-pair execution on both reducers (P1).
- STOPPED: when every r1 finding had a driver reproduction or an explicit partial label and
  every consumer named by the r1 round had an adopt/replace/extend disposition.

## Search log (the driver own external sweep)

- External: none run by the driver this round; the r2 prior-art positions (swarm testing ·
  NIST coverage criteria · differential-pseudo-oracle) were SEARCHED at origin by r1 seats and
  are cited in the banked verdicts; the driver adopted them in bounded form. Seats: treat any
  further external angle as YOUR sweep lane — the driver's claims this round rest on the
  lane's own executed bytes.

## Premises, byted pre-send

- The three r1 verdicts and their execution evidence — banked in-tree, driver-reproduced
  where acted on (`MBCX-01-COHORT-R1-DRIVER-REPRODUCTIONS.md`; C3's binomial reproduced to
  four decimals; P1/P2/P3 executed; P4 partial and labeled; P5 read at the byte).
- The r2 design pin above — emitted by rev-parse, cat-file-gated.
- The frozen files' identity — unchanged through the r1/r2 records commits (`git diff --stat`
  design-pin..HEAD touches records and the design only).

## Re-review trigger

Architecture/interface changes (candidate shape, authority surfaces, module set) re-round;
declared-constant VALUES (k, minimums, envelope constant, coverage floors) are BUILD test
material. From round 3 the ROUND CALL binds: GO-TO-CODE outranks further design findings.

## Blind round

Sealed, independent first pass; no seat sees another's r2 view (r1's banked record is history,
available to all). No driver recommendation rides this packet — the pinned r2 design is the
proposal.
