"""
Tests unitarios para el ciclo de vida y archivo de TODOs (archive_todo.py).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from archive_todo import (
    adjust_relative_links,
    parse_todo_file,
    process_archive,
    slugify_title,
)


def test_slugify_title():
    assert slugify_title("Tarea 2.1: Auditoría y Poda de Contexto") == "Tarea_2_1_Auditoria_y_Poda_de_Contexto"
    assert slugify_title("[docs](http://example.com) Link Title") == "docs_Link_Title"
    assert slugify_title("") == "TAREA"


def test_adjust_relative_links(tmp_path):
    source_dir = tmp_path / "doc"
    source_dir.mkdir()
    target_dir = tmp_path / "doc" / "TODO_DONE"
    target_dir.mkdir()

    text = "Ver archivo [manual](manual/GUIA.md)."
    adjusted = adjust_relative_links(text, source_dir, target_dir)
    assert "../manual/GUIA.md" in adjusted


def test_parse_todo_file_and_process_archive(tmp_path):
    todo_file = tmp_path / "TODO.md"
    todo_content = """# BACKLOG

* [ ] **Tarea 1.1: Pendiente**
  * Detalle pendiente.

* [x] **Tarea 2.1: Completada**
  * Detalle completado línea 1.
  * Detalle completado línea 2.

* [ ] **Tarea 3.1: Otra pendiente**
"""
    todo_file.write_text(todo_content, encoding="utf-8")
    done_dir = tmp_path / "TODO_DONE"

    # Procesar archivo
    code = process_archive(
        todo_path=todo_file,
        done_dir=done_dir,
        archive_all=True,
        notes="Completado con éxito.",
    )
    assert code == 0

    # Verificar que se generó archivo en TODO_DONE
    archived_files = list(done_dir.glob("TODO_*.md"))
    assert len(archived_files) == 1
    content = archived_files[0].read_text(encoding="utf-8")
    assert "Tarea 2.1: Completada" in content
    assert "Completado con éxito." in content

    # Verificar que el TODO.md original se podó y sólo contiene tareas pendientes
    remaining_todo = todo_file.read_text(encoding="utf-8")
    assert "Tarea 2.1: Completada" not in remaining_todo
    assert "Tarea 1.1: Pendiente" in remaining_todo
    assert "Tarea 3.1: Otra pendiente" in remaining_todo
