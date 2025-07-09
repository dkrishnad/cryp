#!/usr/bin/env python3
"""
Test script to verify the execute signal functionality works end-to-end
"""

import requests
import json
import time

API_URL = "http://localhost:8001"

def test_execute_signal():
    """Test the complete execute signal flow"""
    
    print("=== Testing Execute Signal Functionality ===\n")
      # 1. Check auto trading status
    print("1. Checking auto trading status...")
    try:
        resp = requests.get(f"{API_URL}/auto_trading/status")
        if resp.status_code == 200:
            status_data = resp.json()
            status = status_data["auto_trading"]
            print(f"   ✓ Auto trading enabled: {status['enabled']}")
            print(f"   ✓ Virtual balance: ${status['balance']}")
            print(f"   ✓ Signals processed: {status['signals_processed']}")
        else:
            print(f"   ✗ Failed to get status: {resp.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error getting status: {e}")
        return False
    
    # 2. Get current signal
    print("\n2. Getting current signal...")
    try:
        resp = requests.get(f"{API_URL}/auto_trading/current_signal")
        if resp.status_code == 200:
            signal_data = resp.json()["signal"]
            print(f"   ✓ Symbol: {signal_data['symbol']}")
            print(f"   ✓ Direction: {signal_data['direction']}")
            print(f"   ✓ Confidence: {signal_data['confidence']}%")
            print(f"   ✓ Price: ${signal_data.get('price', 'N/A')}")
            print(f"   ✓ Timestamp: {signal_data['timestamp']}")
        else:
            print(f"   ✗ Failed to get signal: {resp.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error getting signal: {e}")
        return False
    
    # 3. Get trades before execution
    print("\n3. Getting current trades...")
    try:
        resp = requests.get(f"{API_URL}/auto_trading/trades")
        if resp.status_code == 200:
            trades_before = resp.json()["trades"]
            print(f"   ✓ Current trades count: {len(trades_before)}")
        else:
            print(f"   ✗ Failed to get trades: {resp.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error getting trades: {e}")
        return False
    
    # 4. Execute the signal
    print("\n4. Executing signal...")
    try:
        # Prepare payload like the dashboard does
        execute_payload = {
            "symbol": signal_data["symbol"],
            "signal": signal_data["direction"], 
            "confidence": signal_data["confidence"],
            "price": signal_data.get("price", 0.0),
            "timestamp": signal_data["timestamp"]
        }
        
        resp = requests.post(f"{API_URL}/auto_trading/execute_signal", json=execute_payload)
        if resp.status_code == 200:
            result = resp.json()
            print(f"   ✓ Execution status: {result['status']}")
            if result["status"] == "success":
                trade = result["trade"]
                print(f"   ✓ Trade ID: {trade['id']}")
                print(f"   ✓ Action: {trade['action']}")
                print(f"   ✓ Amount: ${trade['amount']}")
                print(f"   ✓ Price: ${trade['price']}")
                print(f"   ✓ Status: {trade['status']}")
            elif result["status"] == "skipped":
                print(f"   ⚠ Execution skipped: {result['message']}")
            else:
                print(f"   ⚠ Unexpected status: {result}")
        else:
            print(f"   ✗ Failed to execute: {resp.status_code}")
            print(f"   Response: {resp.text}")
            return False
    except Exception as e:
        print(f"   ✗ Error executing signal: {e}")
        return False
    
    # 5. Verify trade was created
    print("\n5. Verifying trade creation...")
    try:
        resp = requests.get(f"{API_URL}/auto_trading/trades")
        if resp.status_code == 200:
            trades_after = resp.json()["trades"]
            print(f"   ✓ Trades count after execution: {len(trades_after)}")
            
            if len(trades_after) > len(trades_before):
                latest_trade = trades_after[-1]
                print(f"   ✓ Latest trade: {latest_trade['action']} {latest_trade['symbol']} @ ${latest_trade['price']}")
                return True
            else:
                print(f"   ⚠ No new trade created")
                return False
        else:
            print(f"   ✗ Failed to verify trades: {resp.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error verifying trades: {e}")
        return False

if __name__ == "__main__":
    success = test_execute_signal()
    
    if success:
        print("\n🎉 Execute signal test PASSED! Auto trading is working correctly.")
    else:
        print("\n❌ Execute signal test FAILED! Check the logs above for details.")
    
    print("\n=== Test Complete ===")
