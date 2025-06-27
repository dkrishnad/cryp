#!/usr/bin/env python3
"""
Quick test to verify auto trading toggle and virtual balance display
"""

import requests
import json
import time

API_URL = "http://localhost:8001"

def quick_test():
    """Quick test of critical functionality"""
    print("🔧 QUICK AUTO TRADING & BALANCE TEST")
    print("=" * 50)
    
    # 1. Test virtual balance endpoint
    print("1. Testing virtual balance endpoint...")
    try:
        resp = requests.get(f"{API_URL}/virtual_balance", timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            print(f"   ✓ Status: {data.get('status')}")
            print(f"   ✓ Balance: ${data.get('balance', 0):,.2f}")
            print(f"   ✓ P&L: ${data.get('current_pnl', 0):,.2f}")
        else:
            print(f"   ✗ Error: {resp.status_code}")
    except Exception as e:
        print(f"   ✗ Exception: {e}")
    
    # 2. Test auto trading status
    print("\n2. Testing auto trading status...")
    try:
        resp = requests.get(f"{API_URL}/auto_trading/status", timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            print(f"   ✓ Status: {data.get('status')}")
            auto_trading = data.get('auto_trading', {})
            print(f"   ✓ Enabled: {auto_trading.get('enabled', False)}")
            print(f"   ✓ Balance in status: ${auto_trading.get('balance', 0):,.2f}")
        else:
            print(f"   ✗ Error: {resp.status_code}")
    except Exception as e:
        print(f"   ✗ Exception: {e}")
    
    # 3. Test toggle functionality
    print("\n3. Testing toggle functionality...")
    try:
        # Enable
        resp = requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": True}, timeout=3)
        if resp.status_code == 200:
            print("   ✓ Enable toggle successful")
        else:
            print(f"   ✗ Enable failed: {resp.status_code}")
        
        time.sleep(0.5)
        
        # Disable  
        resp = requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": False}, timeout=3)
        if resp.status_code == 200:
            print("   ✓ Disable toggle successful")
        else:
            print(f"   ✗ Disable failed: {resp.status_code}")
            
    except Exception as e:
        print(f"   ✗ Toggle exception: {e}")
    
    print("\n" + "=" * 50)
    print("📋 RESULTS")
    print("=" * 50)
    print("If all tests passed, the backend is working correctly.")
    print("If dashboard still shows issues, it's a frontend sync problem.")
    print("\nTo fix dashboard issues:")
    print("1. Refresh browser page")
    print("2. Check browser console for errors")
    print("3. Verify dashboard callbacks are running")

if __name__ == "__main__":
    quick_test()
