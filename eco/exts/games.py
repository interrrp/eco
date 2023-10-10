from random import random, uniform

from disnake.interactions import AppCmdInter
from disnake.ext.commands import Cog, Bot, slash_command

from eco.utils import error, success, format_money
from eco.database import SessionLocal
from eco.models import User


class Games(Cog):
    @slash_command()
    async def fish(self, inter: AppCmdInter) -> None:
        """Fish and earn money. A small amount of money, but it's money after all."""

        if random() < 0.3:
            await error(inter, "No luck...")
            return

        amount = uniform(1.0, 4.0)
        async with SessionLocal() as session:
            user = await User.get_or_create(session, inter.author.id)
            user.balance = User.balance + amount
            await session.commit()

        await success(inter, f"You fished and earned `{format_money(amount)}`")


def setup(bot: Bot) -> None:
    bot.add_cog(Games())
