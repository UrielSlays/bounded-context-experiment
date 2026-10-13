param(
    [string]$RoleCardPath = '<vault>',
    [string]$OutputPath = (Join-Path $PSScriptRoot 'MBCX-01-COHORT-SEAT3-CODEX-EXEC-PROMPT-r3.txt'),
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

You are SEAT 3 (codex-exec) of the MBCX-01 cohort-content design council, round 3 (issue #17); r1 was 3/3 NO-GO, r2 was GWF/NO-GO/NO-GO, and both folds are the r3 design.

Read ``MBCX-01-COHORT-CONTENT-DESIGN-COUNCIL-PACKET-r3.md`` at commit $PacketCommit in this
repository. The packet pins the artifact under review — ``MBCX-01-BUILD-COHORT-CONTENT-DESIGN.md``
at commit ded124f66ab10b18e9cb08e46c471287a2bc9c33 (rev-parse-emitted, cat-file-verified) — and the frozen bytes it diagnoses. Confirm
what you read and at which commit.

DESIGN-class artifact, council round 3: THE ROUND CALL BINDS - your verdict FIRST LINE is exactly GO-TO-CODE or CONTINUE-DESIGN: <one sentence>; GO-TO-CODE outranks further design findings, and mechanically-testable findings are BUILD red-witness material, not round fuel; the PROPOSE
lane's two questions (what would you build / would you do it differently) DO apply, after the
verdict. The EXECUTE lane applies to the packet's executable DIAGNOSIS: execute at least one fresh probe of your own against the r3 folds (S1/S2 especially).

HOLD THE PACKET'S FIRST IMMUTABLE TRUTH: this lane's design of record has NO threat model; it is
a scientific measurement harness. A finding counts only if you can name how it makes the
experiment produce a WRONG NUMBER, admit WRONG EVIDENCE, or refuse RIGHT evidence — state that
consequence on every finding. Hardening against an actor deliberately evading a check is out of
model and will be ruled out rather than folded. Do not propose a new machine or subsystem.

THE CLAIMS-TO-ATTACK SECTION IS AN AGENDA: answer S1 through S7 each explicitly
(SOUND / DEFECTIVE + one line of why + your evidence), in addition to any findings of your own.

VERDICT CONTRACT: first line GO / GO-WITH-FIXES(class) / NO-GO. Then evidence read (path:line),
your SWEEP LOG, findings each labelled EXECUTED or READ-ONLY with their data consequence, the
seven explicit C-rulings, the four WHY-THIS-EXISTS answers, the two PROPOSE-lane answers,
residual risks, fix class. Your final message IS the banked verdict.
"@

$prompt = $seatCard + $pointer
[System.IO.File]::WriteAllText($OutputPath, $prompt, [System.Text.UTF8Encoding]::new($false))

[pscustomobject]@{
    Path = $OutputPath
    Bytes = (Get-Item -LiteralPath $OutputPath).Length
    SHA384 = (Get-FileHash -LiteralPath $OutputPath -Algorithm SHA384).Hash
}
