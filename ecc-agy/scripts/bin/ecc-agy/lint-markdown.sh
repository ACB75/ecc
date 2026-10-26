#!/usr/bin/env bash
# ==============================================================================
# Script: lint-markdown.sh (Debian 12 / Linux / WSL)
# Descripción: Audita y formatea Markdown leyendo .markdownlint.json del repositorio.
# ==============================================================================
set -euo pipefail

FIX_FLAG=""
TARGET=""
ROOT_DIR=""

for arg in "$@"; do
    case "$arg" in
        --fix|-Fix)
            FIX_FLAG="--fix"
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

ARGS=("-c" "$CONFIG_FILE" "--ignore" "**/TODO_DONE/**" "--ignore" "**/node_modules/**")

if [[ -n "$FIX_FLAG" ]]; then
    ARGS+=("$FIX_FLAG")
fi

if [[ -n "$TARGET" ]]; then
    ARGS+=("$TARGET")
else
    ARGS+=("$ROOT_DIR/doc/**/*.md" "$ROOT_DIR/AGENTS.md")
fi

echo "Ejecutando markdownlint (DavidAnson) con configuración en $CONFIG_FILE..."
npx --yes markdownlint-cli "${ARGS[@]}"
