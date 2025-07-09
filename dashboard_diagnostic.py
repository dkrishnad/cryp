#!/usr/bin/env python3
"""
Dashboard Functionality Diagnostic
Tests why the dashboard is static and not responding
"""

import requests
import time
import json

def test_backend_connectivity():
    """Test if backend is running and responding"""
    print("🔍 TESTING BACKEND CONNECTIVITY")
    print("=" * 50)
    
    try:
        # Test basic health
        response = requests.get("http://localhost:5000/health", timeout=5)
        print(f"✅ Backend Health: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response: {data.get('status', 'No status')}")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is NOT running on port 5000")
        print("🔧 FIX: Start backend with: python main.py (in backendtest folder)")
        return False
    except Exception as e:
        print(f"❌ Backend error: {e}")
        return False
    
    return True

def test_critical_endpoints():
    """Test critical endpoints for dashboard functionality"""
    print("\n🔍 TESTING CRITICAL ENDPOINTS")
    print("=" * 50)
    
    critical_endpoints = [
        "/portfolio",
        "/trades", 
        "/futures/analytics",
        "/model/analytics",
        "/prices"
    ]
    
    working_endpoints = 0
    for endpoint in critical_endpoints:
        try:
            response = requests.get(f"http://localhost:5000{endpoint}", timeout=3)
            if response.status_code == 200:
                print(f"✅ {endpoint}: Working")
                working_endpoints += 1
            else:
                print(f"❌ {endpoint}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: Error - {str(e)[:50]}")
    
    print(f"\n📊 Working endpoints: {working_endpoints}/{len(critical_endpoints)}")
    return working_endpoints >= len(critical_endpoints) - 1  # Allow 1 failure

def test_websocket_connection():
    """Test WebSocket connection for real-time data"""
    print("\n🔍 TESTING WEBSOCKET CONNECTION")
    print("=" * 50)
    
    try:
        # Try to connect to WebSocket endpoint
        response = requests.get("http://localhost:5000/ws/price", timeout=3)
        print(f"WebSocket endpoint status: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ WebSocket connection failed: {e}")
        print("🔧 This may cause static dashboard behavior")
        return False

def test_frontend_backend_integration():
    """Test a typical frontend-to-backend call"""
    print("\n🔍 TESTING FRONTEND-BACKEND INTEGRATION")
    print("=" * 50)
    
    # Test data format that callbacks expect
    try:
        response = requests.get("http://localhost:5000/portfolio", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Portfolio endpoint working")
            
            # Check if data format matches what callbacks expect
            if isinstance(data, dict) and 'status' in data:
                print("✅ Data format correct")
                return True
            else:
                print("⚠️ Data format may not match callback expectations")
                print(f"Data structure: {type(data)}")
                return False
        else:
            print(f"❌ Portfolio endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def diagnose_static_dashboard():
    """Main diagnostic function"""
    print("🚨 DASHBOARD FUNCTIONALITY DIAGNOSTIC")
    print("=" * 60)
    print("Diagnosing why dashboard is static...")
    print("=" * 60)
    
    # Run all tests
    backend_ok = test_backend_connectivity()
    endpoints_ok = test_critical_endpoints()
    websocket_ok = test_websocket_connection()
    integration_ok = test_frontend_backend_integration()
    
    print("\n" + "=" * 60)
    print("📋 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    tests = [
        ("Backend Running", backend_ok),
        ("Critical Endpoints", endpoints_ok), 
        ("WebSocket Connection", websocket_ok),
        ("Integration Test", integration_ok)
    ]
    
    passed = sum(1 for _, status in tests if status)
    
    for test_name, status in tests:
        icon = "✅" if status else "❌"
        print(f"{icon} {test_name}")
    
    print(f"\n📊 Tests Passed: {passed}/{len(tests)}")
    
    # Provide specific fixes
    print("\n🔧 RECOMMENDED FIXES:")
    
    if not backend_ok:
        print("1. 🚀 START BACKEND:")
        print("   cd backendtest")
        print("   python main.py")
        
    if not endpoints_ok:
        print("2. 🔗 FIX ENDPOINTS:")
        print("   Some backend endpoints are not responding")
        print("   Check backend logs for errors")
        
    if not websocket_ok:
        print("3. 📡 FIX WEBSOCKET:")
        print("   WebSocket connection failed")
        print("   This causes static dashboard behavior")
        print("   Check if WebSocket routes are registered")
        
    if not integration_ok:
        print("4. 🔄 FIX DATA FORMAT:")
        print("   Backend data format may not match frontend expectations")
        print("   Check callback data parsing")
    
    if passed == len(tests):
        print("🎉 ALL TESTS PASSED!")
        print("📋 Dashboard should be functional")
        print("🔍 Check browser console for JavaScript errors")
    
    return passed, len(tests)

if __name__ == "__main__":
    passed, total = diagnose_static_dashboard()
    
    if passed < total:
        print(f"\n⚠️ {total - passed} issue(s) detected")
        print("🔧 Fix the issues above and restart the dashboard")
    else:
        print("\n✅ No obvious issues detected")
        print("🔍 Check browser developer console for frontend errors")
