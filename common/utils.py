"""Various utilities for the bot."""

from disnake import Embed
from disnake.ext.commands import Bot, Cog
from disnake.interactions import AppCmdInter

from common.colors import GREEN, RED
from common.settings import settings


class BotCog(Cog):
    """A cog that is passed the bot instance."""

    def __init__(self, bot: Bot) -> None:
        """Initialize the cog."""
        self.bot = bot


def format_money(money: float) -> str:
    """Format money into a string.

    This uses the money_prefix setting.
    """
    return f"{settings.money_prefix}{money:,.2f}"


async def error(inter: AppCmdInter, message: str, ephemeral: bool = True) -> None:
    """Send an error message.

    This sends an embed with a red color and a cross emoji.
    """
    await inter.send(
        embed=Embed(description=f"🙅‍♂️ {message}", color=RED),
        ephemeral=ephemeral,
    )


async def success(inter: AppCmdInter, message: str) -> None:
    """Send a success message.

    This sends an embed with a green color and a check emoji.
    """
    await inter.send(embed=Embed(description=f"👍 {message}", color=GREEN))
