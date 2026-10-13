# MBCX-01 Council r4 Dispatch Receipt

Dispatched/staged: 2026-08-12 03:06–03:07 America/Los_Angeles

## Immutable review target

- Design commit: `f3f9273678867ace9747413d808a5f47243548c0`
- Design blob: `4d7fd5035d746935778020dcd7fab1df573ec3d8`
- Design bytes/lines: `32,319` / `569`
- Design SHA-384: `C1D80168F0CBE0683E94CC4564238622C5EF87AEA6D51101EB89CADBD7EBF3A0A30856A05CCDC1967E262F3A3C228BDC`
- Council packet: `MBCX-01-EXPERIMENT-COUNCIL-PACKET-r4.md`
- Packet/prompt commit: `354c5cc`

## Seat 1 — Claude Opus 5 Extra

- Council browser/CDP: `<council-browser-port>`
- Fresh page prepared: `https://claude.ai/new`
- Prompt entered from `MBCX-01-BROWSER-SEAT-PROMPT-r4.txt`.
- **Dispatch state: BLOCKED-NOT-SENT.** Claude displayed: `You're out of usage credits ... wait until Aug 12 at 10:00 AM when your plan usage resets.`
- The unsent prompt remains staged in the fresh browser tab. This seat must not be counted until the message is actually sent after reset.
- Temporary Moonwalker driver session closed; the browser/tab was not killed.

## Seat 2 — ChatGPT Moonwalker MCP / Extra High

- Council browser/CDP: `<council-browser-port>`
- Fresh project conversation: `https://chatgpt.com/g/<chatgpt-project>/c/<id>`
- Prompt: `MBCX-01-BROWSER-SEAT-PROMPT-r4.txt`.
- Dispatch verified: prompt is the first user turn; UI showed `Thinking` / `Searching project context`.
- Temporary Moonwalker driver session closed; browser and conversation continue independently.

## Seat 3 — Codex exec

- Mode: `codex exec --sandbox read-only --ephemeral` with reasoning effort `xhigh`.
- Prompt: `MBCX-01-SEAT3-CODEX-EXEC-PROMPT-r4.txt`.
- Expected verdict: `MBCX-01-SEAT3-CODEX-VERDICT-r4.md`.
- Codex PID: `32108`.
- Completion watcher PID: `38504`.
- Completion marker: `MBCX-01-SEAT3-CODEX-EXEC-r4.complete.json`.
- Logs: `MBCX-01-SEAT3-CODEX-EXEC-r4.stdout.log` and `.stderr.log`.

## Polling and cleanup posture

- No browser polling loop or recurring browser watcher was created.
- The Codex watcher waits on exactly PID `32108`, writes one bounded completion marker, and exits.
- Both temporary Moonwalker dispatch sessions were closed after verification.
- One unrelated pre-existing Moonwalker session for `dodsbirsttr.mil` was observed and deliberately left untouched.
- No council browser process or tab was killed.
