<#
.SYNOPSIS
    Ejecuta la auditoría estática de SonarQube Quality Gate A en ECC.
.DESCRIPTION
    Script rutinario para Windows 11 (pwsh) que delega en scripts/ecc-agy/sonar_audit.py.
.EXAMPLE
    pwsh -File scripts/bin/ecc-agy/sonar-audit.ps1
#>
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$WorkspaceRoot = (Resolve-Path "$ScriptDir\..\..\..").Path
$PyScript = Join-Path $WorkspaceRoot "scripts\ecc-agy\sonar_audit.py"

if (-not (Test-Path $PyScript)) {
    Write-Error "[ERROR] No se encuentra el script en $PyScript"
    exit 1
}

python $PyScript --root $WorkspaceRoot
exit $LASTEXITCODE
