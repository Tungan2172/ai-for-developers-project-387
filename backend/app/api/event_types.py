from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from app.api.dependencies import get_event_type_repository
from app.api.errors import api_error_response
from app.api.schemas import EventTypeCreateIn, EventTypeOut
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
