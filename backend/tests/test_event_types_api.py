"""Unit-тесты HTTP-слоя event-types с фейковым репозиторием."""

from collections.abc import Generator
from datetime import date, datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.dependencies import get_booking_repository as get_booking_dep
from app.api.dependencies import get_event_type_repository as get_repo_dep
from app.domain.interfaces import BookingRepository, EventTypeRepository
from app.domain.models import Booking
from app.main import create_app
from tests.fakes import FakeBookingRepository, FakeEventTypeRepository


@pytest.fixture
def fake_repo() -> FakeEventTypeRepository:
    return FakeEventTypeRepository()


@pytest.fixture
def fake_booking_repo() -> FakeBookingRepository:
    return FakeBookingRepository()


@pytest.fixture
def app(fake_repo: FakeEventTypeRepository) -> FastAPI:
    application = create_app()

    def override_get_repo() -> EventTypeRepository:
        return fake_repo

    application.dependency_overrides[get_repo_dep] = override_get_repo
    return application


@pytest.fixture
def app_with_bookings(
    fake_repo: FakeEventTypeRepository,
    fake_booking_repo: FakeBookingRepository,
) -> FastAPI:
    application = create_app()

    def override_get_repo() -> EventTypeRepository:
        return fake_repo

    def override_get_booking() -> BookingRepository:
        return fake_booking_repo

    application.dependency_overrides[get_repo_dep] = override_get_repo
    application.dependency_overrides[get_booking_dep] = override_get_booking
    return application


@pytest.fixture
def client_with_bookings(
    app_with_bookings: FastAPI,
) -> Generator[TestClient, Any, None]:
    with TestClient(app_with_bookings, raise_server_exceptions=False) as c:
        yield c


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


class TestGetSlots:
    def test_not_found(
        self, client_with_bookings: TestClient
    ) -> None:
        resp = client_with_bookings.get("/event-types/999/slots")
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "event_type_not_found"

    def test_returns_slots_for_event_type(
        self,
        client_with_bookings: TestClient,
        fake_repo: FakeEventTypeRepository,
    ) -> None:
        fake_repo.create(title="30min", description="desc", duration_minutes=30)
        resp = client_with_bookings.get("/event-types/1/slots")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) > 0
        slot = data[0]
        assert "start" in slot
        assert "end" in slot
        assert slot["status"] in ("free", "busy")

    def test_slot_step_equals_duration(
        self,
        client_with_bookings: TestClient,
        fake_repo: FakeEventTypeRepository,
    ) -> None:
        fake_repo.create(title="15min", description="desc", duration_minutes=15)
        resp = client_with_bookings.get("/event-types/1/slots")
        assert resp.status_code == 200
        data = resp.json()
        if len(data) > 1:
            start0 = datetime.fromisoformat(data[0]["start"])
            start1 = datetime.fromisoformat(data[1]["start"])
            diff = (start1 - start0).total_seconds()
            assert diff == 15 * 60

    def test_slots_only_on_weekdays(
        self,
        client_with_bookings: TestClient,
        fake_repo: FakeEventTypeRepository,
    ) -> None:
        fake_repo.create(title="60min", description="desc", duration_minutes=60)
        resp = client_with_bookings.get("/event-types/1/slots")
        assert resp.status_code == 200
        data = resp.json()
        for slot in data:
            start = datetime.fromisoformat(slot["start"])
            assert start.weekday() < 5

    def test_slots_within_working_hours(
        self,
        client_with_bookings: TestClient,
        fake_repo: FakeEventTypeRepository,
    ) -> None:
        fake_repo.create(title="30min", description="desc", duration_minutes=30)
        resp = client_with_bookings.get("/event-types/1/slots")
        assert resp.status_code == 200
        data = resp.json()
        for slot in data:
            start = datetime.fromisoformat(slot["start"])
            end = datetime.fromisoformat(slot["end"])
            assert start.hour >= 9
            assert end.hour <= 17 or (end.hour == 17 and end.minute == 0)

    def test_booking_marks_slot_busy(
        self,
        client_with_bookings: TestClient,
        fake_repo: FakeEventTypeRepository,
        fake_booking_repo: FakeBookingRepository,
    ) -> None:
        fake_repo.create(title="60min", description="desc", duration_minutes=60)
        msk = ZoneInfo("Europe/Moscow")
        monday = _next_weekday(datetime.now(msk).date(), 0)
        slot_start = datetime(monday.year, monday.month, monday.day, 9, 0, tzinfo=msk)
        slot_end = slot_start + timedelta(hours=1)
        fake_booking_repo.create(
            Booking(
                id=0,
                event_type_id=1,
                event_type_title="Booking",
                duration_minutes=60,
                start=slot_start,
                end=slot_end,
                guest_name="Test",
                guest_email="test@test.com",
            )
        )

        resp = client_with_bookings.get(
            "/event-types/1/slots",
            params={"from": monday.isoformat(), "to": (monday + timedelta(days=1)).isoformat()},
        )
        assert resp.status_code == 200
        data = resp.json()
        busy_slots = [s for s in data if s["status"] == "busy"]
        assert len(busy_slots) > 0


def _next_weekday(d: date, target_weekday: int) -> date:
    days_ahead = target_weekday - d.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return d + timedelta(days=days_ahead)
