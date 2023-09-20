import logging
import os

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("logs/trading_bot.log")  # Log to a file
        ]
    )
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        logging.error(f"Environment variable {var_name} not set.")
        exit(1)