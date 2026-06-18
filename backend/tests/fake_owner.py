from app.domain.interfaces import OwnerRepository
from app.domain.models import Owner


class FakeOwnerRepository(OwnerRepository):
    def __init__(self) -> None:
        self._owner: Owner | None = None

    def get(self) -> Owner | None:
        return self._owner

    def save(self, owner: Owner) -> Owner:
        self._owner = owner
        return owner
