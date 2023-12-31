"""Loads the ErrorHandler cog."""

from time import time

from disnake.ext.commands import Bot, Cog, CommandError, CommandOnCooldown
from disnake.interactions import AppCmdInter
from loguru import logger

from common.utils import error


class ErrorHandler(Cog):
    """A cog that handles errors that occur during slash command execution."""

    @Cog.listener()
    async def on_slash_command_error(
        self, inter: AppCmdInter, err: CommandError
    ) -> None:
        """Handle errors that occur during slash command execution."""
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
        """Build an internal error log message."""
        return f"""
An unknown error occurred. Please [report](https://github.com/interrrp/eco/issues) this,
attaching the following log and what you did to trigger it:

```
{err}
```
""".strip()


def setup(bot: Bot) -> None:
    """Load the ErrorHandler cog."""
    bot.add_cog(ErrorHandler(bot))
