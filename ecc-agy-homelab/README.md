# ECC-AGY-HOMELAB (`ecc-agy-homelab`)

> **Fork Especializado de ECC-AGY para el Ecosistema Home-Lab**  
> Repositorio Canónico: [`ACB75/ecc-agy-homelab`](https://github.com/ACB75/ecc-agy-homelab).  
> Parte del ecosistema multiproyecto [`ecc-aecb`](../README.md).

---

## 1. Visión General

`ecc-agy-homelab` es la distribución especializada y contextualizada para el monorepo y servidores físicos del entorno **Home-Lab**. A diferencia de `ecc-agy` (que es agnóstico), este fork incorpora el conocimiento concreto, reglas de gobernanza y dependencias operativas del ecosistema del laboratorio:

- **Ecosistema Multi-Servicio**: `cluster` (Traefik, PostgreSQL, Kafka KRaft, Apache Ignite, Emuladores Cloud), `whoiam` (IAM), `kakebo` (finanzas personales), `doc-viewer`, `token-hill`.
- **Topología Tri-Entorno**: Despliegue en servidores `FRACTAL` y `NEO` bajo entornos `LOCAL` (trunk HEAD), `SANDBOX` (tags `vX.Y.Z-sandbox`), y `LIVE` (tags semánticos inmutables `vX.Y.Z`).
- **Sincronización Obligatoria de `/portal`**: Verificación y regeneración del catálogo dinámico ante cambios en Docker o rutas Traefik.
- **Formato Estricto de Commits**: `[type]+[projects]: <title>` + cuerpo explicativo obligatorio.
- **SRE & Resiliencia Operativa**: Auditoría estática mediante `audit-sre.ps1` y [ADR-0008](../../doc/adr/0008-software-reliability-engineering-baseline.md).

---

## 2. Instalación

Para activar el perfil Home-Lab en Antigravity:

```powershell
pwsh -File ../install.ps1 -Target homelab
```
