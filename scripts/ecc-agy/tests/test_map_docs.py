import os
import sys
import tempfile
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from map_docs import (
    DocLink,
    extract_links_from_markdown,
    validate_links,
    generate_report
)

def test_extract_links_from_markdown():
    sample = """# Documentation Index
Check out [Architecture Overview](./architecture.md) and [Guide](../guide.md#section).
Also external link [Google](https://google.com) and mailto [Email](mailto:dev@example.com).
"""
    file_path = Path("/tmp/doc/index.md")
    links = extract_links_from_markdown(file_path, sample)
    targets = [l.target_path for l in links]
    assert "./architecture.md" in targets
    assert "../guide.md#section" in targets
    # External and mailto should be excluded from relative link validation
    assert "https://google.com" not in targets
    assert "mailto:dev@example.com" not in targets

def test_validate_links_detects_broken_and_valid():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        doc_dir = root / "doc"
        doc_dir.mkdir()

        index_md = doc_dir / "index.md"
        valid_md = doc_dir / "valid.md"
        valid_md.write_text("# Valid target", encoding="utf-8")

        index_md.write_text("""# Index
Link to [Valid](valid.md) and [Broken](broken.md).
""", encoding="utf-8")

        links = validate_links(doc_dir)
        assert len(links) == 2
        valid_link = next(l for l in links if "valid.md" in l.target_path)
        broken_link = next(l for l in links if "broken.md" in l.target_path)

        assert valid_link.is_valid is True
        assert broken_link.is_valid is False

def test_generate_report_formats_cleanly():
    links = [
        DocLink(source_file=Path("doc/index.md"), line_no=5, link_text="Broken", target_path="missing.md", is_valid=False),
        DocLink(source_file=Path("doc/index.md"), line_no=2, link_text="Valid", target_path="ok.md", is_valid=True)
    ]
    broken_count, report_text = generate_report(links)
    assert broken_count == 1
    assert "missing.md" in report_text
    assert "doc/index.md:5" in report_text
