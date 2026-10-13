# MBCX-01 Council r3 Dispatch Receipt

**Dispatched:** 2026-08-11 23:27–23:28 America/Los_Angeles

## Immutable review target

- Design commit: `b5874994f89d73efde6da90a445dd5f807808375`
- Design blob: `1e7161e455d6f82707018db454e86985ae85e07f`
- Design SHA-384: `09EF07882AD086F0CA0DD079906894C574F6B81BBA9B7D7F7BD3D8DBBC9A0C2B7FCB0E454698177C3CEF1C53981DFA7A`
- Council packet: `MBCX-01-EXPERIMENT-COUNCIL-PACKET-r3.md`
- Packet/prompt commit: `315351c`

## Seat 1 — Claude Opus 5 Extra

- Council browser profile/CDP: `<browser-profile>` / `<council-browser-port>`
- Fresh conversation: `https://claude.ai/chat/<id>`
- Prompt: `Hey homie, can you help me out? Read this and execute completely:` plus the full r3 packet path.
- Dispatch verification: the seat opened the packet, began role/pin verification, and reported that it was bypassing restricted files.
- Driver state after dispatch: Moonwalker CDP attachment closed; browser and tab left running.

## Seat 2 — ChatGPT / GPT-5.6 Sol lane

- Council browser profile/CDP: `<browser-profile>` / `<council-browser-port>`
- Fresh conversation: `https://chatgpt.com/g/<chatgpt-project>/c/<id>`
- Prompt: `Hey homie, can you help me out? Read this and execute completely:` plus the full r3 packet path.
- Dispatch verification: the seat acknowledged a fresh byte-first packet execution, sealed from prior verdicts, and began reading the driving guide/packet.
- Driver state after dispatch: Moonwalker CDP attachment closed; browser and tab left running.

## Seat 3 — Codex exec

- Command mode: `codex exec`, `--sandbox read-only`, `--ephemeral`, reasoning effort `xhigh`.
- Prompt: `MBCX-01-SEAT3-CODEX-EXEC-PROMPT-r3.txt`
- Expected verdict: `MBCX-01-SEAT3-CODEX-VERDICT-r3.md`
- Codex PID at launch: `37968`
- Completion watcher PID at launch: `32024`
- Completion marker: `MBCX-01-SEAT3-CODEX-EXEC-r3.complete.json`
- Stdout/stderr: `MBCX-01-SEAT3-CODEX-EXEC-r3.stdout.log` / `MBCX-01-SEAT3-CODEX-EXEC-r3.stderr.log`

## Cleanup and polling posture

- Both temporary Moonwalker driver sessions were closed after one dispatch verification; active driver-session count was zero.
- No council browser process or tab was closed.
- The unwanted Ollama app/server processes disclosed by the prior ChatGPT seat were terminated before this dispatch; verification showed no Ollama process remained.
- Codex owns one explicit process and one watcher. The watcher exits after Codex and writes one completion marker.
- No browser polling loop or recurring browser watcher was created. The owner or a later task wakeup may collect results once.

