#!/usr/bin/env python3
"""
Catalog Token Optimizer: Condensation of skill and agent frontmatters.

Enforces:
  - Skill description <= 140 characters, preserving trigger keywords.
  - Agent description <= 120 characters.
  - Agent model in {flash, inherit}.
"""

import glob
import os
import re
from pathlib import Path
from typing import Dict, Tuple

DEEP_REASONING_AGENTS = {
    "architect.md", "planner.md", "code-architect.md", "homelab-architect.md",
    "network-architect.md", "spec-miner.md", "gan-planner.md",
}


def condense_agent_description(name: str, desc: str) -> str:
    clean = desc.strip().strip("\"'")
    if len(clean) <= 120:
        return clean

    # Heurísticas de condensación para agentes
    replacements = [
        ("Accessibility Architect specializing in WCAG 2.2 compliance audits, accessible design patterns, and cross-platform a11y engineering", "WCAG 2.2 accessibility architect for UI audits, accessible design patterns, and cross-platform a11y."),
        ("Evaluates agent output against 5-axis quality rubric (accuracy, completeness, clarity, actionability, conciseness) and assigns calibrated 1-5 scores with concrete evidence", "Evaluates agent outputs against 5-axis rubric with calibrated 1-5 scores and actionable evidence."),
        ("Reviews code handling Bengali (Bangla) text for Unicode correctness, NFC normalization, grapheme clusters, conjuncts, zero-width joiners, and Bangla NLP patterns", "Reviews Bengali/Bangla code for Unicode correctness, NFC normalization, conjuncts, and NLP patterns."),
        ("Personal communication chief of staff that triages email, Slack, calendar, and task streams into prioritized briefings and drafts high-context responses", "Triages email, chat, calendar, and tasks into prioritized briefings and drafts high-context replies."),
        ("Designs feature architectures by analyzing existing codebase patterns, data models, and integration points before implementation", "Designs feature architectures by analyzing codebase patterns, data models, and integration points."),
        ("Deeply analyzes existing codebase features by tracing execution paths, data flow, component interactions, and edge cases to inform changes", "Analyzes codebase features by tracing execution paths, data flows, and component interactions."),
        ("Simplifies and refines code for clarity, consistency, and maintainability without changing external behavior or breaking tests", "Refines code for clarity, consistency, and maintainability without breaking behavior or tests."),
        ("Reviews a staged diff and drafts a Conventional Commits-compliant commit message with imperative title and bulleted details", "Reviews staged diffs and drafts Conventional Commits messages with imperative title and details."),
        ("Use this agent when analyzing conversation transcripts to find root causes of agent failures, evaluate tool usage efficiency, identify prompt confusion, or audit multi-turn drift", "Analyzes agent transcripts to diagnose failures, audit tool usage, and identify prompt confusion."),
        ("C++ build, CMake, and compilation error resolution specialist. Fixes undefined references, template errors, and missing includes", "C++ & CMake build error resolver. Fixes undefined references, template errors, and missing includes."),
        ("Reviews C++ code for modern C++20/23 idioms, RAII, memory safety, value semantics, and adherence to C++ Core Guidelines", "Reviews C++ code for modern C++20/23 idioms, RAII, memory safety, and C++ Core Guidelines."),
        ("Reviews C# and .NET code for idiomatic patterns, async/await correctness, LINQ efficiency, nullable reference types, and clean architecture", "Reviews C#/.NET code for idiomatic patterns, async/await, LINQ, nullable types, and clean architecture."),
        ("Diagnoses and fixes Dart/Flutter build failures, analysis errors, dependency conflicts, Gradle/CocoaPods issues, and compilation errors", "Fixes Dart/Flutter build failures, analyzer issues, Gradle/CocoaPods and dependency conflicts."),
        ("Diagnoses and fixes Django compilation errors, migration conflicts, import errors, setting misconfigurations, and Celery worker issues", "Fixes Django build errors, migration conflicts, setting misconfigurations, and Celery issues."),
        ("Reviews Django code for ORM query efficiency (N+1 queries), security (CSRF, injection), REST framework patterns, model design, and clean separation of concerns", "Reviews Django code for ORM N+1 queries, security, REST framework patterns, and clean architecture."),
        ("Looks up Context7 documentation for libraries, frameworks, APIs, and tools. Consults official docs before implementation to ensure accurate API usage", "Looks up Context7 official documentation for APIs and frameworks to verify up-to-date usage."),
        ("Reviews Flutter code for widget performance, state management correctness (Bloc/Provider/Riverpod), architecture layers, and platform-specific platform channel handling", "Reviews Flutter code for widget performance, state management, architecture, and platform channels."),
        ("Reviews F# code for idiomatic functional patterns, type safety, immutability, pattern matching completeness, railway-oriented programming, and clean domain modeling", "Reviews F# code for functional patterns, immutability, exhaustive matching, and domain modeling."),
        ("Evaluates generated applications against the PRD quality bar, scores across 10 dimensions, and produces structured pass/fail reports with actionable feedback", "Evaluates generated apps against PRDs, scoring 10 dimensions with actionable pass/fail feedback."),
        ("Generates complete, production-grade applications by iteratively implementing features, fixing defects identified by the evaluator, and refining until the quality bar is met", "Iteratively generates production-grade apps, resolving evaluator findings to meet quality bars."),
        ("Decomposes PRDs into sequenced implementation plans for the generator agent, defining milestone criteria, edge cases, and architectural boundaries", "Decomposes PRDs into sequenced milestone plans, edge cases, and architectural boundaries."),
        ("Diagnoses and resolves HarmonyOS (ArkTS / ArkUI) build errors, hvigor build failures, Ohpm dependency conflicts, DevEco Studio issues, and compilation errors", "Resolves HarmonyOS (ArkTS/ArkUI) build errors, hvigor issues, and Ohpm dependency conflicts."),
        ("Audits and optimizes agent harnesses, action spaces, tool descriptions, context efficiency, and prompt caching to maximize task completion rates and minimize token costs", "Optimizes agent harnesses, action spaces, context efficiency, and token costs to maximize completion."),
        ("Reviews clinical decision support, EHR/EMR integrations, healthcare data pipelines, and HIPAA compliance for safety and standards adherence", "Reviews clinical CDSS, EHR/EMR integrations, health data pipelines, and HIPAA compliance."),
        ("Diagnoses and fixes Kotlin/JVM, Kotlin/Native, and Kotlin Multiplatform build errors, Gradle configuration issues, dependency resolution failures, and compilation errors", "Fixes Kotlin, KMP, and Gradle build errors, dependency failures, and compilation issues."),
        ("Reviews Kotlin code for idiomatic idioms, coroutine and Flow safety, null safety, Compose Multiplatform best practices, and clean architecture", "Reviews Kotlin code for idiomatic patterns, coroutines/Flow safety, Compose, and clean architecture."),
        ("Plans, creates, and executes multi-platform marketing campaigns including content creation, distribution strategy, and performance tracking", "Plans and executes multi-platform marketing campaigns, content distribution, and tracking."),
        ("Reviews ML/DL code, PyTorch pipelines, training loops, evaluation metrics, data preprocessing, model architectures, and training reproducibility", "Reviews ML/DL pipelines, PyTorch training loops, evaluation metrics, and reproducibility."),
        ("Fork, clone, or branch an open source repository, configure remotes, inspect upstream changes, and manage upstream sync for private/public workflows", "Forks/clones open source repos, configures remotes, and manages upstream synchronization workflows."),
        ("Package and publish open source releases: build artifacts, sign releases, generate checksums, create GitHub Releases with changelogs, and publish to registries", "Packages and publishes open source releases, changelogs, signatures, and registry artifacts."),
        ("Sanitize open source contributions and forks before publishing: strip secrets, proprietary configs, internal URLs, company names, and private Git history", "Sanitizes open source contributions before publishing: strips secrets, private URLs, and history."),
        ("Reviews PHP and Laravel code for PSR compliance, modern PHP 8.x features, Eloquent query efficiency (N+1), type safety, security (SQLi, XSS, CSRF), and clean architecture", "Reviews PHP/Laravel code for PSR compliance, PHP 8.x features, Eloquent queries, and security."),
        ("Analyzes CI test failures, classifies failure types (regression vs flaky), isolates root causes, and recommends minimal fixes", "Analyzes CI test failures, classifies flaky vs regression, isolates root cause, and recommends fixes."),
        ("Diagnoses and fixes PyTorch training/inference errors: CUDA OOM, tensor shape mismatches, dtype conflicts, distributed training (DDP) hangs, and device placement issues", "Fixes PyTorch CUDA OOM, tensor shape mismatches, DDP hangs, and device placement issues."),
        ("Reviews RAG pipelines for retrieval quality, chunking strategy, embedding model fit, vector DB queries, re-ranking effectiveness, context injection, and hallucination prevention", "Reviews RAG pipelines for retrieval quality, chunking, embeddings, re-ranking, and hallucination."),
        ("Diagnoses and fixes React/Next.js/Vite build errors, TypeScript errors, JSX/TSX syntax issues, SSR hydration mismatches, bundler configuration failures, and module resolution issues", "Fixes React/Next.js/Vite build errors, TypeScript issues, SSR hydration mismatches, and bundler bugs."),
        ("Reviews React/Next.js code for hooks rules, server/client boundary correctness, rendering performance, accessibility (ARIA), state management, and modern component patterns", "Reviews React/Next.js for hooks rules, RSC boundaries, render performance, a11y, and state."),
        ("Reviews Ruby and Rails code for idiomatic patterns, ActiveRecord efficiency (N+1 queries), security, testing practices, and clean architecture", "Reviews Ruby/Rails code for idiomatic patterns, ActiveRecord queries, security, and architecture."),
        ("Diagnoses and fixes Rust compilation errors, borrow checker conflicts, trait bound issues, lifetime mismatches, and Cargo dependency problems", "Fixes Rust compilation errors, borrow checker conflicts, lifetimes, and Cargo dependencies."),
        ("Reviews Rust code for idiomatic patterns, ownership and borrowing correctness, error handling, unsafe code justification, and performance", "Reviews Rust code for idiomatic patterns, borrow correctness, error handling, and performance."),
        ("Conducts technical SEO audits, optimizes meta tags, structured data (JSON-LD), sitemaps, robots.txt, canonicalization, Core Web Vitals, and content keyword targeting", "Conducts technical SEO audits, optimizes meta tags, schema JSON-LD, sitemaps, and Core Web Vitals."),
        ("Extracts, consolidates, and verifies formal specifications, contracts, protocols, invariants, and edge-case boundaries from scattered requirements, code, and documentation", "Extracts and verifies formal specifications, API contracts, protocols, and edge-case boundaries."),
        ("Diagnoses and fixes Swift, SwiftUI, and Xcode build errors, compiler errors, SPM/CocoaPods dependency conflicts, code signing issues, and platform SDK mismatches", "Fixes Swift/SwiftUI and Xcode build errors, SPM conflicts, code signing, and SDK mismatches."),
        ("Reviews Swift and SwiftUI code for modern Swift 6 concurrency, approachable concurrency, actor isolation, memory safety, SwiftUI view lifecycle, and clean architecture", "Reviews Swift/SwiftUI for Swift 6 concurrency, actor isolation, memory safety, and lifecycle."),
        ("Reviews Vue 3 and Nuxt code for Composition API best practices, reactivity pitfalls, script setup idioms, SSR hydration safety, component architecture, and performance", "Reviews Vue 3/Nuxt code for Composition API, reactivity, SSR hydration safety, and performance."),
    ]
    for old, new in replacements:
        if old in clean or clean in old:
            return new

    # Si no hubo match exacto, acortar inteligentemente
    if ". " in clean:
        first_sentence = clean.split(". ")[0].strip() + "."
        if len(first_sentence) <= 120:
            return first_sentence

    return clean[:117].rstrip() + "..."


