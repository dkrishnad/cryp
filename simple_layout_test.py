#!/usr/bin/env python3
"""
Simple test to check layout import
"""
import sys
import os

# Add the dashboard directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboardtest'))

print("Testing basic imports...")

try:
    import dash
    from dash import html, dcc
    import dash_bootstrap_components as dbc
    print("✅ Dash imports successful")
except Exception as e:
    print(f"❌ Dash import failed: {e}")
    exit(1)

try:
    # Test individual layout components
    print("Testing layout components...")
    
    # First, test the layout file can be imported at all
    import layout
    print("✅ Layout module imported successfully")
    
    # Check if the layout variable exists
    if hasattr(layout, 'layout'):
        print("✅ Layout variable exists")
        layout_obj = layout.layout
        print(f"Layout type: {type(layout_obj)}")
        print(f"Is dict: {isinstance(layout_obj, dict)}")
        
        # Try to serialize it to see what it contains
        if isinstance(layout_obj, dict):
            print("❌ FOUND THE PROBLEM: Layout is a dictionary!")
            print(f"Dict keys: {list(layout_obj.keys())}")
        
    else:
        print("❌ Layout variable not found in module")
        
except Exception as e:
    print(f"❌ Layout import failed: {e}")
    import traceback
    traceback.print_exc()
