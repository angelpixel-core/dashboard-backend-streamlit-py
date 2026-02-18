# dashboard-backend-streamlit-py

Streamlit dashboard backend con arquitectura DDD + Hexagonal, listo como seed reutilizable.

![Dashboard Overview](docs/assets/dashboard/overview.png)

## Quickstart

```sh
uv sync --group dev
make run
make lint
make typecheck
make test
make check
make test-watch
```

## Virtual Environment & uv

No es necesario ejecutar manualmente:

```sh
source .venv/bin/activate
```

Comandos oficiales del proyecto:

```sh
make run
make lint
make typecheck
make test
make check
```

Todos esos targets usan `uv run` internamente.
`uv run <command>` ejecuta dentro del entorno virtual correcto sin modificar la
sesion actual del shell.

Activar el entorno manualmente es opcional y solo tiene sentido para trabajo
interactivo fuera de `make`, por ejemplo cuando quieras usar directamente
`python`, `pip` o una REPL.

Detalle tecnico:
- `source .venv/bin/activate` modifica la sesion actual del shell.
- Los comandos de `make` corren en subshells y no pueden activar el entorno del shell padre.
- Por eso este repo estandariza `uv run` como mecanismo de ejecucion.

## Architecture

- `src/dashboard/domain` y `src/dashboard/application` encapsulan reglas y casos de uso sin dependencia de Streamlit.
- Los puertos se definen con `Protocol` en `src/dashboard/application/ports` y se implementan con adaptadores en infraestructura/presentación.
- `src/dashboard/presentation/streamlit` es un adaptador de UI reemplazable, no parte del core de negocio.

## Quality Gates

- Gate atómico de lint: `make lint`
- Gate atómico de formato: `make format`
- Gate atómico de tipos: `make typecheck`
- Tests unitarios: `make test-unit`
- Tests de integración: `make test-integration`
- Tests end-to-end: `make test-e2e`
- Agregado local (unit + integration): `make test`
- Orquestador equivalente CI: `make check`
- CI (`.github/workflows/quality.yml`) ejecuta `make check` en push/PR.

Orden recomendado antes de pushear:

```sh
make format
make lint
make typecheck
make test
# o en una sola corrida equivalente CI
make check
```

### E2E snapshots y artifacts

- Snapshots versionables: `tests/e2e/snapshots/`
- Artifacts runtime no versionados (traces/videos/screenshots): `tests/artifacts/`
- `make test-e2e` crea ambos directorios antes de ejecutar y exporta:
  - `PLAYWRIGHT_SNAPSHOTS_DIR`
  - `PLAYWRIGHT_ARTIFACTS_DIR`
- Si aún no existen tests `e2e`, el target informa `No e2e tests collected` y finaliza en OK.

## Seed Baseline

Este repositorio mantiene un baseline estable etiquetado como `seed-v0.1.0`.
Ese tag marca una semilla reusable (seed) con DDD + Hexagonal + adaptador Streamlit + quality gates.

### Crear un proyecto nuevo desde el seed tag

```sh
git archive --format=tar --prefix=my-new-dashboard/ seed-v0.1.0 | tar -x
cd my-new-dashboard
git init
uv sync --group dev
make run
```

Opcional a futuro: crear un repositorio template dedicado. Método oficial actual: iniciar desde el tag seed.

## Screenshots

Vista general:

![Dashboard Hero](docs/assets/dashboard/overview.png)

Interacción (tooltip/hover):

![Dashboard Tooltip Interaction](docs/assets/dashboard/interaction-tooltip.png)

Captura adicional de referencia:

![Dashboard Home Reference](docs/assets/01-home.png)
