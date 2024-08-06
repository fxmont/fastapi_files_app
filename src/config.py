import os

from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

SQLITE_DATABASE_URL = "sqlite:///sqlitedb.db"

upload_dir_path = "./uploads"
os.makedirs(upload_dir_path, exist_ok=True)


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env.dev`
        env_file=("src/.env.dev", "src/.env.prod"),
        env_file_encoding="utf-8",
        # env_prefix='very_secret_', # this prefix should be set to env vars
        # extra=forbid - will raise an error, if var from .env doesn't defined in model
        # extra='ignore'
    )

    DB_HOST: str
    DB_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DATABASE_URL: PostgresDsn | None = None
    DATABASE_ASYNC_URL: PostgresDsn | None = None
    S3_ACCESS_KEY: str
    S3_SECRET_ACCESS_KEY: str
    S3_STORAGE_ACTIVE: bool
    # DATABASE_URL=postgresql://app:app@localhost:5432/app
    # DATABASE_ASYNC_URL=postgresql+asyncpg://app:app@localhost:5432/app

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def build_db_url(cls, v, values):
        return v or PostgresDsn.build(
            scheme="postgresql",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("DB_HOST"),
            port=values.data.get("DB_PORT"),
            path=f"{values.data.get('POSTGRES_DB') or ''}",
        )

    @field_validator("DATABASE_ASYNC_URL", mode="before")
    @classmethod
    def build_db_async_url(cls, v, values):
        return v or PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("DB_HOST"),
            port=values.data.get("DB_PORT"),
            path=f"{values.data.get('POSTGRES_DB') or ''}",
        )


settings = Config()
