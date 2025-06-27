import requests
import time

# Test what the dashboard would do when user interacts
API_URL = "http://localhost:8000"

print("🔍 TESTING DASHBOARD-SPECIFIC FUNCTIONALITY")
print("=" * 50)

print("\n1. Testing Dashboard's Symbol Selection Flow:")
# This is what happens when user selects BTC in sidebar
try:
    resp = requests.get(f"{API_URL}/price", params={"symbol": "BTCUSDT"})
    print(f"   Price API: {resp.status_code}")
    if resp.ok:
        data = resp.json()
        print(f"   ✅ Price for BTCUSDT: {data['price']}")
    else:
        print(f"   ❌ Price API failed: {resp.text}")
except Exception as e:
    print(f"   ❌ Price API error: {e}")

print("\n2. Testing Dashboard's Technical Indicators:")
# This is what happens in the indicators callback
try:
    resp = requests.get(f"{API_URL}/features/indicators", params={"symbol": "BTCUSDT"})
    print(f"   Indicators API: {resp.status_code}")
    if resp.ok:
        data = resp.json()
        print(f"   ✅ Data: {data}")
    else:
        print(f"   ❌ Indicators API failed: {resp.text}")
except Exception as e:
    print(f"   ❌ Indicators API error: {e}")

print("\n3. Testing Dashboard's Trade Button:")
# This is what happens when user clicks Open Long
try:
    trade_data = {
        "symbol": "BTCUSDT",
        "direction": "LONG", 
        "amount": 0.1,
        "entry_price": 0,
        "tp_pct": 2.0,
        "sl_pct": 1.0
    }
    resp = requests.post(f"{API_URL}/trade", json=trade_data)
    print(f"   Trade API: {resp.status_code}")
    if resp.ok:
        result = resp.json()
        print(f"   ✅ Trade created: {result}")
    else:
        print(f"   ❌ Trade API failed: {resp.text}")
except Exception as e:
    print(f"   ❌ Trade API error: {e}")

print("\n4. Testing Dashboard's Trade Table:")
# This is what happens to populate the trades table
try:
    resp = requests.get(f"{API_URL}/trades")
    print(f"   Trades API: {resp.status_code}")
    if resp.ok:
        trades = resp.json()
        print(f"   ✅ Found {len(trades)} trades")
        if trades:
            print(f"   ✅ Sample trade: {trades[0]}")
    else:
        print(f"   ❌ Trades API failed: {resp.text}")
except Exception as e:
    print(f"   ❌ Trades API error: {e}")

print("\n" + "=" * 50)
print("🎯 DASHBOARD CONNECTIVITY TEST COMPLETE")
print("If all above are ✅, then the backend APIs are working.")
print("If dashboard still not working, the issue is in the frontend callbacks.")
