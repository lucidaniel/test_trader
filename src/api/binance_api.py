import logging
from dotenv import load_dotenv
import aiohttp
import asyncio
import os
import pandas as pd
import ccxt
import hmac
import hashlib
import time
from src.initialize import initialize_app

initialize_app()
# Load environment variables from .env file
load_dotenv()

# Fetch API keys from environment variables
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

async def fetch_data(url, headers):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    logging.error(f"Failed to fetch data: {response.status}")
                    return None
                return await response.json()
    except Exception as e:
        logging.error(f"An error occurred while fetching data: {e}")
        return None

async def fetch_historical_data(symbol, timeframe, since, limit):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={timeframe}&startTime={since}&limit={limit}"
    headers = {'X-MBX-APIKEY': API_KEY}
    data = await fetch_data(url, headers)
    logging.info(f"Fetched historical data for {symbol}.")
    return data

async def save_historical_data_to_csv(symbol, data):
    try:
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        historical_data_path = os.path.join('data', 'historical_data', f"{symbol}_historical_data.csv")
        df.to_csv(historical_data_path, index=False)
        logging.info(f"Saved historical data to CSV for {symbol}.")
    except Exception as e:
        logging.error(f"Failed to save historical data to CSV: {e}")

async def fetch_real_time_data(symbol, timeframe, limit):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={timeframe}&limit={limit}"
    headers = {'X-MBX-APIKEY': API_KEY}
    data = await fetch_data(url, headers)
    logging.info(f"Fetched real-time data for {symbol}.")
    return data

async def execute_trade(symbol, side, amount, price):
    try:
        url = f"https://api.binance.com/api/v3/order"
        
        # Define the request parameters
        params = {
            'symbol': symbol,
            'side': side,
            'type': 'LIMIT',
            'timeInForce': 'GTC',
            'quantity': amount,
            'price': price,
            'timestamp': int(time.time() * 1000)  # Binance requires timestamp in milliseconds
        }

        # Generate the signature
        params_string = '&'.join([f"{key}={value}" for key, value in params.items()])
        signature = hmac.new(bytes(API_SECRET , 'latin-1'), msg = bytes(params_string , 'latin-1'), digestmod = hashlib.sha256).hexdigest()
        params['signature'] = signature

        headers = {
            'X-MBX-APIKEY': API_KEY
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, params=params) as response:
                order = await response.json()
                logging.info(f"Executed {side} order for {symbol} at {price} with amount {amount}.")
                return order
    except ccxt.NetworkError as e:
        logging.error(f"Network error while executing trade for {symbol}: {e}")
        return None
    except ccxt.ExchangeError as e:
        logging.error(f"Exchange error while executing trade for {symbol}: {e}")
        return None
