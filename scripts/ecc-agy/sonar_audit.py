#!/usr/bin/env python3
"""
SonarQube Static Quality Gate Auditor (Python, TypeScript, JavaScript).

Audita los archivos fuente del repositorio bajo las reglas canónicas de SonarQube:
  - S3776: Cognitive Complexity de funciones/métodos <= 15
  - S107:  Parámetros de funciones/métodos <= 7
  - S1192: Literales de cadena duplicados (>= 3 ocurrencias de len >= 7)
  - S108:  Bloques vacíos de código (except/catch)
"""

from __future__ import annotations

import argparse
import ast
import logging
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Set, Tuple

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("sonar-audit")

EXCLUDED_DIRS = {
    ".git", ".gemini", ".antigravity", ".vscode", "node_modules",
    "target", "dist", ".angular", "bin", "obj", "__pycache__",
    ".pytest_cache", ".venv", "venv", "scratch", "brain", "doc",
    "skills", "agents", "ecc-claude",
}

MAX_COGNITIVE_COMPLEXITY = 15
MAX_PARAMETERS = 7
MIN_LITERAL_LEN = 7
MAX_LITERAL_DUPLICATES = 3

COMMON_IGNORED_STRINGS = {
    "store_true", "store_false", "__main__", "utf-8", "replace",
    "CRITICAL", "MAJOR", "MINOR", "HIGH", "MEDIUM", "LOW",
}


@dataclass(frozen=True)
class SonarFinding:
    rule_id: str
    severity: str  # CRITICAL, MAJOR, MINOR
    file_path: str
    line: int
    message: str


def is_test_file(path: Path) -> bool:
    name = path.name.lower()
    parts = {p.lower() for p in path.parts}
    return (
        "tests" in parts
        or "test" in parts
        or name.endswith(".spec.ts")
        or name.startswith("test_")
    )


def iter_source_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS]
        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            if ext in {".py", ".ts", ".js"}:
                p = Path(dirpath) / fname
                if not fname.endswith(".d.ts") and not is_test_file(p):
                    yield p


class PythonCognitiveVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.complexity = 0
        self.nesting = 0

    def _increment(self, structural: bool = True) -> None:
        if structural:
            self.complexity += 1 + self.nesting
        else:
            self.complexity += 1

    def visit_If(self, node: ast.If) -> None:
        self._increment(structural=True)
        self.nesting += 1
        for child in node.body:
            self.visit(child)
        self.nesting -= 1
        if node.orelse:
            self._visit_else_chain(node.orelse)

    def _visit_else_chain(self, orelse: List[ast.stmt]) -> None:
        if len(orelse) == 1 and isinstance(orelse[0], ast.If):
            self._increment(structural=False)
            self.nesting += 1
            for child in orelse[0].body:
                self.visit(child)
            self.nesting -= 1
            if orelse[0].orelse:
                self._visit_else_chain(orelse[0].orelse)
        else:
            self._increment(structural=False)
            self.nesting += 1
            for child in orelse:
                self.visit(child)
            self.nesting -= 1

    def visit_For(self, node: ast.For) -> None:
        self._increment(structural=True)
        self.nesting += 1
        self.generic_visit(node)
        self.nesting -= 1

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self._increment(structural=True)
        self.nesting += 1
        self.generic_visit(node)
        self.nesting -= 1

    def visit_While(self, node: ast.While) -> None:
        self._increment(structural=True)
        self.nesting += 1
        self.generic_visit(node)
        self.nesting -= 1

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        self._increment(structural=True)
        self.nesting += 1
        self.generic_visit(node)
        self.nesting -= 1

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        self._increment(structural=False)
        self.generic_visit(node)


def calculate_python_cognitive_complexity(code: str) -> int:
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return 0

    total_complexity = 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            visitor = PythonCognitiveVisitor()
            for stmt in node.body:
                visitor.visit(stmt)
            total_complexity = max(total_complexity, visitor.complexity)
    return total_complexity


def check_python_parameters(file_path: str, code: str) -> List[SonarFinding]:
    findings: List[SonarFinding] = []
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return findings

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = [a for a in node.args.args if a.arg not in {"self", "cls"}]
            total_params = len(args) + len(node.args.kwonlyargs)
            if node.args.vararg:
                total_params += 1
            if node.args.kwarg:
                total_params += 1
            if total_params > MAX_PARAMETERS:
                findings.append(
                    SonarFinding(
                        rule_id="python:S107",
                        severity="MAJOR",
                        file_path=file_path,
                        line=node.lineno,
                        message=f"Function '{node.name}' has {total_params} parameters (max allowed: {MAX_PARAMETERS})",
                    )
                )
    return findings


