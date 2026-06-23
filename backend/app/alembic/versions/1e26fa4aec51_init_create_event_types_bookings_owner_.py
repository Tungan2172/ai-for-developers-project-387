"""init: create event_types, bookings, owner tables + EXCLUDE

Revision ID: 1e26fa4aec51
Revises:
Create Date: 2026-06-18 23:28:23.881870
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "1e26fa4aec51"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")

    op.create_table(
        "event_types",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("duration_minutes", sa.Integer, nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )

    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("event_type_id", sa.Integer, nullable=False),
        sa.Column("event_type_title", sa.String(200), nullable=False),
        sa.Column("duration_minutes", sa.Integer, nullable=False),
        sa.Column("start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("guest_name", sa.String(200), nullable=False),
        sa.Column("guest_email", sa.String(200), nullable=False),
        sa.Column("note", sa.Text, nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )

    op.execute(
        "ALTER TABLE bookings ADD EXCLUDE USING gist (  tstzrange(start, \"end\", '[)') WITH &&)"
    )

    op.create_table(
        "owner",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("title", sa.String(100), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("owner")
    op.drop_table("bookings")
    op.drop_table("event_types")
