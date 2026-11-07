<#
.SYNOPSIS
    Generador automatizado de autopsia Post-Mortem 5W para ramas fix/*.
.DESCRIPTION
    Script rutinario para Windows 11 (pwsh) que delega en scripts/ecc-agy/generate_postmortem.py.
    Instancia la plantilla doc/post-mortem/TEMPLATE_POSTMORTEM_5W.md con metadatos reales de Git.
.PARAMETER Branch
    Nombre opcional de la rama del incidente (por defecto la activa).
.PARAMETER DryRun
    Muestra la plantilla instanciada sin guardarla en disco.
.EXAMPLE
    pwsh -File scripts/bin/ecc-agy/generate-postmortem.ps1
    pwsh -File scripts/bin/ecc-agy/generate-postmortem.ps1 -DryRun
#>
[CmdletBinding()]
param(
    [string]$Branch = "",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$WorkspaceRoot = (Resolve-Path "$ScriptDir\..\..\..").Path
$PyScript = Join-Path $WorkspaceRoot "scripts\ecc-agy\generate_postmortem.py"

if (-not (Test-Path $PyScript)) {
    Write-Error "[ERROR] No se encuentra el script en $PyScript"
    exit 1
}

$cmdArgs = @()
if ($Branch) { $cmdArgs += "--branch", $Branch }
if ($DryRun) { $cmdArgs += "--dry-run" }

python $PyScript $cmdArgs
exit $LASTEXITCODE
