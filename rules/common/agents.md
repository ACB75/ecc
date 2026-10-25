# Agent Orchestration, Script Automation & Customization Auto-Generation

## 1. Active Antigravity Subagents (`ecc-agy`)

Invoke subagents via `invoke_subagent(TypeName, Role, Prompt, Model)`:

| Subagent (`TypeName`) | Purpose | Recommended Model |
| :--- | :--- | :--- |
| `planner` | Implementation planning for complex features and refactoring | `inherit` |
| `architect` | Software architecture, system design, and technical trade-offs | `inherit` |
| `tdd-guide` | TDD specialist enforcing write-tests-first (`RED -> GREEN -> REFACTOR`) and 80%+ coverage | `inherit` |
| `code-reviewer` | Code review for quality, security, and maintainability after code changes | `inherit` |
| `security-reviewer` | Security vulnerability detection and hardening (OWASP, SSRF, injection, secrets) | `inherit` |
| `build-error-resolver` | Build and type error resolution with minimal diffs | `flash` / `inherit` |
| `refactor-cleaner` | Dead code cleanup, deduplication, and usability refactoring | `flash` / `inherit` |
| `doc-updater` | Documentation, ADR, and workspace doc governance updates | `flash` / `inherit` |
| `silent-failure-hunter` | Audits code for silent failures, swallowed exceptions, and missing error propagation | `flash` / `inherit` |
| `research` | Read-only multi-file codebase and documentation exploration | `flash` |

## 2. Repetitive Task Script Automation (`scripts/bin/<project>`)

1. **Extract Repetitive Commands into `/scripts/bin/<project>`**:
   - Whenever an operational, audit, verification, build, or cleanup task is executed repeatedly ($\ge 2$ times) or is recurring across sessions, create a reusable, idempotent, parameterized script under `scripts/bin/<project>/`.
   - Respect OS/shell conventions: `.ps1` (`$ErrorActionPreference = "Stop"`, `Set-StrictMode -Version Latest`) for Windows 11, `.sh` (`set -euo pipefail`, POSIX `LF` `\n`) for Linux/WSL, or cross-platform `.js`/`.py`.
   - Always invoke the persisted script from `/scripts/bin/<project>` instead of regenerating ad-hoc inline one-liners.

## 3. Optimal Auto-Generation of Skills, Subagents & Rules

When a new workflow, domain pattern, or specialized check emerges that can accelerate future requests, synthesize it into the optimal customization artifact:

1. **Choose the Right Artifact Tier (Token & Context Optimization)**:
   - **Script (`scripts/bin/<project>/<task>.{ps1,sh,js,py}`)**: Pure deterministic execution (audits, builds, migrations, log parsing). Zero prompt token overhead.
   - **Skill (`skills/<name>/SKILL.md`)**: Multi-step domain procedures or specialized guidance needed *on-demand*. Because Antigravity lazy-loads `SKILL.md` bodies, only `name` + `description` consume base context tokens:
     - Keep YAML frontmatter `description` single-line ($\le 140$ chars) with exact trigger terms and `DO NOT trigger for` boundaries.
     - Keep `SKILL.md` concise ($\le 120$ lines) and delegate heavy examples to `references/` and deterministic checks to `/scripts/bin/<project>/`.
   - **Subagent (`agents/<name>.md` or `define_subagent`)**: High-volume context tasks (reading many files, auditing logs, parallel review) that would pollute the main conversation window:
     - Keep YAML frontmatter `description` $\le 120$ chars.
     - Enforce least-privilege `tools` (`read_file`, `grep_search`, `find_by_name` only unless write access is essential).
     - Define a strict, structured output contract so the parent agent receives a compact summary.
   - **Rule (`rules/AGENTS.md` or `<project>/.agents/rules/<name>.md`)**: Reserve *exclusively* for non-negotiable invariants that apply to every turn (global) or every file in a project (`.agents/rules/`). Never put step-by-step tutorials in rules.
2. **Reuse & Catalog Sync**:
   - Search `C:\Workspace\projects\ecc-agy` (`skills/`, `agents/`, `rules/`) before creating a new customization; extend an existing skill/agent if overlap is $>50\%$.
   - Register new reusable skills/agents in `C:\Workspace\projects\ecc-agy` and sync active ones to `C:\Users\Master\.gemini\config\plugins\ecc-agy`.

## 4. Delegation Completion Contract

Applies to every agent at every depth:

1. **Your final message IS the deliverable**: Never end a turn while background subagents are running.
2. **If you delegate, you own collection**: Wait for subagent notifications, integrate their findings, and return a unified result.
3. **Decompose only when work exceeds single-context efficiency**: Use parallel subagents for independent heavy tasks, not trivial single-file lookups.
