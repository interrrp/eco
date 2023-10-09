from disnake.ext.commands import Cog, Bot


class BotCog(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
