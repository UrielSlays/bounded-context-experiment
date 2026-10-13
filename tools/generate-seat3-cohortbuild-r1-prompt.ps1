param(
    [string]$RoleCardPath = '<vault>',
    [string]$OutputPath = (Join-Path $PSScriptRoot 'MBCX-01-COHORTBUILD-SEAT3-CODEX-EXEC-PROMPT-r1.txt'),
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

You are SEAT 3 (codex-exec) of the MBCX-01 cohort-BUILD acceptance council, round 1. This is a
FRESH arc: the cohort-content DESIGN arc closed GO-TO-CODE at its r3; the artifact under review
now is the CODE that build delivered.

Read ``MBCX-01-COHORT-BUILD-ACCEPTANCE-COUNCIL-PACKET-r1.md`` at commit $PacketCommit in this
repository. The packet pins the content commit under review
(f35851e94b73731dc9cb5db8cb7085471d4c1bac; py-diff-empty to HEAD is driver-verified, so the
working tree's .py bytes ARE the pinned bytes) and enumerates the five artifacts. Confirm what
you read and at which commit.

CODE-class artifact: NO round-call token, and SKIP the two design PROPOSE questions — this
round is purely adversarial-by-execution. The EXECUTE lane is mandatory: run the pinned suites,
then construct and RUN at least one fresh adversarial probe per claim you rule on. The packet's
claims-to-attack section is an AGENDA: answer items 1 through 10 each explicitly
(SOUND / DEFECTIVE + one line of why + your evidence), in addition to any findings of your own.

HOLD THE PACKET'S FIRST IMMUTABLE TRUTH: this lane's design of record has NO threat model; it
is a scientific measurement harness. A finding counts only if you can name how it makes the
experiment produce a WRONG NUMBER, admit WRONG EVIDENCE, or refuse RIGHT evidence — state that
consequence on every finding. Hardening against an actor deliberately evading a check is out of
model and will be ruled out rather than folded. Do not propose a new machine or subsystem.
Constraints while probing: no network calls, no ETW/Job-Object execution, no
MBCX01_BUILD_ALLOW_PHYSICAL, no route trials, no spend. The cohort suite runs ~97s and the full
discover ~170s — let them finish.

VERDICT CONTRACT: first line GO / GO-WITH-FIXES(class) / NO-GO. Then evidence read (path:line),
your SWEEP LOG, findings each labelled EXECUTED or READ-ONLY with their data consequence, the
ten explicit item rulings, the four WHY-THIS-EXISTS answers, residual risks, fix class. Your
final message IS the banked verdict.
"@

$prompt = $seatCard + $pointer
[System.IO.File]::WriteAllText($OutputPath, $prompt, [System.Text.UTF8Encoding]::new($false))

[pscustomobject]@{
    Path = $OutputPath
    Bytes = (Get-Item -LiteralPath $OutputPath).Length
    SHA384 = (Get-FileHash -LiteralPath $OutputPath -Algorithm SHA384).Hash
}
