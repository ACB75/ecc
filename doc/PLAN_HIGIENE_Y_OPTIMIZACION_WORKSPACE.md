# Plan de Requisitos, Arquitectura e Higiene Recurrente del Workspace (`ecc-agy`)

> **Instrucciones de Uso (Regla Global ECC-AGY)**:
> Toma de requisitos detallada y diseño arquitectónico para el sistema recurrente de higiene, optimización de coste/rendimiento, deduplicación y resolución de conflictos de skills, agents y rules en el workspace.

---

## 1. Contexto y Metadatos de la Petición

- **Proyecto / Módulo**: `ecc-agy` / `home-lab/scripts/ecc-agy`
- **Tipo de Intervención**: `Refactorización Arquitectónica & Nueva Funcionalidad Recurrente`
- **Fecha**: `2026-10-25`
- **Objetivo Principal**: Implementar una auditoría e higiene integral y recurrente que optimice el coste de tokens, elimine duplicados, detecte artefactos obsoletos o muertos, prevenga conflictos en reglas y mantenga una higiene estricta en el monorepo y sus subproyectos.

---

## 2. Toma de Requisitos Detallada y Criterios de Aceptación

### 2.1. Requisitos Funcionales (`RF`)

- **`RF-01` (Auditoría de Redundancias y Duplicados)**: Detectar skills y agentes que existan duplicados en múltiples ubicaciones (por ejemplo, skills globales del plugin `ecc-agy` copiados innecesariamente en `.agents/skills/` locales de proyectos).
- **`RF-02` (Optimización y Poda Segura `--optimize` / `--prune`)**: Proveer un mecanismo automatizado e idempotente que elimine las copias locales redundantes de skills que ya son provistas de forma global por el plugin, ahorrando tokens de prompt y espacio en disco.
- **`RF-03` (Detección de Artefactos Muertos u Huérfanos)**: Detectar carpetas de skills sin archivo `SKILL.md`, definiciones de agentes en Markdown sin bloque frontmatter válido, o archivos de reglas vacíos/huérfanos.
- **`RF-04` (Auditoría de Conflictos de Reglas)**: Validar coherencia entre `home-lab/AGENTS.md`, `.agents/rules/*.md` y las reglas globales del plugin `ecc-agy`, alertando si hay contradicciones.
- **`RF-05` (Higiene de Archivos y Cachés `--clean`)**: Escanear y purgar archivos temporales (`.bak`, `.old`, `.orig`, `.tmp`, `.swp`), cachés de tests/compilación (`__pycache__`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`) y directorios vacíos.
- **`RF-06` (Auditoría de Presupuesto de Tokens y Frontmatter)**: Validar que toda skill tenga `description` $\le 140$ caracteres y todo agente tenga `description` $\le 120$ caracteres, modelo en `{"flash", "inherit"}` y principio de mínimo privilegio en herramientas.
- **`RF-07` (Automatización Recurrente CLI)**: Exponer el flujo mediante scripts de shell estándar en `scripts/bin/ecc-agy/audit-workspace.ps1` (Windows 11) y `audit-workspace.sh` (Debian 12) con switches `-Clean` y `-Optimize`.

### 2.2. Requisitos No Funcionales (`RNF`)

- **Rendimiento / Latencia**: El escaneo completo de higiene, tokens, duplicados y reglas debe completarse en $<3$ segundos en el entorno local.
- **Concurrencia e Inmutabilidad**: Operaciones de lectura sin efectos secundarios salvo que se especifique explícitamente `--clean` u `--optimize`.
- **Zero Dependencias Externas**: Implementado en Python 3 puro utilizando exclusivamente la librería estándar (`pathlib`, `re`, `argparse`, `dataclasses`, `logging`, `shutil`, `collections`).
- **Usabilidad (UX / DX)**: Salida estructurada y legible con códigos de salida inequívocos (`0` para éxito, `!= 0` ante fallos o violaciones).

### 2.3. Casos Límite (*Edge Cases*) y Condiciones de Fallo

- Proyectos con carpetas `.agents` inexistentes o parcialmente pobladas (gestión segura sin lanzar excepciones no controladas).
- Enlaces simbólicos (ignorados explícitamente para evitar bucles infinitos).
- Codificación de caracteres en Windows (`cp1252`): Manejo forzado de `utf-8` en stdout/stderr para evitar `UnicodeEncodeError`.
- Permisos de solo lectura o archivos bloqueados: reporte y omisión controlada sin abortar el escaneo.

### 2.4. Criterios de Aceptación (`CA` - Verificables por Tests)

- [ ] **`CA-01`**: La ejecución de `workspace-audit.py` detecta duplicados reales de skills y agentes e informa su ubicación.
- [ ] **`CA-02`**: La opción `--optimize` elimina limpiamente skills locales redundantes que ya residen en el plugin global (e.g. `sonarqube-quality-gate`), verificando que el plugin global siga abasteciendo la capacidad.
- [ ] **`CA-03`**: Se ejecutan tests unitarios en `scripts/ecc-agy/tests/test_workspace_audit.py` con 100% de éxito cubriendo duplicados, artefactos muertos y presupuesto de tokens.
- [ ] **`CA-04`**: La ejecución de `pwsh -File scripts/bin/ecc-agy/audit-workspace.ps1` finaliza con código de salida `0` y 0 violaciones.

---

## 3. Auditoría de Reutilización y Retrocompatibilidad

### 3.1. Inventario de Activos Existentes a Reutilizar

- [workspace-audit.py](file:///C:/Workspace/projects/home-lab/scripts/ecc-agy/workspace-audit.py): Base extensible de auditoría modular de 4 fases. Se refactoriza para incorporar las fases de duplicados, artefactos muertos y conflictos de reglas.
- [audit-workspace.ps1](file:///C:/Workspace/projects/home-lab/scripts/bin/ecc-agy/audit-workspace.ps1): Wrapper PowerShell existente, se enriquece con el parámetro `-Optimize`.
- [audit-docs.py](file:///C:/Users/Master/.gemini/config/plugins/ecc-agy/skills/docs-governance/scripts/audit-docs.py): Auditor de gobernanza documental integrado.
- [sonar-audit.py](file:///C:/Workspace/projects/home-lab/scripts/ecc-agy/sonar-audit.py): Auditor estático de calidad SonarQube integrado.

### 3.2. Impacto en Contratos y Estrategia de Retrocompatibilidad

- **Contratos Afectados**: Ninguno destructivo. Se añaden nuevos argumentos `--optimize` y `--check-conflicts` al CLI sin alterar el comportamiento de las invocaciones por defecto.
- **Garantía de Retrocompatibilidad**: La invocación existente sin parámetros o con `--clean` mantiene 100% su semántica original.
- **Plan de Rollback**: Revertir los cambios en `scripts/ecc-agy/workspace-audit.py` mediante Git si se detecta cualquier regresión.

---

## 4. Arquitectura, Patrones de Diseño y Flujo de Datos

### 4.1. Diseño Arquitectónico

Consulte el diagrama de flujo detallado en [workspace_hygiene_and_optimization_pipeline.mmd](file:///C:/Workspace/projects/home-lab/doc/ecc-agy/diagrama/workspace_hygiene_and_optimization_pipeline.mmd).

### 4.2. Patrones de Diseño Aplicados

- **Pipeline / Chain of Responsibility**: El script ejecuta fases secuenciales independientes (`Hygiene` $\to$ `Token Budget` $\to$ `Duplicates & Dead Artifacts` $\to$ `Rules Consistency` $\to$ `Docs Governance` $\to$ `SonarQube`).
- **Data Transfer Objects (DTOs) Inmutables**: Modelos `@dataclass(frozen=True)` para `HygieneReport`, `BudgetReport`, `DuplicateReport` y `ArtifactReport`.
- **Strategy & Delegation**: Ejecución no interactiva y sin shell de scripts hijos especializados (`audit-docs.py`, `sonar-audit.py`).

---

## 5. Seguridad y Análisis de Riesgos

| Vector de Amenaza | Riesgo | Mitigación |
| :--- | :---: | :--- |
| **Borrado accidental de código o datos** | Alto | La eliminación con `--clean` o `--optimize` restringe estrictamente sus rutas a patrones de temporales (`.bak`, `.tmp`, cachés) y carpetas de skills duplicadas confirmadas en global. Nunca elimina código fuente de aplicaciones. |
| **Command Injection en subprocesos** | Medio | Uso de listas de argumentos fijas `subprocess.run([sys.executable, str(script), *args], shell=False)` sin concatenación de cadenas shell. |
| **Path Traversal en escaneo** | Bajo | Resolución canónica mediante `pathlib.Path.resolve()` asegurando que las rutas pertenezcan a los límites del workspace. |

---

## 6. Análisis de Costes

- **Coste Visible**: ~200 líneas de código Python stdlib y ~100 líneas de tests unitarios. Tiempo de ejecución $<2$ segundos.
- **Coste Oculto (Ahorro)**: Reducción de ~400 tokens por prompt de inicio al deduplicar skills repetidas en proyectos locales que ya residían en el catálogo global. Eliminación de deuda técnica de duplicación de mantenimiento.
