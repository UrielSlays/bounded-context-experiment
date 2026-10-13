[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $scriptRoot
try {
    python verify-r11-normative-bundle.py --write-report
    if ($LASTEXITCODE -ne 0) { throw "r11 normative verifier failed with exit $LASTEXITCODE" }
}
finally {
    Pop-Location
}
