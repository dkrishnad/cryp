#!/usr/bin/env python3
"""
Add missing signal generation endpoint to main.py for auto trading
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

# Test if we can generate a signal using hybrid predictions
import requests

API_URL = "http://localhost:8001"

def test_signal_generation_options():
    """Test different ways to generate signals for auto trading"""
    print("🔍 Auto Trading Signal Generation Analysis")
    print("=" * 60)
    
    # Option 1: Check if we can use hybrid predictions
    print("📊 Option 1: Using Hybrid Predictions for Auto Trading")
    try:
        resp = requests.get(f"{API_URL}/ml/hybrid/predict?symbol=kaiausdt", timeout=5)
        if resp.status_code == 200:
            result = resp.json()
            prediction = result.get("prediction", {})
            
            ensemble_pred = prediction.get("ensemble_prediction", 0)
            ensemble_conf = prediction.get("ensemble_confidence", 0)
            signal = prediction.get("signal", "HOLD")
            timestamp = prediction.get("timestamp")
            
            print(f"   ✅ Hybrid prediction available:")
            print(f"      Signal: {signal}")
            print(f"      Confidence: {ensemble_conf:.2%}")
            print(f"      Prediction: {ensemble_pred}")
            print(f"      Timestamp: {timestamp}")
            
            # Convert to auto trading format
            if ensemble_conf > 0.60:  # 60% confidence threshold
                auto_signal = {
                    "timestamp": timestamp,
                    "symbol": "KAIAUSDT", 
                    "direction": signal,
                    "confidence": ensemble_conf * 100,
                    "current_price": "N/A",
                    "source": "hybrid_ml"
                }
                print(f"   💡 Auto trading signal would be: {auto_signal}")
            else:
                print(f"   ⚠️  Confidence {ensemble_conf:.1%} below 60% threshold - no signal")
                
        else:
            print(f"   ❌ Hybrid prediction failed: {resp.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Option 2: Check if original signal generation exists
    print(f"\n🛠️  Option 2: Check Available Endpoints")
    try:
        # Test various possible signal endpoints
        endpoints_to_test = [
            "/auto_trading/signals",
            "/auto_trading/current_signal", 
            "/signals",
            "/trading_signals"
        ]
        
        for endpoint in endpoints_to_test:
            try:
                resp = requests.get(f"{API_URL}{endpoint}", timeout=3)
                print(f"   {endpoint}: {resp.status_code} - {resp.json() if resp.status_code == 200 else 'Error'}")
            except:
                print(f"   {endpoint}: Not available")
                
    except Exception as e:
        print(f"   ❌ Error testing endpoints: {str(e)}")

def create_signal_from_hybrid_prediction():
    """Create a live signal using hybrid predictions"""
    print(f"\n🎯 Creating Live Signal from Hybrid Predictions")
    print("=" * 60)
    
    try:
        # Get prediction for KAIA/USDT (current auto trading symbol)
        resp = requests.get(f"{API_URL}/ml/hybrid/predict?symbol=kaiausdt", timeout=5)
        if resp.status_code == 200:
            result = resp.json()
            prediction = result.get("prediction", {})
            
            ensemble_pred = prediction.get("ensemble_prediction", 0)
            ensemble_conf = prediction.get("ensemble_confidence", 0)
            signal = prediction.get("signal", "HOLD")
            timestamp = prediction.get("timestamp")
            
            # Set confidence threshold (configurable)
            confidence_threshold = 0.60  # 60%
            
            if ensemble_conf >= confidence_threshold:
                # Create signal data
                signal_data = {
                    "timestamp": timestamp,
                    "symbol": "KAIAUSDT",
                    "direction": signal,
                    "confidence": round(ensemble_conf * 100, 2),
                    "ml_prediction": ensemble_pred,
                    "source": "hybrid_learning",
                    "threshold_met": True
                }
                
                print(f"✅ Generated Auto Trading Signal:")
                print(f"   📊 Symbol: {signal_data['symbol']}")
                print(f"   🎯 Direction: {signal_data['direction']}")
                print(f"   📈 Confidence: {signal_data['confidence']}%")
                print(f"   🤖 ML Prediction: {signal_data['ml_prediction']}")
                print(f"   🕒 Timestamp: {signal_data['timestamp']}")
                print(f"   ✅ Above {confidence_threshold*100}% threshold")
                
                return signal_data
                
            else:
                print(f"⚠️  Signal confidence {ensemble_conf:.1%} below {confidence_threshold:.1%} threshold")
                print(f"   📊 Current prediction: {signal} ({ensemble_conf:.2%})")
                print(f"   💡 No trading signal generated")
                
                return {
                    "timestamp": timestamp,
                    "symbol": "KAIAUSDT", 
                    "direction": "NO SIGNAL",
                    "confidence": 0.0,
                    "threshold_met": False,
                    "reason": f"Confidence {ensemble_conf:.1%} < {confidence_threshold:.1%}"
                }
                
        else:
            print(f"❌ Failed to get hybrid prediction: {resp.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating signal: {str(e)}")
        return None

if __name__ == "__main__":
    test_signal_generation_options()
    signal = create_signal_from_hybrid_prediction()
    
    print(f"\n" + "=" * 60)
    print("🎯 Summary & Solution:")
    print("• Auto trading dashboard expects signals from /auto_trading/signals")
    print("• Current main.py only stores historical signals, doesn't generate new ones")
    print("• Hybrid ML system IS generating live predictions")
    print("• Solution: Add signal generation endpoint that uses hybrid predictions")
    print(f"\n💡 Next Steps:")
    print("1. Add signal generation endpoint to main.py")
    print("2. Use hybrid predictions with confidence threshold")
    print("3. Return live signals for dashboard display")
    print("4. Test auto trading signal display")
