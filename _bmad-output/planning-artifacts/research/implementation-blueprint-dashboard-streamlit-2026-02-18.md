# Execution Blueprint

## Scope

Blueprint ejecutable para `dashboard-backend-streamlit-py` con arquitectura
hexagonal, DDD pragmático y Streamlit como adaptador de presentación.

## Fase 1: Estructura base del proyecto

### Estructura final de carpetas

```txt
.
├── app.py
├── Makefile
├── pyproject.toml
├── src/
│   └── dashboard/
│       ├── __init__.py
│       ├── domain/
│       │   ├── __init__.py
│       │   ├── sales/
│       │   │   ├── __init__.py
│       │   │   ├── entities.py
│       │   │   ├── value_objects.py
│       │   │   ├── services.py
│       │   │   └── events.py
│       ├── application/
│       │   ├── __init__.py
│       │   ├── dto/
│       │   │   ├── __init__.py
│       │   │   └── sales_dto.py
│       │   ├── ports/
│       │   │   ├── __init__.py
│       │   │   ├── inbounds.py
│       │   │   └── outbounds.py
│       │   └── use_cases/
│       │       ├── __init__.py
│       │       └── build_sales_dashboard.py
│       ├── infrastructure/
│       │   ├── __init__.py
│       │   ├── persistence/
│       │   │   ├── __init__.py
│       │   │   ├── in_memory_sales_repo.py
│       │   │   └── sqlalchemy_sales_repo.py
│       │   └── providers/
│       │       ├── __init__.py
│       │       └── clock_provider.py
│       └── presentation/
│           ├── __init__.py
│           └── streamlit/
│               ├── __init__.py
│               ├── app.py
│               ├── state.py
│               ├── pages/
│               │   ├── __init__.py
│               │   └── sales_page.py
│               └── components/
│                   ├── __init__.py
│                   └── chart_card.py
├── tests/
│   ├── unit/
│   │   ├── domain/
│   │   └── application/
│   ├── integration/
│   │   ├── infrastructure/
│   │   └── presentation/
│   └── fixtures/
│       ├── __init__.py
│       └── sales_data.py
└── docs/
    └── adr/
        └── 0001-streamlit-adapter-hexagonal-protocol.md
```

### Regla de boundary (obligatoria)

- `domain` no importa `streamlit`, `pandas`, ni infraestructura.
- `application` depende de puertos (`Protocol`), no de implementaciones.
- `presentation/streamlit` invoca casos de uso de `application`.
- `infrastructure` implementa puertos de `application`.

## Fase 2: `pyproject.toml` definitivo

```toml
[build-system]
requires = ["hatchling>=1.27.0"]
build-backend = "hatchling.build"

[project]
name = "dashboard-backend-streamlit-py"
version = "0.1.0"
description = "Streamlit dashboard backend for Angel DevStack"
readme = "README.md"
requires-python = ">=3.14"
dependencies = [
  "streamlit>=1.54.0",
  "pandas>=2.3.3",
  "plotly>=6.5.2",
]

[dependency-groups]
dev = [
  "ruff>=0.11.0",
  "mypy>=1.15.0",
  "pytest>=8.3.0",
  "pytest-cov>=6.0.0",
  "pytest-watch>=4.2.0",
]

[tool.hatch.build.targets.wheel]
packages = ["src/dashboard"]

[tool.ruff]
line-length = 80
target-version = "py314"
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "N", "ANN", "PT"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "lf"

[tool.mypy]
python_version = "3.14"
strict = true
mypy_path = "src"
packages = ["dashboard"]
warn_unused_configs = true

[tool.pytest.ini_options]
addopts = "-q --maxfail=1 --cov=src/dashboard --cov-report=term-missing"
testpaths = ["tests"]
pythonpath = ["src"]

[tool.coverage.run]
source = ["src/dashboard"]
branch = true

[tool.coverage.report]
show_missing = true
skip_covered = true
```

## Fase 3: Tooling mínimo viable

### Dependencias y entorno

1. `uv sync --group dev`
2. `uv run ruff check .`
3. `uv run ruff format .`
4. `uv run mypy src`
5. `uv run pytest`
6. `uv run ptw -- -q`

### Makefile mínimo

```make
run:
	uv run streamlit run app.py

lint:
	uv run ruff check .
	uv run mypy src

format:
	uv run ruff format .

test:
	uv run pytest

test-watch:
	uv run ptw -- -q
```

## Fase 4: Checklist de implementación por commit

1. `chore(structure): create src layout for hexagonal architecture`
: Crear estructura `src/dashboard/*`, `tests/*`, `docs/adr/*`.
2. `build(pyproject): define build backend and dev tooling`
: Migrar `pyproject.toml` a versión definitiva + groups dev.
3. `chore(make): add run/lint/format/test/test-watch targets`
: Alinear `Makefile` con comandos `uv`.
4. `feat(domain): add first sales aggregate and value objects`
: Entidades y reglas de negocio sin dependencias externas.
5. `feat(app): add use case and protocol-based ports`
: Caso de uso + puertos inbound/outbound con `Protocol`.
6. `feat(infra): add in-memory and sql adapters`
: Adaptadores de persistencia que implementan puertos.
7. `feat(presentation): connect streamlit adapter to use case`
: `presentation/streamlit` invoca capa aplicación.
8. `test(unit): add domain and application tests`
: Cobertura de reglas y casos de uso.
9. `test(integration): add adapter and streamlit interaction tests`
: Validar wiring entre capas.
10. `docs(adr): add ADR-0001 for architectural decisions`
: Formalizar decisiones y trade-offs.
11. `ci(quality): enforce lint type test gates`
: Pipeline PR con gates obligatorios.

## Fase 5: Definition of Done (DoD)

1. Arquitectura
- No hay imports de `streamlit` fuera de `presentation/streamlit`.
- No hay imports de `infrastructure` dentro de `domain`.
- Todos los puertos están definidos con `Protocol`.

2. Calidad
- `uv run ruff check .` pasa sin errores.
- `uv run mypy src` pasa en modo `strict`.
- `uv run pytest` pasa completo.

3. Testing
- Cobertura dominio >= 90%.
- Cobertura aplicación >= 85%.
- Tests de integración para al menos 1 adaptador de persistencia.

4. Operación
- `make run` levanta app local sin errores.
- `make test-watch` reacciona a cambios.
- Configuración y comandos documentados en `README.md`.

5. Gobierno técnico
- ADR publicado y revisado.
- Pipeline CI con gates de lint, type y test.
- Commits atómicos y trazables por fase.

## Secuencia de ejecución sugerida

1. Ejecutar Fase 1 + Fase 2 en una rama corta de bootstrap.
2. Cerrar Fase 3 para tener feedback loop temprano.
3. Implementar Fase 4 con PR por bloque funcional.
4. Validar DoD al cierre de cada PR, no solo al final.
