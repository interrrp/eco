"""The entrypoint."""

import asyncio

from disnake import AllowedMentions, Game, Status
from disnake.ext.commands import InteractionBot
from loguru import logger

from admin.settings import settings
from common.models import create_tables


async def main() -> None:
    """Start the bot."""
    logger.info("Creating tables")
    await create_tables()
    logger.info("Finished creating tables")

    logger.info("Starting bot")
    bot = InteractionBot(
        activity=Game("with the users"),
        status=Status.idle,
        test_guilds=settings.test_guild_ids,
        allowed_mentions=AllowedMentions.none(),
    )
    bot.load_extensions("common/exts")
    bot.load_extensions("admin/exts")
    await bot.start(settings.admin_token)


if __name__ == "__main__":
    asyncio.run(main())
