#!/usr/bin/env python3
"""
Módulo de validación de nombres de rama Git en ECC (validate_branch.py).
Enforza la convención canónica de ramas de tarea e incidencias (fix/*).
Cumple con SonarQube Quality Gate A (S3776 <= 15, S1192 sin duplicados).
"""

import argparse
import re
import subprocess
import sys
from typing import Optional, Sequence, Tuple

MSG_OK = "OK"
MSG_RESERVED_BRANCH = "Rama 'main' o 'master' no permitida directamente para desarrollo de tareas."
MSG_INVALID_BRANCH = (
    "Nombre de rama no cumple la convención canónica: "
    "debe seguir <tipo>/<nombre> o <tipo>/<proyecto>/<nombre> "
    "(tipos permitidos: fix, feat, refactor, infra, chore, docs, test)."
)

# Regex canónica de ramas de tarea
BRANCH_REGEX = re.compile(
    r"^(?P<type>fix|feat|refactor|infra|chore|docs|test)/"
    r"(?P<segment1>[a-zA-Z0-9._-]+)"
    r"(?:/(?P<segment2>[a-zA-Z0-9._-]+))?$"
)


def is_fix_branch(branch_name: str) -> bool:
    """Determina si una rama corresponde a una incidencia o corrección."""
    return branch_name.strip().startswith("fix/")


def validate_branch_name(branch_name: str, allow_main: bool = False) -> Tuple[bool, str]:
    """
    Valida si el nombre de rama cumple la política estricta de gobernanza Git.
    Retorna tupla (es_valido, mensaje_error).
    """
    cleaned = branch_name.strip()
    if cleaned in ("main", "master"):
        if allow_main:
            return True, MSG_OK
        return False, MSG_RESERVED_BRANCH

    if " " in cleaned or cleaned.endswith("/") or "//" in cleaned:
        return False, MSG_INVALID_BRANCH

    match = BRANCH_REGEX.match(cleaned)
    if not match:
        return False, MSG_INVALID_BRANCH

    branch_type = match.group("type")
    # Para ramas no-fix, requerir minúsculas consistentes
    if branch_type != "fix":
        if any(c.isupper() for c in cleaned):
            return False, MSG_INVALID_BRANCH

    return True, MSG_OK


def get_current_git_branch() -> str:
    """Obtiene el nombre de la rama activa en el directorio actual."""
    try:
        res = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True,
        )
        return res.stdout.strip()
    except (subprocess.SubprocessError, OSError):
        return ""


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Parsea argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(description="Validador canónico de nombres de rama Git en ECC.")
    parser.add_argument("--branch", type=str, default="", help="Nombre de la rama a validar (por defecto la activa).")
    parser.add_argument("--allow-main", action="store_true", help="Permite 'main' como rama válida.")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Punto de entrada CLI."""
    args = parse_args(argv)
    branch = args.branch or get_current_git_branch()
    if not branch:
        print("[ERROR] No se pudo determinar el nombre de la rama.")
        return 1

    valid, msg = validate_branch_name(branch, allow_main=args.allow_main)
    if not valid:
        print(f"[REJECT] Rama '{branch}' inválida: {msg}")
        return 1

    fix_note = " (Incidencia / Corrección)" if is_fix_branch(branch) else ""
    print(f"[PASS] Rama '{branch}' cumple la convención canónica{fix_note}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
