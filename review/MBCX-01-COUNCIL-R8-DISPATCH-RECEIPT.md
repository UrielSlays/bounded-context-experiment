# MBCX-01 Council r8 Dispatch Receipt

Dispatched: 2026-08-12 18:26-18:27 America/Los_Angeles

## Immutable review bundle

- Normative bundle commit: `7c43d67c6f8d8cf9ecedc09a059dbb0f3fccbba7`.
- Design blob: `9010a4ef8e5b5d10593ef48012bf6d1f92ee9e9a`.
- State/action contract blob: `cc067bd9756b78ceeb14696d0b5daea49330e6ac`.
- Packet-schemas blob: `80e739b955613fffd619de753291a99ff8cbc5c4`.
- Measurement contract blob: `e58aed18aca116415b3b408ca668f7676433b06a`.
- Inference contract blob: `edbfa2e78a53bc07ef2de22f087d5d377b2afaf0`.
- Council packet: `MBCX-01-EXPERIMENT-COUNCIL-PACKET-r8.md`.
- Packet/prompt commit: `163403eb2093acf27a38e678a75c3b0ea7454983`.
- Packet bytes/SHA-384: `18,436` / `7D673BA71FACB0778DA4446DE15C77BA0963834EC2800C66CE0A9DE788682D9CE4FC8821DEBFAB67BB9965FD6FE44545`.
- Full no-paid verification: five sections PASS; 10,000 synthetic replicates per nine cells; zero paid calls.

## Browser pointer delivered identically to both maintained lanes

```text
Hey homie, can you help me out? Read this and execute:
<repo>\MBCX-01-EXPERIMENT-COUNCIL-PACKET-r8.md
```

Retained own-lane context is intentional under the owner's longitudinal-seat ruling. The packet preserves the current-round lateral seal: neither browser seat may inspect another seat's r8 work or output.

## Seat 1 — Claude maintained Opus lane

- Council browser/CDP: `<council-browser-port>`.
- Exact maintained conversation: `https://claude.ai/chat/<id>`.
- Moonwalker dispatch session: `<id>`.
- Dispatch verified: the Claude stop-generation control became visible after submission.

## Seat 2 — ChatGPT maintained Sol lane

- Council browser/CDP: `<council-browser-port>`.
- Exact maintained conversation: `https://chatgpt.com/g/<chatgpt-project>/c/<id>`.
- Moonwalker dispatch session: `<id>`.
- Dispatch verified: `button[data-testid='stop-button']` became visible after submission.

## Seat 3 — Codex EXEC

- Mode: `codex exec --sandbox read-only --ephemeral`.
- Model/reasoning: `gpt-daybreak-blue-latest`, `xhigh`, matching the preceding Codex EXEC lane.
- Prompt: `MBCX-01-SEAT3-CODEX-EXEC-PROMPT-r8.txt`.
- Prompt bytes/SHA-384 before launch: `11,202` / `B8B2A601D52152F1E0ADBE1A00EE508B862AD8D0D1897042158A4C6DB8EA86E221D9C28CDB1EA455B77E28EF1D780BD3`.
- Expected verdict: `MBCX-01-SEAT3-CODEX-VERDICT-r8.md`.
- Codex PID: `55980`.
- Completion watcher PID: `18900`.
- Completion marker: `MBCX-01-SEAT3-CODEX-EXEC-r8.complete.json`.
- Logs: `MBCX-01-SEAT3-CODEX-EXEC-r8.stdout.log` and `.stderr.log`.
- Dispatch verified: the process banner recorded the exact root, model, read-only sandbox, xhigh effort, ephemeral session, and r8 prompt; Codex and watcher PIDs were live at 18:28 local.

## Polling and cleanup posture

- No recurring browser poller or browser watcher was created.
- The Codex watcher waits on exactly PID `55980`, copies stdout to the expected verdict, writes one completion marker, and exits.
- The two temporary Moonwalker CDP attachments were closed after launch verification. Closing the attachments disconnected Playwright only; it did not kill or close either provider tab/browser.
- No council browser process or tab was killed.
- The driver now yields until the owner reports that the seats are finished.
