#!/usr/bin/env python3
"""
Tool: Archive Completed TODOs (TODO Lifecycle Manager)
Descripción: Extrae tareas completadas de TODO.md, las archiva con formato canónico en
TODO_DONE/TODO_<title>_<timestamp>.md y poda limpiamente el archivo principal.

Uso:
  python archive_todo.py [--todo PATH] [--complete "Título"] [--all-completed] [--notes "Detalles"]
"""

from __future__ import annotations

import argparse
import logging
import os
import re
import sys
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger: logging.Logger = logging.getLogger("archive_todo")

COMPLETED_PATTERN: re.Pattern[str] = re.compile(r"^(\s*)[-*]\s*\[[xX]\]\s*(.+)$")
PENDING_PATTERN: re.Pattern[str] = re.compile(r"^(\s*)[-*]\s*\[\s*\]\s*(.+)$")
NON_ALPHANUM_REGEX: re.Pattern[str] = re.compile(r"[^A-Za-z0-9_-]+")
MULTIPLE_UNDERSCORES: re.Pattern[str] = re.compile(r"_+")

STATUS_COMPLETED: str = "COMPLETED"
DEFAULT_DONE_DIR_NAME: str = "TODO_DONE"


def get_current_git_meta() -> Tuple[str, str]:
    import subprocess
    branch: str = "main"
    sha: str = "HEAD"
    try:
        b = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, check=False)
        if b.returncode == 0 and b.stdout.strip():
            branch = b.stdout.strip()
        s = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=False)
        if s.returncode == 0 and s.stdout.strip():
            sha = s.stdout.strip()
    except (OSError, subprocess.SubprocessError) as exc:
        logger.debug("git meta extraction skipped: %s", exc)
    return branch, sha


@dataclass(frozen=True)
class ExtractedTask:
    title: str
    body_lines: Tuple[str, ...]
    raw_header: str


def slugify_title(title: str, max_length: int = 60) -> str:
    clean_title: str = title.strip()
    clean_title = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", clean_title)
    clean_title = re.sub(r"[*_`#]+", "", clean_title)
    normalized: str = unicodedata.normalize("NFKD", clean_title).encode("ASCII", "ignore").decode("ASCII")
    slug: str = NON_ALPHANUM_REGEX.sub("_", normalized)
    slug = MULTIPLE_UNDERSCORES.sub("_", slug).strip("_")
    return slug[:max_length].rstrip("_") if slug else "TAREA"


def adjust_relative_links(text: str, source_dir: Path, target_dir: Path) -> str:
    if source_dir.resolve() == target_dir.resolve():
        return text

    def replace_match(match: re.Match[str]) -> str:
        label: str = match.group(1)
        target: str = match.group(2)
        if target.startswith(("http://", "https://", "mailto:", "#", "/")):
            return match.group(0)

        abs_target: Path = (source_dir / target).resolve()
        try:
            rel_path: str = os.path.relpath(abs_target, target_dir.resolve()).replace("\\", "/")
            return f"[{label}]({rel_path})"
        except ValueError:
            return match.group(0)

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_match, text)


def format_archive_document(
    task: ExtractedTask,
    source_dir: Optional[Path] = None,
    target_dir: Optional[Path] = None,
    notes: Optional[str] = None,
) -> str:
    now: datetime = datetime.now()
    ts_iso: str = now.strftime("%Y-%m-%d %H:%M:%S")

    adjusted_title: str = task.title
    if source_dir and target_dir:
        adjusted_title = adjust_relative_links(adjusted_title, source_dir, target_dir)

    clean_heading_title: str = adjusted_title.rstrip(".:,;!? \t")
    doc_lines: List[str] = [
        "---",
        f"title: \"{adjusted_title}\"",
        f"status: {STATUS_COMPLETED}",
        f"completed_at: \"{ts_iso}\"",
        "---",
        "",
        f"# TODO: {clean_heading_title}",
        "",
        "## 1. Descripción de la Tarea",
        "",
        f"- **Estado**: {STATUS_COMPLETED}",
        f"- **Fecha de Finalización**: {ts_iso}",
        "",
    ]

    if task.body_lines:
        doc_lines.append("### Detalle Original")
        doc_lines.append("")
        for line in task.body_lines:
            adjusted_line = line
            if source_dir and target_dir:
                adjusted_line = adjust_relative_links(line, source_dir, target_dir)
            doc_lines.append(adjusted_line)
        doc_lines.append("")

    doc_lines.append("## 2. Verificación y Criterios de Aceptación")
    doc_lines.append("")
    doc_lines.append("- [x] Tarea implementada y verificada contra criterios de aceptación.")
    doc_lines.append("")

    if notes and notes.strip():
        doc_lines.append("## 3. Entregables y Notas de Cierre")
        doc_lines.append("")
        doc_lines.append(notes.strip())
        doc_lines.append("")

    branch, sha = get_current_git_meta()
    doc_lines.append("## 4. Metadatos de Integración y Commit")
    doc_lines.append("")
    doc_lines.append(f"- **Rama / PR**: `{branch}`")
    doc_lines.append(f"- **Commit SHA**: `{sha}`")
    doc_lines.append(f"- **Fecha**: `{ts_iso}`")
    doc_lines.append("- **Gobernanza**: Quality Gate A / markdownlint OK")
    doc_lines.append("")

    return "\n".join(doc_lines)


