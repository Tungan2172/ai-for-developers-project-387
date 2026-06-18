from fastapi import FastAPI

from app.api import event_types, health
from app.api.errors import register_error_handlers


def create_app() -> FastAPI:
    app = FastAPI(title="Meeting Scheduler API", version="0.1.0")
    register_error_handlers(app)
    app.include_router(health.router)
    app.include_router(event_types.router)
    return app


app = create_app()
