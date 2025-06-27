"""
Debug Auto Trading State Persistence
Check if auto trading stays enabled after toggling
"""

import requests
import time

API_URL = "http://127.0.0.1:8000"

print("=== DEBUGGING AUTO TRADING STATE PERSISTENCE ===")

# 1. Check current state
print("\n1. Checking current state...")
resp = requests.get(f"{API_URL}/auto_trading/status")
if resp.status_code == 200:
    data = resp.json()
    enabled = data.get("auto_trading", {}).get("enabled", False)
    print(f"Current state: {enabled}")

# 2. Enable auto trading
print("\n2. Enabling auto trading...")
resp = requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": True})
if resp.status_code == 200:
    data = resp.json()
    print(f"Toggle response: {data}")

# 3. Immediately check state
print("\n3. Immediately checking state after toggle...")
resp = requests.get(f"{API_URL}/auto_trading/status")
if resp.status_code == 200:
    data = resp.json()
    enabled = data.get("auto_trading", {}).get("enabled", False)
    print(f"State immediately after toggle: {enabled}")

# 4. Wait a few seconds and check again
print("\n4. Waiting 5 seconds and checking again...")
time.sleep(5)
resp = requests.get(f"{API_URL}/auto_trading/status")
if resp.status_code == 200:
    data = resp.json()
    enabled = data.get("auto_trading", {}).get("enabled", False)
    print(f"State after 5 seconds: {enabled}")
    
# 5. If it's disabled, check if something is resetting it
if not enabled:
    print("\n❌ Auto trading was disabled automatically!")
    print("This suggests:")
    print("1. Backend is not persisting the state correctly")
    print("2. Some other process is disabling it")
    print("3. There's a condition in the backend that auto-disables it")
else:
    print("\n✅ Auto trading is still enabled - state is persistent")

print("\nNow check the dashboard to see if UI updates!")
