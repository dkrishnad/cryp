"""
Silent P&L Status Check
"""

import requests
import sys

try:
    vb_resp = requests.get("http://127.0.0.1:8000/virtual_balance", timeout=5)
    vb_data = vb_resp.json()
    
    balance = vb_data.get("balance", 0)
    initial = vb_data.get("initial_balance", 0)
    pnl = vb_data.get("current_pnl", 0)
    pnl_percent = vb_data.get("portfolio_pnl_percent", 0)
    
    print("\n🎯 CRYPTO BOT P&L STATUS:")
    print(f"   Balance: ${balance:,.2f}")
    print(f"   P&L: ${pnl:,.2f} ({pnl_percent:+.2f}%)")
    print(f"   Status: {'🟢 PROFIT' if pnl >= 0 else '🔴 LOSS'}")
    print("   ✅ System: OPERATIONAL")
    print("   🌐 Dashboard: http://localhost:8050")
    
except Exception as e:
    print(f"❌ {e}")
    sys.exit(1)
