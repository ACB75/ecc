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
  - **[`ADR-0001`](adr/ADR_ecc_0001_two_tier_global_plugin_and_project_scaffolding.md)**: Arquitectura en dos niveles: Plugin Global (`ecc-agy`) y Scaffolding por Proyecto (`.agents/`).
  - **[`ADR-0002`](adr/ADR_ecc_0002_multi_harness_architecture_and_agent_runtime_design.md)**: Arquitectura Multi-Harness y Diseño de Runtimes de Agentes Autónomos (`ecc-claude` vs `ecc-agy`).

---

## 3. Informes y Planes Arquitectónicos (`doc/adr/`)

- 📋 **[`ADR_ecc_plan_documentacion_arquitectura_harness.md`](adr/ADR_ecc_plan_documentacion_arquitectura_harness.md)**: Plan de toma de requisitos, criterios de aceptación y diseño arquitectónico para la documentación integral del harness.
- 🏢 **[`ADR_ecc_informe_abstraccion_reutilizable_n_proyectos.md`](adr/ADR_ecc_informe_abstraccion_reutilizable_n_proyectos.md)**: Análisis de desacoplamiento para reutilización en $N$ proyectos o empresas externas (ej. corporativos en Barcelona).
- 🔬 **[`ADR_ecc_informe_funcionamiento_ecc_agy_homelab.md`](adr/ADR_ecc_informe_funcionamiento_ecc_agy_homelab.md)**: Especificación técnica previa del fork antes de su consolidación en `ecc-agy`.

---

## 4. Diagramas de Arquitectura y Flujo (`doc/diagrams/`)

| Diagrama MMD | Descripción del Flujo / Arquitectura | Formato |
| :--- | :--- | :---: |
| **[`DGRM_ecc_harness_anatomy_and_lifecycle.mmd`](diagrams/DGRM_ecc_harness_anatomy_and_lifecycle.mmd)** | Anatomía completa del arnés y ciclo de vida de razonamiento/ejecución | `flowchart TD` |
| **[`DGRM_ecc_agy_environment_architecture.mmd`](diagrams/DGRM_ecc_agy_environment_architecture.mmd)** | Capas de descubrimiento, progressive disclosure y reactive wakeup de AGY | `flowchart TD` |
| **[`DGRM_ecc_harness_dual_claude_vs_agy.mmd`](diagrams/DGRM_ecc_harness_dual_claude_vs_agy.mmd)** | Comparativa arquitectónica entre Claude Code CLI y Google Antigravity | `flowchart LR` |
| **[`DGRM_ecc_autonomous_loop_recovery_flow.mmd`](diagrams/DGRM_ecc_autonomous_loop_recovery_flow.mmd)** | Máquina de estados para bucles continuos y recuperación con error contracts | `stateDiagram-v2` |
| **[`DGRM_ecc_auto_execution_on_creation.mmd`](diagrams/DGRM_ecc_auto_execution_on_creation.mmd)** | Pipeline de smoke-test inmediato al sintetizar artefactos | `flowchart TD` |
| **[`DGRM_ecc_commit_format_standard.mmd`](diagrams/DGRM_ecc_commit_format_standard.mmd)** | Pipeline de validación de commits `[type]-[projects]: <title>` | `flowchart TD` |
| **[`DGRM_ecc_sonarqube_quality_gate_pipeline.mmd`](diagrams/DGRM_ecc_sonarqube_quality_gate_pipeline.mmd)** | Compuertas de calidad estricta SonarQube Rating A | `flowchart TD` |
| **[`DGRM_ecc_sync_clean_align_flow.mmd`](diagrams/DGRM_ecc_sync_clean_align_flow.mmd)** | Flujo de sincronización de proyectos y erradicación de deriva | `flowchart TD` |
| **[`DGRM_ecc_todo_lifecycle_pipeline.mmd`](diagrams/DGRM_ecc_todo_lifecycle_pipeline.mmd)** | Ciclo de vida y archivado de tareas a `/TODO_DONE/` | `flowchart TD` |
| **[`DGRM_ecc_todo_prompt_transformation_flow.mmd`](diagrams/DGRM_ecc_todo_prompt_transformation_flow.mmd)** | Transformación sistemática de prompts mediante las 7 Fases | `flowchart TD` |
| **[`DGRM_ecc_workspace_hygiene_and_optimization_pipeline.mmd`](diagrams/DGRM_ecc_workspace_hygiene_and_optimization_pipeline.mmd)** | Pipeline de auditoría y optimización del workspace | `flowchart TD` |
| **[DGRM_ecc_business_flow.mmd](diagrams/DGRM_ecc_business_flow.mmd)** | Flujo de negocio y ciclo de vida de desarrollo de arneses y skills | lowchart TD |
| **[DGRM_ecc_actors.mmd](diagrams/DGRM_ecc_actors.mmd)** | Mapa de actores y límites del sistema ECC-AGY | lowchart LR |
