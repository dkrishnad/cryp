#!/usr/bin/env python3
"""
Test if the layout is a dictionary instead of a Dash component
"""
import sys
import os

# Add the dashboard directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboardtest'))

try:
    print("🔍 Testing layout structure...")
    
    # Import the layout
    from layout import layout
    
    print(f"Layout type: {type(layout)}")
    print(f"Layout is dict: {isinstance(layout, dict)}")
    
    # Check if it's a Dash component
    try:
        from dash import html
        print(f"Layout is Dash component: {hasattr(layout, '_namespace')}")
        
        if hasattr(layout, '_namespace'):
            print(f"Layout namespace: {layout._namespace}")
            print(f"Layout component name: {layout._component_name}")
        
        # If it's a dict, let's see what keys it has
        if isinstance(layout, dict):
            print(f"Dict keys: {list(layout.keys())}")
            print("🔍 This is the problem! Layout is a dict instead of a Dash component")
            
        # Test if we can create a simple layout
        test_layout = html.Div([html.H1("Test")])
        print(f"Test layout type: {type(test_layout)}")
        print(f"Test layout is dict: {isinstance(test_layout, dict)}")
        
    except Exception as e:
        print(f"Error checking Dash properties: {e}")
        import traceback
        traceback.print_exc()
        
except Exception as e:
    print(f"❌ Error importing layout: {e}")
    import traceback
    traceback.print_exc()
