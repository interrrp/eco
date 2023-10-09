from loguru import logger
from disnake.ext.commands import Cog, Bot

from eco.utils import BotCog


class Log(BotCog):
    @Cog.listener()
    async def on_ready(self) -> None:
        logger.info(f"Ready as {self.bot.user}")


def setup(bot: Bot) -> None:
    bot.add_cog(Log(bot))
