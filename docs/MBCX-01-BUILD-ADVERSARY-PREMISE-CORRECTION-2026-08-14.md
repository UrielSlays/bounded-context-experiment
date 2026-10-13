# MBCX-01 BUILD — premise correction: the adversary these rounds probed does not exist

Written 2026-08-14 by the BUILD driver, after the OWNER challenged the premise in live chat and was
right. This file supersedes the framing (NOT the evidence) of the r1/r2/r3 acceptance packets and of
`MBCX-01-BUILD-ACCEPTANCE-ROUND-r{2,3}-SYNTHESIS.md`.

## The byte that settles it

```
grep -niE "threat model|adversary|attacker|untrusted|api-caller|hostile" \
  MBCX-01-EXPERIMENT-DESIGN-r9.md MBCX-01-R13-CLOSURE-ARCHITECTURE.md \
  MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md
  -> ZERO hits
```

The design of record has no threat model, because it is not a security artifact. Its seventeen
invariants are a **scientific-validity device**: `MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md` §1 —
*"Every row represents one fact expressed in two places… The join is valid only when the listed
equality is mechanically reproduced from independently admitted inputs."* Every "adversarial
witness" in that matrix is **the experiment fooling itself**: a self-consistent non-member candidate
rehashed (I01), a legal same-cut state with one obligation changed (I02), a receipt replayed under
another scenario (I05), *"caller supplies naked bits… or substitutes a same-scenario scorer graph
from another episode"* (I10), *"inject real key/root or flip production flag"* (I13), *"packet
builder self-signs/injects its root"* (I14), *"self-authors PASS, flips production mode"* (I16).

§3 states the whole point in the design's own words: `FIXTURE_ONLY` *"may test parsers, signatures,
reducers and join logic; **cannot create an experiment-eligible score or physical pass**."*

## What went wrong in the review rounds

The r1 BUILD acceptance packet declared `ADVERSARY: api-caller — a contractually-untrusted caller
supplying scorer inputs and V2 receipts`. **There is no such caller.** MBCX-01 has no API, no
production runtime and no external submitter; every caller of these authorities is the harness and
its own tests. An actor who can run code in that process **is the box owner**, and on-box walls
against the box owner are theater — the permanent T2 ceiling, `DESIGN-SHELF-MAP.md` §1.

r2 and r3 **inherited that declaration verbatim** and the driver never byte-checked the premise —
the exact failure LAW ZERO's packet-premise rule names (*"a packet's load-bearing PREMISE is a CLAIM
— byte it BEFORE the packet ships"*). It is also a near-repeat of the Muninn slice-3 A-4 case
recorded in ANTI-DRIFT §7: the packet handed all three seats the T2 ceiling as an immutable truth
and then asked questions that invited off-tenet answers, and all three seats duly went hunting
in-process gadgets. Fields are context; questions are instructions; a seat works the instruction.

⚠ `packet:check` passed GREEN on all three packets and this is not its failure: its own header says
*"It checks PRESENCE + SHAPE, never TRUTH. A well-formed packet with a stupid adversary line passes,
by design."* Canon requires a REAL class to carry `ADMITTED AT: <path>:<symbol>`; the gate enforces
it **zero** times (`grep -c ADMITTED src/council-packet-check.ts` → 0). Handed to the #716 lane.

## The recut — what is real and what is theater

**REAL, built, red-witnessed, clean-room verified — these ARE the DoR:**

| Built | DoR row it satisfies |
|---|---|
| Production admission requires an independently configured trust root the signer cannot edit | **I14** — witness: *"packet builder self-signs/injects its root"* |
| Fixture material cannot grant production authority at any door | **I13** / **I16** / §3 authority modes |
| A binding-only exactness result cannot present as `PASS` | **I16** — witness: *"self-authors PASS"* |
| Trust-root validity judged at the verifier's clock, never a date carried inside the artifact | validity/staleness (a stale root silently counting is self-deception) |
| One signature, one carrier (strict base64) | receipt identity / dedup hygiene |

**THEATER — accepted residual, named, ZERO grind (TAR-PIT decision matrix):** an actor able to run
code inside the verifier's process can edit the anchor or the context (`object.__setattr__`, a
mapping subclass with behaviour). That actor is the box owner. **We are tamper-EVIDENT, not
tamper-proof.** The r2 wiring-freeze rider built against this class is being REVERTED — ANTI-DRIFT
§1, *revert self-inflicted machinery rather than complete it* — and it additionally carries a real
reliability cost in a long unattended run, because it can only ever FALSE-fire (`_VERIFICATION_DEPTH`
is a plain module int; `threading` is never imported).

## Status of the review rounds after the recut

- **r1 NO-GO: stands.** Its finding was a genuine I13/I14 violation.
- **r2 GO-WITH-FIXES: stands for its named closes** (fixture isolation, clock, exactness labelling,
  carrier); its gadget-defence half is void.
- **r3 NO-GO: DOES NOT STAND.** It rests on the `object.__setattr__` class, which is theater. The
  round's genuinely useful residuals were the two P3s (a fixture key recognised by a flag rather
  than by key material — MITRE CWE-1291; and the non-atomic depth counter), and the second one
  disappears with the freeze.
- `OPEN-OWNER-DECISIONS` **row 68 is WITHDRAWN** by the driver, same day it was filed.

Nothing was spent. No experiment, provider call, route qualification, physical grid, Job/ETW
collection or signing ceremony has occurred. The frozen r13.2 design is untouched at 145/145.
