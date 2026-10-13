[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $scriptRoot
try {
    python verify-r13-normative-bundle.py
    if ($LASTEXITCODE -ne 0) { throw "r13 normative verifier failed with exit $LASTEXITCODE" }
}
finally {
    Pop-Location
}
