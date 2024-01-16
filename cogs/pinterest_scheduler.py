from __future__ import annotations
from typing import TYPE_CHECKING

from discord.ext import commands
from random import random

if TYPE_CHECKING:
    from bot import ShaitanBot

class PinterestScheduler(commands.Cog):

    def __init__(self, bot: ShaitanBot) -> None:
        self.bot = bot
    
    @commands.command()
    async def add_pin_board(self, ctx: commands.Context) -> None:
        pass

    @commands.command()
    async def remove_pin_board(self, ctx: commands.Context) -> None:
        pass

    @commands.command()
    async def show_schedule(self, ctx: commands.Context) -> None:
        pass

    @commands.command()
    async def change_scheduling(self, ctx: commands.Context) -> None:
        pass
    
    @commands.command()
    async def change_send_time(self, ctx: commands.Context) -> None:
        pass

async def setup(bot: commands.Bot):
    await bot.add_cog(PinterestScheduler(bot))