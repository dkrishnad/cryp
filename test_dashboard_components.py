"""
Test Dashboard Component Updates
Check if dashboard components are receiving updates
"""

import requests
import time

API_URL = "http://127.0.0.1:8000"

def test_all_components():
    print("=== TESTING DASHBOARD COMPONENT UPDATES ===")
    
    # 1. Enable auto trading first
    print("\n1. Enabling auto trading...")
    resp = requests.post(f"{API_URL}/auto_trading/toggle", json={"enabled": True})
    if resp.status_code == 200:
        data = resp.json()
        print(f"✅ Toggle successful: {data}")
    else:
        print(f"❌ Toggle failed: {resp.status_code}")
    
    # Wait for dashboard to update
    time.sleep(3)
    
    # 2. Check all endpoint data
    print("\n2. Checking all API endpoints...")
    
    # Virtual Balance
    resp = requests.get(f"{API_URL}/virtual_balance")
    if resp.status_code == 200:
        data = resp.json()
        if data.get("status") == "success":
            balance = data.get("balance", 0)
            pnl = data.get("current_pnl", 0)
            print(f"   Virtual Balance: ${balance:,.2f}")
            print(f"   Current P&L: ${pnl:,.2f}")
    
    # Auto Trading Status
    resp = requests.get(f"{API_URL}/auto_trading/status")
    if resp.status_code == 200:
        data = resp.json()
        if data.get("status") == "success":
            auto_trading = data.get("auto_trading", {})
            enabled = auto_trading.get("enabled", False)
            print(f"   Auto Trading Enabled: {enabled}")
    
    # Trades
    resp = requests.get(f"{API_URL}/auto_trading/trades")
    if resp.status_code == 200:
        data = resp.json()
        if data.get("status") == "success":
            count = data.get("count", 0)
            summary = data.get("summary", {})
            win_rate = summary.get("win_rate", 0)
            wins = summary.get("winning_trades", 0)
            losses = summary.get("losing_trades", 0)
            print(f"   Total Trades: {count}")
            print(f"   Win Rate: {win_rate:.1f}%")
            print(f"   Wins/Losses: {wins}/{losses}")
    
    # 3. Check signal
    resp = requests.get(f"{API_URL}/auto_trading/current_signal")
    if resp.status_code == 200:
        data = resp.json()
        if data.get("status") == "success" and data.get("signal"):
            signal = data["signal"]
            direction = signal.get("direction", "")
            confidence = signal.get("confidence", 0)
            print(f"   Current Signal: {direction} ({confidence:.1f}%)")
    
    print("\n3. Expected Dashboard Values:")
    print("   - Auto Trading Toggle: Should be ON")
    print("   - Virtual Balance: Should show dollar amount")
    print("   - Total P&L: Should show dollar amount")
    print("   - Total Trades: Should show number")
    print("   - Win Rate: Should show percentage")
    print("   - Current Signal: Should show BUY with confidence")
    
    print("\n4. If dashboard still shows empty values, there's a callback/UI issue")
    print("   Check: http://127.0.0.1:8050 -> Auto Trading tab")

if __name__ == "__main__":
    test_all_components()
