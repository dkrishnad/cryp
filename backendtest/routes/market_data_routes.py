"""
Market Data Routes
Handles market data operations: prices, market_data, klines
"""

from fastapi import APIRouter, HTTPException
import time
import random

router = APIRouter()

@router.get("/prices")
async def get_all_prices():
    """Get all symbol prices"""
    try:
        symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "DOTUSDT"]
        prices = {}
        for symbol in symbols:
            base_price = 45000 if "BTC" in symbol else 3000 if "ETH" in symbol else 300
            prices[symbol] = round(base_price * (1 + random.uniform(-0.05, 0.05)), 2)
        
        return {
            "prices": prices,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/market_data")
async def get_market_data():
    """Get comprehensive market data"""
    try:
        return {
            "btc_price": 45000.0,
            "eth_price": 3000.0,
            "market_cap": 2000000000000,
            "total_volume": 50000000000,
            "fear_greed_index": 75,
            "dominance": {
                "BTC": 45.2,
                "ETH": 18.5,
                "Others": 36.3
            },
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/klines")
async def get_klines(symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 100):
    """Get candlestick data"""
    try:
        base_price = 45000.0
        klines = []
        
        for i in range(limit):
            timestamp = int(time.time() * 1000) - (i * 3600000)  # 1 hour intervals
            price_change = random.uniform(-0.02, 0.02)
            open_price = base_price * (1 + price_change)
            close_price = open_price * (1 + random.uniform(-0.01, 0.01))
            high_price = max(open_price, close_price) * (1 + random.uniform(0, 0.005))
            low_price = min(open_price, close_price) * (1 - random.uniform(0, 0.005))
            volume = random.uniform(100, 1000)
            
            klines.append([
                timestamp,
                str(open_price),
                str(high_price),
                str(low_price),
                str(close_price),
                str(volume)
            ])
        
        return {
            "symbol": symbol,
            "interval": interval,
            "klines": klines[::-1]  # Reverse to get chronological order
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
