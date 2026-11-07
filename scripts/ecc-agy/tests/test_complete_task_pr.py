"""Tests para consolidación y auditoría de complete-task-pr."""

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent


def test_validate_branch_integration():
    """Verifica que validate_branch.py sea ejecutable y valide ramas correctamente."""
    script_path = REPO_ROOT / "scripts" / "ecc-agy" / "validate_branch.py"
    assert script_path.exists(), "validate_branch.py debe existir"

    # Rama válida
    res_valid = subprocess.run(
        [sys.executable, str(script_path), "--branch", "feat/ecc/consolidate-complete-task-pr"],
        capture_output=True,
        text=True,
    )
    assert res_valid.returncode == 0
    assert "[PASS]" in res_valid.stdout

    # Rama no permitida (directo a main)
    res_invalid = subprocess.run(
        [sys.executable, str(script_path), "--branch", "main"],
        capture_output=True,
        text=True,
    )
    assert res_invalid.returncode != 0
    assert "[REJECT]" in res_invalid.stdout


def test_todo_contains_completed_items_regex():
    """Verifica que la expresión regular detecte correctamente tareas completadas."""
    pattern = re.compile(r"^[\s*\-]*\[x\]", re.MULTILINE | re.IGNORECASE)

    sample_active = "# TODO\n* [ ] Tarea pendiente 1\n* [ ] Tarea pendiente 2\n"
    assert not pattern.search(sample_active)

    sample_with_done = "# TODO\n* [x] Tarea completada\n* [ ] Tarea pendiente 2\n"
    assert pattern.search(sample_with_done) is not None

    sample_dash = "- [X] Tarea completada con guion\n"
    assert pattern.search(sample_dash) is not None


def test_scripts_bin_permissions_and_existence():
    """Verifica la existencia y sintaxis básica de los scripts de cierre."""
    ps1_script = REPO_ROOT / "scripts" / "bin" / "ecc-agy" / "complete-task-pr.ps1"
    sh_script = REPO_ROOT / "scripts" / "bin" / "ecc-agy" / "complete-task-pr.sh"

    assert ps1_script.exists(), "complete-task-pr.ps1 debe existir"
    assert sh_script.exists(), "complete-task-pr.sh debe existir"

    # Verificar que el script shell use finales de línea LF (\n)
    sh_content = sh_script.read_bytes()
    assert b"\r\n" not in sh_content, "complete-task-pr.sh debe usar finales de línea LF estrictos"


def test_preflight_review_mode_dryrun():
    """Verifica que complete-task-pr proteja main o ejecute -ReviewOnly en rama de tarea."""
    ps1_script = REPO_ROOT / "scripts" / "bin" / "ecc-agy" / "complete-task-pr.ps1"
    res = subprocess.run(
        ["pwsh", "-NoProfile", "-File", str(ps1_script), "-ReviewOnly"],
        capture_output=True,
        text=True,
    )
    current_branch = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True,
        text=True,
    ).stdout.strip()

    if current_branch in ("main", "master"):
        assert res.returncode != 0
        assert "gobernanza" in res.stderr.lower() or "rama" in res.stderr.lower()
    else:
        assert res.returncode == 0
        assert "AVISO DE" in res.stdout
        assert "Modo -ReviewOnly" in res.stdout
