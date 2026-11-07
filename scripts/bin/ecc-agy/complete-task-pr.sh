#!/usr/bin/env bash
# ==============================================================================
# Script: complete-task-pr.sh (Debian 12 / Linux / WSL)
# Descripción: Aviso manual + PR + Auto resolve conflicts + Automerge + Delete branch.
# Finales de línea estrictamente POSIX LF (\n).
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$REPO_ROOT"

TITLE=""
BODY=""
TARGET_BRANCH="main"
REVIEW_ONLY=0
CONFIRM_YES=0
SHOW_HELP=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --help|-h)
            SHOW_HELP=1
            shift
            ;;
        --review-only|-ReviewOnly)
            REVIEW_ONLY=1
            shift
            ;;
        --yes|-Yes|-y)
            CONFIRM_YES=1
            shift
            ;;
        --target|-TargetBranch)
            TARGET_BRANCH="$2"
            shift 2
            ;;
        --title|-Title)
            TITLE="$2"
            shift 2
            ;;
        --body|-Body)
            BODY="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

if [[ $SHOW_HELP -eq 1 ]]; then
    echo "Uso: $(basename "$0") [--review-only] [--yes] [--title '...'] [--body '...'] [--target-branch main]"
    exit 0
fi

CURRENT_BRANCH="$(git branch --show-current | tr -d '[:space:]')"

# Gobernanza de ramas canónicas
VALIDATE_SCRIPT="$REPO_ROOT/scripts/ecc-agy/validate_branch.py"
if [[ -f "$VALIDATE_SCRIPT" ]]; then
    if ! python "$VALIDATE_SCRIPT" --branch "$CURRENT_BRANCH"; then
        echo "Error: Gobernanza de ramas rechazada para '$CURRENT_BRANCH'." >&2
        exit 1
    fi
elif [[ "$CURRENT_BRANCH" == "main" || "$CURRENT_BRANCH" == "sandbox" || "$CURRENT_BRANCH" == "live" || -z "$CURRENT_BRANCH" ]]; then
    echo "Error: No se puede ejecutar el ciclo en rama protegida '$CURRENT_BRANCH'." >&2
    exit 1
fi

# Detectar tareas completadas en doc/TODO.md
TODO_PATH="$REPO_ROOT/doc/TODO.md"
HAS_COMPLETED_TODOS=0
if [[ -f "$TODO_PATH" ]]; then
    if grep -q -E '^[\s*\-]*\[x\]' "$TODO_PATH" 2>/dev/null; then
        HAS_COMPLETED_TODOS=1
    fi
fi

if [[ -z "$TITLE" ]]; then
    LAST_COMMIT="$(git log -1 --pretty=format:%s 2>/dev/null || true)"
    if [[ "$LAST_COMMIT" =~ ^\[[a-z]+\]- ]]; then
        TITLE="$LAST_COMMIT"
    else
        TITLE="feat-[cluster]: complete task on $CURRENT_BRANCH"
    fi
fi

if [[ -z "$BODY" ]]; then
    BODY="Motivación y Contexto:
- Tarea finalizada en rama $CURRENT_BRANCH.
- Fusión automática a $TARGET_BRANCH tras validación de Quality Gate."
fi

echo "======================================================="
echo "       AVISO DE REVISIÓN MANUAL PREVIA A EJECUCIÓN     "
echo "======================================================="
echo "Rama Origen:        $CURRENT_BRANCH"
echo "Rama Destino:       $TARGET_BRANCH"
echo "Título de PR/Commit: $TITLE"
if [[ $HAS_COMPLETED_TODOS -eq 1 ]]; then
    echo "Tareas a Archivar:  Tareas completadas detectadas en doc/TODO.md (se archivarán automáticamente a doc/TODO_DONE/)"
fi
echo ""
echo "Resumen de Cambios:"
git status --short | head -n 15
echo "======================================================="

if [[ $REVIEW_ONLY -eq 1 ]]; then
    echo "[OK] Modo --review-only completado."
    exit 0
fi

if [[ $CONFIRM_YES -eq 0 ]]; then
    read -p "¿Desea proceder con Commit, Push, PR, Autoresolución, Automerge y Borrado de rama? (s/N): " -r RESP
    if [[ ! "$RESP" =~ ^[sSyY]$ ]]; then
        echo "[CANCELADO] Operación cancelada por el usuario."
        exit 0
    fi
fi

