<#
.SYNOPSIS
    Valida y formatea mensajes de commit bajo el estándar [type]+[projects]: <title> con cuerpo obligatorio.
.DESCRIPTION
    Invoca scripts/ecc-agy/format_commit.py asegurando el cumplimiento de la regla en Windows 11.
.PARAMETER Validate
    Mensaje de commit a validar.
.PARAMETER ValidateFile
    Ruta al archivo que contiene el mensaje de commit.
.PARAMETER Type
    Tipo de commit Conventional (feat, fix, refactor, chore, docs, test, perf, build, ci, sec).
.PARAMETER Projects
    Proyectos o módulos afectados (ej. cluster, kakebo, whoiam, net, ecc-agy).
.PARAMETER Title
    Título en modo imperativo.
.PARAMETER Body
    Cuerpo explicativo detallando motivación, contexto y pruebas.
.PARAMETER Json
    Emite el resultado en formato JSON estructurado.
.EXAMPLE
    .\format-commit.ps1 -Type feat -Projects cluster -Title "implement storage manager" -Body "Detalle..."
#>
[CmdletBinding()]
param(
    [string]$Validate,
    [string]$ValidateFile,
    [ValidateSet("feat", "fix", "refactor", "chore", "docs", "test", "perf", "build", "ci", "sec", "security")]
    [string]$Type,
    [string]$Projects,
    [string]$Title,
    [string]$Body,
    [switch]$Json
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$WorkspaceRoot = (Resolve-Path "$ScriptDir\..\..\..").Path
$PyScript = Join-Path $WorkspaceRoot "scripts\ecc-agy\format_commit.py"

if (-not (Test-Path $PyScript)) {
    Write-Error "[ERROR] No se encuentra el script en $PyScript"
    exit 1
}

$Arguments = @($PyScript)
if ($Validate) {
    $Arguments += @("--validate", $Validate)
}
if ($ValidateFile) {
    $Arguments += @("--validate-file", $ValidateFile)
}
if ($Type) {
    $Arguments += @("--type", $Type)
}
if ($Projects) {
    $Arguments += @("--projects", $Projects)
}
if ($Title) {
    $Arguments += @("--title", $Title)
}
if ($Body) {
    $Arguments += @("--body", $Body)
}
if ($Json) {
    $Arguments += "--json"
}

python @Arguments
exit $LASTEXITCODE
