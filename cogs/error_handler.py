from __future__ import annotations
from typing import TYPE_CHECKING

import discord
import traceback
from discord.ext import commands
from discord import Interaction
from discord.app_commands import AppCommandError

if TYPE_CHECKING:
    from bot import ShaitanBot

class ErrorHandler(commands.Cog):

    def __init__(self, bot: ShaitanBot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: Exception) -> None:
        embed = discord.Embed(color=0xFE676E)

        traceback.print_exception(type(error), error, error.__traceback__)
        cm_error = f"An unknown error occurred, sorry"

        embed.description = cm_error
        await ctx.send(embed=embed, delete_after=30, ephemeral=True)
    
    async def on_app_command_error(self, interaction: Interaction, error: AppCommandError) -> None:
        """Handles errors for all application commands."""
        traceback.print_exception(type(error), error, error.__traceback__)

async def setup(bot: commands.Bot):
    await bot.add_cog(ErrorHandler(bot))