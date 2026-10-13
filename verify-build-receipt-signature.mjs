// BUILD-side Ed25519 receipt verifier — STRICT signature carrier.
//
// Identical closed request/response contract to the FROZEN
// `verify-r13-receipt-signature.mjs` ({"items":[{payload_b64, public_key_pem,
// signature_b64}]} -> {"ok":true,"valid":[bool]}), which is committed at/under the
// r13.2 base and is NOT edited by this lane. This sibling adds the one thing the r1
// council found missing (codex F6, MBCX01-BUILD-R1-SIGNATURE-CARRIER):
//
//   Node's `Buffer.from(value, "base64")` ignores whitespace and also accepts the
//   base64url alphabet, so MANY carrier strings decode to ONE 64-byte signature.
//   That does not forge authority, but it gives a receipt more than one accepted
//   byte string — i.e. no single identity for dedup, replay bookkeeping or audit.
//
// Here the carrier must be canonical base64 BEFORE any cryptographic verification:
// standard alphabet only, length a multiple of 4, at most two '=' at the end, and the
// decoded bytes must re-encode to the exact same string. A non-canonical carrier is a
// refusal (`valid:false`), never a quiet acceptance.

import { createPublicKey, verify } from "node:crypto";

const STRICT_BASE64 = /^[A-Za-z0-9+/]+={0,2}$/;

function strictDecode(value, expectedBytes) {
  if (typeof value !== "string" || !STRICT_BASE64.test(value) || value.length % 4 !== 0) {
    return null;
  }
  const decoded = Buffer.from(value, "base64");
  if (decoded.toString("base64") !== value) return null;
  if (expectedBytes !== null && decoded.length !== expectedBytes) return null;
  return decoded;
}

let request;
try {
  request = JSON.parse(await new Promise((resolve, reject) => {
    let input = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", chunk => { input += chunk; });
    process.stdin.on("end", () => resolve(input));
    process.stdin.on("error", reject);
  }));
  if (Object.keys(request).join(",") !== "items" || !Array.isArray(request.items)) {
    throw new Error("closed verifier request schema");
  }
  const valid = request.items.map(item => {
    if (Object.keys(item).sort().join(",") !==
        "payload_b64,public_key_pem,signature_b64") {
      throw new Error("closed verifier item schema");
    }
    const payload = strictDecode(item.payload_b64, null);
    const signature = strictDecode(item.signature_b64, 64);
    if (payload === null || signature === null) return false;
    return verify(null, payload, createPublicKey(item.public_key_pem), signature);
  });
  process.stdout.write(JSON.stringify({
    ok: true,
    valid,
  }));
} catch (error) {
  process.stdout.write(JSON.stringify({ ok: false, error: String(error) }));
  process.exitCode = 1;
}
