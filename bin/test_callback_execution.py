"""
Force Dashboard Callback Test
Directly test the dashboard callback to see if it's working
"""

import requests
import time
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

def test_dashboard_callback():
    """Test what the dashboard callback should return"""
    print("=== Testing Dashboard Callback Logic ===")
    print(f"Timestamp: {datetime.now()}")
    
    try:
        # Step 1: Test auto trading status API
        print("\n1. Auto Trading Status API:")
        resp = requests.get(f"{API_URL}/auto_trading/status")
        print(f"   Status Code: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"   Response type: {type(data)}")
            print(f"   Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            
            if isinstance(data, dict) and data.get("status") == "success":
                state = data.get("auto_trading", {})
                print(f"   Auto trading state type: {type(state)}")
                print(f"   Auto trading state keys: {list(state.keys()) if isinstance(state, dict) else 'Not a dict'}")
                
                if isinstance(state, dict):
                    backend_enabled = bool(state.get("enabled", False))
                    print(f"   Backend enabled: {backend_enabled}")
                    
                    # Status message
                    if backend_enabled:
                        status_msg = "Auto Trading Active"
                        status_class = "text-success"
                    else:
                        status_msg = "Auto Trading Paused"
                        status_class = "text-warning"
                    print(f"   Status: {status_msg} ({status_class})")
                else:
                    print(f"   ERROR: State is not a dict: {state}")
                    return
            else:
                print(f"   ERROR: Unexpected response structure: {data}")
                return
        else:
            print(f"   ERROR: HTTP {resp.status_code}")
            return
        
        # Step 2: Test virtual balance API
        print("\n2. Virtual Balance API:")
        balance_resp = requests.get(f"{API_URL}/virtual_balance")
        print(f"   Status Code: {balance_resp.status_code}")
        
        if balance_resp.status_code == 200:
            balance_data = balance_resp.json()
            print(f"   Response type: {type(balance_data)}")
            print(f"   Response keys: {list(balance_data.keys()) if isinstance(balance_data, dict) else 'Not a dict'}")
            
            if isinstance(balance_data, dict) and balance_data.get("status") == "success":
                virtual_balance = float(balance_data.get("balance", 10000.0))
                current_pnl = float(balance_data.get("current_pnl", 0.0))
                
                balance_display = f"${virtual_balance:,.2f}"
                pnl_display = f"${current_pnl:,.2f}"
                pnl_color = "text-success" if current_pnl >= 0 else "text-danger"
                
                print(f"   Virtual balance: {virtual_balance}")
                print(f"   Current P&L: {current_pnl}")
                print(f"   Balance display: {balance_display}")
                print(f"   P&L display: {pnl_display} ({pnl_color})")
            else:
                print(f"   ERROR: Unexpected balance response: {balance_data}")
                return
        else:
            print(f"   ERROR: HTTP {balance_resp.status_code}")
            return
        
        # Step 3: Test trades API
        print("\n3. Trades API:")
        trades_resp = requests.get(f"{API_URL}/auto_trading/trades")
        print(f"   Status Code: {trades_resp.status_code}")
        
        if trades_resp.status_code == 200:
            trades_data = trades_resp.json()
            print(f"   Response type: {type(trades_data)}")
            print(f"   Response keys: {list(trades_data.keys()) if isinstance(trades_data, dict) else 'Not a dict'}")
            
            if isinstance(trades_data, dict) and trades_data.get("status") == "success":
                trades_summary = trades_data.get("summary", {})
                total_trades_count = int(trades_data.get("count", 0))
                
                wins = int(trades_summary.get("winning_trades", 0))
                losses = int(trades_summary.get("losing_trades", 0))
                win_rate = float(trades_summary.get("win_rate", 0))
                
                winrate_display = f"{win_rate:.1f}%"
                trades_display = str(total_trades_count)
                wl_display = f"{wins}/{losses}"
                
                print(f"   Total trades: {total_trades_count}")
                print(f"   Wins: {wins}")
                print(f"   Losses: {losses}")
                print(f"   Win rate: {win_rate}")
                print(f"   Winrate display: {winrate_display}")
                print(f"   Trades display: {trades_display}")
                print(f"   W/L display: {wl_display}")
            else:
                print(f"   ERROR: Unexpected trades response: {trades_data}")
                return
        else:
            print(f"   ERROR: HTTP {trades_resp.status_code}")
            return
        
        # Step 4: Simulate callback return
        print("\n4. Simulated Callback Return:")
        print(f"   Return values would be:")
        print(f"   - status: {status_msg}")
        print(f"   - balance_display: {balance_display}")
        print(f"   - pnl_display: {pnl_display}")
        print(f"   - winrate: {winrate_display}")
        print(f"   - trades: {trades_display}")
        print(f"   - wl_ratio: {wl_display}")
        print(f"   - toggle_value: {backend_enabled}")
        
        return {
            'status': status_msg,
            'balance': balance_display,
            'pnl': pnl_display,
            'winrate': winrate_display,
            'trades': trades_display,
            'wl': wl_display,
            'enabled': backend_enabled
        }
        
    except Exception as e:
        print(f"ERROR: Exception in callback test: {e}")
        return None

if __name__ == "__main__":
    result = test_dashboard_callback()
    if result:
        print(f"\n✅ Callback test successful!")
        print(f"Expected UI values: {result}")
    else:
        print(f"\n❌ Callback test failed!")
