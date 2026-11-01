<#
.SYNOPSIS
    Harness de Autodescubrimiento y Autoevolución de home-lab (OCP).
.DESCRIPTION
    Inspecciona telemetría, histórico de tareas y commits para detectar patrones
    repetitivos y autogenerar skills, rules, hooks, subagentes y scripts.
    Abierto a la expansión y cerrado a la modificación.
.PARAMETER Discover
    Solo ejecuta el autodescubrimiento y muestra la tabla de candidatos detectados.
.PARAMETER DryRun
    Simula la síntesis y validación sin escribir archivos en disco (activo por defecto).
.PARAMETER Write
    Escribe los artefactos sintetizados y validados en el workspace.
.PARAMETER Limit
    Límite máximo de candidatos a procesar (por defecto: 5).
.PARAMETER Tier
    Filtra por nivel de artefacto (script, skill, agent, rule, hook).
.PARAMETER Json
    Produce salida en formato JSON estructurado.
.PARAMETER Help
    Muestra la ayuda detallada.
.EXAMPLE
    pwsh -File scripts/bin/ecc-agy/auto-evolve.ps1 -Discover
.EXAMPLE
    pwsh -File scripts/bin/ecc-agy/auto-evolve.ps1 -DryRun
.EXAMPLE
    pwsh -File scripts/bin/ecc-agy/auto-evolve.ps1 -Write -Limit 3
#>
[CmdletBinding()]
param(
    [switch]$Discover,
    [switch]$DryRun,
    [switch]$Write,
    [int]$Limit = 5,
    [ValidateSet('script', 'skill', 'agent', 'rule', 'hook')]
    [string]$Tier,
    [switch]$Json,
    [switch]$Help
)

$ErrorActionPreference = 'Stop'

if ($Help) {
    Get-Help $MyInvocation.MyCommand.Path -Full
    exit 0
}

# Resolver la raíz del repositorio
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = (Resolve-Path "$ScriptDir\..\..\..").Path
$CliScript = Join-Path $RootDir "scripts\plugin\ecc-agy\evolution\cli.py"

if (-not (Test-Path $CliScript)) {
    Write-Error "No se encontro el modulo CLI de autoevolucion en: $CliScript"
    exit 1
}

$Arguments = @($CliScript)

if ($Discover) {
    $Arguments += "--discover"
}

if ($Write) {
    $Arguments += "--write"
} else {
    $Arguments += "--dry-run"
}

if ($Limit -gt 0) {
    $Arguments += @("--limit", $Limit)
}

if ($Tier) {
    $Arguments += @("--tier", $Tier)
}

if ($Json) {
    $Arguments += "--json"
}

python @Arguments
$ExitCode = $LASTEXITCODE
exit $ExitCode
