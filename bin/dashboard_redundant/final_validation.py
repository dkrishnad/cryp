#!/usr/bin/env python3
"""
Final validation test for dashboard components
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Add dashboard directory to path
dashboard_dir = os.path.dirname(os.path.abspath(__file__))
if dashboard_dir not in sys.path:
    sys.path.insert(0, dashboard_dir)

def test_dashboard_components():
    """Test all dashboard components are working"""
    print("=" * 60)
    print("🚀 DASHBOARD COMPONENT VALIDATION TEST")
    print("=" * 60)
    
    try:
        print("📦 Testing imports...")
        
        # Test dash app import
        from dash_app import app
        print("✅ dash_app.py imported successfully")
        
        # Test callbacks import
        import callbacks
        print("✅ callbacks.py imported successfully")
        
        # Test layout import
        from layout import layout
        print("✅ layout.py imported successfully")
        
        # Test layout assignment
        app.layout = layout
        print("✅ Layout assigned to app successfully")
        
        # Check callback registration
        callback_count = len(app.callback_map)
        print(f"✅ {callback_count} callbacks registered successfully")
        
        if callback_count == 0:
            print("⚠️ WARNING: No callbacks registered - this might be an issue")
            return False
        
        # Test that layout has critical components
        layout_str = str(layout)
        
        critical_components = [
            'price-chart',
            'indicators-chart', 
            'virtual-balance',
            'performance-monitor',
            'auto-trading-tab-content',
            'performance-interval',
            'balance-sync-interval'
        ]
        
        missing = []
        for component in critical_components:
            if component not in layout_str:
                missing.append(component)
        
        if missing:
            print(f"❌ Missing critical components: {missing}")
            return False
        else:
            print("✅ All critical components found in layout")
        
        print("\n" + "=" * 60)
        print("🎉 DASHBOARD VALIDATION SUCCESSFUL!")
        print("=" * 60)
        print("✅ All imports working")
        print(f"✅ {callback_count} callbacks registered")
        print("✅ All critical components present")
        print("✅ Dashboard is ready to run")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error during validation: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_backend_endpoints():
    """Test if we can connect to backend endpoints"""
    print("\n🔍 Testing backend connectivity...")
    
    try:
        import requests
        
        # Test health endpoint
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend health check passed")
            
            # Test a data endpoint
            response = requests.get("http://localhost:8000/features/indicators?symbol=btcusdt", timeout=5)
            if response.status_code == 200:
                print("✅ Backend data endpoints working")
                return True
            else:
                print(f"⚠️ Backend data endpoint returned: {response.status_code}")
                return False
        else:
            print(f"⚠️ Backend health check failed: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("⚠️ Backend not running or not accessible")
        return False
    except Exception as e:
        print(f"❌ Backend test error: {e}")
        return False

if __name__ == "__main__":
    dashboard_ok = test_dashboard_components()
    backend_ok = test_backend_endpoints()
    
    print("\n" + "=" * 60)
    print("📋 FINAL VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Dashboard Components: {'✅ PASS' if dashboard_ok else '❌ FAIL'}")
    print(f"Backend Connectivity: {'✅ PASS' if backend_ok else '⚠️ OFFLINE'}")
    
    if dashboard_ok:
        if backend_ok:
            print("\n🎉 FULL SYSTEM READY!")
            print("💡 Start with: python app.py")
        else:
            print("\n🎯 DASHBOARD READY!")
            print("💡 Start backend first, then: python app.py")
    else:
        print("\n❌ DASHBOARD NEEDS FIXES")
    
    print("=" * 60)
