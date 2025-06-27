#!/usr/bin/env python3
"""
Test script to verify the Streamlit app functionality
"""
import requests
import time

def test_app_response():
    """Test if the app responds correctly"""
    try:
        response = requests.get("http://localhost:8502", timeout=5)
        print(f"✅ App Status: {response.status_code}")
        print(f"✅ Response Time: {response.elapsed.total_seconds():.2f}s")        
        # Check if key content is present
        content = response.text.lower()
        
        tests = {
            "Streamlit App": "streamlit" in content,
            "Trading Dashboard": "dashboard" in content or "bot stats" in content,
            "Decimal Scalping": "decimal" in content or "scalping" in content,
            "Multi-Coin Scanner": "multi-coin" in content or "scanner" in content,
            "Auto Trading": "auto trading" in content,
            "Trading Buttons": "long" in content and "short" in content,
            "Virtual Balance": "balance" in content or "virtual" in content,
            "Backtesting": "backtest" in content,
            "Futures Trading": "futures" in content
        }
        
        print("\n🧪 Content Tests:")
        for test_name, passed in tests.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"  {status}: {test_name}")
        
        all_passed = all(tests.values())
        print(f"\n🎯 Overall Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
        
        return all_passed
        
    except requests.exceptions.ConnectionError:
        print("❌ App is not running or not accessible at http://localhost:8502")
        return False
    except Exception as e:
        print(f"❌ Error testing app: {e}")
        return False

def test_api_endpoints():
    """Test if the app's API endpoints work"""
    try:
        # Test Binance API (used by the app)
        response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5)
        if response.status_code == 200:
            price_data = response.json()
            print(f"✅ Binance API: BTC Price = ${float(price_data['price']):.2f}")
            return True
        else:
            print(f"❌ Binance API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Streamlit Crypto Trading Bot...")
    print("=" * 50)
    
    # Test 1: App Response
    app_test = test_app_response()
    
    print("\n" + "=" * 50)
    
    # Test 2: API Connectivity
    api_test = test_api_endpoints()
    
    print("\n" + "=" * 50)
    print("📋 FINAL RESULTS:")
    print(f"  App Running: {'✅ YES' if app_test else '❌ NO'}")
    print(f"  API Working: {'✅ YES' if api_test else '❌ NO'}")
    
    if app_test and api_test:
        print("\n🎉 SUCCESS: App is ready for testing!")
        print("👉 Open http://localhost:8502 in your browser")
        print("👉 Navigate to 'Decimal Scalping' tab")
        print("👉 Click LONG/SHORT buttons to test functionality")
    else:
        print("\n⚠️  Issues detected. Check the app and try again.")
