# Unified Workspace Engineering & Stack Rules (`AGENTS.md`)

## 1. Core Engineering Pipeline, Pre-Implementation Analysis & Token Efficiency

- **Workflow**: `search-first -> plan -> test (RED) -> implement (GREEN) -> refactor -> review -> verify`.
- **Google 5-Pillar Architectural Alignment**: All applications and infrastructure must adhere to the 5 Core Google Engineering Pillars:
  1. *Hermetic Monorepo & Multi-stage Builds*: Self-contained repos, container builds with zero host tool dependencies.
  2. *Single Ingress & Unified TLS*: All external HTTP(S) traffic enters through the reverse proxy / Ingress Gateway; microservices do not expose raw ports externally.
  3. *Centralized Multi-Database Persistence (LTS)*: Prefer a single, hardened LTS database engine with logical databases per app over running multiple daemon containers.
  4. *Modern Reactive Web (Angular + Wiz)*: Standalone components, Signals, `OnPush` change detection, and deferrable views (`@defer`).
  5. *Native Lightweight Observability*: Distributed tracing and structured logs over OpenTelemetry protocols; prioritize low-memory footprint (<300 MB) components.
- **Mandatory Per-Request Requirements & Architecture Analysis**: For EVERY request involving a new feature, bugfix, or refactor, generate a structured Requirements & Architecture Plan before coding, explicitly addressing:
  1. **Detailed Requirements & Implementation**: Exact functional/non-functional requirements, edge cases, acceptance criteria, and step-by-step implementation strategy.
  2. **Backward Compatibility & Reuse First**: Strictly preserve backward compatibility (zero breaking changes to existing contracts/data/tests) and reuse existing workspace modules, services, components, and utilities before writing net-new code.
  3. **Architecture, Design Patterns, Clean Code & Usability Refactors**: Apply appropriate architectural and GoF design patterns, Clean Code principles (SOLID, KISS, DRY, YAGNI, immutability), and proactive refactoring to improve UX and DX.
  4. **Security, Attack Vectors, Robustness & Hardening**: Analyze threat surface and attack vectors (injection, XSS/CSRF/SSRF, path traversal, AuthN/AuthZ, DoS, secret/trace leaks), enforce boundary hardening, and guarantee robustness (explicit error handling, timeouts, fault tolerance).
  5. **Visible & Hidden Architectural Costs**: Explicitly state both the **visible cost** (implementation effort, latency/CPU/memory/network overhead, schema/infra changes) and the **hidden cost** (long-term maintainability, cognitive load, coupling, testing/CI overhead, technical debt) of architectural decisions.
- **Software Reliability Engineering (SRE) & Operational Resilience Baseline (ADR-0008)**: Adopt a systematic Google SRE mindset across all applications and infrastructure:
  1. *SLI/SLO & Error Budget Governance*: Define measurable Service Level Indicators (4 Golden Signals: Latency p95/p99, Traffic RPS, Errors 5xx ratio, Saturation) and target SLOs (base: 99.9% uptime). If the monthly Error Budget is exhausted, freeze feature velocity and allocate 100% engineering effort to reliability and stabilization.
  2. *Blast Radius & Anti-Fragile Isolation*: Design defensive perimeters on all service boundaries using Circuit Breakers, Bulkheads, strict timeouts (2s-5s), and Jittered Exponential Backoff. Zero unbounded retry loops or blocking calls without deadlines.
  3. *Toil Elimination (<50% cap)*: Codify repetitive operational and diagnostic tasks into idempotent automation scripts in `scripts/bin/<project>/`.
  4. *Resource Throttling & Probes*: Enforce container memory limits, `GOMEMLIMIT=80%` on Go runtimes, JVM container percentage limits, Docker log caps (`max-size: 10m`, `max-file: 3`), and explicit liveness/readiness health probes.
  5. *Blameless Postmortems*: Every critical outage or error budget breach requires an asynchronous blameless postmortem in `doc/postmortem/` documenting the 5-Whys root cause analysis and preventative action items.
