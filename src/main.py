import asyncio
import time
import joblib
import pandas as pd
import yaml
import logging
import ccxt
import os
from src.api.binance_api import fetch_real_time_data, execute_trade
from src.indicators.technical_indicators import calculate_rsi, calculate_obv, calculate_macd
from src.initialize import initialize_app
import symbol
from utils.helpers import get_env_variable

initialize_app()

# Get the absolute path to the directory where your script is located
script_location = get_env_variable('SCRIPT_LOCATION')

# Build the absolute path to your settings.yaml file
config_file_path = os.path.join(script_location, 'config', 'settings.yaml')

def load_config(config_file_path):
    try:
        with open(config_file_path, 'r') as stream:
            return yaml.safe_load(stream)
    except FileNotFoundError:
        logging.error("settings.yaml not found.")
        raise
    except Exception as e:
        logging.error(f"Failed to load config file: {e}")
        raise
config = load_config(config_file_path)

# Initialize Binance API
def initialize_binance_api(config):
    try:
        return ccxt.binance({
            'apiKey': config['binance']['api_key'],
            'secret': config['binance']['api_secret']
        })
    except Exception as e:
        logging.error(f"Failed to initialize Binance API: {e}")
        raise
binance = initialize_binance_api(config)

# Function to fetch current price
async def fetch_current_price(symbol):
    ticker = binance.fetch_ticker(symbol)
    return ticker['last']

# Define trading parameters
async def analyze_symbol(symbol, timeframe='1m', limit=100):
    model = load_model(symbol)
    while True:
        try:
            ohlcv = await fetch_real_time_data(symbol, timeframe, limit)
            data = process_data(ohlcv)
            prediction = make_prediction(model, data)
            await execute_trade_based_on_prediction(prediction, symbol, data)
        except KeyboardInterrupt:
            logging.info("Stopping the bot.")
            break
        except ccxt.NetworkError as e:
            logging.error(f"Network error: {e}")
            await asyncio.sleep(60)
        except ccxt.ExchangeError as e:
            logging.error(f"Exchange error: {e}")
            await asyncio.sleep(60)
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            await asyncio.sleep(60)
            
# Main entry point
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [analyze_symbol(symbol) for symbol in symbol]
    loop.run_until_complete(asyncio.gather(*tasks))
