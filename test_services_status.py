#!/usr/bin/env python3
"""
Test script to verify backend and dashboard services are running and responsive.
"""

import requests
import time

def test_backend():
    """Test backend API endpoints."""
    print("=== TESTING BACKEND API ===")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8001/health", timeout=5)
        print(f"✓ Backend health: {response.status_code} - {response.json()}")
        
        # Test auto trading status
        response = requests.get("http://localhost:8001/auto_trading/status", timeout=5)
        print(f"✓ Auto trading status: {response.status_code} - {response.json()}")
        
        # Test current signal
        response = requests.get("http://localhost:8001/auto_trading/current_signal", timeout=5)
        print(f"✓ Current signal: {response.status_code} - {response.json()}")
        
        # Test virtual balance
        response = requests.get("http://localhost:8001/virtual_balance", timeout=5)
        print(f"✓ Virtual balance: {response.status_code} - {response.json()}")
        
        return True
        
    except Exception as e:
        print(f"✗ Backend error: {e}")
        return False

def test_dashboard():
    """Test dashboard accessibility."""
    print("\n=== TESTING DASHBOARD ===")
    
    try:
        response = requests.get("http://localhost:8050", timeout=10)
        if response.status_code == 200:
            print(f"✓ Dashboard accessible: {response.status_code}")
            return True
        else:
            print(f"✗ Dashboard error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Dashboard error: {e}")
        return False

if __name__ == "__main__":
    print("Testing crypto bot services...")
    
    backend_ok = test_backend()
    dashboard_ok = test_dashboard()
    
    print(f"\n=== FINAL STATUS ===")
    print(f"Backend: {'✓ RUNNING' if backend_ok else '✗ NOT RUNNING'}")
    print(f"Dashboard: {'✓ RUNNING' if dashboard_ok else '✗ NOT RUNNING'}")
    
    if backend_ok and dashboard_ok:
        print("\n🎉 ALL SERVICES ARE RUNNING AND RESPONSIVE!")
        print("You can now:")
        print("- Access dashboard at: http://localhost:8050")
        print("- Backend API at: http://localhost:8001")
        print("- Test auto trading features in the dashboard")
    else:
        print("\n⚠️ Some services are not running properly.")
        print("Please start the missing services:")
        if not backend_ok:
            print("- Start backend: python backend/main.py")
        if not dashboard_ok:
            print("- Start dashboard: python dashboard/app.py")
