#!/usr/bin/env python3
"""
Final Virtual Balance Verification
"""
import requests
import json

API_URL = "http://localhost:8001"

print("🎯 FINAL VIRTUAL BALANCE VERIFICATION")
print("=" * 50)

# Test all endpoints that should show balance
endpoints_to_test = [
    {
        "name": "Virtual Balance",
        "url": f"{API_URL}/virtual_balance",
        "balance_path": ["balance"]
    },
    {
        "name": "Auto Trading Status", 
        "url": f"{API_URL}/auto_trading/status",
        "balance_path": ["auto_trading", "balance"]
    }
]

balances = {}

for endpoint in endpoints_to_test:
    print(f"\n📡 Testing {endpoint['name']}:")
    try:
        resp = requests.get(endpoint["url"], timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            
            # Navigate to balance using path
            current = data
            for key in endpoint["balance_path"]:
                current = current.get(key, {})
            
            if isinstance(current, (int, float)):
                balance = current
                balances[endpoint["name"]] = balance
                print(f"   ✅ Balance: ${balance:,.2f}")
            else:
                print(f"   ❌ Balance not found at path: {' -> '.join(endpoint['balance_path'])}")
                print(f"   📋 Response: {json.dumps(data, indent=2)}")
        else:
            print(f"   ❌ HTTP {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

# Final verification
print(f"\n🔍 SYNCHRONIZATION CHECK:")
if len(balances) == len(endpoints_to_test):
    unique_balances = set(balances.values())
    if len(unique_balances) == 1:
        balance = list(unique_balances)[0]
        print(f"   ✅ ALL SYNCHRONIZED: ${balance:,.2f}")
        print(f"   🎉 SUCCESS: Virtual balances are now consistent!")
    else:
        print(f"   ❌ MISMATCH DETECTED:")
        for name, balance in balances.items():
            print(f"      {name}: ${balance:,.2f}")
else:
    print(f"   ❌ Some endpoints failed to return balances")

print(f"\n💡 Expected Dashboard Behavior:")
print(f"   • Sidebar Virtual Balance: Should show ${balances.get('Virtual Balance', 'UNKNOWN'):,.2f}")
print(f"   • Auto Trading Balance: Should show ${balances.get('Auto Trading Status', 'UNKNOWN'):,.2f}")
print(f"   • Both should update automatically every few seconds")
print(f"   • Reset button should work for both")

print(f"\n" + "=" * 50)
if len(set(balances.values())) == 1 and len(balances) == 2:
    print("🏆 ISSUE RESOLVED: Virtual balances are now synchronized!")
else:
    print("⚠️  Issue may still exist - check specific endpoints above")
