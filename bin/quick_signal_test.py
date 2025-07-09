"""
Quick Signal Test
"""
import requests

try:
    resp = requests.get("http://127.0.0.1:8000/auto_trading/current_signal", timeout=5)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print("Signal Response:")
        print(data)
        
        if data.get("signal"):
            signal = data["signal"]
            print(f"\nSignal Details:")
            print(f"Direction: {signal.get('direction', 'MISSING')}")
            print(f"Confidence: {signal.get('confidence', 0)}")
            print(f"Symbol: {signal.get('symbol', 'MISSING')}")
    else:
        print(f"Error: {resp.text}")
except Exception as e:
    print(f"Error: {e}")
