#!/usr/bin/env python3
"""
Test script to verify backend startup issues are resolved
"""
import sys
import os

# Add backend to path
backend_dir = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_dir)

print("Testing TA-Lib installation...")
try:
    import talib
    print("✅ TA-Lib is installed and working")
except ImportError as e:
    print(f"❌ TA-Lib import failed: {e}")

print("\nTesting backend imports...")
try:
    from data_collection import data_collector
    print("✅ data_collection imports successfully")
except Exception as e:
    print(f"❌ data_collection import failed: {e}")

try:
    from online_learning import online_learning_manager
    print("✅ online_learning imports successfully")
except Exception as e:
    print(f"❌ online_learning import failed: {e}")

try:
    import main
    print("✅ main module imports successfully")
except Exception as e:
    print(f"❌ main module import failed: {e}")

print("\nStarting backend test...")
try:
    import subprocess
    import time
    
    # Try to start the backend process
    backend_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "main:app",
        "--host", "127.0.0.1", "--port", "8001"
    ], cwd=backend_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
       universal_newlines=True)
    
    print("Backend process started, waiting 10 seconds...")
    time.sleep(10)
    
    if backend_process.poll() is None:
        print("✅ Backend is running successfully!")
        backend_process.terminate()
    else:
        print("❌ Backend process terminated early")
        stdout, stderr = backend_process.communicate()
        print(f"Output: {stdout}")
        
except Exception as e:
    print(f"❌ Backend test failed: {e}")

print("\nTest completed.")
