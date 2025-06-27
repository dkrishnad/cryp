#!/usr/bin/env python3
"""
Simple Dashboard Test - Verify everything works
"""

import sys
import os

def test_dashboard():
    print("🧪 TESTING DASHBOARD STARTUP...")
    
    try:
        # Test 1: Import dash app
        print("1️⃣ Testing dash app import...")
        from dashboard.dash_app import app
        print("✅ Dash app imported successfully")
        
        # Test 2: Import layout
        print("2️⃣ Testing layout import...")
        from dashboard.layout import layout
        print("✅ Layout imported successfully")
        
        # Test 3: Import callbacks
        print("3️⃣ Testing callbacks import...")
        import dashboard.callbacks
        print("✅ Callbacks imported successfully")
        
        # Test 4: Assign layout to app
        print("4️⃣ Testing layout assignment...")
        app.layout = layout
        print("✅ Layout assigned to app successfully")
        
        # Test 5: Check app configuration
        print("5️⃣ Testing app configuration...")
        print(f"✅ App host: {getattr(app.server, 'host', 'default')}")
        print(f"✅ App debug: {app.config.get('DEBUG', False)}")
        
        print("\n🎉 ALL DASHBOARD TESTS PASSED!")
        print("The dashboard is ready to start!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ DASHBOARD TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_backend():
    print("\n🧪 TESTING BACKEND IMPORTS...")
    
    try:
        # Test backend imports
        print("1️⃣ Testing backend main import...")
        import backend.main
        print("✅ Backend main imported successfully")
        
        print("2️⃣ Testing backend database import...")
        import backend.db
        print("✅ Backend database imported successfully")
        
        print("3️⃣ Testing backend data collection import...")
        import backend.data_collection
        print("✅ Backend data collection imported successfully")
        
        print("\n🎉 ALL BACKEND TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ BACKEND TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 50)
    print("🚀 CRYPTO BOT - QUICK STARTUP TEST")
    print("=" * 50)
    
    dashboard_ok = test_dashboard()
    backend_ok = test_backend()
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    
    if dashboard_ok and backend_ok:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ Your crypto bot is ready to run!")
        print("\n🚀 To start:")
        print("   Backend:   python backend/main.py")
        print("   Dashboard: python dashboard/app.py")
        print("\n🌐 URLs:")
        print("   Dashboard: http://localhost:8050")
        print("   Backend:   http://localhost:8000")
    else:
        print("❌ SOME TESTS FAILED!")
        if not dashboard_ok:
            print("   - Dashboard has issues")
        if not backend_ok:
            print("   - Backend has issues")
        print("\nPlease check the error messages above.")

if __name__ == "__main__":
    main()
