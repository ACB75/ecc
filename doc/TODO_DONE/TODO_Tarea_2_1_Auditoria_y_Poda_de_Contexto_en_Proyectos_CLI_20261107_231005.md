---
title: "**Tarea 2.1: Auditoría y Poda de Contexto en Proyectos & CLI:**"
status: COMPLETED
completed_at: "2026-11-07 23:10:05"
---

# TODO: **Tarea 2.1: Auditoría y Poda de Contexto en Proyectos & CLI:**

## 1. Descripción de la Tarea

- **Estado**: COMPLETED
- **Fecha de Finalización**: 2026-11-07 23:10:05

### Detalle Original

- **01 - ROLE:** Context Window Architect & LLM Token Economy Lead.
- **02 - CONTEXT:** `[Sector: AI Agent Context Optimization & Cost Control]` `[Data Type: System Prompts, Rules, Skills Catalog, Token Metrics]` `[Objective: Analizar y podar el consumo de tokens en la carga de contexto para proyectos estándar y CLI, aplicando priorización por capas: 1) workflows nucleares, 2) meta-capacidades esenciales, y 3) purga de instrucciones redundantes]`.
- **03 - PHASE 1 (ANALYSIS):**
  - La sobrecarga de reglas, instrucciones y skills no utilizadas en la carga inicial penaliza el presupuesto de tokens y degrada la capacidad de razonamiento del LLM.
  - Deben aplicarse límites estrictos: frontmatter description <= 140 chars en skills, <= 120 chars en agentes, y lazy-loading para procedimientos no transversales.
- **04 - PHASE 2 (STRATEGY):**
  - Ejecutar `scripts/bin/ecc-agy/audit-workspace.ps1 -Clean -Optimize` para medir el tamaño total del contexto.
  - Prioridad 1: Mantener intactas directivas operativas de workflows nucleares.
  - Prioridad 2: Condensar meta-capacidades y skills esenciales de orquestación.
  - Depuración: Eliminar prompts sobrecargados, skills obsoletas o duplicadas entre global y local.
- **05 - PHASE 3 (EXECUTION):**
    1. Medir métricas de tokens actuales por módulo (rules, skills, agents).
    2. Refactorizar descripciones extensas a formato ultra-conciso de activación precisa.
    3. Mover lógica procedimental a scripts deterministas en `scripts/bin/ecc-agy/`.
    4. Validar reducción de huella de tokens mediante informe comparativo.
- **06 - PHASE 4 (CRITIC):**
  - Comprobar que la poda de tokens no afecte la precisión de activación ni introduzca alucinaciones en los subagentes.
- **07 - PHASE 5 (FORMAT):**
  - Reducción verificada en métricas de tokens, 0 skills huérfanas y reglas consolidadas.

## 2. Verificación y Criterios de Aceptación

- [x] Tarea implementada y verificada contra criterios de aceptación.

## 3. Entregables y Notas de Cierre

Implementadas y verificadas con éxito Tareas 2.1 y 2.2: Reducción del 53.8% en caracteres de skills y 45.3% en agentes (~13.6k tokens ahorrados), SonarQube Quality Gate A verificado con exit code 0, escaneo de seguridad superado y GitHub Actions CI configurado en .github/workflows/ci-quality-gate.yml.

## 4. Metadatos de Integración y Commit

- **Rama / PR**: `feat/ecc/token-opt-ci-quality-gate`
- **Commit SHA**: `e4659d6`
- **Fecha**: `2026-11-07 23:10:05`
- **Gobernanza**: Quality Gate A / markdownlint OK
