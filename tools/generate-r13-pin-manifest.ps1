[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Commit,
    [string]$OutputPath
)

$ErrorActionPreference = 'Stop'
if (-not $OutputPath) { $OutputPath = Join-Path $PSScriptRoot 'MBCX-01-R13-PIN-MANIFEST.json' }
if ($Commit -notmatch '^[0-9a-fA-F]{40}$') { throw 'Commit must be an exact 40-hex Git object ID.' }
$repoRoot = (git -C $PSScriptRoot rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0 -or -not $repoRoot) { throw 'Unable to resolve repository root.' }

$subjects = @(
    'MBCX-01-EXPERIMENT-DESIGN-r9.md',
    'MBCX-01-COUNCIL-R12-SYNTHESIS-AND-CLOSURE-COMMISSION.md',
    'MBCX-01-R13-AUTHORITY-INVARIANT-MATRIX.md',
    'MBCX-01-R13-CLOSURE-ARCHITECTURE.md',
    'MBCX-01-R13-PRIOR-ART-AND-ENVIRONMENT-ADDENDUM.md',
    'MBCX-01-R13.1-SHELF-QUERY-LOG.md',
    'MBCX-01-R13.2-NO-PAID-VERIFICATION-REPORT.json',
    'MBCX-01-R13-PHYSICAL-HARNESS-REQUIREMENTS.md',
    'MBCX-01-R13-SYNTHETIC-COHORT-GENERATOR.json',
    'MBCX-01-R13-MEASUREMENT-TRUST-ROOTS.json',
    'MBCX-01-R13-CARRIER-EXACTNESS-SUITE.json',
    'MBCX-01-STATE-TRANSITION-CONTRACT-v8.json',
    'MBCX-01-PACKET-SCHEMAS-v7.json',
    'MBCX-01-MEASUREMENT-CONTRACT-v7.json',
    'MBCX-01-INFERENCE-CONTRACT-v8.json',
    'MBCX-01-R13-REPAIR-LEDGER.json',
    'mbcx01_r13_common.py', 'mbcx01_r13_state_reference.py', 'mbcx01_r13_state_oracle.py',
    'mbcx01_r13_packets.py', 'mbcx01_r13_measurement.py', 'mbcx01_r13_inference.py',
    'mbcx01_r13_integration.py', 'test_mbcx01_r13_state.py', 'test_mbcx01_r13_packets.py',
    'test_mbcx01_r13_measurement.py', 'test_mbcx01_r13_inference.py',
    'test_mbcx01_r13_integration.py', 'verify-r13-normative-bundle.py',
    'verify-r13-schema-ajv.mjs', 'verify-r13-receipt-signature.mjs',
    'vendor/ajv-r12.bundle.cjs', 'verify-r13-pinned.ps1', 'test-r13-normative-bundle.ps1'
)

$tempBase = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
$tempDir = Join-Path $tempBase ('mbcx01-r13-pin-' + [guid]::NewGuid().ToString('N'))
[System.IO.Directory]::CreateDirectory($tempDir) | Out-Null
try {
    $rows = foreach ($path in $subjects) {
        $blob = (git -C $repoRoot rev-parse "$Commit`:$path").Trim()
        if ($LASTEXITCODE -ne 0 -or $blob -notmatch '^[0-9a-f]{40}$') { throw "Unable to resolve: $path" }
        $tempFile = Join-Path $tempDir ([guid]::NewGuid().ToString('N'))
        $process = Start-Process -FilePath 'git' -ArgumentList @('-C', $repoRoot, 'cat-file', 'blob', $blob) -RedirectStandardOutput $tempFile -PassThru -Wait -WindowStyle Hidden
        if ($process.ExitCode -ne 0) { throw "Unable to extract: $path" }
        $bytes = [System.IO.File]::ReadAllBytes($tempFile)
        $lfCount = ($bytes | Where-Object { $_ -eq 10 }).Count
        [ordered]@{path=$path;bytes=$bytes.Length;lines=if($bytes.Length -eq 0){0}elseif($bytes[-1] -eq 10){$lfCount}else{$lfCount+1};lf_count=$lfCount;sha384=(Get-FileHash -LiteralPath $tempFile -Algorithm SHA384).Hash;git_blob=$blob}
    }
    $manifest = [ordered]@{
        manifest_id='MBCX-01-R13-PIN-MANIFEST';created_at='2026-08-13T00:00:00.000000Z';normative=$true;
        governing_commit=$Commit.ToLowerInvariant();hash_algorithm='SHA-384';git_object_algorithm='SHA-1 as configured by this repository';
        governing_commit_binding='Every subject resolves as governing_commit:path and must match git_blob, bytes, LF count and SHA-384 before import or execution.';
        manifest_self_binding='The council packet pins this file by Git blob; this manifest does not self-hash.';
        paid_calls=0;experiment_executed=$false;physical_harness_executed=$false;subjects=@($rows)
    }
    [System.IO.File]::WriteAllText($OutputPath,(($manifest | ConvertTo-Json -Depth 8)+[Environment]::NewLine),[System.Text.UTF8Encoding]::new($false))
    [pscustomobject]@{Path=$OutputPath;Subjects=$rows.Count;Bytes=(Get-Item -LiteralPath $OutputPath).Length}
}
finally {
    $resolved=[System.IO.Path]::GetFullPath($tempDir)
    if(-not $resolved.StartsWith($tempBase,[System.StringComparison]::OrdinalIgnoreCase)-or -not([System.IO.Path]::GetFileName($resolved)).StartsWith('mbcx01-r13-pin-')){throw 'Refusing cleanup outside validated temporary pin directory.'}
    if(Test-Path -LiteralPath $resolved){Remove-Item -LiteralPath $resolved -Recurse -Force}
}
