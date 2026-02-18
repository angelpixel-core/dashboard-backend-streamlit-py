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
