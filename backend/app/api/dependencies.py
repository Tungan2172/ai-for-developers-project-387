from fastapi import Depends
from sqlalchemy.orm import Session

from app.adapters.database import get_session
from app.adapters.repositories import (
    SqlAlchemyBookingRepository,
    SqlAlchemyEventTypeRepository,
    SqlAlchemyOwnerRepository,
)
from app.domain.interfaces import BookingRepository, EventTypeRepository, OwnerRepository


def get_event_type_repository(session: Session = Depends(get_session)) -> EventTypeRepository:
    return SqlAlchemyEventTypeRepository(session)


def get_booking_repository(session: Session = Depends(get_session)) -> BookingRepository:
    return SqlAlchemyBookingRepository(session)


def get_owner_repository(session: Session = Depends(get_session)) -> OwnerRepository:
    return SqlAlchemyOwnerRepository(session)
