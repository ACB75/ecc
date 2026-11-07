<#
.SYNOPSIS
    Auditoría, mapeo y validación de enlaces relativos en documentación Markdown.
.DESCRIPTION
    Script rutinario para Windows 11 (pwsh) que delega en scripts/ecc-agy/map_docs.py.
    Detecta enlaces rotos en doc/ y genera un informe de salud documental estructurado.
.PARAMETER DocRoot
    Directorio o archivo raíz a auditar (por defecto doc/).
.EXAMPLE
    pwsh -File scripts/bin/ecc-agy/map-docs.ps1
    pwsh -File scripts/bin/ecc-agy/map-docs.ps1 -DocRoot "doc/plan"
#>
[CmdletBinding()]
param(
    [string]$DocRoot = "doc"
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$WorkspaceRoot = (Resolve-Path "$ScriptDir\..\..\..").Path
$PyScript = Join-Path $WorkspaceRoot "scripts\ecc-agy\map_docs.py"

if (-not (Test-Path $PyScript)) {
    Write-Error "[ERROR] No se encuentra el script en $PyScript"
    exit 1
}

python $PyScript --doc-root (Join-Path $WorkspaceRoot $DocRoot)
exit $LASTEXITCODE
