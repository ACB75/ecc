import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from validate_branch import (
    validate_branch_name,
    is_fix_branch
)

@pytest.mark.parametrize("branch", [
    "fix/SEC-001",
    "fix/auth-leak",
    "fix/kakebo/issue-102",
    "fix/cluster/timeout-p99",
    "fix/login-redirect-302",
])
def test_valid_fix_branches(branch: str):
    valid, msg = validate_branch_name(branch)
    assert valid is True
    assert msg == "OK"
    assert is_fix_branch(branch) is True

@pytest.mark.parametrize("branch", [
    "feat/ecc/new-feature",
    "feat/cluster-portal",
    "refactor/kakebo/signals",
    "infra/cluster/traefik-v3",
    "chore/deps-update",
    "docs/adr-0012",
    "test/e2e-auth",
])
def test_valid_task_branches(branch: str):
    valid, msg = validate_branch_name(branch)
    assert valid is True
    assert msg == "OK"
    assert is_fix_branch(branch) is False

@pytest.mark.parametrize("branch", [
    "main",
    "master",
    "bugfix/broken",
    "hotfix/urgent",
    "patch/memory",
    "FEAT/UPPERCASE",
    "fix/has space in name",
    "invalid_no_slash",
    "feat//double-slash",
    "feat/trailing-slash/",
])
def test_invalid_task_branches(branch: str):
    valid, msg = validate_branch_name(branch)
    assert valid is False
    assert "no cumple la convención canónica" in msg or "no permitida" in msg
