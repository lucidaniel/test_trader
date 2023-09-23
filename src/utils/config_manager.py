import yaml
import logging
from src.initialize import initialize_app
from typing import Any, Dict

initialize_app()

class ConfigManager:
    def __init__(self, config_path: str) -> None:
        self.config: Dict[str, Any] = self.load_config(config_path)
        self.validate_config()

    def load_config(self, config_path: str) -> Dict[str, Any]:
        try:
            with open(config_path, 'r') as stream:
                config = yaml.safe_load(stream)
                logging.info(f"Successfully loaded configuration from {config_path}.")
                return config
        except FileNotFoundError:
            logging.error(f"Configuration file {config_path} not found.")
            raise
        except yaml.YAMLError as e:
            logging.error(f"Failed to load YAML config file: {e}")
            raise

    def validate_config(self) -> None:
        """Validates the loaded configuration to ensure it contains the necessary sections."""
        required_sections = ['binance', 'trading_pairs']
        for section in required_sections:
            if section not in self.config:
                logging.error(f"Missing '{section}' section in config.")
                raise ValueError(f"Invalid configuration: Missing '{section}' section.")
        logging.info("Configuration validated successfully.")
        # Validate trading pairs
        valid_pairs = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']  # Add more valid pairs as needed
        for pair in self.config['trading_pairs']:
            if pair not in valid_pairs:
                logging.error(f"Invalid trading pair: {pair}")
                raise ValueError(f"Invalid trading pair: {pair}")