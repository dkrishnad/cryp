"""
Quick Toggle Test
"""

import requests

resp = requests.post("http://127.0.0.1:8000/auto_trading/toggle", json={"enabled": True})
print(f"Toggle response: {resp.status_code}")
if resp.status_code == 200:
    print(f"Data: {resp.json()}")

# Check status
resp = requests.get("http://127.0.0.1:8000/auto_trading/status")
print(f"Status response: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    enabled = data.get("auto_trading", {}).get("enabled", False)
    print(f"Enabled: {enabled}")
