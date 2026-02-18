E2E_ARTIFACTS_DIR ?= tests/artifacts
E2E_SNAPSHOTS_DIR ?= tests/e2e/snapshots

.PHONY: run lint format typecheck test-unit test-integration test-e2e test test-watch check ensure-e2e-dirs

run:
	uv run streamlit run app.py

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run mypy src

test-unit:
	uv run pytest -m unit

test-integration:
	uv run pytest -m integration

ensure-e2e-dirs:
	mkdir -p "$(E2E_ARTIFACTS_DIR)" "$(E2E_SNAPSHOTS_DIR)"

test-e2e: ensure-e2e-dirs
	@set -eu; \
	PLAYWRIGHT_ARTIFACTS_DIR="$(E2E_ARTIFACTS_DIR)" \
	PLAYWRIGHT_SNAPSHOTS_DIR="$(E2E_SNAPSHOTS_DIR)" \
	uv run pytest -m e2e || rc=$$?; \
	if [ "$${rc:-0}" -eq 5 ]; then \
		echo "No e2e tests collected (marker: e2e)."; \
		exit 0; \
	fi; \
	exit "$${rc:-0}"

test: test-unit test-integration

test-watch:
	uv run ptw -- -q

check: lint typecheck test