PATTERNS_LITERAL = "patterns"


def condense_skill_description(name: str, desc: str) -> str:
    clean = desc.strip().strip("\"'")
    if len(clean) <= 140:
        return clean

    use_when_match = re.search(r"\b(Use when\b.+)$", clean, re.IGNORECASE)
    lead_part = clean[:use_when_match.start()].strip().rstrip(".:;,") if use_when_match else clean

    lead_part = lead_part.replace("Design, implement, and audit", "Audit and implement")
    lead_part = lead_part.replace("best practices and conventions", PATTERNS_LITERAL)
    lead_part = lead_part.replace("best practices", PATTERNS_LITERAL)
    lead_part = lead_part.replace("patterns and best practices", PATTERNS_LITERAL)
    lead_part = lead_part.replace("patterns including", "for")
    lead_part = lead_part.replace("guidance for", "for")
    lead_part = lead_part.replace("patterns for", "for")

    if use_when_match:
        use_when = use_when_match.group(1).strip()
        combined = f"{lead_part}. {use_when}"
        if len(combined) <= 140:
            return combined

        short_use = re.sub(r",?\s*(?:especially|specifically|rather than|and not|without).*", "", use_when)
        if not short_use.endswith("."):
            short_use += "."
        combined2 = f"{lead_part}. {short_use}"
        if len(combined2) <= 140:
            return combined2

        budget_for_lead = 140 - len(short_use) - 2
        if budget_for_lead > 30:
            short_lead = lead_part[:budget_for_lead].rstrip()
            return f"{short_lead}. {short_use}"

    if len(lead_part) <= 140:
        return lead_part if lead_part.endswith(".") else lead_part + "."

    return lead_part[:136].rsplit(" ", 1)[0].rstrip(".,;:") + "..."


