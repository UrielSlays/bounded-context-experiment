$ErrorActionPreference = 'Stop'
$packet = Join-Path $PSScriptRoot 'MBCX-01-EXPERIMENT-COUNCIL-PACKET-r10.md'
$browserPrompt = Join-Path $PSScriptRoot 'MBCX-01-BROWSER-SEAT-PROMPT-r10.txt'
$generator = Join-Path $PSScriptRoot 'generate-seat3-experiment-r10-prompt.ps1'
$watcher = Join-Path $PSScriptRoot 'watch-seat3-codex-r10.ps1'
foreach ($path in @($packet,$browserPrompt,$generator,$watcher)) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing r10 dispatch artifact: $path" }
}
$packetText = [System.IO.File]::ReadAllText($packet)
foreach ($needle in @('efaa1bbff91b887597b711ff4936109e79ccfddd','12589dbf0cc48704ae758d00fff1d9b0d16e2c01',
        '456 trials','2,736','exact conservative DP hull','Windows Job Object','lateral seal')) {
    if (-not $packetText.Contains($needle)) { throw "Packet lacks review contract: $needle" }
}
$expected = "Hey homie, can you help me out? Read this and execute:`n<repo>\MBCX-01-EXPERIMENT-COUNCIL-PACKET-r10.md"
$actual = [System.IO.File]::ReadAllText($browserPrompt).Replace("`r`n","`n").TrimEnd()
if ($actual -ne $expected) { throw 'Browser pointer mismatch.' }
$temporary = Join-Path ([System.IO.Path]::GetTempPath()) ('mbcx-r10-dispatch-' + [Guid]::NewGuid().ToString('N'))
[void](New-Item -ItemType Directory -Path $temporary)
try {
    $promptPath = Join-Path $temporary 'seat3-r10.txt'
    & $generator -OutputPath $promptPath | Out-Null
    $prompt = [System.IO.File]::ReadAllText($promptPath)
    if ($prompt.StartsWith('[COUNCIL MODE') -or $prompt -match 'Council Mode ready') { throw 'One-shot prompt retained handshake.' }
    if (-not $prompt.Contains('MBCX-01-EXPERIMENT-COUNCIL-PACKET-r10.md') -or
            -not $prompt.Contains('12589dbf0cc48704ae758d00fff1d9b0d16e2c01')) { throw 'One-shot prompt lacks pins.' }
    $stdout = Join-Path $temporary 'MBCX-01-SEAT3-CODEX-EXEC-r10.stdout.log'
    [System.IO.File]::WriteAllText($stdout,'R10-WATCHER-VERDICT',[System.Text.UTF8Encoding]::new($false))
    $shell = (Get-Process -Id $PID).Path
    $process = Start-Process -FilePath $shell -ArgumentList @('-NoProfile','-Command','Start-Sleep -Milliseconds 100') -PassThru -WindowStyle Hidden
    & $watcher -CodexPid $process.Id -Root $temporary
    if ([System.IO.File]::ReadAllText((Join-Path $temporary 'MBCX-01-SEAT3-CODEX-VERDICT-r10.md')) -ne 'R10-WATCHER-VERDICT') {
        throw 'Watcher failed.'
    }
    'PASS: r10 browser pointer, immutable packet, one-shot prompt, and watcher contracts hold.'
}
finally {
    $resolved = [System.IO.Path]::GetFullPath($temporary)
    $base = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
    if ($resolved.StartsWith($base,[StringComparison]::OrdinalIgnoreCase) -and (Test-Path -LiteralPath $resolved)) {
        Remove-Item -LiteralPath $resolved -Recurse -Force
    }
}
