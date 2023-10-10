from random import random, uniform

from disnake import Member
from disnake.ext.commands import Bot, Cog, slash_command
from disnake.interactions import AppCmdInter

from eco.database import SessionLocal
from eco.models import User
from eco.utils import error, format_money, success


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

    @slash_command()
    async def rob(self, inter: AppCmdInter, victim: Member) -> None:
        """Rob a user."""

        if random() < 0.8:
            await error(
                inter,
                f"You got caught, and {victim.mention} ran away!",
                ephemeral=False,
            )
            return

        async with SessionLocal() as session:
            victim_data = await User.get_or_create(session, victim.id)
            robber_data = await User.get_or_create(session, inter.author.id)

            amount = victim_data.balance * 0.05

            victim_data.balance = User.balance - amount
            robber_data.balance = User.balance + amount

            await session.commit()

        await success(inter, f"You robbed {victim.mention} of `{format_money(amount)}`")


def setup(bot: Bot) -> None:
    bot.add_cog(Games())
