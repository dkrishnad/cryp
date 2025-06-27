import requests
import json

# Test backend connection
try:
    health_resp = requests.get("http://localhost:8000/health")
    print(f"Backend health: {health_resp.status_code} - {health_resp.text}")
except Exception as e:
    print(f"Backend connection error: {e}")

# Test price endpoint
try:
    price_resp = requests.get("http://localhost:8000/price", params={"symbol": "BTCUSDT"})
    print(f"Price endpoint: {price_resp.status_code} - {price_resp.text}")
except Exception as e:
    print(f"Price endpoint error: {e}")

# Test trade creation
try:
    trade_data = {
        "symbol": "BTCUSDT",
        "direction": "LONG",
        "amount": 0.1,
        "entry_price": 0,
        "tp_pct": 2.0,  # 2% take profit
        "sl_pct": 1.0   # 1% stop loss
    }
    
    trade_resp = requests.post("http://localhost:8000/trade", json=trade_data)
    print(f"Trade creation: {trade_resp.status_code} - {trade_resp.text}")
    
    if trade_resp.ok:
        result = trade_resp.json()
        print(f"Trade created successfully: {result}")
    else:
        print(f"Trade creation failed: {trade_resp.text}")
        
except Exception as e:
    print(f"Trade creation error: {e}")

# Test get trades
try:
    trades_resp = requests.get("http://localhost:8000/trades")
    print(f"Get trades: {trades_resp.status_code}")
    if trades_resp.ok:
        trades = trades_resp.json()
        print(f"Number of trades: {len(trades)}")
        if trades:
            print(f"Latest trade: {trades[-1]}")
except Exception as e:
    print(f"Get trades error: {e}")
