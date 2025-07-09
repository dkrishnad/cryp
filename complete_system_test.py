#!/usr/bin/env python3
"""
Complete System Integration Test
Test both backend functionality and dashboard integration
"""

import requests
import json
import time
from datetime import datetime

def test_backend_integration():
    """Test backend endpoints and dashboard integration"""
    
    base_url = "http://localhost:5000"
    
    print("🔍 COMPLETE SYSTEM INTEGRATION TEST")
    print("=" * 60)
    
    # Test 1: Backend Health
    print("\n1️⃣ Testing Backend Health...")
    try:
        health_resp = requests.get(f"{base_url}/health", timeout=5)
        if health_resp.status_code == 200:
            health_data = health_resp.json()
            print(f"✅ Backend Health: {health_data.get('status', 'Unknown')}")
            print(f"   Message: {health_data.get('message', 'No message')}")
        else:
            print(f"❌ Backend Health Failed: {health_resp.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend Connection Failed: {e}")
        return False
    
    # Test 2: Critical Endpoints
    print("\n2️⃣ Testing Critical Endpoints...")
    critical_endpoints = [
        ("/portfolio", "GET"),
        ("/trades", "GET"), 
        ("/model/analytics", "GET"),
        ("/futures/analytics", "GET"),
        ("/futures/account", "GET"),
        ("/futures/positions", "GET"),
        ("/futures/open_position", "POST"),
        ("/risk/portfolio_metrics", "GET"),
        ("/performance/dashboard", "GET")
    ]
    
    endpoint_results = []
    for endpoint, method in critical_endpoints:
        try:
            if method == "GET":
                resp = requests.get(f"{base_url}{endpoint}", timeout=5)
            else:
                resp = requests.post(f"{base_url}{endpoint}", json={"test": True}, timeout=5)
            
            if resp.status_code == 200:
                print(f"✅ {method} {endpoint}")
                endpoint_results.append(True)
            else:
                print(f"❌ {method} {endpoint} - {resp.status_code}")
                endpoint_results.append(False)
        except Exception as e:
            print(f"❌ {method} {endpoint} - Error: {str(e)[:50]}")
            endpoint_results.append(False)
    
    endpoint_success_rate = sum(endpoint_results) / len(endpoint_results) * 100
    print(f"\n   📊 Endpoint Success Rate: {endpoint_success_rate:.1f}%")
    
    # Test 3: Dashboard Specific Features
    print("\n3️⃣ Testing Dashboard Features...")
    
    # Test live price data (BTC is working)
    try:
        price_resp = requests.get(f"{base_url}/price/btcusdt", timeout=5)
        if price_resp.status_code == 200:
            price_data = price_resp.json()
            print(f"✅ Live BTC Price: {price_data.get('price', 'Unknown')}")
        else:
            print(f"❌ Live Price Failed: {price_resp.status_code}")
    except Exception as e:
        print(f"❌ Live Price Error: {str(e)[:50]}")
    
    # Test futures trading
    try:
        futures_data = {
            "symbol": "BTCUSDT",
            "side": "BUY", 
            "quantity": 0.01,
            "leverage": 10
        }
        futures_resp = requests.post(f"{base_url}/futures/open_position", json=futures_data, timeout=5)
        if futures_resp.status_code == 200:
            print("✅ Futures Trading Integration")
        else:
            print(f"❌ Futures Trading Failed: {futures_resp.status_code}")
    except Exception as e:
        print(f"❌ Futures Trading Error: {str(e)[:50]}")
    
    # Test ML model integration
    try:
        ml_resp = requests.get(f"{base_url}/model/analytics", timeout=5)
        if ml_resp.status_code == 200:
            print("✅ ML Model Integration")
        else:
            print(f"❌ ML Model Failed: {ml_resp.status_code}")
    except Exception as e:
        print(f"❌ ML Model Error: {str(e)[:50]}")
    
    # Test 4: Dashboard Component Endpoints
    print("\n4️⃣ Testing Dashboard Components...")
    dashboard_endpoints = [
        "/notifications",
        "/portfolio", 
        "/trades",
        "/performance/dashboard",
        "/features/indicators?symbol=btcusdt",
        "/risk/portfolio_metrics"
    ]
    
    dashboard_working = 0
    for endpoint in dashboard_endpoints:
        try:
            resp = requests.get(f"{base_url}{endpoint}", timeout=5)
            if resp.status_code == 200:
                print(f"✅ Dashboard: {endpoint}")
                dashboard_working += 1
            else:
                print(f"❌ Dashboard: {endpoint} - {resp.status_code}")
        except Exception as e:
            print(f"❌ Dashboard: {endpoint} - Error")
    
    dashboard_success_rate = dashboard_working / len(dashboard_endpoints) * 100
    print(f"\n   📊 Dashboard Component Success Rate: {dashboard_success_rate:.1f}%")
    
    # Final Assessment
    print("\n" + "=" * 60)
    print("🎯 FINAL SYSTEM ASSESSMENT")
    print("=" * 60)
    
    overall_score = (endpoint_success_rate + dashboard_success_rate) / 2
    
    if overall_score >= 90:
        print("🎉 EXCELLENT: System is fully functional!")
        print("   ✅ Backend endpoints working")
        print("   ✅ Dashboard integration working") 
        print("   ✅ Ready for production use")
        status = "EXCELLENT"
    elif overall_score >= 75:
        print("👍 GOOD: System is mostly functional")
        print("   ✅ Core features working")
        print("   ⚠️  Some minor issues may exist")
        print("   ✅ Ready for testing")
        status = "GOOD"
    elif overall_score >= 50:
        print("⚠️  FAIR: System has significant issues")
        print("   ⚠️  Some core features not working")
        print("   ❌ Needs fixes before production")
        status = "FAIR"
    else:
        print("❌ POOR: System needs major fixes")
        print("   ❌ Critical functionality broken")
        print("   ❌ Not ready for use")
        status = "POOR"
    
    print(f"\n📊 Overall Score: {overall_score:.1f}%")
    print(f"🏆 System Status: {status}")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if overall_score >= 90:
        print("   • System is ready!")
        print("   • Monitor for any edge cases")
        print("   • Consider adding more advanced features")
    elif overall_score >= 75:
        print("   • Fix remaining endpoint issues")
        print("   • Test all dashboard buttons")
        print("   • Verify real-time updates")
    else:
        print("   • Fix critical backend endpoints")
        print("   • Check callback registrations")
        print("   • Verify port configurations")
    
    return overall_score >= 75

if __name__ == "__main__":
    test_backend_integration()
