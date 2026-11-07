<#
.SYNOPSIS
    Ejecuta la auditoría integral de higiene, tokens y calidad de arnés de ECC.
.DESCRIPTION
    Script rutinario para Windows 11 (pwsh) que delega en scripts/ecc-agy/workspace_audit.py.
.PARAMETER Clean
    Elimina archivos temporales, cachés y copias obsoletas detectadas.
.PARAMETER Optimize
    Poda automáticamente redundancias y optimiza descripciones del catálogo.
.PARAMETER SkipSonar
    Omite la fase estática de SonarQube.
.PARAMETER SkipSecurity
    Omite la fase estática de seguridad.
.EXAMPLE
    pwsh -File scripts/bin/ecc-agy/audit-workspace.ps1 -Clean -Optimize
#>
param(
    [switch]$Clean,
    [switch]$Optimize,
    [switch]$SkipSonar,
    [switch]$SkipSecurity
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$WorkspaceRoot = (Resolve-Path "$ScriptDir\..\..\..").Path
$PyScript = Join-Path $WorkspaceRoot "scripts\ecc-agy\workspace_audit.py"

if (-not (Test-Path $PyScript)) {
    Write-Error "[ERROR] No se encuentra el script en $PyScript"
    exit 1
}

$Arguments = @($PyScript, "--root", $WorkspaceRoot)
if ($Clean) {
    $Arguments += "--clean"
}
if ($Optimize) {
    $Arguments += "--optimize"
}
if ($SkipSonar) {
    $Arguments += "--skip-sonar"
}
if ($SkipSecurity) {
    $Arguments += "--skip-security"
}

python @Arguments
exit $LASTEXITCODE
