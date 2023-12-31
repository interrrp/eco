"""Loads the Loan cog."""

from typing import Sequence

from disnake import Embed
from disnake.ext.commands import Bot, Cog, Param, slash_command
from disnake.interactions import AppCmdInter
from disnake.utils import escape_markdown
from sqlalchemy import select

from common.database import SessionLocal
from common.models import Account, LoanRequest
from common.utils import format_money, success


class Loan(Cog):
    """Commands for managing loan requests."""

    @slash_command()
    async def loan(self, inter: AppCmdInter) -> None:
        """Manage loan requests."""
        pass

    @loan.sub_command()
    async def show(self, inter: AppCmdInter) -> None:
        """Show all your pending loan requests."""
        embed = Embed(
            title="Your pending loan requests", color=inter.author.accent_color
        )
        embed.set_author(
            name=inter.author.display_name, icon_url=inter.author.display_avatar
        )

        async with SessionLocal() as session:
            await Account.get_or_create(session, inter.author.id)

            query = select(LoanRequest).where(LoanRequest.user_id == inter.author.id)
            requests: Sequence[LoanRequest] = (await session.scalars(query)).all()

            for request in requests:
                embed.add_field(
                    f"Request for `{format_money(request.amount)}`",
                    f"{escape_markdown(request.application)[:50]}...",
                )

        await inter.send(embed=embed)

    @loan.sub_command()
    async def request(
        self,
        inter: AppCmdInter,
        amount: int = Param(description="How much you're requesting"),
        application: str = Param(description="The application for your request"),
    ) -> None:
        """Request a loan."""
        async with SessionLocal() as session:
            session.add(
                LoanRequest(
                    user_id=inter.author.id, amount=amount, application=application
                )
            )
            await session.commit()

        await success(
            inter,
            f"You asked for a loan of `{format_money(amount)}`\n```\n{application}```",
        )


def setup(bot: Bot) -> None:
    """Load the Loan cog."""
    bot.add_cog(Loan())
