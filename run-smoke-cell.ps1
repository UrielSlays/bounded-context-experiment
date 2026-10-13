[CmdletBinding(DefaultParameterSetName = 'SelfTest')]
param(
    [Parameter(ParameterSetName = 'SelfTest')][switch]$SelfTest,
    [Parameter(ParameterSetName = 'Preflight')][switch]$Preflight,
    [Parameter(ParameterSetName = 'Execute')][switch]$Execute,

    [Parameter(ParameterSetName = 'Preflight')]
    [Parameter(ParameterSetName = 'Execute')]
    [string]$Authorization = 'C:\AgentVault\Moonwalker\MBCX-01-SMOKE-AUTHORIZATION-2026-08-14.md',

    [Parameter(ParameterSetName = 'Execute')]
    [string]$Destination = 'C:\AgentVault\_mbcx01-smoke-2026-08-14\',

    # Preflight takes these too: the driver's preflight now resolves the candidate
    # image and reads the authorization document for THIS run's command line and
    # cell, so a preflight that could not be told them would quietly report on the
    # default run instead of the one the operator is about to make.
    [Parameter(ParameterSetName = 'Preflight')]
    [Parameter(ParameterSetName = 'Execute')]
    [string]$CommandLine = 'cmd.exe /c exit 0',

    [Parameter(ParameterSetName = 'Preflight')]
    [Parameter(ParameterSetName = 'Execute')]
    [string]$Cell = '0,0,0',

    # FIXTURE key only. A smoke run is fixture-kind evidence by definition and
    # can NEVER clear production admission; FixtureSigner refuses any key id
    # that is not a test id, so a production key cannot be routed through here.
    [Parameter(ParameterSetName = 'Execute', Mandatory = $true)]
    [string]$FixtureSigningKeyPem,

    [Parameter(ParameterSetName = 'Execute', Mandatory = $true)]
    [string]$FixtureSigningKeyId,

    [Parameter(ParameterSetName = 'Preflight')]
    [Parameter(ParameterSetName = 'Execute')]
    [switch]$OperatorConfirmsNotNested,

    [string]$ReportPath
)

# MBCX-01 BUILD B - ONE-CELL smoke proof launcher (SMOKE-RUNBOOK section 3).
#
# ⛔ THIS SCRIPT AUTHORIZES NOTHING. -Execute runs only when ALL of the
#    following already hold, and it checks each one before it does anything:
#
#      1. the authorization document named by -Authorization exists and carries
#         the literal marker line MBCX01-BUILD-B-PHYSICAL-COLLECTION-AUTHORIZED;
#      2. this PowerShell session is ELEVATED (kernel PMC requires it);
#      3. the operator has confirmed with -OperatorConfirmsNotNested that this
#         is NOT running inside nested virtualization - the guest side cannot
#         read that, and nested virtualization must ABORT;
#      4. -Destination does not already exist. Evidence lands there and NOWHERE
#         else, so a pre-existing directory is refused rather than merged into;
#      5. `node` resolves on this shell's PATH. Signature verification shells out
#         to it, so a run that cannot reach it cannot be certified. The driver
#         probes it AGAIN inside the elevated session, because elevation changes
#         PATH and that is the session that signs.
#
#    MBCX01_BUILD_ALLOW_PHYSICAL=1 is set ONLY inside the -Execute branch and
#    ONLY in this process. It is never set for -SelfTest or -Preflight, never
#    persisted to the user or machine environment, and mbcx01_smoke_cell.py
#    never sets it itself.
#
# THE PASS CRITERION IS AN HONEST RED. The run is expected to produce a
# structurally valid signed envelope that admission REFUSES with the honest
# sentinel(s) - fixture-kind evidence, no production roots. A GREEN admission
# would be a DEFECT, not a success. Capability gaps (unsupported PMU, counter
# losses, a refused ordinal) are FINDINGS to record verbatim.
#
# Modes:
#   -SelfTest    pure logic + static ABI only. No OS state. This is the ONLY
#                mode the BUILD that wrote this script ever ran.
#   -Preflight   adds READ-ONLY host probes (elevation, virtualization posture,
#                authorization marker, PMU profile-source enumeration). Starts
#                no session, creates no process, writes nothing.
#   -Execute     the runbook step itself.

$ErrorActionPreference = 'Stop'
$python = if ($env:MBCX01_PYTHON) { $env:MBCX01_PYTHON } else { 'python' }
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$driver = Join-Path $here 'mbcx01_smoke_cell.py'

if (-not (Test-Path -LiteralPath $driver)) {
    throw "smoke driver not found: $driver"
}

