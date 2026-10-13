# MBCX-01 BUILD acceptance round r4 — synthesis

Round complete at **3/3, every verdict EXECUTED** (the first complete BUILD round in this lane).

| Seat | Verdict | Basis |
|---|---|---|
| SEAT1 Opus 5 (fresh, model verified at mint) | GO-WITH-FIXES(TRUST-ROOT-KEY-IDENTITY · PIN-MANIFEST-FRESHNESS · CITATION-ACCURACY) | EXECUTED |
| SEAT2 ChatGPT Sol (fresh, connector restored) | NO-GO | EXECUTED |
| SEAT3 codex-exec (sol / default / xhigh) | NO-GO | EXECUTED |

**Round outcome: NO-GO.** Not by vote count. Two seats constructed and RAN falsifying probes; the
GO-WITH-FIXES seat says in its own last paragraph that its vote becomes NO-GO if the round is read as
authorising the ceremony. Per the authority ladder an executed bypass outranks a reasoned pass, and
here even the pass is conditional.

⚠ **Nothing scientific is corrupted.** Readiness remains
`BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`: no ceremony, no production root, no
experiment, no provider call, no spend. Every finding below corrupts something that has not happened
yet. That is the whole value of running the gate before the ceremony rather than after.

---

## Driver reproduction — what I re-derived at the byte myself

⛔ LAW ZERO / ANTI-DRIFT §1: a seat verdict is a pointer, including the GO. Nothing below entered this
synthesis on a seat's authority. Each line is my own executed probe or my own byte read.

### D1 — CONFIRMED · the canonical world omits two fields the design of record requires (SEAT2 F1)

The design of record, `MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md:35`, says the canonical world carries
*"all visible obligation IDs with **subject, owner role**, lifecycle, due time, critical flag and
sorted prerequisite IDs."*

The frozen implementation, `mbcx01_r13_packets.py:83-87`, projects five fields:
`lifecycle · critical · due_at · completion_action_id · prerequisite_obligation_ids`.
**`subject_id` and `owner_role` are not among them.** At `:365` both are supplied as flat defaults
(`SUB.SHARED` / `WORKER`) and then overwritten by the reduced field set, so they are never bound to the
manifest at all.

My own probe, built from the lane's own fixture manifest and state builder:

```
target obligation : OBL.DECOY
owner_role BEFORE : WORKER          owner_role AFTER : ROLE.FRESH.ADVERSARY
subject_id BEFORE : SUB.SHARED      subject_id AFTER : SUB.SUBSTITUTED

projection byte-IDENTICAL across the change : True
projection hash BEFORE : D743C7834F09AE52...D19725F3
projection hash AFTER  : D743C7834F09AE52...D19725F3   (equal)
```

**Why it is live rather than cosmetic** (the discriminator I ran before escalating): `owner_role` is not
a constant of the experiment. `mbcx01_r13_state_reference.py:222` (`delegate_obligation`) and `:216`
(`reopen_obligation`) both legally mutate it. So a legal transition in the experiment's own reducer
produces a state change that the canonical world cannot express and the manifest-cut check cannot see.

**Bounding it honestly:** because the field is not projected, it also cannot feed
`legal_action_ids_from_world`, so no *gold answer* changes today and no banked score is wrong. What is
false is the DoR's own claim about what the canonical world binds, and I02's promise that a legal
same-cut obligation change yields `MANIFEST_CUT_STATE_MISMATCH`. The banked I02 red witness mutates
`critical` — one of the five fields that IS projected — which is exactly why 145/145 stays green over
this hole.

⚖ **This is an OWNER call, not a driver fold.** Closing it changes a **frozen r13.2 artifact**: either
the frozen projection gains two fields, or the frozen matrix prose drops them. My own r4 packet listed
"zero frozen files may change" as an immutable truth, and the freeze rests on a 3/3 CONFIRMED council.
A driver cannot rule either way. → escalation row, below.

### D2 — CONFIRMED · trust-root identity is computed over the key's spelling, not the key (SEAT1 F1)

`public_key_identity` (`mbcx01_build_trust_anchor.py:418-433`) returns the base64 body as text. RFC 4648
§3.5 is explicit that where non-significant trailing bits are not zeroed there is no canonical
representation and multiple strings decode to the same bytes.

