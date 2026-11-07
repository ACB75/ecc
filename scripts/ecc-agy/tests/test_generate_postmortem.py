import sys
import tempfile
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from generate_postmortem import (
    slugify_branch_name,
    format_postmortem_markdown,
    generate_postmortem_file,
    PostMortemMetadata
)

def test_slugify_branch_name():
    assert slugify_branch_name("fix/SEC-001") == "fix_sec_001"
    assert slugify_branch_name("fix/kakebo/issue-102") == "fix_kakebo_issue_102"
    assert slugify_branch_name("fix/cluster/timeout_p99") == "fix_cluster_timeout_p99"

def test_format_postmortem_markdown():
    meta = PostMortemMetadata(
        branch_name="fix/auth-leak",
        author="SRE Engineer",
        timestamp_utc="2026-11-07T22:00:00Z",
        affected_files=["services/auth/login.go"],
        diff_summary="1 file changed, 2 insertions(+), 1 deletion(-)",
        environment="SANDBOX"
    )
    template = """# Post-Mortem 5W: {{BRANCH}}
- **Fecha UTC:** {{TIMESTAMP_UTC}}
- **Autor:** {{AUTHOR}}
- **Entorno:** {{ENVIRONMENT}}
- **Diff:** {{DIFF_SUMMARY}}
"""
    result = format_postmortem_markdown(meta, template)
    assert "Post-Mortem 5W: fix/auth-leak" in result
    assert "2026-11-07T22:00:00Z" in result
    assert "SRE Engineer" in result
    assert "SANDBOX" in result

def test_generate_postmortem_file_creates_file_in_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        out_dir = Path(tmpdir) / "post-mortem"
        out_dir.mkdir()
        tpl = out_dir / "TEMPLATE.md"
        tpl.write_text("# Template {{BRANCH}} - {{AUTHOR}}", encoding="utf-8")

        created_file = generate_postmortem_file(
            output_dir=out_dir,
            template_path=tpl,
            branch_name="fix/kakebo/jwt-leak",
            author="DevOps",
            diff_stat="1 file changed"
        )

        assert created_file.is_file()
        assert created_file.name.startswith("PM_fix_kakebo_jwt_leak_")
        assert created_file.name.endswith(".md")

        content = created_file.read_text(encoding="utf-8")
        assert "fix/kakebo/jwt-leak" in content
        assert "DevOps" in content
