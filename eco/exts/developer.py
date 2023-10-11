import disnake
from disnake.ext.commands import Bot, Cog, Param, is_owner, slash_command
from disnake.interactions import AppCmdInter

from eco import models
from eco.database import SessionLocal
from eco.utils import format_money, success


class Developer(Cog):
    @slash_command()
    @is_owner()
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


def setup(bot: Bot) -> None:
    bot.add_cog(Developer())
