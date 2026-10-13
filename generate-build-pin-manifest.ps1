[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Commit,
    [string]$OutputPath
)

# Enumerates the BUILD subject set at one exact commit into MBCX-01-BUILD-PIN-MANIFEST.json
# with git_blob / bytes / lf_count / lines / SHA-384 per subject. Mirrors
# generate-r13-pin-manifest.ps1.
#
# Two groups are pinned, and the distinction is deliberate:
#   subjects             - the BUILD lane's own artifacts (what this lane authored);
#   frozen_dependencies  - the r13.2 subjects verify-build-bundle.py must import and run
#                          to prove the 145 frozen tests still pass. A BUILD
#                          reconstruction that omitted them could not execute the frozen
#                          suites at all, and "could not run" must never look like "passed".

$ErrorActionPreference = 'Stop'
if (-not $OutputPath) { $OutputPath = Join-Path $PSScriptRoot 'MBCX-01-BUILD-PIN-MANIFEST.json' }
if ($Commit -notmatch '^[0-9a-fA-F]{40}$') { throw 'Commit must be an exact 40-hex Git object ID.' }
$repoRoot = (git -C $PSScriptRoot rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0 -or -not $repoRoot) { throw 'Unable to resolve repository root.' }

$buildSubjects = @(
    'MBCX-01-PRODUCTION-BUILD-SENIOR-HANDOFF-r13.2.md',
    'MBCX-01-BUILD-DESIGN-NOTES.md',
    'MBCX-01-BUILD-COHORT-CONTENT-DESIGN.md',
    'MBCX-01-BUILD-EXACTNESS-PRODUCTION-VERIFIER-SPEC.md',
    'MBCX-01-BUILD-KEY-CUSTODY-CEREMONY.md',
    'MBCX-01-BUILD-SHELF-LOG.md',
    'MBCX-01-BUILD-SMOKE-RUNBOOK.md',
    'MBCX-01-BUILD-STATE-TRUST-ROOTS-V1.schema.json',
    'MBCX-01-BUILD-STATE-TRUST-ROOTS-V1.fixture.json',
    'MBCX-01-BUILD-MEASUREMENT-TRUST-ROOTS-V3.schema.json',
    'MBCX-01-BUILD-MEASUREMENT-TRUST-ROOTS-V3.fixture.json',
    'MBCX-01-BUILD-REPAIR-LEDGER.json',
    'MBCX-01-BUILD-OWNER-TRUST-ANCHOR.fixture.json',
    # 2026-08-16, cohort registration task (design MBCX-01-BUILD-COHORT-CONTENT-DESIGN.md
    # r6 FINAL section 3): the cohort slice's committed generator spec, its three
    # production siblings and its witness suite. verify-build-bundle.py's W14 level (b)
    # now cross-checks this list against its own REQUIRED set, so an artifact that lands
    # without a line here fails the bundle by name instead of going unnoticed.
    'MBCX-01-BUILD-COHORT-GENERATOR-V1.json',
    'mbcx01_build_cohort_authority.py',
    'mbcx01_build_cohort_generator.py',
    'mbcx01_build_cohort_packet.py',
    'test_mbcx01_build_cohort.py',
    'mbcx01_build_trust_anchor.py',
    'mbcx01_build_etw_consumer.py',
    'mbcx01_smoke_cell.py',
    'run-smoke-cell.ps1',
    'mbcx01_build_fixturekey_probe.py',
    'mbcx01_build_fixtureiso_probe.py',
    'mbcx01_build_ceremony_fixture.py',
    'mbcx01_build_trustboot_probe.py',
    'verify-build-receipt-signature.mjs',
    'mbcx01_build_exactness_authority.py',
    'mbcx01_build_integration.py',
    'mbcx01_build_measurement_authority.py',
    'mbcx01_build_state_adapter.py',
    'mbcx01_build_state_authority.py',
    'mbcx01_build_state_operator_b.py',
    'mbcx01_build_state_store.py',
    'mbcx01_build_win32.py',
    'mbcx01_build_windows_producer.py',
    'test_mbcx01_build_state.py',
    'test_mbcx01_build_measurement.py',
    'test_mbcx01_build_integration.py',
    'verify-build-bundle.py',
    'verify-build-schema-ajv.mjs',
    'verify-build-canonical-parity.mjs',
    'verify-build-pinned.ps1',
    'generate-build-pin-manifest.ps1'
)

$frozenDependencies = @(
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
    'vendor/ajv-r12.bundle.cjs'
)