def _update_agent_frontmatter(agent_name: str, fm: str) -> str:
    target_model = "inherit" if agent_name in DEEP_REASONING_AGENTS else "flash"
    model_match = re.search(r"^model:\s*(.+)$", fm, re.MULTILINE)
    if model_match:
        curr_model = model_match.group(1).strip().strip("\"'")
        if curr_model not in ("flash", "inherit"):
            fm = re.sub(r"^model:\s*.+$", f"model: {target_model}", fm, flags=re.MULTILINE)
    else:
        fm += f"\nmodel: {target_model}"

    desc_match = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
    if desc_match:
        curr_desc = desc_match.group(1).strip()
        new_desc = condense_agent_description(agent_name, curr_desc)
        if len(new_desc) > 120:
            new_desc = new_desc[:117].rsplit(" ", 1)[0] + "..."
        fm = re.sub(r"^description:\s*.+$", f'description: "{new_desc}"', fm, flags=re.MULTILINE)
    return fm


def optimize_agents(root_dir: Path) -> int:
    agents_pattern = str(root_dir / "agents" / "*.md")
    files = glob.glob(agents_pattern)
    modified = 0

    for fpath in files:
        if os.path.basename(fpath) == "README.md":
            continue
        p = Path(fpath)
        content = p.read_text(encoding="utf-8", errors="replace")
        fm_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not fm_match:
            continue

        orig_fm = fm_match.group(1)
        new_fm = _update_agent_frontmatter(p.name, orig_fm)

        if new_fm != orig_fm:
            new_content = content[:fm_match.start(1)] + new_fm + content[fm_match.end(1):]
            p.write_text(new_content, encoding="utf-8")
            modified += 1

    return modified


