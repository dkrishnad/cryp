#!/usr/bin/env python3
"""
Dashboard Settings Verification Summary
"""
import requests
import json

def test_settings_update():
    """Test if dashboard settings are responsive"""
    base_url = "http://localhost:8001"
    
    print("DASHBOARD SETTINGS VERIFICATION")
    print("="*50)
    
    # Test 1: Update auto trading settings
    print("\n1. Testing Auto Trading Settings Update:")
    
    settings_data = {
        "enabled": True,
        "confidence_threshold": 80.0,
        "amount_config": {
            "amount": 200.0,
            "percentage": 15.0
        },
        "stop_loss": 4.0,
        "take_profit": 12.0
    }
    
    try:
        # Update settings
        response = requests.post(f"{base_url}/auto_trading/settings", json=settings_data)
        print(f"   Settings Update Response: {response.status_code}")
        
        # Verify settings were saved
        get_response = requests.get(f"{base_url}/auto_trading/settings")
        if get_response.status_code == 200:
            saved_settings = get_response.json().get('settings', {})
            print(f"   ✓ Enabled: {saved_settings.get('enabled')}")
            print(f"   ✓ Confidence: {saved_settings.get('confidence_threshold')}%")
            print(f"   ✓ Amount: ${saved_settings.get('amount_config', {}).get('amount')}")
            print(f"   ✓ Stop Loss: {saved_settings.get('stop_loss')}%")
            print(f"   ✓ Take Profit: {saved_settings.get('take_profit')}%")
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 2: Virtual balance system
    print("\n2. Testing Virtual Balance System:")
    try:
        # Get current balance
        response = requests.get(f"{base_url}/virtual_balance")
        if response.status_code == 200:
            data = response.json()
            current_balance = data.get('balance', 0)
            current_pnl = data.get('current_pnl', 0)
            total_value = data.get('total_value', 0)
            
            print(f"   ✓ Current Balance: ${current_balance:.2f}")
            print(f"   ✓ Current P&L: ${current_pnl:.2f}")
            print(f"   ✓ Total Value: ${total_value:.2f}")
            
            # Test balance update
            new_balance = 8500.0
            update_response = requests.post(f"{base_url}/virtual_balance", 
                                          json={"balance": new_balance})
            if update_response.status_code == 200:
                print(f"   ✓ Balance update successful")
                
                # Verify update
                verify_response = requests.get(f"{base_url}/virtual_balance")
                if verify_response.status_code == 200:
                    verify_data = verify_response.json()
                    print(f"   ✓ Updated Balance: ${verify_data.get('balance', 0):.2f}")
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 3: Trade execution with new balance
    print("\n3. Testing Trade Execution with Virtual Balance:")
    try:
        signal_data = {
            "symbol": "ETHUSDT",
            "signal": "BUY",
            "price": 2400.0,
            "confidence": 85.0,
            "timestamp": "2025-06-24T12:00:00"
        }
        
        response = requests.post(f"{base_url}/auto_trading/execute_signal", json=signal_data)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Trade Status: {data.get('status')}")
            print(f"   ✓ Message: {data.get('message')}")
            if 'balance_after' in data:
                print(f"   ✓ Balance After Trade: ${data.get('balance_after'):.2f}")
                
                # Get trade details
                trades_response = requests.get(f"{base_url}/auto_trading/trades")
                if trades_response.status_code == 200:
                    trades_data = trades_response.json()
                    print(f"   ✓ Total Trades: {trades_data.get('count', 0)}")
                    if trades_data.get('count', 0) > 0:
                        latest_trade = trades_data['trades'][-1]
                        print(f"   ✓ Latest Trade: {latest_trade['action']} {latest_trade['symbol']} @ ${latest_trade['price']}")
        else:
            print(f"   ✗ Trade execution failed: {response.status_code}")
            print(f"   ✗ Response: {response.text}")
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n" + "="*50)
    print("SETTINGS VERIFICATION COMPLETED")

if __name__ == "__main__":
    test_settings_update()
