#!/usr/bin/env python3
"""
Comprehensive test script to verify all dashboard settings and functionality
"""
import requests
import json
import time
from datetime import datetime

# Backend URL
BASE_URL = "http://localhost:8001"
DASHBOARD_URL = "http://127.0.0.1:8050"

def test_endpoint(url, method="GET", data=None, description=""):
    """Test an API endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=data, timeout=10)
        
        print(f"✓ {description}: {response.status_code}")
        if response.status_code == 200:
            try:
                result = response.json()
                if "status" in result and result["status"] == "success":
                    print(f"  → Success: {result}")
                    return result
                else:
                    print(f"  → Response: {result}")
                    return result
            except:
                print(f"  → Text response: {response.text[:100]}...")
                return response.text
        else:
            print(f"  → Error: {response.text}")
            return None
    except Exception as e:
        print(f"✗ {description}: Error - {e}")
        return None

def main():
    print("="*80)
    print("COMPREHENSIVE DASHBOARD SETTINGS TEST")
    print("="*80)
    
    print("\n1. TESTING BACKEND CONNECTIVITY")
    print("-"*50)
    
    # Test basic endpoints
    test_endpoint(f"{BASE_URL}/health", description="Backend Health Check")
    test_endpoint(f"{BASE_URL}/status", description="Backend Status")
    
    print("\n2. TESTING VIRTUAL BALANCE SYSTEM")
    print("-"*50)
    
    # Test virtual balance
    balance_result = test_endpoint(f"{BASE_URL}/virtual_balance", description="Get Virtual Balance")
    
    # Test virtual balance update
    new_balance_data = {"balance": 12000.0}
    test_endpoint(f"{BASE_URL}/virtual_balance", method="POST", data=new_balance_data, description="Update Virtual Balance")
    
    # Verify balance updated
    test_endpoint(f"{BASE_URL}/virtual_balance", description="Verify Balance Updated")
    
    # Reset balance
    test_endpoint(f"{BASE_URL}/virtual_balance/reset", method="POST", description="Reset Virtual Balance")
    
    print("\n3. TESTING AUTO TRADING SETTINGS")
    print("-"*50)
    
    # Test auto trading status
    test_endpoint(f"{BASE_URL}/auto_trading/status", description="Get Auto Trading Status")
    
    # Test auto trading settings
    test_endpoint(f"{BASE_URL}/auto_trading/settings", description="Get Auto Trading Settings")
    
    # Update auto trading settings
    settings_data = {
        "enabled": True,
        "confidence_threshold": 75.0,
        "amount_config": {
            "amount": 150.0,
            "percentage": 10.0
        },
        "stop_loss": 3.0,
        "take_profit": 8.0
    }
    test_endpoint(f"{BASE_URL}/auto_trading/settings", method="POST", data=settings_data, description="Update Auto Trading Settings")
    
    # Verify settings updated
    test_endpoint(f"{BASE_URL}/auto_trading/settings", description="Verify Settings Updated")
    
    print("\n4. TESTING TRADE EXECUTION SYSTEM")
    print("-"*50)
    
    # Test current signal
    test_endpoint(f"{BASE_URL}/auto_trading/current_signal", description="Get Current Signal")
    
    # Test trade execution with mock signal
    signal_data = {
        "symbol": "BTCUSDT",
        "signal": "BUY",
        "price": 43000.0,
        "confidence": 82.5,
        "timestamp": datetime.now().isoformat()
    }
    trade_result = test_endpoint(f"{BASE_URL}/auto_trading/execute_signal", method="POST", data=signal_data, description="Execute Test Signal")
    
    # Get trades
    trades_result = test_endpoint(f"{BASE_URL}/auto_trading/trades", description="Get Auto Trading Trades")
    
    # Close the trade if it was created
    if trade_result and "trade" in trade_result:
        trade_id = trade_result["trade"]["id"]
        test_endpoint(f"{BASE_URL}/auto_trading/close_trade/{trade_id}", method="POST", description=f"Close Trade {trade_id}")
    
    print("\n5. TESTING ML PREDICTIONS AND DATA")
    print("-"*50)
    
    # Test ML prediction
    test_endpoint(f"{BASE_URL}/predict", description="Get ML Prediction")
    
    # Test available symbols
    test_endpoint(f"{BASE_URL}/symbols", description="Get Available Symbols")
    
    # Test data for a symbol
    test_endpoint(f"{BASE_URL}/data/BTCUSDT", description="Get BTCUSDT Data")
    
    print("\n6. TESTING HYBRID LEARNING SETTINGS")
    print("-"*50)
    
    # Test hybrid learning status
    test_endpoint(f"{BASE_URL}/hybrid_learning/status", description="Get Hybrid Learning Status")
    
    # Test hybrid learning settings
    test_endpoint(f"{BASE_URL}/hybrid_learning/settings", description="Get Hybrid Learning Settings")
    
    print("\n7. TESTING EMAIL CONFIGURATION")
    print("-"*50)
    
    # Test email settings
    test_endpoint(f"{BASE_URL}/email_settings", description="Get Email Settings")
    
    # Update email settings
    email_data = {
        "enabled": True,
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "email": "test@example.com",
        "password": "app_password"
    }
    test_endpoint(f"{BASE_URL}/email_settings", method="POST", data=email_data, description="Update Email Settings")
    
    print("\n8. TESTING NOTIFICATIONS")
    print("-"*50)
    
    # Test notifications
    test_endpoint(f"{BASE_URL}/notifications", description="Get Notifications")
    
    print("\n9. TESTING DASHBOARD ACCESSIBILITY")
    print("-"*50)
    
    # Test dashboard main page
    try:
        response = requests.get(DASHBOARD_URL, timeout=10)
        if response.status_code == 200:
            print(f"✓ Dashboard Main Page: {response.status_code}")
            print(f"  → Dashboard is accessible and serving content")
        else:
            print(f"✗ Dashboard Main Page: {response.status_code}")
    except Exception as e:
        print(f"✗ Dashboard Main Page: Error - {e}")
    
    print("\n10. TESTING FINAL BALANCE STATE")
    print("-"*50)
    
    # Final balance check
    final_balance = test_endpoint(f"{BASE_URL}/virtual_balance", description="Final Virtual Balance Check")
    final_trades = test_endpoint(f"{BASE_URL}/auto_trading/trades", description="Final Trades Summary")
    
    print("\n" + "="*80)
    print("DASHBOARD SETTINGS TEST COMPLETED")
    print("="*80)
    
    if final_balance:
        print(f"Final Balance: ${final_balance.get('balance', 0):.2f}")
        print(f"Current P&L: ${final_balance.get('current_pnl', 0):.2f}")
        print(f"Total Value: ${final_balance.get('total_value', 0):.2f}")
    
    if final_trades and "summary" in final_trades:
        summary = final_trades["summary"]
        print(f"Total Trades: {final_trades.get('count', 0)}")
        print(f"Open Trades: {summary.get('open_trades', 0)}")
        print(f"Win Rate: {summary.get('win_rate', 0):.1f}%")
        print(f"Total P&L: ${summary.get('total_pnl', 0):.2f}")

if __name__ == "__main__":
    main()
