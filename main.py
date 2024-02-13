import asyncio
import logging

from pinterest_board_parser.pinterest_parse_logger import get_parsing_logger
from config import Config
from bot import run_bot

if __name__ == "__main__":
    Config.load("config.json")
    
    parser_file_handler = logging.FileHandler("./logs/parser_logger.txt", mode='w', encoding="utf-8")
    pin_scheduler_file_handler = logging.FileHandler("./logs/pin_logger.txt", mode='w', encoding="utf-8")
    parser_file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    pin_scheduler_file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

    get_parsing_logger().addHandler(parser_file_handler)
    get_parsing_logger().setLevel(logging.DEBUG)
    logging.getLogger("SchedulingLogger").addHandler(pin_scheduler_file_handler)
    logging.getLogger("SchedulingLogger").setLevel(logging.DEBUG)
    
    # Run bot
    asyncio.run(run_bot(Config.data()["DISCORD_BOT_TOKEN"]))