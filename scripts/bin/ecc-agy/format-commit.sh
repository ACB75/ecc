#!/usr/bin/env bash
# ==============================================================================
# format-commit.sh - Valida y formatea mensajes de commit bajo [type]+[projects]: <title>
# Entorno: Debian 12 / Linux / WSL
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
PY_SCRIPT="${WORKSPACE_ROOT}/scripts/ecc-agy/format_commit.py"

if [[ ! -f "${PY_SCRIPT}" ]]; then
    echo "[ERROR] No se encuentra el script ${PY_SCRIPT}" >&2
    exit 1
fi

python3 "${PY_SCRIPT}" "$@"
