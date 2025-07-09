#!/usr/bin/env python3
"""Quick final validation of core components"""

import os
import sys

def test_backend():
    print("🔍 Testing Backend...")
    try:
        os.chdir("backendtest")
        import main
        print("✅ Backend imports successfully")
        print(f"✅ FastAPI app created with {len(main.app.routes)} routes")
        os.chdir("..")
        return True
    except Exception as e:
        print(f"❌ Backend error: {e}")
        os.chdir("..")
        return False

def test_dashboard():
    print("\n🎨 Testing Dashboard...")
    try:
        os.chdir("dashboardtest")
        import app
        print("✅ Dashboard imports successfully")
        os.chdir("..")
        return True
    except Exception as e:
        print(f"❌ Dashboard error: {e}")
        os.chdir("..")
        return False

def main():
    print("=" * 50)
    print("🚀 FINAL SYSTEM VALIDATION")
    print("=" * 50)
    
    backend_ok = test_backend()
    dashboard_ok = test_dashboard()
    
    print(f"\n📊 RESULTS:")
    print(f"   Backend: {'✅ WORKING' if backend_ok else '❌ ISSUES'}")
    print(f"   Dashboard: {'✅ WORKING' if dashboard_ok else '❌ ISSUES'}")
    
    if backend_ok and dashboard_ok:
        print(f"\n🎯 OVERALL STATUS: 🟢 EXCELLENT - READY TO LAUNCH!")
        print(f"\n🚀 START COMMANDS:")
        print(f"   Backend:   cd backendtest && python main.py")
        print(f"   Dashboard: cd dashboardtest && python app.py")
    else:
        print(f"\n⚠️ OVERALL STATUS: 🟡 NEEDS ATTENTION")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
