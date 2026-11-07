#!/usr/bin/env bash
# ==============================================================================
# sonar-audit.sh - Auditoría estática SonarQube Quality Gate A
# Entorno: Debian 12 / Linux / WSL (POSIX LF)
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
PY_SCRIPT="${WORKSPACE_ROOT}/scripts/ecc-agy/sonar_audit.py"

if [[ ! -f "${PY_SCRIPT}" ]]; then
    echo "[ERROR] No se encuentra el script ${PY_SCRIPT}" >&2
    exit 1
fi

python3 "${PY_SCRIPT}" --root "${WORKSPACE_ROOT}" "$@"
