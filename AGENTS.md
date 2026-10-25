# Unified Workspace Engineering & Stack Rules (`AGENTS.md`)

## 1. Core Engineering Pipeline, Pre-Implementation Analysis & Token Efficiency

- **Workflow**: `search-first -> plan -> test (RED) -> implement (GREEN) -> refactor -> review -> verify`.
- **Google 5-Pillar Architectural Alignment**: All applications and infrastructure must adhere to the 5 Core Google Engineering Pillars:
  1. *Hermetic Monorepo & Multi-stage Builds*: Self-contained repos, container builds with zero host tool dependencies.
  2. *Single Ingress & Unified TLS*: All external HTTP(S) traffic enters through the reverse proxy / GFE (`cluster-lb`); microservices do not expose raw ports externally.
  3. *Centralized Multi-Database Persistence (LTS)*: Prefer a single, hardened LTS PostgreSQL engine instance with logical databases per app (`cluster_db`, `kakebo`, `whoiam_db`) over running multiple Postgres daemon containers.
  4. *Modern Reactive Web (Angular + Wiz)*: Standalone components, Signals, `OnPush` change detection, and deferrable views (`@defer`).
  5. *Native Lightweight Observability*: Distributed tracing and structured logs over OpenTelemetry protocols; prioritize low-memory footprint (<300 MB) components for home lab environments.
- **Mandatory Per-Request Requirements & Architecture Analysis**: For EVERY request involving a new feature, bugfix, or refactor, generate a structured Requirements & Architecture Plan before coding (using template `C:\Workspace\projects\home-lab\doc\TEMPLATE_REQUISITOS_ARQUITECTURA.md`), explicitly addressing:
  1. **Detailed Requirements & Implementation**: Exact functional/non-functional requirements, edge cases, acceptance criteria, and step-by-step implementation strategy.
  2. **Backward Compatibility & Reuse First**: Strictly preserve backward compatibility (zero breaking changes to existing contracts/data/tests) and reuse existing workspace modules, services, components, and utilities before writing net-new code.
  3. **Architecture, Design Patterns, Clean Code & Usability Refactors**: Apply appropriate architectural and GoF design patterns, Clean Code principles (SOLID, KISS, DRY, YAGNI, immutability), and proactive refactoring to improve both user usability (UX/a11y) and developer ergonomics (DX).
  4. **Security, Attack Vectors, Robustness & Hardening**: Analyze threat surface and attack vectors (injection, XSS/CSRF/SSRF, path traversal, AuthN/AuthZ, DoS, secret/trace leaks), enforce boundary hardening, and guarantee robustness (explicit error handling, timeouts, fault tolerance).
  5. **Visible & Hidden Architectural Costs**: Explicitly state both the **visible cost** (implementation effort, latency/CPU/memory/network overhead, schema/infra changes) and the **hidden cost** (long-term maintainability, cognitive load, coupling, testing/CI overhead, technical debt) of architectural decisions.
