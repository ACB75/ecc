---
title: "**Tarea 1.4: Workflow y Skill de Generación Automatizada de Post-Mortem 5W**"
status: COMPLETED
completed_at: "2026-11-07 23:48:53"
---

# TODO: **Tarea 1.4: Workflow y Skill de Generación Automatizada de Post-Mortem 5W**

## 1. Descripción de la Tarea

- **Estado**: COMPLETED
- **Fecha de Finalización**: 2026-11-07 23:48:53

### Detalle Original

- **01 - ROLE:** Lead SRE Incident Response Architect & Automation Specialist.
- **02 - CONTEXT:** `[Sector: Site Reliability Engineering & Root Cause Analysis]` `[Data Type: Markdown Post-Mortem Templates, Automation Scripts, Git Lifecycle Hooks]` `[Objective: Automatizar la creación obligatoria del documento de autopsia post-incidencia tras el cierre de ramas fix/*, siguiendo el patrón de nombrado PM_<branch>_<timestamp>.md y estructurado con el análisis exhaustivo de las 5W (Who, What, When, Where, Why/How)]`.
- **03 - PHASE 1 (ANALYSIS):**
  - Tras solventar incidencias críticas, la redacción de autopsias suele omitirse o quedar incompleta, perdiendo el aprendizaje institucional y las acciones preventivas.
  - Se requiere un disparador automático en el arnés que instancie la plantilla al fusionar o cerrar ramas `fix/*`.
- **04 - PHASE 2 (STRATEGY):**
  - Diseñar el script generador `scripts/bin/ecc-agy/generate-postmortem.ps1` / `.sh`.
  - Integrar la generación en `complete-task-pr.ps1` cuando la rama procesada comience con `fix/`.
  - Enforzar la estructura de 5W: Who (actores/servicios), What (anomalía e impacto), When (tiempos UTC), Where (entorno LOCAL/SANDBOX/LIVE y rutas), Why/How (causa raíz y remediación).
- **05 - PHASE 3 (EXECUTION):**
    1. Crear la plantilla canónica `doc/post-mortem/TEMPLATE_POSTMORTEM_5W.md`.
    2. Desarrollar el generador que extraiga metadatos de Git (autor, timestamps, diff summary).
    3. Guardar el artefacto en `doc/post-mortem/PM_<branch>_<timestamp>.md`.
    4. Auto-ejecutar pruebas sintéticas del generador.
- **06 - PHASE 4 (CRITIC):**
  - Asegurar que el post-mortem sea estrictamente sin culpables (*blameless*) y que no bloquee fixes de emergencia críticos.
- **07 - PHASE 5 (FORMAT):**
  - Script generador probado, artefactos versionados y regla vinculante en el arnés.

## 2. Verificación y Criterios de Aceptación

- [x] Tarea implementada y verificada contra criterios de aceptación.

## 4. Metadatos de Integración y Commit

- **Rama / PR**: `feat/ecc/sre-postmortem-5w-generator`
- **Commit SHA**: `2bef381`
- **Fecha**: `2026-11-07 23:48:53`
- **Gobernanza**: Quality Gate A / markdownlint OK
