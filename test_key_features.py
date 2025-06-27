#!/usr/bin/env python3
"""
Quick test script for key dashboard settings and auto trading functionality
"""
import requests
import json

def test_key_features():
    base_url = "http://localhost:8001"
    
    print("TESTING KEY DASHBOARD FEATURES")
    print("="*50)
    
    # 1. Test virtual balance with P&L
    print("\n1. Virtual Balance & P&L System:")
    try:
        response = requests.get(f"{base_url}/virtual_balance")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Balance: ${data.get('balance', 0):.2f}")
            print(f"   ✓ Current P&L: ${data.get('current_pnl', 0):.2f}")
            print(f"   ✓ Total Value: ${data.get('total_value', 0):.2f}")
        else:
            print(f"   ✗ Error: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Exception: {e}")
    
    # 2. Test auto trading settings
    print("\n2. Auto Trading Settings:")
    try:
        response = requests.get(f"{base_url}/auto_trading/settings")
        if response.status_code == 200:
            data = response.json()
            settings = data.get('settings', {})
            print(f"   ✓ Enabled: {settings.get('enabled', False)}")
            print(f"   ✓ Confidence Threshold: {settings.get('confidence_threshold', 0)}%")
            print(f"   ✓ Trade Amount: ${settings.get('amount_config', {}).get('amount', 0)}")
            print(f"   ✓ Stop Loss: {settings.get('stop_loss', 0)}%")
            print(f"   ✓ Take Profit: {settings.get('take_profit', 0)}%")
        else:
            print(f"   ✗ Error: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Exception: {e}")
    
    # 3. Test trade execution and P&L
    print("\n3. Trade Execution System:")
    try:
        # Execute a test trade
        signal_data = {
            "symbol": "BTCUSDT",
            "signal": "BUY", 
            "price": 103000.0,
            "confidence": 85.0,
            "timestamp": "2025-06-24T00:00:00"
        }
        response = requests.post(f"{base_url}/auto_trading/execute_signal", json=signal_data)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Trade executed: {data.get('message', '')}")
            if 'trade' in data:
                trade_id = data['trade']['id']
                print(f"   ✓ Trade ID: {trade_id}")
                
                # Get updated balance
                balance_response = requests.get(f"{base_url}/virtual_balance")
                if balance_response.status_code == 200:
                    balance_data = balance_response.json()
                    print(f"   ✓ New Balance: ${balance_data.get('balance', 0):.2f}")
                
                # Close the trade to test P&L calculation
                close_response = requests.post(f"{base_url}/auto_trading/close_trade/{trade_id}")
                if close_response.status_code == 200:
                    close_data = close_response.json()
                    print(f"   ✓ Trade closed with P&L: ${close_data.get('pnl', 0):.2f}")
                    print(f"   ✓ Final Balance: ${close_data.get('balance_after', 0):.2f}")
        else:
            print(f"   ✗ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ✗ Exception: {e}")
    
    # 4. Test trades summary
    print("\n4. Trades Summary:")
    try:
        response = requests.get(f"{base_url}/auto_trading/trades")
        if response.status_code == 200:
            data = response.json()
            summary = data.get('summary', {})
            print(f"   ✓ Total Trades: {data.get('count', 0)}")
            print(f"   ✓ Open Trades: {summary.get('open_trades', 0)}")
            print(f"   ✓ Closed Trades: {summary.get('total_closed_trades', 0)}")
            print(f"   ✓ Win Rate: {summary.get('win_rate', 0):.1f}%")
            print(f"   ✓ Total P&L: ${summary.get('total_pnl', 0):.2f}")
            print(f"   ✓ Realized P&L: ${summary.get('realized_pnl', 0):.2f}")
            print(f"   ✓ Unrealized P&L: ${summary.get('unrealized_pnl', 0):.2f}")
        else:
            print(f"   ✗ Error: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Exception: {e}")
    
    # 5. Test dashboard accessibility
    print("\n5. Dashboard Accessibility:")
    try:
        response = requests.get("http://127.0.0.1:8050", timeout=5)
        if response.status_code == 200:
            print("   ✓ Dashboard is accessible and running")
            if "Crypto Trading Dashboard" in response.text or "dash" in response.text.lower():
                print("   ✓ Dashboard content is loading properly")
            else:
                print("   ? Dashboard may not be fully loaded")
        else:
            print(f"   ✗ Dashboard error: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Dashboard exception: {e}")
    
    print("\n" + "="*50)
    print("KEY FEATURES TEST COMPLETED")

if __name__ == "__main__":
    test_key_features()
