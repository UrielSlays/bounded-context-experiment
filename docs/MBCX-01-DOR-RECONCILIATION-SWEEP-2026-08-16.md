# MBCX-01 DoR reconciliation sweep (#23) — 2026-08-16 — **RATIFIED (all three groups)**

> OWNER RULING, 2026-08-16 live chat, verbatim: *"Anyways, ratify. And then continue."* — all
> three groups ratified in one sitting. Additional owner directive in the same ruling: the
> target-reopen class must NOT evaporate — it is preserved as the declared MBCX-02 follow-up
> (filed on the board), conditional on a positive MBCX-01 primary result. Every Group A/C
> sentence below is now APPLIED to the frozen docs with dated amendment markers; Group B closes
> #27 and #4.

**What this is, in crayon:** the frozen design papers were written before the machine existed.
The machine now exists (verification half + the cohort engine). This sweep walks every frozen
sentence that no longer matches reality and PROPOSES the amendment sentence — **nothing moves
until the owner ratifies** (the A-1/A-2 precedent). The scientific content — estimand, n=768,
route gate, inference math — is untouched by every proposal below; these are truth-of-prose
corrections, ratifications already owed, and rulings made this session that need their DoR
sentence. This document is also the start of the "one place" rebuild map the owner asked for:
each item carries the byte pointer to where reality lives.

**Sweep basis:** the full frozen set read at the byte this session (design r9 · R10 spec ·
closure architecture · invariant matrix · amendments 1–3) against the lane state at slice-#17
close (`02fbac6`, remote == local; bundle real exit 0; frozen 156 / BUILD 229 / ledger 98/229).

---

## GROUP A — factual staleness: frozen prose that is now simply false or outdated
*(No science changes. Ratifying A means: "make the paper tell the truth about the machine.")*

**A1. "The physical harness remains absent" — no longer true.**
- Frozen: `MBCX-01-R13-CLOSURE-ARCHITECTURE.md:72`.
- Reality: the ETW consumer, collector, and Windows producer are BUILT and red-witnessed
  (BUILD suite; three codex rounds folded 25 defects; A-2/A-3 amended the measurement
  semantics). NOT yet executed against a live ETW session — the smoke run (#2) remains the
  only thing that can settle the live half.
- Proposed sentence: *"The physical harness is BUILT and witness-covered but has never
  executed against a live ETW session; every live-platform fact remains unverified until the
  elevated smoke run. The signed receipt represents the evidence required by the prose, not
  Boolean claims about it:"* (replacing the first sentence of :72 only).

**A2. "Merkle-style SHA-384 retained-set root" — the implementation is a flat root, and a tree was deliberately declined.**
- Frozen: `MBCX-01-R13-CLOSURE-ARCHITECTURE.md:55`.
- Reality: `mbcx01_r13_measurement.py:363` computes SHA-384 over the canonical JSON of the
  ordered 768-hash array — no tree, no inclusion proofs. The cohort design councils (r1–r3)
  examined building a true Merkle tree and DECLINED it (no consumer; no-adversary law).
- Proposed edit: *"a SHA-384 retained-set root computed over the canonical ordered list of
  all 768 candidate hashes (a flat list digest; a Merkle tree with inclusion proofs was
  considered and declined — no consumer exists for per-candidate proofs)."*

**A3. The r9 authority-order versions are r10-era.**
- Frozen: `MBCX-01-EXPERIMENT-DESIGN-r9.md:32-33` — names `MBCX-01-R10-PIN-MANIFEST.json`
  and "the four machine-readable v5/v4/v4/v5 contracts."
- Reality: the governing pin is the r13/BUILD manifest lineage; contracts moved to
  v8/v7/v7/v8 through the amendment process.
- Proposed: a one-line dated supersession note under :38 — *"[2026-08-16: the authority
  order's concrete artifacts are superseded by the r13.2 closure (§9) and the BUILD pin
  manifest lineage; this section's PRINCIPLE (no later chat message or uncommitted byte can
  silently change a frozen value) is unchanged and governs.]"* Original preserved in place.

**A4. The machine-wide Kernel-Process provider constraint is unrecorded in the DoR.**
- Reality: the collector's provider is machine-wide with member filtering downstream (#3);
  the smoke run may abort on a busy host — a real, discovered platform constraint.
- Proposed: one sentence in `MBCX-01-R13-PHYSICAL-HARNESS-REQUIREMENTS.md` (supported-
  environments block): *"The Kernel-Process ETW provider is machine-wide; membership is
  enforced by downstream filtering, and a capture on a non-idle host may abort rather than
  degrade — an abort is the correct fail-loud outcome."*

