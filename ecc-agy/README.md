# ECC-AGY (`ecc-agy`)

> **Distribución Unificada de ECC para Google Antigravity & Gemini Workflows**  
> Parte del ecosistema multi-harness [`ecc`](../README.md).

---

## 1. Visión General

`ecc-agy` es la distribución especializada de **Everything Claude Code (ECC)** adaptada para **Google Antigravity** y **Gemini Code Assist**, integrando:

- **Catálogo Completo**: 315+ skills y 73+ subagentes optimizados para la API y SDK de Antigravity.
- **SRE & Resiliencia Operativa (ADR-0008)**: Auditoría estática de confiabilidad, gestión de presupuestos de error, aislamiento antifrágil y erradicación de toil.
- **Calidad de Código y Markdownlint**: Quality Gate SonarQube Rating A y cumplimiento estricto de sintaxis DavidAnson (`.markdownlint.json`).
- **Gobernanza Git Trunk-Based**: Validación de commits `[type]-[projects]: <title>`, ramas efímeras y apertura automática de Pull Requests.

---

## 2. Instalación

Para activar o sincronizar este perfil en Antigravity:

```powershell
# En Windows 11
pwsh -File ./install.ps1 -Target agy

# O desde la raíz del ecosistema
pwsh -File ../install.ps1 -Target agy
```
