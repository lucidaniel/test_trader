import asynctest
from src.main import fetch_current_price

class TestMain(asynctest.TestCase):

    async def test_fetch_current_price(self):
        symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
        
        # Mocking the API call to return a float (e.g., 50000.0)
        with asynctest.patch('src.main.binance.fetch_ticker', return_value={'last': 50000.0}):
            for symbol in symbols:
                price = await fetch_current_price(symbol)
                self.assertIsInstance(price, float)

if __name__ == '__main__':
    asynctest.main()