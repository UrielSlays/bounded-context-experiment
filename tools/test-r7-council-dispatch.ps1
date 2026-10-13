$ErrorActionPreference = 'Stop'

$packetPath = Join-Path $PSScriptRoot 'MBCX-01-EXPERIMENT-COUNCIL-PACKET-r7.md'
$browserPromptPath = Join-Path $PSScriptRoot 'MBCX-01-BROWSER-SEAT-PROMPT-r7.txt'
$generator = Join-Path $PSScriptRoot 'generate-seat3-experiment-r7-prompt.ps1'
$watcher = Join-Path $PSScriptRoot 'watch-seat3-codex-r7.ps1'
$testRoot = Join-Path ([System.IO.Path]::GetTempPath()) ('mbcx-r7-dispatch-' + [Guid]::NewGuid().ToString('N'))
[void](New-Item -ItemType Directory -Path $testRoot)

try {
    foreach ($path in @($packetPath, $browserPromptPath, $generator, $watcher)) {
        if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing r7 dispatch artifact: $path" }
    }
    $expectedPointer = @'
Hey homie, can you help me out? Read this and execute:
<repo>\MBCX-01-EXPERIMENT-COUNCIL-PACKET-r7.md
'@
    $actualPointer = [System.IO.File]::ReadAllText($browserPromptPath).TrimEnd()
    if ($actualPointer -ne $expectedPointer) { throw 'Browser pointer differs from the owner-approved two-line form.' }

    $bundleCommit = '6cf58b4ad123cb7487faae5499e623d316a06d47'
    $files = @(
        'MBCX-01-EXPERIMENT-DESIGN-r6.md',
        'MBCX-01-STATE-ACTION-CONTRACT-v2.json',
        'MBCX-01-PACKET-SCHEMAS-v1.json',
        'MBCX-01-MEASUREMENT-CONTRACT-v1.json',
        'MBCX-01-INFERENCE-CONTRACT-v2.json'
    )
    $packet = [System.IO.File]::ReadAllText($packetPath)
    if (-not $packet.Contains($bundleCommit)) { throw 'Packet is missing the immutable bundle commit.' }
    foreach ($file in $files) {
        $spec = '{0}:{1}' -f $bundleCommit, $file
        $blob = (& git -C $PSScriptRoot rev-parse $spec).Trim()
        if (-not $packet.Contains($file) -or -not $packet.Contains($blob)) {
            throw "Packet is missing pinned file/blob: $file / $blob"
        }
    }
    foreach ($needle in @('longitudinal council lane', 'lateral seal', 'fourteen red witnesses', 'three-look bounded-martingale Hoeffding intervals')) {
        if (-not $packet.Contains($needle)) { throw "Packet is missing r7 review contract: $needle" }
    }
    if ($packet -match 'genuinely fresh.*browser|fresh replacement seat') { throw 'Packet retained the obsolete fresh browser-seat rule.' }

    $promptPath = Join-Path $testRoot 'seat3-r7.txt'
    & $generator -OutputPath $promptPath | Out-Null
    $prompt = [System.IO.File]::ReadAllText($promptPath)
    if ($prompt.StartsWith('[COUNCIL MODE')) { throw 'One-shot prompt retained browser handshake header.' }
    if ($prompt -match 'Reply "Council Mode ready"') { throw 'One-shot prompt retained browser acknowledgement.' }
    if (-not $prompt.StartsWith('ROLE: You are an independent Moonwalker council reviewer')) { throw 'One-shot prompt lacks canonical role line.' }
    if (-not $prompt.Contains('MBCX-01-EXPERIMENT-COUNCIL-PACKET-r7.md')) { throw 'One-shot prompt lacks r7 packet pointer.' }
    if (-not $prompt.Contains($bundleCommit)) { throw 'One-shot prompt lacks r7 bundle pin.' }

    $stdout = Join-Path $testRoot 'MBCX-01-SEAT3-CODEX-EXEC-r7.stdout.log'
    $stderr = Join-Path $testRoot 'MBCX-01-SEAT3-CODEX-EXEC-r7.stderr.log'
    [System.IO.File]::WriteAllText($stdout, 'R7-WATCHER-VERDICT', [System.Text.UTF8Encoding]::new($false))
    [System.IO.File]::WriteAllText($stderr, '', [System.Text.UTF8Encoding]::new($false))
    $shell = (Get-Process -Id $PID).Path
    $process = Start-Process -FilePath $shell -ArgumentList @('-NoProfile','-Command','Start-Sleep -Milliseconds 250') -PassThru -WindowStyle Hidden
    & $watcher -CodexPid $process.Id -Root $testRoot
    if ([System.IO.File]::ReadAllText((Join-Path $testRoot 'MBCX-01-SEAT3-CODEX-VERDICT-r7.md')) -ne 'R7-WATCHER-VERDICT') {
        throw 'Watcher did not preserve stdout verdict.'
    }
    $marker = Get-Content -LiteralPath (Join-Path $testRoot 'MBCX-01-SEAT3-CODEX-EXEC-r7.complete.json') -Raw | ConvertFrom-Json
    if (-not $marker.verdict_exists -or $marker.codex_pid -ne $process.Id) { throw 'Watcher completion marker is invalid.' }
    'PASS: r7 pointer, immutable packet, one-shot prompt, and bounded watcher contracts hold.'
}
finally {
    $resolved = [System.IO.Path]::GetFullPath($testRoot)
    $tempBase = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
    if ($resolved.StartsWith($tempBase, [StringComparison]::OrdinalIgnoreCase) -and (Test-Path -LiteralPath $resolved)) {
        Remove-Item -LiteralPath $resolved -Recurse -Force
    }
}
