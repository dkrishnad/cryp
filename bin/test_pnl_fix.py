"""
Test P&L Calculation Fix
"""

import requests

try:
    resp = requests.get("http://127.0.0.1:8000/virtual_balance")
    print(f"Status: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"Response: {data}")
        
        balance = data.get("balance", 0)
        current_pnl = data.get("current_pnl", 0)
        total_value = data.get("total_value", 0)
        
        print(f"\n💰 BALANCE SUMMARY:")
        print(f"Current Balance: ${balance:,.2f}")
        print(f"P&L: ${current_pnl:,.2f}")
        print(f"Total Value: ${total_value:,.2f}")
        
        # Expected calculation
        initial = 10000.0
        expected_pnl = balance - initial
        print(f"\n🧮 EXPECTED:")
        print(f"Expected P&L: ${balance:,.2f} - ${initial:,.2f} = ${expected_pnl:,.2f}")
        
        if abs(current_pnl - expected_pnl) < 0.01:
            print("✅ P&L calculation is correct!")
        else:
            print("❌ P&L calculation is incorrect!")
            
    else:
        print(f"Error: {resp.text}")
        
except Exception as e:
    print(f"Error: {e}")

print("\nRefresh the dashboard to see the corrected P&L!")
