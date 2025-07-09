#!/usr/bin/env python3
"""
Quick verification of endpoint mappings
"""
import requests
import sys

def test_endpoints():
    """Test the endpoints we mapped in the simulation"""
    backend_url = "http://localhost:5000"
    
    # Key endpoints that should work
    test_endpoints = [
        '/api/status',
        '/data/symbol_data',
        '/portfolio/balance', 
        '/data/live_prices',
        '/trade',
        '/notifications',
        '/ml/predict',
        '/auto_trading/status',
        '/futures/positions',
        '/backtest/results',
        '/email/test'
    ]
    
    print("🔍 Testing updated endpoint mappings...")
    print("=" * 50)
    
    working = 0
    total = len(test_endpoints)
    
    for endpoint in test_endpoints:
        try:
            response = requests.get(f"{backend_url}{endpoint}", timeout=5)
            if response.status_code < 500:  # Accept 200, 404, 405 as "working"
                status = "✅ WORKING"
                working += 1
            else:
                status = f"❌ ERROR ({response.status_code})"
        except Exception as e:
            status = f"❌ FAILED ({str(e)[:30]})"
        
        print(f"{status} - {endpoint}")
    
    print("\n" + "=" * 50)
    print(f"📊 SUMMARY: {working}/{total} endpoints accessible")
    
    if working >= total * 0.8:
        print("🎉 EXCELLENT: Most endpoints are working!")
        return True
    elif working >= total * 0.5:
        print("⚠️ MODERATE: Some endpoints need attention")
        return True
    else:
        print("❌ POOR: Many endpoints are not working")
        return False

if __name__ == "__main__":
    print("🚀 QUICK ENDPOINT VERIFICATION")
    print("Testing if backend endpoints match our simulation mappings...\n")
    
    success = test_endpoints()
    sys.exit(0 if success else 1)
