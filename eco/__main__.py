import asyncio

from disnake.ext.commands import InteractionBot

from eco.settings import settings


async def main() -> None:
    bot = InteractionBot()
    bot.load_extensions("eco/exts")
    await bot.start(settings.token)


asyncio.run(main())
