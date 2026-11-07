#!/usr/bin/env python3
"""
Módulo de sincronización e ingesta de IDEAS.md hacia TODO.md.
Aplica la metodología canónica de 7 fases a cada propuesta aprobada.
Cumple con SonarQube Quality Gate A (S3776 <= 15, S1192 sin duplicados).
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence

SECTION_HEADER = "## Idea "
STATUS_APPROVED = "Approved"


@dataclass(frozen=True)
class IdeaItem:
    """Representa una propuesta estructurada en IDEAS.md."""
    title: str
    status: str
    sector: str
    data_type: str
    objective: str
    description: str


def _parse_idea_block(header: str, lines: List[str]) -> Optional[IdeaItem]:
    """Parsea un bloque individual de idea."""
    title = header.split(":", 1)[1].strip() if ":" in header else header.strip()
    status = ""
    sector = "Universal Engineering & Architecture"
    data_type = "Markdown / Code Artifacts"
    objective = ""
    desc = ""

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- Status:"):
            status = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("- Sector:"):
            sector = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("- DataType:"):
            data_type = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("- Objective:"):
            objective = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("- Description:"):
            desc = stripped.split(":", 1)[1].strip()

    if status.lower() == STATUS_APPROVED.lower():
        if not objective:
            objective = desc
        return IdeaItem(
            title=title,
            status=STATUS_APPROVED,
            sector=sector,
            data_type=data_type,
            objective=objective,
            description=desc,
        )
    return None


def parse_ideas_file(content: str) -> List[IdeaItem]:
    """Extrae las ideas aprobadas de un documento Markdown."""
    ideas: List[IdeaItem] = []
    current_header = ""
    current_lines: List[str] = []

    for line in content.splitlines():
        if line.startswith(SECTION_HEADER):
            if current_header:
                parsed = _parse_idea_block(current_header, current_lines)
                if parsed:
                    ideas.append(parsed)
            current_header = line
            current_lines = []
        elif current_header:
            current_lines.append(line)

    if current_header:
        parsed = _parse_idea_block(current_header, current_lines)
        if parsed:
            ideas.append(parsed)

    return ideas


def transform_to_7_phases(idea: IdeaItem) -> str:
    """Transforma una idea en una tarea TODO estructurada bajo el meta-prompt de 7 fases."""
    return f"""* [ ] **Tarea: {idea.title}**
  * **01 - ROLE:** Principal Systems & Software Automation Architect.
  * **02 - CONTEXT:** `[Sector: {idea.sector}]` `[Data Type: {idea.data_type}]` `[Objective: {idea.objective}]`.
  * **03 - PHASE 1 (ANALYSIS):**
    * Contexto y problemática: {idea.description}
    * Análisis de pre-implementación: verificar dependencias existentes y evitar anti-patrones.
  * **04 - PHASE 2 (STRATEGY):**
    * Lateral 1: Implementación mínima mediante utilidades nativas.
    * Lateral 2: Arquitectura modular extensible con contratos estables.
    * Lateral 3: Automatización end-to-end con guardrails de CI/CD.
  * **05 - PHASE 3 (EXECUTION):**
    1. Diseñar el contrato y plan de arquitectura.
    2. Desarrollar suite de tests unitarios TDD (RED).
    3. Implementar la solución y validar con código de salida 0 (GREEN).
    4. Refactorizar y verificar SonarQube Rating A.
  * **06 - PHASE 4 (CRITIC):**
    * Auditar posibles regresiones, cobertura de tests >=80% y cumplimiento de directivas de gobernanza.
  * **07 - PHASE 5 (FORMAT):**
    * Entregable probado, código limpio y auto-ejecución inmediata (Smoke-Test)."""


def inject_task_into_todo(todo_content: str, transformed_task: str, task_title: str) -> str:
    """Inyecta una tarea en TODO.md si no existe previamente."""
    if f"**Tarea: {task_title}**" in todo_content:
        return todo_content

    # Inyectar al final de la primera lista de tareas o al final del archivo
    pattern = r"(##\s*1\..*?\n)"
    match = re.search(pattern, todo_content)
    if match:
        idx = match.end()
        return todo_content[:idx] + "\n" + transformed_task + "\n\n" + todo_content[idx:]
    return todo_content.rstrip() + "\n\n" + transformed_task + "\n"


def sync_ideas(ideas_path: Path, todo_path: Path, dry_run: bool = False) -> int:
    """Sincroniza propuestas de ideas_path hacia todo_path."""
    if not ideas_path.is_file():
        return 0

    ideas_content = ideas_path.read_text(encoding="utf-8")
    approved_ideas = parse_ideas_file(ideas_content)
    if not approved_ideas:
        return 0

    todo_content = todo_path.read_text(encoding="utf-8") if todo_path.is_file() else "# BACKLOG MAESTRO\n"
    synced_count = 0
    updated_todo = todo_content

    for idea in approved_ideas:
        if f"**Tarea: {idea.title}**" not in updated_todo:
            task_md = transform_to_7_phases(idea)
            updated_todo = inject_task_into_todo(updated_todo, task_md, idea.title)
            synced_count += 1

    if synced_count > 0 and not dry_run:
        todo_path.write_text(updated_todo, encoding="utf-8")

    return synced_count


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Parsea argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(description="Ingesta automatizada de IDEAS.md a TODO.md con meta-prompt 7-fases.")
    parser.add_argument("--ideas", type=Path, default=Path("doc/IDEAS.md"), help="Ruta al archivo IDEAS.md.")
    parser.add_argument("--todo", type=Path, default=Path("doc/TODO.md"), help="Ruta al archivo TODO.md.")
    parser.add_argument("--dry-run", action="store_true", help="Simula la sincronización sin escribir en disco.")
    parser.add_argument("--check", action="store_true", help="Comprueba si existen ideas pendientes de sincronizar.")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Punto de entrada principal del CLI."""
    args = parse_args(argv)
    synced = sync_ideas(args.ideas, args.todo, dry_run=(args.dry_run or args.check))
    if args.check:
        if synced > 0:
            print(f"[WARN] Existen {synced} ideas aprobadas pendientes de sincronizar en TODO.md.")
            return 1
        print("[OK] Todas las ideas aprobadas están sincronizadas en TODO.md.")
        return 0

    print(f"[OK] {synced} tareas sincronizadas con éxito en {args.todo}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