- **Repetitive Task Automation (`C:\Workspace\projects\home-lab\scripts\bin\<project>`)**: Whenever a diagnostic, audit, build, cleanup, or operational task is executed repeatedly ($\ge 2$ times) or is recurring, extract and persist an idempotent, parameterized script in `C:\Workspace\projects\home-lab\scripts\bin\<project>\` (respecting `.ps1` for Windows 11, `.sh` with LF `\n` for Linux/WSL, or cross-platform `.js`/`.py`) and invoke that script directly instead of repeating ad-hoc inline commands.
- **TODO Lifecycle & Mandatory Archival (`/TODO_DONE/TODO_<title>_TS.md`)**: Whenever a task item in `TODO.md` is completed (`- [x]`), it must be eliminated from the main active file and archived into `/TODO_DONE/TODO_<title>_<timestamp>.md` with its completion metadata, deliverables, and verification details (invoking `C:\Workspace\projects\home-lab\scripts\bin\ecc-agy\archive-todo.ps1` / `archive-todo.sh` or `archive_todo.py`). The main `TODO.md` must remain strictly pruned containing only pending/active items (`- [ ]`).
- **Optimal Auto-Generation of Skills, Subagents & Rules**: Proactively synthesize reusable patterns into the right customization tier for maximum leverage and minimum token cost:
  - **Skills (`skills/<name>/SKILL.md`)**: Use for domain workflows or multi-step procedures needed *on-demand* (lazy-loaded: `0` base token cost for the body). Keep frontmatter `description` single-line ($\le 140$ chars) with exact trigger keywords + negative boundaries, and delegate deterministic logic to `scripts/bin/<project>/` or `skills/<name>/scripts/`.
  - **Subagents (`agents/<name>.md`)**: Use when tasks require *context isolation* (broad searches, multi-file audits, log analysis). Keep frontmatter `description` $\le 120$ chars, restrict `tools` to minimum privilege (read-only by default unless writing is required), select the most cost-effective model (`flash` for exploration/triage, `inherit` for deep reasoning), and enforce a concise output contract.
  - **Rules (`rules/AGENTS.md` or `<project>/.agents/rules/<name>.md`)**: Reserve strictly for universal invariants (global) or project-wide constraints (`.agents/rules/`). Never bloat always-on rules with tutorials; check `ecc-agy` catalog first to extend existing skills/agents before creating new ones.
- **Immediate Auto-Execution on Creation (`Smoke-Test on Synthesis`)**: Whenever a new script (`scripts/bin/...`), skill (`skills/...`), subagent (`agents/...`), tool, or automated rule is created or adjusted, it MUST be auto-executed immediately upon creation (e.g., invoking the script with `--help` / test inputs, executing unit tests, or running a subagent dry-run) to prove real-world runtime viability (exit code `0`, clean imports, zero missing dependencies) before declaring the task finished or ending the turn.
- **Mandatory /portal Synchronization on Infra/Net Changes**: Whenever changes are made to infrastructure or network configurations (Docker Compose services, Traefik routes/middlewares in dynamic.yml, CoreDNS/AdGuard records, port allocations, or network topology), the central `/portal` index in `cluster/cmd/server/main.go` (both HTML catalog and JSON `/` endpoints) MUST be synchronized and verified via `scripts/bin/cluster/sync-portal.ps1 -Audit` (exit code `0`, zero drift) before finishing the task.
- **Code Quality**: Prefer KISS/DRY/YAGNI, immutable transformations, focused files (200-400 lines, 800 max), early returns (<4 nesting levels), and explicit error handling (never swallow exceptions; validate at system boundaries).
- **Zero Unofficial Third-Party Dependencies**: NEVER introduce non-official third-party libraries or external packages (use native language/framework APIs and official packages only) UNLESS you first warn the user about the dependency and receive explicit confirmation.
- **Mandatory Mermaid Diagrams & Centralized Persistence**: Whenever an architectural proposal, topology, workflow, state machine, or data flow is designed or explained, generate clear and robust Mermaid diagrams (`flowchart`, `sequenceDiagram`, `stateDiagram-v2`, `erDiagram`) and ALWAYS persist them directly in the corresponding project's documentation folder under `C:\Workspace\projects\home-lab\doc\<project>/diagrama/` (or `diagramas/` for `net`), linking them within the relevant Markdown manuals and ADRs.
- **Documentation Centralization**: All project manuals, diagrams, reports, and artifacts belong in `C:\Workspace\projects\home-lab\doc` (organized by project: `<project>/`, with `.governance/docs-map.json`, `INDEX.md`, `STATUS.md`, `LOG.md`, and `adr/`). Do not scatter loose `.md` docs across project roots.
- **Token Efficiency & Delegation Contract**: Be direct and concise. Prefer targeted `grep` and line-range reads over full-file reads. Never end a turn while background subagents are still running; collect and integrate their results first.
- **Token Exhaustion Warning**: Si la tarea consumirá más tokens de los disponibles antes debes responder: "Estoy cansado, jefe. Cansado de tanto viajar solo como un gorrión en la lluvia. Cansado de no tener un compañero que me diga a dónde vamos, de dónde venimos o por qué".

## 2. Security & Secrets Baseline

- Never hardcode secrets, API keys, passwords, or tokens; use `.env` or secret managers and validate presence at startup.
- Parameterize all SQL queries; never concatenate user input.
- Sanitize HTML/URLs (prevent XSS/CSRF/SSRF/path traversal) and never leak stack traces or internal infrastructure paths in client responses.

## 3. Stack-Specific Rules (ECC-AGY Authority)

### Java 25 & Spring Boot 4 (`**/*.java`, `pom.xml`)

- **Style & Immutability**: Use `record` for DTOs/value types, `final` fields by default, defensive copies (`List.copyOf()`), sealed classes, pattern matching (`instanceof`/`switch`), and `Optional` only as return types (never fields/params).
- **DI & Architecture**: Constructor injection only (never `@Autowired` field injection). Keep controllers thin, business logic in services, and data access behind repositories.
- **Testing**: JUnit 5 + AssertJ + Mockito + Testcontainers (`postgres`), targeting 80%+ coverage.

### Angular 21+, TypeScript & Web (`**/*.ts`, `**/*.html`, `**/*.scss`)

- **Components & State**: Standalone components with `ChangeDetectionStrategy.OnPush`. Use `inject()` for DI (empty/no constructors), `input()`/`output()`, Signals (`signal`, `computed`, `linkedSignal`, `resource`), and `@if`/`@for (...; track id)` control flow. Never sync signals inside `effect()`.
- **Routing & HTTP**: Functional guards (`canMatch`), lazy `loadChildren`, and `HttpClient` with functional interceptors (`withInterceptors`). Clean up manual RxJS streams with `takeUntilDestroyed()`.
- **TypeScript & Validation**: Explicit types on public APIs; never use `any` (use `unknown` + type narrowing). Validate inputs using native TypeScript type guards and official Angular/platform validators (do not add third-party schema libraries like Zod without prior warning and user confirmation). No `console.log` in production code.
- **Web Design Quality**: Avoid generic boilerplate layouts; ensure clear typographic hierarchy, intentional spacing/states, semantic HTML, and compositor-friendly animations (`transform`, `opacity`), unless overridden by a project-specific rule (e.g., `kakebo-frontend`).
- **Testing**: Vitest/Jest + Angular `TestBed`/`ComponentHarness` for unit/integration (80%+ coverage), and Playwright/Cypress for E2E.

### Python & FastAPI (`**/*.py`)

- **Style & Typing**: PEP 8, explicit type annotations on all functions, immutable `@dataclass(frozen=True)` or Pydantic v2 models, `ruff`/`black` formatting, and `logging` instead of `print()`.
- **FastAPI**: Separate request/response Pydantic schemas (`response_model`), inject DB/auth via `Depends()`, and use `async def` with async I/O drivers (never run blocking `requests` or sync DB drivers inside `async def` routes).
- **Testing**: `pytest` (`@pytest.mark.unit` / `integration`) with 80%+ coverage.

### Multi-Environment & Infrastructure (Windows 11 / WSL Debian / Arch / Docker / K8s / Net)

- Respect shell/OS boundaries: `pwsh` on Windows 11 vs `bash`/`zsh` on Linux (POSIX LF `\n` for `.sh`).
- Verify port bindings, Split-DNS (`CoreDNS`), reverse proxy (`Apache`/`Traefik`), OpenVPN, and firewall impacts before modifying network or container configs.
- **Go Container Memory Throttling (`GOMEMLIMIT`)**: For all containerized Go services (`Traefik`, `whoiam`, `OpenTelemetry Collector`, `Prometheus`), ALWAYS set `GOMEMLIMIT` to 80% of the container memory limit (e.g. `GOMEMLIMIT=80MiB` for 100MiB limit) to enforce proactive GC and prevent sudden Linux OOM kills under constrained environments.
