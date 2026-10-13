$ErrorActionPreference = 'Stop'

$generator = Join-Path $PSScriptRoot 'generate-seat3-experiment-r6-prompt.ps1'
$watcher = Join-Path $PSScriptRoot 'watch-seat3-codex-r6.ps1'
$browserPromptPath = Join-Path $PSScriptRoot 'MBCX-01-BROWSER-SEAT-PROMPT-r6.txt'
$packetPath = Join-Path $PSScriptRoot 'MBCX-01-EXPERIMENT-COUNCIL-PACKET-r6.md'
$testRoot = Join-Path ([System.IO.Path]::GetTempPath()) ('mbcx-r6-dispatch-test-' + [Guid]::NewGuid().ToString('N'))
[void](New-Item -ItemType Directory -Path $testRoot)

try {
    if (-not (Test-Path -LiteralPath $generator)) {
        throw 'Expected r6 one-shot prompt generator is missing.'
    }
    if (-not (Test-Path -LiteralPath $watcher)) {
        throw 'Expected r6 bounded completion watcher is missing.'
    }

    $expectedBrowserPrompt = "Hey homie, can you help me out? Read this and execute:`n<repo>\MBCX-01-EXPERIMENT-COUNCIL-PACKET-r6.md`n"
    $actualBrowserPrompt = [System.IO.File]::ReadAllText($browserPromptPath).Replace("`r`n", "`n")
    if ($actualBrowserPrompt -ne $expectedBrowserPrompt) {
        throw 'Browser prompt is not the exact owner-approved pointer form.'
    }

    $packet = [System.IO.File]::ReadAllText($packetPath)
    foreach ($needle in @(
        '08421f49c39c8c79c14f1ad9ba1789a2a96bcf4a',
        'd37dad7281310974dd9b15a1ae880a6ad84e4108',
        '27abf1a85f80ac942dfc98dc965b2cb3a0226cc9',
        '906a36438460c498c459a2fdb59704698fda4e53',
        'MBCX-01-STATE-ACTION-CONTRACT-v1.json',
        'MBCX-01-INFERENCE-CONTRACT-v1.json'
    )) {
        if (-not $packet.Contains($needle)) {
            throw "Council packet is missing immutable review target: $needle"
        }
    }

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
    if ($prompt -notmatch [regex]::Escape('MBCX-01-EXPERIMENT-COUNCIL-PACKET-r6.md')) {
        throw 'One-shot prompt is missing the r6 packet pointer.'
    }
    if ($prompt -notmatch '08421f49c39c8c79c14f1ad9ba1789a2a96bcf4a') {
        throw 'One-shot prompt is missing the immutable r5 design bundle commit.'
    }
    if ($prompt -notmatch 'packet section 8 exactly') {
        throw 'One-shot prompt is missing the r6 verdict-format pointer.'
    }
    if ($prompt -match 'PACKET-r[1-5]\.md') {
        throw 'One-shot prompt contains a stale packet pointer.'
    }

    $stdoutPath = Join-Path $testRoot 'MBCX-01-SEAT3-CODEX-EXEC-r6.stdout.log'
    $stderrPath = Join-Path $testRoot 'MBCX-01-SEAT3-CODEX-EXEC-r6.stderr.log'
    [System.IO.File]::WriteAllText($stdoutPath, 'WATCHER-VERDICT', [System.Text.UTF8Encoding]::new($false))
    [System.IO.File]::WriteAllText($stderrPath, '', [System.Text.UTF8Encoding]::new($false))
    $shellPath = (Get-Process -Id $PID).Path
    $process = Start-Process -FilePath $shellPath -ArgumentList @(
        '-NoProfile',
        '-Command',
        'Start-Sleep -Milliseconds 250'
    ) -PassThru -WindowStyle Hidden

    & $watcher -CodexPid $process.Id -Root $testRoot

    $verdictPath = Join-Path $testRoot 'MBCX-01-SEAT3-CODEX-VERDICT-r6.md'
    $markerPath = Join-Path $testRoot 'MBCX-01-SEAT3-CODEX-EXEC-r6.complete.json'
    $actualVerdict = [System.IO.File]::ReadAllText($verdictPath)
    if ($actualVerdict -ne 'WATCHER-VERDICT') {
        throw "Watcher did not preserve stdout as the verdict. Actual=<$actualVerdict>"
    }
    $marker = Get-Content -Raw -LiteralPath $markerPath | ConvertFrom-Json
    if (-not $marker.verdict_exists -or $marker.codex_pid -ne $process.Id) {
        throw 'Watcher completion marker is incomplete or identifies the wrong process.'
    }

    'PASS: r6 prompt generation, immutable bundle, and bounded completion watcher contracts hold.'
}
finally {
    $resolved = [System.IO.Path]::GetFullPath($testRoot)
    $tempBase = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
    if ($resolved.StartsWith($tempBase, [StringComparison]::OrdinalIgnoreCase) -and (Test-Path -LiteralPath $resolved)) {
        Remove-Item -LiteralPath $resolved -Recurse -Force
    }
}
