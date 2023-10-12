import disnake
from disnake.ext.commands import Bot, Cog, Param, slash_command
from disnake.interactions import AppCmdInter

from common import models
from common.database import SessionLocal
from common.utils import error, format_money, success


class Money(Cog):
    @slash_command()
    async def money(self, inter: AppCmdInter) -> None:
        pass

    @money.sub_command()
    async def add(
        self,
        inter: AppCmdInter,
        user: disnake.User = Param(description="The user to give the money to"),
        amount: float = Param(description="The amount of money"),
    ) -> None:
        """Add money to a user."""

        if amount <= 0.0:
            await error(inter, "Amount must be more than zero")
            return

        async with SessionLocal() as session:
            user_data = await models.User.get_or_create(session, user.id)
            user_data.balance = models.User.balance + amount
            await session.commit()

        await success(inter, f"Added `{format_money(amount)}` into their account")

    @money.sub_command()
    async def subtract(
        self,
        inter: AppCmdInter,
        user: disnake.User = Param(description="The user to take the money from"),
        amount: float = Param(description="The amount of money"),
    ) -> None:
        """Subtract money from a user."""

        if amount <= 0.0:
            await error(inter, "Amount must be more than zero")
            return

        async with SessionLocal() as session:
            user_data = await models.User.get_or_create(session, user.id)
            if user_data.balance < amount:
                await error(inter, "User doesn't have enough money")
                return
            user_data.balance = models.User.balance - amount
            await session.commit()

        await success(inter, f"Subtracted `{format_money(amount)}` from their account")


def setup(bot: Bot) -> None:
    bot.add_cog(Money())
