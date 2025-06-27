#!/usr/bin/env python3
"""
Test app startup after syntax fix
"""
try:
    print("Testing app import...")
    from dash_app import app
    print("✓ App imported successfully")
    
    print("Testing layout import...")
    from layout import layout
    print("✓ Layout imported successfully")
    
    print("Testing callbacks import...")
    import callbacks
    print("✓ Callbacks imported successfully")
    
    print("Setting layout...")
    app.layout = layout
    print("✓ Layout set successfully")
    
    print(f"✓ App ready with {len(app.callback_map)} callbacks registered")
    print("\nApp is ready to start!")
    print("Run: python app.py")
    print("Then open: http://localhost:8050")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
