from abc import ABC, abstractmethod
from datetime import datetime

from app.domain.models import Booking, EventType, Owner


class EventTypeRepository(ABC):
    @abstractmethod
    def create(self, title: str, description: str, duration_minutes: int) -> EventType: ...

    @abstractmethod
    def get_by_id(self, event_type_id: int) -> EventType | None: ...

    @abstractmethod
    def list_all(self) -> list[EventType]: ...

    @abstractmethod
    def update(
        self,
        event_type_id: int,
        title: str | None,
        description: str | None,
        duration_minutes: int | None,
    ) -> EventType | None: ...

    @abstractmethod
    def delete(self, event_type_id: int) -> None: ...

    @abstractmethod
    def has_upcoming_bookings(self, event_type_id: int) -> bool: ...


class BookingRepository(ABC):
    @abstractmethod
    def create(self, booking: Booking) -> Booking: ...

    @abstractmethod
    def get_by_id(self, booking_id: int) -> Booking | None: ...

    @abstractmethod
    def list_upcoming(self) -> list[Booking]: ...

    @abstractmethod
    def delete(self, booking_id: int) -> None: ...

    @abstractmethod
    def has_overlap(self, start: datetime, end: datetime) -> bool: ...

    @abstractmethod
    def list_by_range(self, start: datetime, end: datetime) -> list[Booking]: ...


class OwnerRepository(ABC):
    @abstractmethod
    def get(self) -> Owner | None: ...

    @abstractmethod
    def save(self, owner: Owner) -> Owner: ...
