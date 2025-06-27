#!/usr/bin/env python3
"""
Test auto trading metrics calculation to verify dashboard should display correctly
"""
import requests
import json

API_URL = "http://localhost:8001"

def test_auto_trading_metrics():
    print("🧪 Testing Auto Trading Metrics Calculation...")
    print()
    
    # Get auto trading status
    print("1. Fetching auto trading status...")
    status_resp = requests.get(f"{API_URL}/auto_trading/status")
    if status_resp.status_code == 200:
        status_data = status_resp.json()
        if status_data["status"] == "success":
            state = status_data["auto_trading"]
            print(f"   ✅ Status: {json.dumps(state, indent=6)}")
    
    # Get auto trading trades
    print("\n2. Fetching auto trading trades...")
    trades_resp = requests.get(f"{API_URL}/auto_trading/trades")
    if trades_resp.status_code == 200:
        trades_data = trades_resp.json()
        if trades_data["status"] == "success":
            all_trades = trades_data["trades"]
            print(f"   ✅ Trades: {json.dumps(all_trades, indent=6)}")
            
            # Calculate metrics like the dashboard callback does
            print("\n3. Calculating metrics (like dashboard callback)...")
            total_trades_count = len(all_trades)
            executed_trades = [t for t in all_trades if t.get("status") == "executed"]
            wins = len(executed_trades)
            losses = 0  # Temporary since we don't track losses yet
            
            if total_trades_count > 0:
                winrate = f"{(wins / total_trades_count) * 100:.1f}%"
            else:
                winrate = "0%"
            
            trades_display = str(total_trades_count)
            wl_ratio = f"{wins}/{losses}"
            
            print(f"   📊 Dashboard should show:")
            print(f"      Total Trades: {trades_display}")
            print(f"      Win Rate: {winrate}")
            print(f"      W/L Ratio: {wl_ratio}")
            print(f"      Balance: ${state.get('balance', 0):,.2f}")
            print(f"      P&L: ${state.get('total_profit', 0):,.2f}")
            
    print("\n✅ Metrics test complete!")
    print("If dashboard still shows 0 trades, there may be a callback or interval issue.")

if __name__ == "__main__":
    test_auto_trading_metrics()
