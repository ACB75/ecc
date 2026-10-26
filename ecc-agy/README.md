# ECC-AGY (`ecc-agy`)

> **Distribución Agnóstica y Reutilizable de ECC para Google Antigravity (AGY)**  
> Parte del ecosistema multiproyecto [`ecc-aecb`](../README.md).

---

## 1. Visión General

`ecc-agy` es la adaptación pura y desacoplada de Everything Claude Code (ECC) para el motor de agentes **Google Antigravity (AGY)**. Ha sido despojada de cualquier acoplamiento o dependencia específica de infraestructuras particulares, convirtiéndose en un acelerador listo para producción reutilizable en **$N$ proyectos**, empresas (ej. empresas en Barcelona / corporativos) o clientes.

---

## 2. Capacidades Incluidas

- **16 Skills Especializadas**: `sre-reliability`, `architecture-decision-records`, `coding-standards`, `config-cleanup`, `conventional-commit-review`, `docs-governance`, `error-handling`, `git-workflow`, `search-first`, `security-review`, `sonarqube-quality-gate`, `sync-clean-align`, `tdd-workflow`, `todo-lifecycle`, `verification-loop`, `workspace-health-audit`.
- **12 Subagentes de Contexto Aislado**: `sre-engineer`, `architect`, `build-error-resolver`, `code-reviewer`, `doc-updater`, `planner`, `refactor-cleaner`, `security-reviewer`, `silent-failure-hunter`, `sync-aligner`, `tdd-guide`, `todo-archiver`.
- **Reglas Globales Estandarizadas**: Alineación con los 5 Pilares de Google, SRE Baseline (ADR-0008), Trunk-Based Development con PRs aisladas (Fast-Failure / Fast-Rollback) y Quality Gate SonarQube Rating A.
- **Arquitectura en 2 Niveles**: Reglas globales agnósticas en `rules/AGENTS.md` + inyección de reglas locales de cada proyecto en `<project>/.agents/rules/`.

---

## 3. Instalación

Para instalar `ecc-agy` como plugin global en Antigravity:

```powershell
# Windows 11
pwsh -File ../install.ps1 -Target agy
```

```bash
# Linux / WSL
bash ../install.sh --target agy
```
