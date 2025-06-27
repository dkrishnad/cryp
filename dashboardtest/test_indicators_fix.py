#!/usr/bin/env python3
"""
Test the fixed technical indicators issue
"""
from dash_app import app
from layout import layout
import callbacks

# Set layout
app.layout = layout

print(f"Dashboard ready with {len(app.callback_map)} callbacks registered")
print("\nTesting Instructions:")
print("1. Open http://localhost:8050 in your browser")
print("2. Change the symbol dropdown from 'BTCUSDT' to 'KAIAUSDT' or 'ETHUSDT'")
print("3. Watch the console for debug messages:")
print("   - '[DASH DEBUG] sync_selected_symbol' - symbol dropdown change")
print("   - '[DASH DEBUG] update_technical_indicators' - indicators update")
print("4. Verify the indicators change:")
print("   - BTCUSDT should show: Regime=Sideways, RSI=55.1")
print("   - KAIAUSDT should show: Regime=Bullish, RSI=65.2") 
print("   - Others should show: Regime=Neutral, RSI=50.0")

if __name__ == "__main__":
    app.run(debug=True, port=8050, host="0.0.0.0")
