#!/usr/bin/env python3
"""
Dashboard Import Test
Tests if all import issues are resolved
"""
import sys
import os
import traceback

def test_dashboard_imports():
    """Test all dashboard imports"""
    print("🔍 Testing dashboard imports...")
    
    # Add dashboard to path
    dashboard_dir = os.path.join(os.getcwd(), "dashboard")
    if dashboard_dir not in sys.path:
        sys.path.insert(0, dashboard_dir)
    
    try:
        print("Testing app.py imports...")
        
        # Test importing layout
        from layout import layout
        print("✅ layout imported successfully")
        
        # Test importing dash_app
        from dash_app import app, server
        print("✅ dash_app imported successfully")
        
        # Test importing binance_exact_callbacks
        from binance_exact_callbacks import register_binance_exact_callbacks
        print("✅ binance_exact_callbacks imported successfully")
        
        # Test importing callbacks (this will test all the nested imports)
        print("Testing callbacks.py imports...")
        import callbacks
        print("✅ callbacks imported successfully")
        
        print("\n🎉 ALL DASHBOARD IMPORTS SUCCESSFUL!")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        print("Full traceback:")
        traceback.print_exc()
        return False

def test_dashboard_startup():
    """Test if dashboard can start without errors"""
    print("\n🔍 Testing dashboard startup simulation...")
    
    try:
        # Simulate the main app.py execution without actually running the server
        import sys
        import os
        
        # Add dashboard to path
        dashboard_dir = os.path.join(os.getcwd(), "dashboard")
        if dashboard_dir not in sys.path:
            sys.path.insert(0, dashboard_dir)
        
        # Import main components
        from layout import layout
        from dash_app import app, server
        from binance_exact_callbacks import register_binance_exact_callbacks
        
        # Import callbacks (this registers all callbacks)
        import callbacks
        
        # Register binance callbacks
        register_binance_exact_callbacks(app)
        
        # Set layout
        app.layout = layout
        
        print("✅ Dashboard startup simulation successful")
        return True
        
    except Exception as e:
        print(f"❌ Dashboard startup failed: {e}")
        traceback.print_exc()
        return False

def main():
    print("🧪 DASHBOARD IMPORT TEST")
    print("="*40)
    
    # Test imports
    import_success = test_dashboard_imports()
    
    # Test startup simulation
    startup_success = False
    if import_success:
        startup_success = test_dashboard_startup()
    
    print("\n📊 TEST RESULTS:")
    print(f"Import Test: {'✅ PASS' if import_success else '❌ FAIL'}")
    print(f"Startup Test: {'✅ PASS' if startup_success else '❌ FAIL'}")
    
    if import_success and startup_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Dashboard is ready to run")
        print("🚀 Start with: python dashboard/app.py")
        return True
    else:
        print("\n❌ Some tests failed")
        return False

if __name__ == "__main__":
    main()
