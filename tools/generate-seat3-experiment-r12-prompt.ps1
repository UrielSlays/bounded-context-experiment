param(
    [string]$RoleCardPath = '<vault>',
    [string]$OutputPath
)
$ErrorActionPreference = 'Stop'
if (-not $OutputPath) { $OutputPath = Join-Path $PSScriptRoot 'MBCX-01-SEAT3-CODEX-EXEC-PROMPT-r12.txt' }
$raw = [System.IO.File]::ReadAllText($RoleCardPath)
$fence = [string]([char]96) * 3
$pattern = '(?s)' + [regex]::Escape($fence) + '\r?\n(.*?)\r?\n' + [regex]::Escape($fence)
$match = [regex]::Match($raw,$pattern)
if (-not $match.Success) { throw 'Council role-card fenced block was not found.' }
$lines = $match.Groups[1].Value -split '\r?\n'
if (-not $lines[0].StartsWith('[COUNCIL MODE')) { throw 'Unexpected role-card header.' }
if ($lines[-1] -ne 'Reply "Council Mode ready" (one line) and I''ll send the packet.') { throw 'Unexpected role-card close.' }
$seatCard = ($lines[1..($lines.Count - 2)] -join [Environment]::NewLine).Trim()
$requiredRoleCardText = @(
    'SOURCE-POISONING RULE:',
    'WHY THIS EXISTS',
    'EXECUTE WHERE THE CLAIM IS EXECUTABLE:',
    'WHAT WOULD YOU BUILD?',
    'WOULD YOU DO IT DIFFERENTLY'
)
foreach ($needle in $requiredRoleCardText) {
    if (-not $seatCard.Contains($needle)) { throw "Council role-card lost required doctrine: $needle" }
}
$pointer = @'


COUNCIL ROUND — MBCX-01 AUTHORITY CLOSURE r12.

Read and execute this packet completely:
<repo>\MBCX-01-EXPERIMENT-COUNCIL-PACKET-r12.md

The packet pins governing commit 235f37bcbf213e6700c30333d6fee6a68f0886b6, manifest blob bd84a65b7b85530345a82a552d7c47f9e148f1a7, and launcher blob 2b575b10f3c00c7a3ac79a39e54693104443f330. Authenticate the launcher before execution, reconstruct every subject, execute all no-model attacks, audit the authoritative state transition, ambiguity terminal, receipt/trust-root boundary, exact Windows physical-harness prerequisites and inference witnesses, sweep relevant prior art and the internal shelf, and return the required verdict. Remain sealed from both browser seats and their current-round outputs. Do not edit files, build or run the physical harness, run the scientific experiment, qualify routes, invoke providers/models, or make paid calls. Return the complete verdict in this command's final response only.
'@
$prompt = $seatCard + $pointer
[System.IO.File]::WriteAllText($OutputPath,$prompt,[System.Text.UTF8Encoding]::new($false))
[pscustomobject]@{Path=$OutputPath;Bytes=(Get-Item -LiteralPath $OutputPath).Length;SHA384=(Get-FileHash -LiteralPath $OutputPath -Algorithm SHA384).Hash}
