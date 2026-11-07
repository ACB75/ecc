import os
import sys
import tempfile
import shutil
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from execute_sweep import (
    purge_skills,
    purge_agents,
    optimize_skills,
    _parse_frontmatter_lines,
    DELETION_SET,
    ALIEN_AGENTS
)

def test_parse_frontmatter_lines_normalizes_description():
    lines = [
        "name: test-skill",
        "description: " + ("a" * 150),
        "tools: Read, Grep"
    ]
    new_lines, desc = _parse_frontmatter_lines(lines, "test-skill")
    assert len(desc) <= 140
    assert desc.endswith("...")
    assert any(line.startswith("name: test-skill") for line in new_lines)
    assert any(line.startswith('description: "') for line in new_lines)

def test_parse_frontmatter_lines_defaults_missing_description():
    lines = [
        "name: default-skill",
        "tools: Read"
    ]
    new_lines, desc = _parse_frontmatter_lines(lines, "default-skill")
    assert "default-skill" in desc
    assert len(desc) <= 140

def test_purge_skills_and_agents_in_temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        skills_dir = os.path.join(tmpdir, "skills")
        agents_dir = os.path.join(tmpdir, "agents")
        os.makedirs(skills_dir)
        os.makedirs(agents_dir)

        # Create one skill in deletion set and one kept
        del_skill = list(DELETION_SET)[0]
        os.makedirs(os.path.join(skills_dir, del_skill))
        os.makedirs(os.path.join(skills_dir, "kept-skill"))

        # Create one agent in alien set and one kept
        del_agent = ALIEN_AGENTS[0]
        with open(os.path.join(agents_dir, del_agent), "w", encoding="utf-8") as f:
            f.write("# alien")
        with open(os.path.join(agents_dir, "kept-agent.md"), "w", encoding="utf-8") as f:
            f.write("# kept")

        del_s = purge_skills(tmpdir)
        del_a = purge_agents(tmpdir)

        assert del_s == 1
        assert del_a == 1
        assert not os.path.exists(os.path.join(skills_dir, del_skill))
        assert os.path.exists(os.path.join(skills_dir, "kept-skill"))
        assert not os.path.exists(os.path.join(agents_dir, del_agent))
        assert os.path.exists(os.path.join(agents_dir, "kept-agent.md"))

def test_optimize_skills_rewrites_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        skills_dir = os.path.join(tmpdir, "skills")
        target_skill = os.path.join(skills_dir, "sample-skill")
        os.makedirs(target_skill)
        skill_file = os.path.join(target_skill, "SKILL.md")

        raw_content = "---\nname: sample-skill\ndescription: " + ("x" * 160) + "\n---\n# Sample Body\n"
        with open(skill_file, "w", encoding="utf-8") as f:
            f.write(raw_content)

        updated = optimize_skills(tmpdir)
        assert updated == 1

        with open(skill_file, "r", encoding="utf-8") as f:
            new_content = f.read()

        assert "# Sample Body" in new_content
        assert len(new_content) < len(raw_content)
