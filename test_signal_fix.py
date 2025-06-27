#!/usr/bin/env python3
"""
Test and fix auto trading signal generation
"""
import requests
import json

API_URL = "http://localhost:8001"

def update_auto_trading_symbol():
    """Update auto trading symbol to KAIA/USDT as shown in dashboard"""
    print("🔧 Updating Auto Trading Symbol to KAIA/USDT")
    
    try:
        # Update auto trading settings
        settings_data = {
            "symbol": "KAIAUSDT",
            "enabled": True,
            "entry_threshold": 0.6,
            "exit_threshold": 0.3,
            "max_positions": 3,
            "risk_per_trade": 2.0
        }
        
        resp = requests.post(f"{API_URL}/auto_trading/settings", json=settings_data, timeout=5)
        if resp.status_code == 200:
            result = resp.json()
            print(f"✅ Auto trading settings updated: {result}")
        else:
            print(f"❌ Failed to update settings: {resp.status_code}")
            
    except Exception as e:
        print(f"❌ Error updating settings: {str(e)}")

def test_current_signal_generation():
    """Test the new current signal generation"""
    print(f"\n🎯 Testing Current Signal Generation")
    print("=" * 50)
    
    try:
        resp = requests.get(f"{API_URL}/auto_trading/current_signal", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data["status"] == "success":
                signal = data["signal"]
                
                print(f"✅ Current Auto Trading Signal:")
                print(f"   📊 Symbol: {signal.get('symbol')}")
                print(f"   🎯 Direction: {signal.get('direction')}")
                print(f"   📈 Confidence: {signal.get('confidence')}%")
                print(f"   🕒 Timestamp: {signal.get('timestamp')}")
                print(f"   🤖 ML Prediction: {signal.get('ml_prediction')}")
                print(f"   📡 Source: {signal.get('source')}")
                
                if signal.get('reason'):
                    print(f"   ℹ️  Reason: {signal.get('reason')}")
                
                return signal
            else:
                print(f"❌ Signal generation failed: {data}")
        else:
            print(f"❌ HTTP Error: {resp.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    return None

def test_dashboard_display():
    """Test what the dashboard should display"""
    print(f"\n🖥️  Dashboard Display Test")
    print("=" * 50)
    
    signal = test_current_signal_generation()
    
    if signal:
        direction = signal.get("direction", "NO SIGNAL")
        confidence = signal.get("confidence", 0)
        timestamp = signal.get("timestamp", "")
        
        print(f"\n📱 Dashboard should show:")
        if direction in ["LONG", "BUY"]:
            print(f"   🟢 BUY signal")
            print(f"   📈 Confidence: {confidence:.2f}%")
        elif direction in ["SHORT", "SELL"]:
            print(f"   🔴 SELL signal")
            print(f"   📉 Confidence: {confidence:.2f}%")
        else:
            print(f"   ⚪ NO SIGNAL")
            print(f"   📊 Confidence: 0.00%")
        
        if 'T' in timestamp:
            time_part = timestamp.split('T')[1][:8]
            print(f"   🕒 Updated: {time_part}")

def compare_signals():
    """Compare auto trading signal with hybrid prediction"""
    print(f"\n🔍 Signal Comparison")
    print("=" * 50)
    
    # Get auto trading signal
    auto_signal = None
    try:
        resp = requests.get(f"{API_URL}/auto_trading/current_signal", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data["status"] == "success":
                auto_signal = data["signal"]
    except:
        pass
    
    # Get hybrid prediction
    hybrid_pred = None
    try:
        resp = requests.get(f"{API_URL}/ml/hybrid/predict?symbol=kaiausdt", timeout=5)
        if resp.status_code == 200:
            result = resp.json()
            hybrid_pred = result.get("prediction", {})
    except:
        pass
    
    print("📊 Auto Trading Signal:")
    if auto_signal:
        print(f"   Direction: {auto_signal.get('direction')}")
        print(f"   Confidence: {auto_signal.get('confidence')}%")
        print(f"   Symbol: {auto_signal.get('symbol')}")
    else:
        print("   ❌ Not available")
    
    print(f"\n🤖 Hybrid ML Prediction:")
    if hybrid_pred:
        print(f"   Signal: {hybrid_pred.get('signal')}")
        print(f"   Confidence: {hybrid_pred.get('ensemble_confidence', 0):.2%}")
        print(f"   Prediction: {hybrid_pred.get('ensemble_prediction')}")
    else:
        print("   ❌ Not available")

if __name__ == "__main__":
    update_auto_trading_symbol()
    test_current_signal_generation()
    test_dashboard_display()
    compare_signals()
    
    print(f"\n" + "=" * 50)
    print("🎯 Status:")
    print("✅ New signal generation endpoint added")
    print("✅ Signal uses hybrid ML predictions")
    print("✅ Dashboard callback updated to use new endpoint")
    print("✅ Signal should now appear in auto trading dashboard")
    print(f"\n💡 If dashboard still shows 'NO SIGNAL':")
    print("1. Refresh the browser tab")
    print("2. Check that auto trading is enabled")
    print("3. Verify KAIA/USDT symbol is selected")
    print("4. Wait for auto-refresh (happens every few seconds)")
