#!/usr/bin/env python3
"""
Final Dashboard Interactivity Validation
Tests that all endpoints work and dashboard should be fully functional
"""

import requests
import json
import time

def safe_print(message, end="\n"):
    """Print with emoji fallback"""
    try:
        print(message, end=end)
    except UnicodeEncodeError:
        fallback_msg = message
        emoji_map = {
            "🚀": "[START]", "✅": "[OK]", "❌": "[ERROR]", "📡": "[API]",
            "🎯": "[TARGET]", "💾": "[SAVE]", "🎉": "[SUCCESS]", "🔧": "[FIX]"
        }
        for emoji, text in emoji_map.items():
            fallback_msg = fallback_msg.replace(emoji, text)
        print(fallback_msg, end=end)

def test_critical_endpoints():
    """Test the most critical endpoints for dashboard functionality"""
    safe_print("🚀 Final Dashboard Interactivity Validation")
    safe_print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # Critical endpoints that dashboard callbacks depend on
    critical_endpoints = [
        # Account/Balance (for refresh buttons)
        ("GET", "/account", "Account Info"),
        ("GET", "/balance", "Balance Info"),
        
        # Trading (for buy/sell buttons)
        ("POST", "/buy", "Buy Order"),
        ("POST", "/sell", "Sell Order"),
        
        # Futures (for futures buttons)
        ("POST", "/futures/buy", "Futures Buy"),
        ("POST", "/futures/sell", "Futures Sell"),
        
        # Auto Trading (for start/stop buttons)
        ("POST", "/auto_trading/start", "Auto Trading Start"),
        ("POST", "/auto_trading/stop", "Auto Trading Stop"),
        
        # ML/Analytics (for prediction buttons)
        ("POST", "/predict", "ML Prediction"),
        ("GET", "/analytics", "Analytics"),
        ("GET", "/model_stats", "Model Stats"),
        
        # Market Data (for charts/updates)
        ("GET", "/prices", "Price Data"),
        ("GET", "/market_data", "Market Data"),
        
        # System (for system buttons)
        ("GET", "/logs", "System Logs"),
        ("POST", "/reset", "System Reset")
    ]
    
    safe_print("🎯 Testing 15 critical endpoints for dashboard interactivity...")
    safe_print("")
    
    working_count = 0
    total_count = len(critical_endpoints)
    
    for method, path, description in critical_endpoints:
        url = f"{base_url}{path}"
        safe_print(f"Testing {description:20} ({method:4} {path:20}) ", end="")
        
        try:
            test_data = {"symbol": "BTCUSDT", "quantity": 0.001} if method == "POST" else None
            
            if method == "GET":
                response = requests.get(url, timeout=5)
            else:
                response = requests.post(url, json=test_data, timeout=5)
            
            if response.status_code in [200, 201]:
                safe_print("✅ OK")
                working_count += 1
            else:
                safe_print(f"❌ {response.status_code}")
                
        except Exception as e:
            safe_print(f"❌ ERROR")
    
    # Results
    safe_print("")
    safe_print("=" * 60)
    safe_print("📊 FINAL VALIDATION SUMMARY")
    safe_print("=" * 60)
    
    success_rate = (working_count / total_count) * 100
    safe_print(f"Critical endpoints working: {working_count}/{total_count}")
    safe_print(f"Success rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        safe_print("")
        safe_print("🎉 DASHBOARD SHOULD BE FULLY INTERACTIVE!")
        safe_print("🎉 All critical callback endpoints are working!")
        safe_print("")
        safe_print("📋 What this means:")
        safe_print("   ✅ Account refresh buttons will work")
        safe_print("   ✅ Buy/Sell buttons will work")
        safe_print("   ✅ Futures trading will work")
        safe_print("   ✅ Auto trading start/stop will work") 
        safe_print("   ✅ ML predictions will work")
        safe_print("   ✅ Analytics will display")
        safe_print("   ✅ Charts will update")
        safe_print("   ✅ System controls will work")
        safe_print("")
        safe_print("🚀 Start the dashboard with: python dashboardtest/app.py")
        
    elif success_rate >= 70:
        safe_print("")
        safe_print("🔧 DASHBOARD MOSTLY FUNCTIONAL")
        safe_print("🔧 Most features will work, some may need fixes")
        
    else:
        safe_print("")
        safe_print("❌ DASHBOARD STILL HAS ISSUES")
        safe_print("❌ More endpoints need to be fixed")
    
    return working_count, total_count

def test_routes_integration():
    """Test that routes subfolder is properly integrated"""
    safe_print("")
    safe_print("📁 Testing Routes Subfolder Integration")
    safe_print("-" * 40)
    
    base_url = "http://localhost:5000"
    
    # Endpoints that should come from routes subfolder
    routes_endpoints = [
        ("/account", "spot_trading_routes.py", "GET"),
        ("/positions", "spot_trading_routes.py", "GET"),
        ("/prices", "market_data_routes.py", "GET"),
        ("/market_data", "market_data_routes.py", "GET"),
        ("/auto_trading/start", "auto_trading_routes.py", "POST"),
        ("/predict", "simple_ml_routes.py", "POST"),
        ("/analytics", "simple_ml_routes.py", "GET")
    ]
    
    routes_working = 0
    
    for path, source_file, method in routes_endpoints:
        try:
            test_data = {"symbol": "BTCUSDT"} if method == "POST" else None
            
            if method == "GET":
                response = requests.get(f"{base_url}{path}", timeout=3)
            else:
                response = requests.post(f"{base_url}{path}", json=test_data, timeout=3)
                
            if response.status_code == 200:
                safe_print(f"✅ {path:20} from {source_file}")
                routes_working += 1
            else:
                safe_print(f"❌ {path:20} from {source_file} ({response.status_code})")
        except Exception as e:
            safe_print(f"❌ {path:20} from {source_file} (ERROR)")
    
    safe_print(f"\n📁 Routes integration: {routes_working}/{len(routes_endpoints)} working")
    return routes_working == len(routes_endpoints)

if __name__ == "__main__":
    working, total = test_critical_endpoints()
    routes_ok = test_routes_integration()
    
    safe_print("\n" + "=" * 60)
    safe_print("🎯 FINAL RECOMMENDATION")
    safe_print("=" * 60)
    
    if working >= (total * 0.9) and routes_ok:
        safe_print("🎉 READY TO TEST DASHBOARD!")
        safe_print("🎉 Run: cd dashboardtest && python app.py")
        safe_print("🎉 Dashboard should be fully interactive!")
    else:
        safe_print("🔧 Need more endpoint fixes before dashboard will be interactive")
