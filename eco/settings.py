from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    token: str
    sqlite_url: str = "sqlite+aiosqlite:///db.sqlite3"
    money_prefix: str = "$"


settings = Settings()  # type: ignore[call-arg]
