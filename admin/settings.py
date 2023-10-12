from common.settings import Settings


class AdminSettings(Settings):
    admin_token: str


settings = AdminSettings()  # type: ignore[call-arg]
