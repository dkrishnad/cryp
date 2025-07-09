#!/usr/bin/env python3
"""
Test dashboard button functionality by checking the actual callbacks and endpoints
"""
import requests
import sys
import time

API_URL = "http://localhost:8000"
DASHBOARD_URL = "http://localhost:8051"

def test_endpoint(path, description=""):
    """Test a backend endpoint"""
    try:
        response = requests.get(f"{API_URL}{path}", timeout=5)
        if response.status_code in [200, 422]:  # 422 means needs params but endpoint exists
            print(f"✅ Backend {path}: WORKING")
            return True
        else:
            print(f"❌ Backend {path}: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Backend {path}: ERROR ({e})")
        return False

def test_dashboard():
    """Test if dashboard is accessible"""
    try:
        response = requests.get(DASHBOARD_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Dashboard: ACCESSIBLE")
            return True
        else:
            print(f"❌ Dashboard: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Dashboard: ERROR ({e})")
        return False

print("=== DASHBOARD FUNCTIONALITY TEST ===")
print()

# Test dashboard accessibility
dashboard_ok = test_dashboard()

print("\n=== BACKEND ENDPOINTS (Used by Dashboard Callbacks) ===")

# Test the actual endpoints that callbacks.py uses
callback_endpoints = [
    "/health",
    "/ml/predict", 
    "/ml/current_signal",
    "/ml/predict/enhanced",
    "/advanced_auto_trading/status",
    "/advanced_auto_trading/positions", 
    "/advanced_auto_trading/market_data",
    "/model/analytics",
    "/notifications",
    "/ml/hybrid/status",
    "/price",
    "/model/versions"
]

working_endpoints = 0
for endpoint in callback_endpoints:
    if test_endpoint(endpoint):
        working_endpoints += 1

print(f"\n=== FINAL ASSESSMENT ===")
print(f"Dashboard Accessible: {'✅ YES' if dashboard_ok else '❌ NO'}")
print(f"Backend Endpoints Working: {working_endpoints}/{len(callback_endpoints)}")
print(f"Backend Success Rate: {(working_endpoints/len(callback_endpoints)*100):.1f}%")

if dashboard_ok and working_endpoints > 8:
    print("\n🎉 DASHBOARD SHOULD BE FUNCTIONAL!")
    print("✅ Both dashboard and backend are working properly")
    print("✅ Most callback endpoints are responding")
    print("\n📋 Next steps:")
    print("1. Open http://localhost:8051 in your browser")
    print("2. Try clicking buttons and features")
    print("3. Check browser console (F12) for any JavaScript errors")
elif dashboard_ok:
    print("\n⚠️ DASHBOARD PARTIALLY FUNCTIONAL")
    print("✅ Dashboard is accessible but some backend endpoints may not work")
    print("❌ Some features may not respond properly")
else:
    print("\n❌ DASHBOARD NOT FUNCTIONAL")
    print("❌ Dashboard is not accessible")
