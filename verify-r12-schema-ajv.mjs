import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const root = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const { createAjv } = require(path.join(root, "vendor", "ajv-r12.bundle.cjs"));

const readJson = (name) => JSON.parse(fs.readFileSync(path.join(root, name), "utf8"));
const ajv = createAjv();
const validators = {
  event: ajv.compile(readJson("MBCX-01-STATE-TRANSITION-CONTRACT-v7.json").event_schema),
  scorer_input: ajv.compile(readJson("MBCX-01-PACKET-SCHEMAS-v6.json").schema),
  signed_measurement_envelope: ajv.compile(
    readJson("MBCX-01-MEASUREMENT-CONTRACT-v6.json").signed_measurement_envelope_schema),
};

function fail(message, errors = []) {
  process.stderr.write(`${message}\n${JSON.stringify(errors, null, 2)}\n`);
  process.exit(1);
}

if (process.argv[2] === "--compile-only") {
  process.stdout.write("AJV_R12_STRICT_COMPILE_OK\n");
  process.exit(0);
}
if (process.argv.length !== 3) {
  fail("usage: node verify-r12-schema-ajv.mjs <fixture.json> | --compile-only");
}

const fixture = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
for (const [name, validate] of Object.entries(validators)) {
  if (!validate(fixture[name])) fail(`schema rejected valid ${name}`, validate.errors);
  const mutant = structuredClone(fixture[name]);
  mutant.__unexpected_r12_field = true;
  if (validate(mutant)) fail(`schema accepted extra-field ${name}`);
}

const nestedMutants = [
  ["event payload type", "event", (row) => { row.payload.due_at = 7; }],
  ["calendar-impossible UTC", "event", (row) => {
    row.observed_at = "2026-99-99T99:99:99.999999Z";
  }],
  ["transition authority extra field", "scorer_input", (row) => {
    row.transition_authority.__unexpected_r12_field = true;
  }],
  ["writer authority digest type", "scorer_input", (row) => {
    row.writer_receipt.postcommit_state_hash = 7;
  }],
  ["signed envelope extra field", "signed_measurement_envelope", (row) => {
    row.receipt.job_receipt.__unexpected_r12_field = true;
  }],
  ["signature algorithm confusion", "signed_measurement_envelope", (row) => {
    row.algorithm = "NONE";
  }],
];
for (const [label, schemaName, mutate] of nestedMutants) {
  const mutant = structuredClone(fixture[schemaName]);
  mutate(mutant);
  if (validators[schemaName](mutant)) fail(`schema accepted nested mutant: ${label}`);
}
process.stdout.write("AJV_R12_FIXTURE_AND_MUTANTS_OK\n");
