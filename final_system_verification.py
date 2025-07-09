#!/usr/bin/env python3
"""
Final system verification after all fixes
"""

import sys
import os
import traceback

def test_backend_startup():
    """Test if backend can start successfully"""
    print("🔍 Testing Backend Startup...")
    
    try:
        # Add backend to path
        sys.path.insert(0, "backendtest")
        
        # Test critical imports
        print("  📦 Testing database import...")
        from db import initialize_database, get_trades
        print("  ✅ Database import successful")
        
        print("  📦 Testing trading import...")
        from trading import open_virtual_trade
        print("  ✅ Trading import successful")
        
        print("  📦 Testing ML import...")
        from ml import real_predict
        print("  ✅ ML import successful")
        
        print("  📦 Testing WebSocket import...")
        from ws import router as ws_router
        print("  ✅ WebSocket import successful")
        
        print("  📦 Testing futures trading import...")
        from futures_trading import FuturesTradingEngine
        print("  ✅ Futures trading import successful")
        
        print("  📦 Testing advanced auto trading import...")
        from advanced_auto_trading import AdvancedAutoTradingEngine
        print("  ✅ Advanced auto trading import successful")
        
        print("  📦 Testing main FastAPI app import...")
        from main import app
        print("  ✅ FastAPI app import successful")
        
        print("🎉 BACKEND STARTUP TEST PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ BACKEND STARTUP TEST FAILED: {e}")
        traceback.print_exc()
        return False

def test_dashboard_imports():
    """Test if dashboard can import successfully"""
    print("\n🔍 Testing Dashboard Imports...")
    
    try:
        # Add dashboard to path
        sys.path.insert(0, "dashboardtest")
        
        print("  📦 Testing dash app import...")
        from dash_app import app
        print("  ✅ Dash app import successful")
        
        print("  📦 Testing layout import...")
        from layout import layout
        print("  ✅ Layout import successful")
        
        print("  📦 Testing utils import...")
        from utils import make_api_call
        print("  ✅ Utils import successful")
        
        print("🎉 DASHBOARD IMPORTS TEST PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ DASHBOARD IMPORTS TEST FAILED: {e}")
        traceback.print_exc()
        return False

def test_missing_dependencies():
    """Test for any remaining missing dependencies"""
    print("\n🔍 Testing Missing Dependencies...")
    
    try:
        # Test all major dependencies
        dependencies = [
            'fastapi', 'uvicorn', 'requests', 'pandas', 'numpy',
            'dash', 'plotly', 'httpx', 'websockets', 'talib', 'ta'
        ]
        
        for dep in dependencies:
            try:
                __import__(dep)
                print(f"  ✅ {dep} available")
            except ImportError:
                print(f"  ❌ {dep} missing")
                return False
        
        print("🎉 ALL DEPENDENCIES TEST PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ DEPENDENCIES TEST FAILED: {e}")
        return False

def main():
    """Run comprehensive system verification"""
    print("🚀 FINAL SYSTEM VERIFICATION")
    print("=" * 50)
    
    # Change to the correct directory
    os.chdir(r"c:\Users\Hari\Desktop\Testin dub")
    
    # Run all tests
    backend_ok = test_backend_startup()
    dashboard_ok = test_dashboard_imports() 
    deps_ok = test_missing_dependencies()
    
    print("\n" + "=" * 50)
    print("📋 FINAL RESULTS:")
    print(f"  Backend Startup: {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print(f"  Dashboard Imports: {'✅ PASS' if dashboard_ok else '❌ FAIL'}")
    print(f"  Dependencies: {'✅ PASS' if deps_ok else '❌ FAIL'}")
    
    if backend_ok and dashboard_ok and deps_ok:
        print("\n🎉 ALL TESTS PASSED - SYSTEM IS READY!")
        print("✅ Backend can start with: uvicorn main:app --host 0.0.0.0 --port 8000")
        print("✅ Dashboard can start from dashboardtest/ folder")
        print("✅ All imports and dependencies are working")
    else:
        print("\n⚠️  SOME TESTS FAILED - CHECK OUTPUT ABOVE")
    
    return backend_ok and dashboard_ok and deps_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
