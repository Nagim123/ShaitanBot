from __future__ import annotations
from typing import TYPE_CHECKING, Dict

import os
import logging

from discord.ext import commands, tasks
from random import random
from pinterest_board_parser.pinterest_board_does_not_exist_exception import PinterestBoardDoesNotExistException
from pin_scheduling.pinterest_board_pool import PinterestBoardPool
from pin_scheduling.pinterest_channel_scheduler import PinteresetChannelScheduler
from pin_scheduling.board_not_found_exception import BoardNotFoundException
from pin_scheduling.board_already_added_exception import BoardAlreadyAddedException
from pin_scheduling.no_more_pins_exception import NoMorePinsException
from pin_scheduling.wrong_scheduling_time_exception import WrongSchedulingTimeException

from config import Config

if TYPE_CHECKING:
    from bot import ShaitanBot

import datetime
EACH_HOUR_TIMES = [datetime.time(i, 0, 0) for i in range(0, 24)]

class PinterestScheduler(commands.Cog):
    def __init__(self, bot: ShaitanBot) -> None:
        self.__bot = bot
        self.__board_pool = PinterestBoardPool()
        self.__channel_schedulers: Dict[int, PinteresetChannelScheduler] = dict()
        self.__schedule_cache_folder_path = Config.data()["PINTEREST_BOARD_SCHEDULE_CACHE_FOLDER"]
        self.__logger = logging.getLogger("SchedulingLogger")

        self.__load_all_board_schedulers_from_cache()
        self.__send_pins_to_channels_on_time.start()
        self.__logger.info("Pinterest module loaded succesfully!")
    
    @commands.command()
    async def add_pin_board(self, ctx: commands.Context, board_owner: str, board_name: str) -> None:
        """Add board to current channel"""
        self.__logger.info(f"/add_pin_board {board_owner} {board_name} command was entered")
        try:
            board = self.__board_pool.link_board(board_owner, board_name)
            if ctx.channel.id in self.__channel_schedulers:
                self.__channel_schedulers[ctx.channel.id].add_pin_board(board_owner, board_name, board)
            else:
                channel_scheduler = PinteresetChannelScheduler(ctx.channel.id, self.__board_pool)
                channel_scheduler.add_pin_board(board_owner, board_name, board)
                self.__channel_schedulers[ctx.channel.id] = channel_scheduler
        except BoardAlreadyAddedException as e:
            await ctx.reply(e.get_user_format_error())
            self.__logger.info(f"Board {board_name} already added to channel")
            return
        except PinterestBoardDoesNotExistException:
            await ctx.reply("Такой доски не существует.")
            self.__logger.info(f"Board {board_name} was not found")
            return

        self.__logger.info(f"Board {board_name} added succesfully")
        await ctx.reply("Доска успешно добавлена!")

    @commands.command()
    async def remove_pin_board(self, ctx: commands.Context, board_owner: str, board_name: str) -> None:
        """Remove board from current channel"""
        self.__logger.info(f"/remove_pin_board {board_owner} {board_name} command was entered")
        if not ctx.channel.id in self.__channel_schedulers:
            self.__logger.info(f"No boards in channel {ctx.channel.id}")
            await ctx.reply("К этому каналу не прикрепленна ни одна доска.")
            return
        try:
            self.__channel_schedulers[ctx.channel.id].remove_pin_board(board_owner, board_name)
            self.__board_pool.unlink_board(board_owner, board_name)
            self.__logger.info(f"Board {board_name} removed succesfully from {ctx.channel.id}")
        except BoardNotFoundException as e:
            self.__logger.info(f"Board {board_name} was not found in {ctx.channel.id}")
            await ctx.reply(e.get_user_format_error())
            return

        await ctx.reply(f"Доска {board_name} успешно удалена из данного канала!")

    # @commands.command()
    # async def show_schedule(self, ctx: commands.Context) -> None:
    #     await ctx.reply(f"NOT IMPLEMENTED")

    # @commands.command()
    # async def change_scheduling(self, ctx: commands.Context, new_scheduling: str) -> None:
    #     await ctx.reply(f"NOT IMPLEMENTED")
    
    @commands.command()
    async def change_send_time(self, ctx: commands.Context, new_hour: int) -> None:
        """Changes time when the bot sends pic or video"""
        self.__logger.info(f"/change_send_time {new_hour} command was entered")
        if ctx.channel.id in self.__channel_schedulers:
            self.__channel_schedulers[ctx.channel.id].change_accept_time_hour(new_hour)
            await ctx.reply(f"Время отправки ежедневного пина изменена на {new_hour}:00")
            self.__logger.info(f"Send time changed to {new_hour}:00 for channel {ctx.channel.id} successfully!")
            return
        await ctx.reply(f"Добавьте хотя бы 1 доску, чтобы изменять время отправки.")
        self.__logger.info(f"No boards in channel {ctx.channel.id}")

    @tasks.loop(time=EACH_HOUR_TIMES)
    async def __send_pins_to_channels_on_time(self) -> None:
        self.__logger.info("Time to broadcast pins!")
        for channel in self.__channel_schedulers:
            try:
                pin = self.__channel_schedulers[channel].get_scheduled_pin()
                self.__logger.info(f"Send pin {pin.pin_id} to {channel} channel")
                discord_channel = await self.__bot.fetch_channel(channel)
                await discord_channel.send(f"Название:{pin.title}\nДоска:{pin.board_name}")
                await discord_channel.send(pin.resource_link)
                self.__logger.info("Send operation was succesfull")
            except NoMorePinsException:
                discord_channel = await self.__bot.fetch_channel(channel)
                self.__logger.info(f"No pins left for channel {channel}")
                await discord_channel.send("Вы просмотрели все пины из всех досок. Добавьте новые)")
            except WrongSchedulingTimeException:
                continue
            
    def __load_all_board_schedulers_from_cache(self) -> None:
        for channel_id in os.listdir(self.__schedule_cache_folder_path):
            channel_dir_path = self.__schedule_cache_folder_path + '/' + channel_id + '/'
            if os.path.isdir(channel_dir_path):
                self.__channel_schedulers[int(channel_id)] = PinteresetChannelScheduler(int(channel_id), self.__board_pool)

async def setup(bot: commands.Bot):
    await bot.add_cog(PinterestScheduler(bot))