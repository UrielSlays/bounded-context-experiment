param(
    [Parameter(Mandatory = $true)][string]$Commit,
    [Parameter(Mandatory = $true)][string]$ManifestBlob
)
$ErrorActionPreference = 'Stop'
$manifestName = 'MBCX-01-R10-PIN-MANIFEST.json'
$temporary = Join-Path ([System.IO.Path]::GetTempPath()) ('mbcx-r10-git-object-' + [Guid]::NewGuid().ToString('N'))
[void](New-Item -ItemType Directory -Path $temporary)

function Export-GitBlobExact([string]$Spec, [string]$Destination) {
    $parent = Split-Path -Parent $Destination
    if (-not (Test-Path -LiteralPath $parent)) { [void](New-Item -ItemType Directory -Path $parent) }
    $info = [System.Diagnostics.ProcessStartInfo]::new()
    $info.FileName = 'git'
    $info.Arguments = 'cat-file blob "' + $Spec.Replace('"', '\"') + '"'
    $info.WorkingDirectory = $PSScriptRoot
    $info.RedirectStandardOutput = $true
    $info.RedirectStandardError = $true
    $info.UseShellExecute = $false
    $process = [System.Diagnostics.Process]::Start($info)
    $stream = [System.IO.File]::Create($Destination)
    try { $process.StandardOutput.BaseStream.CopyTo($stream) } finally { $stream.Dispose() }
    $stderr = $process.StandardError.ReadToEnd()
    $process.WaitForExit()
    if ($process.ExitCode -ne 0) { throw "git cat-file failed for $Spec : $stderr" }
}

function Get-LineCount([byte[]]$Bytes) {
    if ($Bytes.Length -eq 0) { return 0 }
    $count = ($Bytes | Where-Object { $_ -eq 10 }).Count
    if ($Bytes[-1] -ne 10) { $count += 1 }
    return $count
}

try {
    $manifestSpec = '{0}:{1}' -f $Commit, $manifestName
    $actualManifestBlob = (& git -C $PSScriptRoot rev-parse $manifestSpec).Trim()
    if ($LASTEXITCODE -ne 0 -or $actualManifestBlob -ne $ManifestBlob) {
        throw 'Council-pinned manifest blob does not match the governing commit.'
    }
    $manifestPath = Join-Path $temporary $manifestName
    Export-GitBlobExact $manifestSpec $manifestPath
    $manifest = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json
    if ($manifest.manifest_id -ne 'MBCX-01-R10-PIN-MANIFEST') { throw 'Wrong manifest identity.' }

    foreach ($subject in $manifest.subjects) {
        $name = [string]$subject.path
        if ([System.IO.Path]::IsPathRooted($name) -or $name -match '(^|[\\/])\.\.([\\/]|$)') {
            throw "Unsafe manifest path: $name"
        }
        $spec = '{0}:{1}' -f $Commit, $name
        $blob = (& git -C $PSScriptRoot rev-parse $spec).Trim()
        if ($LASTEXITCODE -ne 0 -or $blob -ne [string]$subject.git_blob) {
            throw "Git blob mismatch for $name"
        }
        $destination = Join-Path $temporary $name
        $resolvedDestination = [System.IO.Path]::GetFullPath($destination)
        $resolvedRoot = [System.IO.Path]::GetFullPath($temporary) + [System.IO.Path]::DirectorySeparatorChar
        if (-not $resolvedDestination.StartsWith($resolvedRoot, [StringComparison]::OrdinalIgnoreCase)) {
            throw "Manifest path escaped reconstruction root: $name"
        }
        Export-GitBlobExact $spec $destination
        $bytes = [System.IO.File]::ReadAllBytes($destination)
        $sha = (Get-FileHash -LiteralPath $destination -Algorithm SHA384).Hash
        $lines = Get-LineCount $bytes
        if ($bytes.Length -ne [int64]$subject.bytes -or $lines -ne [int64]$subject.lines -or
                $sha -ne [string]$subject.sha384) {
            throw "Byte/line/SHA-384 mismatch for $name"
        }
    }

    $env:MBCX_AJV_ROOT = 'C:\Users\Kingo\source\agentvault-mcp-bridge\node_modules\ajv'
    & python (Join-Path $temporary 'verify-r10-normative-bundle.py')
    if ($LASTEXITCODE -ne 0) { throw 'Reconstructed r10 verifier failed.' }
    $report = Get-Content -Raw -LiteralPath (Join-Path $temporary 'MBCX-01-R10-NO-PAID-VERIFICATION.json') | ConvertFrom-Json
    if ($report.paid_calls -ne 0 -or $report.experiment_evidence -ne $false) {
        throw 'Verification report evidence classification is invalid.'
    }
    'PASS: r10 council pin, exact Git-object reconstruction, and executable verification hold.'
}
finally {
    Remove-Item Env:MBCX_AJV_ROOT -ErrorAction SilentlyContinue
    $resolved = [System.IO.Path]::GetFullPath($temporary)
    $tempBase = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
    if ($resolved.StartsWith($tempBase, [StringComparison]::OrdinalIgnoreCase) -and
            (Test-Path -LiteralPath $resolved)) {
        Remove-Item -LiteralPath $resolved -Recurse -Force
    }
}

