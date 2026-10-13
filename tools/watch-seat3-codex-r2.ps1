param(
    [Parameter(Mandatory = $true)]
    [int]$CodexPid,
    [Parameter(Mandatory = $true)]
    [string]$Root
)

$ErrorActionPreference = 'Stop'
Wait-Process -Id $CodexPid -ErrorAction SilentlyContinue

$verdict = Join-Path $Root 'MBCX-01-SEAT3-CODEX-VERDICT-r2.md'
$stdout = Join-Path $Root 'MBCX-01-SEAT3-CODEX-EXEC-r2.stdout.log'
$stderr = Join-Path $Root 'MBCX-01-SEAT3-CODEX-EXEC-r2.stderr.log'
$marker = Join-Path $Root 'MBCX-01-SEAT3-CODEX-EXEC-r2.complete.json'

$record = [ordered]@{
    codex_pid = $CodexPid
    completed_at_utc = [DateTime]::UtcNow.ToString('o')
    verdict_exists = Test-Path -LiteralPath $verdict
    verdict_bytes = if (Test-Path -LiteralPath $verdict) { (Get-Item -LiteralPath $verdict).Length } else { 0 }
    stdout_bytes = if (Test-Path -LiteralPath $stdout) { (Get-Item -LiteralPath $stdout).Length } else { 0 }
    stderr_bytes = if (Test-Path -LiteralPath $stderr) { (Get-Item -LiteralPath $stderr).Length } else { 0 }
}

[System.IO.File]::WriteAllText(
    $marker,
    ($record | ConvertTo-Json),
    [System.Text.UTF8Encoding]::new($false)
)
