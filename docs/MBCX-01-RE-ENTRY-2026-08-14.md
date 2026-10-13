# MBCX-01 — RE-ENTRY, session close 2026-08-14

For a session that arrives cold. Read this, then `MBCX-01-OPEN-ISSUES.json` (13 issues, that file IS
the tracker — ⛔ there is no git remote and no GitHub issue list). Byte-check anything you act on.

## Where the lane is, in one paragraph

The r13.2 EXPERIMENT DESIGN is frozen and 3/3 CONFIRMED — do not reopen it. The production BUILD is
implemented: BUILD A (state authority), BUILD B (measurement authority + evidence producer), the
trust-anchor layer, and — as of today — the ETW consumer that BUILD B always needed and never had.
Suites 114/114 BUILD + 145/145 frozen, `verify-build-bundle.py` exit 0 across all seven sections
(ledger 44 invariants / 114 witnesses, two-way total), and the clean-room reconstruction
`verify-build-pinned.ps1 -Commit 3527f510c1a91f789d1aa691331c09f2423beb0c -ManifestBlob
23009028b4eb32322064be4d92f81e48f604e1ae` prints `PINNED RECONSTRUCTION COMPLETE`. Readiness is
`BUILD_IMPLEMENTED_PRODUCTION_AUTHORITY_NOT_ACTIVATED`, which is correct: no ceremony has happened,
no production root exists, and nothing scientific has run. **Zero spend to date. Zero provider calls.
Zero frozen r13.2 files modified across every commit in this lane.**

## ⛔ READ THIS BEFORE YOU WRITE A COUNCIL PACKET — the lane's most expensive lesson

**This design of record has NO threat model.** Verify it yourself: run the one-line check recorded in
§"The byte that settles it" of `MBCX-01-BUILD-ADVERSARY-PREMISE-CORRECTION-2026-08-14.md`. It greps
the three governing design documents for the whole threat-model vocabulary and returns **ZERO hits**.
(The literal word list lives in that archive file, not here — re-listing it on a surface every fresh
session is forced to read is exactly what ends a reader at cold start. Method: Gravity memory
`fable-neutral-framing`.)

The seventeen invariants are a **scientific-validity** device. Every witness in the matrix's
falsification column is *the experiment fooling itself* — a non-member candidate rehashed, a scorer
that self-authors PASS, a fixture flag flipped so test data counts as real. There is no API, no
production runtime and no external submitter; every caller is the harness and its own tests, so an
in-process actor **is the box owner**, which the T2 ceiling puts out of model — we are
tamper-EVIDENT, not tamper-proof.

The r1 BUILD packet's threat-declaration field named an untrusted API caller (quoted here as a
citation, not as framing). r2 and r3 **inherited that line unchecked**.
It cost three council rounds, nine seat-verdicts, and a "wiring freeze" mechanism built against a
phantom — which was then reverted. The owner caught it, not the loop. `packet:check` was GREEN every
time and correctly so: its own header says it checks *"PRESENCE + SHAPE, never TRUTH."*
**Full record: `MBCX-01-BUILD-ADVERSARY-PREMISE-CORRECTION-2026-08-14.md`.**

⇒ The next packet asks whether **the instrument can produce a false scientific result** — falsify the
I01–I17 validity invariants and the new ETW surface. ⛔ Do not re-declare an outside-caller threat
class, and ⛔ **do not copy r1/r2/r3 as a template** — all three carry a CLOSED-ROUND banner saying so.
**Write the packet in the neutral CS register** (method: Gravity memory `fable-neutral-framing`; tool
`<vault>`, dry-run first). Keep exact only the packet field names
`packet:check` enforces — widening those is owner-ruled register row 65, not a driver call.

## What today changed (36 commits since the r13.2 council base, `git log --oneline 91329b2..HEAD`)

