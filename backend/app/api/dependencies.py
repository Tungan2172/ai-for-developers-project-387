from fastapi import Depends
from sqlalchemy.orm import Session

from app.adapters.database import get_session
from app.adapters.repositories import SqlAlchemyBookingRepository, SqlAlchemyEventTypeRepository
from app.domain.interfaces import BookingRepository, EventTypeRepository


def get_event_type_repository(session: Session = Depends(get_session)) -> EventTypeRepository:
    return SqlAlchemyEventTypeRepository(session)


def get_booking_repository(session: Session = Depends(get_session)) -> BookingRepository:
    return SqlAlchemyBookingRepository(session)
