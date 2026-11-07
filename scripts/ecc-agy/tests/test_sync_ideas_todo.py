import os
import sys
import tempfile
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sync_ideas_todo import (
    IdeaItem,
    parse_ideas_file,
    transform_to_7_phases,
    inject_task_into_todo,
    sync_ideas
)

def test_parse_ideas_file_extracts_approved_ideas():
    sample_content = """# IDEAS BACKLOG
## Idea 1: Telemetry Exporter
- Status: Approved
- Sector: Observability & SRE
- DataType: OTLP metrics
- Objective: Export p95 latency to Prometheus
- Description: Needs native OpenTelemetry exporter in cluster app.

## Idea 2: Draft Idea
- Status: Draft
- Sector: Marketing
- DataType: Text
- Objective: Write blog post
- Description: Draft text.
"""
    ideas = parse_ideas_file(sample_content)
    assert len(ideas) == 1
    assert ideas[0].title == "Telemetry Exporter"
    assert ideas[0].status == "Approved"
    assert ideas[0].sector == "Observability & SRE"

def test_transform_to_7_phases_generates_correct_sections():
    idea = IdeaItem(
        title="Telemetry Exporter",
        status="Approved",
        sector="Observability & SRE",
        data_type="OTLP metrics",
        objective="Export p95 latency to Prometheus",
        description="Needs native OpenTelemetry exporter in cluster app."
    )
    task_md = transform_to_7_phases(idea)
    assert "* [ ] **Tarea: Telemetry Exporter**" in task_md
    assert "* **01 - ROLE:**" in task_md
    assert "[Sector: Observability & SRE]" in task_md
    assert "[Data Type: OTLP metrics]" in task_md
    assert "* **03 - PHASE 1 (ANALYSIS):**" in task_md
    assert "* **04 - PHASE 2 (STRATEGY):**" in task_md
    assert "* **05 - PHASE 3 (EXECUTION):**" in task_md
    assert "* **06 - PHASE 4 (CRITIC):**" in task_md
    assert "* **07 - PHASE 5 (FORMAT):**" in task_md

def test_inject_task_into_todo_prevents_duplicates():
    todo_content = """# PROTOCOLO DE EJECUCIÓN
## 1. Prioridad 1: Tareas
* [ ] **Tarea: Telemetry Exporter**
  * **01 - ROLE:** Lead SRE
"""
    transformed = "* [ ] **Tarea: Telemetry Exporter**\n  * **01 - ROLE:** New"
    res = inject_task_into_todo(todo_content, transformed, "Telemetry Exporter")
    assert res == todo_content  # No duplication

def test_sync_ideas_end_to_end():
    with tempfile.TemporaryDirectory() as tmpdir:
        ideas_p = Path(tmpdir) / "IDEAS.md"
        todo_p = Path(tmpdir) / "TODO.md"

        ideas_p.write_text("""# IDEAS
## Idea 1: New Feature
- Status: Approved
- Sector: Core
- DataType: JSON
- Objective: Build new feature
- Description: Feature details.
""", encoding="utf-8")

        todo_p.write_text("""# BACKLOG\n## 1. Active Tasks\n""", encoding="utf-8")

        synced = sync_ideas(ideas_p, todo_p, dry_run=False)
        assert synced == 1

        new_todo = todo_p.read_text(encoding="utf-8")
        assert "Tarea: New Feature" in new_todo
        assert "[Sector: Core]" in new_todo
