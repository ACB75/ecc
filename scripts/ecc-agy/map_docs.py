#!/usr/bin/env python3
"""
Módulo de auditoría, mapeo y validación de enlaces relativos en documentación Markdown (map_docs.py).
Detecta enlaces rotos en doc/ y genera un informe de salud documental estructurado.
Cumple con SonarQube Quality Gate A (S3776 <= 15, S1192 sin duplicados).
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

# Regex para extraer enlaces Markdown: [texto](destino)
MD_LINK_REGEX = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
IGNORED_SCHEMES = ("http://", "https://", "mailto:", "ftp://", "file://")


@dataclass(frozen=True)
class DocLink:
    """Representa un enlace extraído de un archivo Markdown."""
    source_file: Path
    line_no: int
    link_text: str
    target_path: str
    is_valid: bool


def _is_relative_doc_link(raw_target: str) -> bool:
    """Verifica si el enlace es una referencia relativa interna a archivo."""
    trimmed = raw_target.strip()
    if not trimmed or trimmed.startswith("#"):
        return False
    return not any(trimmed.startswith(scheme) for scheme in IGNORED_SCHEMES)


def extract_links_from_markdown(file_path: Path, content: str) -> List[DocLink]:
    """Extrae enlaces relativos de un archivo Markdown, ignorando bloques y fragmentos de código."""
    links: List[DocLink] = []
    in_fence = False
    for line_idx, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        sanitized_line = re.sub(r"`[^`]*`", "", line)
        for match in MD_LINK_REGEX.finditer(sanitized_line):
            text = match.group(1).strip()
            target = match.group(2).strip()
            if _is_relative_doc_link(target):
                links.append(
                    DocLink(
                        source_file=file_path,
                        line_no=line_idx,
                        link_text=text,
                        target_path=target,
                        is_valid=False,
                    )
                )
    return links


def _resolve_link_target(source_file: Path, target_path: str) -> bool:
    """Comprueba la existencia del archivo de destino en disco."""
    # Eliminar anchor #section si existe
    clean_target = target_path.split("#", 1)[0].strip()
    if not clean_target:
        return True  # Anchor interno
    resolved = (source_file.parent / clean_target).resolve()
    return resolved.exists()


def validate_links(doc_root: Path) -> List[DocLink]:
    """Escanea y valida todos los enlaces relativos bajo doc_root."""
    results: List[DocLink] = []
    if not doc_root.exists():
        return results

    md_files = [doc_root] if doc_root.is_file() else list(doc_root.rglob("*.md"))
    for md_file in md_files:
        try:
            content = md_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        extracted = extract_links_from_markdown(md_file, content)
        for link in extracted:
            valid = _resolve_link_target(link.source_file, link.target_path)
            results.append(
                DocLink(
                    source_file=link.source_file,
                    line_no=link.line_no,
                    link_text=link.link_text,
                    target_path=link.target_path,
                    is_valid=valid,
                )
            )
    return results


def generate_report(links: List[DocLink]) -> Tuple[int, str]:
    """Genera un reporte textual estructurado de los enlaces auditados."""
    total = len(links)
    broken = [l for l in links if not l.is_valid]
    valid_count = total - len(broken)

    report_lines = [
        "==================================================================",
        "          INFORME DE SALUD Y MAPEO DOCUMENTAL (MAP-DOCS)          ",
        "==================================================================",
        f"Total de enlaces relativos auditados: {total}",
        f"Enlaces válidos: {valid_count}",
        f"Enlaces rotos detectados: {len(broken)}",
    ]

    if broken:
        report_lines.append("\n=== ENLACES ROTOS DETECTADOS ===")
        for b in broken:
            clean_path = str(b.source_file).replace("\\", "/")
            report_lines.append(f"  [BROKEN] {clean_path}:{b.line_no} -> '{b.target_path}' ({b.link_text})")
    else:
        report_lines.append("\n[PASS] Todos los enlaces relativos de la documentación son válidos.")

    report_lines.append("==================================================================")
    return len(broken), "\n".join(report_lines)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Parsea argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(description="Auditoría y validación de enlaces documentales relativos.")
    parser.add_argument("--doc-root", type=Path, default=Path("doc"), help="Directorio raíz de documentación a auditar.")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Punto de entrada principal."""
    args = parse_args(argv)
    links = validate_links(args.doc_root)
    broken_count, report_text = generate_report(links)
    print(report_text)
    return 1 if broken_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
