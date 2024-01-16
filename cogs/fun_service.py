from __future__ import annotations
from typing import TYPE_CHECKING

from discord.ext import commands
from random import random

if TYPE_CHECKING:
    from bot import ShaitanBot

class FunService(commands.Cog):

    def __init__(self, bot: ShaitanBot) -> None:
        self.bot = bot
    
    @commands.command()
    async def question(self, ctx: commands.Context) -> None:
        if random() > 0.5:
            await ctx.reply("Да")
        else:
            await ctx.reply("Нет")

async def setup(bot: commands.Bot):
    await bot.add_cog(FunService(bot))