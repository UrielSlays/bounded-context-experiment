# MBCX-01 Council r10 Dispatch Receipt

Dispatched: 2026-08-12 23:22-23:23 America/Los_Angeles

## Immutable review bundle

- Governing repair commit: `efaa1bbff91b887597b711ff4936109e79ccfddd`.
- Owner-pinned manifest blob: `12589dbf0cc48704ae758d00fff1d9b0d16e2c01`.
- Council delivery commit: `c21533306daffcc77949eddddf1ae234e82724a2`.
- Council packet: `MBCX-01-EXPERIMENT-COUNCIL-PACKET-r10.md`.
- Packet working-copy bytes/SHA-384: `17,304` / `8CF025C8EC81C14394D5CC1155AEF51B23353736987ED75C0B8DB0887901FAC2FDADF4C7E465CFE6ECFE5AB6B3D8899D`.
- Browser pointer artifact working-copy bytes/SHA-384: `178` / `4553C777E48E0A6CD511208311C34D2551FDCBE443CC9BED5803BF6A5D95919DF759FF8DE24D174E38BC6F580FFD7F5F`.
- Codex prompt working-copy bytes/SHA-384: `11,301` / `6D976FABF6107C76FEBB7703F4931C454BDBD7557AB3F1F709FD00FE75A65D30D39DCE5E3F09294AE793900D683AE7D1`.
- Git-object-only reconstruction: state, packets, cohort, measurement, inference, and integration all PASS.
- Evidence classification: deterministic no-model verification only; `experiment_evidence=false`, `paid_calls=0`.

Both browser composers were read and confirmed empty before this round's content was entered. Moonwalker's rich-text editors did not preserve the approved newline on the first fill, so the incomplete draft was cleared and the same complete pointer was sent as one line:

```text
Hey homie, can you help me out? Read this and execute: <repo>\MBCX-01-EXPERIMENT-COUNCIL-PACKET-r10.md
```

The content and artifact path are identical in both seats. Retained own-lane context is intentional under the owner's longitudinal-seat ruling. The packet requires the current-round lateral seal.

## Seat 1 — maintained Claude Opus lane

- CDP endpoint: `<council-browser-port>`.
- Conversation: `https://claude.ai/chat/<id>` (`Council mode activation`).
- Moonwalker attachment: `<id>`.
- Bound URL was verified before typing.
- Dispatch witness: `moonwalker_browser_wait_quiesced` returned `state=generating`, current-turn text beginning `Working`, and Moonwalker file reads.
- Attachment close: `terminalOutcome=ok`; the tab and conversation remained open.

## Seat 2 — maintained ChatGPT Sol lane

- CDP endpoint: `<council-browser-port>`.
- Conversation: `https://chatgpt.com/g/<chatgpt-project>/c/<id>` (`ChatGPT - Moonwalker MCP`).
- Moonwalker attachment: `<id>`.
- Bound URL was verified before typing.
- Dispatch witness: `moonwalker_browser_wait_quiesced` returned `state=generating`, current-turn text `Thinking`.
- Attachment close: `terminalOutcome=ok`; the tab and conversation remained open.

## Seat 3 — fresh Codex EXEC

- Invocation: `codex exec -m gpt-5.6-sol -c service_tier=default -c model_reasoning_effort=xhigh -c approval_policy=never -s danger-full-access --ephemeral -` with the generated one-shot prompt on stdin.
- Fresh ephemeral session: `<id>`.
- Codex PID: `41072`.
- Watcher PID: `55068`.
- Stderr banner verified the pinned working root, `gpt-5.6-sol`, `approval=never`, `danger-full-access`, and `xhigh`.
- Completion marker: `MBCX-01-SEAT3-CODEX-EXEC-r10.complete.json`.
- Logs: `MBCX-01-SEAT3-CODEX-EXEC-r10.stdout.log` and `.stderr.log`.
- Expected banked verdict: `MBCX-01-SEAT3-CODEX-VERDICT-r10.md`.

## Polling and cleanup posture

- No recurring browser poller or browser watcher was created; the owner will wake the driver when the council is finished.
- The Codex watcher waits only on PID `41072`, banks stdout as the r10 verdict, writes one completion marker, and exits.
- Both temporary Moonwalker CDP attachments were closed after generation was verified.
- No browser, tab, council process, or unrelated Codex process was killed.
- No FD/FC/TN candidate, route soak, provider experiment, or paid scientific model call was run.

