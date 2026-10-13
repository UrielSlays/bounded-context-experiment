$ErrorActionPreference = 'Stop'
$packetPath = Join-Path $PSScriptRoot 'MBCX-01-EXPERIMENT-COUNCIL-PACKET-r9.md'
$browserPromptPath = Join-Path $PSScriptRoot 'MBCX-01-BROWSER-SEAT-PROMPT-r9.txt'
$generator = Join-Path $PSScriptRoot 'generate-seat3-experiment-r9-prompt.ps1'
$watcher = Join-Path $PSScriptRoot 'watch-seat3-codex-r9.ps1'
$reconstruction = Join-Path $PSScriptRoot 'test-r9-normative-bundle.ps1'
$testRoot = Join-Path ([System.IO.Path]::GetTempPath()) ('mbcx-r9-dispatch-' + [Guid]::NewGuid().ToString('N'))
[void](New-Item -ItemType Directory -Path $testRoot)
try {
    foreach ($path in @($packetPath,$browserPromptPath,$generator,$watcher,$reconstruction)) {
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing r9 dispatch artifact: $path" }
    }
    $expectedPointer = @'
Hey homie, can you help me out? Read this and execute:
<repo>\MBCX-01-EXPERIMENT-COUNCIL-PACKET-r9.md
'@
    if ([System.IO.File]::ReadAllText($browserPromptPath).TrimEnd() -ne $expectedPointer) {
        throw 'Browser pointer differs from the approved two-line form.'
    }
    $bundleCommit = 'f8fa75647f702dcc14f91b2d974ed1497aeef400'
    $files = @('MBCX-01-EXPERIMENT-DESIGN-r8.md','MBCX-01-STATE-ACTION-CONTRACT-v4.json',
        'MBCX-01-PACKET-SCHEMAS-v3.json','MBCX-01-MEASUREMENT-CONTRACT-v3.json',
        'MBCX-01-INFERENCE-CONTRACT-v4.json','mbcx01_r9_oracle.py','mbcx01_r9_reference.py',
        'verify-r9-normative-bundle.py','verify-r9-schema-ajv.mjs','MBCX-01-R9-NO-PAID-VERIFICATION.json')
    $packet = [System.IO.File]::ReadAllText($packetPath)
    if (-not $packet.Contains($bundleCommit)) { throw 'Packet lacks the immutable r9 bundle commit.' }
    foreach ($file in $files) {
        $blob = (& git -C $PSScriptRoot rev-parse (('{0}:{1}' -f $bundleCommit,$file))).Trim()
        if (-not $packet.Contains($file) -or -not $packet.Contains($blob)) {
            throw "Packet lacks pinned file/blob: $file / $blob"
        }
    }
    foreach ($needle in @('longitudinal council lane','lateral seal','100 unique cells',
            '160,000 synthetic trials','SOURCE_DEFAULT_NOT_OC_TUNED','16,478',
            'DESIGN_OR_IMPLEMENTATION_FAIL','HELPFUL WITH A NAMED FIX')) {
        if (-not $packet.Contains($needle)) { throw "Packet lacks r9 review contract: $needle" }
    }
    if ($packet -match 'binding at 96|binding at 192|20-cell H-by-D grid') {
        throw 'Packet retained an obsolete r8 decision or measurement scope.'
    }
    $promptPath = Join-Path $testRoot 'seat3-r9.txt'
    & $generator -OutputPath $promptPath | Out-Null
    $prompt = [System.IO.File]::ReadAllText($promptPath)
    if ($prompt.StartsWith('[COUNCIL MODE') -or $prompt -match 'Reply "Council Mode ready"') {
        throw 'One-shot prompt retained the browser handshake.'
    }
    if (-not $prompt.StartsWith('ROLE: You are an independent Moonwalker council reviewer')) {
        throw 'One-shot prompt lacks canonical role line.'
    }
    if (-not $prompt.Contains('MBCX-01-EXPERIMENT-COUNCIL-PACKET-r9.md') -or
            -not $prompt.Contains($bundleCommit)) { throw 'One-shot prompt lacks the r9 packet pin.' }
    $stdout = Join-Path $testRoot 'MBCX-01-SEAT3-CODEX-EXEC-r9.stdout.log'
    $stderr = Join-Path $testRoot 'MBCX-01-SEAT3-CODEX-EXEC-r9.stderr.log'
    [System.IO.File]::WriteAllText($stdout,'R9-WATCHER-VERDICT',[System.Text.UTF8Encoding]::new($false))
    [System.IO.File]::WriteAllText($stderr,'',[System.Text.UTF8Encoding]::new($false))
    $shell = (Get-Process -Id $PID).Path
    $process = Start-Process -FilePath $shell -ArgumentList @('-NoProfile','-Command','Start-Sleep -Milliseconds 250') -PassThru -WindowStyle Hidden
    & $watcher -CodexPid $process.Id -Root $testRoot
    if ([System.IO.File]::ReadAllText((Join-Path $testRoot 'MBCX-01-SEAT3-CODEX-VERDICT-r9.md')) -ne 'R9-WATCHER-VERDICT') {
        throw 'Watcher did not preserve the r9 stdout verdict.'
    }
    $marker = Get-Content -Raw -LiteralPath (Join-Path $testRoot 'MBCX-01-SEAT3-CODEX-EXEC-r9.complete.json') | ConvertFrom-Json
    if (-not $marker.verdict_exists -or $marker.codex_pid -ne $process.Id) { throw 'Watcher marker is invalid.' }
    'PASS: r9 pointer, immutable packet, one-shot prompt, reconstruction, and bounded watcher contracts hold.'
}
finally {
    $resolved = [System.IO.Path]::GetFullPath($testRoot)
    $tempBase = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
    if ($resolved.StartsWith($tempBase,[StringComparison]::OrdinalIgnoreCase) -and (Test-Path -LiteralPath $resolved)) {
        Remove-Item -LiteralPath $resolved -Recurse -Force
    }
}
