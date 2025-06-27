"""
Debug Dashboard Component IDs and Callback Outputs
Check if the callback outputs match the component IDs in the layout
"""

import requests
import json

# Backend URL
API_URL = "http://127.0.0.1:8000"

def test_backend_apis():
    """Test all backend APIs that feed the dashboard"""
    print("🔍 Testing Backend APIs...")
    
    # 1. Virtual Balance API
    print("\n1. Virtual Balance API:")
    try:
        resp = requests.get(f"{API_URL}/virtual_balance", timeout=3)
        print(f"   Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
        else:
            print(f"   Error: {resp.text}")
    except Exception as e:
        print(f"   Exception: {e}")
    
    # 2. Auto Trading Status API
    print("\n2. Auto Trading Status API:")
    try:
        resp = requests.get(f"{API_URL}/auto_trading/status", timeout=3)
        print(f"   Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
        else:
            print(f"   Error: {resp.text}")
    except Exception as e:
        print(f"   Exception: {e}")
    
    # 3. Auto Trading Trades API
    print("\n3. Auto Trading Trades API:")
    try:
        resp = requests.get(f"{API_URL}/auto_trading/trades", timeout=3)
        print(f"   Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
        else:
            print(f"   Error: {resp.text}")
    except Exception as e:
        print(f"   Exception: {e}")

def check_component_ids():
    """List the expected component IDs from the layout"""
    print("\n🔍 Expected Component IDs from Layout:")
    print("   virtual-balance (main layout)")
    print("   auto-balance-display (auto trading tab)")
    print("   auto-pnl-display (auto trading tab)")
    print("   auto-winrate-display (auto trading tab)")
    print("   auto-trades-display (auto trading tab)")
    print("   auto-wl-display (auto trading tab)")
    print("   auto-trading-toggle (auto trading tab)")
    print("   auto-trading-status (auto trading tab)")

def simulate_callback_logic():
    """Simulate the callback logic to see what should be returned"""
    print("\n🔍 Simulating Callback Logic...")
    
    try:
        # Get auto trading status
        resp = requests.get(f"{API_URL}/auto_trading/status")
        if resp.status_code == 200:
            data = resp.json()
            state = data.get("auto_trading", {})
            backend_enabled = bool(state.get("enabled", False))
            print(f"   Backend enabled: {backend_enabled}")
            
            # Get virtual balance
            balance_resp = requests.get(f"{API_URL}/virtual_balance")
            if balance_resp.status_code == 200:
                balance_data = balance_resp.json()
                virtual_balance = float(balance_data.get("balance", 10000.0))
                current_pnl = float(balance_data.get("current_pnl", 0.0))
                print(f"   Virtual balance: ${virtual_balance:,.2f}")
                print(f"   Current P&L: ${current_pnl:,.2f}")
                
                # Format displays
                balance_display = f"${virtual_balance:,.2f}"
                pnl_display = f"${current_pnl:,.2f}"
                print(f"   Balance display: {balance_display}")
                print(f"   P&L display: {pnl_display}")
            
            # Get trades
            trades_resp = requests.get(f"{API_URL}/auto_trading/trades")
            if trades_resp.status_code == 200:
                trades_data = trades_resp.json()
                if trades_data.get("status") == "success":
                    trades_summary = trades_data.get("summary", {})
                    total_trades = trades_data.get("count", 0)
                    wins = trades_summary.get("winning_trades", 0)
                    losses = trades_summary.get("losing_trades", 0)
                    win_rate = trades_summary.get("win_rate", 0)
                    
                    print(f"   Total trades: {total_trades}")
                    print(f"   Win rate: {win_rate:.1f}%")
                    print(f"   W/L ratio: {wins}/{losses}")
    
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    print("=== Dashboard Component Debug ===")
    check_component_ids()
    test_backend_apis()
    simulate_callback_logic()
    print("\n✅ Debug complete")
