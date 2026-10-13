# MBCX-01 Council r6 Dispatch Receipt

Dispatched/staged: 2026-08-12 07:36 America/Los_Angeles

## Immutable review bundle

- Bundle commit: `08421f49c39c8c79c14f1ad9ba1789a2a96bcf4a`.
- Design blob: `d37dad7281310974dd9b15a1ae880a6ad84e4108`.
- State/action contract blob: `27abf1a85f80ac942dfc98dc965b2cb3a0226cc9`.
- Inference contract blob: `906a36438460c498c459a2fdb59704698fda4e53`.
- Council packet: `MBCX-01-EXPERIMENT-COUNCIL-PACKET-r6.md`.
- Packet/prompt commit: `8e60562d7cef3f11bd7dd2d1767f171720db3995`.
- Packet bytes/SHA-384: `17,843` / `73B6CB05DF490BCF4DCA2C2749D92F56369DC50648BF90313C9D145E0E65D235F83F2A8DBB42047B0F3D40A50E8C3198`.

## Seat 1 — outside model/account

- Dispatch state: **STAGED FOR OWNER DELIVERY**.
- Prompt: `MBCX-01-BROWSER-SEAT-PROMPT-r6.txt`.
- The r6 packet requires disclosure if the outside conversation retains a prior MBCX-01 round; repeated advice from such a seat is not counted as independent confirmation.

## Seat 2 — ChatGPT Moonwalker MCP / Extra High

- Council browser/CDP: `<council-browser-port>`.
- Fresh project conversation: `https://chatgpt.com/g/<chatgpt-project>/c/<id>`.
- Prompt: `MBCX-01-BROWSER-SEAT-PROMPT-r6.txt`.
- Dispatch verified: the r6 pointer is the first user turn and the active stop control was visible.
- Temporary Moonwalker driver session closed; browser and conversation continue independently.

## Seat 3 — Codex exec

- Mode: `codex exec --sandbox read-only --ephemeral` with reasoning effort `xhigh`.
- Prompt: `MBCX-01-SEAT3-CODEX-EXEC-PROMPT-r6.txt`.
- Expected verdict: `MBCX-01-SEAT3-CODEX-VERDICT-r6.md`.
- Codex PID: `45480`.
- Completion watcher PID: `46272`.
- Completion marker: `MBCX-01-SEAT3-CODEX-EXEC-r6.complete.json`.
- Logs: `MBCX-01-SEAT3-CODEX-EXEC-r6.stdout.log` and `.stderr.log`.

## Polling and cleanup posture

- No browser polling loop or recurring browser watcher was created.
- The Codex watcher waits on exactly PID `45480`, writes one completion marker, and exits.
- The temporary Moonwalker dispatch session was closed after verification.
- No process or tab on council profile `<council-browser-port>` was touched.
- No council browser process or tab was killed.
