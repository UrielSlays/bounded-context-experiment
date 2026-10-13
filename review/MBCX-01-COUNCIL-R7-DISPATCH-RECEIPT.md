# MBCX-01 Council r7 Dispatch Receipt

Dispatched: 2026-08-12 16:20 America/Los_Angeles

## Immutable review bundle

- Bundle commit: `6cf58b4ad123cb7487faae5499e623d316a06d47`.
- Design blob: `124e4be74c795f0ab5e686a2ed9d664d45639d1b`.
- State/action contract blob: `e1d8f598dbc00e18fdaa501953f4e68bc3b27d13`.
- Packet-schemas blob: `d31a9aae27e53c6a4e3d8be150db2652a43ff0aa`.
- Measurement contract blob: `095f24be2faecb19f6a6e772c58f5c7468174f54`.
- Inference contract blob: `907d3f65af540bc1efb5674b711f9f0aa593b75e`.
- Council packet: `MBCX-01-EXPERIMENT-COUNCIL-PACKET-r7.md`.
- Packet/prompt commit: `52592a2a7a1c91e8501d3105a3be36cc6ecedb8d`.
- Packet bytes/SHA-384: `13,129` / `C4951B9BEE8EC7023FE0CE8D5690A91A077B8B9B8DF0644D969A0D9EF0CE4F2DDE04D418C229A003E208A3FDA84C9516`.

## Browser pointer delivered identically to both maintained lanes

```text
Hey homie, can you help me out? Read this and execute:
<repo>\MBCX-01-EXPERIMENT-COUNCIL-PACKET-r7.md
```

Retained own-lane context is intentional under the owner's longitudinal-seat ruling. The packet preserves the current-round lateral seal: neither browser seat may inspect the other seats' r7 work or outputs.

## Seat 1 — Claude / Opus maintained lane

- Council browser/CDP: `<council-browser-port>`.
- Exact maintained conversation: `https://claude.ai/chat/<id>`.
- Moonwalker dispatch session: `<id>`.
- Dispatch verified: Moonwalker reported `state: generating` after the r7 pointer was submitted.

## Seat 2 — ChatGPT maintained lane

- Council browser/CDP: `<council-browser-port>`.
- Exact maintained conversation: `https://chatgpt.com/g/<chatgpt-project>/c/<id>`.
- Moonwalker dispatch session: `<id>`.
- Dispatch verified: the active `button[data-testid='stop-button']` was visible after the r7 pointer was submitted.

## Seat 3 — Codex EXEC

- Mode: `codex exec --sandbox read-only --ephemeral` with reasoning effort `xhigh`.
- Prompt: `MBCX-01-SEAT3-CODEX-EXEC-PROMPT-r7.txt`.
- Expected verdict: `MBCX-01-SEAT3-CODEX-VERDICT-r7.md`.
- Codex PID: `8452`.
- Completion watcher PID: `54700`.
- Completion marker: `MBCX-01-SEAT3-CODEX-EXEC-r7.complete.json`.
- Logs: `MBCX-01-SEAT3-CODEX-EXEC-r7.stdout.log` and `.stderr.log`.
- Dispatch verified: Codex PID `8452` and watcher PID `54700` were both live after launch.

## Polling and cleanup posture

- No recurring browser poller or browser watcher was created.
- The Codex watcher waits on exactly PID `8452`, copies stdout to the expected verdict, writes one completion marker, and exits.
- The temporary Moonwalker driver sessions are detached after launch verification; the browser conversations continue independently in their persistent tabs.
- No council browser process or tab was killed.
- The driver now yields until the owner reports that the seats are finished.
