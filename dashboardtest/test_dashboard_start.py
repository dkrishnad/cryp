#!/usr/bin/env python3
"""
Test dashboard dependencies and imports
"""
import sys
import traceback

def test_imports():
    """Test all required imports"""
    try:
        print("Testing basic imports...")
        import dash
        print(f"✓ Dash version: {dash.__version__}")
        
        import dash_bootstrap_components as dbc
        print(f"✓ Dash Bootstrap Components imported")
        
        import plotly
        print(f"✓ Plotly version: {plotly.__version__}")
        
        print("Testing app imports...")
        from dash_app import app
        print(f"✓ App imported successfully")
        
        from layout import layout
        print(f"✓ Layout imported successfully")
        
        import callbacks
        print(f"✓ Callbacks imported successfully")
        
        app.layout = layout
        print(f"✓ Layout set successfully")
        print(f"✓ Callbacks registered: {len(app.callback_map)}")
        
        print("\n🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        traceback.print_exc()
        return False

def test_minimal_run():
    """Test minimal dashboard run"""
    try:
        from dash_app import app
        from layout import layout
        import callbacks
        
        app.layout = layout
        
        print(f"Attempting to start on 127.0.0.1:8050...")
        app.run(debug=False, port=8050, host="127.0.0.1", dev_tools_hot_reload=False)
        
    except Exception as e:
        print(f"❌ Run error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 50)
    print("🔧 DASHBOARD DEPENDENCY TEST")
    print("=" * 50)
    
    if test_imports():
        print("\n" + "=" * 50)
        print("🚀 STARTING MINIMAL DASHBOARD")
        print("=" * 50)
        test_minimal_run()
    else:
        print("❌ Cannot start dashboard due to import errors")
