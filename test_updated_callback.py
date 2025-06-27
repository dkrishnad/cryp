#!/usr/bin/env python3
"""
Test the updated hybrid prediction callback logic
"""
import requests
import json
from datetime import datetime

API_URL = "http://localhost:8001"

def test_updated_callback_logic():
    """Test the updated callback logic that properly handles nested predictions"""
    print("🔄 Testing Updated Hybrid Prediction Callback Logic")
    print("=" * 60)
    
    symbol = "kaiausdt"
    
    try:
        # Simulate the callback
        resp = requests.get(f"{API_URL}/ml/hybrid/predict?symbol={symbol}", timeout=5)
        if resp.status_code == 200:
            result = resp.json()
            prediction = result.get("prediction", {})
            
            # Extract data like the updated callback does
            ensemble_pred = prediction.get("ensemble_prediction", 0)
            ensemble_conf = prediction.get("ensemble_confidence", 0)
            timestamp = prediction.get("timestamp", "Unknown")
            
            # Get individual predictions from nested structure
            online_predictions = prediction.get("online_predictions", {})
            individual_preds = online_predictions.get("individual_predictions", {})
            
            print(f"✅ Callback Logic Test Results:")
            print(f"   📊 Symbol: {symbol.upper()}")
            print(f"   🎯 Ensemble Prediction: {'📈 BUY' if ensemble_pred == 1 else '📉 SELL'}")
            print(f"   📈 Confidence: {ensemble_conf:.2%}")
            print(f"   🕒 Timestamp: {timestamp}")
            print(f"   🤖 Batch Prediction: {prediction.get('batch_prediction', 'N/A')}")
            print(f"   🧠 Individual Models:")
            
            if individual_preds:
                for name, pred in individual_preds.items():
                    signal = 'BUY' if pred == 1 else 'SELL' if pred == -1 else 'HOLD'
                    print(f"      • {name}: {signal}")
            else:
                print("      • No online models found")
            
            # Check if this represents new data
            current_time = datetime.now()
            if timestamp != "Unknown":
                try:
                    pred_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00').replace('+00:00', ''))
                    time_diff = (current_time - pred_time).total_seconds()
                    print(f"   ⏱️  Prediction age: {time_diff:.1f} seconds")
                    
                    if time_diff < 5:
                        print("   ✅ Fresh prediction (< 5 seconds old)")
                    elif time_diff < 30:
                        print("   ⚠️  Recent prediction (< 30 seconds old)")
                    else:
                        print("   ❌ Old prediction (> 30 seconds old)")
                except:
                    print("   ⚠️  Could not parse timestamp")
            
        else:
            print(f"❌ API Error: {resp.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def test_multiple_symbols():
    """Test predictions for multiple symbols"""
    print(f"\n🔄 Testing Multiple Symbols")
    print("=" * 60)
    
    symbols = ["btcusdt", "kaiausdt", "ethusdt", "solusdt"]
    
    for symbol in symbols:
        try:
            resp = requests.get(f"{API_URL}/ml/hybrid/predict?symbol={symbol}", timeout=5)
            if resp.status_code == 200:
                result = resp.json()
                prediction = result.get("prediction", {})
                
                ensemble_pred = prediction.get("ensemble_prediction", 0)
                ensemble_conf = prediction.get("ensemble_confidence", 0)
                signal = '📈 BUY' if ensemble_pred == 1 else '📉 SELL'
                
                print(f"📊 {symbol.upper()}: {signal} ({ensemble_conf:.1%})")
                
            else:
                print(f"❌ {symbol.upper()}: API Error {resp.status_code}")
                
        except Exception as e:
            print(f"❌ {symbol.upper()}: Exception {str(e)}")

def check_dashboard_auto_refresh():
    """Check if the dashboard should auto-refresh"""
    print(f"\n🔄 Dashboard Auto-Refresh Analysis")
    print("=" * 60)
    
    print("📝 Dashboard Auto-Refresh Configuration:")
    print("   • Refresh Interval: 30 seconds")
    print("   • Callback Inputs: Button clicks, Symbol selector, Auto-refresh timer")
    print("   • Expected Behavior: Updates every 30 seconds automatically")
    print()
    
    # Test if timestamps are updating (indicating fresh predictions)
    print("🧪 Testing Timestamp Updates:")
    timestamps = []
    
    for i in range(2):
        try:
            resp = requests.get(f"{API_URL}/ml/hybrid/predict?symbol=kaiausdt", timeout=5)
            if resp.status_code == 200:
                result = resp.json()
                timestamp = result.get("prediction", {}).get("timestamp")
                timestamps.append(timestamp)
                print(f"   Call {i+1}: {timestamp}")
            
            if i == 0:
                import time
                time.sleep(2)  # Wait 2 seconds between calls
                
        except Exception as e:
            print(f"   Call {i+1}: Error - {str(e)}")
    
    if len(timestamps) >= 2 and timestamps[0] != timestamps[1]:
        print("   ✅ Timestamps are updating - predictions are fresh")
        print("   💡 Dashboard should show live updates every 30 seconds")
    else:
        print("   ⚠️  Timestamps are not updating - check if ML system is active")

if __name__ == "__main__":
    test_updated_callback_logic()
    test_multiple_symbols()
    check_dashboard_auto_refresh()
    
    print("\n" + "=" * 60)
    print("🎯 Summary:")
    print("• Updated callback now properly extracts nested individual predictions")
    print("• Timestamps are displayed to show when predictions were generated")
    print("• Dashboard should auto-refresh every 30 seconds")
    print("• If dashboard still shows static data, check browser console for errors")
    print("\n💡 Next Steps:")
    print("1. Refresh your browser tab with the dashboard")
    print("2. Check if predictions update automatically every 30 seconds") 
    print("3. Try clicking the '🔄 Update Prediction' button manually")
    print("4. Switch between different symbols in the dropdown")
