import logging
import os
from src.initialize import initialize_app

initialize_app()

def setup_logging(log_level="INFO", log_file="logs/trading_bot.log"):
    """
    Sets up logging for the application.
    
    Parameters:
        log_level (str): The logging level.
        log_file (str): The log file path.
    """
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file)  # Log to a file
        ]
    )

def get_env_variable(var_name, expected_type=str):
    try:
        value = os.environ[var_name]
        validate_env_variable(var_name, value, expected_type)
        return value
    except KeyError:
        logging.error(f"Environment variable {var_name} not set.")
        exit(1)

def validate_env_variable(var_name, value, expected_type):
    if not isinstance(value, expected_type):
        logging.error(f"Environment variable {var_name} is not of expected type {expected_type}.")
        exit(1)