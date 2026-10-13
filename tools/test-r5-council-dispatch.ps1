$ErrorActionPreference = 'Stop'

$generator = Join-Path $PSScriptRoot 'generate-seat3-experiment-r5-prompt.ps1'
$watcher = Join-Path $PSScriptRoot 'watch-seat3-codex-r5.ps1'
$testRoot = Join-Path ([System.IO.Path]::GetTempPath()) ('mbcx-r5-dispatch-test-' + [Guid]::NewGuid().ToString('N'))
[void](New-Item -ItemType Directory -Path $testRoot)

try {
    $promptPath = Join-Path $testRoot 'seat3-prompt.txt'
    & $generator -OutputPath $promptPath | Out-Null
    $prompt = [System.IO.File]::ReadAllText($promptPath)

    if ($prompt.StartsWith('[COUNCIL MODE')) {
        throw 'One-shot prompt retained the browser-only handshake header.'
    }
    if ($prompt -match 'Reply "Council Mode ready"') {
        throw 'One-shot prompt retained the browser-only acknowledgement request.'
    }
    if (-not $prompt.StartsWith('ROLE: You are an independent Moonwalker council reviewer')) {
        throw 'One-shot prompt does not begin with the canonical ROLE line.'
    }
    if ($prompt -notmatch [regex]::Escape('MBCX-01-EXPERIMENT-COUNCIL-PACKET-r5.md')) {
        throw 'One-shot prompt is missing the r5 packet pointer.'
    }
    if ($prompt -notmatch '4e45d16ad85f7033e13368e133f30588c47848a7') {
        throw 'One-shot prompt is missing the immutable r4 design commit.'
    }
    if ($prompt -notmatch 'packet section 8 exactly') {
        throw 'One-shot prompt is missing the r5 verdict-format pointer.'
    }
    if ($prompt -match 'PACKET-r[1-4]\.md') {
        throw 'One-shot prompt contains a stale packet pointer.'
    }

    $stdoutPath = Join-Path $testRoot 'MBCX-01-SEAT3-CODEX-EXEC-r5.stdout.log'
    $stderrPath = Join-Path $testRoot 'MBCX-01-SEAT3-CODEX-EXEC-r5.stderr.log'
    [System.IO.File]::WriteAllText($stdoutPath, 'WATCHER-VERDICT', [System.Text.UTF8Encoding]::new($false))
    [System.IO.File]::WriteAllText($stderrPath, '', [System.Text.UTF8Encoding]::new($false))
    $shellPath = (Get-Process -Id $PID).Path
    $process = Start-Process -FilePath $shellPath -ArgumentList @(
        '-NoProfile',
        '-Command',
        'Start-Sleep -Milliseconds 250'
    ) -PassThru -WindowStyle Hidden

    & $watcher -CodexPid $process.Id -Root $testRoot

    $verdictPath = Join-Path $testRoot 'MBCX-01-SEAT3-CODEX-VERDICT-r5.md'
    $markerPath = Join-Path $testRoot 'MBCX-01-SEAT3-CODEX-EXEC-r5.complete.json'
    $actualVerdict = [System.IO.File]::ReadAllText($verdictPath)
    if ($actualVerdict -ne 'WATCHER-VERDICT') {
        throw "Watcher did not preserve stdout as the verdict. Actual=<$actualVerdict>"
    }
    $marker = Get-Content -Raw -LiteralPath $markerPath | ConvertFrom-Json
    if (-not $marker.verdict_exists -or $marker.codex_pid -ne $process.Id) {
        throw 'Watcher completion marker is incomplete or identifies the wrong process.'
    }

    'PASS: r5 prompt generation and bounded completion watcher contracts hold.'
}
finally {
    $resolved = [System.IO.Path]::GetFullPath($testRoot)
    $tempBase = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
    if ($resolved.StartsWith($tempBase, [StringComparison]::OrdinalIgnoreCase) -and (Test-Path -LiteralPath $resolved)) {
        Remove-Item -LiteralPath $resolved -Recurse -Force
    }
}
