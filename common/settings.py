"""Contains the Settings class.

A global instance of this class is available (settings) and should be used instead of
manually instantiating one.
"""

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """The main settings class."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    test_guild_ids: list[int] | None = None
    database_url: PostgresDsn = PostgresDsn(
        "postgresql+asyncpg://postgres:postgres@localhost/eco"
    )
    money_prefix: str = "$"


settings = Settings()  # type: ignore[call-arg]
