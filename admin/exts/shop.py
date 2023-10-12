from disnake.ext.commands import Bot, Cog, Param, slash_command
from disnake.interactions import AppCmdInter

from common.database import SessionLocal
from common.models import ShopItem
from common.utils import success


class Shop(Cog):
    @slash_command()
    async def shop(self, inter: AppCmdInter) -> None:
        pass

    @shop.sub_command()
    async def add(
        self,
        inter: AppCmdInter,
        name: str = Param(description="The name of the item"),
        description: str = Param(description="The description of the item"),
        price: float = Param(description="How much the item costs"),
    ) -> None:
        """Add an item to the shop."""

        async with SessionLocal() as session:
            session.add(ShopItem(name=name, description=description, price=price))
            await session.commit()

        await success(inter, f"Added `{name}` into the shop")


def setup(bot: Bot) -> None:
    bot.add_cog(Shop())
