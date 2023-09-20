from dotenv import load_dotenv
from src.utils.helpers import setup_logging

def initialize_app():
    """
    Initialize the application by setting up logging and loading environment variables.
    """
    # Setup logging
    setup_logging()

    # Load environment variables
    load_environment_variables()

def load_environment_variables():
    """
    Load environment variables from the .env file.
    """
    load_dotenv()

if __name__ == "__main__":
    initialize_app()