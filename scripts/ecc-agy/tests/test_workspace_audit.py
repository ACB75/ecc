"""
Tests unitarios para la auditoría de higiene, tokens y presupuesto de contexto (workspace_audit.py).
"""
import sys
from pathlib import Path

# Añadir ruta para importar scripts/ecc-agy
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from workspace_audit import (
    audit_agents,
    audit_skills,
    check_agent,
    clean_targets,
    frontmatter_field,
    read_frontmatter,
    scan_dead_artifacts,
    scan_hygiene,
    AgentTarget,
)


def test_read_frontmatter_and_fields():
    content = """---
name: test-skill
description: "A short valid skill description."
model: flash
---
# Body
Some markdown content.
"""
    fm = read_frontmatter(content)
    assert fm != ""
    assert frontmatter_field(fm, "name") == "test-skill"
    assert frontmatter_field(fm, "description") == "A short valid skill description."
    assert frontmatter_field(fm, "model") == "flash"
    assert frontmatter_field(fm, "non_existent") is None


def test_audit_skills_length_limits(tmp_path):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()

    # Skill válida (<= 140 chars)
    s1 = skills_dir / "valid-skill"
    s1.mkdir()
    (s1 / "SKILL.md").write_text(
        "---\nname: valid-skill\ndescription: \"Short valid description.\"\n---\nBody",
        encoding="utf-8",
    )

    # Skill que excede 140 chars
    s2 = skills_dir / "long-skill"
    s2.mkdir()
    long_desc = "x" * 150
    (s2 / "SKILL.md").write_text(
        f"---\nname: long-skill\ndescription: \"{long_desc}\"\n---\nBody",
        encoding="utf-8",
    )

    count, chars, violations = audit_skills(skills_dir)
    assert count == 2
    assert len(violations) == 1
    assert "long-skill" in violations[0]


def test_audit_agents_rules_and_models(tmp_path):
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir()

    # Agente válido (<= 120 chars, model flash)
    a1 = agents_dir / "valid-agent.md"
    a1.write_text(
        "---\nname: valid-agent\ndescription: \"Short agent desc.\"\nmodel: flash\n---\nBody",
        encoding="utf-8",
    )

    # Agente con descripción larga (> 120 chars)
    a2 = agents_dir / "long-agent.md"
    long_desc = "a" * 130
    a2.write_text(
        f"---\nname: long-agent\ndescription: \"{long_desc}\"\nmodel: inherit\n---\nBody",
        encoding="utf-8",
    )

    # Agente con modelo no óptimo
    a3 = agents_dir / "bad-model-agent.md"
    a3.write_text(
        "---\nname: bad-model\ndescription: \"Desc\"\nmodel: pro\n---\nBody",
        encoding="utf-8",
    )

    # Agente read-only con tools de escritura
    a4 = agents_dir / "code-reviewer.md"
    a4.write_text(
        "---\nname: code-reviewer\ndescription: \"Reviews code.\"\nmodel: flash\ntools:\n  - edit_file\n---\nBody",
        encoding="utf-8",
    )

    count, chars, violations = audit_agents(agents_dir)
    assert count == 4
    assert any("long-agent.md" in v for v in violations)
    assert any("bad-model-agent.md" in v and "pro" in v for v in violations)
    assert any("code-reviewer.md" in v and "write tools" in v for v in violations)


def test_scan_hygiene_and_clean(tmp_path):
    # Crear backups y cachés
    bak_file = tmp_path / "test.bak"
    bak_file.write_text("old", encoding="utf-8")
    cache_dir = tmp_path / "__pycache__"
    cache_dir.mkdir()
    (cache_dir / "test.pyc").write_text("compiled", encoding="utf-8")
    empty_dir = tmp_path / "empty_folder"
    empty_dir.mkdir()

    report = scan_hygiene(tmp_path)
    assert len(report.backups) == 1
    assert len(report.caches) == 1
    assert len(report.empty_dirs) == 1

    clean_targets(report.all_targets())
    assert not bak_file.exists()
    assert not cache_dir.exists()
    assert not empty_dir.exists()


def test_scan_dead_artifacts(tmp_path):
    target_dir = tmp_path / "project"
    target_dir.mkdir()
    skills_dir = target_dir / "skills"
    skills_dir.mkdir()

    # Skill huérfana (directorio sin SKILL.md)
    orphan_skill = skills_dir / "broken-skill"
    orphan_skill.mkdir()

    target = AgentTarget("test-proj", target_dir)
    report = scan_dead_artifacts([target])
    assert len(report.orphan_skill_dirs) == 1
    assert report.total_issues >= 1
