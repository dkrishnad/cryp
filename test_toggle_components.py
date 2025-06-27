"""
Test Auto Trading Toggle and Component Values
"""

import requests
import json

API_URL = "http://127.0.0.1:8000"

def test_toggle_auto_trading():
    """Test toggling auto trading on/off"""
    print("🔄 Testing Auto Trading Toggle...")
    
    # First, check current status
    print("\n1. Current Status:")
    resp = requests.get(f"{API_URL}/auto_trading/status")
    if resp.status_code == 200:
        data = resp.json()
        current_enabled = data.get("auto_trading", {}).get("enabled", False)
        print(f"   Currently enabled: {current_enabled}")
    
    # Toggle ON
    print("\n2. Toggling ON:")
    toggle_resp = requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": True})
    if toggle_resp.status_code == 200:
        toggle_data = toggle_resp.json()
        print(f"   Toggle response: {json.dumps(toggle_data, indent=2)}")
    else:
        print(f"   Toggle error: {toggle_resp.status_code} - {toggle_resp.text}")
    
    # Check status after toggle
    print("\n3. Status after toggle ON:")
    resp = requests.get(f"{API_URL}/auto_trading/status")
    if resp.status_code == 200:
        data = resp.json()
        print(f"   Response: {json.dumps(data, indent=2)}")
        enabled = data.get("auto_trading", {}).get("enabled", False)
        print(f"   Now enabled: {enabled}")

def test_virtual_balance_detailed():
    """Test virtual balance API in detail"""
    print("\n💰 Testing Virtual Balance API...")
    
    resp = requests.get(f"{API_URL}/virtual_balance")
    if resp.status_code == 200:
        data = resp.json()
        print(f"   Raw response: {json.dumps(data, indent=2)}")
        
        # Test parsing like dashboard does
        if isinstance(data, dict) and data.get("status") == "success":
            balance = float(data.get("balance", 10000.0))
            current_pnl = float(data.get("current_pnl", 0.0))
            print(f"   Parsed balance: ${balance:,.2f}")
            print(f"   Parsed P&L: ${current_pnl:,.2f}")
            
            # Format like dashboard
            balance_display = f"${balance:,.2f}"
            pnl_display = f"${current_pnl:,.2f}"
            print(f"   Dashboard format balance: {balance_display}")
            print(f"   Dashboard format P&L: {pnl_display}")
        else:
            print(f"   ERROR: Unexpected response structure")
    else:
        print(f"   ERROR: Status {resp.status_code} - {resp.text}")

def test_trades_api():
    """Test trades API"""
    print("\n📊 Testing Trades API...")
    
    resp = requests.get(f"{API_URL}/auto_trading/trades")
    if resp.status_code == 200:
        data = resp.json()
        print(f"   Raw response: {json.dumps(data, indent=2)}")
        
        if isinstance(data, dict) and data.get("status") == "success":
            trades_summary = data.get("summary", {})
            total_trades = data.get("count", 0)
            wins = trades_summary.get("winning_trades", 0)
            losses = trades_summary.get("losing_trades", 0)
            win_rate = trades_summary.get("win_rate", 0)
            
            print(f"   Total trades: {total_trades}")
            print(f"   Wins: {wins}")
            print(f"   Losses: {losses}")
            print(f"   Win rate: {win_rate:.1f}%")
            
            # Format like dashboard
            winrate_display = f"{win_rate:.1f}%"
            trades_display = str(total_trades)
            wl_display = f"{wins}/{losses}"
            print(f"   Dashboard format win rate: {winrate_display}")
            print(f"   Dashboard format trades: {trades_display}")
            print(f"   Dashboard format W/L: {wl_display}")
        else:
            print(f"   ERROR: Unexpected response structure")
    else:
        print(f"   ERROR: Status {resp.status_code} - {resp.text}")

if __name__ == "__main__":
    print("=== Auto Trading Component Test ===")
    test_toggle_auto_trading()
    test_virtual_balance_detailed()
    test_trades_api()
    print("\n✅ Test complete")
