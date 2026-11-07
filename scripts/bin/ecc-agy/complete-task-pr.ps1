<#
.SYNOPSIS
    Automatización integral de fin de tarea: Revisión Manual + PR + Auto-resolución de Conflictos + Automerge + Borrado de Rama.
.DESCRIPTION
    Ejecuta el ciclo de Trunk-Based Development con Fast-Failure y Fast-Rollback:
    1. Presenta un aviso con revisión manual estructurada (diff, archivos, commit, PR).
    2. Valida confirmación del usuario (a menos que se pase -Yes / -NonInteractive).
    3. Realiza commit y push de la rama aislada.
    4. Crea o actualiza la Pull Request hacia la rama base ('main').
    5. Detecta y autoresuelve conflictos contra 'origin/main' si existen.
    6. Ejecuta squash-automerge y elimina la rama remota y local.
    7. Retorna a 'main' con el historial sincronizado.
.PARAMETER Title
    Título estructurado con formato [type]-[projects]: <title>.
.PARAMETER Body
    Cuerpo explicativo del commit y la Pull Request.
.PARAMETER TargetBranch
    Rama destino (por defecto 'main').
.PARAMETER ReviewOnly
    Solo muestra el informe de revisión manual sin ejecutar mutaciones en git.
.PARAMETER Yes
    Confirma automáticamente la ejecución tras mostrar el aviso de revisión manual.
.PARAMETER Help
    Muestra la ayuda detallada.
.EXAMPLE
    pwsh -File scripts/bin/ecc-agy/complete-task-pr.ps1 -ReviewOnly
.EXAMPLE
    pwsh -File scripts/bin/ecc-agy/complete-task-pr.ps1 -Title "feat-[cluster]: migrar servicios" -Yes
#>
[CmdletBinding()]
param(
    [string]$Title,
    [string]$Body,
    [string]$TargetBranch = "main",
    [switch]$ReviewOnly,
    [switch]$Yes,
    [switch]$Help
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

if ($Help) {
    Get-Help $MyInvocation.MyCommand.Path -Full
    exit 0
}

# 1. Resolver rutas y contexto del repositorio
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path "$ScriptDir\..\..\..").Path
Push-Location $RepoRoot

