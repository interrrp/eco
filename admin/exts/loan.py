from typing import Sequence

from disnake import Embed
from disnake.ext.commands import Bot, Param, slash_command
from disnake.interactions import AppCmdInter
from sqlalchemy import select

from common import models
from common.database import SessionLocal
from common.models import LoanRequest
from common.utils import BotCog, error, format_money, success


class Loan(BotCog):
    @slash_command()
    async def loan(self, inter: AppCmdInter) -> None:
        pass

    @loan.sub_command()
    async def list(self, inter: AppCmdInter) -> None:
        """List all pending loan requests."""

        embed = Embed(title="Pending loan requests")

        async with SessionLocal() as session:
            query = select(LoanRequest)
            requests: Sequence[LoanRequest] = (await session.scalars(query)).all()
            for req in requests:
                embed.add_field(
                    f"{req.id} - {format_money(req.amount)} - {req.user_id}",
                    req.application,
                )

        await inter.send(embed=embed)

    @loan.sub_command()
    async def approve(
        self,
        inter: AppCmdInter,
        id_: int = Param(name="id", description="The ID of the loan request"),
    ) -> None:
        """Approve a loan request."""

        async with SessionLocal() as session:
            request = await session.get(models.LoanRequest, id_)
            if request is None:
                await error(inter, "Invalid loan ID")
                return

            await request.approve(session)

        # FIXME: The main bot should send this DM, not the admin bot
        user = await self.bot.fetch_user(request.user_id)
        await user.send(
            f"🎉 Your loan for `{format_money(request.amount)}` got approved!"
        )

        await success(
            inter, f"Approved loan `{id_}` for `{format_money(request.amount)}`"
        )

    @loan.sub_command()
    async def reject(
        self,
        inter: AppCmdInter,
        id_: int = Param(name="id", description="The ID of the loan request"),
    ) -> None:
        """Reject a loan request."""

        async with SessionLocal() as session:
            request = await session.get(models.LoanRequest, id_)
            if request is None:
                await error(inter, "Invalid loan ID")
                return

            await request.reject(session)

        # FIXME: The main bot should send this DM, not the admin bot
        user = await self.bot.fetch_user(request.user_id)
        await user.send(
            f"😭 Your loan for `{format_money(request.amount)}` got rejected."
        )

        await success(
            inter, f"Rejected loan `{id_}` for `{format_money(request.amount)}`"
        )


def setup(bot: Bot) -> None:
    bot.add_cog(Loan(bot))
