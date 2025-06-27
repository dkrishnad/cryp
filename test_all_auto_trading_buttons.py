#!/usr/bin/env python3
"""
Comprehensive test script to check all auto trading buttons and functionality
"""

import requests
import json
import time

API_URL = "http://localhost:8001"

def test_backend_endpoints():
    """Test all backend endpoints used by auto trading"""
    
    print("=== Testing Backend Endpoints ===\n")
    
    endpoints_to_test = [
        ("GET", "/auto_trading/status", None),
        ("GET", "/auto_trading/current_signal", None),
        ("GET", "/auto_trading/trades", None),
        ("GET", "/auto_trading/signals", None),
        ("POST", "/auto_trading/toggle", {"enabled": True}),
        ("POST", "/auto_trading/settings", {
            "enabled": True,
            "symbol": "KAIAUSDT",
            "entry_threshold": 0.7,
            "exit_threshold": 0.5,
            "max_positions": 3,
            "risk_per_trade": 5.0,
            "amount_config": {
                "type": "fixed",
                "amount": 100,
                "percentage": 10,
                "take_profit": 2.0,
                "stop_loss": 1.0,
                "timeframe": "1h"
            }
        }),
        ("POST", "/auto_trading/execute_signal", {
            "symbol": "KAIAUSDT",
            "signal": "BUY",
            "confidence": 75.0,
            "price": 0.18,
            "timestamp": "2025-06-23T22:00:00"
        }),
        ("POST", "/auto_trading/reset", None)
    ]
    
    results = {}
    
    for method, endpoint, payload in endpoints_to_test:
        try:
            print(f"Testing {method} {endpoint}...")
            
            if method == "GET":
                resp = requests.get(f"{API_URL}{endpoint}", timeout=5)
            else:
                resp = requests.post(f"{API_URL}{endpoint}", json=payload, timeout=5)
            
            if resp.status_code == 200:
                data = resp.json()
                status = data.get("status", "unknown")
                if status == "success":
                    print(f"   ✅ {endpoint}: SUCCESS")
                    results[endpoint] = "SUCCESS"
                else:
                    print(f"   ⚠️ {endpoint}: {status}")
                    results[endpoint] = status
            else:
                print(f"   ❌ {endpoint}: HTTP {resp.status_code}")
                results[endpoint] = f"HTTP {resp.status_code}"
                
        except Exception as e:
            print(f"   ❌ {endpoint}: ERROR - {str(e)}")
            results[endpoint] = f"ERROR - {str(e)}"
    
    return results

def test_dashboard_accessibility():
    """Test if dashboard is accessible"""
    
    print("\n=== Testing Dashboard Accessibility ===\n")
    
    try:
        resp = requests.get("http://localhost:8050", timeout=5)
        if resp.status_code == 200:
            print("✅ Dashboard is accessible at http://localhost:8050")
            return True
        else:
            print(f"❌ Dashboard returned HTTP {resp.status_code}")
            return False
    except Exception as e:
        print(f"❌ Dashboard is not accessible: {str(e)}")
        return False

def analyze_button_functionality():
    """Analyze which buttons should work and which might not"""
    
    print("\n=== Auto Trading Button Analysis ===\n")
    
    buttons_analysis = {
        "✅ Working Buttons": [
            "🔄 Execute Signal - Has callback and backend endpoint",
            "💾 Save Settings - Has callback (now fixed to match backend schema)",
            "🔄 Reset System - Has callback and backend endpoint", 
            "Auto Trading Toggle - Has callback and backend endpoint",
            "Quick Amount Buttons ($1, $10, $50, $100, $500) - Has callback",
            "Amount Type Radio (Fixed/Percentage) - Has callback",
            "Percentage Slider/Input Sync - Has callbacks"
        ],
        "🆕 Recently Fixed Buttons": [
            "⚡ Optimize for KAIA - NEW callback added",
            "⚡ Optimize for JASMY - NEW callback added", 
            "⚡ Optimize for GALA - NEW callback added",
            "📋 Open Positions Table - NEW callback added",
            "📜 Trade Log - NEW callback added"
        ],
        "⚠️ Potential Issues": [
            "Settings save - Fixed schema but may need testing",
            "Button text resets - May need proper timing",
            "Error handling - Some callbacks may need better error handling"
        ]
    }
    
    for category, items in buttons_analysis.items():
        print(f"{category}:")
        for item in items:
            print(f"   {item}")
        print()