My own probe against the **committed anchor document**:

```
committed anchor SPKI bytes : 44
canonical body : MCowBQYDK2VwAyEAHt3A1PbOnMO1yjjssQWKpzaBOgzgAp0eIeVd9DvZ8zY=
variant  body  : MCowBQYDK2VwAyEAHt3A1PbOnMO1yjjssQWKpzaBOgzgAp0eIeVd9DvZ8zZ=
variant decodes identically : True

canonical body IN derived committed-key set : True
variant  body IN derived committed-key set  : False
identity(canonical) != identity(variant)    : True
```

Same 44-byte key, one different trailing character, and the fixture-key refusal no longer recognises
it. SEAT1 additionally executed the end-to-end admission through the documented
`MBCX01_BUILD_OWNER_TRUST_ANCHOR` OS-config door and got `ctx=True code=None` where the verbatim key is
refused by name. This is CWE-1291 at the exact seam the fixture-key fold was built to close, and the
fold's own claim — *"a fact about the key it carries"* — is falsified: it is a fact about one text
encoding of that key. The module already owns the cure one field away
(`strict_signature_carrier_ok` does decode/re-encode equality on `signature_b64`); `public_key_pem` gets
only prefix/suffix marker checks.

Not in-process, not T2: an operator-authored document through a documented door.

### D3 — CONFIRMED · the pin manifest does not authenticate the reviewed bytes, and my own packet claim was false

`MBCX-01-BUILD-PIN-MANIFEST.json` governs `3527f510…`; the review target is `4c7056e…`.
`git log --stat 3527f51..4c7056e -- '*.py'` returns `mbcx01_build_win32.py | 4 +++-` — **executable BUILD
source, changed after the pin.** The diff is comment-only (I read it: the discharged-ordinal note), so
no runtime byte differs and no scientific bypass follows.

But my r4 packet §14 asserted *"the four commits after the manifest pin are records/ledger files, not
BUILD source"* and offered `git log --stat 331f25b..HEAD` as the check. **That command is what falsifies
it.** Both seats caught it independently. The clean-room `PINNED RECONSTRUCTION COMPLETE` I ran and
banked pre-dispatch attaches to `3527f51`, not to the bytes under review — it is a true statement about
the wrong commit. Driver defect, mine, recorded here rather than quietly fixed.

### D4 — CONFIRMED · the ETW consumer trio (reproduced, then byte-audited by the driver)

Reproduced by a read-only worker; **every decisive byte below I then verified myself** against the
installed SDK header and the module source. The worker left the repo untouched (`git status --porcelain`
carries no tracked change).

**(a) Three constants disagree with the installed Windows SDK — and the one that is USED is the
dangerous one.** SDK of record: `C:\Program Files (x86)\Windows Kits\10\Include\10.0.26100.0\um\evntcons.h`
(the only version installed; all four names are evntcons.h-owned).

| constant | our code | SDK | what our value really is |
|---|---|---|---|
| `EVENT_HEADER_FLAG_CLASSIC_HEADER` | `0x0040` | `0x0100` (`:156`) | `EVENT_HEADER_FLAG_64_BIT_HEADER` (`:154`) |
| `EVENT_HEADER_EXT_TYPE_PROCESS_START_KEY` | `0x000A` | `0x000D` (`:63`) | `EVENT_HEADER_EXT_TYPE_EVENT_KEY` |
| `EVENT_HEADER_EXT_TYPE_EVENT_KEY` | `0x000B` | `0x000A` (`:60`) | `EVENT_HEADER_EXT_TYPE_EVENT_SCHEMA_TL` |
| `EVENT_HEADER_EXT_TYPE_PMC_COUNTERS` | `0x0008` | `0x0008` (`:58`) | correct — the one the packet's §10 sweep had settled |

**Driver refinement the seats did not make:** grep shows the two ext-type mismatches are *dead* —
defined, never read. But `EVENT_HEADER_FLAG_CLASSIC_HEADER` **is live**, at
`mbcx01_build_etw_consumer.py:1746`, on the CSwitch path:

