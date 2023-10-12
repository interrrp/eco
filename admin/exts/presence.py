from disnake import Game, Status
from disnake.ext.commands import Bot, Cog

from common.utils import BotCog


class Presence(BotCog):
    @Cog.listener()
    async def on_ready(self) -> None:
        await self.bot.change_presence(
            activity=Game("with the users"), status=Status.idle
        )


def setup(bot: Bot) -> None:
    bot.add_cog(Presence(bot))
