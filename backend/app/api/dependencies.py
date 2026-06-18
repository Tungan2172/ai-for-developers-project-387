from fastapi import Depends
from sqlalchemy.orm import Session

from app.adapters.database import get_session
from app.adapters.repositories import SqlAlchemyEventTypeRepository
from app.domain.interfaces import EventTypeRepository


def get_event_type_repository(session: Session = Depends(get_session)) -> EventTypeRepository:
    return SqlAlchemyEventTypeRepository(session)