```python
if not (int(header.Flags) & EVENT_HEADER_FLAG_CLASSIC_HEADER):
    return
```

That guard is meant to admit only classic kernel events before CSwitch decoding. With `0x0040` it is
testing the *64-bit header* bit instead. And its failure mode is `return` — a **silent record drop**,
not a fault. So the one wrong constant that executes sits on the path that produces instruction counts
and discards records quietly. This is the packet's Q6 claim ("a wrong value faults loudly") falsified
directly, and it is a stronger result than the seat's version.

**(b) The thread-lifetime join cannot succeed — `process_start_key` is a hard-coded `None`.**
`:1833` literally emits `"process_start_key": None` for every thread event (that append at `:1829-1833`
is the only writer to `_thread_events`). `_start_key_text` (`:844-845`) raises before the membership
check ever runs. Reproduced against the real decoder, with a control arm that isolates the cause:

```
assemble_thread_lifetimes(decoder thread_events, members)
  -> RAISED EtwConsumerFault: ETW_PROCESS_START_KEY_INVALID:None

control: identical events WITH a start key
  -> RETURNED [{'process_id': 4242, 'process_start_key': '00000001DEADBEEF', 'thread_id': 777, ...}]
```

The control is what makes this a finding rather than a fixture artifact. No payload-layout question can
rescue it: the `None` is a literal, not a decode.

**(c) Loss statistics are queried a second time after the session is stopped.** Order verified by me at
the bytes: `stop()` does `CloseTrace` (`:1518`, return value **not checked**) → `join(timeout=30)`
(`:1521`, **result not checked**) → `_query_loss()` (`:1522`) → `ControlTraceW(..., STOP)` (`:1525-1527`),
and never invalidates `_session_handle`; then `capture()` (`:1864-1870`) calls `_query_loss()` **again**
on that same handle. Modelled against Microsoft's documented `ControlTraceW` contract:

```
1. CloseTrace  handle=43981                                    returned=0
2. QUERY       session_stopped_before_this_call=False          returned=0
3. STOP        session_stopped_before_this_call=False          returned=0
4. QUERY       session_stopped_before_this_call=True           returned=4201 (ERROR_WMI_INSTANCE_NOT_FOUND)
   -> capture() RAISED EtwConsumerFault ... evidence unavailable
```

⚖ **Honest bound, and it cuts against the seats' framing:** the finalizer overwrites the post-stop
counters with the pre-stop ones (`capture.loss = loss`, `:1311`), so a *silently zeroed* second read
cannot corrupt the loss that gets signed. What the second query does is **abort the whole finalizer**
when the status is anything outside `(0, 234)` — fail-loud, not false-number. The real Windows status
for QUERY on a stopped session is `pending` (it needs the elevated run), so which arm fires is unknown;
the call-order defect itself is settled at the bytes and does not depend on it.

**Where that leaves SEAT3's headline** (a failed `CloseTrace` plus a live pump thread yielding a
signable delta of `700`): the unchecked `CloseTrace` return and unchecked `join` at `:1518`/`:1521` are
real and confirmed — the drain is genuinely not proven complete before the counters are read. Combined
with (a)'s silent `return`, the instrument has at least one path that discards evidence without saying
so. **The headline promise — never a number where evidence is missing — does not hold as written.**

---

## What survived, executed, in more than one seat

- **Q1 / I01** — a self-consistent non-member candidate with repaired hashes: refused
  `RETAINED_SCENARIO_AUTHORITY_INVALID` (SEAT2, SEAT3 independently).
- **Q2 / I05 / I10** — a same-scenario scorer graph from another episode, with container hashes
  repaired: refused `SCENARIO_OUTCOME_AUTHORITY_INVALID`; a flipped `COMPLETE_PAIR` class: refused
  `EPISODE_PARTITION_MISMATCH`.
- **Q3 (label half)** — relabelling the committed fixture anchor document does not change its key
  identity: refused `PRODUCTION_VERIFIER_CONTEXT_FIXTURE_KEY_MATERIAL`. (D2 is the *encoding* half,
  which is a different mechanism and does get through.)
