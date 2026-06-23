from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.alias_generators import to_camel


class ApiError(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str
    message: str


class EventTypeOut(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    id: int
    title: str
    description: str
    duration_minutes: int = Field(validation_alias="durationMinutes")


class EventTypeCreateIn(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    title: str = Field(min_length=1, max_length=200)
    description: str
    duration_minutes: int = Field(ge=1, le=480, validation_alias="durationMinutes")


class EventTypeUpdateIn(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    duration_minutes: int | None = Field(
        default=None, ge=1, le=480, validation_alias="durationMinutes"
    )


class SlotOut(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    start: datetime
    end: datetime
    status: str


class BookingCreateIn(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    event_type_id: int = Field(validation_alias="eventTypeId")
    start: datetime
    guest_name: str = Field(min_length=1, max_length=200, validation_alias="guestName")
    guest_email: EmailStr = Field(max_length=200, validation_alias="guestEmail")
    note: str | None = Field(default=None, max_length=2000)


class BookingOut(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    id: int
    event_type_id: int = Field(validation_alias="eventTypeId")
    event_type_title: str = Field(validation_alias="eventTypeTitle")
    duration_minutes: int = Field(validation_alias="durationMinutes")
    start: datetime
    end: datetime
    guest_name: str = Field(validation_alias="guestName")
    guest_email: str = Field(validation_alias="guestEmail")
    note: str | None = None
    created_at: datetime = Field(validation_alias="createdAt")


class OwnerOut(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    name: str
    title: str
    description: str
