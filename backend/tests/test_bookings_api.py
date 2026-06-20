"""Unit-тесты HTTP-слоя bookings с фейковыми репозиториями."""

from collections.abc import Generator
from datetime import datetime, timedelta
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

MSK = ZoneInfo("Europe/Moscow")


@pytest.fixture
def fake_repo() -> FakeEventTypeRepository:
    return FakeEventTypeRepository()


@pytest.fixture
def fake_booking_repo() -> FakeBookingRepository:
    return FakeBookingRepository()


@pytest.fixture
def app(
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
def client(app: FastAPI) -> Generator[TestClient, Any, None]:
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


def _next_weekday(d: datetime, target_weekday: int) -> datetime:
    days_ahead = target_weekday - d.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return d + timedelta(days=days_ahead)


def _valid_slot_start(minutes_offset: int = 60) -> datetime:
    now = datetime.now(MSK)
    next_monday = _next_weekday(now, 0)
    return next_monday.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(
        minutes=minutes_offset
    )


class TestCreateBooking:
    def test_creates_booking(self, client: TestClient, fake_repo: FakeEventTypeRepository) -> None:
        fake_repo.create(title="Meeting", description="desc", duration_minutes=60)
        start = _valid_slot_start(0)

        resp = client.post(
            "/bookings",
            json={
                "eventTypeId": 1,
                "start": start.isoformat(),
                "guestName": "John",
                "guestEmail": "john@test.com",
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["eventTypeId"] == 1
        assert data["guestName"] == "John"
        assert data["guestEmail"] == "john@test.com"
        assert "id" in data
        assert "createdAt" in data

    def test_not_found(self, client: TestClient) -> None:
        start = _valid_slot_start(0)
        resp = client.post(
            "/bookings",
            json={
                "eventTypeId": 999,
                "start": start.isoformat(),
                "guestName": "John",
                "guestEmail": "john@test.com",
            },
        )
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "event_type_not_found"

    def test_returns_422_on_invalid_email(
        self, client: TestClient, fake_repo: FakeEventTypeRepository
    ) -> None:
        fake_repo.create(title="Meeting", description="desc", duration_minutes=60)
        start = _valid_slot_start(0)
        resp = client.post(
            "/bookings",
            json={
                "eventTypeId": 1,
                "start": start.isoformat(),
                "guestName": "John",
                "guestEmail": "not-an-email",
            },
        )
        assert resp.status_code == 422

    def test_returns_422_on_empty_guest_name(
        self, client: TestClient, fake_repo: FakeEventTypeRepository
    ) -> None:
        fake_repo.create(title="Meeting", description="desc", duration_minutes=60)
        start = _valid_slot_start(0)
        resp = client.post(
            "/bookings",
            json={
                "eventTypeId": 1,
                "start": start.isoformat(),
                "guestName": "",
                "guestEmail": "john@test.com",
            },
        )
        assert resp.status_code == 422

    def test_returns_422_on_outside_hours(
        self, client: TestClient, fake_repo: FakeEventTypeRepository
    ) -> None:
        fake_repo.create(title="Meeting", description="desc", duration_minutes=30)
        start = _valid_slot_start(0).replace(hour=18)  # outside 09-17

        resp = client.post(
            "/bookings",
            json={
                "eventTypeId": 1,
                "start": start.isoformat(),
                "guestName": "John",
                "guestEmail": "john@test.com",
            },
        )
        assert resp.status_code == 422

    def test_returns_422_on_weekend(
        self, client: TestClient, fake_repo: FakeEventTypeRepository
    ) -> None:
        fake_repo.create(title="Meeting", description="desc", duration_minutes=30)
        now = datetime.now(MSK)
        days_until_saturday = (5 - now.weekday()) % 7
        if days_until_saturday == 0:
            days_until_saturday = 7
        saturday = now + timedelta(days=days_until_saturday)
        start = saturday.replace(hour=10, minute=0, second=0, microsecond=0)

        resp = client.post(
            "/bookings",
            json={
                "eventTypeId": 1,
                "start": start.isoformat(),
                "guestName": "John",
                "guestEmail": "john@test.com",
            },
        )
        assert resp.status_code == 422

    def test_returns_422_on_not_aligned(
        self, client: TestClient, fake_repo: FakeEventTypeRepository
    ) -> None:
        fake_repo.create(title="Meeting", description="desc", duration_minutes=30)
        start = _valid_slot_start(5)  # 5 min offset, not aligned to 30min grid

        resp = client.post(
            "/bookings",
            json={
                "eventTypeId": 1,
                "start": start.isoformat(),
                "guestName": "John",
                "guestEmail": "john@test.com",
            },
        )
        assert resp.status_code == 422

    def test_returns_409_on_slot_busy(
        self,
        client: TestClient,
        fake_repo: FakeEventTypeRepository,
        fake_booking_repo: FakeBookingRepository,
    ) -> None:
        fake_repo.create(title="Meeting", description="desc", duration_minutes=60)
        start = _valid_slot_start(0)
        end = start + timedelta(hours=1)

        fake_booking_repo.create(
            Booking(
                id=0,
                event_type_id=1,
                event_type_title="Existing",
                duration_minutes=60,
                start=start,
                end=end,
                guest_name="Existing",
                guest_email="existing@test.com",
            )
        )

        resp = client.post(
            "/bookings",
            json={
                "eventTypeId": 1,
                "start": start.isoformat(),
                "guestName": "John",
                "guestEmail": "john@test.com",
            },
        )
        assert resp.status_code == 409
        data = resp.json()
        assert data["code"] == "slot_busy"


class TestListBookings:
    def test_empty_list(self, client: TestClient) -> None:
        resp = client.get("/bookings")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_returns_upcoming_bookings(
        self, client: TestClient, fake_booking_repo: FakeBookingRepository
    ) -> None:
        now = datetime.now(MSK)
        future = now + timedelta(days=7)
        fake_booking_repo.create(
            Booking(
                id=0,
                event_type_id=1,
                event_type_title="Future",
                duration_minutes=30,
                start=future,
                end=future + timedelta(minutes=30),
                guest_name="John",
                guest_email="john@test.com",
            )
        )
        resp = client.get("/bookings")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["eventTypeTitle"] == "Future"

    def test_skips_past_bookings(
        self, client: TestClient, fake_booking_repo: FakeBookingRepository
    ) -> None:
        now = datetime.now(MSK)
        past = now - timedelta(days=3)
        fake_booking_repo.create(
            Booking(
                id=0,
                event_type_id=1,
                event_type_title="Past",
                duration_minutes=30,
                start=past,
                end=past + timedelta(minutes=30),
                guest_name="John",
                guest_email="john@test.com",
            )
        )
        resp = client.get("/bookings")
        assert resp.status_code == 200
        assert resp.json() == []


class TestCancelBooking:
    def test_cancels_booking(
        self, client: TestClient, fake_booking_repo: FakeBookingRepository
    ) -> None:
        now = datetime.now(MSK)
        future = now + timedelta(days=7)
        fake_booking_repo.create(
            Booking(
                id=0,
                event_type_id=1,
                event_type_title="Test",
                duration_minutes=30,
                start=future,
                end=future + timedelta(minutes=30),
                guest_name="John",
                guest_email="john@test.com",
            )
        )
        resp = client.delete("/bookings/1")
        assert resp.status_code == 204
        assert fake_booking_repo.get_by_id(1) is None

    def test_not_found(self, client: TestClient) -> None:
        resp = client.delete("/bookings/999")
        assert resp.status_code == 404
        data = resp.json()
        assert data["code"] == "booking_not_found"
