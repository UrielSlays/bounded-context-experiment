[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$packet = [IO.File]::ReadAllText((Join-Path $root 'MBCX-01-TARGETED-CLOSURE-CONFIRMATION-PACKET-r13.2.md'))
$browser = [IO.File]::ReadAllText((Join-Path $root 'MBCX-01-BROWSER-SEAT-PROMPT-r13.2.txt'))
$codex = [IO.File]::ReadAllText((Join-Path $root 'MBCX-01-SEAT3-CODEX-EXEC-PROMPT-r13.2.txt'))
$commit = 'd97d654e21918450994cfddb5a53dc5da2e962bb'
$manifestBlob = '407a1cd73197af7dbad767976f5c077d91986c87'
$launcherBlob = '1bb8c15d1fd14303fa0a10fa615a881cb65e0d96'
foreach ($pin in ($commit,$manifestBlob,$launcherBlob)) {
    if (-not $packet.Contains($pin)) { throw "packet missing pin $pin" }
}
if (-not $browser.Contains('MBCX-01-TARGETED-CLOSURE-CONFIRMATION-PACKET-r13.2.md')) { throw 'browser pointer mismatch' }
$browserTrimmed = $browser.Trim()
if ($browserTrimmed.Contains("`n") -or $browserTrimmed.Contains("`r")) { throw 'browser prompt must remain one line' }
if (-not $codex.Contains('strict lateral seal') -or -not $codex.Contains('Do not edit files')) { throw 'Codex seal/read-only instruction missing' }
$manifest = Get-Content -LiteralPath (Join-Path $root 'MBCX-01-R13-PIN-MANIFEST.json') -Raw | ConvertFrom-Json
if ($manifest.governing_commit -ne $commit -or $manifest.subjects.Count -ne 34) { throw 'pin manifest mismatch' }
foreach ($needle in @('ScenarioOutcomeReceiptV2','six ordered','TotalTerminatedProcesses','Job limit violation','CarrierExactnessReceiptV2','candidate_artifact_digest','measurement_grid_identity_hash','CARRIER_EXACTNESS_AUTHORITY_UNAVAILABLE','STATE_AUTHORITY_UNAVAILABLE','PHYSICAL_HARNESS_UNAVAILABLE','CONFIRMED')) {
    if (-not $packet.Contains($needle)) { throw "packet missing focused surface: $needle" }
}
'R13_2_TARGETED_CONFIRMATION_PACKET_READY'
