from enum import Enum
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    LOCAL = "local"
    TESTING = "testing"


class Settings(BaseSettings):
    database_uri: str
    environment: EnvironmentType
    echo_sql: bool = False
    jwt_issuer_server: str
    jwt_secret_key: str

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file="./app/.env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()  # use this singleton in your app
