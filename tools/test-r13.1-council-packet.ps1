[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$packet = [IO.File]::ReadAllText((Join-Path $root 'MBCX-01-FOCUSED-CLOSURE-COUNCIL-PACKET-r13.1.md'))
$browser = [IO.File]::ReadAllText((Join-Path $root 'MBCX-01-BROWSER-SEAT-PROMPT-r13.1.txt'))
$codex = [IO.File]::ReadAllText((Join-Path $root 'MBCX-01-SEAT3-CODEX-EXEC-PROMPT-r13.1.txt'))
$commit = 'd9b054f9617bbeba2b55fa488736adf808f19457'
$manifestBlob = 'e5d6e8f07d1602dac16f0d7df5e8c4ab1ecda4e4'
$launcherBlob = 'e22013a7be82c3e8899b9b0360e1215819859669'
foreach ($pin in ($commit,$manifestBlob,$launcherBlob)) {
    if (-not $packet.Contains($pin)) { throw "packet missing pin $pin" }
}
if (-not $browser.Contains('MBCX-01-FOCUSED-CLOSURE-COUNCIL-PACKET-r13.1.md')) { throw 'browser pointer mismatch' }
if (-not $codex.Contains('strict lateral seal') -or -not $codex.Contains('Do not edit files')) { throw 'Codex seal/read-only instruction missing' }
$manifest = Get-Content -LiteralPath (Join-Path $root 'MBCX-01-R13-PIN-MANIFEST.json') -Raw | ConvertFrom-Json
if ($manifest.governing_commit -ne $commit -or $manifest.subjects.Count -ne 33) { throw 'pin manifest mismatch' }
foreach ($needle in @('RetainedScenarioAuthorityV2','ManifestCutStateReceiptV1','ScenarioOutcomeReceiptV1','NOT_LAUNCHED_UPSTREAM_TERMINAL','4 × DWORD','GRID_IDENTITY','EngineeringCandidateEvidenceV1','STATE_AUTHORITY_UNAVAILABLE','PHYSICAL_HARNESS_UNAVAILABLE')) {
    if (-not $packet.Contains($needle)) { throw "packet missing focused surface: $needle" }
}
'R13_1_FOCUSED_COUNCIL_PACKET_READY'
