import pandas as pd
import numpy as np
from src.utils.helpers import setup_logging
import logging

def initialize_logging():
    setup_logging()
initialize_logging()

def calculate_rsi(data, window):
    
    """
Calculate the Relative Strength Index (RSI) for a given data frame.

Parameters:
    data (pd.DataFrame): The input data frame containing 'close' prices.
    window (int): The window size for calculating RSI.
    
Returns:
    pd.Series: The calculated RSI values.
    
Formula:
    RSI = 100 - (100 / (1 + RS))
    where RS = Average Gain / Average Loss over the window period
   """
    try:
        delta = data['close'].diff(1)
        gain = (delta.where(delta > 0, 0)).rolling(window=window, min_periods=1).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window, min_periods=1).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        logging.info("RSI calculated successfully.")
        return rsi
    except KeyError as e:
        logging.error(f"Missing key in data: {e}")
        return pd.Series(dtype=float)
    except KeyError as e:
        logging.error(f"Missing key in data: {e}")
        return pd.Series(dtype=float)
    except ZeroDivisionError as e:
        logging.error(f"Division by zero: {e}")
        return pd.Series(dtype=float)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return pd.Series(dtype=float)

def calculate_obv(data):
    """
    Calculate On-Balance Volume (OBV) for a given data frame.
    """
    try:
        obv = (np.sign(data['close'].diff(1).fillna(0)) * data['volume']).cumsum()
        logging.info("OBV calculated successfully.")
        return obv
    except KeyError as e:
        logging.error(f"Missing key in data: {e}")
        return pd.Series(dtype=float)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return pd.Series(dtype=float)

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """
    Calculate Moving Average Convergence Divergence (MACD) for a given data frame.
    """
    try:
        short_ema = data['close'].ewm(span=short_window, adjust=False).mean()
        long_ema = data['close'].ewm(span=long_window, adjust=False).mean()
        macd = short_ema - long_ema
        signal_line = macd.ewm(span=signal_window, adjust=False).mean()
        
        logging.info("MACD and Signal Line calculated successfully.")
        return macd, signal_line
    except Exception as e:
        logging.error(f"Failed to calculate MACD: {e}")
        return None, None