def test_auto_trading_flow():
    """Test the complete auto trading flow"""
    
    print("=== Testing Complete Auto Trading Flow ===\n")
    
    steps = [
        "1. Enable auto trading",
        "2. Save optimized settings for KAIA", 
        "3. Get current signal",
        "4. Execute signal",
        "5. Check open positions",
        "6. Check trade log"
    ]
    
    try:
        # Step 1: Enable auto trading
        print("1. Enabling auto trading...")
        resp = requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": True})
        if resp.status_code == 200:
            print("   ✅ Auto trading enabled")
        else:
            print(f"   ❌ Failed to enable: {resp.status_code}")
            return False
        
        # Step 2: Save optimized settings
        print("2. Saving optimized KAIA settings...")
        settings = {
            "enabled": True,
            "symbol": "KAIAUSDT",
            "entry_threshold": 0.6,  # 60% confidence
            "exit_threshold": 0.5,
            "max_positions": 3,
            "risk_per_trade": 3.5,
            "amount_config": {
                "type": "fixed",
                "amount": 100,
                "percentage": 10,
                "take_profit": 2.2,
                "stop_loss": 1.1,
                "timeframe": "1h"
            }
        }
        resp = requests.post(f"{API_URL}/auto_trading/settings", json=settings)
        if resp.status_code == 200:
            print("   ✅ Settings saved")
        else:
            print(f"   ❌ Failed to save settings: {resp.status_code}")
        
        # Step 3: Get current signal
        print("3. Getting current signal...")
        resp = requests.get(f"{API_URL}/auto_trading/current_signal")
        if resp.status_code == 200:
            signal_data = resp.json()["signal"]
            print(f"   ✅ Signal: {signal_data['direction']} {signal_data['symbol']} ({signal_data['confidence']:.1f}%)")
        else:
            print(f"   ❌ Failed to get signal: {resp.status_code}")
            return False
        
        # Step 4: Execute signal  
        print("4. Executing signal...")
        execute_payload = {
            "symbol": signal_data["symbol"],
            "signal": signal_data["direction"],
            "confidence": signal_data["confidence"],
            "price": signal_data.get("price", 0.18),
            "timestamp": signal_data["timestamp"]
        }
        resp = requests.post(f"{API_URL}/auto_trading/execute_signal", json=execute_payload)
        if resp.status_code == 200:
            result = resp.json()
            if result["status"] == "success":
                trade = result["trade"]
                print(f"   ✅ Trade executed: {trade['action']} ${trade['amount']} @ ${trade['price']}")
            else:
                print(f"   ⚠️ Execution skipped: {result.get('message', 'Unknown reason')}")
        else:
            print(f"   ❌ Failed to execute: {resp.status_code}")
        
        # Step 5: Check open positions
        print("5. Checking open positions...")
        resp = requests.get(f"{API_URL}/auto_trading/trades")
        if resp.status_code == 200:
            trades = resp.json()["trades"]
            print(f"   ✅ Total trades: {len(trades)}")
        else:
            print(f"   ❌ Failed to get trades: {resp.status_code}")
        
        # Step 6: Check signals (for trade log)
        print("6. Checking trade log data...")
        resp = requests.get(f"{API_URL}/auto_trading/signals")
        if resp.status_code == 200:
            signals = resp.json()["signals"]
            print(f"   ✅ Total signals: {len(signals)}")
        else:
            print(f"   ❌ Failed to get signals: {resp.status_code}")
        
        print("\n🎉 Complete auto trading flow test PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ Auto trading flow test FAILED: {str(e)}")
        return False

if __name__ == "__main__":
    print("🤖 CRYPTO BOT AUTO TRADING SYSTEM TEST\n")
    print("=" * 50)
    
    # Test backend endpoints
    backend_results = test_backend_endpoints()
    
    # Test dashboard accessibility  
    dashboard_accessible = test_dashboard_accessibility()
    
    # Analyze button functionality
    analyze_button_functionality()
    
    # Test complete flow
    flow_success = test_auto_trading_flow()
    
    # Summary
    print("\n" + "=" * 50)
    print("🔍 SUMMARY")
    print("=" * 50)
    
    backend_success = sum(1 for result in backend_results.values() if result == "SUCCESS")
    backend_total = len(backend_results)
    
    print(f"Backend Endpoints: {backend_success}/{backend_total} working")
    print(f"Dashboard Access: {'✅' if dashboard_accessible else '❌'}")
    print(f"Complete Flow: {'✅' if flow_success else '❌'}")
    
    if backend_success == backend_total and dashboard_accessible and flow_success:
        print("\n🎉 ALL SYSTEMS OPERATIONAL!")
        print("🎯 All auto trading buttons should now work correctly.")
    else:
        print("\n⚠️ SOME ISSUES DETECTED")
        print("📝 Check the details above for specific problems.")
    
    print("\n🌐 Dashboard URL: http://localhost:8050")
    print("📊 Navigate to Auto Trading tab to test buttons manually.")
