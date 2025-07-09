#!/usr/bin/env python3
"""
Test missing endpoints router registration without starting server
"""
import sys
import os

def test_router_registration():
    """Test if missing endpoints router can be created and registered"""
    print("🔍 TESTING MISSING ENDPOINTS ROUTER REGISTRATION")
    print("=" * 60)
    
    try:
        # Change to backend directory
        os.chdir("backendtest")
        
        # Test import of missing endpoints
        print("📦 Testing missing endpoints import...")
        from missing_endpoints import get_missing_endpoints_router
        print("✅ Successfully imported get_missing_endpoints_router")
        
        # Create router
        print("🔧 Creating missing endpoints router...")
        router = get_missing_endpoints_router()
        print(f"✅ Router created with {len(router.routes)} routes")
        
        # List the routes
        print(f"\n📋 ROUTES IN MISSING ENDPOINTS ROUTER:")
        route_paths = []
        for route in router.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                methods = list(route.methods) if route.methods else ['GET']
                print(f"   {methods[0]:>6} {route.path}")
                route_paths.append(route.path)
        
        # Check if target endpoints are present
        target_missing = {
            "/backtest",
            "/backtest/results", 
            "/model/errors",
            "/model/logs",
            "/model/predict_batch",
            "/model/upload_and_retrain",
            "/safety/check",
            "/system/status",
            "/trades/analytics"
        }
        
        print(f"\n✅ TARGET ENDPOINTS CHECK:")
        found_count = 0
        for endpoint in target_missing:
            if endpoint in route_paths:
                print(f"   ✅ {endpoint}")
                found_count += 1
            else:
                print(f"   ❌ {endpoint}")
        
        print(f"\n📊 SUMMARY:")
        print(f"   Found: {found_count}/{len(target_missing)} endpoints")
        print(f"   Coverage: {found_count/len(target_missing)*100:.1f}%")
        
        if found_count == len(target_missing):
            print("   🎉 ALL TARGET ENDPOINTS FOUND IN ROUTER!")
            return True
        else:
            print("   ⚠️  Some endpoints missing from router")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_fastapi_registration():
    """Test if the router can be registered with FastAPI"""
    print("\n🚀 TESTING FASTAPI REGISTRATION")
    print("=" * 40)
    
    try:
        from fastapi import FastAPI
        from missing_endpoints import get_missing_endpoints_router
        
        # Create test app
        app = FastAPI()
        
        # Include the router
        missing_router = get_missing_endpoints_router()
        app.include_router(missing_router, prefix="", tags=["Missing Endpoints"])
        
        print("✅ Successfully registered missing endpoints router with FastAPI")
        
        # Count total routes in app
        total_routes = len(app.routes)
        print(f"✅ FastAPI app now has {total_routes} total routes")
        
        return True
        
    except Exception as e:
        print(f"❌ FastAPI registration error: {e}")
        return False

def main():
    success1 = test_router_registration()
    success2 = test_fastapi_registration()
    
    if success1 and success2:
        print("\n🎉 ALL TESTS PASSED! Missing endpoints router is working correctly.")
        print("✅ The endpoints should now be available when the backend starts.")
    else:
        print("\n⚠️  SOME TESTS FAILED. Check the errors above.")

if __name__ == "__main__":
    main()
