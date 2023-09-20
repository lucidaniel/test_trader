from dotenv import load_dotenv
import aiohttp
import asyncio
import os
import pandas as pd
from src.initialize import initialize_app
import logging

initialize_app()

api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

async def fetch_data(url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                logging.error(f"Failed to fetch data: {response.status}")
                return None
            return await response.json()

async def fetch_historical_data(symbol, timeframe, since, limit):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={timeframe}&startTime={since}&limit={limit}"
        headers = {'X-MBX-APIKEY': api_key}
        data = await fetch_data(url, headers)
        logging.info(f"Fetched historical data for {symbol}.")
        return data
    except Exception as e:
        logging.error(f"An error occurred while fetching historical data for {symbol}: {e}")
        return None

async def save_historical_data_to_csv(symbol, data):
    try:
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        historical_data_path = os.path.join('data', 'historical_data', f"{symbol}_historical_data.csv")
        df.to_csv(historical_data_path, index=False)
        logging.info(f"Saved historical data to CSV for {symbol}.")
    except Exception as e:
        logging.error(f"Failed to save historical data to CSV: {e}")
        return None

async def save_historical_data_to_csv(symbol, data):
    try:
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        historical_data_path = os.path.join('data', 'historical_data', f"{symbol}_historical_data.csv")
        df.to_csv(historical_data_path, index=False)
        logging.info(f"Saved historical data to CSV for {symbol}.")
    except Exception as e:
        logging.error(f"Failed to save historical data to CSV: {e}")
        return data
    
async def fetch_real_time_data(symbol, timeframe, limit):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={timeframe}&limit={limit}"
    headers = {'X-MBX-APIKEY': api_key}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            logging.info(f"Fetched real-time data for {symbol}.")
            return data

async def execute_trade(symbol, side, amount, price):
    url = f"https://api.binance.com/api/v3/order"
    headers = {
        'X-MBX-APIKEY': api_key,
        # Add other necessary headers for authentication
    }
    params = {
        'symbol': symbol,
        'side': side,
        'type': 'LIMIT',
        'timeInForce': 'GTC',
        'quantity': amount,
        'price': price
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, params=params) as response:
            order = await response.json()
            logging.info(f"Executed {side} order for {symbol} at {price} with amount {amount}.")
            return order
