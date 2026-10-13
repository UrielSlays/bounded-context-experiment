[CmdletBinding(DefaultParameterSetName = 'Pinned')]
param(
    [Parameter(Mandatory = $true, ParameterSetName = 'Pinned')][string]$Commit,
    [Parameter(Mandatory = $true, ParameterSetName = 'Pinned')][string]$ManifestBlob,
    [Parameter(Mandatory = $true, ParameterSetName = 'WorkingTree')][switch]$WorkingTree,
    [string]$ReportPath
)

# Clean-room launcher for the MBCX-01 production BUILD lane. Mirrors verify-r13-pinned.ps1.
#
#   -Commit/-ManifestBlob  PINNED mode. The launcher authenticates ITSELF by Git blob
#                          (the manifest is exported from the object store, never read
#                          from the working tree), reconstructs every pinned subject and
#                          frozen dependency from commit:path into a temporary
#                          directory, verifies git_blob / bytes / LF count / SHA-384 for
#                          each, and only then runs verify-build-bundle.py INSIDE the
#                          reconstruction.
#   -WorkingTree           PROOF mode for a lane whose commit does not exist yet. It
#                          runs the same verifier and the same schema/parity checks
#                          directly against this working tree and states plainly, in its
#                          own output, that no pin was authenticated. It is NOT a
#                          substitute for the pinned run and never claims to be.
#
# The generated report (MBCX-01-BUILD-VERIFICATION-REPORT.json) is a runtime output in
# both modes: it is written where -ReportPath says, never into the repository by default.

$ErrorActionPreference = 'Stop'
$python = if ($env:MBCX01_PYTHON) { $env:MBCX01_PYTHON } else { 'python' }

if ($PSCmdlet.ParameterSetName -eq 'WorkingTree') {
    Write-Output 'MODE: WORKING-TREE PROOF (no pin authenticated, no reconstruction performed)'
    $repoRoot = $PSScriptRoot
    $report = if ($ReportPath) { $ReportPath } else { Join-Path ([System.IO.Path]::GetTempPath()) ('MBCX-01-BUILD-VERIFICATION-REPORT-' + [guid]::NewGuid().ToString('N') + '.json') }
    & node (Join-Path $repoRoot 'verify-build-schema-ajv.mjs') --compile-only
    if ($LASTEXITCODE -ne 0) { throw "Strict schema compilation failed with exit $LASTEXITCODE" }
    & node (Join-Path $repoRoot 'verify-build-schema-ajv.mjs')
    if ($LASTEXITCODE -ne 0) { throw "Schema fixture/mutant validation failed with exit $LASTEXITCODE" }
    & $python (Join-Path $repoRoot 'verify-build-bundle.py') --output-report $report
    if ($LASTEXITCODE -ne 0) { throw "verify-build-bundle.py failed with exit $LASTEXITCODE" }
    Write-Output "WORKING-TREE PROOF COMPLETE. Report: $report"
    return
}

