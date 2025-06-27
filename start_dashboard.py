#!/usr/bin/env python3
"""
Launch script for the crypto bot dashboard
"""

import sys
import os

# Add dashboard directory to Python path
dashboard_dir = os.path.join(os.path.dirname(__file__), 'dashboard')
sys.path.insert(0, dashboard_dir)

try:
    print("🚀 Starting Crypto Bot Dashboard...")
    
    # Import the fully configured app
    from dashboard.app import app
    
    print("✅ Dashboard app loaded successfully!")
    print("✅ Layout and callbacks registered!")
    print("📍 Dashboard URL: http://localhost:8050")
    print("🔥 Starting dashboard server...")
    
    # The app is already configured in app.py, just run it
    app.run(host="0.0.0.0", port=8050, debug=False)
    
except Exception as e:
    print(f"❌ Error starting dashboard: {e}")
    print("📝 Check the dashboard files for issues")
    print("🔧 Trying alternative startup method...")
    
    # Fallback method
    try:
        from dashboard.dash_app import app
        from dashboard.layout import layout
        from dashboard import callbacks
        
        app.layout = layout
        print("✅ Fallback method loaded successfully!")
        app.run(host="0.0.0.0", port=8050, debug=False)
        
    except Exception as e2:
        print(f"❌ Fallback method also failed: {e2}")
        sys.exit(1)
