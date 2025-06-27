#!/usr/bin/env python3
"""
Debug dashboard startup to identify crash cause
"""
import sys
import traceback
import os

print("=== DASHBOARD STARTUP DEBUG ===")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

try:
    print("1. Importing dash...")
    import dash
    print("✓ Dash imported successfully")
    
    print("2. Importing dash_bootstrap_components...")
    import dash_bootstrap_components as dbc
    print("✓ DBC imported successfully")
    
    print("3. Importing dash_app...")
    from dash_app import app
    print("✓ Dash app imported successfully")
    
    print("4. Importing layout...")
    from layout import layout
    print("✓ Layout imported successfully")
    
    print("5. Importing callbacks...")
    import callbacks
    print("✓ Callbacks imported successfully")
    
    print("6. Setting up app layout...")
    app.layout = layout
    print("✓ App layout set successfully")
    
    print("7. Starting server...")
    print(f"Callbacks registered: {len(app.callback_map)}")
    
    # Start with simpler configuration first
    app.run(debug=False, port=8050, host="127.0.0.1", dev_tools_hot_reload=False)
    
except Exception as e:
    print(f"❌ Error occurred: {e}")
    print("Full traceback:")
    traceback.print_exc()
    
print("=== DASHBOARD STARTUP DEBUG END ===")
