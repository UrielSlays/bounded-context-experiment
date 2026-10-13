import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const expectedVersion = "8.20.0";
const expectedPackageHash = "0AF330905106D4E03139621669897AF6C79D138E739FFB3519C98215672F3C922104E1376BD26985EBD921D0209DD66D";
const roots = [process.env.MBCX_AJV_ROOT,
  "C:/Users/Kingo/source/agentvault-mcp-bridge/node_modules/ajv"].filter(Boolean);
const ajvRoot = roots.find((candidate) => fs.existsSync(path.join(candidate, "package.json")));
if (!ajvRoot) {
  process.stderr.write("Pinned Ajv runtime not found\n");
  process.exit(2);
}
const packageBytes = fs.readFileSync(path.join(ajvRoot, "package.json"));
const packageJson = JSON.parse(packageBytes.toString("utf8"));
const packageHash = crypto.createHash("sha384").update(packageBytes).digest("hex").toUpperCase();
if (packageJson.version !== expectedVersion || packageHash !== expectedPackageHash) {
  process.stderr.write(`Ajv pin mismatch: ${packageJson.version} ${packageHash}\n`);
  process.exit(2);
}

const Ajv2020 = require(path.join(ajvRoot, "dist", "2020.js")).default;
const packetContract = JSON.parse(fs.readFileSync("MBCX-01-PACKET-SCHEMAS-v4.json", "utf8"));
const stateContract = JSON.parse(fs.readFileSync("MBCX-01-STATE-ACTION-CONTRACT-v5.json", "utf8"));

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
const nodeModulesRoot = path.dirname(ajvRoot);
for (const [name, pin] of Object.entries(packetContract.validator_runtime.runtime_closure)) {
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
    digest.update(uint64be(relativeBytes.length)); digest.update(relativeBytes);
    digest.update(uint64be(content.length)); digest.update(content);
  }
  const actualHash = digest.digest("hex").toUpperCase();
  if (metadata.version !== pin.version || files.length !== pin.files || actualHash !== pin.tree_sha384) {
    process.stderr.write(`Validator closure pin mismatch: ${name} ${metadata.version} ${files.length} ${actualHash}\n`);
    process.exit(2);
  }
}

function microsecondUtc(value) {
  const match = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.(\d{6})Z$/.exec(value);
  if (!match) return false;
  const [year, month, day, hour, minute, second] = match.slice(1, 7).map(Number);
  const date = new Date(Date.UTC(year, month - 1, day, hour, minute, second));
  return date.getUTCFullYear() === year && date.getUTCMonth() === month - 1 &&
    date.getUTCDate() === day && date.getUTCHours() === hour &&
    date.getUTCMinutes() === minute && date.getUTCSeconds() === second;
}

function createAjv() {
  const ajv = new Ajv2020({ allErrors: true, strict: true });
  ajv.addFormat("microsecond-utc", { type: "string", validate: microsecondUtc });
  return ajv;
}

function eventSchema(name) {
  const rule = stateContract.event_types[name];
  return {
    ...stateContract.event_envelope,
    properties: {
      ...stateContract.event_envelope.properties,
      event_type: { const: name },
      semantic_operation: { const: rule.semantic_operation },
      payload: rule.payload_schema,
    },
    $defs: stateContract.$defs,
  };
}

function selfTest() {
  const ajv = createAjv();
  const packetValidators = Object.fromEntries(Object.entries(packetContract.schemas).map(
    ([name, schema]) => [name, ajv.compile({ ...schema, $defs: packetContract.$defs })]));
  const eventValidators = Object.fromEntries(Object.keys(stateContract.event_types).map(
    (name) => [name, ajv.compile(eventSchema(name))]));
  if (Object.keys(packetValidators).length !== 6 || Object.keys(eventValidators).length !== 17) {
    throw new Error("schema-count invariant failed");
  }
  const worker = {
    schema_id: "WorkerHandoffV4", scenario_id: "SCENARIO.X", scope_id: "SCOPE.X",
    input_packet_hash: "A".repeat(96), manifest_hash: "B".repeat(96),
    request_hash: "C".repeat(96), response_hash: "D".repeat(96), status_code: "PROPOSE",
    proposed_action_ids: [], produced_at: "2026-08-12T00:00:00.000000Z",
  };
  if (packetValidators.WorkerHandoffV4(worker)) throw new Error("PROPOSE empty-array mutant survived");
  worker.proposed_action_ids = ["ACT." + "A".repeat(64)];
  worker.produced_at = "2026-02-30T00:00:00.000000Z";
  if (packetValidators.WorkerHandoffV4(worker)) throw new Error("impossible calendar date survived");
  worker.produced_at = "2026-08-12T00:00:00.000000Z";
  if (!packetValidators.WorkerHandoffV4(worker)) throw new Error("legal worker rejected");
  process.stdout.write(JSON.stringify({ valid: true, packetSchemas: 6, eventSchemas: 17 }));
}

if (process.argv[2] === "--self-test") {
  try { selfTest(); process.exit(0); }
  catch (error) { process.stderr.write(String(error.stack || error)); process.exit(1); }
}

const schemaName = process.argv[2];
const selected = packetContract.schemas[schemaName];
if (!selected) {
  process.stdout.write(JSON.stringify({ valid: false, errors: ["unknown schema_id"] }));
  process.exit(1);
}
const value = JSON.parse(fs.readFileSync(0, "utf8"));
const validate = createAjv().compile({ ...selected, $defs: packetContract.$defs });
const valid = validate(value);
const errors = valid ? [] : validate.errors.map((row) => `${row.instancePath} ${row.message}`);
process.stdout.write(JSON.stringify({ valid, errors }));
process.exit(valid ? 0 : 1);
