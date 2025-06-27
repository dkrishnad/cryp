#!/usr/bin/env python3
"""
DIRECT API TEST - No dashboard interference
"""

import requests
import json

def direct_api_test():
    print("🎯 DIRECT API TEST")
    print("=" * 30)
    
    API_URL = "http://localhost:8001"
    
    # Test 1: Virtual Balance
    print("1. Virtual Balance:")
    try:
        resp = requests.get(f"{API_URL}/virtual_balance", timeout=2)
        data = resp.json()
        balance = data.get("balance", 0)
        pnl = data.get("current_pnl", 0)
        print(f"   Balance: ${balance:,.2f}")
        print(f"   P&L: ${pnl:,.2f}")
    except:
        print("   ERROR")
    
    # Test 2: Enable Auto Trading
    print("\n2. Enable Auto Trading:")
    try:
        resp = requests.post(f"{API_URL}/auto_trading/toggle", 
                           json={"enabled": True}, timeout=2)
        data = resp.json()
        print(f"   Result: {data.get('status')}")
    except:
        print("   ERROR")
    
    # Test 3: Check Status
    print("\n3. Auto Trading Status:")
    try:
        resp = requests.get(f"{API_URL}/auto_trading/status", timeout=2)
        data = resp.json()
        auto_trading = data.get("auto_trading", {})
        enabled = auto_trading.get("enabled", False)
        print(f"   Enabled: {enabled}")
    except:
        print("   ERROR")
    
    # Test 4: Current Signal
    print("\n4. Current Signal:")
    try:
        resp = requests.get(f"{API_URL}/auto_trading/current_signal", timeout=2)
        data = resp.json()
        if data.get("signal"):
            signal = data["signal"]
            signal_type = signal.get("signal", "")
            confidence = signal.get("confidence", 0)
            print(f"   Signal: {signal_type}")
            print(f"   Confidence: {confidence}%")
        else:
            print("   No signal")
    except:
        print("   ERROR")

if __name__ == "__main__":
    direct_api_test()
