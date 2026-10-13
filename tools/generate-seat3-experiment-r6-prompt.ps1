param(
    [string]$RoleCardPath = '<vault>',
    [string]$OutputPath = (Join-Path $PSScriptRoot 'MBCX-01-SEAT3-CODEX-EXEC-PROMPT-r6.txt')
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


COUNCIL ROUND — MBCX-01 EXECUTABLE BOUNDED OBLIGATION CONTINUITY r6.

Read and execute this packet completely:
<repo>\MBCX-01-EXPERIMENT-COUNCIL-PACKET-r6.md

The packet pins a three-artifact normative bundle at Git commit 08421f49c39c8c79c14f1ad9ba1789a2a96bcf4a and carries the experiment-specific scope override. Independently search current prior art and footguns, execute the no-paid attacks, and review scientific validity. Do not turn licensing, distribution, production security, cross-model generalization, concurrent canonical writing, or Moonwalker delivery ceremony into findings unless you prove a direct path to a false MBCX-01 answer.

Remain sealed from browser seats and every prior-round verdict/report/synthesis/log/receipt. Do not open or seek them. Do not edit files or run paid inference. Return the entire verdict in this command's final response only, following packet section 8 exactly.
'@

$prompt = $seatCard + $pointer
[System.IO.File]::WriteAllText($OutputPath, $prompt, [System.Text.UTF8Encoding]::new($false))

[pscustomobject]@{
    Path = $OutputPath
    Bytes = (Get-Item -LiteralPath $OutputPath).Length
    SHA384 = (Get-FileHash -LiteralPath $OutputPath -Algorithm SHA384).Hash
}