## GROUP B — ratifications already owed (the owner's buttons, bundled)

**B1. Amendment-3 (#27) — first-member-interval baseline.** Implemented on the branch with
red witnesses on the A-1/A-2 pattern; the r7 totality rule closed its ambiguity; the accepted
undercount it fixes was wrong by 2× the boundedness threshold. ASK: ratify A-3 as written
(the veto is a revert of its commits).

**B2. Cohort identity roots (#4) — now TWO constants to ratify.** The frozen synthetic
(fixture) root `38A62E8C…AE6F…` (post-A-1/A-2 value, recorded in the open-issues record) and
the BUILD cohort root `7EDCD5AC2FD1D7975D8FBFEC4D7314FF3CB171D1DC45A41C1564B3420EB395BE18DB7F7B51C18B9D8CDB1867CB8C0399`
(committed in `MBCX-01-BUILD-COHORT-GENERATOR-V1.json`'s identity block, W8-witnessed,
determinism-proven across processes). ASK: ratify both numbers as the cohort identities of
record; any future change to either is a declared amendment, never maintenance.

## GROUP C — rulings made this session that need their DoR sentence
*(Each was council-executed and driver-verified today; the sentence records it.)*

**C1. Target-reopen population exclusion.** The generator never reopens the scored target
post-commit inside the scored window (frozen A1-gold expectation preserved without editing
frozen semantics; W9-witnessed). Proposed closure-architecture sentence (§5 call-ledger area):
*"The scientific population excludes target-reopen episodes by generator constraint; BC/OM is
never measured over a scored-target reopen, and the A1 no-recurrence expectation is preserved
by construction rather than by verifier change."*

**C2. Motif content ownership pointer.** The frozen DoR names six motifs nowhere in prose
(they exist only in code and the r4-era design history). Reality: motif SEMANTIC CONTRACTS
(postcondition + realization construction + exact result codes) are owned by
`MBCX-01-BUILD-COHORT-CONTENT-DESIGN.md` (r6 FINAL), council-closed GO-TO-CODE. Proposed
r9 sentence (§Frozen experiment): *"Motif content semantics are owned by the BUILD cohort
design of record; the frozen layer constrains the taxonomy to the six named motifs and their
totals, not their content."*

**C3. Two methodological positions the novelty sweep showed we owe in writing** (rationale
addenda, not frozen-content changes — proposed as a short addendum doc):
  (a) *Freeze-and-attest vs randomization:* the measurement-bias literature's published remedy
  is setup randomization; this lane freezes and attests instead. The honest argument: our
  claim is a preregistered TOLERANCE on a DIFFERENCE (max−min across H at fixed (D,F)) under
  one attested environment — randomization defends point estimates against bias;
  a within-environment difference with a signed environment is the quantity our design
  actually registers, and cross-environment generalization is deliberately NOT claimed.
  (b) *One-sided −0.10 margin vs two-sided TOST:* the estimand is non-inferiority (is BC not
  materially worse), not equivalence (are they the same); the one-sided form is the correct
  match to the research question, and the stricter two-sided form would answer a question the
  design does not ask. Both positions to be recorded in a
  `MBCX-01-METHODOLOGY-POSITIONS` addendum with the sweep memo as the citation base.

**C4. The two signed-field semantic changes from the codex arc** (`counter_value` =
member-attributed accumulator; `root_process_start_key` carries the ETW-published
ProcessSequenceNumber) are already corrected in `MBCX-01-MEASUREMENT-CONTRACT-v7.json` prose
per the council's ruling of record; the sweep verifies NO further frozen-prose site restates
the old semantics (grep clean this session). No action; recorded as checked.

---

## The ask (one sitting, three words each)

1. **Group A** — "ratify A" makes four stale sentences true (no science moves).
2. **Group B** — "ratify B" closes #27 and #4 (A-3 + both cohort roots).
3. **Group C** — "ratify C" records today's three rulings + commissions the methodology
   addendum.

Any single item can be vetoed by name; a veto reverts that item's commits and nothing else.
Until ratification, NOTHING in the frozen set has been edited — this document is the
proposal, the frozen bytes are untouched (verifiable: `git diff <r13.2-base> HEAD -- 
MBCX-01-R13-*.md MBCX-01-EXPERIMENT-DESIGN-r9.md MBCX-01-R10-ARCHITECTURE-SPEC.md` shows
only the owner-ruled A-1/A-2/A-3 changes).
