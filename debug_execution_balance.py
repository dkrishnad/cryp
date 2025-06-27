#!/usr/bin/env python3
"""
Debug script to check auto trading execution and virtual balance display issues
"""

import requests
import json

API_URL = "http://localhost:8001"

def debug_auto_trading_execution():
    """Debug why auto trading is not executing"""
    print("🔍 DEBUGGING AUTO TRADING EXECUTION")
    print("=" * 50)
    
    # 1. Check auto trading status
    print("1. Checking auto trading status...")
    try:
        resp = requests.get(f"{API_URL}/auto_trading/status")
        if resp.status_code == 200:
            data = resp.json()
            print(f"Status API Response: {json.dumps(data, indent=2)}")
            
            if data.get("status") == "success":
                auto_trading = data.get("auto_trading", {})
                enabled = auto_trading.get("enabled", False)
                threshold = auto_trading.get("confidence_threshold", 70.0)
                print(f"✓ Auto trading enabled: {enabled}")
                print(f"✓ Confidence threshold: {threshold}%")
            else:
                print(f"✗ Status API error: {data.get('message')}")
        else:
            print(f"✗ Status API failed: {resp.status_code}")
    except Exception as e:
        print(f"✗ Status API exception: {e}")
    
    # 2. Check current signal
    print("\n2. Checking current signal...")
    try:
        resp = requests.get(f"{API_URL}/auto_trading/current_signal")
        if resp.status_code == 200:
            data = resp.json()
            print(f"Signal API Response: {json.dumps(data, indent=2)}")
            
            if data.get("status") == "success" and data.get("signal"):
                signal = data["signal"]
                confidence = signal.get("confidence", 0.0)
                signal_type = signal.get("signal", "")
                print(f"✓ Signal type: {signal_type}")
                print(f"✓ Confidence: {confidence}%")
                print(f"✓ Should execute: {confidence >= 70.0 and signal_type in ['BUY', 'SELL']}")
            else:
                print("✗ No valid signal found")
        else:
            print(f"✗ Signal API failed: {resp.status_code}")
    except Exception as e:
        print(f"✗ Signal API exception: {e}")
    
    # 3. Check virtual balance
    print("\n3. Checking virtual balance...")
    try:
        resp = requests.get(f"{API_URL}/virtual_balance")
        if resp.status_code == 200:
            data = resp.json()
            print(f"Virtual Balance API Response: {json.dumps(data, indent=2)}")
            
            if data.get("status") == "success":
                balance = data.get("balance", 0.0)
                pnl = data.get("current_pnl", 0.0)
                total = data.get("total_value", 0.0)
                print(f"✓ Balance: ${balance:,.2f}")
                print(f"✓ Current P&L: ${pnl:,.2f}")
                print(f"✓ Total Value: ${total:,.2f}")
            else:
                print(f"✗ Virtual balance API error: {data.get('message')}")
        else:
            print(f"✗ Virtual balance API failed: {resp.status_code}")
    except Exception as e:
        print(f"✗ Virtual balance API exception: {e}")

def test_toggle_enable():
    """Test enabling auto trading"""
    print("\n4. Testing auto trading enable...")
    try:
        # Enable auto trading
        resp = requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": True})
        if resp.status_code == 200:
            data = resp.json()
            print(f"Toggle Enable Response: {json.dumps(data, indent=2)}")
            
            # Check status after enabling
            resp2 = requests.get(f"{API_URL}/auto_trading/status")
            if resp2.status_code == 200:
                data2 = resp2.json()
                auto_trading = data2.get("auto_trading", {})
                enabled = auto_trading.get("enabled", False)
                print(f"✓ Auto trading now enabled: {enabled}")
            else:
                print(f"✗ Status check failed: {resp2.status_code}")
        else:
            print(f"✗ Toggle failed: {resp.status_code}")
    except Exception as e:
        print(f"✗ Toggle exception: {e}")

def check_execution_conditions():
    """Check if all conditions for execution are met"""
    print("\n" + "=" * 50)
    print("📋 EXECUTION CONDITIONS CHECK")
    print("=" * 50)
    
    conditions = {
        "auto_trading_enabled": False,
        "signal_available": False,
        "confidence_meets_threshold": False,
        "valid_signal_type": False
    }
    
    # Check conditions
    try:
        # Auto trading status
        resp = requests.get(f"{API_URL}/auto_trading/status")
        if resp.status_code == 200:
            data = resp.json()
            auto_trading = data.get("auto_trading", {})
            conditions["auto_trading_enabled"] = auto_trading.get("enabled", False)
        
        # Current signal
        resp = requests.get(f"{API_URL}/auto_trading/current_signal")
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success" and data.get("signal"):
                signal = data["signal"]
                confidence = signal.get("confidence", 0.0)
                signal_type = signal.get("signal", "")
                
                conditions["signal_available"] = True
                conditions["confidence_meets_threshold"] = confidence >= 70.0
                conditions["valid_signal_type"] = signal_type in ["BUY", "SELL"]
                
                print(f"Signal Type: {signal_type}")
                print(f"Confidence: {confidence}%")
                print(f"Threshold: 70.0%")
    
    except Exception as e:
        print(f"Error checking conditions: {e}")
    
    # Display results
    for condition, met in conditions.items():
        status = "✓ PASS" if met else "✗ FAIL"
        print(f"{condition.replace('_', ' ').title()}: {status}")
    
    all_met = all(conditions.values())
    print(f"\nALL CONDITIONS MET: {'✓ YES' if all_met else '✗ NO'}")
    
    if all_met:
        print("🚀 Auto trading should be executing!")
    else:
        print("⚠️  Auto trading will not execute until all conditions are met.")

if __name__ == "__main__":
    debug_auto_trading_execution()
    test_toggle_enable()
    check_execution_conditions()
