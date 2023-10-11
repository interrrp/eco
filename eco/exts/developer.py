from typing import Callable, Coroutine

import disnake
from disnake.ext.commands import (
    Bot,
    Cog,
    InvokableSlashCommand,
    Param,
    slash_command,
)
from disnake.interactions import AppCmdInter

from eco import models
from eco.database import SessionLocal
from eco.settings import settings
from eco.utils import format_money, success


def dev_slash_command(
    **kwargs,
) -> Callable[[Callable[..., Coroutine]], InvokableSlashCommand]:
    return slash_command(**kwargs, guild_ids=settings.test_guild_ids)


class Developer(Cog):
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


def setup(bot: Bot) -> None:
    bot.add_cog(Developer())
