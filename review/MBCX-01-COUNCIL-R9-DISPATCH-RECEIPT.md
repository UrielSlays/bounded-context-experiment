# MBCX-01 Council r9 Dispatch Receipt

Dispatched: 2026-08-12 22:01-22:02 America/Los_Angeles

## Immutable review bundle

- Normative bundle commit: `f8fa75647f702dcc14f91b2d974ed1497aeef400`.
- Council delivery commit: `1b450e819af386c82f7b016f2d646f499d7e8290`.
- Council packet: `MBCX-01-EXPERIMENT-COUNCIL-PACKET-r9.md`.
- Packet bytes/SHA-384: `19,264` / `3E257A784EE151202B6D85EBE477AC03B348A8537CC820A56A3B33581E0B7AF729ABCF231CCA50D7874266B9FA6417D7`.
- Browser pointer bytes/SHA-384: `176` / `3535E3A5473B86DA2B2824565D460009212ACFC400D00A0DA8C239C0A3E49458307C4B8729E2DA35C9F6F85ABF59573E`.
- Git-object-only reconstruction: all six sections PASS from extracted pinned blobs.
- Retained no-paid report: 16 OC cells x 10,000 replicates, every practical power target above 90%, `experiment_evidence=false`, `paid_calls=0`.

## Identical browser pointer

```text
Hey homie, can you help me out? Read this and execute:
<repo>\MBCX-01-EXPERIMENT-COUNCIL-PACKET-r9.md
```

Retained own-lane context is intentional under the owner's longitudinal-seat ruling. The packet preserves the current-round lateral seal.

## Seat 1 — maintained Claude Opus lane

- CDP endpoint: `<council-browser-port>`.
- Conversation: `https://claude.ai/chat/<id>` (`Council mode activation`).
- Moonwalker dispatch session: `<id>`.
- Bound URL was verified before typing.
- Dispatch witness: `moonwalker_browser_wait_quiesced` returned `state=generating` with current-turn text `Working` after send.

## Seat 2 — maintained ChatGPT Sol lane

- CDP endpoint: `<council-browser-port>`.
- Conversation: `https://chatgpt.com/g/<chatgpt-project>/c/<id>` (`ChatGPT - Moonwalker MCP`).
- Moonwalker dispatch session: `<id>`.
- Bound URL was verified before typing.
- Dispatch witness: `moonwalker_browser_wait_quiesced` returned `state=generating` after send.

## Seat 3 — fresh Codex EXEC

- Invocation: `codex exec -m gpt-5.6-sol -c service_tier=default -c model_reasoning_effort=xhigh --ephemeral` with the generated prompt on stdin.
- Prompt: `MBCX-01-SEAT3-CODEX-EXEC-PROMPT-r9.txt`.
- Prompt bytes/SHA-384: `11,244` / `D0951D6206292D06F23EDF73E261A2F5AA56C6BD9F3832BC2856730AEC1C7AA2D2E2EC867042B827E644B4201C6C369B`.
- Codex PID: `56220`.
- Watcher PID: `25656`.
- Completion marker: `MBCX-01-SEAT3-CODEX-EXEC-r9.complete.json`.
- Logs: `MBCX-01-SEAT3-CODEX-EXEC-r9.stdout.log` and `.stderr.log`.
- Expected verdict: `MBCX-01-SEAT3-CODEX-VERDICT-r9.md`.
- Dispatch witness: PID and watcher were live; the process command line recorded `service_tier=default`, while the stderr banner recorded the exact working root, `gpt-5.6-sol`, `danger-full-access`, `approval=never`, `xhigh`, and a fresh ephemeral session ID.

## Polling and cleanup posture

- No recurring browser poller or browser watcher was created; the owner will wake the driver when the council is finished.
- The Codex watcher waits on exactly PID `56220`, banks stdout as the r9 verdict, writes one completion marker, and exits.
- Both temporary Moonwalker CDP attachments were closed after generation was verified. Attachment close disconnected Playwright only and did not close either browser tab or conversation.
- No browser, tab, or council process was killed.
- No paid experiment, model, or route-soak call was made by the r9 repair and verification work.
