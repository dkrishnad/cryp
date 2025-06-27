#!/usr/bin/env python3
"""
Test to verify indicators components are working
"""
from dash_app import app
from layout import layout
from dash import Input, Output, callback

# Set layout
app.layout = layout

# Simple test callback to update indicators with static data
@app.callback(
    [Output('current-regime', 'children'),
     Output('rsi-value', 'children'),
     Output('macd-value', 'children'),
     Output('bbands-value', 'children')],
    Input('interval-indicators', 'n_intervals'),
    prevent_initial_call=False
)
def test_indicators_simple(n_intervals):
    print(f"[TEST] Simple indicators test triggered: {n_intervals}")
    return "TEST REGIME", "TEST RSI", "TEST MACD", "TEST BBANDS"

if __name__ == "__main__":
    print("Starting test dashboard to verify indicator components...")
    print("If you see 'TEST REGIME', 'TEST RSI', etc. in the indicators section, components are working")
    app.run(debug=True, port=8051, host="0.0.0.0")
