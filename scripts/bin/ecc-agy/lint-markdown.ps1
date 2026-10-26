<#
.SYNOPSIS
    Audita y formatea archivos Markdown conforme al estándar DavidAnson/markdownlint.
.DESCRIPTION
    Ejecuta markdownlint-cli leyendo dinámicamente la configuración .markdownlint.json
    del repositorio correspondiente en Windows 11 (pwsh). Idempotente y parametrizado.
.PARAMETER Fix
    Corrige automáticamente problemas de espaciado, líneas en blanco y sintaxis.
.PARAMETER Target
    Ruta o patrón de archivos a auditar.
.PARAMETER Root
    Directorio raíz del repositorio (por defecto detectado dinámicamente buscando .markdownlint.json).
.EXAMPLE
    pwsh -File scripts/bin/ecc-agy/lint-markdown.ps1 -Fix
    pwsh -File scripts/bin/ecc-agy/lint-markdown.ps1 -Target doc/LOG.md -Fix
#>
param(
    [switch]$Fix,
    [string]$Target = "",
    [string]$Root = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Find-MarkdownlintRoot([string]$StartDir) {
    $dir = $StartDir
    while ($dir -and (Test-Path $dir)) {
        if (Test-Path (Join-Path $dir ".markdownlint.json")) {
            return $dir
        }
        $parent = Split-Path -Parent $dir
        if (-not $parent -or $parent -eq $dir) { break }
        $dir = $parent
    }
    return $null
}

# 1. Detección dinámica de la raíz del repositorio y su archivo .markdownlint.json
if (-not $Root -and $Target -and (Test-Path $Target)) {
    $targetDir = Split-Path -Parent (Resolve-Path $Target)
    $Root = Find-MarkdownlintRoot $targetDir
}

if (-not $Root) {
    $Root = Find-MarkdownlintRoot (Get-Location).Path
}

if (-not $Root -and $PSScriptRoot) {
    $Root = Find-MarkdownlintRoot $PSScriptRoot
}

if (-not $Root) {
    $Root = (Get-Location).Path
}

$ConfigFile = Join-Path $Root ".markdownlint.json"
if (-not (Test-Path $ConfigFile)) {
    Write-Error "Archivo de configuración .markdownlint.json no encontrado en: $ConfigFile"
    exit 1
}

$ArgsList = @("-c", $ConfigFile)

if ($Fix) {
    $ArgsList += "--fix"
}

# Ignorar directorios de archivo y dependencias
$ArgsList += @("--ignore", "**/TODO_DONE/**", "--ignore", "**/node_modules/**")

if ($Target -ne "") {
    $ArgsList += $Target
} else {
    $defaultFiles = @()
    $docPattern = Join-Path $Root "doc/**/*.md"
    $agentsMd = Join-Path $Root "AGENTS.md"
    $readmeMd = Join-Path $Root "README.md"
    if (Test-Path (Join-Path $Root "doc")) { $defaultFiles += $docPattern }
    if (Test-Path $agentsMd) { $defaultFiles += $agentsMd }
    if (Test-Path $readmeMd) { $defaultFiles += $readmeMd }
    if ($defaultFiles.Count -eq 0) {
        $defaultFiles += (Join-Path $Root "**/*.md")
    }
    $ArgsList += $defaultFiles
}

Write-Host "Ejecutando markdownlint (DavidAnson) con configuración en $ConfigFile..." -ForegroundColor Cyan
npx --yes markdownlint-cli @ArgsList
$ExitCode = $LASTEXITCODE

if ($ExitCode -eq 0) {
    Write-Host "[OK] Todos los archivos Markdown cumplen con el estándar markdownlint." -ForegroundColor Green
} else {
    Write-Host "[FAIL] Se detectaron errores de sintaxis o formato en Markdown." -ForegroundColor Red
}

exit $ExitCode
