# MBCX-01 presentation council VALIDITY r1 — SEAT 1 (claude.ai, <account> · Max, model read back "Opus 5.5 Extra") VERDICT, banked 2026-09-26

Conversation `<id>` (<council-browser-port>, minted in the Moonwalker project). Banked by CDP innerHTML dump of the last long response (`cdp-dump-turn.mjs` + `cdp-expr-last-long-response-claude.js`, 30122 B, sha384 `59561e34ebdb2e7e8a275b57b68ccc55d53a76e4c8c4733fd158d059b7cb4febd28f49b43c6ee1dcbcdefa5080157a74`) converted with `pandoc -f html -t gfm-raw_html --wrap=none`; this file's body = that conversion, 18312 B, sha384 `cf44d6dfe600527b9bca6b5d3466ac51b920670e1abdd053db620421814d5693234ea70c4150c55938cbc5ab8ca95fe1`. The first lines are the seat's tool-chip chrome ("Setting up a read-only git task …"); the verdict begins at the GO-WITH-FIXES line. Packet `review-packets/MBCX01-PRESENTATION-VALIDITY-r1-council-packet-2026-09-26.md @ a9f623b`; pins A `19c16b3`, B `292f315`. claude.ai renders no anchors, so the SWEEP LOG's links carry inline data-URI icons from the page; adjudicated as the seat's own SEARCHED labels.

---

Setting up a read-only git task using a scratch directory.

Setting up a read-only git task using a scratch directory.

Reading the packet at its pin first.

Used Moonwalker, read 3 pages, and 13 more steps



Used Moonwalker, read 3 pages, and 13 more steps

GO-WITH-FIXES(record-fidelity folds: prose, captions, data-record sources; no mechanism) · EXECUTED

Artifact A is mostly faithful. The runs, ledger, codex counts, seat tables, figures, HTML and the 47 banked files all reproduced under execution. Four statements are false against the pinned bytes and must fold before the branch is pushed: A-1 to A-4. Artifact B preserves every fact.

**Track check.** VALIDITY holds and there is no real door. The HTML is pandoc output with the five SVGs embedded as base64 `<img>` data URIs, and it has 0 `<script>` tags. Every string that reaches a figure is driver-authored JSON.

### Deciding findings (fold before push)

**A-1 · EXECUTED · a fourth post-freeze amendment is missing.** The write-up says frozen files changed "in exactly four commits… No other commit touched a frozen file" (write-up:62) and "only through the declared amendments described below" (write-up:56). Both are false.

- `MBCX-01-R13-PIN-MANIFEST.json` names 34 subjects with governing commit `d97d654`.
- `git log d97d654..19c16b3 -- <34 subjects>` returns five commits. The fifth is `07b11b1` (2026-08-16), whose message reads "AMENDMENT (owner-ratified…) … frozen doc blobs changed BY OWNER RULING".
- It changes three subjects: `EXPERIMENT-DESIGN-r9.md:39-40,54`, `R13-CLOSURE-ARCHITECTURE.md:54,67,71` and `R13-PHYSICAL-HARNESS-REQUIREMENTS.md:82-83`.
- Its substance:
  - it excludes target-reopen episodes from the scientific population and defers them to MBCX-02;
  - it hands motif content semantics to the build cohort design;
  - it replaces the Merkle-style root with a flat list digest;
  - it supersedes the authority order's concrete artifacts.
- The driver derived the count from the `mbcx01_r13_*` and `test_mbcx01_r13_*` globs only. So README:22 (scoped to those globs) and the fig 3 frozen-suite annotation hold as scoped. The write-up does not.
- "The method" therefore describes the population without its one ratified narrowing. See the sweep: the change-disclosure conventions require a dated list of amendments (SEARCHED).
- Fix class: sentence fold at :56 and :62, a dated amendment list, a population note in "The method", and a doc-amendment row in `frozen_series`.

**A-2 · EXECUTED · a stale tracker is presented as today.** "Where it stands today" and fig 4 read the tracker as 26 September state.

- The tracker's own header says `generated_at 2026-08-15`, `source_head 5269375`. Its last commit is `41cb3a9` on 2026-08-15.
- Everything after that is missing from it:
  - all nine codex fold commits (08-15 20:09 to 08-16 19:08);
  - build rounds r6 to r8 and both cohort arcs;
  - `07b11b1`, which "closes \#4" (tracker row R5-COHORT-ROOT-UNRECORDED, still listed open) and "#27".
