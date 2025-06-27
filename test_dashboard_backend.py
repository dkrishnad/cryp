#!/usr/bin/env python3
"""
Dashboard Backend Connectivity Tester
"""
import requests
import json

API_URL = "http://localhost:8001"

def test_endpoint(endpoint):
    """Test a single endpoint"""
    try:
        response = requests.get(f"{API_URL}{endpoint}", timeout=3)
        return {
            "status": response.status_code,
            "working": response.status_code == 200,
            "data": response.json() if response.status_code == 200 else None
        }
    except Exception as e:
        return {"status": "ERROR", "working": False, "data": str(e)}

def main():
    print("🔍 TESTING DASHBOARD BACKEND CONNECTIVITY")
    print("=" * 50)
    
    # Test key endpoints that dashboard depends on
    endpoints = [
        "/health",
        "/virtual_balance", 
        "/balance",
        "/price/BTCUSDT",
        "/features/indicators?symbol=BTCUSDT",
        "/trades",
        "/trades/recent", 
        "/trades/analytics",
        "/auto_trading/status",
        "/ml/data_collection/stats",
        "/model/analytics",
        "/email/config"
    ]
    
    working = 0
    total = len(endpoints)
    
    for endpoint in endpoints:
        result = test_endpoint(endpoint)
        status = "✅" if result["working"] else "❌"
        print(f"{status} {endpoint}: {result['status']}")
        if result["working"]:
            working += 1
    
    print(f"\n📊 RESULT: {working}/{total} endpoints working ({working/total*100:.0f}%)")
    
    if working < total:
        print("\n⚠️  DASHBOARD WILL HAVE MISSING DATA DUE TO BROKEN ENDPOINTS")
        print("💡 Start the backend: cd backend && uvicorn main:app --reload")
    else:
        print("\n🎉 ALL ENDPOINTS WORKING - DASHBOARD SHOULD BE FULLY FUNCTIONAL")

if __name__ == "__main__":
    main()
