from disnake import Embed, Member
from disnake.interactions import AppCmdInter
from disnake.ext.commands import Cog, Bot, slash_command

from eco.models import User
from eco.database import Session


class Balance(Cog):
    @slash_command()
    async def balance(self, inter: AppCmdInter, member: Member) -> None:
        async with Session() as session:
            user = await User.get_or_create(session, member.id)

        embed = Embed(
            title=f"{member.display_name}'s balance",
            description=f"{self.describe_balance(user.balance)}\n```\n{user.balance_str}```",
            color=member.accent_color,
        )
        embed.set_author(name=member.display_name, icon_url=member.display_avatar)
        await inter.send(embed=embed)

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