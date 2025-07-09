#!/usr/bin/env python3
"""
Debug script to test auto trading toggle and virtual balance issues
"""

import requests
import json

API_URL = "http://localhost:8001"

def test_backend_health():
    """Test if backend is responding"""
    print("=== TESTING BACKEND HEALTH ===")
    try:
        resp = requests.get(f"{API_URL}/health", timeout=5)
        print(f"Backend health: {resp.status_code}")
        if resp.status_code == 200:
            print(f"Response: {resp.json()}")
            return True
        return False
    except Exception as e:
        print(f"Backend error: {e}")
        return False

def test_auto_trading_toggle():
    """Test auto trading toggle functionality"""
    print("\n=== TESTING AUTO TRADING TOGGLE ===")
    
    # Test enabling
    print("1. Enabling auto trading...")
    try:
        payload = {"enabled": True}
        resp = requests.post(f"{API_URL}/auto_trading/toggle", json=payload, timeout=5)
        print(f"Toggle ON - Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Error response: {resp.text}")
    except Exception as e:
        print(f"Toggle ON error: {e}")
    
    # Check status after enabling
    print("\n2. Checking status after enabling...")
    try:
        resp = requests.get(f"{API_URL}/auto_trading/status", timeout=5)
        print(f"Status check - Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"Status response: {json.dumps(data, indent=2)}")
            if data.get("status") == "success":
                auto_trading = data.get("auto_trading", {})
                enabled = auto_trading.get("enabled", False)
                print(f"Auto trading enabled: {enabled}")
        else:
            print(f"Status error: {resp.text}")
    except Exception as e:
        print(f"Status check error: {e}")
    
    # Test disabling
    print("\n3. Disabling auto trading...")
    try:
        payload = {"enabled": False}
        resp = requests.post(f"{API_URL}/auto_trading/toggle", json=payload, timeout=5)
        print(f"Toggle OFF - Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"Response: {json.dumps(data, indent=2)}")
    except Exception as e:
        print(f"Toggle OFF error: {e}")

def test_virtual_balance():
    """Test virtual balance endpoint"""
    print("\n=== TESTING VIRTUAL BALANCE ===")
    
    try:
        resp = requests.get(f"{API_URL}/virtual_balance", timeout=5)
        print(f"Virtual balance - Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"Virtual balance response: {json.dumps(data, indent=2)}")
            if data.get("status") == "success":
                balance = data.get("balance", 0)
                pnl = data.get("current_pnl", 0)
                total = data.get("total_value", 0)
                print(f"Balance: ${balance:,.2f}")
                print(f"Current P&L: ${pnl:,.2f}")
                print(f"Total Value: ${total:,.2f}")
        else:
            print(f"Virtual balance error: {resp.text}")
    except Exception as e:
        print(f"Virtual balance error: {e}")

def test_dashboard_connection():
    """Test dashboard connection"""
    print("\n=== TESTING DASHBOARD CONNECTION ===")
    
    try:
        resp = requests.get("http://localhost:8050", timeout=5)
        print(f"Dashboard - Status: {resp.status_code}")
        if resp.status_code == 200:
            print("✓ Dashboard is accessible")
            return True
        else:
            print(f"✗ Dashboard error: {resp.status_code}")
            return False
    except Exception as e:
        print(f"✗ Dashboard connection error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 DEBUGGING AUTO TRADING & VIRTUAL BALANCE ISSUES")
    print("=" * 60)
    
    # Test all components
    backend_ok = test_backend_health()
    if backend_ok:
        test_auto_trading_toggle()
        test_virtual_balance()
    
    dashboard_ok = test_dashboard_connection()
    
    print("\n" + "=" * 60)
    print("📋 DIAGNOSIS SUMMARY")
    print("=" * 60)
    print(f"Backend Health: {'✓ OK' if backend_ok else '✗ FAILED'}")
    print(f"Dashboard Access: {'✓ OK' if dashboard_ok else '✗ FAILED'}")
    
    if backend_ok and dashboard_ok:
        print("\n✅ Both backend and dashboard are running")
        print("If toggle/balance still not working, it's a frontend issue")
    elif backend_ok and not dashboard_ok:
        print("\n⚠️ Backend OK, but dashboard not accessible")
        print("Start dashboard with: python dashboard/app.py")
    elif not backend_ok:
        print("\n❌ Backend not responding")
        print("Start backend with: python backend/main.py")
    else:
        print("\n❌ Both services need to be started")
