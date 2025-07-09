#!/usr/bin/env python3
"""
QUICK BACKEND STARTUP TEST
Test main.py startup directly
"""
import sys
import os
import subprocess
import time

def test_backend_startup():
    """Test backend startup with detailed output"""
    print("🔧 Testing Backend Startup...")
    
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    os.chdir(backend_dir)
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Test main.py startup
    print("🚀 Starting main.py...")
    try:
        process = subprocess.Popen([
            sys.executable, "main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        # Wait a few seconds to see if it starts
        print("⏳ Waiting 5 seconds for startup...")
        time.sleep(5)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Backend is running!")
            process.terminate()
            print("🛑 Stopped test process")
            return True
        else:
            print(f"❌ Backend stopped with exit code: {process.poll()}")
            # Get output
            stdout, stderr = process.communicate()
            print(f"📜 Output: {stdout}")
            return False
            
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return False

if __name__ == "__main__":
    success = test_backend_startup()
    if success:
        print("\n🎉 Backend startup test PASSED!")
        print("💡 You can now run START_CRYPTO_BOT.py")
    else:
        print("\n⚠️  Backend startup test FAILED")
        print("💡 Try running main_working.py instead")
