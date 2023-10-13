"""Contains the main settings class.

A global instance of this class is available (settings) and should be used instead of
manually instantiating one.
"""

from common.settings import Settings


class AdminSettings(Settings):
    """An extension of the common settings class for main bot settings."""

    token: str


settings = AdminSettings()  # type: ignore[call-arg]
