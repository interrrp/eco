from disnake import Game, Status
from disnake.ext.commands import Cog, Bot

from eco.utils import BotCog


class Presence(BotCog):
    @Cog.listener()
    async def on_ready(self) -> None:
        await self.bot.change_presence(
            activity=Game("with the economy"), status=Status.idle
        )


def setup(bot: Bot) -> None:
    bot.add_cog(Presence(bot))
