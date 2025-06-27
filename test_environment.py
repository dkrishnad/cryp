#!/usr/bin/env python3
"""
Quick test to verify Python and dependencies
"""
import sys
import os

print("🔧 Python Environment Test")
print("=" * 40)
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current directory: {os.getcwd()}")
print(f"Platform: {sys.platform}")

# Test key imports
try:
    import dash
    print("✅ Dash installed")
except ImportError as e:
    print(f"❌ Dash not found: {e}")

try:
    import dash_bootstrap_components
    print("✅ Dash Bootstrap Components installed")
except ImportError as e:
    print(f"❌ Dash Bootstrap Components not found: {e}")

try:
    import requests
    print("✅ Requests installed")
except ImportError as e:
    print(f"❌ Requests not found: {e}")

try:
    import uvicorn
    print("✅ Uvicorn installed")
except ImportError as e:
    print(f"❌ Uvicorn not found: {e}")

# Check if directories exist
backend_exists = os.path.exists("backend")
dashboard_exists = os.path.exists("dashboard")

print(f"Backend directory exists: {'✅' if backend_exists else '❌'}")
print(f"Dashboard directory exists: {'✅' if dashboard_exists else '❌'}")

if dashboard_exists:
    start_beautiful_exists = os.path.exists("dashboard/start_beautiful.py")
    print(f"start_beautiful.py exists: {'✅' if start_beautiful_exists else '❌'}")

print("\n🚀 Test complete!")
input("Press Enter to continue...")
