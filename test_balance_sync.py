#!/usr/bin/env python3
"""
Test virtual balance synchronization
"""
import requests
import json

API_URL = "http://localhost:8001"

print("🔍 TESTING VIRTUAL BALANCE SYNCHRONIZATION")
print("=" * 50)

# Test 1: Virtual Balance Endpoint
print("\n1️⃣ VIRTUAL BALANCE ENDPOINT:")
try:
    resp = requests.get(f"{API_URL}/virtual_balance", timeout=3)
    if resp.status_code == 200:
        data = resp.json()
        balance = data.get('balance', 0)
        print(f"   ✅ Virtual Balance: ${balance:,.2f}")
    else:
        print(f"   ❌ Error: {resp.status_code} - {resp.text}")
except Exception as e:
    print(f"   ❌ Exception: {e}")

# Test 2: Auto Trading Status Endpoint  
print("\n2️⃣ AUTO TRADING STATUS ENDPOINT:")
try:
    resp = requests.get(f"{API_URL}/auto_trading/status", timeout=3)
    if resp.status_code == 200:
        data = resp.json()
        if data["status"] == "success":
            auto_trading = data["auto_trading"]
            balance = auto_trading.get('balance', 'NOT FOUND')
            print(f"   ✅ Auto Trading Balance: ${balance:,.2f}" if isinstance(balance, (int, float)) else f"   ❌ Balance field: {balance}")
            print(f"   📊 Enabled: {auto_trading.get('enabled', False)}")
            print(f"   🎯 Active Trades: {len(auto_trading.get('active_trades', []))}")
            print(f"   💰 Total Profit: ${auto_trading.get('total_profit', 0):,.2f}")
        else:
            print(f"   ❌ API Error: {data}")
    else:
        print(f"   ❌ HTTP Error: {resp.status_code} - {resp.text}")
except Exception as e:
    print(f"   ❌ Exception: {e}")

# Test 3: Balance Synchronization Test
print("\n3️⃣ SYNCHRONIZATION TEST:")
try:
    # Get both balances
    vb_resp = requests.get(f"{API_URL}/virtual_balance", timeout=3)
    at_resp = requests.get(f"{API_URL}/auto_trading/status", timeout=3)
    
    if vb_resp.status_code == 200 and at_resp.status_code == 200:
        vb_data = vb_resp.json()
        at_data = at_resp.json()
        
        vb_balance = vb_data.get('balance', 0)
        at_balance = at_data.get('auto_trading', {}).get('balance', 'NOT FOUND')
        
        if isinstance(at_balance, (int, float)) and abs(vb_balance - at_balance) < 0.01:
            print(f"   ✅ SYNCHRONIZED: Both show ${vb_balance:,.2f}")
        else:
            print(f"   ❌ MISMATCH:")
            print(f"      Virtual Balance: ${vb_balance:,.2f}")
            print(f"      Auto Trading Balance: {at_balance}")
    else:
        print(f"   ❌ Failed to fetch one or both endpoints")
        
except Exception as e:
    print(f"   ❌ Exception: {e}")

print("\n" + "=" * 50)
print("💡 If balances don't match, the backend needs to be restarted")
print("💡 to apply the code changes for balance synchronization.")
