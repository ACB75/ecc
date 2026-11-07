# Autopsia Post-Incidente (Post-Mortem 5W): {{BRANCH}}

> **Guía de Gobernanza SRE (ADR-0008):**
>
> - Esta autopsia es estrictamente **sin culpables (blameless)**. Su propósito es fortalecer los sistemas, guardrails y procesos defensivos de ingeniería.
> - Se genera automáticamente tras la resolución de ramas `fix/*`.

---

## 1. Metadatos del Incidente

- **Identificador de Rama / Incidente**: `{{BRANCH}}`
- **Fecha y Hora de Cierre (UTC)**: `{{TIMESTAMP_UTC}}`
- **Ingeniero Responsable / Autor**: `{{AUTHOR}}`
- **Entorno Afectado**: `{{ENVIRONMENT}}`
- **Severidad Preliminar**: `SEV-2 (Degradación Parcial)`
- **Impacto en Error Budget (SLO)**: `Agotamiento < 0.1% del presupuesto mensual`
- **Resumen de Cambios (Git Diff)**:
  `{{DIFF_SUMMARY}}`

---

## 2. Resumen Ejecutivo (Blameless Summary)

Breve resumen descriptivo del fallo observado, cómo fue detectado por las sondas o tests, y la estrategia aplicada para mitigar y solventar la anomalía.

---

## 3. Análisis Exhaustivo de las 5W

### 3.1. Who (Quién / Qué Componentes)

- **Microservicios afectados**: Componentes o módulos involucrados en la degradación.
- **Actores y dependencias**: Clientes, proxies Ingress, colas o bases de datos que interactuaron con el fallo.

### 3.2. What (Qué Ocurrió)

- **Síntomas observables**: Códigos de error HTTP 5xx, timeouts, memory leaks o excepciones no controladas.
- **Impacto**: Número de peticiones degradadas o impacto en la experiencia de usuario.

### 3.3. When (Cronología de Eventos UTC)

- `HH:MM:SS UTC` - **Detección**: Activación de alarma o fallo en tests de integración.
- `HH:MM:SS UTC` - **Diagnóstico**: Aislamiento del componente causante y reproducción del error.
- `HH:MM:SS UTC` - **Mitigación / Fix**: Commit correctivo en rama `fix/*` y validación de tests.
- `HH:MM:SS UTC` - **Resolución**: Fusión en `main` y verificación verde del Ingress.

### 3.4. Where (Dónde)

- **Localización técnica**: Módulos, controladores, endpoints o consultas SQL afectadas.
- **Entorno de ejecución**: Contenedores Docker, pods o servicios en red local `*.home.arpa`.

### 3.5. Why & How (Por Qué y Cómo)

- **Mecanismo de fallo**: Descripción técnica exacta de la condición de carrera, desbordamiento o excepción no capturada.
- **Propagación del blast radius**: Por qué el fallo no fue contenido por circuit breakers o bulkheads.

---

## 4. Análisis de Causa Raíz (5 Porqués / 5-Whys)

1. **¿Por qué falló el servicio?** ->
2. **¿Por qué ocurrió esa condición?** ->
3. **¿Por qué no se detectó en tests previos?** ->
4. **¿Por qué no existía un guardrail defensivo?** ->
5. **¿Por qué la arquitectura permitió la propagación?** -> *(Causa Raíz Fundamental)*

---

## 5. Acciones Preventivas y Correctivas

| Tipo | Acción Concreta | Responsable | Prioridad | Estado |
| :--- | :--- | :--- | :--- | :--- |
| **Mitigación** | Corrección aplicada en rama `{{BRANCH}}` | `{{AUTHOR}}` | P0 | Resuelto |
| **Prevención** | Test de regresión automatizado añadido | Equipo Dev | P1 | Planificado |
| **Monitoreo** | Ajuste de métricas SLI y alertas tempranas | Equipo SRE | P1 | Planificado |
