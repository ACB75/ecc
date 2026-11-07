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

### Tarea 1.3: Estandarización de Política de Ramas de Incidencias en el Harness (`fix/<id>`)

### Tarea 1.4: Generador Automatizado de Post-Mortem 5W (`PM_<branch>_<timestamp>.md`)

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
