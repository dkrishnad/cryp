"""
Direct Backend Status Test
"""

import requests

try:
    resp = requests.get("http://127.0.0.1:8000/auto_trading/status")
    print(f"Status Code: {resp.status_code}")
    print(f"Response: {resp.text}")
    if resp.status_code == 200:
        data = resp.json()
        enabled = data.get("auto_trading", {}).get("enabled", "NOT_FOUND")
        print(f"Enabled value: {enabled}")
        print(f"Type: {type(enabled)}")
except Exception as e:
    print(f"Error: {e}")
