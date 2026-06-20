# AGENTS.md

Контекст проекта для ИИ-агента между сессиями. Держать в актуальном состоянии.

## Назначение

Учебное веб-приложение «календарь бронирования» (упрощённый Cal.com, без
авторизации). Владелец публикует типы событий; гость выбирает свободный слот и
создаёт бронь. Подход — Design-First: контракт API на TypeSpec является
единственным источником правды.

## Стек и структура

```
api/        TypeSpec-контракт -> OpenAPI (источник правды)
backend/    FastAPI + SQLAlchemy + Alembic (Postgres)
frontend/   React + TypeScript (Vite)
docker-compose.yml, Makefile   — в корне
```

- **api/**: `main.tsp`, `models.tsp`, `routes.tsp`. Компиляция: `make api`
  (генерирует `api/dist/openapi.yaml`). Файл `openapi.yaml` НЕ коммитится.
- **backend/**: `uv` + `ruff` + `mypy --strict` + `pytest`. Слои (вводятся с B1):
  `app/domain/` (доменное ядро), `app/adapters/` (репозитории SQLAlchemy),
  `app/api/` (роутеры + Pydantic-DTO), `app/config.py` (pydantic-settings).
- **frontend/**: Vite + TS strict + ESLint/Prettier + Vitest + RTL +
  `openapi-typescript` (типы из контракта) + `openapi-fetch` + TanStack Query.
  UI — **Mantine** (`@mantine/core/hooks/dates`), роутинг — **React Router**,
  даты — **dayjs** (плагины utc/timezone, зона `Europe/Moscow`).
  Тесты HTTP — **MSW** (фейковый сервер; фикстуры состояний free/busy/пусто/ошибка).

### Frontend <-> API

В коде путь всегда `/api`. В dev — прокси Vite (`vite.config.ts`) срезает `/api`
и шлёт на `http://localhost:8000`. В prod — nginx (`frontend/nginx.conf`) отдаёт
статику и проксирует `/api/` на `backend:8000`. Один origin, без CORS.

## Доменные правила

- Время в TZ владельца **Europe/Moscow (+03:00)**, в API — `date-time`.
- Слоты: **пн–пт 09:00–17:00**, окно **14 дней** от 00:00 текущей даты.
- Шаг сетки слотов = `durationMinutes` типа события (произвольная, **1..480**,
  НЕ кратна 30). Последний слот заканчивается ≤ 17:00.
- `Slot.status`: `free | busy`. `GET /event-types/{id}/slots` отдаёт весь
  14-дневный горизонт со статусами; прошедшие сегодня слоты — `busy`.
- Правило занятости: запрет пересечения интервалов между ЛЮБЫМИ типами.
  Обеспечивается на уровне БД: расширение `btree_gist` + `EXCLUDE` по `tstzrange`.
- Владелец — единственный профиль `owner` (сидируется в БД).

## API-эндпоинты

- Гость: `GET /event-types`, `GET /event-types/{id}`,
  `GET /event-types/{id}/slots`, `POST /bookings`.
- Владелец: `POST/PATCH/DELETE /event-types` (DELETE -> 409 при предстоящих
  бронях), `GET /bookings` (только предстоящие, с встроенными `eventTypeTitle` и
  `durationMinutes`, сортировка по `start`), `DELETE /bookings/{id}`.
- `GET /owner`, `GET /health`.
- Ошибки — единый `ApiError{code,message}`; коды: `slot_busy`(409),
  `out_of_window`/`not_aligned`/`outside_hours`/`validation_error`(422),
  `*_not_found`(404). Общий обработчик исключений FastAPI.

## Инженерные стандарты

- **SOLID**; **Elegant Objects (дух)** в доменном ядре бэкенда: иммутабельные
  объекты, поведение внутри объектов, зависимости через интерфейсы-порты;
  Pydantic (DTO на границе HTTP) и SQLAlchemy (в адаптерах) — идиоматично,
  изолированы от домена. Фронт — идиоматичный React + SOLID-дух.
- **Тесты**: проверяем поведение, не реализацию. **Mock-объекты НЕ используем —
  только фейки** (in-memory реализации портов). Postgres тестируем реально через
  **testcontainers**. Интеграционные тесты обязательны.
- **Root-cause**: лечим причину бага, не симптом.
- **Единообразие** приоритетнее локальных оптимизаций. Строгая типизация везде.
- **Комментарии** — только там, где решение неочевидно, и отвечают на вопрос
  «почему», а не «что». Не злоупотреблять.
- Перед сдачей на ревью — линтер/тайп-чек + процедура `code-review`
  (`.opencode/skills/code-review/SKILL.md`).

## Рабочий процесс

Порядок: фундамент -> **фронтенд по фичам** (против MSW-фикстур; Prism `make mock`
на :8000 для контракт-smoke) -> **бэкенд по фичам** (schemathesis в B7).
Цикл этапа: реализация -> линтер/тайп-чек -> тесты -> code-review ->
ПАУЗА + инструкция -> ревью пользователя -> правки -> коммиты -> PR -> следующий
этап после одобрения.

- **Ветка на этап**, PR через `gh`, **обычный merge без squash**.
- Коммиты по типам: `feat: ...` (реализация), затем `test: ...` (тесты),
  `chore:`/`docs:`/`ci:` по смыслу. AGENTS.md — отдельным коммитом.
- Git identity (локально): `Tungan2172 <Tungan2172@users.noreply.github.com>`.
- CI — `ci.yml` (lint+test+contract). Файл `.github/workflows/hexlet-check.yml`
  НЕ редактировать.
- `makets/` (макеты фронта) — в `.gitignore`, не коммитим.

## Команды (Makefile)

```
make install         установить зависимости (api, backend, frontend)
make api             сгенерировать openapi.yaml из TypeSpec
make codegen         сгенерировать TS-типы фронта из контракта
make mock            поднять Prism mock из контракта (порт 8000)
make run / deploy    docker compose up (локально)
make stop / clean    остановить / + удалить тома и артефакты
make build           контракт + docker-образы
make test            test-backend + test-frontend
make lint            lint-backend + lint-frontend
make fmt             автоформат
make migrate / seed  Alembic / сид владельца (с B1)
```

uv ставится в `~/.local/bin` (Makefile сам добавляет в PATH).

## Карта этапов

- [x] **S0a** — TypeSpec-контракт (PR #1, смержён).
- [x] **S0b** — скелеты backend/frontend, Makefile, docker, CI, Prism (PR #2, смержён).
- [x] **F0** — скелет фронта: Mantine + React Router + TanStack Query +
      openapi-fetch (кодген) + MSW (PR #3, смержён).
- [x] **F-welcome** — страница приветствия с профилем владельца и списком типов (PR #4, смержён).
- [x] **F1** — страница деталей типа события (PR #5, смержён).
- [x] **F2** — страница календаря и выбора слотов (PR #6, смержён).
- [x] **F3** — форма бронирования с полями guestName/guestEmail/note (PR #7, смержён).
- [x] **F4** — страница списка броней администратора с отменой (PR #8, смержён).
- [x] **F5** — CRUD типов событий администратора (PR #9, смержён).
- [x] **B1** — Postgres+SQLAlchemy+Alembic+testcontainers; таблицы
      `event_types`,`bookings`; `btree_gist`+EXCLUDE; сид `owner`.
- [x] **B2** — `POST/GET /event-types`, `GET /event-types/{id}`.
- [x] **B3** — `PATCH`+`DELETE /event-types/{id}` (409 при бронях).
- [ ] **B4** — генерация слотов + `GET .../slots`.
- [ ] **B5** — `POST /bookings` (409/422, EXCLUDE).
- [ ] **B6** — `GET /bookings` + `DELETE /bookings/{id}` + `GET /owner`.
- [ ] **B7** — полный контракт-тест `schemathesis`.
- [ ] **S-fin** — сборка через docker compose, доводка make, сквозной smoke.
