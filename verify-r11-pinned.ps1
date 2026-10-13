[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Commit,
    [Parameter(Mandatory = $true)][string]$ManifestBlob
)

$ErrorActionPreference = 'Stop'
if ($Commit -notmatch '^[0-9a-fA-F]{40}$' -or $ManifestBlob -notmatch '^[0-9a-fA-F]{40}$') {
    throw 'Commit and ManifestBlob must be exact 40-hex Git object IDs.'
}

$repoRoot = (git rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0 -or -not $repoRoot) { throw 'Not inside the governing Git repository.' }
$tempBase = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
$reconstruction = Join-Path $tempBase ("mbcx01-r11-" + [guid]::NewGuid().ToString('N'))
[System.IO.Directory]::CreateDirectory($reconstruction) | Out-Null
$requiredSubjects = @(
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

function Export-GitBlob([string]$ObjectSpec, [string]$Destination) {
    $parent = Split-Path -Parent $Destination
    [System.IO.Directory]::CreateDirectory($parent) | Out-Null
    $process = Start-Process -FilePath 'git' -ArgumentList @('-C', $repoRoot, 'cat-file', 'blob', $ObjectSpec) -RedirectStandardOutput $Destination -PassThru -Wait -WindowStyle Hidden
    if ($process.ExitCode -ne 0) { throw "Unable to extract Git blob $ObjectSpec" }
}

try {
    $manifestPath = Join-Path $reconstruction 'MBCX-01-R11-PIN-MANIFEST.json'
    Export-GitBlob $ManifestBlob $manifestPath
    $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
    if ($manifest.manifest_id -ne 'MBCX-01-R11-PIN-MANIFEST' -or $manifest.governing_commit -ne $Commit.ToLowerInvariant() -or
        $manifest.paid_calls -ne 0 -or $manifest.experiment_evidence -ne $false) {
        throw 'Pinned manifest identity or governing commit mismatch.'
    }
    $manifestPaths = @($manifest.subjects | ForEach-Object { [string]$_.path })
    if ($manifestPaths.Count -ne ($manifestPaths | Select-Object -Unique).Count -or
        (Compare-Object ($requiredSubjects | Sort-Object) ($manifestPaths | Sort-Object))) {
        throw 'Pinned manifest subject set is incomplete, duplicated, or unexpected.'
    }
    foreach ($subject in $manifest.subjects) {
        $relative = [string]$subject.path
        if ([System.IO.Path]::IsPathRooted($relative) -or $relative -match '(^|[\\/])\.\.([\\/]|$)') {
            throw "Unsafe subject path: $relative"
        }
        $actualBlob = (git -C $repoRoot rev-parse "$Commit`:$relative").Trim()
        if ($LASTEXITCODE -ne 0 -or $actualBlob -ne [string]$subject.git_blob) {
            throw "Subject Git blob mismatch: $relative"
        }
        $destination = Join-Path $reconstruction $relative
        Export-GitBlob ("$Commit`:$relative") $destination
        $bytes = [System.IO.File]::ReadAllBytes($destination)
        $sha384 = (Get-FileHash -LiteralPath $destination -Algorithm SHA384).Hash
        $lfCount = ($bytes | Where-Object { $_ -eq 10 }).Count
        $lineCount = if ($bytes.Length -eq 0) { 0 } elseif ($bytes[-1] -eq 10) { $lfCount } else { $lfCount + 1 }
        if ($sha384 -ne $subject.sha384 -or $bytes.Length -ne $subject.bytes -or
            $lfCount -ne $subject.lf_count -or $lineCount -ne $subject.lines) {
            throw "Subject pin mismatch: $relative"
        }
    }
    & (Join-Path $reconstruction 'test-r11-normative-bundle.ps1')
    if ($LASTEXITCODE -ne 0) { throw "Reconstructed r11 verifier failed with exit $LASTEXITCODE" }
}
finally {
    $resolved = [System.IO.Path]::GetFullPath($reconstruction)
    if (-not $resolved.StartsWith($tempBase, [System.StringComparison]::OrdinalIgnoreCase) -or -not ([System.IO.Path]::GetFileName($resolved)).StartsWith('mbcx01-r11-')) {
        throw 'Refusing cleanup outside the validated temporary reconstruction path.'
    }
    if (Test-Path -LiteralPath $resolved) { Remove-Item -LiteralPath $resolved -Recurse -Force }
}
