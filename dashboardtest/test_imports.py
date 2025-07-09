#!/usr/bin/env python3
"""
Simple test script to identify which import is causing the dashboard startup issue
"""

import sys
import os

# Add dashboard directory to path
dashboard_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, dashboard_dir)

def test_import(module_name, description):
    """Test importing a module and report the result"""
    try:
        print(f"Testing {description}...")
        if module_name == "dash_app":
            from dash_app import app
            print(f"✅ {description} imported successfully")
            return True
        elif module_name == "callbacks":
            import callbacks
            print(f"✅ {description} imported successfully")
            return True
        elif module_name == "layout":
            from layout import layout
            print(f"✅ {description} imported successfully")
            return True
        else:
            exec(f"import {module_name}")
            print(f"✅ {description} imported successfully")
            return True
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Dashboard Import Test")
    print("=" * 50)
    
    # Test basic dependencies first
    test_import("dash", "Dash")
    test_import("dash_bootstrap_components", "Dash Bootstrap Components")
    test_import("plotly", "Plotly")
    
    print("\nTesting dashboard modules:")
    print("-" * 30)
    
    # Test dashboard modules
    test_import("dash_app", "Dash App")
    test_import("layout", "Layout")
    test_import("callbacks", "Callbacks")
    
    print("\nImport test complete!")
