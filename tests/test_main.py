import asynctest
from src.main import fetch_current_price, analyze_symbol

class TestMain(asynctest.TestCase):
    async def test_analyze_symbol(self):
        symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
    
    async def test_invalid_symbol(self):
        # Add a test case for invalid symbols
        pass
        # Mocking the API call to return a float (e.g., 50000.0)
        with asynctest.patch('src.main.binance.fetch_ticker', return_value={'last': 50000.0}):
            for symbol in symbols:
                price = await fetch_current_price(symbol)
                self.assertIsInstance(price, float)

if __name__ == '__main__':
    asynctest.main()