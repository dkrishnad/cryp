#!/usr/bin/env python3
"""
Test symbol selection and indicators update issue
"""
from dash_app import app
from layout import layout
import callbacks

# Set layout
app.layout = layout

# Add a debug callback to monitor symbol changes
from dash import Input, Output, callback

@app.callback(
    Output("test-output", "children", allow_duplicate=True),
    [Input("sidebar-symbol", "value"), Input("selected-symbol-store", "data")],
    prevent_initial_call=True
)
def debug_symbol_changes(sidebar_value, store_data):
    from dash import callback_context
    ctx = callback_context
    
    debug_msg = f"[SYMBOL DEBUG] Sidebar: {sidebar_value}, Store: {store_data}, Triggered: {ctx.triggered}"
    print(debug_msg)
    return debug_msg

if __name__ == "__main__":
    print("Starting dashboard with symbol change debugging...")
    print("Watch for '[SYMBOL DEBUG]' messages when you change symbols")
    print("Also watch for '[DASH DEBUG] update_technical_indicators' messages")
    app.run(debug=True, port=8050, host="0.0.0.0")
