"""
Dashboard P&L Verification Script
"""

import requests
import time

def verify_dashboard_pnl():
    print("🔥 CRYPTO BOT - TRADING PLATFORM STYLE P&L VERIFICATION")
    print("=" * 70)
    
    try:
        # Get current P&L data
        resp = requests.get("http://127.0.0.1:8000/virtual_balance")
        data = resp.json()
        
        balance = data.get("balance", 0)
        initial = data.get("initial_balance", 0)
        total_pnl = data.get("current_pnl", 0)
        pnl_percent = data.get("portfolio_pnl_percent", 0)
        realized = data.get("realized_pnl", 0)
        unrealized = data.get("unrealized_pnl", 0)
        
        print("📊 CURRENT P&L STATUS (should match dashboard):")
        print("-" * 50)
        print(f"💰 Current Balance: ${balance:,.2f}")
        print(f"🏦 Initial Balance: ${initial:,.2f}")
        print(f"📈 Total P&L: ${total_pnl:,.2f} ({pnl_percent:+.2f}%)")
        print(f"✅ Realized P&L: ${realized:,.2f}")
        print(f"⏳ Unrealized P&L: ${unrealized:,.2f}")
        
        # Color-coded display like trading platforms
        if total_pnl >= 0:
            status = "🟢 PROFIT"
            color = "GREEN"
        else:
            status = "🔴 LOSS"
            color = "RED"
            
        print(f"\n{status} - Display Color: {color}")
        
        # Get analytics
        analytics_resp = requests.get("http://127.0.0.1:8000/trading/pnl_analytics")
        if analytics_resp.status_code == 200:
            analytics = analytics_resp.json()
            trading_stats = analytics.get('trading_stats', {})
            
            print(f"\n📊 TRADING STATISTICS:")
            print(f"   Total Trades: {trading_stats.get('total_trades', 0)}")
            print(f"   Win Rate: {trading_stats.get('win_rate', 0):.1f}%")
            print(f"   Profit Factor: {trading_stats.get('profit_factor', 0):.2f}")
        
        print("\n🎯 DASHBOARD SHOULD SHOW:")
        print("   ✅ P&L with both $ amount and % change")
        print("   ✅ Green for profit, Red for loss")
        print("   ✅ Professional trading platform formatting")
        print("   ✅ Real-time updates via interval callbacks")
        
        print(f"\n🌐 Dashboard URL: http://localhost:8050")
        print("💡 Refresh dashboard to see latest P&L data!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verify_dashboard_pnl()
