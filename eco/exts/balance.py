from disnake import Embed, Member
from disnake.ext.commands import Bot, Cog, slash_command
from disnake.interactions import AppCmdInter

from eco.database import SessionLocal
from eco.models import User
from eco.utils import error, format_money, success


class Balance(Cog):
    @slash_command()
    async def balance(self, inter: AppCmdInter, member: Member) -> None:
        """Check the balance of a user."""

        async with SessionLocal() as session:
            user = await User.get_or_create(session, member.id)

        embed = Embed(
            title=f"{member.display_name}'s balance",
            description=f"{self.describe_balance(user.balance)}\n```\n{user.balance_str}```",
            color=member.accent_color,
        )
        embed.set_author(name=member.display_name, icon_url=member.display_avatar)
        await inter.send(embed=embed)

    @slash_command()
    async def give(self, inter: AppCmdInter, member: Member, amount: float) -> None:
        """Give someone some money."""

        if inter.author == member:
            await error(inter, "To yourself?")
            return

        if amount < 0.0:
            await error(inter, "Negative amount?")
            return

        if amount == 0.0:
            await success(
                inter,
                f"{inter.author.mention} gives {member.mention} ABSOLUTELY NOTHING."
                " Good job!",
            )
            return

        async with SessionLocal() as session:
            from_ = await User.get_or_create(session, inter.author.id)
            to = await User.get_or_create(session, member.id)

            if amount > from_.balance:
                await error(inter, "You're too broke for this")
                return

            from_.balance = User.balance - amount
            to.balance = User.balance + amount
            await session.commit()

        await success(
            inter,
            f"{inter.author.mention} gives {member.mention} `{format_money(amount)}`",
        )

    @staticmethod
    def describe_balance(balance: float) -> str:
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
    bot.add_cog(Balance())
