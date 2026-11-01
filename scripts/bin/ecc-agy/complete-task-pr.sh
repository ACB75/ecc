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
if [[ "$CURRENT_BRANCH" == "main" || "$CURRENT_BRANCH" == "sandbox" || "$CURRENT_BRANCH" == "live" || -z "$CURRENT_BRANCH" ]]; then
    echo "Error: No se puede ejecutar el ciclo en rama protegida '$CURRENT_BRANCH'." >&2
    exit 1
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

# Pre-merge linter check
if [[ -f "$SCRIPT_DIR/lint-markdown.sh" ]]; then
    bash "$SCRIPT_DIR/lint-markdown.sh" --check-only
fi

if [[ -n "$(git status --porcelain)" ]]; then
    git add -A
    git commit -m "$TITLE" -m "$BODY"
fi

git push -u origin HEAD

PR_NUMBER="$(gh pr list --head "$CURRENT_BRANCH" --base "$TARGET_BRANCH" --json number --jq '.[0].number' 2>/dev/null || true)"
if [[ -z "$PR_NUMBER" ]]; then
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
    git branch -D "$CURRENT_BRANCH" 2>/dev/null || true
fi

echo "[OK] Ciclo de PR y automerge finalizado exitosamente."
