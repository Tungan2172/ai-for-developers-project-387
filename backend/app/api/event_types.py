from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from app.api.dependencies import get_event_type_repository
from app.api.errors import api_error_response
from app.api.schemas import EventTypeCreateIn, EventTypeOut, EventTypeUpdateIn
from app.domain.interfaces import EventTypeRepository

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
