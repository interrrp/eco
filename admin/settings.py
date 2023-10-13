"""Contains the admin settings class.

A global instance of this class is available (settings) and should be used instead of
manually instantiating one.
"""

from common.settings import Settings


class AdminSettings(Settings):
    """An extension of the main settings class for admin settings."""

    admin_token: str
    admin_guild_ids: list[int]


settings = AdminSettings()  # type: ignore[call-arg]
