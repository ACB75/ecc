---
title: "**Tarea 1.3: Convención de Ramas `fix/*` y Guardrails en el Arnés de Gobernanza**"
status: COMPLETED
completed_at: "2026-11-07 23:44:59"
---

# TODO: **Tarea 1.3: Convención de Ramas `fix/*` y Guardrails en el Arnés de Gobernanza**

## 1. Descripción de la Tarea

- **Estado**: COMPLETED
- **Fecha de Finalización**: 2026-11-07 23:44:59

### Detalle Original

- **01 - ROLE:** Principal GitOps Engineer & SRE Incident Commander.
- **02 - CONTEXT:** `[Sector: SRE Governance & Git Branching Standards]` `[Data Type: Git Hooks, Harness Rules, Branch Name Validation Scripts]` `[Objective: Formalizar e implementar la política estricta de ramas en el harness para que cualquier corrección, bugfix o gestión de fallo deba originarse obligatoriamente bajo el prefijo fix/<identificador-incidencia>, integrando esta regla en git-flow-helper y complete-task-pr]`.
- **03 - PHASE 1 (ANALYSIS):**
  - La creación de ramas ad-hoc sin prefijos estándar dificulta la trazabilidad y la asociación automática con los reportes de incidentes.
  - El arnés debe interceptar el checkout/branching y rechazar commits o PRs de solución de incidentes que no cumplan `fix/<identificador>`.
- **04 - PHASE 2 (STRATEGY):**
  - Configurar regla transversal en `.agents/rules/` y `rules/AGENTS.md`.
  - Extender `scripts/bin/ecc-agy/git-flow-helper.ps1` y los hooks pre-commit/pre-push para validar la nomenclatura canónica de ramas de fix.
- **05 - PHASE 3 (EXECUTION):**
    1. Codificar validador regex de nombres de rama en `git-flow-helper.ps1` / `.sh`.
    2. Actualizar el hook de pre-push del arnés para rechazar ramas no conformes.
    3. Documentar la convención en los manuales de gobernanza del harness.
- **06 - PHASE 4 (CRITIC):**
  - Evitar falsos positivos en ramas de infraestructura o de características (`infra/*`, `feat/*`, `refactor/*`).
- **07 - PHASE 5 (FORMAT):**
  - Script con validación regex robusta, test unitario de branches y regla activa en el arnés.

## 2. Verificación y Criterios de Aceptación

- [x] Tarea implementada y verificada contra criterios de aceptación.

## 4. Metadatos de Integración y Commit

- **Rama / PR**: `feat/ecc/fix-branch-policy-guardrails`
- **Commit SHA**: `8877291`
- **Fecha**: `2026-11-07 23:44:59`
- **Gobernanza**: Quality Gate A / markdownlint OK
