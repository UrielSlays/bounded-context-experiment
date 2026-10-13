import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const root = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const { createAjv } = require(path.join(root, "vendor", "ajv-r11.bundle.cjs"));

const readJson = (name) => JSON.parse(fs.readFileSync(path.join(root, name), "utf8"));
const ajv = createAjv();
const stateSchema = readJson("MBCX-01-STATE-ACTION-CONTRACT-v6.json").event_schema;
const packetSchema = readJson("MBCX-01-PACKET-SCHEMAS-v5.json").schema;
const measurementSchema = readJson("MBCX-01-MEASUREMENT-CONTRACT-v5.json").measurement_receipt_schema;
const validators = {
  event: ajv.compile(stateSchema),
  scorer_input: ajv.compile(packetSchema),
  measurement_receipt: ajv.compile(measurementSchema),
};

function fail(message, errors = []) {
  process.stderr.write(`${message}\n${JSON.stringify(errors, null, 2)}\n`);
  process.exit(1);
}

if (process.argv[2] === "--compile-only") {
  process.stdout.write("AJV_R11_STRICT_COMPILE_OK\n");
  process.exit(0);
}

if (process.argv.length !== 3) {
  fail("usage: node verify-r11-schema-ajv.mjs <fixture.json> | --compile-only");
}

const fixture = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
for (const [name, validate] of Object.entries(validators)) {
  if (!validate(fixture[name])) fail(`schema rejected valid ${name}`, validate.errors);
  const mutant = structuredClone(fixture[name]);
  mutant.__unexpected_r11_field = true;
  if (validate(mutant)) fail(`schema accepted extra-field ${name}`);
}

const nestedMutants = [
  ["event payload type", "event", (row) => { row.payload.due_at = 7; }],
  ["calendar-impossible UTC", "event", (row) => {
    row.observed_at = "2026-99-99T99:99:99.999999Z";
  }],
  ["worker extra field", "scorer_input", (row) => {
    row.worker_handoff.__unexpected_r11_field = true;
  }],
  ["job receipt extra field", "measurement_receipt", (row) => {
    row.job_receipt.__unexpected_r11_field = true;
  }],
];
for (const [label, schemaName, mutate] of nestedMutants) {
  const mutant = structuredClone(fixture[schemaName]);
  mutate(mutant);
  if (validators[schemaName](mutant)) fail(`schema accepted nested mutant: ${label}`);
}
process.stdout.write("AJV_R11_FIXTURE_AND_MUTANT_OK\n");
