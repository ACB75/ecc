# Ecosistema ECC (`ecc`)

> **Distribución Maestra Multi-Harness: Claude Code + Google Antigravity & Gemini**  
> Repositorio Principal: [`ACB75/ecc`](https://github.com/ACB75/ecc)

---

## 1. Visión y Arquitectura

`ecc` es el repositorio raíz y núcleo de orquestación que unifica y desacopla las diferentes adaptaciones de **Everything Claude Code (ECC)** según el motor de IA y el contexto de despliegue:

```mermaid
flowchart TD
    subgraph Core["Ecosistema Maestro ecc"]
        Root["ecc (Orquestador y Repositorio Principal)"]
    end

    subgraph Flavors["Distribuciones Especializadas"]
        Claude["1. ecc-claude<br/>(Boilerplates Oficiales para Claude Code)"]
        AGY["2. ecc-agy<br/>(Distribución Unificada Google Antigravity & Gemini)"]
    end

    subgraph Targets["Entornos y Destinos de Uso"]
        TargetClaude["Anthropic Claude Code CLI<br/>(CLAUDE.md / .claude/)"]
        TargetCorp["Empresas, Startups y Clientes<br/>(Proyectos agnósticos / Barcelona / Monorepos)"]
        TargetHomeLab["Servidores FRACTAL & NEO<br/>(Home-Lab, cluster, whoiam, kakebo, portal)"]
    end

    Root --> Claude
    Root --> AGY

    Claude --> TargetClaude
    AGY --> TargetCorp
    AGY --> TargetHomeLab

    classDef core fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef flavor fill:#fff3e0,stroke:#f57c00,stroke-width:2px;
    classDef target fill:#e8f5e9,stroke:#388e3c,stroke-width:1px;

    class Root core;
    class Claude,AGY flavor;
    class TargetClaude,TargetCorp,TargetHomeLab target;
```

---

## 2. Catálogo de Distribuciones

| Distribución | Harness | Propósito | Estado de Acoplamiento |
| ------------ | ------- | --------- | ---------------------- |
| **[`ecc-claude`](ecc-claude/)** | Claude Code | Boilerplates nativos de Claude Code (`CLAUDE.md`, `.claude/`, hooks y comandos slash). | Totalmente agnóstico, estándar oficial de ECC. |
| **[`ecc-agy`](ecc-agy/)** | Google Antigravity | Distribución unificada para Antigravity & Gemini con 315+ skills, 73+ subagentes, comandos, esquemas y SRE baseline. | **Unificado y Modular**: Apto para $N$ proyectos, empresas externas y laboratorios con control estricto de gobernanza. |

---

## 3. Instalador Rápido (`install.ps1` / `install.sh`)

Instalación rápida mediante un único comando según el objetivo deseado:

```powershell
# 1. Para usar en un proyecto nuevo con Claude Code
pwsh -File install.ps1 -Target claude -Destination C:\Ruta\A\MiProyecto

# 2. Para desplegar el plugin unificado en Google Antigravity
pwsh -File install.ps1 -Target agy
```

---

## 4. Repositorios GitHub Asociados

- **Repositorio Principal**: [`https://github.com/ACB75/ecc`](https://github.com/ACB75/ecc)
