# Registro Histórico de Decisiones y Cambios Materiales | ECC Ecosystem

> **Espina Dorsal de Gobernanza Documental**: Repositorio [`ACB75/ecc`](https://github.com/ACB75/ecc)  
> **Versión Canónica**: `3.0.0`  

---

## 2026-11-08: Consolidación Final, Harness de Gobernanza y Optimización Two-Tier

### Hitos y Decisiones Materiales

1. **Arquitectura Two-Tier y Reducción del 98.25% de Tokens** (PR #9, PR #10 | Commit `352c079`):
   - Adopción de la arquitectura Two-Tier: Tier 1 Global Plugin (`~/.gemini/config/plugins/ecc-agy`) con 21 skills nucleares transversales consumiendo ~701 tokens (reducido de 40.000 tokens iniciales).
   - Barrido y purgado del repositorio: eliminación de 147 skills y 27 agentes redundantes o no relacionados con los stacks autorizados (Java 25/Spring Boot 4, Angular 21/TS, Go/Microservices, Python/FastAPI, PyTorch/RecSys y automatización de oficina).
   - Normalización de 169 skills en Tier 2 con frontmatter $\le 140$ caracteres y 48 subagentes con $\le 120$ caracteres.

2. **Desacoplamiento Agnóstico y Saneamiento de Submódulos** (PR #11 | Commit `0106e39`):
   - Erradicación del subdirectorio anidado duplicado `ecc-agy/` (530 archivos duplicados purgados).
   - Consolidación del plugin agnóstico `aagy` / `ecc-agy` directamente en la raíz de `ACB75/ecc`.
   - Ajuste de `package.json` y `ecc.json` eliminando dependencias obsoletas.

3. **Pipeline Automatizado de Ingesta IDEAS -> TODO y CLI de Mapeo Documental** (PR #12 | Commit `8877291`):
   - Implementación del motor de ingesta [`sync_ideas_todo.py`](../scripts/ecc-agy/sync_ideas_todo.py) con Meta-Prompt de 7 Fases.
   - Creación de la utilidad CLI [`map_docs.py`](../scripts/ecc-agy/map_docs.py) y validación de enlaces relativos ignorando bloques de código.
   - Creación de plantilla canónica [`doc/IDEAS.md`](IDEAS.md).

4. **Estandarización de Política de Ramas de Incidencias en el Harness** (PR #13 | Commit `2bef381`):
   - Implementación de [`validate_branch.py`](../scripts/ecc-agy/validate_branch.py) enforcing prefijos `fix/<id>`, `feat/*`, `refactor/*`, `infra/*`, `chore/*`, `docs/*`, `test/*`.
   - Bloqueo sistemático de commits y PRs directas en ramas protegidas (`main`, `master`).

5. **Generador Automatizado de Post-Mortem SRE 5W** (PR #14 | Commit `30b89e5`):
   - Creación de plantilla SRE [`doc/post-mortem/TEMPLATE_POSTMORTEM_5W.md`](post-mortem/TEMPLATE_POSTMORTEM_5W.md) con análisis Who, What, When, Where, Why/How.
   - Desarrollo del generador [`generate_postmortem.py`](../scripts/ecc-agy/generate_postmortem.py) e integración automática en el cierre de ramas `fix/*`.

6. **Consolidación de Cierre Atómico, Auto-PR y Pre-Flight Review** (PR #15, PR #16 | Commits `ef04125`, `23c40d9`):
   - Fortalecimiento de [`complete-task-pr.ps1`](../scripts/bin/ecc-agy/complete-task-pr.ps1) y [`complete-task-pr.sh`](../scripts/bin/ecc-agy/complete-task-pr.sh).
   - Auto-archivo sincronizado de tareas completadas (`- [x]`) de `doc/TODO.md` a `doc/TODO_DONE/` a write-time con `lint-markdown.ps1 -Fix`.
   - Pre-merge Quality Gate estricto: markdownlint, suite `pytest` (61 tests) y SonarQube Rating A.
   - Manejo determinista de colecciones bajo `Set-StrictMode -Version Latest`.

7. **Normalización de la Espina Dorsal Documental y Limpieza Final**:
   - Reorganización de planes de trabajo sueltos hacia [`doc/plan/`](plan/).
   - Registro de mapeo documental en [`.governance/docs-map.json`](../.governance/docs-map.json).
   - Creación de estado operativo [`doc/STATUS.md`](STATUS.md) e histórico [`doc/LOG.md`](LOG.md).
