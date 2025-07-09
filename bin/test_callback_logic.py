#!/usr/bin/env python3
"""
Direct test of hybrid prediction callback logic
"""

import requests

API_URL = "http://localhost:8001"

def test_prediction_logic():
    """Test the same logic as the hybrid prediction callback"""
    
    symbols = ["btcusdt", "ethusdt", "kaiausdt", "solusdt"]
    
    print("🧪 Testing Hybrid Prediction Callback Logic")
    print("=" * 50)
    
    for symbol in symbols:
        print(f"\n🔍 Testing symbol: {symbol}")
        try:
            resp = requests.get(f"{API_URL}/ml/hybrid/predict?symbol={symbol}", timeout=5)
            if resp.status_code == 200:
                result = resp.json()
                prediction = result.get("prediction", {})
                
                ensemble_pred = prediction.get("ensemble_prediction", 0)
                ensemble_conf = prediction.get("ensemble_confidence", 0)
                
                print(f"✅ Backend Response: OK")
                print(f"📊 Ensemble Prediction: {ensemble_pred}")
                print(f"📈 Signal: {'BUY' if ensemble_pred == 1 else 'SELL'}")
                print(f"🎯 Confidence: {ensemble_conf:.2%}")
                
                # Test the individual predictions part
                individual_preds = prediction.get("individual_predictions", {})
                print(f"🤖 Individual Models: {list(individual_preds.keys())}")
                for name, pred in individual_preds.items():
                    print(f"  - {name}: {pred}")
                
                # This should be the same logic as in the callback
                prediction_display_items = [
                    f"Ensemble: {'BUY' if ensemble_pred == 1 else 'SELL'} ({ensemble_conf:.2%})",
                    f"Batch Model: {prediction.get('batch_prediction', 'N/A')}",
                    f"Online Models: {len(individual_preds)} models"
                ]
                
                print(f"🖥️  UI Display would show: {prediction_display_items}")
                
            else:
                print(f"❌ Backend Error: {resp.status_code}")
                print(f"Response: {resp.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n📋 Summary:")
    print("- If this test shows different results for different symbols, the backend is working")
    print("- If the dashboard doesn't update, the issue is in the frontend callback")
    print("- Check the dashboard logs for the debug message when changing symbols or clicking buttons")

if __name__ == "__main__":
    test_prediction_logic()
