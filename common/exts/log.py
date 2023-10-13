"""Loads the Log cog."""

from disnake.ext.commands import Bot, Cog
from loguru import logger

from common.utils import BotCog


class Log(BotCog):
    """Cog that logs certain events."""

    @Cog.listener()
    async def on_ready(self) -> None:
        """Log that the bot is ready."""
        logger.info(f"Ready as {self.bot.user}")


def setup(bot: Bot) -> None:
    """Load the Log cog."""
    bot.add_cog(Log(bot))
