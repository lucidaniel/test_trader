import logging
import os
from dotenv import load_dotenv

async def initialize_app():
    """
    Asynchronously initialize the application by loading environment variables and setting up logging.
    """
    await load_dotenv_async()
    await setup_logging_async()

async def load_dotenv_async():
    """
    Asynchronously load environment variables from the .env file.
    """
    load_dotenv()

async def setup_logging_async(log_level=None, log_file=None):
    """
    Asynchronously setup logging for the application.
    
    Parameters:
        log_level (str): The logging level. Default is fetched from .env.
        log_file (str): The log file path. Default is fetched from .env.
    """
    log_level = log_level or os.getenv("LOG_LEVEL", "INFO")
    log_file = log_file or os.getenv("LOG_FILE", "logs/trading_bot.log")
    
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file)
        ]
    )
