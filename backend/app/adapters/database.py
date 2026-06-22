from collections.abc import Generator
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


_db_url = get_settings().database_url
if _db_url.startswith("postgresql://") and "+" not in _db_url:
    _db_url = _db_url.replace("postgresql://", "postgresql+psycopg://", 1)
engine = create_engine(_db_url)
SessionFactory = sessionmaker(bind=engine)


def get_session() -> Generator[Session, Any, None]:
    session = SessionFactory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
