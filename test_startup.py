#!/usr/bin/env python3
"""
Quick test script to check if main.py starts without Unicode errors
"""

import sys
import os
import subprocess
import time

# Add backend directory to path
backend_dir = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_dir)

print("[TEST] Testing main.py startup...")
print(f"[TEST] Backend directory: {backend_dir}")

try:
    # Try to import main.py directly
    print("[TEST] Attempting to import main.py...")
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Start the process and capture output
    proc = subprocess.Popen(
        [sys.executable, "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=backend_dir
    )
    
    # Give it a few seconds to start up
    time.sleep(5)
    
    # Check if process is still running
    if proc.poll() is None:
        print("[TEST] SUCCESS: Backend process is running!")
        print("[TEST] Attempting health check...")
        
        # Try to make a health check request
        try:
            import requests
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("[TEST] SUCCESS: Health check passed!")
                print(f"[TEST] Response: {response.json()}")
            else:
                print(f"[TEST] Health check returned status {response.status_code}")
        except Exception as e:
            print(f"[TEST] Health check failed: {e}")
        
        # Terminate the process
        proc.terminate()
        proc.wait()
        print("[TEST] Backend process terminated")
        
    else:
        # Process exited, check for errors
        stdout, stderr = proc.communicate()
        print(f"[TEST] FAILED: Process exited with code {proc.returncode}")
        if stdout:
            print(f"[TEST] STDOUT:\n{stdout}")
        if stderr:
            print(f"[TEST] STDERR:\n{stderr}")
    
except Exception as e:
    print(f"[TEST] ERROR: {e}")
    import traceback
    traceback.print_exc()

print("[TEST] Test completed")
