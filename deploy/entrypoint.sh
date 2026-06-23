#!/bin/sh

envsubst '$PORT' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

cd /app/backend
uv run alembic upgrade head 2>/dev/null || uv run python -m app.ensure_db || echo "WARNING: DB init failed — starting without database"
uv run python -m app.seed || echo "WARNING: seed failed — continuing"

uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 &

nginx -g 'daemon off;'
