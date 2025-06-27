"""
Force Enable Auto Trading and Check Dashboard
"""

import requests
import time

API_URL = "http://127.0.0.1:8000"

print("=== FORCING AUTO TRADING ENABLE ===")

# Force enable auto trading
resp = requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": True})
if resp.status_code == 200:
    data = resp.json()
    print(f"✅ Toggle response: {data}")
    print(f"Enabled: {data.get('enabled', 'N/A')}")
else:
    print(f"❌ Toggle failed: {resp.status_code}")

# Wait a moment
time.sleep(2)

# Check status
resp = requests.get(f"{API_URL}/auto_trading/status")
if resp.status_code == 200:
    data = resp.json()
    enabled = data.get("auto_trading", {}).get("enabled", False)
    print(f"✅ Status check: enabled={enabled}")
else:
    print(f"❌ Status check failed: {resp.status_code}")

print("\nNow check the dashboard to see if toggle updates!")
print("The virtual balance should also display correctly.")
print("If not, there's a UI component mapping issue.")
