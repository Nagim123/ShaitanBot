import discord
from discord.ext import commands

class ShaitanBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__('/', case_insensitive=True, intents=intents)


async def run_bot(bot_token: str) -> None:
    bot = ShaitanBot()
    await bot.load_extension("cogs.fun_service")
    await bot.start(bot_token)
    