#!/usr/bin/env python3
"""
Final verification script to test if backend imports and starts properly
"""
import subprocess
import sys
import os

def test_backend_import():
    """Test if backend can be imported without errors"""
    print("🔄 Testing backend import...")
    
    try:
        result = subprocess.run([
            sys.executable, '-c', 
            '''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), "backend"))
sys.path.insert(0, os.getcwd())
try:
    import main
    print("SUCCESS: Backend imported without errors!")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
'''
        ], cwd=os.getcwd(), capture_output=True, text=True, timeout=30)
        
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if "SUCCESS" in result.stdout:
            print("✅ Backend imports successfully!")
            return True
        else:
            print("❌ Backend import failed")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Import test timed out (this might indicate a hanging import)")
        return False
    except Exception as e:
        print(f"❌ Error running import test: {e}")
        return False

def test_backend_startup():
    """Test if backend can start without immediate errors"""
    print("\n🔄 Testing backend startup...")
    
    try:
        # Start backend and check if it runs for a few seconds without crashing
        process = subprocess.Popen([
            sys.executable, 'backend/main.py'
        ], cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a bit to see if it starts successfully
        try:
            stdout, stderr = process.communicate(timeout=5)
            if process.returncode == 0:
                print("✅ Backend started and exited cleanly")
                return True
            else:
                print(f"❌ Backend exited with code {process.returncode}")
                if stderr:
                    print("STDERR:", stderr)
                return False
        except subprocess.TimeoutExpired:
            # If it's still running after 5 seconds, that's actually good for a server
            process.terminate()
            process.wait()
            print("✅ Backend started successfully (was running when terminated)")
            return True
            
    except Exception as e:
        print(f"❌ Error testing backend startup: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Backend Verification Test\n")
    
    # Test 1: Import
    import_success = test_backend_import()
    
    # Test 2: Startup (only if import succeeded)
    startup_success = False
    if import_success:
        startup_success = test_backend_startup()
    
    print("\n📊 Test Results:")
    print(f"Import Test: {'✅ PASS' if import_success else '❌ FAIL'}")
    print(f"Startup Test: {'✅ PASS' if startup_success else '❌ FAIL'}")
    
    if import_success and startup_success:
        print("\n🎉 All tests passed! Backend is working correctly.")
    elif import_success:
        print("\n⚠️  Import works but startup has issues. Check backend configuration.")
    else:
        print("\n❌ Backend has import issues. Please check the error messages above.")
