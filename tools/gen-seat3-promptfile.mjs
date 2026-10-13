#!/usr/bin/env node
/**
 * THE ONE seat-3 (codex-exec) promptfile generator -- card + pointer + verdict contract, nothing else.
 *
 *   node scripts/gen-seat3-promptfile.mjs --packet <review-packets/....md> --round <N> [--out <file>] [--artifact CODE|DESIGN]
 *
 * Owner ruling 2026-09-07: ONE generator, parameterized by round and packet; the card, the pointer and the
 * verdict contract ONLY; the per-round narratives and anchors are gone. (The repo carried 132 per-round
 * copies; the #167 slice 5b lineage had grown to 1,070 lines emitting 44k-char prompts the browser seats
 * never saw. The codex seat gets exactly what the browser seats get: the card, then the packet pointer.)
 *
 * What it does (CC-DEV-WORKFLOW-GUIDE step 3(a) + the packet-cutting discipline):
 *   1. EXTRACTS the role-prime card's fenced block VERBATIM from its canonical home and, per the card's own
 *      one-shot instruction, drops the bracketed header line and the final "Reply Council Mode ready" line.
 *      REFUSES to emit if any required lane is absent from the extracted block (never transcribed by hand).
 *   2. Appends the packet POINTER: the path and the commit that last touched it (derived from git in the
 *      repository this script runs in) -- WHAT to read, never WHICH tool. REFUSES if the packet is untracked,
 *      dirty, or does not declare `council round <N>` for the given round.
 *   3. Appends the VERDICT CONTRACT the guide enumerates for the codex seat (GO / GO-WITH-FIXES(class) /
 *      NO-GO; construct-the-bypass; omission attack; WHY-THIS-EXISTS all four; own web search; and, on a
 *      DESIGN artifact only, the PROPOSE lane + the ROUND CALL from round 3 on).
 */
