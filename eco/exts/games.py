"""Games to earn money."""

from random import random, uniform

from disnake import User
from disnake.ext.commands import Bot, BucketType, Cog, Param, cooldown, slash_command
from disnake.interactions import AppCmdInter

from common.database import SessionLocal
from common.models import Account
from common.utils import error, format_money, success


class Games(Cog):
    """Commands for playing games."""

    @slash_command()
    @cooldown(1, 30, BucketType.user)
    async def fish(self, inter: AppCmdInter) -> None:
        """Fish and earn money. A small amount of money, but it's money after all."""
        if random() < 0.3:
            await error(inter, "No luck...", ephemeral=False)
            return

        amount = uniform(1.0, 4.0)
        async with SessionLocal() as session:
            account = await Account.get_or_create(session, inter.author.id)
            account.balance = Account.balance + amount
            await session.commit()

        await success(inter, f"You fished and earned `{format_money(amount)}`")

    @slash_command()
    async def rob(
        self,
        inter: AppCmdInter,
        victim: User = Param(description="The unlucky user"),
    ) -> None:
        """Rob a user."""
        if inter.author == victim:
            await error(inter, "You can't rob yourself...")
            return

        if random() < 0.8:
            await error(
                inter,
                f"You got caught, and {victim.mention} ran away!",
                ephemeral=False,
            )
            return

        async with SessionLocal() as session:
            victim_account = await Account.get_or_create(session, victim.id)
            robber_account = await Account.get_or_create(session, inter.author.id)

            amount = victim_account.balance * 0.05

            victim_account.balance = Account.balance - amount
            robber_account.balance = Account.balance + amount

            await session.commit()

        await success(inter, f"You robbed {victim.mention} of `{format_money(amount)}`")


def setup(bot: Bot) -> None:
    """Load the Games cog."""
    bot.add_cog(Games())
