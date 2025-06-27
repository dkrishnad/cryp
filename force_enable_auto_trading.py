"""
Force Enable Auto Trading and Test Execution
"""

import requests
import json

API_URL = "http://127.0.0.1:8000"

print("=== FORCE ENABLE AUTO TRADING & TEST ===")

# 1. Enable auto trading
print("\n1. Enabling auto trading...")
resp = requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": True})
if resp.status_code == 200:
    data = resp.json()
    print(f"✅ Enabled: {data}")
else:
    print(f"❌ Failed: {resp.status_code}")

# 2. Check signal and execute manually
print("\n2. Getting signal for manual execution...")
resp = requests.get(f"{API_URL}/auto_trading/current_signal")
if resp.status_code == 200:
    data = resp.json()
    if data.get("signal"):
        signal = data["signal"]
        direction = signal.get("direction", "")
        confidence = signal.get("confidence", 0)
        print(f"Signal: {direction}, Confidence: {confidence}%")
        
        if confidence >= 70 and direction in ["BUY", "SELL"]:
            print("✅ Executing signal manually...")
            
            payload = {
                "timestamp": signal.get("timestamp", ""),
                "symbol": signal.get("symbol", ""),
                "signal": direction,
                "confidence": confidence,
                "price": signal.get("price", 0.0)
            }
            
            exec_resp = requests.post(f"{API_URL}/auto_trading/execute_signal", json=payload)
            if exec_resp.status_code == 200:
                result = exec_resp.json()
                print(f"✅ Execution successful: {result}")
                
                # Check trade count
                trades_resp = requests.get(f"{API_URL}/auto_trading/trades")
                if trades_resp.status_code == 200:
                    trades_data = trades_resp.json()
                    count = trades_data.get("count", 0)
                    print(f"✅ Total trades: {count}")
            else:
                print(f"❌ Execution failed: {exec_resp.status_code}")
        else:
            print(f"❌ Signal criteria not met")

print("\n✅ Check dashboard now!")