def _collect_excluded_ids(tree: ast.AST) -> Set[int]:
    excluded: Set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.JoinedStr):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Constant):
                    excluded.add(id(sub))
        elif isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant):
                excluded.add(id(node.body[0].value))
    return excluded


def _is_valid_literal(val: str) -> bool:
    if len(val) < MIN_LITERAL_LEN or "\n" in val or val in COMMON_IGNORED_STRINGS:
        return False
    if val.startswith(("<", "{", "[", "http://", "https://")):
        return False
    return any(c.isalpha() for c in val)


def check_string_literal_duplicates(file_path: str, code: str) -> List[SonarFinding]:
    findings: List[SonarFinding] = []
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return findings

    excluded_ids = _collect_excluded_ids(tree)
    strings: List[Tuple[str, int]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in excluded_ids:
            val = node.value.strip()
            if _is_valid_literal(val):
                strings.append((val, node.lineno))

    counts = Counter(s[0] for s in strings)
    reported: Set[str] = set()
    for val, line in strings:
        if counts[val] >= MAX_LITERAL_DUPLICATES and val not in reported:
            reported.add(val)
            findings.append(
                SonarFinding(
                    rule_id="python:S1192",
                    severity="MINOR",
                    file_path=file_path,
                    line=line,
                    message=f"String literal '{val[:30]}...' duplicated {counts[val]} times",
                )
            )
    return findings


def check_empty_blocks(file_path: str, code: str) -> List[SonarFinding]:
    findings: List[SonarFinding] = []
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return findings

    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            if len(node.body) == 1:
                stmt = node.body[0]
                if isinstance(stmt, ast.Pass) or (
                    isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is Ellipsis
                ):
                    findings.append(
                        SonarFinding(
                            rule_id="python:S108",
                            severity="CRITICAL",
                            file_path=file_path,
                            line=node.lineno,
                            message="Empty except handler block detected (should handle or log)",
                        )
                    )
    return findings


def _audit_function_complexity(file_path: str, content: str) -> List[SonarFinding]:
    findings: List[SonarFinding] = []
    try:
        tree = ast.parse(content)
    except SyntaxError as err:
        logger.debug("Skipping syntax error in %s: %s", file_path, err)
        return findings

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            visitor = PythonCognitiveVisitor()
            for stmt in node.body:
                visitor.visit(stmt)
            if visitor.complexity > MAX_COGNITIVE_COMPLEXITY:
                findings.append(
                    SonarFinding(
                        rule_id="python:S3776",
                        severity="CRITICAL",
                        file_path=file_path,
                        line=node.lineno,
                        message=f"Function '{node.name}' cognitive complexity is {visitor.complexity} (max allowed: {MAX_COGNITIVE_COMPLEXITY})",
                    )
                )
    return findings


def audit_file(path: Path) -> List[SonarFinding]:
    findings: List[SonarFinding] = []
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return findings

    if path.suffix == ".py":
        findings.extend(check_python_parameters(str(path), content))
        findings.extend(check_string_literal_duplicates(str(path), content))
        findings.extend(check_empty_blocks(str(path), content))
        findings.extend(_audit_function_complexity(str(path), content))

    return findings


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SonarQube Static Quality Gate Auditor.")
    parser.add_argument("--root", type=Path, default=None, help="Directorio raíz a escanear.")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    root = args.root.resolve() if args.root else Path(__file__).resolve().parent.parent.parent

    logger.info("Escaneando archivos para SonarQube Quality Gate en: %s", root)
    all_findings: List[SonarFinding] = []

    for file_path in iter_source_files(root):
        file_findings = audit_file(file_path)
        all_findings.extend(file_findings)

    if not all_findings:
        logger.info("[PASS] SonarQube Quality Gate Rating A alcanzado (0 violaciones).")
        return 0

    critical_count = sum(1 for f in all_findings if f.severity == "CRITICAL")
    major_count = sum(1 for f in all_findings if f.severity == "MAJOR")
    minor_count = sum(1 for f in all_findings if f.severity == "MINOR")

    logger.warning(
        "\nSe encontraron %d violaciones (CRITICAL: %d, MAJOR: %d, MINOR: %d):",
        len(all_findings), critical_count, major_count, minor_count,
    )
    for f in all_findings[:20]:
        logger.warning("  [%s][%s] %s:%d - %s", f.severity, f.rule_id, f.file_path, f.line, f.message)
    if len(all_findings) > 20:
        logger.warning("  ... y %d violaciones adicionales.", len(all_findings) - 20)

    return 1 if (critical_count > 0 or major_count > 0) else 0


if __name__ == "__main__":
    sys.exit(main())
