import asyncio

from disnake.ext.commands import InteractionBot
from loguru import logger

from eco.database import engine
from eco.models import Base
from eco.settings import settings


async def main() -> None:
    logger.info("Creating tables")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Finished creating tables")

    logger.info("Starting bot")
    bot = InteractionBot()
    bot.load_extensions("eco/exts")
    await bot.start(settings.token)


asyncio.run(main())
