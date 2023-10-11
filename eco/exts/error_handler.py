from time import time

from disnake.ext.commands import Bot, Cog, CommandError, CommandOnCooldown
from disnake.interactions import AppCmdInter
from loguru import logger

from eco.utils import error


class ErrorHandler(Cog):
    @Cog.listener()
    async def on_slash_command_error(
        self, inter: AppCmdInter, err: CommandError
    ) -> None:
        if isinstance(err, CommandOnCooldown):
            await error(
                inter,
                f"Slow down buddy, you're on cooldown. Try again"
                f" <t:{round(time() + err.retry_after)}:R>",
            )
        else:
            logger.error(err)
            await error(
                inter,
                self.build_internal_error_log(err),
            )

    @staticmethod
    def build_internal_error_log(err: CommandError) -> str:
        return f"""
An unknown error occurred. Please [report](https://github.com/interrrp/eco/issues) this,
attaching the following log and what you did to trigger it:
```
{err}
```
""".strip()


def setup(bot: Bot) -> None:
    bot.add_cog(ErrorHandler(bot))
