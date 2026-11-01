#!/usr/bin/env bash
# ==============================================================================
# Script: lint-markdown.sh (Debian 12 / Linux / WSL)
# Descripción: Audita y formatea Markdown leyendo .markdownlint.json del repositorio.
# Formatea automáticamente por defecto (--fix) e incluye TODO el repositorio y *TODO*.
# Finales de línea estrictamente POSIX LF (\n).
# ==============================================================================
set -euo pipefail

APPLY_FIX="1"
TARGET=""
ROOT_DIR=""

for arg in "$@"; do
    case "$arg" in
        --check-only|-CheckOnly|--check|-Check)
            APPLY_FIX="0"
            ;;
        --fix|-Fix)
            APPLY_FIX="1"
            ;;
        --root|-Root)
            shift || true
            ROOT_DIR="${1:-}"
            ;;
        *)
            TARGET="$arg"
            ;;
    esac
done

find_markdownlint_root() {
    local cur="$1"
    while [[ -n "$cur" && "$cur" != "/" && -d "$cur" ]]; do
        if [[ -f "$cur/.markdownlint.json" ]]; then
            echo "$cur"
            return 0
        fi
        local parent
        parent="$(dirname "$cur")"
        if [[ "$parent" == "$cur" ]]; then
            break
        fi
        cur="$parent"
    done
    if [[ -f "/.markdownlint.json" ]]; then
        echo "/"
        return 0
    fi
    return 1
}

if [[ -z "$ROOT_DIR" && -n "$TARGET" && -e "$TARGET" ]]; then
    target_dir="$(dirname "$(realpath "$TARGET")")"
    ROOT_DIR="$(find_markdownlint_root "$target_dir" || true)"
fi

if [[ -z "$ROOT_DIR" ]]; then
    ROOT_DIR="$(find_markdownlint_root "$(pwd)" || true)"
fi

if [[ -z "$ROOT_DIR" ]]; then
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    ROOT_DIR="$(find_markdownlint_root "$script_dir" || true)"
fi

if [[ -z "$ROOT_DIR" ]]; then
    ROOT_DIR="$(pwd)"
fi

CONFIG_FILE="$ROOT_DIR/.markdownlint.json"
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "ERROR: Configuración .markdownlint.json no encontrada en $CONFIG_FILE" >&2
    exit 1
fi

IGNORE_ARGS=(
    "--ignore" "**/node_modules/**"
    "--ignore" "**/.git/**"
    "--ignore" "**/.venv/**"
    "--ignore" "**/dist/**"
    "--ignore" "**/build/**"
)

TARGET_PATTERN=""
if [[ -z "$TARGET" ]]; then
    TARGET_PATTERN="**/*.md"
elif [[ -d "$TARGET" ]]; then
    TARGET_PATTERN="${TARGET%/}"'/**/*.md'
elif [[ "$TARGET" == *"*"* || "$TARGET" == *"?"* ]]; then
    if [[ "$TARGET" != *"/"* ]]; then
        if [[ "$TARGET" == *".md" ]]; then
            TARGET_PATTERN="**/*${TARGET}"
        else
            TARGET_PATTERN="**/*${TARGET}*.md"
        fi
        TARGET_PATTERN="${TARGET_PATTERN//\*\*/\*}"
    else
        TARGET_PATTERN="$TARGET"
    fi
else
    TARGET_PATTERN="$TARGET"
fi

MAX_PASSES=1
if [[ "$APPLY_FIX" == "1" ]]; then
    MAX_PASSES=3
fi

EXIT_CODE=0
for ((pass=1; pass<=MAX_PASSES; pass++)); do
    CMD_ARGS=("-c" "$CONFIG_FILE")
    if [[ "$APPLY_FIX" == "1" ]]; then
        CMD_ARGS+=("--fix")
    fi
    CMD_ARGS+=("${IGNORE_ARGS[@]}")
    CMD_ARGS+=("$TARGET_PATTERN")

    if npx --yes markdownlint-cli "${CMD_ARGS[@]}"; then
        EXIT_CODE=0
        break
    else
        EXIT_CODE=$?
    fi
done

if [[ $EXIT_CODE -eq 0 ]]; then
    echo "[OK] Todos los archivos Markdown cumplen con el estándar markdownlint."
else
    echo "[FAIL] Se detectaron errores de sintaxis o formato en Markdown."
fi

exit $EXIT_CODE
