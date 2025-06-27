#!/usr/bin/env python3
"""
Simple test to enable auto trading and check virtual balance
"""

import requests
import json
import time

API_URL = "http://localhost:8001"

def enable_auto_trading_and_check():
    print("🔧 ENABLING AUTO TRADING AND CHECKING VIRTUAL BALANCE")
    print("=" * 60)
    
    # 1. Check current status
    print("1. Current auto trading status:")
    resp = requests.get(f"{API_URL}/auto_trading/status")
    if resp.status_code == 200:
        data = resp.json()
        auto_trading = data.get("auto_trading", {})
        print(f"   Enabled: {auto_trading.get('enabled', False)}")
    
    # 2. Enable auto trading
    print("\n2. Enabling auto trading...")
    resp = requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": True})
    if resp.status_code == 200:
        data = resp.json()
        print(f"   Toggle result: {data.get('status')} - {data.get('message')}")
    else:
        print(f"   Toggle failed: {resp.status_code}")
    
    # 3. Check status again
    print("\n3. Auto trading status after enabling:")
    resp = requests.get(f"{API_URL}/auto_trading/status")
    if resp.status_code == 200:
        data = resp.json()
        auto_trading = data.get("auto_trading", {})
        enabled = auto_trading.get('enabled', False)
        threshold = auto_trading.get('confidence_threshold', 70.0)
        print(f"   Enabled: {enabled}")
        print(f"   Confidence threshold: {threshold}%")
    
    # 4. Check virtual balance
    print("\n4. Virtual balance:")
    resp = requests.get(f"{API_URL}/virtual_balance")
    if resp.status_code == 200:
        data = resp.json()
        if data.get("status") == "success":
            balance = data.get("balance", 0.0)
            pnl = data.get("current_pnl", 0.0)
            print(f"   Balance: ${balance:,.2f}")
            print(f"   P&L: ${pnl:,.2f}")
        else:
            print(f"   Error: {data.get('message')}")
    
    # 5. Check current signal
    print("\n5. Current signal:")
    resp = requests.get(f"{API_URL}/auto_trading/current_signal")
    if resp.status_code == 200:
        data = resp.json()
        if data.get("status") == "success" and data.get("signal"):
            signal = data["signal"]
            signal_type = signal.get("signal", "")
            confidence = signal.get("confidence", 0.0)
            print(f"   Signal: {signal_type}")
            print(f"   Confidence: {confidence}%")
            print(f"   Should execute: {confidence >= 70.0 and signal_type in ['BUY', 'SELL']}")
        else:
            print(f"   No signal available")
    
    print("\n" + "=" * 60)
    print("💡 SOLUTION:")
    print("1. Make sure to ENABLE auto trading toggle in dashboard")
    print("2. Virtual balance should show in dashboard after refresh")
    print("3. Auto trading will execute when enabled + high confidence signal")

if __name__ == "__main__":
    enable_auto_trading_and_check()
