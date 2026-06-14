from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Service"])


class HealthStatus(BaseModel):
    status: str


@router.get("/health")
def check() -> HealthStatus:
    """Проверка живости сервиса (используется healthcheck в docker compose)."""
    return HealthStatus(status="ok")
