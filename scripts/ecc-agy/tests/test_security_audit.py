"""
Tests unitarios para la auditoría estática de seguridad y detección de secretos (security_audit.py).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from security_audit import (
    scan_secrets_in_content,
    scan_command_injections,
)


def test_scan_secrets_detection():
    clean_text = "const apiKey = process.env.API_KEY;"
    findings = scan_secrets_in_content("config.ts", clean_text)
    assert len(findings) == 0

    dirty_text = "const secret = 'ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890';"
    findings_dirty = scan_secrets_in_content("config.ts", dirty_text)
    assert len(findings_dirty) >= 1
    assert any("GitHub-Token" in f.rule_id or "SECRET" in f.rule_id for f in findings_dirty)


def test_scan_command_injections():
    safe_call = "subprocess.run(['git', 'status'], check=True)"
    findings_safe = scan_command_injections("script.py", safe_call)
    assert len(findings_safe) == 0

    unsafe_call = "subprocess.run(f'git commit -m {user_input}', shell=True)"
    findings_unsafe = scan_command_injections("script.py", unsafe_call)
    assert len(findings_unsafe) >= 1
