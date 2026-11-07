<#
.SYNOPSIS
    Ejecuta el escaneo estático de seguridad y detección de credenciales en ECC.
.DESCRIPTION
    Script rutinario para Windows 11 (pwsh) que delega en scripts/ecc-agy/security_audit.py.
.EXAMPLE
    pwsh -File scripts/bin/ecc-agy/security-audit.ps1
#>
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$WorkspaceRoot = (Resolve-Path "$ScriptDir\..\..\..").Path
$PyScript = Join-Path $WorkspaceRoot "scripts\ecc-agy\security_audit.py"

if (-not (Test-Path $PyScript)) {
    Write-Error "[ERROR] No se encuentra el script en $PyScript"
    exit 1
}

python $PyScript --root $WorkspaceRoot
exit $LASTEXITCODE
