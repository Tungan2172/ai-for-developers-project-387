"""Ensure database schema: tables, extension, EXCLUDE constraint."""

from sqlalchemy import text

from app.adapters.database import Base, engine
from app.adapters.orm import (  # noqa: F401 — register models
    BookingModel,
    EventTypeModel,
    OwnerModel,
)


def ensure_db() -> None:
    Base.metadata.create_all(bind=engine)
    with engine.connect() as c:
        c.execute(text("CREATE EXTENSION IF NOT EXISTS btree_gist"))
        c.execute(
            text(
                """DO $$ BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint WHERE conname = 'bookings_exclude'
                    ) THEN
                        ALTER TABLE bookings ADD EXCLUDE USING gist (
                            tstzrange(start, "end", '[)') WITH &&
                        );
                    END IF;
                END $$;"""
            )
        )
        c.commit()


if __name__ == "__main__":
    ensure_db()
