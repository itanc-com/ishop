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
    # Safe defaults for direct Postgres. Flip the PgBouncer-aware knobs
    # when pointing at a transaction-pool (e.g. Supabase 6543).
    db_pool_pre_ping: bool = True
    db_pool_recycle: int = 1800
    db_use_null_pool: bool = False
    db_statement_cache_size: int | None = None  # set to 0 for PgBouncer tx mode
    db_ssl: str | None = None  # e.g. "require" for Supabase
    db_application_name: str = "ishop-api"
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
