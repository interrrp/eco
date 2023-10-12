from disnake.ext.commands import Bot, Cog
from loguru import logger

from admin.settings import settings
from common.utils import BotCog


class AdminGuilds(BotCog):
    @Cog.listener()
    async def on_ready(self) -> None:
        num_guilds_left = 0

        for guild in self.bot.guilds:
            if guild.id not in settings.admin_guild_ids:
                await guild.leave()
                num_guilds_left += 1

        if num_guilds_left > 0:
            logger.warning(
                f"Left {num_guilds_left} non-admin guild(s). This means that someone"
                " knows about the admin bot - please investigate!"
            )

    @Cog.listener()
    async def on_guild_join(self, guild) -> None:
        if guild.id not in settings.admin_guild_ids:
            await guild.leave()
            logger.warning(
                f"Left guild {guild.name} ({guild.id}) because it is not an admin"
                " guild. This means that someone knows about the admin bot - please"
                " investigate!"
            )


def setup(bot: Bot) -> None:
    bot.add_cog(AdminGuilds(bot))
