---
name: sre-reliability
description: Google SRE practices: SLI/SLO error budgets, blast radius control, circuit breakers, graceful degradation, and blameless audits.
---

# Software Reliability Engineering (SRE) & Operational Resilience

Operational baseline and engineering practices to enforce high reliability, fail-fast boundaries, and toil elimination across services.

## When to Activate

- Designing new microservices, background workers, or infrastructure topologies.
- Defining SLIs, SLOs, and Error Budget policies for critical user journeys.
- Reviewing distributed systems for cascading failure risks, unbounded retries, or missing timeouts.
- Implementing circuit breakers, bulkheads, rate limiters, or graceful shutdown hooks.
- Conducting Blameless Postmortems after incidents or Error Budget depletion.
- Auditing container resource boundaries (`GOMEMLIMIT`, memory/CPU limits, health probes).

## Core Principles

1. **Error Budget Governance**: $100\% - \text{SLO} = \text{Error Budget}$. If the budget is exhausted, freeze feature velocity and allocate 100% engineering effort to reliability.
2. **Blast Radius Minimization**: Every component must degrade gracefully. Isolate failure domains with circuit breakers, timeouts, and bulkheads.
3. **Toil Cap (<50%)**: Codify repetitive manual operations into idempotent automation scripts in `scripts/bin/<project>/`.
4. **4 Golden Signals**: Instrument all production paths for Latency (p95/p99), Traffic, Errors (5xx), and Saturation.
5. **Anti-Fragile Lifecycle**: Mandatory liveness/readiness health probes and graceful termination (`SIGTERM` draining).
6. **Blameless Culture**: Treat failures as systemic design flaws, not personal negligence. Conduct 5-Whys postmortems.

## The 4 Golden Signals Matrix

| Signal | Metric Target | Threshold Warning | Remediation Action |
| ------ | ------------- | ----------------- | ------------------ |
| **Latency** | Percentile p95, p99 | p95 > 200ms, p99 > 1s | Optimize DB queries, add cache fallback, check connection pool saturation. |
| **Traffic** | Requests Per Second (RPS) | Sudden spike > 3x mean | Apply Traefik rate limiting, enable concurrency shaping. |
| **Errors** | HTTP 5xx Ratio | Error rate > 0.1% | Open circuit breaker, fail fast to synthetic response or local cache. |
| **Saturation** | Memory / CPU / DB pool | Memory > 85%, Pool > 80% | Enforce `GOMEMLIMIT`, expand replica pool or shed load. |

## Resilience Patterns Checklist

### 1. Circuit Breakers & Deadlines

- Declare explicit timeouts on all outbound HTTP and database connections:
  - Internal RPC/HTTP: maximum 2.0s.
  - File/Batch operations: maximum 10.0s.
  - SQL execution: `statement_timeout = 5000` (5.0s).
- Trip circuit breaker after 5 consecutive failures in 10s.

### 2. Jittered Exponential Backoff

Never retry immediately. Calculate backoff delay with random jitter:

$$t_{\text{wait}} = \min(t_{\text{max}}, t_{\text{base}} \times 2^{\text{attempt}} \pm \text{jitter})$$

### 3. Graceful Shutdown Draining

- Trap `SIGTERM` and `SIGINT`.
- Stop receiving ingress traffic on HTTP listeners.
- Wait 15-30 seconds to drain active requests before process exit.

### 4. Container Resource Hardening

- Always declare `deploy.resources.limits.memory` in `docker-compose.yml`.
- For Go containers: set `GOMEMLIMIT=80%` of container memory limit.
- For Docker logging: configure `max-size: 10m` and `max-file: 3`.

## Automated SRE Audit

Run the automated static reliability audit:

```powershell
pwsh -File scripts/bin/ecc-agy/audit-sre.ps1 -Root C:\Workspace\projects\home-lab
```

Linux / WSL:

```bash
bash scripts/bin/ecc-agy/audit-sre.sh
```
