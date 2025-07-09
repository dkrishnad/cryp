"""
Debug Toggle API Issue
"""

import requests
import json
import os

API_URL = "http://127.0.0.1:8000"

print("=== DEBUGGING TOGGLE API ISSUE ===")

# 1. Check what files exist
print("1. Checking data files:")
for filename in ["data/auto_trading_status.json", "data/auto_trading_settings.json"]:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        print(f"   {filename}: {data}")
    else:
        print(f"   {filename}: NOT FOUND")

# 2. Call toggle API to enable
print("\n2. Calling toggle API to enable:")
resp = requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": True})
print(f"   Status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    print(f"   Response: {data}")
    api_enabled = data.get("enabled", False)
    print(f"   API says enabled: {api_enabled}")

# 3. Check files after toggle
print("\n3. Checking data files after toggle:")
for filename in ["data/auto_trading_status.json", "data/auto_trading_settings.json"]:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        file_enabled = data.get("enabled", False)
        print(f"   {filename}: enabled={file_enabled}")

# 4. Call status API
print("\n4. Calling status API:")
resp = requests.get(f"{API_URL}/auto_trading/status")
print(f"   Status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    status_enabled = data.get("auto_trading", {}).get("enabled", False)
    print(f"   Status API says enabled: {status_enabled}")

print("\n=== ANALYSIS ===")
print("If toggle API says enabled=True but status API says enabled=False,")
print("then there's a bug in the backend logic.")
