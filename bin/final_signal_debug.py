"""
Final Signal Debug Test
"""
import requests
import json

def test_signal_api():
    print("=== FINAL SIGNAL DEBUG ===")
    
    # Test current signal API
    print("\n1. Current Signal API:")
    try:
        resp = requests.get("http://127.0.0.1:8000/auto_trading/current_signal", timeout=5)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print("Full Response:")
            print(json.dumps(data, indent=2))
            
            if data.get("status") == "success" and data.get("signal"):
                signal = data["signal"]
                print(f"\nSignal Fields:")
                for key, value in signal.items():
                    print(f"  {key}: {value}")
                    
                direction = signal.get("direction", "MISSING")
                confidence = signal.get("confidence", 0)
                print(f"\nKey Values:")
                print(f"  Direction: '{direction}'")
                print(f"  Confidence: {confidence}")
                print(f"  Should execute: {confidence >= 70 and direction in ['BUY', 'SELL']}")
            else:
                print("❌ No signal in response")
        else:
            print(f"❌ Error: {resp.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_signal_api()