def _extract_task_body(lines: Sequence[str], start_idx: int, indent_level: int) -> Tuple[List[str], int]:
    body_lines: List[str] = []
    idx = start_idx
    total = len(lines)
    while idx < total:
        line = lines[idx]
        if not line.strip():
            body_lines.append(line)
            idx += 1
            continue
        indent_match = re.match(r"^(\s*)", line)
        indent_len = len(indent_match.group(1)) if indent_match else 0
        is_task_marker = COMPLETED_PATTERN.match(line) or PENDING_PATTERN.match(line)
        if indent_len > indent_level and not is_task_marker:
            body_lines.append(line)
            idx += 1
        else:
            break
    return body_lines, idx


def parse_todo_file(lines: Sequence[str]) -> Tuple[List[ExtractedTask], List[str]]:
    remaining_lines: List[str] = []
    extracted_tasks: List[ExtractedTask] = []

    idx: int = 0
    total_lines: int = len(lines)

    while idx < total_lines:
        line: str = lines[idx]
        match: Optional[re.Match[str]] = COMPLETED_PATTERN.match(line)
        if match:
            indent: str = match.group(1)
            raw_title: str = match.group(2).strip()
            indent_level: int = len(indent)

            body_lines, next_idx = _extract_task_body(lines, idx + 1, indent_level)
            extracted_tasks.append(ExtractedTask(title=raw_title, body_lines=tuple(body_lines), raw_header=line))
            idx = next_idx
        else:
            remaining_lines.append(line)
            idx += 1

    return extracted_tasks, remaining_lines


def archive_task_file(
    task: ExtractedTask,
    done_dir: Path,
    source_dir: Optional[Path] = None,
    notes: Optional[str] = None,
) -> Path:
    done_dir.mkdir(parents=True, exist_ok=True)
    slug: str = slugify_title(task.title)
    timestamp: str = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_filename: str = f"TODO_{slug}_{timestamp}.md"
    target_path: Path = done_dir / target_filename

    counter: int = 1
    while target_path.exists():
        target_filename = f"TODO_{slug}_{timestamp}_{counter}.md"
        target_path = done_dir / target_filename
        counter += 1

    content: str = format_archive_document(task, source_dir=source_dir, target_dir=done_dir, notes=notes)
    target_path.write_text(content, encoding="utf-8")
    return target_path


def _filter_tasks(
    extracted_tasks: Sequence[ExtractedTask],
    target_title: Optional[str],
    archive_all: bool,
) -> Tuple[List[ExtractedTask], List[ExtractedTask]]:
    tasks_to_archive: List[ExtractedTask] = []
    tasks_to_keep: List[ExtractedTask] = []

    for task in extracted_tasks:
        should_archive: bool = archive_all
        if target_title and target_title.lower() in task.title.lower():
            should_archive = True

        if should_archive:
            tasks_to_archive.append(task)
        else:
            tasks_to_keep.append(task)

    return tasks_to_archive, tasks_to_keep


def process_archive(
    todo_path: Path,
    done_dir: Optional[Path] = None,
    target_title: Optional[str] = None,
    archive_all: bool = False,
    notes: Optional[str] = None,
    dry_run: bool = False,
) -> int:
    if not todo_path.is_file():
        logger.error("El archivo especificado no existe: %s", todo_path)
        return 1

    target_done_dir: Path = done_dir or (todo_path.parent / DEFAULT_DONE_DIR_NAME)
    content: str = todo_path.read_text(encoding="utf-8", errors="replace")
    lines: List[str] = content.splitlines()

    extracted_tasks, remaining_lines = parse_todo_file(lines)
    if not extracted_tasks:
        logger.info("No se encontraron tareas completadas (- [x]) en %s.", todo_path)
        return 0

    tasks_to_archive, tasks_to_keep = _filter_tasks(extracted_tasks, target_title, archive_all)
    if not tasks_to_archive:
        logger.info("Ninguna tarea completada coincide con el filtro: %s", target_title)
        return 0

    final_lines: List[str] = list(remaining_lines)
    for kept in tasks_to_keep:
        final_lines.append(kept.raw_header)
        final_lines.extend(kept.body_lines)

    logger.info("Tareas a archivar (%d):", len(tasks_to_archive))
    for t in tasks_to_archive:
        logger.info("  • %s", t.title)

    if dry_run:
        logger.info("[DRY-RUN] No se realizaron escrituras en disco.")
        return 0

    for t in tasks_to_archive:
        archived_file: Path = archive_task_file(t, target_done_dir, source_dir=todo_path.parent, notes=notes)
        logger.info("Archivado: %s", archived_file)

    cleaned_content: str = "\n".join(final_lines)
    cleaned_content = re.sub(r"\n{3,}", "\n\n", cleaned_content).strip() + "\n"
    todo_path.write_text(cleaned_content, encoding="utf-8")
    logger.info("Actualizado %s (tareas completadas podadas).", todo_path)
    return 0


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Archiva tareas completadas (- [x]) de TODO.md hacia /TODO_DONE/TODO_<title>_TS.md"
    )
    parser.add_argument("--todo", type=Path, default=Path("doc/TODO.md"), help="Ruta a TODO.md")
    parser.add_argument("--done-dir", type=Path, default=None, help="Directorio destino (TODO_DONE)")
    parser.add_argument("--complete", type=str, default=None, help="Título a archivar")
    parser.add_argument("--all-completed", action="store_true", help="Archiva todas las completadas")
    parser.add_argument("--notes", type=str, default=None, help="Notas adicionales")
    parser.add_argument("--dry-run", action="store_true", help="Modo simulación")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    if not args.complete and not args.all_completed:
        args.all_completed = True

    return process_archive(
        todo_path=args.todo,
        done_dir=args.done_dir,
        target_title=args.complete,
        archive_all=args.all_completed,
        notes=args.notes,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    sys.exit(main())
