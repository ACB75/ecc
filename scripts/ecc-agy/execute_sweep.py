#!/usr/bin/env python3
"""
Módulo de barrido y optimización de skills y agentes de ECC-AGY.
Elimina skills y agentes que no corresponden al workspace y normaliza frontmatters.
Cumple con SonarQube Quality Gate A (S3776 <= 15, S1192 sin duplicados).
"""

import os
import shutil
from typing import Tuple, List

DIR_SKILLS = "skills"
DIR_AGENTS = "agents"

# Catálogo consolidado de skills excluidas (bloat / no-alineadas)
DELETION_SET = {
    # Non-technical, Business, Marketing, Corporate, Logistics, Legal (31)
    "article-writing", "brand-discovery", "brand-voice",
    "carrier-relationship-management", "competitive-platform-analysis",
    "competitive-report-structure", "content-engine",
    "counterparty-channel-discipline", "crosspost", "customer-billing-ops",
    "customs-trade-compliance", "energy-procurement", "esign-field-placement",
    "finance-billing-ops", "inventory-demand-planning", "investor-materials",
    "investor-outreach", "lead-intelligence", "logistics-exception-management",
    "market-research", "marketing-campaign", "master-agreement-generator",
    "product-capability", "product-lens", "production-scheduling",
    "quality-nonconformance", "returns-reverse-logistics", "seo",
    "social-graph-ranker", "social-publisher", "visa-doc-translate",

    # Healthcare & Life Sciences (10)
    "healthcare-cdss-patterns", "healthcare-emr-patterns",
    "healthcare-eval-harness", "healthcare-phi-compliance", "hipaa-compliance",
    "scientific-db-pubmed-database", "scientific-db-uspto-database",
    "scientific-pkg-gget", "scientific-thinking-literature-review",
    "scientific-thinking-scholar-evaluation",

    # Crypto, DeFi & Web3 (7)
    "agent-payment-x402", "defi-amm-security", "evm-token-decimals",
    "llm-trading-agent-security", "nodejs-keccak256",
    "prediction-market-oracle-research", "prediction-market-risk-review",

    # Media, Video, 3D Graphics & Creative (14)
    "blender-motion-state-inspection", "fal-ai-media", "frontend-slides",
    "ios-icon-gen", "liquid-glass-design", "manim-video",
    "remotion-video-creation", "taste", "taste-application",
    "taste-distillation", "tasteforge-video", "ui-demo", "video-editing",
    "videodb",

    # Obscure Hacks / Non-Claude Harnesses (26)
    "bengali-nlp", "ck", "deepseek-harness-setup", "dmux-workflows",
    "flox-environments", "gan-style-harness", "hermes-imports",
    "ito-baskets", "ito-compute", "ito-inference", "ito-training",
    "jira-integration", "mailtrap-email-integration", "nanoclaw-repl",
    "nasiko-control-plane", "nutrient-document-processing",
    "openclaw-persona-forge", "osint-investigation", "plankton-code-quality",
    "project-flow-ops", "ralphinho-rfc-pipeline", "santa-method",
    "security-bounty-hunter", "skill-stocktake", "uncloud",
    "windows-desktop-e2e", "x-api",

    # Alien Language/Framework Stacks (62)
    "laravel-patterns", "laravel-plugin-discovery", "laravel-security",
    "laravel-tdd", "laravel-verification", "rails-patterns", "perl-patterns",
    "perl-security", "perl-testing", "dotnet-patterns", "csharp-testing",
    "fsharp-testing", "django-celery", "django-patterns", "django-security",
    "django-tdd", "django-verification", "quarkus-patterns", "quarkus-security",
    "quarkus-tdd", "quarkus-verification", "swift-actor-persistence",
    "swift-concurrency-6-2", "swift-protocol-di-testing", "swiftui-patterns",
    "dart-flutter-patterns", "flutter-dart-code-review",
    "android-clean-architecture", "compose-multiplatform-patterns",
    "cpp-coding-standards", "cpp-testing", "cisco-ios-patterns",
    "netmiko-ssh-automation", "react-patterns", "react-native-patterns",
    "react-performance", "react-testing", "nextjs-turbopack", "vue-patterns",
    "ui-to-vue", "nuxt4-patterns", "motion-advanced", "motion-foundations",
    "motion-patterns", "kotlin-patterns", "kotlin-coroutines-flows",
    "kotlin-exposed-patterns", "kotlin-ktor-patterns", "kotlin-testing",
    "rust-patterns", "rust-testing", "clickhouse-io", "mybatis-patterns",
    "mysql-patterns", "prisma-patterns", "tinystruct-patterns",
    "nestjs-patterns", "bun-runtime",
}

