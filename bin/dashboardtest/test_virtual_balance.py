#!/usr/bin/env python3
"""
Test virtual balance backend integration
"""
import requests
import json

API_URL = "http://localhost:8000"

print("Testing Virtual Balance Integration...")

# Test get virtual balance
print("\n--- Testing GET Virtual Balance ---")
try:
    resp = requests.get(f"{API_URL}/virtual_balance", timeout=3)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        balance = data.get('virtual_balance', 0)
        print(f"Current Virtual Balance: ${balance:,.2f}")
    else:
        print(f"Error: {resp.text}")
except Exception as e:
    print(f"Exception: {e}")

# Test reset virtual balance
print("\n--- Testing POST Reset Virtual Balance ---")
try:
    resp = requests.post(f"{API_URL}/virtual_balance/reset", timeout=3)
    print(f"Reset Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        balance = data.get('virtual_balance', 0)
        print(f"Reset Virtual Balance: ${balance:,.2f}")
    else:
        print(f"Reset Error: {resp.text}")
except Exception as e:
    print(f"Reset Exception: {e}")

print(f"\n--- Expected Dashboard Behavior ---")
print("✅ Virtual balance should display: $10,000.00")
print("✅ Reset button should work")
print("✅ Balance updates automatically every 5 seconds")
print("✅ Balance changes with trading activity")
