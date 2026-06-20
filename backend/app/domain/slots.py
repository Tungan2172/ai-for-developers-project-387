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


BOOKING_WINDOW_DAYS = 14


def validate_booking_slot(
    event_type: EventType,
    start: datetime,
    now: datetime,
    bookings: list[Booking],
) -> str | None:
    start_msk = start.astimezone(MOSCOW_TZ)

    if start_msk <= now:
        return "slot_busy"

    today = now.date()
    window_end = today + timedelta(days=BOOKING_WINDOW_DAYS)
    if start_msk.date() < today or start_msk.date() >= window_end:
        return "out_of_window"

    if start_msk.weekday() not in WEEKDAYS:
        return "outside_hours"

    start_time = start_msk.time()
    if start_time < WORK_START or start_time >= WORK_END:
        return "outside_hours"

    step = timedelta(minutes=event_type.duration_minutes)
    day_start = datetime.combine(start_msk.date(), WORK_START, tzinfo=MOSCOW_TZ)
    if (start_msk - day_start) % step != timedelta(0):
        return "not_aligned"

    end = start_msk + step
    day_end_dt = datetime.combine(start_msk.date(), WORK_END, tzinfo=MOSCOW_TZ)
    if end > day_end_dt:
        return "outside_hours"

    if _overlaps_any_booking(start_msk, end, bookings):
        return "slot_busy"

    return None


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
    import logging
    _log = logging.getLogger(__name__)
    for b in bookings:
        overlap = b.start < end and b.end > start
        if b.start.hour == 7:
            _log.warning("_overlaps CHECK: slot_start=%s slot_end=%s b_start=%s b_end=%s overlap=%s", start, end, b.start, b.end, overlap)
        if overlap:
            return True
    return False
