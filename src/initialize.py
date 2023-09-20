import logging
import os
from dotenv import load_dotenv

def initialize_app():
    load_dotenv()
    setup_logging()

def setup_logging(log_level="INFO", log_file="logs/trading_bot.log"):
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file)
        ]
    )