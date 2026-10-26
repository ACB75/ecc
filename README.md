# Ecosistema ECC (`ecc`)

> **Distribución Maestra Multi-Harness: Claude Code + Antigravity Agnóstico + Fork Home-Lab**  
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
        AGY["2. ecc-agy<br/>(Antigravity Agnóstico Reutilizable para N Proyectos)"]
        HomeLab["3. ecc-agy-homelab<br/>(Fork Especializado para Home-Lab Monorepo)"]
    end

    subgraph Targets["Entornos y Destinos de Uso"]
        TargetClaude["Anthropic Claude Code CLI<br/>(CLAUDE.md / .claude/)"]
        TargetCorp["Empresas, Startups y Clientes<br/>(Ej. Empresa en Barcelona)"]
        TargetHomeLab["Servidores FRACTAL & NEO<br/>(cluster, whoiam, kakebo, portal)"]
    end

    Root --> Claude
    Root --> AGY
    Root --> HomeLab

    Claude --> TargetClaude
    AGY --> TargetCorp
    HomeLab --> TargetHomeLab

    classDef core fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef flavor fill:#fff3e0,stroke:#f57c00,stroke-width:2px;
    classDef target fill:#e8f5e9,stroke:#388e3c,stroke-width:1px;

    class Root core;
    class Claude,AGY,HomeLab flavor;
    class TargetClaude,TargetCorp,TargetHomeLab target;
```

---

## 2. Catálogo de Distribuciones

| Distribución | Harness | Propósito | Estado de Acoplamiento |
| ------------ | ------- | --------- | ---------------------- |
| **[`ecc-claude`](ecc-claude/)** | Claude Code | Boilerplates nativos de Claude Code (`CLAUDE.md`, `.claude/`, hooks y comandos slash). | Totalmente agnóstico, estándar oficial de ECC. |
| **[`ecc-agy`](ecc-agy/)** | Google Antigravity | Distribución agnóstica para Antigravity con 16 skills, 12 subagentes y SRE baseline. | **100% Desacoplado**: Listo para $N$ proyectos o empresas externas sin fuga de datos. |
| **[`ecc-agy-homelab`](ecc-agy-homelab/)** | Google Antigravity | Fork especializado con gobernanza Home-Lab, `/portal`, cluster, kakebo, whoiam. | Especializado para infraestructura física del laboratorio ([ADR-0008](https://github.com/ACB75/home-lab/blob/main/doc/adr/0008-software-reliability-engineering-baseline.md)). |

---

## 3. Instalador Rápido (`install.ps1` / `install.sh`)

Instalación rápida mediante un único comando según el objetivo deseado:

```powershell
# 1. Para usar en un proyecto nuevo con Claude Code
pwsh -File install.ps1 -Target claude -Destination C:\Ruta\A\MiProyecto

# 2. Para usar en una empresa o proyecto genérico con Antigravity
pwsh -File install.ps1 -Target agy

# 3. Para trabajar en el ecosistema Home-Lab con Antigravity
pwsh -File install.ps1 -Target homelab
```

---

## 4. Repositorios GitHub Asociados

- **Repositorio Principal**: [`https://github.com/ACB75/ecc`](https://github.com/ACB75/ecc)
- **Fork Home-Lab**: [`https://github.com/ACB75/ecc-agy-homelab`](https://github.com/ACB75/ecc-agy-homelab)
