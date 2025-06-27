"""
Quick check if futures system is working
"""

import requests

def check_futures():
    try:
        resp = requests.get("http://localhost:8000/futures/account", timeout=2)
        print(f"Futures endpoint status: {resp.status_code}")
        if resp.status_code == 200:
            print("✅ Futures system is loaded!")
            data = resp.json()
            print(f"Response: {data}")
        else:
            print("❌ Futures system not loaded")
            print(f"Response: {resp.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Need to restart backend with futures system")

if __name__ == "__main__":
    check_futures()
