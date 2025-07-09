#!/usr/bin/env python3
"""
Test script to verify automatic trade execution functionality.
This script will enable auto trading and monitor for automatic execution.
"""

import requests
import time
import json

API_URL = "http://127.0.0.1:8001"

def test_auto_execution():
    print("🧪 Testing Automatic Trade Execution...")
    print("=" * 50)
    
    # 1. Check current auto trading status
    print("1. Checking current auto trading status...")
    resp = requests.get(f"{API_URL}/auto_trading/status")
    if resp.status_code == 200:
        data = resp.json()
        if data["status"] == "success":
            state = data["auto_trading"]
            print(f"   ✓ Auto Trading Enabled: {state['enabled']}")
            print(f"   ✓ Balance: ${state['balance']:,.2f}")
            print(f"   ✓ Active Trades: {len(state['active_trades'])}")
    
    # 2. Check current signal
    print("\n2. Checking current signal...")
    resp = requests.get(f"{API_URL}/auto_trading/current_signal")
    if resp.status_code == 200:
        data = resp.json()
        if data["status"] == "success" and data.get("signal"):
            signal = data["signal"]
            print(f"   ✓ Symbol: {signal['symbol']}")
            print(f"   ✓ Direction: {signal['direction']}")
            print(f"   ✓ Confidence: {signal['confidence']:.1f}%")
            print(f"   ✓ Price: ${signal['price']}")
        else:
            print("   ⚠️ No signal available")
            return
    
    # 3. Enable auto trading if not enabled
    print("\n3. Ensuring auto trading is enabled...")
    resp = requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": True})
    if resp.status_code == 200:
        data = resp.json()
        if data["status"] == "success":
            print("   ✓ Auto trading enabled successfully")
        else:
            print(f"   ❌ Failed to enable auto trading: {data.get('message', 'Unknown error')}")
      # 4. Get initial trade count
    print("\n4. Getting initial trade count...")
    resp = requests.get(f"{API_URL}/auto_trading/trades")
    initial_trade_count = 0
    if resp.status_code == 200:
        data = resp.json()
        if data["status"] == "success":
            initial_trade_count = data["count"]
            print(f"   ✓ Initial trade count: {initial_trade_count}")
    
    # 5. Monitor for automatic execution
    print("\n5. Monitoring for automatic execution (waiting 30 seconds)...")
    print("   Dashboard should execute the trade automatically based on the interval callback...")
    
    for i in range(6):  # Check every 5 seconds for 30 seconds
        time.sleep(5)
          # Check trade count
        resp = requests.get(f"{API_URL}/auto_trading/trades")
        if resp.status_code == 200:
            data = resp.json()
            if data["status"] == "success":
                current_trade_count = data["count"]
                print(f"   [{i+1}/6] Trade count: {current_trade_count} (was {initial_trade_count})")
                
                if current_trade_count > initial_trade_count:
                    print("   ✅ AUTOMATIC EXECUTION DETECTED!")
                    print(f"   ✅ New trade executed automatically!")
                    
                    # Show the new trade
                    new_trades = data["trades"][-1:]
                    for trade in new_trades:
                        print(f"      📈 Trade: {trade['action']} {trade['symbol']} at ${trade['price']}")
                        print(f"      📊 Amount: ${trade['amount']} USDT")
                        print(f"      🕐 Time: {trade['timestamp']}")
                    return True
    
    print("   ⚠️ No automatic execution detected in 30 seconds")
    print("   💡 This could be because:")
    print("      - The dashboard auto-trading toggle is not enabled")
    print("      - The confidence threshold is not met")
    print("      - The interval callback is not running frequently enough")
    
    return False

if __name__ == "__main__":
    try:
        result = test_auto_execution()
        if result:
            print("\n🎉 AUTOMATIC EXECUTION TEST PASSED!")
        else:
            print("\n❌ AUTOMATIC EXECUTION TEST FAILED!")
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
