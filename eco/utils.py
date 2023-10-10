from disnake import Embed, Color
from disnake.interactions import AppCmdInter
from disnake.ext.commands import Cog, Bot

from eco.settings import settings


class BotCog(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot


def format_money(money: float) -> str:
    return f"{settings.money_prefix}{money:.2f}"


async def error(inter: AppCmdInter, message: str, ephemeral: bool = True) -> None:
    await inter.send(
        embed=Embed(description=f"🙅‍♂️ {message}", color=Color.red()),
        ephemeral=ephemeral,
    )


async def success(inter: AppCmdInter, message: str) -> None:
    await inter.send(embed=Embed(description=f"👍 {message}", color=Color.green()))
