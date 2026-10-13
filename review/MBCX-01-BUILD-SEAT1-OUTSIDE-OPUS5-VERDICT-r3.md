# MBCX-01 BUILD acceptance r3 — SEAT1 (Opus 5 Extra, <council-browser-port>) verdict — banked from thread

Banked by the driver 2026-08-14 from conversation `<id>`
(model label read back as "Opus 5 Extra" before dispatch). Packet
`MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r3.md@e2e6c662`; code pin `aa3d0b1a`.
Streaming trace omitted; verdict body verbatim.

## 1. Verdict — **GO. — EXECUTED.**

The `MBCX01-BUILD-R2-FIXTURE-ISOLATION` fold closes the r2 class. I hunted the second path the
packet asked for and found none reachable by data; I attacked the wiring-freeze rider on all five
axes it named and it held on every one; and the r2-confirmed set reproduces intact under the new
required-context interface. Two P3 residuals below, neither meeting the re-review trigger.

Longitudinal disclosure (my own lane, labelled): at r2 I returned GO after building an attacker
universe without the anchor key, and the class was still open through our own committed material.
This round I varied that knob first — the committed fixture anchor and its committed private key, at
all three doors — before touching anything else.

## 2. Pins and provenance — EXECUTED

```
packet commit e2e6c662 == HEAD ; packet blob 82b7054f identical in tree and at the pin
code pin aa3d0b1a is an ancestor of the packet commit
tree-vs-pin DRIFT = 0 across all 15 canonical subjects -> my working-tree reads ARE the pinned bytes
committed anchor: fixture_only=true, public_key_pem only, NO private half (read at the pin)
BUILD suites  : Ran 95 tests ... OK   (was 86 at r2)
frozen suites : Ran 145 tests ... OK
```

⚠ **Capability report, honestly:** I did not obtain a usable answer on the packet's `git archive`
method note. My verification loop mis-resolved `rev-parse` twice and produced first "0 mismatches"
then "359 mismatches" — both were my own broken probe, not evidence about the artifact, and I
discarded both. I compensated exactly as the r2 seats did: per-subject blob equality (DRIFT=0) plus
the suites, and I ran every probe against the working tree I had byte-verified. I also did not run
`verify-build-pinned.ps1` to completion in one window; the driver's completion claim stands
unchallenged by me.

Evidence read (path:line@aa3d0b1a): `mbcx01_build_trust_anchor.py:193-231` (anchor), `:233-291`
(`ProductionVerifierContext`), `:294-336` (wiring + freeze), `:398-467`
(coerce/new/configure/scoped install), `:469+` (clear); `mbcx01_build_measurement_authority.py:473`,
`:836`; `mbcx01_build_state_authority.py:498`; `mbcx01_build_exactness_authority.py:27-29, 66,
189-227`; `MBCX-01-BUILD-OWNER-TRUST-ANCHOR.fixture.json` (whole).

## 3. Findings

### C-R3-1 — non-production material cannot grant production authority → HOLDS. EXECUTED.

```
fixture private key IS committed (FIXTURE_OWNER_PRIVATE_KEY_PEM present)  True
D1 measurement, committed fixture anchor + committed fixture key
     -> ["PHYSICAL_HARNESS_UNAVAILABLE","PRODUCTION_TRUST_ANCHOR_FIXTURE_ONLY"]
D3 exactness,  same
     -> MeasurementAuthorityError: PRODUCTION_TRUST_ANCHOR_FIXTURE_ONLY
```

Second-path hunt — every constructor enumerated and driven:

```
A1 ProductionVerifierContext(anchor=fixture)          -> PRODUCTION_VERIFIER_CONTEXT_FIXTURE_ANCHOR_REFUSED
A2 new_production_verifier_context(fixture object)    -> same
A3 new_production_verifier_context(fixture DOCUMENT)  -> same
A4 new_production_verifier_context(fixture PATH)      -> same
A5 configure_owner_trust_anchor(fixture)              -> ACCEPTS the anchor, installs context = None
A6 configure_production_verifier_context(fixture)     -> PRODUCTION_VERIFIER_CONTEXT_INVALID
public constructor surface: ProductionVerifierContext · new_production_verifier_context ·
                            configure_production_verifier_context · resolve_production_verifier_context
```

