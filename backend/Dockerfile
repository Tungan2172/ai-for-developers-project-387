# Образ собирается через uv для воспроизводимых зависимостей.
FROM python:3.12-slim AS base

# Копируем готовый бинарь uv из официального образа — без curl-инсталляторов в слое.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Сначала только манифесты — слой зависимостей кэшируется отдельно от кода.
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-dev --no-install-project

COPY . .
RUN uv sync --no-dev

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
