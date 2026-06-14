from fastapi import FastAPI

from app.api import health


def create_app() -> FastAPI:
    """Фабрика приложения: упрощает создание изолированных экземпляров в тестах."""
    app = FastAPI(title="Meeting Scheduler API", version="0.1.0")
    app.include_router(health.router)
    return app


app = create_app()
