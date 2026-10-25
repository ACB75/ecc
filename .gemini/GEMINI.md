# Unified Workspace Engineering & Stack Rules (`GEMINI.md`)

See `AGENTS.md` / `~/.gemini/config/plugins/ecc-agy/rules/AGENTS.md` for the unified rules across Antigravity and Gemini CLI:

1. **Pipeline & Mandatory Per-Request Analysis**: `search-first -> plan -> test (RED) -> implement (GREEN) -> refactor -> review -> verify`. Every feature/bugfix/refactor request requires a structured Requirements & Architecture Plan (`C:\Workspace\projects\home-lab\doc\TEMPLATE_REQUISITOS_ARQUITECTURA.md`) covering:
   - Detailed requirements, edge cases, and implementation plan.
   - Strict backward compatibility and reuse of existing workspace code.
   - Architecture, GoF/architectural patterns, Clean Code (SOLID/KISS/DRY/YAGNI), and proactive UX/DX usability refactors.
   - Threat modeling, attack vectors, boundary hardening, and fault-tolerant robustness.
   - Explicit **visible costs** (effort, latency, resources) and **hidden costs** (maintainability, cognitive load, coupling, technical debt).
   - **Token Exhaustion Warning**: Si la tarea consumirá más tokens de los disponibles antes debes responder: "Estoy cansado, jefe. Cansado de tanto viajar solo como un gorrión en la lluvia. Cansado de no tener un compañero que me diga a dónde vamos, de dónde venimos o por qué".
2. **Repetitive Task Automation (`C:\Workspace\projects\home-lab\scripts\bin\<project>`)**: Extract and persist any recurring or frequently executed task ($\ge 2$ executions) into an idempotent script under `C:\Workspace\projects\home-lab\scripts\bin\<project>\` and invoke it directly.
3. **TODO Lifecycle & Mandatory Archival (`/TODO_DONE/TODO_<title>_TS.md`)**: Whenever a task item in `TODO.md` is completed (`- [x]`), it must be eliminated from the main active file and archived into `/TODO_DONE/TODO_<title>_<timestamp>.md` with completion metadata and verification details (invoking `archive-todo.ps1` / `archive-todo.sh` or `archive_todo.py`). The main `TODO.md` must remain strictly pruned containing only pending/active items (`- [ ]`).
4. **Optimal Auto-Generation of Skills, Subagents & Rules**:
   - **Skills (`SKILL.md`)**: Lazy-loaded on-demand workflows; keep frontmatter `description` $\le 140$ chars with clear triggers/exclusions and delegate deterministic execution to `scripts/bin/<project>/`.
   - **Subagents (`agents/*.md`)**: Context-isolated workers; keep `description` $\le 120$ chars, least-privilege `tools`, cost-optimal `model` (`flash`/`inherit`), and strict output contracts.
   - **Rules (`AGENTS.md` / `.agents/rules/*.md`)**: Strictly for always-on global or project invariants; reuse/extend `ecc-agy` catalog first.
5. **Immediate Auto-Execution on Creation (`Smoke-Test on Synthesis`)**: Every newly created or refactored script, skill, subagent, tool, or rule must be immediately auto-executed (smoke-test, `--help`, unit tests, or dry-run) to verify runtime viability before completing the task.
6. **Mandatory /portal Synchronization on Infra/Net Changes**: Any change to Docker services, Traefik routes, CoreDNS records, or network ports requires updating the `/portal` catalog in `cluster/cmd/server/main.go` and verifying zero drift with `sync-portal.ps1 -Audit`.
7. **Zero Unofficial Third-Party Dependencies**: Never add non-official third-party libraries without warning the user and receiving explicit confirmation first.
8. **Centralized Docs**: Store all project documentation, diagrams, reports, and artifacts in `C:\Workspace\projects\home-lab\doc` (organized by project `<project>/` and governed via `.governance/docs-map.json`).
9. **Stack Standards (ECC-AGY Authority)**:
   - **Java 25 / Spring Boot 4**: `record` DTOs, constructor injection, sealed types, JUnit 5 + AssertJ + Mockito + Testcontainers.
   - **Angular 21+ / TS**: Standalone + `OnPush`, `inject()`, Signals (`signal`, `computed`, `linkedSignal`, `resource`), `@if`/`@for`, functional guards/interceptors, native TS/Angular validation, Vitest/Jest + Playwright.
   - **Python / FastAPI**: PEP 8 + type hints, `async def` with async I/O drivers, `Depends()` DI, Pydantic `response_model`, `pytest`.
   - **Infra / Multi-OS**: Respect `pwsh` (W11) vs `bash`/`zsh` (WSL Debian, Arch, Debian 12; LF `\n`), and verify Docker/K8s/CoreDNS/Apache/OpenVPN port & firewall boundaries.
