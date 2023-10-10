from typing import Sequence

from sqlalchemy import select
from disnake import Embed
from disnake.interactions import AppCmdInter
from disnake.ext.commands import Cog, Bot, slash_command

from eco.utils import format_money, error, success
from eco.database import SessionLocal
from eco.models import ShopItem, User, UserInventory


class Shop(Cog):
    @slash_command()
    async def shop(self, inter: AppCmdInter) -> None:
        """Show the shop items."""

        embed = Embed(title="Shop", description="Stuff we're selling")

        async with SessionLocal() as session:
            items: Sequence[ShopItem] = (await session.scalars(select(ShopItem))).all()
            for item in items:
                embed.add_field(
                    f"{item.id} - {item.name}",
                    f"`{format_money(item.price)}` - {item.description}",
                )

        await inter.send(embed=embed)

    @slash_command()
    async def buy(self, inter: AppCmdInter, id_: int) -> None:
        """Buy a shop item."""

        async with SessionLocal() as session:
            user = await User.get_or_create(session, inter.author.id)
            item = await session.get(ShopItem, id_)
            if item is None:
                await error(inter, "Invalid item ID")
                return

            user.balance = User.balance - item.price

            session.add(UserInventory(user_id=user.id, item_id=item.id))

            await session.commit()

        await success(
            inter, f"You've bought _{item.name}_ for `{format_money(item.price)}`"
        )

    @slash_command()
    async def inventory(self, inter: AppCmdInter) -> None:
        """Show your inventory."""

        embed = Embed(title="Your inventory")
        embed.set_author(
            name=inter.author.display_name, icon_url=inter.author.display_avatar
        )

        async with SessionLocal() as session:
            query = select(UserInventory).where(
                UserInventory.user_id == inter.author.id
            )
            items: Sequence[UserInventory] = (await session.scalars(query)).all()
            for item in items:
                embed.add_field(item.item.name, item.item.description)

        await inter.send(embed=embed)


def setup(bot: Bot) -> None:
    bot.add_cog(Shop())