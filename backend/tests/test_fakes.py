from datetime import UTC, datetime, timedelta

from app.domain.models import Booking, EventType
from tests.fake_owner import FakeOwnerRepository
from tests.fakes import FakeBookingRepository, FakeEventTypeRepository


def test_create_event_type() -> None:
    repo = FakeEventTypeRepository()
    et = repo.create(title="Test", description="desc", duration_minutes=30)
    assert et.id == 1
    assert et.title == "Test"


def test_get_event_type_by_id() -> None:
    repo = FakeEventTypeRepository()
    repo.create(title="A", description="d", duration_minutes=15)
    result = repo.get_by_id(1)
    assert result is not None
    assert result.title == "A"
    assert repo.get_by_id(999) is None


def test_list_all_event_types() -> None:
    repo = FakeEventTypeRepository()
    repo.create(title="A", description="d", duration_minutes=15)
    repo.create(title="B", description="d", duration_minutes=30)
    assert len(repo.list_all()) == 2


def test_update_event_type() -> None:
    repo = FakeEventTypeRepository()
    repo.create(title="A", description="d", duration_minutes=15)
    updated = repo.update(1, title="Updated", description=None, duration_minutes=None)
    assert updated is not None
    assert updated.title == "Updated"
    assert updated.description == "d"
    assert updated.duration_minutes == 15


def test_update_nonexistent_event_type() -> None:
    repo = FakeEventTypeRepository()
    assert repo.update(999, title="X", description=None, duration_minutes=None) is None


def test_delete_event_type() -> None:
    repo = FakeEventTypeRepository()
    repo.create(title="A", description="d", duration_minutes=15)
    repo.delete(1)
    assert repo.get_by_id(1) is None


def test_has_upcoming_bookings() -> None:
    repo = FakeEventTypeRepository()
    repo.create(title="A", description="d", duration_minutes=15)
    assert not repo.has_upcoming_bookings(1)
    repo.mark_has_bookings(1)
    assert repo.has_upcoming_bookings(1)


def test_create_booking() -> None:
    repo = FakeBookingRepository()
    now = datetime.now(UTC)
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
    assert created.id == 1
    assert created.event_type_title == "Test"


def test_get_booking_by_id() -> None:
    repo = FakeBookingRepository()
    now = datetime.now(UTC)
    b = Booking(
        id=0,
        event_type_id=1,
        event_type_title="T",
        duration_minutes=15,
        start=now,
        end=now + timedelta(minutes=15),
        guest_name="J",
        guest_email="j@t.com",
    )
    repo.create(b)
    result = repo.get_by_id(1)
    assert result is not None
    assert result.guest_name == "J"


def test_list_upcoming_bookings() -> None:
    repo = FakeBookingRepository()
    now = datetime.now(UTC)
    past = Booking(
        id=0,
        event_type_id=1,
        event_type_title="Past",
        duration_minutes=15,
        start=now - timedelta(days=2),
        end=now - timedelta(days=2) + timedelta(minutes=15),
        guest_name="P",
        guest_email="p@t.com",
    )
    future = Booking(
        id=0,
        event_type_id=1,
        event_type_title="Future",
        duration_minutes=15,
        start=now + timedelta(days=1),
        end=now + timedelta(days=1) + timedelta(minutes=15),
        guest_name="F",
        guest_email="f@t.com",
    )
    repo.create(past)
    repo.create(future)
    upcoming = repo.list_upcoming()
    assert len(upcoming) == 1
    assert upcoming[0].event_type_title == "Future"


def test_delete_booking() -> None:
    repo = FakeBookingRepository()
    now = datetime.now(UTC)
    b = Booking(
        id=0,
        event_type_id=1,
        event_type_title="T",
        duration_minutes=15,
        start=now,
        end=now + timedelta(minutes=15),
        guest_name="J",
        guest_email="j@t.com",
    )
    repo.create(b)
    repo.delete(1)
    assert repo.get_by_id(1) is None


def test_has_overlap() -> None:
    repo = FakeBookingRepository()
    now = datetime.now(UTC)
    b = Booking(
        id=0,
        event_type_id=1,
        event_type_title="T",
        duration_minutes=30,
        start=now,
        end=now + timedelta(minutes=30),
        guest_name="J",
        guest_email="j@t.com",
    )
    repo.create(b)
    assert repo.has_overlap(now + timedelta(minutes=10), now + timedelta(minutes=40))
    assert not repo.has_overlap(
        now + timedelta(days=10), now + timedelta(days=10) + timedelta(minutes=30)
    )


def test_fake_owner() -> None:
    repo = FakeOwnerRepository()
    assert repo.get() is None
    owner = EventType(id=1, title="o", description="d", duration_minutes=0)
    _ = owner
    from app.domain.models import Owner

    o = Owner(name="owner", title="Host", description="desc")
    saved = repo.save(o)
    assert saved.name == "owner"
    assert repo.get() is not None
