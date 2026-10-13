param(
    [string]$RoleCardPath = '<vault>',
    [string]$OutputPath = (Join-Path $PSScriptRoot 'MBCX-01-COHORTBUILD-SEAT3-CODEX-EXEC-PROMPT-r2.txt'),
    [Parameter(Mandatory = $true)][string]$PacketCommit
)

# Content-locating extractor per CC-DEV step 3 packet-cutting discipline: reads the card's
# fenced block AT THE BYTE and REFUSES to emit if any load-bearing lane is missing.

$ErrorActionPreference = 'Stop'
$raw = [System.IO.File]::ReadAllText($RoleCardPath)
$match = [regex]::Match($raw, '(?s)```\r?\n(.*?)\r?\n```')
if (-not $match.Success) { throw 'Council role-card fenced block was not found.' }

$lines = $match.Groups[1].Value -split '\r?\n'
if (-not $lines[0].StartsWith('[COUNCIL MODE')) { throw 'Unexpected council role-card header.' }
if ($lines[-1] -ne 'Reply "Council Mode ready" (one line) and I''ll send the packet.') {
    throw 'Unexpected council role-card closing line.'
}

$seatCard = ($lines[1..($lines.Count - 2)] -join "`n").Trim()

# REFUSE-TO-EMIT content checks — every lane the card must carry.
$requiredLanes = @(
    'SOURCE-POISONING RULE',
    'EXECUTE WHERE THE CLAIM IS EXECUTABLE',
    'WHY THIS EXISTS',
    'PRIMARY-CONSUMER',
    'ROUND CALL',
    'WHAT WOULD YOU BUILD',
    'SWEEP THE WORLD'
)
foreach ($lane in $requiredLanes) {
    if ($seatCard -notmatch [regex]::Escape($lane)) {
        throw "REFUSING TO EMIT: card lane missing: $lane"
    }
}

$pointer = @"


--- TASK PACKET POINTER (one-shot seat: no ack turn; begin now) ---

You are SEAT 3 (codex-exec) of the MBCX-01 cohort-BUILD acceptance council, round 2 — a
TARGETED CONFIRM round on the r1 folds only (r1 was GO-WITH-FIXES/NO-GO/NO-GO, all EXECUTED,
and every finding was folded red-first).

Read ``MBCX-01-COHORT-BUILD-ACCEPTANCE-COUNCIL-PACKET-r2.md`` at commit $PacketCommit in this
repository. The packet pins the content commit under review
(ad713b22f9bad58e3de15df1a05bc78ebdb3728c; py-diff-empty to HEAD is driver-verified, so the
working tree's .py bytes ARE the pinned bytes) and the six fold surfaces with a RULING ASK
each (ACCEPT / CHANGE + one line).

CODE-class artifact: NO round-call token, SKIP the design PROPOSE questions. The EXECUTE lane
is mandatory: run the pinned suites (cohort ~110s, discover ~185s, bundle several minutes —
let them finish), then construct and RUN at least one fresh adversarial probe per item. The
packet's six items are an AGENDA: answer each explicitly (ACCEPT / CHANGE + one line + your
evidence), plus any findings of your own — but this is a CONFIRM round: re-litigating the r1
items ruled SOUND by execution spends the round the folds need.

HOLD THE PACKET'S FIRST IMMUTABLE TRUTH: this lane has NO threat model; a finding counts only
if you name its wrong-number / wrong-admission / wrong-refusal consequence. Do not propose a
new machine. Constraints: no network calls from probes, no ETW/Job-Object execution, no
MBCX01_BUILD_ALLOW_PHYSICAL, no route trials, no spend.

VERDICT CONTRACT: first line GO / GO-WITH-FIXES(class) / NO-GO. Then evidence read
(path:line), your SWEEP LOG, findings each labelled EXECUTED or READ-ONLY with their data
consequence, the six explicit item rulings, the four WHY-THIS-EXISTS answers, residual risks,
fix class. Your final message IS the banked verdict.
"@

$prompt = $seatCard + $pointer
[System.IO.File]::WriteAllText($OutputPath, $prompt, [System.Text.UTF8Encoding]::new($false))

[pscustomobject]@{
    Path = $OutputPath
    Bytes = (Get-Item -LiteralPath $OutputPath).Length
    SHA384 = (Get-FileHash -LiteralPath $OutputPath -Algorithm SHA384).Hash
}
