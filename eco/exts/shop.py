from typing import Sequence

from disnake import Embed
from disnake.ext.commands import Bot, Cog, Param, slash_command
from disnake.interactions import AppCmdInter
from sqlalchemy import select

from common.database import SessionLocal
from common.models import ShopItem, User, UserInventory
from common.utils import error, format_money, success


class Shop(Cog):
    @slash_command()
    async def shop(self, inter: AppCmdInter) -> None:
        """Show the shop items."""

        embed = Embed(title="Shop", description="Stuff we're selling")

        async with SessionLocal() as session:
            for item in await ShopItem.all(session):
                embed.add_field(
                    f"{item.id} - {item.name}",
                    f"`{format_money(item.price)}` - {item.description}",
                )

        await inter.send(embed=embed)

    @slash_command()
    async def buy(
        self,
        inter: AppCmdInter,
        id_: int = Param(name="id", description="The ID of the item"),
        quantity: int = Param(description="The quantity of the item", default=1, ge=1),
    ) -> None:
        """Buy a shop item."""

        async with SessionLocal() as session:
            user = await User.get_or_create(session, inter.author.id)
            item = await session.get(ShopItem, id_)
            if item is None:
                await error(inter, "Invalid item ID")
                return

            if item.price * quantity > user.balance:
                await error(inter, "You're too broke for this item")
                return

            for _ in range(quantity):
                user.balance = User.balance - item.price * quantity
                session.add(UserInventory(user_id=user.id, item_id=item.id))

            await session.commit()

        await success(
            inter,
            f"You've bought {quantity}x _{item.name}_ for"
            f" `{format_money(item.price * quantity)}`",
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
