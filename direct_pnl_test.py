"""
Direct P&L Test - Check if backend returns correct values
"""

import requests
import json

print("=== TESTING P&L CALCULATION ===")

try:
    # Call virtual balance API
    resp = requests.get("http://127.0.0.1:8000/virtual_balance", timeout=5)
    
    if resp.status_code == 200:
        data = resp.json()
        
        balance = data.get("balance", 0)
        current_pnl = data.get("current_pnl", 0)
        
        print(f"✅ API Response:")
        print(f"   Balance: ${balance:,.2f}")
        print(f"   P&L: ${current_pnl:,.2f}")
        
        # Calculate what it should be
        initial = 10000.0
        expected_pnl = balance - initial
        
        print(f"\n🧮 Expected Calculation:")
        print(f"   ${balance:,.2f} - ${initial:,.2f} = ${expected_pnl:,.2f}")
        
        if abs(current_pnl - expected_pnl) < 0.01:
            print("\n✅ P&L calculation is now CORRECT!")
            print("The dashboard should update within 5 seconds to show the correct P&L.")
        else:
            print(f"\n❌ P&L is still incorrect!")
            print(f"   Got: ${current_pnl:,.2f}")
            print(f"   Expected: ${expected_pnl:,.2f}")
    else:
        print(f"❌ API Error: {resp.status_code}")
        print(f"Response: {resp.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    
print("\n📱 Check the dashboard now - the P&L should show as approximately -$1,937")
print("(if balance is $8,063 and initial was $10,000)")
