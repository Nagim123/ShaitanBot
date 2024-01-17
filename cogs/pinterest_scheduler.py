from __future__ import annotations
from typing import TYPE_CHECKING

import os

from discord.ext import commands
from random import random
from pinterest_board_parser.pinterest_board import PinterestBoard
from pin_scheduling.pinterest_board_scheduler import PinterestBoardScheduler
from config import Config

if TYPE_CHECKING:
    from bot import ShaitanBot

class PinterestScheduler(commands.Cog):
    def __init__(self, bot: ShaitanBot) -> None:
        self.bot = bot
        self.board_cache_folder_path = Config.data()["PINTEREST_BOARD_CACHE_FOLDER"]
        self.schedule_cache_folder_path = Config.data()["PINTEREST_BOARD_SCHEDULE_CACHE_FOLDER"]
        self.channel_schedules: dict[int, list[tuple[str, PinterestBoardScheduler]]] = dict()
    
    @commands.command()
    async def add_pin_board(self, ctx: commands.Context, board_owner: str, board_name: str) -> None:
        
        if os.path.exists(f"{self.schedule_cache_folder_path}/{ctx.channel.id}/{board_owner}_{board_name}"):
            await ctx.reply("Эта доска уже прикрепленна к текущему каналу")
            return
        
        board = PinterestBoard(board_owner, board_name, cache_file_path=f"{self.board_cache_folder_path}/{board_owner}_{board_name}")
        
        if ctx.channel.id in self.channel_schedules:
            scheduler = PinterestBoardScheduler(board, f"{self.schedule_cache_folder_path}/{ctx.channel.id}/{board_owner}_{board_name}")
            self.channel_schedules[ctx.channel.id].append((f"{board_owner}_{board_name}", scheduler))
        else:
            os.mkdir(f"{self.schedule_cache_folder_path}/{ctx.channel.id}")
            scheduler = PinterestBoardScheduler(board, f"{self.schedule_cache_folder_path}/{ctx.channel.id}/{board_owner}_{board_name}")
            self.channel_schedules[ctx.channel.id] = [(f"{board_owner}_{board_name}", scheduler)]
        
        await ctx.reply("Доска успешно добавлена!")

    @commands.command()
    async def remove_pin_board(self, ctx: commands.Context, board_owner: str, board_name: str) -> None:
        if not ctx.channel.id in self.channel_schedules:
            await ctx.reply("В этом канале нет ни одной доски.")
        else:
            if os.path.exists(f"{self.schedule_cache_folder_path}/{ctx.channel.id}/{board_owner}_{board_name}"):
                scheduler_index = -1
                for index, scheduler in enumerate(self.channel_schedules[ctx.channel.id]):
                    if scheduler[0] == f"{board_owner}_{board_name}":
                        scheduler_index = index
                self.channel_schedules[ctx.channel.id].pop(scheduler_index)
                os.remove(f"{self.schedule_cache_folder_path}/{ctx.channel.id}/{board_owner}_{board_name}")
                await ctx.reply(f"Доска {board_name} успешно удалена из данного канала!")
            else:
                await ctx.reply("Такая доска не прикрепленна к этому каналу.")

    @commands.command()
    async def show_schedule(self, ctx: commands.Context, a:str, b:str) -> None:
        print(a)
        await ctx.reply(f"WHAT {a} {b}")

    @commands.command()
    async def change_scheduling(self, ctx: commands.Context) -> None:
        pass
    
    @commands.command()
    async def change_send_time(self, ctx: commands.Context) -> None:
        pass

async def setup(bot: commands.Bot):
    await bot.add_cog(PinterestScheduler(bot))