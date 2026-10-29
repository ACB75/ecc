# Plan de Requisitos y Arquitectura: Flujo Recurrente de Sincronización, Limpieza y Alineación (`sync-clean-align`)

> **Cumplimiento de Regla Global ECC-AGY**: Planificación técnica y de arquitectura previa a la incorporación de la automatización recurrente solicitada por el usuario: *"Limpia todo lo muerto y obsoleto, actualiza la doc. Deja todo sincronizado y alineado"*.

---

## 1. Contexto y Metadatos de la Petición

- **Proyecto / Módulo**: `ecc-agy` (plugin global) / `scripts` (monorepo `home-lab`)
- **Tipo de Intervención**: Nueva Skill, Script de Automatización Parametrizado y Subagente de Mantenimiento
- **Fecha**: 2026-10-25
- **Objetivo Principal**: Estandarizar y automatizar el flujo recurrente de fin de ciclo o mantenimiento integral: purgar residuos muertos de Docker y del filesystem, actualizar la documentación viva (`STATUS.md`, `LOG.md`, `INDEX.md`), sincronizar el catálogo `/portal` sin drift y ejecutar la auditoría integral de 4 fases (`audit-workspace.ps1`).

---

## 2. Toma de Requisitos Detallada y Criterios de Aceptación

### 2.1. Requisitos Funcionales (`RF`)

- **`RF-01` (Purga de Componentes Muertos y Obsoletos)**:
  - Docker: Purgar de forma segura la caché de compilación (`docker builder prune -f`), imágenes sin uso/dangling y volúmenes locales huérfanos (`docker volume prune -f`), preservando estrictamente volúmenes activos con datos de producción (`cluster_postgres_data`).
  - Filesystem: Eliminar archivos de backup residuales (`.bak`, `.tmp`, `.old`, `*~`), cachés de ejecución (`__pycache__`, `.pytest_cache`) y directorios vacíos.
  - Código y Configuración: Identificar referencias obsoletas o renombradas tras migraciones de nomenclatura (ej. `cluster-lb` -> `cluster-service`, `kakebo-app` -> `kakebo-service`).
- **`RF-02` (Sincronización y Actualización Documental)**:
  - Actualizar el estado de salud de los proyectos y notas en `STATUS.md`.
  - Registrar la entrada cronológica correspondiente en `LOG.md`.
  - Asegurar que `INDEX.md` y `doc/scripts/README.md` indexan cualquier nuevo plan, script o manual generado.
  - Verificar la integridad de enlaces Markdown y la política de *Deletion Zone* mediante `audit-docs.py`.
- **`RF-03` (Alineación y Verificación Integral sin Drift)**:
  - Verificar alcanzabilidad y cero drift entre la infraestructura (Compose, Traefik, CoreDNS) y los endpoints del catálogo en `/portal` mediante `sync-portal.ps1 -Audit`.
  - Superar las 4 fases de `audit-workspace.ps1`: Higiene, Presupuesto de Tokens, Docs Governance y SonarQube Quality Gate Rating A (0 issues).
  - Ejecutar suites de pruebas unitarias y de enrutamiento (`go test`, `pytest`).
- **`RF-04` (Automatización Parametrizada — `sync-clean-align.ps1` y `.sh`)**:
  - Implementar el script idempotente en `scripts/bin/ecc-agy/sync-clean-align.ps1` (Windows 11) y `sync-clean-align.sh` (POSIX LF para Debian/WSL2) soportando flags:
    - `-CleanWorkspace`: Higiene de archivos temporales y cachés.
    - `-PruneDocker`: Limpieza de build cache y volúmenes dangling.
    - `-Audit`: Auditoría de portal y docs governance.
    - `-Verify`: Ejecución de tests críticos.
    - Por defecto (`-All`): Ejecuta el ciclo completo ordenado.
- **`RF-05` (Skill Lazy-Loaded `sync-clean-align`)**:
  - Crear `skills/sync-clean-align/SKILL.md` con descripción $\le 140$ caracteres y palabras clave de activación exactas (`"limpia todo lo muerto y obsoleto"`, `"actualiza la doc"`, `"deja todo sincronizado y alineado"`).
- **`RF-06` (Subagente `sync-aligner`)**:
  - Crear `agents/sync-aligner.md` con descripción $\le 120$ caracteres, modelo `flash` para exploración y ejecución, y contrato de salida estructurado.

### 2.2. Requisitos No Funcionales (`RNF`)

- **`RNF-01` (Eficiencia de Tokens)**:
  - Skill lazy-loaded (0 coste base en prompt).
  - Frontmatter de skill $\le 140$ caracteres y subagente $\le 120$ caracteres.
- **`RNF-02` (Cero Dependencias No Oficiales)**:
  - Python 3 estándar (`subprocess`, `argparse`, `pathlib`, `shutil`) y PowerShell nativo sin módulos externos.
