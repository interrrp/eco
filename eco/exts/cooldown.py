from disnake.ext.commands import Bot, Cog, CommandError, CommandOnCooldown
from disnake.interactions import AppCmdInter

from eco.utils import error


class Cooldown(Cog):
    @Cog.listener()
    async def on_slash_command_error(
        self, inter: AppCmdInter, err: CommandError
    ) -> None:
        if isinstance(err, CommandOnCooldown):
            await error(inter, str(err))
            return


def setup(bot: Bot) -> None:
    bot.add_cog(Cooldown(bot))