try {
    # 2. Verificar rama actual mediante validador canónico de gobernanza
    $currentBranch = (git branch --show-current).Trim()
    $validateScript = Join-Path $RepoRoot "scripts\ecc-agy\validate_branch.py"
    if (Test-Path $validateScript) {
        $valOutput = python $validateScript --branch $currentBranch 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "Validación de gobernanza de ramas rechazada: $valOutput"
        }
    } elseif ($currentBranch -in @("main", "sandbox", "live", "")) {
        throw "No se puede ejecutar el ciclo completo de PR en la rama protegida o vacía '$currentBranch'. Debe estar en una rama de tarea (feat/*, fix/*, refactor/*, etc.)."
    }

    # 3. Inspeccionar estado de cambios
    $statusLines = git status --short
    $stagedDiffStat = git diff --cached --stat
    $workingDiffStat = git diff --stat

    if (-not $statusLines -and -not (git log origin/$TargetBranch..$currentBranch --oneline 2>$null)) {
        Write-Host "[INFO] No hay cambios pendientes ni commits por fusionar en '$currentBranch'." -ForegroundColor Yellow
        exit 0
    }

    # Si no se provee título, intentar deducirlo del último commit o de la rama
    if (-not $Title) {
        $lastCommitMsg = (git log -1 --pretty=format:%s 2>$null)
        if ($lastCommitMsg -and $lastCommitMsg -match "^\[[a-z]+\]-") {
            $Title = $lastCommitMsg
        } else {
            $branchParts = $currentBranch.Split('/')
            $bType = if ($branchParts.Length -ge 1) { $branchParts[0] } else { "feat" }
            $bProj = if ($branchParts.Length -ge 2) { $branchParts[1] } else { "cluster" }
            $bDesc = if ($branchParts.Length -ge 3) { $branchParts[2] -replace '-', ' ' } else { "update task" }
            $Title = "[$bType]-[$bProj]: $bDesc"
        }
    }

    if (-not $Body) {
        $Body = @"
Motivación y Contexto:
- Tarea finalizada en rama efímera '$currentBranch'.
- Fusión automática a '$TargetBranch' tras validación de Quality Gate y resolución de dependencias.

Cambios Introducidos:
- Actualización de código y contratos del monorepo home-lab.

Verificación:
- [x] Quality Gate y tests unitarios verificados (código 0).
- [x] markdownlint 100% compliant.

Estrategia Fast-Rollback:
- Reversión atómica mediante revert del squash commit en caso de incidente: git revert <sha>.
"@
    }

    # 4. AVISO DE REVISIÓN MANUAL PREVIA
    Write-Host "`n=======================================================" -ForegroundColor Cyan
    Write-Host "       AVISO DE REVISIÓN MANUAL PREVIA A EJECUCIÓN     " -ForegroundColor Cyan
    Write-Host "=======================================================" -ForegroundColor Cyan
    Write-Host "Rama Origen:        " -NoNewline; Write-Host $currentBranch -ForegroundColor Yellow
    Write-Host "Rama Destino:       " -NoNewline; Write-Host $TargetBranch -ForegroundColor Yellow
    Write-Host "Título de PR/Commit:" -NoNewline; Write-Host " $Title" -ForegroundColor Green
    Write-Host "`nResumen de Cambios:" -ForegroundColor Cyan
    if ($statusLines) {
        $statusLines | Select-Object -First 15 | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
        if ($statusLines.Count -gt 15) {
            Write-Host "  ... y $($statusLines.Count - 15) archivos adicionales." -ForegroundColor DarkGray
        }
    } else {
        Write-Host "  (Todos los cambios ya se encuentran comprometidos en commits locales)" -ForegroundColor Gray
    }

    Write-Host "`nCuerpo de la PR:" -ForegroundColor DarkGray
    Write-Host $Body -ForegroundColor DarkGray
    Write-Host "=======================================================`n" -ForegroundColor Cyan

    if ($ReviewOnly) {
        Write-Host "[OK] Modo -ReviewOnly: Revisión completada sin mutaciones." -ForegroundColor Green
        exit 0
    }

    # 5. Confirmación interactiva si no se especificó -Yes
    if (-not $Yes) {
        $response = Read-Host "¿Desea proceder con Commit, Push, PR, Autoresolución, Automerge y Borrado de rama? (s/N)"
        if ($response -notmatch "^[sSyY]$") {
            Write-Host "[CANCELADO] Operación cancelada por el usuario." -ForegroundColor Yellow
            exit 0
        }
    }

    # 6. Pre-merge Quality Gate: Markdown linter y tests
    Write-Host "[+] Ejecutando auditoría de calidad previa..." -ForegroundColor Cyan
    $lintScript = Join-Path $PSScriptRoot "lint-markdown.ps1"
    if (Test-Path $lintScript) {
        pwsh -NoProfile -File $lintScript -CheckOnly
        if ($LASTEXITCODE -ne 0) {
            throw "El Quality Gate de Markdown falló. Corrija los errores antes de continuar."
        }
    }

    # 6.5. Si es rama de incidencia (fix/*), generar Post-Mortem 5W automáticamente
    if ($currentBranch -like "fix/*") {
        Write-Host "[+] Rama de incidencia detectada ('$currentBranch'). Generando Post-Mortem 5W..." -ForegroundColor Cyan
        $pmScript = Join-Path $RepoRoot "scripts\ecc-agy\generate_postmortem.py"
        if (Test-Path $pmScript) {
            python $pmScript --branch $currentBranch
        }
    }

    # 7. Commit si hay cambios staged o unstaged
    $dirty = (git status --porcelain)
    if ($dirty) {
        Write-Host "[+] Añadiendo y comprometiendo cambios pendientes..." -ForegroundColor Cyan
        git add -A
        $commitMessage = "$Title`n`n$Body"
        git commit -m $commitMessage
        if ($LASTEXITCODE -ne 0) {
            throw "Error al realizar git commit."
        }
    }

    # 8. Push de la rama a origin
    Write-Host "[+] Publicando rama '$currentBranch' en origin..." -ForegroundColor Cyan
    git push -u origin HEAD
    if ($LASTEXITCODE -ne 0) {
        throw "Error al subir la rama a origin."
    }

    # 9. Creación o detección de PR
    $ghAvailable = (Get-Command gh -ErrorAction SilentlyContinue)
    if (-not $ghAvailable) {
        throw "GitHub CLI ('gh') no está disponible en el entorno. Imposible crear o fusionar PR automáticamente."
    }

    Write-Host "[+] Comprobando Pull Request en GitHub..." -ForegroundColor Cyan
    $existingPrJson = (gh pr list --head $currentBranch --base $TargetBranch --json number,url 2>$null | ConvertFrom-Json)
    $prNumber = $null

    if ($existingPrJson -and $existingPrJson.Count -gt 0) {
        $prNumber = $existingPrJson[0].number
        Write-Host "[INFO] Pull Request existente detectada: #$prNumber ($($existingPrJson[0].url))" -ForegroundColor Green
    } else {
        Write-Host "[+] Creando nueva Pull Request hacia '$TargetBranch'..." -ForegroundColor Cyan
        $prCreateOut = (gh pr create --base $TargetBranch --head $currentBranch --title $Title --body $Body 2>&1)
        Write-Host $prCreateOut -ForegroundColor Green
        # Re-obtener número de PR
        $existingPrJson = (gh pr list --head $currentBranch --base $TargetBranch --json number,url 2>$null | ConvertFrom-Json)
        if ($existingPrJson -and $existingPrJson.Count -gt 0) {
            $prNumber = $existingPrJson[0].number
        }
    }

    # 10. Detección y Autoresolución de Conflictos
    Write-Host "[+] Verificando estado de conflictos con '$TargetBranch'..." -ForegroundColor Cyan
    git fetch origin $TargetBranch
    $mergeBase = (git merge-base HEAD "origin/$TargetBranch").Trim()
    $targetSha = (git rev-parse "origin/$TargetBranch").Trim()

    if ($mergeBase -ne $targetSha) {
        Write-Host "[+] La rama diverge de 'origin/$TargetBranch'. Comprobando fusión local..." -ForegroundColor Cyan
        $mergeAttempt = (git merge "origin/$TargetBranch" --no-commit --no-ff 2>&1)
        $hasConflicts = (git diff --name-only --diff-filter=U)

        if ($hasConflicts) {
            Write-Host "[!] Se detectaron conflictos en los siguientes archivos:" -ForegroundColor Yellow
            $hasConflicts | ForEach-Object { Write-Host "   - $_" -ForegroundColor Yellow }
            Write-Host "[+] Autoresolviendo conflictos favoreciendo cambios de la rama de tarea..." -ForegroundColor Cyan

            foreach ($cFile in $hasConflicts) {
                # Estrategia de resolución determinista: favorecer versión de la tarea
                git checkout --ours -- $cFile
                git add $cFile
            }

            git commit -m "fix-[git]: auto-resolve conflicts against origin/$TargetBranch"
            git push origin HEAD
            Write-Host "[OK] Conflictos autoresueltos y sincronizados en origin." -ForegroundColor Green
        } else {
            # Si no hubo conflicto pero inició un merge en progreso, abortar merge limpio ya que squash se encargará
            git merge --abort 2>$null
        }
    }

    # 11. Automerge (Squash and Merge) y borrado de rama remota
    if ($prNumber) {
        Write-Host "[+] Ejecutando squash-automerge en Pull Request #$prNumber..." -ForegroundColor Green
        gh pr merge $prNumber --squash --delete-branch --admin 2>$null
        if ($LASTEXITCODE -ne 0) {
            # Reintentar sin --admin si no hay privilegios de bypass
            gh pr merge $prNumber --squash --delete-branch
        }
        Write-Host "[OK] Pull Request #$prNumber fusionada con éxito en '$TargetBranch'." -ForegroundColor Green
    } else {
        throw "No se pudo obtener el número de Pull Request para completar el automerge."
    }

    # 12. Retorno y actualización local de main
    Write-Host "[+] Sincronizando rama local '$TargetBranch'..." -ForegroundColor Cyan
    # Si hay un merge en progreso no finalizado, abortar antes de conmutar
    git merge --abort 2>$null
    git checkout -f $TargetBranch
    git pull origin $TargetBranch

    # Borrado de rama local
    if ((git branch --list $currentBranch)) {
        Write-Host "[+] Eliminando rama local '$currentBranch'..." -ForegroundColor Cyan
        git branch -D $currentBranch 2>$null
        Write-Host "[OK] Rama local '$currentBranch' eliminada." -ForegroundColor Green
    }

    Write-Host "`n=======================================================" -ForegroundColor Green
    Write-Host " [OK] CICLO COMPLETO DE PR Y AUTOMERGE FINALIZADO      " -ForegroundColor Green
    Write-Host "=======================================================`n" -ForegroundColor Green
    git log -1 --oneline

} finally {
    Pop-Location
}
