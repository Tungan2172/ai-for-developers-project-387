#!/bin/sh

uv run alembic upgrade head 2>/dev/null || uv run python -m app.ensure_db || echo "WARNING: DB init failed — starting without database"

uv run python -m app.seed || echo "WARNING: seed failed — continuing"

exec uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
