import { createPublicKey, verify } from "node:crypto";

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
    const payload = Buffer.from(item.payload_b64, "base64");
    const signature = Buffer.from(item.signature_b64, "base64");
    return signature.length === 64 && verify(
      null, payload, createPublicKey(item.public_key_pem), signature);
  });
  process.stdout.write(JSON.stringify({
    ok: true,
    valid,
  }));
} catch (error) {
  process.stdout.write(JSON.stringify({ ok: false, error: String(error) }));
  process.exitCode = 1;
}
