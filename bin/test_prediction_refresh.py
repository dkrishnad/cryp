#!/usr/bin/env python3
"""
Test to verify if hybrid predictions are updating automatically
"""
import requests
import time
import json
from datetime import datetime

API_URL = "http://localhost:8001"

def test_prediction_refresh():
    """Test if predictions are updating over time"""
    print("🔄 Testing Hybrid Prediction Auto-Refresh")
    print("=" * 50)
    
    symbols = ["kaiausdt", "btcusdt"]
    
    for symbol in symbols:
        print(f"\n📊 Testing {symbol.upper()}:")
        print("-" * 30)
        
        predictions = []
        
        # Get 3 predictions with 10-second intervals
        for i in range(3):
            try:
                resp = requests.get(f"{API_URL}/ml/hybrid/predict?symbol={symbol}", timeout=5)
                if resp.status_code == 200:
                    result = resp.json()
                    prediction = result.get("prediction", {})
                    timestamp = result.get("timestamp")
                    ensemble_pred = prediction.get("ensemble_prediction", 0)
                    ensemble_conf = prediction.get("ensemble_confidence", 0)
                    
                    predictions.append({
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "api_timestamp": timestamp,
                        "prediction": ensemble_pred,
                        "confidence": ensemble_conf,
                        "signal": "BUY" if ensemble_pred == 1 else "SELL"
                    })
                    
                    print(f"  [{predictions[-1]['time']}] {predictions[-1]['signal']} - Confidence: {ensemble_conf:.2%}")
                    print(f"    API Timestamp: {timestamp}")
                    
                else:
                    print(f"  ❌ Error: {resp.status_code}")
                    
            except Exception as e:
                print(f"  ❌ Exception: {str(e)}")
            
            if i < 2:  # Don't wait after the last request
                print("    ⏳ Waiting 10 seconds...")
                time.sleep(10)
        
        # Analyze changes
        print(f"\n📈 Analysis for {symbol.upper()}:")
        if len(predictions) >= 2:
            timestamps_changed = len(set(p["api_timestamp"] for p in predictions)) > 1
            predictions_changed = len(set(p["prediction"] for p in predictions)) > 1
            confidences_changed = len(set(f"{p['confidence']:.4f}" for p in predictions)) > 1
            
            print(f"  • Timestamps changing: {'✅ YES' if timestamps_changed else '❌ NO'}")
            print(f"  • Predictions changing: {'✅ YES' if predictions_changed else '❌ NO'}")
            print(f"  • Confidences changing: {'✅ YES' if confidences_changed else '❌ NO'}")
            
            if not timestamps_changed:
                print("  ⚠️  API timestamps are not updating - this indicates the model isn't generating new predictions")
            elif not (predictions_changed or confidences_changed):
                print("  ⚠️  Predictions are consistent (this might be expected if market conditions are stable)")
        
        print()

def test_dashboard_callback_simulation():
    """Simulate the dashboard callback to see if it works"""
    print("\n🖥️  Dashboard Callback Simulation")
    print("=" * 50)
    
    # Simulate the callback logic
    symbol = "kaiausdt"
    n_clicks = 1
    n_intervals = 5
    
    print(f"🔍 Simulating callback: symbol={symbol}, n_clicks={n_clicks}, n_intervals={n_intervals}")
    
    try:
        resp = requests.get(f"{API_URL}/ml/hybrid/predict?symbol={symbol}", timeout=5)
        if resp.status_code == 200:
            result = resp.json()
            prediction = result.get("prediction", {})
            
            ensemble_pred = prediction.get("ensemble_prediction", 0)
            ensemble_conf = prediction.get("ensemble_confidence", 0)
            
            print(f"✅ Callback would show:")
            print(f"   Signal: {'📈 BUY' if ensemble_pred == 1 else '📉 SELL'}")
            print(f"   Confidence: {ensemble_conf:.2%}")
            print(f"   Timestamp: {result.get('timestamp')}")
            
            # Show individual predictions
            individual = prediction.get("individual_predictions", {})
            print(f"   Individual models: {individual}")
            
        else:
            print(f"❌ Callback would show error: {resp.status_code}")
            
    except Exception as e:
        print(f"❌ Callback would show error: {str(e)}")

if __name__ == "__main__":
    test_prediction_refresh()
    test_dashboard_callback_simulation()
    
    print("\n" + "=" * 50)
    print("🔍 Key Points to Check:")
    print("1. Are timestamps updating? (Model generating new predictions)")
    print("2. Are predictions/confidences changing? (Model adapting)")
    print("3. Is the dashboard auto-refresh working every 30 seconds?")
    print("4. Are you clicking the '🔄 Update Prediction' button manually?")
    print("\n💡 If timestamps aren't updating, the ML model might need retraining")
    print("💡 If dashboard isn't refreshing, check browser console for errors")