- **`RNF-03` (Idempotencia y Robustez)**:
  - Ejecución repetible sin efectos secundarios adversos; manejo explícito de excepciones si Docker no está corriendo o si no hay elementos que purgar.

### 2.3. Criterios de Aceptación (`CA`)

- [ ] **`CA-01`**: El script `scripts/bin/ecc-agy/sync-clean-align.ps1` se ejecuta con código de salida `0` ejecutando las 4 fases de limpieza, sincronización y verificación.
- [ ] **`CA-02`**: La versión POSIX LF `scripts/bin/ecc-agy/sync-clean-align.sh` está creada y parametrizada con finales de línea `\n`.
- [ ] **`CA-03`**: La skill `skills/sync-clean-align/SKILL.md` está registrada con frontmatter $\le 140$ chars.
- [ ] **`CA-04`**: El subagente `agents/sync-aligner.md` está registrado con frontmatter $\le 120$ chars y modelo `flash`.
- [ ] **`CA-05`**: El diagrama de flujo Mermaid está persistido en `doc/ecc-agy/diagrama/sync_clean_align_flow.mmd`.
- [ ] **`CA-06`**: `audit-workspace.ps1` pasa las 4 fases con 0 incidencias.

---

## 3. Auditoría de Reutilización y Retrocompatibilidad

### 3.1. Inventario de Activos Existentes a Reutilizar

- `scripts/bin/ecc-agy/audit-workspace.ps1`: Reutilizado para las fases de higiene, tokens, gobernanza documental y SonarQube.
- `scripts/bin/cluster/sync-portal.ps1`: Reutilizado para la auditoría de endpoints y verificación de drift en `/portal`.
- `scripts/bin/ecc-agy/format-commit.ps1`: Reutilizado para la propuesta de commit final.

### 3.2. Impacto en Contratos y Retrocompatibilidad

- **Contratos Afectados**: Ninguno. La solución es aditiva y operacional.
- **Seguridad en Docker Volume Prune**: El flag solo elimina volúmenes que no están adjuntos a ningún contenedor activo. El volumen de base de datos `cluster_postgres_data` está permanentemente vinculado al contenedor `cluster-db` en ejecución, garantizando cero pérdida de datos.

---

## 4. Arquitectura y Flujo de Ejecución

```
+-------------------------------------------------------------------------+
|                  COMANDO: "Limpia, actualiza y sincroniza"              |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|               FASE 1: PURGA DE ELEMENTOS MUERTOS Y OBSOLETOS           |
|  - Docker: docker builder prune -f (reclamar build cache)               |
|  - Docker: docker volume prune -f (reclamar dangling volumes)           |
|  - Filesystem: purgar __pycache__, .pytest_cache, .bak, .tmp            |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|               FASE 2: SINCRONIZACIÓN DOCUMENTAL VIVA                    |
|  - Actualizar STATUS.md (estado de proyectos y notas de sesión)         |
|  - Registrar entrada cronológica en LOG.md                              |
|  - Indexar nuevos planes/scripts en INDEX.md y doc/scripts/README.md    |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|               FASE 3: ALINEACIÓN Y AUDITORÍA DE CALIDAD                 |
|  - sync-portal.ps1 -Audit (40/40 endpoints funcionales, 0 drift)       |
|  - audit-workspace.ps1 (Higiene, Tokens, Docs Governance, SonarQube)    |
|  - Suites de pruebas críticas (Go tests, cluster pytest)               |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|               FASE 4: PROPUESTA DE COMMIT ESTRUCTURADO                  |
|  - format-commit.ps1 -Type ... -Projects ... -Title ... -Body ...       |
|  - Presentación al usuario para confirmación explícita                  |
+-------------------------------------------------------------------------+
```

---

## 5. Análisis de Seguridad y Vectores de Ataque

1. **Destrucción Involuntaria de Datos**: El script nunca ejecuta `docker volume rm -f` indiscriminado ni borra carpetas fuera de patrones seguros conocidos (`__pycache__`, `.pytest_cache`).
2. **Elevación y Privilegios**: Los comandos de limpieza de Docker no requieren permisos de kernel adicionales más allá del acceso al daemon de Docker.
3. **Inyección de Comandos**: Parámetros tipados en PowerShell y argumentos en lista (`subprocess.run(["..."])`) sin `shell=True` en Python.

---

## 6. Análisis de Costes Visibles y Ocultos

- **Coste Visible**: ~15-20 segundos de tiempo de ejecución para el ciclo completo.
- **Coste Oculto**: Cero sobrecarga de tokens permanente gracias a la arquitectura lazy-loaded de la Skill (0 tokens base). Recuperación de ~20-25 GB de disco periódica.
