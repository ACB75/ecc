#!/usr/bin/env python3
"""
scripts/ecc-agy/format_commit.py - Validador y Generador de Mensajes de Commit Estandarizados

Soporta formatos Conventional Commits flexibles y ergonómicos:
  1. Formato extendido de monorepo: [type]+[projects]: <title>  (ej. feat+[doc]: update todo.md)
  2. Formato con guión: type-project: <title>                  (ej. feat-doc: update todo.md)
  3. Formato convencional estándar: type(project): <title>     (ej. feat(doc): update todo.md)
  4. Formato convencional simple: type: <title>                (ej. feat: update todo.md)

Garantiza codificación UTF-8 limpia en cualquier terminal (Windows 11 / Linux / Git Bash / VSCode)
y permite commits interactivos de una sola línea sin bloquear al desarrollador.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import logging
import os
from pathlib import Path
import re
import sys
from typing import List, Optional, Sequence, Tuple

# Configurar codificación UTF-8 estricta para evitar caracteres escapados \u2717 o distorsionados
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger: logging.Logger = logging.getLogger("format-commit")

ALLOWED_TYPES: frozenset[str] = frozenset({
    "feat", "fix", "refactor", "chore", "docs", "doc", "test", "tests",
    "perf", "build", "ci", "sec", "security", "style", "revert",
})

ALLOWED_PROJECTS: frozenset[str] = frozenset({
    "cluster", "kakebo", "whoiam", "net", "scripts", "ecc", "ecc-agy", "ecc-aecb", "ecc-claude", "ecc-agy-homelab", "doc",
    "docs", "infra", "portal", "token-hill", "uoc", "sdk", "home-lab-sdk", "all",
})


@dataclass(frozen=True)
class CommitValidationResult:
    is_valid: bool
    commit_type: str
    projects: Tuple[str, ...]
    title: str
    body_length: int
    errors: Tuple[str, ...]


def parse_commit_header(first_line: str) -> Tuple[Optional[str], List[str], str]:
    """Parsea el encabezado del commit soportando múltiples sintaxis ergonómicas."""
    line = first_line.strip()
    if not line:
        return None, [], ""

    # 1. Formato monorepo extendido: type+[projects]: title  (ej. feat+[doc]: ...)
    m1 = re.match(r"^\[?([a-zA-Z0-9_-]+)\]?[-+]\[([a-zA-Z0-9_,-]+)\]:\s*(.+)$", line)
    if m1:
        t = m1.group(1).lower()
        projs = [p.strip().lower() for p in m1.group(2).split(",") if p.strip()]
        return t, projs, m1.group(3).strip()

    # 2. Formato con guión: type-project: title  (ej. feat-doc: update todo.md)
    m2 = re.match(r"^([a-zA-Z0-9_]+)-([a-zA-Z0-9_-]+):\s*(.+)$", line)
    if m2:
        t = m2.group(1).lower()
        proj = m2.group(2).lower()
        if t in ALLOWED_TYPES and proj in ALLOWED_PROJECTS:
            return t, [proj], m2.group(3).strip()

    # 3. Formato convencional con ámbito: type(projects): title (ej. feat(doc): ...)
    m3 = re.match(r"^([a-zA-Z0-9_-]+)\(([a-zA-Z0-9_,-]+)\):\s*(.+)$", line)
    if m3:
        t = m3.group(1).lower()
        projs = [p.strip().lower() for p in m3.group(2).split(",") if p.strip()]
        return t, projs, m3.group(3).strip()

    # 4. Formato con barra: type/project: title (ej. feat/doc: ...)
    m4 = re.match(r"^([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+):\s*(.+)$", line)
    if m4:
        t = m4.group(1).lower()
        proj = m4.group(2).lower()
        if t in ALLOWED_TYPES and proj in ALLOWED_PROJECTS:
            return t, [proj], m4.group(3).strip()

    # 5. Formato convencional simple: type: title (ej. feat: update todo.md, docs: ...)
    m5 = re.match(r"^([a-zA-Z0-9_-]+):\s*(.+)$", line)
    if m5:
        t = m5.group(1).lower()
        if t in ALLOWED_TYPES:
            return t, [], m5.group(2).strip()

    return None, [], line


def validate_commit_message(message: str, strict: bool = False) -> CommitValidationResult:
    """Valida un mensaje de commit permitiendo tanto commits estructurados como interactivos."""
    raw = message.strip()
    if not raw:
        return CommitValidationResult(False, "", (), "", 0, ("El mensaje de commit esta vacio.",))

    # Filtrar comentarios de git (lineas que empiezan con #)
    lines = [line for line in raw.splitlines() if not line.strip().startswith("#")]
    if not lines:
        return CommitValidationResult(False, "", (), "", 0, ("El mensaje de commit solo contiene comentarios.",))

    first_line = lines[0].strip()
    errors: List[str] = []

    commit_type, projects, title = parse_commit_header(first_line)

    if commit_type is None:
        errors.append(
            f"El formato del titulo no es reconocido: '{first_line}'.\n"
            f"  Formatos validos admitidos:\n"
            f"    - feat-doc: <titulo>              (formato rapido por proyecto)\n"
            f"    - feat(doc): <titulo>             (Conventional Commits estandar)\n"
            f"    - feat-[doc]: <titulo>            (monorepo extendido, ej. feat-[ecc-agy]: ...)\n"
            f"    - feat: <titulo>                  (Conventional Commits simple)\n"
            f"  Tipos permitidos: {', '.join(sorted(ALLOWED_TYPES))}"
        )
    else:
        if commit_type not in ALLOWED_TYPES:
            errors.append(
                f"Tipo '{commit_type}' no reconocido. Tipos permitidos: {', '.join(sorted(ALLOWED_TYPES))}"
            )

        for proj in projects:
            if proj not in ALLOWED_PROJECTS:
                errors.append(
                    f"Proyecto '[{proj}]' no reconocido. Proyectos permitidos: {', '.join(sorted(ALLOWED_PROJECTS))}"
                )

        if not title:
            errors.append("El titulo del commit no puede estar vacio.")

    # Analizar cuerpo explicativo
    body_lines = lines[1:]
    if body_lines and not body_lines[0].strip():
        body_lines = body_lines[1:]

    body_text = "\n".join(body_lines).strip()
    body_length = len(body_text)

    # Validacion estricta solo si se solicita explicitamente (--strict para CI o PR gates)
    if strict and body_length < 20:
        errors.append(
            "Cuerpo explicativo (msg comment) insuficiente o ausente bajo modo estricto. "
            "Debe detallar motivacion, modulos afectados y verificaciones realizadas."
        )

    return CommitValidationResult(
        is_valid=len(errors) == 0,
        commit_type=commit_type or "",
        projects=tuple(projects),
        title=title,
        body_length=body_length,
        errors=tuple(errors),
    )


def format_commit_message(
    commit_type: str,
    projects: Sequence[str],
    title: str,
    body: str,
) -> str:
    """Genera un mensaje de commit estructurado en formato monorepo canónico."""
    clean_type = commit_type.strip().lower()
    proj_tag = ",".join(p.strip().lower() for p in projects if p.strip())
    clean_title = title.strip()
    clean_body = body.strip()

    header = f"{clean_type}-[{proj_tag}]: {clean_title}" if proj_tag else f"{clean_type}: {clean_title}"
    if clean_body:
        return f"{header}\n\n{clean_body}"
    return header


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validador y Generador de Commits Conventional flexibles (soporta type-project: <title>, type+[projects]: <title>)."
    )
    parser.add_argument("--validate", "-v", type=str, help="Cadena de texto del mensaje de commit a validar.")
    parser.add_argument("--validate-file", "-f", type=Path, help="Archivo con el mensaje de commit a validar.")
    parser.add_argument("--strict", action="store_true", help="Exige cuerpo explicativo obligatorio de >=20 caracteres.")
    parser.add_argument("--type", "-t", choices=list(ALLOWED_TYPES), help="Tipo de commit.")
    parser.add_argument("--projects", "-p", type=str, help="Proyectos afectados separados por coma (ej. cluster,net,doc).")
    parser.add_argument("--title", type=str, help="Título del commit.")
    parser.add_argument("--body", "-b", type=str, help="Cuerpo explicativo del commit.")
    parser.add_argument("--json", action="store_true", help="Salida en formato JSON.")

    args = parser.parse_args(argv)

    msg_to_validate: Optional[str] = None
    if args.validate:
        msg_to_validate = args.validate
    elif args.validate_file:
        if not args.validate_file.is_file():
            logger.error("[ERROR] Archivo %s no encontrado.", args.validate_file)
            return 1
        msg_to_validate = args.validate_file.read_text(encoding="utf-8", errors="replace")

    if msg_to_validate is not None:
        result = validate_commit_message(msg_to_validate, strict=args.strict)
        if args.json:
            print(json.dumps(asdict(result), indent=2))
        else:
            if result.is_valid:
                projs_str = f"+[{','.join(result.projects)}]" if result.projects else ""
                logger.info("[OK] Mensaje de commit VALIDO: %s%s: %s", result.commit_type, projs_str, result.title)
                if result.body_length > 0:
                    logger.info("     Cuerpo explicativo: %d caracteres.", result.body_length)
                else:
                    logger.info("     (Modo interactivo: commit de una sola linea aceptado).")
            else:
                logger.error("[FAIL] El mensaje de commit NO cumple las reglas:")
                for err in result.errors:
                    logger.error("  [X] %s", err)
        return 0 if result.is_valid else 1

    if args.type and args.title:
        projs = [p.strip() for p in args.projects.split(",") if p.strip()] if args.projects else []
        body = args.body or ""
        formatted = format_commit_message(args.type, projs, args.title, body)
        print(formatted)
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
