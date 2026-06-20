"""Ensure database schema: tables, extension, EXCLUDE constraint."""

from sqlalchemy import text

from app.adapters.database import Base, engine


def ensure_db() -> None:
    Base.metadata.create_all(bind=engine)
    with engine.connect() as c:
        c.execute(text("CREATE EXTENSION IF NOT EXISTS btree_gist"))
        c.execute(
            text(
                "ALTER TABLE bookings ADD EXCLUDE USING gist ("
                "  tstzrange(start, \"end\", '[)') WITH &&"
                ")"
            )
        )
        c.commit()


if __name__ == "__main__":
    ensure_db()
