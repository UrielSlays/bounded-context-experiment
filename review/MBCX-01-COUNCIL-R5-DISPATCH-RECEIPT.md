# MBCX-01 Council r5 Dispatch Receipt

Dispatched/staged: 2026-08-12 06:23–06:24 America/Los_Angeles

## Immutable review target

- Design commit: `4e45d16ad85f7033e13368e133f30588c47848a7`
- Design blob: `3f627032a1c54babc7c1aad5f0146a49138a5412`
- Design bytes/lines: `28,155` / `614`
- Design SHA-384: `FCEB7E5E6757D649019DC69F6A6CB739420C7B4315EFFD26391E8CAD72B893F92E1542569747A6A2F19E4C088E3DEEB8`
- Council packet: `MBCX-01-EXPERIMENT-COUNCIL-PACKET-r5.md`
- Packet/prompt commit: `4022c52a34a4751bdf66eb4ad0404f615d44dc4d`

## Seat 1 — outside model/account

- Dispatch state: **STAGED FOR OWNER DELIVERY**.
- Prompt: `MBCX-01-BROWSER-SEAT-PROMPT-r5.txt`.
- This seat was not opened or sent by Codex because the owner is using an account inaccessible to this council harness.

## Seat 2 — ChatGPT Moonwalker MCP / Extra High

- Council browser/CDP: `<council-browser-port>`.
- Fresh project conversation: `https://chatgpt.com/g/<chatgpt-project>/c/<id>`.
- Prompt: `MBCX-01-BROWSER-SEAT-PROMPT-r5.txt`.
- Dispatch verified: the pointer prompt is present as the first user turn and the UI exposed its active stop control.
- Temporary Moonwalker driver session closed; browser and conversation continue independently.

## Seat 3 — Codex exec

- Mode: `codex exec --sandbox read-only --ephemeral` with reasoning effort `xhigh`.
- Prompt: `MBCX-01-SEAT3-CODEX-EXEC-PROMPT-r5.txt`.
- Expected verdict: `MBCX-01-SEAT3-CODEX-VERDICT-r5.md`.
- Codex PID: `11524`.
- Completion watcher PID: `34992`.
- Completion marker: `MBCX-01-SEAT3-CODEX-EXEC-r5.complete.json`.
- Logs: `MBCX-01-SEAT3-CODEX-EXEC-r5.stdout.log` and `.stderr.log`.

## Polling and cleanup posture

- No browser polling loop or recurring browser watcher was created.
- The Codex watcher waits on exactly PID `11524`, writes one bounded completion marker, and exits.
- The temporary Moonwalker dispatch session was closed after verification.
- No council browser process or tab was killed.
