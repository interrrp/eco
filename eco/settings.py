from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    token: str
    test_guild_ids: list[int] | None = None
    database_url: PostgresDsn = PostgresDsn(
        "postgresql+asyncpg://postgres:postgres@localhost/eco"
    )
    money_prefix: str = "$"


settings = Settings()  # type: ignore[call-arg]
