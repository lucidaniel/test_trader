import logging
import os

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

def get_env_variable(var_name):
    """
    Fetches an environment variable and exits if not found.
    
    Parameters:
        var_name (str): The name of the environment variable.
        
    Returns:
        str: The value of the environment variable.
    """
    try:
        return os.environ[var_name]
    except KeyError:
        logging.error(f"Environment variable {var_name} not set.")
        exit(1)