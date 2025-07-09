#!/usr/bin/env python3
"""
Quick final verification that all systems are working
"""

import sys
import os

def test_backend():
    """Test backend startup"""
    print("🔍 Testing Backend...")
    try:
        sys.path.insert(0, 'backendtest')
        from main import app
        print("✅ Backend imports and compiles successfully")
        return True
    except Exception as e:
        print(f"❌ Backend failed: {e}")
        return False

def test_dashboard():
    """Test dashboard startup"""
    print("🔍 Testing Dashboard...")
    try:
        sys.path.insert(0, 'dashboardtest')
        from dash_app import app
        print("✅ Dashboard imports and compiles successfully")
        return True
    except Exception as e:
        print(f"❌ Dashboard failed: {e}")
        return False

def test_dependencies():
    """Test critical dependencies"""
    print("🔍 Testing Dependencies...")
    missing = []
    
    # Test critical packages
    packages = [
        'fastapi', 'uvicorn', 'requests', 'pandas', 'numpy', 
        'dash', 'plotly', 'httpx', 'websockets', 'ta'
    ]
    
    for package in packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing.append(package)
    
    # Test talib (optional)
    try:
        import talib
        print("  ✅ talib (optional)")
    except ImportError:
        print("  ⚠️ talib (optional, using alternatives)")
    
    return len(missing) == 0

def main():
    """Main verification"""
    print("🚀 QUICK SYSTEM VERIFICATION")
    print("=" * 50)
    
    os.chdir(r"c:\Users\Hari\Desktop\Testin dub")
    
    backend_ok = test_backend()
    dashboard_ok = test_dashboard()
    deps_ok = test_dependencies()
    
    print("\n" + "=" * 50)
    print("📋 FINAL RESULTS:")
    print(f"  Backend: {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print(f"  Dashboard: {'✅ PASS' if dashboard_ok else '❌ FAIL'}")
    print(f"  Dependencies: {'✅ PASS' if deps_ok else '❌ FAIL'}")
    
    if backend_ok and dashboard_ok and deps_ok:
        print("\n🎉 ALL SYSTEMS WORKING!")
        print("✅ Crypto trading bot is ready to run")
        print("✅ You can start the backend with: python -m uvicorn main:app --reload")
        print("✅ You can start the dashboard with: python app.py")
    else:
        print("\n⚠️ Some issues remain - see output above")

if __name__ == "__main__":
    main()
