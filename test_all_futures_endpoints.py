#!/usr/bin/env python3
"""
Complete Futures Endpoints Test
Test all futures endpoints that the dashboard requires
"""

import requests
import json

def test_all_futures_endpoints():
    """Test all futures endpoints required by the dashboard"""
    
    base_url = "http://localhost:5000"
    
    # All futures endpoints the frontend calls
    futures_endpoints = [
        # Dashboard critical endpoints
        "/futures/analytics",
        "/futures/open_position", 
        "/futures/close_position",
        "/futures/update_positions",
        
        # Futures trading tab endpoints
        "/futures/account",
        "/futures/positions", 
        "/futures/history",
        "/futures/balance",
        "/futures/settings",
        "/futures/open",
        "/futures/close", 
        "/futures/update",
        "/futures/execute",
        
        # Additional endpoints
        "/futures/indicators/rsi",
        "/futures/binance/auto_execute",
        "/futures/fapi/v2/account",
        "/futures/fapi/v2/balance",
        "/futures/fapi/v2/positionRisk"
    ]
    
    print("🔍 Testing ALL Futures Backend Endpoints")
    print("=" * 60)
    
    working = 0
    missing = 0
    results = []
    
    for endpoint in futures_endpoints:
        try:
            # Test GET first
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ GET  {endpoint} - {response.status_code}")
                working += 1
                results.append((endpoint, "✅", response.status_code, "GET"))
            elif response.status_code == 405:  # Method not allowed, try POST
                try:
                    post_response = requests.post(f"{base_url}{endpoint}", json={}, timeout=5)
                    if post_response.status_code == 200:
                        print(f"✅ POST {endpoint} - {post_response.status_code}")
                        working += 1
                        results.append((endpoint, "✅", post_response.status_code, "POST"))
                    else:
                        print(f"❌ {endpoint} - GET:{response.status_code}, POST:{post_response.status_code}")
                        missing += 1
                        results.append((endpoint, "❌", f"GET:{response.status_code}, POST:{post_response.status_code}", "BOTH"))
                except:
                    print(f"❌ {endpoint} - GET:{response.status_code}, POST:Error")
                    missing += 1
                    results.append((endpoint, "❌", response.status_code, "GET"))
            else:
                print(f"❌ {endpoint} - {response.status_code}")
                missing += 1
                results.append((endpoint, "❌", response.status_code, "GET"))
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint} - Connection Error")
            missing += 1
            results.append((endpoint, "❌", "Connection Error", "N/A"))
    
    print("\n" + "=" * 60)
    print("📊 FUTURES ENDPOINTS SUMMARY:")
    print(f"✅ Working: {working}")
    print(f"❌ Missing: {missing}")
    print(f"📈 Success Rate: {working}/{len(futures_endpoints)} ({working/len(futures_endpoints)*100:.1f}%)")
    
    if missing > 0:
        print(f"\n🚨 CRITICAL: {missing} futures endpoints are missing!")
        print("Missing endpoints:")
        for endpoint, status, code, method in results:
            if status == "❌":
                print(f"  - {endpoint} ({method}: {code})")
    else:
        print("\n🎉 ALL FUTURES ENDPOINTS ARE WORKING!")
        print("Futures trading dashboard should be fully functional!")
    
    # Test a few with sample data
    print(f"\n🧪 Testing POST endpoints with sample data:")
    test_data = {
        "/futures/open_position": {"symbol": "BTCUSDT", "side": "BUY", "quantity": 0.01},
        "/futures/close_position": {"symbol": "BTCUSDT", "position_id": "test123"},
        "/futures/settings": {"leverage": 10, "margin_type": "cross"}
    }
    
    for endpoint, data in test_data.items():
        try:
            response = requests.post(f"{base_url}{endpoint}", json=data, timeout=5)
            if response.status_code == 200:
                print(f"✅ POST {endpoint} with data - {response.status_code}")
            else:
                print(f"❌ POST {endpoint} with data - {response.status_code}")
        except Exception as e:
            print(f"❌ POST {endpoint} with data - Error: {str(e)[:50]}")

if __name__ == "__main__":
    test_all_futures_endpoints()
