#!/usr/bin/env python3
"""
Complete Endpoint Test - Tests all 27 endpoints
Verifies that the routes subfolder integration is working
"""

import requests
import json
import time

def safe_print(message, end=None):
    """Print with emoji fallback"""
    try:
        if end is not None:
            print(message, end=end)
        else:
            print(message)
    except UnicodeEncodeError:
        fallback_msg = message
        emoji_map = {
            "🚀": "[START]", "✅": "[OK]", "❌": "[ERROR]", "📡": "[API]",
            "🎯": "[TARGET]", "💾": "[SAVE]", "🎉": "[SUCCESS]"
        }
        for emoji, text in emoji_map.items():
            fallback_msg = fallback_msg.replace(emoji, text)
        if end is not None:
            print(fallback_msg, end=end)
        else:
            print(fallback_msg)

def test_endpoint(method, url, data=None):
    """Test a single endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data or {}, timeout=5)
        
        return {
            "status_code": response.status_code,
            "success": response.status_code in [200, 201],
            "response_size": len(response.text)
        }
    except Exception as e:
        return {
            "status_code": None,
            "success": False,
            "error": str(e)
        }

def run_complete_endpoint_test():
    """Test all 27 endpoints"""
    safe_print("🚀 Starting Complete Endpoint Test...")
    safe_print("📡 Testing integration of routes subfolder...")
    safe_print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # Define all 27 endpoints
    endpoints = [
        # System endpoints
        ("GET", "/health"),
        ("GET", "/"),
        
        # Spot trading endpoints (from spot_trading_routes.py)
        ("GET", "/account"),
        ("GET", "/balance"),
        ("GET", "/positions"),
        ("POST", "/buy"),
        ("POST", "/sell"),
        ("POST", "/cancel_order"),
        
        # Futures trading endpoints (from futures_trading_routes.py)
        ("GET", "/futures/account"),
        ("GET", "/futures/positions"),
        ("GET", "/futures/balance"),
        ("POST", "/futures/buy"),
        ("POST", "/futures/sell"),
        
        # Market data endpoints (from market_data_routes.py)
        ("GET", "/price"),
        ("GET", "/prices"),
        ("GET", "/market_data"),
        ("GET", "/klines"),
        
        # ML/AI endpoints (from ml_prediction_routes.py)
        ("POST", "/predict"),
        ("POST", "/retrain"),
        ("GET", "/model_stats"),
        ("GET", "/analytics"),
        
        # Auto trading endpoints (from auto_trading_routes.py)
        ("POST", "/auto_trading/start"),
        ("POST", "/auto_trading/stop"),
        ("GET", "/auto_trading/status"),
        
        # System endpoints (from system_routes.py)
        ("GET", "/logs"),
        ("GET", "/settings"),
        ("POST", "/reset")
    ]
    
    results = {}
    working_count = 0
    total_count = len(endpoints)
    
    safe_print(f"📡 Testing {total_count} endpoints...")
    
    for method, path in endpoints:
        url = f"{base_url}{path}"
        safe_print(f"Testing {method:4} {path:25} ", end="")
        
        # Test data for POST requests
        test_data = {
            "symbol": "BTCUSDT",
            "quantity": 0.001,
            "price": 45000.0
        } if method == "POST" else None
        
        result = test_endpoint(method, url, test_data)
        results[path] = result
        
        if result["success"]:
            safe_print("✅ 200")
            working_count += 1
        else:
            status = result.get("status_code", "ERROR")
            safe_print(f"❌ {status}")
    
    # Summary
    safe_print("\n" + "=" * 60)
    safe_print("📊 COMPLETE ENDPOINT TEST SUMMARY")
    safe_print("=" * 60)
    safe_print(f"Total endpoints tested: {total_count}")
    safe_print(f"✅ Working: {working_count}")
    safe_print(f"❌ Failed: {total_count - working_count}")
    
    # Success rate
    success_rate = (working_count / total_count) * 100
    safe_print(f"🎯 Success rate: {success_rate:.1f}%")
    
    # Show failed endpoints
    failed_endpoints = [path for path, result in results.items() if not result["success"]]
    if failed_endpoints:
        safe_print("\n🔧 FAILED ENDPOINTS:")
        for path in failed_endpoints:
            status = results[path].get("status_code", "ERROR")
            safe_print(f"   - {path}: {status}")
    else:
        safe_print("\n🎉 ALL ENDPOINTS WORKING!")
    
    # Routes subfolder verification
    routes_working = sum(1 for path in ["/account", "/positions", "/buy", "/sell", 
                                       "/prices", "/market_data", "/klines",
                                       "/auto_trading/start", "/auto_trading/stop"] 
                        if results.get(path, {}).get("success", False))
    
    safe_print(f"\n📁 Routes subfolder integration: {routes_working}/9 new endpoints working")
    
    # Save results
    with open("complete_endpoint_test_results.json", "w") as f:
        json.dump({
            "timestamp": time.time(),
            "total_endpoints": total_count,
            "working_endpoints": working_count,
            "success_rate": success_rate,
            "results": results
        }, f, indent=2)
    
    safe_print(f"\n💾 Results saved to: complete_endpoint_test_results.json")
    
    if success_rate >= 90:
        safe_print("\n🎉 Routes subfolder integration SUCCESSFUL!")
        safe_print("🎉 Dashboard should now be fully interactive!")
    else:
        safe_print("\n🔧 Some endpoints still need fixes")
    
    return results

if __name__ == "__main__":
    run_complete_endpoint_test()
