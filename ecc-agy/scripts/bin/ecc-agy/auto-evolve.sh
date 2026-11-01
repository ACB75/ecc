#!/usr/bin/env bash
# ==============================================================================
# Script: auto-evolve.sh (Debian 12 / Linux / WSL)
# Descripción: Harness de autodescubrimiento y autoevolución para home-lab.
# Finales de línea estrictamente POSIX LF (\n).
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
CLI_SCRIPT="$ROOT_DIR/scripts/plugin/ecc-agy/evolution/cli.py"

if [[ ! -f "$CLI_SCRIPT" ]]; then
    echo "Error: No se encontró el módulo CLI en $CLI_SCRIPT" >&2
    exit 1
fi

ARGS=()
SHOW_HELP=0

for arg in "$@"; do
    case "$arg" in
        --help|-h|-Help)
            SHOW_HELP=1
            ;;
        --discover|-d|-Discover)
            ARGS+=("--discover")
            ;;
        --write|-w|-Write)
            ARGS+=("--write")
            ;;
        --dry-run|-DryRun)
            ARGS+=("--dry-run")
            ;;
        --json|-Json)
            ARGS+=("--json")
            ;;
        --limit|-l|-Limit)
            shift || true
            ARGS+=("--limit" "$1")
            ;;
        --tier|-t|-Tier)
            shift || true
            ARGS+=("--tier" "$1")
            ;;
        *)
            ARGS+=("$arg")
            ;;
    esac
done

if [[ $SHOW_HELP -eq 1 ]]; then
    echo "Uso: $(basename "$0") [--discover] [--dry-run] [--write] [--limit N] [--tier TYPE] [--json] [--help]"
    exit 0
fi

python3 "$CLI_SCRIPT" "${ARGS[@]}"
