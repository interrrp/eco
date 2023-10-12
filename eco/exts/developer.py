from typing import Callable, Coroutine, Sequence

import disnake
from disnake import Embed
from disnake.ext.commands import (
    Bot,
    InvokableSlashCommand,
    Param,
    slash_command,
)
from disnake.interactions import AppCmdInter
from sqlalchemy import select

from eco import models
from eco.database import SessionLocal
from eco.settings import settings
from eco.utils import BotCog, error, format_money, success


def dev_slash_command(
    **kwargs,
) -> Callable[[Callable[..., Coroutine]], InvokableSlashCommand]:
    return slash_command(**kwargs, guild_ids=settings.test_guild_ids)


class Developer(BotCog):
    @dev_slash_command()
    async def print_money(
        self,
        inter: AppCmdInter,
        user: disnake.User = Param(description="The user to give the printed money to"),
        amount: float = Param(description="The amount of money to print"),
    ) -> None:
        """Print some money. This is clearly illegal."""

        async with SessionLocal() as session:
            user_data = await models.User.get_or_create(session, user.id)
            user_data.balance = models.User.balance + amount
            await session.commit()

        await success(
            inter,
            f"You illegally printed `{format_money(amount)}` and gave it to"
            f" {user.mention}. Good job, you criminal.",
        )

    @dev_slash_command()
    async def create_shop_item(
        self,
        inter: AppCmdInter,
        name: str = Param(description="The name of the item"),
        description: str = Param(description="The description of the item"),
        price: float = Param(description="How much the item costs"),
    ):
        """Create a shop item."""

        async with SessionLocal() as session:
            session.add(
                models.ShopItem(name=name, description=description, price=price)
            )
            await session.commit()

        await success(inter, f"Put up _{name}_ for `{format_money(price)}` on the shop")

    @dev_slash_command()
    async def approve_loan(
        self,
        inter: AppCmdInter,
        id_: int = Param(name="id", description="The ID of the loan"),
    ) -> None:
        """Approve a loan."""

        async with SessionLocal() as session:
            request = await session.get(models.LoanRequest, id_)
            if request is None:
                await error(inter, "Invalid loan ID")
                return

            await request.approve(session)

        user = await self.bot.fetch_user(request.user_id)
        await user.send(
            f"🎉 Your loan for `{format_money(request.amount)}` got approved!"
        )

        await success(
            inter, f"Approved loan `{id_}` for `{format_money(request.amount)}`"
        )

    @dev_slash_command()
    async def reject_loan(
        self,
        inter: AppCmdInter,
        id_: int = Param(name="id", description="The ID of the loan"),
    ) -> None:
        """Reject a loan."""

        async with SessionLocal() as session:
            request = await session.get(models.LoanRequest, id_)
            if request is None:
                await error(inter, "Invalid loan ID")
                return

            await request.reject(session)

        user = await self.bot.fetch_user(request.user_id)
        await user.send(
            f"😭 Your loan for `{format_money(request.amount)}` got rejected."
        )

        await success(
            inter, f"Rejected loan `{id_}` for `{format_money(request.amount)}`"
        )

    @dev_slash_command()
    async def all_pending_loans(self, inter: AppCmdInter) -> None:
        """List all pending loans."""

        embed = Embed(title="All pending loans")

        async with SessionLocal() as session:
            loans: Sequence[models.LoanRequest] = (
                await session.scalars(select(models.LoanRequest))
            ).all()
            for loan in loans:
                embed.add_field(
                    f"{loan.id} - {format_money(loan.amount)} - {loan.user_id}",
                    loan.application,
                )

        await inter.send(embed=embed)


def setup(bot: Bot) -> None:
    bot.add_cog(Developer(bot))
