from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from enum import StrEnum, auto
from zoneinfo import ZoneInfo

from app.domain.models import Booking, EventType


class SlotStatus(StrEnum):
    free = auto()
    busy = auto()


@dataclass(frozen=True, kw_only=True)
class Slot:
    start: datetime
    end: datetime
    status: SlotStatus


MOSCOW_TZ = ZoneInfo("Europe/Moscow")
WEEKDAYS = {0, 1, 2, 3, 4}
WORK_START = time(9, 0)
WORK_END = time(17, 0)


def generate_slots(
    event_type: EventType,
    from_date: date,
    to_date: date,
    bookings: list[Booking],
    now: datetime,
) -> list[Slot]:
    slots: list[Slot] = []
    step = timedelta(minutes=event_type.duration_minutes)

    current = from_date
    while current < to_date:
        if current.weekday() in WEEKDAYS:
            slot_start = datetime.combine(current, WORK_START, tzinfo=MOSCOW_TZ)
            day_end = datetime.combine(current, WORK_END, tzinfo=MOSCOW_TZ)

            while slot_start + step <= day_end:
                slot_end = slot_start + step

                if slot_end <= now or _overlaps_any_booking(slot_start, slot_end, bookings):
                    status = SlotStatus.busy
                else:
                    status = SlotStatus.free

                slots.append(Slot(start=slot_start, end=slot_end, status=status))
                slot_start = slot_end

        current += timedelta(days=1)

    return slots


def _overlaps_any_booking(start: datetime, end: datetime, bookings: list[Booking]) -> bool:
    return any(b.start < end and b.end > start for b in bookings)