- **Q4** — verifier-owned clock: a manifest valid 2000–2001 evaluated at 2050 refused
  `TRUST_ROOT_VALIDITY_EXPIRED`; SEAT2 confirmed the pattern against Go's `x509.VerifyOptions.CurrentTime`
  at the primary source.
- **Q7 / I16** — a receipt claiming `PASS` without execution: refused
  `CARRIER_EXACTNESS_SUITE_NOT_EXECUTED`.
- **Q8** — deliberate in-memory breaks turned targeted state, measurement, exactness and ETW witnesses
  RED. The suites are not greens that cannot fail. SEAT1 additionally found the one witness (`bw28`)
  that *cannot* discriminate its own named class, because its variant is constructed from the output of
  the normalizer under test — the author-blind-spot that let D2 live behind 114/114.
- **Q6 (struct half)** — the unpublished ETW struct sizes are re-derived from ctypes and honestly
  labelled; SEAT1 examined and cleared them. SEAT3 disputes the *constant values*, a different claim
  (D4c).
- **SEAT3 also refuted one of its own attacks** and recorded the negative: a synthetic roster containing
  an unrelated process was caught downstream by independent Job accounting
  (`PROCESS_MEMBERSHIP_INVALID` / `JOB_QUERY_EVIDENCE_INVALID`).

## Q9 — the three named fixture-key gaps, now ruled

- **Gap 2 is REACHABLE and must close before the ceremony.** SEAT2 executed it: the committed test
  signing pair, used as the production measurement signing root with an independently generated owner
  anchor, cleared production admission with `production_admission_errors = []` while custody documents
  asserted `private_key_never_leaves_custody: True`. The ceremony prose forbids it
  (`MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md:168-177`); the mechanical path does not enforce it. Prose is
  not a control.
- **Gap 1** — disclosure sufficient (both seats agree); technically real but no ordinary ceremony path
  grants it authority.
- **Gap 3** — disclosure sufficient; raising rather than returning a named code is fail-loud and is
  interface ergonomics, not an authority bypass.

## Fix classes (nothing folded yet — the frozen-layer item gates the rest)

1. `I02_STATE_BINDING` / canonical-world projection completeness — **OWNER (frozen artifact)**.
2. `TRUST_ROOT_KEY_IDENTITY` — identity over the decoded key, not any text envelope; carrier refusal on
   `public_key_pem` mirroring `strict_signature_carrier_ok`; adopt the bridge's raw-SPKI pattern
   (`src/crl/crl-authenticate.ts:15-18,109-120`, which SEAT1 found on our own shelf and this lane's
   shelf log had missed). New witness must be built independently of `public_key_identity`.
3. `PRODUCTION_SIGNING_KEY_FIXTURE_ISOLATION` — Q9 gap 2, before the ceremony.
4. ETW classes, pending D4: stream-completion / thread-identity join / SDK-ABI verification.
5. `PIN_MANIFEST_FRESHNESS` — regenerate at the accepted commit + a bundle arm that reconciles the
   manifest against current bytes, so staleness is loud without a clean-room run.
6. `CITATION_ACCURACY` — the CWE-1291 mitigation phase is Implementation, not Architecture-and-Design,
   wrong in three places including my own packet. Leaf, codex-CLI gate.

Items 1–4 each change an invariant consumer, an admission semantic, or the consumer's fault posture, so
the packet's own §13 re-review trigger fires: this comes back to council on the new bytes.

## Owner escalation (one row, category E — clashes with a standing owner ruling)

**The frozen r13.2 layer contains a defect.** The design of record says the canonical experiment world
binds each obligation's subject and owner role; the frozen code binds neither, and the experiment's own
reducer can legally change owner role. Closing it means editing a frozen, 3/3-CONFIRMED artifact —
either the projection or the matrix prose. That is a values/scope call about what the freeze protects,
and it is above the driver. **What it blocks:** nothing today (no experiment has run); it blocks any
claim that I02 binds the state the DoR says it binds, and it should be settled before the instrument
produces a result anyone cites. **Driver recommendation:** add the two fields to the projection rather
than weaken the matrix — the matrix is the scientific contract and the code is the thing that drifted
from it, and the change is additive with a red witness that mutates `owner_role` via a legal
`delegate_obligation`.
