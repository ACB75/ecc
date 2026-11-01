---
name: sync-microservice-sdk
description: "Synchronize home-lab-sdk clients, types, and tests whenever microservices in services/ or cluster/ modify public contracts or APIs."
metadata:
  origin: home-lab
---

# Microservice & home-lab-sdk Synchronization Skill

Operational workflow to audit, synchronize, and verify the polyglot multi-language SDK (`home-lab-sdk/`) whenever changes occur in microservice contracts, routes, DTOs, SQL schemas, or auth mechanisms.

## When to Use

Invoke this skill:

- Whenever any endpoint, route, handler, controller, or DTO is modified in `services/<service>/` or `cluster/`.
- Whenever authentication claims, tokens, or POSIX attributes change in WhoIAm (`services/whoiam`).
- Whenever authorization matrices or roles change in Citadel (`services/citadel`).
- Whenever multi-tenant contexts or headers (`X-Tenant-ID`) are updated.
- Before committing changes that touch `services/` or `cluster/`.

## Non-Negotiable Rules

1. **Zero Contract Drift**: The SDK in `home-lab-sdk/` must strictly mirror the active microservice contracts across all consuming stacks (TypeScript/Angular, Java 25, Go).
2. **Immediate Test Verification**: Always execute `audit-sdk-sync.ps1 -Mode working -RunTests` (or `.sh`) to prove 100% test pass rate (exit code `0`).
3. **Commit Atomicity**: Changes in microservices and their corresponding SDK updates must be committed in the same atomic commit.

## Operational Workflow

```mermaid
flowchart LR
    Diff["1. Detectar Cambios en services/"] --> Audit["2. Ejecutar audit-sdk-sync.ps1"]
    Audit --> Target["3. Identificar Stacks Afectados (TS, Java, Go)"]
    Target --> Update["4. Actualizar Clientes y DTOs en home-lab-sdk"]
    Update --> Test["5. Ejecutar vitest / mvn / go test"]
    Test --> Commit["6. Commit y Push Seguro"]
```

## Commands

### Windows 11 (PowerShell)

```powershell
# Auditoría en árbol de trabajo
pwsh -File scripts/bin/sdk/audit-sdk-sync.ps1 -Mode working

# Auditoría con ejecución de tests del SDK
pwsh -File scripts/bin/sdk/audit-sdk-sync.ps1 -Mode working -RunTests

# Auditoría sobre cambios staged (pre-commit)
pwsh -File scripts/bin/sdk/audit-sdk-sync.ps1 -Mode staged

# Salida en formato JSON
pwsh -File scripts/bin/sdk/audit-sdk-sync.ps1 -Mode working -Json
```

### Linux / Debian 12 (Bash)

```bash
# Auditoría en árbol de trabajo
scripts/bin/sdk/audit-sdk-sync.sh --mode working --run-tests
```
