---
title: "**Tarea 1.2: Motor de Ingesta Automatizada y Utilidad Interactiva de Enlaces Documentales**"
status: COMPLETED
completed_at: "2026-11-07 23:42:05"
---

# TODO: **Tarea 1.2: Motor de Ingesta Automatizada y Utilidad Interactiva de Enlaces Documentales**

## 1. Descripción de la Tarea

- **Estado**: COMPLETED
- **Fecha de Finalización**: 2026-11-07 23:42:05

### Detalle Original

- **01 - ROLE:** DevX & CLI Automation Engineer (experto en parsers AST de Markdown, grafos de dependencias y CLI ergonomics).
- **02 - CONTEXT:** `[Sector: Developer Ergonomics & Backlog Automation]` `[Data Type: Python / PowerShell CLI, Markdown AST, Directed Acyclic Graph (DAG)]` `[Objective: Implementar el pipeline automático de ingesta de propuestas desde IDEAS.md hacia TODO.md y una herramienta accesible para auditar y mapear enlaces documentales]`.
- **03 - PHASE 1 (ANALYSIS):**
  - La traslación manual de ideas a tareas genera retrasos y omisiones. Un script debe evaluar dependencias y calcular el orden secuencial óptimo.
  - Se requiere un dashboard/CLI para validar enlaces cruzados rotos en la documentación técnica.
- **04 - PHASE 2 (STRATEGY):**
  - Desarrollar script `scripts/bin/ecc-agy/sync-ideas-todo.py` (o `.ps1`) para ingesta y validación de DAG.
  - Implementar utilidad `scripts/bin/ecc-agy/map-docs.py` para visualización y validación de enlaces relativos.
- **05 - PHASE 3 (EXECUTION):**
    1. Crear el generador/sincronizador de backlog con soporte para metodología de 7 fases.
    2. Crear el inspector interactivo de enlaces documentales con reporte de salud.
    3. Validar con pruebas unitarias y auto-ejecución inmediata.
- **06 - PHASE 4 (CRITIC):**
  - Asegurar que el parser de Markdown tolere tablas y listas anidadas sin romper el formato.
- **07 - PHASE 5 (FORMAT):**
  - Scripts parametrizados con `--check`, `--fix` y salida estructurada.

## 2. Verificación y Criterios de Aceptación

- [x] Tarea implementada y verificada contra criterios de aceptación.

## 4. Metadatos de Integración y Commit

- **Rama / PR**: `feat/ecc/sync-ideas-map-docs`
- **Commit SHA**: `0106e39`
- **Fecha**: `2026-11-07 23:42:05`
- **Gobernanza**: Quality Gate A / markdownlint OK
