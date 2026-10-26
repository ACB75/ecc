# ECC-Claude (`ecc-claude`)

> **Distribución Oficial de Boilerplates de Everything Claude Code (ECC) para Claude Code**  
> Parte del ecosistema multiproyecto [`ecc-aecb`](../README.md).

---

## 1. Visión General

`ecc-claude` contiene los artefactos, plantillas de configuración y boilerplates extraídos directamente del repositorio canónico de **Everything Claude Code (ECC)** optimizados para su uso nativo con Anthropic Claude Code.

---

## 2. Artefactos Incluidos

- **`CLAUDE.md`**: El archivo maestro de instrucciones de contexto, defensa de prompts y estándares operativos para Claude Code.
- **`.claude/`**: Directorio de configuración nativo con:
  - `commands/`: Comandos slash (`/plan`, `/review`, `/test`, etc.).
  - `rules/`: Reglas de arquitectura, pruebas y calidad.
  - `enterprise/`, `identity.json`, `workflows/`: Configuraciones de equipo y flujo.
- **`.claude-plugin/`**: Manifiestos de marketplace y plugins para Claude Code.
- **`hooks/`**: Sistema de hooks de ciclo de vida (persistencia de memoria, pre/post ejecución).
- **`commands/`**: Catálogo de comandos slash ampliados.
- **`scaffolds/`**: Estructuras de inicio rápido para proyectos.

---

## 3. Modo de Uso

### Opción A: Copia Directa a tu Proyecto Claude Code

Copia los archivos a la raíz de cualquier repositorio donde utilices Claude Code:

```bash
cp CLAUDE.md /ruta/a/tu/proyecto/
cp -r .claude /ruta/a/tu/proyecto/
```

### Opción B: Instalación como Plugin de Claude Code

```bash
claude plugin install ./ecc-claude
```
