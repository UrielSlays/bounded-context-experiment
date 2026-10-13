[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$packetPath = Join-Path $root 'MBCX-01-EXPERIMENT-COUNCIL-PACKET-r12.md'
$browserPath = Join-Path $root 'MBCX-01-BROWSER-SEAT-PROMPT-r12.txt'
$codexPath = Join-Path $root 'MBCX-01-SEAT3-CODEX-EXEC-PROMPT-r12.txt'
$packet = [System.IO.File]::ReadAllText($packetPath)
$browser = [System.IO.File]::ReadAllText($browserPath)
$codex = [System.IO.File]::ReadAllText($codexPath)

$commit = '235f37bcbf213e6700c30333d6fee6a68f0886b6'
$manifestBlob = 'bd84a65b7b85530345a82a552d7c47f9e148f1a7'
$launcherBlob = '2b575b10f3c00c7a3ac79a39e54693104443f330'
foreach ($pin in ($commit,$manifestBlob,$launcherBlob)) {
    if (-not $packet.Contains($pin) -or -not $codex.Contains($pin)) { throw "missing packet/prompt pin $pin" }
}
$expectedBrowser = "Hey homie, can you help me out? Read this and execute:`n<repo>\MBCX-01-EXPERIMENT-COUNCIL-PACKET-r12.md"
if ($browser.TrimEnd() -ne $expectedBrowser) { throw 'browser prompt is not the exact packet pointer' }
$repo = (git -C $root rev-parse --show-toplevel).Trim()
if ((git -C $repo rev-parse "$commit`:verify-r12-pinned.ps1").Trim() -ne $launcherBlob) {
    throw 'launcher blob does not resolve from governing commit'
}
$manifest = git -C $repo cat-file blob $manifestBlob | ConvertFrom-Json
if ($manifest.manifest_id -ne 'MBCX-01-R12-PIN-MANIFEST' -or $manifest.governing_commit -ne $commit -or $manifest.subjects.Count -ne 31) {
    throw 'manifest identity, governing commit or subject total mismatch'
}
foreach ($needle in @('PHYSICAL_HARNESS_UNAVAILABLE','paid/model/provider/route calls remain forbidden','C1–C12','attacks A–H')) {
    if (-not $packet.Contains($needle)) { throw "packet lost required boundary or review surface: $needle" }
}
$forbidden = @(
    'MBCX-01-SEAT1-OUTSIDE-OPUS5-VERDICT-r12.md',
    'MBCX-01-SEAT2-CHATGPT-SOL-VERDICT-r12.md',
    'MBCX-01-SEAT3-CODEX-VERDICT-r12.md',
    'MBCX-01-COUNCIL-R12-DISPATCH-RECEIPT.json',
    'MBCX-01-SEAT3-CODEX-EXEC-r12.complete.json'
)
foreach ($name in $forbidden) {
    if (Test-Path -LiteralPath (Join-Path $root $name)) { throw "r12 was already dispatched or banked: $name" }
}
if (-not $codex.Contains('Remain sealed from both browser seats')) { throw 'Codex lateral seal missing' }
if (-not $codex.Contains('Do not edit files')) { throw 'Codex read-only authority missing' }
'R12_COUNCIL_PACKET_READY_NOT_DISPATCHED'
