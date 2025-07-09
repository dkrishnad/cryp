#!/usr/bin/env python3
"""
Test Auto Trading Toggle and Trade Execution
"""
import requests
import json

def test_auto_trading():
    base_url = "http://localhost:8001"
    
    print("🤖 TESTING AUTO TRADING FUNCTIONALITY")
    print("=" * 50)
    
    # 1. Enable auto trading
    print("\n1. Enabling Auto Trading...")
    toggle_data = {"enabled": True}
    response = requests.post(f"{base_url}/auto_trading/toggle", json=toggle_data)
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Toggle successful: {result.get('message')}")
        print(f"   ✅ Enabled: {result.get('enabled')}")
    else:
        print(f"   ❌ Toggle failed: {response.status_code}")
        return
    
    # 2. Check status
    print("\n2. Checking Auto Trading Status...")
    status_response = requests.get(f"{base_url}/auto_trading/status")
    if status_response.status_code == 200:
        status_data = status_response.json()
        if status_data.get('status') == 'success':
            auto_status = status_data.get('status', {})
            print(f"   ✅ Status retrieved successfully")
            print(f"   ✅ Enabled: {auto_status.get('enabled', False)}")
            print(f"   ✅ Active Trades: {len(auto_status.get('active_trades', []))}")
        else:
            print(f"   ❌ Status error: {status_data}")
    else:
        print(f"   ❌ Status failed: {status_response.status_code}")
    
    # 3. Check virtual balance
    print("\n3. Checking Virtual Balance...")
    balance_response = requests.get(f"{base_url}/virtual_balance")
    if balance_response.status_code == 200:
        balance_data = balance_response.json()
        print(f"   ✅ Balance: ${balance_data.get('balance', 0):.2f}")
        print(f"   ✅ Current P&L: ${balance_data.get('current_pnl', 0):.2f}")
        print(f"   ✅ Total Value: ${balance_data.get('total_value', 0):.2f}")
    
    # 4. Execute a test trade
    print("\n4. Executing Test Trade...")
    signal_data = {
        "symbol": "KAIAUSDT",
        "signal": "BUY", 
        "price": 0.195,
        "confidence": 85.0,
        "timestamp": "2025-06-24T12:00:00"
    }
    
    execute_response = requests.post(f"{base_url}/auto_trading/execute_signal", json=signal_data)
    if execute_response.status_code == 200:
        execute_data = execute_response.json()
        if execute_data.get('status') == 'success':
            print(f"   ✅ Trade executed: {execute_data.get('message')}")
            print(f"   ✅ Trade ID: {execute_data.get('trade', {}).get('id')}")
            if 'balance_after' in execute_data:
                print(f"   ✅ Balance after trade: ${execute_data.get('balance_after'):.2f}")
        else:
            print(f"   ❌ Trade execution failed: {execute_data.get('message')}")
    else:
        print(f"   ❌ Trade execution failed: {execute_response.status_code}")
    
    # 5. Check trades
    print("\n5. Checking Trades...")
    trades_response = requests.get(f"{base_url}/auto_trading/trades")
    if trades_response.status_code == 200:
        trades_data = trades_response.json()
        if trades_data.get('status') == 'success':
            trades = trades_data.get('trades', [])
            summary = trades_data.get('summary', {})
            print(f"   ✅ Total Trades: {len(trades)}")
            print(f"   ✅ Open Trades: {summary.get('open_trades', 0)}")
            print(f"   ✅ Win Rate: {summary.get('win_rate', 0):.1f}%")
            print(f"   ✅ Total P&L: ${summary.get('total_pnl', 0):.2f}")
            
            if trades:
                latest = trades[-1]
                print(f"   ✅ Latest Trade: {latest.get('action')} {latest.get('symbol')} @ ${latest.get('price')}")
    
    print("\n" + "=" * 50)
    print("✅ AUTO TRADING TEST COMPLETED")

if __name__ == "__main__":
    test_auto_trading()
