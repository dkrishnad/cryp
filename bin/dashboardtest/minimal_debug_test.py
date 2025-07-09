#!/usr/bin/env python3
"""
Minimal debug test to isolate dashboard startup issues
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=== MINIMAL DEBUG TEST ===")

# Test 1: Import dash_app
print("1. Testing dash_app import...")
try:
    from dash_app import app
    print("✅ dash_app imported successfully")
except Exception as e:
    print(f"❌ dash_app import failed: {e}")
    sys.exit(1)

# Test 2: Import layout
print("2. Testing layout import...")
try:
    from layout import layout
    print("✅ layout imported successfully")
except Exception as e:
    print(f"❌ layout import failed: {e}")
    sys.exit(1)

# Test 3: Import callbacks
print("3. Testing callbacks import...")
try:
    import callbacks
    print("✅ callbacks imported successfully")
except Exception as e:
    print(f"❌ callbacks import failed: {e}")
    print("Warning: Continuing without callbacks...")

# Test 4: Set layout
print("4. Testing layout assignment...")
try:
    app.layout = layout
    print("✅ layout assigned successfully")
except Exception as e:
    print(f"❌ layout assignment failed: {e}")
    sys.exit(1)

# Test 5: Test server start
print("5. Testing server start...")
try:
    print("Starting server on http://localhost:8051")
    app.run(
        debug=True,
        host='localhost',
        port=8051,
        dev_tools_ui=False,
        dev_tools_props_check=False
    )
except Exception as e:
    print(f"❌ Server start failed: {e}")
    sys.exit(1)
