#!/usr/bin/env python3
"""
Manual backend test script to check startup
"""

import os
import sys
import subprocess
import time

# Change to backend directory
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
print(f"[TEST] Backend directory: {backend_dir}")

try:
    os.chdir(backend_dir)
    
    print("[TEST] Starting backend server manually...")
    
    # Run the backend with output capture
    result = subprocess.run(
        [sys.executable, "main.py"],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=backend_dir
    )
    
    print(f"[TEST] Process exited with code: {result.returncode}")
    if result.stdout:
        print(f"[TEST] STDOUT:\n{result.stdout}")
    if result.stderr:
        print(f"[TEST] STDERR:\n{result.stderr}")
        
except subprocess.TimeoutExpired:
    print("[TEST] Process running - timeout reached (this is good!)")
except Exception as e:
    print(f"[TEST] Error: {e}")

print("[TEST] Manual test completed")
