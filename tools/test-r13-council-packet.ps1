[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$packetPath = Join-Path $root 'MBCX-01-EXPERIMENT-COUNCIL-PACKET-r13.md'
$browserPath = Join-Path $root 'MBCX-01-BROWSER-SEAT-PROMPT-r13.txt'
$codexPath = Join-Path $root 'MBCX-01-SEAT3-CODEX-EXEC-PROMPT-r13.txt'
$packet = [System.IO.File]::ReadAllText($packetPath)
$browser = [System.IO.File]::ReadAllText($browserPath)
$codex = [System.IO.File]::ReadAllText($codexPath)

$commit = 'ec583834e08df77b65ca773ef6fdf525b0ee51b2'
$manifestBlob = 'd71e653d95df662097d2507299fd85ff265ed856'
$launcherBlob = 'ba046408a0a210176d6d53616a8535eb26542be4'
foreach ($pin in ($commit,$manifestBlob,$launcherBlob)) {
    if (-not $packet.Contains($pin) -or -not $codex.Contains($pin)) { throw "missing packet/prompt pin $pin" }
}
$expectedBrowser = "Hey homie, can you help me out? Read this and execute:`n<repo>\MBCX-01-EXPERIMENT-COUNCIL-PACKET-r13.md"
if ($browser.TrimEnd() -ne $expectedBrowser) { throw 'browser prompt is not the exact packet pointer' }
$repo = (git -C $root rev-parse --show-toplevel).Trim()
if ((git -C $repo rev-parse "$commit`:verify-r13-pinned.ps1").Trim() -ne $launcherBlob) {
    throw 'launcher blob does not resolve from governing commit'
}
$manifest = git -C $repo cat-file blob $manifestBlob | ConvertFrom-Json
if ($manifest.manifest_id -ne 'MBCX-01-R13-PIN-MANIFEST' -or $manifest.governing_commit -ne $commit -or $manifest.subjects.Count -ne 31) {
    throw 'manifest identity, governing commit or subject total mismatch'
}
foreach ($needle in @('STATE_AUTHORITY_UNAVAILABLE','PHYSICAL_HARNESS_UNAVAILABLE','I01–I17','attacks A–H','closure review')) {
    if (-not $packet.Contains($needle)) { throw "packet lost required boundary or review surface: $needle" }
}
$forbidden = @(
    'MBCX-01-SEAT1-OUTSIDE-OPUS5-VERDICT-r13.md',
    'MBCX-01-SEAT2-CHATGPT-SOL-VERDICT-r13.md',
    'MBCX-01-SEAT3-CODEX-VERDICT-r13.md',
    'MBCX-01-COUNCIL-R13-DISPATCH-RECEIPT.json',
    'MBCX-01-SEAT3-CODEX-EXEC-r13.complete.json'
)
foreach ($name in $forbidden) {
    if (Test-Path -LiteralPath (Join-Path $root $name)) { throw "r13 was already dispatched or banked: $name" }
}
if (-not $codex.Contains('Remain sealed from both browser seats')) { throw 'Codex lateral seal missing' }
if (-not $codex.Contains('Do not edit files')) { throw 'Codex read-only authority missing' }
'R13_COUNCIL_PACKET_READY_NOT_DISPATCHED'
