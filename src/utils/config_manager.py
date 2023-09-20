import yaml
import logging
from src.initialize import initialize_app

initialize_app()

class ConfigManager:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.validate_config()

    def load_config(self, config_path):
        try:
            with open(config_path, 'r') as stream:
                config = yaml.safe_load(stream)
                logging.info("Loaded configuration from file.")
                return config
        except FileNotFoundError:
            logging.error(f"{config_path} not found.")
            raise
        except Exception as e:
            logging.error(f"Failed to load config file: {e}")
            raise

    def validate_config(self):
        if 'binance' not in self.config:
            logging.error("Missing 'binance' section in config.")
            raise ValueError("Invalid configuration.")
        # Example validation for trading pairs
        if 'trading_pairs' not in self.config:
            logging.error("Missing 'trading_pairs' section in config.")
            raise ValueError("Invalid configuration.")
        # Add further validation logic based on your specific needs
