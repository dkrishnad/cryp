#!/usr/bin/env python3
"""
Quick test to see if callbacks load properly
"""
import sys
import traceback

try:
    print("Creating Dash app...")
    import dash
    import dash_bootstrap_components as dbc
    from dash_app import app
    
    print("Importing layout...")
    from layout import layout
    
    print("Importing callbacks...")
    import callbacks
    
    print("Setting layout...")
    app.layout = layout
    
    print("SUCCESS: Everything loaded without errors")
    print(f"App has {len(app.callback_map)} callbacks registered")
    
    # List callback outputs for debugging
    for callback_id, callback_ctx in app.callback_map.items():
        print(f"Callback: {callback_id}")
        if hasattr(callback_ctx, 'outputs'):
            outputs = [str(output) for output in callback_ctx.outputs]
            print(f"  Outputs: {outputs}")
    
except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)
