param(
    [string]$RoleCardPath = '<vault>',
    [string]$OutputPath = (Join-Path $PSScriptRoot 'MBCX-01-BUILD-SEAT3-CODEX-EXEC-PROMPT-r7.txt'),
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

# REFUSE-TO-EMIT content checks — every lane the card must carry (a hand-retype once dropped
# the whole PROPOSE lane; these are the fences).
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

You are SEAT 3 (codex-exec) of the MBCX-01 BUILD acceptance council, round 7.

Read ``MBCX-01-BUILD-ACCEPTANCE-COUNCIL-PACKET-r7.md`` at commit $PacketCommit
in this repository. The packet's section 2 pins the review target at content commit
396752a680d5f057daef51704a2945ccd2735b41 (commits after it are records only — the pin
manifests and the packet itself; ``git diff --stat 396752a HEAD -- '*.py'`` is empty).
Confirm what you read and at which commit.

CODE-class executable artifact: skip the ROUND CALL token and the two design questions. The
EXECUTE lane and the SWEEP lane apply in full.

READ SECTION 0 BEFORE ANYTHING ELSE AND HOLD TO IT. This lane's design of record has NO threat
model; it is a scientific measurement harness. A finding counts only if you can name how it
makes the experiment produce a WRONG NUMBER, admit WRONG EVIDENCE, or refuse RIGHT evidence.
State that consequence on every finding. Hardening against an actor deliberately evading a
check is out of model here and will be ruled out rather than folded. Do not propose a new
machine or subsystem.

SECTION 4 IS AN AGENDA OF RULINGS: items 1-6 each end in a RULING ASK (several carry sub-calls). Answer every one
explicitly (ACCEPT / CHANGE + one line of why) in addition to your findings.

VERDICT CONTRACT: first line GO / GO-WITH-FIXES(class) / NO-GO. Then evidence read (path:line),
your SWEEP LOG, findings each labelled EXECUTED or READ-ONLY with their data consequence, the
seven explicit rulings, residual risks, fix class. Your final message IS the banked verdict.
"@

$prompt = $seatCard + $pointer
[System.IO.File]::WriteAllText($OutputPath, $prompt, [System.Text.UTF8Encoding]::new($false))

[pscustomobject]@{
    Path = $OutputPath
    Bytes = (Get-Item -LiteralPath $OutputPath).Length
    SHA384 = (Get-FileHash -LiteralPath $OutputPath -Algorithm SHA384).Hash
}
