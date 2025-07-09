#!/usr/bin/env python3
"""
Simple skeleton diagnosis
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=== SIMPLE SKELETON DIAGNOSIS ===")

# Test 1: Basic imports
print("1. Testing basic imports...")
try:
    import dash
    from dash import html, dcc
    import dash_bootstrap_components as dbc
    print("✅ Basic Dash imports work")
except Exception as e:
    print(f"❌ Basic imports failed: {e}")
    exit(1)

# Test 2: App creation
print("2. Testing app creation...")
try:
    from dash_app import app
    print("✅ App imported successfully")
    print(f"App type: {type(app)}")
except Exception as e:
    print(f"❌ App import failed: {e}")
    exit(1)

# Test 3: Simple layout test
print("3. Testing simple layout...")
try:
    simple_layout = html.Div([
        html.H1("Test Dashboard"),
        html.P("This is a test"),
        dbc.Alert("Test alert", color="success")
    ])
    app.layout = simple_layout
    print("✅ Simple layout works")
except Exception as e:
    print(f"❌ Simple layout failed: {e}")
    exit(1)

# Test 4: Try to start server
print("4. Testing server start...")
try:
    print("Starting test server on port 8052...")
    app.run(
        debug=True,
        host='localhost',
        port=8052
    )
except Exception as e:
    print(f"❌ Server start failed: {e}")
    exit(1)