- **Repetitive Task Automation (`scripts/bin/<project>`)**: Whenever a diagnostic, audit, build, cleanup, or operational task is executed repeatedly ($\ge 2$ times) or is recurring, extract and persist an idempotent, parameterized script in `scripts/bin/<project>/` (respecting `.ps1` for Windows 11, `.sh` with LF `\n` for Linux/WSL, or cross-platform `.js`/`.py`) and invoke that script directly instead of repeating ad-hoc inline commands.
- **TODO Lifecycle & Mandatory Archival (`/TODO_DONE/TODO_<title>_TS.md`)**: Whenever a task item in `TODO.md` is completed (`- [x]`), it must be eliminated from the main active file and archived into `/TODO_DONE/TODO_<title>_<timestamp>.md` with its completion metadata, deliverables, and verification details. The main `TODO.md` must remain strictly pruned containing only pending/active items (`- [ ]`).
- **TODO Formulation & Rigorous Meta-Prompt Transformation (7-Phase Methodology)**: For every task point in `TODO.md` (and whenever translating/refining a user request into actionable TODO items), apply the mandatory 7-phase prompt transformation:
  1. *01 – ROLE*: Personality combining the 3-5 greatest global experts on the specific domain.
  2. *02 – CONTEXT*: Explicit `[IN BRACKETS]` placeholders for user context (Sector, Data Type, Objective, Restrictions).
  3. *03 – PHASE 1 (ANALYSIS)*: Forced in-depth problem analysis before coding.
  4. *04 – PHASE 2 (STRATEGY)*: 3 distinct lateral thinking approaches before choosing the optimal one.
  5. *05 – PHASE 3 (EXECUTION)*: Step-by-step resolution of the task.
  6. *06 – PHASE 4 (CRITIC)*: Devil's Advocate audit actively hunting flaws, vulnerabilities, and weaknesses in the solution.
  7. *07 – PHASE 5 (FORMAT)*: Strict output definition (Table, Markdown Code, JSON, etc.).
- **Optimal Auto-Generation of Skills, Subagents & Rules**: Proactively synthesize reusable patterns into the right customization tier:
  - **Skills (`skills/<name>/SKILL.md`)**: Use for domain workflows or multi-step procedures needed *on-demand* (lazy-loaded: `0` base token cost for the body). Keep frontmatter `description` single-line ($\le 140$ chars).
  - **Subagents (`agents/<name>.md`)**: Use when tasks require *context isolation*. Keep frontmatter `description` $\le 120$ chars, restrict `tools` to minimum privilege, select the most cost-effective model (`flash`/`inherit`), and enforce a concise output contract.
  - **Rules (`rules/AGENTS.md` or `<project>/.agents/rules/<name>.md`)**: Reserve strictly for universal invariants (global) or project-wide constraints (`.agents/rules/`).