No data path builds a context around a `fixture_only` anchor. A5 is the design working as
documented — labelling test material as your root is allowed; granting production authority to it is
not, and the refusal lands at the authority. The fixture lane stays usable, which is the point.

Two sequences did succeed and I name them precisely so they are not mistaken for a bypass: **A7**
(`object.__setattr__` to flip `fixture_only` on the anchor) and **A9** (`object.__setattr__` to swap
a built context's anchor). Both require bypassing Python's attribute protocol from inside the
verifier process — squarely the fold's own declared T2 boundary. Not a finding against the fold. The
`ProductionVerifierContext.__setattr__/__delattr__` guards do refuse the normal protocol.

### C-R3-2 — no request-reachable mutation, and the FREEZE rider is sound → HOLDS. EXECUTED.

```
B1 nesting/re-entrancy   depths 1 -> 2 -> 1 -> 0 ; rewire at depth 2 refused
                         OWNER_TRUST_ANCHOR_WIRING_DURING_VERIFICATION:configure_owner_trust_anchor
B2 exception mid-scope   depth after RuntimeError = 0  (NOT stuck — try/finally holds)
B3 FAILED verification   wiring object identity preserved across the failed door (before is after = True), depth=0
B4 scoped install + exc  installed_production_verifier restored prior wiring after an exception inside = True
B5 threads               thread A depth 1 -> 1 across a 0.4 s window; thread B rewire during A
                         -> refused (cross-thread freeze held) ; final depth 0
```

The counter-not-flag choice is correct and I verified the reason it exists
(`verify_production_scorer_input` legitimately nests the state door). **On the rider's contested
naming: I do not contest `*_REWIRED_DURING_VERIFICATION` earning its own code.** It names an
operator/deployment fault, not an authentication outcome — collapsing it into
`ACTIVATION_UNAUTHENTICATED` would tell an operator "your signature is bad" when the truth is "your
process re-wired itself mid-verification."

### C-R3-3 — verifier's clock, never the artifact's → HOLDS. EXECUTED.

```
ctx current_time="1999-01-01T00:00:00Z" -> current_instant()=1999-01-01T00:00:00Z
ctx current_time="2099-01-01T00:00:00Z" -> current_instant()=2099-01-01T00:00:00Z
ctx current_time=None                   -> current_instant()=2026-08-14T20:48:21Z   (REAL clock)
rejected: "2026-08-14T00:00:00+00:00" · "2026-08-14 00:00:00Z" · "not-a-time" · ""
          all -> PRODUCTION_VERIFIER_CONTEXT_INVALID
```

On the scope call: judging manifest validity at the verifier instant while every other instant stays
the receipt's attested `knowledge_time` is the correct seam, not an inconsistency — the manifest is
the trust statement being relied on now, so its freshness must be the relier's clock; the receipt's
other instants are historical facts about a past event and must stay attested. I could not construct
an exploit across it.

### C-R3-4 — binding-only cannot read as "the suite ran" → HOLDS. READ-ONLY.

The only result value emitted or accepted is `BINDING_ONLY_RESULT =
"AUTHORITY_BINDING_ONLY_SUITE_NOT_EXECUTED"` (`:66`); a claimed `"PASS"` is explicitly rejected
(`:189-194`); the recomputed receipt hard-sets `"result": BINDING_ONLY_RESULT` (`:227`). Labelled
READ-ONLY: I did not drive a downstream consumer, so I am not certifying consumer behaviour.

### C-R3-5 — nothing r2 confirmed regressed → HOLDS. EXECUTED.

`context` is KEYWORD_ONLY with no default (required). Exactly two call sites, both in-lane
(measurement `:473`, state `:498`). No legacy/no-context branch reaches authentication.

⚠ **First run proved nothing and I re-ran it.** Under the fixture anchor every r2 axis
short-circuited at `PRODUCTION_TRUST_ANCHOR_FIXTURE_ONLY` — correct precedence, but it never
exercised the r2 codes. Re-run under a genuine production context (operator-built, over a key I minted):

```
CONTROL owner-signed, correct bindings         -> []                                   ADMITS
R1 NON-anchor key, bindings correct            -> PRODUCTION_ACTIVATION_UNAUTHENTICATED
R2 gen rolled back / manifest_digest repointed / authority swapped /
   signing_key_id changed / provenance_digest changed / custody digests emptied
                                               -> PRODUCTION_ACTIVATION_UNAUTHENTICATED (all six)
R2 same-manifest_id manifest mutation          -> MEASUREMENT_TRUST_ROOT_INVALID
R3 carrier whitespace / base64url / no padding -> MEASUREMENT_SIGNATURE_CARRIER_INVALID (all three)
R4 unanchored, legit evidence                  -> PRODUCTION_TRUST_ANCHOR_UNAVAILABLE
```

On the packet's SYMBOL-ABSENCE disclosure: I accept the trade and endorse the refusal to add an
optional-context path — the alternative would have re-opened the exact hole.

## 4. Residual risks

**P3-1 — the fixture key is recognised by a FLAG in a document, not by its key material.
EXECUTED + SEARCHED.**

```
context BUILT: anchor_id=MBCX01.RELABELLED.ANCHOR.1
context public key == committed fixture public key ?  True
key-material denylist of known test keys anywhere in repo:  NONE FOUND
```

Sits at the operator boundary (§2, out of scope) so it is not a NO-GO and not a re-review trigger.
But it is the exact weakness class MITRE names, and I opened it: **CWE-1291, "Public Key Re-Use for
Signing both Debug and Production Code", listed as a PeerOf CWE-321.** Cheap defence-in-depth:
refuse any anchor whose `public_key_pem` equals a known committed fixture key, regardless of the
flag. Fix class: defence-in-depth / codex gate.

**P3-2 — `_VERIFICATION_DEPTH` is a plain module int; `threading` is not imported. EXECUTED.**
The cross-thread freeze held in my test (the safe direction). Two residuals remain, both
deployment-shaped: (a) `x += 1` on a module global is load/add/store, so under genuinely concurrent
doors a lost increment could leave depth at 0 while a verification runs, re-opening the
between-doors window the rider exists to close; (b) the freeze is process-wide, so one thread's
verification denies another thread's legitimate operator rewiring — a liveness cost, not a security
one. Neither is reachable by an api-caller via data. Fix class: hardening / codex gate — a lock or a
per-thread counter, and the docstring should state the concurrency model it assumes.

**P3-3 — my own probe hygiene. EXECUTED.** Two probes this round produced readings I nearly
reported: the extraction check (both directions wrong) and the first C-R3-5 run (short-circuited
before the codes it claimed to test). Sixth consecutive MBCX round in which my probe, not the
artifact, was the broken thing.

Carried, unchanged, not reopened: T2 in-process ceiling · `ba28`'s real-clock time dependence
(`not_after` 2027-08-13) · inert-bytes model not done · BUILD A binds custody digests not documents ·
accumulate-then-refuse ordering · deferred exactness SUITE execution · `mbcx01_build_win32.py`
unexecuted · no production ceremony has occurred · not verified: that no consumer OUTSIDE this lane
calls `authenticate_production_activation` (confirmed only that no in-repo `.py` caller does).

## 5. SWEEP LOG

| Query | Opened | Effect | Label |
|---|---|---|---|
| CWE-321 hard-coded cryptographic key / test key shipped in source / production trust store mitigation | `cwe.mitre.org/data/definitions/321.html` — Relationships: PeerOf **CWE-1291**; Consequences: Bypass Protection Mechanism, Gain Privileges, Likelihood High; Mitigations at Architecture-and-Design | Sharpened P3-1 into a named class; MITRE places the mitigation at Architecture and Design, i.e. at context construction — exactly where the cheap fix goes | SEARCHED |
| Go `crypto/x509` VerifyOptions | not opened this round | Driver opened at origin; I verified the claimed behaviour against pinned bytes instead (`current_instant()` real-clock fallback) | RECALLED (corroborated by pinned bytes) |
| TUF out-of-band trusted root | not opened this round | I opened §5 Step 0 / §2.1.1 at origin in my own r2 verdict; unchanged by this fold | RECALLED |
| Ed25519 carrier malleability | not opened | Settled by executing three carrier mutations against the pinned check | UNSEARCHED (SETTLED-BY-PINNED-BYTES) |

## 6. WHY THIS EXISTS

**(1) ALREADY-BUILT? — ADOPT is correct; shelf log spot-run by me. EXECUTED.**
```
git grep -iE "process\.env\.[A-Z_]*(TRUST|ANCHOR|ROOT_KEY)" HEAD -- src   ->  0 hits
files mentioning "trust anchor" in src/                                  ->  6 (all compile-time / per-run pins)
```
The bridge has pinned anchors in abundance and no operator-config anchor loader to lift. Externally
the shape is Go's `VerifyOptions` plus TUF's out-of-band root — both adopted, neither invented.

**(2) PRODUCT-FIT?** An operator needs the system to refuse production authority to material this
repository ships, and to say by name that it refused because the root was test material.
`PRODUCTION_TRUST_ANCHOR_FIXTURE_ONLY` is that sentence in a code. The fixture lane stays usable,
which is the mirror-not-cop half — we do not make test material unusable, we make it unable to
authorize.

**(3) BIGGER-THAN-THE-BUG? — NO. The codex dissent is live and I rule against it, on my own
reading.** The minimum mechanism that fixes "our own committed fixture material authorized
production" is a value that cannot represent fixture material as production — a class with two
slots, one guard clause, and an immutability pair (~40 lines). No policy language, no key
management, no new subsystem. The strongest form of the dissent — that the freeze rider is a second
mechanism smuggled in under a fold — I also reject, and specifically because of the r2 record: a
snapshot alone left the gadget poisoning the process between doors, so the freeze is not an addition
to the fix, it is the part of the fix that makes the snapshot mean anything.

## 7. Fix class, re-review, side effects

No re-review trigger. P3-1 sits at the declared operator boundary, P3-2 at a concurrency model no
door currently uses, P3-3 is mine. Both actionable items are defence-in-depth / hardening → codex gate.

Side effects: none. HEAD unchanged at `e2e6c662`; nothing modified, staged, or committed; probes ran
in memory and `%TEMP%`, directories removed and verified absent. No experiment, provider call,
Job/ETW collection, ceremony, or spend.

---

## DRIVER NOTE (added at banking; not part of the seat's verdict)

Both P3s REPRODUCED by the driver at the byte before banking:
- **P3-1 confirmed.** A relabelled anchor document (`fixture_only` flipped to `false`, new
  `anchor_id`, same `public_key_pem`) built a production context, and its public key compared EQUAL
  to the committed fixture public key. Since the matching private half is committed at
  `mbcx01_build_ceremony_fixture.py:39`, one flipped flag in an operator document yields a
  "production" root whose private key is public. Cheap named refusal available at construction.
- **P3-2 confirmed.** `mbcx01_build_trust_anchor.py` imports `base64, contextlib, datetime, json,
  os, re, subprocess` — **no `threading`** — and `_VERIFICATION_DEPTH = 0` (`:319`) is mutated with
  `+= 1` (`:326`) / `-= 1` (`:330`) and read at `:334`. Non-atomic, exactly as reported.

Round status at banking: SEAT1 **GO** (this file) · SEAT3 codex-exec still executing · SEAT2
**capability-blocked** (Moonwalker MCP boundary returned `Unknown tool` for every call; the seat
correctly refused to produce a verdict — logged to `Dogfood.md` 2026-08-14). **The round is
INCOMPLETE on 2/3 and will not be rolled on.**
