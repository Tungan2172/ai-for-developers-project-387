"""Засидировать профиль владельца. Запуск: uv run python -m app.seed"""

from app.adapters.database import SessionFactory
from app.adapters.repositories import SqlAlchemyOwnerRepository
from app.config import get_settings
from app.domain.models import Owner


def seed_owner() -> Owner:
    settings = get_settings()
    owner = Owner(
        name=settings.owner_name,
        title=settings.owner_title,
        description=settings.owner_description,
    )
    with SessionFactory() as session:
        repo = SqlAlchemyOwnerRepository(session)
        result = repo.save(owner)
        session.commit()
        return result


if __name__ == "__main__":
    result = seed_owner()
    print(f"Owner seeded: {result.name} ({result.title})")
