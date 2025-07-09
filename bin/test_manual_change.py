"""
Test if backend picks up manual file change
"""

import requests

API_URL = "http://127.0.0.1:8000"

print("=== TESTING BACKEND STATUS AFTER MANUAL FILE CHANGE ===")

# Check status
resp = requests.get(f"{API_URL}/auto_trading/status")
if resp.status_code == 200:
    data = resp.json()
    print(f"Status response: {data}")
    enabled = data.get("auto_trading", {}).get("enabled", False)
    if enabled:
        print("✅ Backend now reports auto trading as ENABLED!")
    else:
        print("❌ Backend still reports auto trading as DISABLED")
else:
    print(f"❌ Status check failed: {resp.status_code} - {resp.text}")
