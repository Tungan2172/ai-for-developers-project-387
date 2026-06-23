from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from app.api.dependencies import get_booking_repository, get_event_type_repository
from app.api.errors import api_error_response
from app.api.schemas import BookingCreateIn, BookingOut
from app.domain.interfaces import BookingRepository, EventTypeRepository
from app.domain.models import Booking
from app.domain.slots import BOOKING_WINDOW_DAYS, MOSCOW_TZ, validate_booking_slot

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("", response_model=list[BookingOut])
def list_bookings(
    booking_repo: BookingRepository = Depends(get_booking_repository),
) -> list[BookingOut]:
    bookings = booking_repo.list_upcoming()
    return [BookingOut.model_validate(b) for b in bookings]


@router.delete("/{booking_id}", status_code=204)
def cancel_booking(
    booking_id: int,
    booking_repo: BookingRepository = Depends(get_booking_repository),
) -> Response:
    booking = booking_repo.get_by_id(booking_id)
    if booking is None:
        return api_error_response(404, "booking_not_found", f"Booking {booking_id} not found")
    booking_repo.delete(booking_id)
    return Response(status_code=204)


@router.post("", status_code=201)
def create_booking(
    body: BookingCreateIn,
    event_type_repo: EventTypeRepository = Depends(get_event_type_repository),
    booking_repo: BookingRepository = Depends(get_booking_repository),
) -> Response:
    et = event_type_repo.get_by_id(body.event_type_id)
    if et is None:
        return api_error_response(
            404, "event_type_not_found", f"Event type {body.event_type_id} not found"
        )

    now = datetime.now(MOSCOW_TZ)
    window_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    window_end = window_start + timedelta(days=BOOKING_WINDOW_DAYS)
    bookings = booking_repo.list_by_range(window_start, window_end)

    error = validate_booking_slot(et, body.start, now, bookings)
    if error is not None:
        status = 409 if error == "slot_busy" else 422
        return api_error_response(status, error, error)

    start_msk = body.start.astimezone(MOSCOW_TZ)
    end = start_msk + timedelta(minutes=et.duration_minutes)

    booking = booking_repo.create(
        Booking(
            id=0,
            event_type_id=et.id,
            event_type_title=et.title,
            duration_minutes=et.duration_minutes,
            start=start_msk,
            end=end,
            guest_name=body.guest_name,
            guest_email=body.guest_email,
            note=body.note,
        )
    )

    return JSONResponse(
        content=BookingOut.model_validate(booking).model_dump(by_alias=True, mode="json"),
        status_code=201,
    )
