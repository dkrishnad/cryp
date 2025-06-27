"""
Test Backend Initialization Logic
Simulate what the backend should do on startup
"""

import json
import os

# Simulate the backend's initialization logic
auto_trading_status = {
    "enabled": False,  # This is the default
    "active_trades": [],
    "total_profit": 0.0,
    "signals_processed": 0
}

print("=== TESTING BACKEND INITIALIZATION ===")
print(f"1. Default state: enabled={auto_trading_status.get('enabled')}")

# Load from persistent storage (like the new backend code should do)
if os.path.exists("data/auto_trading_status.json"):
    with open("data/auto_trading_status.json", "r") as f:
        stored_status = json.load(f)
        auto_trading_status.update(stored_status)
    print(f"2. After loading file: enabled={auto_trading_status.get('enabled')}")
    print(f"3. Full status: {auto_trading_status}")
else:
    print("2. No file found!")
    
print("\nIf enabled=True, then the new backend code would work correctly.")
print("The issue is the current running backend hasn't been restarted.")
