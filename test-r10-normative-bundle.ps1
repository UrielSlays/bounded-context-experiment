param(
    [Parameter(Mandatory = $true)][string]$Commit,
    [Parameter(Mandatory = $true)][string]$ManifestBlob
)
$ErrorActionPreference = 'Stop'
& (Join-Path $PSScriptRoot 'verify-r10-pinned.ps1') -Commit $Commit -ManifestBlob $ManifestBlob
if ($LASTEXITCODE -ne 0) { throw 'r10 pinned verification failed.' }

