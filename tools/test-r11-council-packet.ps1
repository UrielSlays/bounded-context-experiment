[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$packetPath = Join-Path $root 'MBCX-01-EXPERIMENT-COUNCIL-PACKET-r11.md'
$browserPath = Join-Path $root 'MBCX-01-BROWSER-SEAT-PROMPT-r11.txt'
$codexPath = Join-Path $root 'MBCX-01-SEAT3-CODEX-EXEC-PROMPT-r11.txt'
$packet = [System.IO.File]::ReadAllText($packetPath)
$browser = [System.IO.File]::ReadAllText($browserPath)
$codex = [System.IO.File]::ReadAllText($codexPath)

$commit = 'b56e450f8553b96f6121cb045b62eb604e4a0655'
$manifestBlob = '269dbb3fd905c3875616ac70434e333bcede0a1b'
$launcherBlob = 'dca3d7951aeba3947af18978b88cc48028c1b572'
foreach ($pin in ($commit,$manifestBlob,$launcherBlob)) {
    if (-not $packet.Contains($pin) -or -not $codex.Contains($pin)) { throw "missing packet/prompt pin $pin" }
}
if ($browser.TrimEnd() -ne "Hey homie, can you help me out? Read this and execute:`n<repo>\MBCX-01-EXPERIMENT-COUNCIL-PACKET-r11.md") {
    throw 'browser prompt is not the exact packet pointer'
}
$repo = (git -C $root rev-parse --show-toplevel).Trim()
if ((git -C $repo rev-parse "$commit`:verify-r11-pinned.ps1").Trim() -ne $launcherBlob) {
    throw 'launcher blob does not resolve from governing commit'
}
$manifest = git -C $repo cat-file blob $manifestBlob | ConvertFrom-Json
if ($manifest.manifest_id -ne 'MBCX-01-R11-PIN-MANIFEST' -or $manifest.governing_commit -ne $commit -or $manifest.subjects.Count -ne 31) {
    throw 'manifest identity, governing commit or subject total mismatch'
}
if (-not $packet.Contains('PHYSICAL_HARNESS_UNAVAILABLE') -or -not $packet.Contains('paid/model/provider calls remain forbidden')) {
    throw 'packet lost its physical/cost stop boundary'
}
$forbidden = @(
    'MBCX-01-SEAT1-OUTSIDE-OPUS5-VERDICT-r11.md',
    'MBCX-01-SEAT2-CHATGPT-SOL-VERDICT-r11.md',
    'MBCX-01-SEAT3-CODEX-VERDICT-r11.md',
    'MBCX-01-COUNCIL-R11-DISPATCH-RECEIPT.json'
)
foreach ($name in $forbidden) {
    if (Test-Path -LiteralPath (Join-Path $root $name)) { throw "r11 was already dispatched or banked: $name" }
}
if (-not $codex.Contains('Remain sealed from both browser seats')) { throw 'Codex lateral seal missing' }
'R11_COUNCIL_PACKET_READY_NOT_DISPATCHED'
