import requests

BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price"

def get_binance_price(symbol: str) -> float:
    """
    Fetch the latest price for a symbol from Binance (e.g., 'btcusdt').
    Returns the price as a float, or raises an exception if not found.
    """
    symbol = symbol.upper()
    try:
        resp = requests.get(BINANCE_API_URL, params={"symbol": symbol})
        resp.raise_for_status()
        data = resp.json()
        return float(data["price"])
    except Exception as e:
        raise RuntimeError(f"Failed to fetch price for {symbol}: {e}")

if __name__ == "__main__":
    # Test fetch
    print("BTCUSDT:", get_binance_price("BTCUSDT"))
