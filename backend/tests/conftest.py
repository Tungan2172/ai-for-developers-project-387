from collections.abc import Generator
from typing import Any

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.postgres import PostgresContainer  # type: ignore[import-untyped]

from app.adapters.database import Base


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


@pytest.fixture
def session(engine: Any) -> Generator[Session, Any, None]:
    SessionFactory = sessionmaker(bind=engine)
    with SessionFactory() as s:
        yield s
        s.rollback()
