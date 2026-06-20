from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
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
