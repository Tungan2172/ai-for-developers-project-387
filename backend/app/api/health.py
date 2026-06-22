from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import text

from app.adapters.database import engine

router = APIRouter(tags=["Service"])


class HealthStatus(BaseModel):
    status: str
    database: str


@router.get("/health")
def check() -> HealthStatus:
    """Check service liveness and database connectivity."""
    db_ok = False
    try:
        with engine.connect() as c:
            c.execute(text("SELECT 1"))
            db_ok = True
    except Exception:
        pass
    return HealthStatus(
        status="ok" if db_ok else "degraded",
        database="connected" if db_ok else "unavailable",
    )
