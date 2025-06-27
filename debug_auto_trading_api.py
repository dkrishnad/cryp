#!/usr/bin/env python3
"""
Test script to debug the auto trading API responses and fix synchronization issues.
"""

import requests
import json

API_URL = "http://localhost:8001"

def test_auto_trading_status():
    """Test the auto trading status endpoint."""
    print("=== TESTING AUTO TRADING STATUS API ===")
    try:
        resp = requests.get(f"{API_URL}/auto_trading/status")
        print(f"Status Code: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"Response Data: {json.dumps(data, indent=2)}")
            
            if data.get("status") == "success":
                state = data.get("auto_trading", {})
                print(f"Auto Trading State: {json.dumps(state, indent=2)}")
                print(f"Enabled: {state.get('enabled', False)}")
                print(f"Confidence Threshold: {state.get('confidence_threshold', 70.0)}")
            else:
                print(f"API Error: {data.get('message', 'Unknown error')}")
        else:
            print(f"HTTP Error: {resp.status_code}")
            print(f"Response: {resp.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

def test_virtual_balance():
    """Test the virtual balance endpoint."""
    print("\n=== TESTING VIRTUAL BALANCE API ===")
    try:
        resp = requests.get(f"{API_URL}/virtual_balance")
        print(f"Status Code: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"Response Data: {json.dumps(data, indent=2)}")
            
            if data.get("status") == "success":
                balance = data.get("balance", 0.0)
                pnl = data.get("current_pnl", 0.0)
                print(f"Virtual Balance: ${balance:,.2f}")
                print(f"Current P&L: ${pnl:,.2f}")
            else:
                print(f"API Error: {data.get('message', 'Unknown error')}")
        else:
            print(f"HTTP Error: {resp.status_code}")
            print(f"Response: {resp.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

def test_auto_trading_trades():
    """Test the auto trading trades endpoint."""
    print("\n=== TESTING AUTO TRADING TRADES API ===")
    try:
        resp = requests.get(f"{API_URL}/auto_trading/trades")
        print(f"Status Code: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"Response Data: {json.dumps(data, indent=2)}")
            
            if data.get("status") == "success":
                count = data.get("count", 0)
                summary = data.get("summary", {})
                print(f"Total Trades: {count}")
                print(f"Summary: {json.dumps(summary, indent=2)}")
            else:
                print(f"API Error: {data.get('message', 'Unknown error')}")
        else:
            print(f"HTTP Error: {resp.status_code}")
            print(f"Response: {resp.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

def test_current_signal():
    """Test the current signal endpoint."""
    print("\n=== TESTING CURRENT SIGNAL API ===")
    try:
        resp = requests.get(f"{API_URL}/auto_trading/current_signal")
        print(f"Status Code: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"Response Data: {json.dumps(data, indent=2)}")
            
            if data.get("status") == "success":
                signal = data.get("signal", {})
                print(f"Signal: {json.dumps(signal, indent=2)}")
            else:
                print(f"API Error: {data.get('message', 'Unknown error')}")
        else:
            print(f"HTTP Error: {resp.status_code}")
            print(f"Response: {resp.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    print("🔍 DEBUGGING AUTO TRADING API RESPONSES")
    print("=" * 50)
    
    test_auto_trading_status()
    test_virtual_balance()
    test_auto_trading_trades()
    test_current_signal()
    
    print("\n" + "=" * 50)
    print("🔍 Debug complete. Check the responses above to identify issues.")
