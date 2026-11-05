default:
    @just --list

check:
    uv run ruff check .
    uv run ruff format --check .

fix:
    uv run ruff check --fix .
    uv run ruff format .

test:
    uv run pytest
