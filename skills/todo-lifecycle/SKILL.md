---
name: todo-lifecycle
description: Archive completed tasks from TODO.md into /TODO_DONE/TODO_<title>_TS.md and prune main list. Delegates to scripts/bin/ecc-agy/archive-todo.
metadata:
  origin: ECC-AGY
---

# TODO Lifecycle & Completed Tasks Archive

Operational workflow to manage task completion in `TODO.md`, ensuring completed items (`- [x]`) are removed from the main active file and archived with metadata and timestamp in `/TODO_DONE/TODO_<title>_<timestamp>.md`.

## When to Use

- Whenever a task in `TODO.md` is marked as completed (`- [x]`).
- Cleaning and pruning `TODO.md` so it contains only active or pending tasks (`- [ ]`).
- Generating audit-ready completion records under `TODO_DONE/`.

## Non-Negotiable Rules

1. **Clean TODO.md**: Never leave completed items (`- [x]`) lingering in the primary `TODO.md`.
2. **Deterministic Archival**: Always delegate to the canonical script `C:\Workspace\projects\home-lab\scripts\bin\ecc-agy\archive-todo.ps1` (Windows) or `archive-todo.sh` (Linux).
3. **Safe Slugs & Timestamps**: Ensure files in `TODO_DONE/` follow `TODO_<title>_<timestamp>.md`.

## Commands

### Windows 11 (PowerShell)
```powershell
# Archivar todas las tareas completadas en TODO.md
pwsh -NoProfile -File C:\Workspace\projects\home-lab\scripts\bin\ecc-agy\archive-todo.ps1 -AllCompleted

# Archivar una tarea específica con notas de entregable
pwsh -NoProfile -File C:\Workspace\projects\home-lab\scripts\bin\ecc-agy\archive-todo.ps1 -Complete "Configurar TLS" -Notes "Emitido certificado SAN y verificado en proxy."
```

### Linux / Debian (Bash)
```bash
/mnt/c/Workspace/projects/home-lab/scripts/bin/ecc-agy/archive-todo.sh --all-completed
```
