#!/usr/bin/env python3
"""
Test backend startup to verify missing endpoints router inclusion
"""
import sys
import os
import time
import subprocess
import requests
from datetime import datetime

def test_backend_startup():
    """Test if backend starts and missing endpoints are accessible"""
    print("🚀 TESTING BACKEND STARTUP WITH MISSING ENDPOINTS")
    print("=" * 60)
    
    # Change to backend directory
    os.chdir("backendtest")
    
    # Start backend server in background
    print("📡 Starting backend server...")
    try:
        # Start the server process
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a few seconds for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(8)
        
        # Test if server is running
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend server started successfully!")
                
                # Test missing endpoints
                missing_endpoints_to_test = [
                    "/backtest/results",
                    "/system/status", 
                    "/model/logs",
                    "/safety/check"
                ]
                
                print(f"\n🔍 TESTING {len(missing_endpoints_to_test)} MISSING ENDPOINTS:")
                success_count = 0
                
                for endpoint in missing_endpoints_to_test:
                    try:
                        resp = requests.get(f"http://localhost:8000{endpoint}", timeout=3)
                        if resp.status_code == 200:
                            print(f"   ✅ {endpoint} - WORKING (200)")
                            success_count += 1
                        else:
                            print(f"   ⚠️  {endpoint} - Status {resp.status_code}")
                    except Exception as e:
                        print(f"   ❌ {endpoint} - ERROR: {e}")
                
                print(f"\n📊 ENDPOINT TEST RESULTS:")
                print(f"   Working: {success_count}/{len(missing_endpoints_to_test)}")
                print(f"   Success Rate: {success_count/len(missing_endpoints_to_test)*100:.1f}%")
                
                if success_count == len(missing_endpoints_to_test):
                    print("   🎉 ALL MISSING ENDPOINTS ARE WORKING!")
                    return True
                else:
                    print("   ⚠️  Some endpoints not working")
                    return False
            else:
                print(f"❌ Backend health check failed: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Could not connect to backend: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False
    finally:
        # Stop the server
        if 'process' in locals():
            print("\n🛑 Stopping backend server...")
            process.terminate()
            time.sleep(2)
            if process.poll() is None:
                process.kill()
            print("✅ Backend server stopped")

def main():
    try:
        success = test_backend_startup()
        if success:
            print("\n🎉 SUCCESS: Missing endpoints are working correctly!")
        else:
            print("\n⚠️  PARTIAL SUCCESS: Some issues found")
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")

if __name__ == "__main__":
    main()
