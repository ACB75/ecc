#!/usr/bin/env bash
# ==============================================================================
# ECC Multi-Distribution Installer (Linux / WSL / macOS)
# Targets: claude | agy | homelab (alias to agy)
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-agy}"
DESTINATION="${2:-}"

echo "================================================================="
echo "                ECC MASTER MULTI-DISTRIBUTION INSTALLER          "
echo "================================================================="
echo "Target distribution: ${TARGET}"

if [ "${TARGET}" = "homelab" ]; then
  echo "[i] Note: 'homelab' has been unified into 'ecc-agy'. Deploying ecc-agy..."
  TARGET="agy"
fi

case "${TARGET}" in
  claude)
    SOURCE_DIR="${SCRIPT_DIR}/ecc-claude"
    DEST="${DESTINATION:-$(pwd)}"
    echo "[+] Deploying Claude Code boilerplates to: ${DEST}"
    cp -f "${SOURCE_DIR}/CLAUDE.md" "${DEST}/"
    cp -rf "${SOURCE_DIR}/.claude" "${DEST}/"
    echo "[✓] Claude Code boilerplates installed successfully."
    ;;
  agy)
    SOURCE_DIR="${SCRIPT_DIR}/ecc-agy"
    DEST="${DESTINATION:-${HOME}/.gemini/config/plugins/ecc-agy}"
    echo "[+] Deploying unified Antigravity plugin to: ${DEST}"
    mkdir -p "${DEST}"
    cp -rf "${SOURCE_DIR}"/* "${DEST}/"
    echo "[✓] Unified ecc-agy plugin installed successfully."
    ;;
  *)
    echo "Error: Unknown target '${TARGET}'. Use 'claude' or 'agy'." >&2
    exit 1
    ;;
esac

echo "================================================================="
echo "Installation complete."
