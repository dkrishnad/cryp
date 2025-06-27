"""
Test Comprehensive P&L System Like Popular Trading Platforms
"""

import requests
import json

API_URL = "http://127.0.0.1:8000"

def test_comprehensive_pnl():
    print("🔥 TESTING COMPREHENSIVE P&L SYSTEM")
    print("=" * 60)
    print("Testing P&L system similar to TradingView, MetaTrader, Binance, eToro")
    print()
    
    # Test 1: Basic Virtual Balance with Comprehensive P&L
    print("1️⃣ VIRTUAL BALANCE WITH COMPREHENSIVE P&L")
    print("-" * 40)
    try:
        resp = requests.get(f"{API_URL}/virtual_balance")
        if resp.status_code == 200:
            data = resp.json()
            
            balance = data.get("balance", 0)
            total_pnl = data.get("current_pnl", 0)
            realized_pnl = data.get("realized_pnl", 0)
            unrealized_pnl = data.get("unrealized_pnl", 0)
            portfolio_percent = data.get("portfolio_pnl_percent", 0)
            initial_balance = data.get("initial_balance", 0)
            
            print(f"💰 Current Balance: ${balance:,.2f}")
            print(f"💹 Total P&L: ${total_pnl:,.2f} ({portfolio_percent:+.2f}%)")
            print(f"✅ Realized P&L: ${realized_pnl:,.2f}")
            print(f"⏳ Unrealized P&L: ${unrealized_pnl:,.2f}")
            print(f"🏦 Initial Balance: ${initial_balance:,.2f}")
            
            # Open positions
            open_positions = data.get("open_positions", [])
            if open_positions:
                print(f"\n📊 OPEN POSITIONS ({len(open_positions)}):")
                for pos in open_positions:
                    symbol = pos.get("symbol", "")
                    action = pos.get("action", "")
                    entry = pos.get("entry_price", 0)
                    current = pos.get("current_price", 0)
                    pnl = pos.get("unrealized_pnl", 0)
                    pnl_percent = pos.get("unrealized_pnl_percent", 0)
                    print(f"   {symbol} {action}: Entry=${entry:.4f}, Current=${current:.4f}, P&L=${pnl:,.2f} ({pnl_percent:+.2f}%)")
            else:
                print("\n📊 No open positions")
                
        else:
            print(f"❌ Error: {resp.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    
    # Test 2: Advanced P&L Analytics
    print("2️⃣ ADVANCED P&L ANALYTICS (Like TradingView)")
    print("-" * 40)
    try:
        resp = requests.get(f"{API_URL}/trading/pnl_analytics")
        if resp.status_code == 200:
            data = resp.json()
            
            summary = data.get("summary", {})
            performance = data.get("performance", {})
            trading_stats = data.get("trading_stats", {})
            
            print("📈 PERFORMANCE SUMMARY:")
            print(f"   Total P&L: ${summary.get('total_pnl', 0):,.2f}")
            print(f"   Realized: ${summary.get('realized_pnl', 0):,.2f}")
            print(f"   Unrealized: ${summary.get('unrealized_pnl', 0):,.2f}")
            print(f"   Portfolio %: {summary.get('portfolio_pnl_percent', 0):+.2f}%")
            print(f"   Daily P&L: ${summary.get('daily_pnl', 0):,.2f}")
            
            print("\n📊 TRADING STATISTICS:")
            print(f"   Total Trades: {trading_stats.get('total_trades', 0)}")
            print(f"   Win Rate: {trading_stats.get('win_rate', 0):.1f}%")
            print(f"   Profit Factor: {trading_stats.get('profit_factor', 0):.2f}")
            print(f"   Avg Win: ${trading_stats.get('avg_win', 0):,.2f}")
            print(f"   Avg Loss: ${trading_stats.get('avg_loss', 0):,.2f}")
            
            print("\n🏦 ACCOUNT PERFORMANCE:")
            print(f"   Initial: ${performance.get('initial_balance', 0):,.2f}")
            print(f"   Current: ${performance.get('current_balance', 0):,.2f}")
            print(f"   Max Drawdown: ${performance.get('max_drawdown', 0):,.2f} ({performance.get('max_drawdown_percent', 0):.2f}%)")
            print(f"   Total Return: {performance.get('total_return_percent', 0):+.2f}%")
            
        else:
            print(f"❌ Analytics Error: {resp.status_code}")
    except Exception as e:
        print(f"❌ Analytics Error: {e}")
    
    print()
    print("🎯 DASHBOARD SHOULD NOW DISPLAY:")
    print("   ✅ Professional P&L with percentage")
    print("   ✅ Realized vs Unrealized breakdown")
    print("   ✅ Color-coded profit/loss indicators")
    print("   ✅ Trading platform style formatting")
    print()
    print("📱 Refresh your dashboard to see the enhanced P&L system!")

if __name__ == "__main__":
    test_comprehensive_pnl()
