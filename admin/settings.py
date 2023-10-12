from common.settings import Settings


class AdminSettings(Settings):
    admin_token: str
    admin_guild_ids: list[int]


settings = AdminSettings()  # type: ignore[call-arg]
