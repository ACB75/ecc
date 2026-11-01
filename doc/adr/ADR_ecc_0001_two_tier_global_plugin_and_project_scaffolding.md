# ADR-0001: Arquitectura en dos niveles: Plugin Global (`ecc-agy`) y Scaffolding por Proyecto (`.agents/`)

**Date**: 2026-10-24
**Status**: accepted
**Deciders**: Master, Antigravity (ECC-AGY)

## Context

El workspace `C:\Workspace\projects\home-lab` alberga proyectos heterogéneos (`kakebo` en Java 25/Spring Boot 4 + Angular 21, `cluster` en FastAPI/Docker/Kubernetes/Apache, `net` en PowerShell/CoreDNS/OpenVPN, `token-hill` en Python y `scripts` en PowerShell/Bash). Cargar todas las skills y subagentes especializados de todos los stacks de forma global en cada sesión saturaría el presupuesto de contexto, mientras que duplicar las reglas universales en cada repositorio dificultaría el mantenimiento.

## Decision

Adoptar una arquitectura de personalización en **dos niveles (Two-Tier Customization Architecture)**:

1. **Nivel 1 — Plugin Global (`C:\Users\Master\.gemini\config\plugins\ecc-agy`)**: Contiene las reglas universales (`rules/AGENTS.md`) y las skills/agentes transversales a todo el workspace (`search-first`, `tdd-workflow`, `verification-loop`, `security-review`, `coding-standards`, `docs-governance`, `architecture-decision-records`).
2. **Nivel 2 — Scaffolding por Proyecto (`<project>/.agents/skills/` y `<project>/.agents/agents/`)**: Sincronizado mediante `ecc-agy-sync.ps1` / `ecc-agy-sync.sh`, inyecta únicamente las skills y agentes específicos del stack de cada proyecto (`springboot-*`, `angular-developer`, `docker-patterns`, `homelab-*`).

## Alternatives Considered

### Alternative 1: Instalar todas las skills y agentes en el plugin global

- **Pros**: Un único directorio de instalación sin necesidad de sincronizar carpetas `.agents/` por proyecto.
- **Cons**: Infla la lista global de skills y agentes en todas las conversaciones, degradando la eficiencia de tokens y mezclando dominios irrelevantes.
- **Why not**: Viola el principio de eficiencia de contexto (`context-budget`) de ECC-AGY.

### Alternative 2: Copiar manualmente todas las reglas y skills en cada proyecto sin plugin global

- **Pros**: Independencia total entre repositorios.
- **Cons**: Alta deriva de configuración (*configuration drift*) al actualizar reglas de seguridad o gobernanza documental.
- **Why not**: Las reglas núcleo (`AGENTS.md`) y el flujo de ingeniería deben aplicarse sin excepción en todo el workspace.

## Consequences

### Positive

- Presupuesto de tokens optimizado: cada proyecto carga solo las skills de su dominio además del núcleo global.
- Gobernanza unificada y sincronización reproducible mediante `ecc-agy-sync.ps1`.

### Negative

- Requiere ejecutar el script de sincronización cuando se añaden nuevas skills específicas de dominio al catálogo de `ecc-agy`.

### Risks

- Desincronización entre el repositorio fuente `C:\Workspace\projects\ecc-agy` y el plugin desplegado; mitigado mediante `install.ps1` y `ecc-agy-sync.ps1`.
