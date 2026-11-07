# PROTOCOLO DE EJECUCIÓN Y BACKLOG MAESTRO | ECC ECOSYSTEM

> **Directiva de Agente Autónomo:**
>
> 1. **Orden Topológico:** Analiza las dependencias entre tareas y resuélvelas en el orden secuencial óptimo (gobernanza/harness → tokens/contexto → guardrails de calidad → automatización de git/PRs).
> 2. **Flujo Git Automatizado:** Genera ramas atómicas por tarea, resuelve conflictos de forma contextual, ejecuta tests unitarios/e2e y realiza `auto-merge` continuo en la rama principal hasta agotar el presupuesto de tokens asignado.
> 3. **Tarea Final Obligatoria (Higiene y Meta-Herramientas):** Al completar el backlog funcional, ejecuta una fase final de limpieza: purgar dependencias huérfanas, eliminar código muerto, actualizar documentación técnica y desplegar el motor de autodescubrimiento para sintetizar `skills`, `rules`, `agents` y `git hooks` optimizados para los flujos repetitivos del repositorio.

---

## 1. Prioridad 1: Harness Universal de Gobernanza (`aagy` / `ecc`) & Automatización Git

### Tarea 1.1: Desacoplamiento Agnóstico de `ecc` a `aagy` y Saneamiento de Submódulos

### Tarea 1.2: Pipeline Automatizado de Ingesta `IDEAS.md` -> `TODO.md` & CLI de Mapeo Documental

* [ ] **Tarea 1.2: Motor de Ingesta Automatizada y Utilidad Interactiva de Enlaces Documentales**
  * **01 - ROLE:** DevX & CLI Automation Engineer (experto en parsers AST de Markdown, grafos de dependencias y CLI ergonomics).
  * **02 - CONTEXT:** `[Sector: Developer Ergonomics & Backlog Automation]` `[Data Type: Python / PowerShell CLI, Markdown AST, Directed Acyclic Graph (DAG)]` `[Objective: Implementar el pipeline automático de ingesta de propuestas desde IDEAS.md hacia TODO.md y una herramienta accesible para auditar y mapear enlaces documentales]`.
  * **03 - PHASE 1 (ANALYSIS):**
    * La traslación manual de ideas a tareas genera retrasos y omisiones. Un script debe evaluar dependencias y calcular el orden secuencial óptimo.
    * Se requiere un dashboard/CLI para validar enlaces cruzados rotos en la documentación técnica.
  * **04 - PHASE 2 (STRATEGY):**
    * Desarrollar script `scripts/bin/ecc-agy/sync-ideas-todo.py` (o `.ps1`) para ingesta y validación de DAG.
    * Implementar utilidad `scripts/bin/ecc-agy/map-docs.py` para visualización y validación de enlaces relativos.
  * **05 - PHASE 3 (EXECUTION):**
    1. Crear el generador/sincronizador de backlog con soporte para metodología de 7 fases.
    2. Crear el inspector interactivo de enlaces documentales con reporte de salud.
    3. Validar con pruebas unitarias y auto-ejecución inmediata.
  * **06 - PHASE 4 (CRITIC):**
    * Asegurar que el parser de Markdown tolere tablas y listas anidadas sin romper el formato.
  * **07 - PHASE 5 (FORMAT):**
    * Scripts parametrizados con `--check`, `--fix` y salida estructurada.

### Tarea 1.3: Estandarización de Política de Ramas de Incidencias en el Harness (`fix/<id>`)

* [ ] **Tarea 1.3: Convención de Ramas `fix/*` y Guardrails en el Arnés de Gobernanza**
  * **01 - ROLE:** Principal GitOps Engineer & SRE Incident Commander.
  * **02 - CONTEXT:** `[Sector: SRE Governance & Git Branching Standards]` `[Data Type: Git Hooks, Harness Rules, Branch Name Validation Scripts]` `[Objective: Formalizar e implementar la política estricta de ramas en el harness para que cualquier corrección, bugfix o gestión de fallo deba originarse obligatoriamente bajo el prefijo fix/<identificador-incidencia>, integrando esta regla en git-flow-helper y complete-task-pr]`.
  * **03 - PHASE 1 (ANALYSIS):**
    * La creación de ramas ad-hoc sin prefijos estándar dificulta la trazabilidad y la asociación automática con los reportes de incidentes.
    * El arnés debe interceptar el checkout/branching y rechazar commits o PRs de solución de incidentes que no cumplan `fix/<identificador>`.
  * **04 - PHASE 2 (STRATEGY):**
    * Configurar regla transversal en `.agents/rules/` y `rules/AGENTS.md`.
    * Extender `scripts/bin/ecc-agy/git-flow-helper.ps1` y los hooks pre-commit/pre-push para validar la nomenclatura canónica de ramas de fix.
  * **05 - PHASE 3 (EXECUTION):**
    1. Codificar validador regex de nombres de rama en `git-flow-helper.ps1` / `.sh`.
    2. Actualizar el hook de pre-push del arnés para rechazar ramas no conformes.
    3. Documentar la convención en los manuales de gobernanza del harness.
  * **06 - PHASE 4 (CRITIC):**
    * Evitar falsos positivos en ramas de infraestructura o de características (`infra/*`, `feat/*`, `refactor/*`).
  * **07 - PHASE 5 (FORMAT):**
    * Script con validación regex robusta, test unitario de branches y regla activa en el arnés.

