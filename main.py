import asyncio
from config import Config
from bot import run_bot

if __name__ == "__main__":
    Config.load("config.json")
    asyncio.run(run_bot(Config.data()["DISCORD_BOT_TOKEN"]))