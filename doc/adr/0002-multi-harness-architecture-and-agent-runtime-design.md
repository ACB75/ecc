# ADR-0002: Arquitectura Multi-Harness y Diseño de Runtimes de Agentes Autónomos (`ecc-claude` vs `ecc-agy`)

**Date**: 2026-11-01  
**Status**: accepted  
**Deciders**: Master, Antigravity (Advanced Agentic Coding)  

---

## 1. Context

La ingeniería de software asistida por agentes autónomos ha evolucionado hacia la coexistencia de diferentes plataformas y motores de inferencia. En nuestro entorno coexisten dos arneses (*harnesses*) principales:

1. **Anthropic Claude Code**: Basado en una interfaz de línea de comandos (CLI) interactiva, con hooks bash/python, configuración en `CLAUDE.md`, y comandos de barra inclinada (*slash commands*).
2. **Google Antigravity & Gemini**: Basado en un runtime de escritorio/IDE con invocación nativa de herramientas, orquestación de subagentes paralelos en subprocesos aislados (`branch`/`share`), descubrimiento dinámico de plugins (`~/.gemini/config/plugins/`), soporte nativo para el protocolo MCP (Model Context Protocol), y un sistema de activación reactivo (*reactive wakeup* sin sondeo).

Previamente, existía una fragmentación entre `ecc-agy` (agnóstico) y `ecc-agy-homelab` (específico de infraestructura física), además del repositorio original de Everything Claude Code. Esta fragmentación generaba duplicación masiva de código (más de 300 skills repetidas), inconsistencias de gobernanza y dificultades para desplegar el sistema en proyectos de terceros (ej. empresas externas en Barcelona).

---

## 2. Decision

Se adopta formalmente una **Arquitectura Multi-Harness Unificada** en el repositorio maestro `ACB75/ecc`:

1. **Unificación de Distribuciones Antigravity**:
   - Se fusiona `ecc-agy-homelab` dentro de `ecc-agy`. Todos los comandos, esquemas, reglas SRE y subagentes se consolidan en una única distribución unificada `ecc-agy`.
   - Las reglas específicas de infraestructura física o dominios locales se delegan al Nivel 2 de personalización (`<project>/.agents/rules/`), manteniendo el Nivel 1 (`ecc-agy`) limpio y exportable a $N$ proyectos empresariales.
2. **Estructura Multi-Harness en el Monorepo `ecc`**:
   - **`ecc-claude/`**: Almacena los artefactos nativos para Claude Code (`CLAUDE.md`, `.claude/`, slash commands, hooks).
   - **`ecc-agy/`**: Almacena la distribución completa para Google Antigravity (skills progresivos, subagentes tipados, schemas, comandos y reglas).
3. **Contrato de Abstracción de Harness**:
   - Cada harness encapsula su propio *Action Space* (herramientas disponibles) y *Observation Space* (formato de salida estructurada), respetando los mismos principios de ingeniería de Google (5 Pilares, TDD RED-GREEN-REFACTOR, Trunk-Based PRs y SRE Baseline).

---

## 3. Alternatives Considered

### Alternative 1: Mantener repositorios completamente separados (`ecc-claude`, `ecc-agy`, `ecc-agy-homelab`)

- **Pros**: Independencia total de versionado.
- **Cons**: Coste de mantenimiento triplicado, desincronización de skills y reglas, fricción extrema para propagar mejoras en linters o formatos de commit.
- **Why not**: Generaba silos y duplicaba el gasto cognitivo y de almacenamiento.

### Alternative 2: Forzar a Antigravity a consumir directamente el formato de Claude Code sin adaptación

- **Pros**: Cero código de adaptación.
- **Cons**: Incompatibilidad con las capacidades avanzadas de Antigravity (subagentes en paralelo, branches temporales de workspace, progressive disclosure de skills, tipado estricto de herramientas JSON Schema).
- **Why not**: Degradaba severamente el rendimiento y la calidad de inferencia en Gemini y Antigravity.

---

## 4. Consequences

### Positive

- **Mantenimiento Centralizado**: Una sola fuente de verdad para el ecosistema ECC.
- **Desacoplamiento Empresarial**: `ecc-agy` puede ser instalado de forma inmediata en cualquier empresa o proyecto sin filtrar infraestructura privada.
- **Flexibilidad de Motor**: El desarrollador puede elegir desplegar sobre Claude Code o sobre Google Antigravity mediante `install.ps1 -Target <claude|agy>`.
- **Economía de Tokens**: Progressive disclosure garantizado en ambos runtimes.

### Negative

- Requiere mantener alineados los instaladores y esquemas multi-distribución (`ecc.json`, `package.json`, `install.ps1`, `install.sh`).