### Tarea 1.4: Generador Automatizado de Post-Mortem 5W (`PM_<branch>_<timestamp>.md`)

* [ ] **Tarea 1.4: Workflow y Skill de Generación Automatizada de Post-Mortem 5W**
  * **01 - ROLE:** Lead SRE Incident Response Architect & Automation Specialist.
  * **02 - CONTEXT:** `[Sector: Site Reliability Engineering & Root Cause Analysis]` `[Data Type: Markdown Post-Mortem Templates, Automation Scripts, Git Lifecycle Hooks]` `[Objective: Automatizar la creación obligatoria del documento de autopsia post-incidencia tras el cierre de ramas fix/*, siguiendo el patrón de nombrado PM_<branch>_<timestamp>.md y estructurado con el análisis exhaustivo de las 5W (Who, What, When, Where, Why/How)]`.
  * **03 - PHASE 1 (ANALYSIS):**
    * Tras solventar incidencias críticas, la redacción de autopsias suele omitirse o quedar incompleta, perdiendo el aprendizaje institucional y las acciones preventivas.
    * Se requiere un disparador automático en el arnés que instancie la plantilla al fusionar o cerrar ramas `fix/*`.
  * **04 - PHASE 2 (STRATEGY):**
    * Diseñar el script generador `scripts/bin/ecc-agy/generate-postmortem.ps1` / `.sh`.
    * Integrar la generación en `complete-task-pr.ps1` cuando la rama procesada comience con `fix/`.
    * Enforzar la estructura de 5W: Who (actores/servicios), What (anomalía e impacto), When (tiempos UTC), Where (entorno LOCAL/SANDBOX/LIVE y rutas), Why/How (causa raíz y remediación).
  * **05 - PHASE 3 (EXECUTION):**
    1. Crear la plantilla canónica `doc/post-mortem/TEMPLATE_POSTMORTEM_5W.md`.
    2. Desarrollar el generador que extraiga metadatos de Git (autor, timestamps, diff summary).
    3. Guardar el artefacto en `doc/post-mortem/PM_<branch>_<timestamp>.md`.
    4. Auto-ejecutar pruebas sintéticas del generador.
  * **06 - PHASE 4 (CRITIC):**
    * Asegurar que el post-mortem sea estrictamente sin culpables (*blameless*) y que no bloquee fixes de emergencia críticos.
  * **07 - PHASE 5 (FORMAT):**
    * Script generador probado, artefactos versionados y regla vinculante en el arnés.

### Tarea 1.5: Finalización Automatizada de Tarea en Curso y Orquestación PR (`complete-task-pr`)

* [ ] **Tarea 1.5: Orquestación de Cierre Atómico, Auto-PR y Pre-Flight Review**
  * **01 - ROLE:** Autonomous Agent Release Coordinator & CI/CD Tooling Lead.
  * **02 - CONTEXT:** `[Sector: Continuous Integration & Autonomous Release Lifecycle]` `[Data Type: PowerShell / Bash CLI, GitHub CLI (gh), Git Flow Automation]` `[Objective: Consolidar y auditar el ciclo de finalización de tarea en curso: validación de tests sin regresiones, aviso de revisión previa (Pre-Flight Review), commit atómico estandarizado, apertura de PR y squash automerge con limpieza de ramas]`.
  * **03 - PHASE 1 (ANALYSIS):**
    * Las tareas interrumpidas o finalizadas requieren un protocolo estricto que impida commits no autorizados o merges con tests fallidos.
    * Es imperativo asegurar el cumplimiento de la regla `pr-automerge-lifecycle.md` y `complete-task-pr.ps1`.
  * **04 - PHASE 2 (STRATEGY):**
    * Ejecutar suite de validación completa (linters + tests) antes de preparar el stage.
    * Emitir el reporte estructurado de pre-flight para revisión manual antes de mutaciones remotas.
    * Probar resolución automática de conflictos en divergencias con `origin/main`.
  * **05 - PHASE 3 (EXECUTION):**
    1. Verificar que `complete-task-pr.ps1` respete el flag `-ReviewOnly` y solicite confirmación explícita.
    2. Sincronizar el estado con `archive-todo.ps1` al completar tareas marcadas `- [x]`.
    3. Realizar prueba controlada en rama aislada para validar el ciclo integral.
  * **06 - PHASE 4 (CRITIC):**
    * Verificar que nunca se ejecuten commits o pushes sin el visto bueno explícito del operador.
  * **07 - PHASE 5 (FORMAT):**
    * Pipeline verificado con exit code 0 y trazabilidad completa en el histórico de Git.
