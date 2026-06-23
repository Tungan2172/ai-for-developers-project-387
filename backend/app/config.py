from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Конфигурация приложения из переменных окружения (12-factor)."""

    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env", extra="ignore")

    # Подключение к БД задаётся окружением, чтобы не хардкодить креды (см. .env.example).
    database_url: str = "postgresql+psycopg://scheduler:scheduler@localhost:5432/scheduler"

    # Профиль владельца — единственный, без авторизации. Сидируется в БД на этапе B1.
    owner_name: str = "owner"
    owner_title: str = "Host"
    owner_description: str = "Забронируйте встречу в удобное время."


def get_settings() -> Settings:
    return Settings()