$tempBase = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
$tempDir = Join-Path $tempBase ('mbcx01-build-pin-' + [guid]::NewGuid().ToString('N'))
[System.IO.Directory]::CreateDirectory($tempDir) | Out-Null
try {
    function ConvertTo-GitArgument([string]$Value) {
        # Windows CommandLineToArgvW quoting, used only on hosts whose
        # ProcessStartInfo has no ArgumentList (Windows PowerShell 5.1, which the
        # council packets invoke): quote the value, double every backslash run
        # that precedes a quote or the closing quote, escape embedded quotes.
        $escaped = [regex]::Replace($Value, '(\\*)"', '$1$1\"')
        $escaped = [regex]::Replace($escaped, '(\\+)$', '$1$1')
        return '"' + $escaped + '"'
    }
    function Export-GitBlob([string]$ObjectSpec, [string]$Destination) {
        # Deliberately NOT Start-Process: it joins -ArgumentList into one command
        # line WITHOUT quoting, so a repository path containing a space reached
        # git as a truncated -C value and every extraction failed. Each argument
        # is handed to the process separately here.
        # Deliberately NOT `& git ... > $Destination` either: PowerShell's
        # redirection is text, and this manifest pins exact bytes, LF count and
        # SHA-384, so stdout is copied as a RAW byte stream.
        $info = New-Object System.Diagnostics.ProcessStartInfo
        $info.FileName = 'git'
        $info.UseShellExecute = $false
        $info.RedirectStandardOutput = $true
        $info.CreateNoWindow = $true
        $arguments = @('-C', $repoRoot, 'cat-file', 'blob', $ObjectSpec)
        if ($null -ne $info.PSObject.Properties['ArgumentList']) {
            foreach ($argument in $arguments) { $info.ArgumentList.Add($argument) }
        } else {
            $info.Arguments = (($arguments | ForEach-Object { ConvertTo-GitArgument $_ }) -join ' ')
        }
        $process = [System.Diagnostics.Process]::Start($info)
        try {
            $stream = [System.IO.File]::Create($Destination)
            try { $process.StandardOutput.BaseStream.CopyTo($stream) } finally { $stream.Dispose() }
            $process.WaitForExit()
            return $process.ExitCode
        }
        finally { $process.Dispose() }
    }
    function Get-PinRow([string]$Path) {
        $blob = (git -C $repoRoot rev-parse "$Commit`:$Path").Trim()
        if ($LASTEXITCODE -ne 0 -or $blob -notmatch '^[0-9a-f]{40}$') { throw "Unable to resolve: $Path" }
        $tempFile = Join-Path $tempDir ([guid]::NewGuid().ToString('N'))
        $exitCode = Export-GitBlob $blob $tempFile
        if ($exitCode -ne 0) { throw "Unable to extract: $Path" }
        $bytes = [System.IO.File]::ReadAllBytes($tempFile)
        $lfCount = ($bytes | Where-Object { $_ -eq 10 }).Count
        [ordered]@{path=$Path;bytes=$bytes.Length;lines=if($bytes.Length -eq 0){0}elseif($bytes[-1] -eq 10){$lfCount}else{$lfCount+1};lf_count=$lfCount;sha384=(Get-FileHash -LiteralPath $tempFile -Algorithm SHA384).Hash;git_blob=$blob}
    }
    $subjectRows = foreach ($path in $buildSubjects) { Get-PinRow $path }
    $frozenRows = foreach ($path in $frozenDependencies) { Get-PinRow $path }
    $manifest = [ordered]@{
        manifest_id='MBCX-01-BUILD-PIN-MANIFEST';created_at='2026-08-14T00:00:00.000000Z';normative=$true;
        governing_commit=$Commit.ToLowerInvariant();hash_algorithm='SHA-384';git_object_algorithm='SHA-1 as configured by this repository';
        governing_commit_binding='Every subject resolves as governing_commit:path and must match git_blob, bytes, LF count and SHA-384 before import or execution.';
        manifest_self_binding='The launcher pins this file by Git blob; this manifest does not self-hash.';
        generated_report_is_not_pinned='MBCX-01-BUILD-VERIFICATION-REPORT.json is a runtime output of verify-build-bundle.py and is deliberately absent from every subject list.';
        paid_calls=0;experiment_executed=$false;physical_harness_executed=$false;production_activation=$false;
        subjects=@($subjectRows);frozen_dependencies=@($frozenRows)
    }
    [System.IO.File]::WriteAllText($OutputPath,(($manifest | ConvertTo-Json -Depth 8)+[Environment]::NewLine),[System.Text.UTF8Encoding]::new($false))
    [pscustomobject]@{Path=$OutputPath;Subjects=$subjectRows.Count;FrozenDependencies=$frozenRows.Count;Bytes=(Get-Item -LiteralPath $OutputPath).Length}
}
finally {
    $resolved=[System.IO.Path]::GetFullPath($tempDir)
    if(-not $resolved.StartsWith($tempBase,[System.StringComparison]::OrdinalIgnoreCase)-or -not([System.IO.Path]::GetFileName($resolved)).StartsWith('mbcx01-build-pin-')){throw 'Refusing cleanup outside validated temporary pin directory.'}
    if(Test-Path -LiteralPath $resolved){Remove-Item -LiteralPath $resolved -Recurse -Force}
}
