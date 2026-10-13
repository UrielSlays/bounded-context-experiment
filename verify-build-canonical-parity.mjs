// Canonicalization parity across the Python/Node boundary for the BUILD lane.
//
// `mbcx01_r13_common.canonical_json` is
//   json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True,
//              separators=(",", ":")).encode("utf-8")
// and `sha384` is the uppercase hex SHA-384 of those exact bytes. This script
// reproduces that byte-for-byte with `JSON.stringify` over recursively
// key-sorted objects, so a receipt hashed in Python and the same receipt hashed
// by a Node implementation of the same contract must agree on the digest.
//
// Scope stated honestly: the parity claim covers the value domain the BUILD
// receipts actually use — objects, arrays, strings, booleans, null and integers
// exactly representable in both runtimes. Non-integer numbers are NOT claimed
// (Python `repr` and JS number formatting are different specifications), and a
// document carrying one is refused rather than silently blessed.
//
// Usage: node verify-build-canonical-parity.mjs <documents.json>
//   input : {"documents": {"<name>": <value>, ...}}
//   output: {"ok": true, "digests": {"<name>": {"sha384": "...", "bytes": N}}}

import fs from "node:fs";
import crypto from "node:crypto";

function fail(message) {
  process.stderr.write(`${message}\n`);
  process.exit(1);
}

// Python sorts keys by code point; JS Array#sort compares UTF-16 code units.
// They differ only outside the BMP, so compare code points explicitly.
function byCodePoint(left, right) {
  const a = Array.from(left);
  const b = Array.from(right);
  const shared = Math.min(a.length, b.length);
  for (let index = 0; index < shared; index += 1) {
    const x = a[index].codePointAt(0);
    const y = b[index].codePointAt(0);
    if (x !== y) return x < y ? -1 : 1;
  }
  return a.length === b.length ? 0 : (a.length < b.length ? -1 : 1);
}

function canonicalize(value, path) {
  if (value === null || typeof value === "string" || typeof value === "boolean") {
    return value;
  }
  if (typeof value === "number") {
    if (!Number.isFinite(value)) fail(`non-finite number at ${path}`);
    if (!Number.isInteger(value)) fail(`non-integer number at ${path}`);
    if (!Number.isSafeInteger(value)) fail(`unsafe integer at ${path}`);
    return value;
  }
  if (Array.isArray(value)) {
    return value.map((item, index) => canonicalize(item, `${path}[${index}]`));
  }
  if (typeof value === "object") {
    const sorted = {};
    for (const key of Object.keys(value).sort(byCodePoint)) {
      sorted[key] = canonicalize(value[key], `${path}.${key}`);
    }
    return sorted;
  }
  return fail(`unsupported value at ${path}`);
}

if (process.argv.length !== 3) {
  fail("usage: node verify-build-canonical-parity.mjs <documents.json>");
}
const request = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
if (!request || typeof request !== "object" || typeof request.documents !== "object"
    || request.documents === null || Array.isArray(request.documents)) {
  fail("input must be {\"documents\": {name: value}}");
}

const digests = {};
for (const [name, value] of Object.entries(request.documents)) {
  const bytes = Buffer.from(JSON.stringify(canonicalize(value, name)), "utf8");
  digests[name] = {
    sha384: crypto.createHash("sha384").update(bytes).digest("hex").toUpperCase(),
    bytes: bytes.length,
  };
}
process.stdout.write(`${JSON.stringify({ ok: true, digests })}\n`);
