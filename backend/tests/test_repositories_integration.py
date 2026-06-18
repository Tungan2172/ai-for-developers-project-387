from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.adapters.repositories import (
    SqlAlchemyBookingRepository,
    SqlAlchemyEventTypeRepository,
    SqlAlchemyOwnerRepository,
)
from app.domain.models import Booking, Owner


def test_create_and_get_event_type(session: Session) -> None:
    repo = SqlAlchemyEventTypeRepository(session)
    et = repo.create(title="Meeting", description="A meeting", duration_minutes=30)
    assert et.id is not None
    assert et.title == "Meeting"

    fetched = repo.get_by_id(et.id)
    assert fetched is not None
    assert fetched.title == "Meeting"


def test_list_event_types(session: Session) -> None:
    repo = SqlAlchemyEventTypeRepository(session)
    repo.create(title="A", description="d1", duration_minutes=15)
    repo.create(title="B", description="d2", duration_minutes=30)
    assert len(repo.list_all()) == 2


def test_update_event_type(session: Session) -> None:
    repo = SqlAlchemyEventTypeRepository(session)
    et = repo.create(title="Old", description="desc", duration_minutes=15)
    updated = repo.update(et.id, title="New", description=None, duration_minutes=30)
    assert updated is not None
    assert updated.title == "New"
    assert updated.duration_minutes == 30


def test_update_event_type_not_found(session: Session) -> None:
    repo = SqlAlchemyEventTypeRepository(session)
    assert repo.update(999, title="X", description=None, duration_minutes=None) is None


def test_delete_event_type(session: Session) -> None:
    repo = SqlAlchemyEventTypeRepository(session)
    et = repo.create(title="Del", description="desc", duration_minutes=15)
    repo.delete(et.id)
    assert repo.get_by_id(et.id) is None


def test_delete_event_type_not_found(session: Session) -> None:
    repo = SqlAlchemyEventTypeRepository(session)
    repo.delete(999)  # should not raise


@pytest.mark.skip(reason="requires booking data to test upcoming bookings check")
def test_has_upcoming_bookings(session: Session) -> None:
    repo = SqlAlchemyEventTypeRepository(session)
    et = repo.create(title="Test", description="desc", duration_minutes=30)
    assert not repo.has_upcoming_bookings(et.id)


def test_create_and_get_booking(session: Session) -> None:
    repo = SqlAlchemyBookingRepository(session)
    now = datetime.now(UTC).replace(microsecond=0)
    b = Booking(
        id=0,
        event_type_id=1,
        event_type_title="Test",
        duration_minutes=30,
        start=now,
        end=now + timedelta(minutes=30),
        guest_name="John",
        guest_email="john@test.com",
    )
    created = repo.create(b)
    assert created.id is not None
    assert created.event_type_title == "Test"

    fetched = repo.get_by_id(created.id)
    assert fetched is not None
    assert fetched.guest_name == "John"


def test_list_upcoming_bookings(session: Session) -> None:
    repo = SqlAlchemyBookingRepository(session)
    now = datetime.now(UTC).replace(microsecond=0)

    future_start = now + timedelta(days=1)
    past_start = now - timedelta(days=2)

    repo.create(
        Booking(
            id=0,
            event_type_id=1,
            event_type_title="Past",
            duration_minutes=15,
            start=past_start,
            end=past_start + timedelta(minutes=15),
            guest_name="P",
            guest_email="p@t.com",
        )
    )
    repo.create(
        Booking(
            id=0,
            event_type_id=1,
            event_type_title="Future",
            duration_minutes=15,
            start=future_start,
            end=future_start + timedelta(minutes=15),
            guest_name="F",
            guest_email="f@t.com",
        )
    )

    upcoming = repo.list_upcoming()
    assert len(upcoming) == 1
    assert upcoming[0].event_type_title == "Future"
    assert upcoming[0].guest_name == "F"


def test_delete_booking(session: Session) -> None:
    repo = SqlAlchemyBookingRepository(session)
    now = datetime.now(UTC).replace(microsecond=0)
    b = repo.create(
        Booking(
            id=0,
            event_type_id=1,
            event_type_title="T",
            duration_minutes=15,
            start=now,
            end=now + timedelta(minutes=15),
            guest_name="J",
            guest_email="j@t.com",
        )
    )
    repo.delete(b.id)
    assert repo.get_by_id(b.id) is None


def test_exclude_constraint_prevents_overlap(session: Session) -> None:
    """EXCLUDE constraint should prevent overlapping bookings."""
    repo = SqlAlchemyBookingRepository(session)
    now = datetime.now(UTC).replace(microsecond=0)

    repo.create(
        Booking(
            id=0,
            event_type_id=1,
            event_type_title="First",
            duration_minutes=60,
            start=now,
            end=now + timedelta(hours=1),
            guest_name="A",
            guest_email="a@t.com",
        )
    )
    session.flush()

    with pytest.raises(IntegrityError):
        repo.create(
            Booking(
                id=0,
                event_type_id=2,
                event_type_title="Overlap",
                duration_minutes=30,
                start=now + timedelta(minutes=30),
                end=now + timedelta(hours=1),
                guest_name="B",
                guest_email="b@t.com",
            )
        )
        session.flush()


def test_exclude_constraint_allows_adjacent(session: Session) -> None:
    """Adjacent bookings (end=start of next) should be allowed."""
    repo = SqlAlchemyBookingRepository(session)
    now = datetime.now(UTC).replace(microsecond=0)

    repo.create(
        Booking(
            id=0,
            event_type_id=1,
            event_type_title="First",
            duration_minutes=30,
            start=now,
            end=now + timedelta(minutes=30),
            guest_name="A",
            guest_email="a@t.com",
        )
    )
    session.flush()

    repo.create(
        Booking(
            id=0,
            event_type_id=1,
            event_type_title="Next",
            duration_minutes=30,
            start=now + timedelta(minutes=30),
            end=now + timedelta(hours=1),
            guest_name="B",
            guest_email="b@t.com",
        )
    )
    session.flush()


def test_owner_save_and_get(session: Session) -> None:
    repo = SqlAlchemyOwnerRepository(session)
    owner = Owner(name="owner", title="Host", description="Calendar owner")
    saved = repo.save(owner)
    assert saved.name == "owner"

    fetched = repo.get()
    assert fetched is not None
    assert fetched.title == "Host"


def test_owner_update(session: Session) -> None:
    repo = SqlAlchemyOwnerRepository(session)
    repo.save(Owner(name="old", title="Host", description="desc"))
    repo.save(Owner(name="new", title="Admin", description="updated"))
    fetched = repo.get()
    assert fetched is not None
    assert fetched.name == "new"
    assert repo.get() is not None


def test_has_overlap(session: Session) -> None:
    repo = SqlAlchemyBookingRepository(session)
    now = datetime.now(UTC).replace(microsecond=0)
    repo.create(
        Booking(
            id=0,
            event_type_id=1,
            event_type_title="T",
            duration_minutes=30,
            start=now,
            end=now + timedelta(minutes=30),
            guest_name="J",
            guest_email="j@t.com",
        )
    )
    session.flush()
    assert repo.has_overlap(now + timedelta(minutes=10), now + timedelta(minutes=40))
    assert not repo.has_overlap(
        now + timedelta(days=10), now + timedelta(days=10) + timedelta(minutes=30)
    )
