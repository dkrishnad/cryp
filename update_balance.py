#!/usr/bin/env python3
"""
Update virtual balance to $15,000
"""
import requests
import json

API_URL = "http://localhost:8001"

print("📝 Updating virtual balance to $15,000...")

try:
    resp = requests.post(f"{API_URL}/virtual_balance", 
                        json={"balance": 15000.0}, 
                        timeout=3)
    if resp.status_code == 200:
        data = resp.json()
        print(f"✅ Success: Balance updated to ${data.get('balance', 0):,.2f}")
    else:
        print(f"❌ Error: {resp.status_code} - {resp.text}")
except Exception as e:
    print(f"❌ Exception: {e}")

# Verify the update
print("\n🔍 Verifying update...")
try:
    resp = requests.get(f"{API_URL}/virtual_balance", timeout=3)
    if resp.status_code == 200:
        data = resp.json()
        balance = data.get('balance', 0)
        print(f"✅ Virtual Balance: ${balance:,.2f}")
    else:
        print(f"❌ Error: {resp.status_code}")
except Exception as e:
    print(f"❌ Exception: {e}")
