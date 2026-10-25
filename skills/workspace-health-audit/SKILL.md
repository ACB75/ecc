---
name: workspace-health-audit
description: Audit workspace hygiene, token budget, redundant skills, rules and docs governance. Delegates to scripts/ecc-agy/workspace-audit.py.
metadata:
  origin: ECC-AGY
---

# Workspace Health Audit

Operational skill to inspect, audit, and clean the active workspace, verify token budgets and frontmatter compliance across global and project-level `.agents/` scaffolds, eliminate redundant shadow skills, check rule consistency, and enforce deterministic documentation governance and SonarQube quality gates.

## When to Use

- User asks to "auditar workspace", "comprobar estado del workspace", "limpiar temporales", "optimizar skills", or "verificar presupuesto de tokens".
- Verifying whether rules, skills ($\le 140$ chars), and subagents ($\le 120$ chars, `flash`/`inherit`, minimum privilege) comply with `AGENTS.md`.
- Detecting and pruning shadowed skills or duplicate agents across projects.
- Verifying documentation links and role mappings with `audit-docs.py`.
- Running SonarQube static audits with `sonar-audit.py`.
- Running pre-commit or end-of-session hygiene maintenance.

## Non-Negotiable Rules

1. **Delegate Deterministic Work**: Always run the canonical wrapper `scripts/bin/ecc-agy/audit-workspace.ps1` (or `scripts/ecc-agy/workspace-audit.py`) rather than writing ad-hoc find/grep commands.
2. **Safe Cleanup**: Pass `-Clean` / `--clean` to remove confirmed temporary files (`.bak`, `.tmp`, `__pycache__`, `.pytest_cache`). Pass `-Optimize` / `--optimize` to safely prune redundant local skills shadowed by the global plugin.
3. **Never Swallow Failures**: If any phase reports a violation, state the exact file path and violation reason.

## Audit Workflow

### 1. Read-Only Health Inspection
Run the audit script in inspection mode:
```powershell
pwsh -NoProfile -File scripts/bin/ecc-agy/audit-workspace.ps1
```

### 2. Inspect the Six Audit Phases
- **Phase 1: Workspace Hygiene**: Checks for stray `.bak`, `.tmp`, `.old` files and execution caches (`__pycache__`, `.pytest_cache`).
- **Phase 2: Token Budget & Frontmatter Compliance**: Evaluates rules characters and verifies that all skills ($\le 140$c) and agents ($\le 120$c, `flash`/`inherit`, least privilege) comply.
- **Phase 3: Redundancy, Shadow Skills & Dead Artifacts**: Detects local skills that shadow global plugin skills, cross-project duplicates, orphan directories, and invalid agents.
- **Phase 4: Rule Consistency & Conflicts**: Verifies rule alignment and detects deprecated domain conventions.
- **Phase 5: Documentation Governance**: Runs `audit-docs.py` to ensure Markdown link and spine integrity.
- **Phase 6: SonarQube Quality Gate**: Runs `sonar-audit.py` to verify rating A (zero cognitive/duplication violations).

### 3. Cleanup & Optimization Mode (When Requested)
When the user asks to clean up or optimize workspace hygiene:
```powershell
pwsh -NoProfile -File scripts/bin/ecc-agy/audit-workspace.ps1 -Clean -Optimize
```
