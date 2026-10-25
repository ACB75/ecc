---
name: portal-sync
description: Audit and synchronize /portal catalog with Traefik routes, Docker services, and Split-DNS hosts upon infra/net changes.
metadata:
  origin: ECC-AGY
---

# Portal Synchronization Skill

Operational workflow to audit, synchronize, and verify the centralized service catalog (`/portal` and `/?format=json`) served by `cluster/cmd/server/main.go` whenever changes occur in infrastructure (`docker-compose*.yml`, `traefik/dynamic/*.yml`) or networking (`Corefile`, `adguard`, port allocations).

## When to Use

Invoke this skill:
- Whenever any container or service is added, modified, or removed in Docker Compose.
- Whenever Traefik routes, path prefixes, middlewares, or entrypoints are changed.
- Whenever Split-DNS records (`*.home.arpa`) are adjusted in CoreDNS or AdGuard Home.
- Before completing any task that touches `cluster`, `net`, or ingress configurations.

## Non-Negotiable Rules

1. **Zero Drift**: The `/portal` HTML cards and JSON endpoints in `main.go` must strictly mirror the active infrastructure routes, ports, and Split-DNS hosts.
2. **Immediate Verification**: Always execute `sync-portal.ps1 -Audit` (or `.sh --audit`) to prove zero drift and 100% reachability (exit code `0`).
3. **No Dead Links**: Every cataloged service must include valid local, Split-DNS, or direct port links.

## Commands

### Windows 11 (PowerShell)
```powershell
# Auditoría integral (estática y alcanzabilidad en vivo)
pwsh -NoProfile -File C:\Workspace\projects\home-lab\scripts\bin\cluster\sync-portal.ps1 -Audit

# Auditoría estática directa vía Python
python C:\Workspace\projects\home-lab\scripts\cluster\portal_sync.py --audit

# Auditoría en formato JSON
python C:\Workspace\projects\home-lab\scripts\cluster\portal_sync.py --json
```

### Linux / Debian 12 (Bash)
```bash
/mnt/c/Workspace/projects/home-lab/scripts/bin/cluster/sync-portal.sh --audit
```
