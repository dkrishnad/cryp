#!/usr/bin/env python3
"""
Simple dashboard launcher with enhanced error reporting
"""
import sys
import os
import traceback

# Add paths
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboardtest'))

def safe_print(msg):
    """Safe printing function"""
    try:
        print(msg)
        sys.stdout.flush()
    except UnicodeEncodeError:
        print(msg.encode('ascii', 'replace').decode('ascii'))
        sys.stdout.flush()

def main():
    """Main function with enhanced error reporting"""
    safe_print("🚀 Starting Enhanced Dashboard...")
    safe_print("=" * 50)
    
    try:
        safe_print("🔧 Importing Dash app...")
        from dashboardtest.dash_app import app
        safe_print("✅ Dash app imported successfully")
        
        safe_print("🔧 Importing layout...")
        from dashboardtest.layout import layout
        safe_print("✅ Layout imported successfully")
        
        safe_print("🔧 Importing callbacks...")
        import dashboardtest.callbacks
        safe_print("✅ Callbacks imported successfully")
        
        safe_print("🔧 Setting up app layout...")
        app.layout = layout
        safe_print("✅ App layout configured")
        
        safe_print("📊 Dashboard ready to start on http://localhost:8050")
        safe_print("🔧 Starting server...")
        
        # Start the app with enhanced error handling
        app.run(
            debug=True,  # Enable debug mode for better error messages
            host='localhost',
            port=8050,
            dev_tools_ui=True,
            dev_tools_props_check=True,
            use_reloader=False
        )
        
    except ImportError as e:
        safe_print(f"❌ Import error: {e}")
        safe_print("Check if all required modules are installed")
        traceback.print_exc()
        sys.exit(1)
        
    except Exception as e:
        safe_print(f"❌ Unexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