import { readFileSync, writeFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { dirname, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const CARD = "<vault>";

const args = process.argv.slice(2);
const opt = (name, dflt) => { const i = args.indexOf(name); return i >= 0 && i + 1 < args.length ? args[i + 1] : dflt; };
const packetPath = opt("--packet");
const round = Number(opt("--round"));
const artifact = (opt("--artifact", "CODE") || "CODE").toUpperCase();
if (!packetPath || !Number.isInteger(round) || round < 1 || !["CODE", "DESIGN"].includes(artifact)) {
  console.error("usage: node scripts/gen-seat3-promptfile.mjs --packet <path> --round <N> [--out <file>] [--artifact CODE|DESIGN]");
  process.exit(2);
}
const refuse = (why) => { console.error("REFUSING TO EMIT -- " + why); process.exit(1); };

// -- the repository this script runs in ------------------------------------------------------------------
const here = dirname(fileURLToPath(import.meta.url));
let repo; try { repo = execFileSync("git", ["rev-parse", "--show-toplevel"], { cwd: here, encoding: "utf8" }).trim(); } catch { refuse("this script is not inside a git worktree, so no pin can be derived for the packet"); }
// every other git call runs from the REPO ROOT, so a repo-relative packet path resolves as written.
const git = (...a) => execFileSync("git", a, { cwd: repo, encoding: "utf8" }).trim();
const packetAbs = resolve(repo, packetPath);
// the packet path as WRITTEN may be a PowerShell spelling (`.\review-packets\...`) or ABSOLUTE; the pointer line and the
// default output name both use the REPO-RELATIVE form of the RESOLVED path (codex gate r1-3 on the #1089 lane: the
// un-normalized replace aimed at `council-logs/review-packets/`; gate r6-1: an absolute --packet kept its drive and wrote
// beneath `council-logs/C:/...`, and the as-written spelling reached the seat's pointer verbatim).
const packetRel = relative(repo, packetAbs).replace(/\\/g, "/");

// -- 1. the card, extracted, checked -------------------------------------------------------------------
const card = readFileSync(CARD, "utf8");
const fence = card.match(/```\r?\n([\s\S]*?)```/);
if (!fence) refuse("no fenced card block found in " + CARD);
let block = fence[1].replace(/\r\n/g, "\n");
const REQUIRED = [
  ["ROLE / seat framing", /ROLE:\s*You are an independent Moonwalker council reviewer/],
  ["read-only authority", /AUTHORITY:\s*read-only/],
  ["byte doctrine", /DOCTRINE\s*.{1,3}\s*trust nothing but the byte/],
  ["read-at-the-pin", /READ THE PINNED VERSION/],
  ["source-poisoning rule", /SOURCE-POISONING RULE/],
  ["WHY-THIS-EXISTS lane", /WHY THIS EXISTS\s*.{1,3}\s*challenge the BUILD DECISION/],
  ["ROUND CALL", /ROUND CALL \(DESIGN artifacts/],
  ["REVIEW TRACK", /REVIEW TRACK \(REQUIRED/],
  ["bypass-construction lane", /YOUR JOB \(bypass construction\)/],
  ["execute lane", /EXECUTE WHERE THE CLAIM IS EXECUTABLE/],
  ["SWEEP lane", /SWEEP THE WORLD, NOT ONLY THE BYTES/],
  ["verdict format", /VERDICT FORMAT:/],
  ["in-thread delivery", /DELIVER THE ENTIRE VERDICT IN-THREAD/],
  ["PROPOSE lane", /WHAT WOULD YOU BUILD\?/],
];
for (const [name, re] of REQUIRED) if (!re.test(block)) refuse(`the card block is missing its ${name} (${re})`);
// the one-shot form: no ack turn, so the bracketed header and the "Reply Council Mode ready" line go.
const lines = block.split("\n");
if (!/^\[COUNCIL MODE/.test(lines[0])) refuse("the card block does not open with the bracketed COUNCIL MODE header line");
const ackIdx = lines.findIndex((l) => /^Reply "Council Mode ready"/.test(l));
if (ackIdx < 0) refuse("the card block has no final 'Reply Council Mode ready' line to drop");
const oneShot = lines.slice(1, ackIdx).join("\n").replace(/^\n+/, "").replace(/\n+$/, "");

// -- 2. the pointer, derived -----------------------------------------------------------------------------
let tracked = ""; try { tracked = git("ls-files", "--error-unmatch", packetPath); } catch { refuse(`the packet ${packetPath} is not tracked by git in ${repo}`); }
if (git("status", "--porcelain", "--", packetPath) !== "") refuse(`the packet ${packetPath} has uncommitted changes; commit it first so the pointer names its bytes`);
const sha = git("log", "-1", "--format=%h", "--", packetPath);
if (!/^[0-9a-f]{7,}$/.test(sha)) refuse("could not derive the packet's commit");
const packet = readFileSync(packetAbs, "utf8");
if (!/^REVIEW TRACK: (FULL|VALIDITY)/.test(packet)) refuse("the packet's first line does not declare its REVIEW TRACK");
const ledger = packet.match(/ROUND LEDGER:\s*council round (\d+)/);
if (!ledger) refuse("the packet carries no ROUND LEDGER line");
if (Number(ledger[1]) !== round) refuse(`this run is for council round ${round}, but the packet's ROUND LEDGER declares council round ${ledger[1]}`);

const pointer = [
  `THE PACKET -- COUNCIL ${artifact} ROUND ${round}.`,
  `Read \`${packetRel}\` as committed at commit ${sha} in the repository at ${repo.replace(/\\/g, "/")}. Reach the bytes however you like; the pin is the requirement, not any one command. A working-tree read must say so and confirm it matches the commit.`,
].join("\n");

// -- 3. the verdict contract (CC-DEV step 3(a), enumerated so the seat cannot silently drop a lane) ----------
const contract = [
  "VERDICT CONTRACT (from the packet's section 0; enumerated here so nothing is dropped):",
  "  - Verdict: GO / GO-WITH-FIXES(<class>) / NO-GO. Label every finding and the verdict EXECUTED or READ-ONLY.",
  "  - Section 5, construct the bypass: for every safe/closed claim name the byte or scenario that makes it false, or the residual.",
  "  - Section 6, the omission attack: attack the UN-NAMED set -- what did the author not name, and why is that not the real one.",
  "  - Section 7, WHY THIS EXISTS -- all four, on the record: ALREADY-BUILT? PRODUCT-FIT? BIGGER-THAN-THE-BUG? PRIMARY-CONSUMER?",
  "  - Run your OWN online search; deliver a SWEEP LOG under a heading named SWEEP LOG with SEARCHED / RECALLED / UNSEARCHED+reason-token labels.",
  artifact === "DESIGN"
    ? "  - DESIGN artifact: after the verdict answer the PROPOSE lane (what would you build; would you do it differently, and why); from council round 3 on your verdict's FIRST LINE is GO-TO-CODE or CONTINUE-DESIGN: <one sentence>."
    : "  - CODE artifact: skip the ROUND CALL and the PROPOSE lane; name the CLASS of any fix, leaf edges belong to the codex gate.",
  "  - Deliver the ENTIRE verdict as your reply; end with a line beginning exactly \"FINAL VERDICT:\".",
].join("\n");

const out = opt("--out", `council-logs/${packetRel.replace(/^review-packets\//, "").replace(/-council-packet-/, "-SEAT3-promptfile-").replace(/\.md$/, ".txt")}`);
const text = [oneShot, "", pointer, "", contract, ""].join("\n");
writeFileSync(resolve(repo, out), text, "utf8");
console.log(`wrote ${out} (${text.length} chars): card block ${oneShot.length} chars with all ${REQUIRED.length} required lanes; packet ${packetRel} @ ${sha}; council ${artifact} round ${round}; repo ${repo}`);
