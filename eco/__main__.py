import asyncio

from disnake import AllowedMentions
from disnake.ext.commands import InteractionBot
from loguru import logger

from common.models import create_tables
from common.settings import settings


async def main() -> None:
    logger.info("Creating tables")
    await create_tables()
    logger.info("Finished creating tables")

    logger.info("Starting bot")
    bot = InteractionBot(
        test_guilds=settings.test_guild_ids, allowed_mentions=AllowedMentions.none()
    )
    bot.load_extensions("common/exts")
    bot.load_extensions("eco/exts")
    await bot.start(settings.token)


asyncio.run(main())
