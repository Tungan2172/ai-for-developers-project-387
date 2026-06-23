"""Unit-тесты HTTP-слоя owner с фейковым репозиторием."""

from collections.abc import Generator
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.dependencies import get_owner_repository as get_owner_dep
from app.domain.interfaces import OwnerRepository
from app.domain.models import Owner
from app.main import create_app
from tests.fake_owner import FakeOwnerRepository


@pytest.fixture
def fake_owner_repo() -> FakeOwnerRepository:
    return FakeOwnerRepository()


@pytest.fixture
def app(fake_owner_repo: FakeOwnerRepository) -> FastAPI:
    application = create_app()

    def override_get_owner() -> OwnerRepository:
        return fake_owner_repo

    application.dependency_overrides[get_owner_dep] = override_get_owner
    return application


@pytest.fixture
def client(app: FastAPI) -> Generator[TestClient, Any, None]:
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


class TestGetOwner:
    def test_not_found(self, client: TestClient) -> None:
        resp = client.get("/owner")
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "owner_not_found"

    def test_returns_owner(self, client: TestClient, fake_owner_repo: FakeOwnerRepository) -> None:
        fake_owner_repo.save(Owner(name="owner", title="Host", description="Calendar owner"))
        resp = client.get("/owner")
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "owner"
        assert data["title"] == "Host"
        assert data["description"] == "Calendar owner"
