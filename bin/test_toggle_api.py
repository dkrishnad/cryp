"""
Test Backend Toggle API
"""

import requests
import json

API_URL = "http://127.0.0.1:8000"

print("=== TESTING BACKEND TOGGLE API ===")

# 1. Check current status
print("1. Current status:")
resp = requests.get(f"{API_URL}/auto_trading/status")
if resp.status_code == 200:
    data = resp.json()
    current_state = data.get("auto_trading", {}).get("enabled", False)
    print(f"   Current state: {current_state}")
else:
    print(f"   Error: {resp.status_code}")

# 2. Toggle to True
print("\n2. Toggling to TRUE:")
resp = requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": True})
if resp.status_code == 200:
    data = resp.json()
    print(f"   Response: {data}")
else:
    print(f"   Error: {resp.status_code} - {resp.text}")

# 3. Check status immediately after toggle
print("\n3. Status after toggle:")
resp = requests.get(f"{API_URL}/auto_trading/status")
if resp.status_code == 200:
    data = resp.json()
    new_state = data.get("auto_trading", {}).get("enabled", False)
    print(f"   New state: {new_state}")
    if new_state:
        print("   ✅ Toggle worked!")
    else:
        print("   ❌ Toggle failed - still disabled")
else:
    print(f"   Error: {resp.status_code}")

# 4. Check the data file directly
print("\n4. Checking data file:")
try:
    with open("data/auto_trading_status.json", "r") as f:
        file_data = json.load(f)
    print(f"   File contents: {file_data}")
    file_enabled = file_data.get("enabled", False)
    if file_enabled:
        print("   ✅ File shows enabled=true")
    else:
        print("   ❌ File shows enabled=false")
except Exception as e:
    print(f"   Error reading file: {e}")

print("\nNow check the dashboard to see if toggle works!")
