#!/usr/bin/env python3
"""
Simple dashboard test - just try to start the dashboard directly
"""
import os
import sys

# Set UTF-8 for Windows
if os.name == 'nt':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

def main():
    print("🚀 Testing Dashboard Startup...")
    
    # Change to dashboard directory
    dashboard_path = os.path.join(os.getcwd(), "dashboard")
    if not os.path.exists(dashboard_path):
        print("❌ Dashboard directory not found!")
        return
    
    os.chdir(dashboard_path)
    print(f"📁 Changed to: {os.getcwd()}")
    
    # Try to import required modules
    try:
        print("📦 Testing imports...")
        import dash
        print("✅ Dash imported successfully")
        
        import dash_bootstrap_components as dbc
        print("✅ Dash Bootstrap Components imported")
        
        # Add current directory to path for imports
        dashboard_path = os.path.dirname(os.path.abspath(__file__))
        if dashboard_path not in sys.path:
            sys.path.insert(0, dashboard_path)
        
        try:
            from layout import layout
            print("✅ Layout imported successfully")
        except ImportError as e:
            print(f"❌ Could not import layout: {e}")
            return
        
        print("🎯 Creating Dash app...")
        app = dash.Dash(
            __name__,
            suppress_callback_exceptions=True,
            external_stylesheets=[
                dbc.themes.BOOTSTRAP,
                "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css"
            ]
        )
        
        app.layout = layout
        print("✅ Layout set successfully")
        
        print("⚡ Loading callbacks...")
        try:
            import callbacks
            print("✅ Callbacks loaded successfully")
        except ImportError as e:
            print(f"❌ Could not import callbacks: {e}")
            return
        
        print("🌐 Starting server on http://localhost:8050...")
        print("🎉 Dashboard should be working! Press Ctrl+C to stop")
        
        app.run(debug=True, port=8050, host="127.0.0.1")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