- **Mandatory Git Commit Message Format (`[type]+[scope]: <title>` + Explanatory Body)**: All commits across the workspace must strictly follow the structured title and mandatory explanatory message comment:
  1. *Title Format*: `[type]+[scope]: <title>` where `[type]` is a valid Conventional Commit type (`feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `perf`, `build`, `ci`, `sec`), followed by `-`, the affected project/module scope (`[backend]`, `[frontend]`, `[core]`, `[infra]`, etc.), and an imperative title.
  2. *Mandatory Explanatory Body Comment (`msg comment`)*: Single-line commits are strictly prohibited. Every commit must include an explanatory body detailing motivation, affected modules, architectural decisions, and verification tests executed.
  3. *Prohibition of Autonomous Commits/Pushes*: NEVER execute `git commit` or `git push` autonomously without explicit confirmation from the user.
- **Mandatory Automated Pull Request Creation Post Commit & Push**:
  - Immediately following user authorization and execution of git commit and git push on any isolated feature or task branch (eat/*, ix/*, efactor/*, chore/*, infra/*), the agent MUST automatically and immediately create the corresponding Pull Request against main (using gh pr create --fill or scripts/bin/ecc-agy/git-flow-helper.ps1 -Action create-pr), without waiting for an extra manual command from the user.
  - The Pull Request title must inherit the structured commit header ([type]-[projects]: <title>), and its body must inherit the explanatory commit message (*msg comment*), affected components, and verification results.
- **Trunk-Based Branching, Isolated PRs & Multi-Tier Promotion (ADR-0006)**: Adopt Trunk-Based Development (TBD) with canonical trunk `main` (always green, compilable, deployable). Every task, bugfix, or refactor must be developed in an isolated short-lived branch (<24-48h: `<type>/<project>/<name>`) and integrated exclusively via an isolated Pull Request (PR) to enforce **Fast-Failure** and **Fast-Rollback**.
- **Immediate Auto-Execution on Creation (`Smoke-Test on Synthesis`)**: Whenever a new script (`scripts/bin/...`), skill (`skills/...`), subagent (`agents/...`), tool, or automated rule is created or adjusted, it MUST be auto-executed immediately upon creation to prove real-world runtime viability (exit code `0`, clean imports) before declaring the task finished.
- **Code Quality & SonarQube Quality Gate (`Clean as You Code`)**: Prefer KISS/DRY/YAGNI, immutable transformations, focused files (200-400 lines, 800 max), early returns (<4 nesting levels), and explicit error handling. Strictly enforce SonarQube Quality Gate `A` ratings across all stacks: Cognitive Complexity $\le 15$ (`S3776`), $\le 7$ parameters per function/method (`S107`), zero duplicated string literals $\ge 3$ times (`S1192`), zero empty catch/nested blocks (`S108`), $\ge 80\%$ test coverage, and $\le 3\%$ duplication.
- **Workspace Hygiene, Token Optimization & Recurring Deduplication**: Periodically execute the 6-phase workspace audit via `scripts/bin/ecc-agy/audit-workspace.ps1` (`-Clean`, `-Optimize`).
- **Zero Unofficial Third-Party Dependencies**: NEVER introduce non-official third-party libraries without explicit confirmation from the user.
- **Mandatory Write-Time Markdown Linter (.markdownlint.json Repo Configuration)**: Every Markdown (.md) file created or modified across the workspace must be immediately audited and formatted at write-time before concluding the task or turn (pwsh -File scripts/bin/ecc-agy/lint-markdown.ps1 -Target <file> -Fix or lint-markdown.sh --fix <file>). The active linter configuration and rules must be loaded dynamically from the .markdownlint.json located at the root of the target repository (home-lab, cc-aecb, etc.), ensuring repository-level source-of-truth. Canonical DavidAnson invariants (MD022 blank lines around headings, MD032 blank lines around lists, MD031 blank lines around fences, MD009 zero trailing spaces, MD012 zero consecutive blanks, MD047 single EOF newline) are strictly enforced as a Quality Gate blocker (exit code 0 required in lint-markdown.ps1 and udit-workspace.ps1).
- **Token Efficiency & Delegation Contract**: Be direct and concise. Prefer targeted `grep` and line-range reads over full-file reads.

## 2. Security & Secrets Baseline

- Never hardcode secrets, API keys, passwords, or tokens; use `.env` or secret managers and validate presence at startup.
- Parameterize all SQL queries; never concatenate user input.
- Sanitize HTML/URLs (prevent XSS/CSRF/SSRF/path traversal) and never leak stack traces or internal infrastructure paths in client responses.

## 3. Stack-Specific Rules (ECC-AGY Authority)

### Java 25 & Spring Boot 4 (`**/*.java`, `pom.xml`)

- **Style & Immutability**: Use `record` for DTOs/value types, `final` fields by default, defensive copies (`List.copyOf()`), sealed classes, pattern matching (`instanceof`/`switch`), and `Optional` only as return types.
- **DI & Architecture**: Constructor injection only (never `@Autowired` field injection). Keep controllers thin, business logic in services, and data access behind repositories.
- **Testing**: JUnit 5 + AssertJ + Mockito + Testcontainers (`postgres`), targeting 80%+ coverage.

### Angular 21+, TypeScript & Web (`**/*.ts`, `**/*.html`, `**/*.scss`)

- **Components & State**: Standalone components with `ChangeDetectionStrategy.OnPush`. Use `inject()` for DI, `input()`/`output()`, Signals (`signal`, `computed`, `linkedSignal`, `resource`), and `@if`/`@for (...; track id)` control flow.
- **Routing & HTTP**: Functional guards (`canMatch`), lazy `loadChildren`, and `HttpClient` with functional interceptors (`withInterceptors`).
- **Testing**: Vitest/Jest + Angular `TestBed`/`ComponentHarness` for unit/integration (80%+ coverage), and Playwright for E2E.

### Python & FastAPI (`**/*.py`)

- **Style & Typing**: PEP 8, explicit type annotations on all functions, immutable `@dataclass(frozen=True)` or Pydantic v2 models, `ruff`/`black` formatting, and `logging` instead of `print()`.
- **FastAPI**: Separate request/response Pydantic schemas, inject DB/auth via `Depends()`, and use `async def` with async I/O drivers.
- **Testing**: `pytest` with 80%+ coverage.


