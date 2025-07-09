#!/usr/bin/env python3
"""
Dashboard Button Testing Script
Test each button individually to identify which ones work and which don't
"""
import requests
import time
import json

# Dashboard and Backend URLs
DASHBOARD_URL = "http://localhost:8050"
BACKEND_URL = "http://localhost:5000"

def test_backend_connection():
    """Test if backend is responding"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and healthy")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return False

def test_dashboard_connection():
    """Test if dashboard is responding"""
    try:
        response = requests.get(DASHBOARD_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Dashboard is running")
            if "<!doctype html>" in response.text.lower():
                print("✅ Dashboard returned valid HTML")
                return True
            else:
                print("❌ Dashboard returned non-HTML content")
                return False
        else:
            print(f"❌ Dashboard returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Dashboard connection failed: {e}")
        return False

def test_critical_backend_endpoints():
    """Test the most critical backend endpoints that dashboard buttons use"""
    endpoints_to_test = [
        "/health",
        "/price/BTCUSDT", 
        "/ml/predict",
        "/auto_trading/status",
        "/trades",
        "/notifications",
        "/model/analytics",
        "/ml/current_signal"
    ]
    
    print("\n🔍 Testing Backend Endpoints:")
    print("-" * 40)
    
    working_endpoints = []
    failing_endpoints = []
    
    for endpoint in endpoints_to_test:
        try:
            response = requests.get(f"{BACKEND_URL}{endpoint}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {endpoint} - Status: {data.get('status', 'N/A')}")
                working_endpoints.append(endpoint)
            else:
                print(f"❌ {endpoint} - HTTP {response.status_code}")
                failing_endpoints.append(endpoint)
        except Exception as e:
            print(f"❌ {endpoint} - Error: {str(e)[:50]}...")
            failing_endpoints.append(endpoint)
    
    print(f"\n📊 Results: {len(working_endpoints)} working, {len(failing_endpoints)} failing")
    return working_endpoints, failing_endpoints

def check_dashboard_errors():
    """Check dashboard debug log for recent errors"""
    try:
        with open("dashboard_debug.log", "r") as f:
            lines = f.readlines()
            
        # Get last 20 lines
        recent_lines = lines[-20:]
        
        error_count = 0
        for line in recent_lines:
            if "ERROR" in line or "Exception" in line or "500" in line:
                print(f"🔍 {line.strip()}")
                error_count += 1
        
        if error_count == 0:
            print("✅ No recent errors in dashboard log")
        else:
            print(f"⚠️  Found {error_count} recent errors")
            
    except Exception as e:
        print(f"❌ Could not read dashboard log: {e}")

def main():
    print("🚀 Dashboard & Backend Testing")
    print("=" * 50)
    
    # Test connections
    backend_ok = test_backend_connection()
    dashboard_ok = test_dashboard_connection()
    
    if not backend_ok:
        print("\n❌ Backend is not working. Dashboard buttons will fail.")
        return
    
    if not dashboard_ok:
        print("\n❌ Dashboard is not loading properly.")
        return
    
    # Test backend endpoints
    working, failing = test_critical_backend_endpoints()
    
    # Check for dashboard errors
    print("\n🔍 Recent Dashboard Errors:")
    print("-" * 40)
    check_dashboard_errors()
    
    # Summary and recommendations
    print("\n📋 Summary & Next Steps:")
    print("-" * 40)
    
    if len(working) > len(failing):
        print("✅ Most backend endpoints are working")
        print("🔧 Focus on testing individual dashboard buttons")
        print("🔍 Use browser developer tools to check for JavaScript errors")
        print("📱 Interact with buttons and watch the debug logs")
    else:
        print("❌ Many backend endpoints are failing")
        print("🔧 Fix backend endpoints first before testing dashboard buttons")
    
    print(f"\n🌐 Dashboard URL: {DASHBOARD_URL}")
    print(f"🔧 Backend URL: {BACKEND_URL}")
    print("📋 Check browser console (F12) for JavaScript errors")
    print("📝 Watch dashboard_debug.log for callback activity")

if __name__ == "__main__":
    main()
