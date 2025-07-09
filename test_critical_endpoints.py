#!/usr/bin/env python3
"""
Test Critical Backend Endpoints
Updated to test correct paths for missing endpoints
"""

import requests
import json

def test_critical_endpoints():
    """Test all critical endpoints needed by the dashboard"""
    
    base_url = "http://localhost:5000"
    
    # Critical endpoints for dashboard functionality
    critical_endpoints = [
        "/health",
        "/portfolio", 
        "/trades",
        "/model/analytics",
        "/model/versions",
        "/model/active_version",
        "/ml/compatibility/check",
        "/ml/hybrid/status",
        "/futures/analytics",  # FIXED: Added to futures_trading_routes.py
        "/performance/dashboard",
        "/ml/performance/history",
        "/futures/open_position",  # FIXED: Added to futures_trading_routes.py
        "/futures/close_position",  # FIXED: Added to futures_trading_routes.py
        "/futures/update_positions",  # FIXED: Added to futures_trading_routes.py
        "/risk/portfolio_metrics",
        "/model/retrain",  # FIXED: Correct path (not just /retrain)
    ]
    
    print("🔍 Testing Critical Backend Endpoints")
    print("=" * 50)
    
    working = 0
    missing = 0
    results = []
    
    # Endpoints that need POST requests with data
    post_endpoints = {
        "/futures/open_position": {"symbol": "BTCUSDT", "side": "BUY", "quantity": 0.01},
        "/futures/close_position": {"symbol": "BTCUSDT", "position_id": "test123"},
        "/futures/update_positions": {}
    }
    
    for endpoint in critical_endpoints:
        try:
            # Try GET first
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {endpoint} - {response.status_code} (GET)")
                working += 1
                results.append((endpoint, "✅", response.status_code))
            elif response.status_code == 405 and endpoint in post_endpoints:
                # Try POST for 405 errors on known POST endpoints
                try:
                    post_data = post_endpoints[endpoint]
                    post_response = requests.post(f"{base_url}{endpoint}", json=post_data, timeout=5)
                    if post_response.status_code == 200:
                        print(f"✅ {endpoint} - {post_response.status_code} (POST)")
                        working += 1
                        results.append((endpoint, "✅", post_response.status_code))
                    else:
                        print(f"❌ {endpoint} - GET:405, POST:{post_response.status_code} - {post_response.text[:50] if post_response.text else 'None'}")
                        missing += 1
                        results.append((endpoint, "❌", f"GET:405, POST:{post_response.status_code}"))
                except Exception as post_error:
                    print(f"❌ {endpoint} - GET:405, POST:Error - {str(post_error)[:50]}")
                    missing += 1
                    results.append((endpoint, "❌", "GET:405, POST:Error"))
            else:
                print(f"❌ {endpoint} - {response.status_code} - {response.text[:50] if response.text else 'None'}")
                missing += 1
                results.append((endpoint, "❌", response.status_code))
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint} - Connection Error - {str(e)[:50]}")
            missing += 1
            results.append((endpoint, "❌", "Connection Error"))
    
    print("\n" + "=" * 50)
    print("📊 Summary:")
    print(f"✅ Working: {working}")
    print(f"❌ Missing: {missing}")
    print(f"📈 Success Rate: {working}/{len(critical_endpoints)} ({working/len(critical_endpoints)*100:.1f}%)")
    
    if missing > 0:
        print(f"\n🚨 CRITICAL: {missing} endpoints are missing!")
        print("These need to be implemented for the dashboard to work properly.")
        print("\nMissing endpoints:")
        for endpoint, status, code in results:
            if status == "❌":
                print(f"  - {endpoint}")
    else:
        print("\n🎉 ALL ENDPOINTS ARE WORKING!")
        print("Backend is ready for full dashboard integration!")
    
    return working, missing, results

if __name__ == "__main__":
    test_critical_endpoints()
