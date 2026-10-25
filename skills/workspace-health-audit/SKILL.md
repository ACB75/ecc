---
name: workspace-health-audit
description: Audit workspace hygiene, token budget, .agents frontmatters, and docs governance. Delegates to scripts/ecc-agy/workspace-audit.py.
metadata:
  origin: ECC-AGY
---

# Workspace Health Audit

Operational skill to inspect, audit, and clean the active workspace, verify token budgets and frontmatter compliance across global and project-level `.agents/` scaffolds, and enforce deterministic documentation governance.

## When to Use

- User asks to "auditar workspace", "comprobar estado del workspace", "limpiar temporales", or "verificar presupuesto de tokens".
- Verifying whether rules, skills ($\le 140$ chars), and subagents ($\le 120$ chars, `flash`/`inherit`, minimum privilege) comply with `AGENTS.md`.
- Verifying documentation links and role mappings with `audit-docs.py`.
- Running pre-commit or end-of-session hygiene maintenance.

## Non-Negotiable Rules

1. **Delegate Deterministic Work**: Always run the canonical wrapper `scripts/bin/ecc-agy/audit-workspace.ps1` (or `scripts/ecc-agy/workspace-audit.py`) rather than writing ad-hoc find/grep commands.
2. **Safe Cleanup**: Only pass `-Clean` / `--clean` when the user explicitly requests cleanup or after confirming removable temporary files (`.bak`, `.tmp`, `__pycache__`, `.pytest_cache`).
3. **Never Swallow Failures**: If any phase reports a violation, state the exact file path and violation reason.

## Audit Workflow

### 1. Read-Only Health Inspection
Run the audit script in inspection mode:
```powershell
pwsh -NoProfile -File scripts/bin/ecc-agy/audit-workspace.ps1
```

### 2. Inspect the Three Audit Sections
- **Phase 1: Workspace Hygiene**:
  - Checks for stray `.bak`, `.tmp`, `.old` files and execution caches (`__pycache__`, `.pytest_cache`).
- **Phase 2: Token Budget & Frontmatter Compliance**:
  - Evaluates always-on rules characters in `AGENTS.md`.
  - Verifies that all skills in `~/.gemini/config/plugins/ecc-agy` and `<project>/.agents/skills/` have descriptions $\le 140$ characters.
  - Verifies that all subagents have descriptions $\le 120$ characters, use `model: flash` or `model: inherit`, and revoke write tools on read-only roles (`architect`, `planner`, `reviewer`, `hunter`, `troubleshooter`).
- **Phase 3: Documentation Governance**:
  - Runs `audit-docs.py --root doc --scope full` to ensure all Markdown links resolve, deletion-zone targets are respected, and ADR indices are intact.

### 3. Cleanup Mode (When Requested)
When the user asks to clean up or before finishing an operational milestone:
```powershell
pwsh -NoProfile -File scripts/bin/ecc-agy/audit-workspace.ps1 -Clean
```
