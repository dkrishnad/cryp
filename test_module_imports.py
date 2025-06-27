#!/usr/bin/env python3
"""
Simple service startup test script.
"""

import subprocess
import sys
import time
import requests

def test_backend_startup():
    print("Testing if backend can start...")
    try:
        # Just test if we can import the backend module
        sys.path.append('.')
        from backend.main import app
        print("✓ Backend module imports successfully")
        return True
    except Exception as e:
        print(f"✗ Backend import error: {e}")
        return False

def test_dashboard_startup():
    print("Testing if dashboard can start...")
    try:
        # Test if we can import the dashboard module
        sys.path.append('.')
        from dashboard.app import app
        print("✓ Dashboard module imports successfully")
        return True
    except Exception as e:
        print(f"✗ Dashboard import error: {e}")
        return False

def test_requests():
    """Test that requests works for later service testing."""
    try:
        import requests
        print("✓ Requests module available")
        return True
    except Exception as e:
        print(f"✗ Requests error: {e}")
        return False

if __name__ == "__main__":
    print("=== CRYPTO BOT SERVICE STARTUP TEST ===\n")
    
    # Test imports
    backend_ok = test_backend_startup()
    dashboard_ok = test_dashboard_startup()
    requests_ok = test_requests()
    
    print(f"\n=== RESULTS ===")
    print(f"Backend import: {'✓' if backend_ok else '✗'}")
    print(f"Dashboard import: {'✓' if dashboard_ok else '✗'}")
    print(f"Requests available: {'✓' if requests_ok else '✗'}")
    
    if backend_ok and dashboard_ok and requests_ok:
        print("\n🎉 ALL MODULES IMPORT SUCCESSFULLY!")
        print("\nNext steps:")
        print("1. Start backend: python backend/main.py")
        print("2. Start dashboard: python dashboard/app.py")
        print("3. Access dashboard at: http://localhost:8050")
    else:
        print("\n⚠️ Some modules have import issues. Please fix them first.")
