#!/usr/bin/env python3
"""
Final test - start the dashboard with full debugging
"""
import sys
import traceback
from dash_app import app
from layout import layout

# Import callbacks
print("Importing callbacks...")
import callbacks

# Set layout
print("Setting layout...")
app.layout = layout

print(f"App ready with {len(app.callback_map)} callbacks registered")

# Add a simple debug callback to verify functionality
from dash import Input, Output, callback

@app.callback(
    Output("test-output", "children", allow_duplicate=True),
    Input("interval-indicators", "n_intervals"),
    prevent_initial_call=True
)
def debug_callback(n_intervals):
    debug_msg = f"[DEBUG] Interval callback working! Count: {n_intervals}"
    print(debug_msg)
    return debug_msg

if __name__ == "__main__":
    print("Starting dashboard on http://localhost:8050...")
    try:
        app.run(debug=True, port=8050, host="0.0.0.0")
    except Exception as e:
        print(f"Error starting server: {e}")
        traceback.print_exc()
