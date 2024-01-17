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
        self.board_schedulers_count: dict[str, int] = dict()
    
    @commands.command()
    async def add_pin_board(self, ctx: commands.Context, board_owner: str, board_name: str) -> None:
        board_unique_name = f"{board_owner}_{board_name}"
        path_to_channel_cache = f"{self.schedule_cache_folder_path}/{ctx.channel.id}"
        path_to_scheduler = f"{path_to_channel_cache}/{board_unique_name}"
        path_to_board = f"{self.board_cache_folder_path}/{board_unique_name}"


        if os.path.exists(path_to_scheduler):
            await ctx.reply("Эта доска уже прикрепленна к текущему каналу")
            return
        
        board = PinterestBoard(board_owner, board_name, cache_file_path=path_to_board)
        
        if ctx.channel.id in self.channel_schedules:
            scheduler = PinterestBoardScheduler(board, path_to_scheduler)
            self.channel_schedules[ctx.channel.id].append((board_unique_name, scheduler))
        else:
            os.mkdir(path_to_channel_cache)
            scheduler = PinterestBoardScheduler(board, path_to_scheduler)
            self.channel_schedules[ctx.channel.id] = [(board_unique_name, scheduler)]
        
        if not board_unique_name in self.board_schedulers_count:
            self.board_schedulers_count[board_unique_name] = 1
        else:
            self.board_schedulers_count[board_unique_name] += 1
        
        await ctx.reply("Доска успешно добавлена!")

    @commands.command()
    async def remove_pin_board(self, ctx: commands.Context, board_owner: str, board_name: str) -> None:
        board_unique_name = f"{board_owner}_{board_name}"
        path_to_channel_cache = f"{self.schedule_cache_folder_path}/{ctx.channel.id}"
        path_to_scheduler = f"{path_to_channel_cache}/{board_unique_name}"
        path_to_board = f"{self.board_cache_folder_path}/{board_unique_name}"

        if not ctx.channel.id in self.channel_schedules:
            await ctx.reply("В этом канале нет ни одной доски.")
            return
        
        if not os.path.exists(path_to_scheduler):
            await ctx.reply("Такая доска не прикрепленна к этому каналу.")
            return
        
        scheduler_index = -1
        for index, scheduler in enumerate(self.channel_schedules[ctx.channel.id]):
            if scheduler[0] == board_unique_name:
                scheduler_index = index
                break
        self.channel_schedules[ctx.channel.id].pop(scheduler_index)
        os.remove(path_to_scheduler)

        if len(self.channel_schedules[ctx.channel.id]) == 0:
            del self.channel_schedules[ctx.channel.id]
            os.rmdir(path_to_channel_cache)
        
        self.board_schedulers_count[board_unique_name] -= 1
        if self.board_schedulers_count[board_unique_name] == 0:
            os.remove(path_to_board)

        await ctx.reply(f"Доска {board_name} успешно удалена из данного канала!")

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

    def __load_all_board_schedulers(self) -> None:
        pass

    def __remove_unused_boards(self) -> None:
        pass

async def setup(bot: commands.Bot):
    await bot.add_cog(PinterestScheduler(bot))