#!/usr/bin/env python3
"""
Test to see if interval callbacks are working
"""

import requests
import time
import json

def test_interval_activity():
    """Test if interval callbacks are active"""
    print("🔍 Testing if any callbacks are firing...")
    print("   Dashboard should be running at http://127.0.0.1:8050")
    print("   Looking for ANY callback activity in logs...")
    print()
    
    # Test 1: Check basic connection
    try:
        resp = requests.get("http://127.0.0.1:8050", timeout=5)
        print(f"✅ Dashboard is accessible: {resp.status_code}")
    except Exception as e:
        print(f"❌ Dashboard not accessible: {e}")
        return
    
    # Test 2: Wait for interval activity
    print("⏳ Waiting 20 seconds to observe interval callback activity...")
    print("   Check the dashboard terminal for any callback messages")
    time.sleep(20)
    
    print("✅ Check complete. Look at the dashboard terminal for callback activity.")
    print("   Expected intervals: auto-trading-interval (5s), interval-prediction (5s), interval-indicators (30s)")

if __name__ == "__main__":
    test_interval_activity()
