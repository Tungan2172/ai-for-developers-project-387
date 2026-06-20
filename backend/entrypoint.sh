#!/bin/sh
set -e

uv run alembic upgrade head 2>/dev/null || uv run python -m app.ensure_db

uv run python -m app.seed

exec uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
