#!/usr/bin/env python3
"""
Start the dashboard app with better error handling
"""
import sys
import traceback
import dash
import dash_bootstrap_components as dbc
from dash_app import app
from layout import layout
# import callbacks  # [DISABLED: Use only refactored_callbacks_step1 in start_dashboard.py]

print("Setting up app...")
print(f"Python version: {sys.version}")
print(f"Dash version: {dash.__version__}")

app.layout = layout
print("Layout set successfully!")

if __name__ == "__main__":
    print(f"Starting dashboard on port 8050...")
    print(f"Callbacks registered: {len(app.callback_map)}")
    print("Available at: http://127.0.0.1:8050 or http://localhost:8050")
    
    try:
        print("Calling app.run()...")
        app.run(debug=True, port=8050, host="127.0.0.1")
    except Exception as e:
        print(f"Error starting server: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")
