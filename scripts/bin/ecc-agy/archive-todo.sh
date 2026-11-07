#!/usr/bin/env bash
# ==============================================================================
# archive-todo.sh - Archiva tareas completadas de doc/TODO.md a doc/TODO_DONE/
# Entorno: Debian 12 / Linux / WSL (POSIX LF)
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
PY_SCRIPT="${WORKSPACE_ROOT}/scripts/ecc-agy/archive_todo.py"

if [[ ! -f "${PY_SCRIPT}" ]]; then
    echo "[ERROR] No se encuentra el script ${PY_SCRIPT}" >&2
    exit 1
fi

python3 "${PY_SCRIPT}" --todo "${WORKSPACE_ROOT}/doc/TODO.md" --done-dir "${WORKSPACE_ROOT}/doc/TODO_DONE" "$@"

if [[ -f "${SCRIPT_DIR}/lint-markdown.sh" ]]; then
    bash "${SCRIPT_DIR}/lint-markdown.sh" --fix "${WORKSPACE_ROOT}/doc/TODO_DONE" >/dev/null 2>&1 || true
    bash "${SCRIPT_DIR}/lint-markdown.sh" --fix "${WORKSPACE_ROOT}/doc/TODO.md" >/dev/null 2>&1 || true
fi
