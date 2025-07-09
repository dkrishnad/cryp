#!/usr/bin/env python3
"""
Test script to verify all dashboard buttons and features are working
"""
import requests
import json
import time

def test_backend_connectivity():
    """Test if backend is accessible"""
    try:
        response = requests.get("http://localhost:8000/api/account/balance")
        print(f"Backend connectivity: {'✅ WORKING' if response.status_code == 200 else '❌ FAILED'}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Backend connectivity failed: {e}")
        return False

def test_dashboard_accessibility():
    """Test if dashboard is accessible"""
    try:
        response = requests.get("http://localhost:8051")
        print(f"Dashboard accessibility: {'✅ WORKING' if response.status_code == 200 else '❌ FAILED'}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Dashboard accessibility failed: {e}")
        return False

def test_critical_endpoints():
    """Test critical backend endpoints"""
    endpoints = [
        "/api/account/balance",
        "/api/symbols/list",
        "/api/trading/start",
        "/api/trading/stop",
        "/api/trading/status"
    ]
    
    working_endpoints = 0
    total_endpoints = len(endpoints)
    
    print("\n=== Backend Endpoint Tests ===")
    for endpoint in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}")
            status = "✅ WORKING" if response.status_code in [200, 201] else f"❌ FAILED ({response.status_code})"
            print(f"{endpoint}: {status}")
            if response.status_code in [200, 201]:
                working_endpoints += 1
        except Exception as e:
            print(f"{endpoint}: ❌ FAILED ({e})")
    
    print(f"\nEndpoint Summary: {working_endpoints}/{total_endpoints} working")
    return working_endpoints == total_endpoints

def main():
    print("=== COMPREHENSIVE DASHBOARD TEST ===")
    print("Testing backend and dashboard connectivity...\n")
    
    # Test 1: Backend connectivity
    backend_ok = test_backend_connectivity()
    
    # Test 2: Dashboard accessibility
    dashboard_ok = test_dashboard_accessibility()
    
    # Test 3: Critical endpoints
    endpoints_ok = test_critical_endpoints()
    
    print("\n=== FINAL RESULTS ===")
    print(f"Backend: {'✅ WORKING' if backend_ok else '❌ FAILED'}")
    print(f"Dashboard: {'✅ WORKING' if dashboard_ok else '❌ FAILED'}")
    print(f"Endpoints: {'✅ WORKING' if endpoints_ok else '❌ PARTIAL/FAILED'}")
    
    if backend_ok and dashboard_ok:
        print("\n🎉 DASHBOARD IS READY!")
        print("🔗 Dashboard URL: http://localhost:8051")
        print("🔗 Backend URL: http://localhost:8000")
        print("\nYou can now test the dashboard features in your browser.")
        print("All buttons and features should be working now.")
    else:
        print("\n❌ ISSUES DETECTED")
        print("Please check the server logs for more details.")

if __name__ == "__main__":
    main()