1. **Trust-bootstrap fold** — production admission now requires an operator-configured root the
   signer cannot edit (design row **I14**, whose own falsification-oriented witness is *"packet builder
   self-signs/injects its root"*). Council-confirmed across r2/r3 by three independent fresh-key
   untrusted caller universes, all refused.
2. **Fixture isolation** — fixture material cannot create an experiment-eligible score or physical
   pass (rows **I13/I16**, §3 authority modes).
3. **Freeze revert** — the phantom-driven machinery deleted. It could only ever FALSE-fire (plain-int
   depth counter, `threading` never imported). Differential witness banked: the trustboot probe is
   byte-identical before/after; only the six gadget lines changed. **Accepted residual, stated not
   hidden:** in-process code can leave the process re-wired — it buys NO admission (every door still
   refuses against the context it snapshotted at entry), and that actor is the box owner.
4. **Fixture-key fold** — a committed fixture KEY cannot become a production root whatever the flag
   says, on both the in-code and OS-config paths. Derived, not hardcoded: zero literal key material
   in source. Prior art MITRE CWE-1291.
5. **⭐ The ETW consumer** — the instrument's missing half, and building it **exposed three latent
   defects in the already-delivered collector**, none visible to any review round: the capability
   record could not carry both the evidence shape and the platform facts (a real run would have
   signed instruction counts beside `etw_pmc_source_available=False`); `configure()` raised a
   `KeyError`; and **the CSwitch attachment blob was ALL ZEROES**, so the counter would have attached
   to `GUID_NULL` and no PMC data would ever have arrived. Post-fix it decodes to
   `3d6fa8d1-fe05-11d0-9dda-00c04fd7ba7c` / Type 36.

## Do this next, in this order

1. **The elevated smoke run** — `MBCX01-SMOKE-RUN-OUTSTANDING`. Owner action; the driver's shell is
   not elevated. Authorization is written and banked at
   `<vault>` (marker line present; binary
   `cmd.exe /c exit 0`, cell (0,0,0), evidence to `<vault>`). **The
   pass criterion is an honest RED at admission** — a green admission would be a defect. It is the
   only thing that can settle seven unverified platform facts, chief among them
   `EVENT_HEADER_EXT_TYPE_PMC_COUNTERS = 0x0008`, which Microsoft names but never numbers.
2. **Council + codex-CLI on current bytes** — `MBCX01-REVIEW-GATES-OWED-ON-CURRENT-BYTES`. Fresh
   seats minted inside the project, **model set at mint and read back before message one**, read-probe
   first. ⚠ The ChatGPT seat's connector fails `Unknown tool` on every call — likely a stale manifest
   after the #858 bare-name rename (`ba80125f`); refreshing it is an owner action, logged in
   `Dogfood.md`.
3. **The remote decision** — `MBCX01-NO-GIT-REMOTE`. ~35 commits on one disk with no off-box copy,
   and the bot gate is unreachable until this is answered. Driver recommends a new private repo.

## Traps a fresh session will otherwise walk into

- ⚠ **`git archive` is NOT byte-identical in this clone** (`core.autocrlf=true` rewrites to CRLF).
  For pre-fix reconstruction use
  `git -c core.autocrlf=false -c core.eol=lf checkout-index -a -f --prefix=<tmp>/` and byte-verify
  against `git cat-file blob`. Two workers hit this.
- ⚠ **`MBCX-01-BUILD-FIXTUREISO-GREEN-WITNESS-RUN-2026-08-14.txt` is STALE** — its P2 block still
  shows `*_REWIRED_DURING_VERIFICATION`, deleted by the freeze revert. Compare against current bytes,
  not that bank.
- ⚠ **`MBCX-01-BUILD-COMPLETION-HANDOFF.md` predates the last five commits** and describes the build
  as it was before fixture isolation, the freeze revert, the fixture-key fold and the ETW consumer.
- ⚠ **Regenerate the pin manifest after ANY content commit** (`generate-build-pin-manifest.ps1
  -Commit <sha>`), or `verify-build-pinned.ps1` will not authenticate the tree.
- ⚠ **The smoke driver embeds no key material by design.** The operator must supply
  `--fixture-signing-key-pem`; the committed fixture measurement key lives only in
  `test_mbcx01_build_measurement.SIMULATED_PRIVATE_KEY_PEM` and a driver must not import a test module.
- ⛔ Never run the experiment, provider calls, the 456 route trials, the 100-cell grid, the physical
  collector, or the custody ceremony without a NEW explicit owner authorization. The route freeze is
  additionally gated on the startup-credits decision.

## Claim ceiling — what a green suite here does and does not mean

The BUILD's verification half is exercised and clean-room reproducible. The MEASUREMENT half has
**never executed a single instruction**. A green suite means the logic is right *if the platform
behaves as documented*; it does not mean the consumer works. Six constants are flagged in-source as
unverified, and the Kernel-Process provider identity has **no Microsoft page at all** — the same flag
class as `ProcessTelemetryIdInformation = 64`. Every one of them faults loudly rather than degrading
to a number, which is the property that makes the smoke run safe to trust.