def optimize_skills(root_dir: Path) -> int:
    skills_pattern = str(root_dir / "skills" / "*" / "SKILL.md")
    files = glob.glob(skills_pattern)
    modified = 0

    for fpath in files:
        p = Path(fpath)
        content = p.read_text(encoding="utf-8", errors="replace")
        fm_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not fm_match:
            continue

        fm = fm_match.group(1)
        desc_match = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
        if not desc_match:
            continue

        curr_desc = desc_match.group(1).strip()
        skill_name = p.parent.name
        new_desc = condense_skill_description(skill_name, curr_desc)
        if len(new_desc) > 140:
            new_desc = new_desc[:136].rsplit(" ", 1)[0] + "..."

        if new_desc != curr_desc.strip("\"'"):
            new_fm = re.sub(r"^description:\s*.+$", f'description: "{new_desc}"', fm, flags=re.MULTILINE)
            new_content = content[:fm_match.start(1)] + new_fm + content[fm_match.end(1):]
            p.write_text(new_content, encoding="utf-8")
            modified += 1

    return modified


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent.parent
    print(f"Optimizing catalog in: {repo_root}")

    # Optimizar root
    m_agents = optimize_agents(repo_root)
    m_skills = optimize_skills(repo_root)
    print(f"Root: {m_agents} agents updated, {m_skills} skills updated.")

    # Optimizar ecc-agy si existe
    ecc_agy = repo_root / "ecc-agy"
    if ecc_agy.is_dir():
        m_agents_sub = optimize_agents(ecc_agy)
        m_skills_sub = optimize_skills(ecc_agy)
        print(f"ecc-agy: {m_agents_sub} agents updated, {m_skills_sub} skills updated.")


if __name__ == "__main__":
    main()
