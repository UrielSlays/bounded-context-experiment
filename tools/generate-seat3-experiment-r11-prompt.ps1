param(
    [string]$RoleCardPath = '<vault>',
    [string]$OutputPath
)
$ErrorActionPreference = 'Stop'
if (-not $OutputPath) { $OutputPath = Join-Path $PSScriptRoot 'MBCX-01-SEAT3-CODEX-EXEC-PROMPT-r11.txt' }
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


COUNCIL ROUND — MBCX-01 SEAM CLOSURE r11.

Read and execute this packet completely:
<repo>\MBCX-01-EXPERIMENT-COUNCIL-PACKET-r11.md

The packet pins governing commit b56e450f8553b96f6121cb045b62eb604e4a0655, manifest blob 269dbb3fd905c3875616ac70434e333bcede0a1b, and launcher blob dca3d7951aeba3947af18978b88cc48028c1b572. Authenticate the launcher before execution, reconstruct every subject, execute all no-model attacks, audit the physical-harness prerequisite and conditional-hazard route theorem, sweep relevant prior art, and return the required verdict. Remain sealed from both browser seats and their current-round outputs. Do not edit files, build the physical harness, implement FD/FC/TN, run providers/models/routes, or make paid calls. Return the complete verdict in this command's final response only.
'@
$prompt = $seatCard + $pointer
[System.IO.File]::WriteAllText($OutputPath,$prompt,[System.Text.UTF8Encoding]::new($false))
[pscustomobject]@{Path=$OutputPath;Bytes=(Get-Item -LiteralPath $OutputPath).Length;SHA384=(Get-FileHash -LiteralPath $OutputPath -Algorithm SHA384).Hash}
