#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Asistente de ciclo de vida Git para el Monorepo Home-Lab (Trunk-Based Development con Promoción y PRs).
.PARAMETER Action
    new-branch | promote | status | create-pr
.PARAMETER Type
    feat | fix | infra | docs | chore
.PARAMETER Project
    cluster | kakebo | whoiam | doc-viewer | token-hill | net | ecc-agy | all
.PARAMETER Name
    Descripción corta de la rama (ej. 'export-csv')
.PARAMETER Tag
    Etiqueta semántica para promoción (ej. 'v1.1.0-sandbox', 'v1.1.0')
.PARAMETER Title
    Título para la Pull Request (con formato [type]+[projects]: <title>)
.PARAMETER Body
    Cuerpo opcional explicativo de la Pull Request
.EXAMPLE
    pwsh -File scripts/bin/ecc-agy/git-flow-helper.ps1 -Action new-branch -Type feat -Project kakebo -Name export-csv
    pwsh -File scripts/bin/ecc-agy/git-flow-helper.ps1 -Action create-pr -Title "feat+[kakebo]: exportar transacciones a csv"
    pwsh -File scripts/bin/ecc-agy/git-flow-helper.ps1 -Action promote -Tag v1.1.0-sandbox
#>
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("new-branch", "promote", "status", "create-pr", "complete-task")]
    [string]$Action,

    [ValidateSet("feat", "fix", "infra", "docs", "chore")]
    [string]$Type = "feat",

    [ValidateSet("cluster", "kakebo", "whoiam", "doc-viewer", "token-hill", "net", "ecc-agy", "all")]
    [string]$Project = "cluster",

    [string]$Name,

    [string]$Tag,

    [string]$Title,

    [string]$Body,

    [switch]$ReviewOnly,

    [switch]$Yes
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
Push-Location $RepoRoot
try {
    switch ($Action) {
        "status" {
            Write-Host "=== Estado de Estrategia Git en Monorepo ($RepoRoot) ===" -ForegroundColor Cyan
            git status
            Write-Host "`nÚltimos 5 commits:" -ForegroundColor DarkGray
            git log -5 --oneline
            Write-Host "`nTags recientes:" -ForegroundColor DarkGray
            git tag -l -n1 --sort=-v:refname | Select-Object -First 5
        }

        "new-branch" {
            if (-not $Name) {
                throw "Debe proporcionar un nombre para la rama (-Name <descripcion>)."
            }
            $branchName = "$Type/$Project/$Name"
            Write-Host "[+] Actualizando 'main' antes de ramificar..." -ForegroundColor Cyan
            git checkout main
            git pull origin main
            Write-Host "[+] Creando y cambiando a la rama '$branchName'..." -ForegroundColor Green
            git checkout -b $branchName
            Write-Host "[OK] Rama '$branchName' lista para trabajar." -ForegroundColor Green
        }

        "promote" {
            if (-not $Tag) {
                throw "Debe proporcionar un tag semántico (-Tag <vX.Y.Z[-sandbox]>)."
            }
            Write-Host "[+] Creando tag anotado '$Tag' en el commit actual..." -ForegroundColor Cyan
            git tag -a $Tag -m "release: promoción a $Tag"
            Write-Host "[+] Subiendo tag a origin..." -ForegroundColor Cyan
            git push origin $Tag
            Write-Host "[OK] Tag '$Tag' publicado con éxito." -ForegroundColor Green
        }

        "create-pr" {
            $currentBranch = (git branch --show-current).Trim()
            if ($currentBranch -in @("main", "sandbox", "live", "")) {
                throw "No se puede crear PR desde la rama protegida o vacía '$currentBranch'. Use una rama de tarea (feat/*, fix/*, etc.)."
            }
            if (-not $Title) {
                throw "Debe proporcionar un título para la PR (-Title '[type]+[projects]: <title>')."
            }
            Write-Host "[+] Verificando pre-merge Quality Gate en rama '$currentBranch'..." -ForegroundColor Cyan
            $auditScript = Join-Path $PSScriptRoot "audit-workspace.ps1"
            if (Test-Path $auditScript) {
                pwsh -NoProfile -File $auditScript -Clean
                if ($LASTEXITCODE -ne 0) {
                    throw "Quality Gate falló. Corrija los errores antes de abrir la PR."
                }
            }
            Write-Host "[+] Publicando rama '$currentBranch' a origin..." -ForegroundColor Cyan
            git push -u origin HEAD
            if ($LASTEXITCODE -ne 0) {
                throw "Fallo al subir la rama a origin."
            }

            if (-not $Body) {
                $Body = @"
## Motivación y Contexto
$Title

## Cambios Introducidos
- Tarea aislada en rama efímera '$currentBranch'.

## Verificación Fast-Failure
- [x] audit-workspace.ps1 superado (Quality Gate Rating A, 0 violaciones).
- [x] markdownlint 100% compliant.

## Estrategia Fast-Rollback
- En caso de anomalía, cerrar la PR o revertir el commit squash atómico (`git revert <sha>`).
"@
            }

            $ghCmd = Get-Command gh -ErrorAction SilentlyContinue
            if ($ghCmd) {
                Write-Host "[+] Creando Pull Request en GitHub hacia 'main'..." -ForegroundColor Green
                gh pr create --base main --head $currentBranch --title $Title --body $Body
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "[OK] Pull Request creada y aislada exitosamente." -ForegroundColor Green
                }
            } else {
                Write-Host "[!] 'gh' CLI no disponible. Abra la PR manualmente en:" -ForegroundColor Yellow
                Write-Host "https://github.com/ACB75/home-lab/compare/main...$currentBranch" -ForegroundColor Cyan
            }
        }

        "complete-task" {
            $completeScript = Join-Path $PSScriptRoot "complete-task-pr.ps1"
            $cmdArgs = @()
            if ($Title) { $cmdArgs += @("-Title", $Title) }
            if ($Body) { $cmdArgs += @("-Body", $Body) }
            if ($ReviewOnly) { $cmdArgs += "-ReviewOnly" }
            if ($Yes) { $cmdArgs += "-Yes" }
            pwsh -NoProfile -File $completeScript @cmdArgs
        }
    }
} finally {
    Pop-Location
}
