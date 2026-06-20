"""Unit-тесты HTTP-слоя event-types с фейковым репозиторием."""

from collections.abc import Generator
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.dependencies import get_event_type_repository as get_repo_dep
from app.domain.interfaces import EventTypeRepository
from app.main import create_app
from tests.fakes import FakeEventTypeRepository


@pytest.fixture
def fake_repo() -> FakeEventTypeRepository:
    return FakeEventTypeRepository()


@pytest.fixture
def app(fake_repo: FakeEventTypeRepository) -> FastAPI:
    application = create_app()

    def override_get_repo() -> EventTypeRepository:
        return fake_repo

    application.dependency_overrides[get_repo_dep] = override_get_repo
    return application


@pytest.fixture
def client(app: FastAPI) -> Generator[TestClient, Any, None]:
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


class TestListEventTypes:
    def test_empty_list(self, client: TestClient) -> None:
        resp = client.get("/event-types")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_returns_event_types(
        self, client: TestClient, fake_repo: FakeEventTypeRepository
    ) -> None:
        fake_repo.create(title="Meeting", description="desc", duration_minutes=30)
        fake_repo.create(title="Call", description="desc2", duration_minutes=15)

        resp = client.get("/event-types")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2
        assert data[0]["title"] == "Meeting"
        assert data[0]["durationMinutes"] == 30


class TestGetEventType:
    def test_found(self, client: TestClient, fake_repo: FakeEventTypeRepository) -> None:
        fake_repo.create(title="Meeting", description="desc", duration_minutes=30)
        resp = client.get("/event-types/1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "Meeting"
        assert data["description"] == "desc"

    def test_not_found(self, client: TestClient) -> None:
        resp = client.get("/event-types/999")
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "event_type_not_found"


class TestCreateEventType:
    def test_creates_event_type(self, client: TestClient) -> None:
        resp = client.post(
            "/event-types",
            json={
                "title": "New Meeting",
                "description": "A new meeting type",
                "durationMinutes": 30,
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == "New Meeting"
        assert data["durationMinutes"] == 30

    def test_returns_422_on_invalid_duration(self, client: TestClient) -> None:
        resp = client.post(
            "/event-types",
            json={
                "title": "Bad",
                "description": "bad",
                "durationMinutes": 1000,
            },
        )
        assert resp.status_code == 422

    def test_returns_422_on_empty_title(self, client: TestClient) -> None:
        resp = client.post(
            "/event-types",
            json={
                "title": "",
                "description": "desc",
                "durationMinutes": 30,
            },
        )
        assert resp.status_code == 422


class TestUpdateEventType:
    def test_partial_update_title(
        self, client: TestClient, fake_repo: FakeEventTypeRepository
    ) -> None:
        fake_repo.create(title="Old", description="desc", duration_minutes=30)
        resp = client.patch("/event-types/1", json={"title": "Updated"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "Updated"
        assert data["description"] == "desc"
        assert data["durationMinutes"] == 30

    def test_partial_update_duration(
        self, client: TestClient, fake_repo: FakeEventTypeRepository
    ) -> None:
        fake_repo.create(title="T", description="desc", duration_minutes=15)
        resp = client.patch("/event-types/1", json={"durationMinutes": 45})
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "T"
        assert data["durationMinutes"] == 45

    def test_update_all_fields(
        self, client: TestClient, fake_repo: FakeEventTypeRepository
    ) -> None:
        fake_repo.create(title="Old", description="old desc", duration_minutes=15)
        resp = client.patch(
            "/event-types/1",
            json={
                "title": "New",
                "description": "new desc",
                "durationMinutes": 60,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "New"
        assert data["description"] == "new desc"
        assert data["durationMinutes"] == 60

    def test_not_found(self, client: TestClient) -> None:
        resp = client.patch("/event-types/999", json={"title": "X"})
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "event_type_not_found"

    def test_returns_422_on_invalid_duration(
        self, client: TestClient, fake_repo: FakeEventTypeRepository
    ) -> None:
        fake_repo.create(title="T", description="desc", duration_minutes=30)
        resp = client.patch("/event-types/1", json={"durationMinutes": 999})
        assert resp.status_code == 422

    def test_returns_422_on_empty_title(
        self, client: TestClient, fake_repo: FakeEventTypeRepository
    ) -> None:
        fake_repo.create(title="T", description="desc", duration_minutes=30)
        resp = client.patch("/event-types/1", json={"title": ""})
        assert resp.status_code == 422


class TestDeleteEventType:
    def test_deletes_event_type(
        self, client: TestClient, fake_repo: FakeEventTypeRepository
    ) -> None:
        fake_repo.create(title="Del", description="desc", duration_minutes=30)
        resp = client.delete("/event-types/1")
        assert resp.status_code == 204
        assert fake_repo.get_by_id(1) is None

    def test_not_found(self, client: TestClient) -> None:
        resp = client.delete("/event-types/999")
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "event_type_not_found"

    def test_returns_409_on_upcoming_bookings(
        self, client: TestClient, fake_repo: FakeEventTypeRepository
    ) -> None:
        fake_repo.create(title="Busy", description="desc", duration_minutes=30)
        fake_repo.mark_has_bookings(1)
        resp = client.delete("/event-types/1")
        assert resp.status_code == 409
        data = resp.json()
        assert data["code"] == "has_upcoming_bookings"
