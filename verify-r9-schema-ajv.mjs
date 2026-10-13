import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const expectedVersion = "8.20.0";
const expectedPackageHash = "0AF330905106D4E03139621669897AF6C79D138E739FFB3519C98215672F3C922104E1376BD26985EBD921D0209DD66D";
const roots = [
  process.env.MBCX_AJV_ROOT,
  "<home>/source/agentvault-mcp-bridge/node_modules/ajv",
].filter(Boolean);
const ajvRoot = roots.find((candidate) => fs.existsSync(path.join(candidate, "package.json")));
if (!ajvRoot) {
  process.stderr.write("Pinned Ajv 8.20.0 runtime not found\n");
  process.exit(2);
}
const packageBytes = fs.readFileSync(path.join(ajvRoot, "package.json"));
const packageHash = crypto.createHash("sha384").update(packageBytes).digest("hex").toUpperCase();
const packageJson = JSON.parse(packageBytes.toString("utf8"));
if (packageJson.version !== expectedVersion || packageHash !== expectedPackageHash) {
  process.stderr.write(`Ajv pin mismatch: ${packageJson.version} ${packageHash}\n`);
  process.exit(2);
}
const contract = JSON.parse(fs.readFileSync("MBCX-01-PACKET-SCHEMAS-v3.json", "utf8"));
const nodeModulesRoot = path.dirname(ajvRoot);
function regularFiles(directory, root = directory, output = []) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const absolute = path.join(directory, entry.name);
    if (entry.isDirectory()) regularFiles(absolute, root, output);
    else if (entry.isFile()) output.push(path.relative(root, absolute).split(path.sep).join("/"));
  }
  return output;
}
function uint64be(value) {
  const bytes = Buffer.alloc(8);
  bytes.writeBigUInt64BE(BigInt(value));
  return bytes;
}
for (const [name, pin] of Object.entries(contract.validator_runtime.runtime_closure)) {
  const packageRoot = path.join(nodeModulesRoot, name);
  if (!fs.existsSync(path.join(packageRoot, "package.json"))) {
    process.stderr.write(`Pinned validator dependency missing: ${name}\n`);
    process.exit(2);
  }
  const metadata = JSON.parse(fs.readFileSync(path.join(packageRoot, "package.json"), "utf8"));
  const files = regularFiles(packageRoot).sort((left, right) =>
    Buffer.compare(Buffer.from(left), Buffer.from(right)));
  const digest = crypto.createHash("sha384");
  for (const relative of files) {
    const relativeBytes = Buffer.from(relative);
    const content = fs.readFileSync(path.join(packageRoot, ...relative.split("/")));
    digest.update(uint64be(relativeBytes.length));
    digest.update(relativeBytes);
    digest.update(uint64be(content.length));
    digest.update(content);
  }
  const actualHash = digest.digest("hex").toUpperCase();
  if (metadata.version !== pin.version || files.length !== pin.files || actualHash !== pin.tree_sha384) {
    process.stderr.write(`Validator closure pin mismatch: ${name} ${metadata.version} ${files.length} ${actualHash}\n`);
    process.exit(2);
  }
}
const Ajv2020 = require(path.join(ajvRoot, "dist", "2020.js")).default;
const schemaName = process.argv[2];
const selected = contract.schemas[schemaName];
if (!selected) {
  process.stdout.write(JSON.stringify({ valid: false, errors: ["unknown schema_id"] }));
  process.exit(1);
}
const schema = { ...selected, $defs: contract.$defs };
const value = JSON.parse(fs.readFileSync(0, "utf8"));
const ajv = new Ajv2020({ allErrors: true, strict: true });
const validate = ajv.compile(schema);
const valid = validate(value);
const errors = valid ? [] : validate.errors.map((row) => `${row.instancePath} ${row.message}`);
process.stdout.write(JSON.stringify({ valid, errors }));
process.exit(valid ? 0 : 1);
