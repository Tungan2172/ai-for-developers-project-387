from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.adapters.orm import BookingModel, EventTypeModel, OwnerModel
from app.domain.interfaces import BookingRepository, EventTypeRepository, OwnerRepository
from app.domain.models import Booking, EventType, Owner


class SqlAlchemyEventTypeRepository(EventTypeRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, title: str, description: str, duration_minutes: int) -> EventType:
        model = EventTypeModel(
            title=title, description=description, duration_minutes=duration_minutes
        )
        self._session.add(model)
        self._session.flush()
        return self._to_domain(model)

    def get_by_id(self, event_type_id: int) -> EventType | None:
        model = self._session.get(EventTypeModel, event_type_id)
        return self._to_domain(model) if model else None

    def list_all(self) -> list[EventType]:
        models = (
            self._session.execute(select(EventTypeModel).order_by(EventTypeModel.id))
            .scalars()
            .all()
        )
        return [self._to_domain(m) for m in models]

    def update(
        self,
        event_type_id: int,
        title: str | None,
        description: str | None,
        duration_minutes: int | None,
    ) -> EventType | None:
        model = self._session.get(EventTypeModel, event_type_id)
        if not model:
            return None
        if title is not None:
            model.title = title
        if description is not None:
            model.description = description
        if duration_minutes is not None:
            model.duration_minutes = duration_minutes
        self._session.flush()
        return self._to_domain(model)

    def delete(self, event_type_id: int) -> None:
        model = self._session.get(EventTypeModel, event_type_id)
        if model:
            self._session.delete(model)
            self._session.flush()

    def has_upcoming_bookings(self, event_type_id: int) -> bool:
        now = datetime.now(UTC)
        stmt = (
            select(BookingModel)
            .where(BookingModel.event_type_id == event_type_id, BookingModel.start > now)
            .limit(1)
        )
        return self._session.execute(stmt).first() is not None

    @staticmethod
    def _to_domain(model: EventTypeModel) -> EventType:
        return EventType(
            id=model.id,
            title=model.title,
            description=model.description,
            duration_minutes=model.duration_minutes,
        )


class SqlAlchemyBookingRepository(BookingRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, booking: Booking) -> Booking:
        model = BookingModel(
            event_type_id=booking.event_type_id,
            event_type_title=booking.event_type_title,
            duration_minutes=booking.duration_minutes,
            start=booking.start,
            end=booking.end,
            guest_name=booking.guest_name,
            guest_email=booking.guest_email,
            note=booking.note,
        )
        self._session.add(model)
        self._session.flush()
        return Booking(
            id=model.id,
            event_type_id=model.event_type_id,
            event_type_title=model.event_type_title,
            duration_minutes=model.duration_minutes,
            start=model.start,
            end=model.end,
            guest_name=model.guest_name,
            guest_email=model.guest_email,
            note=model.note,
            created_at=model.created_at,
        )

    def get_by_id(self, booking_id: int) -> Booking | None:
        model = self._session.get(BookingModel, booking_id)
        return self._to_domain(model) if model else None

    def list_upcoming(self) -> list[Booking]:
        now = datetime.now(UTC)
        models = (
            self._session.execute(
                select(BookingModel).where(BookingModel.start > now).order_by(BookingModel.start)
            )
            .scalars()
            .all()
        )
        return [self._to_domain(m) for m in models]

    def delete(self, booking_id: int) -> None:
        model = self._session.get(BookingModel, booking_id)
        if model:
            self._session.delete(model)
            self._session.flush()

    def has_overlap(self, start: datetime, end: datetime) -> bool:
        stmt = (
            select(BookingModel).where(BookingModel.start < end, BookingModel.end > start).limit(1)
        )
        return self._session.execute(stmt).first() is not None

    @staticmethod
    def _to_domain(model: BookingModel) -> Booking:
        return Booking(
            id=model.id,
            event_type_id=model.event_type_id,
            event_type_title=model.event_type_title,
            duration_minutes=model.duration_minutes,
            start=model.start,
            end=model.end,
            guest_name=model.guest_name,
            guest_email=model.guest_email,
            note=model.note,
            created_at=model.created_at,
        )


class SqlAlchemyOwnerRepository(OwnerRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self) -> Owner | None:
        model = self._session.execute(select(OwnerModel).limit(1)).scalar_one_or_none()
        return self._to_domain(model) if model else None

    def save(self, owner: Owner) -> Owner:
        existing = self._session.execute(select(OwnerModel).limit(1)).scalar_one_or_none()
        if existing:
            existing.name = owner.name
            existing.title = owner.title
            existing.description = owner.description
        else:
            existing = OwnerModel(name=owner.name, title=owner.title, description=owner.description)
            self._session.add(existing)
        self._session.flush()
        return self._to_domain(existing)

    @staticmethod
    def _to_domain(model: OwnerModel) -> Owner:
        return Owner(name=model.name, title=model.title, description=model.description)
