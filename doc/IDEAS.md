# Catálogo de Propuestas e Ideas de Ingeniería (`IDEAS.md`)

> **Protocolo de Ingesta:**
>
> 1. Añade propuestas con el formato estructurado a continuación.
> 2. Cuando una propuesta sea aprobada para desarrollo, cambia su estado a `- Status: Approved`.
> 3. Ejecuta `pwsh -File scripts/bin/ecc-agy/sync-ideas-todo.ps1` para transformarla mediante la metodología de 7 fases e inyectarla en `doc/TODO.md`.

---

## Plantilla de Propuesta

```markdown
## Idea N: Nombre Conciso de la Propuesta
- Status: Draft | Approved
- Sector: <Dominio / Stack>
- DataType: <Formatos de datos / Artefactos>
- Objective: <Objetivo medible>
- Description: <Detalle del problema y solución planteada>
```

---

## 1. Propuestas en Evaluación

## Idea 1: Telemetría OTLP Nativa de Bajo Consumo para Ingress Traefik

- Status: Draft
- Sector: Observability & SRE
- DataType: OpenTelemetry Metrics & JSON Logs
- Objective: Integrar exportación OTLP nativa con consumo de memoria menor a 50MB
- Description: Conectar métricas de Traefik v3 directamente con el recolector liviano del cluster.
