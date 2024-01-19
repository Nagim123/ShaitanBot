import asyncio
import logging

from pinterest_board_parser.pinterest_parse_logger import get_parsing_logger
from config import Config
from bot import run_bot

if __name__ == "__main__":
    Config.load("config.json")
    # Logging stuff
    logging.basicConfig(format="%(asctime)s [%(levelname)s] %(message)s")
    get_parsing_logger().setLevel(logging.DEBUG)
    get_parsing_logger().addHandler(logging.FileHandler("./logs/parser_logger.txt", mode='w', encoding="utf-8"))
    logging.getLogger("SchedulingLogger").setLevel(logging.DEBUG)
    # Run bot
    asyncio.run(run_bot(Config.data()["DISCORD_BOT_TOKEN"]))