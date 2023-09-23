import asynctest
from src.main import fetch_current_price, analyze_symbol

class TestMain(asynctest.TestCase):
    async def test_analyze_symbol(self):
        result = await analyze_symbol('BTC/USDT', 'ETH/USDT', 'SOL/USDT')
        assert result is not None  # Replace with actual assertions
    
    #async def test_invalid_symbol(self):
        #TODO: Add a test case for invalid symbols
    
    async def test_fetch_current_price(self):
        price = await fetch_current_price('BTC/USDT', 'ETH/USDT', 'SOL/USDT')
        assert isinstance(price, float), "Price should be a float value"
        assert price > 0, "Price should be greater than 0"
    
if __name__ == '__main__':
    asynctest.main()