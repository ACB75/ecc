#!/usr/bin/env bash
# ==============================================================================
# ECC-AECB Multi-Distribution Installer (Linux / WSL / macOS)
# Targets: claude | agy | homelab
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-agy}"
DESTINATION="${2:-}"

echo "================================================================="
echo "             ECC-AECB MASTER MULTI-DISTRIBUTION INSTALLER         "
echo "================================================================="
echo "Target distribution: ${TARGET}"

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
    echo "[+] Deploying agnostic Antigravity plugin to: ${DEST}"
    mkdir -p "${DEST}"
    cp -rf "${SOURCE_DIR}"/* "${DEST}/"
    echo "[✓] Agnostic ecc-agy plugin installed successfully."
    ;;
  homelab)
    SOURCE_DIR="${SCRIPT_DIR}/ecc-agy-homelab"
    DEST="${DESTINATION:-${HOME}/.gemini/config/plugins/ecc-agy}"
    echo "[+] Deploying specialized Home-Lab fork to: ${DEST}"
    mkdir -p "${DEST}"
    cp -rf "${SOURCE_DIR}"/* "${DEST}/"
    echo "[✓] Specialized ecc-agy-homelab installed successfully."
    ;;
  *)
    echo "Error: Unknown target '${TARGET}'. Use 'claude', 'agy', or 'homelab'." >&2
    exit 1
    ;;
esac

echo "================================================================="
echo "Installation complete."
