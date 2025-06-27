#!/usr/bin/env python3
"""
Dashboard test script - diagnose issues
"""
import sys
import os

# Force UTF-8 encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'

def safe_print(msg):
    """Print safely without encoding errors"""
    try:
        print(msg)
        sys.stdout.flush()
    except Exception as e:
        print(f"Print error: {e}")

def main():
    try:
        safe_print("=== Dashboard Diagnostic Test ===")
        safe_print(f"Python version: {sys.version}")
        safe_print(f"Working directory: {os.getcwd()}")
        
        safe_print("Testing imports...")
        
        # Test basic imports
        import dash
        safe_print(f"Dash version: {dash.__version__}")
        
        import dash_bootstrap_components as dbc
        safe_print("dash_bootstrap_components OK")
        
        # Test layout import
        safe_print("Importing layout...")
        from layout import layout
        safe_print("Layout imported successfully!")
        
        # Test app creation
        safe_print("Creating app...")
        app = dash.Dash(
            __name__,
            suppress_callback_exceptions=True,
            external_stylesheets=[dbc.themes.BOOTSTRAP]
        )
        
        app.layout = layout
        safe_print("App created successfully!")
        
        # Test server start
        safe_print("Starting server...")
        app.run(debug=True, port=8051, host="127.0.0.1")
        
    except Exception as e:
        safe_print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    main()
