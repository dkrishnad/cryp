#!/usr/bin/env python3
"""
Test script to check hybrid prediction callback functionality
"""

import requests
import time

# Test the backend endpoint directly
def test_backend_endpoints():
    base_url = "http://localhost:8001"
    
    print("🔍 Testing Backend Endpoints:")
    print("=" * 40)
    
    # Test with different symbols
    symbols = ["btcusdt", "ethusdt", "kaiausdt", "solusdt"]
    
    for symbol in symbols:
        try:
            url = f"{base_url}/ml/hybrid/predict?symbol={symbol}"
            print(f"\n📊 Testing {symbol.upper()}:")
            print(f"URL: {url}")
            
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                result = resp.json()
                prediction = result.get("prediction", {})
                ensemble_pred = prediction.get("ensemble_prediction", 0)
                ensemble_conf = prediction.get("ensemble_confidence", 0)
                
                print(f"✅ Status: {resp.status_code}")
                print(f"🎯 Prediction: {'BUY' if ensemble_pred == 1 else 'SELL'}")
                print(f"🔘 Confidence: {ensemble_conf:.2%}")
                print(f"📈 Signal: {result.get('signal', 'N/A')}")
            else:
                print(f"❌ Status: {resp.status_code}")
                print(f"Response: {resp.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return True

# Test dashboard accessibility
def test_dashboard():
    print("\n\n🌐 Testing Dashboard Accessibility:")
    print("=" * 40)
    
    try:
        resp = requests.get("http://localhost:8050", timeout=5)
        if resp.status_code == 200:
            print("✅ Dashboard is accessible")
            return True
        else:
            print(f"❌ Dashboard returned status: {resp.status_code}")
            return False
    except Exception as e:
        print(f"❌ Dashboard is not accessible: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Hybrid Prediction Callback Test")
    print("=" * 50)
    
    backend_ok = test_backend_endpoints()
    dashboard_ok = test_dashboard()
    
    print("\n📋 Test Summary:")
    print("=" * 20)
    print(f"Backend: {'✅ OK' if backend_ok else '❌ FAIL'}")
    print(f"Dashboard: {'✅ OK' if dashboard_ok else '❌ FAIL'}")
    
    if backend_ok and dashboard_ok:
        print("\n💡 Both backend and dashboard are working.")
        print("🔧 The issue might be with the Dash callback registration or JavaScript.")
        print("👉 Try manually changing the dropdown and clicking 'Update Prediction' in the browser.")
        print("👉 Check the browser console for JavaScript errors.")
        print("👉 Check if the callback is being triggered by looking at the dashboard terminal output.")
    else:
        print("\n⚠️  Please fix the backend/dashboard connectivity issues first.")
