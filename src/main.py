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
from src.utils.helpers import setup_logging, get_env_variable
from src.ml.gradient_boost_classifier import load_model

# Initialize logging
setup_logging()

# Get the absolute path to the directory where your script is located
script_location = get_env_variable('SCRIPT_LOCATION')

# Build the absolute path to your settings.yaml file
config_file_path = os.path.join(script_location, 'config', 'settings.yaml')

try:
    with open(config_file_path, 'r') as stream:
        config = yaml.safe_load(stream)
        logging.info("Loaded settings from config file.")
except FileNotFoundError:
    logging.error("settings.yaml not found.")
    raise
except Exception as e:
    logging.error(f"Failed to load config file: {e}")
    raise

# Initialize Binance API
try:
    binance = ccxt.binance({
        'apiKey': config['binance']['api_key'],
        'secret': config['binance']['api_secret']
    })
    logging.info("Initialized Binance API.")
except Exception as e:
    logging.error(f"Failed to initialize Binance API: {e}")
    raise

# Function to fetch current price
async def fetch_current_price(symbol):
    ticker = binance.fetch_ticker(symbol)
    return ticker['last']

# Define trading parameters
symbols = config['trading_pairs']  # Multiple symbols from settings.yaml
timeframe = '1m'
limit = 100

async def analyze_symbol(symbol):
    model = load_model(symbol)  # Load the appropriate model for each symbol
    while True:
        try:
            # Fetch real-time data
            ohlcv = await fetch_real_time_data(symbol, timeframe, limit)
            data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            logging.info(f"Fetched real-time data for {symbol}.")
            
            # Calculate Indicators
            data['rsi'] = calculate_rsi(data, 14)
            data['obv'] = calculate_obv(data)
            data['macd'], data['signal_line'] = calculate_macd(data)
            
            # Prepare feature vector for prediction
            latest_data = data.iloc[-1]
            X = [latest_data['rsi'], latest_data['obv'], latest_data['macd'], latest_data['signal_line']]
            
            # Make a prediction
            prediction = model.predict([X])
            logging.info(f"Made a prediction for {symbol}: {prediction[0]}")
            
            # Execute trade based on prediction
            if prediction == 1:
                logging.info(f"Executing buy order for {symbol}.")
                await execute_trade(symbol, 'buy', 0.01, latest_data['close'])
            elif prediction == 0:
                logging.info(f"Executing sell order for {symbol}.")
                await execute_trade(symbol, 'sell', 0.01, latest_data['close'])
            
            await asyncio.sleep(60)
            
        except KeyboardInterrupt:
            logging.info("Stopping the bot.")
            break
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            await asyncio.sleep(60)

# Main entry point
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [analyze_symbol(symbol) for symbol in symbols]
    loop.run_until_complete(asyncio.gather(*tasks))
