import os
import discord
from discord.ext import commands

class ShaitanBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        super().__init__('/', case_insensitive=True, intents=intents)


async def run_bot(bot_token: str) -> None:
    bot = ShaitanBot()
    
    for file_name in os.listdir('./cogs'):
        if file_name.endswith('.py'):
            await bot.load_extension(f"cogs.{file_name[:-3]}")

    await bot.start(bot_token)
    