[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Commit,
    [string]$OutputPath
)

$ErrorActionPreference = 'Stop'
if (-not $OutputPath) { $OutputPath = Join-Path $PSScriptRoot 'MBCX-01-R11-PIN-MANIFEST.json' }
if ($Commit -notmatch '^[0-9a-fA-F]{40}$') { throw 'Commit must be an exact 40-hex Git object ID.' }
$repoRoot = (git -C $PSScriptRoot rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0 -or -not $repoRoot) { throw 'Unable to resolve repository root.' }

$subjects = @(
    'MBCX-01-EXPERIMENT-DESIGN-r9.md',
    'MBCX-01-COUNCIL-R10-SYNTHESIS-AND-DISPOSITION.md',
    'MBCX-01-R11-ARCHITECTURE-SPEC.md',
    'MBCX-01-R11-PRIOR-ART-MEMO.md',
    'MBCX-01-R11-IMPLEMENTATION-PLAN.md',
    'MBCX-01-R11-PHYSICAL-HARNESS-REQUIREMENTS.md',
    'MBCX-01-R11-SYNTHETIC-COHORT-GENERATOR.json',
    'MBCX-01-STATE-ACTION-CONTRACT-v6.json',
    'MBCX-01-PACKET-SCHEMAS-v5.json',
    'MBCX-01-MEASUREMENT-CONTRACT-v5.json',
    'MBCX-01-INFERENCE-CONTRACT-v6.json',
    'MBCX-01-R11-REPAIR-LEDGER.json',
    'MBCX-01-R11-NO-PAID-VERIFICATION.json',
    'mbcx01_r11_common.py',
    'mbcx01_r11_state_reference.py',
    'mbcx01_r11_state_oracle.py',
    'mbcx01_r11_packets.py',
    'mbcx01_r11_measurement.py',
    'mbcx01_r11_inference.py',
    'mbcx01_r11_integration.py',
    'test_mbcx01_r11.py',
    'test_mbcx01_r11_packets.py',
    'test_mbcx01_r11_measurement.py',
    'test_mbcx01_r11_inference.py',
    'test_mbcx01_r11_integration.py',
    'verify-r11-normative-bundle.py',
    'verify-r11-schema-ajv.mjs',
    'vendor/ajv-r11-entry.cjs',
    'vendor/ajv-r11.bundle.cjs',
    'verify-r11-pinned.ps1',
    'test-r11-normative-bundle.ps1'
)

$tempBase = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
$tempDir = Join-Path $tempBase ('mbcx01-r11-pin-' + [guid]::NewGuid().ToString('N'))
[System.IO.Directory]::CreateDirectory($tempDir) | Out-Null
try {
    $rows = foreach ($path in $subjects) {
        $blob = (git -C $repoRoot rev-parse "$Commit`:$path").Trim()
        if ($LASTEXITCODE -ne 0 -or $blob -notmatch '^[0-9a-f]{40}$') {
            throw "Unable to resolve governed subject: $path"
        }
        $tempFile = Join-Path $tempDir ([guid]::NewGuid().ToString('N'))
        $process = Start-Process -FilePath 'git' -ArgumentList @('-C', $repoRoot, 'cat-file', 'blob', $blob) -RedirectStandardOutput $tempFile -PassThru -Wait -WindowStyle Hidden
        if ($process.ExitCode -ne 0) { throw "Unable to extract governed subject: $path" }
        $bytes = [System.IO.File]::ReadAllBytes($tempFile)
        $lfCount = ($bytes | Where-Object { $_ -eq 10 }).Count
        [ordered]@{
            path = $path
            bytes = $bytes.Length
            lines = if ($bytes.Length -eq 0) { 0 } elseif ($bytes[-1] -eq 10) { $lfCount } else { $lfCount + 1 }
            lf_count = $lfCount
            sha384 = (Get-FileHash -LiteralPath $tempFile -Algorithm SHA384).Hash
            git_blob = $blob
        }
    }
    $manifest = [ordered]@{
        manifest_id = 'MBCX-01-R11-PIN-MANIFEST'
        created_at = '2026-08-13T00:00:00.000000Z'
        normative = $true
        governing_commit = $Commit.ToLowerInvariant()
        hash_algorithm = 'SHA-384'
        git_object_algorithm = 'SHA-1 as configured by this repository'
        governing_commit_binding = 'Every subject resolves as governing_commit:path and must match git_blob, bytes, LF count and SHA-384 before import or execution.'
        manifest_self_binding = 'The council packet pins this file by Git blob; this manifest does not self-hash.'
        paid_calls = 0
        experiment_evidence = $false
        subjects = @($rows)
    }
    [System.IO.File]::WriteAllText(
        $OutputPath,
        (($manifest | ConvertTo-Json -Depth 8) + [Environment]::NewLine),
        [System.Text.UTF8Encoding]::new($false))
    [pscustomobject]@{Path=$OutputPath;Subjects=$rows.Count;Bytes=(Get-Item -LiteralPath $OutputPath).Length}
}
finally {
    $resolved = [System.IO.Path]::GetFullPath($tempDir)
    if (-not $resolved.StartsWith($tempBase, [System.StringComparison]::OrdinalIgnoreCase) -or -not ([System.IO.Path]::GetFileName($resolved)).StartsWith('mbcx01-r11-pin-')) {
        throw 'Refusing cleanup outside validated temporary pin directory.'
    }
    if (Test-Path -LiteralPath $resolved) { Remove-Item -LiteralPath $resolved -Recurse -Force }
}
