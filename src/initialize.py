import logging
import os
import dotenv


def initialize_app():
    load_dotenv()
    setup_logging()

def load_dotenv():
    dotenv.load_dotenv()

def setup_logging(log_level=None, log_file=None):
    """
    Set up logging for the application.
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