function Test-Elevated {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal]::new($identity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

$arguments = @()
switch ($PSCmdlet.ParameterSetName) {
    'SelfTest' {
        Write-Host 'MODE: selftest - pure logic and static ABI only. No OS state is touched.'
        $arguments = @('selftest')
    }
    'Preflight' {
        Write-Host 'MODE: preflight - READ-ONLY host probes. No session is started.'
        Write-Host "  candidate     : $CommandLine"
        Write-Host "  cell          : $Cell"
        $arguments = @('preflight', '--authorization', $Authorization,
                       '--command-line', $CommandLine,
                       '--cell', $Cell)
        if ($OperatorConfirmsNotNested) { $arguments += '--operator-confirms-not-nested' }
    }
    'Execute' {
        Write-Host 'MODE: execute - the owner-authorized one-cell smoke proof.'

        if (-not (Test-Path -LiteralPath $Authorization)) {
            throw "ABORT: authorization document not found: $Authorization"
        }
        $marker = 'MBCX01-BUILD-B-PHYSICAL-COLLECTION-AUTHORIZED'
        if (-not (Select-String -LiteralPath $Authorization -SimpleMatch -Pattern $marker -Quiet)) {
            throw "ABORT: authorization document does not carry the marker $marker"
        }
        # The signature-verification toolchain, read in THIS shell BEFORE anything
        # else, because the operator is usually standing here about to elevate and
        # this is the cheapest moment to learn the toolchain is missing. It is NOT
        # the same check the driver makes: elevation commonly changes PATH, so
        # mbcx01_smoke_cell.preflight probes `node` AGAIN inside the elevated
        # session - that one is the session that signs. Both are needed; neither is
        # a substitute (BUILD acceptance r6, ruling 6; SEAT1 + SEAT3, both EXECUTED).
        $nodeCommand = Get-Command node -ErrorAction SilentlyContinue
        if (-not $nodeCommand) {
            throw ('ABORT: SIGNATURE_VERIFIER_TOOLCHAIN_UNAVAILABLE - `node` is not ' +
                   'resolvable on this PATH. Both halves of the smoke pass criterion ' +
                   'verify an Ed25519 signature by shelling out to node, so a run ' +
                   'that cannot reach it cannot be certified. Nothing was started.')
        }
        # The verifier SCRIPT is deliberately NOT re-checked here. Its path lives in
        # the frozen layer (mbcx01_r13_measurement.VERIFIER) and the driver's
        # preflight reads it from there, so the file probed is by construction the
        # file that will be run. Naming it a second time in this script would be a
        # constant that can drift away from the one that matters.

        if (-not (Test-Elevated)) {
            throw ('ABORT: this session is NOT elevated. Kernel PMC requires an ' +
                   'elevated session (smoke runbook section 3 step 2). Nothing was started.')
        }
        if (-not $OperatorConfirmsNotNested) {
            throw ('ABORT: nested virtualization is unsupported and cannot be read ' +
                   'from inside a guest. Re-run with -OperatorConfirmsNotNested only ' +
                   'if you have confirmed this host is bare metal or a Hyper-V ROOT ' +
                   'partition (authorization document, Host row).')
        }
        if (Test-Path -LiteralPath $Destination) {
            throw ("ABORT: evidence destination already exists: $Destination. The " +
                   'authorization names a NEW directory; refusing to merge evidence ' +
                   'into an existing one.')
        }
        if (-not (Test-Path -LiteralPath $FixtureSigningKeyPem)) {
            throw "ABORT: fixture signing key not found: $FixtureSigningKeyPem"
        }
        if (($FixtureSigningKeyId -notlike '*.TEST.*') -and
            ($FixtureSigningKeyId -notlike '*.TEST')) {
            throw ("ABORT: '$FixtureSigningKeyId' is not a TEST key id. A smoke run is " +
                   'fixture-kind evidence and must never be signed with a production key.')
        }

        Write-Host ''
        Write-Host 'Preconditions PASSED:'
        Write-Host "  authorization : $Authorization (marker present)"
        Write-Host "  elevation     : yes"
        Write-Host "  nested        : operator-confirmed NOT nested"
        Write-Host "  destination   : $Destination (new)"
        Write-Host "  candidate     : $CommandLine"
        Write-Host "  cell          : $Cell"
        Write-Host "  node (this shell): $($nodeCommand.Source) - the ELEVATED session is probed again by the driver"
        Write-Host ''
        Write-Host 'EXPECTED RESULT: a structurally valid envelope that admission REFUSES.'
        Write-Host 'A green admission would be a DEFECT. Capability gaps are FINDINGS.'
        Write-Host ''

        # Set ONLY here, ONLY in this process, and only after every check above.
        $env:MBCX01_BUILD_ALLOW_PHYSICAL = '1'
        $arguments = @('execute',
                       '--authorization', $Authorization,
                       '--destination', $Destination,
                       '--command-line', $CommandLine,
                       '--cell', $Cell,
                       '--fixture-signing-key-pem', $FixtureSigningKeyPem,
                       '--fixture-signing-key-id', $FixtureSigningKeyId,
                       '--operator-confirms-not-nested')
    }
}

if ($ReportPath) { $arguments += @('--report', $ReportPath) }

try {
    & $python $driver @arguments
    $code = $LASTEXITCODE
}
finally {
    # Never leave the physical-collection flag set in this process, whatever
    # happened above.
    Remove-Item Env:\MBCX01_BUILD_ALLOW_PHYSICAL -ErrorAction SilentlyContinue
}

switch ($code) {
    0 { Write-Host ''; Write-Host 'RESULT: OK - read the JSON report; the pass criterion is the RED at admission.' }
    2 { Write-Host ''; Write-Host 'RESULT: ABORT - a legitimate outcome. Record the reason verbatim; do not retry blindly.' }
    default { Write-Host ''; Write-Host "RESULT: FAULT (exit $code) - record the traceback verbatim." }
}
exit $code
