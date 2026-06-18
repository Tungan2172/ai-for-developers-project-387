from datetime import UTC, datetime

from app.domain.models import Booking, EventType, Owner
from app.domain.slots import Slot, SlotStatus


def test_owner_creation() -> None:
    owner = Owner(name="test", title="Host", description="test desc")
    assert owner.name == "test"
    assert owner.title == "Host"


def test_event_type_creation() -> None:
    et = EventType(id=1, title="meeting", description="desc", duration_minutes=30)
    assert et.duration_minutes == 30
    assert et.title == "meeting"


def test_booking_immutability() -> None:
    b = Booking(
        id=1,
        event_type_id=1,
        event_type_title="meeting",
        duration_minutes=30,
        start=datetime.now(UTC),
        end=datetime.now(UTC),
        guest_name="John",
        guest_email="john@test.com",
    )
    assert b.guest_name == "John"


def test_slot_status_enum() -> None:
    assert SlotStatus.free.value == "free"
    assert SlotStatus.busy.value == "busy"


def test_slot_creation() -> None:
    start = datetime.now(UTC)
    end = datetime.now(UTC)
    slot = Slot(start=start, end=end, status=SlotStatus.free)
    assert slot.status == SlotStatus.free
