#!/usr/bin/env python3
"""
Dashboard app with fixed imports for direct execution
"""

import sys
import os

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

import dash
import dash_bootstrap_components as dbc
import requests

# Import layout and app components
from layout import layout
from dash_app import app, server

def check_backend_health():
    try:
        r = requests.get("http://localhost:8001/health", timeout=2)
        if r.status_code == 200:
            print("✅ Backend is healthy and running")
            return True
        else:
            print(f"❌ Backend health check failed. Status: {r.status_code}")
            return False
    except Exception as e:
        print(f"❌ Could not connect to backend API: {e}")
        return False

# Check backend before starting
if not check_backend_health():
    print("⚠️  Warning: Backend not accessible, some features may not work")

# Import and register callbacks
try:
    import callbacks  # This will register all main callbacks
    print("✅ Main callbacks registered")
except Exception as e:
    print(f"❌ Error registering main callbacks: {e}")

# Import and register Binance-exact callbacks
try:
    from binance_exact_callbacks import register_binance_exact_callbacks
    register_binance_exact_callbacks(app)
    print("✅ Binance-exact callbacks registered")
except Exception as e:
    print(f"❌ Error registering Binance-exact callbacks: {e}")

# Set the layout
app.layout = layout

if __name__ == "__main__":
    print("🚀 Starting Crypto Trading Bot Dashboard...")
    print("📍 Dashboard URL: http://localhost:8050")
    print("🔗 New Binance-Exact API tab available!")
    print("=" * 60)
    
    try:
        app.run(debug=False, port=8050, host='127.0.0.1')
    except Exception as e:
        print(f"❌ Failed to start dashboard: {e}")
