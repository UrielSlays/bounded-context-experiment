param(
    [string]$Commit = 'f8fa75647f702dcc14f91b2d974ed1497aeef400'
)
$ErrorActionPreference = 'Stop'
$expected = [ordered]@{
    'MBCX-01-EXPERIMENT-DESIGN-r8.md' = @('24e2b230cc2e293cbe6bd7e6dd37100c680b9ff1',19867,180,'5A690CFB6071D67831551C38066600E62C5A5E08A45A8B8A8AD599A4C72602FBFB5D326BF7BBD70A70806510A33E7DA3')
    'MBCX-01-STATE-ACTION-CONTRACT-v4.json' = @('9efb8dbca72542db522ded09269cae332e396def',16328,173,'16B89FDFD08992D9E65143E8AED4D84402A096919A3B522AFD48B78070C5778024C80D1C2070A1ABB7CCB90155D199CD')
    'MBCX-01-PACKET-SCHEMAS-v3.json' = @('a42be28546bf213d237adf306d2e0a8758ad2d52',14674,161,'E48B690F2FFF3BDF605A1CC6D98A0CD2BF7FD7D8F78CA9B70B7A875CD2D6326C20EA15571EB9C2217F0DD59A13C0398C')
    'MBCX-01-MEASUREMENT-CONTRACT-v3.json' = @('bf9dab5500beb49b6ed3a51e90661e76dc530dec',9551,115,'A96ED13DF6C7F0F4DD63C1B1CBC6703615F922D2AC30D9ACEC6F25C9FCDD3F50B870C88920359DE339BB5EDD6A090A0D')
    'MBCX-01-INFERENCE-CONTRACT-v4.json' = @('6d649433d5e36db3a81c3ecc7ec86e43f8d5ce8f',11390,147,'F53748B8C4AB1515A81C4E63965BB2AF37AA665A4290B6FE0CCCAEC353CB12ADB56DC99E431047F46585C57D69CBB7DB')
    'mbcx01_r9_oracle.py' = @('76560dd49cbc225d36ca9090aae26efd8b7493ce',16681,368,'34A795648A3A2236CA43367077AF70E281E8D87CBF0D4CEDB586C25E371F012F909A8BDCB9F5F538C9C55F2C2DE4706A')
    'mbcx01_r9_reference.py' = @('170f7d2c2815c4f2d78f2c75ea5c58b4442d0fa9',66936,1394,'6DA11124D3B90E2D649A99E54338E2395BC3D3BD6686BBE3F17D632394ABA6F49245D8D416340EEC60B9CA212C448A37')
    'verify-r9-normative-bundle.py' = @('ecac64be665a05f6c47d2b4ed828dd9d4118004d',22271,507,'88E157644F199D46035DA41B504851A741A210830604999206483E4FB9B4F8A593DF5DC266456E773168708514EF09D8')
    'verify-r9-schema-ajv.mjs' = @('4ffd38bd67147ad475309e1eefd0de3795d714ed',3659,78,'37FB06B5761D208D650EB29A563A3A4D63A47A9633FA0638FB1D27F0258AA1CB25B8084AB5E9DA11C63269DFD314372C')
    'MBCX-01-R9-NO-PAID-VERIFICATION.json' = @('6c0f66a0d96501e6d687a3bad72e5a00e140e40c',15537,429,'3294001EE104D0C14B0FD4B2C2E8D3FFD317FDE3F6CEF9165FE314196082C98657B9B211FD4157FBFBA72E934A0EDC25')
}
$temporary = Join-Path ([System.IO.Path]::GetTempPath()) ('mbcx-r9-git-object-' + [Guid]::NewGuid().ToString('N'))
[void](New-Item -ItemType Directory -Path $temporary)
try {
    foreach ($entry in $expected.GetEnumerator()) {
        $name = $entry.Key
        $pin = $entry.Value
        $spec = '{0}:{1}' -f $Commit,$name
        $blob = (& git -C $PSScriptRoot rev-parse $spec).Trim()
        if ($LASTEXITCODE -ne 0 -or $blob -ne $pin[0]) { throw "Git blob mismatch for $name" }
        $path = Join-Path $temporary $name
        $parent = Split-Path -Parent $path
        if (-not (Test-Path -LiteralPath $parent)) { [void](New-Item -ItemType Directory -Path $parent) }
        $start = [System.Diagnostics.ProcessStartInfo]::new('git')
        $start.WorkingDirectory = $PSScriptRoot
        $start.ArgumentList.Add('cat-file'); $start.ArgumentList.Add('blob'); $start.ArgumentList.Add($spec)
        $start.RedirectStandardOutput = $true; $start.UseShellExecute = $false
        $process = [System.Diagnostics.Process]::Start($start)
        $stream = [System.IO.File]::Create($path)
        try { $process.StandardOutput.BaseStream.CopyTo($stream) } finally { $stream.Dispose() }
        $process.WaitForExit()
        if ($process.ExitCode -ne 0) { throw "git cat-file failed for $name" }
        $bytes = [System.IO.File]::ReadAllBytes($path)
        $lines = if ($bytes.Length -eq 0) { 0 } else { ($bytes | Where-Object { $_ -eq 10 }).Count + $(if ($bytes[-1] -eq 10) { 0 } else { 1 }) }
        $sha = (Get-FileHash -LiteralPath $path -Algorithm SHA384).Hash
        if ($bytes.Length -ne $pin[1] -or $lines -ne $pin[2] -or $sha -ne $pin[3]) {
            throw "Git-object byte/line/hash pin mismatch for $name"
        }
    }
    $env:MBCX_AJV_ROOT = '<home>\source\agentvault-mcp-bridge\node_modules\ajv'
    & python (Join-Path $temporary 'verify-r9-normative-bundle.py') --oc-reps 25
    if ($LASTEXITCODE -ne 0) { throw 'Extracted Git-object verifier failed.' }
    $report = Get-Content -Raw -LiteralPath (Join-Path $temporary 'MBCX-01-R9-NO-PAID-VERIFICATION.json') | ConvertFrom-Json
    if ($report.paid_calls -ne 0 -or $report.experiment_evidence -ne $false) { throw 'Retained report evidence classification is invalid.' }
    'PASS: r9 pins and executable reconstruction hold using only extracted Git-object bytes.'
}
finally {
    Remove-Item Env:MBCX_AJV_ROOT -ErrorAction SilentlyContinue
    $resolved = [System.IO.Path]::GetFullPath($temporary)
    $tempBase = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
    if ($resolved.StartsWith($tempBase,[StringComparison]::OrdinalIgnoreCase) -and (Test-Path -LiteralPath $resolved)) {
        Remove-Item -LiteralPath $resolved -Recurse -Force
    }
}