if ($Commit -notmatch '^[0-9a-fA-F]{40}$' -or $ManifestBlob -notmatch '^[0-9a-fA-F]{40}$') { throw 'Commit and ManifestBlob must be exact 40-hex Git object IDs.' }
$repoRoot=(git rev-parse --show-toplevel).Trim()
if($LASTEXITCODE -ne 0 -or -not $repoRoot){throw 'Not inside the governing Git repository.'}
$tempBase=[System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
$reconstruction=Join-Path $tempBase ('mbcx01-build-'+[guid]::NewGuid().ToString('N'))
[System.IO.Directory]::CreateDirectory($reconstruction)|Out-Null
function ConvertTo-GitArgument([string]$Value){
    # Windows CommandLineToArgvW quoting, used only on hosts whose
    # ProcessStartInfo has no ArgumentList (Windows PowerShell 5.1, which the
    # council packets invoke): quote the value, double every backslash run that
    # precedes a quote or the closing quote, and escape embedded quotes.
    $escaped=[regex]::Replace($Value,'(\\*)"','$1$1\"')
    $escaped=[regex]::Replace($escaped,'(\\+)$','$1$1')
    return '"'+$escaped+'"'
}
function Export-GitBlob([string]$ObjectSpec,[string]$Destination){
    # Deliberately NOT Start-Process: it joins -ArgumentList into one command
    # line WITHOUT quoting, so a repository path containing a space reached git
    # as a truncated -C value and every extraction failed. Each argument is
    # handed to the process separately here.
    # Deliberately NOT `& git ... > $Destination` either: PowerShell's
    # redirection is text, and a pinned subject is judged on its exact bytes, LF
    # count and SHA-384, so stdout is copied as a RAW byte stream.
    $parent=Split-Path -Parent $Destination
    [System.IO.Directory]::CreateDirectory($parent)|Out-Null
    $info=New-Object System.Diagnostics.ProcessStartInfo
    $info.FileName='git'
    $info.UseShellExecute=$false
    $info.RedirectStandardOutput=$true
    $info.CreateNoWindow=$true
    $arguments=@('-C',$repoRoot,'cat-file','blob',$ObjectSpec)
    if($null -ne $info.PSObject.Properties['ArgumentList']){foreach($argument in $arguments){$info.ArgumentList.Add($argument)}}
    else{$info.Arguments=(($arguments|ForEach-Object{ConvertTo-GitArgument $_}) -join ' ')}
    $process=[System.Diagnostics.Process]::Start($info)
    try{
        $stream=[System.IO.File]::Create($Destination)
        try{$process.StandardOutput.BaseStream.CopyTo($stream)}finally{$stream.Dispose()}
        $process.WaitForExit()
        if($process.ExitCode-ne 0){throw "Unable to extract Git blob $ObjectSpec"}
    }
    finally{$process.Dispose()}
}
try{
    $manifestPath=Join-Path $reconstruction 'MBCX-01-BUILD-PIN-MANIFEST.json'
    Export-GitBlob $ManifestBlob $manifestPath
    $manifest=Get-Content -LiteralPath $manifestPath -Raw|ConvertFrom-Json
    if($manifest.manifest_id-ne'MBCX-01-BUILD-PIN-MANIFEST'-or $manifest.governing_commit-ne$Commit.ToLowerInvariant()-or $manifest.paid_calls-ne 0-or $manifest.experiment_executed-ne$false-or $manifest.physical_harness_executed-ne$false-or $manifest.production_activation-ne$false){throw 'Pinned manifest identity, governing commit, or no-execution facts mismatch.'}
    $allSubjects=@($manifest.subjects)+@($manifest.frozen_dependencies)
    $paths=@($allSubjects|ForEach-Object{[string]$_.path})
    if($paths.Count-ne($paths|Select-Object -Unique).Count){throw 'Pinned manifest subject set contains duplicates.'}
    if($paths -contains 'MBCX-01-BUILD-VERIFICATION-REPORT.json'){throw 'The generated verification report must never be a pinned subject.'}
    foreach($required in @('verify-build-bundle.py','MBCX-01-BUILD-REPAIR-LEDGER.json','verify-build-schema-ajv.mjs','verify-build-canonical-parity.mjs','vendor/ajv-r12.bundle.cjs')){if($paths -notcontains $required){throw "Pinned manifest is missing a required subject: $required"}}
    foreach($subject in $allSubjects){$relative=[string]$subject.path;if([System.IO.Path]::IsPathRooted($relative)-or$relative-match'(^|[\/])\.\.([\/]|$)'){throw "Unsafe subject path: $relative"};$blob=(git -C $repoRoot rev-parse "$Commit`:$relative").Trim();if($LASTEXITCODE-ne 0-or$blob-ne[string]$subject.git_blob){throw "Subject Git blob mismatch: $relative"};$destination=Join-Path $reconstruction $relative;Export-GitBlob("$Commit`:$relative")$destination;$bytes=[System.IO.File]::ReadAllBytes($destination);$lf=($bytes|Where-Object{$_-eq 10}).Count;$lines=if($bytes.Length-eq 0){0}elseif($bytes[-1]-eq 10){$lf}else{$lf+1};if((Get-FileHash -LiteralPath $destination -Algorithm SHA384).Hash-ne$subject.sha384-or$bytes.Length-ne$subject.bytes-or$lf-ne$subject.lf_count-or$lines-ne$subject.lines){throw "Subject pin mismatch: $relative"}}
    $report=if($ReportPath){$ReportPath}else{Join-Path $reconstruction 'MBCX-01-BUILD-VERIFICATION-REPORT.json'}
    & node (Join-Path $reconstruction 'verify-build-schema-ajv.mjs') --compile-only
    if($LASTEXITCODE-ne 0){throw "Reconstructed strict schema compilation failed with exit $LASTEXITCODE"}
    Push-Location $reconstruction
    try{
        & $python (Join-Path $reconstruction 'verify-build-bundle.py') --output-report $report
        if($LASTEXITCODE-ne 0){throw "Reconstructed BUILD verifier failed with exit $LASTEXITCODE"}
    }
    finally{Pop-Location}
    if($ReportPath){Write-Output "PINNED RECONSTRUCTION COMPLETE. Report: $ReportPath"}else{Write-Output 'PINNED RECONSTRUCTION COMPLETE. Report discarded with the reconstruction (pass -ReportPath to keep it).'}
}
finally{$resolved=[System.IO.Path]::GetFullPath($reconstruction);if(-not$resolved.StartsWith($tempBase,[System.StringComparison]::OrdinalIgnoreCase)-or-not([System.IO.Path]::GetFileName($resolved)).StartsWith('mbcx01-build-')){throw 'Refusing cleanup outside the validated temporary reconstruction path.'};if(Test-Path -LiteralPath $resolved){Remove-Item -LiteralPath $resolved -Recurse -Force}}
