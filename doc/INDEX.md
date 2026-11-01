# Índice Maestro de Documentación y Gobernanza del Ecosistema ECC (`doc/INDEX.md`)

> **Espina Dorsal de Gobernanza Documental**: Repositorio [`ACB75/ecc`](https://github.com/ACB75/ecc)  
> Versión: `3.0.0` | Última Actualización: 2026-11-01

---

## 1. Manuales Técnicos y Guías de Arquitectura (`doc/manual/`)

- 📘 **[`GUIA_ARQUITECTURA_HARNESS_Y_ENTORNO_AGY.md`](manual/GUIA_ARQUITECTURA_HARNESS_Y_ENTORNO_AGY.md)**: Manual maestro exhaustivo sobre el funcionamiento de los arneses de IA, el runtime de Google Antigravity & Gemini, flujos de trabajo de ingeniería, espacios de acción/observación y principios de diseño para agentes autónomos.
- 🛡️ **[`the-security-guide.md`](the-security-guide.md)**: Guía exhaustiva de seguridad, bastionado de límites y prevención de ataques en entornos asistidos por agentes.
- 🏛️ **[`STACK_MODERNO_GOOGLE.md`](STACK_MODERNO_GOOGLE.md)**: Especificación de alineación con los 5 Pilares de Ingeniería de Google.

---

## 2. Registro de Decisiones de Arquitectura (`doc/adr/`)

- 📑 **[`doc/adr/README.md`](adr/README.md)**: Índice consolidado de ADRs del ecosistema ECC.
  - **[`ADR-0001`](adr/0001-two-tier-global-plugin-and-project-scaffolding.md)**: Arquitectura en dos niveles: Plugin Global (`ecc-agy`) y Scaffolding por Proyecto (`.agents/`).
  - **[`ADR-0002`](adr/0002-multi-harness-architecture-and-agent-runtime-design.md)**: Arquitectura Multi-Harness y Diseño de Runtimes de Agentes Autónomos (`ecc-claude` vs `ecc-agy`).

---

## 3. Informes y Planes Arquitectónicos (`doc/report/`)

- 📋 **[`PLAN_DOCUMENTACION_ARQUITECTURA_HARNESS.md`](report/PLAN_DOCUMENTACION_ARQUITECTURA_HARNESS.md)**: Plan de toma de requisitos, criterios de aceptación y diseño arquitectónico para la documentación integral del harness.
- 🏢 **[`INFORME_ABSTRACCION_REUTILIZABLE_N_PROYECTOS.md`](report/INFORME_ABSTRACCION_REUTILIZABLE_N_PROYECTOS.md)**: Análisis de desacoplamiento para reutilización en $N$ proyectos o empresas externas (ej. corporativos en Barcelona).
- 🔬 **[`INFORME_FUNCIONAMIENTO_ECC_AGY_HOMELAB.md`](report/INFORME_FUNCIONAMIENTO_ECC_AGY_HOMELAB.md)**: Especificación técnica previa del fork antes de su consolidación en `ecc-agy`.

---

## 4. Diagramas de Arquitectura y Flujo (`doc/diagrama/`)

| Diagrama MMD | Descripción del Flujo / Arquitectura | Formato |
| :--- | :--- | :---: |
| **[`harness_anatomy_and_lifecycle.mmd`](diagrama/harness_anatomy_and_lifecycle.mmd)** | Anatomía completa del arnés y ciclo de vida de razonamiento/ejecución | `flowchart TD` |
| **[`agy_environment_architecture.mmd`](diagrama/agy_environment_architecture.mmd)** | Capas de descubrimiento, progressive disclosure y reactive wakeup de AGY | `flowchart TD` |
| **[`harness_dual_claude_vs_agy.mmd`](diagrama/harness_dual_claude_vs_agy.mmd)** | Comparativa arquitectónica entre Claude Code CLI y Google Antigravity | `flowchart LR` |
| **[`autonomous_loop_recovery_flow.mmd`](diagrama/autonomous_loop_recovery_flow.mmd)** | Máquina de estados para bucles continuos y recuperación con error contracts | `stateDiagram-v2` |
| **[`auto_execution_on_creation.mmd`](diagrama/auto_execution_on_creation.mmd)** | Pipeline de smoke-test inmediato al sintetizar artefactos | `flowchart TD` |
| **[`commit_format_standard.mmd`](diagrama/commit_format_standard.mmd)** | Pipeline de validación de commits `[type]-[projects]: <title>` | `flowchart TD` |
| **[`sonarqube_quality_gate_pipeline.mmd`](diagrama/sonarqube_quality_gate_pipeline.mmd)** | Compuertas de calidad estricta SonarQube Rating A | `flowchart TD` |
| **[`sync_clean_align_flow.mmd`](diagrama/sync_clean_align_flow.mmd)** | Flujo de sincronización de proyectos y erradicación de deriva | `flowchart TD` |
| **[`todo_lifecycle_pipeline.mmd`](diagrama/todo_lifecycle_pipeline.mmd)** | Ciclo de vida y archivado de tareas a `/TODO_DONE/` | `flowchart TD` |
| **[`todo_prompt_transformation_flow.mmd`](diagrama/todo_prompt_transformation_flow.mmd)** | Transformación sistemática de prompts mediante las 7 Fases | `flowchart TD` |
| **[`workspace_hygiene_and_optimization_pipeline.mmd`](diagrama/workspace_hygiene_and_optimization_pipeline.mmd)** | Pipeline de auditoría y optimización del workspace | `flowchart TD` |
