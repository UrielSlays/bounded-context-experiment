param(
    [string]$RoleCardPath = '<vault>',
    [string]$OutputPath = (Join-Path $PSScriptRoot 'MBCX-01-SEAT3-CODEX-EXEC-PROMPT-r2.txt')
)

$ErrorActionPreference = 'Stop'
$raw = [System.IO.File]::ReadAllText($RoleCardPath)
$match = [regex]::Match($raw, '(?s)```\r?\n(.*?)\r?\n```')
if (-not $match.Success) {
    throw 'Council role-card fenced block was not found.'
}

$lines = $match.Groups[1].Value -split '\r?\n'
if (-not $lines[0].StartsWith('[COUNCIL MODE')) {
    throw 'Unexpected council role-card header.'
}
if ($lines[-1] -ne 'Reply "Council Mode ready" (one line) and I''ll send the packet.') {
    throw 'Unexpected council role-card closing line.'
}

$seatCard = ($lines[1..($lines.Count - 2)] -join "`n").Trim()
$pointer = @'


COUNCIL ROUND — MBCX-01 EXPERIMENT-SPECIFIC DESIGN r2.

Read and execute this packet completely:
<repo>\MBCX-01-EXPERIMENT-COUNCIL-PACKET-r2.md

The packet pins the artifact under review at Git commit 7fa45e092bb7db14d85761f65a63b97a3740c65e and carries the experiment-specific scope override. That override governs applicability: independently search prior art and footguns, execute the no-cost attacks, and review scientific validity; do not turn licensing, distribution, production security, or Moonwalker delivery ceremony into findings unless you prove a direct path to a false experimental answer.

Remain sealed from the browser seats and prior-round verdict files. Do not open or seek them. Do not edit files or run paid inference. Return the entire verdict in this command's final response only, following packet section 10 exactly.
'@

$prompt = $seatCard + $pointer
[System.IO.File]::WriteAllText($OutputPath, $prompt, [System.Text.UTF8Encoding]::new($false))

[pscustomobject]@{
    Path = $OutputPath
    Bytes = (Get-Item -LiteralPath $OutputPath).Length
    SHA384 = (Get-FileHash -LiteralPath $OutputPath -Algorithm SHA384).Hash
}
