"""
Check Current Signal API Response
"""
import requests
import json

API_URL = "http://127.0.0.1:8000"

print("🔍 Current Signal API Response:")
try:
    resp = requests.get(f"{API_URL}/auto_trading/current_signal")
    print(f"Status Code: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print("Response:")
        print(json.dumps(data, indent=2))
        
        if data.get("status") == "success" and data.get("signal"):
            signal = data["signal"]
            print(f"\nSignal Details:")
            print(f"Signal Type: '{signal.get('signal', 'MISSING')}'")
            print(f"Confidence: {signal.get('confidence', 0)}%")
            print(f"Symbol: {signal.get('symbol', 'MISSING')}")
            print(f"Price: {signal.get('price', 0)}")
        else:
            print("No signal in response or error")
    else:
        print(f"Error: {resp.text}")
except Exception as e:
    print(f"Exception: {e}")
