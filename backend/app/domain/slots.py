from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum, auto


class SlotStatus(StrEnum):
    free = auto()
    busy = auto()


@dataclass(frozen=True, kw_only=True)
class Slot:
    start: datetime
    end: datetime
    status: SlotStatus
