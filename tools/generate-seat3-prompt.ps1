param(
    [string]$RoleCardPath = '<vault>',
    [string]$OutputPath = (Join-Path $PSScriptRoot 'MBCX-01-SEAT3-CODEX-EXEC-PROMPT-r1.txt')
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


COUNCIL ROUND — MBCX-01 DESIGN r1.

Read <repo>\MBCX-01-DESIGN-COUNCIL-PACKET-r1.md at Git commit 95c2b359afb59b1f4e1b096d402a3106c44da339. The packet points to the artifact at commit 5c7ccfe72d0aa84141f7296f185b9c022c6fe294 and all local sources.

Execute the packet exactly. Do your own independent web, prior-art, and footgun search. Return the entire verdict in this command's final response; do not write or edit any file. The verdict must include GO / GO-WITH-FIXES(class) / NO-GO, evidence read, sweep log, findings, residual risks, fix classes, WHAT WOULD YOU BUILD?, and WOULD YOU DO IT DIFFERENTLY?
'@

$prompt = $seatCard + $pointer
[System.IO.File]::WriteAllText($OutputPath, $prompt, [System.Text.UTF8Encoding]::new($false))

[pscustomobject]@{
    Path = $OutputPath
    Bytes = (Get-Item -LiteralPath $OutputPath).Length
    SHA384 = (Get-FileHash -LiteralPath $OutputPath -Algorithm SHA384).Hash
}
