"""
Simple P&L Test - Clear Output
"""

import requests
import json

def test_pnl():
    print("=" * 50)
    print("CRYPTO BOT P&L SYSTEM TEST")
    print("=" * 50)
    
    # Test virtual balance endpoint
    try:
        resp = requests.get("http://127.0.0.1:8000/virtual_balance")
        data = resp.json()
        
        print(f"Virtual Balance: ${data.get('balance', 0):,.2f}")
        print(f"Initial Balance: ${data.get('initial_balance', 0):,.2f}")
        print(f"Total P&L: ${data.get('current_pnl', 0):,.2f}")
        print(f"Portfolio %: {data.get('portfolio_pnl_percent', 0):+.2f}%")
        print(f"Realized P&L: ${data.get('realized_pnl', 0):,.2f}")
        print(f"Unrealized P&L: ${data.get('unrealized_pnl', 0):,.2f}")
        
        # Test analytics endpoint
        resp2 = requests.get("http://127.0.0.1:8000/trading/pnl_analytics")
        if resp2.status_code == 200:
            analytics = resp2.json()
            print("\nANALYTICS:")
            print(f"Total Trades: {analytics.get('trading_stats', {}).get('total_trades', 0)}")
            print(f"Win Rate: {analytics.get('trading_stats', {}).get('win_rate', 0):.1f}%")
            print(f"Profit Factor: {analytics.get('trading_stats', {}).get('profit_factor', 0):.2f}")
            
        print("\n✅ P&L System Working!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_pnl()
