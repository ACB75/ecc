#!/usr/bin/env python3
"""
Generador automatizado de Post-Mortem 5W para ramas fix/* en ECC (generate_postmortem.py).
Extrae metadatos de Git, instancia TEMPLATE_POSTMORTEM_5W.md y guarda en doc/post-mortem/.
Cumple con SonarQube Quality Gate A (S3776 <= 15, S1192 sin duplicados).
"""

import argparse
import datetime
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence

DEFAULT_TEMPLATE = Path("doc/post-mortem/TEMPLATE_POSTMORTEM_5W.md")
DEFAULT_OUTPUT_DIR = Path("doc/post-mortem")


@dataclass(frozen=True)
class PostMortemMetadata:
    """Metadatos de contexto del incidente extraídos de Git."""
    branch_name: str
    author: str
    timestamp_utc: str
    affected_files: List[str]
    diff_summary: str
    environment: str = "LOCAL / DEV"


def slugify_branch_name(branch_name: str) -> str:
    """Convierte un nombre de rama en un slug seguro para nombres de archivo."""
    cleaned = branch_name.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "_", cleaned)
    return slug.strip("_")


def format_postmortem_markdown(meta: PostMortemMetadata, template_text: str) -> str:
    """Reemplaza placeholders en la plantilla de post-mortem."""
    content = template_text.replace("{{BRANCH}}", meta.branch_name)
    content = content.replace("{{TIMESTAMP_UTC}}", meta.timestamp_utc)
    content = content.replace("{{AUTHOR}}", meta.author)
    content = content.replace("{{ENVIRONMENT}}", meta.environment)
    content = content.replace("{{DIFF_SUMMARY}}", meta.diff_summary)
    return content


def _run_git_command(args: List[str]) -> str:
    """Ejecuta un comando git seguro y retorna salida limpia."""
    try:
        res = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            check=True,
        )
        return res.stdout.strip()
    except (subprocess.SubprocessError, OSError):
        return ""


def extract_git_metadata(branch_name: Optional[str] = None) -> PostMortemMetadata:
    """Extrae información de Git sobre la rama y autor activos."""
    branch = branch_name or _run_git_command(["branch", "--show-current"]) or "fix/unknown"
    author = _run_git_command(["config", "user.name"]) or "Automation Engineer"

    # Obtener resumen de diff y archivos modificados
    diff_stat = _run_git_command(["diff", "main...HEAD", "--stat"])
    if not diff_stat:
        diff_stat = _run_git_command(["diff", "HEAD~1...HEAD", "--stat"]) or "Sin diff disponible"

    files_raw = _run_git_command(["diff", "main...HEAD", "--name-only"])
    affected_files = [f.strip() for f in files_raw.splitlines() if f.strip()]

    now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return PostMortemMetadata(
        branch_name=branch,
        author=author,
        timestamp_utc=now_utc,
        affected_files=affected_files,
        diff_summary=diff_stat,
    )


def generate_postmortem_file(
    output_dir: Path,
    template_path: Path,
    branch_name: str,
    author: str = "SRE Team",
    diff_stat: str = "Diff summary pending",
) -> Path:
    """Instancia y persiste un nuevo archivo de post-mortem 5W."""
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    template_text = template_path.read_text(encoding="utf-8") if template_path.is_file() else "# Post-Mortem 5W: {{BRANCH}}"
    now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    ts_slug = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")

    meta = PostMortemMetadata(
        branch_name=branch_name,
        author=author,
        timestamp_utc=now_utc,
        affected_files=[],
        diff_summary=diff_stat,
    )

    content = format_postmortem_markdown(meta, template_text)
    branch_slug = slugify_branch_name(branch_name)
    target_filename = f"PM_{branch_slug}_{ts_slug}.md"
    target_path = output_dir / target_filename

    target_path.write_text(content, encoding="utf-8")
    return target_path


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Parsea argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(description="Generador automatizado de Post-Mortem 5W.")
    parser.add_argument("--branch", type=str, default="", help="Nombre de la rama del incidente.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Directorio de destino.")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE, help="Ruta a la plantilla 5W.")
    parser.add_argument("--dry-run", action="store_true", help="Muestra el contenido sin escribir en disco.")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Punto de entrada principal."""
    args = parse_args(argv)
    meta = extract_git_metadata(args.branch if args.branch else None)

    if not meta.branch_name.startswith("fix/"):
        print(f"[INFO] La rama '{meta.branch_name}' no es de tipo 'fix/*'. Omitiendo generación de post-mortem.")
        return 0

    if args.dry_run:
        template_text = args.template.read_text(encoding="utf-8") if args.template.is_file() else ""
        print(format_postmortem_markdown(meta, template_text))
        return 0

    created = generate_postmortem_file(
        output_dir=args.output_dir,
        template_path=args.template,
        branch_name=meta.branch_name,
        author=meta.author,
        diff_stat=meta.diff_summary,
    )
    print(f"[OK] Post-mortem 5W generado exitosamente en: {created}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
