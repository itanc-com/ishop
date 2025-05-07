from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_uri: str
    environment: str
    jwt_issuer_server: str
    jwt_secret_key: str
   
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file='./app/.env',
        env_file_encoding="utf-8",
    )


settings: Settings = Settings()
