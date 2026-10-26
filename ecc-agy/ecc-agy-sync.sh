#!/usr/bin/env bash
# ecc-agy-sync.sh - Sincronizador de ECC-AGY para Linux (WSL Debian, Arch Linux, Debian 12 Server)
set -euo pipefail

PHASE="${1:-status}"
TARGET_DIR="${2:-$HOME/.gemini/config/plugins/ecc-agy}"
ECC_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$TARGET_DIR/skills" "$TARGET_DIR/agents" "$TARGET_DIR/rules"

case "$PHASE" in
  status)
    echo "=== ECC-AGY Status ($TARGET_DIR) ==="
    echo "Skills ($(find "$TARGET_DIR/skills" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)):"
    ls -1 "$TARGET_DIR/skills" 2>/dev/null || true
    echo "Agents ($(find "$TARGET_DIR/agents" -maxdepth 1 -name '*.md' 2>/dev/null | wc -l)):"
    ls -1 "$TARGET_DIR/agents" 2>/dev/null || true
    exit 0
    ;;
  generic)
    SKILLS=(tdd-workflow search-first verification-loop security-review coding-standards git-workflow conventional-commit-review architecture-decision-records error-handling docs-governance workspace-health-audit config-cleanup sonarqube-quality-gate)
    AGENTS=(planner.md architect.md tdd-guide.md code-reviewer.md security-reviewer.md build-error-resolver.md silent-failure-hunter.md refactor-cleaner.md doc-updater.md)
    ;;
  infra)
    SKILLS=(docker-patterns deployment-patterns kubernetes-patterns homelab-network-readiness homelab-network-setup homelab-pihole-dns homelab-vlan-segmentation homelab-wireguard-vpn network-config-validation network-interface-health netmiko-ssh-automation security-scan safety-guard)
    AGENTS=(homelab-architect.md network-architect.md network-config-reviewer.md network-troubleshooter.md)
    ;;
  kakebo)
    SKILLS=(springboot-patterns springboot-security springboot-tdd springboot-verification java-coding-standards angular-developer e2e-testing postgres-patterns database-migrations api-design sonarqube-quality-gate)
    AGENTS=(java-reviewer.md java-build-resolver.md typescript-reviewer.md database-reviewer.md e2e-runner.md)
    ;;
  cluster)
    SKILLS=(golang-patterns golang-testing docker-patterns kubernetes-patterns postgres-patterns latency-critical-systems data-throughput-accelerator benchmark-optimization-loop sonarqube-quality-gate)
    AGENTS=(go-reviewer.md go-build-resolver.md performance-optimizer.md database-reviewer.md)
    ;;
  token-hill)
    SKILLS=(python-patterns python-testing benchmark-optimization-loop sonarqube-quality-gate)
    AGENTS=(python-reviewer.md performance-optimizer.md)
    ;;
  *)
    echo "Uso: $0 {status|generic|infra|kakebo|cluster|token-hill} [target_dir]"
    exit 1
    ;;
esac

for s in "${SKILLS[@]}"; do
  if [ -d "$ECC_ROOT/skills/$s" ]; then
    rm -rf "$TARGET_DIR/skills/$s"
    cp -R "$ECC_ROOT/skills/$s" "$TARGET_DIR/skills/"
    echo "[+] Skill instalada ($PHASE): $s"
  fi
done

ECC_ROOT_ENV="$ECC_ROOT" TARGET_DIR_ENV="$TARGET_DIR" node -e '
const fs = require("fs");
const path = require("path");
const { adaptAntigravityAgent } = require(path.join(process.env.ECC_ROOT_ENV, "scripts/lib/install/antigravity-agent"));
const agents = process.argv.slice(1);
for (const a of agents) {
  const src = path.join(process.env.ECC_ROOT_ENV, "agents", a);
  const dst = path.join(process.env.TARGET_DIR_ENV, "agents", a);
  if (fs.existsSync(src)) {
    const raw = fs.readFileSync(src, "utf8");
    fs.writeFileSync(dst, adaptAntigravityAgent(raw, a), "utf8");
    console.log("[+] Agente adaptado:", a);
  }
}
' "${AGENTS[@]}"
