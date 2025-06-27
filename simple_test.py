import requests
try:
    r = requests.get('http://localhost:8001/fapi/v2/account', timeout=3)
    print(f"Account API: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"Balance: {data.get('totalWalletBalance', 'N/A')} USDT")
    
    r2 = requests.get('http://localhost:8001/fapi/v1/ticker/24hr', timeout=3)
    print(f"Ticker API: {r2.status_code}")
    
    order_data = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "type": "MARKET", 
        "quantity": "0.001"
    }
    r3 = requests.post('http://localhost:8001/fapi/v1/order', data=order_data, timeout=3)
    print(f"Order API: {r3.status_code}")
    if r3.status_code == 200:
        order = r3.json()
        print(f"Order ID: {order.get('orderId', 'N/A')}")
        
    print("✅ All tests completed!")
except Exception as e:
    print(f"❌ Error: {e}")
