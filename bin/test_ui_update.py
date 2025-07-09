"""
Test UI Update by Forcing Different Values
"""

import requests
import json

# Force a change to the virtual balance to see if UI updates
balance_data = {
    "balance": 12345.67,
    "current_pnl": 245.33,
    "total_value": 12345.67 + 245.33
}

with open("data/virtual_balance.json", "w") as f:
    json.dump(balance_data, f)

print("✅ Updated virtual balance to $12,345.67 with P&L of $245.33")
print("Check the dashboard - if the Virtual Balance section still shows empty,")
print("then there's a UI component rendering issue.")
print("If it updates to show the new values, then the callback is working correctly.")
