from datetime import UTC, datetime

from app.domain.interfaces import BookingRepository, EventTypeRepository
from app.domain.models import Booking, EventType


class FakeEventTypeRepository(EventTypeRepository):
    def __init__(self) -> None:
        self._storage: dict[int, EventType] = {}
        self._next_id = 1
        self._bookings_event_type_ids: set[int] = set()

    def create(self, title: str, description: str, duration_minutes: int) -> EventType:
        et = EventType(
            id=self._next_id,
            title=title,
            description=description,
            duration_minutes=duration_minutes,
        )
        self._next_id += 1
        self._storage[et.id] = et
        return et

    def get_by_id(self, event_type_id: int) -> EventType | None:
        return self._storage.get(event_type_id)

    def list_all(self) -> list[EventType]:
        return list(self._storage.values())

    def update(
        self,
        event_type_id: int,
        title: str | None,
        description: str | None,
        duration_minutes: int | None,
    ) -> EventType | None:
        existing = self._storage.get(event_type_id)
        if not existing:
            return None
        updated = EventType(
            id=existing.id,
            title=title if title is not None else existing.title,
            description=description if description is not None else existing.description,
            duration_minutes=duration_minutes
            if duration_minutes is not None
            else existing.duration_minutes,
        )
        self._storage[event_type_id] = updated
        return updated

    def delete(self, event_type_id: int) -> None:
        self._storage.pop(event_type_id, None)

    def has_upcoming_bookings(self, event_type_id: int) -> bool:
        return event_type_id in self._bookings_event_type_ids

    def mark_has_bookings(self, event_type_id: int) -> None:
        self._bookings_event_type_ids.add(event_type_id)


class FakeBookingRepository(BookingRepository):
    def __init__(self) -> None:
        self._storage: dict[int, Booking] = {}
        self._next_id = 1

    def create(self, booking: Booking) -> Booking:
        b = Booking(
            id=self._next_id,
            event_type_id=booking.event_type_id,
            event_type_title=booking.event_type_title,
            duration_minutes=booking.duration_minutes,
            start=booking.start,
            end=booking.end,
            guest_name=booking.guest_name,
            guest_email=booking.guest_email,
            note=booking.note,
            created_at=booking.created_at,
        )
        self._next_id += 1
        self._storage[b.id] = b
        return b

    def get_by_id(self, booking_id: int) -> Booking | None:
        return self._storage.get(booking_id)

    def list_upcoming(self) -> list[Booking]:
        now = datetime.now(UTC)
        return sorted(
            [b for b in self._storage.values() if b.start > now],
            key=lambda b: b.start,
        )

    def delete(self, booking_id: int) -> None:
        self._storage.pop(booking_id, None)

    def has_overlap(self, start: datetime, end: datetime) -> bool:
        return any(b.start < end and b.end > start for b in self._storage.values())

    def list_by_range(self, start: datetime, end: datetime) -> list[Booking]:
        return sorted(
            [b for b in self._storage.values() if b.start < end and b.end > start],
            key=lambda b: b.start,
        )