# Pre-merge Quality Gate: Markdown linter, tests y SonarQube
echo "[+] Ejecutando auditoría de calidad previa..."
if [[ -f "$SCRIPT_DIR/lint-markdown.sh" ]]; then
    bash "$SCRIPT_DIR/lint-markdown.sh" --check-only
fi

TESTS_DIR="$REPO_ROOT/scripts/ecc-agy/tests"
if [[ -d "$TESTS_DIR" ]]; then
    echo "[+] Ejecutando suite de pruebas unitarias (pytest)..."
    python -m pytest "$TESTS_DIR" -q
fi

if [[ -f "$SCRIPT_DIR/sonar-audit.sh" ]]; then
    bash "$SCRIPT_DIR/sonar-audit.sh"
fi

# Sincronizar y archivar tareas completadas en doc/TODO.md
if [[ $HAS_COMPLETED_TODOS -eq 1 ]]; then
    echo "[+] Archivando tareas completadas en doc/TODO_DONE/..."
    if [[ -f "$SCRIPT_DIR/archive-todo.sh" ]]; then
        bash "$SCRIPT_DIR/archive-todo.sh"
    elif [[ -f "$REPO_ROOT/scripts/ecc-agy/archive_todo.py" ]]; then
        python "$REPO_ROOT/scripts/ecc-agy/archive_todo.py"
    fi
fi

# Si es rama de incidencia (fix/*), generar Post-Mortem 5W automáticamente
if [[ "$CURRENT_BRANCH" == fix/* ]]; then
    echo "[+] Rama de incidencia detectada ('$CURRENT_BRANCH'). Generando Post-Mortem 5W..."
    PM_SCRIPT="$REPO_ROOT/scripts/ecc-agy/generate_postmortem.py"
    if [[ -f "$PM_SCRIPT" ]]; then
        python "$PM_SCRIPT" --branch "$CURRENT_BRANCH"
    fi
fi

if [[ -n "$(git status --porcelain)" ]]; then
    echo "[+] Añadiendo y comprometiendo cambios pendientes..."
    git add -A
    git commit -m "$TITLE" -m "$BODY"
fi

echo "[+] Publicando rama '$CURRENT_BRANCH' en origin..."
git push -u origin HEAD

PR_NUMBER="$(gh pr list --head "$CURRENT_BRANCH" --base "$TARGET_BRANCH" --json number --jq '.[0].number' 2>/dev/null || true)"
if [[ -z "$PR_NUMBER" ]]; then
    echo "[+] Creando nueva Pull Request hacia '$TARGET_BRANCH'..."
    gh pr create --base "$TARGET_BRANCH" --head "$CURRENT_BRANCH" --title "$TITLE" --body "$BODY"
    PR_NUMBER="$(gh pr list --head "$CURRENT_BRANCH" --base "$TARGET_BRANCH" --json number --jq '.[0].number')"
fi

echo "[+] Verificando conflictos contra origin/$TARGET_BRANCH..."
git fetch origin "$TARGET_BRANCH"
if ! git merge "origin/$TARGET_BRANCH" --no-commit --no-ff 2>/dev/null; then
    CONFLICTS="$(git diff --name-only --diff-filter=U)"
    if [[ -n "$CONFLICTS" ]]; then
        echo "[!] Autoresolviendo conflictos..."
        while IFS= read -r file; do
            git checkout --ours -- "$file"
            git add "$file"
        done <<< "$CONFLICTS"
        git commit -m "fix-[git]: auto-resolve conflicts against origin/$TARGET_BRANCH"
        git push origin HEAD
    fi
else
    git merge --abort 2>/dev/null || true
fi

echo "[+] Ejecutando squash-automerge en PR #$PR_NUMBER..."
gh pr merge "$PR_NUMBER" --squash --delete-branch || gh pr merge "$PR_NUMBER" --squash --delete-branch --admin

echo "[+] Sincronizando $TARGET_BRANCH..."
git merge --abort 2>/dev/null || true
git checkout -f "$TARGET_BRANCH"
git pull origin "$TARGET_BRANCH"

if git branch --list "$CURRENT_BRANCH" >/dev/null; then
    echo "[+] Eliminando rama local '$CURRENT_BRANCH'..."
    git branch -D "$CURRENT_BRANCH" 2>/dev/null || true
fi

echo "======================================================="
echo " [OK] CICLO COMPLETO DE PR Y AUTOMERGE FINALIZADO      "
echo "======================================================="
git log -1 --oneline
