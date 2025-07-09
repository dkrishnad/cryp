#!/usr/bin/env python3
"""
Test ultra-fast endpoints to verify instant responses
"""
import requests
import time
import json

def test_fast_endpoints():
    """Test the critical timeout endpoints"""
    base_url = "http://localhost:5000"
    
    timeout_endpoints = [
        "/trade",
        "/portfolio/balance", 
        "/portfolio/reset",
        "/ml/predict",
        "/ml/status",
        "/ml/analytics",
        "/ml/train",
        "/auto_trading/status",
        "/auto_trading/toggle",
        "/futures/positions",
        "/data/live_prices",
        "/backtest/results"
    ]
    
    print("🚀 Testing Ultra-Fast Endpoints")
    print("=" * 50)
    
    for endpoint in timeout_endpoints:
        start_time = time.time()
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=2)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                backend_time = data.get("response_time_ms", "N/A")
                print(f"✅ {endpoint:<25} - {response_time:.1f}ms (backend: {backend_time}ms)")
            else:
                print(f"❌ {endpoint:<25} - Status: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"⚠️ {endpoint:<25} - TIMEOUT")
        except Exception as e:
            print(f"❌ {endpoint:<25} - ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    print("Starting backend endpoint speed test...")
    print("Make sure backend is running on localhost:5000")
    time.sleep(2)
    test_fast_endpoints()