ALIEN_AGENTS = [
    "bengali-reviewer.md", "cpp-build-resolver.md", "cpp-reviewer.md",
    "csharp-reviewer.md", "dart-build-resolver.md", "django-build-resolver.md",
    "django-reviewer.md", "flutter-reviewer.md", "fsharp-reviewer.md",
    "gan-evaluator.md", "gan-generator.md", "gan-planner.md",
    "harmonyos-app-resolver.md", "kotlin-build-resolver.md",
    "kotlin-reviewer.md", "loop-operator.md", "marketing-agent.md",
    "php-reviewer.md", "react-build-resolver.md", "react-reviewer.md",
    "ruby-reviewer.md", "rust-build-resolver.md", "rust-reviewer.md",
    "seo-specialist.md", "swift-build-resolver.md", "swift-reviewer.md",
    "vue-reviewer.md",
]


def purge_skills(root_dir: str) -> int:
    """Elimina directorios de skills ajenas."""
    skills_dir = os.path.join(root_dir, DIR_SKILLS)
    if not os.path.exists(skills_dir):
        return 0
    count = 0
    for name in DELETION_SET:
        p = os.path.join(skills_dir, name)
        if os.path.exists(p):
            shutil.rmtree(p)
            count += 1
    return count


def purge_agents(root_dir: str) -> int:
    """Elimina archivos markdown de agentes ajenos."""
    agents_dir = os.path.join(root_dir, DIR_AGENTS)
    if not os.path.exists(agents_dir):
        return 0
    count = 0
    for name in ALIEN_AGENTS:
        p = os.path.join(agents_dir, name)
        if os.path.exists(p):
            os.remove(p)
            count += 1
    return count


def _parse_frontmatter_lines(lines: List[str], skill_name: str) -> Tuple[List[str], str]:
    """Extrae y normaliza líneas del frontmatter para reducir complejidad."""
    new_lines = []
    desc = ""
    for line in lines:
        if line.startswith("name:"):
            val = line.split("name:", 1)[1].strip()
            new_lines.append(f"name: {val}")
        elif line.startswith("description:"):
            desc = line.split("description:", 1)[1].strip().strip('"').strip("'")
        elif not line.startswith("description"):
            new_lines.append(line)
    if len(desc) > 140:
        desc = desc[:137] + "..."
    if not desc:
        desc = f"Expert workflows and standards for {skill_name}."
    new_lines.insert(1, f'description: "{desc}"')
    return new_lines, desc


def _optimize_single_skill_file(skill_file: str, skill_name: str) -> bool:
    """Normaliza el archivo SKILL.md de una skill individual."""
    with open(skill_file, "r", encoding="utf-8") as fp:
        content = fp.read()
    if not content.startswith("---"):
        return False
    parts = content.split("---", 2)
    if len(parts) < 3:
        return False

    raw_lines = parts[1].strip().splitlines()
    new_lines, _ = _parse_frontmatter_lines(raw_lines, skill_name)
    new_frontmatter = "\n".join(new_lines)
    new_content = f"---\n{new_frontmatter}\n---{parts[2]}"

    if new_content != content:
        with open(skill_file, "w", encoding="utf-8") as fp:
            fp.write(new_content)
        return True
    return False


def optimize_skills(root_dir: str) -> int:
    """Recorre y optimiza todas las skills activas."""
    skills_dir = os.path.join(root_dir, DIR_SKILLS)
    if not os.path.exists(skills_dir):
        return 0
    count = 0
    for s in os.listdir(skills_dir):
        skill_file = os.path.join(skills_dir, s, "SKILL.md")
        if os.path.exists(skill_file) and _optimize_single_skill_file(skill_file, s):
            count += 1
    return count


def run_sweep() -> Tuple[int, int]:
    """Ejecuta el barrido y retorna total de skills y agentes resultantes."""
    purge_skills(".")
    purge_agents(".")
    optimize_skills(".")

    total_skills = len([d for d in os.listdir(DIR_SKILLS) if os.path.isdir(os.path.join(DIR_SKILLS, d))])
    total_agents = len([f for f in os.listdir(DIR_AGENTS) if f.endswith(".md")])
    return total_skills, total_agents


if __name__ == "__main__":
    skills_cnt, agents_cnt = run_sweep()
    print(f"Barrido completado exitosamente: {skills_cnt} skills y {agents_cnt} agentes activos.")
