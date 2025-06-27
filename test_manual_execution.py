#!/usr/bin/env python3
"""
Test the auto trading callback functionality directly.
"""

import requests
import time
import json

API_URL = "http://127.0.0.1:8001"

def test_auto_trading_callback():
    print("🧪 Testing Auto Trading Callback Trigger...")
    print("=" * 50)
    
    # 1. Check if auto trading is enabled
    print("1. Checking backend auto trading status...")
    resp = requests.get(f"{API_URL}/auto_trading/status")
    if resp.status_code == 200:
        data = resp.json()
        if data["status"] == "success":
            state = data["auto_trading"]
            print(f"   ✓ Backend Auto Trading Enabled: {state['enabled']}")
            
            if not state["enabled"]:
                print("   🔧 Enabling auto trading in backend...")
                toggle_resp = requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": True})
                if toggle_resp.status_code == 200:
                    print("   ✓ Auto trading enabled")
    
    # 2. Check current signal for auto execution
    print("\n2. Checking current signal...")
    resp = requests.get(f"{API_URL}/auto_trading/current_signal")
    if resp.status_code == 200:
        data = resp.json()
        if data["status"] == "success" and data.get("signal"):
            signal = data["signal"]
            confidence = signal.get("confidence", 0.0)
            signal_type = signal.get("direction", "")
            print(f"   ✓ Signal: {signal_type}")
            print(f"   ✓ Confidence: {confidence:.1f}%")
            print(f"   ✓ Symbol: {signal.get('symbol', 'N/A')}")
            
            # 3. Test manual execution
            if confidence >= 70 and signal_type in ["BUY", "SELL"]:
                print(f"\n3. Testing manual execution (confidence {confidence:.1f}% >= 70%)...")
                
                # Get initial trade count
                resp = requests.get(f"{API_URL}/auto_trading/trades")
                initial_count = 0
                if resp.status_code == 200:
                    data = resp.json()
                    if data["status"] == "success":
                        initial_count = data["count"]
                        print(f"   📊 Initial trade count: {initial_count}")
                
                # Execute signal manually
                signal_payload = {
                    "timestamp": signal.get("timestamp", ""),
                    "symbol": signal.get("symbol", ""),
                    "signal": signal.get("direction", ""),  # Use 'direction' instead of 'signal'
                    "confidence": confidence,
                    "price": signal.get("price", 0.0)
                }
                
                print(f"   🚀 Executing signal manually...")
                execute_resp = requests.post(f"{API_URL}/auto_trading/execute_signal", json=signal_payload)
                if execute_resp.status_code == 200:
                    execute_data = execute_resp.json()
                    if execute_data["status"] == "success":
                        print(f"   ✅ MANUAL EXECUTION SUCCESS: {execute_data.get('message', 'Trade executed')}")
                        
                        # Check new trade count
                        resp = requests.get(f"{API_URL}/auto_trading/trades")
                        if resp.status_code == 200:
                            data = resp.json()
                            if data["status"] == "success":
                                new_count = data["count"]
                                print(f"   📊 New trade count: {new_count}")
                                
                                if new_count > initial_count:
                                    print(f"   🎉 SUCCESS: Trade was executed and recorded!")
                                    # Show the trade details
                                    trades = data["trades"]
                                    if trades:
                                        last_trade = trades[-1]
                                        print(f"      📈 Last Trade: {last_trade['action']} {last_trade['symbol']}")
                                        print(f"      💰 Amount: {last_trade['amount']}")
                                        print(f"      💲 Price: {last_trade['price']}")
                                        print(f"      📊 Confidence: {last_trade['confidence']:.1f}%")
                                else:
                                    print(f"   ❌ ERROR: Trade count did not increase")
                    else:
                        print(f"   ❌ MANUAL EXECUTION FAILED: {execute_data.get('message', 'Unknown error')}")
                else:
                    print(f"   ❌ EXECUTION API ERROR: Status {execute_resp.status_code}")
                    print(f"   📄 Response: {execute_resp.text}")
            else:
                print(f"\n3. ⚠️ Signal confidence {confidence:.1f}% is below 70% threshold or signal type '{signal_type}' is not BUY/SELL")
    
    print("\n" + "=" * 50)
    print("✅ Manual execution test completed!")

if __name__ == "__main__":
    try:
        test_auto_trading_callback()
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
