"""Schemathesis contract test — проверяет, что API не падает (без 5xx).

Использует реальный Postgres (testcontainers) с пре-сидом (owner + event type).
schemathesis генерирует запросы по OpenAPI-спецификации и проверяет, что ни
один эндпоинт не возвращает 500. Ошибки 4xx считаются корректными.
"""

import pathlib
from collections.abc import Generator
from typing import Any

import httpx
import pytest
import schemathesis
from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.postgres import PostgresContainer  # type: ignore[import-untyped]

from app.adapters.database import Base, get_session
from app.adapters.orm import OwnerModel
from app.config import get_settings
from app.main import create_app

OPENAPI_PATH = str(
    pathlib.Path(__file__).resolve().parent.parent.parent / "api" / "dist" / "openapi.yaml"
)

schema = schemathesis.openapi.from_path(OPENAPI_PATH)

settings = get_settings()


@pytest.fixture(scope="session")
def postgres_container() -> Generator[PostgresContainer, Any, None]:
    with PostgresContainer("postgres:16-alpine") as pc:
        yield pc


@pytest.fixture(scope="session")
def database_url(postgres_container: PostgresContainer) -> str:
    return str(postgres_container.get_connection_url(driver="psycopg"))


@pytest.fixture(scope="session")
def engine(database_url: str) -> Generator[Any, Any, None]:
    eng = create_engine(database_url)
    Base.metadata.create_all(eng)
    with eng.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS btree_gist"))
        conn.execute(
            text(
                "ALTER TABLE bookings ADD EXCLUDE USING gist ("
                "  tstzrange(start, \"end\", '[)') WITH &&"
                ")"
            )
        )
        conn.commit()
    yield eng
    eng.dispose()


@pytest.fixture(scope="session")
def app(engine: Any) -> Generator[FastAPI, Any, None]:
    application = create_app()

    SessionFactory = sessionmaker(bind=engine)

    def _get_session() -> Generator[Session, Any, None]:
        with SessionFactory() as s:
            yield s

    application.dependency_overrides[get_session] = _get_session

    # Seed minimal data
    with SessionFactory() as s:
        s.execute(text("DELETE FROM bookings"))
        s.execute(text("DELETE FROM event_types"))
        s.execute(text("DELETE FROM owner"))
        s.add(
            OwnerModel(
                name=settings.owner_name,
                title=settings.owner_title,
                description=settings.owner_description,
            )
        )
        s.execute(
            text(
                "INSERT INTO event_types (id, title, description, duration_minutes) "
                "VALUES (1, 'Consultation', '30 min meeting', 30)"
            )
        )
        s.execute(text("SELECT setval('event_types_id_seq', (SELECT MAX(id) FROM event_types))"))
        s.commit()

    yield application


def _call_case(case: schemathesis.Case[Any], app: FastAPI) -> httpx.Response:
    """Execute a schemathesis Case against a FastAPI app."""
    from starlette.testclient import TestClient  # noqa: PLC0415

    with TestClient(app) as client:
        kwargs: dict[str, Any] = {
            "method": case.method,
            "url": case.formatted_path,
        }
        if case.query:
            kwargs["params"] = case.query
        if case.headers:
            kwargs["headers"] = case.headers
        if case.body is not None and not isinstance(case.body, schemathesis.core.NotSet):
            if isinstance(case.body, str | bytes):
                kwargs["data"] = case.body
            else:
                kwargs["json"] = case.body
        return client.request(**kwargs)  # type: ignore[no-any-return]


@schema.parametrize()
def test_no_server_errors(case: schemathesis.Case[Any], app: FastAPI) -> None:
    """Ни один эндпоинт контракта не возвращает 500."""
    response = _call_case(case, app)
    assert response.status_code < 500, (
        f"Server error {response.status_code} on {case.method} {case.path}: {response.text[:200]}"
    )
