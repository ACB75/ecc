<#
.SYNOPSIS
    Audita y formatea archivos Markdown conforme al estándar DavidAnson/markdownlint.
.DESCRIPTION
    Ejecuta markdownlint-cli leyendo dinámicamente la configuración .markdownlint.json
    del repositorio correspondiente en Windows 11 (pwsh). Idempotente y parametrizado.
    Formatea automáticamente los archivos por defecto (--fix) en múltiples pasadas.
    Permite validar y formatear TODO.md, TODO_DONE/ y cualquier ruta o patrón del repositorio.
.PARAMETER Fix
    Fuerza el formateo automático (activo por defecto salvo que se indique -CheckOnly).
.PARAMETER CheckOnly
    Modo sólo lectura / verificación estricta sin modificar archivos (útil para CI gates).
.PARAMETER Target
    Ruta, directorio o patrón glob de archivos a auditar (ej. "*TODO*", "doc/TODO.md", "doc", "**/*.md").
    Por defecto audita y formatea todos los archivos Markdown del repositorio (**/*.md).
.PARAMETER Root
    Directorio raíz del repositorio (por defecto detectado dinámicamente buscando .markdownlint.json).
.EXAMPLE
    pwsh -File scripts/bin/ecc-agy/lint-markdown.ps1
    pwsh -File scripts/bin/ecc-agy/lint-markdown.ps1 -Target "*TODO*"
    pwsh -File scripts/bin/ecc-agy/lint-markdown.ps1 -Target doc/TODO.md
    pwsh -File scripts/bin/ecc-agy/lint-markdown.ps1 -CheckOnly
#>
param(
    [switch]$Fix,
    [switch]$CheckOnly,
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

# 2. Configurar exclusiones (ignorar solo dependencias y artefactos compilados)
$IgnoreList = @(
    "--ignore", "**/node_modules/**",
    "--ignore", "**/.git/**",
    "--ignore", "**/.venv/**",
    "--ignore", "**/dist/**",
    "--ignore", "**/build/**"
)

# 3. Resolución dinámica del objetivo (Target)
# Todo archivo .md y cualquier patrón *TODO* pasa a ser 100% válido y auditable
$TargetPattern = ""
if ([string]::IsNullOrWhiteSpace($Target)) {
    $TargetPattern = "**/*.md"
} else {
    $cleanTarget = $Target.Trim()
    if ((Test-Path $cleanTarget) -and (Get-Item $cleanTarget).PSIsContainer) {
        $normalizedDir = $cleanTarget.Replace("\", "/").TrimEnd("/")
        $TargetPattern = "$normalizedDir/**/*.md"
    } elseif ($cleanTarget -match "\*|\?") {
        $normalized = $cleanTarget.Replace("\", "/")
        if ($normalized -notmatch "[/]") {
            if ($normalized -notmatch "\.md$") {
                $TargetPattern = "**/*$normalized*.md"
            } else {
                $TargetPattern = "**/*$normalized"
            }
            $TargetPattern = $TargetPattern -replace "\*+", "*"
        } else {
            $TargetPattern = $normalized
        }
    } else {
        $TargetPattern = $cleanTarget.Replace("\", "/")
    }
}

$ApplyFix = (-not $CheckOnly)

Write-Host "Ejecutando markdownlint (DavidAnson) con configuración en $ConfigFile..." -ForegroundColor Cyan
Write-Host "Objetivo: $TargetPattern | Modo: $(if ($ApplyFix) { 'Formateo automático (--fix)' } else { 'Sólo verificación (-CheckOnly)' })" -ForegroundColor Gray

# 4. Ejecución en bucle multi-pasada cuando se formatea (resuelve problemas en cascada AST)
$MaxPasses = if ($ApplyFix) { 3 } else { 1 }
$ExitCode = 0

for ($pass = 1; $pass -le $MaxPasses; $pass++) {
    $CurrentArgs = @("-c", $ConfigFile)
    if ($ApplyFix) {
        $CurrentArgs += "--fix"
    }
    $CurrentArgs += $IgnoreList
    $CurrentArgs += $TargetPattern

    npx --yes markdownlint-cli @CurrentArgs
    $ExitCode = $LASTEXITCODE

    if ($ExitCode -eq 0) {
        break
    }
    if ($ApplyFix -and $pass -lt $MaxPasses) {
        Start-Sleep -Milliseconds 100
    }
}

if ($ExitCode -eq 0) {
    Write-Host "[OK] Todos los archivos Markdown cumplen con el estándar markdownlint." -ForegroundColor Green
} else {
    Write-Host "[FAIL] Se detectaron errores de sintaxis o formato en Markdown." -ForegroundColor Red
}

exit $ExitCode
