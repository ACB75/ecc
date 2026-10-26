<#
.SYNOPSIS
    Instalador Multi-Distribución del Ecosistema ECC-AECB.
.DESCRIPTION
    Permite desplegar de forma interactiva o parametrizada cualquiera de las 3 distribuciones:
      - claude  : Boilerplates oficiales para Claude Code (.claude/, CLAUDE.md, hooks).
      - agy     : Distribución agnóstica para Google Antigravity (16 skills, 12 agents, SRE, lista para cualquier proyecto).
      - homelab : Fork especializado para el ecosistema Home-Lab (portal, cluster, kakebo, whoiam, ADR-0008).
.PARAMETER Target
    claude | agy | homelab
.PARAMETER Destination
    Directorio de destino (por defecto el entorno configurado de AGY o proyecto actual).
.EXAMPLE
    pwsh -File install.ps1 -Target agy
    pwsh -File install.ps1 -Target claude -Destination C:\MiProyectoClaude
    pwsh -File install.ps1 -Target homelab
#>
param(
    [ValidateSet("claude", "agy", "homelab")]
    [string]$Target = "agy",

    [string]$Destination
)

$ErrorActionPreference = "Stop"
$ScriptRoot = $PSScriptRoot

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "             ECC-AECB MASTER MULTI-DISTRIBUTION INSTALLER         " -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "Distribución seleccionada: $Target" -ForegroundColor Yellow

switch ($Target) {
    "claude" {
        $sourceDir = Join-Path $ScriptRoot "ecc-claude"
        if (-not $Destination) {
            $Destination = Get-Location
        }
        Write-Host "[+] Desplegando boilerplates de Claude Code en: $Destination" -ForegroundColor Green
        Copy-Item -Path (Join-Path $sourceDir "CLAUDE.md") -Destination $Destination -Force
        Copy-Item -Path (Join-Path $sourceDir ".claude") -Destination (Join-Path $Destination ".claude") -Recurse -Force
        Write-Host "[✓] Boilerplates de Claude Code instalados con éxito." -ForegroundColor Green
    }
    "agy" {
        $sourceDir = Join-Path $ScriptRoot "ecc-agy"
        if (-not $Destination) {
            $Destination = Join-Path $env:USERPROFILE ".gemini\config\plugins\ecc-agy"
        }
        Write-Host "[+] Desplegando plugin agnóstico de Antigravity en: $Destination" -ForegroundColor Green
        New-Item -ItemType Directory -Path $Destination -Force | Out-Null
        Copy-Item -Path (Join-Path $sourceDir "*") -Destination $Destination -Recurse -Force
        Write-Host "[✓] Plugin agnóstico ecc-agy instalado en Antigravity." -ForegroundColor Green
    }
    "homelab" {
        $sourceDir = Join-Path $ScriptRoot "ecc-agy-homelab"
        if (-not $Destination) {
            $Destination = Join-Path $env:USERPROFILE ".gemini\config\plugins\ecc-agy"
        }
        Write-Host "[+] Desplegando fork especializado Home-Lab en: $Destination" -ForegroundColor Green
        New-Item -ItemType Directory -Path $Destination -Force | Out-Null
        Copy-Item -Path (Join-Path $sourceDir "*") -Destination $Destination -Recurse -Force
        Write-Host "[✓] Fork ecc-agy-homelab instalado en Antigravity." -ForegroundColor Green
    }
}

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "Operación completada exitosamente." -ForegroundColor Cyan
