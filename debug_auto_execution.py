"""
Debug Auto Trading Execution
Check why the BUY signal with 79.03% confidence is not being auto-executed
"""

import requests
import json

API_URL = "http://127.0.0.1:8000"

def debug_auto_execution():
    """Debug the auto execution logic"""
    print("🔍 DEBUGGING AUTO TRADING EXECUTION")
    print("="*50)
    
    # 1. Check auto trading status and settings
    print("\n1. Auto Trading Status & Settings:")
    try:
        resp = requests.get(f"{API_URL}/auto_trading/status")
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success":
                state = data.get("auto_trading", {})
                print(f"   Enabled: {state.get('enabled', False)}")
                print(f"   Confidence Threshold: {state.get('confidence_threshold', 'Not set')}%")
                print(f"   Active Symbol: {state.get('symbol', 'Not set')}")
                print(f"   Signals Processed: {state.get('signals_processed', 0)}")
                print(f"   Last Signal: {state.get('last_signal_time', 'None')}")
                
                # Check if confidence threshold is the issue
                threshold = float(state.get('confidence_threshold', 70.0))
                print(f"\n   🎯 Current threshold: {threshold}%")
                print(f"   📊 Signal confidence: 79.03%")
                print(f"   ✅ Should execute: {79.03 >= threshold}")
            else:
                print(f"   ❌ API Error: {data}")
        else:
            print(f"   ❌ HTTP Error: {resp.status_code}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # 2. Check current signal details
    print("\n2. Current Signal Details:")
    try:
        resp = requests.get(f"{API_URL}/auto_trading/current_signal")
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success" and data.get("signal"):
                signal = data["signal"]
                print(f"   Signal Type: {signal.get('signal', 'None')}")
                print(f"   Confidence: {signal.get('confidence', 0)}%")
                print(f"   Symbol: {signal.get('symbol', 'None')}")
                print(f"   Price: ${signal.get('price', 0)}")
                print(f"   Timestamp: {signal.get('timestamp', 'None')}")
                
                # Check if this signal should be executed
                confidence = float(signal.get('confidence', 0))
                signal_type = signal.get('signal', '')
                print(f"\n   🔍 Execution check:")
                print(f"   - Signal type valid: {signal_type in ['BUY', 'SELL']}")
                print(f"   - Confidence sufficient: {confidence >= 70.0} ({confidence}% >= 70%)")
            else:
                print(f"   ❌ No signal or API error: {data}")
        else:
            print(f"   ❌ HTTP Error: {resp.status_code}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # 3. Check trades history
    print("\n3. Trade History:")
    try:
        resp = requests.get(f"{API_URL}/auto_trading/trades")
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success":
                trades = data.get("trades", [])
                count = data.get("count", 0)
                print(f"   Total Trades: {count}")
                if trades:
                    print("   Recent trades:")
                    for trade in trades[-3:]:  # Show last 3 trades
                        print(f"   - {trade.get('timestamp', '')}: {trade.get('signal', '')} {trade.get('symbol', '')} @ {trade.get('confidence', 0)}%")
                else:
                    print("   No trades found")
            else:
                print(f"   ❌ API Error: {data}")
        else:
            print(f"   ❌ HTTP Error: {resp.status_code}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # 4. Manual execution test
    print("\n4. Manual Execution Test:")
    try:
        # Get current signal
        resp = requests.get(f"{API_URL}/auto_trading/current_signal")
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success" and data.get("signal"):
                signal = data["signal"]
                
                print(f"   Attempting to execute signal manually...")
                signal_payload = {
                    "timestamp": signal.get("timestamp", ""),
                    "symbol": signal.get("symbol", ""),
                    "signal": signal.get("signal", ""),
                    "confidence": signal.get("confidence", 0),
                    "price": signal.get("price", 0.0)
                }
                
                execute_resp = requests.post(f"{API_URL}/auto_trading/execute_signal", json=signal_payload)
                if execute_resp.status_code == 200:
                    execute_data = execute_resp.json()
                    print(f"   ✅ Manual execution result: {execute_data}")
                else:
                    print(f"   ❌ Manual execution failed: {execute_resp.status_code}")
                    print(f"   Response: {execute_resp.text}")
            else:
                print(f"   ❌ No signal to execute")
        else:
            print(f"   ❌ Cannot get signal for manual test")
    except Exception as e:
        print(f"   ❌ Manual execution exception: {e}")

def check_dashboard_logs():
    """Check if dashboard is logging execution attempts"""
    print("\n5. Dashboard Callback Check:")
    print("   Check the dashboard terminal for auto execution logs...")
    print("   Look for messages like:")
    print("   - '🤖 AUTO TRADING ENABLED - Checking for signals...'")
    print("   - '🔍 Execution check: signal=BUY, confidence=79.03%'")
    print("   - '🤖 AUTO-EXECUTING: BUY signal with 79.03% confidence'")
    print("   - '✅ AUTO-EXECUTION SUCCESS' or '❌ AUTO-EXECUTION FAILED'")

if __name__ == "__main__":
    debug_auto_execution()
    check_dashboard_logs()
    
    print("\n" + "="*50)
    print("📋 NEXT STEPS:")
    print("1. Check if confidence threshold is too high")
    print("2. Verify auto execution logic in dashboard callback")
    print("3. Check if manual execution works")
    print("4. Look for errors in dashboard logs")
    print("="*50)
