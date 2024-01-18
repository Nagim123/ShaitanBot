from __future__ import annotations
from typing import TYPE_CHECKING

import os

from discord.ext import commands
from random import random
from pinterest_board_parser.pinterest_board_does_not_exist_exception import PinterestBoardDoesNotExistException
from pin_scheduling.pinterest_board_pool import PinterestBoardPool
from pin_scheduling.pinterest_channel_scheduler import PinteresetChannelScheduler
from pin_scheduling.board_not_found_exception import BoardNotFoundException
from pin_scheduling.board_already_added_exception import BoardAlreadyAddedException

from config import Config

if TYPE_CHECKING:
    from bot import ShaitanBot

class PinterestScheduler(commands.Cog):
    def __init__(self, bot: ShaitanBot) -> None:
        self.bot = bot
        self.board_pool = PinterestBoardPool()
        self.channel_schedulers: dict[int, PinteresetChannelScheduler] = dict()
        self.schedule_cache_folder_path = Config.data()["PINTEREST_BOARD_SCHEDULE_CACHE_FOLDER"]
        
        self.__load_all_board_schedulers_from_cache()
    
    @commands.command()
    async def add_pin_board(self, ctx: commands.Context, board_owner: str, board_name: str) -> None:
        try:
            board = self.board_pool.link_board(board_owner, board_name)
            if ctx.channel.id in self.channel_schedulers:
                self.channel_schedulers[ctx.channel.id].add_pin_board(board_owner, board_name, board)
            else:
                channel_scheduler = PinteresetChannelScheduler(ctx.channel.id, self.board_pool)
                channel_scheduler.add_pin_board(board_owner, board_name, board)
                self.channel_schedulers[ctx.channel.id] = channel_scheduler
        except BoardAlreadyAddedException as e:
            await ctx.reply(e.get_user_format_error())
            return
        except PinterestBoardDoesNotExistException:
            await ctx.reply("Такой доски не существует.")
            return

        await ctx.reply("Доска успешно добавлена!")

    @commands.command()
    async def remove_pin_board(self, ctx: commands.Context, board_owner: str, board_name: str) -> None:
        if not ctx.channel.id in self.channel_schedulers:
            await ctx.reply("К этому каналу не прикрепленна ни одна доска.")
            return
        
        try:
            self.channel_schedulers[ctx.channel.id].remove_pin_board(board_owner, board_name)
            self.board_pool.unlink_board(board_owner, board_name)
        except BoardNotFoundException as e:
            await ctx.reply(e.get_user_format_error())
            return

        await ctx.reply(f"Доска {board_name} успешно удалена из данного канала!")

    @commands.command()
    async def show_schedule(self, ctx: commands.Context) -> None:
        await ctx.reply(f"WHAT TEST")

    @commands.command()
    async def change_scheduling(self, ctx: commands.Context) -> None:
        await ctx.reply(f"NOT IMPLEMENTED")
    
    @commands.command()
    async def change_send_time(self, ctx: commands.Context) -> None:
        await ctx.reply(f"NOT IMPLEMENTED")

    def __load_all_board_schedulers_from_cache(self) -> None:
        for channel_id in os.listdir(self.schedule_cache_folder_path):
            channel_dir_path = self.schedule_cache_folder_path + '/' + channel_id + '/'
            if os.path.isdir(channel_dir_path):
                self.channel_schedulers[int(channel_id)] = PinteresetChannelScheduler(int(channel_id), self.board_pool)

async def setup(bot: commands.Bot):
    await bot.add_cog(PinterestScheduler(bot))