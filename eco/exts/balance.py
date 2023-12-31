"""Loads the Balance cog."""

from disnake import Embed, Member, User
from disnake.ext.commands import Bot, Cog, Param, slash_command
from disnake.interactions import AppCmdInter

from common.database import SessionLocal
from common.models import Account
from common.utils import error, format_money, success


class Balance(Cog):
    """Commands for managing balance."""

    @slash_command()
    async def balance(
        self,
        inter: AppCmdInter,
        user: User
        | Member
        | None = Param(
            description="The user to check the balance of. If not specified, it's you.",
            default=None,
        ),
    ) -> None:
        """Check the balance of a user."""
        if user is None:
            user = inter.author

        async with SessionLocal() as session:
            account = await Account.get_or_create(session, user.id)

        embed = Embed(
            title=f"{user.display_name}'s balance",
            description=(
                f"{self.describe_balance(account.balance)}\n"
                f"```\n{account.balance_fmt}```"
            ),
            color=user.accent_color,
        )
        embed.set_author(name=user.display_name, icon_url=user.display_avatar)
        await inter.send(embed=embed)

    @slash_command()
    async def give(
        self,
        inter: AppCmdInter,
        user: User = Param(description="The lucky user"),
        amount: float = Param(description="The amount of money to give them"),
    ) -> None:
        """Give someone some money."""
        if inter.author == user:
            await error(inter, "To yourself?")
            return

        if amount < 0.0:
            await error(inter, "Negative amount?")
            return

        if amount == 0.0:
            await success(
                inter,
                f"{inter.author.mention} gives {user.mention} ABSOLUTELY NOTHING."
                " Good job!",
            )
            return

        async with SessionLocal() as session:
            from_ = await Account.get_or_create(session, inter.author.id)
            to = await Account.get_or_create(session, user.id)

            if amount > from_.balance:
                await error(inter, "You're too broke for this")
                return

            from_.balance = Account.balance - amount
            to.balance = Account.balance + amount
            await session.commit()

        await success(
            inter,
            f"{inter.author.mention} gives {user.mention} `{format_money(amount)}`",
        )

    @staticmethod
    def describe_balance(balance: float) -> str:
        """Describe a balance."""
        if balance < 50.0:
            return "Broke"
        elif balance < 100.0:
            return "Broke but cooler"
        elif balance < 500.0:
            return "I guess"
        elif balance < 1000.0:
            return "Okay, I guess"
        elif balance < 5000.0:
            return "Good"
        else:
            return "Nice"


def setup(bot: Bot) -> None:
    """Load the Balance cog."""
    bot.add_cog(Balance())
