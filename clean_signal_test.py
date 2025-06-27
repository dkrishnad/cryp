"""Direct Signal Test - No Terminal Output"""
import requests
import json
import sys

# Redirect stdout to suppress prints
class NullWriter:
    def write(self, s): pass
    def flush(self): pass

sys.stdout = NullWriter()

try:
    resp = requests.get("http://127.0.0.1:8000/auto_trading/current_signal", timeout=3)
    sys.stdout = sys.__stdout__  # Restore stdout
    
    print("=== SIGNAL API TEST ===")
    print(f"Status: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        print("\nResponse Structure:")
        print(f"Status: {data.get('status')}")
        print(f"Has Signal: {bool(data.get('signal'))}")
        
        if data.get("signal"):
            signal = data["signal"]
            print(f"\nSignal Data:")
            print(f"Direction: '{signal.get('direction', 'MISSING')}'")
            print(f"Confidence: {signal.get('confidence', 0)}")
            print(f"Symbol: {signal.get('symbol', 'MISSING')}")
            print(f"Price: {signal.get('price', 0)}")
            print(f"Timestamp: {signal.get('timestamp', 'MISSING')}")
            
            # Check execution criteria
            direction = signal.get('direction', '')
            confidence = signal.get('confidence', 0)
            print(f"\nExecution Check:")
            print(f"Direction valid: {direction in ['BUY', 'SELL']} ('{direction}')")
            print(f"Confidence OK: {confidence >= 70} ({confidence}% >= 70%)")
            print(f"Should execute: {confidence >= 70 and direction in ['BUY', 'SELL']}")
        else:
            print("\n❌ No signal data in response")
    else:
        print(f"❌ HTTP Error: {resp.text}")
        
except Exception as e:
    sys.stdout = sys.__stdout__  # Restore stdout
    print(f"❌ Exception: {e}")
