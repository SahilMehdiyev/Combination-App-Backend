from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=False, extra="ignore"
    )

    app_name: str = "Combination App"
    app_version: str = "1.0.0"
    debug: bool = True

    database_url: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    test_database_url: Optional[str] = None

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    environment: str = "development"


@lru_cache()
def get_settings():
    return Settings()
