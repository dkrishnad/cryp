#!/usr/bin/env python3
"""
Initialize virtual balance and auto trading data
"""

import os
import json
from datetime import datetime

def initialize_data_files():
    """Initialize required data files with default values"""
    print("🔧 INITIALIZING CRYPTO BOT DATA FILES")
    print("=" * 50)
    
    # Create data directory
    os.makedirs("data", exist_ok=True)
    print("✓ Created data directory")
    
    # Initialize virtual balance
    virtual_balance_file = "data/virtual_balance.json"
    if not os.path.exists(virtual_balance_file):
        balance_data = {
            "balance": 10000.0,
            "last_updated": datetime.now().isoformat()
        }
        with open(virtual_balance_file, "w") as f:
            json.dump(balance_data, f, indent=2)
        print("✓ Initialized virtual_balance.json with $10,000.00")
    else:
        with open(virtual_balance_file, "r") as f:
            data = json.load(f)
        print(f"✓ Virtual balance file exists: ${data.get('balance', 0):,.2f}")
    
    # Initialize auto trading status
    auto_status_file = "data/auto_trading_status.json"
    if not os.path.exists(auto_status_file):
        status_data = {
            "enabled": False,
            "signals_processed": 0,
            "last_signal_time": None,
            "last_execution_time": None
        }
        with open(auto_status_file, "w") as f:
            json.dump(status_data, f, indent=2)
        print("✓ Initialized auto_trading_status.json (disabled)")
    else:
        with open(auto_status_file, "r") as f:
            data = json.load(f)
        print(f"✓ Auto trading status file exists: enabled={data.get('enabled', False)}")
    
    # Initialize auto trading settings
    auto_settings_file = "data/auto_trading_settings.json"
    if not os.path.exists(auto_settings_file):
        settings_data = {
            "enabled": False,
            "symbol": "BTCUSDT",
            "timeframe": "1h",
            "risk_per_trade": 2.0,
            "take_profit": 3.0,
            "stop_loss": 1.5,
            "confidence_threshold": 75.0,
            "amount_type": "percentage",
            "fixed_amount": 100.0,
            "percentage_amount": 5.0
        }
        with open(auto_settings_file, "w") as f:
            json.dump(settings_data, f, indent=2)
        print("✓ Initialized auto_trading_settings.json")
    else:
        print("✓ Auto trading settings file exists")
    
    print("\n" + "=" * 50)
    print("✅ ALL DATA FILES INITIALIZED")
    print("=" * 50)
    print("Now you can:")
    print("1. Start backend: python backend/main.py")
    print("2. Start dashboard: python dashboard/app.py") 
    print("3. Virtual balance should display $10,000.00")
    print("4. Auto trading toggle should work properly")

if __name__ == "__main__":
    initialize_data_files()
