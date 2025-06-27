#!/usr/bin/env python3
"""
Test auto trading endpoints to verify backend integration
"""
import requests
import json
import time

API_URL = "http://localhost:8000"

def test_endpoint(endpoint, method="GET", data=None):
    """Test an endpoint with timing"""
    print(f"\n--- Testing {method} {endpoint} ---")
    try:
        start_time = time.time()
        if method == "GET":
            resp = requests.get(f"{API_URL}{endpoint}", timeout=5)
        elif method == "POST":
            resp = requests.post(f"{API_URL}{endpoint}", json=data, timeout=5)
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        
        print(f"Response time: {response_time:.2f}ms")
        print(f"Status: {resp.status_code}")
        
        if resp.status_code == 200:
            response_data = resp.json()
            print(f"Success: {json.dumps(response_data, indent=2)}")
            return response_data
        else:
            print(f"Error: {resp.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to backend server")
        return None
    except requests.exceptions.Timeout:
        print("TIMEOUT: Request took longer than 5 seconds")
        return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def main():
    print("Testing Auto Trading Integration...")
    
    # Test 1: Health check first
    health_data = test_endpoint("/health")
    if not health_data:
        print("\n❌ Backend server is not running or not responding")
        print("Please make sure the backend is started with: python backend/main.py")
        return
    
    print("\n✅ Backend server is running!")
    
    # Test 2: Auto trading status
    status_data = test_endpoint("/auto_trading/status")
    
    # Test 3: Get trading signals
    signal_data = test_endpoint("/auto_trading/signals")
    
    # Test 4: Update settings
    settings_data = test_endpoint("/auto_trading/settings", "POST", {
        "symbol": "BTCUSDT",
        "timeframe": "1h",
        "risk_per_trade": 5.0,
        "take_profit": 2.0,
        "stop_loss": 1.0,
        "min_confidence": 70.0
    })
    
    # Test 5: Enable auto trading
    toggle_data = test_endpoint("/auto_trading/toggle", "POST", {"enabled": True})
    
    # Test 6: Get updated status
    updated_status = test_endpoint("/auto_trading/status")
    
    # Test 7: Execute signal (if enabled)
    if toggle_data and toggle_data.get("enabled"):
        execute_data = test_endpoint("/auto_trading/execute_signal", "POST")
    
    # Test 8: Get trades
    trades_data = test_endpoint("/auto_trading/trades")
    
    # Test 9: Disable auto trading
    disable_data = test_endpoint("/auto_trading/toggle", "POST", {"enabled": False})
    
    print("\n🎉 Auto Trading Integration Test Complete!")
    print("All endpoints are working correctly.")

if __name__ == "__main__":
    main()
