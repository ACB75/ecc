#!/usr/bin/env python3
"""
Security & Secrets Static Auditor (NIST SP 800-63-4, OWASP Top 10).

Audita archivos de código y configuración en busca de:
  1. Secretos y credenciales expuestas (GitHub tokens, AWS keys, JWTs, private keys).
  2. Patrones de inyección de comandos shell (shell=True con interpolación, os.system).
  3. Comprobaciones de seguridad operativa.
"""

from __future__ import annotations

import argparse
import logging
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("security-audit")

EXCLUDED_DIRS = {
    ".git", ".gemini", ".antigravity", ".vscode", "node_modules",
    "target", "dist", ".angular", "bin", "obj", "__pycache__",
    ".pytest_cache", ".venv", "venv", "scratch", "brain",
}

SECRET_PATTERNS = [
    ("GitHub Token", re.compile(r"\b(ghp_[A-Za-z0-9_]{36,}|github_pat_[A-Za-z0-9_]{60,})\b")),
    ("AWS Access Key", re.compile(r"\b(AKIA[0-9A-Z]{16})\b")),
    ("Private Key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("Hardcoded Password", re.compile(r"""(?:password|passwd|pwd|secret)\s*[:=]\s*['"][^'"\s]{8,}['"]""", re.IGNORECASE)),
]

INJECTION_PATTERNS = [
    ("Subprocess Shell Injection", re.compile(r"""subprocess\.(?:run|Popen|call|check_output)\s*\([^)]*shell\s*=\s*True""")),
    ("os.system Usage", re.compile(r"""\bos\.system\s*\(""")),
]


@dataclass(frozen=True)
class SecurityFinding:
    rule_id: str
    severity: str  # HIGH, MEDIUM, LOW
    file_path: str
    line: int
    message: str


def iter_scannable_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            if ext in {".py", ".ts", ".js", ".json", ".yml", ".yaml", ".env", ".ps1", ".sh"}:
                p = Path(dirpath) / fname
                yield p


def scan_secrets_in_content(file_path: str, content: str) -> List[SecurityFinding]:
    findings: List[SecurityFinding] = []
    # Ignorar archivos de tests explícitos para no alertar sobre strings sintéticos de prueba
    if "test_" in file_path or "_test" in file_path:
        return findings

    lines = content.splitlines()
    for line_idx, line in enumerate(lines, 1):
        for name, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                # Descartar si es un placeholder como <YOUR_KEY> o process.env
                if "process.env" in line or "os.environ" in line or "example" in line.lower():
                    continue
                findings.append(
                    SecurityFinding(
                        rule_id=f"SEC-SECRET-{name.replace(' ', '-')}",
                        severity="HIGH",
                        file_path=file_path,
                        line=line_idx,
                        message=f"Possible hardcoded credential detected: {name}",
                    )
                )
    return findings


def scan_command_injections(file_path: str, content: str) -> List[SecurityFinding]:
    findings: List[SecurityFinding] = []
    if "test_" in file_path or "_test" in file_path:
        return findings

    lines = content.splitlines()
    for line_idx, line in enumerate(lines, 1):
        for name, pattern in INJECTION_PATTERNS:
            if pattern.search(line):
                findings.append(
                    SecurityFinding(
                        rule_id="SEC-INJECTION-SHELL",
                        severity="HIGH",
                        file_path=file_path,
                        line=line_idx,
                        message=f"Unsafe shell execution pattern detected: {name}",
                    )
                )
    return findings


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Static Security & Secrets Auditor.")
    parser.add_argument("--root", type=Path, default=None, help="Directorio raíz a escanear.")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve() if args.root else Path(__file__).resolve().parent.parent.parent

    logger.info("Iniciando escaneo de seguridad en: %s", root)
    findings: List[SecurityFinding] = []

    for path in iter_scannable_files(root):
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        findings.extend(scan_secrets_in_content(str(path), content))
        findings.extend(scan_command_injections(str(path), content))

    if not findings:
        logger.info("[PASS] Escaneo de seguridad finalizado sin vulnerabilidades detectadas.")
        return 0

    logger.warning("\n[FAIL] Se detectaron %d problemas de seguridad:", len(findings))
    for f in findings:
        logger.warning("  [%s][%s] %s:%d - %s", f.severity, f.rule_id, f.file_path, f.line, f.message)
    return 1


if __name__ == "__main__":
    sys.exit(main())
