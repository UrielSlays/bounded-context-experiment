# MBCX-01 cohort-content generator — DESIGN council packet r3 (issue #17)

Packet prose is a pointer map, not evidence — byte-check it.

ROUND LEDGER: council round 3 (r1: NO-GO / NO-GO / NO-GO · r2: GO-WITH-FIXES / NO-GO / NO-GO, all EXECUTED — syntheses `MBCX-01-COHORT-DESIGN-COUNCIL-R{1,2}-SYNTHESIS.md`, banked verdicts beside them) · codex rounds 0 of 2

## Verdict shape

**ROUND CALL BINDS THIS ROUND: your verdict's FIRST LINE is exactly one of `GO-TO-CODE` or
`CONTINUE-DESIGN: <one sentence why>`.** GO-TO-CODE outranks further design findings; a finding
a test suite would catch (byte shapes, presence laws, enum spellings, ordering, declared
constants) is BUILD red-witness material, named for the build's test list, never a reason for
another round. Then GO / GO-WITH-FIXES(class) / NO-GO and the PROPOSE lane's two questions.

## Canonical bytes (read AT THE PIN — every 40-hex below emitted by `git rev-parse` and
gated by `git cat-file -e` before this packet shipped; the r1 fabricated-pin defect is closed)

- Artifact under review: `MBCX-01-BUILD-COHORT-CONTENT-DESIGN.md` (now r3) at commit
  `ded124f66ab10b18e9cb08e46c471287a2bc9c33` — worktree
  `<repo>-build`,
  branch `codex/mbcx01-production-build`. A working-tree read must say so and confirm the pin.
- Round record (banked history of two completed rounds): both syntheses, both driver
  verification records, all six banked verdicts — same commit.
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

## Claims to attack (the r3 folds; label EXECUTED or READ-ONLY)

No REAL adversary class exists in this packet; every declaration is a validity question. Each
item is one r2 fix class folded — attack the FOLD, not the already-settled architecture.

1. **S1 — the fourth surface is truly closed.**
   ADVERSARY: internal-consistency — a frozen consumer the enumeration still misses.
   REACHES IT VIA: in-process code — our own scoring path; no boundary crossed (validity question, never a control)
   Claim: module 3 supplying `authoritative_state` from replayed generation state (W18) plus
   the exact-subtractive scorer/outcome wrapper (W16) reaches every population-dependent
   frozen call site; the design's §1 four-surface enumeration is complete. Attack: walk the
   frozen call graph fresh (as r2 seat 1 prescribed) and name a fifth surface, or a route by
   which a BUILD candidate still defaults into `_fixture_authoritative_state`.
2. **S2 — contracts now carry their constructions.**
   ADVERSARY: internal-consistency — a contract whose obvious construction yields a different code.
   REACHES IT VIA: in-process code — our own event programs against frozen reducers (validity question, never a control)
   Claim: §2.1's realization column (byte-identical replay for the NOOPs; exact code
   sequences per motif) makes every W4 witness discriminating. Attack BY EXECUTION: find a
   motif row whose stated construction produces a different code sequence on either reducer,
   or a legal ambiguity the exact-code clause still admits.
3. **S3 — observation non-leakage.**
   ADVERSARY: internal-consistency — the served packet carrying its own answer.
   REACHES IT VIA: in-process code — our own derivation rule; no boundary crossed (validity question, never a control)
   Claim: the closed grammar + forbidden-input list + the two-part witness (no gold/action
   encoding; relabeling invariance) close the r2 leakage class wholesale. Attack: an encoding
   channel the two-part witness misses (ordering, cardinality, family-choice correlation with
   gold), or show the forbidden-input list is not closeable at build.
4. **S4 — total-admission quota + multivariate census.**
   ADVERSARY: internal-consistency — a floor that faults on honest plans or a census that misses a deleted stratum.
   REACHES IT VIA: in-process code — our own selector; no boundary crossed (validity question, never a control)
   Claim: composing every refusal class into the arithmetic and censusing all declared axes
   closes r2's family-deletion and envelope-composition findings. Attack: a plan the
   arithmetic admits that still faults, or a stratum deletion the axis census cannot see.
5. **S5 — renderer-delegated envelope.**
   ADVERSARY: internal-consistency — a comparator diverging from the frozen boundary.
   REACHES IT VIA: in-process code — our own admission; no boundary crossed (validity question, never a control)
   Claim: admission = both renders succeed (unpadded ≤ 65,536; exact-fit legal) matches the
   frozen semantics exactly, and refused candidates stay a pure function of the spec. Attack:
   any residual divergence from `render_served_input`'s behavior, incl. the padded-hash
   downstream (`served_input_hash` requires exactly 65,536).
6. **S6 — sequence coverage is the right primary.**
   ADVERSARY: internal-consistency — a coverage number measuring the wrong dimension.
   REACHES IT VIA: in-process code — our own census; no boundary crossed (validity question, never a control)
   Claim: LTS-constrained ordered-pair sequence coverage over the alphabet (reducers as the
   LTS), with presence + event×position as secondary, is the right provenance claim and
   composes with the omission-configuration axis. Attack: a reducer-sensitive ordering
   property ordered PAIRS cannot see (is the length-2 floor enough to claim what the
   provenance record will be read as claiming?), or a conflict between omission configs and
   SCA coverage targets.
7. **S7 — four-level registration totality.**
   ADVERSARY: internal-consistency — a green bundle over an unregistered or untested artifact.
   REACHES IT VIA: in-process code — our own registration; no boundary crossed (validity question, never a control)
   Claim: glob-vs-tuple (both ways) + REQUIRED==manifest-subjects + artifact-namespace
   totality + module-to-witness coverage (W14) close every registration route found in r1+r2.
   Attack: the route that still slips — incl. artifacts outside the `MBCX-01-BUILD-COHORT-*`
   glob and witnesses that exercise a module only trivially.

## Red witnesses per closed class

The design closes two rounds' classes ON PAPER; every closure is `pending` until the build
lands red-first. W1–W18 are declared in design §4; W10/W11/W12/W16 are RED TODAY BY
CONSTRUCTION against the frozen layer. Attack the witness set once more: name an r3 defect no
W would catch.

## Executable-attack lane (ALL seats)

The frozen generator/selector/reducers/packet-builder are pinned Python; the r1 probes are in
`driver-repro-cohort-r1.py` and the banked verdicts. Execute at least one fresh probe of your
own against the r3 folds (S1/S2 especially). Label every finding and the verdict EXECUTED or
READ-ONLY; a round with zero EXECUTED verdicts is incomplete.

## Omission attack (≥1 seat)

What does r3 still not name? Candidates: a fifth frozen surface; an encoding channel in the observation grammar; an SCA/omission interaction; a frozen coupling beyond the three recorded (MANIFEST_KEYS, frozen motif six, retained_position); anything the widened module 3 leaves orphaned.

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