- Commit messages show board issues \#17 to \#23 beyond the tracker's \#1 to \#16.
- Its REVIEW-GATES-OWED row says the codex CLI was "never run on this lane", while the write-up reports nine codex rounds.
- "15 open" is the 15 August count.
- Fix class: date-scope the section and the fig 4 title to the tracker's own date. Refreshing the tracker is out of scope here.

**A-3 · EXECUTED · the "two gate the first real run" count is under-counted.** This checks write-up:83, fig 4, and make_figures.py:348 and :383-386 (hard-coded) against the tracker's own fields.

- Six open rows are `load_bearing: true`.
- R5-SMOKE-FIXTURE-CONTAINMENT-UNEXECUTED has status "open_verify_before_the_smoke_run", so it also sits before the smoke run.
- Two rows are neither "leaf gaps, doc fixes" nor "residuals":
  - REVIEW-GATES-OWED-ON-CURRENT-BYTES is a review gate that is still owed;
  - EXACTNESS-SUITE-RUNNER-UNBUILT says "no runner exists", and the physical stage needs it.
- The tracker's phrase is "first real *smoke* run". The write-up's "first real run" reads as the paid run.
- Fix class: use the tracker's phrase, count from its fields, and name the exactness runner.

**A-4 · EXECUTED · the data-record provenance sentence is false.** Write-up:115 says "Each block in it names the file and line…", and the record's own `provenance` string makes the same claim. Parsed at the pin:

- 4 of 8 blocks carry no source at all: `today`, `rounds`, `ledger_final` and `pins`. The `rounds` block holds 28 rows, which is every fig 2 cell and bar.
- `codex_cli_gate`, `suite` and `issues` name files but no lines.
- Only `prereg` and `premise_correction` name lines.
- The packet's claim 1 and §6(d) ("the line range the data record names") rest on lines that do not exist.
- Fix class: add a file:line per round row and per block, or scope the sentence.

### Further findings (BUILD-MATERIAL)

**A-5 · EXECUTED · two premise-correction citations point at the wrong files.**

- "Named there, with its four call sites" (:66) is wrong. The correction file names neither `AuthorityWiringDuringVerification` nor any call site: a grep for `four|site|AuthorityWiring` finds only :64 "the r2 wiring-freeze rider". Both the name and "all four call sites" are in revert `fd26275`'s message.
- The record cites `RE-ENTRY-2026-08-14.md:37-38` for 3 rounds, 8 verdicts and 1 capability report. Line 37 says "nine seat-verdicts".
- The 8+1 split is right per the build r3 synthesis seat table: seat 2 was a capability failure. The number is right and the cite is wrong.

**A-6 · READ-ONLY · fidelity to design r9 (byte comparison at the pin).**

- \(a\) :22 says the design states "in so many words" that more calls are "not an escape". Design r9:75 says "not an *automatic* escape". The limiting word is dropped under a verbatim claim.
- \(b\) :20 "act as well as an agent handed the ideal slice" asserts equivalence. The design tests "without materially underperforming", with a −0.10 margin.
- \(c\) :30 drops "descriptions" and "neutral" from the shared list in r9:54, then says the conditions "differ in one thing".
- \(d\) :40 reduces step three to "runs the physical gates". Design r9:70 lists exactness, complete accounting, boundedness and affordability; fig 1 carries all four.
- \(e\) :50 gives the power figures without the design's own non-claims: r9:58 makes no 90% promise in the transition region, and council packet r9:91 guarantees no decision at −0.10 or 0.80.

**A-7 · READ-ONLY · the fixture-key totality claim is wrong.**

- Write-up:128 says "every production door refuses them by construction, which the suite proves". README:49 says the same.
- `mbcx01_build_trust_anchor.py:731-739` at the pin scopes its own guard: the committed `FIXTURE_NON_ANCHOR_PRIVATE_KEY_PEM` (ceremony_fixture.py:58) "is not in this set… a NAMED, ACCEPTED gap".
- The tracker's FIXTUREKEY-NAMED-GAPS row is still open.

**A-8 · EXECUTED · the "every verdict" absolute is wrong.**

- README:26 says "every packet, every verdict, every gate log".
- `ls-files` at the pin has no design SEAT2 r1 verdict and no SEAT1 or SEAT2 r8 verdict. Write-up:46 says so itself.

