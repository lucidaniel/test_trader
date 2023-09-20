import yaml
import logging

class ConfigManager:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)

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
        # Add validation logic here
        pass
