import sys
from pathlib import Path
import pytest

# Asegurar importación de scripts/ecc-agy/format_commit.py
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from format_commit import (
    validate_commit_message,
    format_commit_message,
)


def test_validate_valid_commit():
    valid_msg = """feat-[cluster]: implement tenant storage manager

Introduce isolated storage telemetry and directory quotas per tenant.
- Enforce hermetic environments in cluster inventory.
- Verified with 100% unit tests passing.
"""
    result = validate_commit_message(valid_msg)
    assert result.is_valid is True
    assert result.commit_type == "feat"
    assert result.projects == ("cluster",)
    assert result.title == "implement tenant storage manager"
    assert result.body_length > 20
    assert len(result.errors) == 0


def test_validate_multi_project_commit():
    multi_proj_msg = """fix-[kakebo,cluster]: resolve cross-service jwt verification

Normalize curve parameters and ensure public keys match Ed25519 specification.
- Verified with auth actuator health tests.
"""
    result = validate_commit_message(multi_proj_msg)
    assert result.is_valid is True
    assert result.commit_type == "fix"
    assert result.projects == ("kakebo", "cluster")
    assert len(result.errors) == 0


def test_validate_ecc_agy_commit():
    ecc_msg = """feat-[ecc-agy]: incorporar baseline de software reliability engineering sre

- Formalizar regla transversal de SRE en AGENTS.md, rules/AGENTS.md y .gemini/GEMINI.md.
- Crear skill sre-reliability/SKILL.md y agente sre-engineer.md con presupuesto de tokens acotado.
- Sincronizar plugin global en ~/.gemini/config/plugins/ecc-agy/.
- Verificado con audit-workspace.ps1 (6/6 fases OK).
"""
    result = validate_commit_message(ecc_msg)
    assert result.is_valid is True
    assert result.commit_type == "feat"
    assert result.projects == ("ecc-agy",)
    assert result.title == "incorporar baseline de software reliability engineering sre"
    assert len(result.errors) == 0


def test_validate_backwards_compatible_plus_commit():
    # Asegura compatibilidad hacia atrás con commits previos que usaban '+'
    legacy_msg = """feat+[ecc-agy]: legacy format with plus

This commit uses the legacy plus separator and must still validate cleanly.
- Preserves backwards compatibility with git history.
"""
    result = validate_commit_message(legacy_msg)
    assert result.is_valid is True
    assert result.commit_type == "feat"
    assert result.projects == ("ecc-agy",)
    assert len(result.errors) == 0


def test_validate_rejects_single_line_commit():
    single_line = "feat-[cluster]: quick commit without explanation"
    result = validate_commit_message(single_line, strict=True)
    assert result.is_valid is False
    assert any("Cuerpo explicativo" in e for e in result.errors)


def test_validate_rejects_invalid_title_format():
    invalid_header = """invalidtype-[cluster]: standard commit format

Here is an explanation of the change that is long enough.
"""
    result = validate_commit_message(invalid_header)
    assert result.is_valid is False
    assert any("Tipo 'invalidtype' no reconocido" in e for e in result.errors)


def test_format_commit_message():
    output = format_commit_message(
        commit_type="refactor",
        projects=["net", "cluster"],
        title="streamline traefik dynamic routing",
        body="Consolidated entrypoints and verified TLS passthrough.",
    )
    assert output.startswith("refactor-[net,cluster]: streamline traefik dynamic routing\n\n")
    assert "Consolidated entrypoints" in output

    # Validar que el resultado de format_commit_message pasa la validación
    result = validate_commit_message(output)
    assert result.is_valid is True