**A-9 · EXECUTED · fig 3 labels overstate the data.**

- The axis says "tests passing at that commit". The values are witness-name counts parsed from each commit's ledger. I reproduced all 24 from names alone, and nothing was run at those commits.
- The subtitle says "every red-first witness", but the count includes pins: build r8 synthesis:71-73 says bw93 is "labelled a PIN and not a red". The codex r3 "red first" fold reached the prose but not this figure.
- The title "while the frozen core held" sits beside A-1.

**A-10 · READ-ONLY (scan EXECUTED) · register and labels.**

- Honesty narration: :46 "and the record says so", :83 "recorded so that no one claims them closed", fig 4 "Nothing here is hidden", README:27 "none hidden".
- Self-commentary: :50 "in ways that matter", :66 "cost more than it should have".
- ":10 designed in the open": the repository is private, and the seat files were never on the remote until `5630b6a`.
- Two claims in one sentence: :36, the second sentence of :46, and :48.
- Undefined acronyms: API, CPU, I/O, SQL, SHA-384, and MBCX-01 itself.
- Tense: :32 says retries "are capped" and :36 says "under the frozen endpoint", while :89 says no ceiling, endpoint or snapshot has been frozen.
- "Two void": one of the two is status "superseded_by_r13.2_confirmed". The fig 4 legend says "void or superseded", but the title and prose say void.
- "248 seconds" varies by box and by load; my run on the same host took 238.8 s.
- Mechanical scan over all three documents: em dash 0, en dash 0, contrast tails 0. The write-up uses "first" nine times, all ordinal.

**A-11 · READ-ONLY · the seal label omits the longitudinal-seat ruling.** From r7 on, seats were longitudinal by owner ruling; the R7 to R10 dispatch receipts say "Retained own-lane context is intentional". So "sealed" at :46 and in the fig 2 subtitle means the lateral seal only, and one clause fixes it.

**B-1 · EXECUTED · artifact B preserves every fact.**

- Code blocks are byte-identical (20 lines).
- The link-target set is identical; one added `[DOR]` link points to an existing target.
- All 12 identifiers are present. No number was lost; "8" was added from expanding "8B".
- The old second "lacks" list (old:128-132) is merged into the status list in full.
- 49 of 49 tests pass, with 0 dashes and 0 contrast tails. No fourth fact change.

**B-2 · READ-ONLY · the three DOR disagreements are confirmed, and leaving them is right for a register recut.**

- They sit at DOR:13 and :558 (gate 10a), :200 (§7.6) and :231 (§9). They belong on PR \#1.
- The recut made \#3 more legible: README:21-23 now reads as an explicit pick-then-test sequence.
- README contradicts itself on \#1: :120-121 says proposals stay empty "until an authenticated intake…", while :238-239 says v0.1 "will emit no action proposals".
- Fix all three before this README becomes the public face.

**B-3 · READ-ONLY · three nuance shifts, low severity.**

- The :220 gloss "files the bootstrap trusts" reverses who does the trusting.
- :60 drops "one… one" before the input and output contracts.
- :155 moves "air-gap-first" from "target architecture" to "v0.1 build", while DOR:6 says "air-gap-capable".

### Held under execution

- **Claim 3:**
  - 601 tests OK, bundle exit 0, frozen 156, build 289, ledger 118/289 two-way, readiness word identical.
  - I also ran the pinned clean-room launcher at governing commit `d347553` with manifest blob `7a8abc1`. It ended "PINNED RECONSTRUCTION COMPLETE" in mode BYTE_RECONCILED, with the same totals.
  - That backs README:5 and fig 1 step 1 on current bytes. The driver did not run it, so the record should name this run.
- **Claim 1:**
  - Ledger 24 of 24 match, with 88 positive and 201 adversarial witnesses.
  - Codex r3 is \[10,4,6\] and r7 is \[4,2,2\]. The r7 log also carries a verbatim copy of r6's block at 5566-5602, so a whole-file grep returns 18 lines. That is one reason A-4 needs line ranges.
  - Binomial bounds reproduced exactly, and the outward rounding is correct.
  - Power figures match packet r9:86-91, physical limits match closure:93-98, and pin counts match.
- **Claim 2:**
  - Design r2 and r10, and build r3 and r8, seat tables match fig 2.
  - The three seal breaches are confirmed, and a grep across 47 synthesis and packet files finds no others.
