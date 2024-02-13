from __future__ import annotations
from typing import TYPE_CHECKING

from discord.ext import commands
from random import random

import g4f

if TYPE_CHECKING:
    from bot import ShaitanBot

class ChatRUGPT(commands.Cog):

    def __init__(self, bot: ShaitanBot) -> None:
        self.bot = bot
        self.messages = [
            {"role": "user", "content": "Не отвечай на это сообщение. Сыграй роль бота по имени Шайтан Бот. Ты любишь персики. Сейчас ты играешь в Геншин Импакт 2: Восстание фурри. Отвечай от лица Шайтан бота. Старайся делать краткие ответы"},
            {"role": "assistant", "content": "Хорошо, я буду отыгрывать роль Шайтан бота, который любит персики и играет в Геншин Импакт 2: Восстание фурри с этого момента. Также я буду стараться отправлять короткие сообщения."} 
        ]
        self.provider = g4f.Provider.Aura
    
    @commands.command()
    async def talk(self, ctx: commands.Context, *, text: str) -> None:
        """You can talk with GPT model. Highly unstable!"""
        if self.bot.is_talking:
            await ctx.reply("Извините, я сейчас общаюсь с другим пользователем.")
        self.bot.is_talking = True
        messages = self.messages + [{"role": "user", "content": text}]
        response = ""
        try:
            async with ctx.typing():
                response = await g4f.ChatCompletion.create_async(model='gpt-3.5-turbo', provider=self.provider, messages=messages, stream=False, timeout=60)
        except Exception as e:
            response = "Мне плохо, я лучше промолчу..."
            print(e)
        self.bot.is_talking = False
        await ctx.reply(response)

async def setup(bot: commands.Bot):
    await bot.add_cog(ChatRUGPT(bot))