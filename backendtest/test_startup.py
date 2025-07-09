#!/usr/bin/env python3
"""
Backend Startup Test
Quick test to verify backend starts without errors
"""

import sys
import os

# Add backend directory to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

def test_backend_startup():
    """Test if backend can be imported and started"""
    try:
        print("🚀 Testing backend startup...")
        
        # Test import of main module
        print("📦 Importing main module...")
        import main
        print("✅ Main module imported successfully")
        
        # Test app creation
        print("🔧 Checking FastAPI app...")
        app = main.app
        if app:
            print("✅ FastAPI app created successfully")
        else:
            print("❌ FastAPI app not found")
            return False
            
        # Test route inclusion
        print("🔗 Checking route inclusion...")
        routes = [str(route.path) for route in app.routes]
        print(f"📊 Found {len(routes)} routes")
        
        # Check for key endpoints
        key_endpoints = ["/account", "/positions", "/buy", "/sell", "/prices", "/market_data"]
        missing_endpoints = [endpoint for endpoint in key_endpoints if endpoint not in routes]
        
        if missing_endpoints:
            print(f"⚠️ Missing endpoints: {missing_endpoints}")
        else:
            print("✅ All key endpoints found")
            
        print("🎉 Backend startup test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Backend startup test failed: {e}")
        import traceback
        print(f"Error details: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    test_backend_startup()
