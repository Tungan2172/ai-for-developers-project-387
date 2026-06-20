import logging
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, Query, Response
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

from app.api.dependencies import get_booking_repository, get_event_type_repository
from app.api.errors import api_error_response
from app.api.schemas import EventTypeCreateIn, EventTypeOut, EventTypeUpdateIn, SlotOut
from app.domain.interfaces import BookingRepository, EventTypeRepository
from app.domain.slots import generate_slots

MOSCOW_TZ = ZoneInfo("Europe/Moscow")

router = APIRouter(prefix="/event-types", tags=["Event Types"])


@router.get("", response_model=list[EventTypeOut])
def list_event_types(
    repo: EventTypeRepository = Depends(get_event_type_repository),
) -> list[EventTypeOut]:
    types = repo.list_all()
    return [EventTypeOut.model_validate(t) for t in types]


@router.get("/{event_type_id}", response_model=EventTypeOut)
def get_event_type(
    event_type_id: int,
    repo: EventTypeRepository = Depends(get_event_type_repository),
) -> Response:
    et = repo.get_by_id(event_type_id)
    if et is None:
        return api_error_response(
            404, "event_type_not_found", f"Event type {event_type_id} not found"
        )
    return JSONResponse(content=EventTypeOut.model_validate(et).model_dump(by_alias=True))


@router.post("", response_model=EventTypeOut, status_code=201)
def create_event_type(
    body: EventTypeCreateIn,
    repo: EventTypeRepository = Depends(get_event_type_repository),
) -> EventTypeOut:
    et = repo.create(
        title=body.title,
        description=body.description,
        duration_minutes=body.duration_minutes,
    )
    return EventTypeOut.model_validate(et)


@router.patch("/{event_type_id}", response_model=EventTypeOut)
def update_event_type(
    event_type_id: int,
    body: EventTypeUpdateIn,
    repo: EventTypeRepository = Depends(get_event_type_repository),
) -> Response:
    et = repo.get_by_id(event_type_id)
    if et is None:
        return api_error_response(
            404, "event_type_not_found", f"Event type {event_type_id} not found"
        )
    updated = repo.update(
        event_type_id=event_type_id,
        title=body.title,
        description=body.description,
        duration_minutes=body.duration_minutes,
    )
    return JSONResponse(content=EventTypeOut.model_validate(updated).model_dump(by_alias=True))


@router.delete("/{event_type_id}", status_code=204)
def delete_event_type(
    event_type_id: int,
    repo: EventTypeRepository = Depends(get_event_type_repository),
) -> Response:
    et = repo.get_by_id(event_type_id)
    if et is None:
        return api_error_response(
            404, "event_type_not_found", f"Event type {event_type_id} not found"
        )
    if repo.has_upcoming_bookings(event_type_id):
        return api_error_response(
            409,
            "has_upcoming_bookings",
            f"Event type {event_type_id} has upcoming bookings and cannot be deleted",
        )
    repo.delete(event_type_id)
    return Response(status_code=204)


@router.get("/{event_type_id}/slots", response_model=list[SlotOut])
def get_slots(
    event_type_id: int,
    from_date: date | None = Query(default=None, alias="from"),
    to_date: date | None = Query(default=None, alias="to"),
    event_type_repo: EventTypeRepository = Depends(get_event_type_repository),
    booking_repo: BookingRepository = Depends(get_booking_repository),
) -> Response:
    et = event_type_repo.get_by_id(event_type_id)
    if et is None:
        return api_error_response(
            404, "event_type_not_found", f"Event type {event_type_id} not found"
        )

    today = datetime.now(MOSCOW_TZ).date()
    from_val = from_date if from_date is not None else today
    to_val = to_date if to_date is not None else today + timedelta(days=14)

    window_start = datetime.combine(from_val, datetime.min.time(), tzinfo=MOSCOW_TZ)
    window_end = datetime.combine(to_val, datetime.min.time(), tzinfo=MOSCOW_TZ) + timedelta(days=1)

    bookings = booking_repo.list_by_range(window_start, window_end)
    now = datetime.now(MOSCOW_TZ)

    logger.warning("get_slots: window_start=%s window_end=%s bookings=%d", window_start, window_end, len(bookings))
    for b in bookings:
        logger.warning("get_slots:  booking id=%d start=%s end=%s", b.id, b.start, b.end)

    slots = generate_slots(et, from_val, to_val, bookings, now)
    return JSONResponse(
        content=[SlotOut.model_validate(s).model_dump(by_alias=True, mode="json") for s in slots]
    )
