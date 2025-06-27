"""
Quick Enable Auto Trading and Check State
"""

import requests
import json
import os

API_URL = "http://127.0.0.1:8000"

print("=== ENABLING AUTO TRADING & CHECKING STATE ===")

# 1. Enable auto trading
print("1. Enabling auto trading...")
resp = requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": True})
if resp.status_code == 200:
    print(f"✅ Toggle response: {resp.json()}")
else:
    print(f"❌ Toggle failed: {resp.status_code} - {resp.text}")

# 2. Check status
print("\n2. Checking status...")
resp = requests.get(f"{API_URL}/auto_trading/status")
if resp.status_code == 200:
    data = resp.json()
    print(f"Status response: {data}")
    enabled = data.get("auto_trading", {}).get("enabled", False)
    print(f"Auto trading enabled: {enabled}")
else:
    print(f"❌ Status check failed: {resp.status_code} - {resp.text}")

# 3. Check the data file directly
data_file = "data/auto_trading_status.json"
if os.path.exists(data_file):
    print(f"\n3. Checking {data_file}...")
    with open(data_file, 'r') as f:
        file_data = json.load(f)
    print(f"File contents: {file_data}")
else:
    print(f"\n3. Data file {data_file} does not exist!")

print("\nNow refresh the dashboard to see if the toggle updates!")
