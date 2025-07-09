#!/usr/bin/env python3
"""
Quick Backend Endpoint Verification
Tests what endpoints are actually available in the backend
"""
import requests
import subprocess
import sys
import time
import os

def test_backend_endpoints():
    """Test if backend endpoints are actually working"""
    
    # Start backend
    print("🔧 Starting backend server...")
    backend_script = os.path.join('backendtest', 'app.py')
    backend_process = subprocess.Popen(
        [sys.executable, backend_script],
        cwd=os.path.dirname(__file__),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for backend to start
    time.sleep(3)
    
    # Test endpoints
    base_url = "http://localhost:5000"
    
    # Test basic endpoints
    test_endpoints = [
        "/",
        "/docs",
        "/api/status", 
        "/data/symbol_data",
        "/portfolio/balance",
        "/data/live_prices",
        "/trade",
        "/notifications",
        "/model/predict",
        "/futures/open_position",
        "/auto_trading/status"
    ]
    
    print(f"\n🔍 Testing endpoints on {base_url}:")
    print("=" * 50)
    
    working_endpoints = []
    missing_endpoints = []
    
    for endpoint in test_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=2)
            if response.status_code == 200:
                print(f"✅ {endpoint} - OK")
                working_endpoints.append(endpoint)
            elif response.status_code == 404:
                print(f"❌ {endpoint} - NOT FOUND")
                missing_endpoints.append(endpoint)
            else:
                print(f"⚠️  {endpoint} - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} - ERROR: {str(e)[:50]}")
            missing_endpoints.append(endpoint)
    
    print("\n📊 SUMMARY:")
    print(f"✅ Working endpoints: {len(working_endpoints)}")
    print(f"❌ Missing endpoints: {len(missing_endpoints)}")
    
    if missing_endpoints:
        print("\n❌ Missing endpoints:")
        for endpoint in missing_endpoints:
            print(f"  - {endpoint}")
    
    # Try to get all available endpoints from docs
    try:
        response = requests.get(f"{base_url}/openapi.json", timeout=2)
        if response.status_code == 200:
            openapi_data = response.json()
            all_paths = list(openapi_data.get('paths', {}).keys())
            print(f"\n📄 Total available endpoints from OpenAPI: {len(all_paths)}")
            print("Available endpoints:")
            for path in sorted(all_paths)[:20]:  # Show first 20
                print(f"  - {path}")
            if len(all_paths) > 20:
                print(f"  ... and {len(all_paths) - 20} more")
    except Exception as e:
        print(f"❌ Could not fetch OpenAPI schema: {e}")
    
    # Cleanup
    backend_process.terminate()
    
    return len(working_endpoints) > 0

if __name__ == "__main__":
    success = test_backend_endpoints()
    if success:
        print("\n✅ Backend is working with some endpoints")
    else:
        print("\n❌ Backend has major issues")
