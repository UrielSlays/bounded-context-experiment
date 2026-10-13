param(
    [string]$RoleCardPath = '<vault>',
    [string]$OutputPath
)
$ErrorActionPreference = 'Stop'
if (-not $OutputPath) { $OutputPath = Join-Path $PSScriptRoot 'MBCX-01-SEAT3-CODEX-EXEC-PROMPT-r13.txt' }
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


COUNCIL ROUND — MBCX-01 FINAL AUTHORITY CLOSURE r13.

Read and execute this packet completely:
<repo>\MBCX-01-EXPERIMENT-COUNCIL-PACKET-r13.md

The packet pins governing commit ec583834e08df77b65ca773ef6fdf525b0ee51b2, manifest blob d71e653d95df662097d2507299fd85ff265ed856, and launcher blob ba046408a0a210176d6d53616a8535eb26542be4. Authenticate the launcher, reconstruct all 31 subjects, run the no-paid closure attacks, and adjudicate I01–I17 under the owner-locked GO / GO-WITH-FIXES / NO-GO taxonomy. This is a closure decision, not an unconstrained new design round. Remain sealed from both browser seats and their r13 outputs. Do not edit files, build or run production adapters or the physical harness, run the scientific experiment, qualify routes, invoke providers/models, or make paid calls. Return the complete verdict in this command's final response only.
'@
$prompt = $seatCard + $pointer
[System.IO.File]::WriteAllText($OutputPath,$prompt,[System.Text.UTF8Encoding]::new($false))
[pscustomobject]@{Path=$OutputPath;Bytes=(Get-Item -LiteralPath $OutputPath).Length;SHA384=(Get-FileHash -LiteralPath $OutputPath -Algorithm SHA384).Hash}
