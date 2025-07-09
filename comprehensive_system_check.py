#!/usr/bin/env python3
"""
Comprehensive System Check - Port Configuration and Dashboard Visibility
This script checks all critical components for proper port configuration
"""

import requests
import time
import json
from datetime import datetime

def test_backend_connectivity():
    """Test backend on port 5000"""
    print("🔍 Testing Backend Connectivity (Port 5000)")
    print("=" * 50)
    
    try:
        # Test basic health
        health_resp = requests.get("http://localhost:5000/health", timeout=5)
        print(f"✅ Health Check: {health_resp.status_code}")
        
        # Test key endpoints
        endpoints = [
            "/portfolio",
            "/trades", 
            "/futures/analytics",
            "/model/analytics"
        ]
        
        working = 0
        for endpoint in endpoints:
            try:
                resp = requests.get(f"http://localhost:5000{endpoint}", timeout=3)
                if resp.status_code == 200:
                    print(f"✅ {endpoint}: {resp.status_code}")
                    working += 1
                else:
                    print(f"❌ {endpoint}: {resp.status_code}")
            except Exception as e:
                print(f"❌ {endpoint}: Connection Error")
        
        print(f"\n📊 Backend Status: {working}/{len(endpoints)+1} endpoints working")
        return working >= len(endpoints)
        
    except Exception as e:
        print(f"❌ Backend Connection Failed: {e}")
        return False

def test_dashboard_accessibility():
    """Test if dashboard is accessible on port 8050"""
    print("\n🌐 Testing Dashboard Accessibility (Port 8050)")
    print("=" * 50)
    
    try:
        # Test if dashboard is running
        resp = requests.get("http://localhost:8050", timeout=5)
        print(f"✅ Dashboard Accessible: {resp.status_code}")
        
        # Check if it's actually loading content
        if "Crypto" in resp.text or "Dashboard" in resp.text:
            print("✅ Dashboard Content: Crypto dashboard detected")
            return True
        else:
            print("⚠️ Dashboard Content: Generic page (may still be loading)")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Dashboard Not Running: Port 8050 not accessible")
        print("💡 Start dashboard with: python app.py (in dashboardtest folder)")
        return False
    except Exception as e:
        print(f"❌ Dashboard Error: {e}")
        return False

def test_port_configuration():
    """Test all files are using correct ports"""
    print("\n🔧 Testing Port Configuration")
    print("=" * 50)
    
    # Check key files for correct API URLs
    files_to_check = [
        ("dashboardtest/callbacks.py", "http://localhost:5000"),
        ("dashboardtest/futures_callbacks.py", "http://localhost:5000"),
        ("dashboardtest/dashboard_utils.py", "http://localhost:5000"),
        ("dashboardtest/app.py", "port=8050")
    ]
    
    correct_config = 0
    for file_path, expected in files_to_check:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if expected in content:
                    print(f"✅ {file_path}: Correct port configuration")
                    correct_config += 1
                else:
                    print(f"❌ {file_path}: Incorrect port configuration")
        except FileNotFoundError:
            print(f"⚠️ {file_path}: File not found")
        except Exception as e:
            print(f"❌ {file_path}: Error reading file")
    
    print(f"\n📊 Port Config: {correct_config}/{len(files_to_check)} files correct")
    return correct_config == len(files_to_check)

def test_integration():
    """Test backend-frontend integration"""
    print("\n🔗 Testing Backend-Frontend Integration")
    print("=" * 50)
    
    try:
        # Test a typical frontend-to-backend call
        resp = requests.get("http://localhost:5000/futures/analytics", timeout=5)
        if resp.status_code == 200:
            print("✅ Integration Test: Frontend can call backend successfully")
            data = resp.json()
            if "status" in data and data["status"] == "success":
                print("✅ Data Format: Backend returns expected format")
                return True
            else:
                print("⚠️ Data Format: Unexpected response format")
                return False
        else:
            print(f"❌ Integration Test: Backend call failed ({resp.status_code})")
            return False
    except Exception as e:
        print(f"❌ Integration Test: {e}")
        return False

def main():
    """Run comprehensive system check"""
    print("🚀 COMPREHENSIVE SYSTEM CHECK")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)
    
    # Run all tests
    backend_ok = test_backend_connectivity()
    dashboard_ok = test_dashboard_accessibility()
    config_ok = test_port_configuration()
    integration_ok = test_integration()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 SYSTEM STATUS SUMMARY")
    print("=" * 60)
    
    tests = [
        ("Backend (Port 5000)", backend_ok),
        ("Dashboard (Port 8050)", dashboard_ok),
        ("Port Configuration", config_ok),
        ("Backend Integration", integration_ok)
    ]
    
    passed = sum(1 for _, status in tests if status)
    
    for test_name, status in tests:
        icon = "✅" if status else "❌"
        print(f"{icon} {test_name}")
    
    print(f"\n📊 Overall Status: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n🎉 SYSTEM READY!")
        print("✅ Backend running on port 5000")
        print("✅ Dashboard should be visible on http://localhost:8050")
        print("✅ All configurations correct")
    else:
        print("\n⚠️ ISSUES DETECTED!")
        if not backend_ok:
            print("🔧 Fix: Start backend with python main.py (in backendtest folder)")
        if not dashboard_ok:
            print("🔧 Fix: Start dashboard with python app.py (in dashboardtest folder)")
        if not config_ok:
            print("🔧 Fix: Update port configurations in files")
        if not integration_ok:
            print("🔧 Fix: Check backend endpoints and data formats")

if __name__ == "__main__":
    main()
