#!/usr/bin/env python3
"""
Test to simulate the dashboard callback logic
"""

import requests
import json
from datetime import datetime

# Backend URL
API_URL = "http://localhost:8001"

def test_prediction_callback(symbol="btcusdt", n_clicks=None, n_intervals=0):
    """Simulate the hybrid prediction callback"""
    print(f"🔍 TESTING CALLBACK: symbol={symbol}, n_clicks={n_clicks}, n_intervals={n_intervals}")
    
    try:
        resp = requests.get(f"{API_URL}/ml/hybrid/predict?symbol={symbol}", timeout=5)
        if resp.status_code == 200:
            result = resp.json()
            prediction = result.get("prediction", {})
            
            ensemble_pred = prediction.get("ensemble_prediction", 0)
            ensemble_conf = prediction.get("ensemble_confidence", 0)
            
            print(f"✅ Response received successfully")
            print(f"📊 Symbol: {symbol.upper()}")
            print(f"🎯 Ensemble Prediction: {'BUY' if ensemble_pred == 1 else 'SELL'}")
            print(f"📈 Confidence: {ensemble_conf:.2%}")
            
            # Show what would be displayed
            batch_pred = prediction.get("batch_prediction", "N/A")
            individual_preds = prediction.get("individual_predictions", {})
            
            print(f"🤖 Batch Model: {batch_pred}")
            print(f"🔄 Online Models:")
            for name, pred in individual_preds.items():
                print(f"  - {name}: {pred}")
            
            return True
        else:
            print(f"❌ HTTP Error: {resp.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def test_multiple_symbols():
    """Test multiple symbols to verify different responses"""
    symbols = ["btcusdt", "kaiausdt", "ethusdt", "solusdt"]
    
    print("🌐 Testing Multiple Symbols:")
    print("=" * 50)
    
    for i, symbol in enumerate(symbols):
        print(f"\n{i+1}. Testing {symbol.upper()}:")
        print("-" * 30)
        test_prediction_callback(symbol, n_clicks=1, n_intervals=i)

if __name__ == "__main__":
    print("🚀 Dashboard Callback Logic Test")
    print("=" * 50)
    
    # Test default case (page load)
    print("\n📋 Test 1: Page Load (n_intervals=0)")
    test_prediction_callback()
    
    # Test button click
    print("\n📋 Test 2: Button Click (n_clicks=1)")
    test_prediction_callback(n_clicks=1)
    
    # Test symbol change
    print("\n📋 Test 3: Symbol Change")
    test_prediction_callback(symbol="kaiausdt")
    
    # Test multiple symbols
    test_multiple_symbols()
    
    print("\n🏁 Test Complete!")
    print("💡 If this works but the dashboard doesn't update, the issue is likely:")
    print("   1. Dash callback registration problem")
    print("   2. HTML element ID mismatch")
    print("   3. Browser-side JavaScript issue")
    print("   4. Callback output not being applied to the correct element")
