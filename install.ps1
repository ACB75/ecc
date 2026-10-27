<#
.SYNOPSIS
    Instalador Multi-Distribución del Ecosistema ECC.
.DESCRIPTION
    Permite desplegar de forma interactiva o parametrizada cualquiera de las distribuciones:
      - claude  : Boilerplates oficiales para Claude Code (.claude/, CLAUDE.md, hooks).
      - agy     : Distribución unificada para Google Antigravity & Gemini (315+ skills, 73+ agents, SRE baseline).
      - homelab : Alias de compatibilidad hacia 'agy'.
.PARAMETER Target
    claude | agy | homelab
.PARAMETER Destination
    Directorio de destino (por defecto el entorno configurado de AGY o proyecto actual).
.EXAMPLE
    pwsh -File install.ps1 -Target agy
    pwsh -File install.ps1 -Target claude -Destination C:\MiProyectoClaude
#>
param(
    [ValidateSet("claude", "agy", "homelab")]
    [string]$Target = "agy",

    [string]$Destination
)

$ErrorActionPreference = "Stop"
$ScriptRoot = $PSScriptRoot

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "                ECC MASTER MULTI-DISTRIBUTION INSTALLER          " -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "Distribución seleccionada: $Target" -ForegroundColor Yellow

if ($Target -eq "homelab") {
    Write-Host "[i] Nota: 'homelab' ha sido unificado en la distribución 'ecc-agy'. Desplegando ecc-agy..." -ForegroundColor Yellow
    $Target = "agy"
}

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
        Write-Host "[+] Desplegando plugin unificado de Antigravity en: $Destination" -ForegroundColor Green
        New-Item -ItemType Directory -Path $Destination -Force | Out-Null
        Copy-Item -Path (Join-Path $sourceDir "*") -Destination $Destination -Recurse -Force
        Write-Host "[✓] Plugin unificado ecc-agy instalado en Antigravity." -ForegroundColor Green
    }
}

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "Operación completada exitosamente." -ForegroundColor Cyan
