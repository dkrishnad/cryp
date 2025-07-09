#!/usr/bin/env python3
"""
Dashboard Button Debugging Script
Test each button endpoint individually to identify what's not working
"""

import requests
import json
from datetime import datetime

API_URL = "http://localhost:5000"

def test_endpoint(method, endpoint, description, data=None):
    """Test a specific endpoint and report results"""
    print(f"\n🔧 Testing: {description}")
    print(f"   Endpoint: {method.upper()} {endpoint}")
    
    try:
        if method.lower() == 'get':
            response = requests.get(f"{API_URL}{endpoint}", timeout=10)
        elif method.lower() == 'post':
            response = requests.post(f"{API_URL}{endpoint}", json=data or {}, timeout=10)
        else:
            print(f"   ❌ Unsupported method: {method}")
            return False
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"   ✅ SUCCESS: {result.get('status', 'No status')}")
                if 'message' in result:
                    print(f"   📝 Message: {result['message']}")
                return True
            except:
                print(f"   ✅ SUCCESS: Response received but not JSON")
                return True
        else:
            print(f"   ❌ FAILED: HTTP {response.status_code}")
            try:
                error = response.json()
                print(f"   📝 Error: {error}")
            except:
                print(f"   📝 Error: {response.text[:100]}...")
            return False
            
    except requests.exceptions.Timeout:
        print(f"   ⏱️ TIMEOUT: Request timed out")
        return False
    except requests.exceptions.ConnectionError:
        print(f"   🔌 CONNECTION ERROR: Cannot connect to backend")
        return False
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False

def main():
    print("Dashboard Button Endpoint Testing")
    print("=" * 60)
    print(f"Backend URL: {API_URL}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test basic connectivity
    print("\n" + "="*60)
    print("1. BASIC CONNECTIVITY TESTS")
    print("="*60)
    
    basic_tests = [
        ("GET", "/", "Root endpoint"),
        ("GET", "/health", "Health check"),
        ("GET", "/price/BTCUSDT", "Price fetch (working feature)"),
    ]
    
    basic_working = 0
    for method, endpoint, desc in basic_tests:
        if test_endpoint(method, endpoint, desc):
            basic_working += 1
    
    print(f"\n📊 Basic connectivity: {basic_working}/{len(basic_tests)} working")
    
    # Test feature buttons that should work
    print("\n" + "="*60)
    print("2. FEATURE BUTTON ENDPOINT TESTS")
    print("="*60)
    
    feature_tests = [
        ("GET", "/model/versions", "Model versions (refresh button)"),
        ("GET", "/model/analytics", "Model analytics"),
        ("GET", "/ml/predict?symbol=btcusdt", "ML prediction"),
        ("GET", "/ml/current_signal", "Current trading signal"),
        ("GET", "/auto_trading/status", "Auto trading status"),
        ("GET", "/trades", "Get trades"),
        ("GET", "/balance", "Get balance"),
        ("GET", "/notifications", "Get notifications"),
        ("GET", "/features/indicators?symbol=btcusdt", "Technical indicators"),
        ("POST", "/ml/tune_models", "Tune models", {"symbol": "BTCUSDT", "hyperparameters": {}}),
        ("GET", "/ml/online/stats", "Online learning stats"),
        ("GET", "/ml/data_collection/stats", "Data collection stats"),
    ]
    
    feature_working = 0
    for method, endpoint, desc, *data in feature_tests:
        test_data = data[0] if data else None
        if test_endpoint(method, endpoint, desc, test_data):
            feature_working += 1
    
    print(f"\n📊 Feature endpoints: {feature_working}/{len(feature_tests)} working")
    
    # Test auto trading endpoints
    print("\n" + "="*60)
    print("3. AUTO TRADING ENDPOINT TESTS")
    print("="*60)
    
    auto_trading_tests = [
        ("GET", "/auto_trading/status", "Auto trading status"),
        ("GET", "/auto_trading/signals", "Auto trading signals"),
        ("POST", "/auto_trading/toggle", "Toggle auto trading", {"enabled": True}),
    ]
    
    auto_working = 0
    for method, endpoint, desc, *data in auto_trading_tests:
        test_data = data[0] if data else None
        if test_endpoint(method, endpoint, desc, test_data):
            auto_working += 1
    
    print(f"\n📊 Auto trading endpoints: {auto_working}/{len(auto_trading_tests)} working")
    
    # Summary
    total_tests = len(basic_tests) + len(feature_tests) + len(auto_trading_tests)
    total_working = basic_working + feature_working + auto_working
    
    print("\n" + "="*60)
    print("📊 FINAL SUMMARY")
    print("="*60)
    print(f"Total endpoints tested: {total_tests}")
    print(f"Working endpoints: {total_working}")
    print(f"Failed endpoints: {total_tests - total_working}")
    print(f"Success rate: {(total_working/total_tests)*100:.1f}%")
    
    if total_working == total_tests:
        print("\n🎉 ALL ENDPOINTS WORKING! The issue is likely in the dashboard callbacks.")
    elif total_working == 0:
        print("\n⚠️  NO ENDPOINTS WORKING! Backend may not be running correctly.")
    else:
        print(f"\n🔧 PARTIAL SUCCESS: {total_tests - total_working} endpoints need fixing.")
    
    print("\n💡 Next steps:")
    if total_working < total_tests:
        print("   1. Fix failed backend endpoints")
        print("   2. Check callback registration in dashboard")
        print("   3. Verify button IDs match between layout and callbacks")
    else:
        print("   1. Check dashboard callback registration")
        print("   2. Verify button click handlers are working")
        print("   3. Check browser console for JavaScript errors")

if __name__ == "__main__":
    main()
