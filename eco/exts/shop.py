from typing import Sequence

from disnake import Embed
from disnake.ext.commands import Bot, Cog, slash_command
from disnake.interactions import AppCmdInter
from sqlalchemy import select

from eco.database import SessionLocal
from eco.models import ShopItem, User, UserInventory
from eco.utils import error, format_money, success


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

        item_count: dict[ShopItem, int] = {}

        async with SessionLocal() as session:
            query = select(UserInventory).where(
                UserInventory.user_id == inter.author.id
            )
            items: Sequence[UserInventory] = (await session.scalars(query)).all()
            for item in items:
                if item.item not in item_count:
                    item_count[item.item] = 1
                    continue
                item_count[item.item] += 1

        for inv_item, count in item_count.items():
            embed.add_field(f"{count}x {inv_item.name}", inv_item.description)

        await inter.send(embed=embed)


def setup(bot: Bot) -> None:
    bot.add_cog(Shop())
