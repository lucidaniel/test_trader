import logging
import os
from typing import Type, Any
from src.initialize import initialize_app

initialize_app()

def setup_logging(log_level: str = "INFO", log_file: str = "logs/trading_bot.log") -> None:
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
            logging.FileHandler(log_file)
        ]
    )

def get_env_variable(var_name: str, expected_type: Type[Any] = str) -> Any:
    try:
        value = os.environ[var_name]
        validate_env_variable(var_name, value, expected_type)
        return value
    except KeyError:
        logging.error(f"Environment variable {var_name} not set.")
        raise EnvironmentError(f"Environment variable {var_name} not set.")

def validate_env_variable(var_name: str, value: Any, expected_type: Type[Any]) -> None:
    if not isinstance(value, expected_type):
        logging.error(f"Environment variable {var_name} is not of expected type {expected_type}.")
        raise TypeError(f"Environment variable {var_name} is not of expected type {expected_type}.")
