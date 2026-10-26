# Unified Workspace Engineering & Stack Rules (`GEMINI.md`)

See `AGENTS.md` / `~/.gemini/config/plugins/ecc-agy/rules/AGENTS.md` for the unified rules across Antigravity and Gemini CLI:

1. **Pipeline & Mandatory Per-Request Analysis**: `search-first -> plan -> test (RED) -> implement (GREEN) -> refactor -> review -> verify`. Every feature/bugfix/refactor request requires a structured Requirements & Architecture Plan (`doc/TEMPLATE_REQUISITOS_ARQUITECTURA.md`) covering:
   - Detailed requirements, edge cases, and implementation plan.
   - Strict backward compatibility and reuse of existing workspace code.
   - Architecture, GoF/architectural patterns, Clean Code (SOLID/KISS/DRY/YAGNI), and proactive UX/DX usability refactors.
   - Threat modeling, attack vectors, boundary hardening, and fault-tolerant robustness.
   - Explicit **visible costs** (effort, latency, resources) and **hidden costs** (maintainability, cognitive load, coupling, technical debt).
   - **Token Exhaustion Warning**: Si la tarea consumirá más tokens de los disponibles antes debes responder: "Estoy cansado, jefe. Cansado de tanto viajar solo como un gorrión en la lluvia. Cansado de no tener un compañero que me diga a dónde vamos, de dónde venimos o por qué".
2. **Repetitive Task Automation (`scripts/bin/<project>`)**: Extract and persist any recurring or frequently executed task ($\ge 2$ executions) into an idempotent script under `scripts/bin/<project>/` and invoke it directly.
3. **TODO Lifecycle & Mandatory Archival (`/TODO_DONE/TODO_<title>_TS.md`)**: Whenever a task item in `TODO.md` is completed (`- [x]`), it must be eliminated from the main active file and archived into `/TODO_DONE/TODO_<title>_<timestamp>.md` with completion metadata and verification details (invoking `archive-todo.ps1` / `archive-todo.sh` or `archive_todo.py`). The main `TODO.md` must remain strictly pruned containing only pending/active items (`- [ ]`).
4. **TODO Formulation & Rigorous Meta-Prompt Transformation (7-Phase Methodology)**: Every task point in `TODO.md` must be transformed using the 7-phase meta-prompt (01-Role of 3-5 top experts, 02-Context placeholders [IN BRACKETS], 03-Analysis, 04-Strategy/3 lateral approaches, 05-Execution step-by-step, 06-Devil's advocate critic, 07-Strict format) to force intellectual rigor and reject generic answers.
5. **Optimal Auto-Generation of Skills, Subagents & Rules**:
   - **Skills (`SKILL.md`)**: Lazy-loaded on-demand workflows; keep frontmatter `description` $\le 140$ chars with clear triggers/exclusions and delegate deterministic execution to `scripts/bin/<project>/`.
   - **Subagents (`agents/*.md`)**: Context-isolated workers; keep `description` $\le 120$ chars, least-privilege `tools`, cost-optimal `model` (`flash`/`inherit`), and strict output contracts.
   - **Rules (`AGENTS.md` / `.agents/rules/*.md`)**: Strictly for always-on global or project invariants; reuse/extend `ecc-agy` catalog first.
6. **Immediate Auto-Execution on Creation (`Smoke-Test on Synthesis`)**: Every newly created or refactored script, skill, subagent, tool, or rule must be immediately auto-executed (smoke-test, `--help`, unit tests, or dry-run) to verify runtime viability before completing the task.
7. **Mandatory /portal Synchronization on Infra/Net Changes**: Any change to Docker services, Traefik routes, CoreDNS records, or network ports requires updating the `/portal` catalog in `cluster/cmd/server/main.go` and verifying zero drift with `sync-portal.ps1 -Audit`.
8. **Zero Unofficial Third-Party Dependencies**: Never add non-official third-party libraries without warning the user and receiving explicit confirmation first.
9. **Centralized Docs**: Store all project documentation, diagrams, reports, and artifacts in `doc/` (organized by project `doc/<project>/` and governed via `.governance/docs-map.json`).
10. **Mandatory Write-Time Markdown Linter (`.markdownlint.json` Repo Configuration)**: Every `.md` file created or modified must be immediately audited/formatted at write-time using repo-level `.markdownlint.json` (`lint-markdown.ps1 -Fix`), enforcing DavidAnson invariants (MD022, MD032, MD031, MD009, MD012, MD047) as an exit-code-0 Quality Gate blocker.
11. **Mandatory Commit Format, Trunk-Based Git & Isolated PRs (ADR-0006)**: All commits follow `[type]+[projects]: <title>` with mandatory body comment. Adopt Trunk-Based Development with short-lived branches (`<type>/<project>/<name>`), isolated PRs for fast-failure and fast-rollback, Fast-Forward/Squash linear merges, and environment promotion tags (`LOCAL` trunk HEAD, `SANDBOX` `vX.Y.Z-sandbox`, `LIVE` `vX.Y.Z`). Never commit/push autonomously without user authorization.
12. **Software Reliability Engineering (SRE) & Operational Resilience (ADR-0008)**: Enforce Google SRE practices across all systems: SLI/SLO and Error Budget policies (freeze feature velocity if budget is exhausted), blast radius reduction via circuit breakers/bulkheads/timeouts, toil elimination (<50% cap), container resource boundaries (GOMEMLIMIT=80%, memory limits, log rotation), and blameless postmortems.
13. **Stack Standards (ECC-AGY Authority)**:
   - **Java 25 / Spring Boot 4**: `record` DTOs, constructor injection, sealed types, JUnit 5 + AssertJ + Mockito + Testcontainers.
   - **Angular 21+ / TS**: Standalone + `OnPush`, `inject()`, Signals (`signal`, `computed`, `linkedSignal`, `resource`), `@if`/`@for`, functional guards/interceptors, native TS/Angular validation, Vitest/Jest + Playwright.
   - **Python / FastAPI**: PEP 8 + type hints, `async def` with async I/O drivers, `Depends()` DI, Pydantic `response_model`, `pytest`.
   - **Infra / Multi-OS**: Respect `pwsh` (W11) vs `bash`/`zsh` (WSL Debian, Arch, Debian 12; LF `\n`), and verify Docker/K8s/CoreDNS/Apache/OpenVPN port & firewall boundaries.
