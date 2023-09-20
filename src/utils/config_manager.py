import yaml
import logging
from src.initialize import initialize_app
from typing import Any, Dict

initialize_app()

class ConfigManager:
    def __init__(self, config_path: str) -> None:
        self.config = self.load_config(config_path)
        self.validate_config()

    def load_config(self, config_path: str) -> Dict[str, Any]:
        try:
            with open(config_path, 'r') as stream:
                config = yaml.safe_load(stream)
                logging.info("Successfully loaded configuration from file.")
                return config
        except FileNotFoundError:
            logging.error(f"{config_path} not found.")
            raise
        except Exception as e:
            logging.error(f"Failed to load config file: {e}")
            raise

    def validate_config(self) -> None:
        """Validates the loaded configuration to ensure it contains the necessary sections."""
        if 'binance' not in self.config:
            logging.error("Missing 'binance' section in config.")
            raise ValueError("Invalid configuration.")
        if 'trading_pairs' not in self.config:
            logging.error("Missing 'trading_pairs' section in config.")
            raise ValueError("Invalid configuration.")
        logging.info("Configuration validated successfully.")
        # Add further validation logic based on your specific needs