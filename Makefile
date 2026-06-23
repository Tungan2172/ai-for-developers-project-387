# uv устанавливается в ~/.local/bin — добавляем в PATH, чтобы таргеты работали
# в свежей оболочке без ручной настройки.
export PATH := $(HOME)/.local/bin:$(PATH)

.DEFAULT_GOAL := help

.PHONY: help install api codegen mock run deploy stop clean build \
        test test-backend test-frontend lint lint-backend lint-frontend \
        fmt migrate seed smoke

help: ## Показать список команд
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  %-16s %s\n", $$1, $$2}'

install: ## Установить зависимости (api, backend, frontend)
	cd api && npm install
	cd backend && uv sync
	cd frontend && npm install

api: ## Сгенерировать openapi.yaml из TypeSpec (источник правды)
	cd api && npx tsp compile .

codegen: api ## Сгенерировать TS-типы фронта из контракта
	cd frontend && npm run codegen

mock: api ## Поднять Prism mock-сервер из контракта (порт 8000, как у backend)
	cd api && npx prism mock dist/openapi.yaml --port 8000

run: ## Поднять всё локально через docker compose
	docker compose up --build -d

deploy: ## Полный локальный деплой: контракт → образы → БД → сид
	$(MAKE) build
	docker compose up -d
	@echo "Waiting for backend..."
	@for i in $$(seq 1 30); do \
		if curl -sf http://localhost:8000/health > /dev/null 2>&1; then \
			echo "Backend ready"; \
			break; \
		fi; \
		sleep 1; \
	done
	$(MAKE) smoke

stop: ## Остановить контейнеры
	docker compose down

clean: ## Остановить, удалить тома и артефакты сборки
	docker compose down -v
	rm -rf api/dist frontend/dist

build: ## Собрать контракт, TS-типы и docker-образы
	$(MAKE) api
	$(MAKE) codegen
	docker compose build

test: test-backend test-frontend ## Прогнать все тесты

test-backend: ## Тесты бэкенда (pytest, в т.ч. интеграционные с testcontainers)
	cd backend && uv run pytest

test-frontend: ## Тесты фронтенда (vitest)
	cd frontend && npm test

lint: lint-backend lint-frontend ## Линтеры и тайп-чек обеих сторон

lint-backend: ## ruff + mypy
	cd backend && uv run ruff check . && uv run ruff format --check . && uv run mypy

lint-frontend: ## eslint + prettier + tsc
	cd frontend && npm run lint && npm run format:check && npm run typecheck

fmt: ## Автоформат бэка и фронта
	cd backend && uv run ruff format . && uv run ruff check --fix .
	cd frontend && npm run format

migrate: ## Применить миграции БД (Alembic) — добавляется на этапе B1
	cd backend && uv run alembic upgrade head

seed: ## Засидировать профиль владельца — добавляется на этапе B1
	cd backend && uv run python -m app.seed

smoke: ## Сквозной smoke-тест — проверить, что всё работает
	@echo "Health..."
	curl -sf http://localhost:8000/health > /dev/null && echo "  OK"
	@echo "Owner..."
	curl -sf http://localhost:8000/owner > /dev/null && echo "  OK"
	@echo "Event types list..."
	curl -sf http://localhost:8000/event-types > /dev/null && echo "  OK"
	@echo "Frontend..."
	curl -sf http://localhost:8080/ > /dev/null && echo "  OK"
	@echo "All smoke checks passed"