- **Claim 8:**
  - 47 of 47 SHA-256 match the vault, including the two largest.
  - Every vault file outside .git and **pycache** is tracked.
- **Figures and HTML:**
  - The figures regenerate with identical text nodes.
  - The HTML carries every markdown sentence and embeds the committed SVG bytes exactly.

### Evidence read (at 19c16b3 / 292f315)

The write-up (all 140 lines), README, LICENSE, the data record, make_figures.py (all 450 lines), the SVGs and HTML. Also: design r9:1-76, closure:88-100, R10 spec:55-61, packet r9:62-92, completion handoff:1-8 and :62-65, the r8 synthesis:1-90, the r3 synthesis:1-16, the round-2 and R10 syntheses, the premise correction, re-entry-08-14:35-40, the codex r3, r6 and r7 logs, the tracker, trust_anchor.py:723-745, Heph README (old and new) and DOR (targeted lines), and house source:360-446.

### SWEEP LOG

- **Queries:**
  - "COS preregistration transparent changes report deviations"
  - "SPIRIT 2025 statement protocol items checklist amendments"
- **Opened:**
  - **cos.io/initiatives/prereg, Resources and FAQ:** COS says that when you write up preregistered research you should openly disclose every change from the plan, and it offers a Transparent Changes template for this. This confirmed the convention the driver adopted. [cos![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgZmlsbD0iY3VycmVudENvbG9yIiB2aWV3Ym94PSIwIDAgMjU2IDI1NiIgY2xhc3M9InRyYW5zaXRpb24tW29wYWNpdHksc2NhbGUsdHJhbnNmb3JtXSBncm91cC1ob3Zlci90YWc6ZWFzZS1vdXQgZHVyYXRpb24tWzUwMG1zXSBlYXNlLWluIHRleHQtYWNjZW50LTEwMCBncm91cC1ob3Zlci90YWc6c2NhbGUtWzEwMCVdIHNjYWxlLVs4MCVdIGdyb3VwLWhvdmVyL3RhZzpvcGFjaXR5LVsxMDAlXSBvcGFjaXR5LVswJV0gLW1yLVsycHhdIj48cGF0aCBkPSJNMjAwLDY0VjE2OGE4LDgsMCwwLDEtMTYsMFY4My4zMUw2OS42NiwxOTcuNjZhOCw4LDAsMCwxLTExLjMyLTExLjMyTDE3Mi42OSw3Mkg4OGE4LDgsMCwwLDEsMC0xNkgxOTJBOCw4LDAsMCwxLDIwMCw2NFoiIC8+PC9zdmc+)](https://www.cos.io/initiatives/prereg)
  - **equator-network.org CONSORT 2025 entry:** its stated scope is reporting of randomised trials, and it points to SPIRIT for protocols. This changed my reading: CONSORT is the wrong member of the pair for a pre-result report. [equator-network![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgZmlsbD0iY3VycmVudENvbG9yIiB2aWV3Ym94PSIwIDAgMjU2IDI1NiIgY2xhc3M9InRyYW5zaXRpb24tW29wYWNpdHksc2NhbGUsdHJhbnNmb3JtXSBncm91cC1ob3Zlci90YWc6ZWFzZS1vdXQgZHVyYXRpb24tWzUwMG1zXSBlYXNlLWluIHRleHQtYWNjZW50LTEwMCBncm91cC1ob3Zlci90YWc6c2NhbGUtWzEwMCVdIHNjYWxlLVs4MCVdIGdyb3VwLWhvdmVyL3RhZzpvcGFjaXR5LVsxMDAlXSBvcGFjaXR5LVswJV0gLW1yLVsycHhdIj48cGF0aCBkPSJNMjAwLDY0VjE2OGE4LDgsMCwwLDEtMTYsMFY4My4zMUw2OS42NiwxOTcuNjZhOCw4LDAsMCwxLTExLjMyLTExLjMyTDE3Mi42OSw3Mkg4OGE4LDgsMCwwLDEsMC0xNkgxOTJBOCw4LDAsMCwxLDIwMCw2NFoiIC8+PC9zdmc+)](https://www.equator-network.org/reporting-guidelines/consort/)
  - **PLOS Med SPIRIT 2025, "Definition of a randomised trial protocol":** every protocol version should keep an audit trail of dated change descriptions, and important amendments should later be described in reports. This confirmed the dated-amendments requirement. [plos![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgZmlsbD0iY3VycmVudENvbG9yIiB2aWV3Ym94PSIwIDAgMjU2IDI1NiIgY2xhc3M9InRyYW5zaXRpb24tW29wYWNpdHksc2NhbGUsdHJhbnNmb3JtXSBncm91cC1ob3Zlci90YWc6ZWFzZS1vdXQgZHVyYXRpb24tWzUwMG1zXSBlYXNlLWluIHRleHQtYWNjZW50LTEwMCBncm91cC1ob3Zlci90YWc6c2NhbGUtWzEwMCVdIHNjYWxlLVs4MCVdIGdyb3VwLWhvdmVyL3RhZzpvcGFjaXR5LVsxMDAlXSBvcGFjaXR5LVswJV0gLW1yLVsycHhdIj48cGF0aCBkPSJNMjAwLDY0VjE2OGE4LDgsMCwwLDEtMTYsMFY4My4zMUw2OS42NiwxOTcuNjZhOCw4LDAsMCwxLTExLjMyLTExLjMyTDE3Mi42OSw3Mkg4OGE4LDgsMCwwLDEsMC0xNkgxOTJBOCw4LDAsMCwxLDIwMCw2NFoiIC8+PC9zdmc+)](https://journals.plos.org/plosmedicine/article?id=10.1371%2Fjournal.pmed.1004589)
- **Why I stopped:** two primaries settle the one external question. Neither binds a non-clinical AI experiment, but both converge on dated amendment disclosure, which decides A-1.
- **Labels:** A-1's disclosure point is SEARCHED. My recollection of CONSORT 2010 item 3b is RECALLED and not load-bearing. All other findings are NOT-LOAD-BEARING, because they rest on pinned bytes.

### WHY THIS EXISTS

1.  **ALREADY-BUILT · EXECUTED:**
    - The packet's internal-shelf log is present.
    - I spot-ran q1 over `docs/` in the bridge @35d7d0d5, Photon @4ff2fbb and Gravity @010bda0: 0 files each, matching the driver.
    - A broader query hits only council logs and build records, and I checked those by name only.
    - No external convention fixes the package shape. The dated-amendment content is what should have been adopted.
2.  **PRODUCT-FIT:** In one sentence, the need is that an outside reader can check the experiment's state from files. That fits FAIL-LOUD and MIRROR-NOT-COP. A-2 and A-7 cut against it, because they show completeness the record itself disclaims.
3.  **BIGGER-THAN-THE-BUG:** No. `5630b6a` is records hygiene riding on a presentation branch, and that is why the packet's scope witness failed.
4.  **PRIMARY-CONSUMER:** The outside reader gets the hypothesis, method and state. Fig 4 hands that reader a 15 August snapshot as today. Fig 2's 28 cells carry no per-cell source, so the next driver cannot re-check a cell cheaply.

### Residual risks

- **Going public:** the banked logs carry 6,230 local user-path strings across 26 files and the committed Ed25519 test key in 4 files. That key is already in 19 files at `d002b41`. I found no real secret. This is the owner's call.
- **House rules:** §3 lines 16 and 17 (codenames and paths, measured counts) are broken by design. The packet's claim-6 subset omits them, so the owner needs to rule on them before outbound use.
- **Step two:** "passed" (:40) rests on the r13.2 bytes. Fig 1's scoping to r13.2 is the honest form.
- **Out of scope:** each build-suite run leaks three `mbcx01-build-pin-witness-*` temp dirs and raises two ResourceWarnings (test_mbcx01_build_integration.py:698 and :705).

### Packet-level notes

- **SCOPE witness:** the `git diff --stat … 'MBCX-01-*'` listed 44 files, not none. All are record additions.
- **Research-question line:** it is at design r9:9, not :10.
- **NOT RUN authority:** the handoff the packet cites for it is bannered as superseded, though its list is harmless.

### Hygiene

- The scratch clones are deleted, along with the six temp dirs my unittest and bundle runs created.
- Five pin-witness triples from 04:07 to 04:11 remain. One is from my pinned run, and the rest appeared after that run ended, from a concurrent process. I could not tell them apart, so I left all of them.
- `git status` on the two working clones may have refreshed their index stat cache. HEADs and tracked trees are verified unchanged.
