from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True, kw_only=True)
class Owner:
    name: str
    title: str
    description: str


@dataclass(frozen=True, kw_only=True)
class EventType:
    id: int
    title: str
    description: str
    duration_minutes: int


@dataclass(frozen=True, kw_only=True)
class Booking:
    id: int
    event_type_id: int
    event_type_title: str
    duration_minutes: int
    start: datetime
    end: datetime
    guest_name: str
    guest_email: str
    note: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
