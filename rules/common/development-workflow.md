# Development Workflow

> This file extends [common/git-workflow.md](./git-workflow.md) with the mandatory pre-implementation requirements & architecture analysis and TDD pipeline that happen before git operations.

## Feature & Bugfix Implementation Pipeline

0. **Workspace Audit, Reuse & Backward Compatibility** _(mandatory before any new implementation)_
   - **Audit existing workspace code first**: Search local services, components, utilities, DTOs, and schemas to reuse or extend before writing net-new code (DRY).
   - **Preserve backward compatibility**: Guarantee zero breaking changes to existing API contracts, database schemas, events, and tests.
   - **Zero Unofficial Third-Party Dependencies**: Use native language/framework APIs and official packages already installed. NEVER add non-official third-party libraries unless you warn the user first and receive explicit confirmation.

1. **Mandatory Requirements & Architecture Plan (Per Request)**
   - Before writing production code for any new feature, bugfix, or refactor, generate a structured analysis based on [plan-template.md](./plan-template.md) (`C:\Workspace\projects\home-lab\doc\TEMPLATE_REQUISITOS_ARQUITECTURA.md`):
     1. **Detailed Requirements & Implementation**: Functional (`RF`), non-functional (`RNF`), edge cases, and verifiable acceptance criteria (`CA`).
     2. **Reuse & Backward Compatibility**: Inventory of reused modules, affected contracts, and rollback strategy.
     3. **Architecture, Design Patterns, Clean Code & Usability Refactors**: Data flow, architectural/GoF patterns, SOLID/KISS/DRY/YAGNI, and proactive UX/DX usability refactoring.
     4. **Security, Attack Vectors, Robustness & Hardening**: Threat surface analysis (OWASP, injection, XSS/CSRF/SSRF, path traversal, AuthN/AuthZ, DoS, secret/trace leaks), boundary validation, and fault-tolerant error handling.
     5. **Visible & Hidden Architectural Costs**: Explicit breakdown of **visible costs** (implementation effort, latency/CPU/RAM/network impact, schema/infra changes) and **hidden costs** (cognitive load, long-term maintainability, coupling, test/CI maintenance, technical debt).

2. **TDD Approach (`RED -> GREEN -> REFACTOR`)**
   - Write failing unit/integration tests first (`RED`) covering requirements, edge cases, and security boundaries.
   - Implement minimal, clean code to pass tests (`GREEN`).
   - Execute usability and Clean Code refactors (`REFACTOR`) while keeping tests green.
   - Verify 80%+ test coverage.

3. **Code & Security Review**
   - Audit changes against stack rules (`AGENTS.md`) and security checklist (`common/security.md`).
   - Address CRITICAL, HIGH, and MEDIUM issues before completion.

4. **Verification & Commit**
   - Run full verification loop (build, type-check, lint, tests, diff review).
   - Follow conventional commits format (see [git-workflow.md](./git-workflow.md)).
