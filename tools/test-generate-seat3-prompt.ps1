$ErrorActionPreference = 'Stop'

$generator = Join-Path $PSScriptRoot 'generate-seat3-prompt.ps1'
$output = Join-Path $PSScriptRoot '.seat3-prompt-test-output.txt'

try {
    & $generator -OutputPath $output | Out-Null
    $text = [System.IO.File]::ReadAllText($output)

    if ($text.StartsWith('[COUNCIL MODE')) {
        throw 'One-shot prompt retained the browser-only handshake header.'
    }
    if ($text -match 'Reply "Council Mode ready"') {
        throw 'One-shot prompt retained the browser-only acknowledgement request.'
    }
    if (-not $text.StartsWith('ROLE: You are an independent Moonwalker council reviewer')) {
        throw 'One-shot prompt does not begin with the canonical ROLE line.'
    }
    if ($text -notmatch [regex]::Escape('MBCX-01-DESIGN-COUNCIL-PACKET-r1.md')) {
        throw 'One-shot prompt is missing the pinned packet pointer.'
    }
    if ($text -notmatch 'WHAT WOULD YOU BUILD\?') {
        throw 'One-shot prompt is missing the design proposal contract.'
    }

    'PASS: seat-3 prompt generator preserves the canonical one-shot contract.'
}
finally {
    if (Test-Path -LiteralPath $output) {
        Remove-Item -LiteralPath $output -Force
    }
}
