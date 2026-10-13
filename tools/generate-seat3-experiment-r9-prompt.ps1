param(
    [string]$RoleCardPath = '<vault>',
    [string]$OutputPath = (Join-Path $PSScriptRoot 'MBCX-01-SEAT3-CODEX-EXEC-PROMPT-r9.txt')
)
$ErrorActionPreference = 'Stop'
$raw = [System.IO.File]::ReadAllText($RoleCardPath)
$fence = [string]([char]96) * 3
$pattern = '(?s)' + [regex]::Escape($fence) + '\r?\n(.*?)\r?\n' + [regex]::Escape($fence)
$match = [regex]::Match($raw,$pattern)
if (-not $match.Success) { throw 'Council role-card fenced block was not found.' }
$lines = $match.Groups[1].Value -split '\r?\n'
if (-not $lines[0].StartsWith('[COUNCIL MODE')) { throw 'Unexpected role-card header.' }
if ($lines[-1] -ne 'Reply "Council Mode ready" (one line) and I''ll send the packet.') { throw 'Unexpected role-card close.' }
$seatCard = ($lines[1..($lines.Count - 2)] -join [Environment]::NewLine).Trim()
$pointer = @'


COUNCIL ROUND — MBCX-01 ANSWERABLE RECONSTRUCTION r9.

Read and execute this packet completely:
<repo>\MBCX-01-EXPERIMENT-COUNCIL-PACKET-r9.md

The packet pins the normative bundle at Git commit f8fa75647f702dcc14f91b2d974ed1497aeef400. Execute the Git-object reconstruction, no-paid behavioral attacks, theorem/numerical audit, physical-work attacks, practical power and cost audit, and exact verdict format. Remain sealed from both browser seats and their current-round outputs. Do not edit files, implement FD/FC/TN, or make paid calls. Return the complete verdict in this command's final response only.
'@
$prompt = $seatCard + $pointer
[System.IO.File]::WriteAllText($OutputPath,$prompt,[System.Text.UTF8Encoding]::new($false))
[pscustomobject]@{Path=$OutputPath;Bytes=(Get-Item -LiteralPath $OutputPath).Length;SHA384=(Get-FileHash -LiteralPath $OutputPath -Algorithm SHA384).Hash}
