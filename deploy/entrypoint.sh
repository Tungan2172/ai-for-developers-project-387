#!/bin/sh
set -e

envsubst '$PORT' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

cd /app/backend
uv run alembic upgrade head 2>/dev/null || uv run python -m app.ensure_db
uv run python -m app.seed

uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 &

nginx -g 'daemon off;'
