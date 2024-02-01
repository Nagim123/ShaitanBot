from __future__ import annotations
from typing import TYPE_CHECKING

from discord.ext import commands
from random import random

import requests

if TYPE_CHECKING:
    from bot import ShaitanBot

class ChatRUGPT(commands.Cog):

    def __init__(self, bot: ShaitanBot) -> None:
        self.bot = bot
    
    @commands.command()
    async def talk(self, ctx: commands.Context, *, text: str) -> None:
        """You can talk with GPT model. Highly unstable!"""

        prompt = dict()
        prompt["text"] = f"system: Добрый день как я могу помочь?\nuser: {text}\nsystem:"

        headers = {"Origin": "https://russiannlp.github.io"}
        try:
            response = requests.post("https://api.aicloud.sbercloud.ru/public/v1/public_inference/gpt3/predict", json=prompt, headers=headers, timeout=20)
            prediction = response.json()["predictions"].split('\n')[2]
            await ctx.reply(prediction[8:])
        except requests.exceptions.Timeout:
            await ctx.reply("Can't access sber API")

async def setup(bot: commands.Bot):
    await bot.add_cog(ChatRUGPT(bot))